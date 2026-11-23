---
title: "Decisions — commit-hook-stamp"
category: decisions
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, commit-hook]
---

# commit-hook-stamp — Decisions

Class: bounded (bead coding-harness-yv9i.2).

## Q-1 · Build this layer now, as its own bounded change

asked: 2026-11-23
answer: 'A — two small bounded P1 beads beside coding-harness-7ftj (maintainer, 2026-11-23, dialog in session c820a13d); this one: the commit hook runs check_frontmatter_current.py --stamp on the staged held documents and re-stages them, for every harness and every human commit.'
answered_by: maintainer
status: answered
context: |
  Topic: preventing the failure of 2026-11-23, when an orchestrator hand edit of plans/changes/isolated-attempts/decisions.md left updated: stale and a draft spent three model attempts on a starting tree no draft may change.
  Intention: the fault should not depend on the orchestrator's care.
  Today: the pre-commit hook in .beads/hooks/ does not check frontmatter; the gate frontmatter-current only reports after the fact.
  Repository change: the pre-commit hook stamps staged held documents; a test with a temporary repository.
  Architecture change: none.

In the context of a stale document date that cost three model attempts, facing a choice between two bounded layers, one note in bead coding-harness-7ftj, or the hook layer alone, we decided on two bounded P1 changes, of which this is one, to achieve a fix that holds for every harness and saves model calls, accepting two small changes instead of one larger feature — 2026-11-23
