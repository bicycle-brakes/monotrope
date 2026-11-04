---
title: "Decisions — registry-block-last"
category: decisions
status: draft
implementation_status: none
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-2g7y
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verification, stage-2]
---

# registry-block-last — Decisions

Class: bounded.

## SKIP · interview

status: skipped
reason: A bounded bug fix whose intent the maintainer stated on 2026-11-03 in the conversation ("A: Abnahme + Fix parallel" — the blocking lines reach the model, in its own small pull request; then "B: kleiner Ordner + Phase 6"). No design choice is left that the maintainer must answer; the mechanics are decided below with reasons.

## Decided by the agent

[DETAIL] **Repeat, do not reorder.** The report keeps BLOCK first for a human
reader and repeats the blocking messages last when other findings follow.
Reason: a reader of the head and a reader of the tail both see the block; no
assertion on the existing order breaks.

[DETAIL] **Fix in `_verdict.py`, not in the runner.** Reason: every gate that
renders through it gains the same tail, and the runner's tail rule stays one
rule for all gates.

[DETAIL] **No repeat when only blocks stand.** Reason: the block section is
then already the tail.
