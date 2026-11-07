---
title: "Decisions — session-launch-length"
category: decisions
status: draft
implementation_status: none
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-rm8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, implement, session]
---

# session-launch-length — Decisions

Class: bounded (bead coding-harness-rm8).

## Q-1 · Reasoned interview skip

asked: 2026-11-07
answer: "ja" — the maintainer approved a reasoned interview skip for this bug: a measured cause (the terminal truncates the launch command at its input-line limit, MAX_CANON, so the session never starts; observed 2026-10-20 21:16Z and 21:19Z) and one obvious remedy, so the night run may draft spec and plan.
answered_by: maintainer
status: answered
context: |
  Topic: `stage2.py session` builds a launch command that a terminal cuts at its input-line limit, so the session never starts.
  Intention: the night run of 2026-11-07 takes clear bugs to their plan card; this one needs no behaviour choice from the maintainer.
  Today: a long prompt makes the launch fail silently.
  Repository change: the launch avoids the line limit (for example the prompt travels as a file, not on the command line), with a test.
  Architecture change: none.

In the context of a launch command cut by the terminal, facing a choice between asking the maintainer and a reasoned skip, we decided to skip the interview with this reason, to achieve a plan card by morning, accepting that any behaviour question the explore surfaces still goes to the maintainer. — 2026-11-07
