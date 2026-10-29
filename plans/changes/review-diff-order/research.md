---
title: "Research — review-diff-order"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-ut8q
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
---

# review diff order — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-29: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 733 files, 2633 commits, 12 rules.

## Runner exploration — 2026-10-29

Research complete. Below is the prose for `plans/changes/review-diff-order/research.md`, in the required structure (what exists today · where it lives · what is unclear · which files a change would have to touch), every statement with its source.

---

## What exists today

**The direct predecessor artefact.** `docs/research/2026-10-29-review-diff-cut.md` (status draft, same bead coding-harness-ut8q) measured the review diff of three changes on 2026-10-29 and is the factual basis of this change. Its result: `change_diff` hands Git's diff over in path order, so the change's own workflow files (`docs/`, `plans/` with the growing `findings.md`, `prompts/`, `scripts/`) come first and `tests/` last; the 2000-line cut therefore drops the tests. Measured cases: `fail-fast-attempts` (head `78676b5e`, 3371 diff lines, 1445 before any code, `findings.md` alone 582, `tests/test_stage2.py` 698 and `tests/test_stage2_fail_fast.py` 615 not seen at all), `index-merge-regenerates` (`60cd44f2`, 3209 lines, `tests/test_pr_sync.py` 1029 not seen), `run-report` (`358472d8`, 2284 lines, last 284 of `tests/test_run_report.py` not seen). Twelve rounds ran over a cut diff that night. The note names three options — leave `findings.md` and `plans/INDEX.md` out of the diff, order code and tests before prose, split a large change across reviewers — states they combine, and states they touch ADR 0021, so the choice is the maintainer's. Its "Not measured" section records that reviewer finding quality under a new order is unknown, and that the free stage has its own bounds (`FREE_DIFF_MAX_LINES`, `FREE_DIFF_MAX_TOTAL`) which did not run that night.

**The bead's origin and scope drift.** `docs/journal/handover/2026-10-23-night-run.md` (section "New bead coding-harness-ut8q") created the bead as a P1 spike: a diff over the 2000-line bound can never end the loop cleanly, with Pi auto-compaction as the background (`docs/compaction.md`; "whether disabling compaction also disables overflow recovery is not read", same handover). The night-run plans of 2026-10-26 and 2026-10-28 (`docs/research/2026-10-26-night-run-plan.md`, `docs/research/2026-10-28-night-run-plan.md`, item 5 each) still list it as "spike, research note only". The handover of 2026-10-29 (`docs/journal/handover/2026-10-29-three-lane-night.md` item 7) then carries the follow-up as a concrete change: "The review diff order (bead coding-harness-ut8q, PR #274; touches ADR 0021)", with the three options of the research note and the recorded recommendation to take the first two now as one bounded change and the split later. The recommendation is recorded text; no maintainer decision on an option exists in the tree.

**How the diff is built today (`scripts/stage2.py`).** `change_diff` builds the paid round's input as `git diff --no-color --no-ext-diff --no-textconv <merge-base>` for tracked changes plus one `git diff --no-index /dev/null <path>` per untracked file appended after, in `ls-files --others` order; it applies no ordering and no exclusion of its own, so the reviewer sees git's path order followed by the untracked tail. `bounded_review_diff` cuts that to the first `REVIEW_DIFF_MAX_LINES` = 2000 lines (constant near the top of the file; the count splits on `\n` only, per O191-4) and appends the marker `## (the change diff was cut at …; the rest is not carried)`, returning the cut note. `_review_round` embeds the result into the paid prompt as `prompts/04b-review-loop.md` body + round head + answer format + read request + `## The diff` + diff + read request; for the free stage it merges the free diff's own cut note with the prompt-bound note. The free stage's input comes from `free_diff`: the same merge base with uncommitted and untracked files, filtered through `_free_candidate` (only `scripts/*.py`, `tests/*.py` and executable non-text `tools/` source pass; `FREE_DIFF_SKIP_PARTS` excludes `node_modules`, `.venv`, `venv`, `dist`, `build`, `__pycache__`, `.git`, `.beads`; binaries, symlinked paths and deleted non-source fail), bounded per file at `FREE_DIFF_MAX_LINES` = 400 and in total at `FREE_DIFF_MAX_TOTAL` = 2000, with a `later files are not carried` marker and a cuts list. The free prompt (`free_round_prompt` over `FREE_REVIEW_BODY`) carries that diff alone — no tools, no repository access (criterion 3; ADR 0021 decision 3). The same `free_diff` feeds the free availability probe (`free_probe_prompt`) and the paid `probe` command. Free diff ordering follows the changed-then-untracked name list, deduped — the same git path order, but plans/docs never pass `_free_candidate`, so the prose-ordering problem exists only in the paid `change_diff`.

**Why a cut round cannot end the loop.** The record writer emits `The diff was cut: <note>` (`CUT_LINE`) with the sentence that a clean answer over a cut diff does not end the loop; `cut_rounds` parses those lines per round, `release_block` carries them into `findings.md` as a `Cut rounds:` line, `released_cut_rounds` reads them back after the record is deleted, and `round_was_cut` blocks the clean stop in the loop driver. A related defect — the free diff's own cuts once stayed out of the round note, letting a clean answer end the loop — is described as fixed context in `docs/journal/handover/2026-10-25-cloud-runner-fixes.md` (called "the opposite problem to ut8q"); current code merges both cut notes in `_review_round`.

**Where the order is not configurable.** `model-endpoints.yaml` holds the model selection as data (`flash_swarm`, `free_stage` rule, `availability_preflight`, `modelle_terms` with `anfragen_5h` cost values); the diff bounds and the diff's file order are code constants and code order in `scripts/stage2.py`, with no configuration knob. A change to order or exclusions is a code change, not a data change — unlike the ladder/swarm membership.

## Where it lives

- Diff building and bounds: `scripts/stage2.py` — `change_diff`, `free_diff`, `bounded_review_diff`, `_free_candidate`, `_bound_hunks`, `_merge_base`, `free_round_prompt`/`FREE_REVIEW_BODY`, `free_probe_prompt`, and the constants `REVIEW_DIFF_MAX_LINES`, `FREE_DIFF_MAX_LINES`, `FREE_DIFF_MAX_TOTAL`, `FREE_DIFF_SKIP_PARTS`, `FREE_DIFF_TEXT_SUFFIXES`.
- Round embedding and cut recording: `_review_round` (prompt assembly, cut-note merge), the record writer's `CUT_LINE` statement, `cut_rounds`, `released_cut_rounds`, `round_was_cut`, `release_block`'s `Cut rounds:` line.
- Tests: `tests/test_stage2.py` — `test_a_cut_round_stays_cut_after_the_release`, `test_the_review_diff_is_split_on_newlines_only`, `test_free_diff_reports_its_own_cut`, `test_a_free_round_over_a_cut_file_is_never_clean`, `test_free_diff_includes_nested_and_deleted_source`, `test_free_diff_untracked_headers_are_relative`, `test_empty_free_diff_skips_to_paid_models`, plus prompt-content assertions (`## The implementation diff` in the free prompt, no read request in it).
- Doctrine and reviewer text: `docs/WORKFLOW.md` §4 review-loop paragraphs (bound, cut recording, never-clean rule R-12/R-15, free-stage confinement); `prompts/04b-review-loop.md` input paragraph ("a paid round reads the change's diff against its merge base…", "A free round is confined to the implementation diff alone"); `docs/adr/0021-review-swarms-until-clean.md` decisions 1 and 3 plus the availability and restart amendments.
- Predecessor measurement: `docs/research/2026-10-29-review-diff-cut.md` (draft; per-change numbers and options).

## What is unclear

- **The maintainer's choice among the three options is open.** The research note says the options touch ADR 0021, so the choice is the maintainer's; the 2026-10-29 handover records a recommendation, not a decision. No `[DECISION]` answer exists in the tree.
- **Whether the cut-round rule stays as is under a new order.** The measured night shows rounds over a cut diff; if ordering keeps tests inside the bound, the interaction of the never-clean rule (`round_was_cut`) with an ordered-but-still-cut diff is not stated anywhere I read.
- **Whether the untracked tail's position (after all tracked output) is intended.** `change_diff` concatenates it without comment; no source states the intent.
- **The measured numbers are recorded, not re-verified by me.** The three heads named in the research note (`78676b5e`, `60cd44f2`, `358472d8`) were not re-measured in this worktree.
- **Pi compaction interplay remains unread**, as the bead's origin handover states: whether disabling Pi's compaction also disables overflow recovery (`docs/journal/handover/2026-10-23-night-run.md`).
- **`_free_candidate` has no test named after it.** Searching `tests/` for the symbol finds no matches; its classification is covered only indirectly through `free_diff` behaviour tests. Not found as a direct test; not there as a direct test — two statements.

## Which files a change would have to touch

`scripts/stage2.py` (at minimum `change_diff` for order/exclusions; `bounded_review_diff`, `free_diff` and the constants block if bounds move; the `CUT_LINE` wording only together with its parsers `cut_rounds`, `released_cut_rounds`, `round_was_cut`), `tests/test_stage2.py` (the tests listed above), `docs/WORKFLOW.md` §4 review-loop paragraphs, `prompts/04b-review-loop.md` input paragraph, `docs/adr/0021-review-swarms-until-clean.md` if an amendment is needed, and the predecessor note `docs/research/2026-10-29-review-diff-cut.md` (draft → updated once the direction is decided). `plans/INDEX.md` regenerates and is not hand-edited.

**Neighbours I already know:** `plans/changes/loop-until-clean/spec.md`, `plans/changes/review-loop-deep-a/spec.md`, `plans/changes/review-loop-deep-b/spec.md`, `plans/changes/free-member-rate-limit/spec.md`, `plans/changes/review-release-lock/spec.md`, `plans/changes/research-swarm/spec.md` (source of the R-numbered review findings the runner cites).

---

For you (the orchestrator/maintainer), the one open item before phase 1a: the three options in `docs/research/2026-10-29-review-diff-cut.md` are recorded as the maintainer's choice (they touch ADR 0021); the 2026-10-29 handover's recommendation (exclude the loop's own records + code/tests first, as one bounded change) is written down but not yet answered.

## Objective and the decision recorded after exploration

The work item (coding-harness-ut8q): a phase-4b reviewer receives at most
2000 lines of the change diff, and a round over a cut diff never ends the
loop cleanly. The measurement of 2026-10-29
(`docs/research/2026-10-29-review-diff-cut.md`) showed that the cut drops the
tests, because the change's own workflow files come first in Git's path order.

The open item above — which option — was answered by the maintainer on
2026-10-29 (recorded in the work item's notes and in `decisions.md`, Q-1):
one change that leaves `findings.md` and `plans/INDEX.md` out of the
review-loop diff and puts code and tests first. Splitting the diff across
reviewers is not part of it.
