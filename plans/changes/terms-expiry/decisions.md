---
title: "Decisions — terms-expiry"
status: draft
implementation_status: none
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-abra
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, model-terms, stage-2]
---

# terms-expiry — Decisions

Class: feature. The change amends ADR 0021 (the terms reading that admits a
paid model), so five counted interview records are owed: Q-1 to Q-5 below.

## Q-1 · A machine-readable expiry date on every terms record

context: |
  Topic: how long a model's terms reading stays valid.
  Intention: the DeepSeek zero-retention agreement is valid through
  2026-10-31, but the runner only checks that the retention text is not
  empty, so it would admit the model for ever (finding DL-B-13).
  Today: the expiry stands only as prose inside `aufbewahrung`.
  Repository change: `gilt_bis: YYYY-MM-DD` in each `modelle_terms` record;
  `terms_problem` skips a model whose date has passed and names it.
  Architecture change: the terms reading gains an end date (ADR 0021).
asked: 2026-10-25, conversation 2026-10-25 (night-run plan, answer 2)
answer: "Add a machine-readable gilt_bis: YYYY-MM-DD to each modelle_terms record; terms_problem skips a model whose gilt_bis has passed and names it; re-read the DeepSeek terms now and record the result"
answered_by: maintainer
status: answered

The re-read is in `research.md` ("Source re-read, 2026-10-25").

In the context of a terms reading with a fixed end, facing a runner that admits an expired reading for ever, we decided on a machine-readable `gilt_bis` that `terms_problem` checks, to achieve that an expired reading skips the model by name, accepting a date to maintain. — 2026-10-25

## Q-2 · A record without a date

context: |
  Topic: a terms record that carries no `gilt_bis`.
  Intention: decide whether the date is optional or required.
  Today: no record has the field.
  Repository change: `terms_problem` treats a missing `gilt_bis` like an
  expired one.
  Architecture change: part of the ADR 0021 amendment.
asked: 2026-10-26, conversation 2026-10-26 (interview)
answer: "Every model needs gilt_bis; a model without one is skipped"
answered_by: maintainer
status: answered

In the context of the paid-model admission, facing records without an end date, we decided that a missing `gilt_bis` skips the model, to achieve that no reading is valid by omission, accepting that every record must be dated. — 2026-10-26

## Q-3 · Who writes the date

context: |
  Topic: how a new or renewed `gilt_bis` reaches `model-endpoints.yaml`.
  Intention: the file is human-decided, so an agent cannot change it alone.
  Today: terms readings are written by the session that reads the source.
  Repository change: none in code; the procedure goes into docs/WORKFLOW.md.
  Architecture change: part of the ADR 0021 amendment.
asked: 2026-10-26, conversation 2026-10-26 (interview)
answer: "The agent re-reads the terms, with source and date, and proposes the entry as a decision pull request; the maintainer merges"
answered_by: maintainer
status: answered

In the context of the human-decided endpoint file, facing expiring readings, we decided that the agent re-reads and proposes each new date as a decision pull request, to achieve that the maintainer approves every reading, accepting one merge per renewal. — 2026-10-25

## Q-4 · A warning before the date

context: |
  Topic: when the maintainer learns that a reading is about to expire.
  Intention: a model should not drop out of the swarm without notice.
  Today: no warning exists.
  Repository change: the availability preparation and the review loop name
  each model whose `gilt_bis` is at most 7 days away.
  Architecture change: none beyond Q-1.
asked: 2026-10-26, conversation 2026-10-26 (interview)
answer: "The runner warns from 7 days before the date, naming the model and the date"
answered_by: maintainer
status: answered

In the context of the terms expiry, facing a model that would drop out unannounced, we decided that the runner warns from 7 days before its date, to achieve that a renewal can be merged in time, accepting a repeated warning line. — 2026-10-26

## Q-5 · The date when the source names none

context: |
  Topic: the `gilt_bis` of a model whose provider names no end date.
  Intention: Q-2 requires a date on every model, but most providers state
  none; only DeepSeek's footnote does.
  Today: a reading is valid for ever once written.
  Repository change: such a record gets `gilt_bis` = `gelesen` + 30 days.
  Architecture change: part of the ADR 0021 amendment.
asked: 2026-10-26, conversation 2026-10-26 (interview)
answer: "Read date plus 30 days"
answered_by: maintainer
status: answered

Recommended in the question, with the consequence named: the terms are
re-read monthly, matching DeepSeek's monthly renewal, at some upkeep per
model and month.

In the context of the paid-model admission, facing terms readings that
never expire, we decided that every record carries `gilt_bis` (the
source's date, or the read date plus 30 days), that a missing or passed
date skips the model and a date at most 7 days away is warned about, and
that renewals travel as decision pull requests, to achieve that no model
reviews code on an expired reading, accepting a monthly re-read per model.
— 2026-10-26

## Q-6 · `gilt_bis` beside the prose [DETAIL]

`gilt_bis` stands beside `aufbewahrung`; the prose keeps saying what the
source says ("valid through 2026-10-31"). Only `gilt_bis` binds. Removing
the prose would drop the source's own words from the record.

## Q-7 · The day itself [DETAIL]

A model is admitted on its `gilt_bis` day and skipped from the next day on,
compared in UTC. The DeepSeek footnote says "valid through October 31",
which includes that day.

Note (2026-10-27): the field the answers above call gilt_bis is named valid_until in the code, the declaration and the ADR (maintainer: repository artefacts are English).
