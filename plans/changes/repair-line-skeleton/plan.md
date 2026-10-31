---
title: "Plan — repair-line-skeleton"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-k93f
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, repair]
---

# Plan — repair-line-skeleton

```text
For you:     Repair answers arrive as prefilled lines; one unreadable completion no longer discards other proven repairs.
Done when:   Tests prove typed skeletons, independent acceptance and safe continuation after a partial checkpoint, and make verify is green.
Appetite:    3 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     New answer languages, routes, attempts, evidence standards or answer handling for other verbs.
Pre-mortem:  suppose it failed: most likely because a partial checkpoint loses the original baseline needed to prove a pending repair.
Starts unless you say stop.
```

Proposed against `249840c7`, inspected 2026-10-31; no implementation yet.
Class bounded: no design or ADR. `templates/plan.md` is absent; this follows
the phase-3 prompt. Explore used Stage 2, GLM 5.3 Flash, with no Stage-1
fallback to carry forward. Decisions are in the reasoned interview skip and
the three details in `decisions.md`; do not re-interview or rewrite them.

## Files and steps

1. `prompts/04-implement.md` — **orchestrator only**, as a bootstrap edit
   outside the accepted guarded attempt: replace the repair answer paragraph
   with copy-and-fill instructions, typed fields and the partial-result rule.
   The guarded attempt never edits this held path or loosens its guard.
2. `tests/test_stage2_repair_skeleton.py` — create the ledger regressions
   using `World`, repair fixtures and synthetic process results from
   `tests/test_stage2.py`; no live model calls. Parameterize row location,
   route, omitted/malformed/unfilled/conflicting/wrong-kind completions and
   failed proof. Include free-text identifiers and escaped reason pipes.
3. `scripts/stage2.py` — add one deterministic skeleton renderer, used by
   `repair_prompt` for every endpoint and its cached retry prompt. Preserve
   the taken-row description block; add a separate ordered fill-in block:
   `<ID>: fixed — tests/<path>::<function>` or
   `<ID>: fixed — not a test — <reason>`. Match the taking kind using the
   existing Status interpretation. Tell the model to copy each line, replacing
   only its field; never prefill the repair reason from the taking reason.
4. In `scripts/stage2.py`, split answer checking into shared guards and
   independent known-row outcomes. Preserve exact-id matching, incidental
   prose tolerance, literal claim deduplication, conflicts, canonical status
   parsing and unknown-id refusal. Reject unchanged field sentinels explicitly.
   Return proven fixes/marks alongside row diagnostics; shared failure yields
   no accepted subset. Check definitions, red-first and fixed-code proof per
   eligible row, without abandoning unrelated rows at the first row error.
   Ordinary red/green proof failures belong to their row; proof-environment
   mutation, unsafe restoration and other integrity failures remain shared
   stops. Preserve credential protection and existing proof refusal boundaries.
5. In `scripts/stage2.py`, let `repair` distinguish all-failed from partial
   results in its answer-check closure: no fixes returns diagnostics to the
   existing ladder; some proven fixes and only row failures permits the
   existing verified checkpoint. Filter the taken list passed to both status
   writers to accepted identifiers, avoiding their full-dictionary assumption.
   Do not bypass `verify_attempt`, full verification, audit checks, record
   locks, answer retention, scans or checkpoint recovery. Shared failures
   never reach the partial-success branch. Keep generic `run_attempts`
   behavior for implement and post-commit record-write recovery unchanged.
6. In `scripts/stage2.py`, persist a runner-owned pending-baseline receipt
   in findings before that checkpoint, beside protected per-row diagnostics:
   each pending exact identifier maps to its original full commit hash.
   Use a dedicated unquoted `## Pending repair baselines` section with one
   JSON object in a fenced block; ignore quoted model output and reject
   duplicate sections/keys, invalid hashes or unavailable/non-ancestor commits
   before any call. Absence on a first repair means current HEAD; a present
   unreadable receipt refuses, never silently resets the baseline. Retain
   mappings only for still-taken rows; new rows use the invocation's HEAD.
   Pass the resulting per-row baseline map to proof checks (keep the existing
   baseline argument as the default for callers without a receipt).
7. Keep receipt updates in the same pre-commit findings snapshot/rollback
   boundary as accepted statuses; failed shared checks add no acceptance
   receipt, and a rolled-back checkpoint restores it with the statuses.
   After a successful partial checkpoint and record marking, report accepted
   and pending identifiers and return a nonzero failure describing the pending
   rows, without spending another route in this invocation. Full acceptance
   clears fulfilled mappings and returns success. A later call excludes fixed
   rows, keeps pending baselines and proves them against the original code.
   Do not call a partial checkpoint a wholly rejected attempt or all rows fixed.
8. `tests/test_stage2.py` — preserve existing test function names but update
   multi-row rejection expectations that now require partial acceptance;
   retain all-bad retry, unknown-id, proof, audit and rollback assertions.
   Update the shared contract assertions to match the new row-local wording.
   `tests/test_stage2_fail_fast.py` needs no planned edit: run its existing
   prompt and verification-order regressions unchanged.
9. `docs/WORKFLOW.md` — revise only “Repairing taken findings”: typed
   skeletons, field completion, row failures versus shared failures, partial
   outcome/continuation, retained original baseline and runner-derived marks.
   `plans/changes/repair-line-skeleton/plan.md` — remove `not yet written`
   from ledger entries as their tests land; the runner appends measured time.
   `plans/changes/repair-line-skeleton/findings.md` — runner-owned audit,
   repair receipts and review evidence. `plans/INDEX.md` — runner regeneration.
   No file is deleted; this change's spec, research and decisions remain inputs.

## Verification

The orchestrator ensures this worktree's `make venv` and
`bash tools/pi/install.sh` setup has completed. Show each new behavior red
against baseline code and green after the implementation. Partial-result
tests must inspect both findings and the loop record and then run a second
repair whose proof would pass incorrectly on the new HEAD; assert the original
baseline is actually used. Include two pending rows with different historical
baselines, a new row, a malformed receipt and checkpoint rollback. No live calls.

```sh
.venv/bin/python3 -m ruff check scripts/stage2.py tests/test_stage2.py tests/test_stage2_repair_skeleton.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py tests/test_stage2.py tests/test_stage2_repair_skeleton.py
.venv/bin/python3 -m pytest -q -n auto tests/test_stage2_repair_skeleton.py tests/test_stage2.py tests/test_stage2_fail_fast.py
.venv/bin/python3 scripts/check_interview_minimums.py --change repair-line-skeleton
.venv/bin/python3 scripts/check_research_handoff.py --change repair-line-skeleton
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

`scripts/validate_change_artefacts.py` is absent at the inspected baseline;
its advertised check cannot be run. Draft-local checks use the three available
artifact gates above. Registry checking, index generation, full verification
and the commit belong to the outer runner, not this drafting call.

Draft checks on 2026-10-31: interview minimums passed, research handoff passed
with this non-swarm change exempt, the criterion ledger passed, and
`git diff --check` passed. Implementation tests and full verification have
not run in this drafting call.

## Criterion ledger

- 1: not yet written tests/test_stage2_repair_skeleton.py::test_skeletons_cover_only_taken_rows_on_every_route — a source or route omits, repeats or invents a skeleton
- 2: not yet written tests/test_stage2_repair_skeleton.py::test_skeleton_kind_comes_from_taken_status — the kind changes or the taking reason becomes claimed repair evidence
- 3: not yet written tests/test_stage2_repair_skeleton.py::test_copied_lines_keep_the_fixed_status_contract — prose, identical repetitions or distinct conflicts are misread
- 4: not yet written tests/test_stage2_repair_skeleton.py::test_bad_completion_does_not_discard_another_proven_row — a row failure loses another row's fixed status or mark
- 5: not yet written tests/test_stage2_repair_skeleton.py::test_each_accepted_code_row_keeps_both_proofs — missing, baseline-green or fixed-red evidence earns acceptance
- 6: not yet written tests/test_stage2_repair_skeleton.py::test_shared_failure_never_accepts_a_subset — unknown ids, verification, audit, evidence or rollback failures leak acceptance
- 7: not yet written tests/test_stage2_repair_skeleton.py::test_partial_checkpoint_preserves_pending_baselines — a second call repeats a fixed row, loses pending diagnostics or proves against the new HEAD
- 7: not yet written tests/test_stage2_repair_skeleton.py::test_pending_baseline_receipts_fail_closed_and_rollback — invalid/ambiguous receipts are ignored or a rollback leaves acceptance bookkeeping
- 8: not yet written tests/test_stage2_repair_skeleton.py::test_zero_accepted_rows_keep_the_existing_retry_ladder — empty success, changed routes or lost protected answer evidence
- 9: not yet written tests/test_stage2_repair_skeleton.py::test_repair_documents_describe_field_completion_and_partial_results — any shared instruction retains whole-batch rejection for a known-row error

## Not touched

No ADR, design file, dependency, gate declaration, endpoint, permission,
tracker state, other change, other verb's answer handling, format-reminder
call or new persistent storage location. The only held edit is explicitly
assigned to the orchestrator in step 1. Drafting writes no implementation,
git state or time entries.

## Time used
