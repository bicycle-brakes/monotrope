---
title: "Spec — origin-check-across-blocks"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-3h96
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, repair, origin]
class: bounded
appetite: 1
adr_files: []
neighbours:
  - plans/changes/origin-cell/spec.md
  - plans/changes/repair-targeted-check/spec.md
---

# Spec — origin-check-across-blocks

Repair refuses outstanding findings with invalid provenance even when a newer
phase-6 block follows them (bead `coding-harness-3h96`). Research:
`research.md`; recorded scope and reasoned interview skip: `decisions.md`.

## Problem

At commit `89339cbd` (2026-11-10), repair selects taken rows from every
phase-6 block, while its Origin check reads only the newest block. An older
taken row with Origin `invalid` therefore reaches the repair model and status
writes after a newer block says `No finding.` (`research.md`, “The gap,
mechanically”; predecessor finding F-1, the missed historical repair target).

Scanning all historical accepted rows instead would restore an earlier
blocker: superseded fixed rows with legacy provenance would prevent normal
continuation. Existing tests require those rows to remain exempt
(`research.md`, “Why the check is narrow”).

## Terms

- **Outstanding target:** a row selected by repair because Status begins
  `taken`, case-insensitively, in the record, a released block or any phase-6 block.
- **Valid Origin:** the complete trimmed cell is `base` or `fix-r<N>`, where
  N is a positive decimal whole number without a leading zero; case matters.
- **Row location:** the row's ID and its file (`loop.md` or `findings.md`).
  Finding IDs are unique within a change, and a check refuses a duplicate ID
  (including a release of loop rows that repeats an ID already in
  `findings.md`), so the ID suffices; no block heading or occurrence is
  computed (maintainer's answer A, 2026-11-11).

## Acceptance criteria

1. When repair selects an outstanding target with an invalid Origin, it
   refuses regardless of the target's source or position before newer phase-6 blocks.
   *Refuted by:* a blank or malformed Origin on an older taken row admits
   repair after an empty, rowless or populated newer block.
2. If repair refuses for an invalid target Origin, it leaves the attempt without effects.
   *Refuted by:* any model or availability probe runs, an audit or time entry
   is appended, findings or record bytes change, stage state changes, or a commit is made.
3. When the target-Origin check refuses, its diagnostic identifies every
   invalid selected row by ID and file and tells the orchestrator
   to correct the cell to `base` or `fix-r<N>` with the stated positive-number rule.
   *Refuted by:* an offending row cannot be found by its ID and file, a valid
   row is accused, or the message omits the allowed values or asks a reviewer to fix its answer.
4. When older outstanding targets have valid Origins and all existing repair
   prerequisites hold, repair processes them in their original places without changing Origin.
   *Refuted by:* `base`, `fix-r1` or `fix-r12` is refused, an older target is
   omitted from the model batch, or repair moves its row or replaces its Origin.
5. While the added target check runs only in repair, existing admission rules
   retain their validation scopes.
   *Refuted by:* review, release or review-loop newly reject superseded Origin
   cells; repair rejects an unselected historical fixed/rejected row for Origin;
   undecided rows cease holding repair; or release control flags begin checking Origin.
6. When the workflow describes repair, it states that selected rows from every
   phase-6 block are checked for valid Origin before calls or writes.
   *Refuted by:* the repair section permits an older selected row to escape
   validation or requires passive historical backfill to continue other verbs.

## Non-goals

- No automatic provenance inference, historical migration, reviewer-output
  rewriting, new Origin vocabulary, repair-brake policy or row format.
- No change to which rows repair selects, its retry routes, targeted
  verification, duplicate-ID checks or legacy completion checks.
- No design phase or ADR: this bounded correction adds an admission check
  inside the existing repair boundary.

## Protected areas

Keep other changes, their historical findings and the general row parsers
unchanged; the fix must not erase selected older targets. Do not edit prompts,
templates, governance, settings, endpoint configuration, tracker data or ADRs.

## Definition of Done

- All criterion-ledger tests and `make verify` pass on the implementation head.
- Changed together: `scripts/stage2.py`, `tests/test_stage2.py`,
  `docs/WORKFLOW.md` and this change's lifecycle artifacts; no ADR.
- The pull request's file list respects the non-goals and protected areas.
- The pull request closes `coding-harness-3h96`, the outstanding-target Origin
  correction; its final commit carries `Closes-Bead: coding-harness-3h96`.
- No special external-model run is needed to demonstrate the bug; local stand-ins suffice.

## Open decisions

None open. The reasoned interview skip and repair-only scope are already in
`decisions.md`; this draft supplies no maintainer answer.

[DETAIL] Check every selected target, including selected released rows, rather
than re-auditing all historical rows: selection is the boundary recorded in
`decisions.md`, and an actively selected legacy row differs from passive history.
[DETAIL] Name an offending row by its ID and file only: IDs are unique within
a change and a duplicate is refused, so no heading or occurrence is needed
(maintainer's answer A, 2026-11-11, replacing the earlier heading-plus-occurrence wording).
[DETAIL] Set a one-hour phase-4 appetite including repairs, a stop rather than
an estimate, because the correction stays within one existing admission path.
