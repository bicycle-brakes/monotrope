---
title: "Plan — ledger-ids-before-pytest"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.9
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, criterion-ledger]
---

# Plan — ledger-ids-before-pytest

```text
For you:     Missing ledger tests are named early, repairs can finish their own findings, and phase 6 holds unwritten tests.
Done when:   Focused tests prove those boundaries and make verify is green.
Appetite:    4 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Faster pytest startup, a new ledger format, or weaker proof for repairs.
Pre-mortem:  suppose it failed: most likely because a successful repair loses the missing-test record.
Starts unless you say stop.
```

## Build sequence and files

1. Change `scripts/stage2.py`: use the accepted plan snapshot to classify both ledger test forms before pytest, reusing the existing parsed-name checks; distinguish an absent file/function from read or parse failure. Keep changed-test and retry selection, whole-file coverage and deduplication, but never pass a missing ledger ID to pytest. Run all remaining targets even when an implement attempt owes missing tests; skip pytest when none remain. Preserve pytest failures and include each missing ID in the persistent attempt record, including a successful repair. Propagate implement versus repair explicitly through both full and targeted verification paths; implement fails on missing ledger tests, repair does not fail solely on unrelated missing ledger tests. Retain the separate finding-proof checks and their failures. Adjust implement and repair must-run prompt text to match their distinct obligations.
2. In `scripts/stage2.py`, check the current plan's actual ledger entries, excluding fenced examples, at phase-6 entry before reviewer invocation; refuse on every `not yet written` entry and name the entries plus the next step: write the tests and run verification so the runner clears their markers. Refuse unreadable or unassessable inputs rather than assuming a clear ledger; retain the existing full-verification and reviewer checks.
3. Change `tests/test_stage2_fail_fast.py` and `tests/test_stage2.py` to exercise the behavior below, updating the old assertion that deliberately sent a missing ledger ID to pytest and existing prompt assertions. Keep existing test function names used by other ledgers. Use isolated fixtures and stubbed launches, not model or network calls; exercise both verification paths and successful as well as failed attempt records.
4. Change `docs/WORKFLOW.md` to describe pre-launch diagnostics, implement and repair obligations, the phase-6 checkpoint and the existing clearing order; remove conflicting must-run wording. Maintain this change's `spec.md` and `plan.md` status and ledger markers as work proceeds; the runner owns `findings.md` and time entries. No files are deleted, no held path is edited by the attempt, and no design or ADR is due for this bounded change.

## Verification

Plant both ledger forms, multiple missing IDs and a standing changed test in the same run, including a new whole test file; check the pytest arguments, record, outcome and event order. Cover only-missing targets, successful and failing standing tests, retries, a finding's missing proof, and unreadable or invalid test files. Exercise phase 6 with multiple markers, a fenced example, a clear ledger, and an unreadable plan; assert refusal before reviewer launch and existing full-check behavior on a clear plan. Run:

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2_fail_fast.py tests/test_stage2.py
python3 scripts/check_interview_minimums.py --root . --change ledger-ids-before-pytest
python3 scripts/check_criterion_ledger.py --root .
make verify
```

The runner performs the final full check and commit. The explore record used Stage 2, route `flash`, model `glm-5.3-flash`; it records no Stage-1 fallback.

## Criterion ledger

- 1: not yet written tests/test_stage2_fail_fast.py::test_ledger_ids_are_checked_before_pytest — a missing written or unwritten ID reaches pytest
- 2: not yet written tests/test_stage2_fail_fast.py::test_missing_ledger_ids_persist_in_attempt_record — a successful repair loses a missing ID
- 3: not yet written tests/test_stage2_fail_fast.py::test_standing_targets_run_when_ledger_ids_are_missing — a missing ID blocks a standing target, including in a new file
- 4: not yet written tests/test_stage2_fail_fast.py::test_only_missing_ledger_ids_skip_pytest — pytest starts without a standing target
- 5: not yet written tests/test_stage2_fail_fast.py::test_implement_fails_after_running_standing_tests_with_missing_ledger_ids — implement accepts missing ledger tests
- 6: not yet written tests/test_stage2_fail_fast.py::test_repair_accepts_unrelated_missing_ledger_ids — unrelated missing tests alone reject repair
- 7: not yet written tests/test_stage2.py::test_repair_still_requires_finding_proof_with_missing_ledger_ids — missing finding proof is accepted
- 8: not yet written tests/test_stage2_fail_fast.py::test_standing_test_failure_is_not_hidden_by_missing_ledger_ids — a red selected test is accepted
- 9: not yet written tests/test_stage2.py::test_review_refuses_all_unwritten_ledger_entries_before_reviewer — a marker is omitted or the reviewer starts
- 10: not yet written tests/test_stage2.py::test_review_ledger_checkpoint_allows_clear_plan — written or non-test entries cause refusal
- 11: not yet written tests/test_stage2_fail_fast.py::test_unreadable_or_invalid_ledger_test_is_not_missing — a read or parse error becomes a missing ID or green
- 11: not yet written tests/test_stage2.py::test_review_refuses_unreadable_plan_at_ledger_checkpoint — unreadable plan is treated as clear

## Time used

2026-11-20 17:19:37–17:22:38 UTC, 181 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
