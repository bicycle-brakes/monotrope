---
title: "Spec — ci-caller-rule"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-8sxb
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-terra, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, ci]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — ci-caller-rule

Teach the existing script-caller rule and check it during an implement or repair attempt that adds a file under `scripts/`, so a violation reaches its retry (bead coding-harness-8sxb). Research: `research.md`. Decision: `decisions.md#Q-1`.

## Problem

- The implement prompt did not explain the caller rule although its test rejects a covered script without a caller or declared reason (`research.md`, inspected 2026-11-07; `decisions.md#Q-1`).
- A targeted attempt can pass without selecting the caller test, leaving an orphan to the later full verification (`scripts/stage2.py`, `targeted_selection` and `_targeted_body`, inspected at commit `065d6541` on 2026-11-21; phase-2a review SR-1).

## Terms

- **Added file:** a surviving tracked or untracked, non-ignored file under `scripts/` at any depth, absent from the attempt's comparison commit; staged additions and rename destinations count, but Git-ignored files do not.
- **Caller test:** `tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason`. Its current rule covers non-`test_` `.py` and `.sh` files directly under `scripts/` and accepts a literal script path in the generated CI workflow or local verification runner, or a reason in `ci_gates.OHNE_AUFRUFER`.
- **Targeted check:** the existing post-run verification for implement and repair; it falls back to full verification when its coverage cannot be established safely.

## Acceptance criteria

1. When an implementer reads `prompts/04-implement.md`, the English instruction explains the existing caller rule and its three accepted forms: a CI step through the orchestrator, a literal path in `scripts/verify_all.sh`, or a reason in `ci_gates.OHNE_AUFRUFER`, with the latter two writable by the attempt subject to existing checks.
   *Refuted by:* omitted or misleading guidance, a changed caller inventory, an omitted accepted form, or a direction for the attempt to edit the held CI source or generated workflow.
   *Basis:* `decisions.md#Q-1`; phase-2a review SR-2.
2. When an implement or repair attempt adds a file under `scripts/`, the caller test is selected for its cheap check.
   *Refuted by:* an untracked, staged, renamed, nested, non-Python or `test_`-prefixed added file does not select it, or multiple additions cause duplicate execution in the same pytest invocation.
   *Basis:* `decisions.md#Q-1`; phase-2a review SR-4.
3. When an attempt adds no file under `scripts/`, this rule adds no caller-test target to its existing selection.
   *Refuted by:* a modification or deletion alone adds a caller-test target, or a pre-existing selection source is lost.
   *Basis:* `decisions.md#Q-1`.
4. When the caller test runs, it applies the existing caller rule to the current worktree inventory and declarations.
   *Refuted by:* a covered orphan passes, a supported caller or valid declaration fails, or a substitute rule changes coverage.
   *Basis:* `decisions.md#Q-1`.
5. If the caller check fails or cannot be selected or run, the attempt is rejected before acceptance and its retry receives the failure.
   *Refuted by:* an orphan, selection error, missing test, launch error or timeout permits a checkpoint, or the retry omits the failure.
   *Basis:* `decisions.md#Q-1`; phase-2a review SR-3.
6. When an implement or repair attempt adds a file under `scripts/` and reaches a targeted check, that check includes the caller test.
   *Refuted by:* a targeted acceptance omits the caller test, or a red caller test is overridden by full verification.
   *Basis:* `decisions.md#Q-1`; phase-2a review SR-1.
7. If the new-file coverage guard or an earlier cheap check rejects an attempt with an added file under `scripts/`, the caller test also runs in that check round and any caller failure joins the same retry listing.
   *Refuted by:* an uncovered orphan or an orphan with a lint failure yields only the earlier failure, or either failure permits acceptance.
   *Basis:* phase-2a review SR-3.
8. When a caller test selected by this change reports an orphan, its test identifier and each offending script's bare name reach the retry prompt even if later output exceeds the ordinary diagnostic tail.
   *Refuted by:* output longer than 80 lines leaves the retry without the test identifier or without any reported offending name.
   *Basis:* phase-2a review SR-5 and SR-9–11.

## Non-goals

- Widen the existing caller test's inventory, alter its textual matching, exemptions or age checks, or translate its identifiers.
- Add a CI gate, model route, standalone caller rule or new permission; change draft or review verification.
- Require every accepted attempt to run full verification: the existing targeted route and its full fallback remain, with full verification before phase 6.
- Change the two-hour phase-4 appetite or create an ADR or design for this bounded change.
- Change full-verification diagnostics for caller failures outside the checks selected by this change.

## Protected areas

The attempt does not edit the held CI source, generated workflow or implement prompt; the orchestrator owns any permitted prompt edit. The local verification runner retains its existing command-list restriction.

## Definition of Done

- After an accepted implement attempt, the orchestrator edits the held prompt and runs the criterion-1 regression before phase 6; the criterion-ledger regressions and `PYTHON=.venv/bin/python3 make verify` pass after that edit.
- The existing caller rule and held-path policy remain intact; the pull request identifies the task and tracker changes.

## Open decisions

None open.

- [DETAIL] Compare non-ignored, surviving worktree files against the attempt's existing comparison commit, because that includes staged, untracked and renamed additions without treating caches as scripts.
- [DETAIL] Select the existing caller test for both cheap and targeted checks; preserve its identifier and each printed bare script name outside the ordinary output tail, because both are needed to act on a failure.
- [DETAIL] Retain the two-hour phase-4 stop from the original draft; the interview did not set an appetite.
