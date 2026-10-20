---
title: "Decisions — runner-precheck"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-csm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# runner-precheck — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · How a repair or implement attempt is checked before make verify

context: |
  Topic: what the stage-2 runner checks after a model's attempt, before the
  full make verify, and what the next attempt is told when it fails.
  Intention: on 2026-10-16 implement attempts failed repeatedly while the
  next attempt saw only cut gate tails; each make verify took about ten
  minutes. (Context reconstructed from the bead's record of the
  conversation of 2026-10-16; the wording shown then was not recorded.)
  Today: every attempt runs the full make verify; a red run passes on the
  last 80 lines per red gate.
  Repository change: a pre-check step and richer failure evidence in
  scripts/stage2.py.
  Architecture change: none; make verify stays the only commit gate and the
  model still runs no command.
asked: 2026-10-16, the evening conversation (recorded in bead coding-harness-csm)
answer: before the full make verify, run ruff on the changed Python files
  and the tests named in plan.md's criterion ledger; a red pre-check fails the
  attempt with those tests' full assertion messages and skips make verify; a
  red make verify adds the assertion text of the first failing tests; make
  verify stays the only check after which the runner commits; the model does
  not run pytest itself
answered_by: maintainer
status: answered

In the context of runner attempts that fail late and blind, facing a full
make verify per attempt and cut evidence, we decided a cheap pre-check of the
attempt's own tests and fuller assertion evidence, to achieve retries that
see why they failed, accepting that a green pre-check proves nothing on its
own. — 2026-10-20
