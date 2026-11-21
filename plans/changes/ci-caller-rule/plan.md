---
title: "Plan — ci-caller-rule"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-8sxb
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-terra, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, ci]
---

# Plan — ci-caller-rule

```text
For you:     Added files under scripts trigger an early caller check, and the implement prompt explains how to satisfy the rule.
Done when:   Tests prove selection, rejection and useful retry feedback, the prompt states the rule, and make verify is green.
Appetite:    2 hours of phase 4 in total, repairs included; a stop, not an estimate.
Not now:     Wider caller-rule coverage, identifier translation, new gates or model routes.
Pre-mortem:  suppose it failed: most likely because an earlier failure hides the orphan from the retry.
Starts unless you say stop.
```

Class `bounded`: no design or ADR. No `templates/plan.md` exists in this tree; the card and sections follow the phase-3 prompt. Explore used Stage 2, GLM 5.3 Flash, with no Stage-1 fallback recorded.

## Files and steps

1. **Implement attempt — `scripts/stage2.py`:** use the existing changed-path and baseline-inventory helpers with the attempt's `against` commit to detect surviving added files anywhere below `scripts/`, including staged, untracked and rename destinations. A query or inspection failure must reject rather than silently prove no addition. Share this detection across cheap and targeted selection, and keep existing target sources and whole-file deduplication. Add the existing caller test to the cheap selection and to targeted test files; a full fallback retains its existing coverage.
2. **Implement attempt — `scripts/stage2.py`:** use the existing pytest execution and diagnostic protection to run the caller test even when the new-file coverage guard or an earlier cheap check is red, and combine both failures in the same retry listing. Do not permit a red, uncollectable, unstartable or timed-out caller check to reach a checkpoint or be overridden by full verification. Protect the caller test identifier and each reported orphan path from the ordinary 80-line output-tail cut; continue to scrub secrets and bound other diagnostics. On the green path retain the existing targeted check, fallback and phase-6 full verification.
3. **Implement attempt — `tests/test_stage2_ci_caller.py`:** create the ledger tests below using isolated repositories and the existing stage-2 fixtures; cover both implement and repair, all addition forms, no-addition controls, whole-file deduplication, real caller-rule outcomes, guard and lint failures, and long output. Exercise actual post-run ordering and retry evidence, not selection alone.
4. **Implement attempt — `tests/test_stage2_fail_fast.py` and `tests/test_stage2.py`:** adjust only fixtures and expectations affected by the new check; synthetic repositories must have a collectable caller test, and earlier assertions must remain effective.
5. **Orchestrator after the accepted attempt — `prompts/04-implement.md`:** add English guidance on the existing covered inventory, supported caller or reason in `ci_gates.OHNE_AUFRUFER`, and early check. Explain that a CI step is declared via `decisions/gates.yaml` and generated into `.github/workflows/ci.yml`, both held for the orchestrator; the attempt may supply an appropriate reason for an unwired script. Do not ask the attempt to edit a held path.
6. **Runner/orchestrator — `plans/changes/ci-caller-rule/plan.md`, `plans/changes/ci-caller-rule/findings.md`, `plans/INDEX.md`:** update ledger markers as tests land, record review outcomes and regenerate the index through the existing runner; no file is deleted. Re-run full verification after the orchestrator's prompt edit.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2_ci_caller.py tests/test_stage2_fail_fast.py tests/test_stage2.py
.venv/bin/python3 -m pytest -q tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
python3 scripts/check_interview_minimums.py --change ci-caller-rule
python3 scripts/check_criterion_ledger.py
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: not a test — phase-6 review checks the English prompt, both remedies and the held-path handoff; absent or misleading guidance refutes it.
- 2: not yet written tests/test_stage2_ci_caller.py::test_added_files_select_caller_in_cheap_check — staged, untracked, renamed, nested, non-Python or test-prefixed additions omit it, or duplicate sources run it twice in one invocation.
- 3: not yet written tests/test_stage2_ci_caller.py::test_no_addition_does_not_select_caller — a modification or deletion adds it, or another existing selection source disappears.
- 4: not yet written tests/test_stage2_ci_caller.py::test_existing_caller_rule_checks_current_inventory — the real caller test accepts a planted orphan or rejects a valid CI, local-runner or declaration case.
- 5: not yet written tests/test_stage2_ci_caller.py::test_caller_failure_or_error_rejects_and_reaches_retry — an orphan, selection fault, missing test, launch error or timeout reaches acceptance or loses its retry diagnostic in implement or repair.
- 6: not yet written tests/test_stage2_ci_caller.py::test_targeted_check_includes_caller_for_added_file — targeted acceptance omits the caller test, duplicates its whole-file selection, or a targeted red is overridden by full verification.
- 7: not yet written tests/test_stage2_ci_caller.py::test_guard_and_cheap_failure_also_report_caller — an uncovered orphan or lint-failing orphan produces only the earlier failure or reaches acceptance.
- 8: not yet written tests/test_stage2_ci_caller.py::test_retry_keeps_caller_identity_and_orphan_paths_after_long_output — over 80 later lines hide the caller identifier or an offending path, or sensitive output bypasses diagnostic protection.

## Not touched

Keep `tests/test_ci.py`, `scripts/ci_gates.py`, `scripts/verify_all.sh`, `scripts/kit/probe.py`, `decisions/gates.yaml`, `.github/workflows/ci.yml`, held-path policy, research and decisions unchanged. No new script, gate, workflow, ADR, design, translation or model-policy change is needed.

## Time used

2026-11-21 22:49:39–22:52:03 UTC, 143 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
