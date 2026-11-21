---
title: "Plan — gates-never-import-runner"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7ayv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, gates, imports]
---

# Plan — gates-never-import-runner

```text
For you:     Gate scripts cannot silently start importing the model runner.
Done when:   The existing pytest gate detects the specified imports, the negative control proves it, and make verify is green.
Appetite:    1 hour of phase 4, repairs included — a stop, not an estimate.
Not now:     Other scripts, indirect imports, computed imports, and new gates.
Pre-mortem:  suppose it failed: most likely because an import spelling escapes the static check.
Starts unless you say stop.
```

## Build sequence and files

1. Create `tests/test_gate_imports.py`: use one shared AST-based checker to scan the current direct `scripts/check_*.py` files without importing them. Detect the import forms and literal `importlib.import_module` calls in the spec, including imports nested in functions and aliased import statements; report the offending path and fail on parse errors. Do not match `stage2_*` as `stage2`.
2. In the same file, use temporary matching scripts and the same checker for a negative control and parameterized forbidden and allowed examples. Exercise discovery with a newly added matching file, and ensure an empty discovery cannot silently pass. No held path needs an edit.
3. The runner maintains `plans/changes/gates-never-import-runner/plan.md` time and ledger entries, `plans/changes/gates-never-import-runner/findings.md` findings, and the generated `plans/INDEX.md` when required. The spec is `plans/changes/gates-never-import-runner/spec.md`; update its status as the workflow requires. No files are deleted.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_gate_imports.py
python3 scripts/check_interview_minimums.py --change gates-never-import-runner
python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_gate_imports.py::test_all_gate_scripts_are_checked — a newly added matching script is ignored
- 2: not yet written tests/test_gate_imports.py::test_direct_runner_imports_are_rejected — an indicated import form or alias is accepted
- 3: not yet written tests/test_gate_imports.py::test_literal_dynamic_runner_imports_are_rejected — a specified literal call is accepted
- 4: not yet written tests/test_gate_imports.py::test_negative_control_rejects_runner_import — a temporary offending script is accepted
- 5: not yet written tests/test_gate_imports.py::test_unrelated_imports_are_allowed — an unrelated or stage2-family import is rejected

## Limits and ownership

Do not change `scripts/research_census.py`, runner files, `decisions/gates.yaml`, generated gate views, governance rules or tests outside the new test file. Tests elsewhere remain free to import the runner. Dynamic imports through computed strings, aliases of the import function or other APIs and transitive imports are outside this static check's boundary. The orchestrator shows the card; this draft does not start implementation or commit.

## Time used

2026-11-21 17:48:07–17:49:58 UTC, 111 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
