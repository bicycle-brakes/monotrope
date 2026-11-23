---
title: "Plan — ledger-ids-before-pytest"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-22
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
For you:     Missing ledger tests are named early, and repairs can finish their own findings.
Done when:   Focused tests prove those boundaries and make verify is green.
Appetite:    4 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     A phase-6 checkpoint for unwritten tests, a new ledger format, or weaker proof for repairs.
Pre-mortem:  suppose it failed: most likely because a successful repair loses the missing-test record.
Starts unless you say stop.
```

## Build sequence and files

1. Change `scripts/stage2.py`: after lint, classify both recognized forms of the accepted plan's ledger with the existing parsed-name check before pytest; preserve each ID's written or unwritten status, with written taking precedence for duplicates. Distinguish absent files or names from read and parse faults. Keep changed-test and retry selection, whole-file coverage and deduplication, but never pass a missing ledger ID to pytest. Run standing targets even when implement owes missing tests; skip pytest if none stand. Preserve pytest failures and every missing ID in an accepted attempt's `plan.md` time line or a failed attempt's `findings.md` diagnostics. Pass attempt type and diagnostic evidence through both full and targeted paths: implement fails for either missing ledger form; repair fails for a missing written entry, but a missing unwritten-only entry alone does not fail its cheap check. Preserve the existing finding-proof checks.
2. In `scripts/stage2.py`, update both prompt variants: implement owes every ledger test; repair owes written entries and its findings' tests, reports other unwritten tests without owing them, and its model-run pytest list excludes missing IDs. An absent file is missing; an existing unreadable or invalid file is a fault. Repair prompt construction must still succeed and identify an uninspectable input without presenting it as standing. Exclude malformed ledger lines from cheap selection; leave their diagnosis to the existing gate.
3. Change `tests/test_stage2_fail_fast.py` and `tests/test_stage2.py` to exercise the ledger below, updating the old assertion that deliberately sent a missing ledger ID to pytest and the prompt assertions. Keep existing test function names used by other ledgers. Use isolated fixtures and stubbed launches; cover both verification paths and accepted as well as failed attempt records.
4. Change `docs/WORKFLOW.md` to describe pre-launch diagnostics and implement and repair obligations, retaining the existing clearing order. Maintain this change's `spec.md` and `plan.md` status and ledger markers as work proceeds; the runner owns `findings.md` and time entries. No files are deleted; no design or ADR is due for this bounded change.

## Verification

Cover multiple missing IDs with a standing changed test, including a new whole test file; check pytest arguments, both record locations, outcome and order, including an earlier lint failure. Cover only-missing targets, successful and failing standing tests, duplicate written and unwritten references, retries, ordinary and guard-test claims, absent files, async definitions, definitions inside strings, malformed ledger entries, and unreadable or invalid files. Run:

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2_fail_fast.py tests/test_stage2.py
python3 scripts/check_interview_minimums.py --root . --change ledger-ids-before-pytest
python3 scripts/check_criterion_ledger.py --root .
make verify
```

The runner performs the final full check and commit. Explore used Stage 2, route `flash`, model `glm-5.3-flash`; it records no Stage-1 fallback. Do not change the ledger gate, clearing, phase-6 admission, finding-proof rules, or held paths.

## Criterion ledger

- 1: tests/test_stage2_fail_fast.py::test_ledger_ids_are_checked_before_pytest — a missing written or unwritten ID reaches pytest
- 2: tests/test_stage2_fail_fast.py::test_missing_ledger_ids_persist_in_attempt_record — a successful repair or failed attempt loses a missing ID
- 3: tests/test_stage2_fail_fast.py::test_standing_targets_run_when_ledger_ids_are_missing — a missing ID blocks a standing target, including in a new file
- 4: tests/test_stage2_fail_fast.py::test_only_missing_ledger_ids_skip_pytest — pytest starts without a standing target
- 5: tests/test_stage2_fail_fast.py::test_implement_fails_after_running_standing_tests_with_missing_ledger_ids — implement accepts missing ledger tests
- 6: tests/test_stage2_fail_fast.py::test_repair_accepts_unclaimed_unwritten_ledger_ids — an unwritten-only test alone rejects repair even if later claimed
- 7: tests/test_stage2_fail_fast.py::test_repair_fails_for_missing_written_ledger_test — a missing written proof is accepted, including when also marked unwritten
- 8: tests/test_stage2_fail_fast.py::test_standing_test_failure_is_not_hidden_by_missing_ledger_ids — a red selected test is accepted
- 9: tests/test_stage2_fail_fast.py::test_unreadable_or_invalid_ledger_test_is_not_missing — a read or parse error becomes a missing ID or green
- 10: tests/test_stage2.py::test_repair_rejects_missing_claimed_proof — the existing answer check accepts an undefined ordinary or guard-test claim
- 11: tests/test_stage2.py::test_repair_still_requires_finding_proof_with_missing_ledger_ids — missing finding proof is accepted
- 12: tests/test_stage2_fail_fast.py::test_implement_prompt_requires_all_ledger_tests — an unwritten test is optional in the implement prompt
- 13: tests/test_stage2_fail_fast.py::test_repair_prompt_distinguishes_finding_proof_from_unwritten_tests — repair omits an obligation or the named-but-not-owed statement
- 14: tests/test_stage2_fail_fast.py::test_repair_prompt_pytest_list_excludes_missing_ledger_ids — a missing ID is supplied to model-run pytest
- 15: tests/test_stage2_fail_fast.py::test_missing_ledger_file_is_reported_as_missing — an absent file becomes a read fault
- 16: tests/test_stage2_fail_fast.py::test_repair_prompt_reports_uninspectable_ledger_test — an unreadable or invalid file prevents the prompt or is silently listed as standing
- 17: tests/test_stage2_fail_fast.py::test_malformed_ledger_entry_is_not_selected — a malformed entry is selected or named as missing

## Time used

2026-11-20 17:19:37–17:22:38 UTC, 181 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-20 17:28:09–17:31:32 UTC, 203 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-20 17:39:25–17:42:29 UTC, 185 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-20 17:57:44–18:00:50 UTC, 186 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-20 19:50:24–22:17:52 UTC, 8848 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-20 22:31:44–2026-11-21 00:19:06 UTC, 6443 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 03:21:41–03:39:03 UTC, 1042 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-21 03:39:15–04:15:09 UTC, 2154 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 05:11:26–05:12:37 UTC, 71 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files none; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-21 05:32:13–06:03:25 UTC, 1872 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 06:20:47–06:44:07 UTC, 1400 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-21 10:53:08–11:10:00 UTC, 1013 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
