---
title: "Spec — findings-per-model"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-18
updated: 2026-11-18
supersedes: null
superseded_by: null
bead: coding-harness-qut1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, measurement]
class: bounded
appetite: 6
adr_files: []
---

# Spec — findings-per-model

The review loop and phase-6 review become measurable per model (bead coding-harness-qut1). Research: `research.md`; decisions: `decisions.md`.

## Problem

At commit `2e3d9d47`, released loop rows retained their reviewer, but the existing counter aggregated outcomes per change rather than per reviewer. Phase-6 rows identify the review route rather than the model; review call lines can identify the model, but calls and blocks do not pair one to one. Manual evaluation cannot readily compare model contributions (`research.md`).

## Acceptance criteria

1. When the report runs, it reads released phase-4b loop rows and eligible phase-6 sections from every active and archived change at one identified commit, excluding phase-2a and rejected phase-6 answers.
   *Refuted by:* an eligible committed row is omitted, a rejected answer is counted, or evidence from different commits is combined.
2. When a finding ID recurs within a change, only its latest eligible row supplies its current state; the same ID in another change is a separate finding.
   *Refuted by:* two historical rows are counted or the same ID in two changes is collapsed.
3. When a released loop row names its model, the shared findings reader attributes it to that model.
   *Refuted by:* a named model's row is attributed elsewhere.
4. When a runner-form `## Phase 6 — <who>, <date>` block has a nearest preceding Stage-2 call whose verb is exactly `review`, with no intervening phase-6 block, the shared reader’s legacy attribution source assigns that call’s model to the block.
   *Refuted by:* a `review-loop` call is used or skipped to reach an older review call, or a call across another phase-6 block is used.
5. If an eligible readable finding has no identifiable model under those rules, including a row under a phase-6-like heading outside the runner form, it appears in an unattributed bucket with its change and ID.
   *Refuted by:* an unpaired historical seven-cell phase-6 row disappears or is assigned a guessed model.
6. When an attribution source receives the change, findings file, block heading, position and directly preceding call lines, it returns a model ID or `unattributed` through the shared reader without changing consumer calls.
   *Refuted by:* a substitute source that attributes from the heading alone cannot be plugged in without changing a report consumer’s reader calls.
7. When a legacy Status names another row ID with `same as`, `duplicate of`, `repeat`, `repeats` or `repeat of`, matched without regard to case, that row is a duplicate.
   *Refuted by:* `Duplicate of L2-2` counts as a new finding or a marker without a row ID counts as a duplicate.
8. When duplicate references form a chain, each non-duplicate root receives its own credit and every duplicate receives none, including when a root is unattributed.
   *Refuted by:* a duplicate earns credit, a root loses credit, or an unattributed root’s credit moves to a duplicate’s model.
9. When a finding row added or changed relative to the merge base with `origin/main` marks a duplicate, a gate requires the exact Status `rejected — duplicate of <ID>`.
   *Refuted by:* a changed `rejected — Same as L1-1` passes the gate or the canonical form fails it.
10. When a non-duplicate finding is counted, its model's raised total includes it once, including open and rejected findings.
    *Refuted by:* an open finding is omitted or a finding is counted twice.
11. When a non-duplicate Status begins with `taken` or `fixed`, its model's defects-accepted total includes it once.
    *Refuted by:* `fixed — orchestrator hand edit` is omitted or `rejected` is included.
12. When a non-duplicate Status begins with `resolved`, `answered` or `in spec`, its model's questions-settled total includes it once.
    *Refuted by:* `resolved 2026-11-18 by decisions.md` is omitted or a taken defect is included.
13. When a non-duplicate Status begins with `rejected`, its model's rejected total includes it once.
    *Refuted by:* a rejected row is omitted or an open row is included in an outcome total.
14. When the report runs, a plain table on standard output and JSON Lines in a state-directory file carry the same raised, defects-accepted, questions-settled and rejected counts, including unattributed, and the full cutoff commit; the file path is printed last.
    *Refuted by:* a count differs between formats or either lacks the full commit.
15. When `make findings-per-model` runs, it produces both formats for `HEAD` by default and accepts a requested revision via `REV`.
    *Refuted by:* `make findings-per-model REV=<revision>` ignores that revision or produces only one format.
16. If a row or input cannot be read, has an unknown status or an unresolved duplicate reference or duplicate cycle, both outputs mark the report incomplete and identify the affected input or row, and the command exits non-zero.
    *Refuted by:* malformed cells, invalid encoding, an unknown status or a missing duplicate target silently yields a complete report or no output.
17. When a morning handover is prepared, `AGENTS.md` and `docs/orchestration.md` require the generated table and cutoff for each unmerged change branch that gained rows that night and for main at handover time, without combining commits into one report.
    *Refuted by:* following either governing instruction can omit the night's lane tables including an earlier branch in a lane, or their cutoff commits.

18. When a findings table has no phase-6 heading, the report identifies its rows as outside the count.
    *Refuted by:* a heading-less table is silently omitted or credited to a model.

19. When a row has a `2a-` ID, it is excluded from phase-6 counts.
    *Refuted by:* a phase-2a question answered in a phase-6 table increases a model’s totals.

## Non-goals

Changing review execution, release format, model selection, the ladder, the stage-2 stop rule, or ranking models is out of scope. A later event-log attribution source and the separate metrics consumer are not implemented here. Phase 2b does not run for a bounded change.

## Protected areas

Historical findings and decisions remain evidence; model declarations and review execution are unchanged.

## Definition of Done

- `make verify` green; the shared reader, report, duplicate gate, template and morning instructions ship together.
- Protected areas remain untouched and non-goals unbuilt, as shown by the pull request file list.
- The pull request closes bead `coding-harness-qut1` and its last commit carries `Closes-Bead: coding-harness-qut1`.
- Special runs: none.

## Open decisions

None open. [DETAIL] A report defaults to the checked-out commit and the handover shows separate lane reports, so unmerged evidence is visible without combining snapshots. JSON Lines uses a metadata record followed by model records, with diagnostic records for gaps and unattributed IDs; explicit types make it machine-readable. Heading-less tables are shown separately because their phase cannot be established reliably. Existing historical rows keep legacy duplicate forms; the gate applies to newly introduced or changed rows so history need not be rewritten.
