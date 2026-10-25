---
title: "Spec — review-mixed-malformed-row"
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
tags: [spec, stage-2, review-loop]
class: bounded
appetite: 1
adr_files: []
---

# Spec — review-mixed-malformed-row

A finding line the runner cannot read refuses the review round even when
the same answer holds readable rows, so it can never drop out undecided
and let the loop end clean (bead coding-harness-vque). Research:
`research.md`.

## Terms

- **Finding-shaped line:** a line that starts with `|` and has `BLOCKER`,
  `MAJOR` or `MINOR` (any case) in its second cell, closed or not.

## Acceptance criteria

1. An answer with a readable row and a finding-shaped line that is no row
   refuses the round with #235's refusal, naming the member and the line;
   no record is written.
   *Refuted by:* a written round, or a refusal without the member or line.
2. A table without a severity in cell 2 beside readable rows (a summary
   table) keeps the existing treatment: the round stands.
   *Refuted by:* a refusal of such an answer.
3. An answer whose only finding-shaped line is unclosed or has the wrong
   cell count refuses the round as in criterion 1, also without a readable
   row beside it. A severity decorated with `*`, `_` or a trailing `:`
   counts as a severity. Added after runner review R-2 and pre-review row
   P238-1, 2026-10-25.
   *Refuted by:* such an answer treated as an ordinary failed member, so a
   peer's `No finding.` ends the round clean.

## Non-goals

- Carry an unreadable line as an undecided row (the bead's second route).
- Change how an answer without any finding-shaped line is handled (#235,
  #236). Criterion 3 changes the case with one, on purpose.

## Known limits (2026-10-25)

- A line is finding-shaped only by a severity in cell 2. A finding whose
  ID column is missing (severity in cell 1) is not caught: a summary table
  with the severity in cell 1 must keep the round (criterion 2).
- By design, a 2-to-5-cell table line with a severity in cell 2 beside
  readable rows refuses the round, also when it is a summary keyed by ID,
  a format example in a code fence, or prose such as `| note | minor | …`.
  The table parser ignores fences as well.
- Phase 6 (`review`) and phase 2a read answers with `parse_rows` alone and
  do not use this check: a malformed line beside valid rows stays quoted
  text there. A shared check is a change of its own.

## Definition of Done

- Tests red before the edit; `PYTHON=.venv/bin/python3 make verify` green
  except the gates this container cannot run.
- The last commit carries `Closes-Bead: coding-harness-vque`.

## Open decisions

None open.

- [DETAIL] Refuse rather than carry: the 2026-10-16 answer on
  coding-harness-6jg (research).
- [DETAIL] Only finding-shaped lines refuse beside rows, so a reviewer's
  summary table does not throw away a paid round.
