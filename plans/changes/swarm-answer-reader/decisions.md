---
title: "Decisions — swarm-answer-reader"
category: decisions
status: draft
implementation_status: none
date: 2026-11-15
created: 2026-11-15
last_reviewed: 2026-11-15
updated: 2026-11-15
supersedes: null
superseded_by: null
bead: coding-harness-xsta
class: feature
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm, answer-reader, correction-prompt, probe, quorum]
---

# swarm-answer-reader — Decisions

Class: feature (maintainer, 2026-11-15: the change is explored through the
research swarm once that swarm works again; it was opened as bounded).
The minimum is three counted answers, five when the change edits an ADR
file; five stand below.

## Where these answers come from

The maintainer gave all five answers in the orchestrating conversation of
2026-11-15, after research run fc0e84ae (change review-loop-flash-after-free)
stopped because two of three finders were refused. The answers are recorded
as stated; the context fields hold what the agent read in the repository on
the same day (commit 49162f8f), not new decisions.

The evidence, read from the run's stdouts on 2026-11-15 (notes of bead
coding-harness-xsta): the claude-haiku-5-5 finder wrote a prose sentence and
then a fenced object that parses with all four keys, refused only for the
wrapper; the deepseek-v4.1-flash finder wrote a fenced but invalid JSON
object (`Expecting ',' at char 13598`); the mimo-v2.6-flash finder answered
the bare object, which passed.

## Q-1 · One reader for every structured model answer

asked: 2026-11-15
answer: One reader for every structured model answer in the swarm stages (finder, research seats, reconcile, plus any other stage2 path that parses a model's JSON answer); find them all with grep. It accepts exactly one top-level JSON object anywhere in the answer and ignores fences and surrounding prose. It refuses zero or several objects. Schema validation stays strict and unchanged.
answered_by: maintainer
status: answered
context: |
  Topic: how the research swarm reads a model's structured answer (finder lists, topic reports, map merge, judge reconciliation).
  Intention: research run fc0e84ae stopped on 2026-11-15 because a finder answer that held a valid object behind a sentence of prose and a fence was refused; the run could not go on.
  Today: two readers exist in scripts/stage2_research_run.py (commit 49162f8f). `payload_text` (finders, merge, judge) accepts only the bare object or a fence that is the whole answer. `topic_report_payload` (topics) accepts the bare object or exactly one JSON fence with prose around it, and never reads text outside the fence: the maintainer's answer Q-7 of plans/changes/swarm-report-format/decisions.md (2026-11-13). No other stage2 path parses a model's JSON answer; the public sentence is plain text.
  Repository change: one shared reader replaces both, its callers keep their strict validators; the tests that pin the fence-only rule of swarm-report-format Q-7 change with it.
  Architecture change: none to ADR 0020 (phase-1 research swarm), which names a format contract but not its wrapper; this answer supersedes swarm-report-format Q-7 (fence-only reading) for every swarm stage.

In the context of a research run stopped by finder answers whose valid
object stood behind prose and a fence,
facing two readers with different wrapper rules and a third stage family
that tolerated no wrapper at all,
we decided for one reader that accepts exactly one top-level JSON object
anywhere in the answer, ignores fences and prose, and refuses zero or several
objects, with every schema check unchanged,
to achieve one rule for every structured answer,
accepting that the fence-only rule of swarm-report-format Q-7 no longer
holds — 2026-11-15

## Q-2 · One repair retry per refused answer

asked: 2026-11-15
answer: One repair retry per refused answer. The model gets the exact parse or schema error and answers once more. Model the retry on how PR 392 (bead coding-harness-t2wm) told the model why a citation was refused.
answered_by: maintainer
status: answered
context: |
  Topic: what happens after the reader or a schema check refuses a model's structured answer.
  Intention: the deepseek-v4.1-flash finder of run fc0e84ae wrote invalid JSON inside its fence; no reader can accept that, only a second answer can.
  Today: only a topic report gets one correction call (`correction_entry` and `correction_prompt` in scripts/stage2_research_run.py), which since PR 392 also carries each failed citation with its reason. A refused finder, map merge or judge answer stops the run with no second call.
  Repository change: the correction mechanism of the topic stage extends to the finder, merge and judge stages, each refused answer once, with the exact error text in the correction prompt.
  Architecture change: yes. ADR 0020 point 9 (amended 2026-11-10) allows one correction for a topic report only, says "No other retry is allowed", and fixes the invocation ceiling at 72 + 6N. A retry for finders, merge and judge needs an amendment of ADR 0020 by the maintainer before it is built.

In the context of a finder answer that was invalid JSON and stopped the run,
facing a correction that today exists for topic reports alone,
we decided that every refused structured answer gets one repair retry that
states the exact parse or schema error, in the manner PR 392 used for
refused citations,
to achieve that a format fault costs one call instead of the run,
accepting more calls per run and an amendment of the invocation ceiling of
ADR 0020 — 2026-11-15

## Q-3 · A format probe in prepare-explore

asked: 2026-11-15
answer: A format probe in prepare-explore. Each candidate model must return a tiny object in the required shape. A model that cannot is dropped before seats are shown, and the report says why.
answered_by: maintainer
status: answered
context: |
  Topic: the preparation step before a research run (prepare-explore), which probes each candidate model and seals the seat selection.
  Intention: a model that cannot produce the required object shape should be known before the maintainer chooses seats, not found out by a stopped run.
  Today: the probe in scripts/stage2_availability.py (`probe_go`, `probe_claude`) sends the fixed text "Availability probe only. Reply with OK." and checks only that the answer is not empty; the review loop's preparation shares that probe implementation.
  Repository change: the research preparation's probe asks for a tiny object in the required shape and reads the answer with the reader of Q-1; a model that fails is dropped from the candidates with its reason in the preparation report. The review loop's probe stays as it is.
  Architecture change: ADR 0020 point 11 states one probe per distinct model with a fixed text, no tools and no repository content, and that Go free models and Opus roles are not probed; a fixed format probe fits that wording, but whether it may replace the reachability text and whether it covers free and Opus models is for the explore to settle against the ADR.

In the context of models that answer the required object in different
wrappers or not at all,
facing a preparation that today only checks that a model answers something,
we decided that each candidate model must return a tiny object in the
required shape during prepare-explore and is dropped with its reason when it
cannot,
to achieve that the seats the maintainer is shown can answer in the format,
accepting a stricter probe and models dropped that would only have needed a
repair retry — 2026-11-15

## Q-4 · Per-model outcome counts in the run records

asked: 2026-11-15
answer: Per-model outcome counts in the run records: bare, fenced, repaired, refused.
answered_by: maintainer
status: answered
context: |
  Topic: what the research run records about how each model answered.
  Intention: after Q-1 and Q-2 a refused wrapper no longer stops a run, so it would go unseen unless it is counted; the counts show which models need the reader's tolerance or the retry.
  Today: the run manifest (`manifest_record` in scripts/stage2_research_run.py) records each slot's outcome, attempt and correction count, but not the shape of the answer.
  Repository change: the manifest gains, per model, the counts of bare, fenced, repaired and refused answers.
  Architecture change: none.

In the context of a reader that now tolerates wrappers and a retry that now
repairs faults,
facing run records that do not show how a model answered,
we decided to count per model the bare, fenced, repaired and refused answers
in the run records,
to achieve evidence for choosing and dropping models,
accepting a larger manifest — 2026-11-15

## Q-5 · Quorum of two of three finders

asked: 2026-11-15
answer: Quorum: the run continues while at least two of three finders answered validly. The failure is recorded in the run record and the research.md header.
answered_by: maintainer
status: answered
context: |
  Topic: whether one failed finder stops the research run.
  Intention: in run fc0e84ae one finder's answer was valid and two were refused; with Q-1 and Q-2 one finder may still fail, and the map can be built from the others.
  Today: `stage_finders` in scripts/stage2_research_run.py stops the run when any finder is not ok (`require_ok`), and `merge_research_map` in scripts/stage2_research_map.py refuses unless exactly three finder reports are given.
  Repository change: the finder stage continues with two valid reports, the merge accepts two or three, and the failed finder is named in the run manifest and in the heading line of the record appended to research.md.
  Architecture change: yes. ADR 0020 point 2 states that finder step 0 uses the three repository seats, and point 9 states that a failed finder stage prevents later stages. Continuing with two finders needs an amendment of ADR 0020 by the maintainer before it is built.

In the context of a finder stage that stops the run when one of three
finders fails,
facing finder answers that fail for reasons a second finder does not share,
we decided that the run continues while at least two of three finders
answered validly, with the failure recorded in the run record and the
research.md header,
to achieve runs that a single finder cannot stop,
accepting a map built from two finders where the third is missing, and an
amendment of ADR 0020 — 2026-11-15
