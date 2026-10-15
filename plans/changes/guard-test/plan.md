---
title: "Plan — guard-test"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
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
Done when:   Both guard runs, preserved ordinary proofs and status handling are tested, the repair texts agree, and make verify is green.
Appetite:    2 hours of phase 4, including repairs; stop at the limit.
Not now:     Runner-generated faults, proof-free exceptions, old-record migration or model routing changes.
Pre-mortem:  suppose it failed: most likely because the fault switch reaches both runs.
Starts unless you say stop.
```

## Prerequisite

Return to phase 1a before phase 4: the planned ADR 0017 addendum owes five
human answers, but only Q-1 is recorded as of 2026-10-15. Do not invent
answers, skip the ADR claim, or start implementation on the strength of a
draft-only green gate. Once the interview is complete, run
`python3 scripts/check_interview_minimums.py --change guard-test` before
implementation and again with the ADR edit present. No design or new ADR
is due for this bounded change. There are no phase-2a rows in the existing
findings file to resolve at this drafting baseline (`a4b0780`).

## Changes

1. `tests/test_stage2.py`: add the ledger's guard cases first, using the existing temporary `World`, `repair_world` and scripted repairs, with an actual local pytest guard that conditionally changes a checked value and asserts the correct value, rather than an unconditional switch-triggered failure.
2. `scripts/stage2.py`: extend `fixed_status` with the exact `guard test — ` prefix while reusing all `FIXED_TEST` and path checks; in `check_repair_answer`, separate proof kind from test reference, extract the named top-level function's source (AST source span) for the switch check, and dispatch only marked rows to the two-run proof.
3. In the same `scripts/stage2.py`, extend `red_first` with an optional guard mode that defaults off for current callers, sharing baseline checkout, copied tests, pytest startup probe, timeout, ref checks and cleanup; run planted first (exit 1) then unplanted (exit 0), with `STAGE2_PLANT_FAULT` explicitly removed from both environments before setting it only for the first invocation, and report the row, mode and exit/error on failure.
4. In the same `scripts/stage2.py`, teach `REPAIR_ANSWER` (shared by both repair routes) the guard spelling and semantic review limit; keep `mark_repaired_findings` and `mark_repaired_record` generic unless the new integration tests expose a loss of the full fixed status.
5. `templates/findings.md`: add the fixed guard form and its two-run proof and review limit beside the existing Status vocabulary; keep taken forms unchanged.
6. `prompts/04-implement.md`: describe the marked guard alternative, the literal switch in the named test, required exits and phase-6 inspection alongside ordinary red first.
7. `docs/WORKFLOW.md`: update the evidence rule, repair section and `Broke a test` explanation to distinguish the two proof modes without counting the new proof as an existing broken test.
8. `docs/adr/0017-codex-repairs-taken-findings.md`: after the interview prerequisite, append the agreed dated detail clarifying the guard proof and statuses, proposed until merge, leaving the original decision body intact; this is an existing ADR edit, not a new draft.
9. `plans/changes/guard-test/plan.md`: fill `Time used` only during phase 4; runner-owned bookkeeping may refresh metadata in `plans/changes/guard-test/spec.md` and `plans/changes/guard-test/research.md`, append audit/check evidence to `plans/changes/guard-test/findings.md`, and regenerate `plans/INDEX.md`.

## Verification

After the prerequisite, run `.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'guard or red_first or fixed_line or passing_repair or failed_repair or findings_template or prompts_name_the_repair'` first against the new tests and old runner (red), then against the implementation (green).
Run `.venv/bin/python3 -m pytest -q tests/test_stage2.py`, `python3 scripts/check_criterion_ledger.py`, `python3 scripts/check_interview_minimums.py --change guard-test` and `make verify` after the repair and doctrine changes.
For the new proof, test actual subprocess behavior over baseline code: both-required-exit combinations, absent ambient switch, missing-switch source, missing pytest, failed launch/timeout in either stage, refs created/moved, and failed cleanup; ordinary regressions keep their current proof requirements.
Record the refuting faults and measured phase-4 time below; remove `not yet written` from ledger entries as their functions are added.
Phase 6 reads the sample guard's mutation and rejects a switch-only failure without a real fault; review also checks the four documentary files and protected areas in the diff.
Explore used Stage 2, `glm-coding-plan` / `glm-5.3-flash`, on 2026-10-15; there is no Stage-1 Explore fallback to carry forward.
The requested `python3 scripts/validate_change_artefacts.py --check` cannot run at `a4b0780`: that script is absent; do not add it here. There is also no `templates/plan.md`; this plan follows `prompts/03-plan.md` and the existing bounded plans.

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
- 9: not a test — phase-6 review checks templates/findings.md, prompts/04-implement.md, docs/WORKFLOW.md and the ADR 0017 addendum against criterion 9; a missing form/run or a claim of semantic proof refutes it.

## Do not touch

Keep criterion-ledger grammar, interview rules, adoption dates, human answers,
endpoint declarations, model routes, historical findings and existing guard
tests unchanged. No changes to `prompts/04b-review-loop.md` are needed:
taken-row grammar and the orchestrator's selection remain unchanged.

## Time used
