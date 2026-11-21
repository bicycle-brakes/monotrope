---
title: "Plan — red-first-baseline"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7aso
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, red-first]
---

# Plan — red-first-baseline

```text
For you:     A repair's baseline check reports the test's actual outcome.
Done when:   All three attempts are investigated, measured in-scope faults have regressions, and make verify is green.
Appetite:    4 hours of phase 4, repairs included — stop at the limit.
Not now:     Red-first proofs for code under test inside test files, or changes to guard-test policy.
Pre-mortem:  suppose it failed: most likely because the original attempt evidence is unavailable.
Starts unless you say stop.
```

## Files and sequence

1. In `plans/changes/red-first-baseline/findings.md`, record the investigation of all three refusals in commit `ca493614`: L3-1 names `tests/test_stage2_swarm.py::test_finder_deep_envelope_is_invalid_without_crashing` (attempts 1 and 2), L3-4 names `tests/test_stage2_research_map.py::test_finder_filter_reports_each_invalid_entry` (attempt 3). Search that commit, branch `fix/finder-partial-report`, saved-attempt refs and files in the lane's Git directory, and bead notes; record searches and inaccessible sources before declaring evidence unavailable. Find each attempt's actual test tree and the HEAD captured before that repair run; `feacd0c8` is only a candidate, not a verified baseline. Label derived inputs with their evidence and do not reconstruct missing test bytes from prose. For each available attempt compare direct pytest in a normal checkout and this branch's `red_first` using the same baseline, attempt `tests/` bytes, selector and this worktree's `.venv` interpreter; record environments, commands, inputs, outcomes and commits. Record the diff of `scripts/stage2.py` against the incident commit to distinguish historical-only faults. Do not compare hand-repaired tests as if they were refused tests. A difference caused by the runner's private checkout or filtered environment is in scope; missing external packages are not. Record whether causes are shared, distinct, absent or outside scope, with evidence.
2. In `tests/test_stage2.py`, distil each reproduced in-scope mechanism into a self-contained disposable repository and run its regression against the unfixed runner first; record the failure. Add outcome, fixed-code and guard-proof controls in the ledger using real pytest runs and fault cases; no test may need incident Git objects. In `scripts/stage2.py`, fix measured in-scope causes and truthful outcome reporting in the existing `red_first` path; shared helpers may be repaired while retaining the fixed-code and guard contracts, qualifying-failure contract and private-ref safeguards. For non-exit-1 refusals report the actual exit and the first true recorded outcome, not a generic session-status fault; retain exit-1 refusal wording. When no probe record exists after a nonzero exit, protect combined stdout and stderr with the existing diagnostic protection, failing closed if protection fails, and cap the diagnostic at 40 lines and 4,000 characters including a truncation marker. Re-run regressions and each available incident comparison after the fix and record results.
3. In `docs/WORKFLOW.md`, correct the red-first exit requirement to exactly 1 and retain the qualifying-outcome checks; `tests/test_stage2.py` holds a focused wording check. These paths are not held. No files are deleted.
4. In `plans/changes/red-first-baseline/plan.md`, replace each `not yet written` ledger marker as its test is defined. The runner maintains call records in `plans/changes/red-first-baseline/findings.md`, measured time and generated `plans/INDEX.md`.

If no runner mismatch is found, or the measured cause is outside scope, record all three attempts and ship the applicable reporting and workflow corrections without claiming a reproduced fix. If necessary preserved evidence is missing or an out-of-scope bug remains, leave the bead open and record the limitation; overwritten, never-saved attempt-1 bytes alone do not block closure when preserved evidence explains the refusals and the reporting fix is complete. Close only when all measured runner causes are fixed or confirmed not to be runner faults and no incident remains unresolved. Stop at four hours and report remaining work. The orchestrator updates the bead and pull request outcome; the implementation attempt does not write tracker data.

Do not change the guard proof, tests-only boundary, accepted ADRs, other change folders or tracker data. Held paths are assigned to the orchestrator after an accepted attempt if needed; none is planned.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py
make verify
```

For every reproduced in-scope fault, record the pre-fix failing regression and post-fix result; the focused run does not replace `make verify`.

## Criterion ledger

- 1: not a test — phase-6 review checks all three attempts, the required searches and accessible evidence against each record.
- 2: not a test — phase-6 review checks recorded commits, test-tree identity, selectors, interpreter, commands and historical runner diff for each available paired run.
- 3: not a test — phase-6 review checks each measured mechanism has a self-contained regression, a recorded pre-fix failure and a post-fix comparison on available incident inputs; this is conditional on the investigation.
- 4: not yet written tests/test_stage2.py::test_red_first_reports_actual_pytest_outcomes — a non-exit-1 refusal omits or misstates the exit, or substitutes generic session status for a recorded pass, empty selection, skip, xfail, XPASS or collection error.
- 5: tests/test_stage2.py::test_red_first_accepts_only_clean_assertion_runs — a qualifying assertion failure is refused.
- 5: tests/test_stage2.py::test_red_first_accepts_pytest_failed_call_outcomes — a qualifying pytest failure is refused.
- 6: tests/test_stage2.py::test_a_named_test_that_is_not_red_first_fails_the_attempt — a passing baseline is accepted.
- 7: tests/test_stage2.py::test_red_first_refuses_setup_and_teardown_errors — a fixture error is accepted.
- 7: tests/test_stage2.py::test_red_first_refuses_non_assertion_call_failures — an unrelated call error is accepted.
- 7: tests/test_stage2.py::test_a_red_first_interpreter_that_cannot_start_pytest_fails_the_attempt — an interpreter startup error is accepted.
- 7: tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes — a collection error is accepted.
- 8: tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes — a skipped, xfailed or XPASS case is accepted.
- 9: not yet written tests/test_stage2.py::test_red_first_keeps_baseline_code_attempt_tests_and_source_state — attempt production bytes reach the proof, attempt tests do not, or source refs, index or worktree change.
- 10: not yet written tests/test_stage2.py::test_workflow_red_first_exit_contract — the workflow permits exit 2 or omits the exact exit-1 requirement.
- 11: tests/test_stage2.py::test_fixed_proof_uses_current_file_tree — the fixed-code proof uses the wrong source tree.
- 11: tests/test_stage2.py::test_fixed_code_proof_keeps_pytest_failed_red — the fixed-code proof accepts a failing test.
- 11: tests/test_stage2.py::test_repair_marks_no_proof_when_the_named_test_does_not_pass_fixed_code — a non-passing test proves fixed code.
- 11: tests/test_stage2.py::test_fixed_proof_names_refs_after_initial_tree_failure — ref interference is concealed after a tree failure.
- 11: not yet written tests/test_stage2.py::test_fixed_code_proof_preserves_pass_and_refusal_contract — a passing fixed-code test is refused or a skipped, xfailed or failing test is accepted after a shared-helper repair.
- 11: tests/test_stage2.py::test_guard_proof_requires_clean_green_without_the_switch — a non-passing clean guard leg is accepted.
- 11: tests/test_stage2.py::test_guard_proof_preserves_outcome_and_execution_guards — a skipped or nonqualifying planted guard leg is accepted.
- 11: tests/test_stage2.py::test_guard_proof_uses_attempt_code_and_planted_switch — a valid clean and planted guard proof is refused.
- 12: not yet written tests/test_stage2.py::test_red_first_protects_pre_record_pytest_diagnostics — a pre-record import error loses its exit or diagnostic, exceeds either cap, omits a required truncation marker, or leaks output after protection failure.

## Time used

2026-11-21 02:34:36–02:37:14 UTC, 158 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 10:36:17–10:39:31 UTC, 193 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 10:52:18–10:55:18 UTC, 179 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 11:14:17–11:17:22 UTC, 185 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
