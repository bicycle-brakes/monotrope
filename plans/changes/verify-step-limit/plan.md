---
title: "Plan — verify-step-limit"
status: draft
implementation_status: none
date: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-xkvr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, timeout]
---

# Plan — verify-step-limit

```text
For you:     Runner verification gets 45 minutes, and its timeout messages and tests follow the shared limit.
Done when:   The 45-minute default and all three launch paths are covered, timeout expectations follow the constant, admission waits stay excluded, and make verify is green.
Appetite:    1 hour of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Central configuration, measured defaults, separate job budgets, or changes to other time limits.
Pre-mortem:  suppose it failed: most likely because a timeout test still hard-codes 30 minutes.
Starts unless you say stop.
```

## Build sequence and files

1. Attempt: in `tests/test_stage2.py`, add `test_verify_step_limit_is_45_minutes`, asserting the unpatched default equals `45 * 60`; measure it red before changing production code. Extend the existing post-attempt, full-verification fallback and draft-documents call-site tests named in the ledger to capture both `timeout` and `limit`, substituting `VERIFY_SECONDS = 7 * 60` to reject a stale or separately hard-coded value or label. Restore via monkeypatch.
2. Attempt: in `scripts/stage2.py`, set `VERIFY_SECONDS = 45 * 60`; preserve the three existing `timeout=VERIFY_SECONDS` launches and their derived minute labels. No new configuration or refactoring.
3. Attempt: in `tests/test_stage2.py`, replace the fixed 30-minute timeout labels and expectations in `test_a_hanging_runner_step_aborts_with_its_limit_named`, `test_a_make_verify_that_hangs_is_a_repairable_diagnostic`, and the timeout case of `test_review_requires_fresh_full_verification_before_model_call` with text derived from `stage2.VERIFY_SECONDS // 60`. Keep the real hang test's short execution timeout; sleep durations are not diagnostic labels. Reuse admission-wait and process-group cleanup regressions unchanged.
4. Attempt: in `plans/changes/verify-step-limit/plan.md`, remove `not yet written` when the new test exists; update implementation status in this file and `plans/changes/verify-step-limit/spec.md` to reflect actual work. Runner: retain evidence in `plans/changes/verify-step-limit/findings.md`, record measured Time used, and regenerate `plans/INDEX.md` through `python3 scripts/plans_registry.py --index` before verification. No files are deleted; no held-path bootstrap edit is required.

## Limits and route

Do not touch `scripts/verify_lock.py`, `scripts/verify_all.sh`, `tests/test_stage2_fail_fast.py`, tool/git/model/proof limits, retry logic, gate order, other change folders, held paths, or doctrine. No design or ADR is due for class `bounded`. Phase 1 used Stage 2, route `flash`, endpoint `glm-coding-plan`, model `glm-5.3-flash`; no Stage-1 fallback is recorded. The research's unread intent is settled by decisions.md Q-1 and its class declaration. At `2ce11fe2` (2026-11-11), `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent; use the phase-3 prompt's form and report the unavailable validator. Findings contain only the draft-call record, no phase-2a review rows. Live PR and concurrent-session state were not read within this runner boundary.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'verify_step_limit_is_45_minutes or runner_steps_carry_their_limits_at_the_call_sites or targeted_stage2_test_file_requires_full_verification or draft_docs_check_keeps_admission_and_execution_limit or hanging_runner_step_aborts_with_its_limit_named or make_verify_that_hangs_is_a_repairable_diagnostic or review_requires_fresh_full_verification_before_model_call or verification_admission_is_outside_execution_timeout or timeout_kills_the_whole_process_group'
.venv/bin/python3 -m ruff check scripts/stage2.py tests/test_stage2.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py tests/test_stage2.py
python3 scripts/check_interview_minimums.py --change verify-step-limit
python3 scripts/check_criterion_ledger.py
make verify
```

The runner owns the full check and commit. No real 45-minute sleep is needed.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_verify_step_limit_is_45_minutes — the default remains 1800 seconds or changes to another value
- 1: tests/test_stage2.py::test_the_runner_steps_carry_their_limits_at_the_call_sites — post-attempt make uses a different timeout
- 1: tests/test_stage2.py::test_targeted_stage2_test_file_requires_full_verification — full_verify ignores the shared timeout
- 1: tests/test_stage2.py::test_draft_docs_check_keeps_admission_and_execution_limit — the documents launch ignores the shared timeout
- 2: tests/test_stage2.py::test_the_runner_steps_carry_their_limits_at_the_call_sites — the post-attempt label fails to follow a substituted limit
- 2: tests/test_stage2.py::test_targeted_stage2_test_file_requires_full_verification — the full_verify label fails to follow a substituted limit
- 2: tests/test_stage2.py::test_draft_docs_check_keeps_admission_and_execution_limit — the documents label fails to follow a substituted limit
- 3: tests/test_stage2.py::test_a_hanging_runner_step_aborts_with_its_limit_named — a derived label is passed but a stale literal is expected
- 3: tests/test_stage2.py::test_a_make_verify_that_hangs_is_a_repairable_diagnostic — a derived injected timeout is checked against stale minute text
- 3: tests/test_stage2.py::test_review_requires_fresh_full_verification_before_model_call — timeout handling admits a reviewer after failed verification
- 3: not a test — phase-6 review confirms timeout fixtures and expectations derive their minute text from VERIFY_SECONDS, including the review timeout fixture that only checks refusal
- 4: tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout — queue time is charged to execution

## Time used
