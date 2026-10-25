---
title: "Research — review-mixed-malformed-row"
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
tags: [research, stage-2, review-loop]
---

# review-mixed-malformed-row — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session on `fix/review-row-closing-pipe`
(`394c8c4`, pull request #236, stacked on #235), 2026-10-25.

## The finding

A runner audit at `378879a` (2026-10-21) reproduced without model calls:
an answer with one valid and one malformed row is accepted; after the
valid row was rejected, the loop reported clean, although the malformed
BLOCKER row was never decided (bead coding-harness-vque).

## What exists today

Read in `scripts/stage2.py` at `394c8c4`:

- `run_swarm` refuses an answer with **no** readable row and table lines
  (`MalformedTable`, #235) and reads an open six-cell row (#236).
- An answer **with** readable rows keeps every other line as text: the
  round quotes it under "not rows", and no row stands for it, so nothing
  makes the orchestrator decide it.
- `finding`-shaped lines are recognisable: their second cell is a
  severity (`SEVERITIES`), as `parse_rows` already uses to widen a long row.

## The maintainer's rule that covers it

The interview answer of 2026-10-16 for bead coding-harness-6jg reads:
"refuse — a round whose answer holds row-shaped lines with non-conforming
ids fails, and the refusal names the ids; no renumbering". The bead offers
two routes: fail the answer, or carry the line as an undecided row. Failing
the round is the route that answer already chose for unreadable finding
lines; carrying a line with the wrong cell count as a row would invent
cells.

## Sources

- Bead coding-harness-vque; bead coding-harness-6jg (notes, interview
  2026-10-16).
- `scripts/stage2.py` at `394c8c4`: `run_swarm`, `parse_rows`,
  `MalformedTable`, `review_loop`.
