---
title: "Plan — address-drift-warning"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-x2g9
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, opencode-go, address]
---

# Plan — address-drift-warning

```text
For you:     Go catalog address differences are visible, including an unrecorded API, while existing admission rules keep applying.
Done when:   Offline regressions prove the missing API warning, its audit trail and unchanged admission; make verify is green.
Appetite:    2 hours of phase 4, repairs included; stop at the limit.
Not now:     Address-record updates, new API admission or consolidation of repeated warnings.
Pre-mortem:  suppose it failed: most likely because eligibility filtering hides the API warning before evidence is collected.
Starts unless you say stop.
```

## Files and steps

1. **Implementer — `tests/test_stage2_go_access.py`:** add the ledger's
   not-yet-written tests using its synthetic records, `row`, `bridge_with`,
   `Harness` and session fixtures; first show the API-warning tests red.
   Cover a single declared API and several mappings, an unrecorded API on
   an explicit admitted base, and an unmeasured research row retaining its
   exclusion reason. Assert values and outcomes rather than exact prose.
2. **Implementer — `scripts/stage2_go.py`:** extend `assess`'s existing
   admitted/no-recorded-path branch to return a notice for a non-empty
   unrecorded API, naming the model, observed API and sorted declared API
   names. Preserve `definition`, `problem`, defaults and mapped-path logic;
   do not guess a baseline path. Safely describe unreadable API strings
   without echoing control characters. Update the Assessment/assess comments
   that currently describe only path notices.
3. **Implementer — `scripts/stage2_swarm.py`:** collect shared-policy notices
   for structurally valid, address-admissible catalog rows before eligibility
   filtering; retain each model's notice once in `address_notices`, including
   a row excluded as `wire-api-not-measured`. Keep all reasons and selected
   IDs unchanged. Update its path-only notice comment; use the resolved
   definition rather than turning an absent base into explicit null.
4. **Implementer:** verify API notices through existing consumers without
   changing them: review stderr and round evidence, probe audit, research
   launch lines and session pending audit. A notice alone must neither
   prevent a permitted synthetic send nor permit a refused one. If a caller
   needs production changes beyond the two modules above, stop and report
   the gap rather than silently extending the file list.
5. **Implementer — `plans/changes/address-drift-warning/plan.md`:** replace
   not-yet-written ledger markers as the tests appear and record actual
   phase-4 time under Time used; **`spec.md`** updates implementation status
   only, without changing criteria or class.
6. **Runner/orchestrator — `plans/changes/address-drift-warning/findings.md`:**
   retain verification and review evidence; **`research.md`** retains the
   repository gap check; **`plans/INDEX.md`** is regenerated after artifact
   metadata changes. No paths are deleted; no held-path bootstrap is needed.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2_go_access.py tests/test_stage2_swarm.py tests/test_stage2_availability.py tests/test_stage2_session_policy.py
python3 scripts/check_interview_minimums.py --change address-drift-warning
python3 scripts/check_criterion_ledger.py
make verify
```

Use synthetic catalog/transport fixtures only; compare the new warning tests
against the unchanged production implementation before step 2. The runner
regenerates the index before its full verification. The prompt's
`scripts/validate_change_artefacts.py` and a plan template do not exist at
`a40f22e5`; do not introduce either as part of this change.

## Criterion ledger

- 1: tests/test_stage2_go_access.py::test_same_host_path_moves_run_with_notice — a same-host move loses its model or either path
- 2: tests/test_stage2_go_access.py::test_unrecorded_api_warns_without_changing_definition — the explicit same-host unrecorded API stays silent or borrows another API's base
- 3: tests/test_stage2_go_access.py::test_catalog_drift_notices_survive_eligibility_filters — review preparation loses a notice or research omits the excluded API row's notice
- 4: tests/test_stage2_go_access.py::test_api_notices_reach_launch_evidence — review-round, probe or research-launch evidence loses the API notice
- 4: tests/test_stage2_go_access.py::test_session_records_unrecorded_api_notice — the initial session audit loses its API notice
- 5: tests/test_stage2_go_access.py::test_matching_recorded_addresses_do_not_warn — equivalent/defaulted bases or a second mapped API invent drift
- 6: tests/test_stage2_go_access.py::test_unrecorded_api_warns_without_changing_definition — the warning drops or changes the effective API/base
- 6: tests/test_stage2_go_access.py::test_unsafe_destinations_are_refused_before_any_send — a warning admits an unsafe destination
- 6: tests/test_stage2_go_access.py::test_absent_bases_get_the_recorded_api_default — a missing base guesses an unmapped API default
- 6: tests/test_stage2_go_access.py::test_admission_preserves_the_other_restrictions — address notice bypasses terms or measured-API exclusion
- 7: tests/test_stage2_go_access.py::test_api_notices_sanitise_untrusted_values — control-bearing API text leaks into diagnostics
- 7: tests/test_stage2_go_access.py::test_notices_are_kept_and_sanitised — credential-bearing URL text leaks into diagnostics

## Do not touch

No design or ADR: the approved class is bounded. No endpoint record, held
paths, Pi installation, wire-API measurement, receipt/state schema, terms,
selection policy or predecessor artifacts. Existing caller modules
`scripts/stage2.py`, `scripts/stage2_availability.py` and
`scripts/stage2_session.py` consume the shared notice unchanged.
Explore used Stage 2 Flash (`glm-5.3-flash`, `glm-coding-plan`, 2026-11-07);
no Stage-1 fallback is recorded in research.

## Time used

2026-11-08 10:43:13–12:04:40 UTC, 4887 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
