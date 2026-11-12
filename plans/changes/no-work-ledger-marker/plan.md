---
title: "Plan — no-work-ledger-marker"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-11
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-twbl
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, no-work-check]
---

# Plan — no-work-ledger-marker

```text
For you:     A retry cannot pass as model work solely because the runner cleared a pending-test marker.
Done when:   Tests reject that retry for implement and repair, preserve real model edits and ledger clearing, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Retry-policy changes, new ledger rules, or a broader definition of model work.
Pre-mortem:  suppose it failed: most likely because the discount also hides a genuine model edit in the same ledger entry.
Starts unless you say stop.
```

## Files and steps

1. Change `tests/test_stage2.py`: first add the retry regression below and
   demonstrate its false acceptance on the input runner; add the positive
   attribution and failed-measurement cases without live model calls.
2. Change `scripts/stage2.py`: capture actual ledger clearing in both
   `verify_attempt` and `_targeted_body`, and pass attempt-local evidence
   through `run_attempts` to `attempt_has_work` for the narrow discount below.
3. Change `docs/WORKFLOW.md`: add actual runner clearing to the implement/repair
   work-discount paragraph, distinguishing it from surviving model edits.
4. Update `plans/changes/no-work-ledger-marker/plan.md`: clear pending test
   references as they land; the runner owns its time section,
   `plans/changes/no-work-ledger-marker/findings.md` and `plans/INDEX.md`.
   No other file is created or deleted; no held-path bootstrap edit is needed.

## Implementation contract

- Wrap the existing `clear_written` calls with one shared capture helper in
  `scripts/stage2.py`. Record the plan bytes immediately before and after the
  actual clearing, after formatting and cheap checks and before stamping.
  Retain the exact changed ledger entries and their section positions;
  criterion numbers alone cannot identify several tests for one criterion.
- Start a fresh evidence container for every model call. Pass it through
  full and targeted verification to the final work check, including targeted
  fallback to full checks. Preserve optional defaults for direct callers;
  no clearing evidence means no new discount. A failed required read or
  comparison rejects with its reason, never a permissive work result.
- In the in-memory final-plan comparison only, undo the exact marker removals
  captured from that attempt's clearing; preserve all other bytes. Match
  recorded entries within their ledger section, not every equal string in
  the document. Never recompute eligibility from the later test tree, apply
  a blanket marker replacement, or ignore the whole plan. Unmatched or
  ambiguous evidence must fail closed. Do not write the comparison back.
- Apply the existing time-body and stamp masking to that comparison, against
  the original pre-call plan. Keep the unbounded Git candidate filter and
  all other discounts, mode/binary handling and per-call baselines. Other
  plan edits, including changed references or explanations on a cleared
  entry, remain visible. A marker the model already removed produces no
  clearing event and remains eligible as work.
- Keep alias/hard-link refusals before capture, and leave the clearing order,
  rejection flow, time writer, diagnostics, repair proofs and checkpoint
  restrictions unchanged; do not change verification's return contract.
- Parameterize the retry regression over both verbs: seed a marked ledger,
  have attempt 1 create its test but fail verification, assert the retry
  restores the marker while retaining the test, then have remaining attempts
  edit only the time body. Assert each later clearing occurs, every retry
  is rejected as no work, records remain rejected exactly once per call,
  repair rows stay taken, exhaustion exits 1 and HEAD does not advance.
  Force the first repair's full-check fallback as in the existing idle-retry
  fixture; also exercise a repair that takes the actual targeted path.
- Cover one and multiple cleared entries, repeated criterion numbers,
  adjacent prose, fenced examples and missing tests. Pair clearing with
  real prose, ledger reference/explanation and other-file edits; separately
  let the model clear a marker itself. A control with no recorded clearing
  must not mask a model edit. Inject a capture/comparison failure and assert
  reported rejection without checkpoint; retain existing clearing-order,
  alias-refusal and no-work regressions.

## Criterion ledger

- 1: tests/test_stage2.py::test_runner_ledger_clearing_cannot_qualify_a_retry — a time-only retry is accepted using a retained test's runner-cleared marker
- 2: tests/test_stage2.py::test_ledger_discount_preserves_model_work — the discount hides model prose, a ledger rewrite, a model-cleared marker or another file's edit
- 2: tests/test_stage2.py::test_work_check_accepts_nonempty_changes — existing code, document, binary or mode work is refused
- 3: tests/test_stage2.py::test_implement_clears_the_ledger_marker_of_a_test_the_attempt_wrote — an eligible marker survives verification
- 3: tests/test_stage2.py::test_the_ledger_is_cleared_after_formatting_before_stamping_and_verify — clearing runs before formatting or after stamping/verification
- 3: tests/test_stage2.py::test_clearing_the_ledger_refuses_an_aliased_parent_or_a_hard_link — capture or clearing writes through an alias
- 3: tests/test_stage2.py::test_ledger_discount_keeps_clearing_in_both_verify_modes — full or targeted verification skips eligible entries or changes fenced/missing-test entries
- 4: tests/test_stage2.py::test_runner_ledger_clearing_cannot_qualify_a_retry — marker-only retries lose diagnostics/records, mark repairs fixed or checkpoint on exhaustion
- 4: tests/test_stage2.py::test_no_work_rejection_reaches_existing_retry — the next allowed call loses the no-work reason
- 4: tests/test_stage2.py::test_empty_attempt_keeps_rejected_records — audit or measured time is lost, duplicated or accepted
- 4: tests/test_stage2.py::test_all_empty_attempts_leave_no_checkpoint — exhaustion reports success or moves HEAD
- 5: tests/test_stage2.py::test_ledger_discount_measurement_failure_prevents_acceptance — unreadable or ambiguous clearing evidence permits acceptance
- 5: tests/test_stage2.py::test_work_measurement_failure_prevents_acceptance — failed tree or diff measurement permits acceptance

## Verification

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m pytest tests/test_stage2.py tests/test_stage2_fail_fast.py tests/test_check_criterion_ledger.py -q
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_interview_minimums.py --change no-work-ledger-marker
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_criterion_ledger.py
PYTHON=$PWD/.venv/bin/python3 make verify
```

The retry regression must be red before the runner fix and green afterward;
the ordinary suite and final full verification must pass. The runner owns
full verification and the commit. At input `c54bbdd5`, neither
`templates/plan.md` nor `scripts/validate_change_artefacts.py` exists; use the
phase-3 prompt's form and the available interview, ledger and registry gates.

## Boundaries and Explore route

Do not edit `scripts/check_criterion_ledger.py`,
`plans/specs/implementation-verification/spec.md`, other changes' artifacts,
or the protected areas in the spec. Research used Stage 2 on 2026-11-10,
route `flash`, model `glm-5.3-flash`; it records no Stage-1 fallback.
The bounded class requires neither a design nor an ADR. The orchestrator
shows the card with the already-recorded interview skip before implementation.

## Runner route — 2026-11-12

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-12 02:31:16–03:06:16 UTC, 2100 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-12 03:06:27–03:14:54 UTC, 508 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-12 03:15:05–03:40:41 UTC, 1535 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
