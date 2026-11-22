---
title: "Spec — pin-merge-queue"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-tsdr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, merge-queue, repo-settings]
class: bounded
appetite: 2
adr_files: []
---

# Spec — pin-merge-queue

The ruleset check recognises a merge queue as the freshness alternative only when its merge method and group sizes match the measured settings (bead `coding-harness-tsdr` — pin the merge queue). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `d77bf280`, the ruleset check accepts any active merge queue as the freshness alternative, even if its method or group sizes drift; its fixture uses field names that were not measured (`research.md`, “What exists today”). On 2026-11-22 the active ruleset's parameters were measured, including the method and all three group-size fields (`decisions.md`, “The bead and the measurement”).

## Acceptance criteria

1. When a queue rule has `merge_method` equal to `MERGE` and each of `max_entries_to_build`, `max_entries_to_merge` and `min_entries_to_merge` equal to the integer 1, it supplies the freshness alternative.
   *Refuted by:* With the strict up-to-date flag off and all other rules satisfied, that queue is rejected.
2. When any one of the four pinned fields has a different value or an invalid type, that queue does not supply the freshness alternative.
   *Refuted by:* With the strict flag off and no other qualifying queue, a changed method, a group size other than 1, a boolean, a string or a null passes as freshness.
3. When a pinned field is missing from a queue used as the freshness alternative, the check refuses it and names the missing field.
   *Refuted by:* With the strict flag off and no other qualifying queue, an absent field passes or its name is absent from the failure.
4. When the queue's other measured parameters change, those parameters alone do not disqualify it as the freshness alternative.
   *Refuted by:* A queue with the four pinned values is rejected solely because `grouping_strategy`, `check_response_timeout_minutes` or `min_entries_to_merge_wait_minutes` differs or is absent.
5. When the strict up-to-date rule supplies freshness, the ruleset check continues to accept that alternative without a queue.
   *Refuted by:* A ruleset satisfying the existing floor with the strict flag and no queue fails for lack of a queue.
6. When a qualifying queue supplies freshness, its supplying ruleset remains subject to the existing fail-closed bypass and other ruleset-floor checks.
   *Refuted by:* A bypass, unreadable supplier, missing required rule or unpinned required check passes because the queue qualifies.
7. When the queue fixtures represent the measured rule, they use the measured field names and values for all four pinned fields.
   *Refuted by:* The fixture still substitutes `min_pull_requests` or `max_pull_requests`, omits a pinned field, or gives it a different value.

## Non-goals

- Pinning grouping strategy, response timeout or wait minutes; changing queue settings or merge procedure; adding an automatic rollback.
- Changing the ruleset gate's wiring, other protection requirements, governance rules or the architecture decision records.

## Protected areas

Leave `decisions/gates.yaml`, `docs/governance/`, `prompts/`, `templates/`, `.github/` and `AGENTS.md` unchanged: the existing gate and the previously decided queue policy remain in place.

## Definition of Done

- `make verify` green, including the existing writer-side ruleset gate where its live measurement is available.
- No ADR or policy document changes; the change artifacts and their registry entry accompany the test change.
- The protected areas untouched and the non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead `coding-harness-tsdr` and its last commit carries `Closes-Bead: coding-harness-tsdr`.
- Special runs: none.

## Open decisions

[DETAIL] A queue that fails the pin cannot supply freshness, while an independently valid strict up-to-date rule or another qualifying queue can still supply it; this preserves the existing alternatives. When no alternative supplies freshness, identify missing pinned fields in the finding so the refusal is actionable.

[DETAIL] A two-hour phase-4 stop allows for the tests and repair loop; neither research nor the interview sets an appetite. No maintainer decision is open.
