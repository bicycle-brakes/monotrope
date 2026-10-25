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

## Non-goals

- Carry an unreadable line as an undecided row (the bead's second route).
- Change how an answer without readable rows is handled (#235, #236).

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
