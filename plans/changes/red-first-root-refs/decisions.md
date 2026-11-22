---
title: "Decisions — red-first-root-refs"
category: decisions
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-dk0h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, red-first, refs]
---

# red-first-root-refs — Decisions

Class: bounded (bead coding-harness-dk0h).

## The bead and its source (read by the orchestrator, 2026-11-22)

> Follow-up of F-10 from the phase-6 re-check 3 of the red-first private-clone change (bead coding-harness-wkxm, PR #320): the reference comparison measures refs/ but not root references such as ORIG_HEAD, FETCH_HEAD or MERGE_HEAD, so a red-first run that moves one of them goes unseen. Remedy proposed in plans/changes/red-first-own-refs/findings.md (F-10). Accepted as a named limit by the maintainer on 2026-11-03.

F-10 (archived red-first-own-refs findings, line 628): a qualifying named test can run `git update-ref ORIG_HEAD HEAD` and leave a persistent reference change that both proofs accept, because `_proof_ref_targets` and `_ref_targets` enumerate `refs/` and HEAD only.

## SKIP · interview

status: skipped
reason: The bead and F-10 fix the gap and its remedy (root references must also invalidate the proof); the maintainer accepted it as a named limit on 2026-11-03 and filed this follow-up to close it. The maintainer asked for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Which root references:** every file directly in the git directory whose name is all capitals, digits and underscores and ends in `HEAD` (ORIG_HEAD, FETCH_HEAD, MERGE_HEAD, CHERRY_PICK_HEAD, REVERT_HEAD, BISECT_HEAD, AUTO_MERGE and HEAD itself), read as file content, so a pseudo-ref with several lines (FETCH_HEAD) compares whole. Reason: git's own pseudo-ref naming, and FETCH_HEAD is not a single object id.
- **Both snapshots** (`_proof_ref_targets` and `_ref_targets`) include them; a created, changed or deleted root reference invalidates the proof with the reference named. Reason: F-10's remedy.
- **The limit text** that named this gap is removed from the living docs where it stands. Reason: the limit no longer holds.
- **Regression:** a named test that runs `git update-ref ORIG_HEAD HEAD` (and one that writes FETCH_HEAD) is refused, red before the fix. Reason: F-10's case.
