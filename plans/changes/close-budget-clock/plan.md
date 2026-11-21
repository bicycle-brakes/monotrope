---
title: "Plan — close-budget-clock"
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
tags: [plan, close-merged, clock]
---

# Plan — close-budget-clock

```text
For you:     The close-merged budget tests stop depending on machine load while the existing budget policy stays intact.
Done when:   Both tests prove the exact partial batch and publication order with a controlled clock, and make verify passes.
Appetite:    2 hours of phase 4 including repairs; stop at the limit.
Not now:     Changes to the budget policy, session-start watchdog or runner clock guard.
Pre-mortem:  suppose it failed: most likely because one budget calculation still reads the real clock.
Starts unless you say stop.
```

## Files and sequence

1. In `scripts/close_merged_beads.py`, add one module-level function returning `time.monotonic()` and route all three budget reads through it; leave all arithmetic, subprocess calls and reporting unchanged.
2. In `tests/test_close_merged_beads.py`, adapt `test_subsecond_startup_remainder_refuses_closures` to patch that function. Convert `test_startup_budget_reserves_publication` to invoke the imported reconciler with isolated preflight stubs, five eligible records and a recording subprocess stand-in; start the clock at zero and advance it by 0.5 seconds on each successful close. Assert exactly three closes, two refusals, successful publication after the closes, expected exit status and the actual close and publication timeout arguments. Add `test_budget_clock_seam_preserves_calculations` to exercise deadline creation, the one-second boundary, publication timeout bounds and the default delegation to the monotonic clock; a real sleep must not determine these outcomes.
3. In `tests/test_beads_start.py`, keep the real hook and its disposable project, history and recording wrapper. For `test_startup_budget_reaches_publication_before_prime`, replace the copied reconciler entry script only inside the fixture with a test wrapper that imports the copied real module, patches its clock and advances it by 0.5 seconds after each successful close. Preserve actual stub close and push calls and their order, but prevent their real subprocess timeout from determining the simulated budget result; independently assert the timeout arguments in the reconciler tests. Give the unchanged outer watchdog 180 seconds and a reserve of 178 seconds, leaving the same two-second reconciler budget; assert exactly three completed closes, exhaustion, publication before prime and no watchdog abort. Do not expose a test clock through production configuration.
4. In `plans/changes/close-budget-clock/plan.md`, update the ledger when the new test exists; the runner records time and findings in `plans/changes/close-budget-clock/findings.md` and regenerates `plans/INDEX.md` using `python3 scripts/plans_registry.py --index` after the artifact headers change. `plans/changes/close-budget-clock/spec.md` and this plan describe the change; `decisions.md` and `research.md` remain the recorded inputs. No file is deleted, no design or ADR is due, and no held path is assigned to the implementation attempt.

Keep `tools/claude-code/hooks/beads-start.sh`, `tests/runner_clock_guard.py`, other budget mechanisms and unrelated wall-clock tests untouched. The watchdog remains a real integration boundary; its generous test limit is not the simulated reconciler budget.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_close_merged_beads.py tests/test_beads_start.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_close_merged_beads.py::test_budget_clock_seam_preserves_calculations — any deadline, close or publication read bypasses the seam.
- 2: tests/test_close_merged_beads.py::test_startup_budget_reserves_publication — a wrong partial count, missing exhaustion or publication before closures passes.
- 3: tests/test_beads_start.py::test_startup_budget_reaches_publication_before_prime — a wrong count or publication after prime passes.
- 4: tests/test_close_merged_beads.py::test_subsecond_startup_remainder_refuses_closures — a close starts below one second or publication is omitted.
- 4: not yet written tests/test_close_merged_beads.py::test_budget_clock_seam_preserves_calculations — a publication timeout violates the existing bounds.
- 5: not yet written tests/test_close_merged_beads.py::test_budget_clock_seam_preserves_calculations — the default clock or budget calculations differ from the existing policy.
- 5: tests/test_close_merged_beads.py::test_startup_budget_reserves_publication — equivalent readings change the diagnostic, timeout or exit status.

## Time used

2026-11-21 17:16:22–17:18:42 UTC, 140 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
