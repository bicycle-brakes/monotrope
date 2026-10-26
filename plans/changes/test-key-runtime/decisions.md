---
title: "Decisions — test-key-runtime"
status: draft
implementation_status: partial
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-05op
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# test-key-runtime — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · How the planted test key stops blocking foreign calls

context: |
  Topic: the fake GLM key the stage-2 tests plant.
  Intention: the leak check refused review-loop round 2 of PR #250 because
  the key showed up as diff context in the prompt.
  Today: the key is one key-shaped literal in tests/test_stage2.py.
  Repository change: the literal is joined from two parts at run time; the
  leak check stays unchanged.
  Architecture change: none.
asked: 2026-10-26, conversation 2026-10-26 (interview)
answer: "Build the key at run time; the leak check stays unchanged; in its own pull request, then resume the loop of PR #250"
answered_by: maintainer
status: answered

In the context of the stage-2 test suite, facing a fake key that blocks real
foreign calls whenever it travels as diff context, we decided to join the
key from two parts at run time, to achieve that no prompt carries a
key-shaped literal, accepting that a future key-shaped literal in a test
blocks again until it is written the same way. — 2026-10-26
