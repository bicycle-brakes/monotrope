"""The one Go address policy: same-host path moves run on, foreign hosts refuse (go-access-point).

Every test drives the real caller functions — reviewer, swarm, probe and
research seat — with synthetic send stand-ins, and reads only synthetic
address records written into the test world's own declaration; no test
touches the working tree's held `model-endpoints.yaml` and no test reaches a
network. The interactive session has its own record here
(`test_the_session_binds_the_checked_model_without_reading_auth`), and the
real-Pi half of the binding lives in `tests/test_pi_contract.py`. Leak,
free-class and data-class rules have their own suites: this file proves the
address never replaces them, not the rules themselves.

Each behavioral test's fault is the launch the baseline still sends: before
this change a catalog's foreign `baseUrl` reached Pi's configuration and the
transport unchecked (DL-B-8).
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import stage2  # noqa: E402
import stage2_availability as availability  # noqa: E402
import stage2_go  # noqa: E402
import stage2_session  # noqa: E402
import stage2_swarm as swarm  # noqa: E402
from test_stage2 import (  # noqa: E402
    TEST_ADDRESS,
    TEST_LADDER,
    TEST_RUNGS,
    World,
    loop_state,
)
from test_stage2 import world as stage2_world  # noqa: E402
from test_stage2_session import GO_BARE, GO_MODEL, pi_steps  # noqa: E402
from test_stage2_session import world as _session_world  # noqa: E402

world = stage2_world
session_world = _session_world
RECORDED_BASE = TEST_ADDRESS["apis"]["openai-completions"]["basis"]
MOVED_BASE = "https://opencode.ai/inference/go/v1"


# ---------------------------------------------------------------------------
# Fixtures and harnesses: synthetic records, stores and the launch families
# ---------------------------------------------------------------------------


def edit_entry(w, change) -> None:
    """Rewrite the world's `opencode-go` entry through `change`, in its own declaration.

    A session world declares in its worktree (`tree`), a review world in its root.
    """
    path = getattr(w, "tree", w.root) / "model-endpoints.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    entry = next(item for item in data["endpunkte"] if item["name"] == "opencode-go")
    change(entry)
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")


def row(model: str, **changes: object) -> dict:
    """One fresh Go definition as a catalog row carries it, on the recorded base."""
    return {
        "id": model,
        "name": model,
        "provider": "opencode-go",
        "api": "openai-completions",
        "baseUrl": RECORDED_BASE,
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 4096,
        **changes,
    }


def go_store(*models: dict) -> dict:
    """A refreshed store with the given Go definitions, as the retrieval evidence is shaped."""
    return {"opencode-go": {"models": list(models), "lastModified": 0}}


def bridge_with(*models: dict) -> dict:
    """A synthetic pinned-Pi bridge for the research selector, sources answering these rows."""
    capabilities = {item["id"]: {"id": item["id"], "tool_call": True} for item in models}
    return {
        "exit_code": 0,
        "pi_version": "test-pin",
        "baseline": [],
        "models_store": {"opencode-go": {"models": list(models), "lastModified": 0}},
        "sources": {
            "pi": {"status": 200, "body": json.dumps(list(models))},
            "models_dev": {
                "status": 200,
                "outcome": "ok",
                "body": json.dumps({"opencode-go": {"models": capabilities}}),
            },
        },
    }


def selector_policy() -> dict:
    return {"provider": "opencode-go", "suffix": "-free", "include": [], "exclude": []}


class Harness:
    """The real launch families against one world and one send counter.

    Every family runs its production preparation and dispatch: the reviewer
    through `run_reviewer` (the swarm's member path through `run_swarm`), the
    probe through `probe_go`, the research seat through `Run.launch`. The
    transport stand-ins count sends; nothing leaves the process.
    """

    def __init__(self, w: World, monkeypatch: pytest.MonkeyPatch) -> None:
        import stage2_research_run as research

        self.w = w
        self.research = research
        self.sent: list[tuple] = []

        def send(*args, **kwargs):
            command = args[0] if args else kwargs.get("args")
            if isinstance(command, list) and command[:1] == ["node"]:
                # The offline overlay validation of the checked configuration: no model request.
                return SimpleNamespace(returncode=0, stdout="", stderr="")
            self.sent.append((args, kwargs))
            return SimpleNamespace(returncode=0, stdout="OK", stderr="")

        monkeypatch.setattr(stage2, "launch", send)
        # Only the research module sees the stand-in; the process-wide `subprocess` stays real.
        monkeypatch.setattr(
            research,
            "subprocess",
            SimpleNamespace(Popen=send, DEVNULL=subprocess.DEVNULL, PIPE=subprocess.PIPE),
        )
        monkeypatch.setattr(availability, "_checked_probe", lambda *_args, **_kwargs: None)

    def reviewer(self, model: str, store: dict, *, free: bool = False):
        ctx = stage2.Context(self.w.root, "demo", self.w.research.parent, "test-bead")
        ctx.models_store = store
        return lambda: stage2.run_reviewer(ctx, model, "review prompt", "test-key", free=free)

    def swarm(self, model: str, store: dict):
        ctx = stage2.Context(self.w.root, "demo", self.w.research.parent, "test-bead")
        ctx.models_store = store
        return lambda: stage2.run_swarm(ctx, [model], {model: "prompt"}, "test-key", free=False)

    def probe(self, model: str, store: dict):
        audit: list[str] = []
        return (lambda: availability.probe_go(stage2, self.w.root, "demo", model, "test-key", audit, store)), audit

    def seat(self, model: str, store: dict, lines: list[str]):
        from stage2_research_dispatch import Slot

        entry = {"program": "pi", "model": model, "endpoint": availability.GO, "role": "repository"}

        def pi_command(_entry, _prompt, scratch):
            agent = scratch / "agent"
            agent.mkdir()
            availability.install_measured_models(
                stage2, agent, store, model=model, address=availability.go_policy(stage2, self.w.root)
            )
            return ["synthetic-pi"], self.w.root, {"PI_CODING_AGENT_DIR": str(agent)}

        run = SimpleNamespace(
            runner=stage2,
            root=self.w.root,
            entries={"saved": entry},
            scratch={},
            line=lines.append,
            lines=lines,
            selection={"catalog": {"models_store": store}},
            free=[],
            pi_command=pi_command,
        )
        slot = Slot("saved", availability.GO, True, (0,), 60, {}, "prompt")

        def call():
            try:
                return self.research.Run.launch(run, slot, 60)
            finally:
                for tmp in list(run.scratch.values()):
                    tmp.cleanup()
                run.scratch.clear()

        return call


# ---------------------------------------------------------------------------
# Criterion 1: one record, every launch family
# ---------------------------------------------------------------------------


def test_every_go_path_reads_the_one_address_record(world, monkeypatch, capsys):
    """Criterion 1: no caller keeps its own Go origin rule or missing-address default.

    Fault: a caller that prepared against one record and dispatched from a
    private one would send after the record changed, or would run when the
    record is gone.
    """
    model = TEST_LADDER[0]
    harness = Harness(world, monkeypatch)
    store = go_store(row(model))
    seat_lines: list[str] = []
    seat = harness.seat(model, store, seat_lines)
    calls = [
        harness.reviewer(model, store),
        harness.reviewer(model, store, free=True),
        harness.probe(model, store)[0],
        seat,
    ]
    for call in calls:
        capsys.readouterr()
        call()
    assert len(harness.sent) == len(calls), "a family did not dispatch under the admitted record"
    # The record alone changes; every family's next launch refuses.
    edit_entry(world, lambda e: e["adresse"].update({"host": "elsewhere.invalid"}))
    for call in calls:
        capsys.readouterr()
        with pytest.raises((stage2.Refused, stage2_go.DestinationRefused)) as raised:
            call()
        assert "not the admitted host" in str(raised.value)
    # A refused member aborts the swarm: an admission refusal is no answer to replace.
    with pytest.raises(stage2.Refused) as raised:
        harness.swarm(model, store)()
    assert "not the admitted host" in str(raised.value)
    assert len(harness.sent) == len(calls), "a changed record dispatched a further send"
    # The record disappears: fail closed, no caller fills a default in.
    edit_entry(world, lambda e: e.pop("adresse"))
    for call in calls:
        with pytest.raises(stage2.Refused) as raised:
            call()
        assert "unusable" in str(raised.value)
    with pytest.raises(stage2.Refused) as raised:
        harness.swarm(model, store)()
    assert "unusable" in str(raised.value)
    assert len(harness.sent) == len(calls), "a missing record admitted a launch"


# ---------------------------------------------------------------------------
# Criterion 2: hostile destinations refuse before any send
# ---------------------------------------------------------------------------

HOSTILE = {
    "missing-path": "https://opencode.ai",
    "root-path": "https://opencode.ai/",
    "missing-path-default-port": "https://opencode.ai:443",
    "root-path-default-port": "https://opencode.ai:443/",
    "plain-http": "http://opencode.ai/zen/go/v1",
    "foreign-host": "https://evil.test/zen/go/v1",
    "host-suffix": "https://opencode.ai.evil.test/zen/go/v1",
    "non-default-port": "https://opencode.ai:8443/zen/go/v1",
    "userinfo": "https://user:pw@opencode.ai/zen/go/v1",
    "query": "https://opencode.ai/zen/go/v1?x=1",
    "fragment": "https://opencode.ai/zen/go/v1#frag",
    "backslash": "https://opencode.ai\\@evil.test/zen/go/v1",
    "control-character": "https://opencode.ai/zen/go/v1\n",
    "loopback": "http://127.0.0.1:9/v1",
}


@pytest.mark.parametrize("base", HOSTILE.values(), ids=HOSTILE.keys())
def test_unsafe_destinations_are_refused_before_any_send(world, monkeypatch, capsys, base):
    """Criterion 2: no hostile form reaches a send, and no diagnostic echoes the refused URL.

    Fault: the baseline copied a catalog's `baseUrl` into the launch unchecked
    (DL-B-8); each variant here is exactly such a row.
    """
    model = TEST_LADDER[0]
    harness = Harness(world, monkeypatch)
    store = go_store(row(model, baseUrl=base))
    with pytest.raises(stage2.Refused) as reviewer_error:
        harness.reviewer(model, store)()
    assert "refused" in str(reviewer_error.value)
    probe_call, audit = harness.probe(model, store)
    with pytest.raises(stage2_go.DestinationRefused) as probe_error:
        probe_call()
    assert all("address notice" not in line for line in audit), "a hostile row was announced as a move"
    assert len(harness.sent) == 0, "a hostile destination reached the transport"
    read = capsys.readouterr()
    joined = str(reviewer_error.value) + str(probe_error.value) + read.out + read.err
    assert base not in joined, "a diagnostic echoed the refused URL"
    if base == HOSTILE["userinfo"]:
        assert "user:pw" not in joined


# ---------------------------------------------------------------------------
# Criterion 3: same-host path moves run on with a notice
# ---------------------------------------------------------------------------


def test_same_host_path_moves_run_with_notice(world, monkeypatch, capsys):
    """Criterion 3: `/inference/go/v1` is neither refused nor rewritten; the move is announced.

    Fault: the offline reproduction stopped otherwise identical models on the
    path alone, so the swarm could not run.
    """
    model = TEST_LADDER[0]
    harness = Harness(world, monkeypatch)
    store = go_store(row(model, baseUrl=MOVED_BASE))
    policy = stage2_go.load_address_policy(world.root)
    verdict = stage2_go.assess(policy, model, row(model, baseUrl=MOVED_BASE))
    assert verdict.admitted and verdict.notice
    assert model in verdict.notice and "/zen/go/v1" in verdict.notice and "/inference/go/v1" in verdict.notice
    assert verdict.definition["baseUrl"] == MOVED_BASE, "the observed path was replaced"
    capsys.readouterr()
    harness.reviewer(model, store)()
    err = capsys.readouterr().err
    assert "Address notice:" in err and "/inference/go/v1" in err
    probe_call, audit = harness.probe(model, store)
    probe_call()
    assert any("address notice" in line and "/inference/go/v1" in line for line in audit)
    lines: list[str] = []
    harness.seat(model, store, lines)()
    assert any("Address notice:" in line and "/inference/go/v1" in line for line in lines)
    assert len(harness.sent) == 3, "a move notice replaced or stopped a send"
    # One trailing slash is the same path: no notice is invented for it.
    verdict = stage2_go.assess(policy, model, row(model, baseUrl=RECORDED_BASE + "/"))
    assert verdict.admitted and verdict.notice is None


# ---------------------------------------------------------------------------
# Criterion 4: absent bases take the recorded api default
# ---------------------------------------------------------------------------


def test_absent_bases_get_the_recorded_api_default(world, monkeypatch, tmp_path):
    """Criterion 4: a missing base becomes the record's explicit base for the resolved wire api.

    Fault: Pi supplies a shipped or ambient default after validation, an
    invalid explicit base counts as absent, or an unmapped api guesses.
    """
    model = TEST_LADDER[0]
    policy = stage2_go.load_address_policy(world.root)
    verdict = stage2_go.assess(policy, model, {"id": model, "api": "openai-completions"})
    assert verdict.admitted and verdict.notice is None
    assert verdict.definition["baseUrl"] == RECORDED_BASE
    # An explicit invalid base is not treated as absent.
    assert not stage2_go.assess(
        policy, model, {"id": model, "api": "openai-completions", "baseUrl": "http://opencode.ai/x"}
    ).admitted
    assert not stage2_go.assess(policy, model, {"id": model, "api": "openai-completions", "baseUrl": None}).admitted, (
        "an explicit null base was treated as omitted"
    )
    # An unmapped api has no default, and neither has a definition without an api.
    assert not stage2_go.assess(policy, model, {"id": model, "api": "other-wire"}).admitted
    assert not stage2_go.assess(policy, model, {"id": model}).admitted
    # The reviewer family dispatches the filled definition.
    harness = Harness(world, monkeypatch)
    bare = row(model)
    del bare["baseUrl"]
    harness.reviewer(model, go_store(bare))()
    assert len(harness.sent) == 1
    probe_call, _audit = harness.probe(model, go_store(bare))
    probe_call()
    assert len(harness.sent) == 2
    # The installation fills the same default and names the fill.
    agent = tmp_path / "agent"
    agent.mkdir()
    notes = availability.install_measured_models(None, agent, go_store(bare), model=model, address=policy)
    activated = json.loads((agent / "models.json").read_text(encoding="utf-8"))
    carried = activated["providers"]["opencode-go"]["models"][0]["baseUrl"]
    assert carried == RECORDED_BASE, "the installation let Pi fill the base instead"
    assert any("filled from the record's default" in note for note in notes)
    unmapped = tmp_path / "unmapped"
    unmapped.mkdir()
    with pytest.raises(availability.OverlayError):
        availability.install_measured_models(
            None, unmapped, go_store({"id": model, "api": "other-wire"}), model=model, address=policy
        )


# ---------------------------------------------------------------------------
# Criterion 5: refused rows stay refused
# ---------------------------------------------------------------------------


def test_refused_rows_stay_refused(world, monkeypatch):
    """Criterion 5: a refused catalog row returns as neither a shipped model nor a lost peer.

    Fault: dropping the row lets the same id's shipped definition run, one bad
    row excludes unrelated candidates, or an empty admitted set reads as a
    clean round.
    """
    good, bad = TEST_LADDER[0], TEST_LADDER[1]
    harness = Harness(world, monkeypatch)
    store = go_store(row(good), row(bad, baseUrl="https://evil.test/zen/go/v1"))
    harness.reviewer(good, store)()
    assert len(harness.sent) == 1, "one refused row excluded a valid peer"
    with pytest.raises(stage2.Refused) as error:
        harness.reviewer(bad, store)()
    assert "not the admitted host" in str(error.value)
    assert len(harness.sent) == 1, "the refused row fell back to a shipped definition and ran"
    # The research selector refuses the candidate alone and keeps its raw evidence.
    policy = stage2_go.load_address_policy(world.root)
    result = swarm.select_research_catalog(
        bridge_with(row("aa-free"), row("bb-free", baseUrl="https://evil.test/x")),
        selector_policy(),
        [],
        expected_version="test-pin",
        address=policy,
    )
    assert result["selected"] == ["aa-free"]
    reasons = {item["id"]: item["reason"] for item in result["candidates"]}
    assert reasons["bb-free"] == "pi-malformed"
    evidence = next(item for item in result["candidates"] if item["id"] == "bb-free")["evidence"]
    assert evidence["pi"]["baseUrl"]["value"] == "https://evil.test/x", "raw catalog evidence was rewritten"
    # An empty admitted set is not a clean selection: nothing stays selected.
    empty = swarm.select_research_catalog(
        bridge_with(row("cc-free", baseUrl="https://evil.test/x")),
        selector_policy(),
        [],
        expected_version="test-pin",
        address=policy,
    )
    assert empty["selected"] == [] and empty["selection_outcome"] != "selected"


def test_compatibility_probe_continues_after_a_refused_destination(world, monkeypatch, capsys):
    """A refused first paid member must not prevent the next valid member's send."""
    bad, good = TEST_LADDER[:2]
    harness = Harness(world, monkeypatch)
    store = go_store(row(bad, baseUrl="https://evil.test/go/v1"), row(good))
    monkeypatch.setattr(stage2, "require_pi", lambda: None)
    monkeypatch.setattr(stage2, "discover_free", lambda *_args, **_kwargs: {"selected": [], "models_store": store})
    monkeypatch.setattr(stage2, "ladder", lambda _root: [bad, good])
    with pytest.raises(stage2.CallFailed, match=f"1 members failed: {bad}"):
        stage2.probe(world.root, "demo")
    assert len(harness.sent) == 1, "the valid member was skipped or the refused member sent"
    output = capsys.readouterr().out
    assert f"{bad} failed:" in output and "not the admitted host" in output
    assert f"{good} · OK" in output


# ---------------------------------------------------------------------------
# Criterion 6: every send re-checks current policy
# ---------------------------------------------------------------------------


def test_every_send_rechecks_current_policy(world, monkeypatch, capsys):
    """Criterion 6: a saved selection, resumed round, replacement or retry dispatches no now-refused base.

    Fault: an old receipt or saved overlay authorized the send; here the
    record turns hostile after every preparation and nothing dispatches.
    """
    model = TEST_LADDER[0]
    harness = Harness(world, monkeypatch)
    store = go_store(row(model))
    seat_lines: list[str] = []
    seat = harness.seat(model, store, seat_lines)
    probe_call, _audit = harness.probe(model, store)
    prepared = [harness.reviewer(model, store), harness.reviewer(model, store, free=True), probe_call, seat]
    for call in prepared:
        capsys.readouterr()
        call()
    assert len(harness.sent) == len(prepared), "preparation itself failed"
    history = (list(harness.sent), list(seat_lines))
    # The record turns hostile after preparation: no saved evidence dispatches.
    edit_entry(world, lambda e: e["adresse"].update({"host": "elsewhere.invalid"}))
    for call in prepared:
        capsys.readouterr()
        with pytest.raises((stage2.Refused, stage2_go.DestinationRefused)) as raised:
            call()
        assert "not the admitted host" in str(raised.value)
    with pytest.raises(stage2.Refused):
        harness.swarm(model, store)()
    assert (list(harness.sent), list(seat_lines)) == history, "earlier completed history was rewritten"


# ---------------------------------------------------------------------------
# Criterion 7: the session binds the checked model without reading auth
# ---------------------------------------------------------------------------


def test_session_keeps_the_catalog_path_and_records_its_notice(session_world, capsys):
    """The shipped same-host base survives binding and its move stays in the launch audit."""
    w = session_world
    w.declare_go()
    catalog = w.bin / "node_modules/@earendil-works/pi-ai/dist/providers/data/opencode-go.json"
    data = json.loads(catalog.read_text(encoding="utf-8"))
    observed = "https://opencode.ai/inference/go/openai/v1"
    data["openai-completions"][f"chat:{GO_BARE}"]["baseUrl"] = observed
    catalog.write_text(json.dumps(data), encoding="utf-8")
    w.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
    assert w.run(model=GO_MODEL) == 0
    sidecar = w.bindings[0]["extension"].parent / "checked-model.json"
    assert json.loads(sidecar.read_text(encoding="utf-8"))["model"]["baseUrl"] == observed
    for evidence in (capsys.readouterr().out, w.text()):
        assert GO_BARE in evidence and "/zen/go/v1" in evidence and "/inference/go/openai/v1" in evidence


def test_the_session_binds_the_checked_model_without_reading_auth(session_world, monkeypatch):
    """Criterion 7: the terminal receives the checked binding, and no credential file is read.

    Fault: the terminal receives a launch whose selected model still resolves
    another base, or the check reads the user's saved credentials.
    """
    w = session_world
    w.declare_go()
    # A canary in the user's own agent credentials: nothing may read or copy it.
    home = Path(os.environ["HOME"])
    auth = home / ".pi" / "agent" / "auth.json"
    auth.parent.mkdir(parents=True, exist_ok=True)
    auth.write_text('{"CANARY-AUTH-TOKEN": "bearer-canary"}', encoding="utf-8")
    w.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
    assert w.run(model=GO_MODEL) == 0
    assert len(w.bindings) == 1 and len(w.calls("pi")) == 3, "the binding needed no extra Pi call"
    binding = w.bindings[0]
    assert binding["bare"] == GO_BARE and str(binding["cli"]).endswith("pin-pi")
    private = binding["extension"].parent
    sidecar = private / "checked-model.json"
    carried = json.loads(sidecar.read_text(encoding="utf-8"))
    assert carried["provider"] == "opencode-go" and carried["model"]["id"] == GO_BARE
    assert carried["model"]["baseUrl"] == RECORDED_BASE, "the terminal launch carries an unchecked base"
    assert set(carried["model"]) <= {
        "id",
        "name",
        "api",
        "baseUrl",
        "reasoning",
        "input",
        "contextWindow",
        "maxTokens",
        "cost",
    }, "the sidecar carries more than the allow-listed fields"
    # Unit level: the checked definition comes from the record for the shipped catalog's wire api.
    unit, _verdict = stage2_session.checked_session_model(w.tree, GO_BARE, stage2)
    assert unit["baseUrl"] == RECORDED_BASE and set(unit) <= set(carried["model"])
    # The confirmation asks the installed Pi with a scratch HOME and agent directory only.
    seen: dict = {}

    def spy(command, **kwargs):
        seen["command"], seen["env"] = list(command), dict(kwargs.get("env") or {})
        return SimpleNamespace(returncode=0, stdout=f"opencode-go  {GO_BARE}\n", stderr="")

    evidence = sidecar.read_text(encoding="utf-8") + json.dumps(w.calls()) + w.command()
    monkeypatch.setattr(stage2_session.subprocess, "run", spy)
    w.real_confirm_binding(w.tree, str(w.bin / "pin-pi"), binding["extension"], GO_BARE, stage2)
    assert seen["env"]["HOME"] != os.environ["HOME"], "the confirmation read the user's home"
    assert seen["env"]["PI_CODING_AGENT_DIR"] == seen["env"]["HOME"]
    # The canary reaches nothing: not the sidecar, not the command, not any recorded call.
    assert "bearer-canary" not in evidence + json.dumps(seen), "a credential entered the launch"


def test_the_session_refuses_without_the_address_record(session_world, capsys):
    """Criterion 8 at the session: with the record gone, the session refuses before anything opens.

    Fault: a literal or cached base bound the model anyway and the window opened.
    """
    w = session_world
    w.declare_go()
    edit_entry(w, lambda e: e.pop("adresse"))
    w.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
    assert w.run(model=GO_MODEL) == 2
    assert "unusable" in capsys.readouterr().err
    assert w.bindings == [] and w.calls("osascript") == [], "an unusable record still opened a window"


# ---------------------------------------------------------------------------
# Criterion 8: an unusable record stops Go admission
# ---------------------------------------------------------------------------

GOOD_RECORD_TEXT = """\
endpunkte:
  - name: opencode-go
    modelle: []
    adresse:
      host: opencode.ai
      apis:
        openai-completions:
          basis: "https://opencode.ai/zen/go/v1"
          quelle: "the Go page"
          gelesen: "2026-10-31"
"""

UNUSABLE = {
    "duplicate-entry": """\
endpunkte:
  - name: opencode-go
    adresse:
      host: opencode.ai
      apis:
        openai-completions:
          basis: "https://opencode.ai/zen/go/v1"
          quelle: "the Go page"
          gelesen: "2026-10-31"
  - name: opencode-go
    modelle: []
""",
    "duplicate-key": GOOD_RECORD_TEXT.replace(
        "      host: opencode.ai\n", "      host: opencode.ai\n      host: evil.test\n"
    ),
    "native-date": GOOD_RECORD_TEXT.replace('gelesen: "2026-10-31"', "gelesen: 2026-10-31"),
    "no-entries": "endpunkte: []\n",
}


@pytest.mark.parametrize("text", UNUSABLE.values(), ids=UNUSABLE.keys())
def test_an_unusable_record_stops_go_admission(world, monkeypatch, text):
    """Criterion 8: a missing, duplicated or malformed record activates no literal.

    Fault: a silent last-one-wins load, a YAML-native date, or a missing
    entry list quietly activated a cached or built-in policy.
    """
    model = TEST_LADDER[0]
    harness = Harness(world, monkeypatch)
    (world.root / "model-endpoints.yaml").write_text(text, encoding="utf-8")
    with pytest.raises(stage2_go.RecordUnusable) as unit:
        stage2_go.load_address_policy(world.root)
    assert str(unit.value)
    with pytest.raises(stage2.Refused) as error:
        harness.reviewer(model, go_store(row(model)))()
    assert "unusable" in str(error.value)
    probe_call, _audit = harness.probe(model, go_store(row(model)))
    with pytest.raises(stage2.Refused):
        probe_call()
    assert len(harness.sent) == 0, "an unusable record activated a literal default"
    # A dict-level malformation refuses too: no host, no apis, an unknown key, a plain-http basis.
    # Start from a declaration the edit helper can rewrite, whatever the case above broke.
    (world.root / "model-endpoints.yaml").write_text(GOOD_RECORD_TEXT, encoding="utf-8")
    for adresse in (
        {"apis": {"openai-completions": {"basis": RECORDED_BASE, "quelle": "x", "gelesen": "2026-10-31"}}},
        {"host": "opencode.ai"},
        {
            "host": "https://opencode.ai",
            "apis": {"openai-completions": {"basis": RECORDED_BASE, "quelle": "x", "gelesen": "2026-10-31"}},
        },
        {
            "host": "opencode.ai",
            "typo_key": True,
            "apis": {"openai-completions": {"basis": RECORDED_BASE, "quelle": "x", "gelesen": "2026-10-31"}},
        },
        {
            "host": "opencode.ai",
            "apis": {
                "openai-completions": {"basis": "http://opencode.ai/zen/go/v1", "quelle": "x", "gelesen": "2026-10-31"},
            },
        },
    ):
        edit_entry(world, lambda e, a=adresse: e.update({"adresse": a}))
        with pytest.raises(stage2_go.RecordUnusable):
            stage2_go.load_address_policy(world.root)
    edit_entry(world, lambda e: e.update({"adresse": copy.deepcopy(TEST_ADDRESS)}))
    policy = stage2_go.load_address_policy(world.root)
    assert policy.host == "opencode.ai", "a valid record did not load again"


# ---------------------------------------------------------------------------
# Criterion 9: path maintenance records source and date
# ---------------------------------------------------------------------------


def test_path_maintenance_records_source_and_date(world):
    """Criterion 9: a recorded path carries its source and reading date; an undated path never activates.

    Fault: an agent's documented path move was accepted without `quelle` or a
    quoted `gelesen`, or needed a code change to take effect.
    """
    policy = stage2_go.load_address_policy(world.root)
    record = policy.apis["openai-completions"]
    assert record.source.strip() and record.read == "2026-10-31"
    assert policy.recorded_path("openai-completions") == "/zen/go/v1"
    # A maintained record: the moved path is recorded as data, dated and sourced, and loads without a code change.
    maintained = copy.deepcopy(TEST_ADDRESS)
    maintained["apis"]["anthropic-messages"] = {
        "basis": MOVED_BASE,
        "quelle": "the Go page, path moved (documented)",
        "gelesen": "2026-11-02",
    }
    edit_entry(world, lambda e: e.update({"adresse": maintained}))
    policy = stage2_go.load_address_policy(world.root)
    assert policy.recorded_path("anthropic-messages") == "/inference/go/v1"
    verdict = stage2_go.assess(policy, "m", {"id": "m", "api": "anthropic-messages"})
    assert verdict.admitted and verdict.notice is None
    # An undated, unsourced or blank-sourced path is refused, never repaired.
    for broken_record in (
        {"basis": MOVED_BASE, "quelle": "x"},
        {"basis": MOVED_BASE, "gelesen": "2026-11-02"},
        {"basis": MOVED_BASE, "quelle": "   ", "gelesen": "2026-11-02"},
    ):
        broken = copy.deepcopy(TEST_ADDRESS)
        broken["apis"]["anthropic-messages"] = broken_record
        edit_entry(world, lambda e, b=broken: e.update({"adresse": b}))
        with pytest.raises(stage2_go.RecordUnusable):
            stage2_go.load_address_policy(world.root)


# ---------------------------------------------------------------------------
# Criterion 10: address admission preserves the other restrictions
# ---------------------------------------------------------------------------


def test_admission_preserves_the_other_restrictions(world, monkeypatch):
    """Criterion 10: a good host admits an address alone — terms and wire-API rules keep applying.

    Fault: an admitted address admitted an expired paid model or an unmeasured
    research wire api. Leak and free-class rules have their own suites; the
    address check runs before them and replaces none of them.
    """
    model = TEST_LADDER[0]
    harness = Harness(world, monkeypatch)
    store = go_store(row(model))
    # Terms: long past the far-future declared expiry, the admitted host still refuses.
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(3000, 1, 1))
    with pytest.raises(stage2.Refused) as error:
        harness.reviewer(model, store)()
    assert "expired" in str(error.value)
    assert harness.sent == [], "a good host bypassed the terms check"
    # Wire api: a seat candidate on the admitted host under an unmeasured api is excluded.
    policy = stage2_go.load_address_policy(world.root)
    result = swarm.select_research_catalog(
        bridge_with(row("paid-seat", api="anthropic-messages")),
        selector_policy(),
        ["paid-seat"],
        expected_version="test-pin",
        address=policy,
    )
    seat = next(item for item in result["models"] if item["id"] == "paid-seat")
    assert seat["reason"] == "wire-api-not-measured"
    assert result["selected"] == []


# ---------------------------------------------------------------------------
# Criterion 11: notices are kept and sanitised
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("dispatch_only", [False, True])
def test_notices_are_kept_and_sanitised(world, monkeypatch, capsys, dispatch_only):
    """Criterion 11: a move notice reaches durable evidence; refusals sanitise; raw evidence stands.

    Fault: the notice was transient console output, a refusal echoed a
    credential-bearing URL, or admission rewrote the catalog's raw evidence.
    """
    model = TEST_RUNGS[0] if dispatch_only else TEST_LADDER[0]
    # Resume a paid round: discovery notices cannot stand in for reviewer evidence.
    state = loop_state(consumed=("free", "flash") if dispatch_only else ("free",))
    state["free"]["models_store"] = go_store(*(row(member, baseUrl=MOVED_BASE) for member in TEST_LADDER))
    world.write_record([("L1-1", "fixed — tests/test_x.py::test_y", "no")], state=state)
    if dispatch_only:
        # Activation sees a known path; the policy changes before the final send.
        edit_entry(world, lambda e: e["adresse"]["apis"]["openai-completions"].update(basis=MOVED_BASE))
        real_check = stage2.check_overlay

        def check_then_move(*args, **kwargs):
            real_check(*args, **kwargs)
            edit_entry(world, lambda e: e["adresse"]["apis"]["openai-completions"].update(basis=RECORDED_BASE))

        monkeypatch.setattr(stage2, "check_overlay", check_then_move)
    world.script(pi=[{"stdout": "No finding."}] * len(TEST_LADDER))
    capsys.readouterr()
    assert world.run("review-loop") == 0
    if dispatch_only:
        assert "Address notice:" not in capsys.readouterr().err, "activation already saw the move"
    record = world.record().read_text(encoding="utf-8").split("## Round 2", 1)[1]
    assert f"Address notice: opencode-go/{model}:" in record, "the reviewer's move notice stayed transient"
    assert "/zen/go/v1" in record and "/inference/go/v1" in record
    harness = Harness(world, monkeypatch)
    store = go_store(row(model, baseUrl=MOVED_BASE))
    capsys.readouterr()
    harness.reviewer(model, store)()
    read = capsys.readouterr()
    assert "Address notice:" in read.err, "the move notice stayed transient"
    assert store["opencode-go"]["models"][0]["baseUrl"] == MOVED_BASE, "raw catalog evidence was rewritten"
    # A refusal sanitises: the credential-bearing URL never enters a diagnostic.
    secret = go_store(row(model, baseUrl=HOSTILE["userinfo"]))
    with pytest.raises(stage2.Refused) as error:
        harness.reviewer(model, secret)()
    read = capsys.readouterr()
    joined = str(error.value) + read.out + read.err
    assert "user:pw" not in joined and "opencode.ai/" not in joined
    # The notice names paths only: no authority, no scheme.
    policy = stage2_go.load_address_policy(world.root)
    verdict = stage2_go.assess(policy, model, row(model, baseUrl=MOVED_BASE))
    assert "opencode.ai" not in verdict.notice and "https://" not in verdict.notice
    # The probe's audit keeps the notice; the research seat's lines do too (see criterion 3).
    probe_call, audit = harness.probe(model, store)
    probe_call()
    assert any("address notice" in line for line in audit)


def test_probe_checks_the_installed_definition_not_a_vouched_destination(world, monkeypatch):
    """A safe caller-supplied definition cannot authorise a hostile installed row."""
    import inspect

    model = TEST_LADDER[0]
    harness = Harness(world, monkeypatch)
    store = go_store(row(model, baseUrl="https://unassessed.invalid/v1"))
    # Exercise the former override where present, and the store-only API after its removal.
    overrides = (
        {"destination": row(model)} if "destination" in inspect.signature(availability.probe_go).parameters else {}
    )
    with pytest.raises(stage2_go.DestinationRefused, match="not the admitted host"):
        availability.probe_go(stage2, world.root, "demo", model, "test-key", [], store, **overrides)
    assert harness.sent == []


def test_session_lookup_reads_the_real_pinned_chat_catalog(world, monkeypatch):
    """The real pin's chat-prefixed keys must resolve, without synthetic catalog data."""
    monkeypatch.setattr(stage2, "PI_WRAPPER", Path(__file__).resolve().parents[1] / "tools/pi/pi")
    catalog = Path(stage2.PI_WRAPPER).parent / "node_modules/@earendil-works/pi-ai/dist/providers/data/opencode-go.json"
    data = json.loads(catalog.read_text(encoding="utf-8"))
    models = data["openai-completions"]
    model = "mimo-v2.6-flash"
    assert f"chat:{model}" in models and model not in models
    binding, verdict = stage2_session.checked_session_model(world.root, model, stage2)
    assert verdict.admitted
    assert binding["id"] == model
    assert binding["baseUrl"] == models[f"chat:{model}"]["baseUrl"]


@pytest.mark.parametrize("family", ["reviewer", "probe", "seat", "session"])
@pytest.mark.parametrize("field,value", [("baseUrl", MOVED_BASE), ("api", "openai-responses")])
def test_dispatch_refuses_a_configuration_mismatch(request, monkeypatch, capsys, family, field, value):
    """An admitted caller dictionary cannot conceal a different sending configuration."""
    w = request.getfixturevalue("session_world" if family == "session" else "world")
    harness = Harness(w, monkeypatch) if family != "session" else None
    original = stage2.dispatch_go

    def tampered(root, model, send, *args, **kwargs):
        config = kwargs.get("configuration")
        if config is not None:
            content = json.loads(config.read_text(encoding="utf-8"))
            if config.name == "checked-model.json":
                content["model"][field] = value
            else:
                content["providers"]["opencode-go"]["models"][0][field] = value
            config.write_text(json.dumps(content), encoding="utf-8")
        return original(root, model, send, *args, **kwargs)

    monkeypatch.setattr(stage2, "dispatch_go", tampered)
    model = TEST_LADDER[0]
    store = go_store(row(model))
    if family == "session":
        w.declare_go()
        w.script(pi=pi_steps({}), osascript=[{"exec_command": True}])
        assert w.run(model=GO_MODEL) != 0
        assert not w.calls("osascript")
        assert "sending configuration" in capsys.readouterr().err
    else:
        call = {
            "reviewer": lambda: harness.reviewer(model, store)(),
            "probe": lambda: harness.probe(model, store)[0](),
            "seat": lambda: harness.seat(model, store, [])(),
        }[family]
        with pytest.raises(stage2.Refused, match="configuration"):
            call()
        assert not harness.sent


@pytest.mark.parametrize("base", ["https://foreign.invalid/go/v1", None])
def test_installation_refuses_an_unassessed_go_row(world, tmp_path, base):
    """A refused row must never be installed as dispatchable models.json."""
    policy = stage2_go.load_address_policy(world.root)
    with pytest.raises(availability.OverlayError):
        availability.install_measured_models(
            stage2, tmp_path, go_store(row(TEST_LADDER[0], baseUrl=base)), model=TEST_LADDER[0], address=policy
        )
    assert not (tmp_path / "models.json").exists()
