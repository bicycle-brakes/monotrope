---
title: "Plan — verify-absolute-python"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-4x2c
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verify, leerprobe]
---

# Plan — verify-absolute-python

```text
For you:     PYTHON=.venv/bin/python3 make verify stops failing leerprobe locally.
Done when:   The runner exports an absolute PYTHON, a test shows it from two caller directories, and leerprobe is green under make verify.
Appetite:    0.5 hours of phase 4; stop at the limit.
Not now:     The probe's own environment handling.
Pre-mortem:  suppose it failed: most likely because the path was resolved after the cd, against the wrong directory.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_ci.py`: add the regression test named in the ledger.
2. `scripts/verify_all.sh`: before the `cd`, turn a relative `$PYTHON`
   that contains `/` into `$PWD/$PYTHON`.
3. Update this plan, `findings.md` and `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_ci.py
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_ci.py::test_the_runner_exports_a_relative_python_as_an_absolute_path — a gate sees a relative or wrongly resolved path.
- 2: tests/test_ci.py::test_the_runner_prefers_the_checkouts_own_environment — the interpreter choice without `$PYTHON` changed.
- 2: tests/test_ci.py::test_an_absolute_or_bare_python_reaches_the_gate_unchanged — an absolute or bare `$PYTHON` is rewritten.
- 2: tests/test_ci.py::test_a_python_path_with_a_space_still_starts_the_gate — a gate starting with `python3` breaks under a directory with a space.

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction (conversation 2026-10-25). The review loop and the phase-6
Codex review are still owed.

## Time used
2026-10-25 11:40:01–11:46:30 UTC, 389 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
