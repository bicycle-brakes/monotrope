---
title: "Decisions — loop-state-block"
status: draft
implementation_status: partial
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-i70
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# loop-state-block — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · Where the runner keeps and reads its loop state

context: |
  Topic: the review loop's state line (which stages ran, which models are
  frozen) that the runner writes into the loop record and findings.md.
  Intention: a runner audit showed a forged state line in a phase-6
  reviewer's text was read as state and steered model selection (bead
  coding-harness-i70).
  Today: the runner matches a `Loop state:` line by pattern in text that can
  also hold reviewer words.
  Repository change: a marked runner-owned block; reviewer text is never
  parsed as state; a test with a forged line.
  Architecture change: none.
asked: 2026-10-22, conversation 2026-10-22 (joint window)
answer: "the runner writes its loop state into a clearly marked block of its own and reads state only from there; reviewer text is never parsed as state, whatever it contains"
answered_by: maintainer
status: answered

In the context of the review loop's state, facing reviewer text that can
carry a forged state line, we decided that the runner writes and reads its
state only in a clearly marked block of its own, to achieve that no reviewer
can steer model selection, accepting a format change of the loop record's
state line. — 2026-10-22
