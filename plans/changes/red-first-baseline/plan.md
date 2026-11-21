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
For you:     A repair's baseline check reflects the named test's actual result.
Done when:   The recorded refusal is reproduced before the fix, its regression passes afterward, and make verify is green.
Appetite:    4 hours of phase 4, repairs included — stop at the limit.
Not now:     Red-first proofs for code under test inside test files, or changes to guard-test policy.
Pre-mortem:  suppose it failed: most likely because the original attempt's evidence cannot reproduce the mismatch.
Starts unless you say stop.
```

## Files and sequence

1. In `tests/test_stage2.py`, first add the incident regression. The parent of the refusal-record commit `ca493614` is `feacd0c8`, a candidate baseline to verify against the saved evidence; the refusal names `tests/test_stage2_swarm.py::test_finder_deep_envelope_is_invalid_without_crashing` (finding L3-1). Read the saved attempt evidence named by `git show ca493614:plans/changes/finder-partial-report/findings.md` and its attempt tree from this repository's Git storage; compare the actual pytest result on baseline code with `red_first` on the same baseline and attempt tests. Confirm the regression fails on the current runner for the recorded mismatch and save the commands, test bytes, baseline, outcomes and commit for the PR. The hand-finished test is in `5121a00c` but is not a substitute for the refused attempt without checking its bytes and setup. If the evidence is unavailable, the hand and private runs differ in inputs, or the mismatch cannot be reproduced, stop and report the evidence instead of guessing a fix.
2. In `scripts/stage2.py`, repair the measured cause in the existing baseline-proof path, preserving the contract and safeguards in criteria 2–4. If the measured cause requires a different file or changes the stated contract, stop for a revised scope. Add the ledger regressions in `tests/test_stage2.py`, including controls that prove real green and nonqualifying errors remain refusals and that baseline production and attempt tests are the bytes exercised. Use disposable repositories and actual pytest execution, not a stubbed success, for the incident and outcome checks.
3. In `docs/WORKFLOW.md`, replace “exits 1 or 2” in the red-first paragraph with the actual requirement of exit exactly 1 plus the existing qualifying outcome checks. Add a focused contract check in `tests/test_stage2.py` that fails if the old wording returns. The runner's attempt may edit these paths; none is a held path. No files are deleted.
4. In `plans/changes/red-first-baseline/plan.md`, replace each `not yet written` ledger marker as its test is defined. The runner owns call records in `plans/changes/red-first-baseline/findings.md`, measured time and the generated `plans/INDEX.md`.

Do not change the guard proof, the tests-only boundary, accepted ADRs, other change folders or tracker data. Preserve the private repository and ref checks. Any newly necessary held-path edit belongs to the orchestrator after an accepted attempt, never to the attempt; no such edit is planned.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py
make verify
```

Run the incident regression against the unfixed runner first and record its expected failure, then rerun after the repair; the focused test does not replace `make verify`.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_red_first_reproduces_finder_round_three_refusal — the old runner reports green for the independently confirmed qualifying red, or the fixed runner still refuses it.
- 2: not yet written tests/test_stage2.py::test_red_first_still_refuses_a_passing_baseline — accepting a passing test fails.
- 3: not yet written tests/test_stage2.py::test_red_first_still_refuses_nonqualifying_failures — accepting a collection, environment, fixture or unrelated call error fails.
- 4: not yet written tests/test_stage2.py::test_red_first_keeps_baseline_code_attempt_tests_and_source_state — changed production bytes reach the proof, attempt test bytes do not, or source refs, index or worktree change.
- 5: not yet written tests/test_stage2.py::test_workflow_red_first_exit_contract — the workflow permits exit 2 or omits the exact exit-1 requirement.

## Time used

2026-11-21 02:34:36–02:37:14 UTC, 158 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
