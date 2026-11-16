---
title: "Decisions — swarm-answer-reader"
category: decisions
status: draft
implementation_status: none
date: 2026-11-15
created: 2026-11-15
last_reviewed: 2026-11-15
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-xsta
class: architectural
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm, answer-reader, correction-prompt, quorum]
---

# swarm-answer-reader — Decisions

Class: architectural (2026-11-15: the answers amend ADR 0020, so the class
moved from feature, under which it was first recorded; it was opened as
bounded in error). The change is explored through the research swarm once
that swarm works again. The minimum is five counted answers because the
change edits an ADR; seven stand below, and Q-3 was revised by the maintainer
the same day (addendum at the end).

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

## Q-6 · One reading rule for every swarm stage

asked: 2026-11-15
answer: Yes: the reading rule of Q-7 in the swarm-report-format change (2026-11-13) applies to every stage of the research swarm.
answered_by: maintainer
status: answered
context: |
  Topic: how the research swarm reads a model's structured answer at each stage.
  Intention: the haiku finder in run fc0e84ae was refused although its fenced object was valid; a sentence stood before the fence.
  Today: topic reports are read by `topic_report_payload` in scripts/stage2_research_run.py (a whole JSON object or exactly one json or unlabelled fence; text outside the fence is never read, the rule of Q-7 in swarm-report-format, 2026-11-13); finders, merge and judge are read by `payload_text`, which accepts a fence only when it is the whole answer.
  Repository change: one shared reader for finders, merge, judge and topics, with the Q-7 rule. Read in the code on origin/main 2026-11-15, the topic reader accepts every answer form the stricter reader accepts plus surrounding prose; this is proposed, not yet replayed against the recorded answers, and the replay comes before the build.
  Architecture change: yes, an amendment of ADR 0020 by the maintainer before it is built.

In the context of a swarm whose stages read the same kind of answer with two
different readers,
facing valid fenced answers refused only because prose stood around the
fence,
we decided that the Q-7 reading rule applies to every swarm stage through one
shared reader,
to achieve that a stage only turns former refusals into acceptances,
accepting that text outside the fence is never read — 2026-11-15

## Addendum — 2026-11-15, Q-3 revised by the maintainer

The maintainer withdrew the format probe of Q-3 later the same day and
answered "ja" to dropping it. The Q-3 record above stays as it was asked and
first answered; this addendum supersedes its answer.

- Revised answer: no format probe in prepare-explore; the per-model counts of
  Q-4 show which model often answers in the wrong format.
- Reason given with the question: both recorded deepseek-v4.1-flash failures
  lay deep in long answers (char 9979 and char 13598), which a tiny probe
  cannot see; the haiku case is covered by Q-6; a probe would only add one
  more point at which a run can stop.
- The question this left open, what the merge and the judge do when their
  one repair retry also fails, is answered in Q-7 below.

## Q-7 · A single-call stage hands its call to another model once

asked: 2026-11-15
answer: Yes: when the merge or the judge also fails its one repair retry, another model takes that call once; if that fails too, the run ends and keeps what it has for resume.
answered_by: maintainer
status: answered
context: |
  Topic: the research swarm's single-call stages, the merge of the source map and the judge (the Opus reconcile).
  Intention: Q-5 lets the finder stage survive one failed finder, but the merge and the judge are each one call, so one bad model can still end the run after Q-2's one retry.
  Today: ADR 0020 point 9 ends the run when a stage fails; an aborted run resumes from what it stored.
  Repository change: after the stage's one repair retry fails, the same call goes once to another admitted model of the stage's role; the answer is read with the same strict reader; if it also fails, the run ends as today and keeps its stored results for resume.
  Architecture change: yes, an amendment of ADR 0020 point 9 by the maintainer before it is built.

In the context of single-call swarm stages that end the run when their
answer fails,
facing failures that belong to one model rather than to the task,
we decided that after the stage's one repair retry another model takes the
call once, and only then does the run end, keeping its results for resume,
to achieve that one model alone no longer ends a run,
accepting one more call per failed stage and an amendment of ADR 0020 —
2026-11-15

## Q-8 · Where the answer-reading and repair rules live

asked: 2026-11-16
answer: "Nachtrag zu ADR 0020 (Empfohlen)"
answered_by: maintainer
status: answered
context: |
  Topic: where the rules of Q-1 to Q-7 (one answer reader, one repair retry, per-model counts, the finder quorum, the hand-over of a single-call stage) are written down as architecture.
  Intention: the runner's draft of 2026-11-16 (attempt 3, GLM 5.3) wrote a new ADR 0026 (docs/adr/0026-swarm-answer-reading-and-repair.md) instead of amending ADR 0020, the phase-1 research swarm ADR that Q-2, Q-5, Q-6 and Q-7 named as the place.
  Today: ADR 0020 (docs/adr/0020-phase-1-research-swarm.md) governs the research swarm; the draft failed its post-run checks, and its output (the new ADR 0026, spec.md, design.md, plan.md, findings.md and a change to plans/INDEX.md) stands uncommitted in the worktree.
  Repository change: the rules become an amendment to ADR 0020, not a new ADR; the uncommitted draft is superseded, and the draft is restarted through the runner.
  Architecture change: yes, an amendment of ADR 0020 by the maintainer instead of a new ADR 0026.

In the context of rules that change how the research swarm reads and
repairs model answers,
facing a draft that placed them in a new ADR 0026,
we decided that they are an amendment to ADR 0020, that the uncommitted
draft is superseded and that the draft restarts through the runner,
to achieve one ADR that states the whole research swarm contract,
accepting that the draft's work is discarded and redone — 2026-11-16
