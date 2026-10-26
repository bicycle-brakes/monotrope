---
title: "Decisions — malformed-answer-retry"
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
tags: [decisions]
---

# malformed-answer-retry — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · What the runner does with a malformed reviewer answer

context: |
  Topic: a review-loop reviewer whose answer is neither six-cell rows nor
  exactly "No finding.".
  Intention: such an answer fails the whole round, and a plain rerun with
  the same model has passed every time it was measured.
  Today: the member fails; a round without another answer exits 1.
  Repository change: the runner asks once more with the format reminder.
  Architecture change: none.
asked: 2026-10-24, conversation 2026-10-24 (interview)
answer: "The runner asks a reviewer whose answer is malformed once more with the format reminder and records both answers in the loop record; if the second answer is malformed too, the round fails as today"
answered_by: maintainer
status: answered

The answer was recorded in the bead's notes on 2026-10-24; this record
copies it from there. On 2026-10-26 the maintainer asked for this change
to be pulled forward.

In the context of the review loop, facing malformed answers that fail a
round a plain rerun would pass, we decided that the runner asks once more
with the format reminder, to achieve that a round survives one formatting
slip, accepting one more call per slip. — 2026-10-24

## Q-2 · Where the second call runs [DETAIL]

The retry runs in the parent after `run_swarm`, the way a Flash
replacement does: its prompt passes the leak check, its call line is
written and counted in `audited` before it starts, and it shares the
round's one deadline. Retrying inside `run_swarm`'s worker would call a
foreign model without a call line in `findings.md`.
