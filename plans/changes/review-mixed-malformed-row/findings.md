---
title: "Findings — review-mixed-malformed-row"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-vque
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — review-mixed-malformed-row

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: the
three cases of criterion 1 failed before the edit (the round was written
with the malformed line only quoted); criterion 2's guard passed before
and after. All 908 runner tests pass except the root-only one.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- A line with more than six cells and a severity is widened into a row by
  `parse_rows`, so it never reaches `finding_shaped` as leftover text.
- The header line `| ID | Severity | … |` has no severity in cell 2 and is
  furniture anyway; it does not refuse.

## Independent runner review, 2026-10-25

An Opus sub-agent of the orchestrating session reviewed the runner with all
open pull requests merged (read-only, in a separate context). Its row for
this change (introduced across #235 and #238, reachable through #236):

| ID | Severity | Finding | Status |
|---|---|---|---|
| R-2 | MAJOR | An answer whose only finding line has no closing pipe and the wrong cell count (`\| X9 \| BLOCKER \| CODE \| src/app.py:1`) is an ordinary failed member, not a malformed table, so a peer's `No finding.` leaves a clean round and the loop ends (reproduced). | fixed — tests/test_stage2.py::test_an_open_short_finding_line_alone_refuses_the_round |

`run_swarm` now counts finding-shaped lines among the table lines of an
answer without rows, so the round is refused.

## Pre-review by an Opus 5.5 subagent, 2026-10-25

At the maintainer's request, a read-only Opus 5.5 subagent reviewed this
change, including the merge of #236 into it, before the phase-6 Codex
review, which this container cannot reach. Phase 6 is still owed. It found
no blocker. The orchestrating session fixed or recorded every row.

- **P238-1 (MAJOR, spec divergence), fixed.** The R-2 fix changed how an
  answer without readable rows is handled, which a non-goal excluded, and
  no criterion covered it. The spec now has criterion 3 and a narrowed
  non-goal; the ledger names the R-2 test.
- **P238-2 (MINOR), fixed in part.** A decorated severity (`**BLOCKER**`,
  `BLOCKER:`) in cell 2 was not finding-shaped, so such a line dropped out
  undecided. `finding_shaped` now trims `*`, `_` and `:`. New cases in
  `tests/test_stage2.py::test_a_malformed_finding_row_beside_a_valid_one_refuses_the_round`
  and `::test_an_open_short_finding_line_alone_refuses_the_round`, red
  before. A missing ID column (severity in cell 1) stays uncaught, because
  criterion 2 keeps a summary table with the severity in cell 1; the spec
  lists it under known limits. `CRITICAL` is no severity in this workflow.
- **P238-3 (MINOR), recorded as by design.** A short table line with a
  severity in cell 2 beside rows refuses the round, also for a summary keyed
  by ID, a fenced format example or prose with pipes. The spec's known
  limits say so.
- **P238-4 (MINOR), not now.** Phase 6 and phase 2a do not use the check;
  listed under the spec's known limits.
- **P238-5 (NIT), not now.** The refusal says "table line(s) that are not
  six-cell rows" also for an unclosed finding line; it quotes the line, so
  the wording stays.
- The merge of #236 (`780140f`) was checked: both helpers are kept, and the
  adjusted planted line in `test_unreadable_answer_is_quoted_in_the_round`
  weakens no assertion.

## Deferred rows fixed, 2026-10-25

The maintainer asked to fix all runner defects the reviewers found. An Opus
5.5 subagent made these fixes at the orchestrator's direction, test first,
in the worktree of this change; nothing was committed. Red output: the new
tests run before the edit to `scripts/stage2.py` (`pytest -n 4`), 23 failed
and 6 passed. The 6 that passed are guards for the other side of each rule
and held before and after. Spec criteria 4 to 7 replace the matching
known limits.

- **P235-1, quoted or listed finding line (criterion 4), fixed.**
  `finding_shaped` strips nested blockquote and list markers (`>`, `-`, `*`,
  `+`, `1.`) before it looks for the leading `|`. A quoted or listed
  complete six-cell row is refused, not read (spec [DETAIL]). A line without
  a leading `|` stays out of scope (known limit). Tests:
  `tests/test_stage2.py::test_a_quoted_or_listed_finding_line_refuses_the_round`
  (14 cases, beside a row and alone). Red: all 14 failed with
  `assert 0 == 1`, because the round was written.
  `::test_a_line_without_a_leading_pipe_is_not_finding_shaped` is a guard
  and passed before and after.
- **P238-2, missing ID column (criterion 5), fixed.** A line with a
  decorated severity in cell 1 and at least four cells is finding-shaped.
  Tests: `::test_a_finding_without_its_id_column_refuses_the_round`. Red:
  3 of 3 failed with `assert 0 == 1`. The guard
  `::test_a_summary_keyed_by_severity_keeps_the_round` checks two- and
  three-cell summaries and passed before and after.
- **P238-3, fenced format example (criterion 6), fixed.** The new helper
  `_fence_blocks` follows `_fenced` in `scripts/check_criterion_ledger.py`
  but does not import it. The finding check skips a fenced block when
  `parse_rows` reads no row from it, and only when the answer has readable
  rows. `parse_rows` still reads rows inside fences, so a reviewer that
  fences its whole table keeps its findings (spec [DETAIL]). Tests:
  `::test_a_fenced_format_example_beside_rows_keeps_the_round`. Red: 3 of
  3 failed with `assert 1 == 0`, because the round was refused.
  `::test_parse_rows_reads_a_fenced_row_and_the_check_skips_only_an_example`
  was red with `AttributeError: module 'stage2' has no attribute
  'unread_finding_lines'`. The guard
  `::test_a_fenced_finding_table_with_a_malformed_line_still_refuses`
  checks a table fenced with its rows and a fenced line alone. It passed
  before and after.
- **P238-4, phases 6 and 2a (criterion 7), fixed.** Both phases now call
  the shared `unread_finding_lines`. When it finds a line, phase 6 appends
  its rejected phase-6 answer block and fails before any verdict. Phase 2a
  fails before it appends anything, as it does after a failed call, but
  only when the answer has readable rows. Without rows, its existing
  treatment stands: the lines are appended and named as table lines that
  are not rows, which
  `::test_table_lines_that_are_not_rows_are_never_reported_as_no_finding`
  pins. A first version that refused in both cases broke that test in the
  full-file run and was narrowed. Both
  failures name the lines (`unread_refusal`). The rejected-block sentence
  now says "neither six-cell findings alone nor exactly `No finding.`".
  Tests: `::test_phase6_refuses_a_malformed_finding_line_beside_rows` and
  `::test_spec_review_refuses_a_malformed_finding_line_beside_rows`. Red:
  both failed with `assert 0 == 1`, because the verdict or block was
  written. The guard `::test_spec_review_keeps_a_fenced_example_beside_rows`
  passed before and after.
