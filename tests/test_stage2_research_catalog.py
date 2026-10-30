"""Research preflight contracts: real pinned Pi, local sources, no model calls.

The planned graph is not an execution result. Dispatcher/barrier/handoff
qualification remains separate from these catalog and seat-plan checks.
"""

from __future__ import annotations

import contextlib
import copy
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import stage2_swarm as swarm  # noqa: E402

GO = "opencode-go"
FIXED = ["deepseek-v4.1-flash", "mimo-v2.6-pro", "qwen3.8-flash"]
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


def held_name(path: str) -> str | None:
    """The held-set name of a request; the versioned hop is held apart from the initial request."""
    base = path.split("?", 1)[0]
    if base == f"/api/models/providers/{GO}":
        return "pi-hop" if "pi-version=" in path else "pi"
    return "metadata" if base == "/metadata" else None


class Sources:
    def __init__(self) -> None:
        self.pi_models = [model(ident) for ident in FIXED] + [model("alpha-free"), model("beta-free")]
        self.metadata = {GO: {"models": {ident: capability(ident) for ident in ("alpha-free", "beta-free")}}}
        self.pi_body: str | None = None
        self.metadata_body: str | None = None
        self.pi_status = self.metadata_status = 200
        self.pi_delay = self.metadata_delay = 0.0
        self.requests: list[tuple[str, dict]] = []
        self.events: list[tuple[str, str]] = []
        self.overlap: threading.Barrier | None = None
        self.stop = threading.Event()
        # Held sources answer only at teardown; `held_marker` is written once every held request has arrived
        # (bead coding-harness-jik: deadline tests wait on this event, not on wall-clock delays).
        self.held: set[str] = set()
        self.held_marker: Path | None = None
        # A redirect rule answers one request with (status, Location); a callable rule receives the
        # full request path, and a None Location sends no Location header at all. The request whose
        # query carries pi-version is the admitted hop, not the initial catalog request.
        self.pi_redirect: object | None = None
        self.hop_redirect: object | None = None
        self.metadata_redirect: object | None = None
        self.hop_resets = False


@pytest.fixture
def sources():
    state = Sources()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def do_GET(self):  # noqa: N802 - stdlib callback
            path = self.path.split("?", 1)[0]
            hop = "pi-version=" in self.path
            state.requests.append((self.path, dict(self.headers)))
            if hop and state.hop_resets:
                # The admitted hop's connection is dropped without a response: its network-failure case.
                self.close_connection = True
                return
            rule = None
            if path == f"/api/models/providers/{GO}":
                rule = state.hop_redirect if hop else state.pi_redirect
            elif path == "/metadata":
                rule = state.metadata_redirect
            if rule is not None:
                status, location = rule(self.path) if callable(rule) else rule
                state.events.append(("start", self.path))
                payload = b"redirecting"  # a body the bridge must never record as the catalog
                try:
                    self.send_response(status)
                    if location is not None:
                        self.send_header("Location", location)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(payload)))
                    self.end_headers()
                    self.wfile.write(payload)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                state.events.append(("end", self.path))
                return
            if path == f"/api/models/providers/{GO}":
                body = state.pi_body if state.pi_body is not None else json.dumps(state.pi_models)
                status, delay = state.pi_status, state.pi_delay
            elif path == "/metadata":
                body = state.metadata_body if state.metadata_body is not None else json.dumps(state.metadata)
                status, delay = state.metadata_status, state.metadata_delay
            else:
                body, status, delay = "unexpected endpoint", 404, 0
            state.events.append(("start", self.path))
            if state.overlap is not None:
                state.overlap.wait(timeout=60)
            name = held_name(self.path)
            if name in state.held:
                arrived = {held_name(p) for event, p in state.events if event == "start"}
                if state.held_marker is not None and state.held <= arrived:
                    state.held_marker.write_text("held")
                state.stop.wait()
            state.stop.wait(delay)
            state.events.append(("end", self.path))
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
    state.stop.set()
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
// The controlled deadline (bead coding-harness-jik): the bridge's own deadline timer - the one setTimeout of
// deadlineMs - runs its callback once every held request has reached the server (the marker file) and the
// bodies of the sources that answer have been read, a few event-loop turns later. Its abort path is the real one;
// only the moment is an event instead of a wall-clock bet on the machine's load.
const options = JSON.parse(process.argv[2]);
const control = options.controlledDeadline;
delete options.controlledDeadline;
let deadlineTimers = 0;
if (control) {
  const realFetch = globalThis.fetch;
  let consumed = 0;
  globalThis.fetch = async (...args) => {
    const response = await realFetch(...args);
    const text = response.text.bind(response);
    response.text = async () => { const body = await text(); consumed++; return body; };
    return response;
  };
  const realSetTimeout = globalThis.setTimeout;
  globalThis.setTimeout = (callback, ms, ...rest) => {
    if (ms !== options.deadlineMs) return realSetTimeout(callback, ms, ...rest);
    deadlineTimers++;
    let ready = 0;
    const poll = setInterval(() => {
      ready = fs.existsSync(control.marker) && consumed >= control.answered ? ready + 1 : 0;
      if (ready >= 3) { clearInterval(poll); callback(...rest); }
    }, 5);
    return poll;
  };
}
const { collectCatalog } = await import(process.argv[1]);
const result = await collectCatalog(options);
result.test_guard = { commands, credentialReads };
result.test_deadline_timers = deadlineTimers;
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
        timeout=90,
        check=False,
    )
    assert done.returncode == 0, done.stderr
    result = json.loads(done.stdout)
    assert result["test_guard"] == {"commands": 0, "credentialReads": 0}
    if "controlledDeadline" in options:
        assert result["test_deadline_timers"] == 1, "the bridge must arm exactly one timer of deadlineMs"
    assert all("authorization" not in {key.lower() for key in headers} for _, headers in sources.requests)
    return result


def held_collect(tmp_path: Path, sources: Sources, held: set[str]) -> dict:
    """`collect` with the named requests held until teardown and the shared deadline fired by event.

    Held names: "pi" is the initial catalog request, "pi-hop" the admitted versioned hop and
    "metadata" the capability source. Every held request, like every redirect body, is a body the
    bridge never reads, so exactly `2 - len(held)` reads remain answerable before the deadline.
    """
    sources.held = set(held)
    sources.held_marker = tmp_path / f"held-{len(sources.requests)}"
    control = {"marker": str(sources.held_marker), "answered": 2 - len(sources.held)}
    return collect(tmp_path, sources, deadlineMs=10000, controlledDeadline=control)


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
    # The slow source is held until teardown and the deadline fires once it is in flight (bead jik): no
    # outcome depends on how fast the machine imports Pi.
    bridge = held_collect(tmp_path, sources, {slow})
    assert len(sources.requests) == 2
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


def test_preflight_raw_duplicate_id_key_inside_models_is_document_ambiguity(tmp_path, sources):
    entry = '"id":"alpha-free","tool_call":true,"id":"alpha-free"'
    sources.metadata_body = (
        '{"opencode-go":{"models":{"alpha-free":{' + entry + '},"beta-free":{"id":"beta-free","tool_call":true}}}}'
    )
    result = select(collect(tmp_path, sources))
    assert result["selected"] == []
    assert result["fixed"] == FIXED
    assert result["capability_reason"] == "duplicate-id"


@pytest.mark.parametrize(
    "entry",
    [
        '"id":"alpha-free","tool_call":true,"tool_call":true',
        '"id":"alpha-free","tool_call":true,"cost":{"input":1,"input":2}',
    ],
)
def test_other_repeated_keys_inside_one_entry_exclude_only_that_candidate(tmp_path, sources, entry):
    # Criterion 42 (deep review RS-3-5). Planted fault: a repeated key nested anywhere in the models object - not a
    # repeated model key or id - makes the whole source capability-unavailable and excludes every free model.
    sources.metadata_body = (
        '{"opencode-go":{"models":{"alpha-free":{' + entry + '},"beta-free":{"id":"beta-free","tool_call":true}}}}'
    )
    result = select(collect(tmp_path, sources))
    assert result["capability_status"] == "available"
    assert result["selected"] == ["beta-free"]
    assert next(c for c in result["candidates"] if c["id"] == "alpha-free")["reason"] == "metadata-malformed"


def test_a_repeated_nested_key_in_a_pi_row_excludes_only_that_row(tmp_path, sources):
    # Criteria 41, 42 (deep review RS-3-5). Planted fault: a repeated key inside one Pi row's nested object ends
    # the whole preflight with exit 1 instead of excluding that candidate as pi-malformed.
    body = json.dumps(sources.pi_models)
    row = json.dumps(sources.pi_models[3])
    assert row in body
    sources.pi_body = body.replace(row, row[:-1] + ',"cost":{"input":1,"input":2}}', 1)
    result = select(collect(tmp_path, sources))
    assert next(c for c in result["candidates"] if c["id"] == "alpha-free")["reason"] == "pi-malformed"
    assert result["selected"] == ["beta-free"]


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


# ---------------------------------------------------------------------------
# Catalog ledger rows (criteria 19, 38, 39, 41, 42): named contracts over the actual wrapper
# ---------------------------------------------------------------------------


def pi_requests(sources: Sources) -> list[str]:
    return [path for path, _ in sources.requests if path.startswith("/api/models/providers/")]


def candidate(result: dict, ident: str) -> dict:
    return next(item for item in result["candidates"] if item["id"] == ident)


def test_each_run_forces_a_fresh_go_catalog(tmp_path, sources):
    # Criterion 38. Planted fault: a cached or shipped list stands in for the refresh, or the selection lacks provenance.
    seed = {GO: {"models": [model("alpha-free")], "checkedAt": int(time.time() * 1000), "lastModified": 4102444800000}}
    first = select(collect(tmp_path, sources, seedStore=seed))
    assert first["selected"] == ["alpha-free", "beta-free"]
    assert len(pi_requests(sources)) == 1, "a fresh store replaced the refresh"
    # The source changes between two runs: the second run sees the change, never the first run's roster.
    sources.pi_models = [item for item in sources.pi_models if item["id"] != "alpha-free"]
    second = select(collect(tmp_path, sources, seedStore=seed))
    assert second["selected"] == ["beta-free"]
    assert len(pi_requests(sources)) == 2, "each run makes exactly one Pi request of its own"
    for result in (first, second):
        for name in ("pi", "models_dev"):
            evidence = result["sources"][name]
            assert evidence["url"].startswith("http") and evidence["retrieved_at"].endswith("Z")
            assert len(evidence["sha256"]) == 64
    # Another provider cannot supply a seat: its entry in the overlay is a faulty candidate, never a selection.
    sources.pi_models.append(model("gamma-free", provider="other"))
    sources.metadata[GO]["models"]["gamma-free"] = capability("gamma-free")
    third = select(collect(tmp_path, sources))
    assert "gamma-free" not in third["selected"]


def test_removed_shipped_free_ids_do_not_return(tmp_path, sources):
    # Criterion 38. Planted fault: a free id that only the shipped list or a cache still names is dispatched.
    sources.metadata[GO]["models"]["removed-free"] = capability("removed-free")
    seed = {GO: {"models": [model("removed-free")], "checkedAt": 0, "lastModified": 0}}
    bridge = collect(tmp_path, sources, seedStore=seed)
    bridge["baseline"] = [*bridge["baseline"], "removed-free"]
    result = select(bridge)
    assert result["selected"] == ["alpha-free", "beta-free"]
    assert candidate(result, "removed-free")["reason"] == "not-in-fresh-pi", "audited, never eligible"
    assert "removed-free" not in {entry["id"] for entry in result["models_store"][GO]["models"]}
    # A removed id named by an include is a missing explicit include, a preflight failure, not a silent revival.
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge, {**POLICY, "include": ["removed-free"]})
    assert failure.value.exit_code == 1


@pytest.mark.parametrize(
    "fault",
    ["pi-timeout", "pi-status-304", "pi-status-500", "pi-malformed", "pi-duplicate", "pi-not-a-list", "stale-only"],
)
def test_unmeasured_catalog_never_becomes_zero_availability(tmp_path, sources, fault):
    # Criterion 41. Planted fault: an unmeasured Pi result becomes N=0 (measured empty) or exits other than 1.
    options = {}
    if fault == "pi-timeout":
        sources.pi_delay = 60  # far beyond the deadline: only a deadline that never fires can pass
        options["deadlineMs"] = 800
    elif fault.startswith("pi-status"):
        sources.pi_status = int(fault.rsplit("-", 1)[1])
    elif fault == "pi-malformed":
        sources.pi_body = "{broken"
    elif fault == "pi-duplicate":
        sources.pi_body = '[{"id":"alpha-free","id":"beta-free"}]'
    elif fault == "pi-not-a-list":
        sources.pi_body = "5"
    else:
        # Only a stale cache exists: the refresh failed, so the cached roster must not stand in.
        sources.pi_status = 500
        options["seedStore"] = {
            GO: {"models": [model("alpha-free")], "checkedAt": int(time.time() * 1000), "lastModified": 4102444800000}
        }
    bridge = collect(tmp_path, sources, **options)
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge)
    assert failure.value.exit_code == 1


def test_free_eligibility_requires_text_chat_and_explicit_tools(tmp_path, sources):
    # Criterion 39. Planted fault: a non-chat, baseline-only, tool-less or deprecated entry yields a selected seat.
    for ident in ("image-free", "tool-less-free", "no-flag-free", "old-free", "baseline-free"):
        sources.metadata[GO]["models"][ident] = capability(ident)
    sources.pi_models += [
        model("image-free", type="image"),
        model("tool-less-free"),
        model("no-flag-free"),
        model("old-free"),
    ]
    sources.metadata[GO]["models"]["tool-less-free"]["tool_call"] = False
    del sources.metadata[GO]["models"]["no-flag-free"]["tool_call"]
    sources.metadata[GO]["models"]["old-free"]["status"] = "deprecated"
    bridge = collect(tmp_path, sources)
    bridge["baseline"] = [*bridge["baseline"], "baseline-free"]
    result = select(bridge)
    assert result["selected"] == ["alpha-free", "beta-free"]
    assert candidate(result, "image-free")["reason"] == "not-chat"
    assert candidate(result, "tool-less-free")["reason"] == "no-tool-support"
    assert candidate(result, "no-flag-free")["reason"] == "no-tool-support"
    assert candidate(result, "old-free")["reason"] == "deprecated"
    assert candidate(result, "baseline-free")["reason"] == "not-in-fresh-pi"


def test_models_dev_capabilities_intersect_only_fresh_pi_ids(tmp_path, sources):
    # Criteria 39. Planted fault: a models.dev-only id, a wrong-provider entry or a missing flag is selected.
    sources.metadata[GO]["models"]["metadata-only-free"] = capability("metadata-only-free")
    sources.metadata["other"] = {"models": {"alpha-free": capability("alpha-free", tool_call=True)}}
    del sources.metadata[GO]["models"]["alpha-free"]
    sources.metadata[GO]["models"]["beta-free"]["tool_call"] = False
    result = select(collect(tmp_path, sources))
    assert result["selected"] == []
    assert result["capability_status"] == "available"
    assert result["selection_outcome"] == "measured-empty"
    assert candidate(result, "alpha-free")["reason"] == "metadata-missing", "another provider's entry granted a seat"
    assert candidate(result, "beta-free")["reason"] == "no-tool-support"
    assert "metadata-only-free" not in {item["id"] for item in result["candidates"]}


@pytest.mark.parametrize("fault", ["http-500", "http-404", "unparsable", "timeout", "not-an-object", "no-provider"])
def test_models_dev_failure_excludes_free_and_keeps_required_slots(tmp_path, sources, fault):
    # Criterion 42. Planted fault: a failed source launches free models, aborts required slots or reads as measured empty.
    if fault.startswith("http"):
        sources.metadata_status = int(fault.split("-")[1])
    elif fault == "unparsable":
        sources.metadata_body = "{broken"
    elif fault == "not-an-object":
        sources.metadata_body = "[]"
    elif fault != "timeout":
        sources.metadata_body = "{}"
    bridge = held_collect(tmp_path, sources, {"metadata"}) if fault == "timeout" else collect(tmp_path, sources)
    result = select(bridge)
    assert result["selected"] == [] and result["N"] == 0
    assert result["capability_status"] == "capability-unavailable"
    assert result["selection_outcome"] != "measured-empty", "an unread source masqueraded as measured empty metadata"
    assert result["capability_reason"], "the reason of the failure is not kept"
    assert result["fixed"] == FIXED
    graph = swarm.research_slot_plan(roles(), result["selected"])
    assert len(graph) == 39 and all(slot["required"] for slot in graph)


def test_capability_document_faults_and_candidate_faults_are_distinct(tmp_path, sources):
    # Criteria 39, 42. Planted fault: one malformed candidate excludes a valid peer, a non-boolean flag selects a seat,
    # or a document-level fault reads as measured absence.
    sources.metadata[GO]["models"]["alpha-free"]["tool_call"] = "yes"
    candidate_fault = select(collect(tmp_path, sources))
    assert candidate_fault["capability_status"] == "available"
    assert candidate_fault["selected"] == ["beta-free"]
    assert candidate(candidate_fault, "alpha-free")["reason"] == "metadata-malformed"
    # An unrelated provider's malformed entry never disables Go selection.
    sources.metadata[GO]["models"]["alpha-free"]["tool_call"] = True
    sources.metadata_body = json.dumps({**sources.metadata, "unrelated": {"models": 5}})
    assert select(collect(tmp_path, sources))["selected"] == ["alpha-free", "beta-free"]
    # A document-level fault is unavailability, with a reason, never a measured empty selection.
    sources.metadata_body = '{"opencode-go":{"models":[]}}'
    document_fault = select(collect(tmp_path, sources))
    assert document_fault["capability_status"] == "capability-unavailable"
    assert document_fault["selection_outcome"] != "measured-empty"
    assert document_fault["capability_reason"] == "malformed"


def test_catalog_shared_deadline_keeps_asymmetric_failure_rules(tmp_path, sources):
    # Criteria 19, 41, 42. Planted fault: the reads start one after the other or get separate budgets; a Pi timeout
    # dispatches; a models.dev timeout retries, extends the deadline or aborts fixed work.
    # Both requests must start before either response can finish; speed is irrelevant.
    sources.overlap = threading.Barrier(2)
    bridge = collect(tmp_path, sources, deadlineMs=60000)
    assert [event for event, _ in sources.events[:2]] == ["start", "start"]
    assert len(sources.events) == 4
    assert bridge["exit_code"] == 0
    assert len(pi_requests(sources)) == 1 and len([p for p, _ in sources.requests if p == "/metadata"]) == 1
    sources.overlap = None
    # Both slow past one shared deadline: Pi decides (exit 1), the models.dev timeout is a reason, never a retry.
    sources.pi_delay = sources.metadata_delay = 60
    sources.requests.clear()
    bridge = collect(tmp_path, sources, deadlineMs=10000)
    assert bridge["sources"]["models_dev"]["outcome"] == "timeout"
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge)
    assert failure.value.exit_code == 1
    assert len(sources.requests) == 2, "a timed-out read was retried"
    # Pi on time, models.dev timed out: a reasoned, required-slot-preserving selection; an explicit include is fatal.
    # models.dev is held and the deadline fires once Pi has answered (bead jik), not after a wall-clock bet.
    sources.pi_delay = sources.metadata_delay = 0.0
    bridge = held_collect(tmp_path, sources, {"metadata"})
    result = select(bridge)
    assert result["capability_reason"] == "timeout" and result["fixed"] == FIXED and result["selected"] == []
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge, {**POLICY, "include": ["alpha-free"]})
    assert failure.value.exit_code == 1


def test_nonempty_selection_keeps_both_sources_and_exclusion_evidence(tmp_path, sources):
    # Criteria 38, 39. Planted fault: at N=1 a source record or an excluded candidate's reason and raw value is dropped.
    sources.metadata[GO]["models"]["alpha-free"]["status"] = "deprecated"
    result = select(collect(tmp_path, sources))
    assert result["N"] == 1 and result["selected"] == ["beta-free"]
    for name in ("pi", "models_dev"):
        evidence = result["sources"][name]
        assert evidence["url"] and evidence["retrieved_at"].endswith("Z") and len(evidence["sha256"]) == 64
    excluded = candidate(result, "alpha-free")
    assert excluded["reason"] == "deprecated"
    assert excluded["evidence"]["status"] == {"present": True, "value": "deprecated"}
    assert candidate(result, "beta-free")["reason"] is None


@pytest.mark.parametrize(
    "body",
    [
        '{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"alpha-free":{"id":"alpha-free","tool_call":true},"beta-free":{"id":"beta-free","tool_call":true}}}}',
        '{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"beta-free":{"id":"alpha-free","tool_call":true}}}}',
        '{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","id":"alpha-free","tool_call":true},"beta-free":{"id":"beta-free","tool_call":true}}}}',
    ],
)
def test_duplicate_raw_keys_or_claimed_ids_exclude_all_free_candidates(tmp_path, sources, body):
    # Criterion 42. Planted fault: repeated raw keys or equal ids under different keys leave a seat selectable.
    sources.metadata_body = body
    result = select(collect(tmp_path, sources))
    assert result["selected"] == []
    assert result["capability_status"] == "capability-unavailable"
    assert result["capability_reason"] == "duplicate-id"
    assert result["fixed"] == FIXED


def test_missing_metadata_id_excludes_only_that_candidate(tmp_path, sources):
    # Criterion 42. Planted fault: a missing id admits the seat, loses its absent marker or excludes a valid peer.
    del sources.metadata[GO]["models"]["alpha-free"]["id"]
    result = select(collect(tmp_path, sources))
    assert result["selected"] == ["beta-free"]
    excluded = candidate(result, "alpha-free")
    assert excluded["reason"] == "metadata-malformed"
    assert excluded["evidence"]["id"] == {"present": False}
    assert result["capability_status"] == "available"


# ---------------------------------------------------------------------------
# Pi catalog redirect (bead coding-harness-j2wb): the one admitted version hop
# ---------------------------------------------------------------------------


def versioned_location(path: str, pin: str = PIN, prefix: bool = False) -> str:
    """A Location that repeats the request's own query and adds exactly `pi-version=<pin>`.

    `prefix` puts the version parameter first: query order must not matter for admission.
    """
    base, _, query = path.partition("?")
    version = f"pi-version={pin}"
    if prefix:
        return f"{base}?{version}&{query}" if query else f"{base}?{version}"
    return f"{base}?{query}&{version}" if query else f"{base}?{version}"


@contextlib.contextmanager
def foreign_server():
    """A second, independently counted loopback server: a foreign origin no request may reach."""
    requests: list[tuple[str, dict]] = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def do_GET(self):  # noqa: N802 - stdlib callback
            requests.append((self.path, dict(self.headers)))
            self.send_response(200)
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"[]")

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.02), daemon=True)
    thread.start()
    try:
        yield requests, f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


@pytest.mark.parametrize(
    "status,build",
    [
        (301, lambda _url, path: versioned_location(path)),
        (302, lambda _url, path: versioned_location(path, prefix=True)),
        (303, lambda _url, path: versioned_location(path).replace("%2C", ",")),
        (307, lambda url, path: f"{url}{versioned_location(path)}"),
        (308, lambda _url, path: versioned_location(path, prefix=True)),
    ],
)
def test_preflight_accepts_one_pinned_version_redirect(tmp_path, sources, status, build):
    # Criterion 1. Planted fault: the admitted version hop fails preflight, hard-codes the version
    # independently of the pin, or loses fresh catalog entries on the way.
    def admitted(path: str) -> tuple[int, str]:
        return status, build(sources.url, path)

    sources.pi_redirect = admitted
    bridge = collect(tmp_path, sources)
    assert bridge["exit_code"] == 0
    first_path = next(p for p in pi_requests(sources) if "pi-version=" not in p)
    assert sum("pi-version=" in p for p, _ in sources.requests) == 1, "the admitted hop ran once"
    evidence = bridge["sources"]["pi"]
    assert evidence["url"] == f"{sources.url}{first_path}", "the requested url was overwritten"
    assert evidence["redirect_status"] == status
    built = build(sources.url, first_path)
    assert evidence["redirected_to"] == (built if built.startswith("http") else f"{sources.url}{built}")
    assert len(pi_requests(sources)) == 2, "the admitted hop is the only second request"
    # Row L1-2: pi.dev's redirect depends on the user agent, so the hop sends the original headers.
    first_headers, hop_headers = (
        {k.lower(): v for k, v in h.items()} for p, h in sources.requests if p.startswith("/api/models/providers/")
    )
    for name in ("user-agent", "accept"):
        assert hop_headers.get(name) == first_headers.get(name), f"the admitted hop dropped {name}"
    result = select(bridge)
    assert result["selected"] == ["alpha-free", "beta-free"]
    assert result["fixed"] == FIXED
    kept = result["sources"]["pi"]
    assert kept["redirected_to"] == evidence["redirected_to"]
    assert kept["redirect_status"] == status
    assert kept["sha256"] == hashlib.sha256(evidence["body"].encode()).hexdigest()


@pytest.mark.parametrize(
    "fault",
    [
        "foreign-origin",
        "other-path",
        "altered-original-value",
        "duplicated-original-pair",
        "comma-collision",
        "wrong-version",
        "duplicate-version",
        "extra-parameter",
        "credentials",
        "fragment",
        "missing-location",
        "unparsable-location",
    ],
)
def test_preflight_refuses_unapproved_catalog_redirect(tmp_path, sources, fault):
    # Criterion 2. Planted fault: a forbidden target is contacted before the refusal, or the refusal
    # evidence is absent or reads as an empty catalog.
    with foreign_server() as (foreign_requests, foreign_url):
        chosen: dict[str, str | None] = {}

        def refused(path: str) -> tuple[int, str | None]:
            base, _, query = path.partition("?")
            admitted = f"{path}&pi-version={PIN}"
            if fault == "foreign-origin":
                location = f"{foreign_url}{admitted}"
            elif fault == "other-path":
                location = f"/api/models/providers/other?{query}&pi-version={PIN}"
            elif fault == "altered-original-value":
                location = f"{base}?{query.split('=', 1)[0]}=altered&pi-version={PIN}"
            elif fault == "duplicated-original-pair":
                location = f"{path}&{query}&pi-version={PIN}"
            elif fault == "comma-collision":
                # Row L1-6: `types=chat,image` and `types,chat=image` joined to the same string.
                name, value = next((n, v) for n, v in urllib.parse.parse_qsl(query) if "," in v)
                head, _, rest = value.partition(",")
                moved = urllib.parse.urlencode([(f"{name},{head}", rest)])
                others = [(n, v) for n, v in urllib.parse.parse_qsl(query) if n != name]
                tail = f"&{urllib.parse.urlencode(others)}" if others else ""
                location = f"{base}?{moved}{tail}&pi-version={PIN}"
            elif fault == "wrong-version":
                location = f"{path}&pi-version=0"
            elif fault == "duplicate-version":
                location = f"{admitted}&pi-version={PIN}"
            elif fault == "extra-parameter":
                location = f"{admitted}&extra=1"
            elif fault == "credentials":
                location = f"{sources.url.replace('http://', 'http://catalog-user@')}{admitted}"
            elif fault == "fragment":
                location = f"{admitted}#catalog"
            elif fault == "missing-location":
                location = None
            else:
                location = "http://"
            chosen["location"] = location
            return 307, location

        sources.pi_redirect = refused
        bridge = collect(tmp_path, sources)

    evidence = bridge["sources"]["pi"]
    assert evidence["outcome"] == "redirect-refused"
    if fault == "missing-location":
        assert "no usable Location" in evidence["error"]
    elif fault == "unparsable-location":
        assert "not a usable URL" in evidence["error"] and "http://" in evidence["error"]
    else:
        named = chosen["location"]
        assert (named if named.startswith("http") else f"{sources.url}{named}") in evidence["error"]
    assert "body" not in evidence and "status" not in evidence, "a refusal was accepted as a snapshot"
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge)
    assert failure.value.exit_code == 1
    assert len(pi_requests(sources)) == 1, "the refused target was contacted"
    assert not any("pi-version=" in path for path in pi_requests(sources)), "the versioned target was contacted"
    assert not foreign_requests, "a foreign target was contacted"


def test_preflight_refuses_a_second_catalog_redirect(tmp_path, sources):
    # Criterion 3. Planted fault: a third GET happens, preflight succeeds, or the second redirect is
    # an indistinguishable ordinary request failure.
    def admitted(path: str) -> tuple[int, str]:
        return 307, versioned_location(path)

    with foreign_server() as (foreign_requests, foreign_url):

        def again(path: str) -> tuple[int, str]:
            return 307, f"{foreign_url}{path}"

        sources.pi_redirect = admitted
        sources.hop_redirect = again
        bridge = collect(tmp_path, sources)

    evidence = bridge["sources"]["pi"]
    assert evidence["outcome"] == "redirect-refused"
    assert evidence["redirected_to"] in evidence["error"], "the admitted target is not named"
    assert evidence["redirect_status"] == 307
    assert "body" not in evidence and "status" not in evidence and "sha256" not in evidence
    assert len(pi_requests(sources)) == 2, "a third catalog GET happened"
    assert not foreign_requests, "the hidden second Location was followed"
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge)
    assert failure.value.exit_code == 1


def test_preflight_redirect_record_preserves_request_and_final_evidence(tmp_path, sources):
    # Criterion 4. Planted fault: the requested url is overwritten, a hop field is missing, the
    # digest describes the redirect body, or selection drops the hop evidence.
    def admitted(path: str) -> tuple[int, str]:
        return 307, versioned_location(path)

    sources.pi_redirect = admitted
    bridge = collect(tmp_path, sources)
    first_path = next(p for p in pi_requests(sources) if "pi-version=" not in p)
    evidence = bridge["sources"]["pi"]
    assert evidence["url"] == f"{sources.url}{first_path}"
    assert evidence["redirected_to"] == f"{sources.url}{versioned_location(first_path)}"
    assert evidence["redirect_status"] == 307
    assert evidence["status"] == 200 and evidence["outcome"] == "ok"
    assert evidence["body"] == json.dumps(sources.pi_models), "the final body was not the recorded one"
    assert evidence["sha256"] == hashlib.sha256(evidence["body"].encode()).hexdigest()
    kept = select(bridge)["sources"]["pi"]
    assert kept["url"] == evidence["url"]
    assert kept["redirected_to"] == evidence["redirected_to"]
    assert kept["redirect_status"] == evidence["redirect_status"]
    assert kept["sha256"] == evidence["sha256"]
    assert "body" not in kept


def test_preflight_redirect_failure_keeps_hop_evidence(tmp_path, sources):
    # Criterion 4. Planted fault: a followed HTTP or network failure loses the hop fields or is
    # classified as a success.
    def admitted(path: str) -> tuple[int, str]:
        return 307, versioned_location(path)

    sources.pi_redirect = admitted
    sources.pi_status = 500
    bridge = collect(tmp_path, sources)
    evidence = bridge["sources"]["pi"]
    assert evidence["outcome"] == "http-error" and evidence["status"] == 500
    assert evidence["redirect_status"] == 307 and evidence["redirected_to"]
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge)
    assert failure.value.exit_code == 1
    assert len(pi_requests(sources)) == 2
    # A hop connection dropped without a response is a request failure, never a refusal or a success.
    sources.requests.clear()
    sources.pi_status = 200
    sources.hop_resets = True
    bridge = collect(tmp_path, sources)
    evidence = bridge["sources"]["pi"]
    assert evidence["outcome"] == "request-failed"
    assert evidence["redirect_status"] == 307 and evidence["redirected_to"]
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge)
    assert failure.value.exit_code == 1
    assert len(pi_requests(sources)) == 2, "a retry sent further catalog GETs"


def test_preflight_redirect_failure_does_not_retry(tmp_path, sources):
    # Criterion 5. Planted fault: Pi's retries send further catalog GETs or replace the refusal record.
    sources.pi_redirect = (307, f"/api/models/providers/{GO}?types=chat&pi-version={PIN}")
    bridge = collect(tmp_path, sources)
    evidence = bridge["sources"]["pi"]
    assert evidence["outcome"] == "redirect-refused"
    assert f"pi-version={PIN}" in evidence["error"], "the refusal no longer names the Location"
    assert "only one Go catalog request" not in evidence["error"], "a retry replaced the refusal evidence"
    assert len(pi_requests(sources)) == 1, "a direct refusal sent two catalog GETs"
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge)
    assert failure.value.exit_code == 1
    # A failed admitted hop also stays at two GETs: Pi's retry of the retryable 429 is aborted before I/O.
    sources.requests.clear()

    def admitted(path: str) -> tuple[int, str]:
        return 307, versioned_location(path)

    sources.pi_redirect = admitted
    sources.pi_status = 429
    bridge = collect(tmp_path, sources)
    assert bridge["sources"]["pi"]["outcome"] == "http-error"
    assert bridge["sources"]["pi"]["redirect_status"] == 307
    assert len(pi_requests(sources)) == 2, "a followed failure sent three catalog GETs"


def test_preflight_redirect_hop_uses_shared_deadline(tmp_path, sources):
    # Criterion 6. Planted fault: the held hop gets a fresh deadline (held_collect asserts exactly one
    # deadline timer), a third request starts, or the held hop yields a usable or measured-empty snapshot.
    def admitted(path: str) -> tuple[int, str]:
        return 307, versioned_location(path)

    sources.pi_redirect = admitted
    bridge = held_collect(tmp_path, sources, {"pi-hop"})
    assert len(pi_requests(sources)) == 2, "a third request started while the hop was held"
    assert sum("pi-version=" in p for p, _ in sources.requests) == 1, "the held request was not the hop"
    evidence = bridge["sources"]["pi"]
    assert evidence["outcome"] == "timeout"
    assert evidence["redirect_status"] == 307 and evidence["redirected_to"]
    assert "status" not in evidence, "a held hop produced a measured body"
    with pytest.raises(swarm.ResearchCatalogError) as failure:
        select(bridge)
    assert failure.value.exit_code == 1


def test_preflight_metadata_redirect_stays_refused(tmp_path, sources):
    # Criterion 7. Planted fault: models.dev's redirect target is fetched, fixed seats are lost for
    # that failure alone, or free seats are selected without capability evidence.
    with foreign_server() as (foreign_requests, foreign_url):

        def elsewhere(path: str) -> tuple[int, str]:
            return 307, f"{foreign_url}{path}?pi-version={PIN}"

        sources.metadata_redirect = elsewhere
        bridge = collect(tmp_path, sources)
        result = select(bridge)

    evidence = bridge["sources"]["models_dev"]
    assert evidence["outcome"] == "request-failed", "models.dev kept its refusal vocabulary"
    assert "redirected_to" not in evidence and "redirect_status" not in evidence
    assert not foreign_requests, "the metadata redirect target was fetched"
    assert len([p for p, _ in sources.requests if p == "/metadata"]) == 1
    assert result["selected"] == [] and result["fixed"] == FIXED
    assert result["capability_status"] == "capability-unavailable"
    assert result["capability_reason"] == "request-failed"


def test_preflight_direct_catalog_has_no_redirect_fields(tmp_path, sources):
    # Criterion 8. Planted fault: a direct 200 claims a redirect, costs an extra GET or a model
    # subprocess, or touches credentials (the collect traps fail on the latter two).
    bridge = collect(tmp_path, sources)
    evidence = bridge["sources"]["pi"]
    assert bridge["exit_code"] == 0 and evidence["outcome"] == "ok"
    assert "redirected_to" not in evidence and "redirect_status" not in evidence
    assert len(pi_requests(sources)) == 1 and len(sources.requests) == 2
    result = select(bridge)
    assert result["selected"] == ["alpha-free", "beta-free"]
    assert "redirected_to" not in result["sources"]["pi"]


def test_the_bridge_takes_the_admitted_version_from_the_pin_not_a_literal() -> None:
    # Row L1-5 (criterion 1's refutation "the version is hard-coded independently of the pin"):
    # every redirect case builds pi-version from the pin, so a literal would pass them all; the
    # bridge source must not carry the pinned version as a literal.
    source = (ROOT / "scripts/stage2_research_catalog.mjs").read_text(encoding="utf-8")
    assert PIN not in source, "the bridge hard-codes the pinned Pi version"
    assert "manifest.dependencies" in source, "the bridge no longer reads the version from the pin"
