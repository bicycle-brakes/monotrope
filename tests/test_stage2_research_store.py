"""Resumable research state store (Q-13): durable records, exact-binding reuse, lock.

Real files under a temporary ``XDG_STATE_HOME``, the disposable Git repository of the
snapshot tests, and real short-lived subprocesses for the SIGKILL and lock contracts.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import select
import signal
import stat
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
REPO_ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from test_stage2_research_history import commit, git  # noqa: E402

CHANGE = "plans/changes/example"
RESEARCH = CHANGE + "/research.md"


def module():
    import stage2_research_store

    return stage2_research_store


def snapshot():
    import stage2_research_snapshot

    return stage2_research_snapshot


@pytest.fixture
def state_home(tmp_path, monkeypatch):
    home = tmp_path / "xdg-state"
    monkeypatch.setenv("XDG_STATE_HOME", str(home))
    return home


@pytest.fixture
def store(state_home):  # noqa: ARG001 - sets XDG_STATE_HOME
    m = module()
    return m.Store(m.research_dir("example", REPO_ROOT))


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / CHANGE).mkdir(parents=True)
    (root / RESEARCH).write_bytes(b"---\nupdated: 2000-01-01\n---\nOriginal research\n")
    (root / "a.py").write_bytes(b"VALUE = 1\n")
    (root / ".gitignore").write_bytes(b"ignored.txt\n")
    commit(root, "baseline", paths=["a.py", RESEARCH, ".gitignore"])
    return root


def freeze(repo):
    return snapshot().freeze_research_state(repo, CHANGE, deadline=time.monotonic() + 30)


def key(slot_id="s1", *, stage="topics", topic=1, seat=0, endpoint="go", model="m-1", prompt="p-1"):
    return {
        "slot_id": slot_id,
        "stage": stage,
        "topic": topic,
        "seat": seat,
        "endpoint": endpoint,
        "model": model,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
    }


def terminal(slot_key, outcome="ok", report="REPORT", started="2026-10-18T10:00:00Z", ended="2026-10-18T10:01:00Z"):
    return {
        **slot_key,
        "outcome": outcome,
        "started": started,
        "ended": ended,
        "report": report,
        "stderr": "",
        "leak_check": {"leak": "clean"},
    }


BINDING = {
    "paths": {"a.py": "1" * 64, RESEARCH: "2" * 64},
    "research": RESEARCH,
    "research_normalised_sha256": "3" * 64,
}


def begin(store, *, binding=None, receipt="receipt-1"):
    return store.start_run(CHANGE, receipt, binding if binding is not None else BINDING)


def pipe_line(proc, timeout=120.0):
    # Read the descriptor directly: TextIOWrapper may buffer the next marker,
    # making select report no data although that marker is already in memory.
    deadline = time.monotonic() + timeout
    line = bytearray()
    while not line.endswith(b"\n"):
        ready, _, _ = select.select([proc.stdout], [], [], max(0, deadline - time.monotonic()))
        assert ready, "driver printed no marker in time"
        chunk = os.read(proc.stdout.fileno(), 1)
        assert chunk, "driver exited before its marker"
        line.extend(chunk)
    return line.decode().strip()


def test_terminal_markers_already_in_one_pipe_write_are_read_in_order():
    from types import SimpleNamespace

    reader, writer = os.pipe()
    try:
        with os.fdopen(reader, "r") as stream:
            proc = SimpleNamespace(stdout=stream)
            os.write(writer, b"TERMINAL s1\nLAUNCHED s2\n")
            assert pipe_line(proc, timeout=1) == "TERMINAL s1"
            assert pipe_line(proc, timeout=1) == "LAUNCHED s2"
    finally:
        os.close(writer)


# --- criterion 51: durable, atomic, never torn -------------------------------------------------


DRIVER = textwrap.dedent(
    """
    import subprocess, sys
    sys.path.insert(0, {scripts!r})
    import stage2_research_dispatch as d
    import stage2_research_store as s

    store = s.Store(s.research_dir("example", {root!r}))
    run = store.start_run("plans/changes/example", "receipt-1", {binding!r})
    # s2 ends only when the test releases it after the kill, so no load-dependent delay can finish it first
    child = "import os,time\\nt=time.time()\\nwhile not os.path.exists({gate!r}) and time.time()-t<300: time.sleep(0.05)"
    def slot(i):
        return d.Slot(slot_id="s%d" % i, provider="go", required=True, order=(i,), role_allowance=600.0,
                      identity={{"stage": "topics", "topic": i, "seat": 0, "endpoint": "go", "model": "m"}},
                      prompt="p%d" % i, payload="print('x')" if i == 1 else child)
    def key(slot):
        return {{"slot_id": slot.slot_id, "stage": "topics", "topic": slot.order[0], "seat": 0, "endpoint": "go",
                 "model": "m", "prompt_sha256": "0" * 64}}
    def gate(slot):
        return d.GateVerdict(blocked=False, record={{"leak": "clean"}})
    def launcher(slot, allowance):
        return subprocess.Popen([sys.executable, "-c", slot.payload], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
    def audit(slot, verdict):
        store.write_launch(run, slot.slot_id, key(slot))
        if slot.slot_id == "s2":
            print("LAUNCHED s2", flush=True)
    def on_terminal(slot, result):
        store.write_result(run, slot.slot_id, {{**key(slot), "outcome": result.outcome, "started": "t0", "ended": "t1",
                                              "report": result.stdout, "stderr": "", "leak_check": result.gate_record}})
        if slot.slot_id == "s1":
            print("TERMINAL s1", flush=True)
    d.dispatch([slot(1), slot(2)], gate=gate, launcher=launcher, audit=audit, on_terminal=on_terminal,
               per_provider_limit=1)
    """
)


def test_terminal_record_survives_sigkill_after_the_outcome(state_home):
    m = module()
    gate = state_home / "release-s2"
    script = DRIVER.format(scripts=str(SCRIPTS), binding=BINDING, gate=str(gate), root=str(REPO_ROOT))
    proc = subprocess.Popen(
        [sys.executable, "-c", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        env={**os.environ, "XDG_STATE_HOME": str(state_home)},
    )
    store = m.Store(m.research_dir("example", REPO_ROOT))
    run_id = None
    try:
        # Wait for the durable records instead of readiness on two pipe reads:
        # under the full suite's parallel load a read deadline on the driver's
        # stdout measures the machine's scheduling, not the contract (bead
        # coding-harness-jik). The bounded wait reports the driver's exit
        # status on early exit and the run ids on timeout. Output goes to a
        # sink, so neither pipe capacity nor an orphan holding a pipe delays
        # cleanup. The second launch record proves an audited attempt - audit
        # precedes the launcher - never that the child has started.
        deadline = time.monotonic() + 120.0
        while True:
            run_ids = [run["run_id"] for run in store.runs()]
            assert len(run_ids) <= 1, f"expected exactly one driver run, found {run_ids}"
            if run_ids:
                (candidate_run_id,) = run_ids
                results, interrupted = store.slot_records(candidate_run_id)
                if "s1" in results and "s2" in interrupted:
                    run_id = candidate_run_id
                    break
            if proc.poll() is not None:
                pytest.fail(f"driver exited before its records were durable: exit {proc.returncode}; runs {run_ids}")
            if time.monotonic() >= deadline:
                proc.kill()
                proc.wait(timeout=10)
                pytest.fail(f"first result and second launch record not durable within 120s: runs {run_ids}")
            time.sleep(0.05)
        if proc.poll() is None:
            proc.send_signal(signal.SIGKILL)
        proc.wait(timeout=10)
    finally:
        if proc.poll() is None:
            proc.kill()
        with contextlib.suppress(subprocess.TimeoutExpired):
            proc.wait(timeout=10)
        gate.parent.mkdir(parents=True, exist_ok=True)
        gate.write_text("release")  # the orphaned s2 child outlives its killed driver and now ends
    results, interrupted = store.slot_records(run_id)
    assert results["s1"]["outcome"] == "ok"
    assert results["s1"]["report"].strip() == "x"
    assert "s2" not in results
    assert interrupted == ["s2"]  # a launch record only


def test_temporary_or_torn_files_never_read_as_results(store):
    run = begin(store)
    store.write_launch(run, "s1", key("s1"))
    store.write_launch(run, "s2", key("s2"))
    directory = store.directory / run
    # a temporary name that would parse, a truncated result, and a result whose hash does not match
    (directory / ".tmp-s1.result.json").write_text(json.dumps(terminal(key("s1"))))
    store.write_result(run, "s2", terminal(key("s2")))
    path = directory / "s2.result.json"
    path.write_bytes(path.read_bytes()[:-9])
    results, interrupted = store.slot_records(run)
    assert results == {}
    assert interrupted == ["s1", "s2"]
    forged = json.loads(json.dumps(terminal(key("s1"))))
    forged["sha256"] = "0" * 64
    (directory / "s1.result.json").write_text(json.dumps(forged))
    results, interrupted = store.slot_records(run)
    assert results == {} and interrupted == ["s1", "s2"]
    unhashed = terminal(key("s1"))
    (directory / "s1.result.json").write_text(json.dumps(unhashed))
    assert store.slot_records(run)[0] == {}


def test_write_is_atomic_flushed_and_leaves_no_temporary_file(store, monkeypatch):
    synced = []
    real = os.fsync
    monkeypatch.setattr(os, "fsync", lambda fd: (synced.append(stat.S_ISDIR(os.fstat(fd).st_mode)), real(fd))[1])
    run = begin(store)
    store.write_result(run, "s1", terminal(key("s1")))
    assert True in synced and False in synced  # the file and its directory were flushed
    assert sorted(p.name for p in (store.directory / run).iterdir()) == ["run.json", "s1.result.json"]


def test_unsafe_slot_ids_are_refused(store):
    m = module()
    run = begin(store)
    for bad in ("../x", "a/b", "", ".hidden", "x" * 200, "a\0b"):
        with pytest.raises(m.StoreWriteError):
            store.write_launch(run, bad, key("s1"))


# --- criterion 52 and 17: placement and modes ----------------------------------------------------


def test_store_is_owner_only_outside_every_model_directory(store, repo):
    m = module()
    run = begin(store)
    store.write_launch(run, "s1", key("s1"))
    store.write_result(run, "s1", terminal(key("s1")))
    for path in [store.directory, store.directory / run]:
        assert stat.S_IMODE(path.stat().st_mode) == 0o700
    for path in (store.directory / run).iterdir():
        assert stat.S_IMODE(path.stat().st_mode) == 0o600
    store.acquire_lock()
    assert stat.S_IMODE((store.directory / ".lock").stat().st_mode) == 0o600
    store.release_lock()
    git_dir = Path(git(repo, "rev-parse", "--absolute-git-dir"))
    home = repo.parent / "home"
    store.assert_outside(repo, git_dir, home, repo.parent / "agent")  # the XDG state home is none of these
    for model_directory in (repo, git_dir, home):
        for inside in (model_directory, model_directory / "deeper"):
            with pytest.raises(m.StoreWriteError):
                m.Store(inside / "research").assert_outside(repo, git_dir, home)
    with pytest.raises(m.StoreWriteError):  # a model directory inside the store
        store.assert_outside(store.directory / "agent")
    # a loosened directory or a symbolic link in its place is refused
    store.directory.chmod(0o750)
    with pytest.raises(m.StoreWriteError):
        m.Store(store.directory).start_run(CHANGE, "r", BINDING)
    store.directory.chmod(0o700)


def test_store_refuses_a_symlinked_directory(state_home, tmp_path):
    m = module()
    target = tmp_path / "elsewhere"
    target.mkdir(mode=0o700)
    link = state_home / "coding-harness" / "stage2" / "example" / "research"
    link.parent.mkdir(parents=True)
    link.symlink_to(target)
    with pytest.raises(m.StoreWriteError):
        m.Store(link).start_run(CHANGE, "r", BINDING)


def test_store_canary_never_reaches_a_payload_argv_or_environment(state_home):
    """A store path canary stays out of everything the dispatcher hands a child."""
    import stage2_research_dispatch as d

    m = module()
    canary = "CANARY-STORE-PATH-7731"
    store = m.Store(state_home / canary / "research")
    run = begin(store)
    seen = []

    def launcher(slot, _allowance):
        script = "import os,sys; print(sys.argv, dict(os.environ), os.getcwd())"
        seen.append((slot.prompt, slot.payload))
        return subprocess.Popen(
            [sys.executable, "-c", script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
            cwd=str(state_home.parent),
            env={k: v for k, v in os.environ.items() if k != "XDG_STATE_HOME"},
        )

    slot = d.Slot("s1", "go", True, (1,), 10.0, {"stage": "topics"}, "prompt s1", "payload")
    result = d.dispatch(
        [slot],
        gate=lambda _s: d.GateVerdict(False, {"leak": "clean"}),
        launcher=launcher,
        audit=lambda s, _v: store.write_launch(run, s.slot_id, key(s.slot_id)),
        on_terminal=lambda s, r: store.write_result(run, s.slot_id, terminal(key(s.slot_id), report=r.stdout)),
    )
    assert result.exit_code == 0
    assert canary not in result.results[0].stdout
    assert canary not in repr(seen)


# --- criterion 21: scrubbing -----------------------------------------------------------------------


@pytest.mark.usefixtures("state_home")
def test_store_receipt_and_probe_records_are_scrubbed():
    stage2 = pytest.importorskip("stage2", reason="the runner is not part of this repository")
    m = module()
    secret = "sk-test-0123456789abcdefghij"
    store = m.Store(m.research_dir("example", REPO_ROOT), scrub=lambda text: stage2.scrub(text, secret))
    run = begin(store, receipt="rcpt-" + secret)
    fragment = secret[5:17]
    store.write_launch(run, "s1", {**key("s1"), "note": "launch " + fragment})
    record = terminal(key("s1"), report=f"answer {secret} and {fragment}")
    record["stderr"] = "boom " + secret[3:15]
    record["leak_check"] = {"nested": [secret, {"deep": fragment}]}
    store.write_result(run, "s1", record)
    blob = b"".join(p.read_bytes() for p in (store.directory / run).iterdir()).decode()
    assert secret not in blob and fragment not in blob and secret[3:15] not in blob
    assert "[credential]" in blob


@pytest.mark.usefixtures("state_home")
def test_a_scrub_that_raises_stops_the_write():
    m = module()

    def broken(_text):
        raise RuntimeError("scrubber lost")

    store = m.Store(m.research_dir("example", REPO_ROOT), scrub=broken)
    with pytest.raises(m.StoreWriteError):
        begin(store)


# --- criterion 53 and the binding ------------------------------------------------------------------


def stored_binding(state, research_bytes):
    return snapshot().stored_binding(state.manifest(), RESEARCH, research_bytes)


def changed(state, stored):
    return snapshot().changed_against_stored(state.manifest(), RESEARCH, state.sources()[RESEARCH], stored)


def test_binding_equal_bytes_match_and_a_foreign_tracked_edit_names_the_path(repo):
    with freeze(repo) as first:
        stored = stored_binding(first, first.sources()[RESEARCH])
    with freeze(repo) as same:
        assert changed(same, stored) == []
    (repo / "a.py").write_bytes(b"VALUE = 2\n")
    with freeze(repo) as edited:
        assert changed(edited, stored) == ["a.py"]


def test_binding_names_an_untracked_change_input_edit_added_or_removed(repo):
    (repo / CHANGE / "notes.md").write_text("notes\n")
    with freeze(repo) as first:
        stored = stored_binding(first, first.sources()[RESEARCH])
    (repo / CHANGE / "notes.md").write_text("notes edited\n")
    with freeze(repo) as edited:
        assert changed(edited, stored) == [CHANGE + "/notes.md"]
    (repo / CHANGE / "notes.md").unlink()
    with freeze(repo) as removed:
        assert changed(removed, stored) == [CHANGE + "/notes.md"]


def test_binding_refuses_a_foreign_research_tail(repo):
    with freeze(repo) as first:
        stored = stored_binding(first, first.sources()[RESEARCH])
    (repo / RESEARCH).write_bytes((repo / RESEARCH).read_bytes() + b"someone else wrote this\n")
    with freeze(repo) as edited:
        assert changed(edited, stored) == [RESEARCH]


def own_tail_stored(repo):
    """Freeze, then record the runner's append the way a published run would."""
    with freeze(repo) as first:
        frozen = first.sources()[RESEARCH]
        tail = b"\n## Research\nthe swarm's own findings\n"
        stored = snapshot().stored_binding(first.manifest(), RESEARCH, frozen, append=tail)
    restamped = frozen.replace(b"updated: 2000-01-01", b"updated: 2026-10-18") + tail
    return stored, restamped


def test_binding_ignores_only_the_own_research_append_and_head(repo):
    stored, restamped = own_tail_stored(repo)
    (repo / RESEARCH).write_bytes(restamped)
    with freeze(repo) as after:
        assert changed(after, stored) == []
    # the tail with one byte altered, or a body byte changed, is foreign
    (repo / RESEARCH).write_bytes(restamped.replace(b"swarm's", b"swarm-s"))
    with freeze(repo) as altered:
        assert changed(altered, stored) == [RESEARCH]
    (repo / RESEARCH).write_bytes(restamped.replace(b"Original", b"Rewritten"))
    with freeze(repo) as rewritten:
        assert changed(rewritten, stored) == [RESEARCH]


def test_binding_survives_head_moving_by_a_commit_of_the_own_tail(repo):
    stored, restamped = own_tail_stored(repo)
    (repo / RESEARCH).write_bytes(restamped)
    first_head = git(repo, "rev-parse", "HEAD")
    commit(repo, "record research", paths=[RESEARCH])
    assert git(repo, "rev-parse", "HEAD") != first_head
    with freeze(repo) as after:
        assert changed(after, stored) == []


def test_binding_with_the_append_not_yet_written_still_matches(repo):
    """A crash between recording the intended append and writing it leaves the frozen bytes."""
    stored, _ = own_tail_stored(repo)
    with freeze(repo) as same:
        assert changed(same, stored) == []


def make_source(store, repo, *, results, binding=None):
    """A stored run with finished results; returns (run id, freeze for the next run)."""
    with freeze(repo) as first:
        stored = binding or stored_binding(first, first.sources()[RESEARCH])
    run = store.start_run(CHANGE, "receipt-1", stored)
    for slot_key, record in results:
        store.write_launch(run, slot_key["slot_id"], slot_key)
        if record is not None:
            store.write_result(run, slot_key["slot_id"], record)
    store.finish_run(run, "incomplete")
    return run


def resume(store, repo, planned, validate=lambda _record: True):
    m = module()
    with freeze(repo) as state:
        source = store.resume_source(state.manifest(), RESEARCH, state.sources()[RESEARCH])
        return source, m.plan_reuse(source, planned, validate)


def test_reuse_requires_the_exact_binding_seat_model_and_prompt(store, repo):
    k = key("s1")
    make_source(store, repo, results=[(k, terminal(k))])
    source, plan = resume(store, repo, [k])
    assert source.usable and set(plan.reused) == {"s1"} and plan.not_reused == []
    assert plan.reused["s1"]["report"] == "REPORT"
    for field, other in [
        ("stage", "map"),
        ("topic", 2),
        ("seat", 1),
        ("endpoint", "claude"),
        ("model", "m-2"),
        ("prompt_sha256", hashlib.sha256(b"other").hexdigest()),
    ]:
        planned = {**k, field: other}
        _, plan = resume(store, repo, [planned])
        assert plan.reused == {}, field
        assert [reason for _, reason in plan.not_reused] == [field.replace("_sha256", "")], field


def test_a_changed_binding_reuses_nothing_and_names_the_paths(store, repo):
    k = key("s1")
    make_source(store, repo, results=[(k, terminal(k))])
    (repo / "a.py").write_bytes(b"VALUE = 3\n")
    source, plan = resume(store, repo, [k])
    assert not source.usable
    assert source.reasons == ["binding changed: a.py"]
    assert plan.reused == {}
    # the stored result stays: reverting the edit makes it match again
    (repo / "a.py").write_bytes(b"VALUE = 1\n")
    _, plan = resume(store, repo, [k])
    assert set(plan.reused) == {"s1"}


def test_only_the_latest_stored_run_is_a_source(store, repo):
    # Criterion 53 (deep review RS-2-4). Planted faults: an older run's result is reused, or it is passed over
    # silently - the design keeps it stored because a reverted edit may match again, and names it.
    k = key("s1")
    older = make_source(store, repo, results=[(k, terminal(k))])
    time.sleep(0.01)
    make_source(store, repo, results=[])  # a newer run holding no results
    source, plan = resume(store, repo, [k])
    assert plan.reused == {}
    assert plan.not_reused == [(f"s1 (run {older})", "not the latest run")]


def test_an_unusable_source_names_each_of_its_stored_results(store, repo):
    # Criterion 53 (deep review RS-2-4). Planted fault: an unusable latest run reuses nothing and names none of
    # its stored results.
    k = key("s1")
    make_source(store, repo, results=[(k, terminal(k))], binding={"research": "changed"})
    source, plan = resume(store, repo, [k])
    assert not source.usable
    assert plan.not_reused == [("s1", "source run unusable")]


@pytest.mark.parametrize("outcome", ["cancelled", "failed", "timed-out", "refused", "not-started-deadline"])
def test_unfinished_outcomes_are_never_reused_and_are_named(store, repo, outcome):
    k = key("s1")
    make_source(store, repo, results=[(k, terminal(k, outcome=outcome))])
    source, plan = resume(store, repo, [k])
    if outcome == "refused":
        assert not source.usable and "refused" in " ".join(source.reasons)
    assert plan.reused == {}


def test_interrupted_and_invalid_results_are_not_reused_and_are_named(store, repo):
    ok, invalid, interrupted = key("s1"), key("s2", topic=2), key("s3", topic=3)
    make_source(
        store,
        repo,
        results=[(ok, terminal(ok)), (invalid, terminal(invalid, report="BAD")), (interrupted, None)],
    )
    source, plan = resume(store, repo, [ok, invalid, interrupted], validate=lambda r: r["report"] != "BAD")
    assert set(plan.reused) == {"s1"}
    reasons = dict(plan.not_reused)
    assert reasons == {"s2": "validation", "s3": "interrupted"}
    assert source.interrupted == ["s3"]


def test_a_result_with_no_planned_slot_is_named(store, repo):
    extra = key("s9", topic=9)
    make_source(store, repo, results=[(extra, terminal(extra))])
    _, plan = resume(store, repo, [key("s1")])
    assert dict(plan.not_reused) == {"s9": "not planned"}


def test_a_matching_valid_result_is_never_also_a_launch(store, repo):
    ks = [key(f"s{i}", topic=i) for i in range(1, 4)]
    make_source(store, repo, results=[(ks[0], terminal(ks[0])), (ks[1], terminal(ks[1], outcome="failed"))])
    _, plan = resume(store, repo, ks)
    assert set(plan.reused) == {"s1"}
    assert [slot["slot_id"] for slot in plan.to_launch] == ["s2", "s3"]


# --- criterion 55 and 56: copy-forward, refused runs -------------------------------------------------


def test_adopted_results_carry_their_source_run_and_original_times(store, repo):
    k = key("s1")
    source_run = make_source(store, repo, results=[(k, terminal(k, started="T0", ended="T1"))])
    with freeze(repo) as state:
        source = store.resume_source(state.manifest(), RESEARCH, state.sources()[RESEARCH])
        new_run = store.start_run(CHANGE, "receipt-2", stored_binding(state, state.sources()[RESEARCH]))
    assert new_run != source_run
    plan = module().plan_reuse(source, [k], lambda _r: True)
    store.adopt(new_run, source, plan.reused["s1"])
    record = store.slot_records(new_run)[0]["s1"]
    assert record["reused_from"] == {"run_id": source_run}
    assert (record["started"], record["ended"]) == ("T0", "T1")
    assert record["leak_check"] == {"leak": "clean"}
    # the adopted copy is itself a source for the next run
    assert record["outcome"] == "ok"


def test_a_refused_run_is_never_a_resume_source(store, repo):
    k1, k2 = key("s1"), key("s2", topic=2)
    run = make_source(store, repo, results=[(k1, terminal(k1)), (k2, terminal(k2, outcome="refused"))])
    source, plan = resume(store, repo, [k1, k2])
    assert not source.usable
    assert plan.reused == {}
    assert source.run_id == run
    assert any("refused" in reason and "s2" in reason for reason in source.reasons)
    # a refusal recorded on the run, with no refused result record, is the same
    store2_run = store.start_run(CHANGE, "receipt-3", BINDING)
    store.finish_run(store2_run, "incomplete", refusal={"slot": "s7", "reason": "leak check blocked"})
    source, _ = resume(store, repo, [k1])
    assert not source.usable and source.run_id == store2_run
    assert any("s7" in reason and "leak check blocked" in reason for reason in source.reasons)


def test_a_complete_run_clears_the_store_and_a_cleared_store_has_no_source(store, repo):
    k = key("s1")
    run = make_source(store, repo, results=[(k, terminal(k))])
    store.finish_run(run, "complete")
    store.clear()
    assert store.runs() == []
    source, plan = resume(store, repo, [k])
    assert not source.usable and plan.reused == {}
    # a stored run published complete is not a source even if clearing was interrupted
    run = make_source(store, repo, results=[(k, terminal(k))])
    store.finish_run(run, "complete")
    # unpublished (no record in research.md): the completion flag alone does not reject it (F-35)
    source, plan = resume(store, repo, [k])
    assert source.usable and set(plan.reused) == {"s1"}
    # published: its record carries the marker
    with (repo / RESEARCH).open("ab") as handle:
        handle.write(f"\n<!-- research-swarm/v2 run {run} -->\n".encode())
    source, plan = resume(store, repo, [k])
    assert not source.usable and plan.reused == {}
    assert any("published complete" in reason for reason in source.reasons)


def test_an_unreadable_newest_run_fails_closed(store, repo):
    k = key("s1")
    make_source(store, repo, results=[(k, terminal(k))])
    broken = store.directory / ("f" * 32)
    broken.mkdir(mode=0o700)
    (broken / "run.json").write_text("{not json")
    source, plan = resume(store, repo, [k])
    assert not source.usable and plan.reused == {}
    assert "unreadable" in " ".join(source.reasons)


def test_an_empty_run_directory_left_by_a_crash_is_ignored(store, repo):
    k = key("s1")
    run = make_source(store, repo, results=[(k, terminal(k))])
    (store.directory / ("e" * 32)).mkdir(mode=0o700)
    source, plan = resume(store, repo, [k])
    assert source.usable and source.run_id == run and set(plan.reused) == {"s1"}


# --- criterion 57: a failed write -------------------------------------------------------------------


def test_a_failed_write_raises_a_named_error_and_leaves_no_partial_record(store, monkeypatch):
    m = module()
    run = begin(store)

    def deny(*_args, **_kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(Path, "replace", deny)
    with pytest.raises(m.StoreWriteError) as raised:
        store.write_result(run, "s1", terminal(key("s1")))
    assert raised.value.stage_stop_reason == "state-store-unwritable"
    monkeypatch.undo()
    assert sorted(p.name for p in (store.directory / run).iterdir()) == ["run.json"]


# --- criterion 58: the lock ---------------------------------------------------------------------------


def test_one_run_per_change_and_a_killed_runs_lock_is_released(state_home):
    m = module()
    directory = m.research_dir("example", REPO_ROOT)
    holder = subprocess.Popen(
        [
            sys.executable,
            "-c",
            f"import sys; sys.path.insert(0, {str(SCRIPTS)!r}); import stage2_research_store as s; "
            f"st = s.Store(s.research_dir('example', {str(REPO_ROOT)!r})); st.acquire_lock(); print('LOCKED', flush=True); "
            "import time; time.sleep(30)",
        ],
        stdout=subprocess.PIPE,
        text=True,
        env={**os.environ, "XDG_STATE_HOME": str(state_home)},
    )
    try:
        assert pipe_line(holder) == "LOCKED"
        second = m.Store(directory)
        with pytest.raises(m.StoreLocked) as raised:
            second.acquire_lock()
        assert raised.value.exit_code == 2
        holder.send_signal(signal.SIGKILL)
        holder.wait(timeout=10)
    finally:
        if holder.poll() is None:
            holder.kill()
    third = m.Store(directory)
    third.acquire_lock()
    with pytest.raises(m.StoreLocked):
        m.Store(directory).acquire_lock()
    third.release_lock()
    m.Store(directory).acquire_lock()


def test_the_home_guard_resolves_dotdot_and_parent_links_before_comparing(tmp_path: Path) -> None:
    # Criterion 52 (phase-6 F-19, Q-15). Planted fault: a lexical comparison lets a store under HOME pass
    # when its path spells ``..`` or reaches HOME through a parent symlink.
    store_module = module()
    home = tmp_path / "home"
    (home / ".local" / "state").mkdir(parents=True)
    link = tmp_path / "link-to-home"
    link.symlink_to(home)
    spelled = {
        "dotdot": tmp_path / "other" / ".." / "home" / ".local" / "state" / "s",
        "parent link": link / ".local" / "state" / "s",
    }
    for label, directory in spelled.items():
        with pytest.raises(store_module.StoreWriteError, match="XDG_STATE_HOME"):
            store_module.Store(directory).assert_outside(home=home)
        assert label
    # A forbidden directory reached through a link is refused too, and a store truly outside passes.
    forbidden = tmp_path / "worktree"
    forbidden.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(forbidden)
    with pytest.raises(store_module.StoreWriteError):
        store_module.Store(alias / "s").assert_outside(forbidden)
    store_module.Store(tmp_path / "elsewhere" / "s").assert_outside(forbidden, home=home)


def test_a_reused_result_keeps_the_run_that_launched_it(store, repo):
    # Criterion 55 (deep review RS-2-5). Planted fault: after A -> B -> C reuse, C's record names only B although
    # it carries A's start and end times, so the run that made the call is lost.
    k = key("s1")
    first = make_source(store, repo, results=[(k, terminal(k))])
    for _ in range(2):
        time.sleep(0.01)
        source, plan = resume(store, repo, [k])
        assert source.usable and set(plan.reused) == {"s1"}
        with freeze(repo) as state:
            run = store.start_run(CHANGE, "receipt-2", stored_binding(state, state.sources()[RESEARCH]))
        store.adopt(run, source, plan.reused["s1"])
        store.finish_run(run, "incomplete")
    record = store.slot_records(run)[0]["s1"]
    assert record["launched_in"] == first
    assert record["reused_from"] == {"run_id": source.run_id} and source.run_id != first
    assert record["started"] == "2026-10-18T10:00:00Z"
