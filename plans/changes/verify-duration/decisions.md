---
title: "Decisions — verify-duration"
category: decisions
status: draft
implementation_status: partial
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-1um6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verify, measurement]
---

# verify-duration — Decisions

Class: spike (bead coding-harness-1um6).

## Q-1 · How to measure

asked: 2026-11-04
answer: "B: dauerhaft pro Gate (Recommended)" — scripts/verify_all.sh reports every gate's duration on every run, not a one-off hand measurement.
answered_by: maintainer
status: answered
context: |
  Topic: no per-gate or per-run duration record exists; every number so far was taken by hand.
  Intention: measure make verify before the beads that shrink it (coding-harness-0swp, coding-harness-vg9) so their effect can be checked.
  Today: about 12-13 minutes in total (WORKFLOW), tests/test_stage2.py alone about 9.5 minutes; no per-gate times.
  Repository change: verify_all.sh's gate loop times each gate.
  Architecture change: one line of output per gate.

In the context of make verify without any duration record, facing two changes that promise a shorter run, we decided to time every gate on every run, to achieve a before-and-after comparison without repeated hand measurement, accepting a small change to verify_all.sh. — 2026-11-04

## Q-2 · Where the numbers go

asked: 2026-11-04
answer: "C, denke hier auch sowas wie Memory mir, inwiefern kann das relevant sein" — both: the console line and a local append-only record outside the repository; each record also carries the free memory at start, the pytest worker count and the wait at the verify lock (orchestrator's reading of "memory" as RAM, stated in the conversation).
answered_by: maintainer
status: answered
context: |
  Topic: where the per-gate durations are kept.
  Intention: compare runs over days; separate code-caused from machine-caused duration.
  Today: verify_all.sh prints to the console only; the verify lock refuses entry below 25 % free memory, and the worker count is derived from cores and free memory.
  Repository change: an append-only record in the verify lock's state directory (date, commit, gate, seconds, result, free memory, workers, lock wait) and a small reader.
  Architecture change: a local measurement record, never committed, never sent anywhere.

In the context of per-gate durations that vanish after the run, facing durations that may depend on free memory and parallel lanes as much as on code, we decided to print each gate's time and append it, with free memory, worker count and lock wait, to a local record, to achieve comparable runs with the machine's state as a named rival explanation, accepting a file outside the repository that grows with every run. — 2026-11-04

## Q-3 · What the spike delivers

asked: 2026-11-04
answer: "A: Messung + Basislinie + Vorschlag (Recommended)" — the measurement, a baseline of at least five runs with pytest --durations for the 30 slowest tests, and a note in docs/research/ that proposes a time budget as a warning threshold; the budget itself is the maintainer's decision.
answered_by: maintainer
status: answered
context: |
  Topic: the spike's output.
  Intention: a budget from numbers, not a guessed one.
  Today: no budget, no baseline.
  Repository change: the measurement and a research note; no gate.
  Architecture change: none.

In the context of a suite with no baseline, facing the wish for a time budget, we decided to deliver measurement, a five-run baseline and a proposed budget, to achieve a budget decision on numbers, accepting that a warning gate waits for a later change. — 2026-11-04
