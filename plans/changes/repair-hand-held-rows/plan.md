---
title: "Plan — repair-hand-held-rows"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-22
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

1. In `scripts/stage2.py`, retain all existing pre-call guards over all resolved rows, then extract and normalize each `Where` path as the spec defines; do not reuse strict `where_locations`. Split on whitespace, commas and semicolons, strip wrappers, trailing punctuation and location suffixes including hash-line and en-dash ranges; extract both Markdown link text and target. Match an existing tracked directory without a trailing slash as that directory plus `/`. Apply the checkpoint's committed `_held_prefixes`, case-insensitive prefix semantics and applicable exceptions without another held list. A row with any held path is wholly held; unknown, non-held and pathless locations remain eligible.
2. Append the dated bullet listing once before the attempt snapshot, report every held id, path and reason, and preserve the listing over retries and checkpoint rollback. Make the listing invisible to finding-row resolution and use only valid, conditionally authorized hand-booking hints. For held-only batches use the existing checkpoint after preflight and exit 0 without a model call; retain its existing allowances for this change's findings and derived leftovers and refusal of other dirty work, and use `docs(<change>): hand steps for the orchestrator <ids>` as the commit subject. For mixed batches pass only eligible rows to the prompt, answer check, unchanged-row check and both booking functions; tell the model held rows are not its work, ignore answer lines naming held ids without booking them, and use only repaired ids in the commit subject and held ids in its body. Preserve all held cells and the existing checkpoint rollback.
3. In `tests/test_stage2.py`, cover the criterion ledger below against both active loop and findings rows; use the existing isolated repair fixtures, including failure and rollback paths. In `docs/WORKFLOW.md`, explain the split, the output and existing hand-booking responsibilities, including the test forms and the requirement to retake a row as `not a test` before using that fixed form when no test fits. Regenerate the index with its generator if headers change.

## Files

- `scripts/stage2.py`: classify selected rows, record and commit handoffs, and pass the eligible subset through the existing repair lifecycle.
- `tests/test_stage2.py`: add focused classification, handoff, booking, output and rollback regressions.
- `docs/WORKFLOW.md`: document the repair handoff and the orchestrator's existing hand step.
- `plans/changes/repair-hand-held-rows/decisions.md`: retain the corrected hand-booking decision.
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

- 1: tests/test_stage2.py::test_repair_classifies_held_paths_before_dispatch — a mixed-path row, held link text, case-folded prefix, unknown held file, `docs/adr, decisions.md` or `see prompts.` reaches the model, or an outside target is treated as inside
- 2: tests/test_stage2.py::test_repair_keeps_nonheld_locations_in_model_batch — a pathless row, unknown non-held path or non-held directory is dropped or refused
- 3: tests/test_stage2.py::test_repair_splits_mixed_held_and_committable_rows — a held row reaches the model or a committable row is omitted
- 4: tests/test_stage2.py::test_repair_hands_off_all_held_without_model_call — an all-held batch calls a model, exits nonzero or lacks stdout details
- 5: tests/test_stage2.py::test_repair_reports_and_records_each_held_path — stdout or findings omit an id, normalized path or reason
- 6: tests/test_stage2.py::test_repair_handoff_preserves_held_row_cells — handoff changes a held Status or test mark
- 7: tests/test_stage2.py::test_repair_lifecycle_checkpoint_rollback_reports_restoration — an unexpected held edit survives or is committed
- 8: tests/test_stage2.py::test_repair_mixed_batch_books_only_eligible_rows — an eligible fix fails to commit or the answer check requires a held id
- 9: tests/test_stage2.py::test_repair_handoff_preserves_existing_preflight_guards — a held legacy marker or invalid origin bypasses refusal
- 10: tests/test_stage2.py::test_repair_handoff_survives_failed_attempt_once — retry duplicates the listing or rollback loses it
- 11: tests/test_stage2.py::test_repair_all_held_commits_only_handoff — a successful held-only run leaves findings uncommitted or admits changes outside the existing checkpoint allowances
- 12: tests/test_stage2.py::test_repair_handoff_uses_dated_bullets — the listing is a table, undated, lacks normalized paths, or retains the location in `AGENTS.md#L24` or `agents.md:24–30`
- 13: tests/test_stage2.py::test_repair_handoff_is_not_resolved_as_a_finding — a subsequent resolution treats a listing bullet as a finding
- 14: tests/test_stage2.py::test_repair_mixed_commit_distinguishes_held_rows — the subject claims a held row or the body omits it
- 15: tests/test_stage2.py::test_repair_handoff_uses_valid_booking_hint — the hint uses an invalid form, omits the valid alternatives or permits not-a-test without the required taken status

- 16: tests/test_stage2.py::test_repair_held_only_commit_names_hand_steps — the subject claims held rows as repaired
- 17: tests/test_stage2.py::test_repair_ignores_answer_lines_for_held_rows — a held answer line fails the attempt or marks the row fixed
- 18: tests/test_stage2.py::test_repair_prompt_excludes_handed_off_rows — the prompt does not tell the model held rows are not its work
- 19: not a test — phase-6 review checks the workflow against the existing hand-booking forms and required taken status

## Runner route — 2026-11-22

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-22

Stage-1 route: repair · model claude-sonnet-5-5 · reason: Codex usage-limited until 2026-11-23 16:40; maintainer: repairs to Sonnet meanwhile.

## Time used

2026-11-21 11:54:22–11:56:35 UTC, 132 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:06:37–15:09:21 UTC, 164 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:16:23–15:18:11 UTC, 108 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:26:05–15:27:57 UTC, 112 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-22 13:21:47–14:03:52 UTC, 2525 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-22 14:04:01–14:41:38 UTC, 2257 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-22 14:41:47–14:42:44 UTC, 57 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-22 21:19:52–21:20:44 UTC, 52 s — repair · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
