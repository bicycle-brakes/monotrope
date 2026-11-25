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
For you:     Cheap tests and the targeted kit probe use the existing worker cap without waiting for verify admission.
Done when:   Tests prove the worker policy reaches both pytest processes, failures still block, and make verify is green.
Appetite:    2 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Changing the lock rule, gate selection, worker calculation, or foreign-model environment filtering.
Pre-mortem:  suppose it failed: most likely because the worker setting does not reach the probe's child pytest.
Starts unless you say stop.
```

## Build sequence and files

1. Change `scripts/stage2.py`: pass `targeted_pytest_env(root, env)` to cheap-check pytest in the shared `cheap_checks` function; pass the same policy to the targeted gate execution so the selected kit probe inherits it. Preserve the caller's environment, existing selection, diagnostics and admission-marker stripping; keep the full check's admission unchanged.
2. Change `tests/test_stage2_fail_fast.py`: exercise cheap pytest through both targeted and full-mode preparation with controlled worker readings and explicit overrides, including a failing pytest.
3. Change `tests/test_stage2.py`: exercise selection and execution of the kit probe with a child pytest environment, an explicit override, a failing probe, and an active outer admission; retain existing targeted and full admission proofs. Verify propagation through the real `scripts/kit/probe.py` child boundary, not only the gate launch mock.
4. Change `docs/WORKFLOW.md`: describe the shared worker policy for cheap pytest and the targeted kit probe, and retain the outside-admission rule.

Do not edit `decisions/gates.yaml`, `scripts/kit/probe.py`, the worker calculation, model environment allow-list, or full-verify scheduler. No held paths are planned for the implementation attempt.

Explore used Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`, because GLM 5.3 Flash via Z.ai had reached its weekly limit on 2026-11-25.

## Criterion ledger

- 1: not yet written tests/test_stage2_fail_fast.py::test_cheap_pytest_uses_targeted_worker_policy_in_both_modes — either caller launches uncapped pytest.
- 2: not yet written tests/test_stage2.py::test_targeted_probe_child_pytest_uses_worker_policy — the child loses the computed worker setting.
- 3: not yet written tests/test_stage2.py::test_affected_pytests_preserve_explicit_worker_setting — either child replaces the caller's value.
- 4: tests/test_stage2.py::test_targeted_commands_run_without_verify_admission — a targeted command acquires admission or carries its markers.
- 5: not yet written tests/test_stage2.py::test_affected_pytest_failures_remain_blocking — a red cheap pytest or kit probe is accepted.

## Verification

```sh
make verify
```

## Time used

2026-11-25 07:43:29–07:45:52 UTC, 142 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
