---
title: "Decisions — outcome-test"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-3nm5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, measurement, outcome-test]
---

# outcome-test — Decisions

Class: bounded (bead coding-harness-3nm5).

## Q-1 · Questions, frequency and where results live

asked: 2026-11-06
answer: "8 Fragen, bei Bedarf (Recommended)" — eight questions; the test runs before every change to a handover convention or AGENTS.md and once now as a baseline; results go to one JSONL file under docs/research/, each record dated and bound to a commit.
answered_by: maintainer
status: answered
context: |
  Topic: a fresh, memory-free session answers fixed harness questions (for example who repairs taken findings, where run plans live); the expected answer is read from the repository at test time, never stored; this shows whether a change to the handover or AGENTS.md makes sessions answer better or worse.
  Intention: the lane is explored; size, frequency and storage are open.
  Today: the gates check artefacts, not whether a session knows the current rules.
  Repository change: a question file, a script and a result file.
  Architecture change: none.

In the context of gates that measure artefacts but not what a fresh session knows, facing the cost of nightly runs, we decided on eight questions run on demand before handover or AGENTS.md changes plus one baseline, results in one dated JSONL file under docs/research/, to achieve a measurement exactly where knowledge changes, accepting no trend line between such changes. — 2026-11-06
