#!/usr/bin/env python3
"""time_records.py - the one writer, parser and inserter of a plan's fixed time records.

The runner's attempts and the interactive session's measured spans share one
line format under `## Time used`, so the run report counts both without
interpreting prose (bead coding-harness-v6vk). The line is the existing runner
format; the closing marker stays "measured by the runner" and names the common
machine writer - a record with `route orchestrator` is the interactive
session's own measured span, not an extra model call.

Every record carries its explicit elapsed whole seconds; the UTC endpoints
only name the span, and a duration is never derived from them. This module is
independent of `stage2`: the runner, the `harness.py time-log` command and the
run report all import it, and none of them keeps a second grammar.
"""

from __future__ import annotations

import os
import re
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

MARKER = "measured by the runner"
ACCEPTED = "accepted"
REJECTED = "rejected"
RESULTS = (ACCEPTED, REJECTED)
STAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

TIME_HEADING = re.compile(r"^## Time used[ \t]*$", re.M)
FOLLOWING_HEADING = re.compile(r"^## [^#]", re.M)
RECORD = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<start>\d{2}:\d{2}:\d{2})"
    r"–(?:(?P<end_date>\d{4}-\d{2}-\d{2}) )?(?P<end>\d{2}:\d{2}:\d{2}) UTC, "
    r"(?P<seconds>\d+) s — "
    r"(?P<verb>[^·]+?) · attempt (?P<attempt>\d+) · route (?P<route>[^·]+?)"
    r" · model (?P<model>[^·]+?) · (?P<result>accepted|rejected) · measured by the runner"
)

PUBLISH_CALLBACK = Callable[[Path, bytes], None]


class TimeSectionError(Exception):
    """The time section cannot be found or read; the message is the caller-facing reason."""


@dataclass(frozen=True)
class Record:
    """One readable record: the explicitly measured seconds and the metadata the fixed line carries."""

    seconds: int
    verb: str
    attempt: int
    route: str
    model: str
    result: str


def parse_stamp(value: str) -> datetime:
    """One `YYYY-MM-DDTHH:MM:SSZ` UTC reading, or `ValueError` naming the grammar."""
    if not isinstance(value, str):
        raise ValueError("a timestamp is one `YYYY-MM-DDTHH:MM:SSZ` UTC string")
    try:
        return datetime.strptime(value, STAMP_FORMAT).replace(tzinfo=UTC)
    except ValueError:
        raise ValueError(f"{value!r} is not a `YYYY-MM-DDTHH:MM:SSZ` UTC timestamp") from None


def _check_word(field: str, value: str) -> None:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise ValueError(f"{field} must be non-blank without leading or trailing whitespace")
    if "·" in value:
        raise ValueError(f"{field} must not carry the `·` separator")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"{field} must not carry control characters")


def format_entry(
    start: datetime,
    end: datetime,
    seconds: int,
    verb: str,
    attempt: int,
    route: str,
    model: str,
    result: str,
) -> str:
    """The fixed record line; a malformed field raises `ValueError` before any bytes exist.

    `seconds` is the explicitly measured duration and is never checked against
    the endpoints: they only name the span, and the end carries its date when
    that differs from the start's, so a span across midnight reads unambiguously.
    """
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise ValueError("start and end must be datetimes")
    if end < start:
        raise ValueError("end must not lie before start")
    if not isinstance(seconds, int) or isinstance(seconds, bool) or seconds < 0:
        raise ValueError("seconds must be a whole number of at least 0")
    if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 1:
        raise ValueError("attempt must be a whole number of at least 1")
    if result not in RESULTS:
        raise ValueError(f"result must be one of {', '.join(RESULTS)}")
    _check_word("verb", verb)
    _check_word("route", route)
    _check_word("model", model)
    end_date = f"{end:%Y-%m-%d} " if end.date() != start.date() else ""
    return (
        f"{start:%Y-%m-%d} {start:%H:%M:%S}–{end_date}{end:%H:%M:%S} UTC, {seconds} s — "
        f"{verb} · attempt {attempt} · route {route} · model {model} · {result} · {MARKER}"
    )


def parse_entry(line: str) -> Record | None:
    """One fixed-format record from one line, or None - the shared grammar of writer and report.

    A leading "- " bullet is not part of the record. A line without the exact
    form - the stamped span, the explicit seconds, the metadata and the marker
    - stays unread; prose never becomes a duration here.
    """
    body = line[2:].strip() if line.startswith("- ") else line
    matched = RECORD.fullmatch(body)
    if matched is None:
        return None
    return Record(
        seconds=int(matched.group("seconds")),
        verb=matched.group("verb").strip(),
        attempt=int(matched.group("attempt")),
        route=matched.group("route").strip(),
        model=matched.group("model").strip(),
        result=matched.group("result"),
    )


def section_text(path: Path) -> str:
    """The bytes below `## Time used` and before the next level-two heading (the runner's `time_log`)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise TimeSectionError(f"{path} cannot be read.") from error
    match = TIME_HEADING.search(text)
    if match is None:
        raise TimeSectionError(f"{path} has no `## Time used` heading.")
    following = FOLLOWING_HEADING.search(text[match.end() :])
    end = match.end() + following.start() if following else len(text)
    return text[match.end() : end]


def insert_entry(text: str, entry: str, *, prior: str | None = None) -> str:
    """`text` with `entry` as the last line of the time section, before the next level-two heading.

    With `prior`, the section body comes from that trusted text instead - the
    runner's recovery keeps its earlier records even when a model rewrote the
    plan, while everything else still comes from `text`.
    """
    match = TIME_HEADING.search(text)
    if match is None:
        raise TimeSectionError("the plan has no `## Time used` heading.")
    following = FOLLOWING_HEADING.search(text[match.end() :])
    end = match.end() + following.start() if following else len(text)
    body = text[match.end() : end]
    if prior is not None:
        previous = TIME_HEADING.search(prior)
        if previous is None:
            raise TimeSectionError("the pre-call plan has no `## Time used` heading.")
        next_heading = FOLLOWING_HEADING.search(prior[previous.end() :])
        previous_end = previous.end() + next_heading.start() if next_heading else len(prior)
        body = prior[previous.end() : previous_end]
    body = body.rstrip() or "\n"
    tail = text[end:]
    return text[: match.end()] + body + "\n" + entry + "\n" + (f"\n{tail}" if tail else "")


def publish_atomic(plan: Path, content: bytes) -> None:
    """Replace `plan` with `content`: temporary file, fsync, rename, directory fsync; the mode is kept.

    A failed publication leaves the plan's bytes as they were and removes the
    temporary file - a refused command never truncates its destination.
    """
    try:
        mode = plan.stat().st_mode & 0o7777
    except FileNotFoundError:
        plan.write_bytes(content)  # nothing earlier to lose; the process umask applies as for any new file
        return
    handle, name = tempfile.mkstemp(prefix=f".{plan.name}.", suffix=".tmp", dir=plan.parent)
    temporary = Path(name)
    try:
        with os.fdopen(handle, "wb") as out:
            out.write(content)
            out.flush()
            os.fsync(out.fileno())
        temporary.chmod(mode)
        temporary.replace(plan)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    directory = os.open(plan.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def write_entry(
    entry: str,
    plan: Path,
    *,
    text: str | None = None,
    prior: str | None = None,
    publish: PUBLISH_CALLBACK | None = None,
) -> bytes:
    """The one write operation for one record: insert, then publish once.

    `text` is the plan's current text; it is read from `plan` when omitted.
    `prior`, when given, is the trusted text whose time section the record
    joins - the runner's pre-call plan. `publish` receives the destination and
    the exact bytes; the default is `publish_atomic`. Returns the bytes a
    successful publish wrote, so a retry can keep them in its snapshot.
    """
    if text is None:
        text = plan.read_text(encoding="utf-8")
    content = insert_entry(text, entry, prior=prior).encode("utf-8")
    (publish if publish is not None else publish_atomic)(plan, content)
    return content
