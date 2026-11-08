---
title: "Plan — go-wire-apis"
status: draft
implementation_status: partial
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-36za
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, opencode-go, wire-api]
---

# Plan — go-wire-apis

```text
For you:     Already admitted Go models can use Messages and Responses directly; Google waits for an admissible model (decisions.md Q-2).
Done when:   Native offline contracts, the two recorded live API measurements (Messages, Responses) and make verify pass with the final declaration.
Appetite:    3 hours of phase 4, repairs included — a stop, not an estimate.
Not now:     New model admissions, terms renewal, translation, a Pi upgrade or changed routing policy.
Pre-mortem:  suppose it failed: most likely because the fresh catalog lacks an exact admitted representative for one API.
Starts unless you say stop.
```

## Scope and baseline

Meet criteria 1–6 of `spec.md` under the maintainer's one answered interview
record. Baseline `acebe186`, read 2026-11-06: bounded class, Pi 1.5.0,
single-API address/measurement declarations, nine wire-skipped records, no
open phase-2a finding. No design or ADR is due. Explore used Stage 2, route
`flash`, model `glm-5.3-flash`; no Stage-1 fallback is recorded.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent;
this plan follows the phase-3 prompt, without claiming the missing gate ran.

## Files and sequence

1. **Implement attempt:** change `tests/test_pi_contract.py`. Extend its
   loopback stand-in with native Messages, Responses and Google request
   routes and minimal valid streamed text replies, using the installed
   Pi 1.5.0 adapters as the local protocol reference. Add the two ledger-named
   parametrized tests: assert exact model, route, body format, decoded reply,
   synthetic authentication and absence of foreign keys/body credentials for
   every API; inject HTTP failure, malformed stream and empty answer for each.
   Expected suffixes are `/v1/messages` for Messages, `/responses` for
   Responses, and `/models/<exact-id>:streamGenerateContent` for Google
   (including its streaming query). Check the request's native schema,
   not just its URL; allow protocol-specific synthetic authentication.
   Keep the existing network guard, scratch HOME, mandatory prerequisites,
   no-tools flags and Chat Completions/Zen contracts. Never fall back to a
   fake Pi launch. Record meaningful red-first failures through the runner.
2. In that same file, generalise `test_real_opencode_provider_contracts`:
   flatten the shipped Go catalog across API groups, then hold every eligible
   rung against its own API's recorded base and measured-API declaration.
   Keep exact Go/Zen Chat Completions assertions and their synthetic exchanges;
   the new protocols have their own exchanges from step 1. This must pass the
   old declaration before bootstrap and cover newly eligible rungs afterwards.
3. Change `tests/test_stage2_go_access.py`: add the ledger-named parametrized
   multi-API probe test using the real preparation/install/dispatch path with
   synthetic declarations. For each new API prove its explicit base and an
   absent-base row both resolve to that API's mapping. Plant an API/base
   configuration mismatch and a foreign host; neither may send. Change
   `tests/test_stage2_research_availability.py`: add the ledger-named test
   proving a newly measured, otherwise eligible native model can fill a seat,
   while an otherwise identical unmeasured candidate remains excluded.
4. Change `tests/test_model_endpoints.py`: replace the hard-coded singleton
   measured-list assertion with checks against the address record and a
   supported set of the four APIs; retain nonempty/unique-name validation.
   Add fixture fault cases for a missing API mapping, unrelated API and
   missing source/date. Preserve the six-seat and free-rule assertions.
   Run the offline tests and `make verify`. The attempt edits no held path;
   normal selection still honours the original wire skips at this point.
5. **Orchestrator only, after the accepted attempt:** bootstrap the held
   `model-endpoints.yaml`. Read the current public Go endpoint documentation
   and freshly refreshed catalog before editing. Add `adresse.apis` mappings
   with `basis`, actual documentation `quelle` and quoted reading-date
   `gelesen`; expected Pi-shaped bases are Messages
   `https://opencode.ai/inference/go/anthropic`, Responses
   `https://opencode.ai/inference/go/openai/v1`; Google
   (`https://opencode.ai/inference/go/google/v1beta`) is not declared — no
   admissible model (decisions.md Q-2, bead coding-harness-twdu). Responses legitimately
   shares the completions base; the adapters append different routes.
   A changed source/base is evidence to investigate, never silently replace.
6. **Orchestrator only:** stage the candidate measurement-list expansion and
   removal of wire-only `uebersprungen`/`grund` pairs for exact catalog-matched
   ids with still-valid terms. Preserve every other term field, exclusion,
   id, request cost, seat and legacy Flash declaration. This is provisional
   configuration solely for the existing tool-free preparation command:
   do not start a review, research run or session until measurement succeeds.
   Do not weaken `terms_problem` or `dispatch_go`, use free admission for a
   paid model, change system time or renew an expired reading to get a probe.
7. Run the live command below through `scripts/stage2.py`, with its normal
   forced catalog refresh, leak checks and pinned tool-free probes. Existing
   preparation may also probe other eligible members; do not change its policy
   to restrict the run to three calls. Identify at least one successful exact
   representative per API: prefer `claude-haiku-5-5`, `gpt-6-luna` and
   `gemini-4-argon`; another already wire-skipped id on the same API is usable
   if the preferred one is unreachable, with the choice recorded. No new id
   or contributor alias. Success means a nonempty decoded answer without Pi
   configuration errors, not merely exit zero or presence in the catalog.
8. **Orchestrator only:** create `docs/research/2026-11-06-go-wire-apis.md`
   with provenance, UTC measurement time, code commit, Pi version, source
   reading, refreshed exact model/API/base, native route proven offline,
   live outcome and scrubbed audit location for each API; state which skipped
   ids now qualify and why others remain blocked. Never copy keys or raw
   credential-bearing traffic. If any API has no successful measurement,
   restore its provisional skips/list entry/mapping and report the blocked
   criterion; this change ships the two measured APIs (decisions.md Q-2). On success retain
   only justified wire-skip removals and correct the entry's present-tense
   `bemerkung`/comments, preserving dated history. Report preparation's
   selections/failures in the main conversation; do not consume its receipt
   for a review loop as part of this measurement.
9. Update `plans/changes/go-wire-apis/spec.md` implementation status and
   `plans/changes/go-wire-apis/plan.md` ledger markers as work lands; the runner
   maintains evidence in `plans/changes/go-wire-apis/findings.md` and time
   below. After bootstrap the orchestrator reruns offline tests and the full
   gate before review. Phase 6 compares the final declaration with all three
   live evidence rows; offline green alone is insufficient.

No deletions. Leave `research.md` and `decisions.md` unchanged during
implementation. Leave production `scripts/` (except the one research-selector signature line and its capture caller, spec "Protected areas", decision Q-3), Pi package/lock/install,
`tests/pi_network_guard.mjs`, `tests/pi_contract_driver.mjs`, governance,
ADRs, prompts, templates, CI, agent configuration, other change folders and
`docs/WORKFLOW.md` untouched. A production adapter/runner defect or absent
Google id returns evidence to the orchestrator instead of expanding this
plan. The runner alone regenerates `plans/INDEX.md` and commits the attempt.

## Verification

From the worktree root, after the existing locked environment and pinned Pi
installation are ready:

```sh
.venv/bin/python3 -m pytest tests/test_pi_contract.py tests/test_model_endpoints.py tests/test_stage2_go_access.py tests/test_stage2_research_availability.py -q
.venv/bin/python3 scripts/check_interview_minimums.py --change go-wire-apis
.venv/bin/python3 scripts/check_research_handoff.py --change go-wire-apis
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

Special live run, only at the orchestrator's provisional bootstrap step:

```sh
.venv/bin/python3 scripts/stage2.py prepare-loop go-wire-apis
```

Use the tool-free preparation, not `stage2.py probe`: the latter sends the
implementation diff to free members and keeps read tools for paid members.
Keep final verification and live evidence tied to their exact code commits.

## Criterion ledger

- 1: tests/test_pi_contract.py::test_real_go_native_wire_api_exchange — wrong native route/body/model, missing decoded text, wrong authentication or external traffic passes
- 2: tests/test_pi_contract.py::test_real_go_native_wire_api_failures_are_mandatory — failed, empty or malformed exchange passes
- 2: tests/test_pi_contract.py::test_contract_prerequisites_and_failures_are_mandatory — missing prerequisites skip instead of failing
- 3: not a test — the phase-6 review checks the two dated live rows (Messages, Responses; Google deferred, decisions.md#Q-2) and their code commit in docs/research/2026-11-06-go-wire-apis.md against the runner audit; offline or failed evidence cannot satisfy it
- 4: tests/test_model_endpoints.py::test_the_repository_declaration_carries_six_seats_and_the_rule — an unmeasured API or a measured API without its mapping passes
- 4: tests/test_model_endpoints.py::test_the_address_record_shape_is_validated — an unsourced, undated or invalid API base loads
- 4: not a test — phase 6 verifies that the final address and measured lists contain exactly the existing completions API plus the two successfully measured APIs (decisions.md#Q-2)
- 5: tests/test_pi_contract.py::test_real_opencode_provider_contracts — an eligible native rung is missing or forced into the completions group
- 5: tests/test_stage2_research_availability.py::test_newly_measured_native_apis_admit_only_eligible_seat_models — a qualifying measured model stays excluded or an unmeasured peer is selected
- 5: not a test — phase 6 compares the nine original wire-skip records with the final declaration, fresh catalog and unchanged terms
- 6: tests/test_stage2_go_access.py::test_native_api_probes_keep_their_assessed_destinations — a wrong default, mismatched configuration or foreign host reaches send
- 6: tests/test_stage2_go_access.py::test_admission_preserves_the_other_restrictions — a new mapping bypasses independent terms, purpose or capability restrictions
- 6: tests/test_stage2_go_access.py::test_every_send_rechecks_current_policy — a saved selection sends after the current policy refuses it
- 6: tests/test_stage2_research_availability.py::test_pool_requires_tool_support_and_a_measured_wire_api — an unmeasured or incapable candidate becomes a substitute

## Time used

Appetite overrun, 2026-11-07: 14684 s recorded against the 3 h card; parked at
loop round 3, the maintainer granted one more hour (repair, phase 6, pull
request).

2026-11-06 16:19:48–17:39:18 UTC, 4769 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-06 17:39:28–18:44:18 UTC, 3890 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
2026-11-07 13:19:23–13:42:09 UTC, 1366 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-07 13:55:18–15:12:57 UTC, 4659 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-08 01:43:05–03:34:42 UTC, 6696 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
