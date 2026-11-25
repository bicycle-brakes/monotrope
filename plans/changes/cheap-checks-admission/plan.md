---
title: "Plan — cheap-checks-admission"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.13
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, workers]
---

# Plan — cheap-checks-admission

```text
For you:     Cheap tests use the targeted worker cap; the targeted kit probe stays serial and outside admission.
Done when:   Tests cover both cheap-test paths, the serial probe and blocking failures, and make verify is green.
Appetite:    2 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Changing the lock rule, gate selection, worker calculation, probe parallelism, or foreign-model environment filtering.
Pre-mortem:  suppose it failed: most likely because one cheap-test path still launches without the worker policy.
Starts unless you say stop.
```

## Build sequence and files

1. Change `scripts/stage2.py`: pass `targeted_pytest_env(root, env)` to the pytest launch in shared `cheap_checks`, leaving other launches and the targeted and full-mode admission behavior unchanged. The policy retains nonempty input settings and otherwise computes its usual bound when readings permit.
2. Change `tests/test_stage2_fail_fast.py`: exercise cheap pytest through targeted and full-mode preparation with controlled machine readings, an explicit input setting, and failure; assert the actual pytest launch environment.
3. Change `tests/test_stage2.py`: assert the selected kit probe stays outside admission and failure blocks; retain the existing admission proof.
4. Create `tests/test_kit_probe.py`: inspect the actual probe pytest subprocess command and assert it has no xdist `-n` option, including its joined form.
5. Change `docs/WORKFLOW.md`: describe the cheap pytest worker policy and the serial targeted kit probe without changing the outside-admission rule.

Do not edit `decisions/gates.yaml`, `scripts/kit/probe.py`, `run_gates`, other gate callers, the worker calculation, model environment allow-list, or full-verify scheduler. No held paths are planned for the implementation attempt.

Explore used Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`, because GLM 5.3 Flash via Z.ai had reached its weekly limit on 2026-11-25.

## Criterion ledger

- 1: not yet written tests/test_stage2_fail_fast.py::test_cheap_pytest_uses_targeted_worker_policy_in_both_modes — either preparation launches uncapped pytest.
- 2: not yet written tests/test_kit_probe.py::test_probe_pytest_remains_serial — the probe command contains an xdist worker option.
- 3: not yet written tests/test_stage2_fail_fast.py::test_cheap_pytest_preserves_explicit_worker_setting — the launch replaces a nonempty input setting.
- 4: tests/test_stage2.py::test_targeted_commands_run_without_verify_admission — a targeted command acquires admission or carries its markers.
- 5: not yet written tests/test_stage2_fail_fast.py::test_cheap_pytest_failure_remains_blocking — a red cheap pytest is accepted.
- 5: not yet written tests/test_stage2.py::test_targeted_kit_probe_failure_remains_blocking — a red selected kit probe is accepted.

## Verification

```sh
make verify
```

## Time used

2026-11-25 07:43:29–07:45:52 UTC, 142 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 08:07:28–08:11:35 UTC, 247 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
