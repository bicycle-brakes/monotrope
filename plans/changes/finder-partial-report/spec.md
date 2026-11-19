---
title: "Spec — finder-partial-report"
status: draft
implementation_status: none
date: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-19
supersedes: null
superseded_by: null
bead: coding-harness-yd8w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-swarm]
class: bounded
appetite: 4
adr_files: []
---

# Spec — finder-partial-report

Finder seats recover valid locator entries after one correction, instead of losing a whole report to malformed entries (bead `coding-harness-yd8w`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-19, research found that `stage_finders` invalidates a whole finder answer when locator validation fails and stops before merging the map (`research.md`, Runner exploration). In the recorded incident, 36 of 102 entries named a file without a reference; the whole answer was rejected (decisions.md#Q-1).

## Acceptance criteria

1. When a process-successful finder answer fails locator validation, the same seat gets at most one correction request containing the exact validation error.
   *Refuted by:* a request missing or changing the validator error, a different seat correcting it, or a second correction request.
   *Basis:* decisions.md#Q-1.
2. When the correction is valid, the map merge receives the corrected finder report.
   *Refuted by:* the original invalid report is used, or the valid correction does not reach the merge.
   *Basis:* decisions.md#Q-1.
3. When the correction still contains malformed entries in an otherwise readable four-list report, every valid entry from that correction reaches the map merge and every malformed entry is excluded.
   *Refuted by:* a valid entry is lost, an invalid entry enters the merge, or the finder failure stops the merge solely because entries were dropped.
   *Basis:* decisions.md#Q-1.
4. When entries are dropped from a correction, the published run record identifies the finder, category, dropped entries and their validation errors as a gap.
   *Refuted by:* the run record omits a dropped entry, its category, seat or reason, or presents it as accepted evidence.
   *Basis:* decisions.md#Q-1.
5. When a locator is retained, it satisfies the existing locator validation, including a path and an exact symbol or section.
   *Refuted by:* a whole-file locator without a reference, or any entry violating the existing validator, reaches the map.
   *Basis:* decisions.md#Q-1.
6. When a corrected report has been recovered, the existing exact-union check uses the retained reports from all three finder seats.
   *Refuted by:* the merge adds or drops a retained locator or changes its finder origin and still passes.
   *Basis:* decisions.md#Q-1; research.md, Map merge.
7. If the correction cannot be read as the four locator lists, or the correction call fails or is refused, the run retains the existing incomplete or refusal outcome and does not advance to the map merge.
   *Refuted by:* an unreadable report, failed call or refusal is represented as a successful finder report and the merge starts.
   *Basis:* decisions.md#Q-1; research.md, Finder stage and Run outcome.

## Non-goals

- Accepting whole-file locators, selecting finder seats, changing topic or merge validation, or changing other failure policies.
- Design phase 2b and an ADR: this change is bounded.

## Protected areas

Security and leak checks, availability selection, model configuration and other change folders remain untouched; this repair is limited to finder report recovery.

## Definition of Done

- Targeted tests and `make verify` pass.
- The finder map and runner and their tests move with this spec and plan; no ADR or model changes.
- The pull request's file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes bead `coding-harness-yd8w`; its last commit carries `Closes-Bead: coding-harness-yd8w`.
- Special runs: none.

## Open decisions

None open.

- [DETAIL] The four-hour phase-4 appetite includes repairs; no appetite was stated and this is a bounded runner change.
- [DETAIL] An unreadable outer report cannot reliably identify individual entries to retain or drop, so it remains incomplete; process failures and refusals retain their existing handling. A readable category emptied by filtering needs an explicit `not_read` gap marker so the existing four-list contract remains valid without inventing a locator.
