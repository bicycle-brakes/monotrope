---
title: "Spec — findings-per-model"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-qut1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, measurement]
class: bounded
appetite: 4
adr_files: []
---

# Spec — findings-per-model

The review loop and phase-6 review become measurable per recorded model, so the maintainer can assess their contributions (bead coding-harness-qut1). Research: `research.md`; decision: `decisions.md#Q-1`.

## Problem

At commit `2e3d9d47`, research found that released loop rows retain their reviewer, but `scripts/stage2_runs.py` aggregates outcomes per change, not per reviewer. Phase-6 reviewer identity is recorded differently, and the existing count does not provide model totals. The resulting manual assessment cannot readily compare models.

## Acceptance criteria

1. When the report runs, it reads findings from active and archived changes at one identified commit.
   *Refuted by:* a committed findings file in either location is omitted or files from different commits are combined.
2. When a released review-loop finding or phase-6 finding names its model, the report attributes it to that recorded model identity.
   *Refuted by:* a finding is attributed to another model or omitted despite an unambiguous recorded identity.
3. If a finding's model cannot be identified unambiguously from its record, the report exposes it as unattributed without assigning it to a guessed model.
   *Refuted by:* an unidentified finding disappears or receives a fabricated model id.
4. When a finding is marked as a duplicate of another finding, only the finding first raised receives credit in the model totals.
   *Refuted by:* both models receive credit or the later duplicate receives it instead of the original.
5. When a non-duplicate finding is counted, its model's raised total includes it once regardless of its disposition.
   *Refuted by:* an undecided or rejected finding is omitted from raised, or a finding is counted twice.
6. When a non-duplicate finding has status `taken`, `taken — not a test`, or `fixed`, its model's taken total includes it once.
   *Refuted by:* one of those statuses is omitted or an unaccepted finding is included.
7. When a non-duplicate finding has status `fixed`, its model's fixed total includes it once.
   *Refuted by:* a merely taken finding is counted as fixed or a fixed finding is omitted.
8. When a non-duplicate finding has status `rejected`, its model's rejected total includes it once.
   *Refuted by:* a rejected finding is omitted or a non-rejected finding is included.
9. When the report runs, it produces JSON Lines records and a plain table with the same per-model counts and the full cut-off commit.
   *Refuted by:* the formats disagree, a count is missing, or the commit is absent or ambiguous.
10. When the make entry point is invoked, it runs the report.
    *Refuted by:* the entry point cannot generate both formats.
11. When the morning handover is prepared, its instructions require the generated table and its cut-off commit to be included.
    *Refuted by:* a future handover can follow the instructions without showing that table and cut-off.
12. If an input cannot be read or a duplicate reference cannot be resolved, the report identifies the affected input and refuses to present an incomplete count as complete.
    *Refuted by:* an unreadable file or unresolved duplicate silently produces an apparently complete report.

## Non-goals

Changing review rows, runner release, model selection, the review ladder, or the stage-2 stop rule is out of scope. This measurement informs later decisions; it does not rank models or change the contributor-model trial. Phase 2b does not run for a bounded change.

## Protected areas

Existing findings and archived decisions remain evidence, not data to rewrite; model declarations and review execution remain unchanged.

## Definition of Done

- `make verify` green; the report and handover instructions ship together.
- Protected areas remain untouched and non-goals unbuilt, as shown by the pull request file list.
- The pull request closes bead `coding-harness-qut1` and its last commit carries `Closes-Bead: coding-harness-qut1`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The report reads a fixed commit rather than mixing uncommitted files with a commit label, so the result can be reproduced. [DETAIL] Unidentifiable reviewers are exposed separately because the existing records do not always identify a model. [DETAIL] Four hours is a reversible phase-4 stop, including repairs, chosen to bound this measurement change.
