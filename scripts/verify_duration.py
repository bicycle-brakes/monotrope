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


def _open_history(state_root: Path | None = None) -> int:
    """A private regular history file for appending; an aliased or nonregular destination refuses.

    The same shape as the admission's lock files: the no-follow open fails on
    a symlink standing in the file's place, a FIFO cannot pass the regular
    check, and nothing is ever written through a substituted destination.
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
    path = history_path(root)
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


def append_event(event: dict, state_root: Path | None = None) -> None:
    """Append one complete JSON line under a file lock, so concurrent runs never mix identities."""
    line = json.dumps(event, sort_keys=True) + "\n"
    fd = _open_history(state_root)
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
        "commit": _git(["rev-parse", "HEAD"], cwd=basis),
        # None means git could not answer; only an answer decides yes or no.
        "dirty": None if porcelain is None else bool(porcelain),
        "config_sha256": _gate_file_digest(basis),
        "job": job,
        "placement": placement,
        "memory_pct": memory,
        "workers": _worker_setting(env),
        **_context_fields(),
    }
    append_event(event, state_root=state_root)
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


def _runs(events: list[dict]) -> tuple[dict[str, dict], list[str]]:
    """Group the events by run identity in file order; gate and end rows without a start are diagnosed."""
    runs: dict[str, dict] = {}
    findings: list[str] = []
    order: list[str] = []
    invalid_runs: set[str] = set()
    for event in events:
        run_id = event["run_id"]
        kind = event["event"]
        error = _record_error(event)
        if error:
            findings.append(f"{error} for run {run_id}")
            invalid_runs.add(run_id)
        if kind == RUN_START:
            if run_id in runs:
                findings.append(f"a second start for run {run_id}")
                continue
            runs[run_id] = {"start": event, "gates": [], "end": None}
            order.append(run_id)
        elif run_id not in runs:
            findings.append(f"line with {kind} for unknown run {run_id} — its start row is missing or malformed")
        elif error:
            continue
        elif kind == GATE:
            runs[run_id]["gates"].append(event)
        elif runs[run_id]["end"] is None:
            runs[run_id]["end"] = event
        else:
            findings.append(f"a second end for run {run_id}")
    for run_id in invalid_runs:
        if run_id in runs:
            runs[run_id]["end"] = None
    return {run_id: runs[run_id] for run_id in order}, findings


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
    runs, grouping = _runs(events)
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
