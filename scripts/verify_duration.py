#!/usr/bin/env python3
"""verify_duration.py — measured verification durations, recorded locally only.

The shared scheduler (`scripts.verify_run`) calls the operations of this
module around the gates it already runs: `start` one run identity before the
report and gate selection, `gate` per executed gate (including a cheap pass
that reruns after a changed tree), `end` at the final verdict. Each write
appends one version-1 JSON line to `verify-duration.jsonl` under
`verify_lock.state_root()` — the same shared state root the admission keeps,
outside the repository, local only: no command output, no credentials, no
upload (bead coding-harness-1um6, spec "Non-goals").

**Time.** Elapsed seconds are differences of `time.monotonic()`, so a wall
clock adjustment cannot produce negative or inflated durations, and an
inherited admission's wait is recorded as the shared context it is — never
added into execution seconds. `run_end.seconds` sums the active gate
segments of one invocation, so the queue and memory waits stay outside it.
Unavailable readings are recorded as JSON null, never as zero by assumption
(spec, "Terms").

**Completion context.** A completion may carry optional additive fields —
`admission_requested`, the final admission context (`admission_id`,
`admission_wait_seconds`, `admission_reused`) and the final revision and
configuration identity (`commit`, `config_sha256`). Their presence switches
the reader to the completion's context, so a cheap-only run can state that
no admission was requested and a run that changed trees while queued can
name its final state; a completion without the fields reads exactly as
before (bead coding-harness-bxxt.6).

**Interruption.** A killed run can leave a start without an end; the reader
labels such a run incomplete instead of inventing a verdict. A truncated
final line is diagnosed, and the valid records before it are preserved — the
reader never repairs or truncates history.

**Refusals.** A history destination that is a symlink or not a regular file,
or a state root that cannot be created, refuses the write with a diagnostic
on stderr and exit code 2, without writing through the substituted file. The
caller (`verify_run`) reports the missing history and lets the gates and
their verdicts continue unchanged; such a run cannot supply a persisted
baseline (spec acceptance criterion 7).

Command line:

    python -m scripts.verify_duration clock
    python -m scripts.verify_duration start --job verify --placement local
    python -m scripts.verify_duration gate --run ID --gate GID \
            --start T0 --end T1 --status N --enforcement block
    python -m scripts.verify_duration end --run ID --start T0 --end T1 --verdict green
    python -m scripts.verify_duration end --run ID --start T0 --end T1 --verdict green --no-admission
    python -m scripts.verify_duration report [--run ID]
    python -m scripts.verify_duration slips [--since UTC] [--until UTC] [--change NAME]

**Slips.** A slip is one completed red local full verification run that answers
the immediately preceding completed check of the same repository, change,
checked tree and gate configuration when that check is a green targeted check
(bead coding-harness-bxxt.7). Nothing about a slip is ever written: the `slips`
reader derives the count from the run records the runner already leaves.
Full checks stay in `verify-duration.jsonl` as version-1 events with additive
comparison fields (`check_kind`, `change`, `tree_id` and the marker
`comparison_version`: 2, captured by `record_start` from the runner-owned
variables of the scheduler's environment). Targeted checks record their start and end through
`begin_targeted_run`/`finish_targeted_run` into `verify-targeted.jsonl` beside
it, so no duration reader ever counts a targeted check as a full duration. The
reader combines both histories, orders checks by UTC completion with strict
earlier-than, and stands the count beside the incomplete or not countable runs,
the separate flaky-test signal and the runs outside the count — lost or
conflicting evidence is a gap, never a zero (decisions Q-1, Q-2, Q-8, Q-10).
Exit codes of `slips`: 0 complete evidence, 1 partial or unavailable evidence,
2 an invalid interval or refused storage. Reading never appends, repairs or
creates history.
"""

from __future__ import annotations

import argparse
import datetime
import fcntl
import hashlib
import json
import math
import os
import stat
import subprocess
import sys
import time
import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_lock  # noqa: E402

HISTORY_NAME = "verify-duration.jsonl"
# The targeted checks' own history, beside the duration history and created at
# the first version-2 runner record: a targeted duration never reaches a reader
# of full-run durations.
TARGETED_HISTORY_NAME = "verify-targeted.jsonl"
EVENT_VERSION = 1
# The additive marker every comparison-carrying start holds. The outer event
# version stays 1, so older readers accept the new fields.
COMPARISON_VERSION = 2
RUN_START = "run_start"
GATE = "gate"
RUN_END = "run_end"
EVENTS = (RUN_START, GATE, RUN_END)
GATE_FILE = Path("decisions") / "gates.yaml"
GIT_TIMEOUT_SECONDS = 10.0
# The check kinds a start record can name. `targeted` is written only by
# `begin_targeted_run`, never from the environment: no launcher can mint a
# targeted predecessor by exporting a variable. A distinct kind for a fallback
# full run is not part of this change (bead coding-harness-rodx); a fallback is
# recorded as `full`, and a record naming any other kind is read as unknown.
CHECK_KINDS = ("targeted", "full")
# The one kind a launcher may name through the environment (full_run_context).
ENVIRONMENT_KINDS = ("full",)
# The prefix that keeps a refused environment kind in the record: never a
# known kind, never null, so the reader diagnoses it instead of reading a
# legacy record.
UNRECOGNISED_KIND_PREFIX = "unrecognised:"
# The runner-owned variables of one full launch (full_run_context, full_verify).
# Absent means a legacy record; present-but-empty means the explicit unknown.
KIND_ENV = "HARNESS_VERIFY_DURATION_KIND"
CHANGE_ENV = "HARNESS_VERIFY_DURATION_CHANGE"
TREE_ENV = "HARNESS_VERIFY_DURATION_TREE"
# All three, for the scheduler to drop from its gates' environment once the start is recorded.
COMPARISON_ENV_NAMES = (KIND_ENV, CHANGE_ENV, TREE_ENV)


class StorageUnusable(Exception):
    """Measurement storage cannot be used safely; the caller reports and continues."""


class HistoryMissing(Exception):
    """The reader found no history file where one would be recorded."""


def history_path(state_root: Path | None = None) -> Path:
    """The one history file under the shared verification state root.

    An explicit root scopes the file for an in-process caller that must not
    depend on the environment it happened to inherit; the default resolves
    the shared root from the environment, as always.
    """
    basis = verify_lock.state_root() if state_root is None else Path(state_root)
    return basis / HISTORY_NAME


def targeted_history_path(state_root: Path | None = None) -> Path:
    """The targeted checks' history file beside the duration history."""
    basis = verify_lock.state_root() if state_root is None else Path(state_root)
    return basis / TARGETED_HISTORY_NAME


def _log(message: str) -> None:
    """One line to the operator's stderr, directly — not through a captured launcher."""
    print(f"[verify-duration] {message}", file=sys.stderr, flush=True)


def _utc_now() -> str:
    """The explicit UTC attribution of a record (spec acceptance criterion 4)."""
    return datetime.datetime.now(datetime.UTC).isoformat()


def monotonic() -> float:
    """The monotonic clock; the seam the tests inject fake time through."""
    return time.monotonic()


def _git(arguments: list[str], cwd: Path | None = None) -> str | None:
    """One git answer, or None when git is absent, fails or times out — never a guess."""
    try:
        done = subprocess.run(
            ["git", *arguments], capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS, check=False, cwd=cwd
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if done.returncode != 0:
        return None
    return done.stdout.strip()


def _common_git_dir(root: Path | None = None) -> str | None:
    """Resolve the shared Git directory at recording or reader time."""
    base = root or Path.cwd()
    answer = _git(["rev-parse", "--git-common-dir"], cwd=root)
    if not answer:
        return None
    return str((base / answer).resolve())


def _gate_file_digest(root: Path | None = None) -> str | None:
    """The SHA-256 of the one gate file this run measured, or None when absent."""
    basis = Path(root) if root is not None else Path.cwd()
    try:
        return hashlib.sha256((basis / GATE_FILE).read_bytes()).hexdigest()
    except OSError:
        return None


def _worker_setting(env: dict[str, str] | None = None) -> str | None:
    """The effective worker setting passed to the gates; unset means xdist decides."""
    value = (os.environ if env is None else env).get("PYTEST_XDIST_AUTO_NUM_WORKERS", "")
    return value if value else None


def _open_history(destination: Path | None = None, *, state_root: Path | None = None) -> int:
    """A private regular history file for appending; an aliased or nonregular destination refuses.

    The same shape as the admission's lock files: the no-follow open fails on
    a symlink standing in the file's place, a FIFO cannot pass the regular
    check, and nothing is ever written through a substituted destination.
    `destination` names the targeted history; the default is the duration history.
    `state_root` scopes the default for an in-process caller (`history_path`).
    """
    root = verify_lock.state_root() if state_root is None else Path(state_root)
    try:
        root.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise StorageUnusable(
            f"the shared state directory {root} cannot be created ({error.strerror or error})"
        ) from error
    if root.is_symlink() or not root.is_dir():
        raise StorageUnusable(f"the shared state directory {root} is not a usable directory")
    path = destination or history_path(root)
    try:
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND | os.O_NOFOLLOW, 0o600)
    except FileExistsError:
        pass
    except OSError as error:
        raise StorageUnusable(
            f"the history file {path} cannot be created no-follow ({error.strerror or error}) — "
            "a substituted destination is refused, never written through"
        ) from error
    # O_NONBLOCK so a FIFO standing in the file's place is refused below, never waited on.
    try:
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError as error:
        raise StorageUnusable(
            f"the history file {path} is not a private regular file; refusing substituted history"
        ) from error
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        os.close(fd)
        raise StorageUnusable(f"the history file {path} is not an unaliased regular file; refusing substituted history")
    return fd


def append_event(event: dict, destination: Path | None = None, *, state_root: Path | None = None) -> None:
    """Append one complete JSON line under a file lock, so concurrent runs never mix identities.

    `destination` names the targeted history; `state_root` scopes the default duration history.
    """
    line = json.dumps(event, sort_keys=True) + "\n"
    fd = _open_history(destination, state_root=state_root)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            data = line.encode("utf-8")
            if os.write(fd, data) != len(data):
                raise StorageUnusable("the history write was incomplete; refusing to claim a complete event")
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    except OSError as error:
        raise StorageUnusable(f"the history lock or write failed ({error}); refusing to record event") from error
    finally:
        os.close(fd)


def _seconds(start: str, end: str) -> float:
    """Elapsed seconds from two monotonic readings; a negative window refuses."""
    try:
        elapsed = float(end) - float(start)
    except ValueError:
        raise StorageUnusable(f"a monotonic reading is not a number ({start!r}, {end!r})") from None
    if not math.isfinite(elapsed) or elapsed < 0:
        raise StorageUnusable(f"the monotonic window {start}..{end} is negative — refusing to record it")
    return elapsed


def _context_fields() -> dict:
    """The admission context of this run, with explicit unknowns (spec acceptance criterion 5)."""
    context = verify_lock.admission_context()
    return {
        "admission_id": context.admission_id,
        "admission_wait_seconds": context.wait_seconds,
        "admission_reused": context.reused,
    }


def _comparison_fields(env: dict[str, str] | None = None) -> dict:
    """The comparison context of a full run, when its launcher supplied one.

    Only the runner's own full checks carry these variables (`full_verify` hands
    them to the shared scheduler's environment, which `record_start` reads; a
    shell launch exports them to `verify_all.sh`); a start without them stays a
    legacy duration record. Empty values become the explicit unknown. Any other
    kind than `full` (`targeted` included: the environment must not be able to
    mint a targeted predecessor) is kept with the `unrecognised:` prefix, which
    is no known kind, so the reader diagnoses the run as not countable instead
    of reading a null kind as a legacy record (loop row L4-1).
    """
    source = os.environ if env is None else env
    if KIND_ENV not in source:
        return {}
    kind = source.get(KIND_ENV, "").strip()
    if not kind:
        recorded = None
    elif kind in ENVIRONMENT_KINDS:
        recorded = kind
    else:
        recorded = UNRECOGNISED_KIND_PREFIX + kind
    return {
        "check_kind": recorded,
        "change": source.get(CHANGE_ENV, "").strip() or None,
        "tree_id": source.get(TREE_ENV, "").strip() or None,
        "comparison_version": COMPARISON_VERSION,
    }


def full_run_context(tree: str | None, change: str | None) -> dict[str, str]:
    """The runner-owned environment of one full check, for `record_start` to capture.

    The launcher (`full_verify`) adds these to the environment it hands the shared
    scheduler (`verify_run.run_verification`) for that one run and never to its
    own; ambient variables of the same names cannot leak in, since the runner's
    allow-list already stripped them. Empty means the explicit
    unknown in the start record.
    """
    return {
        KIND_ENV: "full",
        CHANGE_ENV: change or "",
        TREE_ENV: tree or "",
    }


@dataclass
class TargetedRun:
    """One targeted check's comparison evidence, recorded around its execution."""

    run_id: str | None  # None: the start row was refused; nothing of this run is recorded
    started: float  # the monotonic reading at the start, for the end row's seconds
    notes: list[str] = field(default_factory=list)  # diagnostics of refused appends, for the runner to report


def begin_targeted_run(root: Path, change: str | None, tree: str | None) -> TargetedRun:
    """Record the targeted check's start before it runs, as ordinary run evidence.

    The caller (`run_targeted`) captures the checked tree on both sides of
    execution and passes the pre-execution identity here; the end row carries
    the post-execution one. A refused append keeps its diagnostic and records
    nothing — the verdict the caller computes never depends on this evidence.
    """
    porcelain = _git(["status", "--porcelain"], root)
    event = {
        "v": EVENT_VERSION,
        "event": RUN_START,
        "run_id": uuid.uuid4().hex,
        "utc": _utc_now(),
        "repository": str(root),
        "common_git_dir": _common_git_dir(root),
        "commit": _git(["rev-parse", "HEAD"], root),
        # None means git could not answer; only an answer decides yes or no.
        "dirty": None if porcelain is None else bool(porcelain),
        "config_sha256": _gate_file_digest(root),
        "job": "verify",
        "placement": "local",
        "memory_pct": verify_lock.read_available_memory(),
        "workers": _worker_setting(),
        **_context_fields(),
        "check_kind": "targeted",
        "change": change,
        "tree_id": tree,
        "comparison_version": COMPARISON_VERSION,
    }
    notes: list[str] = []
    try:
        append_event(event, targeted_history_path())
    except StorageUnusable as unusable:
        notes.append(f"the targeted run was not recorded: {unusable}")
        return TargetedRun(run_id=None, started=monotonic(), notes=notes)
    return TargetedRun(run_id=event["run_id"], started=monotonic(), notes=notes)


def finish_targeted_run(evidence: TargetedRun, tree_after: str | None, outcome: str | None) -> list[str]:
    """Complete the targeted evidence after the checks; an unfinished check records no end.

    `outcome` is "green" or "red" once the checks returned, and None when they
    never returned. The runner reports a timed-out or failed-to-launch check as
    red, so it ends with a red row — never a predecessor; only work interrupted
    before the checks returned stays a start without an end. The end row
    carries the identity captured after execution: a tree that moved during the
    check shows in the reader as a mismatch and the run counts nowhere. A
    refused append keeps its diagnostic and changes no verdict.
    """
    notes = list(evidence.notes)
    if evidence.run_id is None or outcome not in ("green", "red"):
        return notes
    elapsed = monotonic() - evidence.started
    event = {
        "v": EVENT_VERSION,
        "event": RUN_END,
        "run_id": evidence.run_id,
        "utc": _utc_now(),
        "seconds": elapsed if math.isfinite(elapsed) and elapsed >= 0 else 0.0,
        "verdict": outcome,
        "tree_id": tree_after,
    }
    try:
        append_event(event, targeted_history_path())
    except StorageUnusable as unusable:
        notes.append(f"the targeted run's completion was not recorded: {unusable}")
    return notes


def cmd_clock(_args: argparse.Namespace) -> int:
    """One monotonic reading for the shell to carry around a command."""
    print(f"{monotonic():.6f}")
    return 0


def record_start(
    job: str,
    placement: str,
    *,
    root: Path | None = None,
    state_root: Path | None = None,
    env: dict[str, str] | None = None,
) -> str:
    """Create one run identity and append its start record with the machine context.

    `root` binds the machine context to one checkout — the repository, the
    commit and the gate configuration are the caller's, never the importer's
    checkout by accident (bead coding-harness-bxxt.6).
    """
    basis = Path(root) if root is not None else Path.cwd()
    memory = verify_lock.read_available_memory()
    porcelain = _git(["status", "--porcelain"], cwd=basis)
    event = {
        "v": EVENT_VERSION,
        "event": RUN_START,
        "run_id": uuid.uuid4().hex,
        "utc": _utc_now(),
        "repository": str(basis),
        "common_git_dir": _common_git_dir(basis),
        "commit": _git(["rev-parse", "HEAD"], cwd=basis),
        # None means git could not answer; only an answer decides yes or no.
        "dirty": None if porcelain is None else bool(porcelain),
        "config_sha256": _gate_file_digest(basis),
        "job": job,
        "placement": placement,
        "memory_pct": memory,
        "workers": _worker_setting(env),
        **_context_fields(),
        **_comparison_fields(env),
    }
    append_event(event, state_root=state_root)
    if event.get("comparison_version") == COMPARISON_VERSION:
        try:
            os.close(_open_history(targeted_history_path(state_root), state_root=state_root))
        except (StorageUnusable, OSError) as error:
            _log(f"the targeted history could not be created: {error}")
    return str(event["run_id"])


def cmd_start(args: argparse.Namespace) -> int:
    """Create one run identity and append its start record with the machine context."""
    print(record_start(args.job, args.placement))
    return 0


def record_gate(
    run_id: str,
    gate: str,
    start: float,
    end: float,
    status: int,
    enforcement: str,
    *,
    state_root: Path | None = None,
) -> float:
    """Append one gate record and return its measured seconds for the console."""
    seconds = _seconds(start, end)
    event = {
        "v": EVENT_VERSION,
        "event": GATE,
        "run_id": run_id,
        "utc": _utc_now(),
        "gate": gate,
        "seconds": seconds,
        "exit": status,
        "enforcement": enforcement,
    }
    append_event(event, state_root=state_root)
    return seconds


def cmd_gate(args: argparse.Namespace) -> int:
    """Append one gate record and print its measured seconds for the console."""
    seconds = record_gate(args.run, args.gate, args.start, args.end, args.status, args.enforcement)
    print(f"{seconds:.3f}")
    return 0


def _summary_line(seconds: float, context: verify_lock.AdmissionContext) -> str:
    """The execution/wait summary: an explicit unknown or a reused wait, never a fabricated one."""
    wait = "unknown"
    if context.wait_seconds is not None:
        wait = f"{context.wait_seconds:.3f}s"
        if context.reused:
            wait += " (reused from the inherited admission, not re-counted)"
    return f"execution {seconds:.3f}s · admission wait {wait}"


def record_end(
    run_id: str,
    verdict: str,
    *,
    segments: Sequence[tuple[float, float]],
    state_root: Path | None = None,
    context: verify_lock.AdmissionContext | None = None,
    admission_requested: bool | None = None,
    final_commit: str | None = None,
    final_config: str | None = None,
) -> str:
    """Append the run's completion record and return the execution/wait summary line.

    `segments` are the active (start, end) windows of the gates that actually
    executed; their sum is `run_end.seconds`, so the queue and memory waits
    stay outside it. With `admission_requested` the completion carries the
    additive context fields — the reader prefers them when present; without
    it the record keeps the old shape and the caller's environment decides
    the shown wait.
    """
    if verdict not in ("green", "red"):
        raise StorageUnusable(f"invalid verdict {verdict!r}; refusing to record it")
    seconds = sum(_seconds(start, end) for start, end in segments)
    event = {
        "v": EVENT_VERSION,
        "event": RUN_END,
        "run_id": run_id,
        "utc": _utc_now(),
        "seconds": seconds,
        "verdict": verdict,
    }
    if admission_requested is not None:
        final = context if context is not None else verify_lock.AdmissionContext(None, None, None)
        event.update(
            {
                "admission_requested": admission_requested,
                "admission_id": final.admission_id,
                "admission_wait_seconds": final.wait_seconds,
                "admission_reused": final.reused,
                "commit": final_commit,
                "config_sha256": final_config,
            }
        )
    append_event(event, state_root=state_root)
    if admission_requested is False:
        return f"execution {seconds:.3f}s · admission wait none (no admission was requested)"
    return _summary_line(seconds, context if context is not None else verify_lock.admission_context())


def cmd_end(args: argparse.Namespace) -> int:
    """Append the run's completion record and print the execution/wait summary line."""
    if args.no_admission:
        summary = record_end(
            args.run,
            args.verdict,
            segments=[(args.start, args.end)],
            context=verify_lock.AdmissionContext(None, None, None),
            admission_requested=False,
        )
    else:
        summary = record_end(args.run, args.verdict, segments=[(args.start, args.end)])
    print(summary)
    return 0


class _Event(dict):
    """A parsed record retaining its original bytes for duplicate detection."""

    raw: bytes


def _read_events(source: Path | None = None) -> tuple[list[dict], list[str]]:
    """The valid version-1 events in file order, plus one diagnostic per unreadable line.

    A malformed line never stops the read: the valid records before and after
    it are preserved, and each one is named by its line number — a truncated
    final row is an interrupted run, not a crash. `source` names the targeted
    history; the default is the duration history.
    """
    path = source or history_path()
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise StorageUnusable(f"the history file {path} is not an unaliased regular file; refusing history")
            with os.fdopen(fd, "rb", closefd=False) as stream:
                data = stream.read()
        finally:
            os.close(fd)
    except FileNotFoundError:
        raise HistoryMissing(f"no history at {path}; nothing has been recorded yet") from None
    except OSError as error:
        raise StorageUnusable(
            f"the history file {path} cannot be read safely ({error.strerror or error}); refusing history"
        ) from error
    events: list[dict] = []
    findings: list[str] = []
    for number, raw_line in enumerate(data.split(b"\n"), start=1):
        try:
            line = raw_line.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(f"line {number}: not valid UTF-8 — a damaged row stays a diagnosed gap, never a run")
            continue
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError:
            findings.append(f"line {number}: not valid JSON — a truncated row stays a diagnosed gap, never a run")
            continue
        if not isinstance(event, dict) or event.get("event") not in EVENTS or not isinstance(event.get("run_id"), str):
            findings.append(f"line {number}: not a version-1 verify-duration event")
            continue
        if type(event.get("v")) is not int or event["v"] != EVENT_VERSION:
            findings.append(f"line {number}: unsupported event version {event.get('v')!r}; expected {EVENT_VERSION}")
            continue
        record = _Event(event)
        record.raw = raw_line
        events.append(record)
    return events, findings


def _record_error(event: dict) -> str | None:
    """Validate the required fields of each version-1 record, including explicit unknowns."""

    def text(value: object) -> bool:
        return isinstance(value, str) and bool(value.strip())

    def seconds(value: object) -> bool:
        return type(value) in (int, float) and value >= 0 and (not isinstance(value, float) or math.isfinite(value))

    def timestamp(value: object) -> bool:
        if not isinstance(value, str):
            return False
        try:
            parsed = datetime.datetime.fromisoformat(value)
            return parsed.tzinfo is not None and parsed.utcoffset() == datetime.timedelta(0)
        except ValueError:
            return False

    fields = {"run_id": text, "utc": timestamp}
    kind = event["event"]
    if kind == RUN_START:
        fields.update(
            {
                "repository": text,
                "job": text,
                "placement": text,
                "commit": lambda v: v is None or text(v),
                "config_sha256": lambda v: v is None or text(v),
                "dirty": lambda v: v is None or type(v) is bool,
                "workers": lambda v: v is None or text(v),
                "admission_id": lambda v: v is None or text(v),
                "admission_reused": lambda v: v is None or type(v) is bool,
                "admission_wait_seconds": lambda v: v is None or seconds(v),
                "memory_pct": lambda v: v is None or (seconds(v) and v <= 100),
            }
        )
    elif kind == GATE:
        fields.update(
            {
                "gate": text,
                "seconds": seconds,
                "exit": lambda v: type(v) is int,
                "enforcement": lambda v: v in ("block", "advisory", "report"),
            }
        )
    else:
        fields.update({"seconds": seconds, "verdict": lambda v: v in ("green", "red")})
        if "admission_requested" in event:
            # The additive completion context (bead coding-harness-bxxt.6):
            # present or not, never half-present — every field of the block
            # is validated when the marker is there, and unknowns stay null.
            fields.update(
                {
                    "admission_requested": lambda v: type(v) is bool,
                    "admission_id": lambda v: v is None or text(v),
                    "admission_wait_seconds": lambda v: v is None or seconds(v),
                    "admission_reused": lambda v: v is None or type(v) is bool,
                    "commit": lambda v: v is None or text(v),
                    "config_sha256": lambda v: v is None or text(v),
                }
            )
    invalid = [name for name, check in fields.items() if name not in event or not check(event[name])]
    return f"invalid {kind} fields: {', '.join(invalid)}" if invalid else None


def _runs(
    events: list[dict], orphans: list[tuple[int, dict, str]] | None = None
) -> tuple[dict[str, dict], list[str], set[str], int]:
    """Group the events by run identity in file order, with the damaged runs and unassigned rows.

    Identical duplicate starts and ends collapse — one retried append must not
    turn a run into conflicting evidence. A contradictory start or end, and any
    record with invalid fields, damage their run: its evidence counts nowhere,
    and the reader shows it as not countable instead of guessing. Returns the
    runs in file order, one finding per diagnosed row, the damaged run
    identities, and the number of rows that name no start at all. With an
    `orphans` list, a row without a start goes there as (position, row,
    finding) instead of into the findings: the slip reader classifies it by
    its position against the first version-2 marker.
    """
    runs: dict[str, dict] = {}
    findings: list[str] = []
    order: list[str] = []
    damaged: set[str] = set()
    unassigned = 0
    for position, event in enumerate(events):
        run_id = event["run_id"]
        kind = event["event"]
        error = _record_error(event)
        if error:
            findings.append(f"{error} for run {run_id}")
            damaged.add(run_id)
        if kind == RUN_START:
            if run_id in runs:
                if (
                    getattr(runs[run_id]["start"], "raw", None) == getattr(event, "raw", None)
                    and runs[run_id]["start"] == event
                ):
                    continue  # an identical duplicate is a retried append, not a conflict
                runs[run_id]["starts"].append(event)
                findings.append(f"a second start for run {run_id}")
                damaged.add(run_id)
                continue
            runs[run_id] = {"start": event, "starts": [event], "gates": [], "end": None, "ends": []}
            order.append(run_id)
        elif run_id not in runs:
            unassigned += 1
            finding = f"line with {kind} for unknown run {run_id} — its start row is missing or malformed"
            if orphans is None:
                findings.append(finding)
            else:
                orphans.append((position, event, finding))
        elif error:
            continue
        elif kind == GATE:
            runs[run_id]["gates"].append(event)
        elif runs[run_id]["end"] is None:
            runs[run_id]["end"] = event
            runs[run_id]["ends"].append(event)
        elif getattr(runs[run_id]["end"], "raw", None) == getattr(event, "raw", None) and runs[run_id]["end"] == event:
            continue  # an identical duplicate is a retried append, not a conflict
        else:
            runs[run_id]["ends"].append(event)
            findings.append(f"a second end for run {run_id}")
            damaged.add(run_id)
    for run_id in damaged:
        if run_id in runs:
            runs[run_id]["end"] = None
    return {run_id: runs[run_id] for run_id in order}, findings, damaged, unassigned


def _verdict_of(run: dict) -> str:
    """A run's verdict; no valid end means incomplete, never a successful complete run."""
    end = run["end"]
    if end is None:
        return "incomplete (no completion recorded)"
    return _shown(end.get("verdict"), "unknown verdict")


def _fmt_seconds(value: object, unknown: str = "unknown") -> str:
    """A duration for the console; a row without a number shows its unknown, never a crash."""
    if isinstance(value, bool) or not isinstance(value, int | float) or not math.isfinite(value):
        return unknown
    return f"{value:.3f}s"


def cmd_report(args: argparse.Namespace) -> int:
    """The reader: run summaries, or one run's full detail with `--run`."""
    events, findings = _read_events()
    runs, grouping, _damaged, _unassigned = _runs(events)
    findings.extend(grouping)
    if args.run is not None:
        run = runs.get(args.run)
        if run is None:
            _log(f"run {args.run} is not in the history (malformed rows keep their gaps visible)")
            return 1
        print(_detail(run))
    else:
        if not runs:
            print("the history holds no run")
        for run_id, run in runs.items():
            start = run["start"]
            execution = run["end"].get("seconds") if run["end"] is not None else None
            print(
                f"run {run_id} · {start.get('utc')} · job {start.get('job')} · placement {start.get('placement')}"
                f" · verdict {_verdict_of(run)} · execution {_fmt_seconds(execution)}"
                f" · {len(run['gates'])} gates"
            )
    for finding in findings:
        print(f"history note: {finding}")
    return 1 if grouping else 0


def _shown(value: object, unknown: str = "unknown") -> str:
    """A record field for the console, with its explicit unknown kept unknown."""
    if value is None:
        return unknown
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value)


def _detail(run: dict) -> str:
    """One run's machine context, per-gate durations and outcome, as the reader shows it.

    A completion that carries the additive context fields speaks for the
    whole run: its admission line shows the final context, a cheap-only run
    states that no admission was requested, and the final revision and
    configuration line appears after a changed tree made the queued wait
    move the run. An old start-only record reads exactly as before.
    """
    start = run["start"]
    end = run["end"]
    lines = [
        f"run {start['run_id']}",
        f"  started (UTC): {_shown(start.get('utc'))}",
        f"  repository: {_shown(start.get('repository'))} · commit: {_shown(start.get('commit'))}"
        f" · dirty: {_shown(start.get('dirty'))}",
        f"  gate configuration (sha256): {_shown(start.get('config_sha256'))}",
        f"  job: {_shown(start.get('job'))} · placement: {_shown(start.get('placement'))}",
        f"  free memory at start: {_shown(start.get('memory_pct'))}",
        f"  workers: {_shown(start.get('workers'), 'unset (xdist decides)')}",
    ]
    if end is not None and "admission_requested" in end:
        if end.get("admission_requested") is False:
            lines.append("  admission: none (no admission was requested)")
        else:
            lines.append(
                f"  admission (final): {_shown(end.get('admission_id'))} · wait:"
                f" {_shown(end.get('admission_wait_seconds'))} · reused: {_shown(end.get('admission_reused'))}"
            )
        if end.get("commit") is not None or end.get("config_sha256") is not None:
            lines.append(
                f"  final revision: {_shown(end.get('commit'))}"
                f" · final gate configuration (sha256): {_shown(end.get('config_sha256'))}"
            )
    else:
        lines.append(
            f"  admission: {_shown(start.get('admission_id'))} · wait:"
            f" {_shown(start.get('admission_wait_seconds'))} · reused: {_shown(start.get('admission_reused'))}"
        )
    lines.append("  gates:")
    for gate in run["gates"]:
        lines.append(
            f"    {gate.get('gate')}  {_fmt_seconds(gate.get('seconds'))}  exit {gate.get('exit')}"
            f"  {gate.get('enforcement')}"
        )
    if run["end"] is None:
        lines.append("  execution: unknown · verdict: incomplete (no completion recorded)")
    else:
        lines.append(f"  execution: {_fmt_seconds(run['end'].get('seconds'))} · verdict: {_verdict_of(run)}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Slips — derived observations, never persisted (bead coding-harness-bxxt.7)
# ---------------------------------------------------------------------------


def _aware_utc(text: str) -> datetime.datetime:
    """One interval bound: timezone-aware, normalized to UTC; anything else refuses."""
    try:
        parsed = datetime.datetime.fromisoformat(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{text!r} is not an ISO 8601 instant") from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise argparse.ArgumentTypeError(f"{text!r} carries no timezone; give an offset like +00:00")
    return parsed.astimezone(datetime.UTC)


def _instant(value: object) -> datetime.datetime | None:
    """A record's UTC instant, or None when the field cannot be trusted as time."""
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(datetime.UTC)
    except (ValueError, OverflowError):
        return None


def _text(value: object) -> str | None:
    """A recorded identity field, or None when it is absent, blank or not text."""
    return value.strip() if isinstance(value, str) and value.strip() else None


@dataclass
class _Check:
    """One check taking part in the pairing: a run of a known kind, or an orphan completion.

    `certain` means valid, unambiguous evidence: a complete run whose
    repository, change, checked tree(s) and gate configuration are all known,
    whose completion does not precede its start and whose recorded trees agree.
    Targeted checks require both tree readings. Anything else is uncertain and counts
    as incomplete once. `completion` is None while no valid completion exists.
    """

    run_id: str
    kind: str  # "targeted" or "full"
    start: datetime.datetime
    completion: datetime.datetime | None
    verdict: str | None
    change: str | None
    trees: frozenset[str]  # every checked tree the run may stand for
    config: str | None
    selected: bool
    certain: bool
    outside: bool = False


@dataclass
class _Tally:
    """What the collection of one report found besides the pairing checks."""

    checks: list[_Check] = field(default_factory=list)
    selected: int = 0  # runs the scope selects; none at all leaves nothing observed
    outside: int = 0  # attributable legacy or change-less full runs
    unattributed: int = 0  # recognizable legacy runs without enough scope evidence
    partial: bool = False
    findings: list[str] = field(default_factory=list)


def _compatible(first: _Check, second: _Check) -> bool:
    """Whether the known identity fields of two checks do not conflict.

    An unknown field never proves a match and never rules one out; two known,
    different values rule it out. A moved check matches either tree.
    """
    if first.change and second.change and first.change != second.change:
        return False
    if first.config and second.config and first.config != second.config:
        return False
    return not (first.trees and second.trees and not (first.trees & second.trees))


def _may_precede(other: _Check, full: _Check) -> bool:
    """Whether an uncertain check could have completed before the full run's completion."""
    assert full.completion is not None
    if other.completion is not None:
        return other.completion <= full.completion
    return other.start < full.completion


def _may_follow(other: _Check, earlier: _Check) -> bool:
    """Whether an uncertain check could have completed after an earlier check's completion."""
    assert earlier.completion is not None
    return other.completion is None or other.completion >= earlier.completion


def _collect(
    runs: dict[str, dict], damaged: set[str], args: argparse.Namespace, current_repository: str | None
) -> _Tally:
    """Classify every run of the history: pairing check, outside the count, or a diagnosed gap."""
    tally = _Tally()
    since, until = args.since, args.until
    for run_id, run in runs.items():
        start = run["start"]
        moment = _instant(start.get("utc"))
        repository = start.get("common_git_dir")
        job = start.get("job")
        placement = start.get("placement")
        legacy = "check_kind" not in start  # no comparison evidence: a recognizable legacy duration record
        located = (
            moment is not None
            and _text(job) is not None
            and _text(placement) is not None
            and _text(repository) is not None
        )
        if not located:
            if legacy and run_id not in damaged and moment is not None:
                if (since is None or moment >= since) and (until is None or moment < until):
                    tally.unattributed += 1  # its repository cannot be assigned
            else:
                # Damaged or unassignable evidence: the measurement stays
                # partial and no run is invented for it.
                tally.partial = True
                if run_id not in damaged:
                    missing = [
                        name
                        for name, value in (
                            ("start time", moment),
                            ("repository", _text(repository)),
                            ("job", _text(job)),
                            ("placement", _text(placement)),
                        )
                        if value is None
                    ]
                    tally.findings.append(f"run {run_id} cannot be assigned: missing or invalid {', '.join(missing)}")
            continue
        if job != "verify" or placement != "local" or repository != current_repository:
            continue  # complete unrelated jobs, placements and repositories are ignored
        assert moment is not None
        change = _text(start.get("change"))
        in_bounds = (since is None or moment >= since) and (until is None or moment < until)
        named = args.change is None or change == args.change
        end = run["end"]
        completion = _instant(end.get("utc")) if end is not None and run_id not in damaged else None
        valid_end = completion is not None and completion >= moment
        kind = start.get("check_kind")
        outside = legacy or (kind == "full" and change is None)
        selected = in_bounds and named
        if in_bounds and args.change is not None and change is None and not outside:
            tally.partial = True
            tally.findings.append(f"run {run_id} cannot be assigned: missing or invalid change")
        if outside:
            if in_bounds and run_id not in damaged:
                if args.change is None:
                    tally.selected += 1
                tally.outside += 1
            # Outside runs still may interrupt a pair, but never count as incomplete.
            selected = False
        elif selected:
            tally.selected += 1
        tree_start = _text(start.get("tree_id"))
        tree_end = _text(end.get("tree_id")) if end is not None and run_id not in damaged else None
        config = _text(start.get("config_sha256"))
        trees = {tree_start, tree_end, *(_text(row.get("tree_id")) for row in [*run["starts"], *run["ends"]])}
        if any(row.get("check_kind") != kind for row in run["starts"]):
            kind = None
        if any(row.get("change") != start.get("change") for row in run["starts"]):
            change = None
        if any(row.get("config_sha256") != start.get("config_sha256") for row in run["starts"]):
            config = None
        moments = [_instant(row.get("utc")) for row in run["starts"]]
        moment = min((value for value in moments if value is not None), default=moment)
        certain = not outside and kind in CHECK_KINDS and valid_end and bool(change and tree_start and config)
        if kind == "targeted":
            certain = certain and tree_end == tree_start  # both readings must exist and agree
        elif tree_end is not None:
            certain = certain and tree_end == tree_start
        verdict = end.get("verdict") if valid_end and end is not None else None
        tally.checks.append(
            _Check(
                run_id=run_id,
                kind=kind if kind in CHECK_KINDS else "unknown",
                start=moment,
                completion=completion if valid_end else None,
                verdict=verdict,
                change=change,
                trees=frozenset(tree for tree in trees if tree),
                config=config,
                selected=selected,
                certain=certain,
                outside=outside,
            )
        )
    return tally


def _when(check: _Check) -> datetime.datetime:
    """A check's completion, or its start while it has no valid completion."""
    return check.completion or check.start


def _targeted_green(check: _Check) -> bool:
    return check.kind == "targeted" and check.verdict == "green"


def _full_green(check: _Check) -> bool:
    return check.kind == "full" and check.verdict == "green"


def _between(other: _Check, full: _Check, predecessor: _Check | None) -> bool:
    """Whether an uncertain check could stand between a full run and its certain predecessor."""
    if not _compatible(other, full) or not _may_precede(other, full):
        return False
    return predecessor is None or _may_follow(other, predecessor)


def _tie_uncertain(checks: list[_Check]) -> None:
    """Equal completions of compatible, different checks cannot order them: both become uncertain."""
    timed = [check for check in checks if check.completion is not None]
    for index, first in enumerate(timed):
        for second in timed[index + 1 :]:
            if first.completion != second.completion:
                continue
            if _compatible(first, second):
                first.certain = False
                second.certain = False


def _pair(checks: list[_Check], orphans: list[_Check]) -> tuple[int, int, int, set[str]]:
    """Slips, flaky-test signals, undecided signals and the runs promoted to incomplete.

    Checks are ordered by UTC completion with strict earlier-than; equal
    completions of compatible checks cannot establish an order and make both
    uncertain. A complete red full run pairs only with its immediate certain
    predecessor of the same identity. An uncertain check that could stand
    between them — or that could itself be that predecessor or successor —
    leaves the pair undecidable: each selected side counts as incomplete once,
    and no arbitrary pair is chosen. Where only uncertain full runs may
    intervene and no targeted check could be the predecessor, the later full
    run keeps its non-slip status and its flaky-test signal stays undecided.
    """
    _tie_uncertain(checks)
    certain = [check for check in checks if check.certain]
    uncertain = [check for check in checks if not check.certain]
    pool = [*uncertain, *orphans]
    promoted: set[str] = set()
    slips = flaky = undecided = 0
    reds = [check for check in certain if check.kind == "full" and check.verdict == "red"]
    for full in sorted(reds, key=_when):
        earlier = [check for check in certain if check is not full and _compatible(check, full)]
        earlier = [check for check in earlier if _when(check) < _when(full)]
        predecessor = max(earlier, key=_when, default=None)
        between = [check for check in pool if _between(check, full, predecessor)]
        green = predecessor is not None and _targeted_green(predecessor)
        if not between:
            if full.selected and green:
                slips += 1
            elif full.selected and predecessor is not None and _full_green(predecessor):
                flaky += 1
            continue
        if (
            green
            or any(check.kind == "targeted" and not check.outside for check in between)
            or (
                predecessor is not None
                and _full_green(predecessor)
                and any(
                    _targeted_green(candidate)
                    and _compatible(candidate, uncertain_full)
                    and _compatible(candidate, full)
                    and _may_precede(candidate, full)
                    and (uncertain_full.completion is None or _may_precede(candidate, uncertain_full))
                    for candidate in checks
                    for uncertain_full in between
                    if uncertain_full.kind == "full"
                )
            )
            or (predecessor is not None and any(check.kind == "unknown" for check in between))
        ):
            promoted.add(full.run_id)
            promoted.update(check.run_id for check in between)
            if predecessor is not None and not (predecessor.kind == "full" and predecessor.verdict == "red"):
                promoted.add(predecessor.run_id)
        elif full.selected:
            undecided += 1  # the intervening full run may have been green: the signal stays undecided
    for unsure in uncertain:
        if unsure.kind != "full" or unsure.outside:
            continue
        # An uncertain full run could be the red successor of the latest certain check before it.
        before = [check for check in certain if _compatible(check, unsure)]
        if unsure.completion is not None:
            before = [check for check in before if _when(check) < unsure.completion]
        latest = max(before, key=_when, default=None)
        if (
            latest is not None
            and (_targeted_green(latest) or _full_green(latest))
            and any(
                other is not unsure and _compatible(other, unsure) and _between(other, unsure, latest)
                for other in pool
                if unsure.completion is not None
            )
            or latest is not None
            and _targeted_green(latest)
        ):
            promoted.add(latest.run_id)
    return slips, flaky, undecided, promoted


def cmd_slips(args: argparse.Namespace) -> int:
    """The read-only slip count beside the runs that could not be counted.

    The asked interval and change scope select what is counted; the search for
    a predecessor runs over the whole available history, including before the
    interval's lower bound. Exit 0: complete readable evidence, even when the
    slip count is positive. Exit 1: partial or unavailable evidence — usable
    counts are kept when they can stand, and missing history is unavailable,
    never a zero; a selection without any run (a misspelled change, another
    checkout, an empty window) is no statement, never a zero either. Exit 2:
    an invalid interval. Reading never appends, repairs or creates history.
    """
    since, until = args.since, args.until
    if since is not None and until is not None and since >= until:
        _log(f"the interval {since.isoformat()}..{until.isoformat()} is reversed; refusing it")
        return 2
    unavailable = "slips: unavailable; incomplete/not countable runs: unavailable"
    try:
        events, findings = _read_events()
    except HistoryMissing as missing:
        print(unavailable)
        _log(f"{missing} — missing history is unavailable, never a counted zero")
        return 1
    marker: int | None = None  # the position of the first version-2 comparison start
    for position, event in enumerate(events):
        if event["event"] == RUN_START and event.get("comparison_version") == COMPARISON_VERSION:
            marker = position
            break
    try:
        targeted_events, targeted_findings = _read_events(targeted_history_path())
    except HistoryMissing as missing:
        if marker is not None:
            print(unavailable)
            _log(f"{missing} — version-2 evidence exists; a missing targeted history is unavailable")
            return 1
        targeted_events, targeted_findings = [], []
    duration_orphans: list[tuple[int, dict, str]] = []
    targeted_orphans: list[tuple[int, dict, str]] = []
    runs, grouping, damaged, _ = _runs(events, duration_orphans)
    targeted_runs, targeted_grouping, targeted_damaged, _ = _runs(targeted_events, targeted_orphans)
    runs.update(targeted_runs)
    damaged |= targeted_damaged
    targeted_notes = [f"targeted history: {note}" for note in [*targeted_findings, *targeted_grouping]]
    findings = [*findings, *grouping, *targeted_notes]

    current_repository = _common_git_dir()
    tally = _collect(runs, damaged, args, current_repository)
    tally.findings = findings + tally.findings
    orphan_checks: list[_Check] = []
    for source, orphans in (("duration", duration_orphans), ("targeted", targeted_orphans)):
        for position, event, finding in orphans:
            if source == "duration" and (marker is None or position < marker):
                completion = _instant(event.get("utc"))
                if (
                    event["event"] == RUN_END
                    and completion is not None
                    and (since is None or completion >= since)
                    and (until is None or completion < until)
                ):
                    tally.unattributed += 1  # a legacy start lost before any marker: outside the count
                continue
            completion = _instant(event.get("utc"))
            # An end that completed before the lower bound cannot belong to this
            # selection, whatever repository it came from; one without a usable
            # timestamp belongs to every selection.
            if completion is None or since is None or completion >= since:
                tally.partial = True
                tally.findings.append(finding)
            if completion is not None and event["event"] == RUN_END:
                orphan_checks.append(
                    _Check(
                        run_id=f"orphan:{source}:{position}",
                        kind="full" if source == "duration" else "targeted",
                        start=completion,
                        completion=completion,
                        verdict=None,
                        change=None,
                        trees=frozenset(),
                        config=None,
                        selected=False,
                        certain=False,
                    )
                )

    slips, flaky, undecided, promoted = _pair(tally.checks, orphan_checks)
    pending = [check for check in tally.checks if check.selected]
    gaps = sum(1 for check in pending if not check.certain or check.run_id in promoted)
    uncountable = gaps

    scope = f"change {args.change}" if args.change is not None else "change all"
    lower = since.isoformat() if since is not None else "none"
    upper = until.isoformat() if until is not None else "none"
    print(f"repository {current_repository or 'unavailable'} · {scope} · since {lower} · until {upper}")
    outside_label = " (not change-scoped)" if args.change is not None else ""
    if not tally.selected:
        # Nothing of this scope was measured: an observed absence needs runs.
        print("0 runs selected, no statement possible")
        if tally.outside or tally.unattributed:
            print(
                f"outside the count: {tally.outside} legacy or change-less full runs{outside_label}; "
                f"unattributed outside runs: {tally.unattributed}"
            )
        for finding in tally.findings:
            print(f"history note: {finding}")
        return 1
    print(f"slips: {slips}; incomplete/not countable runs: {uncountable}")
    for check in pending:
        if not check.certain or check.run_id in promoted:
            print(
                f"incomplete run: {check.run_id} · {check.start.isoformat()} · change {check.change or 'unknown'} · kind {check.kind}"
            )
    if flaky or undecided:
        print(f"flaky-test signals: {flaky}; undecided flaky-test signals: {undecided}")
    if tally.outside or tally.unattributed:
        print(
            f"outside the count: {tally.outside} legacy or change-less full runs{outside_label}; "
            f"unattributed outside runs: {tally.unattributed}"
        )
    for finding in tally.findings:
        print(f"history note: {finding}")
    if tally.partial or tally.findings or uncountable:
        print("evidence partial — the runs beside the count name what could not be counted")
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Measured verification durations, recorded locally only.")
    operations = parser.add_subparsers(dest="operation", required=True)

    clock = operations.add_parser("clock", help="print one monotonic reading")
    clock.set_defaults(handler=cmd_clock)

    start = operations.add_parser("start", help="create one run identity and record the machine context")
    start.add_argument("--job", default="verify", help="the selected job of this run")
    start.add_argument("--placement", default="local", help="the placement of this run (local|ci)")
    start.set_defaults(handler=cmd_start)

    gate = operations.add_parser("gate", help="record one executed gate's duration and raw result")
    gate.add_argument("--run", required=True, help="the run identity of this run")
    gate.add_argument("--gate", required=True, help="the gate id as the one list names it")
    gate.add_argument("--start", required=True, help="the monotonic reading taken before the gate command")
    gate.add_argument("--end", required=True, help="the monotonic reading taken after the gate command")
    gate.add_argument("--status", required=True, type=int, help="the gate command's raw exit status")
    gate.add_argument("--enforcement", required=True, help="the gate's enforcement (block|advisory|report)")
    gate.set_defaults(handler=cmd_gate)

    end = operations.add_parser("end", help="record the run's execution seconds and final verdict")
    end.add_argument("--run", required=True, help="the run identity of this run")
    end.add_argument("--start", required=True, help="the monotonic reading taken before the report")
    end.add_argument("--end", required=True, help="the monotonic reading taken at the final verdict")
    end.add_argument("--verdict", required=True, choices=("green", "red"), help="the run's final verdict")
    end.add_argument(
        "--no-admission",
        action="store_true",
        help="record the completion context of a run that never requested admission",
    )
    end.set_defaults(handler=cmd_end)

    report = operations.add_parser("report", help="list recorded runs, or show one with --run")
    report.add_argument("--run", help="show this run's machine context and per-gate durations")
    report.set_defaults(handler=cmd_report)

    slips = operations.add_parser(
        "slips",
        help="count slips beside the runs that could not be counted; read-only",
        description="Derived slip observations of the local history; nothing is ever written.",
    )
    slips.add_argument("--since", type=_aware_utc, help="inclusive UTC lower bound (ISO 8601 with offset)")
    slips.add_argument("--until", type=_aware_utc, help="exclusive UTC upper bound (ISO 8601 with offset)")
    slips.add_argument("--change", help="count only this change's runs")
    slips.set_defaults(handler=cmd_slips)

    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except StorageUnusable as unusable:
        _log(str(unusable))
        return 2
    except HistoryMissing as missing:
        _log(str(missing))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
