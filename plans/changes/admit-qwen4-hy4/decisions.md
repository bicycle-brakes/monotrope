---
title: "Decisions — admit-qwen4-hy4"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-x0ph
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: claude-opus-5-5, version: "2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# admit-qwen4-hy4 — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).
Exploration: `research.md` (GLM 5.3 Flash, 2026-11-16). The answers below
were given in conversation on 2026-11-16 and recorded in the bead
(coding-harness-x0ph) the same day; this file copies them from there.

## Q-1 · Admit the paid ids the catalog refresh found

context: |
  Topic: model ids on the opencode-go ladder of the review loop.
  Intention: a live Pi 1.5.0 catalog refresh on 2026-11-16 listed 34
  opencode-go ids, 8 of them not declared; three are paid ids that could
  serve the paid ladder.
  Today: `model-endpoints.yaml` admits only the declared ids; qwen4-max,
  hy4 and longcat-2.0 are not among them.
  Repository change: a `modelle` entry and a `modelle_terms` record per id
  in `model-endpoints.yaml`, with reachability proved by `prepare-loop`.
  Architecture change: none; admission stays central in
  `model-endpoints.yaml`, no runner code changes.
asked: 2026-11-16, conversation
answer: "ja" (to: admit qwen4-max, hy4 and longcat-2.0)
answered_by: maintainer
status: answered

In the context of the opencode-go paid ladder, facing paid ids the live
catalog lists but the endpoint file does not declare, we decided to admit
qwen4-max and hy4 (longcat-2.0 was asked too and excluded in Q-2), each
with its read privacy and request terms, to achieve more reachable review
models at the declared cost order, accepting the work of reading and
dating each id's terms.
— 2026-11-16

## Q-2 · Exclude longcat-2.0

context: |
  Topic: longcat-2.0, one of the three paid ids asked about in Q-1.
  Intention: the maintainer narrowed the scope after Q-1 was answered.
  Today: longcat-2.0 is not declared in `model-endpoints.yaml`.
  Repository change: no entry for longcat-2.0; the scope is qwen4-max and
  hy4.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "longcat 2.0 nicht mit rein nehmen, das hat in den letzen wochen zu schlecht performt"
answered_by: maintainer
status: answered

In the context of the paid ids admitted in Q-1, facing longcat-2.0
performing too poorly in recent weeks in the maintainer's judgement, we
decided to leave longcat-2.0 out of this change, to achieve a ladder of
models that deliver, accepting one cheaper paid id fewer.
— 2026-11-16

## Q-3 · Contributor models stay out of this change

context: |
  Topic: the contributor models (Muse Spark 1.2 and 1.3, Iceman) in the
  same catalog refresh.
  Intention: they carry different data terms from the paid ids, so the
  bead's description excludes them on the maintainer's word.
  Today: they are not declared; ADR 0021 requires training "Not used".
  Repository change: none in this change; their trial admission is its own
  bead (coding-harness-wmy1), an ADR 0021 amendment.
  Architecture change: none here.
asked: 2026-11-16, conversation
answer: excluded from this bead; their admission is tracked in its own bead (coding-harness-wmy1)
answered_by: maintainer
status: answered

In the context of the 2026-11-16 catalog refresh, facing contributor
models whose data terms differ from the paid ids, we decided to keep them
out of this change and handle them in their own bead
(coding-harness-wmy1), to achieve a bounded data change here, accepting
that their trial waits for that ADR amendment.
— 2026-11-16

## Q-4 · Retention above 0 days

context: |
  Topic: which retention value admits a model to the paid ladder.
  Intention: the spec review (finding F-2) found AC 2 fixes training at
  `Not used` but names no rule for retention; the machine rule admits any
  non-empty value, while the `opencode-go` remark records that the
  maintainer admitted the 30-day ids by word.
  Today: Q-1's "ja" came before either id's terms were read.
  Repository change: an id with retention above 0 days is admitted when
  its training reads `Not used`, or the build stops for a question.
  Architecture change: none.
asked: 2026-11-16, conversation (spec review finding F-2)
answer: "Ja, wenn Training 'Not used' (Empfohlen)"
answered_by: maintainer
status: answered

In the context of admitting qwen4-max and hy4 to the paid ladder, facing
retention terms that may read above 0 days, we decided that retention
above 0 days, for example 30 days, is admissible when training reads
`Not used`, to achieve that the build does not stop for a question on
retention alone, accepting that admitted providers may keep request data
for the stated period.
— 2026-11-16

## Q-5 · An id whose reading or probe fails

context: |
  Topic: what happens when the dated terms reading or the probe goes
  against qwen4-max or hy4.
  Intention: the spec review (finding F-1) found AC 4 and AC 5 have no
  condition, so one failing id leaves the change unfinishable (reading A),
  while the house precedent declares such an id with a dated skip
  (reading B), as `gpt-6-luna`, `claude-haiku-5-5` and `gemini-4-argon`
  are declared.
  Today: undecided; the maintainer asked for the advisor's view.
  Repository change: all or nothing, a dated per-id skip, or shipping the
  other id alone.
  Architecture change: none.
  Advisor view (2026-11-16, not a decision): recommend a dated per-id skip
  like the three existing ones; check first that a skipped id cannot be
  seated in the research swarm through `modelle_terms`
  (`scripts/stage2_availability.py`, near line 1174) and read the `grund`
  of the three existing skips; treat an ambiguous single Hy4 row as no
  row; AC 4 and AC 5 become conditional on each admitted id.
asked: 2026-11-16, conversation (spec review finding F-1)
answer: null
answered_by: null
status: open

Open. The maintainer answered with a question, "was sagt der /advisor?",
and has not chosen yet; the advisor view in the context above is a note
for that choice, not a decision.
