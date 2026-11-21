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
- On the same date a synthetic catalog with bare keys missed the `chat:` keys in Pi's shipped catalog, so real Go session lookup refused (`decisions.md`, “The bead”). At commit `8606a0a0`, `tests/test_stage2_go_access.py::test_session_lookup_reads_the_real_pinned_chat_catalog` already exercises the shipped catalog and fails when that file is missing.
- At commit `5e7bd56d`, the pinned Pi contract suite reads shipped files and also creates scratch overlays, while other tests create stand-ins for Pi data (`research.md`, “What exists today”). A passing stand-in alone does not establish compatibility with Pi's actual format.

## Terms

**Real-data twin:** a test of the same production reader or handler as a stand-in, using a file or output shipped or produced by the pinned Pi, or a hook payload rendered by it. A recorded store produced by the pinned Pi counts only with its source, Pi version and capture date recorded. A twin may cover several stand-ins when it establishes their shared format contract; synthetic negative cases remain separate.

## Acceptance criteria

1. When a test substitutes data from a Pi file, a hook payload or a Pi command output parsed by production code, the same production boundary has an offline real-data twin in the normal verification suite.
   *Refuted by:* an applicable stand-in found by the inventory procedure below has no twin, or its twin uses only hand-made Pi data.
2. When session lookup selects a shipped Go model, a twin resolves a `chat:`-keyed entry from the pinned installation's actual `opencode-go.json` and checks that the returned model id and base match the selected entry, using the fields the lookup returns.
   *Refuted by:* a bare-key-only catalog passes, a shipped `chat:` key cannot be resolved, or the returned id or base differs from the selected entry.
3. If the pinned Pi is missing, cannot start, or reports a version other than the pin, every real-data twin counted for this change, including reused twins, fails with the installation hint `bash tools/pi/install.sh`.
   *Refuted by:* a counted twin skips, passes, or fails without that hint in any of those states.
4. If a required installed Pi file is absent, unreadable or incompatible, or its rendering is unsuccessful, its real-data twin fails.
   *Refuted by:* corrupt data or a failed rendering is accepted or skipped.
5. When real-data twins run, they make no external network connection and require no paid model.
   *Refuted by:* a twin connects beyond loopback or requires a paid model.
6. When the specified format fault for an inventory boundary is injected, that boundary's real-data twin fails, demonstrated by a permanent fault check under `make verify`.
   *Refuted by:* the same twin stays green with the boundary's fault in a scratch copy or intercepted output. The installed package is never mutated.

## Inventory and boundary

A stand-in is a fixture, test case or mock that supplies a Pi-produced file, hook event or parsed command output to a production reader or handler. Include indirect users of shared fixtures and monkeypatched Pi calls; synthetic negative cases still need a twin of their production boundary, not a real Pi that emits invalid data. Exclude runner-owned logs and provider HTTP responses that Pi consumes; stderr or stdout Pi writes and the runner parses is included. At commit `1e084b97`, repeat `rg -n 'models-store\.json|opencode-go\.json|models\.json|session.*jsonl|--list-models|--version|--help|--print|before_agent_start|tool_call|confirm_binding|confirm_loaded|last_error_line|_RATE_LIMITED|subprocess|monkeypatch' tests`, trace each relevant match and shared-fixture user to its production reader, and compare its fields with the twin. Review the test list and search results against the mapping. This inventory is **not yet complete**: review finding SR-7 requires classification of all actual stand-in tests before implementation.

| Observed stand-in and test users | Production boundary | Real-data twin or work still needed |
|---|---|---|
| `tests/test_stage2_session.py::world` writes `opencode-go.json`; `tests/test_stage2_go_access.py::test_session_keeps_the_catalog_path_and_records_its_notice`, `test_the_session_binds_the_checked_model_without_reading_auth`, `test_session_sidecar_preserves_shipped_model_behavior`, `test_session_refuses_a_catalog_entry_api_mismatch_before_binding`, and `test_session_records_unrecorded_api_notice` use that fixture. | Shipped catalog to `checked_session_model`. | Existing `tests/test_stage2_go_access.py::test_session_lookup_reads_the_real_pinned_chat_catalog`; compare its coverage with each stand-in field, including behavior fields. |
| `tests/test_stage2.py::world` writes synthetic `models-store.json` and a listing; `test_free_discovery_forces_live_refresh_before_listing`, `test_catalog_parser_uses_header_columns`, `test_catalog_allowlist_fails_closed_when_pi_rejects_the_overlay` and `test_overlay_validation_checks_the_real_resolver` use them. `tests/test_pi_contract.py::offline_world` and `test_real_refreshed_definition_resolves_without_newer_server_date` also substitute refresh data. Other users still require classification. | Store to `overlay_store`, listing to `parse_catalog`, generated `models.json` to Pi's resolver. | `test_shipped_catalog_prepares_both_swarms_offline` passes Pi's real listing through `discover_free` and `parse_catalog`; the resolver tests use a synthetic store. A recorded actual Pi-written store with source, capture date and pin through `overlay_store` is needed; no such recording was located in this worktree on 2026-11-21. |
| `tests/test_stage2_session.py::PI_VERSION_STEP`, `PI_HELP_STEP` and `world` substitute version, extension help and `confirm_binding`; `test_a_pi_off_the_pin_refuses_before_anything_else`, `test_an_extension_that_did_not_load_refuses_and_cleans_up`, and `tests/test_stage2_go_access.py::test_the_session_binds_the_checked_model_without_reading_auth` exercise them. Other users require classification. | `require_pi`, `confirm_loaded`, and `confirm_binding`. | Real output must reach each production reader. `test_real_catalog_move_uses_locked_pi_1_5_0` compares the version independently; `test_real_session_binding_holds_the_assessed_base` exercises registration separately, so neither alone covers its reader. |
| `tests/test_stage2_session_policy.py::World.case` and its tests give the policy synthetic `tool_call` events. | Pi hook event to the production session policy. | `tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads` exercises the production policy with real Pi tool events; compare covered event tools and fields before declaring the boundary covered. |
| `tests/test_stage2.py::test_truncated_pi_print_failure_is_refused` uses a stand-in result. | Pi print result to reviewer failure handling. | `tests/test_pi_contract.py::test_real_truncated_pi_print_failure_is_refused` passes the real Pi result to the production reviewer. |
| `tests/test_stage2.py::test_a_rate_limited_free_round_moves_on_to_the_flash_swarm`, `test_a_rate_limited_member_beside_an_answer_keeps_the_free_round`, and `test_rate_limited_reads_only_a_failed_exit_with_a_rate_limit` substitute error output. | Pi stderr through `last_error_line`, reviewer failure handling and rate-limit classification. | A real Pi call against a loopback 429 or 503 response must reach the production failure and classification path. |
| `tests/stage2_repository_pathlock_driver.mjs` and users in `tests/test_stage2_repository_pathlock.py` manufacture `tool_call` events. | Real Pi event to the repository path-lock extension. | A pinned-Pi twin must exercise the production extension on allowed and escaping paths. |
| `tests/stage2_research_tools_driver.mjs` and users in `tests/test_stage2_research_tools.py`, including `test_the_tools_run_as_pi_calls_them`, manufacture `tool_call` events and tool `execute` arguments. | Real Pi event and registered-tool execution to the research-tools extension. | A pinned-Pi twin must exercise the gate and registered tool input/result with loopback-only transport. |
| `tests/test_stage2_research_availability.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_terms_expiry.py`, and `tests/test_stage2_research_deep_review.py` supply synthetic catalog or listing data through direct helpers or shared fixtures. | Catalog, store, listing and generated configuration readers. | Classify every actual test user and map each boundary and field to the checks above or a new twin before phase 4. |

The neutral-path extension and its hook tests are absent from this worktree. Its future change owns its real-rendered-prompt twin. A search for session JSONL and `before_agent_start` in `scripts/` and `tests/` found no match at this commit; this search alone does not prove the inventory complete.

Faults for the boundaries currently identified: catalog — replace `chat:` keys with bare keys; store — change the provider's `models` array to an object; listing — remove the `model` header; version — substitute a different version; extension help — remove the registered flag; binding — remove the bound model row; session policy and path lock — replace the tool event's `input.path` with a different field; research tools — replace `toolName` or its registered tool's `query`/`url` parameter; print result — make the nonzero exit appear successful; rate limit — remove the rate-limit marker from the actual Pi stderr. Each fault is applied to the same twin's data through a test seam; checks must show that twin fails, rather than merely asserting the production reader refuses independently. Additional boundaries found in the unfinished inventory need similarly specific faults before the spec is final.

## Non-goals

- No live provider calls, paid models, Pi pin change, production behavior repair, or expansion of the access policy.
- No replacement of synthetic negative tests: malformed inputs still need their individual checks.
- No neutral-path extension or twin for its absent `before_agent_start` hook; the change that lands the extension owns that twin.

## Protected areas

`docs/adr/0019-repository-pinned-pi-and-contract-tests.md` and `tools/pi/install.sh` remain unchanged as decided in `decisions.md`; preserve the existing Pi contract suite's mandatory prerequisite failures rather than weakening them to skips.

## Definition of Done

- The inventory is complete, every applicable boundary has an evidenced twin, and `make verify` is green with the pinned Pi installed.
- No ADRs or other enduring documents need to move with this test-only change; the protected areas and non-goals are untouched.
- The pull request closes the real Pi data contract work item (`coding-harness-z4oo`) and its last commit carries `Closes-Bead: coding-harness-z4oo`.
- Special runs: none beyond the targeted tests and `make verify` in the plan.

## Open decisions

- [DETAIL] The appetite is four hours for implementation and repair, a stop rather than an estimate; no prior appetite was recorded, and this bounds the inventory and tests.
- [GAP] The per-test inventory remains incomplete, and the recorded real store's source and capture date have not been located. Finish the fixture and direct-call audit and identify a verifiable recording before phase 4; do not claim criterion 1 or close review finding SR-7 on the partial mapping above.
- [DETAIL] The neutral-path extension has no implementation in this worktree; its own change must carry its real-rendered-prompt twin, as recorded in `decisions.md`.
