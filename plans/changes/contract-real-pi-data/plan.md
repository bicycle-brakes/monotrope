---
title: "Plan — contract-real-pi-data"
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
tags: [plan, pi, contract-tests]
---

# Plan — contract-real-pi-data

```text
For you:     Pi format and command-output drift is checked against the pinned installation's data.
Done when:   The reviewed inventory has offline real-data twins, the recorded catalog fault is refused, and make verify passes.
Appetite:    4 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     The absent neutral-path extension, production repairs, paid calls, a Pi pin change, or replacing synthetic negative tests.
Pre-mortem:  suppose it failed: most likely because a shared fixture hides an uncovered Pi format boundary.
Starts unless you say stop.
```

## Files and steps

1. **Before implementation:** finish the per-test inventory in `plans/changes/contract-real-pi-data/spec.md` using its repeatable search, and resolve review finding SR-7 in `plans/changes/contract-real-pi-data/findings.md`. Trace fixture users, direct stand-ins and mocked calls to each production reader and field, with a named existing or planned twin and a specific fault for every boundary. Locate a verifiable Pi-written store recording with its source, pin and capture date; no such recording has been established here. Do not start phase 4 while the audit or recording is unresolved.
2. Create `tests/fixtures/pi-models-store.json` from that verified recording and record its source, capture date and pinned Pi version in `tests/fixtures/pi-models-store-source.md`; do not fabricate a recording or use a live provider during tests. Pass it through `overlay_store` in `tests/test_real_pi_data.py`. If its source cannot be substantiated, stop and report the gap.
3. Create `tests/test_real_pi_data.py` for uncovered boundaries: call `stage2.require_pi`, `stage2_session.confirm_loaded` and `confirm_binding` against real pinned Pi; use the loopback transport to pass real Pi error output through reviewer failure and rate-limit classification. Run the production path-lock and research-tools extensions in Pi with real tool events and registered-tool calls; retain synthetic negative tests. `tests/test_pi_contract.py::test_shipped_catalog_prepares_both_swarms_offline` already sends the real listing through `parse_catalog`.
4. Change `tests/test_stage2_go_access.py` and, where needed, `tests/test_pi_contract.py` to enforce the pinned-install prerequisite on reused twins and expose a test seam for each twin's scratch data or intercepted output. All counted twins fail with `bash tools/pi/install.sh` for missing, unstartable or wrong-version Pi. Add permanent fault checks in `tests/test_real_pi_data.py` that run the same twins against the precise faults in the inventory; do not modify the installed package. Use synthetic credentials, loopback transport and a network guard.
5. Update the criterion ledger in `plans/changes/contract-real-pi-data/plan.md` when named tests are written. Phase 4 records its own time in `## Time used`. No files are deleted. No design or ADR is due for a bounded change. No held path is assigned to the implement attempt.

## Verification and boundaries

With the pinned Pi installed, run:

```sh
.venv/bin/python3 -m pytest -q tests/test_real_pi_data.py tests/test_pi_contract.py tests/test_stage2_go_access.py tests/test_stage2_session.py
make verify
```

Use isolated prerequisite-failure and fault cases, never a mutation of `tools/pi/node_modules`. Do not change `docs/adr/0019-repository-pinned-pi-and-contract-tests.md`, `tools/pi/install.sh`, the pin, access policy, or the absent neutral-path extension. The runner performs final verification and the commit.

Explore's Stage-1 fallback was recorded by the runner as `claude-code-plan`, `claude-haiku-5-5`, after GLM 5.3 Flash twice returned `unrecognized_model` on 2026-11-21 (`research.md`); `decisions.md` names Sonnet instead, so the discrepancy remains recorded.

## Criterion ledger

- 1: not a test — phase-2 review audits the completed per-test inventory and its boundary-to-twin mapping; phase 6 repeats the audit
- 1: tests/test_pi_contract.py::test_shipped_catalog_prepares_both_swarms_offline — real listing fails to reach the production parser
- 1: not yet written tests/test_real_pi_data.py::test_real_refresh_store_reaches_overlay_reader — a Pi-produced store is rejected or its provider and models are lost
- 1: not yet written tests/test_real_pi_data.py::test_real_session_readbacks — real Pi help or bound-model output is rejected by its production reader
- 1: not yet written tests/test_real_pi_data.py::test_real_pi_version_reaches_production_check — the production version check rejects the pinned Pi
- 1: not yet written tests/test_real_pi_data.py::test_real_pi_error_reaches_rate_limit_classifier — real Pi stderr from loopback throttling is not classified
- 1: not yet written tests/test_real_pi_data.py::test_real_repository_pathlock_events — the real Pi event does not reach the production path lock
- 1: not yet written tests/test_real_pi_data.py::test_real_research_tool_events_and_execution — the real Pi event or tool input is misread by the production research extension
- 2: tests/test_stage2_go_access.py::test_session_lookup_reads_the_real_pinned_chat_catalog — the shipped `chat:` key does not resolve to the expected id and base
- 3: not yet written tests/test_real_pi_data.py::test_each_twin_refuses_missing_unstartable_or_wrong_pi — a counted twin skips, passes, or omits the install hint
- 4: not yet written tests/test_real_pi_data.py::test_unreadable_or_incompatible_pi_data_fails — a required missing, unreadable or incompatible file is accepted
- 5: not yet written tests/test_real_pi_data.py::test_real_pi_data_stays_on_loopback — an external connection or paid credential is required
- 6: not yet written tests/test_real_pi_data.py::test_each_twin_fails_on_its_inventory_fault — the same twin stays green after its specified fault is injected into scratch data or intercepted output

## Time used

2026-11-21 18:00:09–18:03:08 UTC, 179 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 22:26:50–22:30:05 UTC, 195 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 22:35:16–22:38:37 UTC, 202 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
