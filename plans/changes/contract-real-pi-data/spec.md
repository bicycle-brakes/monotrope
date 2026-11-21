---
title: "Spec — contract-real-pi-data"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-z4oo
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, pi, contract-tests]
class: bounded
appetite: 4
adr_files: []
---

# Spec — contract-real-pi-data

Pi format and hook contracts are checked against data from the repository's pinned installation, so format drift cannot pass solely because a stand-in shares the test's assumption (bead `coding-harness-z4oo` — real Pi data in contract tests). Research: `research.md`; scope and interview skip: `decisions.md`.

## Problem

- On 2026-11-01 a hand-made prompt did not match the already rendered `before_agent_start` prompt delivered by Pi 1.2.0; the neutral-path extension failed in a live run (`decisions.md`, “The bead”).
- On the same date a synthetic catalog with bare keys missed the `chat:` keys in Pi's shipped catalog, so real Go session lookup refused (`decisions.md`, “The bead”). At commit `5e7bd56d`, `tests/test_stage2_go_access.py::test_session_lookup_reads_the_real_pinned_chat_catalog` already exercises the shipped catalog; its missing-install behavior is a failure, not the requested skip.
- At commit `5e7bd56d`, the pinned Pi contract suite reads shipped files and also creates scratch overlays, while other tests create stand-ins for Pi data (`research.md`, “What exists today”). A passing stand-in alone does not establish compatibility with Pi's actual format.

## Terms

**Real-data twin:** a test of the same production boundary as a stand-in test, using a file shipped or produced by the pinned Pi, or a hook payload rendered by it. It may cover several stand-in cases when it establishes their shared format contract; synthetic negative cases remain separate.

## Acceptance criteria

1. When a test stands in for a Pi file format or hook payload, its production boundary has a real-data twin exercised by the normal verification suite.
   *Refuted by:* an inventoried stand-in boundary has no twin, or its twin reads only a hand-made format.
2. When the neutral-path extension handles `before_agent_start`, a twin exercises it with the pinned Pi's own rendered prompt.
   *Refuted by:* the twin only calls the hook with a hand-written prompt, or never reaches the production extension.
3. When session lookup selects a shipped Go model, a twin reads the pinned installation's actual `opencode-go.json` and checks the resulting binding against that file.
   *Refuted by:* a bare-key-only lookup passes although the shipped `chat:` key cannot be resolved, or the binding differs from the shipped definition.
4. If the pinned Pi is not installed, each new real-data twin skips with reason `pinned Pi not installed (tools/pi/install.sh)`.
   *Refuted by:* an absent installation causes a new twin to fail, pass without exercising the boundary, or skip with another reason.
5. When the pinned Pi is installed, a real-data twin fails on an incompatible, unreadable or missing required Pi data file or an unsuccessful rendering.
   *Refuted by:* corrupt or incompatible installed data is treated as an absent installation or accepted.
6. When the real-data twins run, they use no external network or paid model.
   *Refuted by:* a twin attempts a non-loopback connection or requires a paid model.
7. When a Pi format or hook payload changes incompatibly, the corresponding real-data twin fails under `make verify`.
   *Refuted by:* an injected incompatible format or rendered payload leaves its relevant twin green.

## Inventory and boundary

The following observed stand-ins and existing real-data checks anchor the inventory at commit `5e7bd56d`; a complete per-test inventory, including tests using shared fixtures, is still owed before implementation is accepted:

- `tests/test_stage2_session.py::world` writes a stand-in `opencode-go.json`; `tests/test_stage2_go_access.py::test_session_keeps_the_catalog_path_and_records_its_notice`, `test_the_session_binds_the_checked_model_without_reading_auth`, `test_session_sidecar_preserves_shipped_model_behavior`, and `test_session_refuses_a_catalog_entry_api_mismatch_before_binding` exercise it. `tests/test_stage2_go_access.py::test_session_lookup_reads_the_real_pinned_chat_catalog` is an existing real-data check.
- `tests/test_stage2.py::test_refreshed_model_definitions_reach_each_launch`, `test_catalog_allowlist_fails_closed_when_pi_rejects_the_overlay`, and `test_overlay_validation_checks_the_real_resolver` use stand-in `models-store.json` or `models.json`. `tests/test_stage2_research_deep_review.py::test_a_launch_writes_only_its_own_allow_listed_row` and `test_a_row_pi_would_refuse_fails_the_launch_closed` use synthetic model definitions. Existing real Pi resolution checks include `tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date` and `test_real_resolution_uses_the_assessed_base`.
- The neutral-path extension and its hand-made hook payload tests are absent from this worktree at that commit. The parked branch `origin/fix/pi-neutral-paths` contains `tests/test_pi_contract.py::test_neutral_registration_covers_launch_directories`, `test_neutral_cwd_fails_closed`, and `test_neutral_docs_fail_closed`; the extension must be available in the implementation base for criterion 2 to be measured. The branch also contains real-Pi checks that must be assessed before adding duplicates.
- No Pi session-record format stand-in was established by the searches for this draft; this is not evidence that none exists. Complete the inventory before claiming criterion 1.

## Non-goals

- No live provider calls, paid models, Pi pin change, production behavior repair, or expansion of the access policy.
- No replacement of synthetic negative tests: malformed inputs still need their individual checks.

## Protected areas

`docs/adr/0019-repository-pinned-pi-and-contract-tests.md` and `tools/pi/install.sh` remain unchanged as decided in `decisions.md`; preserve the existing Pi contract suite's mandatory prerequisite failures rather than weakening them to skips.

## Definition of Done

- The inventory is complete, every applicable boundary has an evidenced twin, and `make verify` is green with the pinned Pi installed.
- No ADRs or other enduring documents need to move with this test-only change; the protected areas and non-goals are untouched.
- The pull request closes the real Pi data contract work item (`coding-harness-z4oo`) and its last commit carries `Closes-Bead: coding-harness-z4oo`.
- Special runs: none beyond the targeted tests and `make verify` in the plan.

## Open decisions

- [DETAIL] The appetite is four hours for implementation and repair, a stop rather than an estimate; no prior appetite was recorded, and this bounds the inventory and tests.
- [GAP] The full test-by-test inventory and the neutral-path extension's landing are unresolved repository facts, not maintainer decisions. The implementer must establish them before claiming criterion 1 or 2; do not silently treat an absent extension as a passing test.
