---
title: "Spec — findings-per-model"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-18
updated: 2026-11-20
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

1. When the report runs, it reads released phase-4b loop rows under `## Phase 4b — loop rows, released <date>` or `## Phase 4b — GLM loop rows, released <date>` and phase-6 rows under `## Phase 6 — <who>, <date>` from every active and archived change at one identified commit, excluding phase-2a and rejected phase-6 answers.
   *Refuted by:* an eligible committed row is omitted, a rejected answer is counted, or evidence from different commits is combined.
2. When a finding ID recurs within a change, its earliest eligible row supplies its model and its latest eligible row supplies its Status; the same ID in another change is a separate finding.
   *Refuted by:* a re-check changes the credited model, an older Status wins, or the same ID in two changes is collapsed.
3. When a released loop row names a model, the shared reader attributes it to that model; a vendor-only Reviewer in a legacy GLM release uses the corresponding Stage-2 call line's model, or is unattributed if it cannot be identified.
   *Refuted by:* a named model's row is attributed elsewhere, or `GLM` becomes a model ID.
4. When a runner-form `## Phase 6 — <who>, <date>` block has a nearest preceding Stage-2 call of any verb which is exactly `review`, with no intervening phase-6 block, the shared reader’s legacy attribution source assigns that call’s model to the block.
   *Refuted by:* a `repair` or `review-loop` call is used or skipped to reach an older review call, or a call across another phase-6 block is used.
5. If an eligible readable finding has no identifiable model under those rules, it appears in an unattributed bucket with its change and ID.
   *Refuted by:* an unpaired historical seven-cell phase-6 row disappears or is assigned a guessed model.
6. When an attribution source receives the change, findings file, block heading, position and directly preceding call lines, it returns a model ID or `unattributed` through the shared reader without changing consumer calls.
   *Refuted by:* a substitute source that attributes from the heading alone cannot be plugged in without changing a report consumer’s reader calls.
7. When a legacy Status names another row ID with `same as`, `duplicate of`, `repeat`, `repeats` or `repeat of`, matched without regard to case, that row is a duplicate.
   *Refuted by:* `Duplicate of L2-2` counts as a new finding or a marker without a row ID counts as a duplicate.
8. When duplicate references form a chain, each non-duplicate root receives its own credit and every duplicate receives none, including when a root is unattributed.
   *Refuted by:* a duplicate earns credit, a root loses credit, or an unattributed root’s credit moves to a duplicate’s model.
9. When a finding row added or changed relative to the merge base with `origin/main` marks a duplicate, a gate requires `rejected — duplicate of <ID>`, allowing multiple IDs joined by ` and ` and an optional colon followed by a reason; rename-aware comparison preserves unchanged rows in moved files.
   *Refuted by:* a changed `rejected — Same as L1-1` passes, a valid multi-ID form fails, or an unchanged archived row is treated as new.
10. When a non-duplicate finding is counted, its model's raised total includes it once, including open and rejected findings.
    *Refuted by:* an open finding is omitted or a finding is counted twice.
11. When a non-duplicate Status begins with `taken`, `fixed` or historical `closed —`, its model's defects-accepted total includes it once.
    *Refuted by:* `fixed — orchestrator hand edit` is omitted or `rejected` is included.
12. When a non-duplicate Status begins with `resolved`, `answered` or `in spec`, its model's questions-settled total includes it once.
    *Refuted by:* `resolved 2026-11-18 by decisions.md` is omitted or a taken defect is included.
13. When a non-duplicate Status begins with `rejected`, its model's rejected total includes it once.
    *Refuted by:* a rejected row is omitted or an open row is included in an outcome total.
14. When the report runs, a plain table on standard output and JSON Lines in `$XDG_STATE_HOME/coding-harness/findings-per-model/main.jsonl` for main, or `$XDG_STATE_HOME/coding-harness/findings-per-model/branches/<encoded-branch>.jsonl` for each unmerged branch carry the same raised, defects-accepted, questions-settled and rejected counts, including unattributed, and the full cutoff commit; the file path is printed last.
    *Refuted by:* a count differs between formats or either lacks the full commit.
15. When `make findings-per-model` runs, it produces both formats for `HEAD` by default and accepts a requested revision via `REV`.
    *Refuted by:* `make findings-per-model REV=<revision>` ignores that revision or produces only one format.
16. If a row or input cannot be read, has a status outside the closed set `open`, `taken`, `fixed`, `closed —`, `resolved`, `answered`, `in spec`, `rejected`, and `accepted limit —` or an unresolved duplicate reference or duplicate cycle, both outputs mark the report incomplete and identify the affected input or row, and the command exits non-zero.
    *Refuted by:* malformed cells, invalid encoding, an unknown status or a missing duplicate target silently yields a complete report or no output.
17. When a morning handover is prepared, `AGENTS.md` and `docs/orchestration.md` require the generated table and cutoff for each unmerged change branch that gained rows that night and for main at handover time, without combining commits into one report.
    *Refuted by:* following either governing instruction can omit the night's lane tables including an earlier branch in a lane, or their cutoff commits.

18. When a table whose first cell holds a finding ID is outside the eligible headings, the report lists it with its heading as outside the count, grouping phase-2a blocks together; a table before any heading is labelled headingless.
    *Refuted by:* an outside table is silently omitted or credited to a model, or a restatement changes an eligible row’s Status.

19. When a row has a `2a-` ID, it is excluded from phase-6 counts.
    *Refuted by:* a phase-2a question answered in a phase-6 table increases a model’s totals.

The JSON Lines contract starts with `{"type":"metadata","commit":"<full hash>","complete":true}`, followed by one `model` record per model with `model`, `raised`, `defects_accepted`, `questions_settled`, and `rejected`; `model: null` denotes unattributed. It also contains `finding` records with `change` and `id` for unattributed findings and `gap` records with `path`, `id` when known, and `reason`. Records are deterministic, and the printed path is last.

## Non-goals

Changing review execution, release format, model selection, the ladder, the stage-2 stop rule, or ranking models is out of scope. A later event-log attribution source and the separate metrics consumer are not implemented here. Phase 2b does not run for a bounded change.

## Protected areas

Historical findings and decisions remain evidence; model declarations and review execution are unchanged.

## Boundary

Limits this change accepts; phase 6 judges a row that describes only one of them as that limit (decisions Q-7, phase-6 grammar review of 2026-11-20).

- **The reader reads the grammar in `scripts/findings_reader.py`, not all of Markdown.** Three cases are deliberately not read as a Markdown renderer would: a setext heading whose text spans several lines is labelled by its last line only; rows without a header row above them are read as rows, although a renderer shows them as a paragraph; and HTML blocks other than comments (`<details>`, `<table>`) are not opaque, so a table line inside one is read as a row.
- **Severity, dimension and origin are measured, not enforced, by the reader.** A non-blank free value (`impl`, `Correctness`) is no gap under criterion 16; the fixed vocabulary is a matter for the new-row gate (decisions Q-7).
- **A released loop section counts only its first table (decisions Q-8).** The runner's `release-loop` writes one table under each `## Phase 4b — loop rows, released <date>` heading; any further table separated by a blank line under that heading stands outside the count.

## Definition of Done

- `make verify` green; the shared reader, report, duplicate gate, template and morning instructions ship together.
- Protected areas remain untouched and non-goals unbuilt, as shown by the pull request file list.
- The pull request closes bead `coding-harness-qut1` and its last commit carries `Closes-Bead: coding-harness-qut1`.
- Special runs: none.

## Open decisions

None open. [DETAIL] If `XDG_STATE_HOME` is unset, use `~/.local/state`; encode each branch name as its UTF-8 bytes in lowercase hexadecimal, so distinct branch names cannot collide. A revision that is not a branch writes `revisions/<full-commit>.jsonl`; these names provide stable separate outputs. The third review decisions in `decisions.md` supersede its older rule counting other phase-6-like headings. [DETAIL] A report defaults to the checked-out commit and the handover shows separate lane reports, so unmerged evidence is visible without combining snapshots. JSON Lines uses a metadata record followed by model records, with diagnostic records for gaps and unattributed IDs; explicit types make it machine-readable. Heading-less tables are shown separately because their phase cannot be established reliably. Existing historical rows keep legacy duplicate forms; the gate applies to newly introduced or changed rows so history need not be rewritten.
