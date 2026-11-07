---
title: "Decisions — swarm-time-limits"
category: decisions
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-ht1b
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm, time-limits]
---

# swarm-time-limits — Decisions

Class: bounded (bead coding-harness-ht1b).

## Q-1 · Which limits move into the configuration

asked: 2026-11-04
answer: "Mache a, lege bead für B an" — only the research swarm's per-role and run limits move into one checked-in configuration; every other runner time limit follows in its own change (bead coding-harness-phop).
answered_by: maintainer
status: answered
context: |
  Topic: the research swarm's time limits are hard-coded (scripts/stage2_research_run.py MINUTES and RUN_MINUTES), and so are the review loop's and the other runner calls'.
  Intention: the finder seat timed out three times on 2026-11-04 and "more time" must not need a code change (maintainer).
  Today: every limit change is a code change with tests and WORKFLOW text.
  Repository change: one checked-in configuration the runner reads and validates for the swarm's limits.
  Architecture change: a new configuration file with a strict loader; a missing or implausible value is refused.

In the context of the research swarm's hard-coded per-role limits, facing a finder that timed out three times and the maintainer's demand that more time need no code change, we decided to move only the swarm's limits into one checked configuration, to achieve an unblocked swarm with a small bounded change, accepting that the other runner limits stay in code until bead coding-harness-phop. — 2026-11-04

## Q-2 · The finder limit

asked: 2026-11-04
answer: "20 Minuten (Recommended)" — the finder limit is 20 minutes; the run limit grows by the same 10 minutes to 160.
answered_by: maintainer
status: answered
context: |
  Topic: the starting value of the finder limit in the new configuration.
  Intention: measured 2026-11-04 — deepseek-v4.1-flash needed 434 s, claude-haiku-5-5 52 s, mimo-v2.6-flash and longcat-2.0 stopped at 600 s.
  Today: finders 10 minutes, run 150 minutes; merge 10, sentence 5, topics 10, judge 15 did not fail.
  Repository change: the finder value in the configuration; the run total grows with it.
  Architecture change: none beyond Q-1.

In the context of the finder stage that timed out at 600 s on 2026-11-04, facing an unknown real need of the slower Go Flash models, we decided on a 20-minute finder limit and a 160-minute run limit, to achieve finders that finish on this repository, accepting that a hanging model holds the run up to 10 minutes longer. — 2026-11-04

## Decided by the agent

[DETAIL] **The other per-role values stay as they are** (merge 10, sentence 5, topics 10, judge 15 minutes): none failed on 2026-11-04; they move into the configuration unchanged.
