---
title: "Plan — test-key-runtime"
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
tags: [plan, stage-2, leak-check]
---

# Plan — test-key-runtime

```text
For you:     A diff that shows the stage-2 test file no longer stops a review-loop round at the leak check.
Done when:   The leak check is clean over the changed file, the stage-2 tests pass, and CI is green.
Appetite:    1 hour; stop at the limit.
Not now:     Changing the leak check.
Pre-mortem:  suppose it failed: most likely because another key-shaped literal sits elsewhere in the tests.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: write the planted key as `"sk-" + "<rest>"`.
2. This change folder and `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py
```

## Criterion ledger

- 1: not a test — `scripts/leakcheck.py --prompt-file` over the changed file, run 2026-10-26: clean; over `origin/main`: BLOCK at the key's line.
- 2: tests/test_stage2.py::test_the_foreign_environment_is_the_runners
