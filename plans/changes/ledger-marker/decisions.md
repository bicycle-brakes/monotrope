---
title: "Decisions — ledger-marker"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-7g6h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# ledger-marker — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · How a stale `not yet written` marker gets cleared

context: |
  Topic: the criterion ledger in a change's plan during a stage-2 run.
  Intention: an otherwise passing attempt failed only because its plan
  still marked an existing test as not yet written (bead coding-harness-7g6h).
  Today: the attempt must remove the marker itself, or the gate fails it.
  Repository change: the runner removes the marker of every test that
  exists before its own make verify.
  Architecture change: none.
asked: 2026-10-23, conversation 2026-10-23
answer: "the runner clears it before its own make verify, like it regenerates plans/INDEX.md and the frontmatter stamps - not a prompt instruction, not a format-only repair round"
answered_by: maintainer
status: answered

The answer was given in the conversation on 2026-10-23 and recorded in the
bead's description the same day; this record copies it from there.

In the context of a stage-2 attempt's post-run check, facing a plan that
still marks an existing test as not yet written, we decided that the runner
clears that marker before its own make verify, to achieve that a derivable
detail no longer fails a correct attempt, accepting that the runner edits
the plan's ledger lines. — 2026-10-23
