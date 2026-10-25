---
title: "Decisions — tolerate-derived-leftovers"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-b5w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# tolerate-derived-leftovers — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · What a second run does with a failed run's derived writes

context: |
  Topic: the pre-existing-change check of implement, draft and repair.
  Intention: a failed run's rendered index and date stamps blocked the
  next run of the same change (bead coding-harness-b5w).
  Today: every change outside findings.md refuses the run.
  Repository change: the check tolerates exactly the runner's own
  derived writes.
  Architecture change: none.
asked: 2026-10-16, conversation 2026-10-16 (interview, about 21:10)
answer: "(a) a second run may start on a failed run's tree; the runner tolerates its own derived writes"
answered_by: maintainer
status: answered

The answer was given in the conversation on 2026-10-16 and recorded in the
bead's notes the same evening; this record copies it from there.

In the context of the runner's pre-existing-change check, facing derived
writes a failed run leaves behind, we decided that the check tolerates
exactly the runner's own derived writes, to achieve that a second run starts
without a hand restore, accepting that a stamp-only change is committed
with the next run. — 2026-10-16
