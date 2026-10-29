#!/usr/bin/env python3
"""run_report.py - one local, read-only report of the active changes (bead coding-harness-o2yc).

    python3 scripts/run_report.py                # every active change, then one live block
    python3 scripts/run_report.py --change NAME  # one active change, then one live block
    make report [CHANGE=name]                    # the same through make; CHANGE passes as data

Per active change (the immediate real folders under `plans/changes/`, `archive`
excluded) it prints the measured attempt rows of the plan's `## Time used`
section, the calls `findings.md` records, the recorded time against the opening
plan card's `Appetite:` line, and one live block with runner and verification
processes plus macOS/Linux memory figures. It is a snapshot to read before a
verify-bearing step, not a gate: it starts, stops and locks nothing.

What it cannot read, it says so:

- an unreadable time record is counted (`unread lines: N`) and marks the
  subtotal incomplete; it never becomes a guessed duration (criterion 5);
- a missing card, an unreadable appetite or a failed source is `not read`,
  never a fabricated zero, ratio or threshold verdict (criteria 7 and 11);
- a clean leak check on a `findings.md` call line is not a completion verdict;
  calls are labelled as evidence of a call, not measured attempts (criterion 3).

It runs no network, tracker, model, Git mutation or state-writing command and
prints only summary fields - never prompt, answer or raw diagnostic text
(criterion 12). `scripts/stage2.py` and `scripts/stage2_runs.py` stay the
writers of the formats: this script reads them through the runner's own
`time_log`, `card_problem`, `CARD_LABELS` and `CALL_LINE`/`CALL_PREFIXES`,
without duplicating their section and audit-line recognition.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # the report writes nothing - bytecode included (criterion 12)

import argparse  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import stat  # noqa: E402
import subprocess  # noqa: E402
from collections.abc import Callable  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from datetime import UTC, datetime  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

import stage2  # noqa: E402
import stage2_runs  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGES_DIR = "plans/changes"
ARCHIVE = "archive"
NOT_READ = "not read"
COMMAND_TIMEOUT = 2.0
# Local until separate verification-resource work lands (bead coding-harness-p6mu).
MEMORY_FLOOR = 25.0
CALL_FIELDS = ("attempt", "route", "endpoint", "model")
FIELD_CAP = 60  # a field longer than this is prose, not the runner's form

RunCommand = Callable[..., str]


class SourceError(Exception):
    """One system source could not be read; the message is bounded and names the source, never its input."""


def run_command(argv: list[str], timeout: float = COMMAND_TIMEOUT) -> str:
    """One system command's stdout, or a SourceError that names the source and nothing else."""
    try:
        done = subprocess.run(argv, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise SourceError(f"not read ({argv[0]}: timed out)") from None
    except OSError:
        raise SourceError(f"not read ({argv[0]}: unavailable)") from None
    if done.returncode != 0:
        raise SourceError(f"not read ({argv[0]}: exit {done.returncode})")
    try:
        return done.stdout.decode("utf-8")
    except UnicodeDecodeError:
        raise SourceError(f"not read ({argv[0]}: not UTF-8)") from None


# ---------------------------------------------------------------------------
# The active changes
# ---------------------------------------------------------------------------


def active_changes(root: Path, unread: list[str] | None = None) -> list[str]:
    """The sorted names of the immediate real directories under plans/changes, archive excluded.

    Symlinks are never followed, so a link cannot pull a foreign folder into
    the report or let a selection escape the active-change directory.
    """
    try:
        entries = sorted((root / CHANGES_DIR).iterdir())
    except OSError:
        raise SourceError("not read (plans/changes: change list cannot be read)") from None
    names = []
    for entry in entries:
        if entry.name == ARCHIVE:
            continue
        try:
            mode = entry.stat(follow_symlinks=False).st_mode
        except OSError:
            if unread is not None:
                unread.append(f"plans/changes/{_bounded(entry.name)}: not read (metadata cannot be read)")
            continue
        if stat.S_ISDIR(mode):
            names.append(entry.name)
    return names


def read_text(path: Path) -> tuple[str | None, str]:
    """The file's text, or (None, a bounded reason that names the file and nothing else)."""
    try:
        return path.read_text(encoding="utf-8"), ""
    except FileNotFoundError:
        return None, f"{path.name} is missing"
    except UnicodeDecodeError:
        return None, f"{path.name} is not valid UTF-8"
    except OSError as error:
        return None, f"{path.name} cannot be read ({error.strerror or 'unreadable'})"


# ---------------------------------------------------------------------------
# Time: the plan's `## Time used` section
# ---------------------------------------------------------------------------

# The runner's time-entry shape (`stage2.time_entry`). Its explicit seconds are
# the authority; the endpoints only name the span and are never subtracted.
RUNNER_ENTRY = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<start>\d{2}:\d{2}:\d{2})"
    r"–(?:(?P<end_date>\d{4}-\d{2}-\d{2}) )?(?P<end>\d{2}:\d{2}:\d{2}) UTC, "
    r"(?P<seconds>\d+) s — "
    r"(?P<verb>[^·]+?) · attempt (?P<attempt>\d+) · route (?P<route>[^·]+?)"
    r" · model (?P<model>[^·]+?) · (?P<result>accepted|rejected) · measured by the runner"
)
# A dated orchestrator record with an explicit measured seconds field.
DATED_SECONDS = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<start>\d{2}:\d{2}(?::\d{2})?)"
    r"–(?:(?P<end_date>\d{4}-\d{2}-\d{2}) )?(?P<end>\d{2}:\d{2}(?::\d{2})?)(?: UTC)?, "
    r"(?P<seconds>\d+) s(?:[ \t]*$|[,;)].*| — .*)"
)
# A dated orchestrator record that is only an exact closed UTC range: same-day
# clock endpoints, or endpoints that carry their own date.
DATED_RANGE = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<start>\d{2}:\d{2}(?::\d{2})?)"
    r"–(?:(?P<end_date>\d{4}-\d{2}-\d{2}) )?(?P<end>\d{2}:\d{2}(?::\d{2})?) UTC(?:[ \t]*$|[,;)].*)"
)
FURNITURE = re.compile(r"^(?:#{1,6} |```|~~~)")


@dataclass
class TimeRecord:
    """One readable duration record; the attempt fields exist only on runner entries."""

    seconds: int
    verb: str | None = None
    attempt: int | None = None
    route: str | None = None
    model: str | None = None
    result: str | None = None

    @property
    def is_attempt(self) -> bool:
        return self.verb is not None


@dataclass
class TimeReading:
    """What the time section yielded: the sum, the unread content lines, the attempt rows."""

    section_read: bool
    seconds: int = 0
    unread: int = 0
    attempts: list[TimeRecord] = field(default_factory=list)


def _clock(text: str, day: str) -> datetime | None:
    for shape in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(f"{day} {text}", shape)
        except ValueError:
            continue
    return None


def parse_time_line(content: str) -> TimeRecord | None:
    """One readable duration record, or None; an explicit duration outranks the endpoints."""
    body = content[2:].strip() if content.startswith("- ") else content
    matched = RUNNER_ENTRY.fullmatch(body)
    if matched:
        return TimeRecord(
            seconds=int(matched.group("seconds")),
            verb=matched.group("verb").strip(),
            attempt=int(matched.group("attempt")),
            route=matched.group("route").strip(),
            model=matched.group("model").strip(),
            result=matched.group("result"),
        )
    if " s — " in body and ("· attempt " in body or "measured by the runner" in body):
        return None  # runner-shaped but broken: unread, never re-derived from its endpoints
    if re.search(r"\b(?:about|approx(?:imate(?:ly)?)?\.?|unmeasured|not measured)\b", body, re.IGNORECASE):
        return None  # exact-looking endpoints do not turn an explicitly guessed record into evidence
    matched = DATED_SECONDS.fullmatch(body)
    if matched:
        return TimeRecord(seconds=int(matched.group("seconds")))
    matched = DATED_RANGE.fullmatch(body)
    if matched:
        start = _clock(matched.group("start"), matched.group("date"))
        end = _clock(matched.group("end"), matched.group("end_date") or matched.group("date"))
        if start is None or end is None or end <= start:
            return None  # malformed, ambiguous or a non-positive range: unread, never guessed
        return TimeRecord(seconds=int((end - start).total_seconds()))
    return None


def read_time(plan: Path) -> tuple[TimeReading, str]:
    """The plan's time section, read through the runner's own `time_log`."""
    try:
        section = stage2.time_log(plan)
    except stage2.Refused as error:
        # Preserve the runner's known reason without exposing its absolute path
        # or forwarding arbitrary exception text into the report.
        reason = "cannot be read."
        missing_heading = "has no `## Time used` heading."
        if str(error) == f"{plan} {missing_heading}":
            reason = missing_heading
        return TimeReading(section_read=False), f"{plan.name} {reason}"
    reading = TimeReading(section_read=True)
    for raw in section.splitlines():
        content = raw.strip()
        if not content or FURNITURE.match(content):
            continue  # blank lines and Markdown heading/fence furniture are not content
        record = parse_time_line(content)
        if record is None:
            reading.unread += 1
            continue
        reading.seconds += record.seconds
        if record.is_attempt:
            reading.attempts.append(record)
    return reading, ""


# ---------------------------------------------------------------------------
# Appetite: the opening plan card only
# ---------------------------------------------------------------------------

APPETITE_VALUE = re.compile(
    r"^\s*(?:(?P<hours>\d+(?:\.\d+)?)\s*(?:hours?|h)\b)?"
    r"\s*(?:(?P<minutes>\d+(?:\.\d+)?)\s*(?:min(?:utes?)?)\b)?"
    r"\s*(?P<rest>.*)$",
    re.IGNORECASE,
)
COMPETING = re.compile(r"\d+(?:\.\d+)?\s*(?:hours?|h|min(?:utes?)?)\b", re.IGNORECASE)


def appetite_seconds(value: str | None) -> int | None:
    """The card value's positive budget in whole seconds, or None (report-local parser).

    Positive decimal hours and hours plus minutes compose; trailing explanatory
    text is ignored. A second budget value competes instead of composing and is
    refused, as is any amount without an hours or minutes unit.
    """
    if not value:
        return None
    matched = APPETITE_VALUE.match(value)
    hours, minutes = matched.group("hours"), matched.group("minutes")
    if hours is None and minutes is None:
        return None
    if COMPETING.search(matched.group("rest")):
        return None
    total_minutes = (float(hours) if hours else 0.0) * 60 + (float(minutes) if minutes else 0.0)
    seconds = int(round(total_minutes * 60))
    return seconds if seconds > 0 else None


def card_appetite_value(plan_text: str) -> str | None:
    """The opening card's Appetite value, or None (report-local lift of the one line).

    Lift only the Appetite line, recognised through the runner's own
    `CARD_LABELS`; defects in other labels do not invalidate this reading.
    """
    body = re.sub(r"\A---\n.*?\n---\n", "", plan_text, count=1, flags=re.S)
    head = re.split(r"^## ", body, maxsplit=1, flags=re.M)[0]
    lines = head.splitlines()
    opening = next((i for i, line in enumerate(lines) if re.match(r"^(?:```|~~~)", line)), None)
    if opening is None:
        return None
    for line in lines[opening + 1 :]:
        if re.match(r"^(?:```|~~~)", line):
            break
        label = next((item for item in stage2.CARD_LABELS if line.startswith(item)), None)
        if label == "Appetite:":
            return line[len("Appetite:") :]
    return None


# ---------------------------------------------------------------------------
# Calls: the audit lines of findings.md
# ---------------------------------------------------------------------------


def call_rows(findings_text: str) -> list[str]:
    """The findings' Stage-2 call lines as bounded rows of explicitly recorded metadata.

    These are evidence of a call, never measured attempts: no verdict is
    inferred (a clean leak check is not a completion), absent fields say
    `not read`, and rows are never joined on their attempt number.
    """
    rows = []
    for line in findings_text.splitlines():
        if not line.startswith(stage2_runs.CALL_PREFIXES):
            continue
        matched = stage2_runs.CALL_LINE.match(line)
        kind = matched.group(1) if matched else ""
        rest = matched.group("rest") if matched else ""
        cells = rest.split(" · ")
        verb = "session" if kind == "session" else cells[0].strip() if len(cells) > 1 else ""
        if not verb or len(verb) > FIELD_CAP:
            verb = "unparsed"
        fields = dict.fromkeys(CALL_FIELDS, NOT_READ)
        verdict = "verdict not recorded"
        for cell in cells if kind == "session" else cells[1:]:
            key, _, value = cell.partition(" ")
            if key in CALL_FIELDS and 0 < len(value) <= FIELD_CAP:
                fields[key] = value.strip()
            if kind == "session":
                dispatch = re.fullmatch(r"dispatch (accepted|pending|failed)(?: \(.*\))?\.", cell)
                if dispatch:
                    verdict = f"dispatch {dispatch.group(1)}"
        rows.append(
            f"  call: {verb} · attempt {fields['attempt']} · route {fields['route']}"
            f" · endpoint {fields['endpoint']} · model {fields['model']} · {verdict}"
        )
    return rows


# ---------------------------------------------------------------------------
# Live figures: processes
# ---------------------------------------------------------------------------

SHELLS = frozenset({"sh", "bash", "zsh", "dash", "ksh", "csh", "tcsh", "fish"})
KNOWN_VERBS = frozenset([*stage2.VERBS, "session", "prepare-explore"])
ETIME = re.compile(r"(?:\d+-)?\d{1,3}:\d{2}(?::\d{2})?")


@dataclass
class ProcessRow:
    """One matched process; only these four fields ever reach the output."""

    pid: str
    elapsed: str
    label: str
    change: str


def _is_stage2_script(token: str) -> bool:
    return token == "scripts/stage2.py" or token.endswith("/scripts/stage2.py")


def _is_verify_script(token: str) -> bool:
    return token == "scripts/verify_all.sh" or token.endswith("/scripts/verify_all.sh")


def _stage2_row(tokens: list[str], pid: str, elapsed: str, changes: frozenset[str]) -> ProcessRow | None:
    script = next((i for i, token in enumerate(tokens) if _is_stage2_script(token)), None)
    if script is None or script + 1 >= len(tokens) or tokens[script + 1] not in KNOWN_VERBS:
        return None
    if script != 0:
        if not re.fullmatch(r"python(?:\d+(?:\.\d+)*)?", Path(tokens[0]).name):
            return None  # the executable owns the invocation, not a preceding argument
        if any(not token.startswith("-") or token in {"-c", "-m", "--"} for token in tokens[1:script]):
            return None
    verb = tokens[script + 1]
    change = NOT_READ
    arguments = iter(tokens[script + 2 :])
    value_options = {
        "--model",
        "--class",
        "--availability-reported",
        "--seats",
        "--handover",
        "--stage-failed",
        "--reason",
        "--root",
    }
    for token in arguments:
        if token == "--stage2-off":
            # Its reason is optional. A known change or another option must
            # remain available to the positional/option reader below.
            following = next(arguments, None)
            if following is None:
                break
            if following not in changes and not following.startswith("-"):
                continue  # the explicit reason
            token = following
        if token in value_options:
            next(arguments, None)
            continue
        if token.startswith("-"):
            continue  # options may stand between the verb and the change
        if token in changes:
            change = token
        break  # only the first non-option token can name the change
    return ProcessRow(pid=pid, elapsed=elapsed, label=verb, change=change)


def _verify_row(tokens: list[str], pid: str, elapsed: str) -> ProcessRow | None:
    head = Path(tokens[0]).name
    if head == "make":
        arguments = iter(tokens[1:])
        options = True
        for token in arguments:
            if options and token == "--":
                options = False
                continue
            if options and token in {
                "-C",
                "-f",
                "-I",
                "-o",
                "-W",
                "--directory",
                "--file",
                "--makefile",
                "--include-dir",
                "--old-file",
                "--assume-old",
                "--what-if",
                "--new-file",
                "--assume-new",
                "--eval",
            }:
                next(arguments, None)
                continue
            if options and token.startswith("-"):
                continue
            if token == "verify":
                return ProcessRow(pid=pid, elapsed=elapsed, label="verify", change=NOT_READ)
        return None
    if head in SHELLS:
        # The shell is a wrapper unless it directly runs the verify script itself.
        arguments = iter(tokens[1:])
        for token in arguments:
            if token == "--":
                token = next(arguments, "")
            elif token in {"-o", "+o", "-O", "+O"}:
                next(arguments, None)
                continue
            elif token.startswith(("-", "+")):
                if token.startswith("-") and not token.startswith("--") and ("c" in token or "s" in token):
                    return None  # command text or stdin, not a script invocation
                continue
            if _is_verify_script(token):
                return ProcessRow(pid=pid, elapsed=elapsed, label="verify", change=NOT_READ)
            break
        return None
    if _is_verify_script(tokens[0]):
        return ProcessRow(pid=pid, elapsed=elapsed, label="verify", change=NOT_READ)
    return None


def parse_processes(ps_text: str, changes: frozenset[str]) -> list[ProcessRow]:
    """The runner invocations and verification processes of one `ps` table.

    Token matching only: a string inside an unrelated command - a shell
    wrapper, an editor, an echo - is discarded, never reported.
    """
    rows = []
    for line in ps_text.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 3 or not parts[0].isdigit() or not ETIME.fullmatch(parts[1]):
            continue  # the header line and anything unshaped
        pid, elapsed, command = parts
        tokens = command.split()
        if not tokens:
            continue
        row = _stage2_row(tokens, pid, elapsed, changes) or _verify_row(tokens, pid, elapsed)
        if row is not None:
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Live figures: memory
# ---------------------------------------------------------------------------


@dataclass
class MemorySnapshot:
    """Two rendered figures and the one number the floor warning compares."""

    available: str
    available_percent: float | None
    compressed: str


def _not_read(source: str, why: str) -> str:
    return f"not read ({source}: {why})"


def macos_memory(run: RunCommand) -> MemorySnapshot:
    """The free percentage of `memory_pressure` and the compressor share of `vm_stat` of `hw.memsize`.

    The compressor share counts the pages the compressor occupies, never the
    (logical) pages stored in it, over the physical bytes of `hw.memsize`.
    """
    percent = None
    try:
        text = run(["memory_pressure"])
        matched = re.search(r"free percentage:\s*(\d{1,3})\s*%", text, re.IGNORECASE)
        if matched is None:
            available = _not_read("memory_pressure", "no free-percentage line")
        else:
            value = int(matched.group(1))
            if value > 100:
                available = _not_read("memory_pressure", "free percentage out of range")
            else:
                percent = float(value)
                available = f"{value}% of physical memory (memory_pressure free percentage)"
    except SourceError as error:
        available = str(error)
    page_size = occupied = None
    try:
        stat_text = run(["vm_stat"])
        size = re.search(r"page size of (\d+) bytes", stat_text)
        pages = re.search(r"Pages occupied by compressor: (\d+)", stat_text)
        if size is not None:
            page_size = int(size.group(1))
        if pages is not None:
            occupied = int(pages.group(1))
    except SourceError:
        pass  # a missing vm_stat is counted below as one missing piece
    memsize = None
    try:
        raw = run(["sysctl", "-n", "hw.memsize"]).strip()
        if raw.isdigit():
            memsize = int(raw)
    except SourceError:
        pass
    if page_size and occupied is not None and memsize:
        share = occupied * page_size / memsize * 100
        compressed = (
            f"{share:.1f}% of physical memory (pages occupied by compressor, {page_size}-byte pages of hw.memsize)"
        )
    else:
        compressed = _not_read("vm_stat/sysctl", "page size, compressor pages or hw.memsize missing")
    return MemorySnapshot(available=available, available_percent=percent, compressed=compressed)


MEMINFO = re.compile(r"^(MemTotal|MemAvailable|Zswap):\s+(\d+)\s+kB$", re.MULTILINE)


def linux_memory(proc_dir: Path) -> MemorySnapshot:
    """MemAvailable/MemTotal and the resident Zswap share of MemTotal, labelled as zswap.

    `Zswapped` holds uncompressed bytes and is never substituted; SwapFree is
    not a compressed-memory source and is not read.
    """
    try:
        text = (proc_dir / "meminfo").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return MemorySnapshot(
            available=_not_read("meminfo", "MemAvailable/MemTotal unreadable"),
            available_percent=None,
            compressed=_not_read("meminfo", "Zswap/MemTotal unreadable"),
        )
    fields = {name: int(value) for name, value in MEMINFO.findall(text)}
    total = fields.get("MemTotal") or 0
    free = fields.get("MemAvailable")
    if free is not None and total > 0:
        share = free / total * 100
        available = f"{share:.1f}% of physical memory (MemAvailable of MemTotal)"
        percent: float | None = share
    else:
        available = _not_read("meminfo", "MemAvailable missing or MemTotal not positive")
        percent = None
    zswap = fields.get("Zswap")
    if zswap is not None and total > 0:
        compressed = f"{zswap / total * 100:.1f}% of MemTotal (zswap, resident Zswap kB)"
    else:
        compressed = _not_read("meminfo", "Zswap missing or MemTotal not positive")
    return MemorySnapshot(available=available, available_percent=percent, compressed=compressed)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _bounded(text: str, cap: int = 80) -> str:
    """User-supplied text, flattened and capped, for the one diagnostic that echoes it."""
    cleaned = "".join(ch if ch.isprintable() else " " for ch in text)
    return cleaned[:cap] + ("…" if len(cleaned) > cap else "")


def change_block(folder: Path, name: str) -> list[str]:
    """One change's block: attempts, calls, time against the card's appetite."""
    out = [f"change: {name}"]
    plan = folder / "plan.md"
    plan_text, plan_reason = read_text(plan)
    if plan_text is None:
        out.append(f"  plan: not read ({plan_reason})")
        reading, time_reason = TimeReading(section_read=False), ""
    else:
        reading, time_reason = read_time(plan)
    if reading.section_read:
        for record in reading.attempts:
            out.append(
                f"  attempt: {record.verb} · attempt {record.attempt} · route {record.route}"
                f" · model {record.model} · {record.result}"
            )
        out.append(f"  time recorded: {reading.seconds} s")
        if reading.unread:
            out.append(f"  unread lines: {reading.unread} — the time subtotal is incomplete")
    elif plan_text is not None:
        out.append(f"  time: not read ({time_reason})")
    findings_text, findings_reason = read_text(folder / "findings.md")
    if findings_text is None:
        out.append(f"  calls: not read ({findings_reason})")
    else:
        rows = call_rows(findings_text)
        out.extend(rows)
        if rows:
            out.append("  (the call lines are evidence of a call, not measured attempts)")
    appetite = None
    if plan_text is not None:
        appetite = appetite_seconds(card_appetite_value(plan_text))
    if appetite is None:
        out.append("  appetite not read (the opening card gives no readable positive budget)")
        return out
    out.append(f"  appetite: {appetite} s (from the opening card)")
    if not reading.section_read:
        return out  # no comparison without time: no ratio, no threshold verdict
    if reading.seconds * 2 >= appetite:
        out.append(
            f"  warn: recorded time {reading.seconds} s is at or over half the appetite"
            f" (half: {appetite // 2} s) — advice on the snapshot, not a stop"
        )
    elif reading.unread:
        out.append(
            f"  note: the time subtotal is incomplete (unread lines: {reading.unread});"
            " the comparison with the appetite is open, and no free budget is claimed"
        )
    return out


def live_block(run: RunCommand, proc_dir: Path | None, changes: frozenset[str]) -> list[str]:
    """The live figures: one process table read and the platform's memory sources."""
    out = ["live figures:"]
    try:
        rows = parse_processes(run(["ps", "-axo", "pid,etime,command"]), changes)
    except SourceError as error:
        out.append(f"  processes: {error}")
    else:
        out.append("  processes:")
        if rows:
            out.extend(f"    pid {row.pid} · {row.label} · change {row.change} · elapsed {row.elapsed}" for row in rows)
        else:
            out.append("    none matched")
    snapshot = macos_memory(run) if proc_dir is None else linux_memory(proc_dir)
    out.append("  memory:")
    out.append(f"    available: {snapshot.available}")
    out.append(f"    compressed: {snapshot.compressed}")
    if snapshot.available_percent is not None and snapshot.available_percent < MEMORY_FLOOR:
        out.append(
            f"  warn: available memory {snapshot.available_percent:g}% is below the"
            f" {MEMORY_FLOOR:g}% floor — advice before starting a step that runs verification;"
            " this report starts, stops and blocks nothing"
        )
    return out


def report_text(
    root: Path,
    selection: str | None,
    *,
    run: RunCommand = run_command,
    proc_dir: Path | None = None,
) -> str:
    """The whole report as text; sources fail independently and the exit stays zero."""
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [f"run report — {stamp} (UTC snapshot · local, read-only · not a gate)"]
    unread: list[str] = []
    try:
        names = active_changes(root, unread)
    except SourceError as error:
        names = []
        lines.append(f"change list: {error}")
    lines.extend(unread)
    known = frozenset(names)
    if selection is None:
        chosen = names
    elif selection in known:
        chosen = [selection]
    else:
        chosen = []  # an invalid selection never falls back to all changes
        lines.append(f"selection: not an active change (asked: '{_bounded(selection)}')")
    for name in chosen:
        lines.extend(change_block(root / CHANGES_DIR / name, name))
    where = proc_dir if proc_dir is not None else (None if sys.platform == "darwin" else Path("/proc"))
    lines.extend(live_block(run, where, known))
    return "\n".join(lines)


def main(argv: list[str] | None = None, *, run: RunCommand = run_command, proc_dir: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument("--change", default="", help="report only this active change (default: all)")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="repository root (default: this checkout)")
    args = parser.parse_args(argv)
    selected = args.change.strip() or (os.environ.get("CHANGE") or "").strip() or None
    try:
        text = report_text(args.root, selected, run=run, proc_dir=proc_dir)
    except Exception as error:  # a report never crashes: the class name is the bounded diagnostic
        print(f"run report: not printed (internal error: {type(error).__name__})")
        return 0
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
