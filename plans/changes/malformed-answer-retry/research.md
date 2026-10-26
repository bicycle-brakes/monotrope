---
title: "Research — malformed-answer-retry"
status: draft
implementation_status: partial
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-70rw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, review-loop]
---

# malformed-answer-retry — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `379df54d`
(2026-10-26).

## The finding

A review-loop member whose answer is neither six-cell rows nor exactly
`No finding.` fails as "malformed finding output". When it is the round's
only answer, the whole round exits 1 and an orchestrator reruns it by hand.
Measured: four times between 2026-10-23 and 2026-10-26 (`longcat-2.0`
three times, `glm-5.3-flash` once); each plain rerun with the same model
passed (bead coding-harness-70rw).

## What exists today

Read in `scripts/stage2.py` at `379df54d`:

- `run_swarm` calls every member concurrently; its inner `one` raises
  `CallFailed("malformed finding output: …")` when `parse_rows` finds no
  row and the answer is not `No finding.`, and stores the error as the
  member's outcome.
- The round body checks every member's prompt with `checked_prompt` and
  writes its `call_line` before `run_swarm`; it counts the written call
  lines in `audited` for the no-round line (DL-A-6).
- A failed Flash member is replaced by a ladder model in the parent, after
  `run_swarm`: checked prompt, call line, `audited += 1`, then
  `run_swarm([nxt], …)` under the round's one deadline.
- `ANSWER_FORMAT` is the format instruction every review prompt ends with.

## Sources

- `scripts/stage2.py`, `prompts/04b-review-loop.md` at `379df54d`.
