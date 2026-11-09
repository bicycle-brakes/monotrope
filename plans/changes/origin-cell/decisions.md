---
title: "Decisions — origin-cell"
category: decisions
status: draft
implementation_status: partial
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-ywbh
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, implement, repair-brake]
---

# origin-cell — Decisions

Class: bounded (bead coding-harness-ywbh).

## Q-1 · Who fills the Origin cell the repair brake reads

asked: 2026-10-25
answer: the orchestrator sets the Origin cell when it decides a row; the runner refuses a taken row whose Origin is neither `base` nor `fix-r<N>`; no prompt change (maintainer, night-run plan of 2026-10-25, answer 4; confirmed as this change's interview on 2026-11-07).
answered_by: maintainer
status: answered
context: |
  Topic: the repair brake of ADR 0021 decision 7 reads an Origin cell that no prompt tells a reviewer to fill, so the brake never bites (deep review part B, finding DL-B-9, 2026-10-25).
  Intention: decide who owns the cell before the runner can rely on it.
  Today: the Origin cell stays empty; the brake is inert.
  Repository change: the runner refuses an accepted row (Status starting with `taken` or `fixed`, case-insensitively) without a valid Origin; the orchestrator writes Origin when it decides a row. Marking a row fixed preserves its acceptance, so fixed rows remain subject to the same Origin check.
  Architecture change: none; the brake ADR 0021 already describes starts to work.

In the context of a repair brake that reads an always-empty cell, facing a choice between reviewers and the orchestrator filling it, we decided that the orchestrator sets Origin and the runner refuses a taken row without base or fix-r<N>, to achieve a brake that bites without changing any reviewer prompt, accepting one more field per decided row. — 2026-11-07
