---
title: "Spec — guard-test"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-0ho
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, repair, guard-test]
class: feature
appetite: 3
change: guard-test
adr_question: {proposed: "yes", reason: "An explicitly authorised guard proof qualifies ADR 0017's baseline-only repair evidence contract."}
adr_files: [docs/adr/0023-guard-proof-for-test-only-repairs.md]
neighbours: []
---

# Spec — guard-test

The goal: the repair runner can prove a test-only fix by a real fault planted
by its test, without weakening baseline proof for ordinary code repairs
(bead coding-harness-0ho, test-only repairs; also coding-harness-y17,
test-strength findings). Sources: `research.md` and `decisions.md#Q-1`–`Q-5`.

## Problem

The research refreshed on 2026-10-29 against `5f57f4e9` records three
test-only repairs whose correct tests were green on correct baseline code.
The runner rejected them; one attempt moved checking logic into production
code merely to obtain baseline red. Accepting pytest's own failed outcome
has since fixed a different cause, not this one (`research.md`, "Refresh
against main" and "The question").

At this draft's baseline `9987eaca`, repair still accepts only ordinary test
and `not a test` fixed lines. Its private probe already proves named-test
outcomes, and `fixed_test_proof` already proves green on the attempt's code.
The missing capability is an authorised planted-fault proof on that code.
The environment allow-list drops caller-supplied planting switches; the
runner must explicitly supply one only to the planted run (research refresh).

## Terms

- **Guard test:** a test-only repair's test which plants a real fault in
  what it exercises only under `STAGE2_PLANT_FAULT=1`.
- **Authorised row:** a finding taken by the orchestrator as
  `taken — guard test — <reason>`, with a nonempty reason.
- **Qualifying red:** exit 1 and runner-owned evidence of a completed,
  nonempty run of the named test only, with at least one call failing by
  Python's `AssertionError` or pytest's own `pytest.fail.Exception`, all
  other calls passing or failing in those ways, and passing setup and
  teardown throughout; skips, xfail, XPASS and collection errors do not qualify.
- **Clean green:** exit 0 and the same invocation-bound evidence with every
  selected setup, call and teardown passing, without the planting switch.

## Acceptance criteria

1. When an authorised row is answered
   `fixed — guard test — tests/<path>::<function>` with a defined named test,
   the runner recognises that form as a guard-proof request.
   *Refuted by:* a valid guard answer rejected as an unknown fixed form.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-2`.
2. If a row has not been explicitly authorised as a guard test, its guard
   answer is refused before any guard-proof run.
   *Refuted by:* an ordinary or `not a test` row obtaining the guard route,
   including a missing-reason or merely quoted guard marker.
   *Basis:* `decisions.md#Q-2`.
3. When an authorised guard repair is proved, its named test produces
   qualifying red on the attempt's code with `STAGE2_PLANT_FAULT=1`.
   *Refuted by:* baseline code used instead of the attempt's code, a switch
   omitted from the planted run, or green accepted as planted proof.
   *Basis:* `decisions.md#Q-1`; research refresh, "Where the guard proof would run".
4. When the planted proof succeeds, the same named test produces clean
   green on the attempt's code before the repair is marked proven.
   *Refuted by:* a failing, skipped or expected-failing clean test receiving
   the evidence mark, or the clean run inheriting the switch.
   *Basis:* `decisions.md#Q-1`.
5. If either guard run lacks valid proof under the existing probe, tool,
   tree, ref, timeout or diagnostic-scrubbing safeguards, the attempt is refused.
   *Refuted by:* a setup crash, missing helper, exit alone, stale or malformed
   record, empty/foreign selection, changed tool/tree/ref, timeout or raw
   secret-bearing diagnostic being accepted as proof.
   *Basis:* `decisions.md#Q-1`; research refresh, existing proof safeguards.
6. If the named guard test's source does not contain `STAGE2_PLANT_FAULT`,
   the runner refuses its guard proof.
   *Refuted by:* a different test's switch reference satisfying this check.
   *Basis:* `decisions.md#Q-1` (source-presence check, not semantic proof).
7. When both guard runs and the existing repair post-checks succeed, the
   row retains the canonical guard fixed status and a distinct proof mark
   `yes — guard test — tests/<path>::<function>` in its existing location.
   *Refuted by:* a normal baseline-proof mark, a lost guard status, a change
   to an unrelated row, or any fixed status/positive mark after failed proof.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-2`; research refresh, fixed-code mark.
8. When an ordinary test repair or a `not a test` repair is processed, its
   existing evidence and authorisation rules continue to apply.
   *Refuted by:* a green-on-baseline ordinary repair accepted, a text answer
   accepted for a code row, or an ordinary proof run receiving the switch.
   *Basis:* `decisions.md#Q-2`, `decisions.md#Q-4`.
9. When phase 6 reviews guard tests introduced or changed by the change
   under review, its recorded verdict includes one evidence line per test
   naming the real fault and whether it catches that fault without the switch.
   *Refuted by:* a test omitted, a line naming no fault, or evidence lost or
   rejected by the runner even alongside `No finding.`.
   *Basis:* `decisions.md#Q-3`.
10. If a guard test merely fails conditionally without planting a real fault,
    phase 6 reports a BLOCKER.
    *Refuted by:* a bare `if switch: assert False` accepted as meaningful
    guard evidence, even though its two runner executions meet red/green.
    *Basis:* `decisions.md#Q-3`.
11. If `STAGE2_PLANT_FAULT` is present in the verification environment,
    blocking verification fails locally and in hosted CI.
    *Refuted by:* any present value, including empty or `0`, passing the
    gate, or the gate being absent/nonblocking on either verification path.
    *Basis:* `decisions.md#Q-5`.
12. When a guard repair is kept, its planting branch remains repeatable
    under the documented repair-only contract.
    *Refuted by:* removal of the branch after proof, conflicting status or
    proof instructions, or guard status becoming valid criterion-ledger syntax.
    *Basis:* `decisions.md#Q-1`–`Q-5`.

## Non-goals

- Guard proof for initial implementation or the criterion ledger; their
  evidence rules change only through separate work (Q-4).
- Runner-generated fault patches, replacing a guarded function on the
  runner's authority, old-versus-new test comparison, or proof-free exceptions.
- Automatic judgment of fault meaning; the runner checks source presence
  and execution evidence, while phase 6 judges the real fault (Q-1, Q-3).
- Reclassifying ordinary repairs, changing model routes/retries, weakening
  checkpoint protection, changing dependencies, probe outcome classes or
  the findings-table schema; mass conversion of historical tests or records.

## Protected areas

- `scripts/check_criterion_ledger.py` and ADR 0013: no new evidence grammar.
- `AGENTS.md`, `model-endpoints.yaml`, `provenance.yaml`, tracker state and
  other change folders: unrelated policy and historical evidence stay intact.
- Existing ADR bodies, including ADR 0017: the proposed amendment is a
  separate draft, not an agent edit to an accepted decision.
- Runner-held paths, including `decisions/gates.yaml`, `prompts/`,
  `templates/` and `.github/`, remain protected during model attempts;
  required coordinated updates are listed in the plan, not a guard bypass.

## Definition of Done

- `make verify` green with the switch absent; the presence gate demonstrably
  red with it set, including an empty value, locally and in generated CI.
- Coordinated documents: `docs/WORKFLOW.md`, `prompts/04-implement.md`,
  `prompts/04b-review-loop.md`, `prompts/06-review.md`, `templates/findings.md`,
  and proposed `docs/adr/0023-guard-proof-for-test-only-repairs.md`.
- The PR file list confirms protected limits and non-goals; no models change.
- The PR closes test-only repair and test-strength work (coding-harness-0ho
  and coding-harness-y17); its closing commit carries their `Closes-Bead` trailers.
- Measured planted-red/clean-green proof, refusal controls and ordinary
  repair regressions name the tested commit in the PR; phase 6 checks the
  meaning of every guard test added or changed by implementation.

## Open decisions

None open about behaviour: Q-1 through Q-5 remain the maintainer's answers.
The feature's formal ADR answer is still owed; this draft records no answer.

- [DETAIL] Three hours of phase 4, repair rounds included, is the appetite
  stop: the work crosses proof execution, review output and verification.
- [DETAIL] Use the existing attempt-tree proof machinery for both guard
  executions, avoiding a new temporary-checkout lifecycle.
- [DETAIL] The distinct proof mark names guard evidence rather than claiming
  a baseline failure; the existing findings columns suffice.
- [DETAIL] The current feature draft proposes a numbered amendment of ADR
  0017, using the runner's single-new-ADR rule. This packages the Q-1–Q-5
  addendum without editing the accepted record; it introduces no further
  behavioural choice and does not turn the old bounded-class context into
  a maintainer answer to this feature's ADR question.
