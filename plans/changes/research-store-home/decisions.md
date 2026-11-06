---
title: "Decisions — research-store-home"
category: decisions
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-06
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

## Q-2 · Directory permissions: check, never change

asked: 2026-11-06
answer: "Prüfen, nie ändern (Recommended)" — like OpenSSH: a store directory the tool creates is created with mode 0700; an existing directory, the store or any ancestor, is never chmod'ed; the store directory is only checked (owned by the current user, not writable by group or other) and otherwise the run refuses with a clear message naming the command to fix it; root needs no special rules; criterion 5 is rewritten by a fresh draft to match.
answered_by: maintainer
status: answered
context: |
  Topic: the store tightens permissions of existing directories (chmod 0700); run as root it can hit system directories such as /, /usr or /opt.
  Intention: the review found the same mechanism a third time (L5-1, L8-1 to L8-3), and spec criterion 5 no longer matches the code. The maintainer asked for the smartest solution that carries most easily to other repositories.
  Today: several root special cases, none complete.
  Repository change: the chmod of existing directories and the root special cases go; a check with a refusal message replaces them; criterion 5 rewritten.
  Architecture change: none.

In the context of a store that changes permissions of directories it does not own, facing a third finding of the same mechanism, we decided to check permissions and never change an existing directory, to achieve a rule that holds for root and carries to any repository, accepting that a user with an unsafe existing store fixes it by hand. — 2026-11-06
