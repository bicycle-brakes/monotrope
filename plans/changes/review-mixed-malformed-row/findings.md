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
