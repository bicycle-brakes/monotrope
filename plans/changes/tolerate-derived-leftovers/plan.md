---
title: "Plan — tolerate-derived-leftovers"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-b5w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, runner]
---

# Plan — tolerate-derived-leftovers

```text
For you:     A second run after a failed one starts without restoring the runner's own index and date stamps by hand.
Done when:   The second run starts on derived leftovers, a content edit is still refused (tests red first), and make verify is green.
Appetite:    1 hour of phase 4; stop at the limit.
Not now:     Putting derived writes back after a failure.
Pre-mortem:  suppose it failed: most likely because a content edit that also touched the updated: line slipped through.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: the two tests named in the ledger.
2. `scripts/stage2.py`: `derived_leftover`, `refuse_preexisting`; the
   three verbs call `refuse_preexisting`.
3. This plan, `findings.md`, `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k derived_writes
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_a_failed_runs_derived_writes_do_not_block_the_next_run — the second run is refused.
- 2: tests/test_stage2.py::test_a_hand_edit_beside_derived_writes_is_still_refused — a content edit starts the run, or the refusal lists the index.

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction. The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 12:39:57–12:44:24 UTC, 267 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
