---
title: "Decisions — implement-route-file"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-9ycy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, implement, routing]
---

# implement-route-file — Decisions

Class: bounded (bead coding-harness-9ycy).

## Q-1 · Who may change the route file

asked: 2026-11-06
answer: "agent auf mein wort, aber es muss eine zentrales artifact dafür geben" — an agent edits the implement route on the maintainer's word in the conversation, as an ordinary pull request (no decision PR); the route file is the one central artifact for the implementer choice: it holds the current route and, per change, the date, the maintainer's stated words and the reason, so no ADR, WORKFLOW text or runner constant names the implementer.
answered_by: maintainer
status: answered
context: |
  Topic: which model implements is a runner constant (GLM 5.3 Flash) and named in ADR 0007; on 2026-11-05 the maintainer decided it moves to one central, plainly editable file and GLM 5.3 replaces Flash at once.
  Intention: Flash failed implementation in 5 of 6 changes on 2026-11-04; the lane is explored and needs this one answer for its spec.
  Today: every change of implementer would be an ADR change, so a decision PR.
  Repository change: a new file at the repository root that the runner reads; ADR and WORKFLOW only point to it.
  Architecture change: the model choice moves from a decision to configuration.

In the context of an implementer that changes often and today needs an ADR edit to change, facing slow model swaps and scattered mentions, we decided that an agent edits one central route file on the maintainer's word, the file recording each change with date, words and reason, to achieve minute-scale swaps with one place that tells the history, accepting that the swap is not a decision PR. — 2026-11-06

The one wording edit that removes the model name from the ADR text is part of this change and follows the same answer: an ordinary pull request (orchestrator's reading of the answer; the bead left it open).
