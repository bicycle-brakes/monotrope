---
title: "Spec — guard-test"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-0ho
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, repair, guard-test]
class: bounded
appetite: 2
adr_files: [docs/adr/0017-codex-repairs-taken-findings.md]
---

# Spec — guard-test

Test-only repairs over correct production code can carry a runner-executed
guard proof instead of failing the ordinary baseline-red requirement
(bead `coding-harness-0ho` — guard-test evidence for test-only repairs).
Research: `research.md`. Human answer: `decisions.md`, Q-1.

## Problem

The repair runner currently rejects a named test that passes against baseline
production code. Three test-only repairs encountered this on 2026-10-14/15;
one attempt changed production checker logic just to satisfy the proof.
The existing parser offers only ordinary tests or the separately authorised
`not a test` form, and `red_first` runs only the baseline-red invocation.
Evidence: `research.md`, "The question", "How the answer's fixed lines are
read today" and "How the red-first proof runs today", checked at
`a4b0780` on 2026-10-15.

## Terms

- **Ordinary proof:** the attempt's named test fails against baseline code.
- **Guard proof:** the same named test fails with a fault it plants when
  `STAGE2_PLANT_FAULT=1` and passes without that switch.
- **Baseline:** the commit captured at the start of the repair verb;
  both guard runs use its production files and the attempt's tests.

## Acceptance criteria

1. When a taken row is answered `<ID>: fixed — guard test — tests/<path>::<function>`, the runner recognises a guard proof for that row.
   *Refuted by:* a valid guard answer is rejected as an unknown fixed form or sent through ordinary baseline-red proof.
2. If a guard answer does not name a defined top-level `test_…` in a `tests/…/test_*.py` file, or that function's source does not contain `STAGE2_PLANT_FAULT`, the attempt fails with the row identified.
   *Refuted by:* an undefined function, a climbing path, or a switch present only in a different function is accepted.
3. When the runner proves a guard answer, it executes the named test against baseline production and the attempt's tests with `STAGE2_PLANT_FAULT=1` and requires pytest exit 1.
   *Refuted by:* no planted invocation runs, the repaired production files are used, or exit 0, 2, 3, 4 or 5 passes as the required failure.
4. When the planted invocation has the required failure, the runner executes the same test against the same baseline with `STAGE2_PLANT_FAULT` absent and requires exit 0.
   *Refuted by:* the second invocation is omitted, inherits an ambient switch, or a nonzero result is accepted.
5. If either guard invocation cannot start or exceeds the existing proof timeout, or the interpreter cannot import pytest, the guard proof fails with the row and failing stage identified.
   *Refuted by:* a startup error or timeout counts as a planted failure, or the diagnostic cannot distinguish the planted and unplanted runs.
6. When a guard proof succeeds or fails, the existing proof checkout cleanup and ref-preservation checks also hold for that proof.
   *Refuted by:* a checkout remains registered, failed removal is hidden, or a created or moved ref is silently accepted or deleted by cleanup.
7. When a guard repair passes all existing attempt checks, its full `fixed — guard test — …` status is written only to the taken rows in each of the existing three locations: private loop record, released loop rows and phase-6 findings.
   *Refuted by:* the mark is lost, an unrelated cell changes, a failed attempt marks a row fixed, or an already fixed guard row is selected again for repair.
8. When an answer uses an existing ordinary-test or `not a test` form, the existing evidence rules continue to apply.
   *Refuted by:* an unmarked baseline-green test passes, ordinary proof stops accepting exit 1 or 2, or a code row gains the unauthorised `not a test` escape.
9. While guard proofs are available, the repair instructions, findings vocabulary and operative repair doctrine state the guard spelling, both switch-controlled runs and the limit that phase 6 must check the planted fault is real.
   *Refuted by:* either repair route omits the guard form, operative documentation demands baseline red for every code row without the guard alternative, or it claims the runner proves fault semantics.

## Non-goals

- No runner-generated mutation, guarded-function naming interface, or proof-free exception.
- No attempt to establish automatically that the switch plants a meaningful fault; phase 6 inspects that, including rejection of a bare conditional failure.
- No migration of old findings, guard tests or criterion-ledger syntax.
- No routing, review-round, checkpoint or model-effort changes, and no new ADR.
- No design artifact: phase 2b does not run for the recorded `bounded` class.

## Protected areas

- `scripts/check_interview_minimums.py`, `decisions/adoption.yaml` and recorded human answers: the new proof cannot weaken governance or manufacture interview completion.
- `scripts/check_criterion_ledger.py`: plan-test references keep their grammar.
- Endpoint declarations, model routes and historical repair records: outside the evidence extension.
- ADR 0017's existing decision body: retain it; the agreed detail is a dated, explicitly proposed addendum, effective on merge.

## Definition of Done

- `make verify` green, with the criterion ledger's new tests executed and their refuting faults demonstrated.
- Updated with the code: `templates/findings.md`, `prompts/04-implement.md`, `docs/WORKFLOW.md`, and a dated detail addendum to `docs/adr/0017-codex-repairs-taken-findings.md`.
- The PR file list confirms protected areas and non-goals; the ADR touch makes this a decision PR, whose merge remains the maintainer's confirmation.
- The implementation PR closes the guard-test evidence task and its final commit carries `Closes-Bead: coding-harness-0ho`.
- Special runs: none; stand-in runner tests and real local pytest proof runs do not claim a live model repair.
- Phase 1a is complete for the planned ADR edit before phase 4 starts: five human answer records are required, and only one is currently recorded (2026-10-15).

## Open decisions

None open about the requested behavior; Q-1 fixes the switch and the proof form.

**Interview prerequisite, still unmet:** the agreed ADR 0017 note requires
four further substantive human answers before implementation. Phase 2 does
not conduct that interview. A draft-only green interview check, before the
ADR file changes, is insufficient evidence for the implementation gate.

- [DETAIL] The guard's planted run requires exit 1; collection/interruption exit 2 is not a guard failure demonstration. The ordinary path retains its existing exits 1 or 2.
- [DETAIL] Check the literal switch in the named function's source, without inferring its semantics; this makes the recorded minimal source check local to the evidence actually named.
- [DETAIL] Reuse the isolated baseline proof checkout for the two successive runs, with a fresh controlled environment per process; this extends the existing proof boundary without a new mutation mechanism.
- [DETAIL] Phase-4 appetite is two hours including repairs, with a stop at the limit; no earlier appetite was recorded.
- [DETAIL] Keep the bounded class and claim the agreed existing ADR file honestly; the additional interview debt is reported rather than evaded by deleting that scope.

These reversible details are proposed here with their reasons; no human
answer or architecture-decision answer is recorded by this draft.
