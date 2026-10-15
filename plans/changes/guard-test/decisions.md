---
title: "Decisions — guard-test"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-0ho
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, repair, red-first]
---

# A guard-test mark for test-only repairs — Decisions

Phase 1a for bead coding-harness-0ho (class bounded). Before the interview
the maintainer chose, in the conversation on 2026-10-15, way A: a guard-test
mark whose test plants the fault itself and must be red with the planted
fault and green without it (rejected: a runner-side mutation check, an
exception without proof), built before the implementation of
coding-harness-agx.

## Q-1 · How the runner tells "with fault" from "without fault"

asked: 2026-10-15
answer: "ja" — option A: the runner runs a guard test twice, once with the environment variable `STAGE2_PLANT_FAULT=1`, where it must be red, and once without, where it must be green; the test plants its fault only when the switch is set.
answered_by: maintainer
status: answered
context: |
  Topic: how the runner proves that a guard test really catches the fault it plants, without taking the model's word.
  Intention: the maintainer decided that a guard test plants the fault itself and must be red with it and green without; open was how the runner separates the two runs.
  Today: the runner runs the named test once on the baseline code and demands red; it reads the test file only to see that the function exists; hand-written guard tests of this kind exist (haiku-5-5), but the runner cannot use them as proof.
  Repository change: the repair answer form `fixed — guard test — tests/…::test_…`, `red_first` with two runs, the status words in the findings template, `prompts/04-implement.md`, `docs/WORKFLOW.md`. Options: A — a switch `STAGE2_PLANT_FAULT` (simple; a test that just fails under the switch without planting a real fault must be caught in phase 6; the runner checks only that the switch appears in the test); B — the line names the guarded function and the runner replaces it with one that finds nothing (stricter, but only for checker functions returning a list of problems).
  Architecture change: a second kind of proof beside "red on the baseline"; ADR 0017 gets a [DETAIL] note, no new ADR, because the principle "every finding needs a proof" stays.

In the context of repairs whose right fix is a test over code that is
already right, facing the choice between a switch the test reads and a
runner that disables a named function, we decided on the switch
`STAGE2_PLANT_FAULT` with one red run with it and one green run without, to
achieve a proof for guard tests that matches the maintainer's choice,
accepting that phase 6 must check that the switch plants a real fault. — 2026-10-15
