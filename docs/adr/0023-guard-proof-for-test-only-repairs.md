---
title: "ADR 0023 — Guard proof for test-only repairs"
category: adr
status: accepted
created: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage2, repair, guard-test]
---

# ADR 0023 — Guard proof for test-only repairs

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, open is proposed and closed is rejected. Adds the guard
  proof exception to ADR 0017, decision 4; amends no D- or O-number and
  supersedes no ADR. The existing proof principle and routing remain.
* Review: the maintainer chose the guard behaviour in Q-1–Q-5 of
  `plans/changes/guard-test/decisions.md` on 2026-10-15/16 and retained those
  answers for the feature redraft on 2026-10-29. This numbered addendum and
  the feature's ADR question remain proposals, not a recorded ADR answer.
  Acceptance is the merge commit; the review header remains pending.
  Decider: maintainer · prepared by Codex.
* Date: 2026-10-29 · takes effect on merge.

## Context

A correct guard test over correct production code cannot fail on baseline.
The research refreshed against `5f57f4e9` on 2026-10-29 documents test-only
repairs refused for that reason and an attempt to move checker logic into
production merely to satisfy red-first. The runner now proves real pytest
outcomes and fixed-code green, but neither capability supplies this missing
test-strength proof (`plans/changes/guard-test/research.md`).

## Decision Drivers

* Every taken finding needs evidence, including a repair confined to tests.
* Only the orchestrator may authorise the exception; a repair model cannot
  evade ordinary baseline proof.
* Execution evidence and semantic review have distinct responsibilities.
* A retained planting branch must never make a planted verification green.

## Considered Options

* **Test-owned planted fault with explicit authorisation and review** — the
  maintainer's choice; repeatable and compatible with general guard tests.
* **Runner-owned mutation or replacement of a named checker** — rejected;
  constrains what can be guarded and gives the runner fault-construction work.
* **Accept green-only test repairs** — rejected; proves no ability to catch
  the fault and weakens the evidence rule.

## Decision

Chosen option: "Test-owned planted fault with explicit authorisation and
review", because it proves test-only repairs without modifying correct
production code or granting an unproved exception.

1. Only `taken — guard test — <reason>` authorises
   `fixed — guard test — tests/<path>::<function>` (Q-2).
2. The runner requires the switch reference in the named test and proves
   that test on the attempt's code: qualifying red with
   `STAGE2_PLANT_FAULT=1`, then clean green with the variable absent (Q-1).
   Existing outcome, environment, runtime and integrity safeguards apply.
3. Phase 6 reads every added/changed guard test and records its real fault
   and whether it catches that fault without the switch. A bare conditional
   failure is a BLOCKER (Q-3).
4. This form applies only to repair. Initial implementation and criterion
   ledgers retain their rules (Q-4).
5. Planting branches remain repeatable; a blocking local/hosted verification
   gate refuses the switch's presence, regardless of its value (Q-5).

## Consequences

* Ordinary code repairs still owe baseline-red and fixed-green proof;
  `not a test` keeps its existing authorisation and separate review.
* The runner proves executions, not fault meaning; mandatory semantic review
  costs time for every guard test and remains necessary even after both runs.
* Guard statuses and evidence marks distinguish this proof without adding
  findings columns. The gate and protected doctrine updates need coordinated
  ownership outside model attempts; no checkpoint guard is relaxed.

## Validation

* The guard-test spec's twelve criteria and the plan's criterion ledger
  cover authorisation, both proof legs, refusal controls, bookkeeping,
  review evidence, ordinary repairs and verification-gate presence.
* `make verify` must be green without the switch; isolated gate tests must
  demonstrate failure for `1`, empty and `0` values and both verification paths.
* Phase 6 records each new guard test's actual fault. The maintainer's merge
  decides this proposal; no draft or passing test records an ADR answer.
