---
title: "Plan — repair-restore-status"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-rcyf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, repair]
---

# Plan — repair-restore-status

```text
For you:     A repair the commit guard refuses no longer leaves its rows marked fixed by tests that are gone.
Done when:   A test that plants a refused path is red first and green after, and make verify is green.
Appetite:    1 hour of phase 4; stop at the limit.
Not now:     Refusing rows up front whose fix may lie in a human-written path.
Pre-mortem:  suppose it failed: most likely because the snapshot was taken after before_commit wrote the statuses.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: the test named in the ledger.
2. `scripts/stage2.py`: in `run_attempts`, wrap `checkpoint`; on `Refused`
   or `CallFailed`, `restore_findings(kept)` and re-raise.
3. This plan, `findings.md`, `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k commit_guard_leaves
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_a_repair_refused_at_the_commit_guard_leaves_its_rows_taken — a row stays fixed or the phase-6 rows differ.
- 2: tests/test_stage2.py::test_a_repair_refused_at_the_commit_guard_leaves_its_rows_taken — the attempt's test survives.

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction. The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 12:06:46–12:11:32 UTC, 286 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
2026-10-25 20:22:07–20:33:00 UTC, 653 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
