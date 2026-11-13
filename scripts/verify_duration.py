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

**Targeted results and local slips** (bead coding-harness-0swp). The stage-2
runner appends one `targeted` record per accepted targeted green, bound to its
checkpoint tree and the gate configuration it measured; the phase-6 boundary
correlates a completed red full run — through the runner-owned
`HARNESS_VERIFY_CORRELATION` identity that `start` records — with this
repository's latest matching targeted green and appends one `slip` per
full-run identity, deduplicated atomically. Timeouts, launch and admission
failures and identity mismatches stay unmeasured; a storage gap is reported
and never changes a verification verdict. The `slips` reader counts distinct
slipped full runs of one repository in a half-open UTC interval and reports
missing, corrupt or incomplete evidence as an unavailable measurement, never
as a trustworthy zero.

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
    python -m scripts.verify_duration targeted --repository P --worktree P \
            --change C --verb V --tests F,G --gates A --outcome green --tree T
    python -m scripts.verify_duration slip --repository P --check C --run R \
            --tree T --failed-gates A,B
    python -m scripts.verify_duration slips --repository P --since UTC --until UTC
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
TARGETED = "targeted"
SLIP = "slip"
EVENTS = (RUN_START, GATE, RUN_END, TARGETED, SLIP)
GATE_FILE = Path("decisions") / "gates.yaml"
GIT_TIMEOUT_SECONDS = 10.0
# The runner-owned identity that ties one full `make verify` to its duration records,
# so a completed local red can be measured against the latest matching targeted green.
CORRELATION_ENV = "HARNESS_VERIFY_CORRELATION"
# run_start fields that arrived after version 1 was already in use: records written before
# them stand without them, and their absence reads as the explicit unknown, never as invalid.
START_OPTIONAL_FIELDS = frozenset({"correlation"})
# Bounded identifiers only: no raw gate output and no credentials ever reach the history.
MAX_FAILED_TESTS = 40
MAX_TEST_ID_LENGTH = 200


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
    return done.stdout.strip()


def _gate_file_digest() -> str | None:
    """The SHA-256 of the one gate file this run measured, or None when absent."""
    try:
        return hashlib.sha256(GATE_FILE.read_bytes()).hexdigest()
    except OSError:
        return None


def gate_file_digest(root: Path) -> str | None:
    """The SHA-256 of the gate file under this repository root, or None when absent.

    The same bytes `_gate_file_digest()` reads for a run started there, so a targeted record and
    the full run it is measured against carry comparable digests.
    """
    try:
        return hashlib.sha256((Path(root) / GATE_FILE).read_bytes()).hexdigest()
    except OSError:
        return None


def _worker_setting() -> str | None:
    """The effective worker setting passed to the gates; unset means xdist decides."""
    value = os.environ.get("PYTEST_XDIST_AUTO_NUM_WORKERS", "")
    return value if value else None


def _open_history(readable: bool = False) -> int:
    """A private regular history file for appending; an aliased or nonregular destination refuses.

    The same shape as the admission's lock files: the no-follow open fails on
    a symlink standing in the file's place, a FIFO cannot pass the regular
    check, and nothing is ever written through a substituted destination.
    `readable` opens read-write, so the caller may inspect the standing records under the same
    guards before appending (the slip deduplication).
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
    write = os.O_RDWR if readable else os.O_WRONLY
    try:
        return os.open(path, write | os.O_CREAT | os.O_EXCL | os.O_APPEND | os.O_NOFOLLOW, 0o600)
    except FileExistsError:
        pass
    except OSError as error:
        raise StorageUnusable(
            f"the history file {path} cannot be created no-follow ({error.strerror or error}) — "
            "a substituted destination is refused, never written through"
        ) from error
    # O_NONBLOCK so a FIFO standing in the file's place is refused below, never waited on.
    try:
        fd = os.open(path, write | os.O_APPEND | os.O_NOFOLLOW | os.O_NONBLOCK)
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


def append_targeted(
    *,
    repository: str,
    worktree: str,
    change: str,
    verb: str,
    check_id: str,
    tests: list[str],
    gates: list[str],
    config_sha256: str | None,
    tree: str,
    commit: str | None,
    outcome: str,
) -> None:
    """Append one targeted-check result: scope, identity and the checkpoint it was accepted at.

    Selected tests and gates are identifiers only, never output; `tree` and `config_sha256` are what
    a later slip measurement compares, so a green is never blamed across changed content.
    """
    append_event(
        {
            "v": EVENT_VERSION,
            "event": TARGETED,
            "check_id": check_id,
            "utc": _utc_now(),
            "repository": repository,
            "worktree": worktree,
            "change": change,
            "verb": verb,
            "tests": list(tests),
            "gates": list(gates),
            "outcome": outcome,
            "config_sha256": config_sha256,
            "tree": tree,
            "commit": commit,
        }
    )


def append_slip(event: dict) -> bool:
    """Append one slip unless this full run's slip already stands; the check and the write share one lock.

    Deduplication is atomic with the append (bead coding-harness-0swp): reprocessing a completed
    red run under the same run identity returns False and writes nothing, so a slip is counted once
    per full run even when two writers race. A storage refusal raises `StorageUnusable`.
    """
    line = json.dumps(event, sort_keys=True) + "\n"
    fd = _open_history(readable=True)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            size = os.fstat(fd).st_size
            standing = os.pread(fd, size, 0).decode("utf-8", "replace") if size else ""
            for row in standing.splitlines():
                if not row.strip():
                    continue
                try:
                    record = json.loads(row)
                except ValueError:
                    continue  # a truncated row is diagnosed by the reader, never repaired here
                if (
                    isinstance(record, dict)
                    and record.get("event") == SLIP
                    and record.get("run_id") == event.get("run_id")
                ):
                    return False
            data = line.encode("utf-8")
            if os.write(fd, data) != len(data):
                raise StorageUnusable("the history write was incomplete; refusing to claim a complete slip")
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    except OSError as error:
        raise StorageUnusable(f"the history lock or write failed ({error}); refusing to record slip") from error
    finally:
        os.close(fd)
    return True


def bounded_failed_tests(ids: list[str]) -> list[str]:
    """Failed test ids bounded for the record: at most `MAX_FAILED_TESTS`, each at most `MAX_TEST_ID_LENGTH`."""
    return [ident[:MAX_TEST_ID_LENGTH] for ident in ids[:MAX_FAILED_TESTS]]


def record_local_slip(repository: str, correlation: str, tree: str, failed_tests: list[str] | None) -> str:
    """Correlate one completed red full run with this repository's latest matching targeted green.

    The run is found through the runner-owned correlation its `start` record carries; only a
    completed red verdict counts, so a timeout and a run that never started stay unmeasured. The
    matching green is the latest recorded `targeted` record of this repository with the same gate
    configuration and the same checked tree — differing commits with identical trees match,
    differing trees never (bead coding-harness-0swp). Returns what was recorded or why the run
    stays unmeasured; raises `HistoryMissing` and `StorageUnusable` for the caller to report.
    """
    events, _findings = _read_events()
    start = None
    for event in events:
        if event["event"] == RUN_START and event.get("correlation") == correlation:
            start = event
    if start is None or _record_error(start):
        return "the red full run carries no recorded start identity; it stays unmeasured"
    if not start.get("config_sha256"):
        return "the full run has an unreadable gate configuration; it stays unmeasured"
    run_id = start["run_id"]
    ends = [event for event in events if event["event"] == RUN_END and event.get("run_id") == run_id]
    if not ends or _record_error(ends[-1]) or ends[-1].get("verdict") != "red":
        return f"full run {run_id[:8]}… has no completed red verdict; it stays unmeasured"
    failed_gates = sorted(
        {
            str(event["gate"])
            for event in events
            if event["event"] == GATE
            and event.get("run_id") == run_id
            and event.get("exit") != 0
            and event.get("enforcement") == "block"
            and not _record_error(event)
        }
    )
    home = str(Path(repository).resolve())
    match = None
    for event in events:
        if event["event"] != TARGETED or event.get("outcome") != "green" or _record_error(event):
            continue
        if str(Path(str(event.get("repository", ""))).resolve()) != home:
            continue
        if (
            not event.get("config_sha256")
            or event.get("config_sha256") != start.get("config_sha256")
            or event.get("tree") != tree
        ):
            continue
        match = event  # file order: the latest matching green of this repository wins
    if match is None:
        return (
            f"no accepted targeted green of {home} matches tree {tree[:12]}… and this gate configuration; "
            f"the red full run {run_id[:8]}… stays unmeasured"
        )
    slip = {
        "v": EVENT_VERSION,
        "event": SLIP,
        "check_id": str(match["check_id"]),
        "run_id": run_id,
        "utc": _utc_now(),
        "repository": home,
        "failed_gates": failed_gates,
        "failed_tests": None if failed_tests is None else bounded_failed_tests(list(failed_tests)),
        "config_sha256": start.get("config_sha256"),
        "tree": tree,
    }
    if append_slip(slip):
        named = ", ".join(failed_gates) or "none recorded"
        return (
            f"recorded one local slip: targeted check {str(match['check_id'])[:8]}… was green on this tree, "
            f"full run {run_id[:8]}… is red (failed gates: {named})"
        )
    return f"the slip of full run {run_id[:8]}… stands already; the red run was not counted twice"


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
        # The runner-owned identity of a full check whose caller asked for slip correlation;
        # a run nobody correlated carries None and stays unmeasured in the slip reader.
        "correlation": os.environ.get(CORRELATION_ENV) or None,
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


def _utc_moment(text_value: str) -> datetime.datetime:
    """A UTC moment from an ISO string that carries its offset; the type of --since and --until."""
    try:
        moment = datetime.datetime.fromisoformat(text_value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"{text_value} is not an ISO-8601 moment") from error
    if moment.tzinfo is None:
        raise argparse.ArgumentTypeError(f"{text_value} carries no UTC offset")
    return moment.astimezone(datetime.UTC)


def _comma_list(raw: str | None) -> list[str]:
    """A comma-separated identifier list from the command line, empty parts dropped."""
    return [name.strip() for name in (raw or "").split(",") if name.strip()]


def cmd_targeted(args: argparse.Namespace) -> int:
    """Append one targeted-check result record; the stage-2 runner calls the function directly."""
    event = {
        "v": EVENT_VERSION,
        "event": TARGETED,
        "check_id": args.check,
        "utc": _utc_now(),
        "repository": str(Path(args.repository).resolve()),
        "worktree": str(Path(args.worktree).resolve()),
        "change": args.change,
        "verb": args.verb,
        "tests": _comma_list(args.tests),
        "gates": _comma_list(args.gates),
        "outcome": args.outcome,
        "config_sha256": args.config_sha256
        if args.config_sha256 is not None
        else gate_file_digest(Path(args.repository)),
        "tree": args.tree,
        "commit": args.commit,
    }
    append_event(event)
    print(event["check_id"])
    return 0


def cmd_slip(args: argparse.Namespace) -> int:
    """Append one slip record, deduplicated on its full-run identity; print what stands."""
    event = {
        "v": EVENT_VERSION,
        "event": SLIP,
        "check_id": args.check,
        "run_id": args.run,
        "utc": _utc_now(),
        "repository": str(Path(args.repository).resolve()),
        "failed_gates": _comma_list(args.failed_gates),
        "failed_tests": _comma_list(args.failed_tests) or None,
        "config_sha256": args.config_sha256,
        "tree": args.tree,
    }
    appended = append_slip(event)
    print("recorded one slip" if appended else "the slip of this full run stands already; it was not counted twice")
    return 0


def cmd_slips(args: argparse.Namespace) -> int:
    """Count distinct slipped full runs of one repository in the half-open [since, until) UTC interval.

    Missing, corrupt or incomplete evidence is an unavailable measurement, named as such — never a
    trustworthy zero (bead coding-harness-0swp).
    """
    repository = str(Path(args.repository).resolve())
    try:
        events, findings = _read_events()
    except HistoryMissing as missing:
        print(f"slip measurement unavailable: {missing}")
        return 1
    slips = [event for event in events if event["event"] == SLIP]
    broken = list(findings)
    broken += [f"invalid slip fields: {event.get('check_id')}" for event in slips if _record_error(event)]
    counted = {
        event["run_id"]
        for event in slips
        if not _record_error(event)
        and str(Path(str(event.get("repository", ""))).resolve()) == repository
        and args.since <= datetime.datetime.fromisoformat(event["utc"]).astimezone(datetime.UTC) < args.until
    }
    # A failed append leaves no slip row to validate. Inspect correlated completed red runs
    # as well: without their record a matching (or unreadable) identity is unmeasured.
    recorded_runs = {event["run_id"] for event in slips if not _record_error(event)}
    greens = [
        event
        for event in events
        if event["event"] == TARGETED
        and not _record_error(event)
        and event.get("outcome") == "green"
        and str(Path(event["repository"]).resolve()) == repository
    ]
    for start in events:
        if (
            start["event"] != RUN_START
            or _record_error(start)
            or not start.get("correlation")
            or str(Path(start["repository"]).resolve()) != repository
            or start["run_id"] in recorded_runs
        ):
            continue
        ends = [
            event
            for event in events
            if event["event"] == RUN_END and event["run_id"] == start["run_id"] and not _record_error(event)
        ]
        if not ends or ends[-1]["verdict"] != "red":
            continue
        ended = datetime.datetime.fromisoformat(ends[-1]["utc"]).astimezone(datetime.UTC)
        if not args.since <= ended < args.until:
            continue
        # Legacy starts have no checked tree. A green on a potentially matching configuration
        # cannot establish a trustworthy zero when the caller's correlation append is missing.
        if any(
            not start.get("config_sha256")
            or not green.get("config_sha256")
            or start["config_sha256"] == green["config_sha256"]
            for green in greens
        ):
            broken.append(f"correlated red full run {start['run_id']} has no slip record; not measured")
    interval = f"{args.since.isoformat()} (inclusive) to {args.until.isoformat()} (exclusive)"
    if broken:
        for note in broken:
            _log(f"slip measurement incomplete: {note}")
        print(f"slip measurement is incomplete; not measured reliably; this count is not trustworthy: {len(counted)}")
        print(f"interval {interval} · repository {repository}")
        return 1
    print(f"slips: {len(counted)} distinct slipped full runs")
    print(f"interval {interval} · repository {repository}")
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
        if not isinstance(event, dict) or event.get("event") not in EVENTS:
            findings.append(f"line {number}: not a version-1 verify-duration event")
            continue
        identity = "check_id" if event["event"] in (TARGETED, SLIP) else "run_id"
        if not isinstance(event.get(identity), str):
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

    def names(value: object) -> bool:
        return isinstance(value, list) and all(isinstance(item, str) and bool(item.strip()) for item in value)

    kind = event["event"]
    if kind in (TARGETED, SLIP):
        fields = {"check_id": text, "utc": timestamp}
        if kind == SLIP:
            fields["run_id"] = text
    else:
        fields = {"run_id": text, "utc": timestamp}
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
                "correlation": lambda v: v is None or text(v),
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
    elif kind == RUN_END:
        fields.update({"seconds": seconds, "verdict": lambda v: v in ("green", "red")})
    elif kind == TARGETED:
        fields.update(
            {
                "repository": text,
                "worktree": text,
                "change": text,
                "verb": text,
                "tests": names,
                "gates": names,
                "outcome": lambda v: v in ("green", "red"),
                "config_sha256": lambda v: v is None or text(v),
                "tree": text,
                "commit": lambda v: v is None or text(v),
            }
        )
    else:
        fields.update(
            {
                "repository": text,
                "failed_gates": names,
                "failed_tests": lambda v: v is None or names(v),
                "config_sha256": lambda v: v is None or text(v),
                "tree": text,
            }
        )
    invalid: list[str] = []
    for name, check in fields.items():
        # `correlation` arrived with coding-harness-0swp: version-1 records written before it
        # carry no such field and must keep reading as valid, so absence is the unknown.
        if name not in event:
            if name not in START_OPTIONAL_FIELDS:
                invalid.append(name)
            continue
        if not check(event[name]):
            invalid.append(name)
    return f"invalid {kind} fields: {', '.join(invalid)}" if invalid else None


def _runs(events: list[dict]) -> tuple[dict[str, dict], list[str]]:
    """Group the full-run events by identity in file order; gate and end rows without a start are diagnosed.

    Targeted and slip records have no run grouping of their own: they are validated and diagnosed
    when malformed, but they never join a run, so the version-1 report keeps reading as it did.
    """
    runs: dict[str, dict] = {}
    findings: list[str] = []
    order: list[str] = []
    invalid_runs: set[str] = set()
    for event in events:
        kind = event["event"]
        if kind in (TARGETED, SLIP):
            error = _record_error(event)
            if error:
                findings.append(f"{error} for check {event.get('check_id')}")
            continue
        run_id = event["run_id"]
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

    targeted = operations.add_parser("targeted", help="append one targeted-check result record")
    targeted.add_argument("--repository", required=True, help="the canonical repository path the check accepted")
    targeted.add_argument("--worktree", required=True, help="the canonical worktree path the check ran in")
    targeted.add_argument("--change", required=True, help="the change the attempt worked on")
    targeted.add_argument("--verb", required=True, help="the runner verb that ran the check")
    targeted.add_argument("--check", default=uuid.uuid4().hex, help="the check's own identity")
    targeted.add_argument("--tests", default="", help="comma-separated selected whole test files")
    targeted.add_argument("--gates", default="", help="comma-separated selected gate ids")
    targeted.add_argument("--outcome", required=True, choices=("green", "red"), help="the check's outcome")
    targeted.add_argument(
        "--config-sha256",
        default=None,
        help="the gate configuration digest; computed from --repository when left out",
    )
    targeted.add_argument("--tree", required=True, help="the accepted checkpoint tree id")
    targeted.add_argument("--commit", default=None, help="the accepted checkpoint commit")
    targeted.set_defaults(handler=cmd_targeted)

    slip = operations.add_parser("slip", help="append one slip record, deduplicated on the full run")
    slip.add_argument("--repository", required=True, help="the repository the red full run measured")
    slip.add_argument("--check", required=True, help="the matched targeted check's identity")
    slip.add_argument("--run", required=True, help="the red full run's identity")
    slip.add_argument("--tree", required=True, help="the checked tree the two runs share")
    slip.add_argument("--failed-gates", default="", help="comma-separated blocking red gate ids")
    slip.add_argument("--failed-tests", default="", help="comma-separated failed pytest ids, if known")
    slip.add_argument("--config-sha256", default=None, help="the gate configuration digest both runs measured")
    slip.set_defaults(handler=cmd_slip)

    slips = operations.add_parser("slips", help="count distinct slipped full runs of one repository in a UTC interval")
    slips.add_argument("--repository", required=True, help="the repository whose slips are counted")
    slips.add_argument(
        "--since", required=True, type=_utc_moment, help="inclusive interval start, ISO-8601 with offset"
    )
    slips.add_argument("--until", required=True, type=_utc_moment, help="exclusive interval end, ISO-8601 with offset")
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
