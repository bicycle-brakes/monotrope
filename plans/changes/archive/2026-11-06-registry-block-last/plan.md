---
title: "Plan — registry-block-last"
status: accepted
implementation_status: done
date: 2026-11-03
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-2g7y
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, stage-2]
---

# Plan — registry-block-last

```text
For you:     A repairing model sees why plans-registry blocked, even behind hundreds of drift lines.
Done when:   The new test is red without the fix and green with it, make verify is green, phase 6 is clean.
Appetite:    1 hour, repairs included; stop at the limit.
Not now:     The runner's tail rule, gate levels, or archiving the drift sources.
Pre-mortem:  suppose it failed: most likely because a test pins the exact rendered text of a mixed report.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_gate_machinery.py`: a report with one block and 300 drift
   findings ends with the repeated block; a block-only report has no repeat.
   Red against the unchanged `_verdict.py` (orchestrator, 2026-11-03).
2. `scripts/_verdict.py`: `Verdict.render()` appends the repeated block
   messages when other findings follow.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_gate_machinery.py
make verify
```

## Criterion ledger

- 1: tests/test_gate_machinery.py::test_a_verdict_repeats_its_blocking_lines_after_the_noise — the tail of a mixed report does not name its block
- 2: tests/test_gate_machinery.py::test_a_verdict_repeats_its_blocking_lines_after_the_noise — a block-only report gains the repeat

## Time used

2026-11-03 08:40–09:00 UTC — orchestrator, by hand: test red without the fix, green with it (a71cda8c)
