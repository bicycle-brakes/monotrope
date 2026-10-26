---
title: "Spec — test-key-runtime"
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
tags: [spec, stage-2, leak-check]
class: bounded
appetite: 1
adr_files: []
---

# Spec — test-key-runtime

The planted GLM test key in `tests/test_stage2.py` is no longer key-shaped
in the file's text (bead coding-harness-05op). Research: `research.md`.
Decisions: `decisions.md`, Q-1.

## Acceptance criteria

1. The leak check over a prompt that holds `tests/test_stage2.py` finds
   nothing at the planted key's line.
   *Refuted by:* a BLOCK at that line from `scripts/leakcheck.py --prompt-file`.
2. The tests still plant the same key value and still see it kept out of
   OpenCode Go calls.
   *Refuted by:* `test_the_foreign_environment_is_the_runners` failing.

## Out of scope

- Changing the leak check's rules or its `tests/` exemption.
