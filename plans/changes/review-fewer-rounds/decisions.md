---
title: "Decisions — review-fewer-rounds"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-3rtn
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, review-loop, adr-0021]
---

# review-fewer-rounds — Decisions

Class: architectural (maintainer 2026-11-07; bead coding-harness-3rtn).

The maintainer gave these answers in the orchestrating conversation on
2026-11-07 and 2026-11-08; the orchestrator recorded each in the notes of
bead coding-harness-3rtn on the day it was given. They are transcribed here
unchanged in substance, one record per question. Questions still open are
listed at the end and are not counted.

## Q-1 · Which review lenses round 1 covers

asked: 2026-11-08
answer: "Plus Wartbarkeit" — five lenses: (1) spec fidelity and scope, (2) hostile input and failure paths, (3) state, retry and abort, (4) tests as evidence, (5) maintainability; artefact formalities (headers, status, plan card against decisions, time ledger) go to a gate instead of a reviewer.
answered_by: maintainer
status: answered
context: |
  Topic: today every reviewer of the loop reads the whole change with no focus, and 26% of 296 loop rows (14 loop records, measured 2026-11-07) concern change-folder formalities only.
  Intention: fewer rounds need each round to find more of what matters; a lens gives every reviewer one job.
  Today: unfocused reviewers; one ladder id per later round; new MAJORs keep appearing late.
  Repository change: reviewer prompts per lens; a formalities gate.
  Architecture change: amends ADR 0021 (review swarms until clean).

In the context of the lenses of review round 1, facing reviews that mixed
defect hunting with artefact formalities, we decided that round 1 covers five
lenses — spec fidelity and scope, hostile input and failure paths, state,
retry and abort, tests as evidence, maintainability — and that artefact
formalities go to a gate instead of a reviewer, to achieve reviewers that
spend their attention on defects, accepting that a formality no gate checks is
found by nobody — 2026-11-09

## Q-2 · Who sits on each lens

asked: 2026-11-08
answer: every lens is reviewed by the model with the best measured precision, a cheap model of another lineage and Codex gpt-6.1-terra at effort medium — 15 calls in round 1, five of them Codex; think deeply about which aspects must be covered and check for empirical evidence.
answered_by: maintainer
status: answered
context: |
  Topic: measured precision by taken share differs widely between reviewers (2026-11-08 over 1205 loop rows: deepseek-v4.1-flash 91%, kimi-k2.7-code 30%).
  Intention: seat reviewers by evidence and lineage diversity instead of "all reachable".
  Today: round 1 runs the free swarm; later rounds one paid ladder id each.
  Repository change: a seating per lens the runner reads; Codex joins round 1.
  Architecture change: amends ADR 0021's stage order.

In the context of the seats on each lens, facing single reviewers that miss
what another lineage finds, we decided that every lens is reviewed by the
model with the best measured precision, a cheap model of another lineage and
Codex gpt-6.1-terra at effort medium — 15 calls in round 1, five of them
Codex, to achieve overlap between independent reviewers on every lens,
accepting that round 1 costs 15 calls for every change, a small one included —
2026-11-09

## Q-3 · When a second round runs

asked: 2026-11-08
answer: per lens, by the overlap of its three reviewers (a capture-recapture estimate of the defects still undiscovered); a second round runs only for lenses with a high estimate; the threshold comes from research with evidence.
answered_by: maintainer
status: answered
context: |
  Topic: round-1 size predicts later MAJOR+ findings only weakly (r=0.22 rows, 0.25 MAJOR+; 63 changes, measured 2026-11-08) and phase-6 MAJOR+ not at all (r=0.01).
  Intention: a second round where the evidence says defects remain, not by raw count.
  Today: the loop runs until a clean round or the paid ladder is spent.
  Repository change: an estimator and a threshold in the runner, read from configuration.
  Architecture change: replaces "until clean" in ADR 0021 by an estimate-driven second round.

In the context of the question when a second review round runs, facing second
rounds that ran for every change whatever round 1 found, we decided that a
second round runs per lens and only where the overlap of its three reviewers
estimates many defects still undiscovered, with the threshold taken from
research with evidence, to achieve fewer rounds where round 1 was thorough,
accepting that an estimate from three reviewers is coarse and can stop a lens
too early — 2026-11-09

## Q-4 · Where seating, rounds and limits live

asked: 2026-11-08
answer: the model selection must be centrally and easily changeable — likewise which rounds run, the number of rounds, which and how many models sit in a round; one declarative, validated file (the central configuration of bead coding-harness-twvx) holds lenses, seats, round count and order, the second-round trigger and its threshold, and the phase-6 re-check limit; no constant repeats it.
answered_by: maintainer
status: answered
context: |
  Topic: today the stage order and model sets are spread over the runner, model-endpoints.yaml and the documents.
  Intention: a change of seating is a one-line edit with a validator, not a code change.
  Today: constants in scripts/stage2.py; the ladder in model-endpoints.yaml.
  Repository change: the runner, prompts, docs and tests read one file; this change depends on bead coding-harness-twvx.
  Architecture change: configuration becomes the single source for the loop's shape.

In the context of the home of seating, rounds and limits, facing values the
maintainer wants to change without a code change, we decided that one
declarative, validated file — the central configuration (bead coding-harness-
twvx) — holds lenses, seats, round count and order, the second-round trigger
and its threshold and the phase-6 re-check limit, and no constant repeats it,
to achieve a change of the review set-up by one edited line, accepting that
this change depends on the central configuration or carries an interim file
until it exists — 2026-11-09

## Q-5 · How many phase-6 re-checks

asked: 2026-11-08
answer: the first phase-6 review plus one re-check; after that the runner stops and reports to the maintainer with a proposal (a named limit in the PR, a mechanism repair, or stop); from the second re-check finding of one kind a mechanism repair is required instead of case repairs. The limit lives in the central configuration.
answered_by: maintainer
status: answered
context: |
  Topic: phase-6 re-checks repeated on some changes without converging.
  Intention: a hard end with a decision for the maintainer instead of open-ended re-checks.
  Today: no stated limit on phase-6 re-checks.
  Repository change: a re-check counter and a stop report in the runner.
  Architecture change: none beyond the configured limit.

In the context of the number of phase-6 re-checks, facing changes that went
through re-check after re-check, we decided that phase 6 is the first review
plus one re-check, after which the runner stops and reports to the maintainer
with a proposal, and that from the second re-check finding of one kind a
mechanism repair is required instead of case repairs; the limit lives in the
central configuration, to achieve a bounded end of every change, accepting
that a change can stop with open findings and wait for the maintainer —
2026-11-09

## Q-6 · What round 2 does with findings

asked: 2026-11-08
answer: round 2 sorts by kind, not by location — a MAJOR or BLOCKER goes into the same last repair (no new full round; phase 6 with its limit follows); a MINOR follows the MINOR rule (tests, security or false statements repaired without asking; style named as an accepted limit); a follow-up bead only for a finding in code outside this change. This replaces the earlier answer of the same day that sorted by location.
answered_by: maintainer
status: answered
context: |
  Topic: round 2 reviews the repair; its reviewers also report rows outside the repair diff.
  Intention: no third full round, yet no real defect left behind.
  Today: every new row may start another round.
  Repository change: triage rules for round 2 in the runner and prompts.
  Architecture change: amends ADR 0021's end condition.

In the context of what round 2 does with its findings, facing findings
that each opened a new full round, we decided that round 2 sorts by kind,
not by location: a MAJOR or BLOCKER goes into the same last repair without
a new full round, a MINOR follows the MINOR rule, and a follow-up bead is
opened only for a finding in code outside this change, to achieve one last
repair instead of a further round, accepting that the last repair is
checked by phase 6 alone — 2026-11-09

## Q-7 · Style findings

asked: 2026-11-08
answer: an unambiguous style finding (a clear proposal, not a matter of taste) rides along in a repair that runs anyway; it never triggers a repair or a round on its own; matters of taste stay accepted limits named in the PR. The MINOR rule in AGENTS.md changes with this change.
answered_by: maintainer
status: answered
context: |
  Topic: AGENTS.md says style rows are accepted limits, even when the fix is obvious.
  Intention: take the cheap, clear fixes without letting style drive rounds.
  Today: every style row is an accepted limit.
  Repository change: AGENTS.md MINOR rule; triage guidance.
  Architecture change: none.

In the context of style findings, facing style rows that triggered repairs and
rounds of their own, we decided that an unambiguous style finding rides along
in a repair that runs anyway and never triggers a repair or a round on its
own, that matters of taste stay accepted limits named in the pull request, and
that the MINOR rule in AGENTS.md changes with this change, to achieve clear
style fixes at no extra round, accepting that a clear style finding stays
unrepaired when no repair runs — 2026-11-09

## Q-8 · Self-review

asked: 2026-11-08
answer: exclude the implementer's model family only when it would be the sole reviewer; when several reviewers run in parallel it may sit among them. Markdownlint and the formalities gate block new and changed files only; the existing stock stays report-only until cleaned.
answered_by: maintainer
status: answered
context: |
  Topic: the implementer's model family may review its own work.
  Intention: keep independence without losing the best-precision seat.
  Today: no stated rule.
  Repository change: a seating constraint the validator checks; gate scope on changed files.
  Architecture change: none.

In the context of self-review and the formalities gates, facing a rule that
excluded the implementer's model family from every review, we decided that the
implementer's model family is excluded only when it would be the sole reviewer
and may sit among several parallel reviewers, and that Markdownlint and the
formalities gate block new and changed files only while the existing stock
stays report-only until cleaned, to achieve more reviewers to choose from and
gates that do not block on old files, accepting that a reviewer of the
implementer's family may share its blind spots, and old formality faults stay
for now — 2026-11-09

## Q-9 · The form of a lens

asked: 2026-11-09
answer: "Fehlerklassen + Prüffragen" — each lens is a defect class with a list of concrete check questions, not a role the reviewer plays.
answered_by: maintainer
status: answered
context: |
  Topic: the five lenses of Q-1 need a form in the reviewer prompt.
  Intention: follow the stronger evidence in research.md (scenario reading by defect class found more defects than ad hoc or checklist reading, Porter, Votta and Basili 1995; perspective-based reading showed no clear gain, Ciolkowski 2009).
  Today: reviewers read without focus.
  Repository change: one prompt per lens with its check questions.
  Architecture change: part of the ADR 0021 amendment.

In the context of the form of a lens, facing reviewer roles that left open
what to look for, we decided that each lens is a defect class with a list of
concrete check questions, not a role the reviewer plays, to achieve reviews
that can be compared and measured per question, accepting that the question
lists must be written and kept current — 2026-11-09

## Q-10 · Where the check questions come from

asked: 2026-11-09
answer: "Aus unseren Funden + Literatur, du gibst frei" — an agent derives the questions per lens from the repository's measured loop and phase-6 rows and from the literature; the maintainer approves the list.
answered_by: maintainer
status: answered
context: |
  Topic: good check questions target the defects this repository actually has (measured 2026-11-08: 86% of phase-6 rows are SPEC, 65% of loop rows MAINT).
  Intention: questions that fit real defects, approved by the maintainer.
  Today: no check questions.
  Repository change: a question list per lens, held in the central configuration (bead coding-harness-twvx) or the prompt.
  Architecture change: none beyond Q-9.

In the context of the source of the check questions, facing check questions
that could be invented without evidence, we decided that an agent derives the
questions per lens from the repository's measured loop and phase-6 rows and
from the literature, and the maintainer approves the list, to achieve
questions grounded in the defects this repository actually had, accepting that
the list waits for the maintainer's approval before it is used — 2026-11-09

## Q-11 · What triggers a second round

asked: 2026-11-09
answer: "Einzelfund-Anteil, Jackknife nur protokolliert" — the share of accepted findings that only one reviewer of the lens reported decides; the Mh-jackknife and Chao estimates are computed and recorded only.
answered_by: maintainer
status: answered
context: |
  Topic: the remaining-defect estimate per lens from the overlap of its three reviewers (Q-3).
  Intention: a rule that is simple and explainable; the Mh-jackknife, best at three reviewers, still runs about 27% low in the median (Briand et al. 2000) and correlated model errors push it lower.
  Today: no estimator.
  Repository change: a small computation in the runner; both estimates logged.
  Architecture change: part of the ADR 0021 amendment.

In the context of the trigger of a second round, facing several estimators
that could decide, we decided that the share of accepted findings that only
one reviewer of the lens reported decides, and that the Mh-jackknife and Chao
estimates are computed and recorded only, to achieve a trigger that is simple
to read and to check, accepting that the simple share may be less accurate
than the recorded estimators — 2026-11-09

## Q-12 · How the second-round threshold is introduced

asked: 2026-11-09
answer: "B: Schatten, immer zweite Runde" — during a shadow period every lens always gets a second round; the single-finding rule (Q-11) is computed and recorded but does not decide; after 10–20 changes the threshold is set from what the second rounds actually found where the rule would have stopped.
answered_by: maintainer
status: answered
context: |
  Topic: the research proposal (second round when at least two single findings make up more than half of a lens's accepted findings, or none of two or more is confirmed by a second reviewer) is the research agent's own derivation; no published threshold exists for three reviewers (research.md).
  Intention: set the threshold from this repository's own data before it decides anything.
  Today: the loop runs until a clean round (4–8 rounds).
  Repository change: threshold and mode (shadow or live) as values in the central configuration (bead coding-harness-twvx); a per-lens record of findings, overlap and both estimates.
  Architecture change: part of the ADR 0021 amendment.

In the context of the introduction of the second-round threshold, facing a
threshold nobody has measured in this repository, we decided that during a
shadow period every lens always gets a second round while the single-finding
rule is computed and recorded but does not decide, and that after 10 to 20
changes the threshold is set from what the second rounds found where the rule
would have stopped, to achieve a threshold set from this repository's own
data, accepting that the shadow period saves no round and costs more calls
than today — 2026-11-09

## Open — not counted

- The research questions of 2026-11-08 are not answered: (a) evidence for
  lens-based against unfocused review; (b) capture-recapture estimators for
  three reviewers per lens and a defensible threshold; (c) evidence on
  ensembles and model diversity of LLM reviewers; (d) cost of 15 round-1
  calls against today's rounds and verify runs. The stage-1 exploration of
  2026-11-09 (research.md) did not read the bead and covers the repository
  only. Answered on 2026-11-09 by the Opus research section of research.md.
