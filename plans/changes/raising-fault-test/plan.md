---
title: "Plan — raising-fault-test"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-xrzf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, repair, red-first]
---

# Plan — raising-fault-test

```text
For you:     Models learn to turn a raising fault into a regression test's failed expectation.
Done when:   Both instruction surfaces have mutation-tested guidance, existing proof regressions pass, and make verify is green.
Appetite:    1 hour of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Guard tests, new proof rules, and repair of the motivating finding.
Pre-mortem:  suppose it failed: most likely because the guidance reached only one repair route.
Starts unless you say stop.
```

## Build sequence and files

1. Attempt: in `scripts/stage2.py`, add the sentence below beside the baseline-test requirement in shared `REPAIR_ANSWER`; change no proof logic.
2. Attempt: in `tests/test_stage2.py`, add `test_repair_prompts_cover_a_fault_that_raises`, checking both `REPAIR_FORMAT` variants with whitespace normalized. Factor a small test-local checker for the guidance; prove it rejects removal of the sentence, the specific-exception instruction, either failure form, and a reversal to passing. Name these planted faults in the docstring and measure the test red before the instruction insertion, then green.
3. Orchestrator bootstrap, after the accepted attempt: in held `prompts/04-implement.md`, add the same sentence next to the repair paragraph's red-first rule. In `tests/test_stage2.py`, add `test_implement_prompt_covers_a_fault_that_raises`, using the same checker and planted omissions against the real prompt. The attempt must not edit this held prompt or add a test that requires its pending edit to pass.
4. Orchestrator: run the commands below after the bootstrap edit; measure the implement-prompt test red with the sentence removed in a temporary text copy and green with it present. Keep both test names stable and remove each ledger's `not yet written` marker when its test is defined.

Sentence for both locations:
> When the fault itself raises an exception, catch that specific exception in the regression test body and fail with `assert` or `pytest.fail` so the baseline failure states the test's expectation.

The attempt and orchestrator update `plans/changes/raising-fault-test/spec.md` and `plans/changes/raising-fault-test/plan.md` implementation status as work advances; only the runner writes measured entries under Time used. The runner owns `plans/changes/raising-fault-test/findings.md` evidence and generated `plans/INDEX.md` updates. No deletions. No design or ADR is due for class `bounded`.

## Limits and route

Do not touch proof/probe functions, status parsing, model routes, other change folders, `docs/WORKFLOW.md`, `docs/testing.md`, gates, ADRs or other held paths. The full verification after bootstrap is required even if the accepted attempt was green before it. Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash`; no Stage-1 fallback is recorded. At `85a344b7` (2026-11-03), `templates/plan.md` and `scripts/validate_change_artefacts.py` do not exist; use the phase-3 prompt's form and report the missing validator. This change's findings file contains draft-call evidence, no phase-2a rows. Live PR state and other sessions were not read within this runner's boundary.

## Verification

```sh
.venv/bin/python3 -m ruff check scripts/stage2.py tests/test_stage2.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py tests/test_stage2.py
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'prompts_cover_a_fault_that_raises or implement_prompt_covers_a_fault_that_raises or red_first_accepts_only_clean_assertion_runs or red_first_accepts_pytest_failed_call_outcomes or red_first_refuses_non_assertion_call_failures or red_first_refuses_setup_and_teardown_errors or red_first_refuses_non_proving_pytest_outcomes or red_first_refuses_missing_or_invalid_evidence'
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_implement_prompt_covers_a_fault_that_raises — missing or reversed guidance on the implement surface passes unnoticed
- 2: not yet written tests/test_stage2.py::test_repair_prompts_cover_a_fault_that_raises — either repair variant loses the specific catch, assert or pytest.fail guidance
- 3: tests/test_stage2.py::test_red_first_accepts_only_clean_assertion_runs — qualifying assertion proof is refused
- 3: tests/test_stage2.py::test_red_first_accepts_pytest_failed_call_outcomes — qualifying pytest failed-outcome proof is refused
- 3: tests/test_stage2.py::test_red_first_refuses_non_assertion_call_failures — an unrelated exception qualifies
- 3: tests/test_stage2.py::test_red_first_refuses_setup_and_teardown_errors — setup or teardown failure qualifies
- 3: tests/test_stage2.py::test_red_first_refuses_non_proving_pytest_outcomes — a skipped or incomplete run qualifies
- 3: tests/test_stage2.py::test_red_first_refuses_missing_or_invalid_evidence — missing or malformed proof qualifies

## Time used
