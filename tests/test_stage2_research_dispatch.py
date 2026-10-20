"""Cancellable research dispatcher: provider queues, ordering, gate, deadlines, cancellation.

Real short-lived child processes; no model, network or file writes by the library.
"""

from __future__ import annotations

import contextlib
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


def module():
    import stage2_research_dispatch

    return stage2_research_dispatch


SLEEPER = (
    "import sys,time\nprint('start',time.time(),flush=True)\ntime.sleep({s})\nprint('end',time.time(),flush=True)\n"
)


def sleeper(seconds, tag=""):
    return SLEEPER.format(s=seconds) + (f"print({tag!r},flush=True)\n" if tag else "")


def make_slot(slot_id, *, provider="go", required=True, order=None, script=None, allowance=30.0, topic=1):
    m = module()
    return m.Slot(
        slot_id=slot_id,
        provider=provider,
        required=required,
        order=order if order is not None else (topic, slot_id),
        role_allowance=allowance,
        identity={
            "run_id": "run-1",
            "input_state": "abc",
            "role": "researcher",
            "topic": topic,
            "endpoint": provider,
            "model": slot_id,
        },
        prompt=f"prompt for {slot_id}",
        payload=script if script is not None else f"print({slot_id!r},flush=True)",
    )


class Harness:
    """Launcher/gate stand-ins recording calls."""

    def __init__(self):
        self.launched = []
        self.allowances = {}
        self.procs = {}
        self.gated = []
        self.in_gate = 0
        self.max_in_gate = 0
        self.lock = threading.Lock()

    def launcher(self, slot, allowance):
        with self.lock:
            self.launched.append(slot.slot_id)
            self.allowances[slot.slot_id] = allowance
        proc = subprocess.Popen(
            [sys.executable, "-c", slot.payload],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        with self.lock:
            self.procs[slot.slot_id] = proc
        return proc

    def gate(self, slot):
        m = module()
        with self.lock:
            self.in_gate += 1
            self.max_in_gate = max(self.max_in_gate, self.in_gate)
            self.gated.append(slot.slot_id)
        time.sleep(0.01)
        with self.lock:
            self.in_gate -= 1
        return m.GateVerdict(blocked=False, record={"leak": "clean", "for": slot.slot_id})


def run(slots, harness, **kwargs):
    m = module()
    return m.dispatch(slots, gate=kwargs.pop("gate", harness.gate), launcher=harness.launcher, **kwargs)


def by_id(result):
    return {r.slot_id: r for r in result.results}


def max_overlap(results):
    spans = []
    for r in results:
        words = {}
        for line in r.stdout.splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[0] in ("start", "end"):
                words[parts[0]] = float(parts[1])
        if "start" in words and "end" in words:
            spans.append((words["start"], words["end"]))
    best = 0
    for start, _ in spans:
        best = max(best, sum(1 for s, e in spans if s <= start < e))
    return best


def test_four_permit_cap_is_provider_wide_across_roles_and_topics():
    h = Harness()
    slots = [make_slot(f"g{i}", topic=i % 3 + 1, script=sleeper(0.4)) for i in range(7)]
    slots += [make_slot(f"c{i}", provider="claude", script=sleeper(0.4)) for i in range(2)]
    result = run(slots, h)
    got = by_id(result)
    go = [r for k, r in got.items() if k.startswith("g")]
    assert all(r.outcome == "ok" for r in result.results)
    assert max_overlap(go) == 4  # saturated, never a fifth
    claude = [r for k, r in got.items() if k.startswith("c")]
    assert max_overlap(claude) == 2  # an independent queue, not blocked by Go
    assert result.exit_code == 0


def test_required_slots_launch_before_any_free_seat_then_declared_order():
    h = Harness()
    slots = [
        make_slot("free-b", required=False, order=(1, "b")),
        make_slot("free-a", required=False, order=(1, "a")),
        make_slot("req-2", order=(2, "x")),
        make_slot("req-1b", order=(1, "b")),
        make_slot("req-1a", order=(1, "a")),
    ]
    run(slots, h, per_provider_limit=1)
    assert h.launched == ["req-1a", "req-1b", "req-2", "free-a", "free-b"]


def test_free_slot_of_one_provider_waits_for_required_slots_of_another():
    # Criterion 19 (F-54): required-first holds across providers, not only inside one queue.
    h = Harness()
    slots = [make_slot(f"c{i}", provider="claude", order=(1, f"c{i}"), script=sleeper(0.3)) for i in range(8)]
    slots += [make_slot("g-req", order=(1, "a"), script=sleeper(0.01))]
    slots += [make_slot("g-free", required=False, order=(1, "z"), script=sleeper(0.01))]
    result = run(slots, h)
    assert result.exit_code == 0
    assert h.launched.index("g-free") > max(h.launched.index(f"c{i}") for i in range(8)), h.launched


def test_gate_called_once_per_prompt_and_never_concurrently():
    h = Harness()
    slots = [make_slot(f"s{i}", script=sleeper(0.05)) for i in range(10)]
    run(slots, h)
    assert sorted(h.gated) == sorted(s.slot_id for s in slots)
    assert h.max_in_gate == 1


def test_audit_writer_runs_under_the_gate_lock_before_launch():
    h = Harness()
    events = []

    def gate(slot):
        events.append(("gate-in", slot.slot_id))
        verdict = h.gate(slot)
        events.append(("gate-out", slot.slot_id))
        return verdict

    def audit(slot, _verdict):
        events.append(("audit", slot.slot_id))

    original = h.launcher

    def launcher(slot, allowance):
        events.append(("launch", slot.slot_id))
        return original(slot, allowance)

    m = module()
    m.dispatch([make_slot(f"s{i}") for i in range(4)], gate=gate, launcher=launcher, audit=audit, per_provider_limit=4)
    # One slot's gate, audit and launch are contiguous: no other slot interleaves.
    for i in range(0, len(events), 4):
        chunk = events[i : i + 4]
        assert [c[0] for c in chunk] == ["gate-in", "gate-out", "audit", "launch"]
        assert len({c[1] for c in chunk}) == 1


def test_block_cancels_queued_stops_and_reaps_running_and_keeps_partial(tmp_path):
    m = module()
    h = Harness()
    marker = tmp_path / "partial-written"
    long_script = f"import time,pathlib\nprint('partial-output',flush=True)\npathlib.Path({str(marker)!r}).write_text('x')\ntime.sleep(60)\n"

    def gate(slot):
        if slot.slot_id == "bad":
            for _ in range(200):
                if marker.exists():
                    break
                time.sleep(0.02)
            return m.GateVerdict(blocked=True, record={"leak": "BLOCK"})
        return h.gate(slot)

    slots = [
        make_slot("running", order=(1, "a"), script=long_script),
        make_slot("bad", order=(1, "b")),
        make_slot("queued-1", order=(2, "a")),
        make_slot("queued-2", order=(2, "b"), required=False),
    ]
    t0 = time.monotonic()
    result = m.dispatch(slots, gate=gate, launcher=h.launcher, per_provider_limit=2, grace=1.0)
    assert time.monotonic() - t0 < 10
    got = by_id(result)
    assert result.exit_code == 2
    assert got["running"].outcome == "cancelled" and got["running"].started is True
    assert "partial-output" in got["running"].stdout
    assert h.procs["running"].poll() is not None  # reaped
    assert got["bad"].outcome == "refused" and got["bad"].started is False
    for name in ("queued-1", "queued-2"):
        assert got[name].outcome == "cancelled" and got[name].started is False
        assert name not in h.launched


def test_block_prevents_next_slot_from_launching_even_with_free_permits():
    m = module()
    h = Harness()

    def gate(slot):
        if slot.slot_id == "bad":
            return m.GateVerdict(blocked=True, record={"leak": "BLOCK"})
        return h.gate(slot)

    slots = [make_slot("bad", order=(1, "a")), make_slot("next", order=(1, "b"))]
    result = m.dispatch(slots, gate=gate, launcher=h.launcher, per_provider_limit=4)
    assert h.launched == []
    assert by_id(result)["next"].outcome == "cancelled"
    assert result.exit_code == 2


def test_gate_exception_fails_closed_as_security_refusal():
    m = module()
    h = Harness()

    def gate(_slot):
        raise RuntimeError("declaration invalid")

    result = m.dispatch([make_slot("a")], gate=gate, launcher=h.launcher)
    assert h.launched == []
    assert by_id(result)["a"].outcome == "refused"
    assert result.exit_code == 2


def test_stop_set_during_gate_is_rechecked_before_launch():
    m = module()
    h = Harness()
    stop = threading.Event()

    def gate(slot):
        stop.set()  # an external cancel arrives while the long leak scan runs
        return h.gate(slot)

    result = m.dispatch([make_slot("a")], gate=gate, launcher=h.launcher, stop=stop)
    assert h.launched == []
    out = by_id(result)["a"]
    assert out.outcome == "cancelled" and out.started is False


def test_deadline_rechecked_after_gate_before_launch():
    m = module()
    h = Harness()
    now = {"t": 0.0}

    def gate(slot):
        now["t"] = 90.0  # the scan consumed the time before the reserve
        return h.gate(slot)

    result = m.dispatch(
        [make_slot("a"), make_slot("b", required=False)],
        gate=gate,
        launcher=h.launcher,
        deadline=100.0,
        reserve=15.0,
        clock=lambda: now["t"],
    )
    assert h.launched == []
    got = by_id(result)
    assert got["a"].outcome == "not-started-deadline" and got["a"].started is False
    assert result.exit_code == 1  # required slot not started


def test_no_launch_inside_reserve_and_free_not_started_is_not_incomplete():
    m = module()
    h = Harness()
    result = m.dispatch(
        [make_slot("free", required=False)],
        gate=h.gate,
        launcher=h.launcher,
        deadline=100.0,
        reserve=15.0,
        clock=lambda: 85.0,
    )
    assert h.launched == [] and h.gated == []
    assert by_id(result)["free"].outcome == "not-started-deadline"
    assert result.exit_code == 0


def test_child_allowance_is_lesser_of_role_and_remaining_before_reserve():
    m = module()
    h = Harness()
    m.dispatch(
        [make_slot("short", allowance=10.0), make_slot("long", allowance=600.0)],
        gate=h.gate,
        launcher=h.launcher,
        deadline=100.0,
        reserve=15.0,
        clock=lambda: 40.0,
    )
    assert h.allowances == {"short": 10.0, "long": 45.0}


def test_queue_wait_counts_against_total_and_child_times_out_at_allowance():
    h = Harness()
    now = time.monotonic()
    slots = [
        make_slot("first", order=(1, "a"), script=sleeper(30)),
        make_slot("second", order=(1, "b")),
    ]
    result = run(slots, h, per_provider_limit=1, deadline=now + 0.8, reserve=0.5, grace=0.5)
    got = by_id(result)
    assert got["first"].outcome == "timed-out" and got["first"].started is True
    assert h.procs["first"].poll() is not None
    assert "start" in got["first"].stdout  # partial output retained
    assert got["second"].outcome == "not-started-deadline"
    assert "second" not in h.launched
    assert result.exit_code == 1


def test_security_exit_overrides_incomplete_exit():
    m = module()
    h = Harness()

    def gate(slot):
        if slot.slot_id == "bad":
            time.sleep(0.2)  # let the failing sibling finish first
            return m.GateVerdict(blocked=True, record={"leak": "BLOCK"})
        return h.gate(slot)

    slots = [
        make_slot("fails", order=(1, "a"), script="import sys;sys.exit(3)"),
        make_slot("bad", order=(1, "b")),
    ]
    result = m.dispatch(slots, gate=gate, launcher=h.launcher)
    assert by_id(result)["fails"].outcome == "failed"
    assert result.exit_code == 2


def test_ordinary_failure_lets_siblings_finish_without_retry():
    h = Harness()
    slots = [
        make_slot("fails", order=(1, "a"), script="import sys;print('oops');sys.exit(3)"),
        make_slot("sibling", order=(1, "b"), script=sleeper(0.3)),
        make_slot("free-fails", required=False, script="import sys;sys.exit(1)"),
    ]
    result = run(slots, h)
    got = by_id(result)
    assert got["fails"].outcome == "failed" and got["fails"].returncode == 3
    assert got["sibling"].outcome == "ok"
    assert h.launched.count("fails") == 1 and h.launched.count("free-fails") == 1
    assert result.exit_code == 1


def test_free_failure_alone_is_exit_zero():
    h = Harness()
    result = run(
        [make_slot("req"), make_slot("free", required=False, script="import sys;sys.exit(1)")],
        h,
    )
    assert by_id(result)["free"].outcome == "failed"
    assert result.exit_code == 0


def test_launcher_error_is_a_failed_unstarted_slot():
    m = module()
    h = Harness()

    def launcher(_slot, _allowance):
        raise OSError("no such program")

    result = m.dispatch([make_slot("a")], gate=h.gate, launcher=launcher)
    out = by_id(result)["a"]
    assert out.outcome == "failed" and out.started is False
    assert result.exit_code == 1


def test_every_slot_one_terminal_outcome_and_own_identity_under_concurrency():
    m = module()
    h = Harness()
    slots = []
    for i in range(14):
        script = f"import sys,time;time.sleep(0.05);print('me-{i}',flush=True);sys.exit({0 if i % 3 else 5})"
        slots.append(make_slot(f"s{i}", required=i % 2 == 0, topic=i % 4, script=script))
    result = m.dispatch(slots, gate=h.gate, launcher=h.launcher)
    assert sorted(r.slot_id for r in result.results) == sorted(s.slot_id for s in slots)
    assert len(result.audit_records) == len(slots)
    for r in result.results:
        i = int(r.slot_id[1:])
        assert f"me-{i}" in r.stdout
        assert r.outcome == ("ok" if i % 3 else "failed")  # failure never audited as success
        assert r.identity["model"] == r.slot_id
        assert r.gate_record == {"leak": "clean", "for": r.slot_id}
    records = {rec["slot_id"]: rec for rec in result.audit_records}
    assert len(records) == len(slots)
    for r in result.results:
        rec = records[r.slot_id]
        assert rec["outcome"] == r.outcome and rec["leak_check"] == r.gate_record
        assert rec["run_id"] == "run-1" and rec["model"] == r.slot_id and "topic" in rec


def test_results_are_immutable():
    h = Harness()
    result = run([make_slot("a")], h)
    try:
        result.results[0].outcome = "ok"
    except Exception as exc:  # FrozenInstanceError
        assert type(exc).__name__ == "FrozenInstanceError"
    else:
        raise AssertionError("result must be frozen")


def test_audit_failure_fails_closed_without_launch_and_drains_queue():
    m = module()
    h = Harness()

    def audit(_slot, _verdict):
        raise OSError("disk full")

    slots = [make_slot("a", order=(1, "a")), make_slot("b", order=(1, "b"))]
    result = m.dispatch(slots, gate=h.gate, launcher=h.launcher, audit=audit, per_provider_limit=1)
    got = by_id(result)
    assert h.launched == []
    assert got["a"].outcome == "refused" and got["a"].started is False
    assert "disk full" in str(got["a"].gate_record)
    assert got["b"].outcome == "cancelled"
    assert result.exit_code == 2


def test_unexpected_supervise_error_reaps_child_and_worker_continues():
    m = module()
    h = Harness()

    class Exploding:
        """Popen wrapper whose first communicate() call raises unexpectedly."""

        def __init__(self, proc):
            self.proc = proc
            self.calls = 0

        def __getattr__(self, name):
            return getattr(self.proc, name)

        def communicate(self, timeout=None):
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("boom")
            return self.proc.communicate(timeout=timeout)

    def launcher(slot, allowance):
        proc = h.launcher(slot, allowance)
        return Exploding(proc) if slot.slot_id == "a" else proc

    slots = [
        make_slot("a", order=(1, "a"), script="import time;print('part',flush=True);time.sleep(60)"),
        make_slot("b", order=(1, "b")),
    ]
    result = m.dispatch(slots, gate=h.gate, launcher=launcher, per_provider_limit=1, grace=0.5)
    got = by_id(result)
    assert got["a"].outcome == "failed" and got["a"].started is True
    assert h.procs["a"].poll() is not None
    assert got["b"].outcome == "ok"


@pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning")
def test_final_guard_gives_every_slot_a_terminal_outcome():
    m = module()
    h = Harness()

    def audit(_slot, _verdict):
        raise BaseException("worker-killing")  # noqa: TRY002

    # A BaseException escapes the per-slot handlers and kills the worker thread.
    slots = [make_slot("a", order=(1, "a")), make_slot("b", order=(1, "b"))]
    result = m.dispatch(slots, gate=h.gate, launcher=h.launcher, audit=audit, per_provider_limit=1)
    assert sorted(r.slot_id for r in result.results) == ["a", "b"]
    assert all(r.outcome in m.OUTCOMES for r in result.results)
    assert result.exit_code in (1, 2)


def test_reap_does_not_hang_without_new_session_and_ignored_sigterm():
    m = module()
    script = (
        "import signal,time\nsignal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
        "print('partial',flush=True)\ntime.sleep(60)\n"
    )
    procs = {}

    def launcher(slot, _allowance):
        proc = subprocess.Popen(
            [sys.executable, "-c", slot.payload], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        procs[slot.slot_id] = proc
        return proc

    t0 = time.monotonic()
    result = m.dispatch(
        [make_slot("a", script=script, allowance=0.5)],
        gate=Harness().gate,
        launcher=launcher,
        grace=0.5,
    )
    assert time.monotonic() - t0 < 10
    assert by_id(result)["a"].outcome == "timed-out"
    assert procs["a"].poll() is not None


def test_cancellation_kills_a_descendant_that_ignores_sigterm_after_the_leader_exited(tmp_path):
    """F-34: the group leader dies on SIGTERM, a grandchild ignores it; the whole group must be gone."""
    m = module()
    pid_file = tmp_path / "grandchild.pid"
    child_code = (
        "import signal,time\nsignal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
        f"open({str(pid_file)!r}, 'w').write(str(__import__('os').getpid()))\ntime.sleep(60)\n"
    )
    script = (
        "import subprocess,sys,time\n"
        f"subprocess.Popen([sys.executable, '-c', {child_code!r}])\n"
        f"while not __import__('os').path.exists({str(pid_file)!r}) or not open({str(pid_file)!r}).read():\n"
        "    time.sleep(0.02)\n"
        "print('ready',flush=True)\ntime.sleep(60)\n"
    )
    h = Harness()
    result = m.dispatch([make_slot("a", script=script, allowance=3.0)], gate=h.gate, launcher=h.launcher, grace=0.5)
    assert by_id(result)["a"].outcome == "timed-out"
    grandchild = int(pid_file.read_text())
    alive = True
    for _ in range(100):
        try:
            os.kill(grandchild, 0)
        except ProcessLookupError:
            alive = False
            break
        time.sleep(0.05)
    if alive:
        os.kill(grandchild, signal.SIGKILL)
    assert not alive, "a descendant that ignores SIGTERM survived the cancellation"


# --- Q-13: the on_terminal callback and a failed state-store write ---------------------------------


def test_terminal_callback_precedes_the_workers_next_launch():
    """One worker: each slot's callback has returned before the next slot is launched."""
    h = Harness()
    events = []
    lock = threading.Lock()
    real_launcher = h.launcher

    def launcher(slot, allowance):
        with lock:
            events.append(("launch", slot.slot_id))
        return real_launcher(slot, allowance)

    def on_terminal(slot, _result):
        with lock:
            events.append(("terminal-start", slot.slot_id))
        time.sleep(0.2)  # a blocking callback holds the worker back
        with lock:
            events.append(("terminal-end", slot.slot_id))

    m = module()
    slots = [make_slot(f"s{i}", order=(i,)) for i in range(3)]
    result = m.dispatch(slots, gate=h.gate, launcher=launcher, on_terminal=on_terminal, per_provider_limit=1)
    assert result.exit_code == 0
    assert events == [
        step for i in range(3) for step in (("launch", f"s{i}"), ("terminal-start", f"s{i}"), ("terminal-end", f"s{i}"))
    ]


def test_terminal_callback_covers_cancelled_refused_and_not_started_slots():
    h = Harness()
    seen = {}
    m = module()

    def gate(slot):
        return m.GateVerdict(blocked=slot.slot_id == "bad", record={"leak": "x"})

    slots = [make_slot("ok1", order=(1,)), make_slot("bad", order=(2,)), make_slot("after", order=(3,))]
    result = m.dispatch(
        slots,
        gate=gate,
        launcher=h.launcher,
        on_terminal=lambda slot, r: seen.setdefault(slot.slot_id, r.outcome),
        per_provider_limit=1,
    )
    assert seen == {"ok1": "ok", "bad": "refused", "after": "cancelled"}
    assert result.exit_code == 2


def test_failed_terminal_write_stops_the_stage_with_exit_one():
    h = Harness()
    m = module()
    calls = []

    def on_terminal(slot, _result):
        calls.append(slot.slot_id)
        if slot.slot_id == "s0":
            error = OSError("disk full")
            error.stage_stop_reason = "state-store-unwritable"
            raise error

    slots = [
        make_slot("s0", order=(0,), script=sleeper(0.05)),
        make_slot("long", provider="claude", order=(0,), script=sleeper(30)),
        make_slot("s1", order=(1,)),
        make_slot("s2", order=(2,)),
    ]
    started = time.monotonic()
    result = m.dispatch(slots, gate=h.gate, launcher=h.launcher, on_terminal=on_terminal, per_provider_limit=1)
    assert time.monotonic() - started < 15  # the running child was stopped and reaped, not waited for
    assert result.exit_code == 1
    assert result.reason == "state-store-unwritable"
    assert "disk full" in result.detail
    got = by_id(result)
    assert got["s1"].outcome == "cancelled" and got["s2"].outcome == "cancelled"
    assert "s1" not in h.launched and "s2" not in h.launched
    assert got["long"].outcome == "cancelled" and got["long"].started
    assert "start" in got["long"].stdout  # partial output kept
    assert calls == ["s0"]  # nothing is written after the store failed


def test_a_failed_launch_record_write_stops_without_launching_that_slot():
    h = Harness()
    m = module()

    def audit(slot, _verdict):
        if slot.slot_id == "s1":
            error = OSError("disk full")
            error.stage_stop_reason = "state-store-unwritable"
            raise error

    slots = [make_slot("s0", order=(0,)), make_slot("s1", order=(1,)), make_slot("s2", order=(2,))]
    result = m.dispatch(slots, gate=h.gate, launcher=h.launcher, audit=audit, per_provider_limit=1)
    assert result.exit_code == 1 and result.reason == "state-store-unwritable"
    assert "s1" not in h.launched and "s2" not in h.launched
    assert by_id(result)["s1"].outcome == "cancelled"


def test_a_raising_terminal_callback_with_a_security_refusal_exits_two():
    h = Harness()
    m = module()

    def on_terminal(_slot, _result):
        raise OSError("disk full")

    def gate(slot):
        return m.GateVerdict(blocked=slot.slot_id == "bad", record={})

    slots = [make_slot("bad", provider="claude", order=(0,)), make_slot("s0", order=(0,), script=sleeper(0.3))]
    result = m.dispatch(slots, gate=gate, launcher=h.launcher, on_terminal=on_terminal)
    assert result.exit_code == 2


def test_cancellation_kills_group_after_leader_was_already_reaped():
    """F-44: cancellation still owns a surviving group after its leader was reaped."""
    m = module()
    script = (
        "import os,signal,time\n"
        "if os.fork() == 0:\n"
        "    signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
        "    print(os.getpid(), flush=True)\n"
        "    time.sleep(60)\n"
        "else:\n"
        "    os._exit(0)\n"
    )
    proc = subprocess.Popen(
        [sys.executable, "-c", script],
        start_new_session=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    descendant = int(proc.stdout.readline())
    proc.wait(timeout=5)  # the process group leader is gone before cancellation starts
    try:
        out, err = m._stop_and_reap(proc, 0.1)
        assert (out, err) == ("", "")
        alive = True
        for _ in range(100):
            try:
                os.kill(descendant, 0)
            except ProcessLookupError:
                alive = False
                break
            time.sleep(0.05)
        assert not alive, "the reaped leader's descendant survived cancellation"
    finally:
        with contextlib.suppress(ProcessLookupError):
            os.kill(descendant, signal.SIGKILL)
