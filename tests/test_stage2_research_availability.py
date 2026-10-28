"""Seat selection for the research swarm: preparation, substitute pool and the reported receipt.

Local stand-ins only: no network, no real Pi or Claude Code, no model call. The
catalog bridge is replaced by a document with the shape the pinned helper
returns; the catalog helper itself is covered with loopback servers in
`test_stage2_research_catalog.py`.
"""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import sys
from contextlib import suppress
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import stage2  # noqa: E402
import stage2_availability as availability  # noqa: E402
import stage2_swarm as swarm  # noqa: E402
from terms_fixtures import admissible_terms  # noqa: E402
from test_stage2 import OKEY, World  # noqa: E402
from test_stage2 import git as run_git  # noqa: E402
from test_stage2 import world as stage2_world  # noqa: E402

world = stage2_world

GO = "opencode-go"
CLAUDE = "claude-code-plan"
HAIKU = "claude-haiku-5-5"
CANARY = "CANARY-PRIVATE-7731"

# One stand-in for the pinned wrapper and for Claude Code. Its answer is chosen
# by model id, so a test scripts reachability per model, not per call order.
STAND_IN = """#!@PYTHON@
import json, os, sys
from pathlib import Path

here = Path(__file__).resolve().parent
name = "pi" if Path(sys.argv[0]).name == "pin-pi" else Path(sys.argv[0]).name
argv = sys.argv[1:]
if name == "pi" and argv == ["--version"]:
    print("@PI@")
    raise SystemExit(0)


def option(flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


scenario = json.loads((here / "models.json").read_text())
model = (option("--model") or "").split("/")[-1]
prompt_file = option("--append-system-prompt-file") or option("--append-system-prompt")
record = {
    "name": name,
    "path": sys.argv[0],
    "argv": argv,
    "env": dict(os.environ),
    "cwd": os.getcwd(),
    "model": model,
    "prompt_file": Path(prompt_file).read_text() if prompt_file and Path(prompt_file).is_file() else None,
    "agent_listing": sorted(os.listdir(os.environ["PI_CODING_AGENT_DIR"]))
    if os.path.isdir(os.environ.get("PI_CODING_AGENT_DIR", ""))
    else None,
}
with (here / "calls.jsonl").open("a") as handle:
    handle.write(json.dumps(record) + "\\n")
step = scenario.get(model, {})
key = os.environ.get("OPENCODE_API_KEY", "")
sys.stdout.write(step.get("stdout", "OK").replace("@KEY@", key))
sys.stderr.write(step.get("stderr", "").replace("@KEY@", key))
raise SystemExit(step.get("exit", 0))
"""

NOW = dt.datetime(2026, 10, 18, 12, 0, tzinfo=dt.UTC)

# id -> (anfragen_5h or None, extra terms fields); every id is declared with a dated reading
TERMS = {
    "deepseek-v4.1-flash": 34670,
    "mimo-v2.6-flash": 30100,
    "longcat-2.0": 11400,
    "glm-5.3-flash": 6320,
    "zz-tie-model": 6320,
    "qwen3.8-flash": 5400,
    "mimo-v2.6-pro": 3250,
    "nocost-model": None,
    "skipped-model": 4000,
    "notool-model": 3900,
    "absent-model": 3800,
    "baseline-only-model": 3700,
    "embed-model": 3600,
    "anthropic-model": 3500,
}
OVERLAY_ONLY = ("noterms-model",)


def terms_record(value, **more) -> dict:
    # The shared builder's far-future expiry: every reading carries one (ADR
    # 0022), far ahead, so the fixture never expires under the live clock.
    record = admissible_terms()
    if value is not None:
        record.update(anfragen_5h=value, anfragen_gelesen="2026-10-17", anfragen_quelle="requests table")
    record.update(more)
    return record


def pi_model(ident: str, **more) -> dict:
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
        **more,
    }


class Catalog:
    """The document the catalog helper returns, built from plain fixture lists."""

    def __init__(self) -> None:
        paid = [
            ident
            for ident in TERMS
            if ident not in ("absent-model", "baseline-only-model", "embed-model", "anthropic-model")
        ]
        self.pi = [pi_model(ident) for ident in [*paid, *OVERLAY_ONLY, "alpha-free", "beta-free"]]
        self.pi.append(pi_model("embed-model", type="classifier"))
        self.pi.append(pi_model("anthropic-model", api="anthropic-messages"))
        self.pi.append(pi_model("qwen3.8-flash", api="anthropic-messages"))
        self.pi = list({item["id"]: item for item in self.pi}.values())
        self.tools = {ident: {"id": ident, "tool_call": True} for ident in [*paid, "anthropic-model", "alpha-free"]}
        self.tools["alpha-free"] = {"id": "alpha-free", "tool_call": True}
        self.tools["beta-free"] = {"id": "beta-free", "tool_call": True}
        self.tools["notool-model"] = {"id": "notool-model", "tool_call": False}
        self.baseline = ["baseline-only-model"]
        self.metadata_ok = True

    def bridge(self) -> dict:
        pi_body = json.dumps(self.pi)
        meta_body = json.dumps({GO: {"models": self.tools}})
        stamp = "2026-10-18T11:59:30.000Z"
        sources = {
            "pi": {
                "url": "http://127.0.0.1/api/models/providers/opencode-go",
                "outcome": "ok",
                "status": 200,
                "retrieved_at": stamp,
                "body": pi_body,
                "sha256": hashlib.sha256(pi_body.encode()).hexdigest(),
            },
            "models_dev": {
                "url": "http://127.0.0.1/metadata",
                "outcome": "ok" if self.metadata_ok else "request-failed",
                "status": 200 if self.metadata_ok else None,
                "retrieved_at": stamp,
                "body": meta_body,
                "sha256": hashlib.sha256(meta_body.encode()).hexdigest(),
            },
        }
        return {
            "schema": 1,
            "exit_code": 0,
            "reason": None,
            "pi_version": stage2.PI_VERSION,
            "pi_runtime": {"errors": [], "aborted": False},
            "sources": sources,
            "baseline": [*self.baseline, *[item["id"] for item in self.pi]],
            "models_store": {GO: {"models": self.pi, "checkedAt": 0, "lastModified": 0}},
            "elapsed_ms": 5,
        }


class Fixture:
    def __init__(self, w: World, monkeypatch: pytest.MonkeyPatch) -> None:
        self.w = w
        self.catalog = Catalog()
        self.models: dict[str, dict] = {}
        self.calls_to_catalog = 0
        self.clock = NOW
        monkeypatch.setattr(availability, "now", lambda: self.clock)
        monkeypatch.delenv(availability.INTELLIGENCE_KEY_ENV, raising=False)

        def bridge(_runner, _root):
            self.calls_to_catalog += 1
            return copy.deepcopy(self.catalog.bridge())

        monkeypatch.setattr(availability, "catalog_bridge", bridge)
        for name in ("pin-pi", "claude"):
            program = w.bin / name
            program.write_text(
                STAND_IN.replace("@PYTHON@", sys.executable).replace("@PI@", stage2.PI_VERSION), encoding="utf-8"
            )
            program.chmod(0o755)
        self.edit_declaration(lambda _data: None)
        self.script()
        research = w.research
        text = research.read_text(encoding="utf-8").replace("class: bounded", "class: feature\nneighbours: []")
        research.write_text(text, encoding="utf-8")
        (w.root / "plans" / "changes" / "other").mkdir()
        (w.root / "plans" / "changes" / "other" / "spec.md").write_text(
            "---\ntitle: Other spec\nbead: other-1\n---\n\n# Other\n", encoding="utf-8"
        )
        run_git(w.root, "add", "-A")
        run_git(w.root, "commit", "--quiet", "-m", "feature research")

    def script(self, **steps: dict) -> None:
        self.models = steps
        (self.w.bin / "models.json").write_text(json.dumps(steps), encoding="utf-8")

    def edit_declaration(self, change) -> None:
        path = self.w.root / "model-endpoints.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        go = next(e for e in data["endpunkte"] if e["name"] == GO)
        go["modelle_terms"] = {ident: terms_record(value) for ident, value in TERMS.items()}
        go["modelle_terms"]["skipped-model"]["uebersprungen"] = "2026-10-17"
        go["modelle_terms"]["skipped-model"]["grund"] = "wire API not measured"
        block = data["research_swarm"]
        block["repository_seats"] = [
            {"endpoint": GO, "model": "deepseek-v4.1-flash"},
            {"endpoint": GO, "model": "mimo-v2.6-flash"},
            {"endpoint": CLAUDE, "model": HAIKU},
        ]
        block["online_seats"] = [
            {"endpoint": GO, "model": "deepseek-v4.1-flash"},
            {"endpoint": GO, "model": "mimo-v2.6-flash"},
            {"endpoint": GO, "model": "qwen3.8-flash"},
        ]
        block["availability_preflight"] = {
            "max_age_seconds": 900,
            "exclude_until": [],
            "measured_wire_apis": ["openai-completions"],
        }
        block["online_free"] = {"provider": GO, "suffix": "-free", "include": [], "exclude": []}
        change(data)
        path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")

    def prepare(self, *options: str) -> int:
        return self.w.run("prepare-explore", "demo", *options)

    def probed(self) -> list[str]:
        return [call["model"] for call in self.w.calls() if call["name"] in {"pi", "claude"}]

    def receipt(self) -> dict:
        return json.loads(availability.research_receipt_path("demo", stage2, self.w.root).read_text(encoding="utf-8"))


@pytest.fixture
def fx(world: World, monkeypatch: pytest.MonkeyPatch) -> Fixture:
    return Fixture(world, monkeypatch)


def seats(state: dict, trio: str) -> list[tuple[str, str, str]]:
    return [(item["endpoint"], item["model"], item["mark"]) for item in state["seats"][trio]]


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------


def test_all_preferred_models_reachable_fill_their_seats_and_substitute_only_the_unadmitted(fx: Fixture) -> None:
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    assert seats(state, "repository") == [
        (GO, "deepseek-v4.1-flash", "preferred"),
        (GO, "mimo-v2.6-flash", "preferred"),
        (CLAUDE, HAIKU, "preferred"),
    ]
    # qwen3.8-flash is on another wire API here, so online seat 3 takes the cheapest unused pool model.
    assert seats(state, "online") == [
        (GO, "deepseek-v4.1-flash", "preferred"),
        (GO, "mimo-v2.6-flash", "preferred"),
        (GO, "longcat-2.0", "substitute for 3"),
    ]


def test_preferred_models_come_first_and_substitutes_never_take_them(fx: Fixture) -> None:
    fx.script(**{"deepseek-v4.1-flash": {"exit": 1, "stderr": "model_coming_soon @KEY@"}})
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    assert seats(state, "repository")[0] == (GO, "longcat-2.0", "substitute for 1")
    assert seats(state, "repository")[1] == (GO, "mimo-v2.6-flash", "preferred")
    assert [m for _, m, _ in seats(state, "online")[:2]].count("mimo-v2.6-flash") == 1
    for trio in ("repository", "online"):
        models = [(e, m) for e, m, _ in seats(state, trio)]
        assert len(set(models)) == 3, "one model filled two seats of a trio"
    unreachable = state["models"][f"{GO}/deepseek-v4.1-flash"]
    assert unreachable["state"] == "unreachable" and "model_coming_soon" in unreachable["reason"]
    assert OKEY not in json.dumps(state), "the unreachable model's error was not scrubbed"
    assert fx.probed().count("deepseek-v4.1-flash") == 1, "a model shared by both trios was probed twice"


def test_substitute_is_the_cheapest_reachable_unused_pool_model(fx: Fixture) -> None:
    fx.script(
        **{
            "deepseek-v4.1-flash": {"exit": 1, "stderr": "down"},
            "longcat-2.0": {"exit": 1, "stderr": "down"},
        }
    )
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    # The tie at 6320 requests is broken by id, not by declaration order.
    assert seats(state, "repository")[0] == (GO, "glm-5.3-flash", "substitute for 1")
    assert [item["model"] for item in state["pool"]][:5] == [
        "deepseek-v4.1-flash",
        "mimo-v2.6-flash",
        "longcat-2.0",
        "glm-5.3-flash",
        "zz-tie-model",
    ]
    probed = fx.probed()
    # The tie partner is only tried afterwards, for the third seat of the online trio.
    assert probed.index("glm-5.3-flash") < probed.index("zz-tie-model")
    assert seats(state, "online")[2] == (GO, "zz-tie-model", "substitute for 3")


def test_frozen_inputs_give_the_same_selection_twice(fx: Fixture) -> None:
    fx.script(**{"mimo-v2.6-flash": {"exit": 1, "stderr": "down"}})
    assert fx.prepare() == 0
    first = fx.receipt()["state"]
    assert fx.prepare() == 0
    second = fx.receipt()["state"]
    assert first["seats"] == second["seats"]
    assert first["pool"] == second["pool"]
    assert first["models"] == second["models"]


def test_pool_requires_tool_support_and_a_measured_wire_api(fx: Fixture) -> None:
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    pool = [item["model"] for item in state["pool"]]
    assert "notool-model" not in pool and "anthropic-model" not in pool and "qwen3.8-flash" not in pool
    assert state["models"][f"{GO}/notool-model"]["reason"].startswith("no-tool-support")
    assert state["models"][f"{GO}/anthropic-model"]["reason"].startswith("wire-api-not-measured")
    # models.dev unavailable: the pool is empty, the preferred models still serve their seats.
    for item in fx.catalog.pi:
        if item["id"] == "qwen3.8-flash":
            item["api"] = "openai-completions"
    fx.catalog.metadata_ok = False
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    assert state["pool"] == []
    assert seats(state, "online")[2] == (GO, "qwen3.8-flash", "preferred")
    # A seat whose preferred model is on an unmeasured wire API has no substitute without a pool.
    for item in fx.catalog.pi:
        if item["id"] == "qwen3.8-flash":
            item["api"] = "anthropic-messages"
    assert fx.prepare() == 1


def test_a_model_without_admitted_terms_or_cost_is_never_used(fx: Fixture) -> None:
    fx.script(**{"deepseek-v4.1-flash": {"exit": 1, "stderr": "down"}, "longcat-2.0": {"exit": 1, "stderr": "down"}})
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    probed = set(fx.probed())
    assert not probed & {"nocost-model", "noterms-model", "skipped-model"}
    assert "no admitted cost value" in state["models"][f"{GO}/nocost-model"]["reason"]
    assert "noterms-model" in state["unread"], "an overlay model without a terms record is not named as unread"
    assert state["models"][f"{GO}/skipped-model"]["state"] == "skipped"
    assert "nocost-model" not in [item["model"] for item in state["pool"]]


def test_unadmitted_or_excluded_models_are_never_probed_or_selected(fx: Fixture) -> None:
    fx.edit_declaration(
        lambda data: data["research_swarm"]["availability_preflight"].update(
            exclude_until=[{"model_prefix": "glm", "until": "2026-10-21T20:34:00+08:00", "reason": "outage"}]
        )
    )
    fx.script(**{"deepseek-v4.1-flash": {"exit": 1, "stderr": "down"}, "longcat-2.0": {"exit": 1, "stderr": "down"}})
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    probed = set(fx.probed())
    for model in ("glm-5.3-flash", "skipped-model", "absent-model", "baseline-only-model", "embed-model"):
        assert model not in probed
        assert state["models"][f"{GO}/{model}"]["state"] in {"skipped", "excluded"}
    assert state["models"][f"{GO}/glm-5.3-flash"]["state"] == "excluded"
    assert state["models"][f"{GO}/absent-model"]["reason"].startswith("not-in-fresh-pi")
    assert state["models"][f"{GO}/baseline-only-model"]["reason"].startswith("baseline-only")
    assert state["models"][f"{GO}/embed-model"]["reason"].startswith("not-chat")
    assert seats(state, "repository")[0] == (GO, "zz-tie-model", "substitute for 1")
    # An expired exclusion lets the model be probed again.
    fx.clock = dt.datetime(2026, 10, 21, 12, 34, tzinfo=dt.UTC)
    assert fx.prepare() == 0
    assert fx.receipt()["state"]["models"][f"{GO}/glm-5.3-flash"]["state"] != "excluded"


def test_one_terms_record_admits_a_new_substitute_without_other_edits(fx: Fixture) -> None:
    fx.script(**{"deepseek-v4.1-flash": {"exit": 1, "stderr": "down"}})
    before = stage2.ladder(fx.w.root)
    fx.catalog.pi.append(pi_model("fresh-model"))
    fx.catalog.tools["fresh-model"] = {"id": "fresh-model", "tool_call": True}
    assert fx.prepare() == 0
    assert "fresh-model" not in [item["model"] for item in fx.receipt()["state"]["pool"]]
    fx.edit_declaration(
        lambda data: next(e for e in data["endpunkte"] if e["name"] == GO)["modelle_terms"].update(
            {"fresh-model": terms_record(20000)}
        )
    )
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    order = [item["model"] for item in state["pool"]]
    assert order.index("fresh-model") == 2, "the new model is not at its cost position"
    assert seats(state, "repository")[0] == (GO, "fresh-model", "substitute for 1")
    assert stage2.ladder(fx.w.root) == before, "the review ladder changed"


# ---------------------------------------------------------------------------
# Stop, report, receipt
# ---------------------------------------------------------------------------


def test_a_seat_without_candidate_stops_before_research_with_exit_one(fx: Fixture, capsys) -> None:
    assert fx.prepare() == 0
    old = availability.research_receipt_path("demo", stage2, fx.w.root)
    assert old.exists()
    fx.catalog.metadata_ok = False
    fx.script(**{"mimo-v2.6-flash": {"exit": 1, "stderr": "down"}})
    capsys.readouterr()
    assert fx.prepare() == 1
    captured = capsys.readouterr()
    assert "seat-unavailable" in captured.out + captured.err
    assert "repository seat 2" in captured.out + captured.err
    assert not old.exists(), "an earlier receipt stayed usable"
    calls = len(fx.w.calls())
    assert fx.w.run("explore", "demo", "--availability-reported", "0" * 64) == 2
    assert len(fx.w.calls()) == calls, "a research call started"


def test_a_seat_whose_candidates_all_miss_the_fresh_catalog_stops(fx: Fixture, capsys) -> None:
    fx.catalog.pi = [item for item in fx.catalog.pi if item["id"].endswith("-free")]
    fx.catalog.baseline = ["deepseek-v4.1-flash"]
    capsys.readouterr()
    assert fx.prepare() == 1
    out = capsys.readouterr()
    assert "seat-unavailable" in out.out + out.err
    paid = [name for name in fx.probed() if name != HAIKU and not name.endswith("-free")]
    assert paid == [], "a Go model absent from the fresh overlay was probed"
    assert not availability.research_receipt_path("demo", stage2, fx.w.root).exists()


def test_a_catalog_failure_stops_before_any_probe_and_leaves_no_receipt(fx: Fixture, monkeypatch) -> None:
    assert fx.prepare() == 0
    receipt = availability.research_receipt_path("demo", stage2, fx.w.root)
    assert receipt.exists()
    before = len(fx.w.calls())

    def failing(_runner, _root):
        bridge = fx.catalog.bridge()
        bridge.update(exit_code=1, reason="pi-refresh-failed")
        return bridge

    monkeypatch.setattr(availability, "catalog_bridge", failing)
    assert fx.prepare() == 1
    assert len(fx.w.calls()) == before, "a probe started on an unmeasured catalog"
    assert not receipt.exists(), "an earlier receipt stayed usable"


def test_report_names_every_seat_candidate_and_check_time(fx: Fixture, capsys) -> None:
    fx.script(**{"deepseek-v4.1-flash": {"exit": 1, "stderr": "down"}})
    assert fx.prepare() == 0
    out = capsys.readouterr().out
    assert "Availability checked: 2026-10-18T12:00:00" in out
    for line in ("repository seat 1", "repository seat 3", "online seat 1", "online seat 3"):
        assert line in out
    assert "substitute for 1" in out and "substitute for 3" in out
    assert "Pool, cheapest first" in out and "longcat-2.0 (11400)" in out
    assert "Free selection: alpha-free, beta-free" in out
    for needle in ("deepseek-v4.1-flash: unreachable", "skipped-model: skipped", "mimo-v2.6-pro: not probed"):
        assert needle in out, needle
    assert "noterms-model" in out and "Unread" in out
    assert "Ask the maintainer in the main conversation which models to use" in out
    assert "run explore demo --availability-reported" in out


@pytest.mark.parametrize(
    "fault",
    ["wrong-id", "expired", "configuration", "class", "neighbours", "other-root", "corrupt", "second-use"],
)
def test_receipt_is_bound_single_use_and_fresh(fx: Fixture, fault: str) -> None:
    assert fx.prepare() == 0
    prepared = fx.receipt()
    path = availability.research_receipt_path("demo", stage2, fx.w.root)
    token = prepared["report_id"]
    if fault == "wrong-id":
        token = "f" * 64
    elif fault == "expired":
        fx.clock = NOW + dt.timedelta(seconds=901)
    elif fault == "configuration":
        fx.edit_declaration(lambda data: data["research_swarm"]["availability_preflight"].update(max_age_seconds=800))
    elif fault == "class":
        fx.w.research.write_text(
            fx.w.research.read_text(encoding="utf-8").replace("class: feature", "class: architectural"),
            encoding="utf-8",
        )
    elif fault == "neighbours":
        fx.w.research.write_text(
            fx.w.research.read_text(encoding="utf-8").replace(
                "neighbours: []", "neighbours: [plans/changes/other/spec.md]"
            ),
            encoding="utf-8",
        )
    elif fault == "other-root":
        prepared["binding"]["root"] = "/another/worktree"
        path.write_text(json.dumps(prepared), encoding="utf-8")
    elif fault == "corrupt":
        path.write_text("not JSON", encoding="utf-8")
    if fault == "second-use":
        # A valid first consumption deletes the receipt before any model call.
        availability.consume_research(fx.w.root, "demo", token, stage2, "feature")
        assert not path.exists()
    before = len(fx.w.calls())
    assert fx.w.run("explore", "demo", "--availability-reported", token) == 2
    assert len(fx.w.calls()) == before, "a research call started on a refused receipt"


def test_fresh_receipt_is_consumed_once_and_returns_the_frozen_selection(fx: Fixture) -> None:
    assert fx.prepare() == 0
    prepared = fx.receipt()
    fx.clock = NOW + dt.timedelta(seconds=900)
    state = availability.consume_research(fx.w.root, "demo", prepared["report_id"], stage2, "feature")
    assert state["seats"] == prepared["state"]["seats"]
    assert state["report_id"] == prepared["report_id"]
    assert not availability.research_receipt_path("demo", stage2, fx.w.root).exists()
    with pytest.raises(stage2.Refused):
        availability.consume_research(fx.w.root, "demo", prepared["report_id"], stage2, "feature")


def test_slot_plan_is_built_from_the_consumed_selection_and_probes_add_no_slots(fx: Fixture) -> None:
    fx.script(**{"deepseek-v4.1-flash": {"exit": 1, "stderr": "down"}})
    assert fx.prepare() == 0
    prepared = fx.receipt()
    state = availability.consume_research(fx.w.root, "demo", prepared["report_id"], stage2, "feature")
    roles = availability.research_roles(state, yaml.safe_load((fx.w.root / "model-endpoints.yaml").read_text()))
    graph = swarm.research_slot_plan(roles, state["free"]["selected"])
    assert len(graph) == 39 + 3 * len(state["free"]["selected"]) == 45
    assert [slot["model"] for slot in graph if slot["stage"] == "finders"][0] == "longcat-2.0"
    finder_models = [slot["model"] for slot in graph if slot["stage"] == "finders"]
    assert finder_models == [item["model"] for item in state["seats"]["repository"]]


# ---------------------------------------------------------------------------
# Probes
# ---------------------------------------------------------------------------


def test_probes_send_only_the_fixed_text_without_tools(fx: Fixture, monkeypatch: pytest.MonkeyPatch) -> None:
    (fx.w.root / "AGENTS.md").write_text(f"# Rules\n\n{CANARY} agents line\n", encoding="utf-8")
    (fx.w.root / "src" / f"{CANARY}.py").write_text("x = 1\n", encoding="utf-8")
    fx.w.research.write_text(
        fx.w.research.read_text(encoding="utf-8") + f"\nmap text {CANARY}\npublic topic {CANARY}\n", encoding="utf-8"
    )
    run_git(fx.w.root, "add", "-A")
    run_git(fx.w.root, "commit", "--quiet", "-m", "canary")
    limits = []
    launch = stage2.launch

    def capture(command, *args, **kwargs):
        if "--version" not in command:
            limits.append(kwargs.get("timeout"))
        return launch(command, *args, **kwargs)

    monkeypatch.setattr(stage2, "launch", capture)
    assert fx.prepare() == 0
    calls = [call for call in fx.w.calls() if call["name"] in {"pi", "claude"}]
    assert len(calls) == 6
    assert limits == [60] * 4 + [availability.FREE_PROBE_SECONDS] * 2
    for call in calls:
        assert CANARY not in json.dumps(call), "a private canary reached a probe"
        assert call["cwd"] != str(fx.w.root)
        if call["model"].endswith("-free"):
            continue  # a free model's probe has its own tests below
        assert "Availability probe only. Reply with OK. Do not review code or request tools." in json.dumps(call)
        if call["name"] == "pi":
            assert call["path"] == str(fx.w.bin / "pin-pi"), "a bare pi ran"
            assert "--no-tools" in call["argv"] and "--tools" not in call["argv"]
            assert "--no-context-files" in call["argv"] and "--no-extensions" in call["argv"]
    audit = fx.receipt()["state"]["audit"]
    assert len(audit) == 6 and all("leak check clean" in line for line in audit)


def test_claude_code_candidate_is_probed_through_official_claude(fx: Fixture) -> None:
    assert fx.prepare() == 0
    claude = [call for call in fx.w.calls() if call["name"] == "claude"]
    assert len(claude) == 1
    argv = claude[0]["argv"]
    assert argv[0] == "-p" and "Availability probe only" in argv[1]
    assert argv[argv.index("--tools") + 1] == ""
    for flag in ("--restricted", "--safe-mode", "--strict-mcp-config", "--no-session-persistence"):
        assert flag in argv
    assert argv[argv.index("--permission-prompts") + 1] == "none"
    assert argv[argv.index("--model") + 1] == HAIKU
    fx.script(**{HAIKU: {"exit": 1, "stderr": "down"}})
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    # The Claude Code seat is not reachable without a successful probe; a Go model substitutes.
    assert seats(state, "repository")[2][2].startswith("substitute for 3")


def test_a_leak_stops_preparation_before_any_probe(fx: Fixture) -> None:
    (fx.w.root / "src" / "leak.txt").write_text("LEAKMARK-123456\n", encoding="utf-8")
    run_git(fx.w.root, "add", "-A")
    run_git(fx.w.root, "commit", "--quiet", "-m", "leak")
    assert fx.prepare() == 2
    assert fx.probed() == []
    assert not availability.research_receipt_path("demo", stage2, fx.w.root).exists()


def tree_digest(root: Path) -> str:
    entries = []
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts or not path.is_file():
            continue
        entries.append((path.relative_to(root).as_posix(), hashlib.sha256(path.read_bytes()).hexdigest()))
    return json.dumps(entries)


def test_probes_are_lazy_unique_and_outside_the_run_budget(fx: Fixture) -> None:
    before = tree_digest(fx.w.root)
    assert fx.prepare() == 0
    probed = fx.probed()
    assert sorted(probed) == sorted(set(probed)), "a model was probed twice"
    # Pool models beyond the one substitute that was needed are never probed.
    assert set(probed) == {"deepseek-v4.1-flash", "mimo-v2.6-flash", HAIKU, "longcat-2.0", "alpha-free", "beta-free"}
    assert "claude-opus-5-5" not in probed, "an Opus role was probed"
    assert tree_digest(fx.w.root) == before, "preparation changed the worktree"
    assert run_git(fx.w.root, "status", "--porcelain") == ""


def test_probe_budget_walks_the_pool_in_order_and_skips_known_unreachable_models(fx: Fixture) -> None:
    fx.script(
        **{
            "deepseek-v4.1-flash": {"exit": 1, "stderr": "down"},
            "longcat-2.0": {"exit": 1, "stderr": "down"},
        }
    )
    assert fx.prepare() == 0
    probed = fx.probed()
    assert probed.index("longcat-2.0") < probed.index("glm-5.3-flash")
    assert probed.count("glm-5.3-flash") == 1 and probed.count("zz-tie-model") == 1


# ---------------------------------------------------------------------------
# Declaration faults and shared helpers
# ---------------------------------------------------------------------------

FAULTS = {
    "no-preferred": lambda b: b["repository_seats"].pop(),
    "fourth-seat": lambda b: b["online_seats"].append({"endpoint": GO, "model": "longcat-2.0"}),
    "fallback-list": lambda b: b["online_seats"][0].update(fallback=["longcat-2.0"]),
    "model-list": lambda b: b["online_seats"][0].update(model=["deepseek-v4.1-flash", "longcat-2.0"]),
    "undeclared": lambda b: b["repository_seats"][0].update(model="never-declared"),
    "free-seat": lambda b: b["online_seats"][0].update(model="alpha-free"),
    "off-go-online": lambda b: b["online_seats"][0].update(endpoint=CLAUDE, model=HAIKU),
    "duplicate-in-trio": lambda b: b["repository_seats"][1].update(model="deepseek-v4.1-flash"),
    "age-zero": lambda b: b["availability_preflight"].update(max_age_seconds=0),
    "age-bool": lambda b: b["availability_preflight"].update(max_age_seconds=True),
    "age-large": lambda b: b["availability_preflight"].update(max_age_seconds=3601),
    "wire-empty": lambda b: b["availability_preflight"].update(measured_wire_apis=[]),
    "wire-type": lambda b: b["availability_preflight"].update(measured_wire_apis="openai-completions"),
    "exclusion": lambda b: b["availability_preflight"].update(
        exclude_until=[{"model_prefix": "x", "until": "tomorrow", "reason": "r"}]
    ),
    "rule-missing": lambda b: b.pop("availability_preflight"),
}


@pytest.mark.parametrize("fault", sorted(FAULTS))
def test_malformed_seat_declaration_refuses_before_any_call(fx: Fixture, fault: str) -> None:
    fx.edit_declaration(lambda data: FAULTS[fault](data["research_swarm"]))
    assert fx.prepare() == 2
    assert fx.w.calls() == [] and fx.calls_to_catalog == 0
    assert not availability.research_receipt_path("demo", stage2, fx.w.root).exists()


def test_no_framework_repository_model_is_refused(fx: Fixture) -> None:
    fx.edit_declaration(
        lambda data: next(e for e in data["endpunkte"] if e["name"] == GO).update(darf_sehen=["public-web"])
    )
    assert fx.prepare() == 2 and fx.w.calls() == []


def test_research_preparation_uses_the_shared_availability_helpers(
    fx: Fixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: list[str] = []
    for name in ("rule_problem", "excluded_reason", "probe_go", "probe_claude", "seal", "verify"):
        original = getattr(availability, name)

        def spy(*args, _name=name, _original=original, **kwargs):
            seen.append(_name)
            return _original(*args, **kwargs)

        monkeypatch.setattr(availability, name, spy)
    assert fx.prepare() == 0
    assert availability.consume_research(fx.w.root, "demo", fx.receipt()["report_id"], stage2, "feature")
    assert {"rule_problem", "excluded_reason", "probe_go", "probe_claude", "seal", "verify"} <= set(seen)


def test_concurrent_consumers_cannot_share_a_single_use_receipt(fx: Fixture, monkeypatch) -> None:
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    assert fx.prepare() == 0
    prepared = fx.receipt()
    path = availability.research_receipt_path("demo", stage2, fx.w.root)
    read_text = Path.read_text
    readers = Barrier(2)

    def synchronized_read(self, *args, **kwargs):
        text = read_text(self, *args, **kwargs)
        if self == path:
            readers.wait(timeout=10)
        return text

    monkeypatch.setattr(Path, "read_text", synchronized_read)

    def consume():
        try:
            return availability.consume_research(fx.w.root, "demo", prepared["report_id"], stage2, "feature")
        except stage2.Refused:
            return None

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: consume(), range(2)))
    accepted = [result for result in results if result is not None]
    assert len(accepted) == 1
    assert accepted[0]["seats"] == prepared["state"]["seats"]
    assert not path.exists()


def test_consumed_receipt_cannot_delete_a_new_preparation(fx: Fixture, monkeypatch) -> None:
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier, Event, current_thread

    assert fx.prepare() == 0
    prepared = fx.receipt()
    path = availability.research_receipt_path("demo", stage2, fx.w.root)
    original_verify = availability.verify
    readers = Barrier(2)
    replacement_ready = Event()
    replacement = {
        **prepared,
        "state": {**prepared["state"], "checked_at": (NOW + dt.timedelta(seconds=1)).isoformat()},
    }
    replacement["report_id"] = availability.seal(replacement)

    def synchronized_verify(receipt, token):
        valid = original_verify(receipt, token)
        readers.wait(timeout=10)
        if current_thread().name.endswith("_1"):
            assert replacement_ready.wait(timeout=10)
        return valid

    monkeypatch.setattr(availability, "verify", synchronized_verify)

    def consume():
        try:
            result = availability.consume_research(fx.w.root, "demo", prepared["report_id"], stage2, "feature")
        except stage2.Refused:
            return None
        if current_thread().name.endswith("_0"):
            availability.write_receipt(path, replacement)
            replacement_ready.set()
        return result

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: consume(), range(2)))
    assert sum(result is not None for result in results) == 1
    assert json.loads(path.read_text(encoding="utf-8")) == replacement


def test_same_second_preparations_have_distinct_single_use_ids(fx: Fixture) -> None:
    assert fx.prepare() == 0
    first = fx.receipt()
    availability.consume_research(fx.w.root, "demo", first["report_id"], stage2, "feature")
    assert fx.prepare() == 0  # The fixture clock and every bound input remain unchanged.
    second = fx.receipt()
    assert first["report_id"] != second["report_id"]
    with pytest.raises(stage2.Refused):
        availability.consume_research(fx.w.root, "demo", first["report_id"], stage2, "feature")
    assert fx.receipt() == second
    assert availability.consume_research(fx.w.root, "demo", second["report_id"], stage2, "feature")


# ---------------------------------------------------------------------------
# The maintainer's choice: open seats, intelligence against cost, --seats (Q-18)
# ---------------------------------------------------------------------------


def open_go_seats(data: dict) -> None:
    block = data["research_swarm"]
    block["repository_seats"] = [{"endpoint": GO}, {"endpoint": GO}, {"endpoint": CLAUDE, "model": HAIKU}]
    block["online_seats"] = [{"endpoint": GO}, {"endpoint": GO}, {"endpoint": GO}]


def intelligence_document() -> dict:
    def entry(slug: str, name: str, score) -> dict:
        return {"slug": slug, "name": name, "evaluations": {"artificial_analysis_intelligence_index": score}}

    return {
        "data": [
            entry("deepseek-v4-1-flash-1017", "DeepSeek V4.1 Flash 1017 (max)", 45),
            entry("longcat-2-0", "LongCat 2.0", 19),
            entry("glm-5-3-flash", "GLM-5.3-Flash", 42),
            entry("mimo-v2-6-pro", "MiMo-V2.6-Pro", 46),
            entry("claude-haiku-5-5", "Claude Haiku 5.5 (max)", 43),
            entry("claude-haiku-5-5-low", "Claude Haiku 5.5 (low)", 29),
        ]
    }


def test_open_seats_take_the_cheapest_reachable_models_of_their_trio(fx: Fixture) -> None:
    # Planted fault: an open seat stays empty, takes an expensive model first, or one model fills two seats.
    fx.edit_declaration(open_go_seats)
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    assert seats(state, "repository") == [
        (GO, "deepseek-v4.1-flash", "cheapest"),
        (GO, "mimo-v2.6-flash", "cheapest"),
        (CLAUDE, HAIKU, "preferred"),
    ]
    assert seats(state, "online") == [
        (GO, "deepseek-v4.1-flash", "cheapest"),
        (GO, "mimo-v2.6-flash", "cheapest"),
        (GO, "longcat-2.0", "cheapest"),
    ]


def test_the_report_weighs_intelligence_against_cost_and_names_the_source(
    fx: Fixture, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    # Planted fault: no intelligence column, the key leaks into the output, or no strongest-model hint.
    fx.edit_declaration(
        lambda data: data["research_swarm"].update(
            intelligence_slugs={"deepseek-v4.1-flash": "deepseek-v4-1-flash-1017"}
        )
    )
    monkeypatch.setenv(availability.INTELLIGENCE_KEY_ENV, "secret-aa-key")
    seen: list[str] = []

    def fetch(key: str) -> dict:
        seen.append(key)
        return intelligence_document()

    monkeypatch.setattr(availability, "INTELLIGENCE_FETCH", fetch)
    capsys.readouterr()
    assert fx.prepare() == 0
    out = capsys.readouterr().out
    assert seen == ["secret-aa-key"] and "secret-aa-key" not in out
    assert "Artificial Analysis Intelligence Index, https://artificialanalysis.ai/ - read" in out
    assert "opencode-go/deepseek-v4.1-flash: requests 34670, intelligence 45" in out
    assert f"claude-code-plan/{HAIKU}: requests subscription, intelligence 43" in out, "the highest effort counts"
    assert "Recommendation: the seats above" in out
    scores = fx.receipt()["state"]["intelligence"]["scores"]
    assert scores["deepseek-v4.1-flash"] == 45 and scores["longcat-2.0"] == 19


def test_intelligence_not_read_never_stops_the_preparation(
    fx: Fixture, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    # Planted fault: a missing key or a failed request stops the run or hides that cost alone decided.
    capsys.readouterr()
    assert fx.prepare() == 0
    out = capsys.readouterr().out
    assert f"not read: {availability.INTELLIGENCE_KEY_ENV} is not set" in out
    assert "intelligence was not read, so cost alone decides" in out
    monkeypatch.setenv(availability.INTELLIGENCE_KEY_ENV, "k-123")

    def broken(key: str) -> dict:
        raise OSError(f"HTTP 401 for {key}")

    monkeypatch.setattr(availability, "INTELLIGENCE_FETCH", broken)
    assert fx.prepare() == 0
    out = capsys.readouterr().out
    assert "not read: HTTP 401 for [key]" in out and "k-123" not in out


def test_the_maintainers_choice_fills_the_go_seats_and_is_never_replaced(fx: Fixture, capsys) -> None:
    # Planted fault: --seats is ignored, or an unreachable chosen model is silently swapped for another.
    fx.edit_declaration(open_go_seats)
    assert fx.prepare("--seats", "repository=glm-5.3-flash,longcat-2.0") == 0
    state = fx.receipt()["state"]
    assert seats(state, "repository")[:2] == [
        (GO, "glm-5.3-flash", "maintainer's choice"),
        (GO, "longcat-2.0", "maintainer's choice"),
    ]
    assert seats(state, "online")[0] == (GO, "deepseek-v4.1-flash", "cheapest")
    fx.script(**{"glm-5.3-flash": {"exit": 1, "stderr": "down"}})
    capsys.readouterr()
    assert fx.prepare("--seats", "repository=glm-5.3-flash,longcat-2.0") == 1
    assert "seat-unavailable: repository seat 1" in capsys.readouterr().err


@pytest.mark.parametrize(
    "options",
    [
        ("--seats", "repository=a"),  # two Go seats, one model
        ("--seats", "repository=a,a"),  # one model twice
        ("--seats", "elsewhere=a,b"),  # no such trio
        ("--seats", "repository"),  # no models
        ("--seats", "online=a,b,c", "--seats", "online=d,e,f"),  # one trio twice
    ],
)
def test_a_malformed_choice_is_refused_before_any_probe(fx: Fixture, options: tuple[str, ...]) -> None:
    fx.edit_declaration(open_go_seats)
    assert fx.prepare(*options) == 2
    assert fx.probed() == []


def test_only_an_opencode_go_seat_may_be_open() -> None:
    data = yaml.safe_load((Path(__file__).resolve().parent.parent / "model-endpoints.yaml").read_text(encoding="utf-8"))
    data["research_swarm"]["repository_seats"][2] = {"endpoint": CLAUDE}
    assert "repository seat 3: only an opencode-go seat may be open" in swarm.seat_problems(data)


# ---------------------------------------------------------------------------
# The global exclusion list binds every research path (PR #208)
# ---------------------------------------------------------------------------


def exclude(*prefixes: str, shape: object = None):
    def change(data: dict) -> None:
        if shape is not None:
            data["ausgeschlossen"] = shape
            return
        for klass in ("framework", "public-web"):
            data.setdefault("ausgeschlossen", []).append(
                {"was": "test exclusion", "klasse": klass, "modelle": list(prefixes)}
            )

    return change


def test_an_excluded_pinned_model_is_never_probed_and_its_seat_takes_a_substitute(fx: Fixture) -> None:
    # Planted fault: selection admits a model that ausgeschlossen denies (finding of PR #208).
    fx.edit_declaration(exclude("deepseek-v4.1-flash"))
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    assert "deepseek-v4.1-flash" not in fx.probed()
    assert all(
        model != "deepseek-v4.1-flash" for trio in ("repository", "online") for _, model, _ in seats(state, trio)
    )
    assert state["models"][f"{GO}/deepseek-v4.1-flash"]["state"] == "excluded"


def test_an_excluded_prefix_keeps_a_model_out_of_open_seats_whatever_its_case(fx: Fixture) -> None:
    def both(data: dict) -> None:
        open_go_seats(data)
        exclude("DEEPSEEK-")(data)

    fx.edit_declaration(both)
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    assert "deepseek-v4.1-flash" not in fx.probed()
    assert seats(state, "repository")[0] == (GO, "mimo-v2.6-flash", "cheapest")


def test_an_excluded_claude_seat_is_never_probed_and_takes_a_go_substitute(fx: Fixture) -> None:
    fx.edit_declaration(exclude("claude-haiku-"))
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    assert HAIKU not in fx.probed()
    endpoint, _, mark = seats(state, "repository")[2]
    assert (endpoint, mark) == (GO, "substitute for 3")


def test_a_malformed_exclusion_list_refuses_before_any_probe(fx: Fixture) -> None:
    fx.edit_declaration(exclude(shape={"kimi": "k3"}))
    assert fx.prepare() == 2
    assert fx.probed() == []


def test_the_maintainer_cannot_choose_an_excluded_model(fx: Fixture, capsys) -> None:
    fx.edit_declaration(lambda data: (open_go_seats(data), exclude("glm-5.3-flash")(data)))
    capsys.readouterr()
    assert fx.prepare("--seats", "repository=glm-5.3-flash,longcat-2.0") == 1
    assert "glm-5.3-flash" not in fx.probed()


def test_an_excluded_free_model_leaves_the_free_selection(fx: Fixture) -> None:
    fx.edit_declaration(exclude("alpha-"))
    assert fx.prepare() == 0
    free = fx.receipt()["state"]["free"]
    assert free["selected"] == ["beta-free"] and free["excluded"] == ["alpha-free"]
    assert "alpha-free" not in fx.probed()


def test_the_probe_admission_refuses_an_excluded_model(fx: Fixture) -> None:
    fx.edit_declaration(exclude("longcat-"))
    problem = availability.research_declaration_problem(fx.w.root, GO, "longcat-2.0")
    assert problem and "excluded by model-endpoints.yaml" in problem


@pytest.mark.parametrize(
    ("role", "endpoint", "model"),
    [
        ("finder", GO, "deepseek-v4.1-flash"),
        ("repository", GO, "deepseek-v4.1-flash"),
        ("online", GO, "deepseek-v4.1-flash"),
        ("repository", CLAUDE, HAIKU),
        ("judge", CLAUDE, "claude-opus-5-5"),
        ("finder_merge", CLAUDE, "claude-opus-5-5"),
        ("topic_author", CLAUDE, "claude-opus-5-5"),
    ],
)
def test_every_research_invocation_refuses_an_excluded_model(role: str, endpoint: str, model: str) -> None:
    # The per-call gate and the role-set check both read invocation_problem; an exclusion added after
    # selection is therefore refused at the next launch, public roles included.
    data = yaml.safe_load((Path(__file__).resolve().parent.parent / "model-endpoints.yaml").read_text(encoding="utf-8"))
    data["research_swarm"]["online_seats"] = [{"endpoint": GO, "model": "deepseek-v4.1-flash"}] * 3
    exclude(model.split("-")[0] + "-")(data)
    problem = swarm.invocation_problem(data, role, endpoint, model)
    assert problem and "excluded by model-endpoints.yaml" in problem, (role, problem)
    data["ausgeschlossen"] = []
    assert "excluded" not in (swarm.invocation_problem(data, role, endpoint, model) or "")


@pytest.mark.parametrize("offset,length", [(0, 12), (5, 8), (9, 15)])
def test_intelligence_errors_redact_credential_fragments(monkeypatch, offset, length):
    key = "synthetic-credential-0123456789-abcdef"
    fragment = key[offset : offset + length]
    monkeypatch.setenv(availability.INTELLIGENCE_KEY_ENV, key)

    def broken(_key):
        raise OSError(f"request failed: {fragment}")

    monkeypatch.setattr(availability, "INTELLIGENCE_FETCH", broken)
    reading = availability.read_intelligence(["model"], {})
    assert "not read" in reading["status"]
    assert fragment not in json.dumps(reading)


@pytest.mark.parametrize(
    "entry", [{"evaluations": "unavailable"}, {"evaluations": [45]}, None, {"evaluations": {"nested": {"score": 45}}}]
)
def test_malformed_intelligence_never_blocks_a_receipt(fx, monkeypatch, capsys, entry):
    monkeypatch.setenv(availability.INTELLIGENCE_KEY_ENV, "synthetic-key")
    monkeypatch.setattr(availability, "INTELLIGENCE_FETCH", lambda _key: {"data": [entry]})
    failure = None
    code = None
    try:
        code = fx.prepare()
    except Exception as error:  # a malformed optional reading must end in a receipt, not a traceback
        failure = repr(error)
    assert failure is None, failure
    assert code == 0
    state = fx.receipt()["state"]
    assert state["intelligence"]["status"].startswith("not read:")
    assert "intelligence was not read" in capsys.readouterr().out


def test_unmatched_intelligence_has_per_model_reason_and_cost_only_caveat(monkeypatch):
    monkeypatch.setenv(availability.INTELLIGENCE_KEY_ENV, "synthetic-key")
    monkeypatch.setattr(availability, "INTELLIGENCE_FETCH", lambda _key: intelligence_document())
    reading = availability.read_intelligence(["longcat-2.0", "deepseek-v4.1-flash"], {})
    state = {
        "intelligence": reading,
        "pool": [],
        "models": {f"{GO}/longcat-2.0": {"state": "selected"}, f"{GO}/deepseek-v4.1-flash": {"state": "selected"}},
    }
    report = "\n".join(availability.intelligence_lines(state))
    assert "intelligence 19" in report
    assert "not read: no matching index entry" in report
    assert "intelligence was not weighed for deepseek-v4.1-flash" in report


@pytest.mark.parametrize(
    "args",
    [("repository",), ("elsewhere=a,b",), ("repository=a",), ("repository=a,a",), ("online=a,b,c", "online=d,e,f")],
)
def test_refused_seat_answer_invalidates_the_previous_receipt(fx, args):
    assert fx.prepare() == 0
    receipt = fx.receipt()
    before = len(fx.w.calls())
    options = [part for arg in args for part in ("--seats", arg)]
    assert fx.prepare(*options) == 2
    assert len(fx.w.calls()) == before
    consumed = None
    with suppress(stage2.Refused):
        consumed = availability.consume_research(fx.w.root, "demo", receipt["report_id"], stage2, "feature")
    assert consumed is None, "the receipt of the declined recommendation is still usable"


@pytest.mark.parametrize("klass", ["Framwork", "", 42])
def test_unknown_exclusion_class_refuses_before_probes(fx, klass):
    fx.edit_declaration(lambda data: data.update(ausgeschlossen=[{"klasse": klass, "modelle": ["deepseek-"]}]))
    assert fx.prepare() == 2
    assert fx.probed() == []
    data = yaml.safe_load((fx.w.root / "model-endpoints.yaml").read_text())
    for role in swarm.ROLE_CLASS:
        problem = swarm.invocation_problem(data, role, GO, "deepseek-v4.1-flash")
        assert problem and "malformed exclusion" in problem


@pytest.mark.parametrize("klass", ["framework", "public-web", "kundencode"])
def test_exclusion_only_binds_its_declared_research_class(fx, klass):
    fx.edit_declaration(lambda data: data.update(ausgeschlossen=[{"klasse": klass, "modelle": ["deepseek-"]}]))
    assert fx.prepare() == 0
    state = fx.receipt()["state"]
    for label, data_class in (("repository", "framework"), ("online", "public-web")):
        models = {model for _, model, _ in seats(state, label)}
        assert ("deepseek-v4.1-flash" not in models) == (klass == data_class)
    data = yaml.safe_load((fx.w.root / "model-endpoints.yaml").read_text())
    for role in ("finder", "repository", "online"):
        problem = swarm.invocation_problem(data, role, GO, "deepseek-v4.1-flash")
        assert bool(problem and "excluded by model-endpoints.yaml" in problem) == (klass == swarm.ROLE_CLASS[role])


def test_public_exclusion_removes_free_researcher_but_customer_exclusion_does_not(fx):
    fx.edit_declaration(lambda data: data.update(ausgeschlossen=[{"klasse": "public-web", "modelle": ["alpha-"]}]))
    assert fx.prepare() == 0
    free = fx.receipt()["state"]["free"]
    assert free["selected"] == ["beta-free"] and free["excluded"] == ["alpha-free"]
    data = yaml.safe_load((fx.w.root / "model-endpoints.yaml").read_text())
    problem = swarm.invocation_problem(data, "online_free", GO, "alpha-free", selected_free=["alpha-free"])
    assert problem and "excluded by model-endpoints.yaml" in problem
    fx.edit_declaration(lambda data: data["ausgeschlossen"][0].update(klasse="kundencode"))
    assert fx.prepare() == 0
    assert set(fx.receipt()["state"]["free"]["selected"]) == {"alpha-free", "beta-free"}


def test_reachable_chosen_go_model_outside_pool_keeps_declared_cost(fx, capsys):
    fx.catalog.tools["mimo-v2.6-pro"] = {"id": "mimo-v2.6-pro", "tool_call": False}
    assert fx.prepare("--seats", "online=mimo-v2.6-pro,longcat-2.0,glm-5.3-flash") == 0
    out = capsys.readouterr().out
    assert "opencode-go/mimo-v2.6-pro: requests 3250," in out


def test_a_matching_deny_does_not_hide_a_later_malformed_class(fx):
    fx.edit_declaration(
        lambda data: data.update(
            ausgeschlossen=[
                {"klasse": "framework", "modelle": ["deepseek-"]},
                {"klasse": "Framwork", "modelle": ["other-"]},
            ]
        )
    )
    problem = availability.research_declaration_problem(fx.w.root, GO, "deepseek-v4.1-flash")
    assert problem and "malformed exclusion" in problem
    assert fx.prepare() == 2
    assert fx.probed() == []


@pytest.mark.parametrize("refused", [False, True])
def test_probe_audits_survive_unsuccessful_preparation(fx: Fixture, monkeypatch, refused: bool) -> None:
    fx.catalog.metadata_ok = False
    fx.script(**{"mimo-v2.6-flash": {"exit": 1, "stderr": "down @KEY@"}})
    original = stage2.launch
    launches = []

    def launch(*args, **kwargs):
        if "--version" in args[0]:
            return original(*args, **kwargs)
        records = list(stage2.record_dir("demo", fx.w.root).glob("research-probe-*.json"))
        durable = [json.loads(path.read_text()) for path in records]
        assert len(durable) == len(launches) + 1, "probe launched before its durable audit"
        launches.append(args)
        if refused and len(launches) == 2:
            raise stage2.Refused("planted refusal after earlier probes")
        return original(*args, **kwargs)

    monkeypatch.setattr(stage2, "launch", launch)
    assert fx.prepare() == (2 if refused else 1)
    records = list(stage2.record_dir("demo", fx.w.root).glob("research-probe-*.json"))
    assert records and len(records) == len(launches)
    for path in records:
        record = json.loads(path.read_text())
        assert "leak check clean" in record["audit"]
        assert "checked_at" in record
        assert not path.is_relative_to(fx.w.root)
        assert path.stat().st_mode & 0o077 == 0
        assert OKEY not in path.read_text()
    assert not availability.research_receipt_path("demo", stage2, fx.w.root).exists()


def test_persisted_probe_audit_scrubs_credentials_before_write(fx: Fixture) -> None:
    directory = stage2.record_dir("demo", fx.w.root)
    audit = availability._ProbeAudit(directory, stage2, lambda: OKEY)
    audit.append(f"leak check clean: {OKEY} fragment {OKEY[3:13]}")
    record = next(directory.glob("research-probe-*.json")).read_text()
    assert OKEY not in record and OKEY[3:13] not in record
    assert json.loads(record)["audit"] == audit[0]


def test_unwritable_probe_audit_refuses_before_launch(fx: Fixture, monkeypatch) -> None:
    def fail(*_args, **_kwargs):
        raise OSError("planted audit failure")

    monkeypatch.setattr(availability, "write_receipt", fail)
    assert fx.prepare() == 2
    assert not fx.probed()
    assert not availability.research_receipt_path("demo", stage2, fx.w.root).exists()


# ---------------------------------------------------------------------------
# Free members are probed with the real online_free request (bead k9rw)
# ---------------------------------------------------------------------------


def free_calls(fx: Fixture) -> list[dict]:
    return [call for call in fx.w.calls() if call["name"] == "pi" and call["model"].endswith("-free")]


def test_a_free_member_is_probed_with_the_real_online_free_request(fx: Fixture, monkeypatch) -> None:
    import stage2_research_run as run

    limits = []
    launch = stage2.launch

    def capture(command, *args, **kwargs):
        if "--version" not in command and any("-free" in part for part in command):
            limits.append(kwargs.get("timeout"))
        return launch(command, *args, **kwargs)

    monkeypatch.setattr(stage2, "launch", capture)
    assert fx.prepare() == 0
    calls = free_calls(fx)
    assert sorted(call["model"] for call in calls) == ["alpha-free", "beta-free"]
    assert limits == [availability.FREE_PROBE_SECONDS] * 2
    # The first free topic's request, the shared builder's own text, with the instruction to reply OK.
    real = run.online_topic_prompt(fx.w.root, 9, availability.PROBE_TOPIC_SENTENCE)
    for call in calls:
        assert real in call["prompt_file"]
        assert "Reply with OK" in call["prompt_file"]
        assert "--no-tools" in call["argv"]
    audit = fx.receipt()["state"]["audit"]
    assert sum("alpha-free" in line or "beta-free" in line for line in audit) == 2
    assert set(fx.receipt()["state"]["free"]["selected"]) == {"alpha-free", "beta-free"}


def test_a_free_member_that_fails_its_probe_is_unavailable_and_leaves_the_selection(fx: Fixture, capsys) -> None:
    fx.script(**{"alpha-free": {"exit": 1, "stderr": "upstream said no"}})
    assert fx.prepare() == 0
    free = fx.receipt()["state"]["free"]
    assert free["selected"] == ["beta-free"]
    assert "upstream said no" in free["unavailable"]["alpha-free"]
    out = capsys.readouterr().out
    assert "Unavailable" in out and "alpha-free" in out and "upstream said no" in out


def test_a_free_model_is_not_probed_when_it_is_excluded_for_the_public_web(fx: Fixture) -> None:
    fx.edit_declaration(exclude("alpha-"))
    assert fx.prepare() == 0
    assert [call["model"] for call in free_calls(fx)] == ["beta-free"]
