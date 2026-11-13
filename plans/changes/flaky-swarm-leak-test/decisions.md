---
title: "Decisions — flaky-swarm-leak-test"
category: decisions
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-yb1l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, tests, flaky, stage-2, swarm]
---

# flaky-swarm-leak-test — Decisions

Class: bounded (bead coding-harness-yb1l).

## Q-1 · Repair at the root or at the one test

asked: 2026-11-13
answer: "ja, Lane 5 an der Wurzel reparieren" — the maintainer chose the root repair: one shared, atomic test-log helper used by all 17 unlocked log appends in five test files, with a reproduction under load before and after; the runner's fail-closed rule stays.
answered_by: maintainer
status: answered
context: |
  Topic: tests/test_stage2_swarm.py::test_a_refused_run_is_printed_before_any_model_call fails now and then on main's CI with "assert 2 == 0" (bead coding-harness-yb1l).
  Intention: a flaky required test can turn any merge-queue run red; the explore (research.md, a0c89b62) traced it to a torn read of a stand-in call log that is appended concurrently without locking.
  Today: 17 log appends in five test files write without a lock (tests/test_stage2.py 7, tests/test_stage2_swarm.py 4, tests/test_pi_install.py 3, tests/test_stage2_session.py 2, tests/test_stage2_research_availability.py 1); a reader can see half a line, and the dispatcher turns the resulting gate exception into a security refusal (exit 2) by design.
  Repository change: one shared helper for atomic test-log appends and reads, used by all 17 sites; a repetition-under-load reproduction before and after.
  Architecture change: none; the production fail-closed rule (scripts/stage2_research_dispatch.py) stays untouched.

In the context of a flaky swarm test caused by unlocked concurrent appends to a stand-in call log, facing a choice between a fix inside the one failing test and a shared atomic helper for every such append in the test suite, we decided for the shared helper at all 17 sites, to achieve that no sibling test fails the same way later, accepting a wider diff over five test files. — 2026-11-13

## Q-2 · A guard against new unlocked log appends

asked: 2026-11-13
answer: "ja" — the change includes a guard test that fails when a test file opens a log for appending without the shared atomic helper.
answered_by: maintainer
status: answered
context: |
  Topic: after Q-1 the 17 known unlocked log appends in the test suite use one shared atomic helper.
  Intention: close the mechanism at its choke point, not case by case; nothing today stops a future test from appending without a lock again.
  Today: no check reads tests/ for append-mode log writes.
  Repository change: one small guard test in this change that reads tests/ and fails on an append-mode open outside the shared helper.
  Architecture change: none.

In the context of a root repair of unlocked test-log appends (Q-1), facing a choice between fixing the 17 known sites only and also guarding against new ones, we decided to add a guard test in this change, to achieve that the same torn-read flake cannot return through a new test, accepting a slightly wider scope for a bounded change. — 2026-11-13
