---
title: "Decisions — close-budget-clock"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-0n4s
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, flaky-test, close-merged]
---

# close-budget-clock — Decisions

Class: bounded (bead coding-harness-0n4s).

## The bead (read from the tracker by the orchestrator, 2026-11-21)

> tests/test_close_merged_beads.py::test_startup_budget_reserves_publication (budget 2 s, each close sleeps 0.3 s) completed 0 of 5 closes in a full make verify on fix/address-drift-warning at d8e1030d (2026-11-08, 1 failed, 4981 passed); alone it passes in 1.69 s. Neither the branch nor main changed close_merged_beads.py or the test. Timing budget under load: make the test independent of wall-clock load (inject a clock) rather than widening the …

So the target is the explore's mechanism A: the close budget of `scripts/close_merged_beads.py`. Mechanisms B and C of the explore are out of scope.

## SKIP · interview

status: skipped
reason: The bead names the test, the failure, the cause class and the remedy ("inject a clock rather than widening the budget"); the maintainer asked for no question windows until the block on 2026-11-23 10:00. The explore's open points 2 and 3 are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **A module seam, not the runner's clock guard.** `scripts/close_merged_beads.py` reads time through one module-level function (in the `verify_lock._now` style) that the budget arithmetic uses everywhere; `tests/runner_clock_guard.py` keeps its one-file scope. Reason: the guard is defined for the runner; one seam is the smallest change.
- **The two budget tests become clock-determined.** `test_startup_budget_reserves_publication` and its sibling with the `0 < completed < N` window drive the injected clock (each close advances it by a fixed step) so the number of completed closes is exact, like `test_subsecond_startup_remainder_refuses_closures` already does. Reason: the bead — independent of wall-clock load, no wider budget.
- **The hook's shell watchdog is unchanged.** Reason: not part of the flake.
- **Behaviour of the script is unchanged;** only where it reads the time. Reason: a test fix, not a policy change.
