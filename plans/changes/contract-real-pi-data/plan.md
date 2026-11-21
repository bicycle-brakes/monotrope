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
For you:     Pi format and hook drift is caught using the pinned installation's own data.
Done when:   Every inventoried boundary has an offline real-data twin, fault checks turn red, and make verify passes.
Appetite:    4 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Production behavior repairs, paid calls, a Pi pin change, or replacing synthetic negative tests.
Pre-mortem:  suppose it failed: most likely because a shared fixture hides an uncovered Pi format boundary.
Starts unless you say stop.
```

## Files and steps

1. **Prerequisite:** `scripts/stage2_pi_neutral_paths.mjs` and its tests are absent at commit `5e7bd56d`; the orchestrator must first arrange an implementation base containing the neutral-path extension. Do not write a substitute extension, skip this obligation, or make an unrelated branch change inside the implement attempt.
2. In `plans/changes/contract-real-pi-data/spec.md`, complete the per-test inventory by tracing Pi file and hook stand-ins and shared fixtures across `tests/`, including session records, and map each to an existing or new twin. Identify which checks already exercise installed Pi; keep malformed synthetic cases. Stop and report any boundary that cannot be exercised with actual pinned data offline rather than silently narrowing criterion 1.
3. Create `tests/test_real_pi_data.py`: exercise the actual shipped Go catalog through `checked_session_model`; compare the binding to its `chat:`-keyed source. Exercise other inventoried formats through their production readers or Pi's real resolver. Generate a real `before_agent_start` rendering with the pinned Pi and run the production neutral-path extension on it, asserting the boundary and preserved instructions; use scratch home and agent directories, synthetic credentials and the existing loopback-only guard where a Pi launch needs transport. Reuse existing real-data tests when they prove a boundary, recording that mapping in the inventory.
4. In `tests/test_real_pi_data.py`, skip only the new twins when the installed package is genuinely absent, with the exact spec reason. A present but broken, wrong-version, unreadable or incompatible installation must fail; retain `tests/test_pi_contract.py` and its existing mandatory missing-prerequisite failures. Plant faults in the data, reader or rendered hook boundary and show that the relevant assertions fail; prohibit non-loopback connections.
5. Update this `plan.md` ledger as tests are written; preserve `findings.md` for the runner, and leave `## Time used` for phase 4. No files are deleted; no design or ADR is due for a bounded change.

## Verification and boundaries

Run the focused tests, including the existing real-Pi suite, and the repository verification with the pinned Pi installed:

```sh
.venv/bin/python3 -m pytest -q tests/test_real_pi_data.py tests/test_pi_contract.py tests/test_stage2_go_access.py
make verify
```

Also run the new twins with the installation absent in an isolated test setup and verify the exact skip reason without weakening existing tests. Verify fault injections for each inventoried format boundary and the rendered prompt. The runner performs final verification and the commit. Do not change `docs/adr/0019-repository-pinned-pi-and-contract-tests.md`, `tools/pi/install.sh`, the Pi pin, access policy, or any held path; no held-path edits are planned.

Explore used the Stage-1 fallback route, endpoint `claude-code-plan`, model `claude-haiku-5-5`, because GLM 5.3 Flash twice returned `unrecognized_model` on 2026-11-21 (`research.md`); `decisions.md` describes the fallback as Sonnet, so the discrepancy remains recorded rather than resolved by assumption.

## Criterion ledger

- 1: not yet written tests/test_real_pi_data.py::test_inventoried_boundaries_use_real_pi_data — an inventoried boundary is exercised only with a stand-in
- 2: not yet written tests/test_real_pi_data.py::test_neutral_paths_receives_pi_rendered_prompt — the production hook sees only a hand-written prompt
- 3: not yet written tests/test_real_pi_data.py::test_session_binding_uses_shipped_chat_catalog — a chat-prefixed model is not resolved from its shipped entry
- 4: not yet written tests/test_real_pi_data.py::test_missing_pi_skips_new_twins_with_reason — an absent install fails or gives a different skip reason
- 5: not yet written tests/test_real_pi_data.py::test_broken_installed_pi_fails_real_data_twins — corrupt or incompatible installed data is skipped or accepted
- 6: not yet written tests/test_real_pi_data.py::test_real_data_twins_deny_external_network — a non-loopback connection is allowed
- 7: not yet written tests/test_real_pi_data.py::test_format_drift_is_detected — an incompatible file or hook payload leaves its corresponding twin green

## Time used

2026-11-21 18:00:09–18:03:08 UTC, 179 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
