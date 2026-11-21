---
title: "Spec — close-budget-clock"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-0n4s
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, close-merged, clock]
class: bounded
appetite: 2
adr_files: []
---

# Spec — close-budget-clock

The close-merged startup budget tests have deterministic outcomes without changing the budget policy (bead `coding-harness-0n4s`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-08 a full verification completed none of five expected closures in `test_startup_budget_reserves_publication`, while the test passed alone; its slow closes and two-second budget compete with machine load (`decisions.md`, “The bead”).
- At commit `490c5e34`, the close-merged reconciler reads the monotonic clock directly for deadline creation, close timeouts and publication timeout. Its test and the session-start integration test use real sleeps and an inexact partial-batch assertion (`research.md`, mechanism A).

## Acceptance criteria

1. When a startup budget is supplied, deadline creation and the remaining budget for closures and publication use one replaceable module-level monotonic clock function.
   *Refuted by:* Any of the three budget reads bypasses that function, or replacing it does not control a budget calculation.
2. When the close-merged budget test runs with a controlled clock, it asserts an exact, nonzero partial batch, budget exhaustion and successful publication after all attempted closures without real-time sleeps determining the batch.
   *Refuted by:* The test accepts an incorrect closure count, loses the exhaustion or publication ordering assertion, or its batch depends on elapsed wall time.
3. When the session-start budget test runs with a controlled reconciler clock, it asserts an exact, nonzero partial batch and publication after completed closures and before prime without real-time sleeps determining the batch.
   *Refuted by:* The test accepts an incorrect closure count or wrong ordering, or its batch depends on elapsed wall time.
4. When the clock reports less than one second remaining before a closure, the reconciler refuses that closure and still attempts publication using the existing publication timeout bounds.
   *Refuted by:* A closure starts below the floor, publication is omitted, or its timeout differs from the existing bounded calculation.
5. When no test clock is installed, the reconciler retains the existing budget calculations, subprocess timeouts, diagnostics and exit behavior.
   *Refuted by:* An equivalent sequence of monotonic readings produces a different deadline, timeout, diagnostic, or exit result.

## Non-goals

- Changing the startup budget, the one-second close floor, publication bounds or reconciliation policy.
- Changing the session-start hook watchdog or its timeout policy; changing the runner clock guard, verify budget or appetite clock.
- Removing real-time behavior from unrelated watchdog and background-process tests.

## Protected areas

The session-start hook and `tests/runner_clock_guard.py` retain their existing behavior and scope; neither needs an edit for this test fix.

## Definition of Done

- The focused tests and `make verify` are green.
- The script, both test files, this change's artifacts and the generated `plans/INDEX.md` move in the same pull request; no ADR is due.
- The protected areas are untouched and the non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes the close-budget-clock work item (`coding-harness-0n4s`), and its last commit carries `Closes-Bead: coding-harness-0n4s`.
- No special runs beyond the stated verification are required.

## Open decisions

- [DETAIL] Use a two-hour implementation appetite including repairs: it is a reversible stop for this small bounded change and neither research nor decisions sets a value.
- [DETAIL] Use a half-second simulated advance per successful close for the two-second test budget: it makes the three completed closures and the sub-second refusal exact in binary arithmetic without widening the budget.
