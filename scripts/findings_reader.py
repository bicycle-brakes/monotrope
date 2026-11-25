#!/usr/bin/env python3
r"""findings_reader.py — the one reader of findings rows, statuses and attribution.

Every consumer of the findings records — the per-model report
(``scripts/findings_per_model.py``), the later metrics consumer (bead
coding-harness-nqaf) and the morning-handover table — reads rows through this
module, so the status vocabulary, the duplicate rule and the attribution rule
live in exactly one place (bead coding-harness-qut1, decisions Q-2 and Q-5).
The row and line shapes are the runner's own (``scripts/stage2.py`` writes
them); the constants below mirror the writer so a consumer can read without
importing the runner. A test pins the mirror against the writer.

The input grammar
-----------------

One grammar, written down once (phase-6 grammar review, maintainer
2026-11-20), and every path of this module reads through it: ``scan`` turns
the text into lines of one kind each, ``parse_findings`` and ``table_rows``
read only those lines. What does not match the grammar inside a counted
section is a ``Gap`` — the report is then incomplete and exits non-zero —
never a row skipped or counted in silence.

=================  ==========================================================
Element            Form
=================  ==========================================================
line               text split at LF, CRLF or a lone CR (CommonMark's line
                   endings); a leading byte-order mark is dropped; U+2028,
                   VT, FF and the other Unicode separators are cell text
front matter       line 1 ``---`` through the next ``---`` or ``...`` line:
                   opaque; unclosed is a gap
code fence         ```` ``` ```` or ``~~~`` (up to three spaces in) through a
                   closing run of the same character at least as long:
                   opaque; unclosed is a gap
HTML comment       a line beginning ``<!--`` (up to three spaces in) through
                   the first ``-->``: opaque; unclosed is a gap
heading            ATX: up to three spaces, ``#`` × 1–6, then a space or tab
                   or the line end; the text is trimmed and an optional
                   closing ``#`` run dropped. Its label is ``#`` × level,
                   one space, the text. Setext: a plain-text line with a
                   ``=`` (level 1) or ``-`` (level 2) underline below it; it
                   never opens a counted section. A heading of ANY level
                   ends the section before it.
phase-6 heading    level 2, ``Phase 6 — <who>, <date>``: ``<who>`` is one
                   or more characters, first and last not blank; ``<date>``
                   a calendar date ``YYYY-MM-DD``; the dash is U+2014
released heading   level 2, ``Phase 4b — loop rows, released <date>`` or
                   ``Phase 4b — GLM loop rows, released <date>``
near miss          a line starting with ``#`` whose text is one of the two
                   forms above once dashes, spaces and case are loosened,
                   but which is not that heading (another level, a hyphen or
                   en dash, no space after ``#``, an impossible date, the
                   setext form): a gap; the line is then read as what it is
call line          column 0, ``Stage-2 call, <date>: <verb> · … model <id>
                   · …``; a column-0 line beginning ``Stage-2 call`` in
                   another shape is a gap
kept line          ``Kept from the loop record:``: ends a released section
table line         up to three spaces, then ``|`` … ``|`` with the last pipe
                   unescaped; cells split at unescaped pipes (``\|`` and
                   ``\\|`` are cell text, as GitHub reads them) and
                   trimmed. A line beginning ``|`` without that end, or
                   indented four or more columns, is a broken table line
header             a table line whose first cell is ``ID`` (any case) or
                   whose cells 2–6 name Severity … Finding; in a counted
                   section it must be one of ``KNOWN_HEADERS`` and fixes
                   the width of the rows below it
separator          every cell ``:?-+:?``
row                any other table line; a blank line or another block ends
                   the table, a plain-text line directly below a row is a
                   gap (GitHub renders it as one more row)
=================  ==========================================================

Sections and rows. A counted section is a released section (it ends with
its first table, a kept line or the next heading) or a phase-6 section (it
ends at the next heading or kept line). In a counted section every row must
pass ``row_error`` — width 10 released, 7, 9 or 10 phase-6, matching its
header when one stands above; an id of ``ROW_ID`` form (``LOOP_ID`` when
released); no blank severity, dimension, origin (historical seven-cell
``CODE`` rows have none), location, finding, reviewer, test or Phase 6
cell; a status of the closed set. Severity, dimension and origin decide no
count, so their vocabulary is not the reader's to enforce (maintainer,
2026-11-20: the reader measures, a gate enforces). A row whose id begins
``2a-`` in a phase-6 section is never counted (criterion 19) and is listed
with the phase-2a tables. Outside a counted section, a table whose first
cell is a finding id stands outside the count (criterion 18) and is listed
under its heading of any level — "headingless" only before the first
heading — and never supplies a row's current state (decisions F-20).

Eligible rows (spec, criterion 1) are thus released loop rows and phase-6
rows; rejected phase-6 answers and phase-2a blocks are excluded because
their headings are not counted.
"""

from __future__ import annotations

import datetime
import re
from collections.abc import Iterator
from dataclasses import dataclass, field, replace

# A catalog id the runner may select: third-party catalog text never carries a `|` or other markup into
# the record's cells (DL-B-7 of the loop's deep review). Defined here, not in stage2_free.py, because this
# reader travels with the kit and the runner modules do not; stage2_free.py imports it from here.
MODEL_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]*")

# The runner's own row shapes (scripts/stage2.py writes them; the mirror is
# pinned by tests/test_findings_per_model.py::test_row_shapes_match_the_runner).
ROW_COLUMNS = ["ID", "Severity", "Dimension", "Origin", "Where", "Finding", "Reviewer", "Status", "Broke a test"]
RELEASED_COLUMNS = [*ROW_COLUMNS, "Phase 6"]
# The seven-column header of the template's Claude-path phase-6 table (templates/findings.md).
TEMPLATE_COLUMNS = ["ID", "Severity", "Dimension", "Origin", "Where", "Finding", "Status"]
KNOWN_HEADERS = {
    "released": (tuple(RELEASED_COLUMNS),),
    "phase6": (tuple(TEMPLATE_COLUMNS), tuple(ROW_COLUMNS), tuple(RELEASED_COLUMNS)),
}
ROW_WIDTHS = {"released": (10,), "phase6": (7, 9, 10)}
RELEASE_HEADING = "## Phase 4b — loop rows, released"
GLM_RELEASE_HEADING = "## Phase 4b — GLM loop rows, released"
_DATE = r"(?P<date>\d{4}-\d{2}-\d{2})"
RELEASE_HEADING_PATTERN = re.compile(rf"## Phase 4b — (?:GLM )?loop rows, released {_DATE}")
REJECTED_ANSWER_HEADING = "## Rejected phase-6 answer"
PHASE2A_HEADING = "## Phase 2a"
PHASE2A_ID_PREFIX = "2a-"
KEPT_FROM = re.compile(r"^Kept from the loop record:[ \t]*$")
LOOP_ID = re.compile(r"L\d+-\d+")
# The runner's phase-6 heading: `## Phase 6 — <who>, <date>`, any non-blank
# <who> of one character or more (F6-1). Older shapes (`## Phase 6, round 3
# (…)`, `## Phase 6 follow-up — …`) are not eligible (decisions F-13, F-20).
PHASE6_HEADING = re.compile(rf"## Phase 6 — (?P<who>\S(?:.*\S)?), {_DATE}")
# A near miss of the two counted headings: dashes, spaces and case loosened.
_LOOSE_DASH = "[-‐-―−]"
_LOOSE_DATE = rf"\d{{4}}\s*{_LOOSE_DASH}\s*\d{{1,2}}\s*{_LOOSE_DASH}\s*\d{{1,2}}"
NEAR_COUNTED_HEADING = re.compile(
    rf"#+\s*phase\s*(?:6\s*{_LOOSE_DASH}+\s*(?:\S(?:.*\S)?)?\s*,"
    rf"|4b\s*{_LOOSE_DASH}+\s*(?:glm\s+)?loop\s+rows\s*,?\s*released)"
    rf"\s*{_LOOSE_DATE}[\W_]*",
    re.I,
)
# The grammar's line forms (see the module docstring).
ATX_HEADING = re.compile(r" {0,3}(?P<marks>#{1,6})(?:[ \t]+(?P<text>.*?))??(?:[ \t]+#+)?[ \t]*")
FENCE = re.compile(r" {0,3}(?P<run>`{3,}|~{3,}).*")
FRONT_MATTER_END = ("---", "...")
LINE_ENDING = re.compile(r"\r\n|\r|\n")
COMMENT_OPEN = re.compile(r" {0,3}<!--")
COMMENT_CLOSE = "-->"
SETEXT_UNDERLINE = re.compile(r" {0,3}(?:=+|-+)[ \t]*")
# A line that starts another Markdown block and so ends a table without being a row.
BLOCK_START = re.compile(r" {0,3}(?:>|[-+*](?:[ \t]|$)|\d{1,9}[.)](?:[ \t]|$)|<|(?:[*_-][ \t]*){3,}$)")
SEPARATOR_CELL = re.compile(r":?-+:?")
# The audit line of one checked call (scripts/stage2.py `call_line` and
# `begin_work_call`); a `Stage-2 session` line is not a call.
CALL_LINE = re.compile(r"^Stage-2 call, (?P<date>\d{4}-\d{2}-\d{2}): (?P<rest>.*)$")
# A column-0 line meant as a call line: anything else in that shape is a gap.
CALL_PREFIX = re.compile(r"Stage-2 call(?:[,:]| \d)")
MODEL_FIELD = re.compile(r"·\s+model\s+(\S+)\s+·")
# Vendor-only labels found in legacy releases do not identify a model.
LEGACY_REVIEWER_NAMES = frozenset({"glm", "codex"})
# A row id in a first cell: tokens with a digit (`F-1`, `L2-2`, `RB-G7`, `2a-1`).
ROW_ID = re.compile(r"(?=[A-Za-z0-9._-]*\d)[A-Za-z0-9][A-Za-z0-9._-]*")
# Duplicate targets use exactly the same grammar as readable row IDs.
FINDING_ID = ROW_ID
DUPLICATE_MARKER = re.compile(r"\b(?:same\s+as|duplicate\s+of|repeats?\s+of|repeats?)", re.I)
DUPLICATE_REFERENCE = re.compile(
    rf"{DUPLICATE_MARKER.pattern}\s+(?:`(?P<quoted>{FINDING_ID.pattern})`|(?P<plain>{FINDING_ID.pattern}))", re.I
)
# Historical duplicate status cells measured from plans/ on 2026-11-25 (baseline 47a6ad4f).
# Exact cells are frozen: prose is evidence, not an open-ended target grammar.
LEGACY_DUPLICATE_STATUSES = {
    "fixed — not a test — duplicate of l3-7 in substance (the per-call refusal already runs through fixed_test_proof since round 3); the docstring now says what each leg proves": [
        "L3-7"
    ],
    "fixed — orchestrator hand edit 1e2de53c: same as l1-2": ["L1-2"],
    "fixed — orchestrator hand edit 74ba4f6a: same as l1-2": ["L1-2"],
    "fixed — orchestrator hand edit: same as l4-4": ["L4-4"],
    "fixed — tests/test_omnigent_deny_layers.py::test_start_hook_wires_reconciliation_before_prime; same as l1-1 and l1-3 (7c5d5b87)": [
        "L1-1",
        "L1-3",
    ],
    "rejected — duplicate of l1-1": ["L1-1"],
    "rejected — duplicate of l1-1 (orchestrator, 2026-10-26)": ["L1-1"],
    "rejected — duplicate of l1-1 (same per-line check)": ["L1-1"],
    "rejected — duplicate of l1-1 (same reviewer, same mechanism, same lines)": ["L1-1"],
    "rejected — duplicate of l1-10": ["L1-10"],
    "rejected — duplicate of l1-11": ["L1-11"],
    "rejected — duplicate of l1-12": ["L1-12"],
    "rejected — duplicate of l1-2 (same reviewer, same mechanism, same lines)": ["L1-2"],
    "rejected — duplicate of l1-2; workflow.md and decisions.md stay true once l1-2 is repaired (orchestrator, 2026-10-26)": [
        "L1-2"
    ],
    "rejected — duplicate of l1-3": ["L1-3"],
    "rejected — duplicate of l1-3 (orchestrator, 2026-10-26)": ["L1-3"],
    "rejected — duplicate of l1-4 (orchestrator, 2026-10-26)": ["L1-4"],
    "rejected — duplicate of l1-4 and l4-3: german reason cells are translated at their source, decisions/gates.yaml, in a pull request of its own (house rule 1, bead coding-harness-yim)": [
        "L1-4",
        "L4-3",
    ],
    "rejected — duplicate of l1-4, l4-3 and l6-4: german governance prose is translated in a pull request of its own, and new text is english (house rule 1, bead coding-harness-yim)": [
        "L1-4",
        "L4-3",
        "L6-4",
    ],
    "rejected — duplicate of l1-4, l4-3, l6-4 and l7-3: german governance prose is translated in a pull request of its own, and new text is english (house rule 1, bead coding-harness-yim)": [
        "L1-4",
        "L4-3",
        "L6-4",
        "L7-3",
    ],
    "rejected — duplicate of l1-4: german reason cells are translated at their source, decisions/gates.yaml, in a pull request of its own (house rule 1, bead coding-harness-yim)": [
        "L1-4"
    ],
    "rejected — duplicate of l1-5": ["L1-5"],
    "rejected — duplicate of l2-1": ["L2-1"],
    "rejected — duplicate of l2-1 (same _free_candidate filter)": ["L2-1"],
    "rejected — duplicate of l2-1 (same text, other reviewer).": ["L2-1"],
    "rejected — duplicate of l2-2 (same mechanism, other reviewer); repaired with l2-2.": ["L2-2"],
    "rejected — duplicate of l2-2 (same workflow.md sentence and test)": ["L2-2"],
    "rejected — duplicate of l2-3 (same defect in terms_problem)": ["L2-3"],
    "rejected — duplicate of l2-3 and l2-4 and l2-5: a held path (decisions/gates.yaml human-decided; templates/ and agents.md human-written, provenance.yaml); the exact text goes to the maintainer in the morning (bead coding-harness-qut1 notes)": [
        "L2-3",
        "L2-4",
        "L2-5",
    ],
    "rejected — duplicate of l2-4": ["L2-4"],
    "rejected — duplicate of l2-4 (same mechanism, same lines, other reviewer); repaired with l2-4 and l2-13.": [
        "L2-4"
    ],
    "rejected — duplicate of l2-5 and l4-3: agents.md is human-written (provenance.yaml); the exact text goes to the maintainer in the morning (bead coding-harness-qut1 notes)": [
        "L2-5",
        "L4-3",
    ],
    "rejected — duplicate of l2-5: agents.md is human-written (provenance.yaml); the exact text goes to the maintainer in the morning (bead coding-harness-qut1 notes)": [
        "L2-5"
    ],
    "rejected — duplicate of l2-7 (same mechanism: the partial batch makes the reuse planner list reused slots as not planned); repaired with l2-7.": [
        "L2-7"
    ],
    "rejected — duplicate of l6-1 (the same answer repeated by the reviewer).": ["L6-1"],
    "rejected — false: repeat of l1-6 and l3-3 with the same reason; the answer record keeps what was shown at answer time": [
        "L1-6",
        "L3-3",
    ],
    "rejected — false: repeat of l1-6; `shown` records the proposal as the maintainer saw it when answering, and the adr takes effect only with the decision pull request's merge": [
        "L1-6"
    ],
    "rejected — false: repeat of l5-2 with the same reason; the destination is judged at dispatch and at selection": [
        "L5-2"
    ],
    "rejected — repeats l2-2: the `run_codex` docstring now names the verbs a codex route may carry; the lookup stops before the call, and no route pairs implement with codex; a refusal message would be new runner scope, named in the pr as an accepted limit": [
        "L2-2"
    ],
    "rejected — same as l1-1": ["L1-1"],
    "rejected — same as l1-1 (fixed in abc123)": ["L1-1"],
    "rejected — same as l1-11": ["L1-11"],
    "rejected — same as l1-2": ["L1-2"],
    "rejected — same as l1-2: ac2 is met by storing a fallback as kind full; a full-fallback producer would be a new guarantee.": [
        "L1-2"
    ],
    "rejected — same as l1-3": ["L1-3"],
    "rejected — same as l1-5": ["L1-5"],
    "rejected — same as l1-5 (orchestrator, 2026-10-26)": ["L1-5"],
    "rejected — same as l1-5: findings.md that cannot be appended to stops every verb anyway, and the error being raised already ends the run (orchestrator, 2026-10-26)": [
        "L1-5"
    ],
    "rejected — same as l1-6": ["L1-6"],
    "rejected — same as l1-7": ["L1-7"],
    "rejected — same as l2-11: the q-1 record stays as answered; the pull request names the real size of the block as an accepted limit.": [
        "L2-11"
    ],
    "rejected — same as l3-1: scripts/ramp_valves.py does not travel with the kit (scripts/export/manifest.yaml: only scripts/kit/ and named files carry; everything else drops), so no kit instance runs it and criterion 4 is untouched; the framework behaviour is the deliberate decision of row l2-10": [
        "L3-1"
    ],
    "rejected — same as l3-2 and l4-4: the baseline is the orchestrator's measurement before the pull request (spec, definition of done)": [
        "L3-2",
        "L4-4",
    ],
    "rejected — same as l3-2: the baseline is the orchestrator's measurement after acceptance and before the pull request (spec, definition of done)": [
        "L3-2"
    ],
    "rejected — same as l5-1: the limit change is pull request #382, merged into this branch only so the runner can check this change; it leaves this diff once #382 is on main.": [
        "L5-1"
    ],
    "rejected — same as l5-3: accepted limit named in the pr; a reworded declaration fails loudly as not measured": [
        "L5-3"
    ],
    "rejected — same as l6-3: the old name would state the opposite of what the test asserts; the other change's findings are a historical record at their own commit": [
        "L6-3"
    ],
    "rejected — superseded by q-4: same as l8-1": ["L8-1"],
    "rejected — the same as l1-1: plan step 7, done by the orchestrator in 5eb38120": ["L1-1"],
}
# A pipe not escaped by a backslash; `\\|` counts as escaped, as GitHub reads it.
_PIPE = re.compile(r"(?<!\\)\|")

UNATTRIBUTED = "unattributed"
# One closed grammar for the whole status cell; suffixes carry historical reasons.
STATUS_CELL = re.compile(
    r"(?P<kind>accepted limit —|closed —|in spec|open|taken|fixed|resolved|answered|rejected)"
    r"(?!\w)(?P<detail>.*)",
    re.I | re.S,
)
OUTCOMES = ("raised", "defects_accepted", "questions_settled", "rejected")


def split_row(line: str) -> list[str] | None:
    """The cells of a complete table line, or None when the line is not one.

    A table line holds at most three spaces before its first pipe and ends with
    an unescaped pipe; cells split at unescaped pipes and are trimmed.
    """
    if table_line_error(line) is not None:
        return None
    stripped = line.strip()
    return [cell.strip() for cell in _PIPE.split(stripped[1:-1])]


def table_line_error(line: str) -> str | None:
    """Why a line beginning with a pipe is not a complete table line; None when it is one."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return "not a table line"
    lead = line[: len(line) - len(line.lstrip())]
    if lead.replace(" ", "") or len(lead) > 3:
        return "table line indented four or more columns (Markdown reads it as code)"
    if len(stripped) < 2 or not stripped.endswith("|") or stripped.endswith("\\|"):
        return "incomplete table row (missing final pipe)"
    return None


def is_separator(cells: list[str]) -> bool:
    """The separator line under a table header."""
    return all(SEPARATOR_CELL.fullmatch(cell) for cell in cells)


def is_header(cells: list[str]) -> bool:
    """A header line: first cell `ID`, or cells 2-6 naming Severity … Finding."""
    named = [cell.lower() for cell in cells[1:6]] == [column.lower() for column in ROW_COLUMNS[1:6]]
    return cells[0].lower() == "id" or named


def furniture(cells: list[str]) -> bool:
    """The header or the separator of a table."""
    return is_header(cells) or is_separator(cells)


def heading_kind(heading: str | None) -> str:
    """`released`, `phase6` or `other` for a heading label (`#` × level, a space, the text)."""
    if heading is None:
        return "other"
    for kind, pattern in (("released", RELEASE_HEADING_PATTERN), ("phase6", PHASE6_HEADING)):
        matched = pattern.fullmatch(heading)
        if matched is not None and _calendar_date(matched.group("date")):
            return kind
    return "other"


def _calendar_date(text: str) -> bool:
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        return False
    return True


@dataclass(frozen=True)
class Line:
    """One line of a findings.md as the grammar reads it.

    ``kind`` is one of ``opaque`` (front matter, code fences), ``blank``,
    ``heading``, ``call``, ``kept``, ``row`` (cells set), ``broken`` (a line
    beginning with a pipe that is no complete table line), ``block`` (another
    Markdown block) or ``text``. ``gap`` carries a grammar fault the line holds
    whatever its kind; ``reason`` explains a ``broken`` line.
    """

    position: int
    kind: str
    raw: str
    heading: str | None = None
    cells: tuple[str, ...] | None = None
    call: CallLine | None = None
    reason: str = ""
    gap: str = ""
    setext: bool = False  # a setext heading never opens a counted section


def physical_lines(text: str) -> list[str]:
    """The lines of a text: split at LF, CRLF or a lone CR (CommonMark's line endings), a leading BOM dropped."""
    if text.startswith("﻿"):
        text = text[1:]
    lines = LINE_ENDING.split(text)
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def scan(text: str) -> Iterator[Line]:
    """Every line of a findings.md, classified by the one grammar of this module."""
    lines = physical_lines(text)
    index = 0
    if lines and lines[0] == "---":
        end = next((at for at in range(1, len(lines)) if lines[at] in FRONT_MATTER_END), None)
        last = len(lines) if end is None else end + 1
        for at in range(last):
            gap = "unclosed front matter" if end is None and at == 0 else ""
            yield Line(at + 1, "opaque", lines[at], gap=gap)
        index = last
    fence: str | None = None
    comment = False
    opened = 0
    previous = "blank"
    at = index
    while at < len(lines):
        raw = lines[at]
        position = at + 1
        at += 1
        if fence is not None:
            closing = FENCE.fullmatch(raw)
            run = closing.group("run") if closing else ""
            if run and run[0] == fence[0] and len(run) >= len(fence) and not raw.strip().strip(fence[0]):
                fence = None
            yield Line(position, "opaque", raw)
            previous = "opaque"
            continue
        if comment:
            comment = COMMENT_CLOSE not in raw
            yield Line(position, "opaque", raw)
            previous = "opaque"
            continue
        opening = FENCE.fullmatch(raw)
        if opening is not None and not (
            opening.group("run")[0] == "`" and "`" in raw.strip()[len(opening.group("run")) :]
        ):
            fence, opened = opening.group("run"), position
            yield Line(position, "opaque", raw)
            previous = "opaque"
            continue
        if COMMENT_OPEN.match(raw):
            comment, opened = COMMENT_CLOSE not in raw[raw.index("<!--") + 4 :], position
            yield Line(position, "opaque", raw)
            previous = "opaque"
            continue
        line = _classify(raw, position)
        below_table, previous = previous in ("row", "broken"), line.kind
        if line.kind == "text" and not below_table and at < len(lines) and SETEXT_UNDERLINE.fullmatch(lines[at]):
            # A setext heading: the text line is the heading, the underline is not content.
            # Directly below a table the text line is one more row, never a heading.
            label = ("#" if "=" in lines[at] else "##") + " " + raw.strip()
            near = NEAR_COUNTED_HEADING.fullmatch("## " + raw.strip()) or heading_kind("## " + raw.strip()) != "other"
            gap = f"setext heading {raw.strip()!r} resembles a counted heading but is not its form" if near else ""
            yield Line(position, "heading", raw, heading=label, gap=gap, setext=True)
            yield Line(at + 1, "opaque", lines[at])
            at += 1
            previous = "heading"
            continue
        yield line
    if fence is not None:
        yield Line(len(lines), "opaque", "", gap=f"unclosed code fence opened at line {opened}")
    if comment:
        yield Line(len(lines), "opaque", "", gap=f"unclosed HTML comment opened at line {opened}")


def _classify(raw: str, position: int) -> Line:
    """One line outside front matter, code fences and HTML comments."""
    heading = ATX_HEADING.fullmatch(raw)
    if heading is not None:
        text = (heading.group("text") or "").strip()
        label = heading.group("marks") + (f" {text}" if text else "")
        near = NEAR_COUNTED_HEADING.fullmatch(raw.strip()) is not None and heading_kind(label) == "other"
        gap = f"heading {label!r} resembles a counted heading but is not its form" if near else ""
        return Line(position, "heading", raw, heading=label, gap=gap)
    near_gap = ""
    if raw.lstrip().startswith("#") and NEAR_COUNTED_HEADING.fullmatch(raw.strip()):
        near_gap = f"line {raw.strip()!r} resembles a counted heading but is not a Markdown heading"
    if not raw.strip():
        return Line(position, "blank", raw)
    if CALL_PREFIX.match(raw):
        call = parse_call_line(raw, position)
        if call is None:
            return Line(position, "text", raw, gap=f"unreadable call line {raw.strip()[:60]!r}")
        return Line(position, "call", raw, call=call)
    if KEPT_FROM.match(raw):
        return Line(position, "kept", raw)
    if raw.strip().startswith("|"):
        error = table_line_error(raw)
        if error is None:
            return Line(position, "row", raw, cells=tuple(split_row(raw) or ()))
        return Line(position, "broken", raw, reason=error)
    if BLOCK_START.match(raw):
        return Line(position, "block", raw, gap=near_gap)
    return Line(position, "text", raw, gap=near_gap)


def table_rows(text: str) -> Iterator[tuple[int, list[str]]]:
    """Every complete table row of any section whose first cell is a finding id, in file order.

    Headers, separators and rows without content are not finding rows; front
    matter and code fences hold none. The duplicate gate reads rows here.
    """
    for line in scan(text):
        if line.kind != "row" or line.cells is None:
            continue
        cells = list(line.cells)
        if furniture(cells) or not any(cells) or ROW_ID.fullmatch(cells[0]) is None:
            continue
        yield line.position, cells


def status_cell(cells: list[str]) -> str | None:
    """The Status cell of a readable row width; None when the width carries none."""
    if len(cells) == 7:
        return cells[6]
    if len(cells) in (9, 10):
        return cells[7]
    return None


def normalized_status(status: str) -> str:
    """The status compared by: trimmed, lowercased, whitespace collapsed."""
    return " ".join(status.strip().lower().split())


@dataclass
class StatusParse:
    outcome: str | None
    targets: list[str]
    known: bool
    names_id: bool


def parse_status(status: str) -> StatusParse:
    """Parse a complete status cell into its outcome and referenced duplicate IDs."""
    cell = " ".join(status.strip().split())
    names_id = any(not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item) for item in FINDING_ID.findall(cell))
    match = STATUS_CELL.fullmatch(cell)
    if not match:
        return StatusParse(None, [], False, names_id)
    kind = match.group("kind").lower()
    outcome = {
        "taken": "defects_accepted",
        "fixed": "defects_accepted",
        "closed —": "defects_accepted",
        "resolved": "questions_settled",
        "answered": "questions_settled",
        "in spec": "questions_settled",
        "rejected": "rejected",
    }.get(kind)
    detail = match.group("detail")
    ids = rf"{FINDING_ID.pattern}(?:\s+and\s+{FINDING_ID.pattern})*"
    # The canonical form ends its targets before the optional reason.
    canonical = re.fullmatch(rf"\s*—\s*duplicate\s+of\s+(?P<ids>{ids})(?::.*)?", detail, re.I)
    if kind == "rejected" and canonical:
        targets = FINDING_ID.findall(canonical.group("ids"))
    elif cell.lower() in LEGACY_DUPLICATE_STATUSES:
        targets = LEGACY_DUPLICATE_STATUSES[cell.lower()]
    else:
        # A named legacy marker outside the measured corpus is unreadable.
        marker = DUPLICATE_REFERENCE.search(cell)
        if marker and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", marker.group("quoted") or marker.group("plain")):
            return StatusParse(None, [], False, names_id)
        targets = []
    return StatusParse(outcome, sorted(set(targets)), True, names_id)


def status_outcome(status: str) -> str | None:
    """Return the outcome of a known status, or None for a raised-only status."""
    parsed = parse_status(status)
    return parsed.outcome if parsed.known else None


def known_status(status: str) -> bool:
    """Whether the complete status cell matches the closed grammar."""
    return parse_status(status).known


def duplicate_targets(status: str) -> list[str]:
    """Return the IDs referenced by a duplicate in a known status."""
    parsed = parse_status(status)
    return parsed.targets if parsed.known else []


def is_duplicate(status: str) -> bool:
    """Whether a known status names another row as a duplicate."""
    parsed = parse_status(status)
    return bool(parsed.known and parsed.targets)


# ---------------------------------------------------------------------------
# Parsed evidence: call lines, blocks, rows, tables outside the count
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CallLine:
    """One `Stage-2 call` audit line and what it names."""

    date: str
    verb: str
    model: str | None
    line: int


@dataclass(frozen=True)
class BlockIdentity:
    """What an attribution source receives (criterion 6, decisions F-17)."""

    change: str
    findings_file: str
    heading: str | None
    position: int
    preceding_calls: tuple[CallLine, ...]
    reviewer: str = ""


@dataclass
class RowRecord:
    """One eligible row and where it stands."""

    cells: list[str]
    line: int


@dataclass
class Block:
    """One eligible section with its rows."""

    identity: BlockIdentity
    kind: str  # "released" or "phase6"
    rows: list[RowRecord] = field(default_factory=list)


@dataclass
class OutsideTable:
    """Finding-id rows under a heading that is not counted (criterion 18)."""

    label: str
    line: int
    rows: int
    change: str
    path: str


@dataclass
class Gap:
    """Evidence the reader cannot resolve (criterion 16)."""

    path: str
    id: str | None
    reason: str


@dataclass
class Parsed:
    """What one findings.md holds at one commit."""

    blocks: list[Block]
    outside: list[OutsideTable]
    gaps: list[Gap]


def parse_call_line(line: str, position: int) -> CallLine | None:
    """The call line's date, verb and model; None when the shape is not the runner's."""
    matched = CALL_LINE.match(line)
    if matched is None:
        return None
    rest = matched.group("rest")
    verb = rest.split("·", 1)[0].strip()
    model_match = MODEL_FIELD.search(rest)
    return CallLine(matched.group("date"), verb, model_match.group(1) if model_match else None, position)


def row_error(cells: list[str], kind: str, header: tuple[str, ...] | None = None) -> str | None:
    """Validate a whole eligible row before any consumer can count it.

    ``header`` is the header line standing above the row in its table, if any:
    the row must then have its width.
    """
    widths = ROW_WIDTHS[kind]
    if len(cells) not in widths:
        return f"a {kind} row needs {' or '.join(map(str, widths))} cells, found {len(cells)}"
    if header is not None and len(header) != len(cells):
        return f"the row has {len(cells)} cells under a header of {len(header)}"
    id_pattern = LOOP_ID if kind == "released" else ROW_ID
    if not id_pattern.fullmatch(cells[0]):
        return f"unreadable {kind} finding id"
    # The reader measures, a gate enforces (maintainer, 2026-11-20): severity,
    # dimension and origin decide no count, so the reader asks only that they
    # are not blank — historical rows with a free vocabulary are counted.
    # Historical seven-cell CODE rows predate the Origin column: their final
    # three fields before Status are Where, Finding and Reviewer. A header
    # above the row names its columns, so only a row without one is read so.
    legacy = len(cells) == 7 and cells[2] == "CODE" and header is None
    for index, name in (
        ((1, "severity"), (2, "dimension"), (3, "location"), (4, "finding"), (5, "reviewer"))
        if legacy
        else ((1, "severity"), (2, "dimension"), (3, "origin"), (4, "location"), (5, "finding"))
    ):
        if not cells[index].strip():
            return f"blank {name}"
    if len(cells) >= 9 and any(not cells[index].strip() for index in (6, 8)):
        return "blank reviewer or test field"
    if len(cells) == 10 and not cells[9].strip():
        return "blank phase 6 field"
    status = status_cell(cells) or ""
    if not known_status(status):
        return f"unknown status {status!r} (the known set is closed)"
    return None


COUNTED = ("released", "phase6")
# Outside tables that group across headings (criterion 18); every other
# heading is its own group, so two equal headings stay two entries.
GROUPED_OUTSIDE = (
    (PHASE2A_HEADING, "phase-2a tables"),
    (REJECTED_ANSWER_HEADING, "rejected phase-6 answer tables"),
)


@dataclass
class Section:
    """The innermost heading, its kind and the table being read under it."""

    heading: str | None = None
    position: int = 0
    kind: str = "other"
    table_started: bool = False  # a released section ends with its first table
    in_table: bool = False  # the line before was a table line of this section
    header: tuple[str, ...] | None = None


def parse_findings(text: str, *, change: str, path: str) -> Parsed:
    """The eligible rows, the outside tables and the gaps of one findings.md, read by ``scan``."""
    blocks: list[Block] = []
    gaps: list[Gap] = []
    calls: list[CallLine] = []
    groups: dict[tuple[str, int], OutsideTable] = {}
    section = Section()
    last_release_heading = 0
    last_phase6_heading = 0

    def gap(row_id: str | None, position: int, reason: str) -> None:
        gaps.append(Gap(path, row_id, f"line {position}: {reason}"))

    def outside(position: int, *, grouped: str | None = None) -> None:
        # criterion 18: a finding table under a heading that is not counted stands
        # outside the count with its heading of any level; "headingless" only
        # before the first heading (F6-2).
        if grouped is not None:
            key = (grouped, 0)
        elif section.heading is None:
            key = ("headingless tables", 0)
        else:
            key = next(((label, 0) for prefix, label in GROUPED_OUTSIDE if section.heading.startswith(prefix)), None)
            key = key or (section.heading, section.position)
        group = groups.get(key)
        if group is None:
            groups[key] = OutsideTable(key[0], position, 1, change, path)
        else:
            group.rows += 1

    for line in scan(text):
        position = line.position
        if line.gap:
            gap(None, position, line.gap)
        if section.in_table and line.kind not in ("row", "broken"):
            # The table ends here. A plain-text line directly below a row is
            # one more row to a Markdown reader, so a counted section cannot
            # pass it by; a released section ends with its first table.
            if line.kind == "text" and section.kind in COUNTED:
                gap(None, position, "a plain-text line directly below a table row (Markdown renders it as a row)")
            if section.kind == "released":
                section.kind = "other"
            section.in_table, section.header = False, None
        if line.kind == "heading":
            section = Section(
                heading=line.heading, position=position, kind="other" if line.setext else heading_kind(line.heading)
            )
            if section.kind in COUNTED:
                window = last_phase6_heading if section.kind == "phase6" else last_release_heading
                preceding = tuple(call for call in calls if call.line > window)
                blocks.append(Block(BlockIdentity(change, path, section.heading, position, preceding), section.kind))
                if section.kind == "released":
                    last_release_heading = position
                else:
                    last_phase6_heading = position
            continue
        if line.kind == "kept":
            section.kind = "other"
            continue
        if line.kind == "call" and line.call is not None:
            calls.append(line.call)
            continue
        if line.kind not in ("row", "broken"):
            continue
        section.in_table = True
        section.table_started = True
        counted = section.kind in COUNTED
        if line.kind == "broken":
            if counted:
                first = _PIPE.split(line.raw.strip()[1:], maxsplit=1)[0].strip()
                gap(first if ROW_ID.fullmatch(first) else None, position, line.reason)
            continue
        cells = list(line.cells or ())
        if is_separator(cells):
            continue
        if is_header(cells):
            section.header = tuple(cells)
            known = {tuple(column.lower() for column in header) for header in KNOWN_HEADERS.get(section.kind, ())}
            if counted and tuple(cell.lower() for cell in cells) not in known:
                gap(None, position, f"unknown {section.kind} table header {' | '.join(cells)!r}")
            continue
        if not any(cells):
            if counted:
                gap(None, position, "a table row without content")
            continue
        if counted:
            if section.kind == "phase6" and cells[0].startswith(PHASE2A_ID_PREFIX):
                outside(position, grouped="phase-2a tables")  # criterion 19: listed, never counted
                continue
            error = row_error(cells, section.kind, section.header)
            if error is not None:
                gap(cells[0] if ROW_ID.fullmatch(cells[0]) else None, position, error)
            else:
                blocks[-1].rows.append(RowRecord(cells, position))
            continue
        if ROW_ID.fullmatch(cells[0]):
            outside(position)
    return Parsed(blocks, [groups[key] for key in sorted(groups)], gaps)


# ---------------------------------------------------------------------------
# Attribution
# ---------------------------------------------------------------------------


class AttributionSource:
    """The interface a later event-log source implements (decisions Q-2, F-17).

    A source receives the change, the findings file, the block heading, the
    block's position and the call lines directly preceding it, and returns a
    model id or ``unattributed``. Consumers pass a source to ``read_change``
    and never change their calls when the source is replaced.
    """

    def attribute(self, block: BlockIdentity) -> str:
        raise NotImplementedError


class LegacyAttributionSource(AttributionSource):
    """The first implementation: the record's own position decides (decisions F-12, F-21, F-23).

    A released loop block: exactly one distinct review-loop model belonging to
    the row’s vendor supplies the model. A
    phase-6 block: the nearest directly preceding call line must itself carry
    the verb exactly ``review`` — any other verb, a call across another
    phase-6 block, or no call leaves the block unattributed.
    """

    def attribute(self, block: BlockIdentity) -> str:
        if block.heading is None:
            return UNATTRIBUTED
        kind = heading_kind(block.heading)
        released, phase6 = kind == "released", kind == "phase6"
        if not released and not phase6:
            return UNATTRIBUTED
        if not block.preceding_calls:
            return UNATTRIBUTED
        if released:
            vendor = block.reviewer.strip().lower()
            models = {
                call.model
                for call in block.preceding_calls
                if vendor
                and call.verb == "review-loop"
                and call.model
                and re.match(rf"^{re.escape(vendor)}(?:[-._+]|\d|$)", call.model.lower())
            }
            return next(iter(models)) if len(models) == 1 else UNATTRIBUTED
        nearest = block.preceding_calls[-1]
        if phase6 and nearest.verb != "review":
            return UNATTRIBUTED
        return nearest.model or UNATTRIBUTED


@dataclass
class AttributedRow:
    """One eligible row and the model the reader attributes it to."""

    change: str
    path: str
    id: str
    model: str | None
    status: str
    line: int


def attribute_rows(parsed: Parsed, *, source: AttributionSource | None = None) -> list[AttributedRow]:
    """The model of every eligible row, through the shared reader (criterion 3).

    A released row whose Reviewer cell names a model is that model's; anything
    else — vendor-only cells and every phase-6 row — goes through the source.
    """
    chosen = source if source is not None else LegacyAttributionSource()
    rows: list[AttributedRow] = []
    for block in parsed.blocks:
        for record in block.rows:
            reviewer = ""
            if len(record.cells) == len(RELEASED_COLUMNS):
                reviewer = record.cells[ROW_COLUMNS.index("Reviewer")]
            if (
                block.kind == "released"
                and MODEL_ID.fullmatch(reviewer)
                and reviewer.lower() not in LEGACY_REVIEWER_NAMES
            ):
                model: str | None = reviewer
            else:
                answer = chosen.attribute(replace(block.identity, reviewer=reviewer))
                model = None if answer in (UNATTRIBUTED, "") else answer
            status = status_cell(record.cells) or ""
            identity = block.identity
            row = AttributedRow(identity.change, identity.findings_file, record.cells[0], model, status, record.line)
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Findings: one row per (change, id), duplicates resolved
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """One finding of one change: earliest row's model, latest row's status (criterion 2)."""

    change: str
    path: str
    id: str
    model: str | None
    status: str
    outcome: str | None
    duplicate: bool


@dataclass
class ReaderResult:
    """What one change's findings.md contributes to a report."""

    findings: list[Finding]
    gaps: list[Gap]
    outside: list[OutsideTable]


def resolve(rows: list[AttributedRow]) -> tuple[list[Finding], list[Gap]]:
    """Findings by (change, id) and the gaps of duplicate resolution (criteria 2, 7, 8, 16)."""
    by_key: dict[tuple[str, str], list[AttributedRow]] = {}
    for row in rows:
        by_key.setdefault((row.change, row.id), []).append(row)
    ids_by_change: dict[str, set[str]] = {}
    findings: list[Finding] = []
    for (change, finding_id), same in sorted(by_key.items()):
        same.sort(key=lambda row: row.line)
        earliest, latest = same[0], same[-1]
        ids_by_change.setdefault(change, set()).add(finding_id)
        duplicate = is_duplicate(latest.status)
        outcome = None if duplicate else status_outcome(latest.status)
        findings.append(Finding(change, latest.path, finding_id, earliest.model, latest.status, outcome, duplicate))
    gaps: list[Gap] = []
    edges: dict[tuple[str, str], list[str]] = {}
    paths: dict[tuple[str, str], str] = {}
    for finding in findings:
        paths[(finding.change, finding.id)] = finding.path
        if not known_status(finding.status):
            reason = f"row {finding.id}: unknown status {finding.status!r} (the known set is closed)"
            gaps.append(Gap(finding.path, finding.id, reason))
        if not finding.duplicate:
            continue
        targets = duplicate_targets(finding.status)
        known_ids = ids_by_change[finding.change]
        for target in targets:
            if target not in known_ids:
                reason = f"row {finding.id}: duplicate marker names row {target}, which the change has no row for"
                gaps.append(Gap(finding.path, finding.id, reason))
        edges[(finding.change, finding.id)] = [target for target in targets if target in known_ids]
    for cycle in _cycles(edges):
        first = cycle[0]
        chain = " -> ".join(name for _, name in cycle)  # the cycle already closes on its first node
        gaps.append(Gap(paths[first], first[1], f"duplicate cycle: {chain}"))
    return findings, gaps


def _cycles(edges: dict[tuple[str, str], list[str]]) -> list[list[tuple[str, str]]]:
    """Cycles of duplicate references, each reported once, deterministically (iterative DFS)."""
    WHITE, GREY, BLACK = 0, 1, 2
    color = {node: WHITE for node in edges}
    found: list[list[tuple[str, str]]] = []

    for start_node in sorted(edges):
        if color[start_node] != WHITE:
            continue
        color[start_node] = GREY
        path = [start_node]
        pos = {start_node: 0}
        stack: list[tuple[tuple[str, str], int]] = [(start_node, 0)]
        while stack:
            node, idx = stack[-1]
            targets = edges[node]
            if idx == len(targets):
                stack.pop()
                path.pop()
                del pos[node]
                color[node] = BLACK
                continue
            stack[-1] = (node, idx + 1)
            key = (node[0], targets[idx])
            if key not in edges:
                continue
            if color[key] == GREY:
                found.append([*path[pos[key] :], key])
            elif color[key] == WHITE:
                color[key] = GREY
                pos[key] = len(path)
                path.append(key)
                stack.append((key, 0))
    return found


def read_change(change: str, path: str, text: str, *, source: AttributionSource | None = None) -> ReaderResult:
    """The one read of one change's findings.md — the call every consumer keeps (criterion 6)."""
    parsed = parse_findings(text, change=change, path=path)
    findings, gaps = resolve(attribute_rows(parsed, source=source))
    return ReaderResult(findings, [*parsed.gaps, *gaps], parsed.outside)
