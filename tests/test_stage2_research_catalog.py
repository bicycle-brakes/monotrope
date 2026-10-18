"""Research preflight contracts: real pinned Pi, local sources, no model calls.

The planned graph is not an execution result. Dispatcher/barrier/handoff
qualification remains separate from these catalog and seat-plan checks.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import stage2_swarm as swarm  # noqa: E402

GO = "opencode-go"
FIXED = ["deepseek-v4.1-flash", "mimo-v2.6-flash", "qwen3.8-flash"]
PIN = json.loads((ROOT / "tools/pi/package.json").read_text())["dependencies"]["@earendil-works/pi-coding-agent"]
POLICY = {"provider": GO, "suffix": "-free", "include": [], "exclude": []}
BRIDGE = ROOT / "scripts/stage2_research_catalog.mjs"


def model(ident: str, **changes) -> dict:
    return {
        "id": ident,
        "name": ident,
        "provider": GO,
        "api": "openai-completions",
        "baseUrl": "https://opencode.ai/zen/go/v1",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 4096,
        **changes,
    }


def capability(ident: str, **changes) -> dict:
    return {"id": ident, "tool_call": True, **changes}


class Sources:
    def __init__(self) -> None:
        self.pi_models = [model(ident) for ident in FIXED] + [model("alpha-free"), model("beta-free")]
        self.metadata = {GO: {"models": {ident: capability(ident) for ident in ("alpha-free", "beta-free")}}}
        self.pi_body: str | None = None
        self.metadata_body: str | None = None
        self.pi_status = self.metadata_status = 200
        self.pi_delay = self.metadata_delay = 0.0
        self.requests: list[tuple[str, dict]] = []


@pytest.fixture
def sources():
    state = Sources()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def do_GET(self):  # noqa: N802 - stdlib callback
            path = self.path.split("?", 1)[0]
            state.requests.append((self.path, dict(self.headers)))
            if path == f"/api/models/providers/{GO}":
                body = state.pi_body if state.pi_body is not None else json.dumps(state.pi_models)
                status, delay = state.pi_status, state.pi_delay
            elif path == "/metadata":
                body = state.metadata_body if state.metadata_body is not None else json.dumps(state.metadata)
                status, delay = state.metadata_status, state.metadata_delay
            else:
                body, status, delay = "unexpected endpoint", 404, 0
            time.sleep(delay)
            encoded = body.encode()
            try:
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
            except (BrokenPipeError, ConnectionResetError):
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.02), daemon=True)
    thread.start()
    state.url = f"http://127.0.0.1:{server.server_port}"
    yield state
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)


def collect(tmp_path: Path, sources: Sources, **options) -> dict:
    """The actual pinned runtime; executable/auth-read traps surround it."""
    script = r"""
import fs from 'node:fs';
import child from 'node:child_process';
import { syncBuiltinESMExports } from 'node:module';
let commands = 0, credentialReads = 0;
for (const name of ['exec', 'execSync', 'execFile', 'execFileSync', 'spawn', 'spawnSync', 'fork']) {
  child[name] = () => { commands++; throw new Error('subprocess forbidden in catalog preflight'); };
}
const read = fs.readFileSync;
fs.readFileSync = function(path, ...args) {
  if (String(path).endsWith('/auth.json')) { credentialReads++; throw new Error('credential read forbidden'); }
  return read.call(this, path, ...args);
};
syncBuiltinESMExports();
const { collectCatalog } = await import(process.argv[1]);
const result = await collectCatalog(JSON.parse(process.argv[2]));
result.test_guard = { commands, credentialReads };
console.log(JSON.stringify(result));
"""
    environment = {key: value for key, value in os.environ.items() if key in {"PATH", "LANG", "LC_ALL", "LC_CTYPE"}}
    environment.update(HOME=str(tmp_path), PI_CODING_AGENT_DIR=str(tmp_path), PI_OFFLINE="1")
    done = subprocess.run(
        [
            "node",
            "--input-type=module",
            "-e",
            script,
            BRIDGE.as_uri(),
            json.dumps({"catalogBaseUrl": sources.url, "metadataUrl": sources.url + "/metadata", **options}),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert done.returncode == 0, done.stderr
    result = json.loads(done.stdout)
    assert result["test_guard"] == {"commands": 0, "credentialReads": 0}
    assert all("authorization" not in {key.lower() for key in headers} for _, headers in sources.requests)
    return result


def select(bridge: dict, policy: dict | None = None, ids: list[str] | None = None) -> dict:
    return swarm.select_research_catalog(
        bridge, POLICY if policy is None else policy, FIXED if ids is None else ids, expected_version=PIN
    )


def test_preflight_uses_fresh_pinned_go_snapshot_without_cache_date(tmp_path, sources):
    bridge = collect(tmp_path, sources)
    result = select(bridge)
    assert bridge["pi_version"] == PIN
    assert result["selected"] == ["alpha-free", "beta-free"]
    assert result["fixed"] == FIXED
    assert result["models_store"][GO]["lastModified"] == 0, "no server date was fabricated"
    assert len([path for path, _ in sources.requests if path.startswith("/api/models/providers/")]) == 1
    assert len(sources.requests) == 2
    for name in ("pi", "models_dev"):
        evidence = result["sources"][name]
        assert evidence["retrieved_at"].endswith("Z")
        assert len(evidence["sha256"]) == 64
        assert "body" not in evidence, "the durable audit needs digests, not whole source documents"
    raw = bridge["sources"]["pi"]["body"]
    assert result["sources"]["pi"]["sha256"] == hashlib.sha256(raw.encode()).hexdigest()


def test_preflight_refreshes_despite_fresh_store_and_never_revives_cached_ids(tmp_path, sources):
    seed = {GO: {"models": [model("cached-free")], "checkedAt": int(time.time() * 1000), "lastModified": 4102444800000}}
    bridge = collect(tmp_path, sources, seedStore=seed)
    assert select(bridge)["selected"] == ["alpha-free", "beta-free"]
    assert "cached-free" not in {entry["id"] for entry in bridge["models_store"][GO]["models"]}
    assert len([path for path, _ in sources.requests if path.startswith("/api/models/")]) == 1


@pytest.mark.parametrize(
    "change,reason",
    [
        ({"tool_call": False}, "no-tool-support"),
        ({"tool_call": "true"}, "metadata-malformed"),
        ({"tool_call": None}, "metadata-malformed"),
        ({"tool_call": 1}, "metadata-malformed"),
        ({"status": "deprecated"}, "deprecated"),
        ({"status": None}, "metadata-malformed"),
        ({"id": "different-free"}, "metadata-malformed"),
    ],
)
def test_preflight_candidate_fault_does_not_exclude_a_valid_peer(tmp_path, sources, change, reason):
    sources.metadata[GO]["models"]["alpha-free"].update(change)
    result = select(collect(tmp_path, sources))
    assert result["selected"] == ["beta-free"]
    excluded = next(item for item in result["candidates"] if item["id"] == "alpha-free")
    assert excluded["reason"] == reason
    assert excluded["evidence"], "excluded values remain auditable beside nonempty selection"


@pytest.mark.parametrize("field,reason", [("id", "metadata-malformed"), ("tool_call", "no-tool-support")])
def test_preflight_missing_metadata_field_is_local_and_explicit(tmp_path, sources, field, reason):
    del sources.metadata[GO]["models"]["alpha-free"][field]
    result = select(collect(tmp_path, sources))
    assert result["selected"] == ["beta-free"]
    candidate = next(item for item in result["candidates"] if item["id"] == "alpha-free")
    assert candidate["reason"] == reason
    assert candidate["evidence"][field] == {"present": False}


@pytest.mark.parametrize(
    "body", ["[]", "null", "{broken", "{}", '{"opencode-go":null}', '{"opencode-go":{"models":[]}}']
)
def test_preflight_unavailable_capabilities_preserve_fixed_model_eligibility(tmp_path, sources, body):
    sources.metadata_body = body
    result = select(collect(tmp_path, sources))
    assert result["selected"] == []
    assert result["fixed"] == FIXED
    assert result["capability_status"] == "capability-unavailable"
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(collect(tmp_path, sources), {**POLICY, "include": ["alpha-free"], "exclude": ["alpha-free"]})
    assert failure.value.exit_code == 1
    assert "alpha-free" in str(failure.value)


@pytest.mark.parametrize(
    "body",
    [
        '{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":false},"alpha-free":{"id":"alpha-free","tool_call":true}}}}',
        '{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"beta-free":{"id":"alpha-free","tool_call":true}}}}',
    ],
)
def test_preflight_duplicate_metadata_identity_disables_all_free_candidates(tmp_path, sources, body):
    sources.metadata_body = body
    result = select(collect(tmp_path, sources))
    assert result["selected"] == []
    assert result["capability_status"] == "capability-unavailable"
    assert result["capability_reason"] == "duplicate-id"
    assert result["fixed"] == FIXED


def test_preflight_ignores_unrelated_provider_and_never_adds_metadata_only_ids(tmp_path, sources):
    sources.metadata["unrelated"] = {"models": 5}
    sources.metadata[GO]["models"]["metadata-only-free"] = capability("metadata-only-free")
    result = select(collect(tmp_path, sources))
    assert result["selected"] == ["alpha-free", "beta-free"]


@pytest.mark.parametrize("change", [{"input": "text"}, {"input": None}, {"type": None}, {"type": "unknown"}])
def test_preflight_malformed_pi_candidate_is_local(tmp_path, sources, change):
    sources.pi_models[3].update(change)
    result = select(collect(tmp_path, sources))
    assert result["selected"] == ["beta-free"]
    assert next(item for item in result["candidates"] if item["id"] == "alpha-free")["reason"] == "pi-malformed"


def outcome(result: dict, ident: str) -> dict:
    return next(item for item in result["models"] if item["id"] == ident)


def test_preflight_duplicate_pi_identity_is_still_a_hard_failure(tmp_path, sources):
    sources.pi_models.append(copy.deepcopy(sources.pi_models[3]))
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(collect(tmp_path, sources))
    assert failure.value.exit_code == 1
    assert "duplicate" in str(failure.value)


@pytest.mark.parametrize(
    "fault,reason",
    [
        ("missing", "not-in-fresh-pi"),
        ("input", "pi-malformed"),
        ("not-chat", "not-chat"),
        ("other-wire-api", "wire-api-not-measured"),
    ],
)
def test_preflight_missing_or_non_chat_seat_candidate_is_skipped(tmp_path, sources, fault, reason):
    if fault == "missing":
        sources.pi_models = [item for item in sources.pi_models if item["id"] != FIXED[2]]
    elif fault == "input":
        sources.pi_models[2]["input"] = "text"
    elif fault == "not-chat":
        sources.pi_models[2]["type"] = "image"
    else:
        sources.pi_models[2]["api"] = "anthropic-messages"
    bridge = collect(tmp_path, sources)
    result = select(bridge)
    skipped = outcome(result, FIXED[2])
    if fault == "missing":
        # The pinned install may still ship the id: then it is baseline-only, never a fresh entry.
        reason = "baseline-only" if FIXED[2] in bridge["baseline"] else "not-in-fresh-pi"
    assert skipped["reason"] == reason
    assert skipped["evidence"], "the raw value behind the skip is not kept"
    assert result["selected"] == ["alpha-free", "beta-free"], "one seat candidate failed the whole preflight"
    assert outcome(result, FIXED[0])["reason"] is None and outcome(result, FIXED[1])["reason"] is None


def test_go_seat_candidates_require_fresh_text_chat_entries(tmp_path, sources):
    sources.pi_models.append(model("paid-extra"))
    for ident in [*FIXED, "paid-extra"]:
        sources.metadata[GO]["models"][ident] = capability(ident)
    bridge = collect(tmp_path, sources)
    bridge["baseline"] = [*bridge["baseline"], "baseline-only-id"]
    result = select(bridge, ids=[*FIXED, "baseline-only-id", "absent-id"])
    assert outcome(result, "baseline-only-id")["reason"] == "baseline-only"
    assert outcome(result, "absent-id")["reason"] == "not-in-fresh-pi"
    assert outcome(result, "paid-extra")["reason"] is None, "a fresh paid overlay model is not classified"
    # models.dev never decides a seat's preferred model, only the substitute pool.
    sources.metadata[GO]["models"][FIXED[0]]["tool_call"] = False
    result = select(collect(tmp_path, sources))
    assert outcome(result, FIXED[0])["reason"] is None
    assert outcome(result, FIXED[0])["tool_support"] == "no-tool-support"
    assert outcome(result, FIXED[1])["tool_support"] is None


@pytest.mark.parametrize(
    "body,reason",
    [("[]", "capability-unavailable"), ("{broken", "capability-unavailable")],
)
def test_preflight_pool_candidates_need_models_dev_tool_support(tmp_path, sources, body, reason):
    sources.metadata_body = body
    result = select(collect(tmp_path, sources))
    assert outcome(result, FIXED[0])["reason"] is None
    assert outcome(result, FIXED[0])["tool_support"] == reason


def test_pi_overlay_duplicates_block_but_malformed_candidates_are_local(tmp_path, sources):
    sources.pi_models[1]["input"] = None
    result = select(collect(tmp_path, sources))
    assert outcome(result, FIXED[1])["reason"] == "pi-malformed"
    assert outcome(result, FIXED[0])["reason"] is None
    sources.pi_models.append(copy.deepcopy(sources.pi_models[0]))
    with pytest.raises(swarm.ResearchCatalogError, match="duplicate"):
        select(collect(tmp_path, sources))


@pytest.mark.parametrize("status", [304, 404, 429, 500])
def test_preflight_unsuccessful_pi_response_is_not_measured_empty_or_retried(tmp_path, sources, status):
    sources.pi_status = status
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(collect(tmp_path, sources))
    assert failure.value.exit_code == 1
    assert len([path for path, _ in sources.requests if path.startswith("/api/models/")]) == 1


@pytest.mark.parametrize("slow", ["pi", "metadata"])
def test_preflight_shared_deadline_has_asymmetric_failure_rules(tmp_path, sources, slow):
    setattr(sources, slow + "_delay", 2.5)
    started = time.monotonic()
    bridge = collect(tmp_path, sources, deadlineMs=1200)
    assert time.monotonic() - started < 3, "the two reads did not share one deadline"
    if slow == "pi":
        with pytest.raises(swarm.ResearchCatalogError) as failure:
            select(bridge)
        assert failure.value.exit_code == 1
    else:
        result = select(bridge)
        assert result["fixed"] == FIXED
        assert result["selected"] == []
        assert result["capability_reason"] == "timeout"


@pytest.mark.parametrize(
    "policy",
    [
        {**POLICY, "provider": "opencode"},
        {**POLICY, "include": ["paid"]},
        {**POLICY, "exclude": ["alpha-free", "alpha-free"]},
        {**POLICY, "suffix": ""},
        {**POLICY, "include": None},
        {**POLICY, "typo": []},
    ],
)
def test_preflight_invalid_policy_is_a_declaration_refusal(policy):
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        swarm.validate_research_free_policy(policy)
    assert failure.value.exit_code == 2


def roles() -> dict:
    repo = [{"endpoint": GO, "model": ident} for ident in FIXED[:2]] + [
        {"endpoint": "claude-code-plan", "model": "claude-haiku-5-5"}
    ]
    opus = {"endpoint": "claude-code-plan", "model": "claude-opus-5-5", "effort": "xhigh"}
    return {
        "repository_agents": repo,
        "finder_agents": copy.deepcopy(repo),
        "online_agents": [{"endpoint": GO, "model": ident} for ident in FIXED],
        "finder_merge": opus,
        "topic_author": {**opus, "effort": "high"},
        "judge": opus,
    }


@pytest.mark.parametrize("selected", [[], ["alpha-free"], ["alpha-free", "beta-free"]])
def test_preflight_planned_graph_preserves_required_roles_and_public_only_free_seats(selected):
    graph = swarm.research_slot_plan(roles(), selected)
    assert len(graph) == 39 + 3 * len(selected)
    assert len([slot for slot in graph if slot["required"]]) == 39
    assert len({slot["id"] for slot in graph}) == len(graph)
    assert [slot["stage"] for slot in graph[:5]] == ["finders"] * 3 + ["merge", "sentence"]
    assert graph[-1]["stage"] == "judge"
    for topic in range(1, 12):
        peers = [slot for slot in graph if slot["topic"] == topic]
        assert len(peers) == (3 if topic <= 8 else 3 + len(selected))
    for slot in graph:
        if slot["model"] in selected:
            assert slot["stage"] == "topics" and slot["topic"] in (9, 10, 11)
            assert slot["endpoint"] == GO and not slot["required"]
    topic_slots = [slot for slot in graph if slot["stage"] == "topics"]
    first_free = next((i for i, slot in enumerate(topic_slots) if not slot["required"]), len(topic_slots))
    assert all(slot["required"] for slot in topic_slots[:first_free])
    assert not any(slot["required"] for slot in topic_slots[first_free:])


@pytest.mark.parametrize(
    "body",
    [
        '[{"id":"alpha-free","id":"beta-free"}]',
        '{"one":{"id":"alpha-free"},"two":{"id":"alpha-free"}}',
    ],
)
def test_preflight_rejects_raw_pi_duplicate_identity_before_selection(tmp_path, sources, body):
    sources.pi_body = body
    with pytest.raises(swarm.ResearchCatalogError, match="duplicate"):
        select(collect(tmp_path, sources))


@pytest.mark.parametrize("status", [404, 429, 500])
def test_preflight_metadata_http_failure_keeps_fixed_slots(tmp_path, sources, status):
    sources.metadata_status = status
    result = select(collect(tmp_path, sources))
    assert result["selected"] == []
    assert result["fixed"] == FIXED
    assert result["capability_reason"] == "http-error"


def test_preflight_include_is_checked_before_exclude_and_both_are_audited(tmp_path, sources):
    bridge = collect(tmp_path, sources)
    result = select(bridge, {**POLICY, "include": ["alpha-free"], "exclude": ["alpha-free"]})
    assert result["selected"] == []
    assert result["capability_status"] == "available"
    reasons = {item["id"]: item["reason"] for item in result["candidates"]}
    assert reasons["alpha-free"] == "excluded"
    assert reasons["beta-free"] == "not-included"
    with pytest.raises(swarm.ResearchCatalogError, match="absent-free"):
        select(bridge, {**POLICY, "include": ["absent-free"], "exclude": ["absent-free"]})


def test_preflight_pi_fault_retains_missing_and_raw_field_evidence(tmp_path, sources):
    sources.pi_models[3]["input"] = "text"
    result = select(collect(tmp_path, sources))
    item = next(item for item in result["candidates"] if item["id"] == "alpha-free")
    assert item["evidence"]["pi"]["input"] == {"present": True, "value": "text"}
    assert item["evidence"]["pi"]["type"] == {"present": False}


def test_preflight_metadata_missing_entry_is_not_eligible(tmp_path, sources):
    del sources.metadata[GO]["models"]["alpha-free"]
    result = select(collect(tmp_path, sources))
    assert result["selected"] == ["beta-free"]
    assert next(item for item in result["candidates"] if item["id"] == "alpha-free")["reason"] == "metadata-missing"


def test_preflight_unrelated_provider_duplicate_keys_do_not_disable_go(tmp_path, sources):
    sources.metadata_body = json.dumps(sources.metadata)[:-1] + ',"unrelated":{"models":{"x":1,"x":2}}}'
    assert select(collect(tmp_path, sources))["selected"] == ["alpha-free", "beta-free"]


@pytest.mark.parametrize("fault", ["missing-seat", "free-private", "missing-identity"])
def test_preflight_graph_refuses_invalid_required_role_shape(fault):
    declaration = roles()
    if fault == "missing-seat":
        declaration["finder_agents"].pop()
    elif fault == "free-private":
        declaration["repository_agents"][0]["model"] = "alpha-free"
    else:
        declaration["judge"].pop("endpoint")
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        swarm.research_slot_plan(declaration, [])
    assert failure.value.exit_code == 2


def test_preflight_zero_selection_retains_policy_and_measured_outcome(tmp_path, sources):
    sources.pi_models = [model(ident) for ident in FIXED]
    result = select(collect(tmp_path, sources))
    assert result["N"] == 0
    assert result["selection_outcome"] == "measured-empty"
    assert result["policy"] == POLICY
    assert result["raw_pi_ids"] == sorted(FIXED)


@pytest.mark.parametrize(
    "body",
    [
        '{"unrelated":1,"unrelated":2,"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"beta-free":{"id":"beta-free","tool_call":true}}}}',
        '{"opencode-go":{"unrelated":1,"unrelated":2,"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"beta-free":{"id":"beta-free","tool_call":true}}}}',
    ],
)
def test_preflight_duplicate_unrelated_metadata_fields_do_not_disable_go(tmp_path, sources, body):
    sources.metadata_body = body
    assert select(collect(tmp_path, sources))["selected"] == ["alpha-free", "beta-free"]


def test_preflight_non_model_pi_entries_are_not_candidate_faults(tmp_path, sources):
    sources.pi_models.extend([{"name": "not-a-model", "input": 0}, model("unrelated-paid", input=None, type="unknown")])
    assert select(collect(tmp_path, sources))["selected"] == ["alpha-free", "beta-free"]


def test_preflight_non_object_capability_keeps_raw_value_evidence(tmp_path, sources):
    sources.metadata[GO]["models"]["alpha-free"] = 5
    result = select(collect(tmp_path, sources))
    assert result["selected"] == ["beta-free"]
    candidate = next(item for item in result["candidates"] if item["id"] == "alpha-free")
    assert candidate["reason"] == "metadata-malformed"
    assert candidate["evidence"]["entry"] == {"present": True, "value": 5}


@pytest.mark.parametrize("field", ["id", "tool_call"])
def test_preflight_raw_duplicate_keys_inside_models_are_document_ambiguity(tmp_path, sources, field):
    entry = '"id":"alpha-free","tool_call":true,' + ('"id":"alpha-free"' if field == "id" else '"tool_call":true')
    sources.metadata_body = (
        '{"opencode-go":{"models":{"alpha-free":{' + entry + '},"beta-free":{"id":"beta-free","tool_call":true}}}}'
    )
    result = select(collect(tmp_path, sources))
    assert result["selected"] == []
    assert result["fixed"] == FIXED
    assert result["capability_reason"] == "duplicate-id"


@pytest.mark.parametrize(
    "change",
    [
        {"provider": "opencode"},
        {"baseUrl": "https://example.invalid/zen/go/v1"},
        {"baseUrl": "https://opencode.ai@other.invalid/zen/go/v1"},
        {"baseUrl": "http://opencode.ai/zen/go/v1"},
    ],
)
def test_preflight_free_definition_cannot_redirect_its_declared_go_origin(tmp_path, sources, change):
    sources.pi_models[3].update(change)
    result = select(collect(tmp_path, sources))
    assert result["selected"] == ["beta-free"]
    item = next(item for item in result["candidates"] if item["id"] == "alpha-free")
    assert item["reason"] == "pi-malformed"
    for field, value in change.items():
        assert item["evidence"]["pi"][field] == {"present": True, "value": value}


@pytest.mark.parametrize(
    "change",
    [
        {"provider": "opencode"},
        {"baseUrl": "https://example.invalid/api"},
        {"baseUrl": "https://opencode.ai@other.invalid/zen/go/v1"},
    ],
)
def test_preflight_seat_candidate_definition_cannot_redirect_its_go_origin(tmp_path, sources, change):
    sources.pi_models[0].update(change)
    result = select(collect(tmp_path, sources))
    skipped = outcome(result, FIXED[0])
    assert skipped["reason"] == "pi-malformed"
    for field, value in change.items():
        assert skipped["evidence"]["pi"][field] == {"present": True, "value": value}
    assert outcome(result, FIXED[1])["reason"] is None
