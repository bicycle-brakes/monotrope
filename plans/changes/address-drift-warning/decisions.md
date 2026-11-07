---
title: "Decisions — address-drift-warning"
category: decisions
status: draft
implementation_status: none
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-x2g9
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, opencode-go, address]
---

# address-drift-warning — Decisions

Class: bounded (bead coding-harness-x2g9).

## Q-1 · Reasoned interview skip

asked: 2026-11-07
answer: "ja" — the maintainer approved a reasoned interview skip: the runner warns when a live catalog entry's baseUrl or api differs from the declared Go address; cause and remedy are clear, so the night run may draft spec and plan.
answered_by: maintainer
status: answered
context: |
  Topic: the OpenCode Go call address is declared in model-endpoints.yaml (ADR 0024); a catalog entry whose baseUrl or api differs from it passes today without a word.
  Intention: the night run of 2026-11-07 takes clear changes to their plan card; this one needs no behaviour choice from the maintainer.
  Today: a differing catalog address goes unnoticed.
  Repository change: a warning in the runner's catalog handling, with a test.
  Architecture change: none.

In the context of a silent difference between the catalog and the declared Go address, facing a choice between asking the maintainer and a reasoned skip, we decided to skip the interview with this reason, to achieve a plan card by morning, accepting that a behaviour question the explore surfaces still goes to the maintainer. — 2026-11-07
