---
title: "Plan — verify-cheap-first"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, model: gpt-6.1-sol, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, make-verify, gates]
---

# Plan — verify-cheap-first

```text
For you:     Local verification catches cheap failures before expensive gates, including in kit adopters, and names what did not run.
Done when:   Planted cheap failures stop before pytest, green runs execute every selected gate, CI remains exhaustive, and make verify is green.
Appetite:    3 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Faster tests, caching, admission changes, fewer gates, or migrating other repositories.
Pre-mortem:  suppose it failed: most likely because schema activation reached the reader before the held gate list.
Starts unless you say stop.
```

## Build sequence and files

1. Attempt: change `scripts/ci_gates.py` to validate required `cost: seconds|minutes` under schema 3, expose cost in normalized records, JSON and the generated catalogue, and derive a stable cost order only for `--commands --placement lokal`; keep `gates()`, CI generation and other output in declaration order. No gate-id scheduling list. During bootstrap preparation only, dispatch by declared schema: v3 exercises the new rules; v2 remains readable with its existing catalogue rendering and declaration order. This lets the attempt test real v3 reader/runner code on synthetic lists without breaking the untouched held v2 list or its committed catalogue. Remove the entire v2 compatibility branch in step 4; it never ships.
2. Attempt: change `scripts/verify_all.sh` to stop executing after the first local blocking failure, collect the remaining selected IDs from the already obtained TSV, and print one explicit not-run summary outside gate frames; finish timing and return red normally. `--ci` continues through all gates. Keep admission, interpreter choice, list-generation errors, existing frames and nonblocking behavior intact.
3. Attempt: create `tests/test_verify_cheap_first.py` with synthetic schema-3 lists and copied runner/reader fixtures exercising the prepared version-3 entry point; use marker commands instead of pytest, network gates or the full suite. Add cost-schema, mixed-order/tie, docs/drift/placement, local red/green/nonblocking, CI-mode, parser/history and kit-transfer proofs. Keep these independent of the pending real gate-list edit. Update `tests/test_ci.py`'s worker-verdict and timing-enforcement regressions to expect local early stop, while retaining their other assertions and existing exhaustive-CI tests. Define the final repository-activation test there with an explicit bootstrap-only skip; only the orchestrator removes it in step 4.
4. Orchestrator bootstrap, after the accepted attempt: change held `decisions/gates.yaml` to schema 3 and add `cost` to every gate (`pytest` and `leerprobe`: `minutes`; all other current entries: `seconds`); document the field and replace pytest's obsolete runs-first reason. In `scripts/ci_gates.py`, activate strict schema 3 and remove all temporary version-2 compatibility. In `tests/test_ci.py` and `tests/test_gate_machinery.py`, migrate synthetic gate-list fixtures to schema 3 with explicit costs and remove the bootstrap-only skip. Never weaken schema enforcement to accept the old list as the final behavior.
5. Orchestrator: regenerate held `.github/workflows/ci.yml` with `python3 scripts/ci_gates.py --generate-ci` (write stdout to that file, even if identical); replace only the generated inventory of `docs/governance/gate-catalog.md` with `python3 scripts/ci_gates.py --catalog` output and explain cost classes in its prose. Change `tests/test_gate_catalog.py` to check the extra cost column independently, and migrate its synthetic normalized records as needed. All enforcement, membership, commands and CI always-run behavior stay intact.
6. Attempt/orchestrator: run the commands below at the appropriate boundary, record real red/green results and complete the transferred-kit smoke proof. New tests that depend on real schema activation stay bootstrap-skipped until step 4; synthetic proofs run before acceptance. The final full check must run after bootstrap even if the attempt passed before it. An expected v2/v3 mismatch is a bootstrap dependency, not a reason to edit held files in a retry.

Implementation status updates belong in `plans/changes/verify-cheap-first/spec.md` and `plans/changes/verify-cheap-first/plan.md`; remove each ledger's `not yet written` marker when its function is defined. The runner owns measured entries under Time used, evidence in `plans/changes/verify-cheap-first/findings.md`, and regeneration of `plans/INDEX.md`. No deletions, design file or ADR draft.

## Verification

The new test file uses actual copied reader/runner code and isolated duration/admission state. Put a failing seconds gate after a minutes gate in input order; assert markers, exact selected skip IDs, exit code, `red_sections` diagnostics and red history with no skipped-gate events. Parameterize both nonblocking levels, all local jobs and `--ci`. Exercise malformed costs and old schemas independently of unrelated schema errors. The bootstrap-only test checks the real list's version/cost assignments and strict rejection of a version-2 copy; remove its skip before final verification.

For the kit proof, copy the mechanism files selected by the existing manifest into a temporary recipient with a synthetic version-3 list and renamed gate IDs. Run the transferred runner and assert cheap-first stop behavior without importing source-tree modules. Check the real source gate-list classification in the final activation test. No manifest edit is needed: these files already travel together.

```sh
python3 scripts/check_interview_minimums.py --change verify-cheap-first
.venv/bin/python3 -m ruff check scripts/ci_gates.py tests/test_verify_cheap_first.py tests/test_ci.py tests/test_gate_machinery.py tests/test_gate_catalog.py
.venv/bin/python3 -m ruff format --check scripts/ci_gates.py tests/test_verify_cheap_first.py tests/test_ci.py tests/test_gate_machinery.py tests/test_gate_catalog.py
bash -n scripts/verify_all.sh
.venv/bin/python3 -m pytest tests/test_verify_cheap_first.py tests/test_ci.py tests/test_gate_machinery.py tests/test_gate_catalog.py -q
python3 scripts/ci_gates.py --check-schema
python3 scripts/ci_gates.py --check-ci
python3 scripts/check_criterion_ledger.py
make verify
```

The schema/CI checks above and final full check follow step 5. Before acceptance, run the synthetic tests and existing regressions against the still-readable v2 list; do not treat bootstrap skips as final evidence. Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash`; no Stage-1 fallback was recorded. At `a764f4c4` (2026-11-10), `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent: follow the phase-3 prompt and use the existing interview, registry and ledger checks. Findings currently contain call evidence only, no open phase-2a rows. Live PR state and other interactive sessions were not read within this runner's worktree-only boundary.

## Criterion ledger

- 1: not yet written tests/test_verify_cheap_first.py::test_cost_schema_rejects_missing_and_invalid_costs — invalid costs on any gate kind pass validation
- 1: not yet written tests/test_ci.py::test_repository_gate_schema_is_v3 — the final reader accepts v2 or the real list has not migrated
- 2: not yet written tests/test_verify_cheap_first.py::test_local_cost_order_preserves_selection_and_ties — declaration position defeats cost order or filtering changes
- 3: not yet written tests/test_verify_cheap_first.py::test_local_blocking_failure_stops_before_pytest — an expensive marker runs after cheap red or exit is zero
- 4: not yet written tests/test_verify_cheap_first.py::test_skip_summary_names_only_unexecuted_selected_gates — missing or false skip IDs, or skipped gates shown as passed
- 5: not yet written tests/test_verify_cheap_first.py::test_green_run_executes_every_selected_gate_once — a selected gate is omitted or repeated
- 5: not yet written tests/test_verify_cheap_first.py::test_unusable_gate_selection_never_reports_green — failed or empty command generation produces a green verdict
- 6: not yet written tests/test_verify_cheap_first.py::test_nonblocking_failures_continue_without_red_verdict — report/advisory failure stops execution or changes exit status
- 7: not yet written tests/test_verify_cheap_first.py::test_ci_mode_continues_after_blocking_failure — --ci loses a later selected gate
- 7: tests/test_ci.py::test_every_gate_step_runs_even_after_a_failing_gate — hosted gate steps lose always-run conditions
- 7: tests/test_ci.py::test_every_step_after_a_failing_gate_still_runs — hosted execution or matrix enforcement stops early
- 8: not yet written tests/test_verify_cheap_first.py::test_early_stop_preserves_repair_diagnostics — the parser loses the failed command/diagnostic or invents a skipped section
- 9: not yet written tests/test_verify_cheap_first.py::test_early_stop_history_records_only_executed_gates — history fabricates a skipped event or omits the red run end
- 9: tests/test_ci.py::test_duration_storage_failure_warns_without_changing_verdict — broken measurement storage changes enforcement
- 10: not yet written tests/test_ci.py::test_repository_gate_schema_is_v3 — real gates have incorrect cost assignments or the obsolete pytest-order claim
- 10: not yet written tests/test_verify_cheap_first.py::test_catalog_exposes_declared_costs — catalogue omits or misstates a declared cost
- 11: not yet written tests/test_verify_cheap_first.py::test_transferred_kit_stops_before_expensive_gate — transferred dependencies or renamed gate IDs break cheap-first stopping

## Limits and ownership

No changes to `scripts/stage2.py`, `scripts/verify_lock.py`, `scripts/verify_duration.py`, `scripts/kit/manifest.yaml`, other change folders, ADRs, prompts or model routes. The existing evidence parser is exercised as a consumer, not rewritten. No external service call is part of the new proofs. The orchestrator presents the card unchanged and owns the decision pull request for the held gate-list edit; this drafting attempt neither implements nor commits it.

## Time used
