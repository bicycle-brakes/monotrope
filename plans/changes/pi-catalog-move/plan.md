---
title: "Plan — pi-catalog-move"
status: draft
implementation_status: none
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-vku6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, pi, model-catalog]
---

# Plan — pi-catalog-move

```text
For you:     Pi 1.5.0 supplies the shipped Go catalog needed for the separate model-admission change.
Done when:   The locked 1.5.0 install contains the specified Go entries and all offline contracts and make verify pass.
Appetite:    2 hours of phase 4, repairs included — a stop, not an estimate.
Not now:     Model admission, Messages calls, routing, catalog-source changes or runtime redesign.
Pre-mortem:  suppose it failed: most likely because Pi 1.5.0 breaks an existing real-runtime contract.
Starts unless you say stop.
```

## Scope and baseline

Implement criteria 1–4 of `spec.md`, preserving the maintainer's 1.5.0 choice.
Baseline `c7886ea5`, read 2026-11-04: manifest and installed Pi are 1.2.0;
`findings.md` has the draft invocation and no phase-2a rows. This is `bounded`:
no design or ADR. Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash`;
no Stage-1 fallback was recorded. `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent; use the phase-3 prompt's
form and report the absent validator rather than claiming it passed.

## Build sequence and files

1. In `tests/test_pi_contract.py`, add the three ledger-named contracts before
   moving the pin. Check exact 1.5.0 agreement across manifest, lock root,
   locked installed-package entry and actual installed wrapper; inspect the
   real shipped `opencode-go` data, not a live store or overlay. Assert the
   three Chat Completions ids and four Messages ids with the exact API/base
   pairs in spec criteria 2–3. Retain mandatory prerequisites and offline
   guards. Record their red result on the 1.2.0 baseline through the runner.
2. In `tools/pi/package.json`, change only the Pi dependency to exact `1.5.0`.
   Regenerate `tools/pi/package-lock.json` with npm, never by hand, then use
   the existing installer. Registry access is needed for the lock/install,
   not for model calls. Keep Node `26.9.0` declared and lifecycle scripts off.
3. In `tests/test_pi_contract.py`, give the shipped Go native-address assertion
   its own explicit expected base `https://opencode.ai/inference/go/openai/v1`.
   Keep the old synthetic `GO_NATIVE`, moved-base fixtures and their path
   notices intact: changing their starting points could erase a move test.
   Preserve Zen's independent native-base assertion, every admitted-rung
   check, synthetic-key wire exchanges and all existing top-level test names.
   If package layout needs adaptation, keep reads tied to the installed
   package and the same assertions; do not substitute fabricated model data.
4. In `docs/WORKFLOW.md`, make only the present-tense “the pinned Pi 1.2.0”
   reference in the read-boundary paragraph version-neutral and stamp its
   `updated` date. Preserve the dated boundary finding, its accepted limitation
   and historical version measurements; do not claim a new sandbox finding.
4a. In `scripts/stage2.py`, make the free selection (`select_free` or its
   callers, wherever the selected list is formed for the review loop and the
   research swarm) drop every id the `opencode-go` entry declares in
   `modelle`; change no other admission check. In
   `tests/test_stage2_availability.py`, add
   `test_a_declared_paid_model_with_the_free_suffix_is_not_selected_free`: a
   catalog with a `-free` id that `modelle` also lists selects it nowhere and
   the preparation does not refuse (spec criterion 5).
5. Run the commands below. Investigate failures without weakening or skipping
   contracts. A runtime change outside the named files, a failed 1.5.0
   contract needing broader repair, or the two-hour stop returns evidence to
   the orchestrator. The interview permits 1.4.0 as a fallback candidate, but
   it must not be reported as satisfying this spec or silently replace it.
6. Update `plans/changes/pi-catalog-move/spec.md` implementation status and
   `plans/changes/pi-catalog-move/plan.md` status/ledger markers as evidence
   becomes available. The runner writes attempt and verification evidence to
   `plans/changes/pi-catalog-move/findings.md` and measured time below.

No deletions. Leave `research.md` unchanged; `decisions.md` changes only by the orchestrator's recorded answers (Q-2, 2026-11-04). Leave
`tests/test_pi_install.py`'s synthetic 1.2.0 fixture alone; it measures arbitrary
exact-pin behavior, not the production pin. Also leave
`tests/test_stage2_research_catalog.py`, `scripts/` (except the free-selection exclusion of step 4a, decisions.md#Q-2), the wrapper/installer,
Node declaration, model admissions and address record, other change folders,
ADRs, governance, agent configuration, templates, prompts and CI untouched.
No held path needs an orchestrator bootstrap edit. The runner alone regenerates
`plans/INDEX.md` and commits the accepted attempt; do not edit it by hand.

## Verification

Lock regeneration and installation (run from the worktree root):

```sh
npm --prefix tools/pi install --package-lock-only --ignore-scripts
bash tools/pi/install.sh
tools/pi/pi --version
```

Run contracts first, then the full gate after the ledger markers are updated:

```sh
.venv/bin/python3 -m pytest tests/test_pi_install.py tests/test_pi_contract.py tests/test_stage2_research_catalog.py -q
.venv/bin/python3 scripts/check_interview_minimums.py --change pi-catalog-move
.venv/bin/python3 scripts/check_research_handoff.py --change pi-catalog-move
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: tests/test_pi_contract.py::test_real_catalog_move_uses_locked_pi_1_5_0 — a different or floating pin, mismatched lock or different running version passes
- 1: tests/test_pi_install.py::test_install_obeys_lock_integrity_and_disables_scripts — broken lock/integrity or a lifecycle script is accepted
- 1: tests/test_pi_install.py::test_wrapper_refuses_unusable_local_pi — a mismatched or missing local install starts
- 2: tests/test_pi_contract.py::test_real_catalog_move_contains_new_go_models — a required shipped id is absent or has another API/base
- 3: tests/test_pi_contract.py::test_real_catalog_move_keeps_messages_catalog_base — a required Messages entry is missing or has another API/base
- 4: tests/test_pi_contract.py::test_real_opencode_provider_contracts — an admitted rung loses its measured API, Go/Zen base or synthetic-key exchange
- 4: tests/test_pi_contract.py::test_real_reviewer_tool_contract — the installed reviewer loses the allowed tools or accepts an undeclared tool
- 4: tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps — ambient configuration or extensions are activated
- 4: tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads — an outside or symlink read succeeds
- 4: tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date — a refreshed API/base loses to the shipped definition
- 4: tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect — the new manifest pin cannot follow its admitted version hop
- 4: tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect — a forbidden target receives a request
- 4: tests/test_stage2_research_catalog.py::test_preflight_refreshes_despite_fresh_store_and_never_revives_cached_ids — cached models replace the fresh catalog
- 5: tests/test_stage2_availability.py::test_a_declared_paid_model_with_the_free_suffix_is_not_selected_free — a declared paid id with the free suffix is selected free or stops the preparation

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-04 15:30:25–16:19:50 UTC, 2965 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 16:20:05–16:41:23 UTC, 1278 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 16:41:35–16:42:27 UTC, 53 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 18:29:45–19:13:52 UTC, 2647 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 19:14:05–20:32:45 UTC, 4719 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
