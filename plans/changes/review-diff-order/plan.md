---
title: "Plan — review-diff-order"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-ut8q
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, review-loop, stage-2]
---

# Plan — review-diff-order

```text
For you:     Paid review rounds see code and tests before prose; findings and the generated plans index no longer consume their diff budget.
Done when:   the criterion ledger holds exclusions, ordering, retained changes and unchanged cut/free/receipt behavior, and `make verify` is green.
Appetite:    1 h of phase 4, repairs included, plus 45 min granted on 2026-10-29 after the stop at about 1.5 h; a stop, not an estimate.
Not now:     splitting large diffs, larger bounds, compaction, model routing or changed review access.
Pre-mortem:  suppose it failed: most likely because paid filtering also changes the raw diff used to invalidate availability receipts.
Starts unless you say stop.
```

Implements [spec.md](spec.md), criteria 1–7, from base `2363f0e`.
Phase 1 used Stage 2 route `flash`, model `glm-5.3-flash`, on 2026-10-29;
no Stage-1 fallback was recorded. No design phase or ADR draft is due.

## Steps and files

1. `tests/test_stage2.py`: add the new tests named below using the existing
   isolated `world` fixture; demonstrate each changed behavior red first.
   Exercise exclusions as tracked/untracked files, exact-name lookalikes,
   and tracked prose mixed with untracked source/tests. Compare full Git
   file diffs before bounding, not merely presence of filenames; cover
   deletion, rename pairs, staged/unstaged edits, CRLF, spaces, newline and
   pathspec metacharacters in filenames. Use stand-ins, no live model calls.
2. `scripts/stage2.py`: add `paid_review_diff(root)` and use it only in the
   paid branch of `_review_round`, before `bounded_review_diff`.
   - Enumerate changed paths with `git diff --name-only --no-renames -z`
     against `_merge_base(root)`, union with NUL-delimited untracked paths;
     deduplicate, exclude exact basenames `findings.md` and `plans/INDEX.md`.
   - Sort by `(prose, relative_path)` using the spec's Terms: `docs/`,
     `plans/`, `prompts/` and suffixes `.md`, `.rst`, `.txt`, `.adoc` are prose;
     all other paths are implementation inputs. Tracked status is no sort key.
   - Emit each complete tracked file diff against the base with
     `--no-renames` and a literal pathspec; untracked paths use the existing
     relative `--no-index -- /dev/null <path>` form, allowing exits 0 and 1.
     Retain `--no-color --no-ext-diff --no-textconv` and `_git_output` refusal
     behavior; use its `preserve_newlines=True` so hunk text is not rewritten.
     Do not parse diff headers or import `_free_candidate` restrictions.
   - Keep `change_diff` unchanged: availability binding must hash the full
     raw diff. Leave `free_diff`, probes, bounds and cut/release parsers alone.
3. `tests/test_stage2.py`: add a paid-round prompt test with source/tests
   fitting under a reduced test bound, larger leading prose and excluded
   findings/index content; assert order and budget in every paid member's
   prompt. Compare `stage2_availability.binding` before/after findings-only
   and index-only edits. For mixed free inputs, assert the existing tracked-
   then-untracked order, source-only contents and matching free probe input.
4. `docs/WORKFLOW.md`: clarify §4's paid input excludes the named paths,
   places implementation inputs before prose and applies the existing bound
   afterwards; replace the misleading paid/free "same bounded diff" wording.
   The matching edit of `prompts/04b-review-loop.md` (its Input paragraph,
   preserving paid read tools and the free stage's distinct confinement) is
   not the model's: a stage-2 run does not commit `prompts/`. The
   orchestrator makes it after the accepted attempt, as a bootstrap edit
   (revised 2026-10-29, maintainer's decision).
5. `plans/changes/review-diff-order/plan.md`: replace completed
   `not yet written` ledger entries and record measured phase-4 time below.
   `plans/changes/review-diff-order/findings.md`: retain runner audit and
   review evidence. `plans/INDEX.md`: regenerate through the registry, never
   hand-edit it. No files are deleted; no other files need edits.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_paid_review_diff_excludes_only_named_records — an excluded tracked/untracked file appears, or a lookalike is dropped.
- 2: not yet written tests/test_stage2.py::test_paid_review_diff_orders_tracked_and_untracked_together — tracked prose precedes untracked implementation or group/path order varies.
- 3: not yet written tests/test_stage2.py::test_paid_review_diff_preserves_retained_file_diffs — any state, rename side, literal path or original line ending is lost or duplicated.
- 4: not yet written tests/test_stage2.py::test_paid_round_bounds_the_filtered_ordered_diff — sorting/filtering happens after the cut, or a paid member receives the raw diff.
- 4: not yet written tests/test_stage2.py::test_paid_review_diff_at_the_bound_is_not_cut — the at-limit input falsely records a cut.
- 5: tests/test_stage2.py::test_an_oversized_diff_reaches_the_paid_prompt_cut_and_the_record_says_so — an over-limit paid round hides its cut or ends cleanly.
- 5: tests/test_stage2.py::test_a_cut_round_stays_cut_after_the_release — release forgets the cut and blocks the next round as clean.
- 6: not yet written tests/test_stage2.py::test_paid_diff_projection_leaves_free_inputs_unchanged — invoking paid projection alters free review/probe input or its order.
- 6: tests/test_stage2.py::test_free_diff_reports_its_own_cut — either free bound loses its cut note.
- 6: tests/test_stage2.py::test_a_free_round_over_a_cut_file_is_never_clean — a free cut no longer blocks clean stop.
- 7: not yet written tests/test_stage2.py::test_paid_exclusions_leave_availability_binding_sensitive — findings-only or index-only edits no longer change the receipt binding.

## Verification

Run the affected `tests/test_stage2.py` cases first; then `make verify`.
The runner regenerates the index and owns full verification and the commit.
`python3 scripts/validate_change_artefacts.py --check` is unavailable in the
read base; do not report it green. Available artifact checks, verbatim:

```sh
python3 scripts/check_interview_minimums.py --change review-diff-order
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py --change review-diff-order
make verify
```

Draft checks on 2026-10-29: interview minimum and criterion ledger passed;
research handoff reported exemption because no research-swarm/v2 run exists.
The commands used this worktree's `.venv/bin/python3`; full verification is
the runner's next gate, not a result claimed by this draft.

## Untouched

`docs/adr/`, `model-endpoints.yaml`, `scripts/stage2_availability.py`, the
predecessor measurement, free admission/order/bounds, raw `change_diff`,
read tools and loop state/stop/release rules retain their current behavior.

## Time used
2026-10-29 17:36–19:07:41 UTC — implement · attempts 1 (flash, 1 test red) and 2 (flash-repair, refused: it changed `prompts/04b-review-loop.md`, a path a stage-2 run does not commit, though plan step names it) · measured with `date -u`
Appetite stop, 2026-10-29 19:10 UTC: about 1.5 h of the 1 h appetite used; parked. The plan's prompt step contradicts the runner's commit rule; the maintainer decides.
Revised 2026-10-29 about 22:25 UTC (maintainer's decision of about 19:25 UTC): the prompt edit moves from the model to the orchestrator; 45 more minutes, read as counted from the stop at about 1.5 h.
