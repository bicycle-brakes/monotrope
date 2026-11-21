---
title: "Spec — review-diff-4000"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, review-loop, diff-bound]
class: bounded
appetite: 2
adr_files: []
---

# Spec — review-diff-4000

Every round of the review loop shares a 4,000-line prompt diff bound as interim relief until multi-part review arrives (bead `coding-harness-mwzv.4`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-21 the shared prompt diff bound is 2,000 lines; a cut round cannot count as clean. The 2026-11-20 day handover reports a change of about 4,100 lines cut at 2,000 (`research.md`, “What exists today”).
- Research measured on 2026-10-29 that documentation and plans filled over half the 2,000-line allowance in three changes, leaving no test-file lines in reviewers' prompts (`research.md`, “The measured effect of the cut”).
- The free stage can produce more than 2,000 lines before its own total threshold stops later files; the shared 2,000-line prompt bound currently cuts that output (`findings.md`, phase 2a, S-1). This corrects the contrary claim in `research.md`.

## Acceptance criteria

1. When a review-loop round receives its selected diff of at most 4,000 lines, the shared prompt bound carries that diff unchanged without its own cut note.
   *Refuted by:* A 4,000-line selected diff is cut or reported cut by the shared bound in any stage.
2. When a review-loop round receives its selected diff of more than 4,000 lines, the shared prompt bound carries the first 4,000 lines and a cut marker.
   *Refuted by:* A 4,001-line selected diff carries a different prefix or lacks the marker.
3. When the shared prompt bound cuts a round's selected diff, the round record reports that cut.
   *Refuted by:* A round over a 4,001-line selected diff has no corresponding cut note in its record.
4. When the free stage produces an uncut selected diff of more than 2,000 and at most 4,000 lines, its round prompt and availability probe carry that selected diff without a shared-bound cut.
   *Refuted by:* Such an output, including an overshoot on its last file without a free-stage cut note, is truncated at 2,000 or the round record reports a shared-bound cut.
5. When the free stage selects and bounds its implementation diff, its existing filter, 400-line per-file bound and 2,000-line total threshold remain unchanged.
   *Refuted by:* The filter or either limit changes, or the existing threshold behavior changes, including its whole-file overshoot.
6. When either the free stage's own bounds or the shared prompt bound cuts a round's diff, the round is recorded as cut and cannot count as clean, including after release.
   *Refuted by:* A free per-file cut is omitted from the cut record, or a cut round ends the loop as clean before or after release.
7. When the living workflow and runner overview describe diff bounds and cuts, each states correctly the bounds and cut behavior it describes; both state the 4,000-line shared bound, and the runner overview states the 400-line per-file bound and that free per-file cuts make a round cut.
   *Refuted by:* Either document omits its required statement, gives a wrong bound or threshold, treats the free total threshold as a strict 2,000-line prompt cap, or says a free per-file or total-threshold cut is not a cut round or can count as clean.
8. When a free-stage selected diff exceeds 2,000 lines but fits within the shared bound and includes a free per-file or total-threshold cut, the availability probe carries that selected diff in full.
   *Refuted by:* A probe truncates either a per-file-cut overshoot or a total-threshold-cut diff at 2,000 lines, or otherwise omits part of that selected diff.

## Non-goals

- Multi-part diff splitting, its recorded four-parts ceiling, diff ordering or path exclusions; multi-part review is a separate change (bead `coding-harness-hchx`).
- Changing the 45-minute review deadline, model selection, context windows, compaction or overflow handling; the deadline's effect is measured separately (bead `coding-harness-8kht`).
- Rewriting dated research, handovers or merged decision records describing the former bound.

## Protected areas

- ADR files and the merged decision record remain historical: this bounded adjustment does not amend their decisions.
- The free diff filter, helpers and their own bounds stay unchanged; the shared prompt bound still applies to their output, as the maintainer decided (`decisions.md`, Q-1).

## Definition of Done

- `make verify` green; the criterion ledger in `plan.md` identifies the checks.
- `docs/WORKFLOW.md` and `docs/how-it-works.md` move with the code; no ADR moves.
- Review the actual patch, including the contents of `scripts/stage2.py`, to verify the protected helpers and limits are unchanged and the non-goals remain unbuilt.
- The pull request closes `coding-harness-mwzv.4`, and its last commit carries `Closes-Bead: coding-harness-mwzv.4`.
- Special runs: none.

## Open decisions

[DETAIL] A two-hour phase-4 stop covers the parameter, regression checks and documentation; it is freely revisable.

[DETAIL] Each living document states the bounds it describes accurately; the workflow need not add the free stage's own numeric thresholds because they are not currently stated there (S-6). Free total-threshold cuts, when described, are recorded as cut rounds like per-file cuts (S-7). The probe covers free-cut overshoots as well as uncut overshoots because both travel through the same shared bound (S-8).

None open.
