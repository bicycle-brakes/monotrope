---
title: "Plan — repair-hand-held-rows"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-0zhf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, repair]
---

# Plan — repair-hand-held-rows

```text
For you:     Repair hands held-path findings to the orchestrator and continues with the other taken rows.
Done when:   Mixed and held-only batches show the hand steps, preserve their rows, and the repair and verification checks pass.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Changes to other verbs, held-path policy, model routes or the orchestrator's hand-repair bookkeeping.
Pre-mortem:  suppose it failed: most likely because a held path in a finding's Where cell is missed.
Starts unless you say stop.
```

## Scope and build

This is bounded: no design or ADR is due. The explore used the Stage-2 Flash route, endpoint `glm-coding-plan`, model `glm-5.3-flash`; no Stage-1 fallback was recorded.

1. In `scripts/stage2.py`, retain all existing pre-call guards over all resolved rows, then extract and normalize each `Where` path as the spec defines; do not reuse strict `where_locations`. Apply the checkpoint's committed `_held_prefixes`, case-insensitive prefix semantics and applicable exceptions without another held list. A row with any held path is wholly held; unknown, non-held and pathless locations remain eligible.
2. Append the dated bullet listing once before the attempt snapshot, report every held id, path and reason, and preserve the listing over retries and checkpoint rollback. Make the listing invisible to finding-row resolution and use only valid, conditionally authorized hand-booking hints. For held-only batches use the existing checkpoint after preflight to commit only the handoff and exit 0 without a model call; retain refusal of unrelated dirty work. For mixed batches pass only eligible rows to the prompt, answer check, unchanged-row check and both booking functions; use only repaired ids in the commit subject and held ids in its body. Preserve all held cells and the existing checkpoint rollback.
3. In `tests/test_stage2.py`, cover the criterion ledger below against both active loop and findings rows; use the existing isolated repair fixtures, including failure and rollback paths. In `docs/WORKFLOW.md`, explain the split, the output and existing hand-booking responsibilities. Regenerate the index with its generator if headers change.

## Files

- `scripts/stage2.py`: classify selected rows, record and commit handoffs, and pass the eligible subset through the existing repair lifecycle.
- `tests/test_stage2.py`: add focused classification, handoff, booking, output and rollback regressions.
- `docs/WORKFLOW.md`: document the repair handoff and the orchestrator's existing hand step.
- `plans/changes/repair-hand-held-rows/spec.md`: retain the contract and update implementation metadata when warranted.
- `plans/changes/repair-hand-held-rows/plan.md`: replace ledger placeholders with existing tests and record phase-4 time.
- `plans/changes/repair-hand-held-rows/findings.md`: retain the audit and let the runner append attempt and review evidence.
- `plans/INDEX.md`: regenerate the derived index if headers change; do not edit it by hand.

Do not change `implement`, `draft`, prompts, held configuration, other changes, ADRs or tracker data. No implementation-time file deletion is planned.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --root . --change repair-hand-held-rows
python3 scripts/check_criterion_ledger.py --root .
python3 scripts/plans_registry.py --check
make verify
```

At draft baseline `4d76c9c8`, `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent; the plan follows the phase-3 prompt. The runner owns full verification and the commit.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_repair_classifies_held_paths_before_dispatch — a mixed-path row, normalized Markdown link, case-folded prefix, unknown held file or held directory reaches the model, or an outside path is treated as inside
- 2: not yet written tests/test_stage2.py::test_repair_keeps_nonheld_locations_in_model_batch — a pathless row, unknown non-held path or non-held directory is dropped or refused
- 3: not yet written tests/test_stage2.py::test_repair_splits_mixed_held_and_committable_rows — a held row reaches the model or a committable row is omitted
- 4: not yet written tests/test_stage2.py::test_repair_hands_off_all_held_without_model_call — an all-held batch calls a model, exits nonzero or lacks stdout details
- 5: not yet written tests/test_stage2.py::test_repair_reports_and_records_each_held_path — stdout or findings omit an id, normalized path or reason
- 6: not yet written tests/test_stage2.py::test_repair_handoff_preserves_held_row_cells — handoff changes a held Status or test mark
- 7: tests/test_stage2.py::test_repair_lifecycle_checkpoint_rollback_reports_restoration — an unexpected held edit survives or is committed
- 8: not yet written tests/test_stage2.py::test_repair_mixed_batch_books_only_eligible_rows — an eligible fix fails to commit or the answer check requires a held id
- 9: not yet written tests/test_stage2.py::test_repair_handoff_preserves_existing_preflight_guards — a held legacy marker or invalid origin bypasses refusal
- 10: not yet written tests/test_stage2.py::test_repair_handoff_survives_failed_attempt_once — retry duplicates the listing or rollback loses it
- 11: not yet written tests/test_stage2.py::test_repair_all_held_commits_only_handoff — a successful held-only run leaves findings uncommitted or includes unrelated changes
- 12: not yet written tests/test_stage2.py::test_repair_handoff_uses_dated_bullets — the listing is a table, undated or lacks the normalized paths
- 13: not yet written tests/test_stage2.py::test_repair_handoff_is_not_resolved_as_a_finding — a subsequent resolution treats a listing bullet as a finding
- 14: not yet written tests/test_stage2.py::test_repair_mixed_commit_distinguishes_held_rows — the subject claims a held row or the body omits it
- 15: not yet written tests/test_stage2.py::test_repair_handoff_uses_valid_booking_hint — the hint uses an invalid form or permits not-a-test for a code row

## Time used

2026-11-21 11:54:22–11:56:35 UTC, 132 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:06:37–15:09:21 UTC, 164 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
