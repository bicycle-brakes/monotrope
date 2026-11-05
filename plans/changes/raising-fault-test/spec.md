---
title: "Spec — raising-fault-test"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-xrzf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, repair, red-first]
class: bounded
appetite: 1
adr_files: []
---

# Spec — raising-fault-test

The goal: implementers and repair models are told how to express a raising
fault as a regression test's failed expectation without changing the runner's
red-first rule (bead `coding-harness-xrzf`). Sources: `research.md` and
`decisions.md`, especially the reasoned interview skip of 2026-11-03.

## Problem

The exploration of 2026-11-03 locates the baseline-proof rule in
`scripts/stage2.py` (`RED_PROBE_SOURCE`, `_red_record_fault`, `red_first`):
an assertion or pytest's own failed outcome qualifies, an application crash
does not. It also locates the repair instructions and the separate guard-test
change. The interview skip resolves the exploration's uncertainty about intent:
both repair models failed to prove a regression whose baseline raised
`ValueError` on 2026-11-03. At `85a344b7`, the implement prompt and shared
repair instructions require baseline failure but omit how to express that case.

## Acceptance criteria

1. When an implementer reads `prompts/04-implement.md`, it contains one sentence telling them to catch the fault's specific exception in the regression test body and fail with `assert` or `pytest.fail`.
   *Refuted by:* the prompt omits catching the exception, omits either failure form, or treats the uncaught application exception as sufficient proof.
2. When either repair route receives its runner instructions, the same guidance is present for both Codex and the file-tools route.
   *Refuted by:* either repair instruction variant lacks the guidance or tells the model to accept the raising fault as a passing test.
3. When the runner classifies baseline proof, its existing distinction between a test's failed expectation and an execution problem remains unchanged.
   *Refuted by:* a clean assertion or pytest failed-outcome run is refused, or an unrelated exception, setup/teardown error, skip or incomplete run qualifies as red.

## Non-goals

- Implementing guard tests, planted-fault switches, new proof forms or gates.
- Repairing the motivating finding or changing another change's tests.
- Changing proof classification, status grammar, routing or retry policy.
- A design document or ADR: phase 2b does not run for this bounded change.

## Protected areas

The runner's probe and proof-classification/execution functions stay untouched:
the maintainer retained their rule. All paths outside the plan's file list,
including other change folders, workflow doctrine, gate definitions and ADRs,
stay untouched because this change only clarifies model instructions.

## Definition of Done

- The prompt tests reject planted omissions and pass on the completed instructions.
- Existing baseline-proof regressions and `make verify` pass after the orchestrator's prompt edit.
- Documents moved with the code: `prompts/04-implement.md`; no models or ADRs.
- The pull request's file list respects the protected areas and non-goals.
- The pull request closes the regression-instruction task (bead `coding-harness-xrzf`); its last commit carries `Closes-Bead: coding-harness-xrzf`.
- Special runs: none beyond the named prompt mutations and baseline-proof regressions.

## Open decisions

None open. The maintainer's intent is recorded in `decisions.md`; no new answer is required.

[DETAIL] Use one hour of phase 4, repairs included, as the appetite because this is two instruction insertions and focused prompt coverage; reaching it stops work.
[DETAIL] Catch only the specific exception caused by the fault, in the test body, so unrelated setup errors remain visible; do not recommend a blanket exception handler.
[DETAIL] Put the repair sentence in shared `REPAIR_ANSWER` so both existing repair instruction variants receive it without separate copies.
