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

1. **Before implementation:** finish the inventory in `plans/changes/contract-real-pi-data/spec.md` and resolve review finding SR-7 in `plans/changes/contract-real-pi-data/findings.md`. Trace every shared-fixture user, direct stand-in and mocked Pi call to the production reader, classify it, and map it to a specific existing or planned twin; search `tests/` for Pi file names, CLI flags, hook events and subprocess mocks. Review the resulting list before phase 4. Do not treat the partial inventory as complete.
2. Create `tests/test_real_pi_data.py` for gaps established by that review: use the pinned wrapper and isolated temporary directories. Pass the real offline `--list-models` output to `stage2.parse_catalog`; pass the production session policy to `stage2_session.confirm_loaded` and its checked binding to `confirm_binding`. Exercise `overlay_store` on a store actually written by the pinned Pi using only a loopback source; if that cannot be produced offline, stop and report the gap rather than replace it with synthetic data. Cover any other uncovered boundary from the inventory with its actual pinned file or rendered event and its production reader. Reuse existing tests only where they exercise that boundary and field.
3. In `tests/test_real_pi_data.py`, use the existing `tests/test_pi_contract.py::require_installed_pi` prerequisite or equivalent behavior: absent, unstartable and wrong-version Pi fail with `bash tools/pi/install.sh`. Required unreadable or malformed files and failed renderings fail; never skip. Run with synthetic credentials and the existing loopback transport and network guard. In a scratch catalog, replace `chat:` keys with bare keys and assert the production session reader refuses it; do not alter the installed package.
4. Update the criterion ledger in `plans/changes/contract-real-pi-data/plan.md` when named tests are written. Phase 4 records its own time in `## Time used`. No files are deleted. No design or ADR is due for a bounded change. No held path is assigned to the implement attempt.

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
- 1: not yet written tests/test_real_pi_data.py::test_real_listing_reaches_catalog_parser — a real listing is rejected or parsed with the wrong provider and model
- 1: not yet written tests/test_real_pi_data.py::test_real_refresh_store_reaches_overlay_reader — a Pi-produced store is rejected or its provider and models are lost
- 1: not yet written tests/test_real_pi_data.py::test_real_session_readbacks — real Pi help or bound-model output is rejected by its production reader
- 2: tests/test_stage2_go_access.py::test_session_lookup_reads_the_real_pinned_chat_catalog — the shipped `chat:` key does not resolve to the expected id and base
- 3: not yet written tests/test_real_pi_data.py::test_missing_or_wrong_pi_fails_with_install_hint — a missing or wrong pin skips or omits the install hint
- 4: not yet written tests/test_real_pi_data.py::test_unreadable_or_incompatible_pi_data_fails — a required missing, unreadable or incompatible file is accepted
- 5: not yet written tests/test_real_pi_data.py::test_real_pi_data_stays_on_loopback — an external connection or paid credential is required
- 6: not yet written tests/test_real_pi_data.py::test_bare_catalog_keys_are_refused — a scratch catalog with bare keys resolves successfully
- 6: not a test — phase-6 review checks the fault demonstration for every inventoried format or payload boundary, including a raw payload where a rendered-payload twin exists

## Time used

2026-11-21 18:00:09–18:03:08 UTC, 179 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 22:26:50–22:30:05 UTC, 195 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
