---
title: "Decisions — slip-counter"
category: decisions
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5.2, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verify-speed, targeted-check, run-log]
---

# slip-counter — Decisions

Class: bounded (bead coding-harness-bxxt.7).

## Q-1 · Derive the count or write slip records

asked: 2026-11-13
answer: "Ableiten statt schreiben (Empfohlen)" — no slip record of its own is written; a reader computes the count from what the local run log holds anyway: a green targeted check followed by a red full run on the same tree.
answered_by: maintainer
status: answered
context: |
  Topic: the slip counter counts faults the targeted check lets through and only the full check finds; it was split out of the change targeted-check-more-verbs on 2026-11-13.
  Intention: in that change the runner wrote a record per slip, and this writing drew five findings in six phase-6 re-checks (duplicates, failed appends, lost records); the maintainer asked for the most long-term build.
  Today: no counter exists on origin/main; the local run log (scripts/verify_duration.py) records full runs.
  Repository change: a reader over the run log; the targeted check leaves its result in the same log so the reader can pair it with the full run; no slip writer.
  Architecture change: none; the run log stays the one local history.

In the context of a counter whose own records drew five findings, facing a choice between taking the removed code up again and deriving the count at read time, we decided to derive it, to achieve a counter without a writer that can fail, accepting that the targeted check must leave its result in the run log. — 2026-11-13

## Q-2 · Incomplete runs in the asked interval

asked: 2026-11-13
answer: "Zahl plus Lücken (Empfohlen)" — the reader names the counted slips and, beside them, how many runs were incomplete and not counted; it never reports a bare zero while incomplete runs exist. The spec states this as a Boundary.
answered_by: maintainer
status: answered
context: |
  Topic: the last finding on the old counter (F6-12) was a reported zero when a red full run had lost its end record.
  Intention: five case repairs did not close the mechanism, so the spec gets a Boundary for incomplete evidence instead of a sixth case.
  Today: an incomplete run is silently skipped.
  Repository change: the reader's output and exit state distinguish "counted" from "not countable"; the night handover names both numbers.
  Architecture change: none.

In the context of runs that end without an end record, facing a choice between no number at all and a count with the gaps named, we decided for the count with the number of incomplete runs beside it, to achieve a figure that stays usable after one crash, accepting that the reader of the handover must look at two numbers. — 2026-11-13

## Decided by the agent

[DETAIL] **The implementation starts after the targeted-check change (bead coding-harness-0swp) is merged.** Reason: this change reads what that one writes; spec and plan are drafted before, on the branch state of origin/main.
