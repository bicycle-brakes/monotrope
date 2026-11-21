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
Done when:   Both refusals are investigated, measured in-scope faults have regressions, and make verify is green.
Appetite:    4 hours of phase 4, repairs included — stop at the limit.
Not now:     Red-first proofs for code under test inside test files, or changes to guard-test policy.
Pre-mortem:  suppose it failed: most likely because the original attempt evidence is unavailable.
Starts unless you say stop.
```

## Files and sequence

1. In `plans/changes/red-first-baseline/findings.md`, record the investigation of both refusals in commit `ca493614`: L3-1 names `tests/test_stage2_swarm.py::test_finder_deep_envelope_is_invalid_without_crashing` (attempts 1 and 2), L3-4 names `tests/test_stage2_research_map.py::test_finder_filter_reports_each_invalid_entry` (attempt 3). Find each saved attempt's actual test tree and the HEAD captured before that repair run; `feacd0c8` is only a candidate, not a verified baseline. For each, run direct pytest and `red_first` with the same baseline production bytes, attempt `tests/` bytes, selector and relevant environment; record commands, inputs, outcome details, commits and any missing evidence. Do not compare the hand-repaired tests as if they were the refused tests. Record whether each cause is shared, distinct, absent or outside scope, with evidence; never infer a shared cause from the symptoms.
2. In `tests/test_stage2.py`, distil each reproduced in-scope mechanism into a self-contained disposable repository and run its regression against the unfixed runner first; record the failure. Add outcome controls in the ledger using real pytest runs and fault cases; no test may need the incident's local Git objects. In `scripts/stage2.py`, fix only measured in-scope causes and truthful outcome reporting in the existing `red_first` path, retaining its baseline construction, qualifying-failure contract and private-ref safeguards. Re-run the regressions and record the post-fix results.
3. In `docs/WORKFLOW.md`, correct the red-first exit requirement to exactly 1 and retain the qualifying-outcome checks; `tests/test_stage2.py` holds a focused wording check. These paths are not held. No files are deleted.
4. In `plans/changes/red-first-baseline/plan.md`, replace each `not yet written` ledger marker as its test is defined. The runner maintains call records in `plans/changes/red-first-baseline/findings.md`, measured time and generated `plans/INDEX.md`.

If no runner mismatch is found, or the measured cause is outside scope, record both cases and ship the applicable reporting and workflow corrections without claiming a reproduced fix. If evidence for either case is missing, record what is unavailable, leave that incident and bead unresolved, and report the limitation; do not guess a mechanism or close the bead. Stop at four hours and report remaining work. The orchestrator updates the bead and pull request outcome; the implementation attempt does not write tracker data.

Do not change the guard proof, tests-only boundary, accepted ADRs, other change folders or tracker data. Held paths are assigned to the orchestrator after an accepted attempt if needed; none is planned.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py
make verify
```

For every reproduced in-scope fault, record the pre-fix failing regression and post-fix result; the focused run does not replace `make verify`.

## Criterion ledger

- 1: not a test — phase-6 review checks both incident evidence records and explicit unavailable inputs against the recorded refusals.
- 2: not a test — phase-6 review checks recorded commits, test-tree identity, selectors and commands for both paired runs.
- 3: not a test — phase-6 review checks each measured mechanism has a self-contained regression and a recorded pre-fix failure; this is conditional on the investigation.
- 4: not yet written tests/test_stage2.py::test_red_first_reports_actual_pytest_outcomes — an exit, skip, xfail or collection-error diagnostic disagrees with the actual run.
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

## Time used

2026-11-21 02:34:36–02:37:14 UTC, 158 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 10:36:17–10:39:31 UTC, 193 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
