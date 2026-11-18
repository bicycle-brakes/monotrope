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

1. When the report runs, it reads released phase-4b loop rows and accepted phase-6 sections from every active and archived change at one identified commit, excluding phase-2a and rejected phase-6 answers.
   *Refuted by:* an eligible committed row is omitted, a rejected answer is counted, or evidence from different commits is combined.
2. When a finding ID recurs within a change, only its latest eligible row supplies its current state; the same ID in another change is a separate finding.
   *Refuted by:* two historical rows are counted or the same ID in two changes is collapsed.
3. When a released loop row names its model, the shared findings reader attributes it to that model.
   *Refuted by:* a named model's row is attributed elsewhere.
4. When a phase-6 block has a preceding review call with no intervening phase-6 block, the shared reader's legacy attribution source assigns the nearest such call's model to the block.
   *Refuted by:* a nearer call is ignored or a call across another phase-6 block is used.
5. If an eligible readable finding has no identifiable model under those rules, it appears in an unattributed bucket with its change and ID.
   *Refuted by:* an unpaired historical seven-cell phase-6 row disappears or is assigned a guessed model.
6. When the attribution source is replaced, the shared reader's consumers can obtain findings without changing their interface.
   *Refuted by:* a substitute source requires a report consumer to change its reader calls.
7. When a legacy Status names another row ID with `same as`, `duplicate of`, `repeat`, `repeats` or `repeat of`, that row is a duplicate.
   *Refuted by:* `repeats L2-2` counts as a new finding or a marker without a row ID counts as a duplicate.
8. When a duplicate names one or more originals, each named original receives its own credit and the duplicate receives none, including when an original is unattributed.
   *Refuted by:* a duplicate earns credit, a named original loses credit, or an unattributed original's credit moves to the duplicate's model.
9. When a new finding row marks a duplicate, its Status uses `duplicate of <ID>` and a gate rejects another duplicate form.
   *Refuted by:* a new `same as L1-1` marker passes the gate or the canonical form fails it.
10. When a non-duplicate finding is counted, its model's raised total includes it once, including open and rejected findings.
    *Refuted by:* an open finding is omitted or a finding is counted twice.
11. When a non-duplicate Status begins with `taken` or `fixed`, its model's defects-accepted total includes it once.
    *Refuted by:* `fixed — orchestrator hand edit` is omitted or `rejected` is included.
12. When a non-duplicate Status begins with `resolved`, `answered` or `in spec`, its model's questions-settled total includes it once.
    *Refuted by:* `resolved 2026-11-18 by decisions.md` is omitted or a taken defect is included.
13. When a non-duplicate Status begins with `rejected`, its model's rejected total includes it once.
    *Refuted by:* a rejected row is omitted or an open row is included in an outcome total.
14. When the report runs, a plain table and JSON Lines carry the same raised, defects-accepted, questions-settled and rejected counts, including unattributed, and the full cutoff commit.
    *Refuted by:* a count differs between formats or either lacks the full commit.
15. When `make findings-per-model` runs, it produces both formats for `HEAD` by default and accepts a requested revision via `REV`.
    *Refuted by:* `make findings-per-model REV=<revision>` ignores that revision or produces only one format.
16. If a row or input cannot be read, has an unknown status or an unresolved duplicate reference, both outputs mark the report incomplete and identify the affected input or row, and the command exits non-zero.
    *Refuted by:* malformed cells, invalid encoding, an unknown status or a missing duplicate target silently yields a complete report or no output.
17. When a morning handover is prepared, `AGENTS.md` and `docs/orchestration.md` require the generated table and cutoff for each relevant unmerged lane commit as well as the chosen main commit, without combining commits into one report.
    *Refuted by:* following either governing instruction can omit the night's lane tables or their cutoff commits.

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

None open. [DETAIL] A report defaults to the checked-out commit and the handover shows separate lane reports, so unmerged evidence is visible without combining snapshots. JSON Lines uses a metadata record followed by model records, with diagnostic records for gaps and unattributed IDs; explicit types make it machine-readable. Existing historical rows keep legacy duplicate forms; the gate applies to newly introduced or changed rows so history need not be rewritten.
