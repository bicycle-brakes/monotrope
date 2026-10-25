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
