---
title: "Plan — close-budget-clock"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-23
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

1. In `scripts/close_merged_beads.py`, add one replaceable module-level function that calls `time.monotonic()` at call time and route all three budget reads through it; leave all arithmetic, subprocess calls and reporting unchanged.
2. In `tests/test_close_merged_beads.py`, keep the disposable history, render and real recording `tools/bd` stub in `test_startup_budget_reserves_publication`. Run a fresh interpreter with the disposable scripts directory first on `sys.path`, importing the copied module and its local dependencies there, in a fixture-only wrapper with `CLOSE_MERGED_BD_TIMEOUT=1.5` that starts the clock at zero and advances it by 0.5 seconds after each successful close. Intercept the copied module's close and push subprocess calls: record their requested timeouts and each real delegate call, run the same stub without those short timeouts, and assert close timeouts 1.5, 1.5 and 1.0 seconds and push timeout 0.5 seconds. Assert each imported local module resolves under the disposable copy and each tracker operation uses its `tools/bd`; assert the real delegate receives no simulated timeout. Exercise the interceptor with a controlled delegate simulating a third close longer than one second and a push longer than 0.5 seconds without sleeping; require the same successful outcome. Assert exactly three closes, two refusals, the exhaustion diagnostic, render read-back, successful publication after the closes and exit status 1. Keep preflight subprocess handling unchanged. Add `test_budget_clock_seam_preserves_calculations` to check the three clock reads, the one-second boundary, publication bounds and the default function's call-time delegation by patching `time.monotonic` after import and exercising a budget path; keep or adapt `test_subsecond_startup_remainder_refuses_closures` to verify the sub-second refusal.
3. In `tests/test_beads_start.py`, retain the real hook, disposable history and real recording `tools/bd` stub in `test_startup_budget_reaches_publication_before_prime`. Replace only the fixture's copied reconciler entry script with a wrapper that imports the real copied module under another filename from the disposable scripts directory in a fresh interpreter, verifies the reconciler and its local imports resolve there, installs the same controlled clock and intercepts close and push as in step 2; assert tracker calls target the fixture and simulated timeouts never reach real delegates, including the controlled slow-delegate case; do not add production configuration. Pass the hook's original argv unchanged to `main` and assert the received budget; use watchdog 100 seconds and reserve 98 seconds for a two-second reconciler budget, below the test harness's existing 120-second outer timeout. Assert exactly three completed closes, exhaustion, publication after every close and before prime, and no watchdog abort. The fixture wrapper does not cover the real entry script's `__main__`; the other entry-point integration tests retain that coverage.
4. In `plans/changes/close-budget-clock/plan.md`, update the ledger when the new test exists; the runner records time and findings in `plans/changes/close-budget-clock/findings.md` and regenerates `plans/INDEX.md` using `python3 scripts/plans_registry.py --index` after the artifact headers change. `plans/changes/close-budget-clock/spec.md` and this plan describe the change; `decisions.md` and `research.md` remain the recorded inputs. No file is deleted, no design or ADR is due, and no held path is assigned to the implementation attempt.

Keep `tools/claude-code/hooks/beads-start.sh`, `tests/runner_clock_guard.py`, other budget mechanisms and unrelated wall-clock tests untouched. The watchdog remains a real integration boundary; its generous test limit is not the simulated reconciler budget.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_close_merged_beads.py tests/test_beads_start.py
make verify
```

## Criterion ledger

- 1: tests/test_close_merged_beads.py::test_budget_clock_seam_preserves_calculations — any deadline, close or publication read bypasses the seam.
- 2: tests/test_close_merged_beads.py::test_startup_budget_reserves_publication — a count other than three, missing exhaustion or publication before closures passes.
- 3: tests/test_beads_start.py::test_startup_budget_reaches_publication_before_prime — a count other than three, missing exhaustion or publication after prime passes.
- 4: tests/test_close_merged_beads.py::test_subsecond_startup_remainder_refuses_closures — a close starts below one second or publication is omitted.
- 4: tests/test_close_merged_beads.py::test_budget_clock_seam_preserves_calculations — a publication timeout violates the existing bounds.
- 5: tests/test_close_merged_beads.py::test_budget_clock_seam_preserves_calculations — the default fails to delegate to the current monotonic clock or budget calculations differ from the existing policy.
- 5: tests/test_close_merged_beads.py::test_startup_budget_reserves_publication — equivalent readings change the diagnostic, timeout or exit status.

- 6: tests/test_close_merged_beads.py::test_startup_budget_reserves_publication — the reconciler or local imports escape the disposable copy or tracker calls reach the real wrapper.
- 6: tests/test_beads_start.py::test_startup_budget_reaches_publication_before_prime — imports or tracker calls escape the fixture.
- 7: tests/test_close_merged_beads.py::test_startup_budget_reserves_publication — a simulated timeout reaches a real delegate or the controlled slow delegate prevents publication.
- 7: tests/test_beads_start.py::test_startup_budget_reaches_publication_before_prime — a simulated timeout reaches a real delegate or the controlled slow delegate changes the result.
- 8: tests/test_beads_start.py::test_startup_budget_reaches_publication_before_prime — the hook's budget argument is missing, changed or ignored.

## Runner route — 2026-11-23

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM Flash: Z.ai 5-hour limit until 22:33 CET (bead coding-harness-363r.4); Sonnet answers on the default profile again.

## Time used

2026-11-21 17:16:22–17:18:42 UTC, 140 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 17:22:44–17:25:45 UTC, 180 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 17:29:53–17:32:13 UTC, 139 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-23 20:49:17–20:53:40 UTC, 263 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_beads_start.py`, `tests/test_close_merged_beads.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
