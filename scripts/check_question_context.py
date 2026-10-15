#!/usr/bin/env python3
"""check_question_context.py — every new answered record keeps its context.

Every question an agent puts to the maintainer carries its context before the
question (ADR 0018): Topic, Intention including why it comes up now, Today,
Repository change, Architecture change, the question last. A record answered
on or after the repository's adoption day keeps that context in its own
`context` field, so a later reader sees what the maintainer answered to.

This gate reads every `decisions.md` under live and archived change folders —
a change needs no spec for its records to be held. It inspects every block
`## Q-<id> · <title>` whose `status:` reads `answered`, counted record or
not, first occurrence or repeat, maintainer or agent. Fenced examples, skip
records, open questions and prose decisions are not records.

The cut-off is each answer's own recording day, read from exactly one em-dash
date (`— YYYY-MM-DD`) anywhere in the record's top-level decision statement
beginning `In the context of`, its wrapped lines joined first. A date inside the
context value, a field or a fence never dates an answer. The day comes from
`decisions/adoption.yaml` through `scripts/adoption.py` and from nowhere
else; the gate holds no date of its own. The adoption day itself is subject
(inclusive), and a changed answer carries its new recording day.

For a subject record the gate accepts one non-blank context text value — a
plain scalar or a multiline literal block. Missing, blank, duplicate, or a
non-text value (unquoted null, boolean, number, date, timestamp, collection)
is a finding.
Presence only: the gate does not grade wording, and fidelity to what was
shown stays a review duty. Absent or unreadable evidence — the adoption day,
a recording day that is missing, ambiguous or impossible, a file that cannot
be read — is not measured, never an exemption, and takes exit precedence over
findings. The gate writes nothing.

Usage:
    python3 scripts/check_question_context.py                # this repository
    python3 scripts/check_question_context.py --root DIR     # another tree (tests)
Exit: 0 = every subject record keeps its context, 1 = findings, 3 = could not measure.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adoption  # noqa: E402 — the one reader of the adoption record

REPO_ROOT = Path(__file__).resolve().parent.parent

# The id of this gate in decisions/gates.yaml: the key of its adoption day.
GATE = "question-context"

CHANGES_DIR = "plans/changes"
ARCHIVE = "archive"

# One interview record: `## Q-<id> · <title>`. The `## ` itself is split
# away before this matches; fence handling belongs to _records.
_RECORD = re.compile(r"^(Q-[^\s·]+)[ \t]*·[ \t]*(.*)$")

# CommonMark fences, the same rule check_criterion_ledger.py applies: a
# fenced example is documentation, never a record to hold.
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_FENCE_CLOSE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")

_STATEMENT = re.compile(r"^In the context of(?:\s|$)")
_CONTEXT_FIELD = re.compile(r"^context:(?P<rest>.*)$")
_BLOCK_INDICATOR = re.compile(r"^[|>](?:[0-9][+-]?|[+-]?[0-9]?)(?:[ \t]+#.*)?$")
_DECISION_DATE = re.compile(r"—[ \t]*([0-9]{4})-([0-9]{2})-([0-9]{2})")
_DATE_CONTINUATION = re.compile(r"(?:—[ \t]*)?(?:[0-9]{4}-[0-9]{2}-[0-9]{2})?$")
_FIELD = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*:")


class CannotMeasure(Exception):  # noqa: N818 — a verdict, not an error class
    """The question cannot be answered here. Exit 3, nothing measured."""


# ---------------------------------------------------------------------------
# reading a decisions.md
# ---------------------------------------------------------------------------


def _fenced(lines: list[str]) -> list[bool]:
    """Per line, whether it stands in a fenced code block (CommonMark fences)."""
    inside = [False] * len(lines)
    marker = ""
    length = 0
    for i, line in enumerate(lines):
        if marker:
            inside[i] = True
            closed = _FENCE_CLOSE.match(line)
            if closed and closed.group(1)[0] == marker and len(closed.group(1)) >= length:
                marker, length = "", 0
            continue
        opened = _FENCE.match(line)
        # CommonMark: the info string of a backtick fence holds no backtick
        # (tildes may); such a line opens nothing.
        if opened and not (opened.group(1)[0] == "`" and "`" in line[opened.end() :]):
            inside[i] = True
            marker, length = opened.group(1)[0], len(opened.group(1))
    return inside


def _records(text: str) -> list[tuple[str, list[tuple[int, str]], list[bool]]]:
    """Answered Q-records as (id, numbered body lines, per-line fence state),
    in document order.

    A record is every line from its `## Q-<id> · <title>` heading to the next
    `## ` heading or the end of the file; headings and content inside fences
    never start or fill a record. A block that is no Q-record — the ADR
    question, prose decisions, a skip record — is not a record even when it
    states `status: answered`. Every `status: answered` Q-record is returned —
    a repeated id and an agent-attributed answer are records here even though
    they count towards no interview minimum.

    This gate skips fenced content; the interview-minimums counting gate
    splits on `## ` headings and reads fields without fence awareness.
    The shared heading form does not make their record sets identical.
    """
    lines = text.splitlines()
    inside = _fenced(lines)
    records: list[tuple[str, list[tuple[int, str]], list[bool]]] = []
    record_id: str | None = None
    body: list[tuple[int, str]] = []
    marks: list[bool] = []
    for number, line in enumerate(lines):
        if not inside[number] and line.startswith("## "):
            if record_id is not None and _status(body, marks) == "answered":
                records.append((record_id, body, marks))
            matched = _RECORD.match(line[len("## ") :].rstrip())
            record_id = matched.group(1) if matched else None
            body = []
            marks = []
            continue
        if record_id is not None:
            body.append((number, line))
            marks.append(inside[number])
    if record_id is not None and _status(body, marks) == "answered":
        records.append((record_id, body, marks))
    return records


def _status(body: list[tuple[int, str]], marks: list[bool]) -> str:
    """The record's `status:` field, last occurrence wins, as the counting
    gate reads it; the empty string when the record states none. A `status:`
    inside a fence is example text, never the record's own field."""
    value = ""
    for position, (_, line) in enumerate(body):
        if marks[position]:
            continue
        if line.startswith("status:"):
            value = line[len("status:") :].strip()
    return value


def _recording_day(rel: str, record_id: str, body: list[tuple[int, str]], marks: list[bool]) -> date:
    """The day the answer was recorded, or CannotMeasure with the reason.

    Read from exactly one em-dash date (`— YYYY-MM-DD`) anywhere in the one
    top-level decision statement beginning `In the context of`, joining
    indented wraps and blank-separated dash/date continuations first. This
    change's own fifth answer splits the dash and date. Dates inside the
    context value, a field or a fence are not read.
    """
    statements: list[list[str]] = []
    for position, (_, line) in enumerate(body):
        if marks[position] or line[:1].isspace() or not _STATEMENT.match(line):
            continue
        paragraph = [line]
        separated = False
        for offset in range(position + 1, len(body)):
            if marks[offset]:
                break  # a fence ends the statement; its lines are never read
            following = body[offset][1]
            if not following.strip():
                separated = True
                continue
            if separated:
                # A blank normally ends the paragraph, except when its missing
                # dash/date marker continues on the next non-blank line.
                if _DECISION_DATE.search(" ".join(part.strip() for part in paragraph)):
                    break
                if not _DATE_CONTINUATION.fullmatch(following.strip()):
                    break
            if _FIELD.match(following) or following.startswith("#") or _STATEMENT.match(following):
                break
            paragraph.append(following)
            separated = False
        statements.append(paragraph)
    if not statements:
        raise CannotMeasure(
            f"{rel}: {record_id} — the record states no decision statement "
            "beginning `In the context of`; the recording day cannot be read"
        )
    if len(statements) > 1:
        raise CannotMeasure(
            f"{rel}: {record_id} — the record states {len(statements)} decision statements; "
            "the recording day is ambiguous"
        )
    joined = " ".join(statement.strip() for statement in statements[0])
    found = _DECISION_DATE.findall(joined)
    if not found:
        raise CannotMeasure(
            f"{rel}: {record_id} — no `— YYYY-MM-DD` date occurs in the decision statement; "
            "the recording day cannot be read"
        )
    if len(found) > 1:
        raise CannotMeasure(
            f"{rel}: {record_id} — the decision statement carries {len(found)} dates; the recording day is ambiguous"
        )
    try:
        return date(int(found[0][0]), int(found[0][1]), int(found[0][2]))
    except ValueError:
        raise CannotMeasure(
            f"{rel}: {record_id} — `{'-'.join(found[0])}` names no calendar day; the recording day is invalid"
        ) from None


def _context_findings(rel: str, record_id: str, body: list[tuple[int, str]], marks: list[bool]) -> list[str]:
    """Findings for the record's context field; empty when one non-blank
    text value stands. Presence only — wording and length are not graded."""
    fields: list[tuple[int, str]] = []
    for position, (_, line) in enumerate(body):
        if marks[position] or line[:1].isspace():
            continue
        matched = _CONTEXT_FIELD.match(line)
        if matched:
            fields.append((position, matched.group("rest").strip()))
    if not fields:
        return [
            f"{rel}: {record_id} — the answered record keeps no context; put what was shown "
            "when it was answered in its own field (`context: |` followed by the explanation)"
        ]
    if len(fields) > 1:
        return [f"{rel}: {record_id} — {len(fields)} context fields stand in one record; one record keeps one value"]
    position, rest = fields[0]
    if _BLOCK_INDICATOR.match(rest):
        text = _literal_block(body, position)
        if not text.strip():
            return [f"{rel}: {record_id} — the context value is an empty block; record the explanation that was shown"]
        return []
    # Resolve only the context value, never the Markdown record. Inspect the
    # parsed scalar's tag and value so comments cannot supply missing text,
    # and every collection form is rejected alike. Compose avoids constructing
    # typed values such as dates and timestamps.
    try:
        scalar = yaml.compose(rest, Loader=yaml.SafeLoader)
    except yaml.YAMLError:
        return [
            f"{rel}: {record_id} — the context value is not a readable text scalar; "
            "record the explanation that was shown"
        ]
    if scalar is None:
        return [f"{rel}: {record_id} — the context value is blank; record the explanation that was shown"]
    if not isinstance(scalar, yaml.ScalarNode) or scalar.tag != "tag:yaml.org,2002:str":
        return [f"{rel}: {record_id} — the context value is not text; record the explanation that was shown"]
    if not scalar.value.strip():
        return [f"{rel}: {record_id} — the context value is blank; record the explanation that was shown"]
    return []


def _literal_block(body: list[tuple[int, str]], position: int) -> str:
    """The content of a literal or folded block under `context:` at `position`,
    its indentation removed; blank lines after it belong to no value."""
    content: list[str] = []
    indents = []
    for _, line in body[position + 1 :]:
        if not line.strip():
            content.append("")
            continue
        if not line[:1].isspace():
            break
        content.append(line)
        indents.append(len(line) - len(line.lstrip()))
    if not indents:
        return ""
    edge = min(indents)
    return "\n".join(line[edge:] if line else "" for line in content).rstrip()


# ---------------------------------------------------------------------------
# the measurement
# ---------------------------------------------------------------------------


def _decision_files(root: Path) -> list[Path]:
    """Every `decisions.md` of a live or archived change folder, whether or
    not the change carries a spec — the records decide, not the folder's age
    or place."""
    changes = root / CHANGES_DIR
    if not changes.is_dir():
        return []
    files = sorted(path for path in changes.glob("*/decisions.md") if path.is_file())
    archive = changes / ARCHIVE
    if archive.is_dir():
        files.extend(sorted(path for path in archive.glob("*/decisions.md") if path.is_file()))
    return files


def measure(root: Path) -> tuple[list[str], list[str], int, int]:
    """Findings, not-measured evidence and the record counts; raises
    CannotMeasure when the adoption day cannot be read."""
    try:
        adoption_day = adoption.adopted_on(root, GATE)
    except adoption.NotRecorded as cannot:
        raise CannotMeasure(str(cannot)) from None

    findings: list[str] = []
    unmeasured: list[str] = []
    answered = 0
    subject = 0
    for path in _decision_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as cannot:
            unmeasured.append(f"{rel}: the file cannot be read ({cannot}); the gate cannot measure its records")
            continue
        for record_id, body, marks in _records(text):
            answered += 1
            try:
                day = _recording_day(rel, record_id, body, marks)
            except CannotMeasure as cannot:
                unmeasured.append(str(cannot))
                continue
            if day < adoption_day:
                continue  # the answer predates the rule and stays as it is
            subject += 1
            findings.extend(_context_findings(rel, record_id, body, marks))
    return findings, unmeasured, answered, subject


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="another tree (tests)")
    args = parser.parse_args()
    try:
        findings, unmeasured, answered, subject = measure(args.root)
    except CannotMeasure as cannot:
        print(f"question-context NOT MEASURED: {cannot} — exit 3, nothing measured.")
        return 3
    for line in [*unmeasured, *findings]:
        print(f"  - {line}")
    if unmeasured:
        print(f"question-context NOT MEASURED: {len(unmeasured)} unreadable evidence — exit 3, nothing measured.")
        return 3
    if findings:
        print(f"question-context: {len(findings)} finding(s) — exit 1.")
        return 1
    day = adoption.adopted_on(args.root, GATE)
    print(
        f"question-context ok: {answered} answered record(s) read, {subject} subject to the adoption day "
        f"{day.isoformat()} — every subject record keeps its context."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
