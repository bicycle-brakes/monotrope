---
title: "Spec — ci-caller-rule"
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
tags: [spec, stage-2, ci]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — ci-caller-rule

Teach the existing script-caller rule and reject an attempt that violates it
before full verification, so its retry receives the failure immediately
(bead coding-harness-8sxb). Research: `research.md`. Maintainer's decision:
`decisions.md#Q-1`, instruction plus runner check.

## Problem

- The implement prompt does not mention the caller rule, although the rule
  rejects scripts without a caller or declared reason; attempts discover it
  only during full verification (`research.md`, “What exists today” and
  “Related context from the night run”, inspected 2026-11-07).
- The rule already has one authoritative test, but ordinary cheap-test
  selection does not select it merely because an attempt adds a script;
  the maintainer chose an early check rather than another full verification
  failure (`research.md`, rule description; `decisions.md#Q-1`, answered
  2026-11-06 and recorded 2026-11-07).

## Terms

- **Covered script:** a non-`test_` file directly under `scripts/` with
  extension `.py` or `.sh`, matching the existing caller test's inventory.
- **New script:** a surviving covered script absent from the attempt's
  starting `HEAD`, including an untracked or staged addition and a rename
  to a new covered path.
- **Caller test:**
  `tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason`.
  It accepts a literal script path in the generated CI workflow or local
  verification runner, or an entry in `ci_gates.OHNE_AUFRUFER`.

## Acceptance criteria

1. When an implementer reads `prompts/04-implement.md`, it states in English
   that a new covered script needs a caller or a reason in
   `ci_gates.OHNE_AUFRUFER`, with CI steps declared through the gate source
   rather than hand-editing the generated workflow.
   *Refuted by:* the instruction is absent, changes the existing inventory,
   or directs a hand edit of the generated workflow.
   *Basis:* `decisions.md#Q-1`.
2. When an implement or repair attempt adds at least one new script, its
   cheap pytest selection covers the caller test exactly once.
   *Refuted by:* an untracked, staged or renamed addition omits the target,
   multiple additions duplicate it, or an existing ledger target is duplicated.
   *Basis:* `decisions.md#Q-1`.
3. When an attempt adds no new script, this rule contributes no extra pytest
   target beyond the existing changed-test, ledger and retry selections.
   *Refuted by:* a modification, deletion, nested script, `.mjs` file or
   `test_` file alone activates the new selection rule.
   *Basis:* `decisions.md#Q-1`.
4. When the early caller test runs, it applies the existing caller rule to
   the worktree's current inventory and declarations.
   *Refuted by:* an orphan passes early, a valid existing form of caller or
   declaration fails early, or the runner substitutes a different rule.
   *Basis:* `decisions.md#Q-1`.
5. If selecting or running the early caller check fails, the attempt follows
   the existing cheap-check rejection path before `make verify`.
   *Refuted by:* full verification or an acceptance checkpoint follows a red
   check, a selection error, a missing test, a launch error or a timeout;
   or the protected caller failure is absent from the retry prompt.
   *Basis:* `decisions.md#Q-1`.
6. When the early caller check and other cheap checks pass, full verification
   remains required before accepting the attempt.
   *Refuted by:* cheap green accepts without `make verify` or despite its failure.
   *Basis:* `decisions.md#Q-1`.

## Non-goals

- Widen the caller rule to JavaScript, subdirectories or other extensions;
  replace its textual matching; change its exemptions or age checks.
- Translate or rename existing German identifiers, including
  `OHNE_AUFRUFER`; that remains separate translation work.
- Add a gate, CI step, attempt, model route, standalone checker or discovery
  of tests importing changed scripts; change draft or review verification.
- Guarantee a wall-clock duration or replace full verification.
- Design phase 2b and an ADR: this bounded change reuses existing selection,
  pytest execution and failure handling without changing architecture.

## Protected areas

`tests/test_ci.py`, `scripts/ci_gates.py`, `scripts/verify_all.sh` and
`scripts/kit/probe.py` retain the existing rule and kit accounting.
`decisions/gates.yaml`, `.github/`, `provenance.yaml` and runner-held path
policy remain unchanged; no new gate or permission is needed.

## Definition of Done

- The criterion-ledger regressions and `PYTHON=.venv/bin/python3 make verify`
  pass; tests exercise selection and the real caller predicate with planted faults.
- The orchestrator's English instruction in `prompts/04-implement.md` lands
  in the same pull request; no living capability spec or ADR changes.
- The pull request's file list demonstrates the non-goals and protected areas.
- The final implementation commit carries `Closes-Bead: coding-harness-8sxb`;
  the pull request names the bead and any tracker changes. Special runs: none.

## Open decisions

None open. The maintainer's recorded answer is not reinterpreted.

- [DETAIL] Preserve the existing inventory, and use absence at starting
  `HEAD` to define additions; this makes the new check predictable without
  widening the rule to the JavaScript gap noted in research.
- [DETAIL] Add the test through shared implement/repair cheap-test selection,
  because both already use the same verification and retry mechanism.
- [DETAIL] Allow two hours of phase 4, repairs included, as a stop; no
  appetite was specified in the interview.
