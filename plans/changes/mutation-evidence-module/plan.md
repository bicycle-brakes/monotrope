---
title: "Plan — mutation-evidence-module"
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
tags: [plan, ci, ratchet]
---

# Plan — mutation-evidence-module

```text
For you:     The repair of PR #248 can be shown red first.
Done when:   The analyzer lives in scripts/mutation_evidence.py, tests/test_ci.py imports it, and make verify is green.
Appetite:    1 hour; stop at the limit.
Not now:     Changing what counts as evidence.
Pre-mortem:  suppose it failed: most likely because the moved module does not travel with the kit.
Starts unless you say stop.
```

## Files and steps

1. `scripts/mutation_evidence.py` (new), `tests/test_ci.py`.
2. `scripts/ci_gates.py` (`OHNE_AUFRUFER`), `scripts/kit/manifest.yaml`.
3. This change folder and `plans/INDEX.md`.

## Verification

```sh
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_ci.py::test_every_gate_step_has_a_mutation_test
- 2: tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
- 3: not a test — the empty-repository probe (gate leerprobe) inside `make verify`, green at 9b43dd4e on 2026-10-26.
