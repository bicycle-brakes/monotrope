---
title: "Decisions — swarm-test-speed"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-dca4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# swarm-test-speed — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; one
answered below).

## Q-1 · May the change speed up production code, or only tests

context: |
  Topic: the scope of the speedup (bead coding-harness-dca4).
  Intention: settle before drafting whether the change may touch code
  under scripts/ or only tests.
  Today: the slowest swarm test spends about two thirds of its time
  parsing the 578-line model-endpoints.yaml again before every model slot;
  that happens in scripts/stage2_availability.py (read_declaration), not in
  the tests (research.md, "Orchestrator profile — 2026-10-28"). The bead
  said test-only.
  Repository change: option 1 — scripts/stage2_availability.py parses with
  the C loader and reuses the parse while the file bytes are unchanged; the
  file is still read fresh before every slot. Option 2 — tests only: the
  test world gets a smaller declaration.
  Architecture change: none; with option 1 a changed file is still noticed
  at once.
  Question: may the change speed up production code?
asked: 2026-10-28, the directing conversation
answer: option 1 — yes, production code too
answered_by: maintainer
status: answered

In the context of a test suite whose slowest file spends most of its time
in the production declaration parse, facing a production speedup or a
test-only smaller declaration, we decided to allow a behaviour-preserving
production speedup, to remove the cause for tests and real runs alike,
accepting that the change now touches scripts/ and must prove that a changed
declaration is still read before every slot. No test is deleted or renamed;
the bead's other limits stand. — 2026-10-28
