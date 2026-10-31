---
title: "Plan — go-access-point"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-4tr4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, opencode-go]
---

# Plan — go-access-point

```text
For you:     One Go address rule: same-host path moves run on with a notice,
             foreign hosts stop before any model call.
Done when:   Criteria 1-11 hold and make verify is green, with the review
             loop refusing a foreign catalog host it admits today.
Appetite:    6 hours of phase 4, repair rounds included; then stop.
Not now:     Catalog sources, the general model registry, model admissions,
             credentials, and changes to earlier ADRs.
Pre-mortem:  suppose it failed: most likely because Pi overrode the checked base.
Starts unless you say stop.
```

Proposed, unimplemented; baseline `b126fce7`, inspected 2026-10-31. Q-4
requires ADR 0024 and Q-5 settles storage and maintenance: the address
part belongs on the `opencode-go` entry, edited by the orchestrator.
The single ADR draft already belongs to this change; no second ADR is
created. No `templates/plan.md` exists at this baseline; this file follows
the phase-3 form. The five answered interview records settle intent;
there is no new maintainer question.

Explore route carried forward (`research.md`, 2026-10-31): phase 1 ran as
a stage-2 `explore` on route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash`, plus a Claude Haiku 5.5 sub-agent reading the repository
and the public Go page — by the maintainer's exception, because the
research swarm refused every Go origin at its own hard-coded check. This
was not a Stage-1 fallback. The explore-only `spike` classification ended
with the interview; the change is a `feature`.

## Files and steps

1. Add `scripts/stage2_go.py`: the one policy module. It loads the
   `adresse` part of the uniquely named `opencode-go` entry from the
   original YAML using a duplicate-rejecting loader; do not validate a
   `safe_load` result after it has lost duplicate keys. Validate one
   host, per-API bases on that host, dated sources, and known address keys;
   then offer
   `assess(policy, model, definition)` — an explicit effective definition
   with an optional move notice, or a sanitised refusal. No literal
   default and no cached policy survive anywhere in it.
   Shape: `adresse: {host: opencode.ai, apis: {<wire-api>: {basis, quelle,
   gelesen}}}`; `basis` is the explicit HTTPS base, `quelle` its nonblank
   documentation source, and `gelesen` a quoted ISO reading date. Resolve
   provider/id/API offline before filling a missing base; an unmapped API
   has no default, and a mapping grants no model or measured-API admission.
2. Add `tests/test_stage2_go_access.py` with the ledger's regressions:
   real caller functions with synthetic send and terminal stand-ins, not
   bare checker calls — every launch family, hostile URL forms,
   recorded, changed and absent bases, duplicate record keys, partial and
   empty catalogs, saved selections, retries and replacements, and the
   notice evidence. Change the policy between preparation and final
   dispatch and assert zero sends and unchanged prior history.
3. Change `scripts/stage2.py`: thread root and policy into discovery,
   `activate_overlay`, `check_overlay` and the reviewer launch; only
   assessed definitions become selectable. `dispatch_go` requires
   concrete effective destination evidence and re-checks current policy
   immediately before its send callback; the no-store reviewer branch is
   resolved offline or refused instead of sending unchecked. Raw stores
   stay intact, dropped-field checks stay in force, and move notices
   attach to the existing preparation and round evidence. Update the
   `probe` docstring and the DL-B-8 comment above `OVERLAY_FIELDS`.
4. Change `scripts/stage2_swarm.py`: `pi_reason` assesses through the
   common policy — host from the record, any path on it admissible, a
   notice on difference — while candidate-local rejection, raw evidence
   and the `measured_wire_apis` checks stay.
5. Change `scripts/stage2_availability.py`: remove `CHECKED_BASE_URL`;
   `install_measured_models` fills an absent base from the recorded API
   default; root and effective target propagate to probes and dispatch,
   and address notices land in the existing receipts and reports. A saved
   or legacy selection is re-checked without resetting membership, and a
   refused set is never reported as a clean operation.
6. Change `scripts/stage2_research_run.py`: pass the record into every
   selected-row installation, keep move notices in the research audit,
   and supply the exact resolved definition to every Go send, including
   replacement and retry.
7. Change `scripts/stage2_session.py` and
   `scripts/stage2_session_policy.mjs`: resolve and assess the initial Go
   model offline without reading ambient credentials, copy only
   allow-listed checked model data into the session's private launch
   directory, bind the checked definition through the pinned Pi's
   model-registry and provider registration at startup, and re-check
   policy at `dispatch_go` before the terminal dispatch. Do not rely on a
   throwing `before_provider_request`: Pi catches handler exceptions. If
   the installed Pi's contract cannot establish the binding, refuse the
   preparation. Keep login, cleanup, selection and audit contracts.
8. Update the pinned tests, keeping their original proof duties:
   `tests/test_pi_contract.py`
   (`test_real_refreshed_definition_resolves_without_newer_server_date`
   proves exact fresh activation at old server dates with an admitted
   same-host changed path instead of a foreign-host positive; the shipped
   catalog tests stay facts about the pin), `tests/test_stage2.py`
   (world, overlay and dispatch fixtures), `tests/test_stage2_swarm.py`,
   `tests/test_stage2_availability.py`,
   `tests/test_stage2_research_catalog.py`,
   `tests/test_stage2_research_availability.py`,
   `tests/test_stage2_research_deep_review.py` (the recorded default
   replaces the removed constant), `tests/test_stage2_session.py`,
   `tests/test_stage2_session_policy.py`, and
   `tests/test_stage2_terms_expiry.py` (destination evidence at dispatch,
   expiry boundary unchanged). Put synthetic address records in test
   declarations, including copies of the real entry used for discovery;
   no test depends on a production record before the bootstrap. Preserve
   loopback wire tests by routing the admitted HTTPS target at the existing
   test subprocess/transport seam, recording its original destination;
   never relax the production host check to allow the loopback URL.
9. Change `scripts/research_capture.py` only to hand the offline capture
   fixture and its selector the central record; its evidence semantics
   stay.
10. Change `tests/test_model_endpoints.py`: validate the entry's address
    record against synthetic declarations during the attempt — shape,
    dated sources, bases on the host. The assertion against the real
    entry lands with step 12.
11. Change `docs/WORKFLOW.md`: one paragraph beside the stage-2
    description — one record, same-host moves run on with a notice,
    foreign hosts are refused, and the maintenance route for the address
    is an agent edit of the held entry through the orchestrator.
12. **Orchestrator bootstrap, after the accepted attempt** — the held
    file: edit `model-endpoints.yaml` once the Go page has been freshly
    read; add the `adresse` record to the `opencode-go` entry, refresh
    the address prose in its `bemerkung`, and update the remark-test
    literals to the strings it then carries. Add
    `test_the_opencode_go_entry_declares_its_address_record` against the
    real entry. Review
    `docs/adr/0024-one-access-policy-for-opencode-go.md` against Q-1–Q-5
    and the final implementation, adjusting only that draft if needed;
    every phase-4 edit of this held ADR path is orchestrator-owned too.
    Then run `make verify`. The stage-2 attempt never edits either held
    file. Until this bootstrap finishes, Go launches fail closed on the
    missing record; no temporary code default is permitted.
13. Within this change, update `plan.md` as named tests land and the
    runner records time; `findings.md` holds runner and reviewer
    evidence. `spec.md`, `design.md`, `research.md` and `decisions.md`
    are inputs — never change their intent or answers to make a check
    pass. The runner regenerates `plans/INDEX.md`; the drafter does not
    edit it.

No file is deleted. Do not touch `scripts/stage2_research_catalog.mjs`
(catalog sources belong to `pi-catalog-redirect`), any earlier file under
`docs/adr/` (only this change's ADR 0024 draft is in scope),
`decisions/answers/`, `decisions/gates.yaml`,
`provenance.yaml`, secrets, the Pi manifest and lock, `prompts/`,
`templates/`, `.github/`, `CLAUDE.md`, `AGENTS.md`, `README.md`, or any
other change's folder. `model-endpoints.yaml` is edited only by the
orchestrator (step 12). The decision pull request uses
`.github/PULL_REQUEST_TEMPLATE/decision.md`, a `decide(go-access-point):`
title and the `decision` label; the orchestrator supplies these at phase 7,
without changing the template. Only the maintainer merges it.

## Verification

The orchestrator establishes the toolchain once per worktree with
`make venv` and `bash tools/pi/install.sh`; tests use synthetic providers
or the installed Pi with outbound network forbidden. Show the new
behaviour tests red against the baseline and green after the change; no
live Go call substitutes for a deterministic destination assertion.

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2_go_access.py tests/test_pi_contract.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_availability.py tests/test_stage2_research_catalog.py tests/test_stage2_research_availability.py tests/test_stage2_research_deep_review.py tests/test_stage2_session.py tests/test_stage2_session_policy.py tests/test_stage2_terms_expiry.py tests/test_model_endpoints.py
python3 scripts/check_interview_minimums.py --change go-access-point
python3 scripts/check_research_handoff.py --change go-access-point
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

`scripts/validate_change_artefacts.py` does not exist at `b126fce7`; its
`--check` cannot be reported green. The runner owns the derived index,
the full verification and the one commit; the orchestrator owns the held
bootstrap edit before the final verification. No commit, tracker write or
foreign model call belongs to a drafting attempt.

Draft evidence belongs to this drafting run's report; previous failed
attempt logs remain unchanged in `findings.md`. The ADR change owes five
counted interview answers and Q-1–Q-5 supply them. There is no complete
`research-swarm/v2` run; phase 1 used the maintainer's recorded routing
exception. The registry check needs the tracker and the regenerated
`plans/INDEX.md`; the runner owns those checks beyond this draft's write
boundary. Do not repair unrelated failures or remove the ADR claim.

Measured 2026-10-31: interview minimums, ADR answers and the criterion
ledger pass; research handoff reports the legacy exemption. Registry and
full verification are left to the runner; the missing artifact validator
is not reported green. No phase-2a review rows exist to reconcile.

## Criterion ledger

- 1: tests/test_stage2_go_access.py::test_every_go_path_reads_the_one_address_record — a caller keeps its own origin rule or default
- 1: tests/test_model_endpoints.py::test_the_opencode_go_entry_declares_its_address_record — the real entry loads no valid record after the orchestrator bootstrap
- 2: tests/test_stage2_go_access.py::test_unsafe_destinations_are_refused_before_any_send — a foreign host, subdomain, userinfo, http, port, query or fragment reaches the send stand-in
- 3: tests/test_stage2_go_access.py::test_same_host_path_moves_run_with_notice — the inference path stops, is rewritten or runs silently
- 4: tests/test_stage2_go_access.py::test_absent_bases_get_the_recorded_api_default — an invalid explicit base or unmapped api falls back to a Pi default
- 4: tests/test_pi_contract.py::test_real_resolution_uses_the_assessed_base — real Pi restores a shipped or cached base after validation
- 5: tests/test_stage2_go_access.py::test_refused_rows_stay_refused — a filtered row returns as a shipped model or an unrelated candidate is lost
- 6: tests/test_stage2_go_access.py::test_every_send_rechecks_current_policy — a saved, resumed, replaced or retried launch dispatches a now-refused destination
- 7: tests/test_stage2_go_access.py::test_the_session_binds_the_checked_model_without_reading_auth — the terminal receives an unbound model or the runner reads saved credentials
- 7: tests/test_pi_contract.py::test_real_session_binding_holds_the_assessed_base — real Pi resolves another base after the binding
- 8: tests/test_stage2_go_access.py::test_an_unusable_record_stops_go_admission — a missing, duplicated or malformed record silently activates a literal
- 9: tests/test_stage2_go_access.py::test_path_maintenance_records_source_and_date — an undated or unsourced path is accepted
- 9: not a test — the phase-6 review reads the maintenance route and the final changed paths against the maintainer's Q-3 and Q-5 answers; a new human path approval or a runner edit of the held entry refutes it
- 10: tests/test_stage2_go_access.py::test_admission_preserves_the_other_restrictions — a good host bypasses terms, wire-api, leak or free-class rules
- 11: tests/test_stage2_go_access.py::test_notices_are_kept_and_sanitised — a move notice is transient, a refusal names no model, or a raw credential-bearing URL enters evidence

## Runner route — 2026-10-31

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-10-31

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash failed twice and the stage-1 attempt ran 44 s; Sonnet continues from the saved work at c17a2696.

## Runner route — 2026-10-31

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash failed twice; Sonnet continues: the full verify at 9d1fc216 left 158 red tests, most because research seats refuse to start without a refreshed definition the swarm world does not supply.

## Time used

2026-10-31 17:02:22–18:45:11 UTC, 6169 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-31 18:45:18–18:49:04 UTC, 226 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-31 18:49:10–18:49:54 UTC, 44 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-31 19:09:22–19:36:45 UTC, 1643 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-31 20:34:57–21:26:18 UTC, 3080 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
