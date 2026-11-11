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
`HARNESS_VERIFY_LOCK_HELD=<holder-pid>` and `HARNESS_VERIFY_LOCK_TOKEN=<token>`,
a random token each admission publishes with its ownership. The marker is
honoured only when the published ownership names its pid and its token and
the work lock is genuinely held. The environment reaches every descendant —
across new sessions, nested runners and a dead holder — and no unrelated
process knows the token, so no process relation has to be proven (review rows
F6-2, F6-6). An absent, malformed, stale or unrelated marker uses ordinary
admission. The holder process itself need not live: a killed supervisor leaves
the lock held by the descriptor its protected child inherited, and that
child's own nested calls still nest. Only the owner removes the published
ownership, and only while it still names the owner.

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

**Run temporary area.** A supervised runner can instead ask for a *scope*
(`--tmp-scope`): its own private temporary area, created in a managed
container (`.harness-verify-tmp` beside the caller's absolute
`PYTEST_DEBUG_TEMPROOT`, or beside the platform temporary parent when unset)
and removed when the protected work ends — on success, on failure and on a
trapped signal alike. The child receives `PYTEST_DEBUG_TEMPROOT=<area>`, so
every pytest session of the run — numbered roots, xdist workers, the kit
probe — writes inside the area, while `TMPDIR` and unrelated pytest options
stay untouched; an inherited `--basetemp` (any accepted spelling in
`PYTEST_ADDOPTS`) refuses the scope before any gate. A scope belongs to one
supervised runner, not to one admission: an inherited admission still
receives a fresh sibling area, two runs never share one, and a nested runner
never removes its parent's. Publication and the start sweep serialize on a
short `registry.lock` flock inside the container, separate from admission.
The ownership record (`owner.json`, versioned, published before launch)
carries the area's directory identity, supervisor and child pids, the
protected process group and the retention request; the lease (`lease.lock`)
is a flock the supervisor holds for the whole scope and the protected child
inherits — so a killed supervisor alone never makes a live child's area an
orphan. The start sweep reclaims an orphan only when its lease can be taken
without waiting, its record matches the directory's identity and its
protected group is gone; a busy lease means live work and the area is
skipped, an unreadable or substituted candidate is reported and left
untouched rather than guessed. With `HARNESS_VERIFY_KEEP_TMP=1` an
*unsuccessful* run keeps its area and reports its absolute path on stderr
(interrupted runs included; a successful run never retains); the caller
inspects it and removes it, and no sweep deletes it. The query (`--tmp-held`)
answers for the calling shell alone: it passes only when the shell is the
recorded child of a live scope supervisor, so a deeper runner or a copied
environment always receives a fresh area of its own.

Command line:

    python -m scripts.verify_lock --held          # exit 0 when the environment names a valid admission
    python -m scripts.verify_lock --tmp-held      # exit 0 when the calling shell is a live scope's child
    python -m scripts.verify_lock -- COMMAND...   # supervise one protected command
    python -m scripts.verify_lock --tmp-scope -- COMMAND...
                                                  # supervise one protected command in its own
                                                  # temporary run area; a failed run is kept for
                                                  # inspection with HARNESS_VERIFY_KEEP_TMP=1:
                                                  # HARNESS_VERIFY_KEEP_TMP=1 PYTHON=.venv/bin/python3 make verify

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
import hmac
import json
import math
import os
import re
import secrets
import shlex
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from collections.abc import Iterator
from pathlib import Path

LOCK_ENV = "HARNESS_VERIFY_LOCK_HELD"
TOKEN_ENV = "HARNESS_VERIFY_LOCK_TOKEN"
FLOOR_ENV = "HARNESS_VERIFY_MEMORY_FLOOR"
# The run temporary area (bead coding-harness-bxxt.3): the container locator
# and the scope marker travel in the scope environment, the retention request
# is the caller's explicit opt-in, and the container is a private directory
# beside the caller's absolute PYTEST_DEBUG_TEMPROOT or the platform temporary
# parent — never inside the caller's TMPDIR, which stays untouched.
TMP_CONTAINER_ENV = "HARNESS_VERIFY_TMP_CONTAINER"
TMP_SCOPE_ENV = "HARNESS_VERIFY_TMP_SCOPE"
KEEP_TMP_ENV = "HARNESS_VERIFY_KEEP_TMP"
CONTAINER_NAME = ".harness-verify-tmp"
AREA_PREFIX = "run-"
TMP_REGISTRY_NAME = "registry.lock"
LEASE_NAME = "lease.lock"
SCOPE_RECORD_NAME = "owner.json"
SCOPE_RECORD_VERSION = 1
SCOPE_QUERY_SECONDS = 0.5
SCOPE_QUERY_POLL_SECONDS = 0.01
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
        # Non-blocking, so a FIFO planted in the record's place is refused below, never waited on (F6-7).
        fd = os.open(base / HOLDER_NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
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
    token = os.environ.get(TOKEN_ENV, "")
    holder = read_holder()
    if holder is None or not _names(holder, pid, token):
        return None
    lock = state_root() / LOCK_NAME
    try:
        fd = os.open(lock, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
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
            return pid if again is not None and _names(again, pid, token) else None
        fcntl.flock(fd, fcntl.LOCK_UN)
        return None
    finally:
        os.close(fd)


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
    inherited = nested_holder_pid()
    if inherited is not None:
        holder = read_holder()
        token = os.environ.get(TOKEN_ENV, "")
        if holder is not None and _names(holder, inherited, token):
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
    """One entry's queue wait, ownership and memory gate on an opened state."""

    def __init__(self, state: State, command: list[str]) -> None:
        self.state = state
        self.command = [str(word) for word in command]
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

    def _publish(self) -> None:
        """Publish pid, token, command, start time and the admission context while owning admission."""
        record = {
            "pid": os.getpid(),
            "token": self.token,
            "command": self.command,
            "start": self.started,
            "admission_id": self.admission_id,
            "admission_wait": self.wait_seconds,
        }
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
    command: list[str], pass_fds: tuple[int, ...], admission: _Admission | None, scope: _TempScope | None = None
) -> subprocess.Popen[bytes]:
    """The protected command in its own session, stdout and stderr reaching the operator.

    A scope hands its child the run area as `PYTEST_DEBUG_TEMPROOT` and the
    container as the locator for nested scopes; `TMPDIR` is deliberately not
    rewritten, so unrelated temporary writers keep their contract.
    """
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
    if scope is not None:
        env["PYTEST_DEBUG_TEMPROOT"] = str(scope.area)
        env[TMP_CONTAINER_ENV] = str(scope.container)
        env[TMP_SCOPE_ENV] = str(scope.area)
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


# ---------------------------------------------------------------------------
# The run temporary area (bead coding-harness-bxxt.3)
# ---------------------------------------------------------------------------


def _record_int(record: dict, name: str) -> int | None:
    """A positive integer field of an ownership record, or None when absent or unusable."""
    value = record.get(name)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return None
    return value


def _record_optional_int(record: dict, name: str) -> int | None:
    """A positive integer field that may legitimately be absent, or None otherwise.

    An unusable value reads as absent: the callers treat both as "cannot be
    established" and fail closed, never as a guess.
    """
    value = record.get(name)
    if value is None:
        return None
    return _record_int(record, name)


def _identity_of(path: Path) -> tuple[int, int]:
    """The directory identity (device, inode) an ownership record is checked against."""
    following = path.lstat()
    return (following.st_dev, following.st_ino)


def _flock_descriptor(fd: int) -> Iterator[None]:
    """Hold one exclusive flock on an open descriptor for the block, release after."""
    fcntl.flock(fd, fcntl.LOCK_EX)
    try:
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)


def _read_scope_record(area: Path) -> dict | None:
    """The scope ownership record, read without following symlinks; None when absent or unusable."""
    try:
        # Non-blocking, so a FIFO planted in the record's place is refused below, never waited on.
        fd = os.open(area / SCOPE_RECORD_NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
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
        record = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    return record if isinstance(record, dict) else None


def _lease_is_busy(area: Path) -> bool:
    """True while someone still holds the area's lease — the supervisor or its inherited child."""
    try:
        fd = os.open(area / LEASE_NAME, os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        return False
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return True
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    finally:
        os.close(fd)


def _scope_record_holds(area: Path, record: dict) -> bool:
    """The record is ours and its supervision is live: version, identity, child, supervisor, lease."""
    version = record.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version != SCOPE_RECORD_VERSION:
        return False
    dev, ino, supervisor = _record_int(record, "dev"), _record_int(record, "ino"), _record_int(record, "supervisor")
    if dev is None or ino is None or supervisor is None:
        return False
    try:
        if _identity_of(area) != (dev, ino):
            return False
    except OSError:
        return False
    if _record_optional_int(record, "child") != os.getppid():
        # The calling shell is not the recorded child: a deeper runner or a copied
        # environment must not inherit the answer (it receives a fresh area of its own).
        return False
    try:
        os.kill(supervisor, 0)
    except ProcessLookupError:
        return False
    except OSError:
        pass  # exists but is not signallable by us: still live
    return _lease_is_busy(area)


def tmp_scope_held() -> bool:
    """True when the calling shell is the recorded child of a live scope supervisor.

    Only the immediate child passes: the query checks its calling shell's
    identity (`getppid` against the published child pid), never the short-lived
    query process itself. A record not yet naming its child belongs to a launch
    in progress — the query waits a bounded moment for it before concluding the
    scope is not ours; an area already gone fails at once.
    """
    marker = os.environ.get(TMP_SCOPE_ENV, "").strip()
    if not marker or not Path(marker).is_absolute():
        return False
    area = Path(marker)
    try:
        area.lstat()
    except OSError:
        return False  # the area is gone; no scope of ours can live there
    deadline = _now() + SCOPE_QUERY_SECONDS
    while True:
        record = _read_scope_record(area)
        if record is not None:
            return _scope_record_holds(area, record)
        if _now() >= deadline:
            return False
        _sleep(SCOPE_QUERY_POLL_SECONDS)


def _refuse_foreign_basetemp() -> None:
    """Refuse inherited pytest options that would place pytest's basetemp outside the run area.

    `PYTEST_ADDOPTS` is parsed the way pytest parses it (`shlex.split`); any
    selection of `--basetemp` — `--basetemp PATH`, `--basetemp=PATH` or an
    accepted abbreviation of the option — refuses the scope before any gate,
    and malformed quoting refuses as well. Unrelated options pass untouched;
    an option *value* that merely looks like the option also refuses, because
    failing closed is the only direction that never escapes containment.
    """
    raw = os.environ.get("PYTEST_ADDOPTS")
    if not raw:
        return
    try:
        words = shlex.split(raw)
    except ValueError as error:
        raise VerifyLockRefused(
            f"PYTEST_ADDOPTS={raw!r} cannot be parsed as pytest options ({error}); refusing the scope"
        ) from None
    for word in words:
        if not word.startswith("--"):
            continue
        name = word[2:].split("=", 1)[0]
        if name and "basetemp".startswith(name):
            raise VerifyLockRefused(
                f"PYTEST_ADDOPTS selects pytest's basetemp ({word}); it would write outside the run area; "
                "refusing the scope"
            )


def _prepare_directory(path: Path) -> Path:
    """Create a directory tree, refusing anything that cannot be created."""
    try:
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
    except OSError as error:
        raise VerifyLockRefused(f"the directory {path} cannot be created ({error.strerror or error})") from error
    return path


def _validate_container(path: Path) -> Path:
    """The container must be a private directory owned by this user; anything else refuses."""
    try:
        following = path.lstat()
    except OSError as error:
        raise VerifyLockRefused(
            f"the managed temporary container {path} is unusable ({error.strerror or error})"
        ) from error
    if stat.S_ISLNK(following.st_mode) or not stat.S_ISDIR(following.st_mode):
        raise VerifyLockRefused(
            f"the managed temporary container {path} is not a directory; refusing substituted state"
        )
    if following.st_uid != os.getuid() or following.st_mode & 0o077:
        raise VerifyLockRefused(
            f"the managed temporary container {path} is not a private directory owned by this user; refusing"
        )
    return path


def _resolve_container() -> Path:
    """The managed container of this run: an inherited locator, or a fresh one beside the parent.

    The locator (`TMP_CONTAINER_ENV`) is carried with the scope environment so
    a nested run allocates a sibling under the *original* container instead of
    treating its inherited pytest root — an area, not a caller-selected
    parent — as a new parent. An unusable locator refuses: sweeping a
    different container would strand the orphans the first one holds.
    """
    given = os.environ.get(TMP_CONTAINER_ENV, "").strip()
    if given:
        container = Path(given)
        if not container.is_absolute():
            raise VerifyLockRefused(f"{TMP_CONTAINER_ENV}={given!r} is not an absolute path; refusing the scope")
        return _validate_container(container)
    raw = os.environ.get("PYTEST_DEBUG_TEMPROOT", "").strip()
    if raw and not Path(raw).is_absolute():
        raise VerifyLockRefused(
            f"PYTEST_DEBUG_TEMPROOT={raw!r} is not an absolute path; refusing to place the run area beside it"
        )
    parent = Path(raw) if raw else Path(tempfile.gettempdir())
    return _validate_container(_prepare_directory(parent / CONTAINER_NAME))


def _clear_directory(dir_fd: int) -> None:
    """Empty one open directory, descriptor-relative and no-follow: a symlink is unlinked, never followed."""
    for name in os.listdir(dir_fd):
        child = os.lstat(name, dir_fd=dir_fd)
        if stat.S_ISDIR(child.st_mode):
            nested = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_DIRECTORY, dir_fd=dir_fd)
            try:
                _clear_directory(nested)
            finally:
                os.close(nested)
            os.rmdir(name, dir_fd=dir_fd)  # noqa: PTH106 — pathlib has no dir_fd; no-follow removal needs it
        else:
            os.unlink(name, dir_fd=dir_fd)  # noqa: PTH108 — pathlib has no dir_fd; no-follow unlink needs it


def _remove_tree(path: Path) -> None:
    """Remove a directory tree without ever descending into a symlink.

    Every step is descriptor-relative and no-follow, so a symlink planted
    inside the tree is unlinked itself and nothing outside the tree — the
    caller's parent, a substituted target — is touched.
    """
    following = path.lstat()  # FileNotFoundError propagates: the caller decides what absence means
    if stat.S_ISLNK(following.st_mode) or not stat.S_ISDIR(following.st_mode):
        raise VerifyLockRefused(f"{path} is not a directory; refusing to remove substituted state")
    root_fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_DIRECTORY)
    try:
        _clear_directory(root_fd)
    finally:
        os.close(root_fd)
    path.rmdir()


def _sweep_container(container: Path) -> list[str]:
    """Reclaim recognizable, unretained orphan areas; report and keep everything unsafe.

    Called under the registry flock at a scope's start, before our own area
    exists. Only `run-*` entries are candidates, so the container's own
    registry, foreign files and legacy pytest roots are never swept. A
    candidate is reclaimed only when its lease can be taken without waiting
    (no live supervisor or inherited child holds it), its published record is
    valid and matches the directory's identity, and its protected process
    group is gone; a busy lease means live protected work and is skipped
    silently. Every other verdict — unreadable record, unknown version,
    substituted entry, live group, an explicitly retained area, a failed
    removal — is reported and left untouched rather than guessed.
    """
    reports: list[str] = []
    try:
        names = sorted(os.listdir(container))
    except OSError as error:
        raise VerifyLockRefused(f"the managed container {container} cannot be read ({error})") from error
    for name in names:
        if not name.startswith(AREA_PREFIX):
            continue
        area = container / name
        try:
            following = area.lstat()
        except OSError:
            continue  # vanished between the listing and the look: nothing left to reclaim
        if stat.S_ISLNK(following.st_mode) or not stat.S_ISDIR(following.st_mode):
            reports.append(f"{area} is not a managed directory; left untouched")
            continue
        verdict = _reclaim_or_report(area, following)
        if verdict is not None:
            reports.append(verdict)
    for line in reports:
        _log(f"sweep: {line}")
    return reports


def _reclaim_or_report(area: Path, following: os.stat_result) -> str | None:
    """One candidate's verdict: None when reclaimed, otherwise the reason it was left untouched."""
    record = _read_scope_record(area)
    if record is None:
        return f"{area} has no usable ownership record; left untouched"
    version = record.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version != SCOPE_RECORD_VERSION:
        return f"{area} carries an unknown record version; left untouched"
    dev, ino = _record_int(record, "dev"), _record_int(record, "ino")
    if dev is None or ino is None or (following.st_dev, following.st_ino) != (dev, ino):
        return f"{area} does not match its published directory identity; left untouched"
    try:
        lease_fd = os.open(area / LEASE_NAME, os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        return f"{area} has no usable lease; left untouched"
    try:
        try:
            fcntl.flock(lease_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return None  # a live supervisor or inherited child holds it: an active sibling, not a finding
        group = _record_optional_int(record, "group")
        if group is not None and _group_alive(group):
            return f"{area} names a live protected process group; left untouched"
        if record.get("retention") is True and record.get("outcome") != 0:
            # An unsuccessful or unknown run under an explicit request keeps its
            # evidence; a known-successful one never retains (retention is for
            # inspection, and only the caller removes a retained area).
            return f"{area} is retained by {KEEP_TMP_ENV}=1; left for inspection"
        try:
            _remove_tree(area)
        except VerifyLockError as error:
            return f"{area} cannot be removed safely ({error}); left in place"
        except OSError as error:
            return f"{area} cannot be removed ({error.strerror or error}); left in place"
        return None
    finally:
        os.close(lease_fd)


@dataclasses.dataclass
class _TempScope:
    """One run's temporary area: container, lease, published ownership.

    The scope belongs to one supervised runner, not to one admission: an
    inherited admission still receives a fresh area without another queue or
    memory wait, and two runs never share one.
    """

    container: Path
    area: Path
    identity: tuple[int, int]
    lease_fd: int
    registry_fd: int
    retention: bool
    started: str

    @classmethod
    def start(cls) -> _TempScope:
        """Refuse foreign basetemps, resolve the container, sweep, allocate and publish our area."""
        _refuse_foreign_basetemp()
        container = _resolve_container()
        registry_fd = _open_lock_file(container / TMP_REGISTRY_NAME)
        area: Path | None = None
        lease_fd: int | None = None
        try:
            with _flock_descriptor(registry_fd):
                _sweep_container(container)
                area, lease_fd = cls._allocate(container)
                scope = cls(
                    container=container,
                    area=area,
                    identity=_identity_of(area),
                    lease_fd=lease_fd,
                    registry_fd=registry_fd,
                    # Snapshotted before the launch, so a recovery after a hard
                    # kill can still honour the request it saw (the record is
                    # all a later sweep can read).
                    retention=os.environ.get(KEEP_TMP_ENV, "") == "1",
                    started=_stamp(),
                )
                scope._publish(None)
        except BaseException:
            if lease_fd is not None:
                os.close(lease_fd)
            if area is not None:
                with contextlib.suppress(OSError, VerifyLockError):
                    _remove_tree(area)
            os.close(registry_fd)
            raise
        return scope

    @staticmethod
    def _allocate(container: Path) -> tuple[Path, int]:
        """A unique user-owned area with a fresh lease, inside the managed container."""
        area = container / f"{AREA_PREFIX}{uuid.uuid4().hex}"
        try:
            area.mkdir(mode=0o700)
        except OSError as error:
            raise VerifyLockRefused(f"the run area {area} cannot be created ({error.strerror or error})") from error
        lease_fd = _open_lock_file(area / LEASE_NAME)
        try:
            fcntl.flock(lease_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            os.close(lease_fd)
            raise VerifyLockRefused(
                f"the lease of the run area {area} cannot be held ({error.strerror or error})"
            ) from error
        return area, lease_fd

    def _publish(self, child: int | None) -> None:
        """Publish the ownership record under the registry flock; a planted hard link is never written through."""
        record = {
            "version": SCOPE_RECORD_VERSION,
            "area": str(self.area),
            "dev": self.identity[0],
            "ino": self.identity[1],
            "supervisor": os.getpid(),
            # The child leads its own session (start_new_session), so its pid
            # is the protected group until it exits; both are None until the
            # launch has handed them to us.
            "child": child,
            "group": child,
            "retention": self.retention,
            "start": self.started,
            "outcome": None,
        }
        payload = json.dumps(record).encode("utf-8")
        fresh = self.area / f".{SCOPE_RECORD_NAME}.{os.getpid()}"
        with contextlib.suppress(FileNotFoundError):
            fresh.unlink()
        try:
            with _flock_descriptor(self.registry_fd):
                descriptor = os.open(fresh, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                with os.fdopen(descriptor, "wb") as handle:
                    handle.write(payload)
                fresh.replace(self.area / SCOPE_RECORD_NAME)
        except OSError as error:
            with contextlib.suppress(OSError):
                fresh.unlink()
            raise VerifyLockRefused(
                f"the ownership record of the run area {self.area} cannot be published ({error.strerror or error})"
            ) from error

    def publish_child(self, child_pid: int) -> None:
        """Name the protected child and its process group once the launch has handed them to us."""
        self._publish(child_pid)

    def _record_outcome(self, outcome: int) -> None:
        """Record the final status so a later sweep can honour an unknown run's retention request.

        Best effort: an unreadable or unwritable record is advisory here — the
        removal decision below uses the supervisor's own knowledge, and a
        sweep reading an unknown outcome conservatively honours the request.
        """
        record = _read_scope_record(self.area)
        if record is None or record.get("version") != SCOPE_RECORD_VERSION:
            return
        record["outcome"] = outcome
        payload = json.dumps(record).encode("utf-8")
        fresh = self.area / f".{SCOPE_RECORD_NAME}.{os.getpid()}.out"
        try:
            with contextlib.suppress(FileNotFoundError):
                fresh.unlink()
            descriptor = os.open(fresh, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
            fresh.replace(self.area / SCOPE_RECORD_NAME)
        except OSError:
            with contextlib.suppress(OSError):
                fresh.unlink()

    def finish(self, outcome: int) -> int | None:
        """End the scope after the protected work: retain on an explicit request, otherwise remove.

        Returns a replacement status only when an otherwise successful run
        could not clean up (exit 2); a pre-existing failure or signal status is
        preserved and the removal failure reported beside it. Runs in every
        ending, after the protected group is gone and before admission is
        released.
        """
        self._record_outcome(outcome)
        if self.retention and outcome != 0:
            _log(
                f"{KEEP_TMP_ENV}=1 and an unsuccessful run: the run area {self.area} is retained for "
                "inspection; remove it once it is no longer needed"
            )
            os.close(self.lease_fd)
            os.close(self.registry_fd)
            return None
        try:
            _remove_tree(self.area)
        except (OSError, VerifyLockError) as error:
            _log(f"the run area {self.area} cannot be removed ({error}); the area is left in place")
            os.close(self.lease_fd)
            os.close(self.registry_fd)
            return 2 if outcome == 0 else None
        os.close(self.lease_fd)
        os.close(self.registry_fd)
        return None


def supervise(command: list[str], tmp_scope: bool = False) -> int:
    """Queue, check memory and run one protected command; return its exit code.

    With `tmp_scope` the command runs inside its own temporary run area
    *instead of* an admission: the scope supervisor of `scripts.verify_all.sh`
    holds no queue and no memory wait, and the runner it supervises enters the
    ordinary admission one layer down. The area is finalized after the child's
    process group is gone and before anything is released; a cleanup failure
    after an otherwise successful run turns the status into 2, and a pre-
    existing failure or signal status is preserved.
    """
    if not command:
        print("[verify-lock] no command given; nothing is protected", file=sys.stderr, flush=True)
        return 2
    previous = _install_signal_handlers()
    child: subprocess.Popen[bytes] | None = None
    admission: _Admission | None = None
    scope: _TempScope | None = None
    cleanup_status: int | None = None
    code = 2
    try:
        if tmp_scope:
            scope = _TempScope.start()
            with _deferred_signals(previous):
                try:
                    child = _spawn_child(command, (scope.lease_fd,), None, scope)
                    scope.publish_child(child.pid)
                except OSError as error:
                    raise VerifyLockRefused(
                        f"the protected command cannot be started ({error.strerror or error})"
                    ) from error
        else:
            inherited = nested_holder_pid()
            if inherited is not None:
                _log(f"inheriting admission from pid {inherited}; no queue and no memory wait")
                with _deferred_signals(previous):
                    child = _spawn_child(command, (), None)
            else:
                admission = _Admission(_prepare_state(), command)
                admission.enter()
                with _deferred_signals(previous):
                    child = _spawn_child(command, (admission.state.lock_fd,), admission)
        code = _watch_child(child)
    except VerifyLockError as refused:
        kind = "scope" if tmp_scope else "admission"
        print(f"[verify-lock] {kind} refused: {refused}", file=sys.stderr, flush=True)
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
            if scope is not None:
                cleanup_status = scope.finish(code)
            if admission is not None:
                admission.release()
        finally:
            _restore_signal_handlers(previous)
    return cleanup_status if cleanup_status is not None else code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="One machine-wide admission for protected verification work.")
    parser.add_argument(
        "--held",
        action="store_true",
        help="exit 0 when the environment names a valid inherited admission, 1 otherwise",
    )
    parser.add_argument(
        "--tmp-held",
        action="store_true",
        help="exit 0 when the calling shell is a live scope's supervised child, 1 otherwise",
    )
    parser.add_argument(
        "--tmp-scope",
        action="store_true",
        help="supervise the command inside its own private temporary run area",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, metavar="COMMAND", help="the protected command, after --")
    args = parser.parse_args(argv)
    if args.held:
        return 0 if nested_holder_pid() is not None else 1
    if args.tmp_held:
        return 0 if tmp_scope_held() else 1
    command = args.command[1:] if args.command[:1] == ["--"] else list(args.command)
    return supervise(command, tmp_scope=args.tmp_scope)


if __name__ == "__main__":
    raise SystemExit(main())
