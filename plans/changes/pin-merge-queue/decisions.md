---
title: "Decisions — pin-merge-queue"
category: decisions
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-tsdr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, merge-queue, repo-settings]
---

# pin-merge-queue — Decisions

Class: bounded (bead coding-harness-tsdr).

## The bead and the measurement (orchestrator, 2026-11-22)

> Follow-up of coding-harness-eh42 (maintainer, 2026-10-30, 'Erst messen, dann pinnen'): after the queue is switched on, read the active merge_queue rule's parameter names and values from gh api; then make tests/test_repo_settings.py's _merge_queue_rules accept only merge method MERGE and groups of one, with fixtures using the measured field names (the eh42 fixtures use unmeasured names min_pull_requests/max_pull_requests).

Measured on 2026-11-22 at 04:37 CET with `gh api repos/bicycle-brakes/monotrope/rulesets/24528176` (ruleset `main`, enforcement `active`), the `merge_queue` rule's parameters:

| Field | Value |
|---|---|
| `merge_method` | `MERGE` |
| `max_entries_to_build` | `1` |
| `max_entries_to_merge` | `1` |
| `min_entries_to_merge` | `1` |
| `min_entries_to_merge_wait_minutes` | `0` |
| `grouping_strategy` | `ALLGREEN` |
| `check_response_timeout_minutes` | `60` |

## SKIP · interview

status: skipped
reason: The maintainer decided the method on 2026-10-30 ("Erst messen, dann pinnen"); the measurement above is the "measure" step, and the bead fixes what is pinned (merge method MERGE, groups of one). The maintainer asked for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **What "groups of one" pins:** `max_entries_to_build`, `max_entries_to_merge` and `min_entries_to_merge` all equal 1. Reason: each of the three can make a group larger than one.
- **What is not pinned:** `grouping_strategy`, `check_response_timeout_minutes` and the wait minutes are read and shown but not refused. Reason: the bead pins method and group size only.
- **Fixtures use the measured field names** and the measured payload shape; the unmeasured eh42 names (`min_pull_requests`, `max_pull_requests`) leave the fixtures. Reason: the bead.
- **A missing field refuses** (the rule cannot be judged), naming the field. Reason: an absent parameter is not evidence of a group of one.
