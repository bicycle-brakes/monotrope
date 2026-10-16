---
title: "Plan — guard-test"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-0ho
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, repair, guard-test]
---

# Plan — guard-test

```text
For you:     Test-only repairs can use a guard test with runner-checked failure and success.
Done when:   Authorised guard proofs and statuses are tested, every guard test has mandatory review, the fault-switch gate works locally and in CI, and make verify is green.
Appetite:    2 hours of phase 4, including repairs; stop at the limit.
Not now:     Runner-generated faults, proof-free exceptions, old-record migration or model routing changes.
Pre-mortem:  suppose it failed: most likely because the fault switch reaches both runs.
Starts unless you say stop.
```

## Prerequisite

The five human answers are recorded as of 2026-10-16; the interview check is
green at `a2a58e8`. Run it again with the ADR edit present. The recorded
`bounded` class requires neither design nor a new ADR. The existing findings
file has audit lines only, with no phase-2a rows to resolve at this baseline.
The planned ADR addendum makes the implementation PR a decision PR; its
merge remains the maintainer's confirmation.

## Changes

1. `tests/test_stage2.py`: add the ledger's guard cases first, using the existing temporary `World`, `repair_world` and scripted repairs, with an actual local pytest guard that conditionally disables a baseline checker and asserts that the checker rejects seeded invalid input; verify each ledger fault, not only today's green case.
2. `scripts/stage2.py`: extend `fixed_status` with the exact `guard test — ` prefix while reusing all `FIXED_TEST` and path checks; in `check_repair_answer`, separate proof kind from test reference, extract the named top-level function's source (AST source span) for the switch check, and require the original Status to match `taken — guard test — <nonempty reason>` before dispatching a guard answer to the two-run proof; ordinary and not-a-test answers retain their existing rules.
3. In the same `scripts/stage2.py`, extend `red_first` with an optional guard mode that defaults off for current callers, sharing baseline checkout, copied tests, pytest startup probe, timeout, ref checks and cleanup; run planted first (exit 1) then unplanted (exit 0), with `STAGE2_PLANT_FAULT` explicitly removed from both environments before setting it only for the first invocation, and report the row, mode and exit/error on failure.
4. In the same `scripts/stage2.py`, teach `REPAIR_ANSWER` (shared by both repair routes) both guard forms, orchestrator authorisation, retained planting branch and mandatory per-test semantic review; add the taken form to `RECORD_INTRO`; in `phase_prompt` use a phase-6-only answer-format variant allowing one `Guard test: <test> — fault: <fault> — detects without switch: <yes/no and reason>` line per test alongside finding rows, instead of the contradictory rows-only rule; preserve these lines through existing `parse_rows`/`answer_block` passthrough; keep `mark_repaired_findings` and `mark_repaired_record` generic unless the new integration tests expose a loss of the full fixed status.
5. `templates/findings.md`: add both `taken — guard test — <reason>` and `fixed — guard test — tests/<path>::<function>` beside the existing Status vocabulary, explaining authorisation, two-run proof and mandatory per-test review.
6. `prompts/04-implement.md`: describe the marked guard alternative, the literal switch in the named test, required exits and phase-6 inspection alongside ordinary red first.
7. `prompts/04b-review-loop.md`: add the orchestrator-only taken guard form and reason requirement; `prompts/06-review.md`: require one line per guard test naming its real planted fault and detection assessment, and a BLOCKER for a bare conditional failure, using the evidence-line format outside finding rows and verdict lines; identify guard tests from the changed tests and their switch branches before the verdict, preserving the private-loop blindness rule.
8. `docs/WORKFLOW.md`: update the evidence rule, repair section and `Broke a test` explanation to distinguish the two proof modes without counting the new proof as an existing broken test; state repair-only scope, retained branches, mandatory review and the environment gate.
9. `docs/adr/0017-codex-repairs-taken-findings.md`: append the agreed dated detail clarifying the guard proof and statuses, proposed until merge, leaving the original decision body intact; this is an existing ADR edit, not a new draft.
10. `scripts/check_guard_environment.py` (new): a standalone gate exits 1 with the switch named whenever `STAGE2_PLANT_FAULT` exists in its environment (including empty/`0`), otherwise 0; it never changes the environment or repository.
11. `tests/test_guard_environment.py` (new): exercise the gate as a subprocess with absent, empty, `0` and `1` values, and verify its gate declaration is blocking in both placements; name the seeded red case `test_guard_environment_gate_goes_red_when_switch_is_set` and reference its script so the existing gate-mutation coverage recognises it.
12. `decisions/gates.yaml`: register `guard-environment`, command `python3 scripts/check_guard_environment.py`, job `verify`, enforcement `block`, placement `both`, floor `false`, no tracker dependency; regenerate `.github/workflows/ci.yml` with `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`, never hand-edit it.
13. `plans/changes/guard-test/plan.md`: fill `Time used` only during phase 4; runner-owned bookkeeping may refresh metadata in `plans/changes/guard-test/spec.md` and `plans/changes/guard-test/research.md`, append audit/check evidence to `plans/changes/guard-test/findings.md`, and regenerate `plans/INDEX.md`.

## Verification

Run `.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'guard or red_first or fixed_line or passing_repair or failed_repair or findings_template or prompts_name_the_repair'` first against the new tests and old runner (red), then against the implementation (green).
Run `.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_guard_environment.py tests/test_ci.py`, `python3 scripts/check_criterion_ledger.py`, `python3 scripts/check_interview_minimums.py --change guard-test`, `python3 scripts/ci_gates.py --check-schema`, `python3 scripts/ci_gates.py --check-ci` and `make verify` after the repair and doctrine changes.
For the new proof, test actual subprocess behavior over baseline code: both-required-exit combinations, absent ambient switch, missing-switch source, missing pytest, failed launch/timeout in either stage, refs created/moved, and failed cleanup; ordinary regressions keep their current proof requirements.
Record the refuting faults and measured phase-4 time below; remove `not yet written` from ledger entries as their functions are added.
Keep a real sample guard's planting branch through checkpoint and rerun its two modes; test guard refusal for ordinary taken rows, text-only rows and missing reasons. Exercise the environment gate with a clean child environment and each present value; do not export the switch into normal verification. Check the gate appears in both local commands and generated CI.
Phase 6 reads every guard test and records the fault and detection assessment per test, treating switch-only failure without a real fault as BLOCKER; review also checks all named documentary files and protected areas in the diff.
Explore used Stage 2, `glm-coding-plan` / `glm-5.3-flash`, on 2026-10-15; there is no Stage-1 Explore fallback to carry forward.
The requested `python3 scripts/validate_change_artefacts.py --check` cannot run at `a2a58e8`: that script is absent; do not add it here. There is also no `templates/plan.md`; this plan follows `prompts/03-plan.md` and the existing bounded plans.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_a_guard_fixed_line_selects_guard_proof — the valid prefix is rejected or ordinary red-first is selected.
- 2: not yet written tests/test_stage2.py::test_a_guard_reference_requires_a_safe_defined_test_and_its_switch — malformed, climbing or undefined references, or a switch only in another function, are accepted.
- 3: not yet written tests/test_stage2.py::test_a_guard_planted_run_requires_exit_one_on_baseline_code — planted exit 0, 2 or other non-1 is accepted, or repaired production is copied into the proof.
- 4: not yet written tests/test_stage2.py::test_a_guard_requires_an_unplanted_green_run_without_an_ambient_switch — second run missing, nonzero accepted, or ambient switch inherited.
- 5: not yet written tests/test_stage2.py::test_guard_startup_and_timeouts_fail_with_the_stage_named — missing pytest, failed launch or timeout in either mode passes or lacks the stage diagnostic.
- 6: not yet written tests/test_stage2.py::test_guard_proofs_preserve_refs_and_clean_up_the_checkout — success/failure leaks a checkout, created/moved refs go unnoticed, a neighbour ref is deleted, or failed removal is hidden.
- 7: not yet written tests/test_stage2.py::test_guard_statuses_survive_all_three_row_locations_only_after_success — status is stripped, failed evidence writes fixed, unrelated cells change, or fixed guard rows are repaired again.
- 8: tests/test_stage2.py::test_a_named_test_that_is_not_red_first_fails_the_attempt — unmarked baseline-green proof passes.
- 8: tests/test_stage2.py::test_a_text_row_taken_as_not_a_test_is_repaired_and_its_status_written — a correctly authorised text row is rejected.
- 8: not yet written tests/test_stage2.py::test_ordinary_proofs_and_not_a_test_permissions_do_not_change_with_guard_support — ordinary exit 2 stops counting as red or a code row can answer not a test.
- 9: not yet written tests/test_stage2.py::test_both_repair_prompts_explain_the_guard_proof_and_its_limit — either route omits the mark, switch, dual proof or semantic-review limit.
- 9: not yet written tests/test_stage2.py::test_guard_doctrine_goes_red_when_authorisation_or_review_rules_are_missing — delete either status, mandatory review, retention or repair-only scope from the named operative texts and the doctrine test must fail.
- 10: not yet written tests/test_stage2.py::test_a_guard_answer_refuses_rows_without_the_orchestrators_guard_mark — an ordinary taken row, a not-a-test row or an empty guard reason bypasses ordinary proof.
- 11: not yet written tests/test_stage2.py::test_the_review_prompt_requires_every_guard_fault_and_rejects_conditional_failure — deleting the per-test fault/detection requirement or BLOCKER rule passes the prompt check.
- 11: not yet written tests/test_stage2.py::test_phase6_keeps_a_guard_evidence_line_per_test_with_or_without_findings — two guard evidence lines disappear from findings.md, the effective prompt still says rows only, or private loop rows reach the pre-verdict call.
- 11: not a test — phase-6 review records one line per guard test with its real fault and detection assessment; an omitted test or accepted bare conditional failure refutes it.
- 12: not yet written tests/test_guard_environment.py::test_guard_environment_gate_goes_red_when_switch_is_set — absent, empty, 0 and 1 cases expose inverted or truthiness-based checks.
- 12: not yet written tests/test_guard_environment.py::test_guard_environment_gate_is_blocking_locally_and_in_generated_ci — removing the gate, changing enforcement or placement, or omitting it from either command list or generated workflow is detected.
- 13: not yet written tests/test_stage2.py::test_a_checkpointed_guard_keeps_its_repeatable_planting_branch — the saved test loses its planting branch or cannot repeat red with the switch and green without.

## Do not touch

Keep criterion-ledger grammar, interview rules, adoption dates, human answers,
endpoint declarations, model routes, historical findings and existing guard
tests unchanged. Keep phase-4 and criterion-ledger evidence rules unchanged;
the new taken-row spelling belongs only to repair triage. No edits to the
Makefile, verify runner or gate generator are needed: both verification paths
already consume the one gate list.

## Time used
