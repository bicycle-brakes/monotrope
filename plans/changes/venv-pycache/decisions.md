---
title: "Decisions — venv-pycache"
status: draft
implementation_status: none
date: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-q94b
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# venv-pycache — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · What the runner does with bytecode the test run wrote into the venv

context: |
  Topic: the runner's tool-integrity check over the worktree's `.venv/`.
  Intention: a pytest bytecode cache written into the venv during an
  attempt failed whole repair runs (bead coding-harness-q94b).
  Today: every changed file in the venv refuses the attempt.
  Repository change: new or changed `__pycache__` files in the venv are
  deleted after the call; every other venv change is still refused.
  Architecture change: none.
asked: 2026-10-23, conversation 2026-10-23 (interview)
answer: "delete instead of refuse: after the call the runner deletes new or changed files under __pycache__ inside the venv; every other change inside the venv is still refused"
answered_by: maintainer
status: answered

In the context of the runner's tool-integrity check, facing bytecode that a
test run writes into the venv, we decided that the runner deletes new or
changed `__pycache__` files in the venv after the call, to achieve that a
test run no longer fails an attempt while no planted code survives, accepting
that Python recompiles those files on the next import. — 2026-10-23
