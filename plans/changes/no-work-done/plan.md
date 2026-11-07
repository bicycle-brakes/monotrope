---
title: "Plan — no-work-done"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-te7q
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, acceptance]
---

# Plan — no-work-done

```text
For you:     Empty implement and repair attempts are rejected instead of reported as verified and committed.
Done when:   Tests prove no-work rejection, acceptance of real document or code work, existing retry behavior and preserved records, and make verify is green.
Appetite:    3 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Every-planned-file checks, proof of completeness, provider or retry-policy changes.
Pre-mortem:  suppose it failed: most likely because runner bookkeeping is mistaken for model work.
Starts unless you say stop.
```

## Files and steps

1. Change `scripts/stage2.py`: add one work predicate at the shared
   `run_attempts` verdict boundary for implement and repair, using per-call
   tree snapshots and the bookkeeping normalization below.
2. Change `tests/test_stage2.py`: add the ledger's tests with the existing
   `World` model/verifier stand-ins and update successful no-op scenarios to
   perform actual work without changing their original assertions or names.
3. Change `docs/WORKFLOW.md`: describe the no-work rejection beside phase 4's
   runner-owned audit, time and checkpoint contract, including repair coverage.
4. Change `plans/specs/implementation-verification/spec.md`: clarify that its
   first-attempt derived-index guarantee presupposes actual work; findings
   creation or regeneration alone cannot satisfy the new acceptance condition.
5. Update `plans/changes/no-work-done/plan.md`: replace pending ledger entries
   as tests land; leave time to the runner, which maintains
   `plans/changes/no-work-done/findings.md` and regenerates `plans/INDEX.md`.
   No implementation file is created or deleted; no held-path bootstrap edit
   is required. Do not edit the protected paths listed in the spec.

## Implementation contract

- Capture the full before/after model-call trees once and retain their ids.
  Keep the existing bounded `attempt_files` output for diagnostics only:
  never parse its display strings or truncated list for the work verdict.
  Compare unbounded, NUL-delimited Git records, including mode-only and
  binary changes, additions and deletions. A same-byte rewrite is empty.
- Compare each call with its own pre-call state, not the invocation's HEAD:
  retained code from a rejected earlier attempt cannot qualify an idle retry.
  Runner audit lines, route insertion, time records, formatting, stamps and
  index rendering lie outside this measurement window. Do not exclude an
  entire path merely because the runner sometimes writes it: a model's own
  document or index edit remains eligible, subject to the existing checks.
- Discount this change's restored findings file. For its plan, compare bytes
  outside the time-section body using the existing time-section boundaries;
  the runner restores that body from the pre-call plan through the shared
  writer. Preserve differences elsewhere in that file and in other files.
  Malformed/unreadable plans still fail their existing checks; a failed tree
  read or comparison must add a measurement problem, never imply work.
- Add `no work done` to the ordinary post-run problem list before answer
  proofs, time verdict, repair-status marking and checkpoint. Preserve the
  existing findings restoration, recovery preflights, integrity/leak stops
  and verification behavior. Do not write through model-supplied aliases or
  relax a safety refusal to record this diagnostic.
- Reuse the current failure-record and retry machinery: implement keeps
  Flash, Flash-repair, Sonnet; repair keeps Codex, Codex-repair, Sonnet;
  explicit Stage-2-off keeps one Sonnet attempt. Completed empty calls retain
  one rejected measured entry; all-empty runs never checkpoint or mark rows
  fixed. A later attempt with its own work can pass the existing checks.
- Parameterize both verbs and the explicit fallback where applicable.
  Cover no edit, same-byte rewrite, findings-only and forged time-body edits;
  also exercise a bookkeeping-looking edit beside actual work. Cover real
  code/document changes, plan edits outside time, unplanned paths, tracked
  deletion, new file, binary bytes and executable-bit changes. Set the
  diagnostic file bound to one in a fixture so restored bookkeeping sorts
  before real work and exposes reliance on the shortened display list.
- Keep the existing derived-index and no-model-time-entry regressions.
  Existing timing, route and diagnostics tests may use otherwise idle model
  stand-ins; give success-designated attempts distinct real edits, including
  retries, without weakening their evidence. Run the whole runner test file
  and the unchanged `tests/test_stage2_fail_fast.py` restoration/check suite.
- Add a guard that, only under `STAGE2_PLANT_FAULT=1`, bypasses the production
  work predicate and actually lets the empty fixture reach acceptance;
  unconditional rejection/HEAD assertions then fail. Never use a switch-only
  assertion as the planted fault. Keep all provider calls stubbed.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_no_work_attempt_is_rejected — no edit, same bytes or discarded bookkeeping passes on either verb
- 1: not yet written tests/test_stage2.py::test_no_work_guard_detects_bypassed_check — bypassing the real predicate accepts the empty fixture
- 1: not yet written tests/test_stage2.py::test_idle_retry_cannot_reuse_previous_work — retained edits from the rejected call qualify an idle retry
- 2: not yet written tests/test_stage2.py::test_work_check_accepts_nonempty_changes — code, documents, plan prose, unplanned paths, binary or mode changes are rejected
- 2: not yet written tests/test_stage2.py::test_work_check_uses_unbounded_changes — a real edit beyond the diagnostic limit is missed
- 2: tests/test_stage2.py::test_runner_accepts_attempt_without_model_time_entry — real work is refused for lacking a model-written time line
- 2: tests/test_stage2.py::test_first_implement_refreshes_derived_files_without_a_model_repair — real work requires a repair solely for the generated index
- 3: not yet written tests/test_stage2.py::test_no_work_rejection_reaches_existing_retry — reason is absent from findings or retry prompt, routes change, or a working retry cannot pass
- 4: not yet written tests/test_stage2.py::test_all_empty_attempts_leave_no_checkpoint — default or explicit Stage-2-off exhaustion reports success or moves HEAD
- 5: not yet written tests/test_stage2.py::test_empty_attempt_keeps_rejected_records — audit or measured entry is lost, duplicated or accepted, or repair status becomes fixed
- 6: not yet written tests/test_stage2.py::test_work_measurement_failure_prevents_acceptance — unreadable snapshots or comparison errors reach a checkpoint
- 7: tests/test_stage2.py::test_a_postcheck_failure_gets_one_flash_repair_with_its_diagnostic — work bypasses a failing verifier
- 7: not yet written tests/test_stage2.py::test_nonempty_repair_still_requires_answer_proof — actual work bypasses the existing repair proof

## Verification

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m pytest tests/test_stage2.py tests/test_stage2_fail_fast.py -q
STAGE2_PLANT_FAULT=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m pytest tests/test_stage2.py::test_no_work_guard_detects_bypassed_check -q
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_interview_minimums.py --change no-work-done
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_criterion_ledger.py
PYTHON=$PWD/.venv/bin/python3 make verify
```

Show the empty-attempt regression red on the input runner, then green after
the fix. The planted-fault command must fail; the ordinary suite and full
verification must pass. The runner owns the full verification and commit.
At input `ed78f742`, no `templates/plan.md` or
`scripts/validate_change_artefacts.py` exists; this plan follows the phase-3
prompt and uses the available interview, ledger and registry gates.

## Explore route

Research records Stage-2 exploration on 2026-11-07, route `flash`, model
`glm-5.3-flash`; no Stage-1 exploration fallback is recorded. Phase 2b is
omitted for the answered bounded class, and no ADR is due.

## Time used
