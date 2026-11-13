---
title: "Decisions — swarm-shared-fixture"
category: decisions
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-wnka
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Sonnet 5.5, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, tests, swarm, verify-speed]
---

# swarm-shared-fixture — Decisions

Class: bounded (bead coding-harness-wnka).

## Q-1 · Re-scope from the shared fixture to the test bodies

asked: 2026-11-13
answer: "ja" — the change is re-scoped from a shared fixture world to the slowest swarm tests themselves; the five slowest tests are measured one by one first, and only what that measurement shows is changed.
answered_by: maintainer
status: answered
context: |
  Topic: bead coding-harness-wnka wants the research-swarm tests faster through one shared fixture world instead of one rebuild per test.
  Intention: pytest is about 75 % of a full make verify, and the swarm tests are the largest block of it; the maintainer wants the full check under 10 minutes.
  Today: measured on 2026-11-13 on the Mac mini (tests/test_stage2_swarm.py, 167 tests, -n 6): fixture setup 23 s, test bodies 768 s summed. A shared fixture can save at most about 3 %.
  Repository change: only test files change; the slowest tests are measured singly, then the repeated per-slot work (declaration re-read, leak checks) inside them is shared or avoided; no test loses an assertion.
  Architecture change: none; production code stays untouched.

In the context of a fixture rebuild that costs 23 s of 791 s, facing a choice between building the shared fixture anyway and aiming at the test bodies, we decided to re-scope to the test bodies after measuring the five slowest tests, to achieve a saving that is measured and not assumed, accepting that the bead's title no longer names the work. — 2026-11-13
