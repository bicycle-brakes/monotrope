---
title: "Decisions — adr-repair-check"
status: draft
implementation_status: none
date: 2026-11-08
last_reviewed: 2026-11-08
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-firy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, adr, repair, verification]
---

# adr-repair-check — Decisions

Class: architectural (bead coding-harness-firy). The change writes ADR 0025,
which amends ADR 0021 decision 6, so five counted interview records are
owed: Q-1 to Q-5 below. The maintainer answered all five in the conversation
on 2026-11-08, after deciding that the amendment travels in a decision pull
request of its own beside pull request #343 (bead coding-harness-gxwg).

## Q-1 · What the targeted check after a runner repair covers

context: |
  Topic: the scope of the check a runner repair passes instead of a full make verify.
  Intention: ADR 0025 should state the scope pull request #343 implements.
  Today: every runner repair runs the full make verify (12 to 13 minutes, measured 2026-10-30, plus the wait for the machine-wide lock).
  Repository change: the targeted check runs the whole test files linked to the touched files, the test selections of earlier retries, ruff on touched Python files and the gates the touched file kinds feed.
  Architecture change: a new verification rule in the runner.
asked: 2026-11-08
answer: "Ja, genau so (Recommended)" — the targeted check covers exactly the four parts named: linked test files, prior retry selections, ruff on touched Python files, the gates the touched file kinds feed.
answered_by: maintainer
status: answered

In the context of a full make verify after every runner repair, facing a choice between the linked scope, a scope with a fixed smoke set and a narrower scope without gates, we decided on the linked scope of pull request #343, to achieve short repair cycles with the full check before phase 6 as the net, accepting that an unlinked test fails only at that later check. — 2026-11-08

## Q-2 · When the full make verify runs instead

context: |
  Topic: the fallback from the targeted check to the full make verify.
  Intention: ADR 0025 should state when a selection is not safe.
  Today: there is no selection; every repair runs the full check.
  Repository change: the full make verify runs when a repair touches prompts, shared test configuration, shared execution infrastructure such as scripts/stage2.py, production code without a linked test or an unsupported file kind, or when the link map is incomplete.
  Architecture change: a runner verification rule.
asked: 2026-11-08
answer: "Ja, so (Recommended)" — the fallback list stands as named; repairs of scripts/stage2.py keep the full check.
answered_by: maintainer
status: answered

In the context of a targeted selection that cannot see every dependency, facing a choice between the named fallback list, a targeted check for scripts/stage2.py as well and a full check for every file outside tests/, we decided on the named fallback list, to achieve that the riskiest files keep the full check, accepting that repairs of scripts/stage2.py stay slow. — 2026-11-08

## Q-3 · The full make verify before phase 6

context: |
  Topic: the one full check that stays per change.
  Intention: keep a net for whatever a targeted check misses.
  Today: phase 6 starts without a fresh full run required on the head it reads.
  Repository change: the runner requires a fresh green full make verify on exactly the head the phase-6 reviewer reads; red, unstartable or timed out stops the review; runner audit lines in findings.md do not count as a new head.
  Architecture change: a runner verification rule.
asked: 2026-11-08
answer: "Ja, so (Recommended)" — one fresh green full run on the reviewed head before phase 6; audit-only lines in findings.md do not require a new run.
answered_by: maintainer
status: answered

In the context of targeted checks after each repair, facing a choice between one full run on the reviewed head, an extra full run before the pull request and a full run after every commit, we decided on one full run on the reviewed head with audit lines exempt, to achieve one full check per change instead of per repair, accepting that CI is the check after the merge with main. — 2026-11-08

## Q-4 · Measuring the effect

context: |
  Topic: whether the rule shortens repair cycles and lock waits.
  Intention: the effect is not measured; ADR 0025 should say when it is checked and when the rule returns to the maintainer.
  Today: lanes take 6 to 13 hours against 2 to 4 planned, mostly waiting for the verify lock (bead coding-harness-po0a).
  Repository change: after the merge the orchestrator measures repair duration, lock wait and how often the full check before phase 6 finds what a targeted check missed.
  Architecture change: none.
asked: 2026-11-08
answer: "Länger messen" — measure over five changes or two weeks, whichever comes first, then report to the maintainer.
answered_by: maintainer
status: answered

In the context of an unmeasured speed-up, facing a choice between three changes, five changes or two weeks, and no measurement, we decided to measure over five changes or two weeks, to achieve a reading that one unusual change cannot dominate, accepting a later report. — 2026-11-08

## Q-5 · The relation to the testing-strategy spike

context: |
  Topic: ADR 0025 and the testing-strategy spike (bead coding-harness-1ga5, why CI and make verify keep growing).
  Intention: the bead note said to write the amendment after the spike; it now comes first.
  Today: the spike waits for pull request #352 and has not started.
  Repository change: ADR 0025 takes effect on merge; the spike may amend or replace it with an ADR of its own, and the measurement of Q-4 enters the spike as a finding.
  Architecture change: the verification rule holds until the spike decides otherwise.
asked: 2026-11-08
answer: "Gilt jetzt, Spike darf ändern (Recommended)" — the rule holds from the merge; the spike may change it with its own ADR; the measurement feeds the spike.
answered_by: maintainer
status: answered

In the context of a pending testing-strategy spike, facing a choice between a rule that holds now, a rule that expires with the spike and a rule that ignores it, we decided that the rule holds now and the spike may amend it, to achieve the speed-up at once, accepting a possible second amendment. — 2026-11-08
