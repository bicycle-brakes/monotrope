---
title: "Decisions — runner-time-line"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-9wp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# runner-time-line — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · Who writes the measured time line, and does the runner retry red tests

context: |
  Topic: runner attempts (implement, repair) rejected for form, not for code.
  Intention: on 2026-10-20 six repair attempts in the research-swarm change
  failed only because no measured time line was added and because wall-clock
  tests lost their bounds on a loaded machine; each was booked by hand.
  Today: the model must add the line, which it cannot measure; any red test
  rejects the attempt.
  Repository change: the runner measures each attempt and writes the line
  itself; the added-line check goes. Red stays red: no retry rule; the
  load-sensitive tests are rebuilt to assert order instead of machine speed.
  Architecture change: none; ADR 0017's attempt sequence is unchanged.
asked: 2026-10-20, the conversation with the maintainer
answer: "okay, das muss im runner sofort korrigiert werden" (both causes), then
  "ja" to the recommendation: the runner writes the time line; no retry rule;
  repair the tests instead
answered_by: maintainer
status: answered

In the context of runner attempts rejected for a time line the model cannot
measure and for tests that depend on machine speed, facing a choice between a
retry rule in the runner and repairing the tests, we decided that the runner
writes the measured line itself and that the tests are made independent of
speed, to achieve attempts judged only on their code, accepting that a test
which still wobbles stays red until it is repaired. — 2026-10-20
