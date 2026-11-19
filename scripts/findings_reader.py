#!/usr/bin/env python3
"""findings_reader.py — the one reader of findings rows, statuses and attribution.

Every consumer of the findings records — the per-model report
(``scripts/findings_per_model.py``), the later metrics consumer (bead
coding-harness-nqaf) and the morning-handover table — reads rows through this
module, so the status vocabulary, the duplicate rule and the attribution rule
live in exactly one place (bead coding-harness-qut1, decisions Q-2 and Q-5).
The row and line shapes are the runner's own (``scripts/stage2.py`` writes
them); the constants below mirror the writer so a consumer can read without
importing the runner. A test pins the mirror against the writer.

Eligible rows (spec, criterion 1): released loop rows under
``## Phase 4b — loop rows, released <date>`` or the legacy GLM form
``## Phase 4b — GLM loop rows, released <date>`` (ten cells, loop id), and
phase-6 rows under the runner form ``## Phase 6 — <who>, <date>`` (seven,
nine or ten cells; pre-stage-2 files hold seven). Rejected phase-6 answers
and phase-2a blocks are excluded; a row whose id begins ``2a-`` never counts
in a phase-6 block (criterion 19). Tables under any other heading —
restatements included — stand outside the count (criterion 18) and never
supply a row's current state (decisions F-20).

Statuses are read from the leading word. The known set is closed (decisions
F-27): ``open``, ``taken``, ``fixed``, the historical ``closed —``,
``resolved``, ``answered``, ``in spec``, ``rejected`` and ``accepted limit
—``. ``open`` and ``accepted limit`` contribute only to raised (criteria 10,
16); ``taken``/``fixed``/``closed —`` are defects accepted, ``resolved``/
``answered``/``in spec`` are questions settled, ``rejected`` is rejected. A
status outside the set is a gap, never a guess (decisions Q-6).

A row is a duplicate when its status names another row id after ``same as``,
``duplicate of``, ``repeat``, ``repeats`` or ``repeat of``, matched without
regard to case (decisions Q-3, F-15); a marker without a row id is an
ordinary row. Duplicates earn nothing; a chain of markers credits only its
non-duplicate roots (decisions Q-4, F-14). A reference without a row and a
cycle of markers are gaps (criterion 16).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace

# The runner's own row shapes (scripts/stage2.py writes them; the mirror is
# pinned by tests/test_findings_per_model.py::test_row_shapes_match_the_runner).
ROW_COLUMNS = ["ID", "Severity", "Dimension", "Origin", "Where", "Finding", "Reviewer", "Status", "Broke a test"]
RELEASED_COLUMNS = [*ROW_COLUMNS, "Phase 6"]
RELEASE_HEADING = "## Phase 4b — loop rows, released"
GLM_RELEASE_HEADING = "## Phase 4b — GLM loop rows, released"
REJECTED_ANSWER_HEADING = "## Rejected phase-6 answer"
PHASE2A_HEADING = "## Phase 2a"
PHASE2A_ID_PREFIX = "2a-"
KEPT_FROM = re.compile(r"^Kept from the loop record:[ \t]*$")
LOOP_ID = re.compile(r"L\d+-\d+")
# The runner's phase-6 heading: `## Phase 6 — <who>, <date>`. Older shapes
# (`## Phase 6, round 3 (…)`, `## Phase 6 follow-up — …`) are not eligible
# (decisions F-13, F-20).
PHASE6_HEADING = re.compile(r"^## Phase 6 — \S.*\S, \d{4}-\d{2}-\d{2}$")
# The audit line of one checked call (scripts/stage2.py `call_line` and
# `begin_work_call`); a `Stage-2 session` line is not a call.
CALL_LINE = re.compile(r"^Stage-2 call, (?P<date>\d{4}-\d{2}-\d{2}): (?P<rest>.*)$")
MODEL_FIELD = re.compile(r"·\s+model\s+(\S+)\s+·")
# A model id, not a vendor: lowercase token with at least one digit
# (`glm-5.3-flash`, `gpt-6.1-terra`, `hy3`), never `GLM`, `Codex`, `Opus 5.5`
# (decisions F-21: the model comes from the call line, never a vendor cell).
MODEL_NAME = re.compile(r"(?=\S*\d)[a-z0-9][a-z0-9._+-]*")
# A row id in a first cell: tokens with a digit (`F-1`, `L2-2`, `RB-G7`, `2a-1`).
ROW_ID = re.compile(r"(?=[A-Za-z0-9._-]*\d)[A-Za-z0-9][A-Za-z0-9._-]*")
# The strict id shape of a duplicate reference (`L1-1`, `F6-2`): at least one
# hyphen segment ending in a digit. `Finding 3` names no row id (criterion 7).
FINDING_ID = re.compile(r"[A-Za-z0-9]{1,8}(?:-[A-Za-z]?\d+)+")
DUPLICATE_MARKER = re.compile(r"\b(?:same\s+as|duplicate\s+of|repeats?\s+of|repeats?)", re.I)
_PIPE = re.compile(r"(?<!\\)\|")

UNATTRIBUTED = "unattributed"
DEFECT_PREFIXES = ("taken", "fixed", "closed —")
QUESTION_PREFIXES = ("resolved", "answered", "in spec")
KNOWN_STATUS_PREFIXES = ("open", "accepted limit —", *DEFECT_PREFIXES, *QUESTION_PREFIXES, "rejected")
OUTCOMES = ("raised", "defects_accepted", "questions_settled", "rejected")


def split_row(line: str) -> list[str] | None:
    """The cells of a table line, or None when the line is not one (the runner's own rule)."""
    stripped = line.strip()
    if len(stripped) < 2 or not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    return [cell.strip() for cell in _PIPE.split(stripped[1:-1])]


def furniture(cells: list[str]) -> bool:
    """The header or the separator of a table (the runner's own rule)."""
    named = [cell.lower() for cell in cells[1:6]] == [column.lower() for column in ROW_COLUMNS[1:6]]
    return cells[0].lower() == "id" or named or all(re.fullmatch(r":?-+:?", cell) for cell in cells)


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


def starts_with_status(status: str, prefixes: tuple[str, ...]) -> bool:
    """Match complete leading status words, not longer words sharing a prefix."""
    return any(re.match(rf"{re.escape(prefix)}(?!\w)", status) for prefix in prefixes)


def status_outcome(status: str) -> str | None:
    """The outcome bucket of a known status; None for raised-only statuses.

    Callers that must tell an unknown status apart check ``known_status`` too.
    """
    lowered = normalized_status(status)
    if starts_with_status(lowered, ("open", "accepted limit —")):
        return None
    if starts_with_status(lowered, DEFECT_PREFIXES):
        return "defects_accepted"
    if starts_with_status(lowered, QUESTION_PREFIXES):
        return "questions_settled"
    if starts_with_status(lowered, ("rejected",)):
        return "rejected"
    return None


def known_status(status: str) -> bool:
    """Whether the status is in the closed set (decisions F-27); duplicates are known."""
    if is_duplicate(status):
        return True  # a marker with a row id is a recognized duplicate form
    return starts_with_status(normalized_status(status), KNOWN_STATUS_PREFIXES)


def duplicate_targets(status: str) -> list[str]:
    """The row ids a duplicate marker names, deduplicated, in deterministic order."""
    targets: set[str] = set()
    pattern = re.compile(
        rf"{DUPLICATE_MARKER.pattern}\s+({FINDING_ID.pattern}(?:\s+and\s+{FINDING_ID.pattern})*)",
        re.I,
    )
    for match in pattern.finditer(status):
        targets.update(
            target for target in FINDING_ID.findall(match.group(1)) if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", target)
        )
    return sorted(targets)


def is_duplicate(status: str) -> bool:
    """A duplicate names another row id with a marker; a marker without an id is none."""
    return bool(duplicate_targets(status))


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


def parse_findings(text: str, *, change: str, path: str) -> Parsed:
    """The eligible rows, the outside tables and the unreadable rows of one findings.md."""
    blocks: list[Block] = []
    gaps: list[Gap] = []
    calls: list[CallLine] = []
    groups: dict[str, OutsideTable] = {}
    heading: str | None = None
    kind = ""  # "", "released", "phase6", "other" (an eligible section ended by its kept-from line)
    last_release_heading = 0
    last_phase6_heading = 0
    prose = False
    release_table = False

    def outside(label: str, position: int) -> None:
        group = groups.get(label)
        if group is None:
            groups[label] = OutsideTable(label, position, 1)
        else:
            group.rows += 1

    for position, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            prose = False
            release_table = False
            heading = line
            if line.startswith(RELEASE_HEADING) or line.startswith(GLM_RELEASE_HEADING):
                kind = "released"
            elif PHASE6_HEADING.match(line):
                kind = "phase6"
            else:
                kind = "other"
            if kind in ("released", "phase6"):
                window = last_phase6_heading if kind == "phase6" else last_release_heading
                preceding = tuple(call for call in calls if call.line > window)
                blocks.append(Block(BlockIdentity(change, path, heading, position, preceding), kind))
                if kind == "released":
                    last_release_heading = position
                if kind == "phase6":
                    last_phase6_heading = position
            continue
        if re.match(r"^#{3,6}[ \t]+", line):
            heading = line
            kind = "other"
            prose = True
            continue
        if KEPT_FROM.match(line):
            kind = "other"
            prose = True
            continue
        if line.startswith("Stage-2 call, "):
            call = None if prose else parse_call_line(line, position)
            if call is not None:
                calls.append(call)
            continue
        cells = split_row(line)
        if kind == "released":
            if cells is not None:
                release_table = True
            elif release_table:
                kind = "other"
        if cells is None or furniture(cells):
            continue
        if not any(cell.strip() for cell in cells):
            continue  # a decorative line of empty cells is no row
        if kind == "released":
            if len(cells) == len(RELEASED_COLUMNS) and LOOP_ID.fullmatch(cells[0]):
                blocks[-1].rows.append(RowRecord(cells, position))
            else:
                reason = (
                    f"line {position}: a released loop row needs {len(RELEASED_COLUMNS)} cells "
                    f"and a loop id, found {len(cells)}"
                )
                gaps.append(Gap(path, cells[0], reason))
            continue
        if kind == "phase6":
            if cells[0].startswith(PHASE2A_ID_PREFIX):
                continue  # criterion 19: a phase-2a row never counts in a phase-6 block
            if len(cells) in (7, 9, 10):
                blocks[-1].rows.append(RowRecord(cells, position))
            else:
                row_id = cells[0] if ROW_ID.fullmatch(cells[0]) else None
                reason = f"line {position}: a phase-6 row needs 7, 9 or 10 cells, found {len(cells)}"
                gaps.append(Gap(path, row_id, reason))
            continue
        if kind in ("", "other") and ROW_ID.fullmatch(cells[0]):
            # criterion 18: a table whose first cell holds a finding id, under a heading
            # that is not counted, stands outside the count with its heading; a table
            # before any heading is labelled headingless.
            if heading is None:
                outside("headingless tables", position)
            elif heading.startswith(PHASE2A_HEADING):
                outside("phase-2a tables", position)
            elif heading.startswith(REJECTED_ANSWER_HEADING):
                outside("rejected phase-6 answer tables", position)
            else:
                outside(heading, position)
    return Parsed(blocks, [groups[label] for label in sorted(groups)], gaps)


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
        released = block.heading.startswith(RELEASE_HEADING) or block.heading.startswith(GLM_RELEASE_HEADING)
        phase6 = PHASE6_HEADING.match(block.heading) is not None
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
            if block.kind == "released" and MODEL_NAME.fullmatch(reviewer):
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
        if not finding.duplicate:
            if not known_status(finding.status):
                reason = f"row {finding.id}: unknown status {finding.status!r} (the known set is closed)"
                gaps.append(Gap(finding.path, finding.id, reason))
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
    """Cycles of duplicate references, each reported once, deterministically."""
    WHITE, GREY, BLACK = 0, 1, 2
    color = {node: WHITE for node in edges}
    found: list[list[tuple[str, str]]] = []

    def visit(node: tuple[str, str], path: list[tuple[str, str]]) -> None:
        color[node] = GREY
        path.append(node)
        for target in edges[node]:
            key = (node[0], target)
            if key not in edges:
                continue
            if color[key] == GREY:
                start = path.index(key)
                found.append([*path[start:], key])
            elif color[key] == WHITE:
                visit(key, path)
        path.pop()
        color[node] = BLACK

    for node in sorted(edges):
        if color[node] == WHITE:
            visit(node, [])
    return found


def read_change(change: str, path: str, text: str, *, source: AttributionSource | None = None) -> ReaderResult:
    """The one read of one change's findings.md — the call every consumer keeps (criterion 6)."""
    parsed = parse_findings(text, change=change, path=path)
    findings, gaps = resolve(attribute_rows(parsed, source=source))
    return ReaderResult(findings, [*parsed.gaps, *gaps], parsed.outside)
