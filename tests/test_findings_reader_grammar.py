"""The one input grammar of the shared findings reader (bead coding-harness-qut1).

Phase-6 rows F6-1 and F6-2 of the last re-check, and the grammar review the
maintainer asked for on 2026-11-20: one parametrized test per grammar element
of `scripts/findings_reader.py` (its module docstring holds the table). Every
input that does not match the grammar inside a counted section must be a gap,
never a row skipped or counted in silence. Criteria 1, 2, 16 and 18 of
plans/changes/findings-per-model/spec.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import findings_reader as fr  # noqa: E402

PHASE6 = "## Phase 6 — Codex, 2026-11-01"
RELEASE = "## Phase 4b — loop rows, released 2026-11-01"
HEADER9 = "| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |"
SEP9 = "|---|---|---|---|---|---|---|---|---|"


def row9(row_id: str = "F-1", status: str = "open", finding: str = "a finding") -> str:
    return f"| {row_id} | MAJOR | SPEC | base | x.py | {finding} | Codex | {status} | — |"


def lrow(row_id: str = "L1-1", status: str = "open") -> str:
    return f"| {row_id} | MAJOR | SPEC | base | x.py | a finding | hy3 | {status} | no | – |"


def doc(*parts: str) -> str:
    return "\n".join(parts) + "\n"


def read(text: str) -> fr.ReaderResult:
    return fr.read_change("c1", "plans/changes/c1/findings.md", text)


def ids(result: fr.ReaderResult) -> list[str]:
    return [finding.id for finding in result.findings]


# --- heading: the phase-6 heading -----------------------------------------------------


@pytest.mark.parametrize("who", ["X", "Codex", "Opus 5.5", "gpt-6.1-terra, re-check", "Ü"])
def test_phase6_heading_accepts_any_nonblank_reviewer(who):
    # F6-1: `## Phase 6 — X, 2026-11-20` heads a counted block; a one-character reviewer is a reviewer.
    result = read(doc(f"## Phase 6 — {who}, 2026-11-20", HEADER9, SEP9, row9()))
    assert ids(result) == ["F-1"], f"the block of reviewer {who!r} fell outside the count"
    assert result.gaps == [] and result.outside == []


@pytest.mark.parametrize(
    "heading",
    [
        "## Phase 6 — X, 2026-11-20   ",  # trailing spaces are not heading text
        "## Phase 6 — X, 2026-11-20 ##",  # an ATX closing run is not heading text
        "   ## Phase 6 — X, 2026-11-20",  # up to three spaces before the marks
        "##\tPhase 6 — X, 2026-11-20",  # a tab after the marks
    ],
)
def test_phase6_heading_spelling_variants_markdown_allows(heading):
    # phase-6 grammar review (maintainer, 2026-11-20): what Markdown reads as the runner's heading counts.
    result = read(doc(heading, row9()))
    assert ids(result) == ["F-1"] and result.gaps == []


# --- heading: a finding table is listed under its heading of any level ------------------


@pytest.mark.parametrize("level", [1, 2, 3, 4, 5, 6])
def test_outside_table_is_listed_under_its_heading_of_any_level(level):
    # F6-2: a table under `# Findings` (or any level) is listed under that heading, not as headingless.
    heading = "#" * level + " Findings — c1"
    result = read(doc(heading, "", row9("H-1", "fixed")))
    assert [(table.label, table.rows) for table in result.outside] == [(heading, 1)]
    assert result.findings == [] and result.gaps == []


@pytest.mark.parametrize(
    "prefix",
    [
        (),
        ("---", "title: x", "# a YAML comment, not a heading", "---"),
        ("Some prose before any heading.", ""),
    ],
)
def test_headingless_applies_only_before_the_first_heading(prefix):
    # F6-2: "headingless" is the label of a table before the first heading — front matter holds none.
    result = read(doc(*prefix, row9("H-1", "fixed"), "", "# Findings", "", row9("H-2", "fixed")))
    assert [(table.label, table.rows) for table in result.outside] == [
        ("# Findings", 1),
        ("headingless tables", 1),
    ]


@pytest.mark.parametrize(
    ("heading", "underline", "label", "gap"),
    [
        ("Findings — c1", "===", "# Findings — c1", False),
        ("Notes", "---", "## Notes", False),
        ("Notes", "-", "## Notes", False),
        ("Phase 6 — Codex, 2026-11-01", "---", "## Phase 6 — Codex, 2026-11-01", True),
    ],
    ids=["setext-1", "setext-2", "setext-short", "setext-phase6"],
)
def test_setext_heading_ends_a_section_and_never_counts(heading, underline, label, gap):
    # F6-2: a setext heading is a heading too — its table is listed under it, and it never opens a counted block.
    result = read(doc(PHASE6, row9("F-1"), "", heading, underline, "", row9("F-2", "fixed")))
    assert ids(result) == ["F-1"]
    assert [(table.label, table.rows) for table in result.outside] == [(label, 1)]
    assert bool(result.gaps) is gap


def test_level_one_heading_ends_a_counted_section():
    # F6-2: a heading of any level ends the section before it; its rows no longer count.
    result = read(doc(PHASE6, row9("F-1"), "", "# Appendix", "", row9("F-2", "fixed")))
    assert ids(result) == ["F-1"]
    assert [(table.label, table.rows) for table in result.outside] == [("# Appendix", 1)]


# --- heading: near misses of the counted headings are gaps ------------------------------


@pytest.mark.parametrize(
    "heading",
    [
        "## Phase 6 - Codex, 2026-11-20",  # hyphen-minus
        "## Phase 6 – Codex, 2026-11-20",  # en dash
        "## phase 6 — Codex, 2026-11-20",  # letter case
        "### Phase 6 — Codex, 2026-11-20",  # another level
        "##Phase 6 — Codex, 2026-11-20",  # no space: Markdown text, not a heading
        "## Phase 6 — Codex, 2026-13-45",  # not a calendar date
        "## Phase 6 — Codex,2026-11-20",  # no space before the date
        "## Phase 6 — , 2026-11-20",  # no reviewer
        "## Phase 6 — Codex, 2026-11-20.",  # trailing punctuation
        "## Phase\u00a06 \u2014 Codex,\u00a02026-11-20",  # no-break spaces
        "## Phase 4b - loop rows, released 2026-11-20",
        "## Phase 4b — loop rows, released 2026-02-30",
    ],
)
def test_near_miss_of_a_counted_heading_is_a_gap(heading):
    # phase-6 grammar review (maintainer, 2026-11-20): a heading that only resembles the runner's is a gap.
    result = read(doc(heading, row9(), lrow()))
    assert ids(result) == [], f"rows under {heading!r} were counted"
    assert any("resembles a counted heading" in gap.reason for gap in result.gaps), "the near miss passed silently"


@pytest.mark.parametrize(
    "heading",
    [
        "## Phase 6 — Sonnet 5.5, 2026-10-26 (re-check after R7)",
        "## Phase 6, round 3 (2026-10-06)",
        "## Phase 6 follow-up — Codex orchestrator, 2026-10-17",
    ],
)
def test_historical_phase6_like_headings_stay_outside_without_gap(heading):
    # phase-6 grammar review (maintainer, 2026-11-20): decided older shapes (F-13, F-20) are listed, not gaps.
    result = read(doc(heading, row9()))
    assert result.findings == [] and result.gaps == []
    assert [table.label for table in result.outside] == [heading]


# --- line: line breaks, byte-order mark, separators ------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        doc(PHASE6, HEADER9, SEP9, row9()).replace("\n", "\r\n"),
        doc(PHASE6, HEADER9, SEP9, row9()).replace("\n", "\r"),
        "﻿" + doc(PHASE6, row9()),
        doc(PHASE6, row9(finding="one two")),
        doc(PHASE6, row9(finding="one\x0btwo\x0cthree\x85four")),
        doc(PHASE6, row9() + "   \t"),
    ],
    ids=["crlf", "lone-cr", "bom", "line-separator-in-cell", "other-separators-in-cell", "trailing-whitespace"],
)
def test_line_forms(text):
    # phase-6 grammar review (maintainer, 2026-11-20): only LF (or CRLF) breaks a line.
    result = read(text)
    assert ids(result) == ["F-1"] and result.gaps == []


# --- front matter and code fences --------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "gap"),
    [
        (doc("---", "# yaml comment", "---", PHASE6, row9()), None),
        (doc(PHASE6, row9("F-1"), "", "```text", "# shell comment", row9("F-2"), "```", "", row9("F-3")), None),
        (doc(PHASE6, row9("F-1"), "", "~~~~", "```", row9("F-2"), "~~~~", row9("F-3")), None),
        (doc(PHASE6, row9("F-1"), "", "```", row9("F-2")), "unclosed code fence"),
        (doc("---", "title: x", PHASE6, row9("F-1")), "unclosed front matter"),
        (doc(PHASE6, row9("F-1"), "", "<!-- hidden", row9("F-2"), "-->", row9("F-3")), None),
        (doc(PHASE6, row9("F-1"), "", "<!-- hidden", row9("F-2")), "unclosed HTML comment"),
    ],
    ids=[
        "front-matter-comment",
        "backtick-fence",
        "tilde-fence-holds-backticks",
        "unclosed-fence",
        "unclosed-front",
        "comment",
        "unclosed-comment",
    ],
)
def test_front_matter_and_fences_are_opaque(text, gap):
    # phase-6 grammar review (maintainer, 2026-11-20): rows and headings inside a fence are code, not findings.
    result = read(text)
    assert "F-2" not in ids(result), "a row inside a code fence was counted"
    if gap is None:
        assert result.gaps == []
        assert "F-1" in ids(result)
    else:
        assert any(gap in g.reason for g in result.gaps), f"{gap} passed silently"


# --- table line: pipes, escapes, indentation -------------------------------------------


@pytest.mark.parametrize(
    ("line", "counted", "reason"),
    [
        (row9(finding=r"a \| b"), True, None),
        (row9(finding=r"a \\| b"), True, None),
        ("   " + row9(), True, None),
        (row9()[:-1], False, "missing final pipe"),
        (row9()[:-1] + "\\|", False, "missing final pipe"),
        ("    " + row9(), False, "indented four or more"),
        ("\t" + row9(), False, "indented four or more"),
    ],
    ids=["escaped-pipe", "escaped-backslash-pipe", "three-spaces", "no-final-pipe", "escaped-final-pipe", "4sp", "tab"],
)
def test_table_line_forms(line, counted, reason):
    # phase-6 grammar review (maintainer, 2026-11-20): a table line is complete or a gap, never skipped.
    result = read(doc(PHASE6, line))
    assert ids(result) == (["F-1"] if counted else [])
    if reason is None:
        assert result.gaps == []
    else:
        assert [gap.id for gap in result.gaps] == ["F-1"] and reason in result.gaps[0].reason


# --- header and separator ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("header", "row", "gap"),
    [
        (HEADER9, row9(), None),
        (HEADER9.lower(), row9(), None),
        (
            "| ID | Severity | Dimension | Origin | Where | Finding | Status |",
            "| F-1 | MAJOR | SPEC | base | x | y | open |",
            None,
        ),
        ("| ID | Severity | Finding | Status |", row9(), "unknown phase6 table header"),
        ("| ID | Severity | Dimension | Origin | Where | Finding | Status |", row9(), "under a header of 7"),
    ],
    ids=["runner-header", "header-case", "template-header", "unknown-header", "width-differs-from-header"],
)
def test_header_forms(header, row, gap):
    # phase-6 grammar review (maintainer, 2026-11-20): a header names the table; an unknown one is a gap.
    result = read(doc(PHASE6, header, SEP9, row))
    if gap is None:
        assert ids(result) == ["F-1"] and result.gaps == []
    else:
        assert any(gap in g.reason for g in result.gaps), f"{gap!r} passed silently"


# --- row: content, ids, cells, statuses -------------------------------------------------


@pytest.mark.parametrize(
    ("line", "gap"),
    [
        ("| | | | | | | | | |", "without content"),
        ("|  |", "without content"),
        (row9("F‑1"), "unreadable phase6 finding id"),  # non-breaking hyphen in the id
        (row9("F-1", "closed – merged"), "unknown status"),  # en dash in a historical form
        (row9("F-1", "**fixed**"), "unknown status"),
        (row9("F-1", "accepted limit - style"), "unknown status"),
    ],
    ids=["empty-row", "one-empty-cell", "unicode-hyphen-id", "en-dash-closed", "emphasis", "hyphen-accepted-limit"],
)
def test_row_forms_outside_the_grammar_are_gaps(line, gap):
    # phase-6 grammar review (maintainer, 2026-11-20): a row the grammar does not read is a gap.
    result = read(doc(PHASE6, row9("F-9"), line))
    assert ids(result) == ["F-9"]
    assert any(gap in g.reason for g in result.gaps), f"{line!r} passed silently"


def test_phase2a_rows_in_a_phase6_block_are_listed_not_counted():
    # phase-6 grammar review (maintainer, 2026-11-20): criterion 19 excludes them, criterion 18 lists them.
    result = read(doc(PHASE6, row9("2a-1", "answered"), row9("F-1")))
    assert ids(result) == ["F-1"] and result.gaps == []
    assert [(table.label, table.rows) for table in result.outside] == [("phase-2a tables", 1)]


# --- table end: blank lines, plain text, other blocks -----------------------------------


@pytest.mark.parametrize(
    ("parts", "counted", "outside", "gap"),
    [
        ((PHASE6, row9("F-1"), "", row9("F-2")), ["F-1", "F-2"], [], None),
        ((RELEASE, lrow("L1-1"), "", lrow("L1-2")), ["L1-1"], [(RELEASE, 1)], None),
        ((PHASE6, row9("F-1"), "a plain line Markdown renders as a row"), ["F-1"], [], "directly below a table row"),
        ((RELEASE, lrow("L1-1"), "plain"), ["L1-1"], [], "directly below a table row"),
        ((PHASE6, row9("F-1"), "plain", "---", row9("F-2")), ["F-1", "F-2"], [], "directly below a table row"),
        ((PHASE6, row9("F-1"), "> a quote"), ["F-1"], [], None),
        ((PHASE6, row9("F-1"), "- a list item"), ["F-1"], [], None),
        ((PHASE6, row9("F-1"), "---"), ["F-1"], [], None),
        ((PHASE6, row9("F-1"), "### Details", row9("F-2")), ["F-1"], [("### Details", 1)], None),
    ],
    ids=[
        "blank-in-phase6",
        "blank-in-release",
        "lazy-text",
        "lazy-text-release",
        "lazy-text-not-setext",
        "quote",
        "list",
        "rule",
        "h3",
    ],
)
def test_table_end_forms(parts, counted, outside, gap):
    # phase-6 grammar review (maintainer, 2026-11-20): where a table ends and what follows it.
    result = read(doc(*parts))
    assert ids(result) == counted
    assert [(table.label, table.rows) for table in result.outside] == outside
    if gap is None:
        assert result.gaps == []
    else:
        assert any(gap in g.reason for g in result.gaps)


# --- duplicate headings -----------------------------------------------------------------


@pytest.mark.parametrize("heading", [PHASE6, "## Notes"])
def test_duplicate_headings_stay_apart(heading):
    # phase-6 grammar review (maintainer, 2026-11-20): two equal headings are two sections.
    call = "Stage-2 call, 2026-11-01: review · model {} · route test"
    result = read(doc(call.format("m-1"), heading, row9("F-1"), "", call.format("m-2"), heading, row9("F-2")))
    if heading == PHASE6:
        assert {finding.id: finding.model for finding in result.findings} == {"F-1": "m-1", "F-2": "m-2"}
    else:
        assert [(table.label, table.line) for table in result.outside] == [(heading, 3), (heading, 7)]


# --- call line --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("line", "model", "gap"),
    [
        ("Stage-2 call, 2026-11-01: review · model m-1 · route test", "m-1", False),
        ("Stage-2 call 2026-11-01: review · model m-1 · route test", None, True),
        ("Stage-2 call, 11/01/2026: review · model m-1 · route test", None, True),
        ("Stage-2 call lines are the runner's audit lines.", None, False),
        ("> Stage-2 call, 2026-11-01: review · model m-1 · route test", None, False),
    ],
    ids=["runner-form", "no-comma", "other-date", "prose", "quoted"],
)
def test_call_line_forms(line, model, gap):
    # phase-6 grammar review (maintainer, 2026-11-20): a column-0 call line is the runner's or a gap.
    result = read(doc(line, "", PHASE6, row9()))
    assert result.findings[0].model == model
    assert bool(result.gaps) is gap


# --- the duplicate gate reads through the same grammar ----------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (doc(row9("F-1")), ["F-1"]),
        (doc("```", row9("F-1"), "```"), []),
        (doc("---", row9("F-1"), "---", row9("F-2")), ["F-2"]),
        (doc(HEADER9, SEP9, "| | | |", row9("F-3")), ["F-3"]),
    ],
    ids=["row", "fenced", "front-matter", "furniture-and-empty"],
)
def test_gate_rows_come_from_the_grammar(text, expected):
    # phase-6 grammar review (maintainer, 2026-11-20): the duplicate gate has no reader of its own.
    import check_finding_duplicates as gate  # noqa: F401 — the gate imports the reader's `table_rows`

    assert [cells[0] for _, cells in fr.table_rows(text)] == expected
