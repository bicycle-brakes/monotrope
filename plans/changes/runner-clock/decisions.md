---
title: "Decisions — runner-clock"
category: decisions
status: draft
implementation_status: none
date: 2026-11-14
created: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-pph3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, flaky-tests, clock, runner]
---

# runner-clock — Decisions

Class: bounded (bead coding-harness-pph3).

## Q-1 · How the load-flaky timing tests become robust

asked: 2026-11-14
answer: "ja" to widening the bead to the class (after asking whether injecting a clock is a durable and smart solution): the runner reads time only through one clock function; a source test with no exemption list forbids any direct time read in the runner; both load-flaky tests and every other runner test with small real-time limits use an injected fake clock.
answered_by: maintainer
status: answered
context: |
  Topic: tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout sets the step limit to 2 seconds and lets real processes sleep; a second test, test_before_admission_execution_budget_is_shared_and_wait_free, uses a real queue holder and a 30-second limit.
  Intention: under the load of several lanes both failed on 2026-11-14 and passed alone; one failure cost a phase-6 review with its full make verify of about ten minutes.
  Today: scripts/stage2.py reads time directly at 7 call sites (time.monotonic, time.time, time.sleep or time.perf_counter, counted 2026-11-14 on origin/main); the tests wait real seconds.
  Repository change: one clock function in the runner that every time read goes through, a source test that no runner code reads time directly, and the timing tests moved to a fake clock the test advances itself.
  Architecture change: none beyond one choke point for time in the runner, the same pattern as run_git.

In the context of tests that fail under machine load because they wait real seconds, facing a choice between an injected clock, larger margins and serial runs, we decided for one clock choke point with a source test and a fake clock in the tests, to achieve that the whole class of load-dependent timing tests closes instead of one test, accepting a change at every direct time read of the runner. — 2026-11-14
