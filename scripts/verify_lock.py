#!/usr/bin/env python3
"""verify_lock.py — the machine-wide admission for protected verification work.

Concurrent full checks exhaust the machine: a three-lane trial recorded load
above 100 and checks past 30 minutes, against 11-12 minutes run one after the
other (bead coding-harness-p6mu). This module queues every independent
protected entry of one user on one machine — across repositories and
worktrees — and checks the system's free memory before work starts, so a
runner's checking time limit is spent on checking, not on waiting for a turn.

**Slots.** By default two independent admissions may hold protected work at
once (bead coding-harness-u1ha); `HARNESS_VERIFY_SLOTS` narrows an entry to
exactly `1` or `2`, and any other value refuses the entry before protected
work. A setting-`2` entry reserves one slot file exclusively and holds
`verify.lock` shared; a setting-`1` entry and every older single-slot
checkout hold `verify.lock` exclusively, so the old machine-wide bound stays
intact during rollout and a mixed setting never shares capacity. Effective
capacity is the minimum of the settings of all occupied slots' retained
holder records and the head live waiter; only the first live waiter may
reserve, in registration order.

**Shared state.** `${XDG_STATE_HOME:-~/.local/state}/coding-harness/` is the
one state root for cooperating entries; neither the repository nor a worktree
identifies it. `verify.lock` carries the compatibility lock (`fcntl.flock`,
kernel-backed: shared for setting-`2` holders, exclusive for setting-`1`
entries and older checkouts), `verify.slot-1.lock` and `verify.slot-2.lock`
one work lock per slot, `verify.holder.json` the ownership published by an
older single-slot checkout, `verify.holder.1.json` / `verify.holder.2.json`
one record per slot holder, `verify.holder.exclusive.json` the record of a
setting-`1` updated holder, and `verify.queue/` one record per waiter, held
open under its owner's liveness flock so a dead waiter's record is
recognisable and pruned. A short-held `verify.registry.lock` serialises
registration, pruning, reservation and turn-taking; registration order is
the admission order — `flock` alone supplies no FIFO, so only the first live
record may try to reserve.

**Nested work.** A protected entry descended from a live admission carries
`HARNESS_VERIFY_LOCK_HELD=<holder-pid>` and `HARNESS_VERIFY_LOCK_TOKEN=<token>`,
a random token each admission publishes with its ownership. The marker is
honoured only when a published ownership record names its pid and its token
and that record's work lock is genuinely held — the compatibility lock
exclusively for the legacy and setting-`1` records, the slot lock for a slot
record. The environment reaches every descendant — across new sessions,
nested runners and a dead holder — and no unrelated process knows the token,
so no process relation has to be proven (review rows F6-2, F6-6). An absent,
malformed, stale or unrelated marker uses ordinary admission. The holder
process itself need not live: a killed supervisor leaves the locks held by
the descriptors its protected child inherited, and that child's own nested
calls still nest. Only the owner removes the published ownership, and only
while it still names the owner.

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
entry with a diagnostic before any protected work, as does a
`HARNESS_VERIFY_SLOTS` value other than the exact strings `1` or `2`, or a
second independent admission requested by a process that already holds or is
acquiring one. Nothing here falls through unlocked, and no substituted file
is written through. `VerifyLockRefused` exits 2, `MemoryFloorRefused` exits 3.

Command line:

    python -m scripts.verify_lock --held          # exit 0 when the environment names a valid admission
    python -m scripts.verify_lock -- COMMAND...   # supervise one protected command

The supervisor queues, checks memory, publishes ownership for its child —
which inherits the compatibility and slot descriptors, so ownership outlives
a killed supervisor for exactly as long as the protected child and its own
children run — and releases only after the child's process group is gone,
including failure, cancellation and signals; signal cleanup kills the child
before the locks are released, and a grandchild left in the group after the
command exits is ended before release. `scripts.verify_run` holds this
admission in-process around the protected gates of the shared two-phase
scheduler, and `scripts.stage2` reaches the same admission through that
scheduler for its timed local checks; the queue and memory waits consume
neither `VERIFY_SECONDS` nor a pytest proof's execution timeout — the
configured limits still apply to actual execution.
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
from collections.abc import Iterator
from pathlib import Path

LOCK_ENV = "HARNESS_VERIFY_LOCK_HELD"
TOKEN_ENV = "HARNESS_VERIFY_LOCK_TOKEN"
FLOOR_ENV = "HARNESS_VERIFY_MEMORY_FLOOR"
SLOTS_ENV = "HARNESS_VERIFY_SLOTS"
# The non-secret admission context (bead coding-harness-1um6): the id names the
# admission to its descendants, the wait is the measured queue-plus-memory
# seconds. The ownership token never travels in either — it stays in TOKEN_ENV
# alone, the one secret of the relation.
ADMISSION_ID_ENV = "HARNESS_VERIFY_ADMISSION_ID"
ADMISSION_WAIT_ENV = "HARNESS_VERIFY_ADMISSION_WAIT"
DEFAULT_MEMORY_FLOOR = 25.0
DEFAULT_SLOTS = 2
MEMORY_POLL_SECONDS = 30.0
QUEUE_LOG_SECONDS = 300.0
MEMORY_DEADLINE_SECONDS = 3600.0
PROBE_SECONDS = 5.0
QUEUE_POLL_SECONDS = 0.25
CHILD_WATCH_SECONDS = 0.25
SIGNAL_GRACE_SECONDS = 5.0
LOCK_NAME = "verify.lock"
SLOT_LOCK_NAMES = ("verify.slot-1.lock", "verify.slot-2.lock")
HOLDER_NAME = "verify.holder.json"
EXCLUSIVE_HOLDER_NAME = "verify.holder.exclusive.json"
SLOT_HOLDER_NAMES = ("verify.holder.1.json", "verify.holder.2.json")
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
    """The opened shared state of one machine: stable reservation descriptors.

    Independent liveness probes reopen lock paths: flock on an owned descriptor
    would alter its lock. These probes refuse non-regular files and symlinks.

    `lock_fd` is the compatibility lock a setting-`2` holder keeps shared and
    a setting-`1` entry or an older checkout keeps exclusive; `slot_fds` are
    the two stable slot locks a setting-`2` holder reserves one of.
    """

    root: Path
    lock_fd: int
    slot_fds: tuple[int, ...]
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
        root=root,
        lock_fd=_open_lock_file(root / LOCK_NAME),
        slot_fds=tuple(_open_lock_file(root / name) for name in SLOT_LOCK_NAMES),
        registry_fd=_open_lock_file(root / REGISTRY_NAME),
    )


def verify_slots_setting() -> int:
    """The configured slot request of one independent entry: 2 by default, else exactly 1 or 2.

    Only the exact strings `1` and `2` are accepted; an empty, padded,
    zero-padded, signed, fractional or other value refuses the entry before
    any protected work, naming the setting. A nested entry never reaches this
    parser: it reuses its ancestor and inherits no setting of its own.
    """
    raw = os.environ.get(SLOTS_ENV)
    if raw is None:
        return DEFAULT_SLOTS
    if raw in ("1", "2"):
        return int(raw)
    raise VerifyLockRefused(f"{SLOTS_ENV}={raw!r} is not one of the exact strings '1' or '2'; refusing admission")


def _record_setting(record: dict | None) -> int:
    """A retained holder record's configured capacity; an unreadable record counts as 1."""
    if record is None:
        return 1
    setting = record.get("slots")
    return setting if setting in (1, 2) else 1


def read_holder(root: Path | None = None) -> dict | None:
    """The legacy published ownership, read without following symlinks; None when absent or unusable.

    Older single-slot checkouts publish only here; a record survives only
    while its compatibility lock is genuinely held, and the shared-state
    prune removes it once that lock is free.
    """
    return _read_record((state_root() if root is None else root) / HOLDER_NAME)


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


def _lock_held_exclusively(path: Path) -> bool | None:
    """Whether the compatibility lock at `path` is held exclusively, or None when unusable.

    A shared probe succeeds when nobody holds the exclusive lock — free, or
    shared by the setting-`2` holders — and fails when a setting-`1` entry or
    an older checkout holds it. This is what separates a live exclusive
    holder from shared holders and from a stale record.
    """
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None
        try:
            fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except OSError:
            return True
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    finally:
        os.close(fd)


def _lock_held(path: Path) -> bool | None:
    """Whether any lock at `path` is held at all, or None when unusable.

    An exclusive probe fails when the slot lock is genuinely held — by a
    live holder or by the inherited descriptor of a survivor — and succeeds
    on a free slot, so a record whose lock is free is stale.
    """
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return True
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    finally:
        os.close(fd)


def _describe_holder(holder: dict | None) -> str:
    """One line naming a holder's pid, command and start time — or saying none is published."""
    if holder is None:
        return "no active holder is published; the lock may be held by a killed entry's inherited child"
    command = holder.get("command")
    words = " ".join(str(word) for word in command) if isinstance(command, list) else "unknown command"
    return f"holder pid {holder.get('pid')} ({words}, started {holder.get('start', 'unknown')})"


def _describe_occupancy(root: Path) -> str:
    """Every occupied slot and exclusive holder named without any ownership token.

    A slot whose lock is held but whose record is unreadable is named as
    occupied with an unavailable holder, never dropped; the same holds for an
    exclusive compatibility holder without a record.
    """
    lines: list[str] = []
    for index, name in enumerate(SLOT_LOCK_NAMES, start=1):
        if _lock_held(root / name) is not True:
            continue
        record = _read_record(root / SLOT_HOLDER_NAMES[index - 1])
        if record is None:
            lines.append(f"slot {index}: occupied; its holder is unavailable")
        else:
            lines.append(f"slot {index}: {_describe_holder(record)}")
    exclusive = _lock_held_exclusively(root / LOCK_NAME)
    if exclusive is True:
        exclusive_record = _read_record(root / EXCLUSIVE_HOLDER_NAME)
        legacy = read_holder(root)
        if exclusive_record is not None:
            lines.append(f"exclusive holder: {_describe_holder(exclusive_record)}")
        elif legacy is not None:
            lines.append(f"exclusive holder (older checkout): {_describe_holder(legacy)}")
        else:
            lines.append("exclusive holder: occupied; its holder is unavailable")
    if not lines:
        return "no active holder is published; the lock may be held by a killed entry's inherited child"
    return "; ".join(lines)


def _nested_record() -> tuple[int, dict] | None:
    """The valid inherited admission's holder pid and its matched record, or None.

    The marker is valid only when a published ownership record names its
    process and token and that record's work lock is genuinely held — the
    compatibility lock exclusively for a legacy or setting-`1` record, the
    slot lock for a slot record. A stale marker (its admission released) or
    an unrelated one falls back to ordinary admission. The holder process
    itself is not required to live: a killed supervisor leaves the locks held
    by the descriptors its protected child inherited, and that child's own
    nested calls must still nest.
    """
    raw = os.environ.get(LOCK_ENV, "").strip()
    if not raw.isdigit() or int(raw) <= 0:
        return None
    pid = int(raw)
    token = os.environ.get(TOKEN_ENV, "")
    root = state_root()
    compatibility = (
        lambda: read_holder(root),
        lambda: _read_record(root / EXCLUSIVE_HOLDER_NAME),
    )
    for reader in compatibility:
        record = reader()
        if record is None or not _names(record, pid, token):
            continue
        if reader is compatibility[1] and read_holder(root) is not None:
            continue
        if _lock_held_exclusively(root / LOCK_NAME) is not True:
            # Free, or only shared by setting-`2` holders: no exclusive
            # admission owns the compatibility lock, so this record is stale.
            continue
        # Re-read after probing to reject a replaced ownership record.
        again = reader()
        if again is not None and _names(again, pid, token):
            return pid, record
        return None
    for index, name in enumerate(SLOT_LOCK_NAMES, start=1):
        record = _read_record(root / SLOT_HOLDER_NAMES[index - 1])
        if record is None or not _names(record, pid, token):
            continue
        if _lock_held(root / name) is not True:
            continue
        again = _read_record(root / SLOT_HOLDER_NAMES[index - 1])
        if again is not None and _names(again, pid, token):
            return pid, record
        return None
    return None


def nested_holder_pid() -> int | None:
    """The holder pid of a valid inherited admission, or None."""
    found = _nested_record()
    return None if found is None else found[0]


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
    """The short-held registry lock that serialises registration, pruning, reservation and turn-taking."""
    fcntl.flock(state.registry_fd, fcntl.LOCK_EX)
    try:
        yield
    finally:
        fcntl.flock(state.registry_fd, fcntl.LOCK_UN)


def _compat_exclusive_held(state: State) -> bool:
    """Whether the compatibility lock is held exclusively, probed on our own stable descriptor.

    The probe takes a shared lock non-blocking: it succeeds when the lock is
    free or shared by the setting-`2` holders and fails while a setting-`1`
    entry or an older checkout holds it exclusively. Call it only while this
    process holds nothing on the descriptor itself.
    """
    try:
        fcntl.flock(state.lock_fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
    except OSError:
        return True
    fcntl.flock(state.lock_fd, fcntl.LOCK_UN)
    return False


_ACTIVE_LOCK = threading.Lock()
_ACTIVE: _Admission | None = None
_ACQUIRING = False


@contextlib.contextmanager
def _independent_admission_guard() -> Iterator[None]:
    """Refuse a second independent admission in one process, held or still acquiring.

    One process owns at most one independent admission, including while it is
    still acquiring it: a concurrent entry would overwrite the process's
    published ownership and its admission state, so the second request is
    refused promptly with a diagnostic. A nested entry never reaches this
    guard — it reuses its ancestor's admission.
    """
    global _ACQUIRING
    with _ACTIVE_LOCK:
        if _ACTIVE is not None or _ACQUIRING:
            raise VerifyLockRefused(
                "this process already holds or is acquiring an independent admission; a second one is refused"
            )
        _ACQUIRING = True
    try:
        yield
    finally:
        with _ACTIVE_LOCK:
            _ACQUIRING = False


def _active_pid() -> int | None:
    """The pid this process publishes while it owns an admission, for the children's marker."""
    with _ACTIVE_LOCK:
        return os.getpid() if _ACTIVE is not None else None


def _active_token() -> str | None:
    """The token this process publishes while it owns an admission, for the children's marker."""
    with _ACTIVE_LOCK:
        return _ACTIVE.token if _ACTIVE is not None else None


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
    found = _nested_record()
    if found is not None:
        holder = found[1]
        return AdmissionContext(
            admission_id=holder.get("admission_id") if isinstance(holder.get("admission_id"), str) else None,
            wait_seconds=_finite_wait(holder.get("admission_wait")),
            reused=True,
        )
    return AdmissionContext(None, None, None)


def _parse_wait(raw: str | None) -> float | None:
    """An inherited wait from the environment as a float, else None."""
    try:
        value = float(raw or "")
    except ValueError:
        return None
    return value if math.isfinite(value) and value >= 0 else None


class _Admission:
    """One entry's queue wait, ownership and memory gate on an opened state."""

    def __init__(self, state: State, command: list[str], setting: int) -> None:
        self.state = state
        self.command = [str(word) for word in command]
        # The setting is parsed by the caller before any shared state is
        # opened, so an invalid value refuses without leaking descriptors.
        self.setting = setting
        self.entered = 0.0
        self.record_name: str | None = None
        self.record_fd: int | None = None
        self.token = secrets.token_hex(16)
        # The non-secret identity of this admission and its measured
        # queue-plus-memory wait (bead coding-harness-1um6); the wait is only
        # known once the memory gate has passed, so the first publish carries
        # None and the second the measurement.
        self.admission_id = uuid.uuid4().hex
        self.wait_seconds: float | None = None
        self.started = _stamp()
        self.reserved_slot: int | None = None
        self._published_paths: list[Path] = []
        self._released = False

    def pass_fds(self) -> tuple[int, ...]:
        """The descriptors a protected child must inherit so a survivor keeps its ownership.

        Both the compatibility lock and the reserved slot travel: a setting-`2`
        holder's survivor keeps its slot and the shared compatibility mark, a
        setting-`1` holder's survivor keeps the exclusive compatibility lock.
        """
        if self.reserved_slot is None:
            return (self.state.lock_fd,)
        return (self.state.lock_fd, self.state.slot_fds[self.reserved_slot - 1])

    def enter(self) -> None:
        """Queue for a slot, publish ownership, then hold the memory gate."""
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
        # Close, never unlock: the lock belongs to the open description, and a protected descendant
        # that inherited it and outlived the group kill keeps it until it exits (review row L1-11).
        # Only afterwards can this process tell whether the capacity is
        # genuinely free: the record is removed only when no inherited
        # descriptor still holds it, and only while it still names this
        # process (review row F6-1).
        owned = list(self._published_paths)
        self._published_paths = []
        with _registry_lock(self.state):
            os.close(self.state.lock_fd)
            for fd in self.state.slot_fds:
                os.close(fd)
            for path in owned:
                self._unlink_record_if_free(path)
            if self.record_name is not None:
                with contextlib.suppress(OSError):
                    (self.state.root / QUEUE_DIR / self.record_name).unlink()
                if self.record_fd is not None:
                    os.close(self.record_fd)
                self.record_name = None
                self.record_fd = None
        os.close(self.state.registry_fd)

    def _unlink_record_if_free(self, path: Path) -> None:
        """Remove our record once no inherited descriptor holds its lock any more.

        A record naming this process may survive its release only while a
        survivor still holds the lock, keeping the slot and its configured
        capacity in force (criterion 7); when a fresh descriptor can take the
        lock exclusively, the last descriptor closed and the record is stale.
        The lock file itself stays — it is stable shared state, recreated
        never.
        """
        if path.name in SLOT_HOLDER_NAMES:
            lock = self.state.root / SLOT_LOCK_NAMES[SLOT_HOLDER_NAMES.index(path.name)]
        else:
            lock = self.state.root / LOCK_NAME
        try:
            fd = os.open(lock, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        except OSError:
            return
        try:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return  # a survivor holds it: the record stays in force
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
        record = _read_record(path)
        if record is not None and record.get("pid") == os.getpid() and _names(record, os.getpid(), self.token):
            with contextlib.suppress(OSError):
                path.unlink()

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

    def _prune_stale_holders_locked(self) -> None:
        """Remove published ownership records whose associated lock is free.

        A record is authoritative only while its lock is genuinely held; once
        the last descriptor closed — its owner's release or the exit of the
        last inherited holder — the stale record would otherwise keep the
        slot reserved or the capacity at one forever. A live holder's record
        is never touched: its lock probe fails, so the record stays in force
        until its own release removes it.
        """
        for name in (*SLOT_HOLDER_NAMES, EXCLUSIVE_HOLDER_NAME, HOLDER_NAME):
            path = self.state.root / name
            record = _read_record(path)
            if record is None:
                continue
            if name in SLOT_HOLDER_NAMES:
                lock = self.state.root / SLOT_LOCK_NAMES[SLOT_HOLDER_NAMES.index(name)]
                free = _lock_held(lock) is False
            else:
                free = _lock_held_exclusively(self.state.root / LOCK_NAME) is False
            if free:
                again = _read_record(path)
                if again is not None and _names(again, record.get("pid"), record.get("token")):
                    with contextlib.suppress(OSError):
                        path.unlink()

    def _effective_capacity_locked(self) -> int:
        """The capacity free under the occupied holders' settings, while holding the registry lock.

        The minimum of the settings of all occupied slots' retained records —
        an occupied slot without a readable record counts as 1 — and 1 while
        an exclusive holder (a setting-`1` entry or an older checkout) holds
        the compatibility lock. The head waiter's own setting applies through
        its reservation rule, not here.
        """
        capacity = DEFAULT_SLOTS
        for index, name in enumerate(SLOT_HOLDER_NAMES, start=1):
            fd = self.state.slot_fds[index - 1]
            try:
                fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except OSError:
                capacity = min(capacity, _record_setting(_read_record(self.state.root / name)))
                continue
            fcntl.flock(fd, fcntl.LOCK_UN)
        if _compat_exclusive_held(self.state):
            capacity = min(capacity, 1)
        return capacity

    def _any_slot_occupied_locked(self) -> bool:
        """True while any slot lock is held by another admission, under the registry lock."""
        for fd in self.state.slot_fds:
            try:
                fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except OSError:
                return True
            fcntl.flock(fd, fcntl.LOCK_UN)
        return False

    def _live_records_locked(self) -> list[str]:
        """The queue records in registration order, while holding the registry lock."""
        queue = self.state.root / QUEUE_DIR
        try:
            names = sorted(os.listdir(queue))
        except OSError as error:
            raise VerifyLockRefused(f"the queue directory {queue} cannot be read ({error})") from error
        return [name for name in names if RECORD_NAME.fullmatch(name) is not None]

    def _try_reserve_locked(self) -> tuple[str, int | None] | None:
        """Reserve capacity without waiting, as the first live waiter, under the registry lock.

        A setting-`1` entry takes the compatibility lock exclusively — every
        holder must have drained first. A setting-`2` entry reserves one free
        slot when the effective capacity is still two, marking the
        compatibility lock shared so an older checkout's exclusive admission
        can never overlap the reservation. None means keep waiting.
        """
        capacity = self._effective_capacity_locked()
        if self.setting == 1:
            # Every slot must be free as well: the shared mark on the compatibility
            # lock is the holders' promise, the slot lock is the occupancy itself
            # (criterion 2: a setting-`1` entry never shares capacity).
            if self._any_slot_occupied_locked():
                return None
            try:
                fcntl.flock(self.state.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return None
            self._leave_queue_locked()
            return ("exclusive", None)
        if capacity != DEFAULT_SLOTS:
            return None
        for index in range(1, len(SLOT_LOCK_NAMES) + 1):
            fd = self.state.slot_fds[index - 1]
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                continue
            try:
                fcntl.flock(self.state.lock_fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except OSError:
                # An exclusive holder appeared inside the race window: give the
                # fresh slot reservation back and wait for a clean turn.
                fcntl.flock(fd, fcntl.LOCK_UN)
                return None
            self._leave_queue_locked()
            self.reserved_slot = index
            return ("slot", index)
        return None

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

    def _record_path(self) -> Path:
        """The ownership record this reservation publishes: one per slot, or the exclusive record."""
        if self.reserved_slot is None:
            return self.state.root / EXCLUSIVE_HOLDER_NAME
        return self.state.root / SLOT_HOLDER_NAMES[self.reserved_slot - 1]

    def _publish(self) -> None:
        """Publish pid, token, command, start time, the admission context and the setting.

        One atomic record per slot (or the exclusive record of a setting-`1`
        entry) so waiters can name every holder and compute the effective
        capacity; the legacy record stays the older checkouts' alone.
        """
        record = {
            "pid": os.getpid(),
            "token": self.token,
            "command": self.command,
            "start": self.started,
            "admission_id": self.admission_id,
            "admission_wait": self.wait_seconds,
            "slots": self.setting,
        }
        payload = json.dumps(record).encode("utf-8")
        path = self._record_path()
        # A fresh file renamed over the record replaces the directory entry itself, so a hard link
        # planted in its place is unlinked, never written through (review row F6-3).
        fresh = self.state.root / f".{path.name}.{os.getpid()}"
        try:
            with contextlib.suppress(FileNotFoundError):
                fresh.unlink()
            descriptor = os.open(fresh, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
            fresh.replace(path)
            if path not in self._published_paths:
                self._published_paths.append(path)
        except OSError as error:
            with contextlib.suppress(OSError):
                fresh.unlink()
            raise VerifyLockRefused(
                f"the holder record {path} cannot be published ({error.strerror or error})"
            ) from error

    def _queue_wait(self) -> None:
        """Wait for our registration turn, logging the wait and the holders as it goes."""
        self._register()
        announced = False
        last_log: float | None = None
        while True:
            reserved: tuple[str, int | None] | None = None
            with _registry_lock(self.state):
                self._prune_locked()
                self._prune_stale_holders_locked()
                records = self._live_records_locked()
                if self.record_name not in records:
                    raise VerifyLockRefused("our own queue record disappeared; the shared queue state is unusable")
                if records[0] == self.record_name:
                    reserved = self._try_reserve_locked()
            if reserved is None:
                described = _describe_occupancy(self.state.root)
                now = _now()
                if not announced:
                    _log(f"waiting for admission: {described}")
                    announced = True
                    last_log = now
                elif last_log is not None and now - last_log >= QUEUE_LOG_SECONDS:
                    _log(f"still waiting for admission ({now - self.entered:.0f}s): {described}")
                    last_log = now
                _sleep(QUEUE_POLL_SECONDS)
                continue
            waited = _now() - self.entered
            _log(f"admitted after {waited:.0f}s" if waited >= 1.0 else "admitted")
            return

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
def hold_admission(command: list[str]) -> Iterator[tuple[int, ...] | None]:
    """One machine admission around protected work: queue, memory gate, published ownership.

    Yields the descriptors local children must inherit, or None when this
    entry is nested in an ancestor's admission. A process that already holds
    or is acquiring an independent admission is refused before any queueing.
    Refusals raise VerifyLockRefused or MemoryFloorRefused before the body
    runs; release happens in every ending, after any child cleanup the caller
    does.
    """
    inherited = nested_holder_pid()
    if inherited is not None:
        _log(f"inheriting admission from pid {inherited}; no queue and no memory wait")
        yield None
        return
    with _independent_admission_guard():
        setting = verify_slots_setting()
        admission = _Admission(_prepare_state(), command, setting)
        try:
            admission.enter()
        except BaseException:
            admission.release()
            raise
        try:
            yield admission.pass_fds()
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
    # The slot setting travels to local children when present, so a nested
    # runner's own protected work — never a nested entry, which parses
    # nothing — sees the same configuration its parent had (criterion 2).
    # The foreign-model environment allowlist stays closed to HARNESS_*.
    if SLOTS_ENV in os.environ:
        env[SLOTS_ENV] = os.environ[SLOTS_ENV]
    nested = nested_holder_pid()
    marker, token = (nested, os.environ.get(TOKEN_ENV)) if nested is not None else (_active_pid(), _active_token())
    if marker is not None and token:
        env[LOCK_ENV] = str(marker)
        env[TOKEN_ENV] = token
    else:
        env.pop(LOCK_ENV, None)
        env.pop(TOKEN_ENV, None)
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


def signal_group(leader: int, signum: int = signal.SIGKILL) -> None:
    """Signal the process group led by `leader`; before the leader's own `setsid`, the leader itself.

    A timed launch registers its child while that child can still sit between fork and its own
    `setsid`: no process group of the child's id exists yet, so the `killpg` a cancellation sends
    misses with `ProcessLookupError`, and suppressed it left freshly created programs running
    through the stop (bead coding-harness-oag7, CI run 44591912821). The fallback signals the
    leader by pid, which owns no descendants in that window; a group already gone — its leader
    waited and reaped — misses the same way and stays silent, as the callers did before.
    """
    try:
        os.killpg(leader, signum)
    except ProcessLookupError:
        with contextlib.suppress(ProcessLookupError):
            os.kill(leader, signum)
    except OSError:
        pass


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
            with _independent_admission_guard():
                setting = verify_slots_setting()
                admission = _Admission(_prepare_state(), command, setting)
                admission.enter()
                with _deferred_signals(previous):
                    child = _spawn_child(command, admission.pass_fds(), admission)
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
