---
title: "Plan — research-free-paid"
status: draft
implementation_status: none
date: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-wb40
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, free-selection, research-swarm]
---

# Plan — research-free-paid

```text
For you:     Both swarms use one free-selection rule, and a Pi catalog move that breaks either preparation fails offline before merge.
Done when:   Both preparations exclude paid free-looking ids before probes, the shared-selection and real-Pi contracts pass, and make verify is green.
Appetite:    4 hours of phase 4, repairs included — a stop, not an estimate.
Not now:     Model admissions, Pi upgrades, catalog sources, paid routing or research/review protocol changes.
Pre-mortem:  suppose it failed: most likely because the offline contract bypasses the production preparation that breaks.
Starts unless you say stop.
```

## Scope and baseline

Implement `spec.md` criteria 1–10 with the shared component shaped in
`design.md`; the instructions below carry everything phase 4 needs from it.
Baseline `58ac347b`, read 2026-11-05: review drops paid/free collisions;
research does not, and its selector has no endpoint admission input. There
are no phase-2a rows in `findings.md` at this cutoff.

Phase 1 used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash` on 2026-11-05 because the swarm is blocked by this fault;
the maintainer grants that one exception (`decisions.md#Q-2`, confirmed by
Q-3). This is not a Stage-1 fallback and grants no future bypass.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at
the baseline: follow the phase-3 prompt and report the unavailable validator.
The maintainer answered "no" to the ADR question on 2026-11-06 (morning question Q-M2), recorded
in `decisions/answers/research-free-paid/adr.yaml` at commit `0baba58f`.
No ADR draft is due. Preserve the recorded answer, including its author and reason.
The earlier missing-answer evidence in `findings.md` predates this record.

## Build sequence and files

1. **Proof first.** Create `tests/test_stage2_free.py` for normalized policy,
   veto, address and cross-caller parity tests. Add the ledger regressions in
   `tests/test_stage2_availability.py` (review preparation/report) and
   `tests/test_stage2_research_availability.py` (research preparation/report
   and stale/forged free membership). Extend
   `tests/test_stage2_research_catalog.py` to pass real admission input and
   retain fresh-source, capability and explicit-include cases. Record the
   research collision's red result before repair; do not weaken existing tests.
2. Create `scripts/stage2_free.py`: pure normalized free-policy selection and
   per-id model veto helper, returning selected ids, drop reasons and address
   notices. Inputs carry provider/model/definition rows, fresh membership,
   suffix/includes/excludes, explicit additive or restrictive include mode,
   paid ids, applicable global exclusions, caller eligibility reasons and
   the loaded Go address policy. Deduplicate plain ids; hard vetoes beat
   includes. Use `stage2_go.assess`, with no new address literals or I/O and
   no import of `stage2` or either caller.
3. Change `scripts/stage2.py`: normalize review's dated policy records and
   framework exclusions; make `discover_free` use the common selector over
   the fresh overlay and parsed listing. Remove duplicated membership logic
   from `select_free` and `free_drops` (thin compatibility wrappers are fine).
   Keep catalog order, activation/launch checks and existing dropped notices.
   Delegate the paid/model veto part of `free_admission_problem` to the
   shared helper, retaining endpoint permission and frozen-membership checks.
4. Change `scripts/stage2_swarm.py`: extend `select_research_catalog` to
   receive paid ids and public-web exclusion evidence, normalize research's
   string policy, and pass Pi/capability eligibility into the shared selector.
   Keep raw parsing, duplicate identity refusal, restrictive explicit includes
   and sorted output; retain structural field validation but delegate
   destination permission to the common Go assessment. Ineligible explicit research includes retain their
   existing error contract; default-policy paid collisions drop normally.
   Its `online_free` invocation check delegates current paid/model vetoes to
   the shared helper before trusting frozen membership; role/data limits stay.
5. Change `scripts/stage2_availability.py`: pass current declaration data
   into research selection, consume the single selected result before free
   probes, and print paid-drop candidate reasons in `research_report` and
   its existing receipt evidence. Do not create a second filter that can
   disagree with the shared result. Keep research's tool/deprecation evidence,
   `N=0`, optional probe failures, paid seat filling and receipt bindings.
6. Change `tests/test_pi_contract.py`: add the mandatory installed-Pi contract
   and its two-path fault proof. Read every shipped Go API group through
   `provider_data`; use the repository's current endpoint declaration in
   scratch roots, without deleting `beam-free` or editing admission/policy
   values to help the contract pass. Serve that shipped catalog through local
   source stand-ins to the production discovery adapters and production
   `prepare_loop`/`prepare_research`. Supply labelled synthetic capability
   evidence and successful probe responses; do not mock selectors, admission
   or complete preparations. Require real pinned Pi version/listing/bridge
   parsing, complete valid receipts and paid-free disjointness. Use a fixed
   test time for dated terms, scratch state/HOME and synthetic keys. Deny
   Python external networking and preload the existing Node network guard;
   unexpected model transport fails. Missing Pi/Node, unreadable installed
   catalog, preparation refusal or malformed receipt fails, never skips.
   Fault-inject each production preparation and the shared-selection bypass
   separately; the same contract assertions must detect every planted fault.
7. Run the commands below, clear `not yet written` only for defined ledger
   tests, and update `plans/changes/research-free-paid/spec.md` implementation
   status and `plans/changes/research-free-paid/plan.md` ledger/time evidence.
   The runner records verification in
   `plans/changes/research-free-paid/findings.md`, regenerates
   `plans/INDEX.md`, stamps derived dates and commits the accepted attempt.

No files are deleted. No held-path bootstrap edit is needed: all source and
test edits above belong to the implementation attempt; the runner owns the
derived index. Do not edit `model-endpoints.yaml`, `scripts/stage2_go.py`,
the Pi manifest/lock/install, `tests/pi_contract_driver.mjs`,
`tests/pi_network_guard.mjs`, doctrine, ADRs, other change folders,
`research.md`, `decisions.md`, governance, prompts, templates, agent/CI
configuration or tracker. If a held-path edit proves necessary, return it to
the orchestrator as a bootstrap edit after the accepted attempt. Stop at the
four-hour appetite or evidence that broader protocol repair is required.

## Verification

From the worktree root, with the installed pinned Pi and locked Python
environment already prepared (`make venv` and `bash tools/pi/install.sh`
are checkout prerequisites, not changes to their pins):

```sh
.venv/bin/python3 -m pytest tests/test_stage2_free.py tests/test_stage2_availability.py tests/test_stage2_research_catalog.py tests/test_stage2_research_availability.py tests/test_pi_contract.py -q
python3 scripts/check_interview_minimums.py --change research-free-paid
python3 scripts/check_research_handoff.py --change research-free-paid
python3 scripts/check_criterion_ledger.py
make verify
```

All model outcomes are synthetic; never run a live prepare/probe to qualify
this change. The offline shipped-catalog contract deliberately supplies a
fresh-response fixture; production must still force a live refresh and
must never fall back to the shipped baseline. Full verification belongs to
the runner; no validator success or implementation result is claimed here.

## Criterion ledger

- 1: tests/test_stage2_free.py::test_both_preparations_use_shared_selection — bypassing the shared selector in either caller leaves its production preparation successful
- 2: tests/test_stage2_free.py::test_preparations_select_same_members_for_equivalent_inputs — equivalent policy/eligibility over one catalog yields different pre-probe memberships
- 3: tests/test_stage2_availability.py::test_a_declared_paid_model_with_the_free_suffix_is_not_selected_free — a paid free-looking id is probed or prevents review preparation
- 3: tests/test_stage2_research_availability.py::test_paid_free_candidate_is_dropped_before_research_probes — beam-free is probed, frozen or blocks the remaining research candidates
- 4: tests/test_stage2_free.py::test_policy_adapters_preserve_membership_contracts — provider/freshness, plain ids, includes, excludes or data-class exclusions widen or shrink incorrectly
- 5: tests/test_stage2_free.py::test_both_preparations_share_destination_assessment — foreign destinations survive or same-host move notices disappear
- 6: tests/test_stage2_research_availability.py::test_shared_selection_preserves_optional_research_eligibility — missing tools/deprecation is admitted or unavailable free capability/probes block required slots
- 7: tests/test_stage2_availability.py::test_review_report_names_paid_free_drop — the report hides the paid admission reason
- 7: tests/test_stage2_research_availability.py::test_research_report_names_paid_free_drop — the report hides the paid admission reason
- 8: tests/test_stage2_free.py::test_free_call_boundaries_reject_paid_ids_in_frozen_selection — either boundary trusts a planted frozen paid id
- 9: tests/test_pi_contract.py::test_shipped_catalog_prepares_both_swarms_offline — installed catalog or either valid preparation receipt is absent, a paid id is free, or external/model traffic occurs
- 10: tests/test_pi_contract.py::test_both_preparation_contracts_detect_planted_faults — a forced failure or selection bypass in either preparation escapes the same contract assertions

## Runner route — 2026-11-05

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash failed twice and Sonnet 5.5 once on 2026-11-05 (the last with two red tests: test_shared_selection_preserves_optional_research_eligibility, test_shipped_catalog_prepares_both_swarms_offline).

## Time used

2026-11-05 18:59:33–21:29:31 UTC, 8997 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-07 00:53:22–02:04:59 UTC, 4297 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-07 02:05:10–05:49:32 UTC, 13461 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
