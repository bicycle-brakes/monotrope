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
import os, time
with open(os.environ["PROBE_LOG"], "a", encoding="utf-8") as handle:
    handle.write(os.environ["PROBE_NAME"] + chr(10))
time.sleep(float(os.environ.get("PROBE_SLEEP", "0")))
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


def _supervised(
    state: Path, body: str, extra: dict[str, str] | None = None, cwd: Path | None = None
) -> subprocess.Popen[bytes]:
    """One independent supervisor entry against an isolated state root."""
    return subprocess.Popen(
        [sys.executable, "-m", "scripts.verify_lock", "--", sys.executable, "-c", body],
        cwd=cwd or REPO_ROOT,
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


def _write_capacity(state: Path, content: str) -> None:
    """Publish the machine-wide capacity setting by atomic replacement, the way an operator would."""
    root = state / "coding-harness"
    root.mkdir(parents=True, exist_ok=True)
    fresh = root / f".{verify_lock.SLOTS_NAME}.{os.getpid()}"
    fresh.write_text(content, encoding="utf-8")
    fresh.replace(root / verify_lock.SLOTS_NAME)


def _log_lines(log: Path) -> list[str]:
    """The order log as it stands, without creating anything."""
    try:
        return log.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []


# ---------------------------------------------------------------------------
# Criterion 1 — one machine, one admission at a time
# ---------------------------------------------------------------------------


def test_independent_entries_share_one_machine_lock(tmp_path: Path) -> None:
    """Independent admissions run their protected work one at a time, at capacity one.

    Fault this pins: an admission that locks nothing lets two supervisor
    entries and a stage-2-style context entry overlap their protected
    intervals against one shared state root — the three-lane trial's overload.
    Capacity one is selected explicitly: the default of two has its own
    criterion test below, and this scenario needs the serial case.
    """
    state = tmp_path / "state"
    _write_capacity(state, "1")
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
    # A slot marker standing in the ambient environment (the runner's real one)
    # would take the slot path before this test's legacy shapes; clear it.
    monkeypatch.delenv(verify_lock.SLOT_ENV, raising=False)
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
    Capacity one is selected explicitly: the orphaned-child scenario needs the
    successor to be excluded until the child's interval ends.
    """
    state = tmp_path / "state"
    _write_capacity(state, "1")
    holder_file = state / "coding-harness" / verify_lock.slot_holder_name(0)

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
    stopping. Capacity one is selected explicitly: the waiting admission must
    hold its reservation through the memory wait, so the second one queues.
    """
    state = tmp_path / "state"
    _write_capacity(state, "1")
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
    monkeypatch.delenv(verify_lock.SLOT_ENV, raising=False)
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)
    inherited = None
    slot_index = None
    with verify_lock.hold_admission(["holder"]) as descriptor:
        assert descriptor is not None
        inherited = os.dup(descriptor)  # what a protected child inherits
        active = verify_lock._ACTIVE
        assert active is not None and active.slot_index is not None
        slot_index = active.slot_index
    probe = os.open(state / "coding-harness" / verify_lock.slot_lock_name(slot_index), os.O_RDONLY)
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
    holder_file = state / "coding-harness" / verify_lock.slot_holder_name(0)
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
    holder_file = state / "coding-harness" / verify_lock.slot_holder_name(0)
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
    os.link(victim, root / verify_lock.slot_holder_name(0))
    with verify_lock.hold_admission(["holder"]):
        assert verify_lock.read_slot_holder(root, 0) is not None, "the holder was not published"
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
        waiter = verify_lock._Admission(verify_lock._prepare_state(), ["cancelled", "waiter"])
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
import json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import verify_lock
context = verify_lock.admission_context()
holder = verify_lock.read_slot_holder(verify_lock.state_root(), int(os.environ[verify_lock.SLOT_ENV]))
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
        verify_lock.SLOT_ENV,
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
        holder = verify_lock.read_slot_holder(state / "coding-harness", active.slot_index)
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
# The configurable slot capacity (bead coding-harness-u1ha)
# ---------------------------------------------------------------------------


def test_default_two_slots_share_capacity_across_trees(tmp_path: Path) -> None:
    """Criterion 1. With no capacity setting, two independent checks overlap and a third queues.

    Fault this pins: an eligible second check that cannot reserve the idle
    second slot, or a third reservation granted while two are occupied. The
    entries run from separate working directories and share one state root,
    the way two worktrees of one machine share it.
    """
    state = tmp_path / "state"
    trees = [tmp_path / f"tree-{index}" for index in range(3)]
    for tree in trees:
        tree.mkdir()
    outs = [tmp_path / f"slot-{index}.json" for index in range(3)]
    marks = [tmp_path / f"started-{index}.flag" for index in range(3)]
    first = _supervised(
        state,
        RECORD_BODY,
        {"PROBE_OUT": str(outs[0]), "PROBE_STARTED": str(marks[0]), "PROBE_SLEEP": "3.0", "PYTHONPATH": str(REPO_ROOT)},
        cwd=trees[0],
    )
    assert _wait_until(marks[0].is_file), "the first entry never started"
    second = _supervised(
        state,
        RECORD_BODY,
        {"PROBE_OUT": str(outs[1]), "PROBE_STARTED": str(marks[1]), "PROBE_SLEEP": "3.0", "PYTHONPATH": str(REPO_ROOT)},
        cwd=trees[1],
    )
    assert _wait_until(marks[1].is_file), "the idle second slot was not granted while the first still ran"
    third = _supervised(
        state,
        RECORD_BODY,
        {"PROBE_OUT": str(outs[2]), "PROBE_STARTED": str(marks[2]), "PROBE_SLEEP": "0.2", "PYTHONPATH": str(REPO_ROOT)},
        cwd=trees[2],
    )
    assert not _wait_until(marks[2].is_file, 1.5), "a third check ran while two slots were occupied"
    for entry in (first, second, third):
        assert entry.wait(timeout=60) == 0
    first_span, second_span = _interval(outs[0]), _interval(outs[1])
    assert first_span[0] < second_span[1] and second_span[0] < first_span[1], (
        f"the two slots did not overlap: {first_span} vs {second_span}"
    )
    third_span = _interval(outs[2])
    assert third_span[0] >= min(first_span[1], second_span[1]) - 0.05, (
        f"the third check started before a slot freed: {third_span} after {first_span} and {second_span}"
    )


def test_shared_capacity_setting_and_live_decrease(tmp_path: Path) -> None:
    """Criterion 2. The one machine-wide setting selects the capacity for every tree; a decrease drains.

    Fault this pins: settings of one or three ignored, a per-checkout copy of
    the value winning, or a lowered capacity granting a new reservation while
    a slot at or above it is still occupied.
    """
    # capacity one serialises independent entries
    state_one = tmp_path / "state-one"
    _write_capacity(state_one, "1")
    out_a = tmp_path / "one-a.json"
    mark_a = tmp_path / "one-a.flag"
    serial_a = _supervised(
        state_one, RECORD_BODY, {"PROBE_OUT": str(out_a), "PROBE_STARTED": str(mark_a), "PROBE_SLEEP": "2.0"}
    )
    assert _wait_until(mark_a.is_file), "the first entry never started"
    mark_b = tmp_path / "one-b.flag"
    serial_b = _supervised(
        state_one,
        RECORD_BODY,
        {"PROBE_OUT": str(tmp_path / "one-b.json"), "PROBE_STARTED": str(mark_b), "PROBE_SLEEP": "0.2"},
    )
    assert not _wait_until(mark_b.is_file, 1.5), "a second check ran while capacity one was occupied"
    for entry in (serial_a, serial_b):
        assert entry.wait(timeout=60) == 0
    assert _interval(tmp_path / "one-b.json")[0] >= _interval(out_a)[1] - 0.05, "capacity one overlapped two checks"

    # capacity three admits three at once
    state_three = tmp_path / "state-three"
    _write_capacity(state_three, "3")
    outs = [tmp_path / f"three-{index}.json" for index in range(3)]
    marks = [tmp_path / f"three-{index}.flag" for index in range(3)]
    trio = []
    for index in range(3):
        trio.append(
            _supervised(
                state_three,
                RECORD_BODY,
                {"PROBE_OUT": str(outs[index]), "PROBE_STARTED": str(marks[index]), "PROBE_SLEEP": "1.5"},
            )
        )
    for mark in marks:
        assert _wait_until(mark.is_file), "capacity three did not admit three checks at once"
    for entry in trio:
        assert entry.wait(timeout=60) == 0
    spans = [_interval(out) for out in outs]
    for outer in spans:
        for inner in spans:
            assert outer[0] < inner[1], f"three admitted checks did not overlap: {spans}"

    # a live decrease drains: slot 1 sits above the lowered capacity and keeps its reservation
    state_drop = tmp_path / "state-drop"
    _write_capacity(state_drop, "2")
    mark_a = tmp_path / "drop-a.flag"
    out_a = tmp_path / "drop-a.json"
    drop_a = _supervised(
        state_drop, RECORD_BODY, {"PROBE_OUT": str(out_a), "PROBE_STARTED": str(mark_a), "PROBE_SLEEP": "1.2"}
    )
    assert _wait_until(mark_a.is_file)
    mark_b = tmp_path / "drop-b.flag"
    out_b = tmp_path / "drop-b.json"
    drop_b = _supervised(
        state_drop, RECORD_BODY, {"PROBE_OUT": str(out_b), "PROBE_STARTED": str(mark_b), "PROBE_SLEEP": "4.0"}
    )
    assert _wait_until(mark_b.is_file), "the second slot was not granted while the capacity stood at two"
    _write_capacity(state_drop, "1")  # lowered while both hold; slot 1 sits above the lowered capacity
    mark_c = tmp_path / "drop-c.flag"
    out_c = tmp_path / "drop-c.json"
    drop_c = _supervised(
        state_drop, RECORD_BODY, {"PROBE_OUT": str(out_c), "PROBE_STARTED": str(mark_c), "PROBE_SLEEP": "0.2"}
    )
    assert not _wait_until(mark_c.is_file, 1.5), "a lowered capacity granted a reservation before the drain"
    for entry in (drop_a, drop_b, drop_c):
        assert entry.wait(timeout=60) == 0
    b_span, c_span = _interval(out_b), _interval(out_c)
    assert c_span[0] >= b_span[1] - 0.05, (
        f"the new reservation started before the occupied higher slot drained: {c_span} after {b_span}"
    )


def test_invalid_or_unsafe_capacity_refuses_before_work(tmp_path: Path) -> None:
    """Criterion 3. A present but invalid or unsafe capacity setting refuses before any protected work.

    Fault this pins: an empty, zero, negative, fractional, nonnumeric,
    substituted or unreadable setting silently selecting a fallback, hanging,
    or letting the protected command run.
    """
    marker = tmp_path / "never.flag"
    command = [
        sys.executable,
        "-c",
        f"import pathlib; pathlib.Path({str(marker)!r}).write_text('ran', encoding='utf-8')",
    ]

    def entry(state: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "scripts.verify_lock", "--", *command],
            cwd=REPO_ROOT,
            env=_env(state),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    for index, content in enumerate(("", " ", "\n", " \n ", "0", "-1", "2.5", "abc", "1 2", "0x10", "١٢")):
        state = tmp_path / f"state-invalid-{index}"
        _write_capacity(state, content)
        done = entry(state)
        setting = str(state / "coding-harness" / verify_lock.SLOTS_NAME)
        assert done.returncode == 2, f"content {content!r} was not refused: {done.stdout} {done.stderr}"
        assert "refusing" in done.stderr, f"content {content!r} carries no diagnostic: {done.stderr}"
        assert setting in done.stderr, f"the diagnostic does not name the setting: {done.stderr}"
        assert not marker.exists(), f"content {content!r} let the protected command run"

    for kind in ("symlink", "directory", "unreadable"):
        state = tmp_path / f"state-{kind}"
        root = state / "coding-harness"
        root.mkdir(parents=True)
        victim = tmp_path / f"victim-{kind}.txt"
        victim.write_text("2", encoding="utf-8")
        setting_path = root / verify_lock.SLOTS_NAME
        if kind == "symlink":
            setting_path.symlink_to(victim)
        elif kind == "directory":
            setting_path.mkdir()
        else:
            setting_path.write_text("2", encoding="utf-8")
            setting_path.chmod(0o000)
        done = entry(state)
        assert done.returncode == 2, f"the {kind} setting was not refused: {done.stdout} {done.stderr}"
        assert "refusing" in done.stderr, f"the {kind} setting carries no diagnostic: {done.stderr}"
        assert not marker.exists(), f"the {kind} setting let the protected command run"
        assert victim.read_text(encoding="utf-8") == "2", f"the {kind} setting's target was modified"

    # the accepted shape: a whitespace-trimmed positive decimal integer, nothing else
    state = tmp_path / "state-trimmed"
    _write_capacity(state, " 2\n")
    done = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.verify_lock",
            "--",
            sys.executable,
            "-c",
            f"import pathlib; pathlib.Path({str(marker)!r}).write_text('ran', encoding='utf-8')",
        ],
        cwd=REPO_ROOT,
        env=_env(state),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert done.returncode == 0, f"a whitespace-trimmed setting was refused: {done.stderr}"
    assert marker.is_file(), "the accepted setting never ran the protected command"


def test_slot_waiters_reserve_in_fifo_order(tmp_path: Path) -> None:
    """Criterion 4. Live waiters reserve freed slots in registration order, without waiting for all to empty.

    Fault this pins: a later waiter overtaking an earlier live registration,
    or a free slot kept idle until every other holder has finished.
    """
    state = tmp_path / "state"
    log = tmp_path / "order.log"
    extra = lambda name, seconds: {"PROBE_LOG": str(log), "PROBE_NAME": name, "PROBE_SLEEP": seconds}  # noqa: E731
    holder_a = _supervised(state, ORDER_BODY, extra("holder-a", "30"))
    assert _wait_until(lambda: "holder-a" in _log_lines(log)), "holder A never started"
    holder_b = _supervised(state, ORDER_BODY, extra("holder-b", "30"))
    assert _wait_until(lambda: "holder-b" in _log_lines(log)), "holder B never started"
    waiter_one = _supervised(state, ORDER_BODY, extra("waiter-1", "0.2"))
    # admitted holders have left the queue: only the live waiters keep a record
    assert _wait_until(lambda: len(_records(state)) >= 1), "the first waiter never registered"
    waiter_two = _supervised(state, ORDER_BODY, extra("waiter-2", "0.2"))
    assert _wait_until(lambda: len(_records(state)) >= 2), "the second waiter never registered"

    # holder B ends first: the first waiter takes the freed slot while holder A still occupies its own
    os.kill(holder_b.pid, signal.SIGTERM)
    assert holder_b.wait(timeout=30) == 128 + signal.SIGTERM, "holder B did not end on its signal"
    assert _wait_until(lambda: "waiter-1" in _log_lines(log), 5.0), (
        "the first waiter was not admitted while the other slot was still occupied"
    )
    assert holder_a.poll() is None, "the first waiter waited for every holder instead of the freed slot"

    # holder A ends and its slot frees; the waiters' registered order stays their admission order
    os.kill(holder_a.pid, signal.SIGTERM)
    assert holder_a.wait(timeout=30) == 128 + signal.SIGTERM, "holder A did not end on its signal"
    for entry in (waiter_one, waiter_two):
        assert entry.wait(timeout=60) == 0
    assert _log_lines(log) == ["holder-a", "holder-b", "waiter-1", "waiter-2"], _log_lines(log)


NESTED_CONTEXT_BODY = """
import json, os, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import verify_lock
go = os.environ["PROBE_GO"]
Path(os.environ["PROBE_STARTED"]).write_text("started")
deadline = time.time() + 30
while not os.path.exists(go) and time.time() < deadline:
    time.sleep(0.05)
held = subprocess.run(
    [sys.executable, "-m", "scripts.verify_lock", "--held"],
    capture_output=True,
    text=True,
    timeout=30,
    check=False,
)
with verify_lock.hold_admission(["nested", "child"]) as owned:
    context = verify_lock.admission_context()
    Path(os.environ["PROBE_OUT"]).write_text(json.dumps({
        "owned_none": owned is None,
        "slot": os.environ.get(verify_lock.SLOT_ENV),
        "marker_pid": os.environ.get(verify_lock.LOCK_ENV),
        "held_exit": held.returncode,
        "id": context.admission_id,
        "wait": context.wait_seconds,
        "reused": context.reused,
    }))
"""


@pytest.mark.parametrize("marker", ["²", "9" * 5000], ids=["non-decimal-digit", "overlong-digits"])
def test_malformed_slot_marker_falls_back_to_admission(monkeypatch: pytest.MonkeyPatch, marker: str) -> None:
    """Malformed slot markers must fall back rather than crash during integer conversion."""
    monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
    monkeypatch.setenv(verify_lock.TOKEN_ENV, "marker-token")
    monkeypatch.setenv(verify_lock.SLOT_ENV, marker)
    try:
        relation = verify_lock._nested_relation()
    except ValueError as error:
        pytest.fail(f"a malformed slot marker must fall back to ordinary admission: {error}")
    assert relation is None, "a malformed slot marker must not validate an inherited admission"


def test_overlong_capacity_refuses_with_diagnostic(tmp_path: Path) -> None:
    """An integer conversion limit must produce the documented refusal, not ValueError."""
    setting = tmp_path / verify_lock.SLOTS_NAME
    setting.write_text("9" * 5000, encoding="utf-8")
    try:
        with pytest.raises(verify_lock.VerifyLockRefused, match="positive decimal.*refusing admission") as refused:
            verify_lock.read_capacity(tmp_path)
    except ValueError as error:
        pytest.fail(f"an overlong capacity must refuse admission with a diagnostic: {error}")
    assert str(setting) in str(refused.value), "the refusal must identify the capacity setting"


def test_nested_entries_use_their_own_slot_and_context(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 5. A nested check reuses its ancestor's admission at full capacity, with its own context.

    Fault this pins: nesting that queues again while both slots are occupied,
    a peer's slot, token or context resolved as its own, or a malformed or
    stale slot marker bypassing admission.
    """
    # in-process: the genuine marker nests; malformed, stale and foreign-token markers do not
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.SLOT_ENV, raising=False)
    monkeypatch.delenv(verify_lock.TOKEN_ENV, raising=False)
    with verify_lock.hold_admission(["fresh", "holder"]) as owned:
        assert owned is not None
        active = verify_lock._ACTIVE
        assert active is not None and active.slot_index is not None
        monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
        monkeypatch.setenv(verify_lock.TOKEN_ENV, active.token)
        monkeypatch.setenv(verify_lock.SLOT_ENV, str(active.slot_index))
        assert verify_lock.nested_holder_pid() == os.getpid(), "the genuine slot marker did not nest"
        monkeypatch.setenv(verify_lock.SLOT_ENV, "not-a-number")
        assert verify_lock.nested_holder_pid() is None, "a malformed slot marker bypassed admission"
        monkeypatch.setenv(verify_lock.SLOT_ENV, str(active.slot_index + 100))
        assert verify_lock.nested_holder_pid() is None, "a stale slot marker bypassed admission"
        monkeypatch.setenv(verify_lock.SLOT_ENV, str(active.slot_index))
        monkeypatch.setenv(verify_lock.TOKEN_ENV, "another-admission-token")
        assert verify_lock.nested_holder_pid() is None, "a foreign token validated a slot marker"
    monkeypatch.delenv(verify_lock.LOCK_ENV)
    monkeypatch.delenv(verify_lock.TOKEN_ENV)
    monkeypatch.delenv(verify_lock.SLOT_ENV)

    # multi-process: both slots occupied, and each nested child resolves its own ancestor's context
    go = tmp_path / "go.flag"
    outs = [tmp_path / f"nested-{index}.json" for index in range(2)]
    marks = [tmp_path / f"holder-{index}.flag" for index in range(2)]
    holders = []
    for index in range(2):
        holders.append(
            _supervised(
                state,
                NESTED_CONTEXT_BODY,
                {"PROBE_OUT": str(outs[index]), "PROBE_GO": str(go), "PROBE_STARTED": str(marks[index])},
            )
        )
        # one after the other, so holder N reserves slot N
        assert _wait_until(marks[index].is_file), f"holder {index} never took its slot"
    root = state / "coding-harness"
    records = [verify_lock.read_slot_holder(root, index) for index in range(2)]
    assert all(record is not None for record in records), f"the slots' ownership was not published: {records}"
    assert records[0]["admission_id"] != records[1]["admission_id"], "two admissions shared one identity"
    go.write_text("now", encoding="utf-8")
    for out in outs:
        assert _wait_until(out.is_file), "a nested child queued or never ran while both slots were occupied"
    for index, out in enumerate(outs):
        result = json.loads(out.read_text(encoding="utf-8"))
        assert result["owned_none"], f"a nested entry owned a slot of its own: {result}"
        # The supervisor's own child carries its ancestor's context as its own fresh
        # measurement (bead coding-harness-1um6); either way it must be THIS ancestor's.
        assert result["reused"] is False, f"the ancestor's context was misread as inherited: {result}"
        assert result["held_exit"] == 0, f"--held did not accept the ancestor's admission: {result}"
        assert result["slot"] == str(index), f"the nested child resolved a peer's slot: {result}"
        assert result["marker_pid"] == str(holders[index].pid), f"the nested child resolved a peer's marker: {result}"
        assert result["id"] == records[index]["admission_id"], f"the nested context lost its ancestor's id: {result}"
        assert result["wait"] == records[index]["admission_wait"], f"the nested context lost its wait: {result}"
    for holder in holders:
        assert holder.wait(timeout=60) == 0


def test_slot_release_preserves_peers_and_inherited_children(tmp_path: Path) -> None:
    """Criterion 6. A reservation covers the protected children's cleanup and releases without hurting peers.

    Fault this pins: a peer's cleanup deleting another slot's ownership,
    capacity leaking after a dead participant, or a successor overlapping
    still-protected work.
    """
    state = tmp_path / "state"
    root = state / "coding-harness"
    mark_a = tmp_path / "peer-a.flag"
    out_a = tmp_path / "peer-a.json"
    peer_a = _supervised(
        state, RECORD_BODY, {"PROBE_OUT": str(out_a), "PROBE_STARTED": str(mark_a), "PROBE_SLEEP": "2.0"}
    )
    assert _wait_until(mark_a.is_file)
    mark_b = tmp_path / "peer-b.flag"
    out_b = tmp_path / "peer-b.json"
    peer_b = _supervised(
        state, RECORD_BODY, {"PROBE_OUT": str(out_b), "PROBE_STARTED": str(mark_b), "PROBE_SLEEP": "0.8"}
    )
    assert _wait_until(mark_b.is_file), "the peer never took the second slot"

    # the first supervisor dies mid-run; its protected child keeps the slot through its own lifetime
    os.kill(peer_a.pid, signal.SIGKILL)
    peer_a.wait(timeout=10)
    assert peer_b.wait(timeout=60) == 0 and out_b.is_file(), "the peer could not finish beside the orphaned child"
    # the peer's release removed only its own ownership, and never a lock file
    assert verify_lock.read_slot_holder(root, 1) is None, "the peer's record outlived its release"
    assert (root / verify_lock.slot_lock_name(1)).is_file(), "the peer's release unlinked a lock file"
    survivor = verify_lock.read_slot_holder(root, 0)
    assert survivor is not None and survivor["pid"] == peer_a.pid, (
        "the peer's cleanup deleted the dead participant's ownership"
    )
    probe = os.open(root / verify_lock.slot_lock_name(0), os.O_RDONLY)
    try:
        with pytest.raises(OSError):
            fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
    finally:
        os.close(probe)

    # the orphaned child's interval ends, its slot is released, and capacity is whole again
    assert _wait_until(out_a.is_file), "the orphaned child never finished"
    mark_c = tmp_path / "after-c.flag"
    mark_d = tmp_path / "after-d.flag"
    after_c = _supervised(
        state,
        RECORD_BODY,
        {"PROBE_OUT": str(tmp_path / "after-c.json"), "PROBE_STARTED": str(mark_c), "PROBE_SLEEP": "1.0"},
    )
    assert _wait_until(mark_c.is_file), "capacity did not recover for the first follower"
    after_d = _supervised(
        state,
        RECORD_BODY,
        {"PROBE_OUT": str(tmp_path / "after-d.json"), "PROBE_STARTED": str(mark_d), "PROBE_SLEEP": "1.0"},
    )
    assert _wait_until(mark_d.is_file), "the dead participant's slot was never reusable: capacity leaked"
    for entry in (after_c, after_d):
        assert entry.wait(timeout=60) == 0


def test_each_slot_checks_memory_before_work(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 7. Every reservation applies the free-memory policy; the second slot skips nothing.

    Fault this pins: a second slot's admission starting work below the floor,
    or an admission that never takes its own probe.
    """
    state = tmp_path / "state"
    _write_capacity(state, "2")
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.setenv(verify_lock.FLOOR_ENV, "25")
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.SLOT_ENV, raising=False)
    # One thread, injected memory readings and an injected sleep: the order of events is
    # fixed by the code under test, never by thread timing.
    mode = {"reading": 30.0}
    probes: list[float] = []
    sleeps: list[float] = []
    work_started: list[int] = []

    def reader(_platform: str | None = None) -> float | None:
        probes.append(mode["reading"])
        return mode["reading"]

    def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)
        # Nothing has started on the below-floor reading; memory recovers during the wait.
        assert work_started == [0], "the second admission started work on a below-floor reading"
        mode["reading"] = 30.0

    monkeypatch.setattr(verify_lock, "_sleep", fake_sleep)
    monkeypatch.setattr(verify_lock, "read_available_memory", reader)

    with verify_lock.hold_admission(["slot", "0"]):
        work_started.append(0)
        assert probes == [30.0], "the first admission skipped its own memory probe"
        mode["reading"] = 10.0
        with verify_lock.hold_admission(["slot", "1"]):
            work_started.append(1)
            second_lock = verify_lock.state_root() / verify_lock.slot_lock_name(1)
            assert second_lock.is_file(), "the second reservation is not slot 1"
    assert work_started == [0, 1]
    assert probes == [30.0, 10.0, 30.0], "the second slot's admission did not apply its own memory policy"
    assert sleeps == [verify_lock.MEMORY_POLL_SECONDS]


def test_wait_logs_name_all_occupied_slots_without_tokens(tmp_path: Path) -> None:
    """Criterion 9. A waiter's log names every occupied slot and its holder, and never a token.

    Fault this pins: a holder missing from the wait logs, one holder's record
    overwritten by another's, or a token printed where the holder's slot,
    process id, command and start time belong.
    """
    state = tmp_path / "state"
    template = (
        "import os, time\nfrom pathlib import Path\n"
        "Path(os.environ['PROBE_STARTED']).write_text({name!r})\ntime.sleep({seconds})\n"
    )
    body_a = template.format(name="a", seconds="5")
    body_b = template.format(name="b", seconds="5.2")
    holder_a = _supervised(state, body_a, {"PROBE_STARTED": str(tmp_path / "logged-a.flag")})
    assert _wait_until((tmp_path / "logged-a.flag").is_file), "holder A never started"
    holder_b = _supervised(state, body_b, {"PROBE_STARTED": str(tmp_path / "logged-b.flag")})
    assert _wait_until((tmp_path / "logged-b.flag").is_file), "holder B never took its slot"
    root = state / "coding-harness"
    records = [verify_lock.read_slot_holder(root, index) for index in range(2)]
    assert all(record is not None for record in records), "a holder's record is missing"
    assert records[0]["pid"] == holder_a.pid and records[1]["pid"] == holder_b.pid, "a holder's record was overwritten"
    waiter = subprocess.run(
        [sys.executable, "-m", "scripts.verify_lock", "--", sys.executable, "-c", "import time; time.sleep(0.2)"],
        cwd=REPO_ROOT,
        env=_env(state),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    stderr = waiter.stderr
    assert waiter.returncode == 0, f"the queued waiter never ran: {stderr}"
    assert "waiting for admission" in stderr, f"the wait was not logged: {stderr}"
    for index in range(2):
        assert f"slot {index}: holder pid {records[index]['pid']}" in stderr, (
            f"slot {index}'s holder is missing from the wait log: {stderr}"
        )
    assert "write_text('a')" in stderr and "write_text('b')" in stderr, f"a holder's command is missing: {stderr}"
    for record in records:
        assert record["token"] not in stderr, "a wait log exposed an ownership token"


LEGACY_HOLDER_BODY = """
import fcntl, json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import verify_lock
root = Path(os.environ["STATE_ROOT"]) / "coding-harness"
root.mkdir(parents=True, exist_ok=True)
descriptor = os.open(root / verify_lock.LOCK_NAME, os.O_RDWR | os.O_CREAT | os.O_NONBLOCK, 0o600)
fcntl.flock(descriptor, fcntl.LOCK_EX)
(root / verify_lock.HOLDER_NAME).write_text(
    json.dumps({
        "pid": os.getpid(),
        "token": "legacy-admission-token",
        "command": ["legacy", "checkout"],
        "start": "2026-11-10T00:00:00",
    }),
    encoding="utf-8",
)
child = subprocess.Popen(
    [sys.executable, "-c", "import os, time; time.sleep(float(os.environ['LEGACY_SLEEP']))"],
    env=dict(os.environ),
    pass_fds=(descriptor,),
    start_new_session=True,
)
Path(os.environ["LEGACY_PIDS"]).write_text(json.dumps({"holder": os.getpid(), "child": child.pid}))
"""


def test_legacy_exclusion_survives_new_holder_supervisor_death(tmp_path: Path) -> None:
    """Criterion 10. A legacy single-slot admission excludes every new reservation, held or orphaned.

    Fault this pins: the added slots letting a new check run beside a legacy
    holder's exclusive admission — including after the legacy supervisor dies
    with its protected child still running.
    """
    state = tmp_path / "state"
    pids_out = tmp_path / "legacy-pids.json"
    legacy = subprocess.Popen(
        [sys.executable, "-c", LEGACY_HOLDER_BODY],
        cwd=REPO_ROOT,
        env=_env(state, {"STATE_ROOT": str(state), "LEGACY_SLEEP": "4.0", "LEGACY_PIDS": str(pids_out)}),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    assert _wait_until(pids_out.is_file), "the legacy holder never took its exclusive admission"
    pids = json.loads(pids_out.read_text(encoding="utf-8"))
    out = tmp_path / "legacy-follower.json"
    mark = tmp_path / "legacy-follower.flag"
    follower = _supervised(
        state, RECORD_BODY, {"PROBE_OUT": str(out), "PROBE_STARTED": str(mark), "PROBE_SLEEP": "0.2"}
    )
    assert not _wait_until(mark.is_file, 1.5), "a new check ran beside a legacy holder's exclusive admission"

    # the legacy supervisor dies; its protected child keeps the inherited exclusion until its work ends
    os.kill(legacy.pid, signal.SIGKILL)
    legacy.wait(timeout=10)
    try:
        os.kill(pids["child"], 0)
    except ProcessLookupError:
        raise AssertionError("the legacy child died with its supervisor; the orphan shape was never built") from None
    assert not _wait_until(mark.is_file, 1.5), "the new check ran while the legacy child still held the exclusion"
    assert _wait_until(mark.is_file, 15.0), "the new check never ran after the legacy child's exclusion ended"
    assert follower.wait(timeout=60) == 0 and out.is_file(), "the follower did not finish after the legacy drain"
