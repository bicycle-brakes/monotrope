---
title: "Decisions — verify-step-limit"
category: decisions
status: draft
implementation_status: none
date: 2026-11-11
created: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-xkvr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, draft]
---

# verify-step-limit — Decisions

Class: bounded (bead coding-harness-xkvr).

## Q-1 · Scope of this change

asked: 2026-11-11
answer: "Nur Stufe 1 (Empfohlen)" — only stage 1: raise the runner's make-verify step limit to 45 minutes; the messages that print it and the tests that pin 30 read the constant. Stage 2 (the limit as a value of the central configuration) goes to bead coding-harness-twvx; stage 3 (a default derived from measured durations) becomes a follow-up bead of its own.
answered_by: maintainer
status: answered
context: |
  Topic: the scope of the lane verify-step-limit (bead coding-harness-xkvr, the runner's step limit for make verify).
  Intention: the bead names three stages; for the class bounded the interview owes one question, and it concerns the scope.
  Today: the code fixes VERIFY_SECONDS = 30 minutes; full runs take 27 minutes in median, at least three died at the limit on 2026-11-11; the central configuration (bead coding-harness-twvx) is parked.
  Repository change: stage 1 changes one constant in scripts/stage2.py and the tests read the constant instead of a fixed "30"; stage 2 would need the central configuration, stage 3 measured data and a derivation rule.
  Architecture change: none for stage 1; stages 2 and 3 add a new configuration source.

In the context of full `make verify` runs that take 27 minutes in median
against the runner's fixed 30-minute step limit, facing at least three runs
on 2026-11-11 that died at the limit rather than on a red test while the
central configuration is parked, we decided to raise the constant to 45
minutes and let the messages and tests read it, leaving the central value to
bead coding-harness-twvx and the measured derivation to a follow-up bead,
to achieve relief at once with one runner file touched, accepting that the
limit stays a fixed constant in code until the central configuration lands
and does not grow with the suite on its own — 2026-11-11

## Settled from the tree

[DETAIL] The bead left open whether `scripts/verify_lock.py` uses
`VERIFY_SECONDS` as a limit of its own. It does not: the only occurrence
(`scripts/verify_lock.py:79`, read 2026-11-11 at `cc013cd8`) is prose stating
that the queue and memory waits consume neither `VERIFY_SECONDS` nor a pytest
proof's timeout. There is one limit, the runner's constant; the change does
not touch the lock.
