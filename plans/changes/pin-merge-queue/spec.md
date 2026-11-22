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

1. When a queue rule in the active branch-rules answer has `merge_method` equal to `MERGE` and each of `max_entries_to_build`, `max_entries_to_merge` and `min_entries_to_merge` equal to the integer 1, it supplies the freshness alternative.
   *Refuted by:* With the strict up-to-date flag off and all other rules satisfied, that queue is rejected.
2. When any one of the four pinned fields has a different value or an invalid type, that queue does not supply the freshness alternative.
   *Refuted by:* With the strict flag off and no other qualifying queue, a changed method, a group size other than 1, a boolean, a string or a null passes as freshness.
3. When no freshness alternative qualifies and a queue lacks a pinned field or its parameters object, the check reports a `not measured:` finding naming each missing pinned field.
   *Refuted by:* With the strict flag off and no other qualifying queue, an absent field passes or its name is absent from the failure.
4. When the queue's other measured parameters change, those parameters alone do not disqualify it as the freshness alternative.
   *Refuted by:* A queue with the four pinned values is rejected solely because `grouping_strategy`, `check_response_timeout_minutes` or `min_entries_to_merge_wait_minutes` differs or is absent.
5. When the strict up-to-date rule supplies freshness, the ruleset check continues to accept that alternative without a queue.
   *Refuted by:* A ruleset satisfying the existing floor with the strict flag and no queue fails for lack of a queue.
6. When a qualifying queue supplies freshness, its supplying ruleset remains subject to the existing fail-closed bypass and other ruleset-floor checks.
   *Refuted by:* A bypass, unreadable supplier, missing required rule or unpinned required check passes because the queue qualifies.
7. When the queue fixtures represent the measured rule, they use the measured field names and values for all four pinned fields.
   *Refuted by:* The fixture still substitutes `min_pull_requests` or `max_pull_requests`, omits a pinned field, or gives it a different value.

8. When a queue fails the pin, that queue alone does not make its ruleset a supplier for the bypass measurement.
   *Refuted by:* With the strict flag on, an invalid queue in a separate otherwise non-supplying ruleset causes its bypass list to be read or reported.
9. When no freshness alternative qualifies and a pinned field is present with a wrong value or type, the freshness finding names that field, its expected value and its found value.
   *Refuted by:* A changed `merge_method` yields only the instruction to activate an already active queue or omits the expected or found value.
10. When a strict rule supplies freshness alongside an invalid or incomplete queue, that queue does not remove the strict alternative.
    *Refuted by:* With the existing ruleset floor satisfied, a queue with `merge_method: SQUASH` or a missing pinned field makes the strict alternative fail.
11. When one queue qualifies alongside another invalid or incomplete queue, the invalid queue does not remove the qualifying alternative.
    *Refuted by:* With the strict flag off and the existing floor satisfied, a second queue with `merge_method: SQUASH` or a missing pinned field makes a valid queue fail.
12. When the live writer-side measurement reads queue parameters, it shows the observed `grouping_strategy`, `check_response_timeout_minutes` and `min_entries_to_merge_wait_minutes`, including an explicit absent marker for a missing field, without treating the display as a finding.
    *Refuted by:* A successful measurement hides a measured value, displays a missing field as an observed value, or fails solely because one of these fields is absent.

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

[DETAIL] The 2026-11-22 04:47 CET branch-rules readback in `findings.md` S-1 confirms the same four pinned values as the ruleset-detail measurement, so the existing branch-rules answer is the source.

[DETAIL] A queue that fails the pin cannot supply freshness, while an independently valid strict up-to-date rule or another qualifying queue can still supply it; this preserves the existing alternatives. Only a qualifying queue supplies freshness and bypass measurement; an invalid queue can still belong to a ruleset that supplies another requirement. When no alternative supplies freshness, identify missing fields as not measured and report wrong values as drift, so the refusal is actionable. A missing field is not a network failure; retain network/login advice only for actual access failures.

[DETAIL] Show the three unpinned values in the live writer-side measurement, with an explicit absent marker, because `decisions.md` says they are read and shown; they never become failing findings.

[DETAIL] A two-hour phase-4 stop allows for the tests and repair loop; neither research nor the interview sets an appetite. No maintainer decision is open.
