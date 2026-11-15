#!/usr/bin/env python3
"""verify_duration.py — measured verification durations, recorded locally only.

`scripts.verify_all.sh` calls the small operations of this module around the
gates it already ran: one `clock` reading immediately before and after each
gate command and around the whole run, `start` before the report and gate
selection, `gate` per executed gate, `end` at the final verdict. Each write
appends one version-1 JSON line to `verify-duration.jsonl` under
`verify_lock.state_root()` — the same shared state root the admission keeps,
outside the repository, local only: no command output, no credentials, no
upload (bead coding-harness-1um6, spec "Non-goals").

**Time.** Elapsed seconds are differences of `time.monotonic()`, so a wall
clock adjustment cannot produce negative or inflated durations, and an
inherited admission's wait is recorded as the shared context it is — never
added into execution seconds. Unavailable readings are recorded as JSON null,
never as zero by assumption (spec, "Terms").

**Interruption.** A killed run can leave a start without an end; the reader
labels such a run incomplete instead of inventing a verdict. A truncated
final line is diagnosed, and the valid records before it are preserved — the
reader never repairs or truncates history.

**Refusals.** A history destination that is a symlink or not a regular file,
or a state root that cannot be created, refuses the write with a diagnostic
on stderr and exit code 2, without writing through the substituted file. The
caller (`verify_all.sh`) reports the missing history and lets the gates and
their verdicts continue unchanged; such a run cannot supply a persisted
baseline (spec acceptance criterion 7).

Command line:

    python -m scripts.verify_duration clock
    python -m scripts.verify_duration start --job verify --placement local
    python -m scripts.verify_duration gate --run ID --gate GID \
            --start T0 --end T1 --status N --enforcement block
    python -m scripts.verify_duration end --run ID --start T0 --end T1 --verdict green
    python -m scripts.verify_duration report [--run ID]
    python -m scripts.verify_duration slips [--since UTC] [--until UTC] [--change NAME]

**Slips.** A slip is a completed red local full verification run that an earlier
completed green targeted check of the same repository, change, checked tree and
gate configuration failed to catch (bead coding-harness-bxxt.7). Nothing about a
slip is ever written: the `slips` reader derives the count from the run records
the runner already leaves — targeted checks record ordinary run evidence through
`begin_targeted_run`/`finish_targeted_run`, full checks carry their comparison
context in runner-owned environment variables that `cmd_start` captures. The
count stands beside the number of incomplete or not countable runs, never
alone: lost or conflicting evidence is a gap, not a zero (decisions Q-1, Q-2).
Reading never appends, repairs or creates history.
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
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_lock  # noqa: E402

HISTORY_NAME = "verify-duration.jsonl"
EVENT_VERSION = 1
RUN_START = "run_start"
GATE = "gate"
RUN_END = "run_end"
EVENTS = (RUN_START, GATE, RUN_END)
GATE_FILE = Path("decisions") / "gates.yaml"
GIT_TIMEOUT_SECONDS = 10.0
# The check kinds a start record can name. `targeted` is written only by
# `begin_targeted_run`, never from the environment: no launcher can mint a
# targeted predecessor by exporting a variable.
CHECK_KINDS = ("targeted", "full", "full-fallback")
# The runner-owned variables of one full launch (full_run_context, full_verify).
# Absent means a legacy record; present-but-empty means the explicit unknown.
KIND_ENV = "HARNESS_VERIFY_DURATION_KIND"
CHANGE_ENV = "HARNESS_VERIFY_DURATION_CHANGE"
TREE_ENV = "HARNESS_VERIFY_DURATION_TREE"


class StorageUnusable(Exception):
    """Measurement storage cannot be used safely; the caller reports and continues."""


class HistoryMissing(Exception):
    """The reader found no history file where one would be recorded."""


def history_path() -> Path:
    """The one history file under the shared verification state root."""
    return verify_lock.state_root() / HISTORY_NAME


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
            ["git", *arguments], cwd=cwd, capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if done.returncode != 0:
        return None
    return done.stdout.strip()


def _gate_file_digest(root: Path | None = None) -> str | None:
    """The SHA-256 of the one gate file this run measured, or None when absent."""
    try:
        return hashlib.sha256(((root or Path.cwd()) / GATE_FILE).read_bytes()).hexdigest()
    except OSError:
        return None


def _worker_setting() -> str | None:
    """The effective worker setting passed to the gates; unset means xdist decides."""
    value = os.environ.get("PYTEST_XDIST_AUTO_NUM_WORKERS", "")
    return value if value else None


def _open_history() -> int:
    """A private regular history file for appending; an aliased or nonregular destination refuses.

    The same shape as the admission's lock files: the no-follow open fails on
    a symlink standing in the file's place, a FIFO cannot pass the regular
    check, and nothing is ever written through a substituted destination.
    """
    root = verify_lock.state_root()
    try:
        root.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise StorageUnusable(
            f"the shared state directory {root} cannot be created ({error.strerror or error})"
        ) from error
    if root.is_symlink() or not root.is_dir():
        raise StorageUnusable(f"the shared state directory {root} is not a usable directory")
    path = history_path()
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


def append_event(event: dict) -> None:
    """Append one complete JSON line under a file lock, so concurrent runs never mix identities."""
    line = json.dumps(event, sort_keys=True) + "\n"
    fd = _open_history()
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


def _comparison_fields() -> dict:
    """The comparison context of a full run, when its launcher supplied one.

    Only the runner's own full checks carry these variables (`full_verify` hands
    them to the one `make verify` it starts); a start without them stays a
    legacy duration record. Empty values become the explicit unknown. A kind
    outside the known ones becomes the unknown too, never `targeted`: the
    environment must not be able to mint a targeted predecessor, and a fallback
    stays a full run.
    """
    if KIND_ENV not in os.environ:
        return {}
    kind = os.environ.get(KIND_ENV, "").strip()
    return {
        "check_kind": kind if kind in CHECK_KINDS else None,
        "change": os.environ.get(CHANGE_ENV, "").strip() or None,
        "tree_id": os.environ.get(TREE_ENV, "").strip() or None,
    }


def full_run_context(tree: str | None, change: str | None) -> dict[str, str]:
    """The runner-owned environment of one full `make verify` launch, for `cmd_start` to capture.

    The launcher (`full_verify`) adds these to that one child's environment and
    never to its own; ambient variables of the same names cannot leak in, since
    the runner's allow-list already stripped them. Empty means the explicit
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
    tree: str | None  # the identity captured before the checks ran
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
    }
    notes: list[str] = []
    try:
        append_event(event)
    except StorageUnusable as unusable:
        notes.append(f"the targeted run was not recorded: {unusable}")
        return TargetedRun(run_id=None, tree=tree, started=monotonic(), notes=notes)
    return TargetedRun(run_id=event["run_id"], tree=tree, started=monotonic(), notes=notes)


def finish_targeted_run(evidence: TargetedRun, tree_after: str | None, outcome: str | None) -> list[str]:
    """Complete the targeted evidence after the checks; an unfinished check records no end.

    `outcome` is "green" or "red" once the checks returned, and None when they
    never completed — interrupted, timed-out or failed-to-start work stays a
    start without an end, so no green completion of it can exist. The end row
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
        append_event(event)
    except StorageUnusable as unusable:
        notes.append(f"the targeted run's completion was not recorded: {unusable}")
    return notes


def cmd_clock(_args: argparse.Namespace) -> int:
    """One monotonic reading for the shell to carry around a command."""
    print(f"{monotonic():.6f}")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    """Create one run identity and append its start record with the machine context."""
    memory = verify_lock.read_available_memory()
    porcelain = _git(["status", "--porcelain"])
    event = {
        "v": EVENT_VERSION,
        "event": RUN_START,
        "run_id": uuid.uuid4().hex,
        "utc": _utc_now(),
        "repository": str(Path.cwd()),
        "commit": _git(["rev-parse", "HEAD"]),
        # None means git could not answer; only an answer decides yes or no.
        "dirty": None if porcelain is None else bool(porcelain),
        "config_sha256": _gate_file_digest(),
        "job": args.job,
        "placement": args.placement,
        "memory_pct": memory,
        "workers": _worker_setting(),
        **_context_fields(),
        **_comparison_fields(),
    }
    append_event(event)
    print(event["run_id"])
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    """Append one gate record and print its measured seconds for the console."""
    seconds = _seconds(args.start, args.end)
    event = {
        "v": EVENT_VERSION,
        "event": GATE,
        "run_id": args.run,
        "utc": _utc_now(),
        "gate": args.gate,
        "seconds": seconds,
        "exit": args.status,
        "enforcement": args.enforcement,
    }
    append_event(event)
    print(f"{seconds:.3f}")
    return 0


def cmd_end(args: argparse.Namespace) -> int:
    """Append the run's completion record and print the execution/wait summary line."""
    seconds = _seconds(args.start, args.end)
    event = {
        "v": EVENT_VERSION,
        "event": RUN_END,
        "run_id": args.run,
        "utc": _utc_now(),
        "seconds": seconds,
        "verdict": args.verdict,
    }
    append_event(event)
    context = verify_lock.admission_context()
    wait = "unknown"
    if context.wait_seconds is not None:
        wait = f"{context.wait_seconds:.3f}s"
        if context.reused:
            wait += " (reused from the inherited admission, not re-counted)"
    print(f"execution {seconds:.3f}s · admission wait {wait}")
    return 0


def _read_events() -> tuple[list[dict], list[str]]:
    """The valid version-1 events in file order, plus one diagnostic per unreadable line.

    A malformed line never stops the read: the valid records before and after
    it are preserved, and each one is named by its line number — a truncated
    final row is an interrupted run, not a crash.
    """
    path = history_path()
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise StorageUnusable(f"the history file {path} is not an unaliased regular file; refusing history")
            with os.fdopen(fd, encoding="utf-8", closefd=False) as stream:
                text = stream.read()
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
    for number, line in enumerate(text.split("\n"), start=1):
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
        events.append(event)
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
    invalid = [name for name, check in fields.items() if name not in event or not check(event[name])]
    return f"invalid {kind} fields: {', '.join(invalid)}" if invalid else None


def _runs(events: list[dict]) -> tuple[dict[str, dict], list[str], set[str], int]:
    """Group the events by run identity in file order, with the damaged runs and unassigned rows.

    Identical duplicate starts and ends collapse — one retried append must not
    turn a run into conflicting evidence. A contradictory start or end, and any
    record with invalid fields, damage their run: its evidence counts nowhere,
    and the reader shows it as not countable instead of guessing. Returns the
    runs in file order, one finding per diagnosed row, the damaged run
    identities, and the number of rows that name no start at all.
    """
    runs: dict[str, dict] = {}
    findings: list[str] = []
    order: list[str] = []
    damaged: set[str] = set()
    unassigned = 0
    for event in events:
        run_id = event["run_id"]
        kind = event["event"]
        error = _record_error(event)
        if error:
            findings.append(f"{error} for run {run_id}")
            damaged.add(run_id)
        if kind == RUN_START:
            if run_id in runs:
                if runs[run_id]["start"] == event:
                    continue  # an identical duplicate is a retried append, not a conflict
                findings.append(f"a second start for run {run_id}")
                damaged.add(run_id)
                continue
            runs[run_id] = {"start": event, "gates": [], "end": None}
            order.append(run_id)
        elif run_id not in runs:
            unassigned += 1
            findings.append(f"line with {kind} for unknown run {run_id} — its start row is missing or malformed")
        elif error:
            continue
        elif kind == GATE:
            runs[run_id]["gates"].append(event)
        elif runs[run_id]["end"] is None:
            runs[run_id]["end"] = event
        elif runs[run_id]["end"] == event:
            continue  # an identical duplicate is a retried append, not a conflict
        else:
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
    """One run's machine context, per-gate durations and outcome, as the reader shows it."""
    start = run["start"]
    lines = [
        f"run {start['run_id']}",
        f"  started (UTC): {_shown(start.get('utc'))}",
        f"  repository: {_shown(start.get('repository'))} · commit: {_shown(start.get('commit'))}"
        f" · dirty: {_shown(start.get('dirty'))}",
        f"  gate configuration (sha256): {_shown(start.get('config_sha256'))}",
        f"  job: {_shown(start.get('job'))} · placement: {_shown(start.get('placement'))}",
        f"  free memory at start: {_shown(start.get('memory_pct'))}",
        f"  workers: {_shown(start.get('workers'), 'unset (xdist decides)')}",
        f"  admission: {_shown(start.get('admission_id'))} · wait:"
        f" {_shown(start.get('admission_wait_seconds'))} · reused: {_shown(start.get('admission_reused'))}",
        "  gates:",
    ]
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
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(datetime.UTC)


def _same_repository(recorded: str) -> bool:
    """Whether a record's repository is the resolved repository the reader runs in."""
    try:
        return os.path.realpath(recorded) == os.path.realpath(str(Path.cwd()))
    except OSError:
        return False


def _slip_predecessor_match(
    predecessors: list[tuple[datetime.datetime, str, str | None, str, str | None]],
    moment: datetime.datetime,
    repository: str,
    change: str | None,
    tree: str,
    config: str | None,
) -> bool:
    """Whether one completed green targeted check of the same identity finished before `moment`.

    Repository, change, checked tree and gate configuration must all be present
    and equal — a missing field never matches another missing field — and the
    completion must precede the full run's start, so overlapping checks do not
    pair. Several qualifying predecessors still count the full run once.
    """
    for completion, place, named, content, basis in predecessors:
        if completion < moment and place == repository and named == change and content == tree and basis == config:
            return True
    return False


def cmd_slips(args: argparse.Namespace) -> int:
    """The read-only slip count beside the runs that could not be counted.

    The asked interval and change scope select what is counted; the search for
    a matching targeted completion runs over the whole available history,
    including before the interval's lower bound. Exit 0: complete readable
    evidence, even when the slip count is positive. Exit 1: partial or
    unavailable evidence — usable counts are kept when they can stand, and
    missing history is unavailable, never a zero. Exit 2: an invalid interval.
    Reading never appends, repairs or creates history.
    """
    since, until = args.since, args.until
    if since is not None and until is not None and since >= until:
        _log(f"the interval {since.isoformat()}..{until.isoformat()} is reversed; refusing it")
        return 2
    try:
        events, findings = _read_events()
    except HistoryMissing as missing:
        print("slips: unavailable; incomplete/not countable runs: unavailable")
        _log(f"{missing} — missing history is unavailable, never a counted zero")
        return 1
    runs, grouping, damaged, unassigned = _runs(events)
    findings.extend(grouping)
    partial = bool(findings) or unassigned > 0

    slips = 0
    uncountable = 0
    # Valid targeted greens of the whole available history, in file order: a
    # qualifying predecessor may lie before the asked interval.
    predecessors: list[tuple[datetime.datetime, str, str | None, str, str | None]] = []
    for run_id, run in runs.items():
        start = run["start"]
        moment = _instant(start.get("utc"))
        repository = start.get("repository")
        job = start.get("job")
        placement = start.get("placement")
        localisable = moment is not None and isinstance(repository, str) and isinstance(job, str)
        if run_id in damaged and not localisable:
            # Damaged evidence of unknown origin: the diagnosis stays visible,
            # the measurement stays partial, and no run is invented for it.
            partial = True
            continue
        if not localisable:
            continue
        if job != "verify" or placement != "local" or not _same_repository(repository):
            continue  # complete unrelated jobs, placements and repositories are ignored
        change = start.get("change")
        # The asked interval and change scope select what is counted; the
        # predecessor search stays whole-history, because a targeted check that
        # started before `since` is still the one that missed the later red run.
        started_in_bounds = (since is None or moment >= since) and (until is None or moment < until)
        named_in_scope = args.change is None or change == args.change
        in_selection = started_in_bounds and named_in_scope
        end = run["end"]
        if run_id in damaged or end is None:
            if in_selection:
                uncountable += 1  # an interrupted or conflicting run is a gap, not a zero
            continue
        verdict = end.get("verdict")
        kind = start.get("check_kind")  # absent: a legacy duration record
        if kind == "targeted":
            stable = (
                isinstance(start.get("tree_id"), str)
                and isinstance(start.get("config_sha256"), str)
                and end.get("tree_id") == start.get("tree_id")
            )
            completion = _instant(end.get("utc"))
            if verdict == "green" and stable and completion is not None:
                predecessors.append((completion, repository, change, start["tree_id"], start["config_sha256"]))
            elif verdict == "green" and in_selection:
                uncountable += 1  # green work whose comparison evidence cannot be trusted
            # A red targeted run is a complete observation and never a predecessor.
            continue
        if not in_selection:
            continue
        # A full verification run: kinds full and full-fallback, and every
        # legacy record, which predates comparison evidence.
        comparable = (
            kind in ("full", "full-fallback")
            and isinstance(start.get("tree_id"), str)
            and isinstance(change, str)
            and isinstance(start.get("config_sha256"), str)
        )
        if verdict != "red":
            continue  # a green full run is a complete observation of zero slips
        if not comparable:
            uncountable += 1  # legacy or incomplete comparison evidence is not evidence of zero
            continue
        if _slip_predecessor_match(predecessors, moment, repository, change, start["tree_id"], start["config_sha256"]):
            slips += 1  # each qualifying red full-run identity counts once

    scope = f"change {args.change}" if args.change is not None else "change all"
    lower = since.isoformat() if since is not None else "none"
    upper = until.isoformat() if until is not None else "none"
    print(f"repository {os.path.realpath(str(Path.cwd()))} · {scope} · since {lower} · until {upper}")
    print(f"slips: {slips}; incomplete/not countable runs: {uncountable}")
    for finding in findings:
        print(f"history note: {finding}")
    if partial or uncountable:
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
