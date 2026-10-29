---
title: "Spec — review-diff-order"
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
tags: [spec, review-loop, stage-2]
class: bounded
appetite: 1
adr_files: []
---

# Spec — review-diff-order

The goal: paid review-loop rounds see code and tests before prose, without
the loop's own findings or generated plans index consuming their diff budget
(bead `coding-harness-ut8q`). Research: [research.md](research.md).
Maintainer's scope: [decisions.md, Q-1](decisions.md#q-1--which-remedy-for-the-cut-review-diff).

## Problem

- The recorded measurement of 2026-10-29 shows Git's path order putting
  workflow prose before source and tests. At `78676b5e`, 1445 of 3371 diff
  lines preceded code; neither changed test file reached the 2000-line paid
  prompt. The growing findings alone consumed 582 lines (research,
  "What exists today"; predecessor measurement linked there).
- At the draft's base `2363f0e`, tracked changes precede all untracked
  files, so new tests can remain behind tracked prose even after sorting
  tracked files alone (`scripts/stage2.py::change_diff`).
- That raw diff also binds availability receipts; excluding files there
  would weaken detection of changed inputs (research, "Draft follow-up").

## Terms

- **Paid review diff:** the file diffs embedded in a paid round's prompt;
  exclusion concerns this input, not the reviewer's existing read tools.
- **Implementation inputs:** paths outside `docs/`, `plans/` and `prompts/`
  whose suffix is not `.md`, `.rst`, `.txt` or `.adoc`; this includes source,
  tests, executable tools and runtime configuration. **Prose:** other paths.
- **Excluded paths:** any file with basename exactly `findings.md`, plus
  exactly the repository-relative path `plans/INDEX.md`.

## Acceptance criteria

1. When a paid review diff is built, it contains no file diff for an excluded path.
   *Refuted by:* a tracked or untracked findings file, or the generated plans index, contributes a diff header or content.
   *Basis:* decisions.md#Q-1.
2. When a paid review diff contains implementation inputs and prose, every implementation file precedes every prose file in one deterministic repository-relative path order within each group, regardless of tracking state.
   *Refuted by:* tracked prose precedes an untracked test, or repeated builds of unchanged inputs order paths differently.
   *Basis:* decisions.md#Q-1; the visible classification detail below.
3. When a non-excluded file differs from the merge base with `origin/main`, its full file diff remains represented exactly once before the prompt limit is applied, including committed, staged, unstaged, untracked and deleted changes.
   *Refuted by:* reordering drops a retained file or hunk, duplicates it, corrupts its line endings, or loses either side of a renamed file represented as deletion and addition.
   *Basis:* decisions.md#Q-1; research, "How the diff is built today".
4. When a paid round embeds its diff, the existing 2000-line prompt limit is applied after exclusion and ordering.
   *Refuted by:* large excluded findings or leading prose consume budget before a small source/test diff, an over-limit diff lacks its cut marker, or an at-limit diff is reported cut.
   *Basis:* decisions.md#Q-1; decisions.md, "The cut-round rule stays".
5. If the resulting paid diff is still cut, a no-finding answer cannot end the loop cleanly, including after release and resumption.
   *Refuted by:* a cut is absent from the round or release record, or the next eligible round is refused as already clean.
   *Basis:* decisions.md, "The cut-round rule stays".
6. While paid diff preparation changes, free review and free availability probes retain their existing source/test admission, ordering and bounds.
   *Refuted by:* paid ordering changes the free diff, admits prose into it, or loses a free cut note.
   *Basis:* decisions.md, "The free stage stays as it is".
7. When an excluded file changes after availability preparation, the preparation receipt is invalidated by that changed input as before.
   *Refuted by:* changing only findings or `plans/INDEX.md` leaves the full-diff binding unchanged.
   *Basis:* research, "Draft follow-up"; ADR 0021's existing input-bound receipt.

## Non-goals

- Splitting a large diff across reviewers, increasing bounds, changing
  compaction, model selection, read tools, or the loop's stop/release rules.
  Splitting returns only as a separate change if retained diffs still exceed
  the bound; this change promises priority, not complete review of any size.
- Re-measuring historical branches or claiming improved finding quality.
- A design phase: class `bounded` skips phase 2b; no architectural rule or
  ADR text changes.

## Protected areas

`docs/adr/`, `model-endpoints.yaml`, `scripts/stage2_availability.py` and
free-diff construction stay unchanged: their contracts are retained.
The predecessor research note remains historical evidence.

## Definition of Done

- `make verify` green; new behavior tests fail under the corresponding old behavior.
- Code, tests, `docs/WORKFLOW.md` §4 and `prompts/04b-review-loop.md` describe
  the same paid diff scope and order; `plans/INDEX.md` is regenerated by the runner.
- The pull request's file list shows the protected areas untouched and the non-goals unbuilt.
- The pull request closes the review-diff-order work item (`coding-harness-ut8q`);
  its last commit carries `Closes-Bead: coding-harness-ut8q`.
- Special live model runs: none required to establish the ordering behavior;
  normal review-loop and phase-6 requirements still apply.

## Open decisions

None open. The maintainer's Q-1 is implemented by the proposed scope above;
no answer is inferred from the earlier handover's recommendation.

- [DETAIL] Implementation inputs and prose use the explicit classification
  in Terms, with lexical path order inside each group: this reversible rule
  avoids a source-language allowlist and treats new tests like tracked tests.
- [DETAIL] Exclude exact basenames `findings.md` throughout the tree and the
  exact index path only: this applies the named exclusions without dropping
  other plans, research, similarly named files or directories.
- [DETAIL] Rename diffs may be deletion/addition pairs: both paths remain
  visible without making ordering depend on Git's similarity detection.
- [DETAIL] Phase 4 has a one-hour appetite, repairs included: this bounds
  a local input-projection change; it is a stop, not an estimate.
