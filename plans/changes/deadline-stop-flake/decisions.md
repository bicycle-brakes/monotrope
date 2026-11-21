---
title: "Decisions — deadline-stop-flake"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-j1i5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, flaky-test, review-loop]
---

# deadline-stop-flake — Decisions

Class: bounded (bead coding-harness-j1i5).

## The bead and what the test already does (orchestrator, 2026-11-21)

> tests/test_stage2.py::test_a_deadline_stop_names_the_round_limit failed in the full make verify of the address-drift-warning repair (attempt 3, 2026-11-08 ~15:40 UTC, StopIteration looking for a line starting 'mimo-v2.6-pro failed:') and passed alone in 3 s on the same tree. A timing-dependent test under the six-lane load; the runner rejected an otherwise green repair on it. Make the test deterministic (inject the clock/deadline).

The test already installs a `FakeClock` and `ScriptedPrograms` and sets `REVIEWER_MINUTES` to two seconds. The `StopIteration` means the round record held no `mimo-v2.6-pro failed:` line: under load the paid member was not stopped by the round deadline. So some part of the deadline path still reads real time or waits on a real thread, and the fake clock does not reach it. The explore ran with `--stage2-off` because GLM 5.3 Flash refused (bead coding-harness-b5pu).

## SKIP · interview

status: skipped
reason: The bead fixes the goal (deterministic, clock or deadline injected); the maintainer asked for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Find the real-time leak first.** The attempt traces every time read and every wait on the round-deadline path of `review-loop` under this test (`time.monotonic`, `time.time`, `threading` waits, `Event.wait`, `join` timeouts, subprocess timeouts) and names the one the fake clock does not cover. A forced reproduction (holding that wait past the fake deadline) is the regression, red before the fix. Reason: the test already injects a clock; guessing another injection fixes nothing.
- **Fix in the runner when the leak is there,** through the clock seam the runner-clock change introduced (`tests/runner_clock_guard.py`), so the guard keeps covering it; fix in the test helper when the leak is only there. Reason: one clock for the runner.
- **No longer limits, no sleeps, no retry.** Reason: the bead.
- **If no leak is found within the appetite,** the attempt stops and reports in `findings.md` what it traced and measured. Reason: as for coding-harness-068l and coding-harness-oag7.
