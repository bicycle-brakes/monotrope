---
title: "Plan — ci-caller-rule"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-8sxb
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, ci]
---

# Plan — ci-caller-rule

```text
For you:     New scripts with no caller or declared reason fail before full verification, and the implement prompt explains the rule.
Done when:   Tests prove early rejection and retry feedback, the prompt states the rule, and make verify is green.
Appetite:    2 hours of phase 4 in total, repairs included; a stop, not an estimate.
Not now:     Wider script coverage, identifier translation, new gates or changes to model routes.
Pre-mortem:  suppose it failed: most likely because untracked additions never reach the caller-test selection.
Starts unless you say stop.
```

Proposed against `286568f8`, inspected 2026-11-07. Class `bounded`: no design
or ADR. There is no `templates/plan.md`; this follows the phase-3 prompt.
Explore used Stage 2, GLM 5.3 Flash; no Stage-1 fallback was recorded.

## Files and steps

1. **Implement attempt:** create `tests/test_stage2_ci_caller.py`, using
   `World`, the process recorder and helpers from `tests/test_stage2.py`.
   Write the ledger tests below alongside the implementation; exercise both
   implement and repair without live models. Cover `.py` and `.sh`, untracked, staged and
   renamed additions, duplicate sources, exclusions and selection failure.
2. **Implement attempt:** change `scripts/stage2.py` only in cheap-test
   selection and its descriptions. In `selected_tests`, use `changed_paths`
   against `HEAD`, including untracked paths; select surviving direct
   `scripts/*.py` and `scripts/*.sh` files except `test_*`, and establish
   absence at `HEAD` with the existing `_git_bytes`/`ls-tree` pattern.
   A failed Git query is a selection fault, never evidence of absence.
   Add `tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason`
   to the existing target set before sorting and whole-file deduplication;
   a selected whole `tests/test_ci.py` already covers this function.
   Reuse the worktree's existing caller test, not a second caller parser.
3. Keep `cheap_checks`, `launch`, `PYTEST`, diagnostic protection, limits,
   findings, retry prompts, timing and full verification on their current
   paths. Test missing/uncollectable targets, red output, launch errors and
   timeouts through these paths; inspect command order, checkpoint absence
   and retry evidence. Test valid caller/declaration and orphan outcomes by
   executing the real caller test in an isolated temporary inventory; the
   `World` subprocess stand-ins alone do not prove its predicate.
4. **Implement attempt:** adjust `tests/test_stage2_fail_fast.py` and
   `tests/test_stage2.py` where fixtures adding scripts now select an extra
   target. Preserve earlier assertions and names; provide a minimal caller
   test in synthetic repositories where collection needs one. Do not
   globally disable or mock away the new selection to repair old tests.
5. **Orchestrator, bootstrap after the accepted attempt:** change
   `prompts/04-implement.md` beside its cheap-check instruction. State in
   English: every new non-`test_` `.py` or `.sh` directly under `scripts/`
   needs an existing supported caller or a reason in
   `ci_gates.OHNE_AUFRUFER`; new CI steps originate in
   `decisions/gates.yaml`, and the runner checks the rule before full
   verification. Remind the implementer to report a required held-path edit
   for the orchestrator. The guarded attempt never edits this prompt or
   changes held-path policy. Review the paragraph against criterion 1,
   then run the final verification again after this bootstrap edit.
6. **Bookkeeping:** update `plans/changes/ci-caller-rule/plan.md` as named
   tests land; the runner owns `plans/changes/ci-caller-rule/findings.md`
   audit entries and regenerates `plans/INDEX.md`. The latter is an
   orchestrator/runner derivation, not an implement-attempt task. No files
   are deleted; `research.md`, `decisions.md` and `spec.md` remain unchanged.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2_ci_caller.py tests/test_stage2_fail_fast.py tests/test_stage2.py
.venv/bin/python3 -m pytest -q tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
python3 scripts/check_interview_minimums.py --change ci-caller-rule
python3 scripts/check_criterion_ledger.py
PYTHON=.venv/bin/python3 make verify
```

The final full run follows the orchestrator's prompt edit. A green cheap run
never substitutes for it. Every regression names the planted fault below;
test selection alone is insufficient evidence of early rejection.

## Criterion ledger

- 1: not a test — phase-6 review reads the English paragraph in prompts/04-implement.md against criterion 1; missing guidance, widened coverage or manual workflow editing refutes it.
- 2: not yet written tests/test_stage2_ci_caller.py::test_new_scripts_select_the_caller_test_once — untracked, staged or renamed additions omit the target, or multiple additions and a ledger reference duplicate it; a whole-file target must also run it only once.
- 3: not yet written tests/test_stage2_ci_caller.py::test_other_changes_do_not_add_the_caller_test — modified, deleted, nested, JavaScript or test-prefixed paths activate the rule, or existing selection sources are lost.
- 4: not yet written tests/test_stage2_ci_caller.py::test_early_check_uses_the_existing_caller_rule — the real caller test accepts a planted orphan or rejects a valid CI, local-runner or declaration case in an isolated inventory.
- 5: not yet written tests/test_stage2_ci_caller.py::test_caller_failure_stops_before_full_verify_and_reaches_retry — implement or repair reaches make/checkpoint after a red caller check, or bounded, protected failure evidence is missing from the next prompt.
- 5: not yet written tests/test_stage2_ci_caller.py::test_caller_selection_and_execution_errors_reject_the_attempt — a Git selection failure, missing target, launch error or timeout becomes green or reaches full verification.
- 6: not yet written tests/test_stage2_ci_caller.py::test_green_caller_check_still_requires_full_verify — cheap green skips make verify or permits acceptance when full verification fails.

## Not touched

Keep the authoritative caller tests, exemptions, kit accounting and generated
CI unchanged: `tests/test_ci.py`, `scripts/ci_gates.py`,
`scripts/verify_all.sh`, `scripts/kit/probe.py`, `decisions/gates.yaml` and
`.github/workflows/ci.yml`. No new script, gate, workflow, ADR, design,
translation or model-policy change is needed.

## Time used
