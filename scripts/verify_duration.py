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


def _git(arguments: list[str]) -> str | None:
    """One git answer, or None when git is absent, fails or times out — never a guess."""
    try:
        done = subprocess.run(
            ["git", *arguments], capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if done.returncode != 0:
        return None
    return done.stdout.strip() or None


def _gate_file_digest() -> str | None:
    """The SHA-256 of the one gate file this run measured, or None when absent."""
    try:
        return hashlib.sha256(GATE_FILE.read_bytes()).hexdigest()
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
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise StorageUnusable(f"the history file {path} is not a regular file; refusing substituted history")
    return fd


def append_event(event: dict) -> None:
    """Append one complete JSON line under a file lock, so concurrent runs never mix identities."""
    line = json.dumps(event, sort_keys=True) + "\n"
    fd = _open_history()
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            os.write(fd, line.encode("utf-8"))
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
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
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise HistoryMissing(f"no history at {path}; nothing has been recorded yet") from None
    except OSError as error:
        raise HistoryMissing(f"the history file {path} cannot be read ({error.strerror or error})") from None
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
        events.append(event)
    return events, findings


def _runs(events: list[dict]) -> tuple[dict[str, dict], list[str]]:
    """Group the events by run identity in file order; gate and end rows without a start are diagnosed."""
    runs: dict[str, dict] = {}
    findings: list[str] = []
    order: list[str] = []
    for event in events:
        run_id = event["run_id"]
        kind = event["event"]
        if kind == RUN_START:
            if run_id in runs:
                findings.append(f"a second start for run {run_id}")
                continue
            runs[run_id] = {"start": event, "gates": [], "end": None}
            order.append(run_id)
        elif run_id not in runs:
            findings.append(f"line with {kind} for unknown run {run_id} — its start row is missing or malformed")
        elif kind == GATE:
            runs[run_id]["gates"].append(event)
        elif runs[run_id]["end"] is None:
            runs[run_id]["end"] = event
        else:
            findings.append(f"a second end for run {run_id}")
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
    return 0


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
