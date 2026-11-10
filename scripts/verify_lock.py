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
identifies it. `verify.lock` is the compatibility work lock (`fcntl.flock`,
kernel-backed): the updated implementation holds it shared, so an older
checkout's exclusive holder still excludes every new entry, while new entries
do not exclude each other. Each admission reserves one slot — an exclusive
`verify.slot-<n>.lock` — up to the machine's capacity, and
`verify.slot-<n>.holder.json` publishes that slot's ownership (pid, command,
start time). The capacity comes from `verify.slots` in the same root — a
whitespace-trimmed positive decimal integer, re-read under the registry lock
for every reservation decision, with two as the declared default when the
file is absent; any other present content, or a substituted or unreadable
file, refuses admission. `verify.holder.json` is the older single-holder
record, kept only for legacy markers. `verify.queue/` holds one record per
waiter, held open under its owner's liveness flock so a dead waiter's record
is recognisable and pruned. A short-held `verify.registry.lock` serialises
registration, pruning and turn-taking; registration order is the reservation
order — `flock` alone supplies no FIFO, so only the first live record may
reserve a free slot.

**Nested work.** A protected entry descended from a live admission carries
`HARNESS_VERIFY_LOCK_HELD=<holder-pid>`, `HARNESS_VERIFY_LOCK_TOKEN=<token>`
—a random token each admission publishes with its ownership — and
`HARNESS_VERIFY_LOCK_SLOT=<slot>`, the index its ancestor reserved. The slot
marker is honoured only when that slot's lock is genuinely held and its
published ownership names the pid and the token; without a slot marker, the
legacy shape stands against `verify.holder.json` and the compatibility lock,
so an older checkout's descendants keep nesting. The environment reaches
every descendant — across new sessions, nested runners and a dead holder —
and no unrelated process knows the token, so no process relation has to be
proven (review rows F6-2, F6-6). An absent, malformed, stale or unrelated
marker uses ordinary admission. The holder process itself need not live: a
killed supervisor leaves the locks held by the descriptors its protected
child inherited, and that child's own nested calls still nest. Only the
owner removes the published ownership, and only while it still names the
owner.

**Admission context.** Each admission also carries a non-secret identity and
its measured queue-plus-memory wait (`admission_id`, `admission_wait` in the
published ownership, `HARNESS_VERIFY_ADMISSION_ID` /
`HARNESS_VERIFY_ADMISSION_WAIT` in a protected child's environment). A nested
entry resolves both from the validated ownership record and marks its wait as
reused — the ancestor's shared context, never measured or re-counted again
(bead coding-harness-1um6, `admission_context()`). The ownership token is
never part of the context.

**Boundary.** The admission protects the machine's load, not data. Normal
exit, failure, cancellation and trapped signals end the protected work before
release. A protected descendant can briefly outlive the admission only when an
intermediate process is killed hard (SIGKILL) while its own descendants run in
another process group; that overlap is an accepted limit, bounded by the
runner's step limits (spec, "Boundary").

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

The supervisor queues for a free slot, checks memory, publishes ownership on
its slot for its child — which inherits the slot and compatibility lock
descriptors, so ownership outlives a killed supervisor for exactly as long
as the protected child and its own children run — and releases only after
the child's process group is gone, including failure,
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
import hmac
import json
import math
import os
import re
import secrets
import signal
import stat
import subprocess
import sys
import threading
import time
import uuid
from collections.abc import Callable, Iterator
from pathlib import Path

LOCK_ENV = "HARNESS_VERIFY_LOCK_HELD"
TOKEN_ENV = "HARNESS_VERIFY_LOCK_TOKEN"
SLOT_ENV = "HARNESS_VERIFY_LOCK_SLOT"
FLOOR_ENV = "HARNESS_VERIFY_MEMORY_FLOOR"
# The non-secret admission context (bead coding-harness-1um6): the id names the
# admission to its descendants, the wait is the measured queue-plus-memory
# seconds. The ownership token never travels in either — it stays in TOKEN_ENV
# alone, the one secret of the relation.
ADMISSION_ID_ENV = "HARNESS_VERIFY_ADMISSION_ID"
ADMISSION_WAIT_ENV = "HARNESS_VERIFY_ADMISSION_WAIT"
DEFAULT_MEMORY_FLOOR = 25.0
MEMORY_POLL_SECONDS = 30.0
QUEUE_LOG_SECONDS = 300.0
MEMORY_DEADLINE_SECONDS = 3600.0
PROBE_SECONDS = 5.0
QUEUE_POLL_SECONDS = 0.25
CHILD_WATCH_SECONDS = 0.25
SIGNAL_GRACE_SECONDS = 5.0
LOCK_NAME = "verify.lock"
HOLDER_NAME = "verify.holder.json"
QUEUE_DIR = "verify.queue"
REGISTRY_NAME = "verify.registry.lock"
# The configurable capacity (bead coding-harness-u1ha): one file, one value,
# no per-checkout copy. The per-slot locks and records hang beside it.
SLOTS_NAME = "verify.slots"
DEFAULT_SLOTS = 2
SLOT_LOCK_FILE = re.compile(r"verify\.slot-(\d+)\.lock")
CAPACITY_VALUE = re.compile(r"[0-9]+")
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


def slot_lock_name(index: int) -> str:
    """The lock file name of one slot; indices are zero-based."""
    return f"verify.slot-{index}.lock"


def slot_holder_name(index: int) -> str:
    """The ownership record name of one slot; indices are zero-based."""
    return f"verify.slot-{index}.holder.json"


def read_capacity(root: Path | None = None) -> int:
    """The declared machine-wide slot capacity: `DEFAULT_SLOTS` unless `verify.slots` says otherwise.

    A missing file means the default. Present content must be a
    whitespace-trimmed positive decimal integer and nothing else; a
    substituted (symlinked or nonregular) or unreadable file, and any other
    present content, refuse admission with a diagnostic before any protected
    work. The file is read without following symlinks and never written here;
    every reservation decision re-reads it, so a lowered capacity drains
    before new reservations are granted (bead coding-harness-u1ha).
    """
    base = state_root() if root is None else root
    path = base / SLOTS_NAME
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return DEFAULT_SLOTS
    except OSError as error:
        raise VerifyLockRefused(
            f"the capacity setting {path} cannot be read ({error.strerror or error}); refusing admission"
        ) from error
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise VerifyLockRefused(f"the capacity setting {path} is not a regular file; refusing substituted state")
        payload = b""
        while len(payload) < 65536:
            block = os.read(fd, 65536)
            if not block:
                break
            payload += block
    except OSError as error:
        raise VerifyLockRefused(
            f"the capacity setting {path} cannot be read ({error.strerror or error}); refusing admission"
        ) from error
    finally:
        os.close(fd)
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        raise VerifyLockRefused(f"the capacity setting {path} is not valid UTF-8; refusing substituted state") from None
    raw = text.strip()
    if CAPACITY_VALUE.fullmatch(raw) is None or int(raw) <= 0:
        raise VerifyLockRefused(
            f"the capacity setting {path} holds {text!r}; a whitespace-trimmed positive decimal "
            "integer is the only accepted content; refusing admission"
        )
    return int(raw)


def _read_record(path: Path) -> dict | None:
    """One published ownership record, read without following symlinks; None when absent or unusable."""
    try:
        # Non-blocking, so a FIFO planted in the record's place is refused below, never waited on (F6-7).
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
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


def read_holder(root: Path | None = None) -> dict | None:
    """The legacy single-holder ownership; kept for older checkouts' records and markers.

    The updated implementation publishes per-slot records instead; this file
    is never written here, only read for a legacy marker's validation.
    """
    base = state_root() if root is None else root
    return _read_record(base / HOLDER_NAME)


def read_slot_holder(root: Path, index: int) -> dict | None:
    """The published ownership of slot `index`, read without following symlinks; None when absent."""
    return _read_record(root / slot_holder_name(index))


def _describe_holder(holder: dict | None) -> str:
    """One line naming a holder's pid, command and start time — or saying none is published."""
    if holder is None:
        return "no active holder is published; the lock may be held by a killed entry's inherited child"
    command = holder.get("command")
    words = " ".join(str(word) for word in command) if isinstance(command, list) else "unknown command"
    return f"holder pid {holder.get('pid')} ({words}, started {holder.get('start', 'unknown')})"


def _describe_occupied(root: Path, occupied: list[tuple[int, dict | None]]) -> str:
    """Every occupied slot with its published holder — or, with none, the compatibility lock's holder.

    A token never appears: the records' names, commands and start times are
    operator diagnostics, the token stays the admission's secret.
    """
    if not occupied:
        return _describe_holder(read_holder(root))
    return "; ".join(f"slot {index}: {_describe_holder(holder)}" for index, holder in occupied)


def _probe_held_lock(lock: Path, reader: Callable[[], dict | None], pid: int, token: str) -> bool:
    """Whether `lock` is genuinely held for the marker (pid, token), read twice around the probe.

    The record is read again after the probe: a release unpublishes before it
    unlocks and a new admission publishes after it locks, so an unchanged
    record here means the lock seen held is still the marker's (review rows
    L1-1, L1-12).
    """
    try:
        fd = os.open(lock, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        return False
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            again = reader()
            return again is not None and _names(again, pid, token)
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    finally:
        os.close(fd)


def _nested_relation() -> tuple[int, int | None] | None:
    """The holder pid and reserved slot of a valid inherited admission, or None.

    A slot marker is honoured only when that exact slot's lock is genuinely
    held and its published ownership names the marker's process and token; a
    malformed, stale or unrelated slot marker falls back to ordinary
    admission. Without a slot marker, the legacy shape stands: the
    compatibility lock genuinely held and the legacy record naming the
    marker's process and token — an older checkout's admission. The holder
    process itself is not required to live: a killed supervisor leaves the
    locks held by the descriptors its protected child inherited, and that
    child's own nested calls must still nest.
    """
    raw = os.environ.get(LOCK_ENV, "").strip()
    if not raw.isdigit() or int(raw) <= 0:
        return None
    pid = int(raw)
    token = os.environ.get(TOKEN_ENV, "")
    slot_raw = os.environ.get(SLOT_ENV, "").strip()
    if slot_raw:
        if not slot_raw.isdigit():
            return None
        slot = int(slot_raw)
        holder = read_slot_holder(state_root(), slot)
        if holder is None or not _names(holder, pid, token):
            return None
        held = _probe_held_lock(
            state_root() / slot_lock_name(slot), lambda: read_slot_holder(state_root(), slot), pid, token
        )
        return (pid, slot) if held else None
    holder = read_holder()
    if holder is None or not _names(holder, pid, token):
        return None
    held = _probe_held_lock(state_root() / LOCK_NAME, read_holder, pid, token)
    return (pid, None) if held else None


def nested_holder_pid() -> int | None:
    """The holder pid of a valid inherited admission, or None."""
    relation = _nested_relation()
    return None if relation is None else relation[0]


def _names(holder: dict, pid: int, token: str) -> bool:
    """True when the published ownership names this pid and this admission's token.

    The token is the relation: it travels only in the environment of the
    admission's own descendants (review rows F6-2, F6-6).
    """
    published = holder.get("token")
    return (
        holder.get("pid") == pid
        and isinstance(published, str)
        and bool(token)
        and hmac.compare_digest(published, token)
    )


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


def _active_token() -> str | None:
    """The token this process publishes while it owns an admission, for the children's marker."""
    with _ACTIVE_LOCK:
        return _ACTIVE.token if _ACTIVE is not None else None


def _active_slot() -> int | None:
    """The slot this process's own active admission reserved, for the children's slot marker."""
    with _ACTIVE_LOCK:
        return _ACTIVE.slot_index if _ACTIVE is not None else None


def inherit_fds(owned: int | None = None) -> tuple[int, ...]:
    """Every descriptor a local child must inherit to keep this admission's ownership alive.

    The active admission holds two locks: its reserved slot and the shared
    compatibility lock — a child that loses either could overlap a peer or a
    legacy exclusive holder, including after this supervisor is killed hard.
    Both come from the active admission, so a caller that holds
    `hold_admission` hands them on whole; a nested entry owns no descriptor of
    its own and inherits nothing here.
    """
    with _ACTIVE_LOCK:
        active = _ACTIVE
    if active is None or active.slot_fd is None:
        return () if owned is None else (owned,)
    return (active.slot_fd, active.state.lock_fd)


def _active_context() -> AdmissionContext | None:
    """The measured context of this process's own active admission, or None."""
    with _ACTIVE_LOCK:
        if _ACTIVE is not None:
            return AdmissionContext(_ACTIVE.admission_id, _ACTIVE.wait_seconds, False)
    return None


@dataclasses.dataclass(frozen=True)
class AdmissionContext:
    """The admission a measurement run happened under (bead coding-harness-1um6).

    `admission_id` is the non-secret admission UUID, `wait_seconds` the queue
    plus memory wait measured by the admission that owns or owns the ancestor
    lock. `reused` is True for an inherited admission (the wait is the
    ancestor's shared context, never re-counted), False for a fresh one, and
    None when no admission context is known at all.
    """

    admission_id: str | None
    wait_seconds: float | None
    reused: bool | None


def _finite_wait(value: object) -> float | None:
    """A published or inherited wait as a finite non-negative float, else None."""
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value) if math.isfinite(value) and value >= 0 else None


def admission_context() -> AdmissionContext:
    """The admission context this process runs under, whichever way it reaches it.

    This process's own active admission first, then the context the admission
    supervisor handed its protected command through the environment — the
    runner decides once whether that context is its own fresh measurement or
    an inherited one and clears the variables for its nested runs — then an
    inherited marker, whose id and wait are read from the validated ownership
    record, never measured again. Old ownership records published before this
    field existed read as unknown values, never as guesses.
    """
    own = _active_context()
    if own is not None:
        return own
    given = os.environ.get(ADMISSION_ID_ENV, "").strip()
    if given:
        return AdmissionContext(given, _parse_wait(os.environ.get(ADMISSION_WAIT_ENV)), False)
    relation = _nested_relation()
    if relation is not None:
        pid, slot = relation
        token = os.environ.get(TOKEN_ENV, "")
        # The context comes from the same record the marker was validated
        # against: the ancestor's own slot, never a peer's.
        holder = read_slot_holder(state_root(), slot) if slot is not None else read_holder()
        if holder is not None and _names(holder, pid, token):
            return AdmissionContext(
                admission_id=holder.get("admission_id") if isinstance(holder.get("admission_id"), str) else None,
                wait_seconds=_finite_wait(holder.get("admission_wait")),
                reused=True,
            )
        return AdmissionContext(None, None, True)
    return AdmissionContext(None, None, None)


def _parse_wait(raw: str | None) -> float | None:
    """An inherited wait from the environment as a float, else None."""
    try:
        value = float(raw or "")
    except ValueError:
        return None
    return value if math.isfinite(value) and value >= 0 else None


class _Admission:
    """One entry's queue wait, slot reservation, ownership and memory gate on an opened state."""

    def __init__(self, state: State, command: list[str]) -> None:
        self.state = state
        self.command = [str(word) for word in command]
        self.entered = 0.0
        self.record_name: str | None = None
        self.record_fd: int | None = None
        self.slot_index: int | None = None
        self.slot_fd: int | None = None
        self.token = secrets.token_hex(16)
        # The non-secret identity of this admission and its measured
        # queue-plus-memory wait (bead coding-harness-1um6); the wait is only
        # known once the memory gate has passed, so the first publish carries
        # None and the second the measurement.
        self.admission_id = uuid.uuid4().hex
        self.wait_seconds: float | None = None
        self.started = _stamp()
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
        self.wait_seconds = _now() - self.entered
        # The same ownership, republished with the measured wait: a nested
        # entry resolves its shared context from this record.
        self._publish()

    def release(self) -> None:
        """End the ownership in every ending; a second call does nothing."""
        if self._released:
            return
        self._released = True
        with _ACTIVE_LOCK:
            global _ACTIVE
            if _ACTIVE is self:
                _ACTIVE = None
        # Only the owner removes its own slot's record, and only while it still names this
        # process and token: a cancelled waiter never published one and must not delete the
        # slot's active holder's (review row F6-1), and a peer's slot state stays untouched.
        if self._published and self.slot_index is not None:
            holder = read_slot_holder(self.state.root, self.slot_index)
            if holder is not None and _names(holder, os.getpid(), self.token):
                with contextlib.suppress(OSError):
                    (self.state.root / slot_holder_name(self.slot_index)).unlink()
        # Close, never unlock: each lock belongs to its open description, and a protected
        # descendant that inherited one and outlived the group kill keeps it until it exits
        # (review row L1-11).
        if self.slot_fd is not None:
            os.close(self.slot_fd)
            self.slot_fd = None
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

    def _survey_slots_locked(self) -> tuple[list[tuple[int, dict | None]], list[tuple[int, int]]]:
        """Which slot locks are genuinely held, and which are free, while holding the registry lock.

        A held lock counts against the capacity whatever its index — one at or
        above a lowered capacity keeps its reservation until it drains. A
        free lock file is a reusable index; lock files are never unlinked.
        Liveness is the flock alone: a record's content is never trusted for
        it, only read for the waiters' diagnostics.
        """
        root = self.state.root
        try:
            names = os.listdir(root)
        except OSError as error:
            raise VerifyLockRefused(f"the shared state directory {root} cannot be read ({error})") from error
        indices = sorted(
            int(matched.group(1)) for name in names if (matched := SLOT_LOCK_FILE.fullmatch(name)) is not None
        )
        occupied: list[tuple[int, dict | None]] = []
        free: list[tuple[int, int]] = []
        for index in indices:
            fd = _open_lock_file(root / slot_lock_name(index))
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                os.close(fd)
                occupied.append((index, read_slot_holder(root, index)))
            else:
                free.append((index, fd))
        return occupied, free

    def _reserve_admission_locked(self) -> tuple[bool, list[tuple[int, dict | None]]]:
        """Try to reserve one free slot and the shared compatibility lock, under the registry lock.

        The capacity is re-read for every decision. Only genuinely held slot
        locks count against it — including indices at or above a lowered
        capacity — and only a free index below it is reserved, the lowest
        first, reusing freed indices. A legacy exclusive holder on the
        compatibility lock excludes the reservation; shared holders do not
        exclude each other.
        """
        capacity = read_capacity(self.state.root)
        occupied, free = self._survey_slots_locked()
        if len(occupied) >= capacity:
            for _index, fd in free:
                os.close(fd)
            return False, occupied
        held = {index for index, _holder in occupied}
        chosen_index: int | None = None
        chosen_fd: int | None = None
        for index in range(capacity):
            if index in held:
                continue
            fd = next((entry_fd for entry_index, entry_fd in free if entry_index == index), None)
            if fd is None:
                # A lock file that did not exist at the survey: create it and take the lock now,
                # so the reservation is a genuinely held slot, not an unlocked file.
                fd = _open_lock_file(self.state.root / slot_lock_name(index))
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except OSError:
                    os.close(fd)
                    continue
            chosen_index, chosen_fd = index, fd
            break
        if chosen_fd is None:
            for _index, fd in free:
                os.close(fd)
            return False, occupied
        try:
            fcntl.flock(self.state.lock_fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except OSError:
            # An older checkout's exclusive admission: wait it out, keep the queue position.
            for _index, fd in free:
                os.close(fd)
            if all(fd != chosen_fd for _index, fd in free):
                os.close(chosen_fd)
            return False, occupied
        self.slot_index, self.slot_fd = chosen_index, chosen_fd
        for _index, fd in free:
            if fd != chosen_fd:
                os.close(fd)
        return True, occupied

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

    def _publish(self) -> None:
        """Publish pid, token, command, start time and the admission context on our own slot."""
        if self.slot_index is None:
            raise VerifyLockRefused("ownership cannot be published without a reserved slot")
        record = {
            "pid": os.getpid(),
            "token": self.token,
            "command": self.command,
            "start": self.started,
            "admission_id": self.admission_id,
            "admission_wait": self.wait_seconds,
        }
        payload = json.dumps(record).encode("utf-8")
        path = self.state.root / slot_holder_name(self.slot_index)
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
        """Wait for our registration turn, logging the wait and every occupied slot as it goes."""
        self._register()
        announced = False
        last_log: float | None = None
        while True:
            occupied: list[tuple[int, dict | None]] = []
            with _registry_lock(self.state):
                self._prune_locked()
                records = self._live_records_locked()
                if self.record_name not in records:
                    raise VerifyLockRefused("our own queue record disappeared; the shared queue state is unusable")
                if records[0] == self.record_name:
                    reserved, occupied = self._reserve_admission_locked()
                    if reserved:
                        self._leave_queue_locked()
                        waited = _now() - self.entered
                        _log(f"admitted after {waited:.0f}s" if waited >= 1.0 else "admitted")
                        return
                else:
                    # Not our turn: still name every occupied slot for the operator.
                    occupied, free = self._survey_slots_locked()
                    for _index, fd in free:
                        os.close(fd)
            described = _describe_occupied(self.state.root, occupied)
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
    """One machine admission around protected work: queue for a slot, memory gate, published ownership.

    Yields the slot descriptor local children must inherit, or None when this
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
        yield admission.slot_fd
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
    relation = _nested_relation()
    if relation is not None:
        marker, slot, token = relation[0], relation[1], os.environ.get(TOKEN_ENV)
    else:
        marker, slot, token = _active_pid(), _active_slot(), _active_token()
    if marker is not None and token:
        env[LOCK_ENV] = str(marker)
        env[TOKEN_ENV] = token
        if slot is not None:
            env[SLOT_ENV] = str(slot)
        else:
            env.pop(SLOT_ENV, None)
    else:
        env.pop(LOCK_ENV, None)
        env.pop(TOKEN_ENV, None)
        env.pop(SLOT_ENV, None)
    # The admission context resolves the same way the child itself would: its
    # own active admission, an inherited one, or nothing (bead
    # coding-harness-1um6). A fresh context travels so the child records the
    # measured wait as its own; an inherited one does not travel — the child
    # resolves the shared context from the validated ownership record instead.
    # Never the token.
    context = admission_context()
    if context.admission_id is not None and context.reused is False:
        env[ADMISSION_ID_ENV] = context.admission_id
        if context.wait_seconds is not None:
            env[ADMISSION_WAIT_ENV] = repr(context.wait_seconds)
    else:
        env.pop(ADMISSION_ID_ENV, None)
        env.pop(ADMISSION_WAIT_ENV, None)
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


@contextlib.contextmanager
def _deferred_signals(trapped: dict[int, object]):
    """Hold a trapped signal back while the child is started, and raise it once the child is registered.

    A signal between `Popen` creating the process and the assignment that hands it to the cleanup
    would otherwise leave the protected group unknown to it (phase-6 row F6-9). This is the
    supervisor's form of the runner's `defer_launch_signals`.
    """
    pending: list[int] = []
    installed: dict[int, object] = {}
    for signum in trapped:
        with contextlib.suppress(ValueError, OSError):
            installed[signum] = signal.signal(signum, lambda received, _frame: pending.append(received))
    try:
        yield
    finally:
        for signum, handler in installed.items():
            with contextlib.suppress(ValueError, OSError):
                signal.signal(signum, handler)  # type: ignore[arg-type]
    if pending:
        raise SupervisorInterrupted(pending[0])


def _restore_signal_handlers(previous: dict[int, object]) -> None:
    for signum, handler in previous.items():
        with contextlib.suppress(ValueError, OSError):
            signal.signal(signum, handler)  # type: ignore[arg-type]


def _spawn_child(
    command: list[str], pass_fds: tuple[int, ...], admission: _Admission | None
) -> subprocess.Popen[bytes]:
    """The protected command in its own session, stdout and stderr reaching the operator."""
    env = dict(os.environ)
    if admission is not None:
        env[LOCK_ENV] = str(os.getpid())
        env[TOKEN_ENV] = admission.token
        env[ADMISSION_ID_ENV] = admission.admission_id
        if admission.wait_seconds is not None:
            env[ADMISSION_WAIT_ENV] = repr(admission.wait_seconds)
        if admission.slot_index is not None:
            env[SLOT_ENV] = str(admission.slot_index)
    else:
        # A nested supervision inherits only the marker: the fresh context of
        # an ancestor's admission must not pass itself off as this child's own.
        env.pop(ADMISSION_ID_ENV, None)
        env.pop(ADMISSION_WAIT_ENV, None)
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
            with _deferred_signals(previous):
                child = _spawn_child(command, (), None)
        else:
            admission = _Admission(_prepare_state(), command)
            admission.enter()
            with _deferred_signals(previous):
                child = _spawn_child(command, inherit_fds(), admission)
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
