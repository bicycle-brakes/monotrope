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

1. Change `scripts/stage2.py`: after lint, classify both forms of the accepted plan's ledger using the runner's parsed-name check before pytest; distinguish absent files or names from read and parse faults. Keep changed-test and retry selection, whole-file coverage and deduplication, but never pass a missing ledger ID to pytest. Run all standing targets even if implement owes missing tests, and skip pytest when none stand. Preserve pytest failures and name every missing ID in an accepted attempt's `plan.md` time line or a failed attempt's `findings.md` diagnostics. Pass the attempt type through both full and targeted paths: implement fails for either missing ledger form; repair fails for a missing written entry, but a missing `not yet written` entry alone does not fail its cheap check. Preserve the existing finding-proof checks. Update both prompt variants: implement owes every ledger test; repair owes its findings' tests, reports other unwritten tests without owing them, and its model-run pytest list excludes missing IDs.
   Treat an absent file as missing; report an existing unreadable or invalid file as a fault. Build repair prompts even when a file cannot be inspected, identifying the fault rather than listing that ID as standing. Keep the existing post-verification check of repair claims.
2. In `scripts/stage2.py`, check the current plan's actual ledger entries, excluding fenced examples, at phase-6 entry before full verification or reviewer invocation; refuse on every `not yet written` marker, even if the test exists, and name each entry and the next step: take one `taken — ledger test — tests/<path>::<function>` finding per marked entry and run `python3 scripts/stage2.py repair ledger-ids-before-pytest`. Refuse unreadable or unassessable inputs rather than assuming a clear ledger; retain the existing full-verification and reviewer checks.
3. In `scripts/stage2.py`, extend finding triage and repair to accept the ledger-debt status only for an exact still-marked entry in the accepted plan, one entry and one fixed claim per row. The existing answer check must require the claim to match and the named test to stand and pass on the repaired tree, recording this proof without a baseline red-first run; keep ordinary and guard-test proofs unchanged. Use the existing ledger clearing and reject acceptance unless the corresponding marker clears. A test seen by the runner but not by ledger clearing (such as `async def`) must be rewritten as a valid top-level synchronous test that both recognize; an already-present test must still pass and clear without requiring an unrelated code edit. Do not authorize the exception from finding prose alone.
4. Change `tests/test_stage2_fail_fast.py` and `tests/test_stage2.py` to exercise the behavior below, updating the old assertion that deliberately sent a missing ledger ID to pytest and existing prompt assertions. Keep existing test function names used by other ledgers. Use isolated fixtures and stubbed launches, not model or network calls; exercise both verification paths and successful as well as failed attempt records.
5. Change `docs/WORKFLOW.md` to describe pre-launch diagnostics, implement and repair obligations, the phase-6 checkpoint and the existing clearing order; remove conflicting must-run wording. Maintain this change's `spec.md` and `plan.md` status and ledger markers as work proceeds; the runner owns `findings.md` and time entries. No files are deleted, no held path is edited by the attempt, and no design or ADR is due for this bounded change.

## Verification

Plant both ledger forms, multiple missing IDs and a standing changed test in the same run, including a new whole test file; check pytest arguments, both record locations, outcome and event order, including an earlier lint failure. Cover only-missing targets, successful and failing standing tests, retries, ordinary and guard-test finding claims, absent files, async definitions, definitions inside strings, and unreadable or invalid files. Exercise ledger-debt triage and proof for multiple entries, a mismatched or unauthorized claim, a test green on baseline, an absent or failing test, an already-existing test, and an async test rewritten to clear its marker; confirm normal findings still require their original proofs. Exercise phase 6 with multiple markers, a marked existing test, a fenced example, a clear ledger, and an unreadable plan; assert one debt row per entry, the exact repair route, refusal before full verification or reviewer launch and existing full-check behavior on a clear plan. Run:

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
- 6: not yet written tests/test_stage2_fail_fast.py::test_repair_accepts_unclaimed_unwritten_ledger_ids — an unclaimed unwritten test alone rejects repair
- 7: not yet written tests/test_stage2_fail_fast.py::test_repair_fails_for_missing_written_ledger_test — a missing written proof is accepted
- 8: not yet written tests/test_stage2_fail_fast.py::test_standing_test_failure_is_not_hidden_by_missing_ledger_ids — a red selected test is accepted
- 9: not yet written tests/test_stage2.py::test_review_refuses_all_unwritten_ledger_entries_before_reviewer — a marker is omitted or the reviewer starts
- 10: not yet written tests/test_stage2.py::test_review_ledger_checkpoint_allows_clear_plan — written or non-test entries cause refusal
- 11: not yet written tests/test_stage2_fail_fast.py::test_unreadable_or_invalid_ledger_test_is_not_missing — a read or parse error becomes a missing ID or green
- 11: not yet written tests/test_stage2.py::test_review_refuses_unreadable_plan_at_ledger_checkpoint — unreadable plan is treated as clear
- 12: not yet written tests/test_stage2.py::test_repair_rejects_missing_claimed_proof — the existing answer check accepts an undefined ordinary or guard-test claim
- 13: not yet written tests/test_stage2.py::test_repair_still_requires_finding_proof_with_missing_ledger_ids — missing finding proof is accepted
- 14: not yet written tests/test_stage2_fail_fast.py::test_implement_prompt_requires_all_ledger_tests — an unwritten test is optional in the implement prompt
- 15: not yet written tests/test_stage2_fail_fast.py::test_repair_prompt_distinguishes_finding_proof_from_unwritten_tests — repair omits the written-test or finding-proof obligation, or the named-but-not-owed statement
- 16: not yet written tests/test_stage2_fail_fast.py::test_repair_prompt_pytest_list_excludes_missing_ledger_ids — a missing ID is supplied to model-run pytest
- 17: not yet written tests/test_stage2_fail_fast.py::test_missing_ledger_file_is_reported_as_missing — an absent file becomes a read fault
- 18: not yet written tests/test_stage2_fail_fast.py::test_repair_prompt_reports_uninspectable_ledger_test — an unreadable or invalid file prevents the prompt or is silently listed as standing
- 19: not yet written tests/test_stage2.py::test_ledger_debt_claim_must_match_and_pass — a mismatched, absent or failing claimed test is accepted
- 20: not yet written tests/test_stage2.py::test_ledger_debt_proof_accepts_test_green_on_baseline — a passing ledger-debt test is rejected for passing on baseline
- 21: not yet written tests/test_stage2.py::test_ledger_debt_exception_requires_marked_entry — an unrelated or already-written test bypasses ordinary proof
- 22: not yet written tests/test_stage2.py::test_ledger_debt_repair_clears_marker — an accepted repair leaves the marker, including for a rewritten async test

## Time used

2026-11-20 17:19:37–17:22:38 UTC, 181 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-20 17:28:09–17:31:32 UTC, 203 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-20 17:39:25–17:42:29 UTC, 185 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
