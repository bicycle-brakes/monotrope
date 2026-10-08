---
title: "Plan — runner-red-gate"
status: draft
implementation_status: partial
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-zci
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, runner]
---

# Plan — runner-red-gate

```text
For you:     A failed implement attempt tells the next one which gate blocked and why.
Done when:   The four criteria have tests, make verify is green, reviewed code is in a PR.
Appetite:    2 hours; a stop, not an estimate.
Not now:     Derived-file regeneration (mfv), stored diagnostics, report-only gate output.
Pre-mortem:  suppose it failed: most likely because verify_all.sh renames its frame lines.
```

## Decided in phase 3

- [DETAIL] Implemented by the orchestrating session (Claude Code with
  Anthropic, Opus 5.5), not through `stage2.py implement`: this change repairs
  that route, and a new change folder trips the derived-file gap
  (coding-harness-mfv) a file-tool worker cannot clear.

## Steps

1. `scripts/stage2.py`: a pure `red_sections(output)` that returns the
   bounded sections of gates framed `RED (block)`, and `verify_attempt`
   using it with the 80-line tail as fallback; scrub as today.
2. `tests/test_stage2.py`: one test per criterion on `red_sections` and on
   `verify_attempt` with a stand-in `make`; a planted fault per test.

## Time used

2026-10-07 22:36–22:41 UTC, 5 min, orchestrator clock (Claude Code with
Anthropic, Opus 5.5): `red_sections`, the criterion tests, five planted
faults each turned its test red, `make verify` green. The research, spec and
plan before 22:36 were not clocked.
