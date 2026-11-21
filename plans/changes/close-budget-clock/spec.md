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
2. When the close-merged budget test runs with a controlled clock starting at zero and advances it by 0.5 seconds after each successful close against a two-second budget, exactly three of five eligible items close before the remaining two are refused and publication succeeds after those closures, independent of real subprocess deadlines.
   *Refuted by:* A different count, a missing exhaustion diagnostic, publication before a completed close, failed publication, or an actual short subprocess timeout affecting the result passes the test.
3. When the session-start budget test runs with the same controlled clock and two-second reconciler budget, exactly three of fifteen eligible items close before exhaustion and publication follows the completed closes and precedes prime, independent of real subprocess deadlines.
   *Refuted by:* A different count, a missing exhaustion diagnostic, incorrect order, watchdog abort, or an actual short subprocess timeout affecting the result passes the test.
4. When the clock reports less than one second remaining before a closure, the reconciler refuses that closure and still attempts publication using the existing publication timeout bounds.
   *Refuted by:* A closure starts below the floor, publication is omitted, or its timeout differs from the existing bounded calculation.
5. When no replacement is installed for the module clock function, the function calls the current `time.monotonic` and the reconciler retains the existing budget calculations, subprocess timeout arguments, diagnostics and exit behavior.
   *Refuted by:* Replacing `time.monotonic` after import does not control the default function and a real budget path, or equivalent readings produce a different deadline, timeout argument, diagnostic or exit result.

## Non-goals

- Changing the startup budget, the one-second close floor, publication bounds or reconciliation policy.
- Changing the session-start hook watchdog or its timeout policy; changing the runner clock guard, verify budget or appetite clock. The test-only watchdog limit may be raised to isolate the simulated budget.
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
- [DETAIL] Use a half-second simulated advance per successful close and a two-second reconciler budget in both budget tests: it makes three closures and the sub-second refusal exact without widening the reconciler budget.
- [DETAIL] Run real fixture `tools/bd` processes without the simulated short timeout in these tests while recording and separately asserting the timeout arguments: otherwise machine load can still make the tests fail even if the clock is controlled. The hook test replaces only its disposable copy of the entry script with an importing wrapper; it does not exercise the real `__main__` block, which remains covered by the other integration tests. No production test-clock switch is added.
- [DETAIL] The default clock delegates to `time.monotonic` at call time, rather than binding its identity at import: the existing monotonic monkeypatch and a default-path test can then expose an incorrect clock source.
