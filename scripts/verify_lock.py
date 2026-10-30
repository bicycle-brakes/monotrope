#!/usr/bin/env python3
"""verify_lock.py — one machine-wide admission for protected verification work.

Concurrent full checks exhaust the machine: a three-lane trial recorded load
above 100 and checks past 30 minutes, against 11-12 minutes run one after the
other (bead coding-harness-p6mu). This module queues every independent
protected entry of one user on one machine — across repositories and
worktrees — and checks the system's free memory before work starts, so a
runner's checking time limit is spent on checking, not on waiting for a turn.

**Shared state.** `${XDG_STATE_HOME:-~/.local/state}/coding-harness/` is the
one state root for cooperating entries; neither the repository nor a worktree
identifies it. `verify.lock` carries the exclusive work lock (`fcntl.flock`,
kernel-backed), `verify.holder.json` the published ownership (pid, command,
start time) of whoever holds it, and `verify.queue/` one record per waiter,
held open under its owner's liveness flock so a dead waiter's record is
recognisable and pruned. A short-held `verify.registry.lock` serialises
registration, pruning and turn-taking; registration order is the admission
order — `flock` alone supplies no FIFO, so only the first live record may try
the work lock.

**Nested work.** A protected entry descended from a live admission carries
`HARNESS_VERIFY_LOCK_HELD=<holder-pid>`. The marker is honoured only when the
published ownership names its process, the work lock is genuinely held, and
this process is related to that admission: the holder is a live ancestor, or
this process runs in the session the supervisor started for its protected
child (published with the ownership). Metadata or an open descriptor on the
lock file never suffices; an absent, malformed, stale
or unrelated marker uses ordinary admission. The holder process itself need
not live: a killed supervisor leaves the lock held by the descriptor its
protected child inherited, and that child's own nested calls still nest
through the session instead of deadlocking on their ancestor. Only the owner
removes the published ownership, and only while it still names the owner.

**Memory.** After the lock, admission reads the system's free memory — macOS
`memory_pressure`'s system-wide free percentage, Linux `MemAvailable` over
`MemTotal` — and waits, rechecking every 30 seconds, while usable readings sit
below the floor (25 percent by default, or `HARNESS_VERIFY_MEMORY_FLOOR`, a
finite percentage in [0, 100]; equality admits). Readings that stay below the
floor for 60 minutes from the first low one refuse the entry, naming the floor
and the last reading; a reading that cannot be taken is logged as unknown and
the entry proceeds. The floor is a starting policy, not continuous monitoring.

**Refusals.** Unusable state — a state directory, lock, holder or queue file
that is a symlink or not a regular file, or cannot be created — refuses the
entry with a diagnostic before any protected work: nothing here falls through
unlocked, and no substituted file is written through. `VerifyLockRefused`
exits 2, `MemoryFloorRefused` exits 3.

Command line:

    python -m scripts.verify_lock --held          # exit 0 when the environment names a valid admission
    python -m scripts.verify_lock -- COMMAND...   # supervise one protected command

The supervisor queues, checks memory, publishes ownership for its child —
which inherits the lock descriptor, so ownership outlives a killed supervisor
for exactly as long as the protected child and its own children run — and
releases only after the child's process group is gone, including failure,
cancellation and signals; signal cleanup kills the child before the lock is
released, and a grandchild left in the group after the command exits is ended
before release. `scripts.verify_all.sh` execs this supervisor, and
`scripts.stage2` holds the same admission around its timed local checks; the
queue and memory waits consume neither `VERIFY_SECONDS` nor a pytest proof's
execution timeout — the configured limits still apply to actual execution.
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime
import fcntl
import json
import math
import os
import re
import signal
import stat
import subprocess
import sys
import threading
import time
from collections.abc import Iterator
from pathlib import Path

LOCK_ENV = "HARNESS_VERIFY_LOCK_HELD"
FLOOR_ENV = "HARNESS_VERIFY_MEMORY_FLOOR"
DEFAULT_MEMORY_FLOOR = 25.0
MEMORY_POLL_SECONDS = 30.0
QUEUE_LOG_SECONDS = 300.0
MEMORY_DEADLINE_SECONDS = 3600.0
PROBE_SECONDS = 5.0
QUEUE_POLL_SECONDS = 0.25
CHILD_WATCH_SECONDS = 0.25
ANCESTRY_DEPTH = 64
SIGNAL_GRACE_SECONDS = 5.0
LOCK_NAME = "verify.lock"
HOLDER_NAME = "verify.holder.json"
QUEUE_DIR = "verify.queue"
REGISTRY_NAME = "verify.registry.lock"
MEMINFO_PATH = Path("/proc/meminfo")
RECORD_NAME = re.compile(r"(\d{20})-(\d+)\.json")
MEMORY_FREE = re.compile(r"System[- ]wide memory free percentage:\s*(\d+(?:\.\d+)?)\s*%")
MEMINFO_VALUE = re.compile(r"\s*(\d+)\s*kB")


class VerifyLockError(Exception):
    """Admission refused before protected work: the caller reports it instead of running."""


class VerifyLockRefused(VerifyLockError):
    """Shared lock or queue state cannot be used safely, or the floor override is invalid."""


class MemoryFloorRefused(VerifyLockError):
    """Usable readings stayed below the memory floor for the whole bound."""


class SupervisorInterrupted(BaseException):
    """The supervisor received SIGINT or SIGTERM: the child's group is cleaned up before release."""

    def __init__(self, signum: int) -> None:
        super().__init__(signum)
        self.signum = signum


@dataclasses.dataclass
class State:
    """The opened shared state of one machine: stable descriptors, never reopened by path."""

    root: Path
    lock_fd: int
    registry_fd: int


def _now() -> float:
    """The monotonic clock; the seam the tests inject fake time through."""
    return time.monotonic()


def _sleep(seconds: float) -> None:
    """The wait between polls; the seam the tests shorten through."""
    time.sleep(seconds)


def _log(message: str) -> None:
    """One line to the operator's stderr, directly — not through a captured launcher."""
    print(f"[verify-lock] {message}", file=sys.stderr, flush=True)


def _stamp() -> str:
    """The local wall-clock time a holder started, for the waiters' logs."""
    return datetime.datetime.now().isoformat(timespec="seconds")


def state_base() -> Path:
    """The state base the shared root hangs off; an inheriting child must keep this, not the root.

    A child handed `XDG_STATE_HOME` pointing at the root itself would resolve
    the next layer down (`.../coding-harness/coding-harness`) and read another
    machine's state — so the environment a local child inherits names the base,
    and both sides resolve the same root.
    """
    base = os.environ.get("XDG_STATE_HOME")
    # A relative value is ignored, as the XDG base-directory rule says: it would resolve against each
    # entry's own working directory and split the shared admission (review row L1-3).
    return Path(base) if base and Path(base).is_absolute() else Path.home() / ".local" / "state"


def state_root() -> Path:
    """The shared state root of this user on this machine; no repository or worktree names it."""
    return state_base() / "coding-harness"


def _open_lock_file(path: Path) -> int:
    """A private regular file for flock locking, created once; an aliased path refuses.

    A symlink standing where the file belongs fails the no-follow open and
    refuses, so no substituted target is ever written or locked through.
    """
    try:
        return os.open(path, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    except FileExistsError:
        pass
    except OSError as error:
        raise VerifyLockRefused(f"{path} cannot be opened for locking ({error.strerror or error})") from error
    try:
        fd = os.open(path, os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError as error:
        raise VerifyLockRefused(f"{path} is not a private regular file; refusing substituted lock state") from error
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise VerifyLockRefused(f"{path} is not a regular file; refusing substituted lock state")
    return fd


def _prepare_state() -> State:
    """Open the shared state, refusing anything that cannot be used safely."""
    root = state_root()
    try:
        root.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise VerifyLockRefused(
            f"the shared state directory {root} cannot be created ({error.strerror or error})"
        ) from error
    if root.is_symlink() or not root.is_dir():
        raise VerifyLockRefused(f"the shared state directory {root} is not a usable directory")
    queue = root / QUEUE_DIR
    try:
        queue.mkdir(exist_ok=True)
    except OSError as error:
        raise VerifyLockRefused(f"the queue directory {queue} cannot be created ({error.strerror or error})") from error
    if queue.is_symlink() or not queue.is_dir():
        raise VerifyLockRefused(f"the queue directory {queue} is not a usable directory")
    return State(
        root=root, lock_fd=_open_lock_file(root / LOCK_NAME), registry_fd=_open_lock_file(root / REGISTRY_NAME)
    )


def read_holder(root: Path | None = None) -> dict | None:
    """The published ownership, read without following symlinks; None when absent or unusable."""
    base = state_root() if root is None else root
    try:
        fd = os.open(base / HOLDER_NAME, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None
        payload = b""
        while len(payload) < 65536:
            block = os.read(fd, 65536)
            if not block:
                break
            payload += block
    finally:
        os.close(fd)
    try:
        holder = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if not isinstance(holder, dict) or not isinstance(holder.get("pid"), int):
        return None
    return holder


def _describe_holder(holder: dict | None) -> str:
    """One line naming a holder's pid, command and start time — or saying none is published."""
    if holder is None:
        return "no active holder is published; the lock may be held by a killed entry's inherited child"
    command = holder.get("command")
    words = " ".join(str(word) for word in command) if isinstance(command, list) else "unknown command"
    return f"holder pid {holder.get('pid')} ({words}, started {holder.get('start', 'unknown')})"


def nested_holder_pid() -> int | None:
    """The holder pid of a valid inherited admission, or None.

    The marker is valid only when the published ownership names its process
    and the work lock is genuinely held; a stale marker (its admission
    released) or an unrelated one (another admission owns the lock) falls back
    to ordinary admission. The holder process itself is not required to live:
    a killed supervisor leaves the lock held by the descriptor its protected
    child inherited, and that child's own nested calls must still nest.
    """
    raw = os.environ.get(LOCK_ENV, "").strip()
    if not raw.isdigit() or int(raw) <= 0:
        return None
    pid = int(raw)
    holder = read_holder()
    if holder is None or holder.get("pid") != pid:
        return None
    lock = state_root() / LOCK_NAME
    # Metadata names a holder; only a relation proves this process descends from it (review row F6-2).
    if not _related_to_holder(pid, holder):
        return None
    try:
        fd = os.open(lock, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError:
        return None
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            # Read the holder again after the probe: a release unpublishes before it unlocks and a
            # new admission publishes after it locks, so an unchanged holder here means the lock
            # seen held is still the marker's (review rows L1-1, L1-12).
            again = read_holder()
            return pid if again is not None and again.get("pid") == pid else None
        fcntl.flock(fd, fcntl.LOCK_UN)
        return None
    finally:
        os.close(fd)


def _parent_of(pid: int) -> int | None:
    """The parent pid of a live process, or None when it cannot be read."""
    if pid == os.getpid():
        return os.getppid()
    try:
        done = subprocess.run(
            ["ps", "-o", "ppid=", "-p", str(pid)],
            capture_output=True,
            text=True,
            timeout=PROBE_SECONDS,
            check=False,
            stdin=subprocess.DEVNULL,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    value = done.stdout.strip()
    return int(value) if done.returncode == 0 and value.isdigit() else None


def _descends_from(pid: int) -> bool:
    """True when `pid` is this process or one of its live ancestors."""
    current: int | None = os.getpid()
    for _ in range(ANCESTRY_DEPTH):
        if current is None or current <= 1:
            return False
        if current == pid:
            return True
        current = _parent_of(current)
    return False


def _related_to_holder(pid: int, holder: dict) -> bool:
    """A marker is honoured only for a real descendant of its admission.

    Two relations prove it: the holder is a live ancestor, or this process
    runs in the session the supervisor started for its protected child (which
    survives a killed supervisor, and no unrelated process can join). An open
    descriptor on the lock file proves nothing: any process can open it
    (review row F6-2, re-check).
    """
    if _descends_from(pid):
        return True
    session = holder.get("session")
    if isinstance(session, int) and session > 1:
        with contextlib.suppress(OSError):
            if os.getsid(0) == session:
                return True
    return False


def _memory_probe_output(command: list[str]) -> str | None:
    """The bounded stdout of one memory probe, or None when it cannot be taken."""
    try:
        done = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=PROBE_SECONDS,
            check=False,
            stdin=subprocess.DEVNULL,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if done.returncode != 0:
        return None
    return done.stdout


def read_available_memory(platform: str | None = None) -> float | None:
    """The system-wide available-memory percentage, or None when it cannot be measured.

    macOS `memory_pressure` names its system-wide free percentage; Linux
    `MemAvailable` over `MemTotal` from /proc/meminfo. Anything else — another
    platform, a failed or hung probe, a malformed reading — is None, and the
    caller logs an unknown reading and proceeds.
    """
    system = sys.platform if platform is None else platform
    if system == "darwin":
        output = _memory_probe_output(["memory_pressure"])
        if output is None:
            return None
        found = MEMORY_FREE.search(output)
        if found is None:
            return None
        value = float(found.group(1))
        return value if math.isfinite(value) else None  # 400 nines are infinity, not free memory (F6-4)
    if system == "linux":
        try:
            text = MEMINFO_PATH.read_text(encoding="utf-8")
        except OSError:
            return None
        fields: dict[str, int] = {}
        for line in text.splitlines():
            key, _, rest = line.partition(":")
            value = MEMINFO_VALUE.fullmatch(rest)
            if value is not None:
                fields[key.strip()] = int(value.group(1))
        available, total = fields.get("MemAvailable"), fields.get("MemTotal")
        if available is None or not total:
            return None
        return available / total * 100.0
    return None


def memory_floor() -> float:
    """The configured floor: 25 percent unless `HARNESS_VERIFY_MEMORY_FLOOR` names a valid one."""
    raw = os.environ.get(FLOOR_ENV, "").strip()
    if not raw:
        return DEFAULT_MEMORY_FLOOR
    try:
        floor = float(raw)
    except ValueError:
        raise VerifyLockRefused(f"{FLOOR_ENV}={raw!r} is not a finite percentage; refusing admission") from None
    if not math.isfinite(floor) or not 0.0 <= floor <= 100.0:
        raise VerifyLockRefused(f"{FLOOR_ENV}={raw!r} is not a finite percentage in [0, 100]; refusing admission")
    return floor


@contextlib.contextmanager
def _registry_lock(state: State) -> Iterator[None]:
    """The short-held registry lock that serialises registration, pruning and turn-taking."""
    fcntl.flock(state.registry_fd, fcntl.LOCK_EX)
    try:
        yield
    finally:
        fcntl.flock(state.registry_fd, fcntl.LOCK_UN)


_ACTIVE_LOCK = threading.Lock()
_ACTIVE: _Admission | None = None


def _active_pid() -> int | None:
    """The pid this process publishes while it owns an admission, for the children's marker."""
    with _ACTIVE_LOCK:
        return os.getpid() if _ACTIVE is not None else None


class _Admission:
    """One entry's queue wait, ownership and memory gate on an opened state."""

    def __init__(self, state: State, command: list[str]) -> None:
        self.state = state
        self.command = [str(word) for word in command]
        self.entered = 0.0
        self.record_name: str | None = None
        self.record_fd: int | None = None
        self._published = False
        self._released = False

    def enter(self) -> None:
        """Queue for the work lock, publish ownership, then hold the memory gate."""
        self.entered = _now()
        self._queue_wait()
        self._publish()
        with _ACTIVE_LOCK:
            global _ACTIVE
            _ACTIVE = self
        self._memory_gate()

    def release(self) -> None:
        """End the ownership in every ending; a second call does nothing."""
        if self._released:
            return
        self._released = True
        with _ACTIVE_LOCK:
            global _ACTIVE
            if _ACTIVE is self:
                _ACTIVE = None
        # Only the owner removes the record, and only while it still names this process: a
        # cancelled waiter never published one and must not delete the active holder's (review row F6-1).
        if self._published:
            holder = read_holder(self.state.root)
            if holder is not None and holder.get("pid") == os.getpid():
                with contextlib.suppress(OSError):
                    (self.state.root / HOLDER_NAME).unlink()
        # Close, never unlock: the lock belongs to the open description, and a protected descendant
        # that inherited it and outlived the group kill keeps it until it exits (review row L1-11).
        os.close(self.state.lock_fd)
        if self.record_name is not None:
            with _registry_lock(self.state), contextlib.suppress(OSError):
                (self.state.root / QUEUE_DIR / self.record_name).unlink()
            if self.record_fd is not None:
                os.close(self.record_fd)
            self.record_name = None
            self.record_fd = None
        os.close(self.state.registry_fd)

    def _register(self) -> None:
        """Claim the next registration number, under the registry lock, with a live record."""
        with _registry_lock(self.state):
            queue = self.state.root / QUEUE_DIR
            try:
                names = os.listdir(queue)
            except OSError as error:
                raise VerifyLockRefused(f"the queue directory {queue} cannot be read ({error})") from error
            highest = 0
            for name in names:
                matched = RECORD_NAME.fullmatch(name)
                if matched is not None:
                    highest = max(highest, int(matched.group(1)))
            path = queue / f"{highest + 1:020d}-{os.getpid()}.json"
            try:
                fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            except OSError as error:
                raise VerifyLockRefused(
                    f"the queue record {path.name} cannot be created ({error.strerror or error})"
                ) from error
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as error:
                os.close(fd)
                raise VerifyLockRefused(
                    f"the queue record {path.name} cannot be locked ({error.strerror or error})"
                ) from error
            self.record_name = path.name
            self.record_fd = fd

    def _prune_locked(self) -> None:
        """Remove dead waiters' records while holding the registry lock."""
        queue = self.state.root / QUEUE_DIR
        try:
            names = sorted(os.listdir(queue))
        except OSError as error:
            raise VerifyLockRefused(f"the queue directory {queue} cannot be read ({error})") from error
        for name in names:
            if name == self.record_name or RECORD_NAME.fullmatch(name) is None:
                continue
            try:
                fd = os.open(queue / name, os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK)
            except FileNotFoundError:
                continue
            except OSError as error:
                raise VerifyLockRefused(
                    f"the queue record {name} cannot be used ({error.strerror or error})"
                ) from error
            try:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except OSError:
                    continue
                with contextlib.suppress(OSError):
                    (queue / name).unlink()
            finally:
                os.close(fd)

    def _live_records_locked(self) -> list[str]:
        """The queue records in registration order, while holding the registry lock."""
        queue = self.state.root / QUEUE_DIR
        try:
            names = sorted(os.listdir(queue))
        except OSError as error:
            raise VerifyLockRefused(f"the queue directory {queue} cannot be read ({error})") from error
        return [name for name in names if RECORD_NAME.fullmatch(name) is not None]

    def _try_acquire_work(self) -> bool:
        """Take the work lock without waiting; only the first live waiter may try."""
        try:
            fcntl.flock(self.state.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return False
        return True

    def _leave_queue_locked(self) -> None:
        """Drop our own record once the work lock is ours, while holding the registry lock."""
        if self.record_name is None:
            return
        with contextlib.suppress(OSError):
            (self.state.root / QUEUE_DIR / self.record_name).unlink()
        if self.record_fd is not None:
            os.close(self.record_fd)
        self.record_name = None
        self.record_fd = None

    def publish_session(self, session: int) -> None:
        """Republish ownership naming the session of the supervised child, for its descendants."""
        self._publish(session)

    def _publish(self, session: int | None = None) -> None:
        """Publish pid, command and start time (and the child's session) while owning admission."""
        record: dict[str, object] = {"pid": os.getpid(), "command": self.command, "start": _stamp()}
        if session is not None:
            record["session"] = session
        payload = json.dumps(record).encode("utf-8")
        path = self.state.root / HOLDER_NAME
        # A fresh file renamed over the record replaces the directory entry itself, so a hard link
        # planted in its place is unlinked, never written through (review row F6-3).
        fresh = self.state.root / f".{HOLDER_NAME}.{os.getpid()}"
        try:
            with contextlib.suppress(FileNotFoundError):
                fresh.unlink()
            descriptor = os.open(fresh, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
            fresh.replace(path)
            self._published = True
        except OSError as error:
            with contextlib.suppress(OSError):
                fresh.unlink()
            raise VerifyLockRefused(
                f"the holder record {path} cannot be published ({error.strerror or error})"
            ) from error

    def _queue_wait(self) -> None:
        """Wait for our registration turn, logging the wait and the holder as it goes."""
        self._register()
        announced = False
        last_log: float | None = None
        while True:
            with _registry_lock(self.state):
                self._prune_locked()
                records = self._live_records_locked()
                if self.record_name not in records:
                    raise VerifyLockRefused("our own queue record disappeared; the shared queue state is unusable")
                if records[0] == self.record_name and self._try_acquire_work():
                    self._leave_queue_locked()
                    waited = _now() - self.entered
                    _log(f"admitted after {waited:.0f}s" if waited >= 1.0 else "admitted")
                    return
            described = _describe_holder(read_holder(self.state.root))
            now = _now()
            if not announced:
                _log(f"waiting for admission: {described}")
                announced = True
                last_log = now
            elif last_log is not None and now - last_log >= QUEUE_LOG_SECONDS:
                _log(f"still waiting for admission ({now - self.entered:.0f}s): {described}")
                last_log = now
            _sleep(QUEUE_POLL_SECONDS)

    def _memory_gate(self) -> None:
        """Read memory while owning the lock; wait below the floor, refuse at the bound."""
        floor = memory_floor()
        low_since: float | None = None
        while True:
            reading = read_available_memory()
            if reading is None:
                _log("available memory cannot be measured; proceeding without a reading")
                return
            if reading >= floor:
                _log(f"available memory {reading:g}% at or above the {floor:g}% floor; starting")
                return
            now = _now()
            if low_since is None:
                low_since = now
                _log(
                    f"available memory {reading:g}% below the {floor:g}% floor; rechecking every {MEMORY_POLL_SECONDS:g}s"
                )
            elif now - low_since >= MEMORY_DEADLINE_SECONDS:
                raise MemoryFloorRefused(
                    f"available memory stayed below the {floor:g}% floor for "
                    f"{MEMORY_DEADLINE_SECONDS / 60:.0f} minutes; last reading {reading:g}%"
                )
            _log(f"available memory {reading:g}% below the {floor:g}% floor; waiting")
            _sleep(MEMORY_POLL_SECONDS)


@contextlib.contextmanager
def hold_admission(command: list[str]) -> Iterator[int | None]:
    """One machine admission around protected work: queue, memory gate, published ownership.

    Yields the lock descriptor local children must inherit, or None when this
    entry is nested in an ancestor's admission. Refusals raise
    VerifyLockRefused or MemoryFloorRefused before the body runs; release
    happens in every ending, after any child cleanup the caller does.
    """
    inherited = nested_holder_pid()
    if inherited is not None:
        _log(f"inheriting admission from pid {inherited}; no queue and no memory wait")
        yield None
        return
    admission = _Admission(_prepare_state(), command)
    try:
        admission.enter()
    except BaseException:
        admission.release()
        raise
    try:
        yield admission.state.lock_fd
    finally:
        admission.release()


def inherit_env(env: dict[str, str]) -> dict[str, str]:
    """The environment a local check runs under, with the admission state it must carry.

    This is additive and local-only: a runner's allowlist stays closed, foreign
    calls receive none of these names, and a genuine inherited marker travels
    so a nested check reuses its ancestor's admission even after local
    environment filtering.
    """
    env = dict(env)
    env["XDG_STATE_HOME"] = str(state_base())
    if FLOOR_ENV in os.environ:
        env[FLOOR_ENV] = os.environ[FLOOR_ENV]
    marker = nested_holder_pid() or _active_pid()
    if marker is not None:
        env[LOCK_ENV] = str(marker)
    else:
        env.pop(LOCK_ENV, None)
    return env


def _install_signal_handlers() -> dict[int, object]:
    """Turn SIGINT, SIGTERM, SIGHUP and SIGQUIT into an interrupt that cleans the child up before release.

    SIGHUP and SIGQUIT are trapped too, so a closed terminal or a quit key never skips the cleanup
    by the default action (review row L4-3).
    """
    previous: dict[int, object] = {}
    if threading.current_thread() is not threading.main_thread():
        return previous

    def interrupted(signum: int, _frame: object) -> None:
        raise SupervisorInterrupted(signum)

    for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT):
        with contextlib.suppress(ValueError, OSError):
            previous[signum] = signal.signal(signum, interrupted)
    return previous


def _hold_signals_during_cleanup(previous: dict[int, object]) -> None:
    """A further trapped signal while the child is stopped is ignored, never raised past the release.

    The first signal already ends the run and sets its exit code (review row L3-3).
    """
    for signum in previous:
        with contextlib.suppress(ValueError, OSError):
            signal.signal(signum, signal.SIG_IGN)


def _restore_signal_handlers(previous: dict[int, object]) -> None:
    for signum, handler in previous.items():
        with contextlib.suppress(ValueError, OSError):
            signal.signal(signum, handler)  # type: ignore[arg-type]


def _spawn_child(command: list[str], pass_fds: tuple[int, ...], override_marker: int | None) -> subprocess.Popen[bytes]:
    """The protected command in its own session, stdout and stderr reaching the operator."""
    env = dict(os.environ)
    if override_marker is not None:
        env[LOCK_ENV] = str(override_marker)
    return subprocess.Popen(command, env=env, stdin=subprocess.DEVNULL, start_new_session=True, pass_fds=pass_fds)


def _watch_child(child: subprocess.Popen[bytes]) -> int:
    """Wait for the child, letting signals raise through to the cleanup."""
    while True:
        try:
            return child.wait(timeout=CHILD_WATCH_SECONDS)
        except subprocess.TimeoutExpired:
            continue


def _stop_child(child: subprocess.Popen[bytes]) -> None:
    """End the child's whole process group, gently first — before the lock is released."""
    with contextlib.suppress(OSError, subprocess.TimeoutExpired):
        os.killpg(child.pid, signal.SIGTERM)
        child.wait(timeout=SIGNAL_GRACE_SECONDS)
    with contextlib.suppress(OSError):
        os.killpg(child.pid, signal.SIGKILL)
    with contextlib.suppress(OSError, subprocess.TimeoutExpired):
        child.wait(timeout=SIGNAL_GRACE_SECONDS)


def _group_alive(group: int) -> bool:
    try:
        os.killpg(group, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def end_lingering_group(group: int) -> None:
    """End what is left of the protected command's process group after the command itself exited.

    Admission covers every protected descendant: a grandchild that outlives the command is ended,
    gently first, before the lock is released (review row F6-5). The runner's timed launches call
    this too, so a check held through `hold_admission` never returns over a live group.
    """
    if not _group_alive(group):
        return
    _log(f"the command exited; ending its remaining process group {group}")
    for signum in (signal.SIGTERM, signal.SIGKILL):
        with contextlib.suppress(OSError):
            os.killpg(group, signum)
        deadline = time.monotonic() + SIGNAL_GRACE_SECONDS
        while time.monotonic() < deadline:
            if not _group_alive(group):
                return
            time.sleep(CHILD_WATCH_SECONDS)


def supervise(command: list[str]) -> int:
    """Queue, check memory and run one protected command; return its exit code."""
    if not command:
        print("[verify-lock] no command given; nothing is protected", file=sys.stderr, flush=True)
        return 2
    previous = _install_signal_handlers()
    child: subprocess.Popen[bytes] | None = None
    admission: _Admission | None = None
    try:
        inherited = nested_holder_pid()
        if inherited is not None:
            _log(f"inheriting admission from pid {inherited}; no queue and no memory wait")
            child = _spawn_child(command, (), None)
        else:
            admission = _Admission(_prepare_state(), command)
            admission.enter()
            child = _spawn_child(command, (admission.state.lock_fd,), os.getpid())
            admission.publish_session(child.pid)
        code = _watch_child(child)
    except VerifyLockError as refused:
        print(f"[verify-lock] admission refused: {refused}", file=sys.stderr, flush=True)
        code = 3 if isinstance(refused, MemoryFloorRefused) else 2
    except SupervisorInterrupted as stop:
        code = 128 + stop.signum
    finally:
        _hold_signals_during_cleanup(previous)
        try:
            if child is not None and child.poll() is None:
                _stop_child(child)
            if child is not None:
                end_lingering_group(child.pid)
            if admission is not None:
                admission.release()
        finally:
            _restore_signal_handlers(previous)
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="One machine-wide admission for protected verification work.")
    parser.add_argument(
        "--held",
        action="store_true",
        help="exit 0 when the environment names a valid inherited admission, 1 otherwise",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, metavar="COMMAND", help="the protected command, after --")
    args = parser.parse_args(argv)
    if args.held:
        return 0 if nested_holder_pid() is not None else 1
    command = args.command[1:] if args.command[:1] == ["--"] else list(args.command)
    return supervise(command)


if __name__ == "__main__":
    raise SystemExit(main())
