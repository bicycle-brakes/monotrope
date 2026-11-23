---
title: "Plan — runner-preflight-gates"
status: draft
implementation_status: none
date: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, verification]
---

# Plan — runner-preflight-gates

```text
For you:     Draft, implement and repair stop before spending model calls when the starting documents fail a blocking check.
Done when:   Fake-model tests show the refusal and fix command, green paths still call the model, and make verify is green.
Appetite:    4 hours of phase 4 including repairs; a stop, not an estimate.
Not now:     Automatic fixes, new gate policy, model routing changes or replacing later verification.
Pre-mortem:  suppose it failed: most likely because a starting check rejects a legitimate draft before its files exist.
Starts unless you say stop.
```

Blocked pending the maintainer answer to the open decision in `spec.md`; the card and steps are provisional and phase 4 must not start yet. Class bounded: no design or ADR. There is no `templates/plan.md` in this tree; this follows the phase-3 prompt. Exploration used Stage 2, GLM 5.3 Flash; no Stage-1 fallback is recorded.

## Files and steps

1. `scripts/stage2.py` — add one shared starting-tree document check, invoked by draft, implement and repair before their first model call on every route. Select the registry gates with `subsets: [docs]` admitted by `ci_gates.declared_cheap`, and execute through `run_gates` with the existing document environment and draft ADR-answer tolerance. Refuse on selection errors, empty runnable set, applicable blocking failure, launch failure or timeout; resolve which failures are applicable after the maintainer answers the open decision; preserve actionable gate output including its fix command. Keep report-only enforcement. Do not call `prepare_derived`, stamp or otherwise modify the tree; do not require draft outputs that do not yet exist. Keep existing guards, leak checks, hand-only repair behavior, retry routes and post-run checks. Extend the shared executor's diagnostic handling if needed so the fix command survives bounded output, without creating a second gate executor.
2. `tests/test_stage2_preflight_gates.py` (new) — use the existing fake runner/world facilities and temporary trees to test each verb and both available route families, without network or real model calls. Exercise an actual stale `updated:` failure and assert its fix command, gate selection and execution failures, report-only enforcement, an absent draft spec and plan, a green path and unchanged starting files. Assert the call recorder and check execution order; do not mock away the behavior each test claims to measure.
3. `plans/changes/runner-preflight-gates/findings.md` — the orchestrator records the required reviews and outcomes; this file is runner-owned during attempts.

No edits to `decisions/gates.yaml`, endpoint declarations, prompts, templates, ADRs or the verification policy. The normal full check before phase 6 remains required.

## Criterion ledger

- 1: not yet written tests/test_stage2_preflight_gates.py::test_all_verbs_run_registry_document_gates_before_model — a verb calls the model first or omits a selected gate.
- 2: not yet written tests/test_stage2_preflight_gates.py::test_blocking_gate_stops_all_routes_without_model_calls — a red gate starts any model or fallback.
- 3: not yet written tests/test_stage2_preflight_gates.py::test_stale_document_refusal_shows_fix_command — the stale-date fix command is missing.
- 4: not yet written tests/test_stage2_preflight_gates.py::test_unavailable_checks_refuse_before_model — a selection, launch, interpreter or timeout failure permits a call.
- 5: not yet written tests/test_stage2_preflight_gates.py::test_green_start_proceeds_for_all_verbs — a passing check blocks a valid route, including a fresh draft without generated artifacts.
- 6: not yet written tests/test_stage2_preflight_gates.py::test_starting_check_does_not_write_tree — document bytes or paths change during the check.
- 7: not yet written tests/test_stage2_preflight_gates.py::test_report_only_gate_does_not_block — a reporting gate prevents the call.

## Verification

```sh
.venv/bin/python -m pytest -q tests/test_stage2_preflight_gates.py
make verify
```

## Time used

2026-11-23 17:16:42–17:19:19 UTC, 156 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-23 17:30:30–17:31:54 UTC, 85 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
