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
# admission order of independent entries. The optional sleep runs before the
# write, so an entry that holds capacity while another queues keeps the write
# order equal to the reservation order, never a race between two starts.
ORDER_BODY = """
import os, time
time.sleep(float(os.environ.get("PROBE_SLEEP", "0")))
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


def _context_entry(
    state: Path, out: Path, sleep: str = "0.3", extra: dict[str, str] | None = None
) -> subprocess.Popen[bytes]:
    """One entry holding admission through the context, the way scripts.stage2 does."""
    return subprocess.Popen(
        [sys.executable, "-c", DIRECT_BODY],
        cwd=REPO_ROOT,
        env=_env(state, {"PROBE_OUT": str(out), "PROBE_SLEEP": sleep, **(extra or {})}),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _slot_record(state: Path, slot: int = 1) -> Path:
    """The published holder record of one slot."""
    return state / "coding-harness" / verify_lock.SLOT_HOLDER_NAMES[slot - 1]


TEST_TOKEN = "test-admission-token"


@contextlib.contextmanager
def fake_holder(
    state: Path, *, pid: int | None = None, publish: bool = True, hold: bool = True, token: str = TEST_TOKEN
) -> Iterator[None]:
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
                    "token": token,
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
    """Independent one-slot admissions run their protected work one at a time.

    Fault this pins: an admission that locks nothing lets two supervisor
    entries and a stage-2-style context entry overlap their protected
    intervals against one shared state root — the three-lane trial's overload.
    The entries explicitly select one slot: two-slot concurrency has its own
    regressions, this one pins the single-slot bound.
    """
    state = tmp_path / "state"
    one_slot = {verify_lock.SLOTS_ENV: "1"}
    outs = [tmp_path / f"entry-{index}.json" for index in range(3)]
    entries = [
        _supervised(state, RECORD_BODY, {"PROBE_OUT": str(outs[0]), "PROBE_SLEEP": "0.4", **one_slot}),
        _supervised(state, RECORD_BODY, {"PROBE_OUT": str(outs[1]), "PROBE_SLEEP": "0.4", **one_slot}),
        _context_entry(state, outs[2], extra=one_slot),
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
    # One slot per entry keeps the order assertion deterministic: two-slot
    # reservations could start the second entry while the first still runs.
    extra = lambda name: {  # noqa: E731
        "PROBE_LOG": str(log),
        "PROBE_NAME": name,
        "PROBE_SLEEP": "0.2",
        verify_lock.SLOTS_ENV: "1",
    }
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
        assert _wait_until(lambda: any("its holder is unavailable" in line for line in drain())), (
            "a wait on a holder without a published record was not reported as unavailable"
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
    monkeypatch.setenv(verify_lock.TOKEN_ENV, TEST_TOKEN)
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
            {
                "PROBE_OUT": str(out),
                "PROBE_SLEEP": "0.2",
                verify_lock.LOCK_ENV: str(os.getpid()),
                verify_lock.TOKEN_ENV: TEST_TOKEN,
            },
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
    holder_file = _slot_record(state)

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

    # SIGKILL of the supervisor alone: the orphaned child keeps ownership of
    # its slot until its work ends; the successor explicitly selects one slot,
    # so it must wait out exactly that remainder.
    started_d = tmp_path / "started-d.json"
    out_d = tmp_path / "child-d.json"
    killed = _supervised(
        state, RECORD_BODY, {"PROBE_SLEEP": "1.2", "PROBE_STARTED": str(started_d), "PROBE_OUT": str(out_d)}
    )
    assert _wait_until(started_d.is_file), "the killed entry never started its protected child"
    os.kill(killed.pid, signal.SIGKILL)
    killed.wait(timeout=10)
    after_d = tmp_path / "after-d.json"
    successor = _supervised(
        state, RECORD_BODY, {"PROBE_OUT": str(after_d), "PROBE_SLEEP": "0.1", verify_lock.SLOTS_ENV: "1"}
    )
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
    """While readings sit below the floor, the entry keeps its slot and rechecks every 30 seconds.

    Fault this pins: protected work starting on a below-floor reading, the
    below-floor wait ending early, or the 30-second rechecks and logs
    stopping. The second entry runs in its own process with a floor it can
    meet — the per-slot memory gate: one slot waiting below the floor never
    blocks another slot's own check.
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
    second_out = tmp_path / "second.json"

    def first() -> None:
        with verify_lock.hold_admission(["first", "work"]):
            started.set()

    thread = threading.Thread(target=first)
    try:
        thread.start()
        assert entered_gate.wait(10.0), "the first admission never reached the memory gate"
        # The second slot's own gate: a floor it meets admits it while the
        # first slot still waits below the floor.
        other = _supervised(
            state,
            RECORD_BODY,
            {"PROBE_OUT": str(second_out), "PROBE_SLEEP": "0.1", verify_lock.FLOOR_ENV: "0"},
        )
        assert other.wait(timeout=60) == 0 and second_out.is_file(), (
            "a below-floor wait on one slot blocked the second slot's own memory check"
        )
        assert not started.is_set(), "the below-floor entry started its work without a sufficient reading"
        release.set()
        assert started.wait(10.0), "a sufficient reading did not start the work"
    finally:
        release.set()
        thread.join(10.0)
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
    monkeypatch.setenv(verify_lock.TOKEN_ENV, TEST_TOKEN)
    readings = iter([{"pid": 4242, "token": TEST_TOKEN}, {"pid": 5151, "token": "other"}])
    monkeypatch.setattr(verify_lock, "read_holder", lambda _root=None: next(readings, {"pid": 5151, "token": "other"}))
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
    inherited: list[int] = []
    with verify_lock.hold_admission(["holder"]) as descriptors:
        assert descriptors is not None
        inherited = [os.dup(fd) for fd in descriptors]  # what a protected child inherits
    probe = os.open(state / "coding-harness" / verify_lock.LOCK_NAME, os.O_RDONLY)
    slot_probe = os.open(state / "coding-harness" / verify_lock.SLOT_LOCK_NAMES[0], os.O_RDONLY)
    try:
        with pytest.raises(OSError):
            fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(OSError):
            fcntl.flock(slot_probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
    finally:
        os.close(probe)
        os.close(slot_probe)
        for fd in inherited:
            os.close(fd)


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
    holder_file = _slot_record(state)
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


def test_a_signal_while_the_child_starts_still_ends_the_child(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Phase-6 row F6-9. Planted fault: a SIGTERM delivered right after Popen created the protected
    process, before it was handed to the cleanup, left the child running past the release."""
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)
    holder_file = _slot_record(state)
    started: list[subprocess.Popen[bytes]] = []
    original_popen = subprocess.Popen

    def popen_then_signal(*args: object, **kwargs: object) -> subprocess.Popen[bytes]:
        child = original_popen(*args, **kwargs)  # type: ignore[call-overload]
        started.append(child)
        os.kill(os.getpid(), signal.SIGTERM)  # arrives before _spawn_child returns
        return child

    monkeypatch.setattr(verify_lock.subprocess, "Popen", popen_then_signal)
    before = signal.getsignal(signal.SIGTERM)
    assert verify_lock.supervise(["sleep", "30"]) == 128 + signal.SIGTERM
    assert started, "the protected child was never started"
    assert started[0].poll() is not None, "the child outlived a signal that arrived while it started"
    assert not holder_file.exists(), "the holder record outlived the cleanup"
    assert signal.getsignal(signal.SIGTERM) is before, "the supervisor left its signal handler installed"


@pytest.mark.parametrize("signum", [signal.SIGHUP, signal.SIGQUIT])
def test_hangup_and_quit_clean_up_like_terminate(tmp_path: Path, signum: int) -> None:
    """Row L4-3. Planted fault: only SIGINT and SIGTERM were trapped, so SIGHUP or SIGQUIT killed the
    supervisor by the default action and left its protected child running with the lock."""
    state = tmp_path / "state"
    started = tmp_path / "started.json"
    out = tmp_path / "child.json"
    entry = _supervised(state, RECORD_BODY, {"PROBE_SLEEP": "5", "PROBE_STARTED": str(started), "PROBE_OUT": str(out)})
    assert _wait_until(started.is_file), "the entry never started its protected child"
    child = int(started.read_text(encoding="utf-8"))
    os.kill(entry.pid, signum)
    assert entry.wait(timeout=30) == 128 + signum, "the supervisor did not report its signal"
    assert not out.is_file(), "the protected child outlived its cleanup"
    with pytest.raises(ProcessLookupError):
        os.kill(child, 0)


def test_a_non_finite_macos_reading_is_unmeasurable(monkeypatch: pytest.MonkeyPatch) -> None:
    """Row F6-4. Planted fault: a percentage of 400 nines became float infinity and passed the floor."""
    monkeypatch.setattr(
        verify_lock,
        "_memory_probe_output",
        lambda _command: "System-wide memory free percentage: " + "9" * 400 + "%\n",
    )
    assert verify_lock.read_available_memory("darwin") is None


def test_publishing_never_writes_through_a_hard_linked_holder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Row F6-3. Planted fault: the holder record was opened with O_TRUNC, so a hard link planted in its
    place had its target truncated and overwritten when ownership was published."""
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)
    root = state / "coding-harness"
    root.mkdir(parents=True, mode=0o700)
    victim = tmp_path / "victim.txt"
    victim.write_text("keep me\n", encoding="utf-8")
    os.link(victim, root / verify_lock.SLOT_HOLDER_NAMES[0])
    with verify_lock.hold_admission(["holder"]):
        assert verify_lock._read_record(_slot_record(state)) is not None, "the holder was not published"
    assert victim.read_text(encoding="utf-8") == "keep me\n", "publishing wrote through the planted hard link"


def test_releasing_an_unentered_admission_keeps_the_active_holder_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Row F6-1. Planted fault: a cancelled waiter's release unlinked the active holder's record,
    so the holder's own nested checks no longer validated and queued behind their ancestor."""
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    with fake_holder(state, pid=os.getpid()):
        waiter = verify_lock._Admission(
            verify_lock._prepare_state(), ["cancelled", "waiter"], verify_lock.verify_slots_setting()
        )
        waiter.release()
        holder = verify_lock.read_holder(state / "coding-harness")
        assert holder is not None and holder.get("pid") == os.getpid(), "a non-owner removed the holder record"


NESTED_PROBE = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import verify_lock
print(verify_lock.nested_holder_pid())
"""


def test_an_unrelated_process_naming_the_published_pid_is_not_nested(tmp_path: Path) -> None:
    """Row F6-2. Planted fault: a marker was validated by metadata and a busy lock alone, so an
    unrelated process naming the published holder pid bypassed admission while that holder ran."""
    state = tmp_path / "state"
    sibling = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        with fake_holder(state, pid=sibling.pid):
            done = subprocess.run(
                [sys.executable, "-c", NESTED_PROBE],
                cwd=REPO_ROOT,
                env=_env(state, {verify_lock.LOCK_ENV: str(sibling.pid)}),
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )
        assert done.stdout.strip() == "None", "an unrelated process inherited a sibling's admission"
    finally:
        sibling.kill()
        sibling.wait(timeout=10)


GRANDCHILD_BODY = """
import os, subprocess, sys
from pathlib import Path
grandchild = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
Path(os.environ["PROBE_OUT"]).write_text(str(grandchild.pid))
"""


def test_admission_ends_only_after_a_lingering_grandchild_is_gone(tmp_path: Path) -> None:
    """Row F6-5. Planted fault: the protected command exited while a grandchild it started kept
    running, and the supervisor released admission without ending the remaining process group."""
    state = tmp_path / "state"
    out = tmp_path / "grandchild.pid"
    entry = _supervised(state, GRANDCHILD_BODY, {"PROBE_OUT": str(out)})
    assert entry.wait(timeout=60) == 0
    grandchild = int(out.read_text())

    def gone() -> bool:
        try:
            os.kill(grandchild, 0)
        except ProcessLookupError:
            return True
        return False

    try:
        assert gone() or _wait_until(gone, 2.0), "admission was released while a protected grandchild still ran"
    finally:
        with contextlib.suppress(ProcessLookupError):
            os.kill(grandchild, signal.SIGKILL)


OPENED_LOCK_PROBE = """
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import verify_lock
handle = os.open(verify_lock.state_root() / verify_lock.LOCK_NAME, os.O_RDONLY)
print(verify_lock.nested_holder_pid())
"""


def test_merely_opening_the_lock_file_is_no_relation(tmp_path: Path) -> None:
    """Row F6-2 (re-check). Planted fault: an open descriptor on `verify.lock` counted as the
    inherited one, so any process that opened the file and named the holder pid bypassed admission."""
    state = tmp_path / "state"
    sibling = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        with fake_holder(state, pid=sibling.pid):
            done = subprocess.run(
                [sys.executable, "-c", OPENED_LOCK_PROBE],
                cwd=REPO_ROOT,
                env=_env(state, {verify_lock.LOCK_ENV: str(sibling.pid)}),
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )
        assert done.stdout.strip() == "None", "opening the lock file passed as inherited ownership"
    finally:
        sibling.kill()
        sibling.wait(timeout=10)


def test_a_fifo_in_place_of_the_holder_record_is_unusable_not_a_hang(tmp_path: Path) -> None:
    """Row F6-7. Planted fault: the holder record was opened blocking before the regular-file check,
    so a FIFO without a writer in its place hung every reader and a finishing holder's release."""
    root = tmp_path / "state" / "coding-harness"
    root.mkdir(parents=True)
    os.mkfifo(root / verify_lock.HOLDER_NAME)
    done = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; from pathlib import Path; sys.path.insert(0, 'scripts'); import verify_lock; "
            f"print(verify_lock.read_holder(Path({str(root)!r})))",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert done.stdout.strip() == "None", done.stderr


def test_a_descendant_in_its_own_session_nests_after_the_holder_died(
    tmp_path: Path,
) -> None:
    """Row F6-6 (re-check). Planted fault: after the holder died, a nested runner started its check in
    a new session, so the check found no relation to the admission and queued behind its own lock;
    the inherited token is the relation, whatever the session."""
    state = tmp_path / "state"
    root = state / "coding-harness"
    root.mkdir(parents=True)
    gone = subprocess.Popen([sys.executable, "-c", "pass"])
    gone.wait(timeout=10)
    descriptor = os.open(root / verify_lock.LOCK_NAME, os.O_RDWR | os.O_CREAT, 0o600)
    fcntl.flock(descriptor, fcntl.LOCK_EX)
    (root / verify_lock.HOLDER_NAME).write_text(
        json.dumps(
            {"pid": gone.pid, "token": TEST_TOKEN, "command": ["dead", "holder"], "start": "2026-10-30T00:00:00"}
        ),
        encoding="utf-8",
    )
    try:
        done = subprocess.run(
            [sys.executable, "-c", NESTED_PROBE],
            cwd=REPO_ROOT,
            env=_env(state, {verify_lock.LOCK_ENV: str(gone.pid), verify_lock.TOKEN_ENV: TEST_TOKEN}),
            capture_output=True,
            text=True,
            timeout=60,
            check=True,
            start_new_session=True,
        )
        assert done.stdout.strip() == str(gone.pid), "a descendant of the published session queued again"
    finally:
        os.close(descriptor)


# ---------------------------------------------------------------------------
# The measured admission context (bead coding-harness-1um6)
# ---------------------------------------------------------------------------


CONTEXT_PROBE = """
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import verify_lock
context = verify_lock.admission_context()
holder = verify_lock._read_record(verify_lock.state_root() / verify_lock.SLOT_HOLDER_NAMES[0])
print(json.dumps({
    "id": context.admission_id,
    "wait": context.wait_seconds,
    "reused": context.reused,
    "holder_id": holder.get("admission_id") if holder else None,
    "holder_wait": holder.get("admission_wait") if holder else None,
}))
"""


def test_admission_measurement_survives_cli_and_inherited_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The measured queue-plus-memory wait reaches the record fresh or inherited, whichever applies.

    Fault this pins: the memory wait omitted from the measured admission wait,
    an inherited context losing its identity, a nested entry measuring or
    re-counting its ancestor's wait, or a fresh context passing itself off as
    a nested child's own.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    for name in (
        verify_lock.LOCK_ENV,
        verify_lock.TOKEN_ENV,
        verify_lock.FLOOR_ENV,
        verify_lock.ADMISSION_ID_ENV,
        verify_lock.ADMISSION_WAIT_ENV,
    ):
        monkeypatch.delenv(name, raising=False)

    # A fresh admission under fake clocks: entry at 0, the queue turn logged at
    # 30, one low-memory recheck at 60, the wait measured at 60 — so the wait
    # is 60 s only if the memory rechecks are counted into it.
    ticks = iter([0.0, 30.0, 60.0, 60.0])
    monkeypatch.setattr(verify_lock, "_now", lambda: next(ticks))
    monkeypatch.setattr(verify_lock, "_sleep", lambda _seconds: None)
    readings = iter([10.0, 30.0])
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: next(readings))

    with verify_lock.hold_admission(["measured", "wait"]) as owned:
        assert owned is not None, "an independent admission must own the lock"
        active = verify_lock._ACTIVE
        assert active is not None
        assert active.wait_seconds == 60.0, "the memory recheck was not counted into the measured wait"
        assert re.fullmatch(r"[0-9a-f]{32}", active.admission_id), active.admission_id
        context = verify_lock.admission_context()
        assert context == verify_lock.AdmissionContext(active.admission_id, 60.0, False)
        holder = verify_lock._read_record(verify_lock.state_root() / verify_lock.SLOT_HOLDER_NAMES[0])
        assert holder is not None
        assert holder["admission_id"] == active.admission_id
        assert holder["admission_wait"] == 60.0
        # A fresh context travels to a local check as the child's own measurement.
        env = verify_lock.inherit_env({"PATH": "/usr/bin:/bin"})
        assert env[verify_lock.ADMISSION_ID_ENV] == active.admission_id
        assert float(env[verify_lock.ADMISSION_WAIT_ENV]) == 60.0
    assert verify_lock._ACTIVE is None, "the released admission stayed active"

    # An inherited admission resolves its context from the published ownership:
    # an old-shape record (published before the field existed) reads unknowns.
    monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
    monkeypatch.setenv(verify_lock.TOKEN_ENV, TEST_TOKEN)
    with fake_holder(state, pid=os.getpid()):
        context = verify_lock.admission_context()
        assert context == verify_lock.AdmissionContext(None, None, True)
        root = state / "coding-harness"
        record = json.loads((root / verify_lock.HOLDER_NAME).read_text(encoding="utf-8"))
        record["admission_id"] = "inherited-admission-id"
        record["admission_wait"] = 7.5
        (root / verify_lock.HOLDER_NAME).write_text(json.dumps(record), encoding="utf-8")
        context = verify_lock.admission_context()
        assert context == verify_lock.AdmissionContext("inherited-admission-id", 7.5, True)
        # An unusable published wait stays unknown — never a guess, never zero.
        record["admission_wait"] = "not-a-number"
        (root / verify_lock.HOLDER_NAME).write_text(json.dumps(record), encoding="utf-8")
        context = verify_lock.admission_context()
        assert context == verify_lock.AdmissionContext("inherited-admission-id", None, True)
        # An inherited context does not travel as a fresh measurement.
        env = verify_lock.inherit_env({verify_lock.ADMISSION_ID_ENV: "should-not-travel"})
        assert verify_lock.ADMISSION_ID_ENV not in env
        assert verify_lock.ADMISSION_WAIT_ENV not in env
        assert env[verify_lock.LOCK_ENV] == str(os.getpid())

    # The same fresh resolution through the supervisor's CLI: the protected
    # command reads its context and the published record, and they agree.
    monkeypatch.delenv(verify_lock.LOCK_ENV)
    monkeypatch.delenv(verify_lock.TOKEN_ENV)
    done = subprocess.run(
        [sys.executable, "-m", "scripts.verify_lock", "--", sys.executable, "-c", CONTEXT_PROBE],
        cwd=REPO_ROOT,
        env=_env(state),
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    seen = json.loads(done.stdout)
    assert seen["reused"] is False, seen
    assert re.fullmatch(r"[0-9a-f]{32}", seen["id"] or ""), seen
    assert seen["wait"] is not None and seen["wait"] >= 0, seen
    assert seen["id"] == seen["holder_id"] and seen["wait"] == seen["holder_wait"], seen


# ---------------------------------------------------------------------------
# Two shared verification slots (bead coding-harness-u1ha)
# ---------------------------------------------------------------------------


@contextlib.contextmanager
def fake_slot_holder(state: Path, slot: int, *, pid: int | None = None, hold: bool = True) -> Iterator[None]:
    """Hold one slot the way a published setting-`2` admission does.

    The record names a pid (the test's own unless given) and the slot lock is
    genuinely flocked, so capacity computation, diagnostics and nested
    validation all see a live slot holder.
    """
    root = state / "coding-harness"
    root.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(root / verify_lock.SLOT_LOCK_NAMES[slot - 1], os.O_RDWR | os.O_CREAT, 0o600)
    record = root / verify_lock.SLOT_HOLDER_NAMES[slot - 1]
    record.write_text(
        json.dumps(
            {
                "pid": os.getpid() if pid is None else pid,
                "token": TEST_TOKEN,
                "command": ["fake", "slot", str(slot)],
                "start": "2026-11-21T00:00:00",
                "slots": 2,
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
            record.unlink()
        if hold:
            with contextlib.suppress(OSError):
                fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def test_two_slots_admit_two_and_queue_third(tmp_path: Path) -> None:
    """Criterion 1. Two independent setting-`2` admissions share the machine; the third queues.

    Fault this pins: a third admission running anyway, or an eligible head
    waiter unable to reserve an otherwise free slot within two queue polls.
    """
    state = tmp_path / "state"
    outs = [tmp_path / f"slot-{index}.json" for index in range(3)]
    entries = [
        _supervised(state, RECORD_BODY, {"PROBE_OUT": str(outs[0]), "PROBE_SLEEP": "0.6"}),
        _supervised(state, RECORD_BODY, {"PROBE_OUT": str(outs[1]), "PROBE_SLEEP": "0.6"}),
    ]
    # The third starts only once both slots are published, so which entry queues is not a race.
    holders = [state / "coding-harness" / name for name in verify_lock.SLOT_HOLDER_NAMES]
    assert _wait_until(lambda: all(path.exists() for path in holders)), "two free slots did not admit two entries"
    entries.append(_supervised(state, RECORD_BODY, {"PROBE_OUT": str(outs[2]), "PROBE_SLEEP": "0.2"}))
    for entry in entries:
        assert entry.wait(timeout=60) == 0
    spans = sorted((_interval(out) for out in outs[:2]), key=lambda span: span[0])
    (first_start, first_end), (second_start, second_end) = spans
    assert second_start < first_end - 0.05, f"two free slots did not admit two entries at once: {spans}"
    third = _interval(outs[2])
    assert third[0] >= min(first_end, second_end) - 0.05, (
        f"a third admission ran while both slots were still held: {spans} then {third}"
    )
    assert third[0] < max(first_end, second_end) + 2.0, (
        f"the eligible head waiter could not reserve the freed slot promptly: {spans} then {third}"
    )


def test_slot_setting_and_capacity_reduction(tmp_path: Path) -> None:
    """Criterion 2. A setting-`1` entry never shares capacity, as holder or as head waiter.

    Fault this pins: a `1` holder sharing the machine with another admission,
    a head `1` waiter entering before all holders drain, or a mixed setting
    ignoring a holder's or the head waiter's setting.
    """
    state = tmp_path / "state"

    # a setting-1 holder: a setting-2 follower must drain instead of taking the second slot
    one_holder_out = tmp_path / "one-holder.json"
    holder_started = tmp_path / "holder-started.json"
    holder = _supervised(
        state,
        RECORD_BODY,
        {
            "PROBE_OUT": str(one_holder_out),
            "PROBE_STARTED": str(holder_started),
            "PROBE_SLEEP": "1.0",
            verify_lock.SLOTS_ENV: "1",
        },
    )
    assert _wait_until(holder_started.is_file), "the setting-1 holder never started its protected work"
    follower_out = tmp_path / "two-follower.json"
    follower = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(follower_out), "PROBE_SLEEP": "0.1"})
    assert not _wait_until(follower_out.is_file, 0.6), (
        "a setting-2 follower reserved capacity beside a setting-1 holder"
    )
    assert holder.wait(timeout=60) == 0 and follower.wait(timeout=60) == 0
    holder_span, follower_span = _interval(one_holder_out), _interval(follower_out)
    assert follower_span[0] >= holder_span[1] - 0.05, (
        f"a setting-1 holder shared capacity: {holder_span} then {follower_span}"
    )

    # a setting-1 head waiter queues behind a live holder; a later setting-2
    # entry cannot overtake it, and follows only once the exclusive hold drains
    log = tmp_path / "order.log"
    names = {"PROBE_LOG": str(log), "PROBE_SLEEP": "0.3"}
    with fake_slot_holder(state, 1):
        first = _supervised(state, ORDER_BODY, {**names, "PROBE_NAME": "one", verify_lock.SLOTS_ENV: "1"})
        assert _wait_until(lambda: len(_records(state)) >= 1), "the setting-1 waiter never registered"
        second = _supervised(state, ORDER_BODY, {**names, "PROBE_NAME": "two"})
        assert _wait_until(lambda: len(_records(state)) >= 2), "the setting-2 waiter never registered"
    for entry in (first, second):
        assert entry.wait(timeout=60) == 0
    assert log.read_text(encoding="utf-8").split() == ["one", "two"], (
        f"a head setting-1 waiter was overtaken or reordered: {log.read_text(encoding='utf-8').split()}"
    )


def test_invalid_slot_setting_refuses(tmp_path: Path) -> None:
    """Criterion 3. Only the exact strings `1` and `2` are settings; everything else refuses.

    Fault this pins: an empty, padded, zero-padded, signed, fractional or
    other invalid value starting protected work, a refusal without a
    diagnostic naming the setting, or a valid inherited descendant refused
    because of its inherited setting.
    """
    state = tmp_path / "state"
    for invalid in ("", " ", " 2", "2 ", "02", "+2", "-1", "0", "3", "2.0", "two"):
        started = tmp_path / "started.json"
        done = subprocess.run(
            [
                sys.executable,
                "-m",
                "scripts.verify_lock",
                "--",
                sys.executable,
                "-c",
                "import pathlib, os; pathlib.Path(os.environ['PROBE_STARTED']).write_text('ran')",
            ],
            cwd=REPO_ROOT,
            env=_env(state, {verify_lock.SLOTS_ENV: invalid, "PROBE_STARTED": str(started)}),
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        assert done.returncode == 2, f"setting {invalid!r} exited {done.returncode}: {done.stderr}"
        assert verify_lock.SLOTS_ENV in done.stderr, (
            f"the refusal of {invalid!r} does not name the setting: {done.stderr}"
        )
        assert invalid in done.stderr, f"the refusal of {invalid!r} does not name the value: {done.stderr}"
        assert not started.exists(), f"setting {invalid!r} ran protected work"

    # a valid inherited descendant is never refused because of its setting
    with fake_holder(state, pid=os.getpid()):
        out = tmp_path / "nested.json"
        done = subprocess.run(
            [sys.executable, "-c", RECORD_BODY],
            cwd=REPO_ROOT,
            env=_env(
                state,
                {
                    "PROBE_OUT": str(out),
                    "PROBE_SLEEP": "0.1",
                    verify_lock.LOCK_ENV: str(os.getpid()),
                    verify_lock.TOKEN_ENV: TEST_TOKEN,
                    verify_lock.SLOTS_ENV: "2",
                },
            ),
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        assert done.returncode == 0, f"a valid nested entry was refused: {done.stderr}"
        assert out.is_file(), "a valid nested entry queued instead of reusing its ancestor"


def test_two_slot_fifo_and_dead_waiter(tmp_path: Path) -> None:
    """Criterion 4. Live waiters reserve in registration order; a dead waiter blocks nobody.

    Fault this pins: a later waiter overtaking a live earlier one, a dead
    waiter blocking progress, or the eligible head unable to reserve the one
    free slot within two queue polls after it frees up. One slot stays
    occupied while the two waiters queue, so the head waiter takes the free
    slot and the later waiter can only follow after the head's protected work
    ends — the write order is the reservation order, never a race between two
    nearly simultaneous starts.
    """
    state = tmp_path / "state"
    log = tmp_path / "fifo.log"
    body = {"PROBE_LOG": str(log)}

    with fake_slot_holder(state, 1):
        # both slots occupied while the two waiters register: neither may reserve yet
        with fake_slot_holder(state, 2):
            first = _supervised(state, ORDER_BODY, {**body, "PROBE_NAME": "first", "PROBE_SLEEP": "0.7"})
            assert _wait_until(lambda: len(_records(state)) >= 1), "the first waiter never registered"
            second = _supervised(state, ORDER_BODY, {**body, "PROBE_NAME": "second", "PROBE_SLEEP": "0.1"})
            assert _wait_until(lambda: len(_records(state)) >= 2), "the second waiter never registered"
        # one slot freed: the head waiter takes it, and the later waiter can only
        # follow once the head's protected work is done — the head was never overtaken
        assert first.wait(timeout=60) == 0 and second.wait(timeout=60) == 0
    order = log.read_text(encoding="utf-8").split()
    assert order == ["first", "second"], f"admission left registration order: {order}"

    # a dead waiter's record is pruned and the next live head proceeds at once
    dead_log = tmp_path / "dead.log"
    with fake_holder(state):
        doomed = _supervised(state, ORDER_BODY, {"PROBE_LOG": str(dead_log), "PROBE_NAME": "doomed"})
        assert _wait_until(lambda: len(_records(state)) >= 1), "the doomed waiter never registered"
        os.kill(doomed.pid, signal.SIGKILL)
        doomed.wait(timeout=10)
        before = set(_records(state))
        survivor = _supervised(state, ORDER_BODY, {"PROBE_LOG": str(dead_log), "PROBE_NAME": "survivor"})
        # the survivor's record is new; the dead waiter's may already be pruned
        assert _wait_until(lambda: set(_records(state)) - before), "the survivor never registered"
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline and not (
        dead_log.exists() and dead_log.read_text(encoding="utf-8").split() == ["survivor"]
    ):
        time.sleep(0.05)
    survivor.wait(timeout=60)
    assert dead_log.exists() and dead_log.read_text(encoding="utf-8").split() == ["survivor"], (
        f"a dead waiter blocked the queue: {sorted(_records(state))} and log {dead_log.read_text(encoding='utf-8') if dead_log.exists() else 'missing'}"
    )


def test_nested_slot_and_legacy_ownership(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 5. A descendant reuses its own ancestor's slot or legacy admission.

    Fault this pins: a stale or forged marker bypassing admission through a
    slot record or the legacy record, a valid descendant waiting for
    capacity, or a descendant adopting a peer's record.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.TOKEN_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)

    # a valid descendant of a live slot holder nests without queueing
    with fake_slot_holder(state, 1, pid=os.getpid()):
        monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
        monkeypatch.setenv(verify_lock.TOKEN_ENV, TEST_TOKEN)
        assert verify_lock.nested_holder_pid() == os.getpid(), "a valid slot descendant did not nest"
    monkeypatch.delenv(verify_lock.LOCK_ENV)
    monkeypatch.delenv(verify_lock.TOKEN_ENV)

    # a slot record whose lock is free is stale: its marker uses ordinary admission
    with fake_slot_holder(state, 1, pid=os.getpid(), hold=False):
        monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
        monkeypatch.setenv(verify_lock.TOKEN_ENV, TEST_TOKEN)
        assert verify_lock.nested_holder_pid() is None, "a stale slot record validated a marker"
    monkeypatch.delenv(verify_lock.LOCK_ENV)
    monkeypatch.delenv(verify_lock.TOKEN_ENV)

    # a forged slot record naming a live stranger with a guessed token does not nest either:
    # the token in the record is only a relation when the descendant's environment carries it
    stranger = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)"])
    try:
        with fake_slot_holder(state, 2, pid=stranger.pid):
            monkeypatch.setenv(verify_lock.LOCK_ENV, str(stranger.pid))
            monkeypatch.setenv(verify_lock.TOKEN_ENV, "guessed-token")
            assert verify_lock.nested_holder_pid() is None, "a forged token validated a stranger's slot record"
    finally:
        stranger.kill()
        stranger.wait(timeout=10)
    monkeypatch.delenv(verify_lock.LOCK_ENV)
    monkeypatch.delenv(verify_lock.TOKEN_ENV)

    # a valid descendant of a legacy holder nests through the legacy record
    with fake_holder(state, pid=os.getpid()):
        monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
        monkeypatch.setenv(verify_lock.TOKEN_ENV, TEST_TOKEN)
        assert verify_lock.nested_holder_pid() == os.getpid(), "a valid legacy descendant did not nest"
    monkeypatch.delenv(verify_lock.LOCK_ENV)
    monkeypatch.delenv(verify_lock.TOKEN_ENV)


def test_second_in_process_admission_refused_during_acquisition(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Criterion 6. A process holding or acquiring one independent admission refuses a second.

    Fault this pins: concurrent entries overwriting the process's published
    ownership and admission state, or the second request hanging or
    succeeding instead of being refused promptly.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.TOKEN_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)

    outcomes: list[str] = []

    def second_entry() -> None:
        try:
            with verify_lock.hold_admission(["second", "entry"]):
                outcomes.append("entered")
        except verify_lock.VerifyLockRefused as refused:
            outcomes.append(str(refused))

    # while the first entry is still acquiring (queued behind a live holder)
    with fake_holder(state):
        acquired = threading.Event()

        def first_entry() -> None:
            with verify_lock.hold_admission(["first", "entry"]):
                acquired.set()

        first = threading.Thread(target=first_entry)
        first.start()
        assert _wait_until(lambda: len(_records(state)) >= 1), "the first entry never began acquiring"
        second = threading.Thread(target=second_entry)
        second.start()
        second.join(10.0)
        assert not second.is_alive(), "the second in-process request hung instead of being refused"
        assert outcomes and "independent admission" in outcomes[0], f"the second request was not refused: {outcomes}"
        assert outcomes == [outcomes[0]], "the second request entered after its refusal"
    assert acquired.wait(30.0), "the first entry was never admitted after the holder let go"
    first.join(30.0)

    # and while the first entry holds: the refusal names the process boundary, then clears
    with verify_lock.hold_admission(["held", "entry"]):
        outcomes.clear()
        third = threading.Thread(target=second_entry)
        third.start()
        third.join(10.0)
        assert not third.is_alive(), "the second in-process request hung while one was held"
        assert outcomes and "independent admission" in outcomes[0], f"the held refusal is missing: {outcomes}"
    assert outcomes == [outcomes[0]], outcomes

    # a sequential entry after release is admitted: the guard cleared with the release
    entered = threading.Event()

    def sequential() -> None:
        with verify_lock.hold_admission(["sequential", "entry"]):
            entered.set()

    fourth = threading.Thread(target=sequential)
    fourth.start()
    assert entered.wait(10.0), "the guard never cleared after the holding entry released"
    fourth.join(10.0)


def test_slot_release_preserves_peer_and_inherited_child(tmp_path: Path) -> None:
    """Criterion 7. One release leaves the peer's record and capacity alone; the freed slot reopens.

    Fault this pins: one holder's release removing a peer's record, disturbing
    a peer's reservation, or a freed slot staying unreservable for the next
    eligible waiter after the last descriptor closed.
    """
    state = tmp_path / "state"
    peer_out = tmp_path / "peer.json"
    peer_started = tmp_path / "peer-started.json"
    peer = _supervised(
        state, RECORD_BODY, {"PROBE_OUT": str(peer_out), "PROBE_STARTED": str(peer_started), "PROBE_SLEEP": "2.5"}
    )
    short_out = tmp_path / "short.json"
    short_started = tmp_path / "short-started.json"
    short = _supervised(
        state, RECORD_BODY, {"PROBE_OUT": str(short_out), "PROBE_STARTED": str(short_started), "PROBE_SLEEP": "0.8"}
    )
    assert _wait_until(peer_started.is_file), "the peer never started its protected work"
    assert _wait_until(short_started.is_file), "the short holder never started beside its peer"
    assert short.wait(timeout=60) == 0 and short_out.is_file(), "the short holder never finished its work"
    # the peer still holds its slot: its published record names it while it runs
    peer_record = verify_lock._read_record(_slot_record(state, 2)) or verify_lock._read_record(_slot_record(state, 1))
    assert peer_record is not None and peer_record.get("pid") == peer.pid, (
        "the short holder's release removed its running peer's published record"
    )
    assert peer.wait(timeout=60) == 0, "the peer was disturbed by its neighbour's release"
    peer_span = _interval(peer_out)
    assert peer_span[1] > 0, "the peer's protected work left no recorded interval"

    # the slot freed by the finished pair is reservable promptly by the next entry
    next_out = tmp_path / "next.json"
    next_entry = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(next_out), "PROBE_SLEEP": "0.1"})
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline and not next_out.exists():
        time.sleep(0.05)
    next_entry.wait(timeout=60)
    assert next_out.is_file(), "a freed slot was not reservable by the next eligible waiter"


def test_killed_one_slot_holder_keeps_capacity_until_child_exits(tmp_path: Path) -> None:
    """Criterion 7. A killed one-slot supervisor's capacity stays in force until its child exits.

    Fault this pins: a two-slot waiter joining the inherited child of a killed
    one-slot supervisor — the exclusive capacity must hold for exactly as long
    as the surviving descriptor, then reopen.
    """
    state = tmp_path / "state"
    child_out = tmp_path / "child.json"
    child_started = tmp_path / "child-started.json"
    holder = _supervised(
        state,
        RECORD_BODY,
        {
            "PROBE_OUT": str(child_out),
            "PROBE_STARTED": str(child_started),
            "PROBE_SLEEP": "2.5",
            verify_lock.SLOTS_ENV: "1",
        },
    )
    assert _wait_until(child_started.is_file), "the one-slot holder never started its protected child"
    os.kill(holder.pid, signal.SIGKILL)
    holder.wait(timeout=10)
    child_pid = int(child_started.read_text(encoding="utf-8"))

    # the exclusive capacity stays: a two-slot waiter must drain, not join
    waiter_out = tmp_path / "waiter.json"
    waiter = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(waiter_out), "PROBE_SLEEP": "0.1"})
    assert not _wait_until(waiter_out.is_file, 1.2), "a two-slot waiter joined a one-slot survivor's capacity"
    try:
        os.kill(child_pid, 0)
    except ProcessLookupError:  # pragma: no cover - the child ended early under heavy load
        pytest.fail("the surviving child ended before the waiter was checked")
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline and not waiter_out.exists():
        time.sleep(0.05)
    waiter.wait(timeout=60)
    waiter_span, child_span = _interval(waiter_out), _interval(child_out)
    assert waiter_span[0] >= child_span[1] - 0.05, (
        f"the waiter entered while the survivor still held the exclusive capacity: {child_span} then {waiter_span}"
    )


def test_memory_floor_applies_to_both_slots(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 8. Every admission — either slot, exclusive, repeated — runs its own memory gate.

    Fault this pins: the second admission skipping the memory check, a
    below-floor reading starting work, or the existing floor override,
    equality, polling, timeout or unmeasurable-reading behaviour changing
    under two slots.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.FLOOR_ENV, raising=False)
    reads = iter([10.0, 10.0, 60.0, 25.0, None])
    seen: list[object] = []
    waits: list[float] = []
    monkeypatch.setattr(verify_lock, "_now", lambda: 0.0)
    monkeypatch.setattr(verify_lock, "_sleep", waits.append)
    monkeypatch.setattr(verify_lock, "_log", lambda _message: None)

    def reader(_platform: str | None = None) -> float | None:
        value = next(reads)
        seen.append(value)
        return value

    monkeypatch.setattr(verify_lock, "read_available_memory", reader)

    # the first admission waits out the floor, then starts on a sufficient reading
    with verify_lock.hold_admission(["first", "slot"]):
        assert seen == [10.0, 10.0, 60.0], f"the first admission's gate read {seen}"
    # the second admission runs its own gate from scratch — equality admits
    with verify_lock.hold_admission(["second", "slot"]):
        assert seen == [10.0, 10.0, 60.0, 25.0], f"the second admission skipped or merged its gate: {seen}"
    # and an unmeasurable reading on a later admission logs unknown and proceeds unchanged
    with verify_lock.hold_admission(["third", "slot"]) as owned:
        assert owned is not None
    assert seen == [10.0, 10.0, 60.0, 25.0, None], f"a later admission skipped its memory gate: {seen}"
    assert waits == [verify_lock.MEMORY_POLL_SECONDS] * 2, f"the polling behaviour changed under two slots: {waits}"


def test_wait_log_names_both_holders_without_tokens(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 9. The wait names every occupied slot and exclusive holder, never a token.

    Fault this pins: a holder overwriting its peer's description, an occupied
    slot missing from the diagnostic, a legacy holder omitted, a slot naming
    an unavailable holder without saying so, or an ownership token printed.
    """
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "QUEUE_LOG_SECONDS", 0.05)
    monkeypatch.setattr(verify_lock, "QUEUE_POLL_SECONDS", 0.01)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)

    slot_pid = 424242
    legacy_pid = 515151
    seen: list[str] = []

    def drain() -> list[str]:
        seen.extend(capsys.readouterr().err.splitlines())
        return seen

    with fake_slot_holder(state, 1, pid=slot_pid), fake_holder(state, pid=legacy_pid):
        admitted = threading.Event()

        def waiter() -> None:
            with verify_lock.hold_admission(["waiter", "body"]):
                admitted.set()

        thread = threading.Thread(target=waiter)
        thread.start()
        assert _wait_until(lambda: any("waiting for admission" in line for line in drain())), "the wait was not logged"
        first = [line for line in seen if "waiting for admission" in line][0]
        for expected in (
            "slot 1:",
            str(slot_pid),
            "fake slot 1",
            "2026-11-21T00:00:00",
            "exclusive holder (older checkout):",
            str(legacy_pid),
            "fake holder",
        ):
            assert expected in first, f"the wait log is missing {expected!r}: {first}"
        assert TEST_TOKEN not in first, "the wait log exposed an ownership token"
        assert all(TEST_TOKEN not in line for line in drain()), "a later wait log line exposed a token"

        # an occupied slot without a readable record says so instead of disappearing
        (state / "coding-harness" / verify_lock.SLOT_HOLDER_NAMES[0]).unlink()
        assert _wait_until(lambda: any("its holder is unavailable" in line for line in drain())), (
            "an occupied slot without a record vanished from the wait log"
        )
    assert admitted.wait(30.0), "the waiter was never admitted"
    thread.join(10.0)


def test_legacy_exclusive_lock_excludes_both_slots(tmp_path: Path) -> None:
    """Criterion 10. An older checkout's exclusive admission never overlaps an updated one.

    Fault this pins: an old holder or its surviving child overlapping an
    updated holder, or a later updated waiter overtaking an earlier live old
    waiter. A setting-`1` entry behaves exactly like the older checkout's
    admission: the compatibility lock taken exclusively, no slot.
    """
    state = tmp_path / "state"

    # an old-style exclusive holder excludes both slots: a setting-2 entry drains
    old_out = tmp_path / "old-holder.json"
    old_started = tmp_path / "old-holder-started.json"
    old_holder = _supervised(
        state,
        RECORD_BODY,
        {
            "PROBE_OUT": str(old_out),
            "PROBE_STARTED": str(old_started),
            "PROBE_SLEEP": "1.2",
            verify_lock.SLOTS_ENV: "1",
        },
    )
    assert _wait_until(old_started.is_file), "the old-style holder never started"
    newcomer_out = tmp_path / "newcomer.json"
    newcomer = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(newcomer_out), "PROBE_SLEEP": "0.1"})
    assert not _wait_until(newcomer_out.is_file, 0.7), "an updated admission overlapped an old exclusive holder"
    assert old_holder.wait(timeout=60) == 0 and newcomer.wait(timeout=60) == 0
    old_span, newcomer_span = _interval(old_out), _interval(newcomer_out)
    assert newcomer_span[0] >= old_span[1] - 0.05, (
        f"an updated admission overlapped the old holder's interval: {old_span} then {newcomer_span}"
    )

    # an earlier old-style waiter is honored: a later updated waiter never overtakes it
    log = tmp_path / "order.log"
    with fake_holder(state):
        old_waiter = _supervised(
            state,
            ORDER_BODY,
            {"PROBE_LOG": str(log), "PROBE_NAME": "old-waiter", verify_lock.SLOTS_ENV: "1"},
        )
        assert _wait_until(lambda: len(_records(state)) >= 1), "the old-style waiter never registered"
        updated_waiter = _supervised(state, ORDER_BODY, {"PROBE_LOG": str(log), "PROBE_NAME": "updated-waiter"})
        assert _wait_until(lambda: len(_records(state)) >= 2), "the updated waiter never registered"
    for entry in (old_waiter, updated_waiter):
        assert entry.wait(timeout=60) == 0
    assert log.read_text(encoding="utf-8").split() == ["old-waiter", "updated-waiter"], (
        f"an updated waiter overtook an earlier live old waiter: {log.read_text(encoding='utf-8').split()}"
    )
