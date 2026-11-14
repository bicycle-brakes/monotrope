---
title: "Decisions — no-work-done"
category: decisions
status: draft
implementation_status: none
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-te7q
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, implement, post-run-check]
---

# no-work-done — Decisions

Class: bounded (bead coding-harness-te7q).

## Q-1 · When an attempt counts as "no work done"

asked: 2026-11-07
answer: "Keine Datei außerhalb der Runner-Zeilen (Recommended)" — the runner refuses an implement or repair attempt as "no work done" when its diff, minus the runner's own audit and time lines, is empty; a planned file left untouched does not refuse on its own.
answered_by: maintainer
status: answered
context: |
  Topic: three times (2026-11-06, GLM 5.3 Flash and Sonnet 5.5) the runner reported "verified and committed" for an attempt whose only change was its own audit and time lines.
  Intention: the night run of 2026-11-07 should take this change to its plan card, so the one behaviour question is asked before the night.
  Today: an empty attempt passes; only the review finds it.
  Repository change: one post-run check in the runner, with tests.
  Architecture change: none.

In the context of empty attempts reported as verified, facing a choice between an empty-diff rule and a stricter every-planned-file rule, we decided to refuse an attempt whose diff minus the runner's own lines is empty, to achieve a simple check that catches all three measured cases, accepting that an attempt touching an unplanned file still passes this check. — 2026-11-07
