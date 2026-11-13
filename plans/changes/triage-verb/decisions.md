---
title: "Decisions — triage-verb"
category: decisions
status: draft
implementation_status: none
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-o2s1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, review-loop, triage]
---

# triage-verb — Decisions

Class: bounded (bead coding-harness-o2s1).

## Q-1 · A taken row that only touches tests, marked without "not a test"

asked: 2026-11-07
answer: "Ablehnen mit Vorschlag (Recommended)" — the verb refuses such a status and names the correct spelling ('taken — not a test — …'); it does not write the row with a warning.
answered_by: maintainer
status: answered
context: |
  Topic: the orchestrator sets loop-row statuses by hand with ad-hoc Python; during 2026-11-04 to 2026-11-07 that broke a row's cells and marked test-only rows without the 'taken — not a test' prefix the runner requires, which cost failed repairs.
  Intention: the night run of 2026-11-07 should take this change to its plan card, so the one open behaviour question is asked before the night.
  Today: no verb; the loop record is edited by hand.
  Repository change: a new verb `stage2.py triage <change> <row>=<status> <reason>` in the runner, with tests.
  Architecture change: one more runner verb; the loop record's shape stays as it is.

In the context of loop rows set by hand and repairs failing on a missing status prefix, facing a choice between refusing and warning, we decided that the verb refuses a test-only taken row without the 'not a test' prefix and names the correct spelling, to achieve that this mistake cannot reach a repair, accepting that the orchestrator must restate such a row. — 2026-11-07
