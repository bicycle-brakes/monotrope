#!/usr/bin/env python3
"""verify_run.py — the two-phase local verification of the ONE gate list.

The one machine admission exists so concurrent full checks never exhaust the
machine (bead coding-harness-p6mu). Taking it before any gate is selected or
executed makes the cheap gates wait for the slot behind the expensive ones —
a lint failure in seconds waited 710 seconds for its turn (research for bead
coding-harness-bxxt.6). This module is the one scheduler both callers share:

  - `scripts/verify_all.sh` execs this file after its interpreter bootstrap;
  - `scripts.stage2` calls `run_verification` in-process for its full check,
    its full-mode attempt verification and its draft document check.

The flow, over the gates `ci_gates.selection_at` selects:

  1. Every *unprotected* gate (declared `seconds`, without the explicit
     `needs_admission` exception) executes first, and every one of them
     executes even after another unprotected gate failed blocking-red — all
     cheap diagnostics together, before any waiting.
  2. A tree snapshot brackets the cheap pass. Only a stable snapshot is a
     baseline: an unstable or unreadable one refuses the run with a request
     to rerun, and never lets unmeasured results stand for the tree.
  3. With a green cheap pass, *protected* work (declared `minutes`, or
     `seconds` explicitly marked `needs_admission: true`) enters ONE
     admission (`verify_lock.hold_admission`). An empty protected set never
     requests admission at all — a docs-only run does not queue.
  4. If the tree changed while the admission was being waited for, the gate
     list is reloaded, the selection is recomputed from it, and the complete
     unprotected set reruns inside the held admission. Stale cheap results
     are never reused for a tree that moved.
  5. Locally the first blocking failure stops the protected phase and the
     run names every selected gate it did not execute. `--ci` stays
     exhaustive: it runs every selected gate of both phases, still under one
     admission for the protected set.

Output stays byte-compatible with the runner this module replaces: the run
report as the first JSON on stdout, the `── [gate] $ command` frames the
repair-evidence parser reads, and the not-run summary outside them. The
durations (`scripts.verify_duration`) carry one run identity across both
phases; the admission wait is recorded beside the execution seconds, never
inside them.

The tree comparison leaves out what git ignores among the untracked files —
the caches the gates create (ruff and pytest ignore their own directories)
are machine state, not the tree — and names no tool or path of its own: the
one gate list stays the only place that names them (decisions Q-5).
"""

from __future__ import annotations

import argparse
import codecs
import contextlib
import dataclasses
import hashlib
import json
import os
import shlex
import signal
import stat
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ci_gates  # noqa: E402
import verify_duration  # noqa: E402
import verify_lock  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

# Every git call of the snapshot is bounded: a wedged git must fail the
# measurement, never hang the run it was supposed to protect.
GIT_TIMEOUT_SECONDS = 10.0

# How long a gate's output is still drained after its process group was ended.
# A descendant that left the group (its own session) can keep the gate's pipes
# open; the run never waits on it longer than this (review row L1-1).
OUTPUT_DRAIN_SECONDS = 5.0

# The exact frames the previous runner printed (the tests and the
# repair-evidence parser read them): gate frames with one space after `──`,
# the not-run summary with three. Never reword either one lightly.
VERDICT_GREEN = "gruen"
VERDICT_RED = "RED (block) — der Lauf ist rot."
VERDICT_NONBLOCK = "rot, aber nur {enforcement} — er meldet, er blockiert nicht."
NOT_RUN_HEADER = "── not run — the run stopped at the blocking failure in [{stop}]:"
NOT_RUN_ENTRY = "──   [{gate}] not run"
BANNER_RED = "VERIFY RED — at least one gate failed; the report above names it."
BANNER_GREEN = "VERIFY GREEN — every local gate of the '{job}' job passed."
STORAGE_WARNING = (
    "verify-duration: measurement storage unusable — this run is not recorded; gates and verdicts continue unchanged"
)


class SnapshotUnusable(Exception):
    """The tree state cannot be measured or was not stable; the run refuses instead of trusting."""


class VerifyRunRefused(Exception):
    """The run cannot continue honestly (unstable tree, failed refresh, unusable state)."""


class GateInterrupted(BaseException):
    """A trapped signal ended the run; every live gate group was killed before it propagated."""

    def __init__(self, signum: int) -> None:
        super().__init__(signum)
        self.signum = signum


@dataclasses.dataclass
class GateProcess:
    """What an executor returns: the raw exit code and the captured streams."""

    returncode: int
    stdout: str
    stderr: str


@dataclasses.dataclass
class GateOutcome:
    """One executed gate's raw result, as the scheduler saw it."""

    gate: str
    exit_code: int
    seconds: float | None


@dataclasses.dataclass
class RunResult:
    """The scheduler's account of one invocation."""

    exit_code: int
    executed: list[str]
    not_run: list[str]
    stop_gate: str | None
    admission_requested: bool
    admission_wait_seconds: float | None
    red: bool


@dataclasses.dataclass(frozen=True)
class TreeSnapshot:
    """One stable reading of a checkout's tree identity (bead coding-harness-bxxt.6).

    HEAD, the semantic index entries and the tracked working paths' types,
    modes and contents, plus the non-ignored untracked paths and contents.
    Index stat-cache churn and the gates' own cache directories change
    nothing here; a content or path change changes the fingerprint.
    """

    fingerprint: str


def _git_bytes(root: Path, *args: str) -> bytes:
    """One bounded git answer, or a refusal — a wedged git never passes for a stable tree."""
    try:
        done = subprocess.run(
            ["git", *args],
            cwd=str(root),
            capture_output=True,
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise SnapshotUnusable(f"git {' '.join(args)} could not run: {error}") from error
    if done.returncode != 0:
        detail = done.stderr.decode("utf-8", "replace").strip() or f"exit {done.returncode}"
        raise SnapshotUnusable(f"git {' '.join(args)} failed: {detail}")
    return done.stdout


def _safe(relative: str) -> str:
    """A repository-relative path the tree comparison may open; anything else refuses."""
    if relative.startswith("/"):
        raise SnapshotUnusable(f"{relative!r} is not a repository-relative path; refusing to measure the tree")
    if any(part in ("", "..") for part in relative.split("/")):
        raise SnapshotUnusable(f"{relative!r} is not a plain repository-relative path; refusing to measure the tree")
    return relative


def _measure(path: Path, allow_missing: bool) -> str:
    """A path's type, mode and content: symlinks by their target, never followed.

    For an indexed (tracked) path a missing file is a legitimate state — a
    deletion is part of the tree. For an untracked path that the listing had
    just named, vanishing mid-snapshot is a changing tree and refuses.
    """
    try:
        info = path.lstat()
    except FileNotFoundError:
        if allow_missing:
            return "missing"
        raise SnapshotUnusable(f"{path} vanished while the tree was being measured") from None
    except OSError as error:
        raise SnapshotUnusable(f"{path} cannot be measured ({error.strerror or error})") from error
    mode = stat.S_IMODE(info.st_mode)
    if stat.S_ISLNK(info.st_mode):
        try:
            target = path.readlink()
        except OSError as error:
            raise SnapshotUnusable(
                f"the symlink target of {path} cannot be read ({error.strerror or error})"
            ) from error
        return f"link {mode:o} {target}"
    if not stat.S_ISREG(info.st_mode):
        raise SnapshotUnusable(f"{path} is not a regular file or symlink; refusing to measure the tree")
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1 << 20), b""):
                digest.update(block)
    except OSError as error:
        raise SnapshotUnusable(f"{path} cannot be read ({error.strerror or error})") from error
    return f"file {mode:o} {digest.hexdigest()}"


def _index_entries(root: Path) -> list[tuple[str, int]]:
    """The semantic index entries: paths and modes; conflict stages and gitlinks refused."""
    raw = _git_bytes(root, "ls-files", "-z", "--stage")
    entries: list[tuple[str, int]] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, _, path_bytes = record.partition(b"\t")
        words = meta.split(b" ")
        if len(words) != 3:
            raise SnapshotUnusable("the git index could not be parsed; refusing to measure the tree")
        mode = int(words[0], 8)
        stage = int(words[2])
        path = os.fsdecode(path_bytes)
        if stage != 0:
            raise SnapshotUnusable("the index holds conflict stages; refusing to measure an unresolved tree")
        if mode == 0o160000:
            raise SnapshotUnusable(f"{path} is a gitlink; the tree cannot be measured until submodules are supported")
        entries.append((_safe(path), mode))
    return entries


def tree_snapshot(root: Path | str) -> TreeSnapshot:
    """One stable reading of the checkout's tree identity, or a refusal that names the gap."""
    wurzel = Path(root)
    digest = hashlib.sha256()
    head = _git_bytes(wurzel, "rev-parse", "HEAD").decode("utf-8", "replace").strip()
    if not head:
        raise SnapshotUnusable("HEAD cannot be named; a checkout without a commit has no measurable tree")
    digest.update(b"head\0" + head.encode("utf-8") + b"\0")
    entries = sorted(_index_entries(wurzel))
    digest.update(b"index\0")
    for path, mode in entries:
        digest.update(f"{path}\0{mode:o}\0{_measure(wurzel / path, allow_missing=True)}\0".encode())
    others = _git_bytes(wurzel, "ls-files", "-z", "--others", "--exclude-standard")
    names = sorted(os.fsdecode(piece) for piece in others.split(b"\0") if piece)
    digest.update(b"untracked\0")
    for name in names:
        digest.update(f"{_safe(name)}\0{_measure(wurzel / name, allow_missing=False)}\0".encode())
    return TreeSnapshot(digest.hexdigest())


def _reading(command: list[str]) -> str:
    """One bounded tool answer for the worker sizing, or nothing — never an error."""
    try:
        done = subprocess.run(
            command, capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS, check=False, stdin=subprocess.DEVNULL
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if done.returncode != 0:
        return ""
    return done.stdout.strip()


def _usable_count(text: str) -> int | None:
    """A raw reading as a positive decimal integer, else None (the shell's rules, kept)."""
    if not text or len(text) > 18 or not (text.isascii() and text.isdigit()):
        return None
    value = int(text)
    return value if value > 0 else None


def worker_default() -> int | None:
    """The local worker default (bead coding-harness-l7sc), moved here for both callers.

    The smaller of half the logical cores (floored, at least one) and the
    detected memory in 2-GiB steps (at least one). A failed or malformed
    reading is ignored, never an error: with no usable reading the caller
    leaves the variable unset and xdist's own auto applies. The caller's own
    non-empty `PYTEST_XDIST_AUTO_NUM_WORKERS` passes through verbatim — only
    this function computes, the caller decides.
    """
    system = _reading(["uname", "-s"])
    cores = ""
    nbytes = ""
    if system == "Darwin":
        cores = _reading(["sysctl", "-n", "hw.logicalcpu"])
        nbytes = _reading(["sysctl", "-n", "hw.memsize"])
    elif system == "Linux":
        cores = _reading(["nproc"])
        # MemTotal is reported in KiB; the bound below counts bytes.
        kib = _reading(["awk", "/^MemTotal:/ { print $2; exit }", "/proc/meminfo"])
        count = _usable_count(kib)
        if count is not None and len(kib) <= 15:
            nbytes = str(count * 1024)
    cpu = _usable_count(cores)
    mem = _usable_count(nbytes)
    bounds = [cpu // 2 if cpu is not None else None, mem // (2**31) if mem is not None else None]
    usable = [max(bound, 1) for bound in bounds if bound is not None]
    return min(usable) if usable else None


# The process groups of gates the default executor is currently running; a
# trapped signal ends them all before the interrupt propagates.
_LIVE_GROUPS: set[int] = set()


def gate_process(
    root: Path,
    python: str,
    lock_slot: dict[str, int | None],
    _gate: dict[str, Any],
    command: str,
    env: dict[str, str],
    out: Any = None,
    err: Any = None,
) -> GateProcess:
    """The default executor's one gate: `sh -c` with the pinned interpreter substituted.

    The declared command is printed by the scheduler, so only the resolved
    form runs here — the substitution replaces the first `python3`, exactly
    like the shell's `${cmd/python3/...}` did. A protected gate's environment
    carries the admission marker, and the lock descriptor travels with it, so
    ownership outlives this process for exactly the gate's own descendants.

    The gate's output is relayed to `out`/`err` while it runs, so an
    interrupted gate keeps what it already printed. The run waits for the gate
    leader, never for end-of-file: a child still holding the pipes is ended
    with the leader's group, and one that left the group is not waited for
    beyond `OUTPUT_DRAIN_SECONDS` — its later output is dropped, never written
    after the gate's verdict (review row L1-1).
    """
    resolved = command.replace("python3", shlex.quote(python), 1)
    pass_fds: tuple[int, ...] = ()
    descriptor = lock_slot.get("fd")
    if env.get(verify_lock.LOCK_ENV) and descriptor is not None:
        pass_fds = (descriptor,)
    proc = subprocess.Popen(
        ["sh", "-c", resolved],
        cwd=str(root),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
        pass_fds=pass_fds,
    )

    complaints = sys.stderr if err is None else err
    closed = threading.Event()
    writing = threading.Lock()

    def relay(source: Any, destination: Any) -> None:
        decoder = codecs.getincrementaldecoder("utf-8")("replace")
        try:
            # Reading goes on after the frame closed, so a writer never blocks on a full pipe.
            while data := source.read1(65536):
                with writing:
                    if not closed.is_set():
                        destination.write(decoder.decode(data))
                        destination.flush()
            with writing:
                if not closed.is_set():
                    destination.write(decoder.decode(b"", final=True))
                    destination.flush()
        finally:
            source.close()

    readers = [
        threading.Thread(target=relay, args=(proc.stdout, sys.stdout if out is None else out), daemon=True),
        threading.Thread(target=relay, args=(proc.stderr, complaints), daemon=True),
    ]
    _LIVE_GROUPS.add(proc.pid)
    for reader in readers:
        reader.start()
    try:
        # Wait for the gate leader, not EOF: descendants may still own its pipes.
        proc.wait()
    finally:
        verify_lock.end_lingering_group(proc.pid)
        proc.wait()
        drained = time.monotonic() + OUTPUT_DRAIN_SECONDS
        for reader in readers:
            reader.join(timeout=max(0.0, drained - time.monotonic()))
        with writing:
            closed.set()
            if any(reader.is_alive() for reader in readers):
                complaints.write(
                    "verify-run: a process that left the gate's group still holds its output; "
                    f"the rest is dropped after {OUTPUT_DRAIN_SECONDS:g}s\n"
                )
                complaints.flush()
        _LIVE_GROUPS.discard(proc.pid)
    return GateProcess(returncode=proc.returncode, stdout="", stderr="")


def _install_run_handlers() -> dict[int, object]:
    """Turn SIGINT, SIGTERM, SIGHUP and SIGQUIT into an interrupt that kills the gate groups first."""
    previous: dict[int, object] = {}
    if threading.current_thread() is not threading.main_thread():
        return previous

    def interrupted(signum: int, _frame: object) -> None:
        for group in list(_LIVE_GROUPS):
            with contextlib.suppress(OSError):
                os.killpg(group, signal.SIGTERM)
        for group in list(_LIVE_GROUPS):
            with contextlib.suppress(OSError):
                os.killpg(group, signal.SIGKILL)
        raise GateInterrupted(signum)

    for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT):
        with contextlib.suppress(ValueError, OSError):
            previous[signum] = signal.signal(signum, interrupted)
    return previous


def _restore_run_handlers(previous: dict[int, object]) -> None:
    for signum, handler in previous.items():
        with contextlib.suppress(ValueError, OSError):
            signal.signal(signum, handler)  # type: ignore[arg-type]


def _final_revision(root: Path) -> str | None:
    """The tree's HEAD at the run's end, or None — never a guess (bounded, tolerant)."""
    try:
        return _git_bytes(root, "rev-parse", "HEAD").decode("utf-8", "replace").strip() or None
    except SnapshotUnusable:
        return None


def _final_config_digest(root: Path) -> str | None:
    """The gate configuration's digest at the run's end, or None (bounded, tolerant)."""
    try:
        return hashlib.sha256((Path(root) / "decisions" / "gates.yaml").read_bytes()).hexdigest()
    except OSError:
        return None


def run_verification(
    root: Path | str,
    *,
    job: str = "verify",
    ci: bool = False,
    env: dict[str, str] | None = None,
    out: Any = None,
    err: Any = None,
    executor: Callable[[dict[str, Any], str, dict[str, str]], GateProcess] | None = None,
    clock: Callable[[], float] = verify_duration.monotonic,
    budget: dict[str, float] | None = None,
    record_history: bool = True,
    python: str | None = None,
    lock_slot: dict[str, int | None] | None = None,
    admission_command: list[str] | None = None,
) -> RunResult:
    """Run the job's local gates in two phases and return the run's account.

    The `executor` receives the gate record, the declared command and the
    environment to run it under, and returns a `GateProcess`; when it raises,
    the run ends visibly incomplete (no completion record). `budget`, when
    given, has its `"deadline"` extended by the measured admission wait, so
    queue and memory waits never consume a caller's execution bound.
    `lock_slot`, when given, is the holder the held admission's lock
    descriptor is published into while the protected phase runs — a callback
    that starts protected children reads it there to hand the descriptor on,
    exactly as the built-in executor does. `admission_command` is what the
    holder record names while waiters queue behind this run (default: this
    scheduler and its job).
    """
    wurzel = Path(root)
    destination = sys.stdout if out is None else out
    complaints = sys.stderr if err is None else err
    # The shell exports the interpreter it chose as `PYTHON`; gates run under that one,
    # exactly as the shell runner substituted it (a wrapper in the checkout stays the pinned one).
    pinned = python if python is not None else (os.environ.get("PYTHON") or sys.executable)
    slot = lock_slot if lock_slot is not None else {"fd": None}

    def emit(text: str) -> None:
        destination.write(text + "\n")
        destination.flush()

    def complain(text: str) -> None:
        complaints.write(text + "\n")

    # The history seam, in the shell's dur_call shape: the first storage
    # failure warns once, and every later operation is skipped — the gates,
    # their enforcement and the verdict continue unchanged.
    broken = False

    def warn_storage() -> None:
        nonlocal broken
        if not broken:
            complain(STORAGE_WARNING)
        broken = True

    def record(operation: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        nonlocal broken
        if not record_history or broken:
            return None
        try:
            return operation(*args, **kwargs)
        except verify_duration.StorageUnusable:
            warn_storage()
            return None

    if executor is None:
        # The shell-shaped default: every gate as a registered process group,
        # signals end all descendants, and a protected gate inherits the lock
        # descriptor through the environment the scheduler hands it.
        def executor(  # noqa: W0201 - one binding, before any use
            gate: dict[str, Any], command: str, run_env: dict[str, str]
        ) -> GateProcess:
            return gate_process(wurzel, pinned, slot, gate, command, run_env, destination, complaints)

    executed: dict[str, GateOutcome] = {}
    reds: list[str] = []
    segments: list[tuple[float, float]] = []
    admission_requested = False
    admission_wait: float | None = None
    context = verify_lock.AdmissionContext(admission_id=None, wait_seconds=None, reused=None)
    base_env = dict(os.environ if env is None else env)
    if not str(base_env.get("PYTEST_XDIST_AUTO_NUM_WORKERS", "")).strip():
        workers = worker_default()
        if workers is None:
            base_env.pop("PYTEST_XDIST_AUTO_NUM_WORKERS", None)
        else:
            base_env["PYTEST_XDIST_AUTO_NUM_WORKERS"] = str(workers)
    run_id_holder: dict[str, str | None] = {
        "id": record(verify_duration.record_start, job, "ci" if ci else "local", root=wurzel, env=base_env)
    }
    selection_holder: dict[str, list[dict[str, Any]]] = {"selection": []}

    def run_gate(gate: dict[str, Any], gate_env: dict[str, str]) -> bool:
        """Execute one gate and print its exact frames; True when it failed blocking."""
        identifier = str(gate["id"])
        emit("")
        emit(f"── [{identifier}] $ {gate['command']}")
        started = clock()
        done = executor(gate, str(gate["command"]), gate_env)
        ended = clock()
        segments.append((started, ended))
        destination.write(done.stdout)
        complaints.write(done.stderr)
        measured = record(
            verify_duration.record_gate,
            run_id_holder["id"],
            identifier,
            started,
            ended,
            done.returncode,
            gate["enforcement"],
        )
        executed[identifier] = GateOutcome(gate=identifier, exit_code=done.returncode, seconds=measured)
        # The verdict closes the gate's frame for the repair-evidence parser, so the
        # measured seconds follow it: a timing line in between would end the section
        # before its RED line (`stage2.GATE_END` counts any non-start frame line).
        failed = False
        if done.returncode == 0:
            emit(f"── [{identifier}] {VERDICT_GREEN}")
        elif gate["enforcement"] == "block":
            emit(f"── [{identifier}] {VERDICT_RED}")
            failed = True
        else:
            emit(f"── [{identifier}] {VERDICT_NONBLOCK.format(enforcement=gate['enforcement'])}")
        if measured is not None:
            emit(f"── [{identifier}] {measured:.3f}s")
        return failed

    def note_blocking(gate: dict[str, Any]) -> None:
        identifier = str(gate["id"])
        if identifier not in reds:
            reds.append(identifier)

    def finish() -> RunResult:
        """The one ending: not-run summary, completion record, banner, exit code."""
        red = bool(reds)
        final = selection_holder["selection"]
        not_run = [str(g["id"]) for g in final if str(g["id"]) not in executed]
        if red and not ci and not_run:
            emit("")
            emit(NOT_RUN_HEADER.format(stop=reds[0]))
            for identifier in not_run:
                emit(NOT_RUN_ENTRY.format(gate=identifier))
        verdict = "red" if red else "green"
        summary = None
        if run_id_holder["id"] is not None:
            summary = record(
                verify_duration.record_end,
                run_id_holder["id"],
                verdict,
                segments=segments,
                context=context,
                admission_requested=admission_requested,
                final_commit=_final_revision(wurzel),
                final_config=_final_config_digest(wurzel),
            )
        if summary is not None:
            emit(summary)
        emit("")
        if red:
            emit(BANNER_RED)
        else:
            emit(BANNER_GREEN.format(job=job))
        return RunResult(
            exit_code=1 if red else 0,
            executed=list(executed),
            not_run=not_run,
            stop_gate=reds[0] if reds else None,
            admission_requested=admission_requested,
            admission_wait_seconds=admission_wait,
            red=red,
        )

    try:
        # The shell ran the gate-list reader as a process of its own, so any failure in it was a
        # red run with a diagnostic. In-process, a malformed list can raise more than the reader
        # names (a non-mapping gate entry reaches `.get` as a string), so every reader failure is
        # caught here, at the one place the scheduler loads the list (review row L1-12).
        try:
            bericht = ci_gates.report_at(wurzel, job)
        except Exception as exc:  # noqa: BLE001 - the reader's process boundary, kept in-process
            complain(f"FEHLER: {exc}")
            complain("die Gate-Liste liess sich nicht erzeugen — kein VERIFY ohne gemessene Gates")
            return RunResult(2, [], [], None, False, None, False)
        emit(json.dumps(bericht, indent=2))
        try:
            selection = ci_gates.selection_at(wurzel, job, ci=ci)
        except Exception as exc:  # noqa: BLE001 - the reader's process boundary, kept in-process
            complain(f"FEHLER: {exc}")
            complain("die Gate-Liste liess sich nicht erzeugen — kein VERIFY ohne gemessene Gates")
            return RunResult(2, [], [], None, False, None, False)
        if not selection:
            complain("die Gate-Liste ist leer — ein Job ohne messbare Gates ist ein Konfigurationsfehler")
            return RunResult(2, [], [], None, False, None, False)
        selection_holder["selection"] = selection

        # Both phases inherit the admission state a nested run must reuse: the
        # cheap gates are not protected, but their children resolve a valid
        # ancestor's admission the same way the protected ones do.
        gate_env = verify_lock.inherit_env(base_env)

        cheap = [g for g in selection if not g["admission"]]
        protected = [g for g in selection if g["admission"]]

        def measure(where: str) -> TreeSnapshot:
            try:
                return tree_snapshot(wurzel)
            except SnapshotUnusable as exc:
                complain(f"the tree state cannot be measured {where}: {exc}")
                complain("rerun the check — unmeasured cheap results are never trusted as a baseline")
                raise VerifyRunRefused(str(exc)) from exc

        # 1. Every unprotected gate executes before any admission, red or not:
        # all cheap diagnostics together, in the selection's order.
        before = measure("before the cheap pass")
        for gate in cheap:
            if run_gate(gate, gate_env):
                note_blocking(gate)
        after = measure("after the cheap pass")
        if before.fingerprint != after.fingerprint:
            complain("the checkout changed while the cheap gates ran — the baseline is not stable")
            complain("rerun the check — a changing tree is never accepted as a stable baseline")
            raise VerifyRunRefused("the tree changed during the cheap pass")

        # 2. A cheap blocking failure ends the run before any protected work.
        if reds and not ci:
            return finish()

        # 3. One admission for the whole protected set; an empty set never queues.
        if protected:
            admission_requested = True
            entered = clock()
            with verify_lock.hold_admission(admission_command or ["verify-run", job]) as lock_fd:
                waited = clock() - entered
                admission_wait = waited
                if budget is not None and waited > 0:
                    budget["deadline"] = budget.get("deadline", 0.0) + waited
                if lock_fd is not None:
                    slot["fd"] = lock_fd
                held = verify_lock.inherit_env(gate_env)
                # 4. The stable baseline must still be there; a moved tree is
                # reselected from the reloaded list and its complete
                # unprotected set reruns inside the held admission.
                current = measure("at the admission boundary")
                if current.fingerprint != after.fingerprint:
                    try:
                        refreshed = ci_gates.selection_at(wurzel, job, ci=ci)
                    except Exception as exc:  # noqa: BLE001 - the reader's process boundary
                        complain(f"FEHLER: {exc}")
                        raise VerifyRunRefused(
                            "the gate list cannot be reloaded after the tree changed; protected work stops"
                        ) from exc
                    if not refreshed:
                        raise VerifyRunRefused(
                            "the reloaded gate list selects nothing — a job without measurable gates "
                            "is a configuration error"
                        )
                    selection_holder["selection"] = refreshed
                    cheap = [g for g in refreshed if not g["admission"]]
                    protected = [g for g in refreshed if g["admission"]]
                    recheck_before = measure("before the refreshed cheap pass")
                    for gate in cheap:
                        if run_gate(gate, gate_env):
                            note_blocking(gate)
                    recheck_after = measure("after the refreshed cheap pass")
                    if recheck_before.fingerprint != recheck_after.fingerprint:
                        raise VerifyRunRefused("the tree changed again during the refreshed cheap pass")
                    if reds and not ci:
                        context = verify_lock.admission_context()
                        return finish()
                # 5. The protected set under the held admission; locally the
                # first blocking failure stops it, `--ci` stays exhaustive.
                for gate in protected:
                    if not ci and reds:
                        break
                    if run_gate(gate, held):
                        note_blocking(gate)
                context = verify_lock.admission_context()
    except VerifyRunRefused as refused:
        complain(f"verify-run: {refused}")
        return RunResult(
            exit_code=2,
            executed=list(executed),
            not_run=[str(g["id"]) for g in selection_holder["selection"] if str(g["id"]) not in executed],
            stop_gate=reds[0] if reds else None,
            admission_requested=admission_requested,
            admission_wait_seconds=admission_wait,
            red=bool(reds),
        )

    return finish()


def main(argv: list[str] | None = None) -> int:
    """The CLI the shell entry point execs: the same scheduler, one argv."""
    parser = argparse.ArgumentParser(
        description="Run the local gates of the one list in two phases: cheap first, one admission for the rest."
    )
    parser.add_argument("--job", choices=ci_gates.JOBS + ci_gates.SUBSETS, default="verify")
    parser.add_argument("--ci", action="store_true", help="the CI's gate set: exhaustive, action equivalents skipped")
    parser.add_argument("--root", default=None, help="the checkout to measure (default: this checkout's root)")
    args = parser.parse_args(argv)
    wurzel = Path(args.root).resolve() if args.root else REPO_ROOT
    previous = _install_run_handlers()
    try:
        return run_verification(wurzel, job=args.job, ci=args.ci).exit_code
    except verify_lock.MemoryFloorRefused as refused:
        print(f"[verify-lock] admission refused: {refused}", file=sys.stderr, flush=True)
        return 3
    except verify_lock.VerifyLockError as refused:
        print(f"[verify-lock] admission refused: {refused}", file=sys.stderr, flush=True)
        return 2
    except GateInterrupted as stop:
        return 128 + stop.signum
    finally:
        _restore_run_handlers(previous)


if __name__ == "__main__":
    raise SystemExit(main())
