---
title: "Decisions — adr-0016-docs-check"
category: decisions
status: draft
implementation_status: done
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-v9xx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, adr]
---

# adr-0016-docs-check — Decisions

Class: bounded, and an ADR change: it claims `docs/adr/0016-*.md`, so five
counted answers are owed. The maintainer gave five confirmations in the 15:00
block on 2026-11-01, about 15:40 UTC; they stand in the notes of bead
`coding-harness-v9xx` and are recorded here as given. On 2026-11-03 the
maintainer asked for the decision pull request to be opened from this text.

## Q-1 · What decision 3 names

asked: 2026-11-01
answer: "ja" — decision 3 names the draft's document check, `bash scripts/verify_all.sh --job docs`, instead of `make verify`.
answered_by: maintainer
status: answered
context: |
  Topic: ADR 0016 decision 3 says the draft runner sets ADR_ANSWERS_TOLERATE_CHANGE for its make verify.
  Intention: the record should say what the runner does since the draft-gates-only change.
  Today: the draft runner runs the document subset of the verify job, not make verify.
  Repository change: one sentence in ADR 0016.
  Architecture change: none; the ADR follows the code.

In the context of ADR 0016 decision 3, facing a record that names make verify while the draft runner runs the document subset, we decided to name `bash scripts/verify_all.sh --job docs` there, to achieve a record that matches the code, accepting an in-place edit of an accepted ADR. — 2026-11-01

## Q-2 · Decisions 2 and 7

asked: 2026-11-01
answer: "ja" — decisions 2 and 7 are corrected in the same pull request only where the runner's code reads differently, each with its evidence in the pull request.
answered_by: maintainer
status: answered
context: |
  Topic: decisions 2 and 7 of ADR 0016 also name make verify for the draft.
  Intention: one correction, not three pull requests.
  Today: verify_draft runs DOCS_VERIFY in both places.
  Repository change: two more sentences in ADR 0016.
  Architecture change: none.

In the context of decisions 2 and 7, facing the same wrong name for the draft's check, we decided to correct them in the same pull request where the code reads differently, to achieve one correction instead of three, accepting a slightly larger decision pull request. — 2026-11-01

## Q-3 · In place or as a new record

asked: 2026-11-01
answer: "in place" — ADR 0016 is amended in place.
answered_by: maintainer
status: answered
context: |
  Topic: whether the correction is a new ADR or an edit of ADR 0016.
  Intention: no behavior changes, so a new record would only add a pointer.
  Today: ADR 0016 is accepted.
  Repository change: an edit of docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md.
  Architecture change: none.

In the context of a correction without a behavior change, facing a new record or an edit, we decided to amend ADR 0016 in place, to achieve one place that is true, accepting that the edit must stay visible by a note. — 2026-11-01

## Q-4 · A dated note

asked: 2026-11-01
answer: "ja" — with a dated note "Amended 2026-11-01" naming bead coding-harness-77qj and saying there is no behavior change.
answered_by: maintainer
status: answered
context: |
  Topic: how a reader sees that the text changed after acceptance.
  Intention: an in-place edit must stay visible.
  Today: ADR 0016 carries no amendment note.
  Repository change: one quoted note after the Decision section.
  Architecture change: none.

In the context of an in-place edit of an accepted record, facing a silent change, we decided on a dated amendment note naming the draft-gates-only work item, to achieve a visible history, accepting one more paragraph in the ADR. — 2026-11-01

## Q-5 · The pull request

asked: 2026-11-01
answer: "ja" — a decision pull request `decide(adr-0016): …` with the label `decision`; the maintainer merges.
answered_by: maintainer
status: answered
context: |
  Topic: ADR 0016 is human-decided, so the edit takes effect only by the maintainer's merge (ADR 0008).
  Intention: the decision path the house rules require.
  Today: no pull request open.
  Repository change: the decision pull request carrying this folder and the ADR edit.
  Architecture change: none.

In the context of a human-decided ADR file, facing the merge rule of ADR 0008, we decided on a decision pull request with the label decision that the maintainer merges, to achieve a decision that takes effect only by that merge, accepting that it waits for the maintainer. — 2026-11-01
