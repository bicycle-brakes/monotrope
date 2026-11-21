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

The paid review loop can receive up to 4,000 lines of a change diff as interim relief until multi-part review arrives (bead `coding-harness-mwzv.4`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-21 the paid review prompt is cut at 2,000 lines; a cut round cannot count as clean. The 2026-11-20 day handover reports a change of about 4,100 lines cut at 2,000 (`research.md`, “What exists today”).
- The 2026-10-29 research measured three changes where documentation and plans filled over half the 2,000-line allowance and no test-file lines reached the reviewers (`research.md`, “The measured effect of the cut”).

## Acceptance criteria

1. When a paid review receives a change diff of at most 4,000 lines, its prompt carries the complete diff without a cut note.
   *Refuted by:* A 4,000-line diff is cut or reported as cut.
2. When a paid review receives a change diff exceeding 4,000 lines, its prompt carries the first 4,000 lines and a cut marker, and the round record reports the cut.
   *Refuted by:* A 4,001-line diff carries fewer or more than its first 4,000 lines, lacks the marker, or has no cut note in the record.
3. When the free review prepares its implementation diff, its 400-line per-file and 2,000-line total bounds remain in force.
   *Refuted by:* The free diff no longer cuts at either existing bound.
4. When a round reviews a diff cut by the overall review bound, it cannot count as clean.
   *Refuted by:* A cut round is recorded as clean or becomes clean after release.
5. When the living workflow and runner overview describe review diff limits, they state the 4,000-line overall bound and distinguish the free review's 2,000-line total and 400-line per-file bounds.
   *Refuted by:* Either document retains 2,000 as the overall bound or misstates a free-review bound.

## Non-goals

- Multi-part diff splitting, its recorded four-parts ceiling, diff ordering or path exclusions; multi-part review is a separate change (bead `coding-harness-hchx`).
- Changing the 45-minute review deadline, model selection, context windows, compaction or overflow handling; the deadline's effect is measured separately (bead `coding-harness-8kht`).
- Rewriting dated research, handovers or merged decision records that describe the former bound.

## Protected areas

- ADR files and the merged decision record: this bounded interim adjustment does not amend their decisions.
- Free-review filtering and its limits: the paid allowance does not widen what the free stage carries.

## Definition of Done

- `make verify` green; the criterion ledger in `plan.md` identifies the checks.
- `docs/WORKFLOW.md` and `docs/how-it-works.md` move with the code; no ADR moves.
- The protected areas remain untouched and the non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes `coding-harness-mwzv.4`, and its last commit carries `Closes-Bead: coding-harness-mwzv.4`.
- Special runs: none.

## Open decisions

[DETAIL] A two-hour phase-4 stop is set for this bounded change: it is freely revisable and covers the parameter, regression checks and documentation.

None open.
