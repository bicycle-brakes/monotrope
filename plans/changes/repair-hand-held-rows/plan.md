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

1. In `scripts/stage2.py`, after existing row resolution and pre-call refusals, split current taken rows using the checkpoint's committed held-prefix classification, case folding and exceptions. Read paths from `Where`, including multiple paths and location suffixes; do not use the finding prose as evidence. Keep rows with no readable path in the model batch. A row with at least one held path is wholly held.
2. Report each held row's identifier, every held path and `runner-held path` to the caller and append the same hand-step listing to `findings.md`, including in the held-only case. Preserve the listing across the attempt lifecycle and rollback; leave held rows' Status and `Broke a test` untouched. If all rows are held, stop without a model call; otherwise use only the committable subset in the prompt, answer validation and fixed-row booking. Retain the checkpoint's existing rollback for unexpected held edits.
3. In `tests/test_stage2.py`, exercise mixed and held-only batches, both row locations, multiple paths, case-folded and committed human-decided prefixes, pathless rows, unchanged held cells and the existing rollback. Capture calls and inspect both output and findings; cover a failed attempt as well as success so the handoff is not lost. Do not weaken existing rollback or lifecycle tests.
4. Update the repair section of `docs/WORKFLOW.md` to explain the split, handoff and unchanged orchestrator responsibilities. Refresh the registry through its generator if artifact headers change; the runner owns attempt records and checkpointing.

## Files

- `scripts/stage2.py`: classify the selected repair rows and record the handoff before dispatch.
- `tests/test_stage2.py`: add focused repair classification, handoff and rollback regressions.
- `docs/WORKFLOW.md`: document the repair handoff and the orchestrator's existing hand step.
- `plans/changes/repair-hand-held-rows/spec.md`: retain the contract and update implementation metadata when warranted.
- `plans/changes/repair-hand-held-rows/plan.md`: replace ledger placeholders with existing tests and record phase-4 time.
- `plans/changes/repair-hand-held-rows/findings.md`: retain the current audit and let the runner append attempt and review evidence.
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

At draft baseline `7b531fd0`, `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent; the plan follows the phase-3 prompt and the unavailable validator cannot be run. The runner owns the full verification and commit.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_repair_classifies_held_paths_before_dispatch — a mixed-path row or a case-folded committed held prefix reaches the model
- 2: not yet written tests/test_stage2.py::test_repair_keeps_pathless_rows_in_model_batch — a pathless row is dropped or handed off
- 3: not yet written tests/test_stage2.py::test_repair_splits_mixed_held_and_committable_rows — a held row reaches the model or a committable row is omitted
- 4: not yet written tests/test_stage2.py::test_repair_hands_off_all_held_without_model_call — an all-held batch calls a model or lacks a hand-step listing
- 5: not yet written tests/test_stage2.py::test_repair_reports_and_records_each_held_path — output or findings omit an id, path or reason, including after a failed attempt
- 6: not yet written tests/test_stage2.py::test_repair_handoff_preserves_held_row_cells — handoff changes a held Status or test mark
- 7: tests/test_stage2.py::test_repair_lifecycle_checkpoint_rollback_reports_restoration — an unexpected held edit survives or is committed

## Time used

2026-11-21 11:54:22–11:56:35 UTC, 132 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
