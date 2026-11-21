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

1. Create `tests/test_gate_imports.py`: resolve the repository root from the test file, select direct `scripts/check_*.py` paths afresh and feed them to one path-list checker that parses without importing. Walk all AST nodes; inspect every name in import statements and track `importlib` module and `import_module` function names introduced by import statements, including aliases, for calls with a literal first positional argument or `name=` argument. Report offending paths and fail on parse errors. Match the runner exactly, not `stage2_*`.
2. In the same file, exercise that checker with a temporary matching script as the negative control and parameterized examples for each forbidden form, nested import, module and function alias, and the same forms naming family modules. Test fresh discovery against a temporary root with a newly added matching file; assert that an empty real selection fails and that the real discovery finds a known existing check script. Do not write fixtures into the real `scripts/` directory. No held path needs an edit.
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
- 2: not yet written tests/test_gate_imports.py::test_direct_runner_imports_are_rejected — an indicated form, later imported name, alias or function-local import is accepted
- 3: not yet written tests/test_gate_imports.py::test_literal_dynamic_runner_imports_are_rejected — a literal call through the module, module alias or imported function alias is accepted
- 4: not yet written tests/test_gate_imports.py::test_negative_control_rejects_runner_import — a temporary offending script is accepted
- 5: not yet written tests/test_gate_imports.py::test_unrelated_imports_are_allowed — an unrelated or stage2-family import in a specified form is rejected
- 6: not yet written tests/test_gate_imports.py::test_empty_gate_selection_fails — an empty selection passes

## Limits and ownership

Do not change `scripts/research_census.py`, runner files, `decisions/gates.yaml`, generated gate views, governance rules or tests outside the new test file. Tests elsewhere remain free to import the runner. Computed strings, assignment-created or cross-scope aliases, other dynamic import APIs and transitive imports are outside this static check's boundary. The orchestrator shows the card; this draft does not start implementation or commit.

## Time used

2026-11-21 17:48:07–17:49:58 UTC, 111 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 17:53:07–17:55:31 UTC, 144 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
