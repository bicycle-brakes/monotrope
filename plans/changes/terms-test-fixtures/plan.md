---
title: "Plan — terms-test-fixtures"
status: draft
implementation_status: none
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-hxkw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, tests, model-terms]
---

# Plan — terms-test-fixtures

```text
For you:     Shared synthetic terms prevent fixture drift, and the process-kill test keeps its evidence under parallel load.
Done when:   The shared builder passes production admission, deliberate refusals still hold, and three consecutive full make verify runs pass.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Production rules, real terms, runner gates, general fixture consolidation or other timing tests.
Pre-mortem:  suppose it failed: most likely because shared defaults conceal an intentionally missing field.
Starts unless you say stop.
```

Baseline `454790ae`, inspected 2026-10-27. Bounded: no design or ADR.
Explore used Stage 2, GLM 5.3 Flash via `glm-coding-plan`; no Stage-1 fallback
is recorded. No plan template exists; this follows `prompts/03-plan.md`.

## Files and steps

1. Create `tests/terms_fixtures.py`: `admissible_terms(**overrides)` returns a
   fresh dictionary with synthetic ISO reading/expiry strings, source,
   retention and `training: "Not used"`; use expiry `2099-01-01`, no default
   cost or skip. Apply overrides last without repairing invalid values.
   Import as `from terms_fixtures import admissible_terms`, like existing
   cross-test imports; no package or pytest configuration change.
2. Create `tests/test_terms_fixtures.py`: add the ledger's production-contract
   and independence tests, pinning `stage2.terms_today` to 2026-10-27; exercise
   YAML round-trip too, so dates remain strings. Prove the contract test
   fails when a required default such as `valid_until` is removed temporarily;
   restore it before verification and record the measured result.
3. Change `tests/test_stage2.py`: migrate `pin_entry`, `pin_the_ladder` and
   admissible unit-record baselines; keep ladder cost/order overrides.
   Negative date/retention cases start from the builder then explicitly
   remove or replace the targeted field, preserving missing-field cases.
4. Change `tests/test_stage2_terms_expiry.py`: retain `a_record`'s entry wrapper
   but delegate its record and `entry_with` to the builder; keep intentional
   invalid records, explicit dates and UTC clock controls. In migrated negative
   cases here and in `test_stage2.py`, assert the intended refusal reason as
   well as refusal, so another missing field cannot mask the tested boundary.
5. Change `tests/test_stage2_session.py`: use the builder in `World.declare_go`
   without overriding explicitly supplied `modelle_terms` or adding cost.
6. Change `tests/test_stage2_swarm.py`: replace copied live seat terms with
   synthetic builder records, preserving only explicitly needed cost metadata;
   do not inherit live expiry, training or skip markers into normal fixtures.
7. Change `tests/test_stage2_research_availability.py`: keep `terms_record`'s
   cost/extra-field behavior but obtain required fields from the builder;
   `None` cost must still omit cost metadata, and overrides remain last.
8. Change `tests/test_pi_contract.py`: build contract-model terms through the
   helper, retaining local stand-ins and loopback-only transport coverage.
9. Change `tests/test_stage2_research_store.py`: keep the pipe-buffer regression;
   make the kill test wait for durable first-result and second-launch records
   instead of readiness on two pipe reads. Keep a bounded diagnostic timeout,
   check driver exit while waiting, hold the second child on the existing
   release file, and always kill/reap the driver and release the child in
   cleanup. Keep real SIGKILL and all outcome/report/interrupted assertions.
   Audit precedes launch: require the audit, not an extra child-start guarantee.
10. Update this folder's `plan.md` as tests land (remove `not yet written`)
    and `findings.md` with contract-fault evidence and all three full-run
    results/durations. No phase-2a rows were present at drafting. The runner
    records measured phase-4 time below and refreshes `plans/INDEX.md`.

Prior draft verification failed on tracker/artifact drift outside this
package and a missing decisions header; one run hit the runner's step limit
(`findings.md`, attempts 1–3). At `454790ae` the decisions header is present;
its current-header and interview checks pass. Tracker drift has not been
remeasured here, and full verification remains the runner's next check.
Report remaining blockers without repairing other changes or the shared
tracker; a red or stopped run is not completion evidence.

## Criterion ledger

- 1: not a test — phase-6 source review checks all six suites' normal builders delegate to the shared helper; any duplicate required-field baseline refutes it.
- 2: not yet written tests/test_terms_fixtures.py::test_default_terms_pass_production_admission — removing a required default or producing a YAML-native expiry causes refusal.
- 3: not yet written tests/test_terms_fixtures.py::test_terms_overrides_and_mutations_are_isolated — one call's overrides or deletion alter a later call's defaults.
- 4: tests/test_stage2.py::test_terms_problem_requires_an_iso_reading_date — a malformed reading is admitted or a valid reading refused.
- 4: tests/test_stage2.py::test_paid_terms_require_a_retention_reading — a missing/unreadable retention field is admitted.
- 4: tests/test_stage2_terms_expiry.py::test_paid_terms_require_a_usable_expiry — a missing/malformed expiry is admitted.
- 4: tests/test_stage2_terms_expiry.py::test_expiry_preserves_prior_admission_guards — defaults hide a skip, training or retention refusal.
- 4: tests/test_stage2_research_availability.py::test_a_model_without_admitted_terms_or_cost_is_never_used — a missing-cost or unadmitted candidate is called.
- 5: tests/test_stage2_research_store.py::test_terminal_record_survives_sigkill_after_the_outcome — SIGKILL loses the first result or completes the second slot.
- 6: tests/test_stage2_research_store.py::test_terminal_record_survives_sigkill_after_the_outcome — readiness times out under the normal parallel verification run.

## Verification and boundaries

Run the following command three times consecutively with normal parallelism:

```bash
make verify
```

Use this checkout's pinned environment and Pi installation; if not initialized,
the orchestrator first runs `make venv` and `bash tools/pi/install.sh`.
For the historical flake, repeated full-run evidence replaces a forced red
reproduction (`decisions.md`); do not weaken the runner to obtain it.
Stop at the appetite or a runner refusal and report the evidence/blocker.

Do not edit `tests/test_stage2_availability.py` (it already consumes the shared
world) or `tests/test_model_endpoints.py` (live-declaration and partial-cost
checks). The full suite covers both. Do not edit production, governance,
parallelism, other changes or the living spec; no other files are deleted.
`scripts/validate_change_artefacts.py` is absent: report it as unavailable,
never as a passing check. Index preparation and commits belong to the runner.

## Time used
