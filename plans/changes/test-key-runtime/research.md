---
title: "Research — test-key-runtime"
status: draft
implementation_status: complete
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
tags: [research, stage-2, leak-check]
---

# test-key-runtime — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `ab3bd415`
(2026-10-26).

## The finding

Round 2 of the review loop on PR #250 was refused by the leak check: the
change's diff showed `tests/test_stage2.py` as context, and its planted GLM
test key was written as one key-shaped literal. The leak check scans the
prompt text itself, so the fake key blocked a real foreign call (bead
coding-harness-05op).

## What exists today

- `tests/test_stage2.py` defines the planted GLM key as a single string
  literal near the top of the file.
- `scripts/leakcheck.py` exempts files under `tests/` from its secret
  rules when it scans the tree, but not the text of a prompt: a diff that
  carries the line is blocked.
- Measured on 2026-10-26: `scripts/leakcheck.py` over a prompt holding the
  unchanged file blocks at that line; over the changed file it is clean.

## Sources

- `scripts/leakcheck.py`, `tests/test_stage2.py` at `ab3bd415`.
