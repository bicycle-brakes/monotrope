---
title: "Decisions — runner-preflight-gates"
category: decisions
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, runner-preflight]
---

# runner-preflight-gates — Decisions

Class: bounded (bead coding-harness-yv9i.3).

## Q-1 · Build this layer now, as its own bounded change

asked: 2026-11-23
answer: 'A — two small bounded P1 beads beside coding-harness-7ftj (maintainer, 2026-11-23, dialog in session c820a13d); this one: before the first model call of draft, implement and repair the runner runs the fast document gates on the starting tree and refuses with the gate's fix command, spending no call.'
answered_by: maintainer
status: answered
context: |
  Topic: preventing the failure of 2026-11-23, when an orchestrator hand edit of plans/changes/isolated-attempts/decisions.md left updated: stale and a draft spent three model attempts on a starting tree no draft may change.
  Intention: the fault should not depend on the orchestrator's care.
  Today: the runner runs the document gates only after a model attempt; a red starting tree fails every attempt.
  Repository change: a preflight step in scripts/stage2.py before the first model call; tests with a fake model that records calls.
  Architecture change: none.

In the context of a stale document date that cost three model attempts, facing a choice between two bounded layers, one note in bead coding-harness-7ftj, or the hook layer alone, we decided on two bounded P1 changes, of which this is one, to achieve a fix that holds for every harness and saves model calls, accepting two small changes instead of one larger feature — 2026-11-23
