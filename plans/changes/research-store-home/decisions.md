---
title: "Decisions — research-store-home"
category: decisions
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-nxdy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm, state-store]
---

# research-store-home — Decisions

Class: bounded (bead coding-harness-nxdy).

## Q-1 · Where the research swarm's store lives

asked: 2026-11-04
answer: "A: eigene Variable + Standard (Recommended)" — a variable of its own for the research store only (for example STAGE2_RESEARCH_STATE), with a documented default outside the home directory (for example /Users/Shared/<user>-stage2-research, mode 700); the verify lock's queue stays where it is, so there is always one lock.
answered_by: maintainer
status: answered
context: |
  Topic: the research swarm refuses a state store inside the home directory (bead coding-harness-nxdy).
  Intention: on 2026-11-04 the orchestrator worked around it with XDG_STATE_HOME=/Users/Shared/mikypiky-stage2-state, which also moves the verify lock's queue; two lanes with different settings would hold two locks and could run make verify twice at once.
  Today: one variable, XDG_STATE_HOME, places both; only the default inside the home directory is documented.
  Repository change: a dedicated variable and default for the research store; the verify lock keeps its own location.
  Architecture change: a new setting.

In the context of a research store that refuses the home directory and a workaround that also moves the verify lock, facing the risk of two locks and two concurrent full verifications, we decided on a dedicated research-store variable with a documented default outside home, to achieve a swarm that runs without a manual setting and exactly one verify lock, accepting one more setting to document. — 2026-11-04
