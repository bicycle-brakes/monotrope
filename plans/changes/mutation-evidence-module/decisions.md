---
title: "Decisions — mutation-evidence-module"
status: draft
implementation_status: partial
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-diic
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# mutation-evidence-module — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · How the repair of PR #248 is made red-first

context: |
  Topic: the gate ratchet's mutation-evidence analyzer.
  Intention: the repair of PR #248 failed red-first because the analyzer
  and its new tests share tests/test_ci.py.
  Today: the analyzer lives inside the test file.
  Repository change: a small pull request moves the analyzer unchanged into
  a module under scripts/; then PR #248 is repaired as usual.
  Architecture change: none.
asked: 2026-10-26, conversation 2026-10-26 (interview)
answer: "Move the analyzer into its own module first (recommended), then repair PR #248 normally"
answered_by: maintainer
status: answered

In the context of the gate ratchet, facing a repair that cannot be shown red
first while the analyzer sits in its own test file, we decided to move the
analyzer unchanged into `scripts/mutation_evidence.py`, to achieve that the
runner's red-first check runs new tests against the old analyzer, accepting
one more module that travels with the kit. — 2026-10-26
