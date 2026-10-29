"""The machine-wide verification admission: what queues, what nests, what refuses.

`scripts.verify_lock` queues independent protected entries of one user on one
machine, checks free memory before work starts, and lets nested work inherit
its ancestor's admission. Every case here builds its own state root, so no
test touches the real machine lock or waits on this checkout's own
verification; each docstring names the fault it was written against — planting
it turned exactly this test red.
"""

from __future__ import annotations

import contextlib
import fcntl
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import verify_lock  # noqa: E402

# One protected body, run as a supervised child: it records its pid before the
# work, then the interval it ran in — so tests can compare intervals of
# independent admissions.
RECORD_BODY = """
import json, os, time
from pathlib import Path
start = time.time()
started = os.environ.get("PROBE_STARTED")
if started:
    Path(started).write_text(str(os.getpid()))
time.sleep(float(os.environ.get("PROBE_SLEEP", "0")))
out = os.environ.get("PROBE_OUT")
if out:
    Path(out).write_text(json.dumps({"start": start, "end": time.time()}))
"""

# One protected body that appends its name — the order of these lines is the
# admission order of independent entries.
ORDER_BODY = """
import os
with open(os.environ["PROBE_LOG"], "a", encoding="utf-8") as handle:
    handle.write(os.environ["PROBE_NAME"] + chr(10))
"""

# An entry that holds admission through the context, the way scripts.stage2
# holds it around its timed checks: a different entry kind against the same
# shared state.
DIRECT_BODY = """
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import verify_lock
with verify_lock.hold_admission(["direct-entry"]) as owned:
    assert owned is not None, "an independent admission must own the lock"
    start = time.time()
    time.sleep(float(os.environ.get("PROBE_SLEEP", "0.3")))
    Path(os.environ["PROBE_OUT"]).write_text(json.dumps({"start": start, "end": time.time()}))
"""


def _env(state: Path, extra: dict[str, str] | None = None) -> dict[str, str]:
    """The environment of an independent entry: its own state root, floor zero.

    The floor of zero keeps these regressions about admission, not about the
    memory of the machine that happens to run them.
    """
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(state.parent),
        "XDG_STATE_HOME": str(state),
        verify_lock.FLOOR_ENV: "0",
    }
    env.update(extra or {})
    return env


def _supervised(state: Path, body: str, extra: dict[str, str] | None = None) -> subprocess.Popen[bytes]:
    """One independent supervisor entry against an isolated state root."""
    return subprocess.Popen(
        [sys.executable, "-m", "scripts.verify_lock", "--", sys.executable, "-c", body],
        cwd=REPO_ROOT,
        env=_env(state, extra),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _context_entry(state: Path, out: Path, sleep: str = "0.3") -> subprocess.Popen[bytes]:
    """One entry holding admission through the context, the way scripts.stage2 does."""
    return subprocess.Popen(
        [sys.executable, "-c", DIRECT_BODY],
        cwd=REPO_ROOT,
        env=_env(state, {"PROBE_OUT": str(out), "PROBE_SLEEP": sleep}),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


@contextlib.contextmanager
def fake_holder(state: Path, *, pid: int | None = None, publish: bool = True, hold: bool = True) -> Iterator[None]:
    """Hold the machine lock the way a published admission does.

    With `publish` the holder record names a pid (the test's own unless given),
    with `hold` the work lock is genuinely flocked — the two apart build the
    stale shape, a published pid nobody holds the lock for.
    """
    root = state / "coding-harness"
    root.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(root / verify_lock.LOCK_NAME, os.O_RDWR | os.O_CREAT | os.O_NONBLOCK, 0o600)
    holder = root / verify_lock.HOLDER_NAME
    if publish:
        holder.write_text(
            json.dumps(
                {
                    "pid": os.getpid() if pid is None else pid,
                    "command": ["fake", "holder"],
                    "start": "2026-10-29T00:00:00",
                }
            ),
            encoding="utf-8",
        )
    try:
        if hold:
            fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        with contextlib.suppress(OSError):
            holder.unlink()
        if hold:
            with contextlib.suppress(OSError):
                fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _records(state: Path) -> list[str]:
    """The queue records as they stand, without creating anything."""
    queue = state / "coding-harness" / verify_lock.QUEUE_DIR
    try:
        return sorted(os.listdir(queue))
    except FileNotFoundError:
        return []


def _wait_until(predicate: Callable[[], object], seconds: float = 10.0) -> bool:
    """Poll a condition for a bounded real time."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.05)
    return bool(predicate())


def _interval(out: Path) -> tuple[float, float]:
    """The recorded start and end of one entry's protected work."""
    record = json.loads(out.read_text(encoding="utf-8"))
    return (record["start"], record["end"])


# ---------------------------------------------------------------------------
# Criterion 1 — one machine, one admission at a time
# ---------------------------------------------------------------------------


def test_independent_entries_share_one_machine_lock(tmp_path: Path) -> None:
    """Independent admissions run their protected work one at a time.

    Fault this pins: an admission that locks nothing lets two supervisor
    entries and a stage-2-style context entry overlap their protected
    intervals against one shared state root — the three-lane trial's overload.
    """
    state = tmp_path / "state"
    outs = [tmp_path / f"entry-{index}.json" for index in range(3)]
    entries = [
        _supervised(state, RECORD_BODY, {"PROBE_OUT": str(outs[0]), "PROBE_SLEEP": "0.4"}),
        _supervised(state, RECORD_BODY, {"PROBE_OUT": str(outs[1]), "PROBE_SLEEP": "0.4"}),
        _context_entry(state, outs[2]),
    ]
    for entry in entries:
        assert entry.wait(timeout=60) == 0
    spans = sorted(_interval(out) for out in outs)
    for (_, previous_end), (start, _) in zip(spans, spans[1:], strict=False):
        assert start >= previous_end - 0.05, f"protected intervals overlap: {spans}"


# ---------------------------------------------------------------------------
# Criterion 2 — registration order is admission order
# ---------------------------------------------------------------------------


def test_live_waiters_enter_in_registration_order(tmp_path: Path) -> None:
    """A later registration never overtakes an earlier live waiter.

    Fault this pins: turn-taking that trusts the work lock's own wake-up order
    (flock supplies no FIFO) lets the second registered entry grab the lock
    first when the holder releases.
    """
    state = tmp_path / "state"
    log = tmp_path / "order.log"
    extra = lambda name: {"PROBE_LOG": str(log), "PROBE_NAME": name, "PROBE_SLEEP": "0.2"}  # noqa: E731
    with fake_holder(state):
        first = _supervised(state, ORDER_BODY, extra("first"))
        assert _wait_until(lambda: len(_records(state)) >= 1), "the first entry never registered"
        second = _supervised(state, ORDER_BODY, extra("second"))
        assert _wait_until(lambda: len(_records(state)) >= 2), "the second entry never registered"
        by_pid = {first.pid: "first", second.pid: "second"}
        sequence: dict[str, int] = {}
        for record in _records(state):
            matched = verify_lock.RECORD_NAME.fullmatch(record)
            assert matched is not None, record
            sequence[by_pid[int(matched.group(2))]] = int(matched.group(1))
        # The test registered "first" before it spawned "second": that is the real order, and the
        # queue's own numbering must agree with it, never stand in for it (review row L3-2).
        assert sequence["first"] < sequence["second"], f"the queue numbered against registration order: {sequence}"
        expected = ["first", "second"]
    for entry in (first, second):
        assert entry.wait(timeout=60) == 0
    assert log.read_text(encoding="utf-8").split() == expected, (
        f"admission order {log.read_text(encoding='utf-8').split()} left registration order {expected}"
    )


# ---------------------------------------------------------------------------
# Criterion 3 — the wait is logged, with the holder's identity
# ---------------------------------------------------------------------------


def test_queue_wait_logs_live_holder_and_progress(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A waiter logs immediately and every five minutes, naming pid, command and start.

    Fault this pins: a silent wait, a missing progress update, a holder
    described without its identity despite published metadata — and a wait
    with no active holder that does not say so.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "QUEUE_LOG_SECONDS", 0.05)
    monkeypatch.setattr(verify_lock, "QUEUE_POLL_SECONDS", 0.01)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)

    seen: list[str] = []

    def drain() -> list[str]:
        """Everything logged so far: capsys hands each line over once, so keep what it gave."""
        seen.extend(capsys.readouterr().err.splitlines())
        return seen

    def waiting_lines() -> list[str]:
        return [line for line in drain() if "waiting for admission" in line]

    with fake_holder(state):
        admitted = threading.Event()

        def waiter() -> None:
            with verify_lock.hold_admission(["waiter", "body"]):
                admitted.set()

        thread = threading.Thread(target=waiter)
        thread.start()
        assert _wait_until(lambda: len(waiting_lines()) >= 2), "the wait was not logged with progress"
        first = waiting_lines()[0]
        for expected in (str(os.getpid()), "fake holder", "2026-10-29T00:00:00"):
            assert expected in first, f"the holder identity is missing from the wait log: {first}"
    assert admitted.wait(10.0), "the waiter was never admitted"
    thread.join(10.0)
    assert re.search(r"\[verify-lock\] admitted", "\n".join(drain())), "the admission was not logged"

    with fake_holder(state, publish=False):
        anonymous = threading.Event()

        def second_waiter() -> None:
            with verify_lock.hold_admission(["waiter", "two"]):
                anonymous.set()

        thread_two = threading.Thread(target=second_waiter)
        thread_two.start()
        assert _wait_until(lambda: any("no active holder is published" in line for line in drain())), (
            "a wait without a published holder was not reported as such"
        )
    assert anonymous.wait(10.0), "the second waiter was never admitted"
    thread_two.join(10.0)


# ---------------------------------------------------------------------------
# Criterion 5 — only live ancestor ownership admits nested work
# ---------------------------------------------------------------------------


def test_only_live_ancestor_ownership_allows_nested_admission(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A valid marker inherits its ancestor's admission; every false shape uses ordinary admission.

    Fault this pins: a nested entry that queues again (self-deadlock) or
    rechecks memory, and an absent, malformed, unrelated or stale marker that
    bypasses admission.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    reads: list[float] = []

    def counting_reader(_platform: str | None = None) -> float | None:
        reads.append(1.0)
        return 1.0

    # valid, in-process: no queue, no memory wait, no descriptor of its own
    monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
    monkeypatch.setattr(verify_lock, "read_available_memory", counting_reader)
    with fake_holder(state, pid=os.getpid()), verify_lock.hold_admission(["nested", "body"]) as owned:
        assert owned is None, "a nested entry must inherit, not own"
    assert reads == [], "a nested entry rechecked memory"
    monkeypatch.delenv(verify_lock.LOCK_ENV)

    # valid, as the shell entry sees it: the supervised nested run completes inside the admission.
    # The child's own environment carries the marker — verify_all.sh publishes it to the command
    # it supervises, so an independently started process env must name it too.
    with fake_holder(state, pid=os.getpid()):
        monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
        out = tmp_path / "nested.json"
        entry = _supervised(
            state,
            RECORD_BODY,
            {"PROBE_OUT": str(out), "PROBE_SLEEP": "0.2", verify_lock.LOCK_ENV: str(os.getpid())},
        )
        assert entry.wait(timeout=60) == 0
        assert out.is_file(), "a validly nested entry could not run inside its ancestor's admission"
    monkeypatch.delenv(verify_lock.LOCK_ENV)

    # absent, malformed and unrelated markers take ordinary admission: queued behind the holder
    unrelated = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)"])
    queued: list[subprocess.Popen[bytes]] = []
    try:
        with fake_holder(state):
            for index, marker in enumerate((None, "not-a-pid", str(unrelated.pid))):
                if marker is None:
                    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
                else:
                    monkeypatch.setenv(verify_lock.LOCK_ENV, marker)
                out = tmp_path / f"ordinary-{index}.json"
                entry = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(out), "PROBE_SLEEP": "0.2"})
                queued.append(entry)
                assert not _wait_until(out.is_file, 1.0), f"marker {marker!r} bypassed a live holder's admission"
        for entry in queued:
            assert entry.wait(timeout=60) == 0
    finally:
        unrelated.kill()
        unrelated.wait(timeout=10)
    monkeypatch.delenv(verify_lock.LOCK_ENV)

    # stale — a marker whose admission released: the memory gate runs like anyone else's
    monkeypatch.delenv(verify_lock.FLOOR_ENV, raising=False)
    monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
    ticks = iter(range(0, 4000, int(verify_lock.MEMORY_POLL_SECONDS)))
    monkeypatch.setattr(verify_lock, "_now", lambda: next(ticks))
    monkeypatch.setattr(verify_lock, "_sleep", lambda _seconds: None)
    with (
        fake_holder(state, pid=os.getpid(), hold=False),
        pytest.raises(verify_lock.MemoryFloorRefused),
        verify_lock.hold_admission(["stale", "marker"]),
    ):
        pass
    assert reads, "the stale marker bypassed the memory gate"


# ---------------------------------------------------------------------------
# Criterion 6 — dead participants never block; ownership outlives the supervisor
# ---------------------------------------------------------------------------


def test_exit_interrupt_and_dead_waiter_release_admission(tmp_path: Path) -> None:
    """Dead participants never block, and ownership outlives a killed supervisor exactly so long.

    Fault this pins: a dead holder or waiter blocking progress forever, a
    signal releasing the lock before the child's group is gone, and a
    supervisor releasing ownership while its protected child still runs.
    """
    state = tmp_path / "state"
    holder_file = state / "coding-harness" / verify_lock.HOLDER_NAME

    # a holder killed mid-run cannot obstruct the next admission
    started = tmp_path / "started-a.json"
    victim = _supervised(state, RECORD_BODY, {"PROBE_SLEEP": "30", "PROBE_STARTED": str(started)})
    assert _wait_until(holder_file.is_file), "the victim never acquired admission"
    assert _wait_until(started.is_file), "the victim never started its protected child"
    child_pid = int(started.read_text(encoding="utf-8"))
    os.kill(victim.pid, signal.SIGKILL)
    os.kill(child_pid, signal.SIGKILL)
    victim.wait(timeout=10)
    after = tmp_path / "after-a.json"
    survivor = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(after), "PROBE_SLEEP": "0.1"})
    assert survivor.wait(timeout=60) == 0 and after.is_file(), "a dead holder blocked the next admission"

    # a waiter killed in the queue cannot obstruct the survivors either
    with fake_holder(state):
        waiter = _supervised(state, RECORD_BODY, {"PROBE_SLEEP": "30"})
        assert _wait_until(lambda: len(_records(state)) >= 1), "the waiter never registered"
        os.kill(waiter.pid, signal.SIGKILL)
        waiter.wait(timeout=10)
    after_two = tmp_path / "after-b.json"
    follower = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(after_two), "PROBE_SLEEP": "0.1"})
    assert follower.wait(timeout=60) == 0 and after_two.is_file(), "a dead waiter blocked the survivor"

    # SIGTERM: the child's group is cleaned up, then the lock is released
    started_c = tmp_path / "started-c.json"
    out_c = tmp_path / "child-c.json"
    interrupted = _supervised(
        state, RECORD_BODY, {"PROBE_SLEEP": "5", "PROBE_STARTED": str(started_c), "PROBE_OUT": str(out_c)}
    )
    assert _wait_until(started_c.is_file), "the interrupted entry never started its protected child"
    child_c = int(started_c.read_text(encoding="utf-8"))
    os.kill(interrupted.pid, signal.SIGTERM)
    assert interrupted.wait(timeout=30) == 128 + signal.SIGTERM, "the supervisor did not report its signal"
    assert not out_c.is_file(), "the protected child outlived its cleanup"
    with pytest.raises(ProcessLookupError):
        os.kill(child_c, 0)
    after_c = tmp_path / "after-c.json"
    next_run = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(after_c), "PROBE_SLEEP": "0.1"})
    assert next_run.wait(timeout=60) == 0 and after_c.is_file(), "the lock was not reusable after SIGTERM"

    # SIGKILL of the supervisor alone: the orphaned child keeps ownership until its work ends
    started_d = tmp_path / "started-d.json"
    out_d = tmp_path / "child-d.json"
    killed = _supervised(
        state, RECORD_BODY, {"PROBE_SLEEP": "1.2", "PROBE_STARTED": str(started_d), "PROBE_OUT": str(out_d)}
    )
    assert _wait_until(started_d.is_file), "the killed entry never started its protected child"
    os.kill(killed.pid, signal.SIGKILL)
    killed.wait(timeout=10)
    after_d = tmp_path / "after-d.json"
    successor = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(after_d), "PROBE_SLEEP": "0.1"})
    assert successor.wait(timeout=60) == 0 and after_d.is_file(), "the successor could not follow the orphaned child"
    child_span, successor_span = _interval(out_d), _interval(after_d)
    assert successor_span[0] >= child_span[1] - 0.05, (
        f"the successor ran while the orphaned child still held the admission: {child_span} then {successor_span}"
    )


# ---------------------------------------------------------------------------
# Criterion 7 — the declared memory sources, the declared percentages
# ---------------------------------------------------------------------------


def test_platform_memory_readers_use_the_declared_percentage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """macOS's system-wide free percentage and Linux MemAvailable over MemTotal, nothing else.

    Fault this pins: another macOS percentage read, Linux `MemFree`
    substituted, or a malformed value accepted as a reading.
    """
    monkeypatch.setattr(
        verify_lock, "_memory_probe_output", lambda _command: "System wide memory free percentage: 62%\n"
    )
    assert verify_lock.read_available_memory("darwin") == 62.0
    monkeypatch.setattr(
        verify_lock, "_memory_probe_output", lambda _command: "System wide memory wired percentage: 30%\n"
    )
    assert verify_lock.read_available_memory("darwin") is None
    monkeypatch.setattr(verify_lock, "_memory_probe_output", lambda _command: "free percentage: half\n")
    assert verify_lock.read_available_memory("darwin") is None

    meminfo = tmp_path / "meminfo"
    meminfo.write_text(
        "MemTotal:        4000000 kB\nMemFree:        3500000 kB\nMemAvailable:    3000000 kB\n", encoding="utf-8"
    )
    monkeypatch.setattr(verify_lock, "MEMINFO_PATH", meminfo)
    assert verify_lock.read_available_memory("linux") == 75.0
    meminfo.write_text("MemTotal:        4000000 kB\nMemFree:        3500000 kB\n", encoding="utf-8")
    assert verify_lock.read_available_memory("linux") is None
    meminfo.write_text(
        "MemTotal:        4000000 kB\nMemAvailable:    3000000 kB\nHugePages_Total:       0\n", encoding="utf-8"
    )
    assert verify_lock.read_available_memory("linux") == 75.0
    assert verify_lock.read_available_memory("win32") is None


# ---------------------------------------------------------------------------
# Criterion 8 — below the floor: exclusion held, rechecks and logs every 30 s
# ---------------------------------------------------------------------------


def test_low_memory_wait_holds_exclusion_and_rechecks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """While readings sit below the floor, admission keeps the lock and rechecks every 30 seconds.

    Fault this pins: protected work starting on a below-floor reading, the
    exclusion dropped during the wait, or the 30-second rechecks and logs
    stopping.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.setenv(verify_lock.FLOOR_ENV, "25")
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    ticks = iter(range(0, 10**9, int(verify_lock.MEMORY_POLL_SECONDS)))
    monkeypatch.setattr(verify_lock, "_now", lambda: next(ticks))
    waits: list[float] = []
    reads: list[float] = []
    entered_gate = threading.Event()
    release = threading.Event()

    def fake_sleep(seconds: float) -> None:
        if seconds == verify_lock.MEMORY_POLL_SECONDS:
            waits.append(seconds)
        time.sleep(0.01)

    def reader(_platform: str | None = None) -> float | None:
        if release.is_set():
            return 30.0
        entered_gate.set()
        reads.append(10.0)
        return 10.0

    monkeypatch.setattr(verify_lock, "_sleep", fake_sleep)
    monkeypatch.setattr(verify_lock, "read_available_memory", reader)

    started = threading.Event()
    second_started = threading.Event()

    def first() -> None:
        with verify_lock.hold_admission(["first", "work"]):
            started.set()

    def second() -> None:
        with verify_lock.hold_admission(["second", "work"]):
            second_started.set()

    thread = threading.Thread(target=first)
    other = threading.Thread(target=second)
    try:
        thread.start()
        assert entered_gate.wait(10.0), "the first admission never reached the memory gate"
        other.start()
        assert not second_started.wait(0.5), "another admission entered while the first waited for memory"
        release.set()
        assert started.wait(10.0), "a sufficient reading did not start the work"
        assert second_started.wait(10.0), "the second admission never entered after the first finished"
    finally:
        release.set()
        thread.join(10.0)
        if other.is_alive():
            other.join(10.0)
    assert reads, "the memory gate never rechecked"
    assert waits and all(value == verify_lock.MEMORY_POLL_SECONDS for value in waits), waits
    err = capsys.readouterr().err
    assert err.count("below the 25% floor") >= 2, "the low-memory wait was not logged per recheck"


# ---------------------------------------------------------------------------
# Criterion 9 — the bound refuses; recovery before it starts
# ---------------------------------------------------------------------------


def test_sustained_low_memory_refuses_at_the_bound(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Readings below the floor for the whole hour refuse, naming the floor and the last reading.

    Fault this pins: an unbounded low-memory wait, a refusal before the bound,
    or a refusal without the two percentages.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.FLOOR_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: 10.0)
    ticks = iter(range(0, 10**9, int(verify_lock.MEMORY_POLL_SECONDS)))
    monkeypatch.setattr(verify_lock, "_now", lambda: next(ticks))
    waits: list[float] = []
    monkeypatch.setattr(verify_lock, "_sleep", waits.append)
    ran = False
    with pytest.raises(verify_lock.MemoryFloorRefused) as raised, verify_lock.hold_admission(["never", "starts"]):
        ran = True
    assert not ran, "protected work started on a refused admission"
    assert len(waits) == int(verify_lock.MEMORY_DEADLINE_SECONDS // verify_lock.MEMORY_POLL_SECONDS), (
        f"the refusal came after {len(waits)} rechecks, not at the bound"
    )
    message = str(raised.value)
    assert "25" in message and "10" in message, f"the refusal does not name floor and last reading: {message}"


def test_memory_recovery_before_deadline_starts_work(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A qualifying reading before the deadline admits instead of refusing.

    Fault this pins: a refusal although memory recovered, or a recovered
    reading that never starts the work.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.FLOOR_ENV, raising=False)
    readings = iter([10.0, 10.0, 10.0, 40.0])
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: next(readings))
    ticks = iter(range(0, 10**9, int(verify_lock.MEMORY_POLL_SECONDS)))
    monkeypatch.setattr(verify_lock, "_now", lambda: next(ticks))
    waits: list[float] = []
    monkeypatch.setattr(verify_lock, "_sleep", waits.append)
    ran = False
    with verify_lock.hold_admission(["recovered", "work"]) as owned:
        ran = True
        assert owned is not None, "a fresh admission must own the lock"
    assert ran, "recovered memory never started the work"
    assert waits == [verify_lock.MEMORY_POLL_SECONDS] * 3, waits


# ---------------------------------------------------------------------------
# Criterion 10 — unknown memory is logged, not fatal, not trusted
# ---------------------------------------------------------------------------


def test_unknown_memory_is_logged_and_does_not_block(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An unavailable, failed, hung, unsupported or malformed probe is logged unknown and proceeds.

    Fault this pins: any of those hanging or refusing the run, or being
    silently treated as a valid percentage.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    waits: list[float] = []
    monkeypatch.setattr(verify_lock, "_sleep", waits.append)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)
    ran = False
    with verify_lock.hold_admission(["unknown", "memory"]) as owned:
        ran = True
        assert owned is not None
    assert ran and waits == [], "an unknown reading waited or refused"
    assert "cannot be measured" in capsys.readouterr().err, "the unknown reading was not logged"

    def hung(command: list[str], **_kwargs: object) -> object:
        raise subprocess.TimeoutExpired(cmd=command, timeout=1)

    def failed(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="")

    def unsupported(_command: list[str], **_kwargs: object) -> object:
        raise OSError("no such file")

    for broken in (hung, failed, unsupported):
        monkeypatch.setattr(verify_lock.subprocess, "run", broken)
        assert verify_lock._memory_probe_output(["memory_pressure"]) is None, broken.__name__
    assert verify_lock.read_available_memory("win32") is None


# ---------------------------------------------------------------------------
# Criterion 11 — the default floor is 25, and equality admits
# ---------------------------------------------------------------------------


def test_default_memory_floor_includes_equality(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The default floor is 25 percent, and exactly 25 is enough.

    Fault this pins: work starting below 25, or an exact-25 reading waiting.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.FLOOR_ENV, raising=False)
    waits: list[float] = []
    monkeypatch.setattr(verify_lock, "_sleep", waits.append)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: 25.0)
    ran = False
    with verify_lock.hold_admission(["exact", "floor"]):
        ran = True
    assert ran and waits == [], "an exact-floor reading waited"

    readings = iter([24.9, 60.0])
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: next(readings))
    ticks = iter(range(0, 10**9, int(verify_lock.MEMORY_POLL_SECONDS)))
    monkeypatch.setattr(verify_lock, "_now", lambda: next(ticks))
    ran = False
    with verify_lock.hold_admission(["below", "floor"]):
        ran = True
    assert ran, "the recovered reading never started the work"
    assert waits == [verify_lock.MEMORY_POLL_SECONDS], "a below-floor reading started without waiting"


# ---------------------------------------------------------------------------
# Criterion 12 — the override is validated and used
# ---------------------------------------------------------------------------


def test_memory_floor_override_is_validated_and_used(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A finite percentage in [0, 100] is used; anything else refuses explicitly.

    Fault this pins: a valid override ignored, or an invalid one running work.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "_sleep", lambda _seconds: None)
    ticks = iter(range(0, 10**9, int(verify_lock.MEMORY_POLL_SECONDS)))
    monkeypatch.setattr(verify_lock, "_now", lambda: next(ticks))

    # a 10-percent floor admits a 15-percent reading the default floor would wait out
    monkeypatch.setenv(verify_lock.FLOOR_ENV, "10")
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: 15.0)
    ran = False
    with verify_lock.hold_admission(["floored", "work"]):
        ran = True
    assert ran, "a valid override was ignored"

    for invalid in ("abc", "150", "-1", "nan", "inf", "2e2"):
        monkeypatch.setenv(verify_lock.FLOOR_ENV, invalid)
        ran = False
        with (
            pytest.raises(verify_lock.VerifyLockRefused) as raised,
            verify_lock.hold_admission(["invalid", "override"]),
        ):
            ran = True
        assert not ran, f"override {invalid!r} ran work"
        assert verify_lock.FLOOR_ENV in str(raised.value), str(raised.value)

    # an empty override supplies nothing: unset, so the default floor applies
    monkeypatch.setenv(verify_lock.FLOOR_ENV, "")
    with pytest.raises(verify_lock.MemoryFloorRefused) as unset, verify_lock.hold_admission(["empty", "override"]):
        raise AssertionError("protected work ran")
    assert "25% floor" in str(unset.value), str(unset.value)

    # the boundaries are valid: zero admits a zero reading, a hundred needs the whole hundred
    monkeypatch.setenv(verify_lock.FLOOR_ENV, "0")
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: 0.0)
    with verify_lock.hold_admission(["zero", "floor"]):
        pass
    monkeypatch.setenv(verify_lock.FLOOR_ENV, "100")
    readings = iter([99.5, 100.0])
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: next(readings))
    with verify_lock.hold_admission(["full", "floor"]):
        pass


# ---------------------------------------------------------------------------
# Criterion 14 — unusable or aliased state refuses before work
# ---------------------------------------------------------------------------


def test_unusable_or_aliased_state_refuses_before_work(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Substituted or unusable state refuses with a diagnostic before work, never runs unlocked.

    Fault this pins: falling through unlocked after a state, lock or queue
    error, or following a substituted file to overwrite another file.
    """
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)

    def refuses(state: Path) -> None:
        monkeypatch.setenv("XDG_STATE_HOME", str(state))
        with pytest.raises(verify_lock.VerifyLockRefused), verify_lock.hold_admission(["refused", "work"]):
            raise AssertionError("protected work ran on refused admission")

    # the whole state root as a symlink: the target's file is never written through
    target = tmp_path / "elsewhere"
    target.mkdir()
    (target / "sentinel.txt").write_text("do not touch", encoding="utf-8")
    aliased = tmp_path / "state-aliased"
    aliased.mkdir()
    (aliased / "coding-harness").symlink_to(target)
    refuses(aliased)
    assert (target / "sentinel.txt").read_text(encoding="utf-8") == "do not touch"
    assert not (target / verify_lock.LOCK_NAME).exists(), "the aliased state root was written through"

    # a lock file substituted by a symlink: refusal, and the victim keeps its bytes
    plain = tmp_path / "state-lock" / "coding-harness"
    plain.mkdir(parents=True)
    victim = tmp_path / "victim.txt"
    victim.write_text("victim", encoding="utf-8")
    (plain / verify_lock.LOCK_NAME).symlink_to(victim)
    refuses(tmp_path / "state-lock")
    assert victim.read_text(encoding="utf-8") == "victim", "the substituted lock's target was modified"

    # a queue directory substituted by a symlink refuses as well
    queue_alias = tmp_path / "state-queue" / "coding-harness"
    queue_alias.mkdir(parents=True)
    (queue_alias / verify_lock.QUEUE_DIR).symlink_to(tmp_path)
    refuses(tmp_path / "state-queue")

    # an unwritable state root refuses rather than running without the lock
    readonly = tmp_path / "readonly"
    readonly.mkdir()
    readonly.chmod(0o500)
    try:
        refuses(readonly)
    finally:
        readonly.chmod(0o700)

    # the supervisor form refuses loudly instead of running the command unlocked
    sabotaged = tmp_path / "state-cli" / "coding-harness"
    sabotaged.mkdir(parents=True)
    cli_victim = tmp_path / "victim-cli.txt"
    cli_victim.write_text("victim", encoding="utf-8")
    (sabotaged / verify_lock.LOCK_NAME).symlink_to(cli_victim)
    never = tmp_path / "never.json"
    done = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.verify_lock",
            "--",
            sys.executable,
            "-c",
            f"import pathlib; pathlib.Path({str(never)!r}).write_text('ran', encoding='utf-8')",
        ],
        cwd=REPO_ROOT,
        env=_env(tmp_path / "state-cli"),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert done.returncode == 2, f"the supervisor did not refuse: {done.stderr}"
    assert "refusing" in done.stderr, f"the refusal carries no diagnostic: {done.stderr}"
    assert not never.exists(), "the refused command ran anyway"


def test_the_macos_reader_parses_the_real_memory_pressure_line(monkeypatch: pytest.MonkeyPatch) -> None:
    """Planted fault (orchestrator bootstrap edit, 2026-10-29): the reader expected `System wide`,
    while macOS `memory_pressure` prints `System-wide memory free percentage: 56%`, so every real
    reading was logged as unmeasurable."""
    monkeypatch.setattr(
        verify_lock, "_memory_probe_output", lambda _command: "Pageouts: 1\n\nSystem-wide memory free percentage: 56%\n"
    )
    assert verify_lock.read_available_memory("darwin") == 56.0


def test_a_marker_whose_holder_changed_during_the_probe_is_not_nested(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Rows L1-1, L1-12. Planted fault: the published holder was read once before the lock probe, so a
    release and a stranger's fresh admission between the two reads let a stale marker pass as nested."""
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.setenv(verify_lock.LOCK_ENV, "4242")
    readings = iter([{"pid": 4242}, {"pid": 5151}])
    monkeypatch.setattr(verify_lock, "read_holder", lambda _root=None: next(readings, {"pid": 5151}))
    with fake_holder(state, pid=5151):
        assert verify_lock.nested_holder_pid() is None


def test_a_relative_state_home_is_ignored(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Row L1-3. Planted fault: a relative `XDG_STATE_HOME` resolved against each entry's working
    directory, so entries started elsewhere lost the shared admission; the XDG rule ignores it."""
    monkeypatch.setenv("XDG_STATE_HOME", "relative/state")
    monkeypatch.setenv("HOME", str(tmp_path))
    assert verify_lock.state_base() == tmp_path / ".local" / "state"


def test_release_keeps_the_lock_held_by_an_inherited_descriptor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Row L1-11. Planted fault: release unlocked the shared lock description, so a protected
    descendant still holding the inherited descriptor lost the lock and a successor could start."""
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)
    inherited = None
    with verify_lock.hold_admission(["holder"]) as descriptor:
        assert descriptor is not None
        inherited = os.dup(descriptor)  # what a protected child inherits
    probe = os.open(state / "coding-harness" / verify_lock.LOCK_NAME, os.O_RDONLY)
    try:
        with pytest.raises(OSError):
            fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
    finally:
        os.close(probe)
        os.close(inherited)


def test_zero_available_memory_on_linux_is_a_reading(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Row L1-14. Planted fault: `MemAvailable: 0` was treated as unmeasurable, so work started at
    zero available memory instead of waiting below the floor."""
    meminfo = tmp_path / "meminfo"
    meminfo.write_text("MemTotal:        4000000 kB\nMemAvailable:          0 kB\n", encoding="utf-8")
    monkeypatch.setattr(verify_lock, "MEMINFO_PATH", meminfo)
    assert verify_lock.read_available_memory("linux") == 0.0


def test_a_second_signal_during_cleanup_still_releases(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Row L3-3. Planted fault: a second SIGTERM while the child is being stopped raised out of the
    cleanup, so the holder record stayed published for a dead process and the handlers stayed swapped."""
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)
    holder_file = state / "coding-harness" / verify_lock.HOLDER_NAME
    original_stop = verify_lock._stop_child

    def first_signal(_child: object) -> int:
        assert holder_file.is_file(), "the admission was not published before the first signal"
        raise verify_lock.SupervisorInterrupted(signal.SIGINT)

    def stop_with_second_signal(child: subprocess.Popen[bytes]) -> None:
        original_stop(child)
        os.kill(os.getpid(), signal.SIGTERM)  # the second signal arrives during cleanup

    monkeypatch.setattr(verify_lock, "_watch_child", first_signal)
    monkeypatch.setattr(verify_lock, "_stop_child", stop_with_second_signal)
    before = signal.getsignal(signal.SIGTERM)
    assert verify_lock.supervise(["sleep", "30"]) == 128 + signal.SIGINT
    assert not holder_file.exists(), "the holder record outlived the cleanup"
    assert signal.getsignal(signal.SIGTERM) is before, "the supervisor left its signal handler installed"
