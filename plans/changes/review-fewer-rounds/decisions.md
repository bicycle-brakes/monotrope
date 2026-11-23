---
title: "Decisions — review-fewer-rounds"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-23
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

On 2026-11-10 the maintainer chose, question by question, the accepted
downside of each decision statement; where that choice added a rule, the
answer line says so and the statement carries that day's date. Q-3 was
answered anew on that day.

## Q-1 · Which review lenses round 1 covers

asked: 2026-11-08
answer: "Plus Wartbarkeit" — five lenses: (1) spec fidelity and scope, (2) hostile input and failure paths, (3) state, retry and abort, (4) tests as evidence, (5) maintainability; artefact formalities (headers, status, plan card against decisions, time ledger) go to a gate instead of a reviewer. Added by the maintainer on 2026-11-10: the spec lists every artefact formality with the gate that checks it; a formality without a gate becomes a follow-up bead.
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
retry and abort, tests as evidence, maintainability — that artefact
formalities go to gates instead of a reviewer, that the spec lists every
formality with the gate that checks it, and that a formality without a gate
becomes a follow-up bead, to achieve reviewers that spend their attention on
defects, accepting that nobody checks a formality without a gate until its
follow-up bead is done — 2026-11-10

## Q-2 · Who sits on each lens

asked: 2026-11-08
answer: every lens is reviewed by the model with the best measured precision, a cheap model of another lineage and Codex gpt-6.1-terra at effort medium — 15 calls in round 1, five of them Codex; think deeply about which aspects must be covered and check for empirical evidence. Added by the maintainer on 2026-11-10: a small change (class bounded, or text-only) gets one reviewer per lens, 5 calls in round 1.
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
Codex gpt-6.1-terra at effort medium — 15 calls in round 1, five of them Codex
— and that a small change (class bounded, or text-only) gets one reviewer per
lens, 5 calls, to achieve overlap between independent reviewers on every lens
where the change is large enough to pay for it, accepting that a small change
has no second voice on any lens — 2026-11-10

## Q-3 · When a second round runs

asked: 2026-11-08
answer: "Die zweite Runde ohne Linsen laufen lassen" (2026-11-10) — the trigger stays per lens (Q-11); when it fires for at least one lens, one single second round runs in which the reviewers read the whole diff freely, without lenses. This replaces the answer of 2026-11-08 (a second round per lens, only for lenses with a high capture-recapture estimate; the threshold from research with evidence).
answered_by: maintainer
status: answered
context: |
  Topic: round-1 size predicts later MAJOR+ findings only weakly (r=0.22 rows, 0.25 MAJOR+; 63 changes, measured 2026-11-08) and phase-6 MAJOR+ not at all (r=0.01).
  Intention: a second round where the evidence says defects remain, not by raw count.
  Today: the loop runs until a clean round or the paid ladder is spent.
  Repository change: an estimator and a threshold in the runner, read from configuration.
  Architecture change: replaces "until clean" in ADR 0021 by an estimate-driven second round.

In the context of the question when a second review round runs, facing second
rounds that ran for every change whatever round 1 found, we decided that the
trigger is measured per lens (Q-11) and that, when it fires for at least one
lens, one single second round runs in which the reviewers read the whole diff
freely, without lenses, to achieve at most one further round and a second look
that is not bound to the questions of round 1, accepting that the second round
is unfocused again and also reads the lenses whose trigger did not fire —
2026-11-10

## Q-4 · Where seating, rounds and limits live

asked: 2026-11-08
answer: the model selection must be centrally and easily changeable — likewise which rounds run, the number of rounds, which and how many models sit in a round; one declarative, validated file (the central configuration of bead coding-harness-twvx) holds lenses, seats, round count and order, the second-round trigger and its threshold, and the phase-6 re-check limit; no constant repeats it. Added by the maintainer on 2026-11-10: no interim file: the implementation of this change waits until the skeleton of the central configuration is merged; spec and plan may be written earlier.
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
declarative, validated file — the central configuration (bead
coding-harness-twvx) — holds lenses, seats, round count and order, the
second-round trigger and its threshold and the phase-6 re-check limit, that no
constant repeats it, and that no interim file is built, to achieve a change of
the review set-up by one edited line, accepting that the implementation of
this change waits until the skeleton of the central configuration is merged,
while spec and plan may be written earlier — 2026-11-10

## Q-5 · How many phase-6 re-checks

asked: 2026-11-08
answer: the first phase-6 review plus one re-check; after that the runner stops and reports to the maintainer with a proposal (a named limit in the PR, a mechanism repair, or stop); from the second re-check finding of one kind a mechanism repair is required instead of case repairs. The limit lives in the central configuration. Added by the maintainer on 2026-11-10: at night the runner may run a second re-check when all open findings belong to one mechanism and that mechanism was repaired.
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
with a proposal, that from the second re-check finding of one kind a mechanism
repair is required instead of case repairs, that at night the runner may run a
second re-check when all open findings belong to one mechanism and that
mechanism was repaired, and that the limit lives in the central configuration,
to achieve a bounded end of every change without a night lost to one
mechanism, accepting that the night re-check costs a further full check and a
Codex call the maintainer did not approve one by one, and that in every other
case a change stops with open findings and waits for the maintainer —
2026-11-10

## Q-6 · What round 2 does with findings

asked: 2026-11-08
answer: round 2 sorts by kind, not by location — a MAJOR or BLOCKER goes into the same last repair (no new full round; phase 6 with its limit follows); a MINOR follows the MINOR rule (tests, security or false statements repaired without asking; style named as an accepted limit); a follow-up bead only for a finding in code outside this change. This replaces the earlier answer of the same day that sorted by location. Added by the maintainer on 2026-11-10: the accepted downside confirmed as worded.
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
answer: an unambiguous style finding (a clear proposal, not a matter of taste) rides along in a repair that runs anyway; it never triggers a repair or a round on its own; matters of taste stay accepted limits named in the PR. The MINOR rule in AGENTS.md changes with this change. Added by the maintainer on 2026-11-10: once a week a clean-up bead collects the clear style findings left standing and repairs them in a pull request of its own.
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
own, that once a week a clean-up bead collects the clear style findings left
standing and repairs them in a pull request of its own, that matters of taste
stay accepted limits named in the pull request, and that the MINOR rule in
AGENTS.md changes with this change, to achieve clear style fixes at no extra
round, accepting one more pull request a week with a full check of its own,
and style work that occupies a lane — 2026-11-10

## Q-8 · Self-review

asked: 2026-11-08
answer: exclude the implementer's model family only when it would be the sole reviewer; when several reviewers run in parallel it may sit among them. Markdownlint and the formalities gate block new and changed files only; the existing stock stays report-only until cleaned. Added by the maintainer on 2026-11-10: at most one reviewer of the implementer's model family sits on a lens.
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
implementer's model family is excluded when it would be the sole reviewer,
that among several parallel reviewers at most one of that family sits on a
lens, and that Markdownlint and the formalities gate block new and changed
files only while the existing stock stays report-only until cleaned, to
achieve more reviewers to choose from without a lens read mainly by the
implementer's family, and gates that do not block on old files, accepting that
the seating is tighter — when a model of another family fails, the lens runs
with fewer reviewers or waits — and that old formality faults stay for now —
2026-11-10

## Q-9 · The form of a lens

asked: 2026-11-09
answer: "Fehlerklassen + Prüffragen" — each lens is a defect class with a list of concrete check questions, not a role the reviewer plays. Added by the maintainer on 2026-11-10: a question list is revised only when phase 6 finds something no question covers.
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
concrete check questions, not a role the reviewer plays, and that a list is
revised only when phase 6 finds something no question covers, to achieve
reviews that can be compared and measured per question, with a stated occasion
for upkeep, accepting that a gap in a list shows only after it has let one
defect through — 2026-11-10

## Q-10 · Where the check questions come from

asked: 2026-11-09
answer: "Aus unseren Funden + Literatur, du gibst frei" — an agent derives the questions per lens from the repository's measured loop and phase-6 rows and from the literature; the maintainer approves the list. Added by the maintainer on 2026-11-10: the maintainer approves only the first list; later additions apply at once and are shown in the pull request.
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
from the literature, that the maintainer approves the first list, and that
later additions apply at once and are shown in the pull request, to achieve
questions grounded in the defects this repository actually had, without a
night waiting for an approval, accepting that a bad addition acts until the
maintainer sees it in the pull request and takes it back — 2026-11-10

## Q-11 · What triggers a second round

asked: 2026-11-09
answer: "Einzelfund-Anteil, Jackknife nur protokolliert" — the share of accepted findings that only one reviewer of the lens reported decides; the Mh-jackknife and Chao estimates are computed and recorded only. Added by the maintainer on 2026-11-10: after the shadow period the simple share is compared once with the recorded estimators, and the better trigger decides from then on.
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
one reviewer of the lens reported is the trigger, that the Mh-jackknife and
Chao estimates are computed and recorded only, and that after the shadow
period (Q-12) the simple share is compared once with the recorded estimators
and the better trigger decides from then on, to achieve a trigger that is
simple to read and to check and is measured once against the alternatives,
accepting the work of that one comparison, and that the less accurate trigger
may stand until it is done — 2026-11-10

## Q-12 · How the second-round threshold is introduced

asked: 2026-11-09
answer: "B: Schatten, immer zweite Runde" — during a shadow period every lens always gets a second round; the single-finding rule (Q-11) is computed and recorded but does not decide; after 10–20 changes the threshold is set from what the second rounds actually found where the rule would have stopped. Added by the maintainer on 2026-11-10: the shadow period ends after 10 changes when the data are clear; otherwise the runner asks the maintainer.
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
shadow period every change always gets the one free second round (Q-3) while
the single-finding rule is computed and recorded per lens but does not decide,
that the threshold is set from what the second rounds found where the rule
would have stopped, and that the shadow period ends after 10 changes when the
data are clear and otherwise the runner asks the maintainer, to achieve a
threshold set from this repository's own data and a shadow period with a
stated end, accepting that 10 changes may be too few for rare kinds of defect,
and that until the end the procedure saves no round and costs more calls than
today — 2026-11-10

## Q-13 · The first list of check questions

asked: 2026-11-10
answer: Use the list — the fifteen check questions proposed in the draft spec (5bda389c, "Open decisions", three per lens) hold unchanged. The maintainer read them in a German rendering of the spec's table; the English table is the approved text.
answered_by: maintainer
status: answered
context: |
  Topic: the five lenses need concrete check questions.
  Intention: the questions should hit the observed defects before models review with them; under Q-10 the maintainer approves only the first list.
  Today: the lenses are decided; no list is approved.
  Repository change: the list becomes part of the central configuration and of the reviewer prompts.
  Architecture change: none beyond the lenses already decided.

In the context of the check questions of the five review lenses, facing
lenses that were decided without questions a model can work through, we
decided that the fifteen questions of the draft spec hold unchanged and that
later additions follow Q-9 and Q-10, to achieve reviewers that start from the
observed defect classes, accepting that special cases are not named one by
one and that what no question hits surfaces only in phase 6 — 2026-11-10

## Q-14 · Who sits in the free second round

asked: 2026-11-10
answer: A team of three — three models of several model families read the whole diff once without a lens (three calls); the family rule of Q-8 holds.
answered_by: maintainer
status: answered
context: |
  Topic: the seating of the free second round.
  Intention: Q-3 decided a free second round without lenses; without a seating the runner cannot call it.
  Today: the earlier planning repeats the five groups of three of round 1; no current answer covers that.
  Repository change: the central configuration gets exactly one seating for the free round.
  Architecture change: no further round; the existing second round reads without lenses.

In the context of the free second review round, facing a decided round with
no seating, we decided that an independent team of three models of several
families reads the whole diff once without a lens, to achieve a second look
at three calls instead of fifteen, accepting that only three independent
voices read and that a defect the many repetitions of the other option would
have found stays hidden until phase 6 — 2026-11-10

## Q-15 · What triggers the second round on a small change

asked: 2026-11-10
answer: Always a second round — a small change gets exactly one free second round, after the shadow period too.
answered_by: maintainer
status: answered
context: |
  Topic: when a small change gets a second round after the shadow period.
  Intention: with one reviewer per lens (Q-2) every finding is a single finding, so the overlap trigger of Q-11 says nothing on a small change.
  Today: open; during the shadow period the free second round runs anyway, on small changes too.
  Repository change: the central configuration gets a rule of its own for small changes.
  Architecture change: no additional reviewers or rounds.

In the context of the second-round trigger on a small change, facing one
reviewer per lens and therefore no overlap to measure, we decided that a
small change always gets exactly one free second round, to achieve a rule
that does not pretend to a measurement, accepting that its three calls are
spent even when round 1 found nothing — 2026-11-10

## Q-16 · Decoupled from the central configuration

asked: 2026-11-23
answer: A — this change no longer waits for bead coding-harness-twvx. The values Q-4 names (lenses, seats, round count and order, the second-round trigger and its threshold, the phase-6 re-check limit) live in one validated section of an existing central file and move into the central configuration unchanged when it lands, as the verify slots did (bead coding-harness-u1ha). This replaces the "no interim file" clause of Q-4; the rest of Q-4 holds (one place, no constant repeats it).
answered_by: maintainer
status: answered
context: |
  Topic: the dependency of this change on bead coding-harness-twvx.
  Intention: the maintainer wants this change soon and fewer verify runs per lane; twvx has not started and is large.
  Today: Q-4 made the implementation wait for the central configuration's skeleton.
  Repository change: one validated section in an existing central file; the spec names which file. Orchestrator's proposal, for the plan card: `model-endpoints.yaml`, which already holds the paid ladder.
  Architecture change: none beyond Q-4; the move into twvx later is a relocation, not a redesign.

In the context of the home of the review set-up, facing a central
configuration that has not started, we decided that this change keeps Q-4's
single place in a validated section of an existing central file and moves it
into the central configuration unchanged later, to achieve the shorter review
loop soon, accepting one later relocation of that section — 2026-11-23

## Q-17 · The two-round house rule meanwhile

asked: 2026-11-23
answer: Until this change lands, the orchestrator runs at most two review-loop rounds per lane; taken rows of round two are repaired and phase 6 checks that repair (AGENTS.md, PR #436). This change makes the runner enforce the shape instead.
answered_by: maintainer
status: answered
context: |
  Topic: the review loop's length before this change lands.
  Intention: fewer verify runs per lane now.
  Today: "rounds until a clean round" (ADR 0021), narrowed by the house rule of 2026-11-23.
  Repository change: none here; the spec's round shape replaces the house rule when it merges.
  Architecture change: none.

In the context of the review loop before this change lands, facing rounds
three to five that each cost a repair and a full verify, we decided that the
orchestrator stops at two rounds and goes to phase 6, to achieve fewer verify
runs now, accepting that late findings move to phase 6 — 2026-11-23

## Q-18 · This change absorbs the review-loop redesign (mwzv.3)

asked: 2026-11-23
answer: A — this change is the one review-loop redesign; bead coding-harness-mwzv.3 is superseded by it. The redraft decides the beads mwzv.3 named: fctf (Q-19), 1gzo and pwdi (Q-20), vi3a (Q-21), py5 (Q-22), r3b6 (Q-23).
answered_by: maintainer
status: answered
context: |
  Topic: two beads redesigned the loop's shape.
  Intention: one ADR 0021 amendment instead of two.
  Today: mwzv.3 open, not started; this change has a drafted spec.
  Repository change: none beyond this change.
  Architecture change: one amendment of ADR 0021.

In the context of two overlapping redesigns of the review loop, we decided that this change is the only one, to achieve one coherent shape and one amendment, accepting a broader redraft — 2026-11-23

## Q-19 · How much review a small change gets (fctf)

asked: 2026-11-23
answer: A — a text-only change skips the review loop and gets phase 6 only; a bounded change gets round 1 with one reviewer per lens, one repair, then phase 6, without the free second round. This replaces Q-15 (a small change always gets one free second round).
answered_by: maintainer
status: answered
context: |
  Topic: review for small changes.
  Intention: fewer verify runs.
  Today: every change runs the whole loop; Q-15 gave small changes a free second round.
  Repository change: the runner skips phase 4b for text-only changes.
  Architecture change: part of the ADR 0021 amendment.

In the context of small changes, facing review rounds that cost more than they find, we decided that text-only changes get phase 6 only and bounded changes one round, to achieve fewer verify runs, accepting that a defect in a small code change may first show in phase 6 — 2026-11-23

## Q-20 · What ends the loop early (1gzo, pwdi)

asked: 2026-11-23
answer: A — the second round also does not run when round 1 brought only MINOR rows and all are repaired; the lane goes to phase 6. 1gzo (a clean free round ends the loop) is closed: the shape has no free pre-round any more.
answered_by: maintainer
status: answered
context: |
  Topic: early end of the loop.
  Intention: no round that brings nothing.
  Today: rounds until a clean round; Q-11's overlap trigger decides the second round.
  Repository change: one more condition next to the Q-11 trigger.
  Architecture change: part of the ADR 0021 amendment.

In the context of the second-round trigger, facing a round with only minor, repaired rows, we decided that such a round goes straight to phase 6, to achieve one verify run less, accepting that a minor-only round gets no independent second look before phase 6 — 2026-11-23

## Q-21 · A cap on findings per reviewer (vi3a)

asked: 2026-11-23
answer: A — each reviewer reports at most five findings, ranked by severity, each with file and line as evidence; BLOCKER and MAJOR rows may exceed the cap. The cap is a setting in the central place (Q-24).
answered_by: maintainer
status: answered
context: |
  Topic: findings per reviewer.
  Intention: few strong findings, less triage and repair.
  Today: no cap; about four rows per reviewer in round 1, 26% about change-folder formalities (2026-11-07).
  Repository change: reviewer prompts, the runner checks the answer form.
  Architecture change: none.

In the context of reviewer answers, facing long lists of small rows, we decided on at most five rows by severity with BLOCKER and MAJOR exempt, to achieve a focused repair, accepting that a sixth minor row may go unreported — 2026-11-23

## Q-22 · Reviewers check their own findings (py5)

asked: 2026-11-23
answer: A — each reviewer checks its findings once against the code in its own context before it answers and drops what it cannot evidence. One pass, not the two py5 proposed.
answered_by: maintainer
status: answered
context: |
  Topic: self-check of reviewer findings.
  Intention: better findings per call, not more rounds.
  Today: one pass per reviewer.
  Repository change: reviewer prompt text; the runner is unchanged.
  Architecture change: none.

In the context of reviewer precision, facing false findings that cost triage, we decided on one self-check pass per reviewer, to achieve fewer false rows at moderate cost, accepting about twice the compute per reviewer call — 2026-11-23

## Q-23 · The tapering ladder (r3b6)

asked: 2026-11-23
answer: A — r3b6 is closed, superseded by this change: a tapering seating can be set later without a code change, because rounds and seats per round are central settings (Q-24).
answered_by: maintainer
status: answered
context: |
  Topic: shrinking reviewer count per round.
  Intention: settings, not code, decide the seating.
  Today: r3b6 drafted for the old ladder of up to six rounds.
  Repository change: none.
  Architecture change: none.

In the context of the per-round seating, facing a draft for the old ladder, we decided to close it, to achieve one shape whose seating is a setting, accepting no tapering default — 2026-11-23

## Q-24 · Rounds, reviewers and lenses are easy to change later

asked: 2026-11-23
answer: Requirement of the maintainer (2026-11-23): the number of review rounds, the number of reviewers per round and the lenses (perspectives) must be easy to change afterwards — one edited value in the central place of Q-4/Q-16, validated, no code change, no constant repeating it; the finding cap (Q-21) and the early-end condition (Q-20) are settings there too.
answered_by: maintainer
status: answered
context: |
  Topic: changeability of the loop's shape.
  Intention: tune the loop by measurement without a new change.
  Today: Q-4 and Q-16 already put seats and rounds in one place.
  Repository change: the spec lists every such setting with its validator and a test that a changed value takes effect.
  Architecture change: none beyond Q-4.

In the context of a loop shape that will be tuned, we decided that rounds, reviewers per round and lenses are central, validated settings, to achieve a change by one edited value, accepting a validator and tests for each setting — 2026-11-23

## Q-30 · Two reviewers per lens: a fixed best and a random challenger

asked: 2026-11-23
answer: Every lens always seats exactly two reviewer models, on every change (small changes included). Seat 1 is the fixed best model, today `deepseek-v4.1-flash`. Seat 2 is drawn at random, at run preparation, from the other models the availability report lists as reachable at that time; the draw and its seed are recorded in the run. The runner measures, per model and per lens, the share of its rows the orchestrator accepted (with bead coding-harness-qut1's per-model measure), and the run report says when a challenger has overtaken the fixed seat. The switch itself stays a maintainer edit of the central setting (as S-3 and Q-26). Both seats, the model of seat 1 and the challenger pool are settings of Q-24.
answered_by: maintainer
status: answered
context: |
  Topic: the seating of each lens.
  Intention: keep the best known reviewer and keep measuring whether another model becomes better.
  Today: Q-2 seated one reviewer per lens on a small change and three (best, cheapest, Codex) otherwise; Codex no longer sits in a lens.
  Repository change: seating, random draw with recorded seed, per-model accepted share in the run report; the substitute list of Q-25 still covers a failed seat.
  Architecture change: replaces the seating of Q-2 and the round-1 Codex seat; phase 6 is unchanged.

In the context of the seating of each lens, facing a best reviewer known
today and models that change over time, we decided on two seats per lens —
the fixed best model and a random reachable challenger — with a per-model
accepted share in every run report, to achieve a stable review and a
running measurement of a possible new best model, accepting that a weak
challenger sometimes takes the second seat and that the switch waits for
the maintainer — 2026-11-23

## Q-25 · A seat fails (S-7)

asked: 2026-11-23
answer: B — when a required seat fails (exhausted quota, timeout), the runner seats a substitute model for that lens from a declared substitute list in the central setting (Q-24); the report names the failure and the substitute. The family rule of Q-8 holds for the substitute.
answered_by: maintainer
status: answered
context: |
  Topic: a failed seat.
  Intention: settle an open spec-review ambiguity of 2026-11-10.
  Today: the spec admits two readings.
  Repository change: the rule in the runner and the spec.
  Architecture change: none.

In the context of a failed seat, we decided on a substitute from a declared list, to achieve a complete round despite outages, accepting one more model per lens to maintain — 2026-11-23

## Q-26 · Who ends the shadow period (S-8)

asked: 2026-11-23
answer: A — always the maintainer: after ten counting changes the runner reports how often the trigger was right and what the second round found in addition; the maintainer switches the mode with one value in the central setting. This replaces Q-12's automatic switch on clear data; 'clear' needs no definition.
answered_by: maintainer
status: answered
context: |
  Topic: the end of the shadow period.
  Intention: settle an open spec-review ambiguity of 2026-11-10.
  Today: the spec admits two readings.
  Repository change: the rule in the runner and the spec.
  Architecture change: none.

In the context of the end of the shadow period, we decided on the maintainer always decides from a report, to achieve a simple, testable rule, accepting a wait for the maintainer even when the data are clear — 2026-11-23

## Q-27 · A mechanism repair after the stop (S-15)

asked: 2026-11-23
answer: A — when the maintainer chooses a mechanism repair after the stop, that recorded choice authorises exactly one more phase-6 re-check, scoped to that repair; then the cap holds again. The choice is recorded in findings.md with the maintainer's word; no state release or loss resets the budget.
answered_by: maintainer
status: answered
context: |
  Topic: the review cap after the stop.
  Intention: settle an open spec-review ambiguity of 2026-11-10.
  Today: the spec admits two readings.
  Repository change: the rule in the runner and the spec.
  Architecture change: none.

In the context of the review cap after the stop, we decided on one authorised re-check of the mechanism repair, to achieve no unreviewed repair merges, accepting one more review call in that case — 2026-11-23

## Q-28 · Maintainability and small logic MINORs (S-17)

asked: 2026-11-23
answer: A — a small logic or state MINOR is repaired; a maintainability MINOR triggers no repair and goes to the weekly clean-up bead, as style does under Q-7.
answered_by: maintainer
status: answered
context: |
  Topic: MINOR rows outside tests, security and false statements.
  Intention: settle an open spec-review ambiguity of 2026-11-10.
  Today: the spec admits two readings.
  Repository change: the rule in the runner and the spec.
  Architecture change: none.

In the context of MINOR rows outside tests, security and false statements, we decided on logic is repaired, maintainability is collected, to achieve fewer repairs without leaving real defects, accepting maintainability debt waits for the weekly bead — 2026-11-23

## Q-29 · What the Markdown gate blocks (S-18)

asked: 2026-11-23
answer: A — only errors on lines the change itself wrote block, measured against the merge base with main, the same locally and in CI; legacy errors on untouched lines stay until a targeted clean-up.
answered_by: maintainer
status: answered
context: |
  Topic: Markdown errors in changed files.
  Intention: settle an open spec-review ambiguity of 2026-11-10.
  Today: the spec admits two readings.
  Repository change: the rule in the runner and the spec.
  Architecture change: none.

In the context of Markdown errors in changed files, we decided on only changed lines block, to achieve small changes to large legacy files, accepting legacy errors stay until a clean-up — 2026-11-23

## Provisional agent decisions on the spec-review ambiguities (2026-11-23)

Maintainer's answer A of 2026-11-23: the orchestrator decides the smaller open ambiguities of the 2026-11-10 spec review by its recommendation, marked as provisional agent decisions; the maintainer sees the list on the plan card and may change any line. S-7, S-8, S-15, S-17 and S-18 go to the maintainer as questions.

- [DETAIL] **S-1 (provisional agent decision):** resolved by Q-24 — no criterion, prompt, test or doc fixes the number of rounds, seats per round or lenses; criteria name the setting and test that a changed value takes effect.
- [DETAIL] **S-3 (provisional agent decision):** Reading A — a seat's "best measured precision" is a dated citation in the central setting; the validator checks that the citation exists and names a measurement date; a stale or wrong value is a maintainer edit, not a red criterion. Reason: Q-24 makes seating an edited value; a runner that re-seats itself would contradict it.
- [DETAIL] **S-4 (provisional agent decision):** Reading C — an out-of-lens BLOCKER is triaged and repaired like any row but enters no lens's observation, so the three-seat basis of each lens stays intact.
- [DETAIL] **S-11 (provisional agent decision):** Reading A — an added check question is committed on the branch of the change whose phase 6 found it and reaches other lanes when that PR merges; "applies immediately" is reworded to "applies from the merge on".
- [DETAIL] **S-13 (provisional agent decision):** Reading B — only changes with full three-seat lenses count toward the ten shadow changes; small changes are reported but do not count.
- [DETAIL] **S-21 (provisional agent decision):** Reading A — a lens with an undefined singleton share (S=0) or an incomplete observation does not trigger the second round; the run reports it.

## Provisional agent decisions on spec review round 2 (2026-11-23)

Under the maintainer's answer A of 2026-11-23 the orchestrator decides the rows of spec review round 2 by its recommendation, marked provisional; the plan card lists them for the maintainer.

- [DETAIL] **S2-1 (provisional agent decision):** Reading A — "all repaired" means every MINOR that the MINOR rule requires to be repaired; deferred maintainability or style rows do not block the early end.
- [DETAIL] **S2-2 (provisional agent decision):** Reading A — only accepted rows count; a rejected MAJOR or BLOCKER does not stop the early end.
- [DETAIL] **S2-3 (provisional agent decision):** Reading A — one independent challenger draw per lens; each pick and the seed are recorded.
- [DETAIL] **S2-4 (provisional agent decision):** The free second round's three models are drawn with a recorded seed from the reachable pool, three distinct families, Codex excluded, the implementer-family rule applied; the substitute list of Q-25 covers it. The pool is a Q-24 setting.
- [DETAIL] **S2-5 (provisional agent decision):** The spec lists every setting key with type, allowed values or range, initial value and meaning: rounds per change 1–2, seats per lens 1–3, lenses as a non-empty list of declared lens ids, finding cap 1–20, early-end on or off, challenger pool and substitute list as lists of declared model ids. Values outside a range refuse at load; a test per key shows that a changed value takes effect.
- [DETAIL] **S2-6 (provisional agent decision):** The trigger compares the singleton share directly with its threshold; no separate jackknife quantity.
- [DETAIL] **S2-7 (provisional agent decision):** Reading A — a seat counts as one call however many bounded chunks its input uses.
- [DETAIL] **S2-8 (provisional agent decision):** Count only MINOR rows: at most the cap of MINOR rows per answer, BLOCKER and MAJOR not capped; rows ranked by severity.
- [DETAIL] **S2-9 (provisional agent decision):** Rows that break the answer form (no file and line, MINOR over the cap) are dropped and listed in the report; the rest of the answer stands; the seat does not count as failed. A finding about something absent cites the path where it belongs and the line `0`.
- [DETAIL] **S2-10 (provisional agent decision):** Reading A — the answer-form rules apply to the phase-4b reviewers (round 1 and the free round); phase 6 keeps its form.
- [DETAIL] **S2-11 (provisional agent decision):** Reading A — the implementer's family is the recorded phase-4 implementer model; repair models do not widen it.
- [DETAIL] **S2-12 (provisional agent decision):** Reading A — at most one extra phase-6 re-check per change in total.
- [DETAIL] **S2-13 (provisional agent decision):** Reading A — the mechanism-fix rule fires on two confirmed findings raised in phase-6 re-checks, as written.
- [DETAIL] **S2-14 (provisional agent decision):** Reading B — the overtake is measured cumulatively per model and lens over all runs since the fixed seat was set, and flagged only when both models have at least 20 triaged rows on that lens.
- [DETAIL] **S2-15 (provisional agent decision):** A loop already running when this change merges finishes under the two-round house rule of AGENTS.md (PR #436), not under the old loop-until-clean.
- [DETAIL] **S2-16 (provisional agent decision):** "Stopped" means stopped by the maintainer or by an outage; a change that reached the phase-6 limit counts toward calibration.
- [DETAIL] **S2-17 (provisional agent decision):** Out-of-lens rows of any severity are triaged and repaired when taken but enter no lens observation (extends S-4).
- [DETAIL] **S2-18 (provisional agent decision):** A failed seat gets one retry of the same model, then the substitutes in list order (order recorded); a failed challenger is replaced by a new draw. If no substitute answers, the run records a waiting state; the next invocation resumes it; after 5 hours it is reported as stopped.
- [DETAIL] **S2-19 (provisional agent decision):** A deferred row gets the Status prefix `deferred — clean-up`; a report command lists deferred rows of a closed ISO week that no clean-up bead names; criterion 21 is tested on a fixture of that command.
- [DETAIL] **S2-20 (provisional agent decision):** A MINOR outside the listed classes (for example performance, a documentation omission) is repaired unless the reviewer marks it maintainability, style or taste.
- [DETAIL] **S2-21 (provisional agent decision):** The reconciler records mechanism, trigger and violated invariant as separate fields, and the grouping check compares them.
- [DETAIL] **S2-22 (provisional agent decision):** Locally the base is `git merge-base HEAD origin/main` after a fetch; in CI it is the PR base commit.

## Provisional agent decisions on spec review round 3 (2026-11-23)

Third and last spec review round (AGENTS.md phase 2a: the final draft after round three needs no new review). Decided by the orchestrator under the maintainer's answer A, marked provisional, listed on the plan card.

- [DETAIL] **S3-1 (provisional agent decision):** Every datum the validator checks gets a key: `model_families` (model id -> family), `substitutes` per lens, `seat1_model` with `seat1_since` (date) and `seat1_citation`; unknown keys still refuse before any call.
- [DETAIL] **S3-2 (provisional agent decision):** Reading A — this change builds only the `singleton_share` trigger; another trigger kind is a later change; the maintainer's end-of-shadow decision sets the mode, not a new rule.
- [DETAIL] **S3-3 (provisional agent decision):** A dropped row (no location, MINOR over the cap) is "not admitted": it never reaches triage and is listed in the report; "accepted" stays the orchestrator's triage term.
- [DETAIL] **S3-4 (provisional agent decision):** Pools contain only models whose data terms are valid on the day of run preparation; an expired model is skipped and named in the report; seat 1 with expired terms falls back to the first substitute and the report says so.
- [DETAIL] **S3-5 (provisional agent decision):** The free pool excludes the endpoint `openai-codex` and every model of the OpenAI family; families come from `model_families`.
- [DETAIL] **S3-6 (provisional agent decision):** Each physical call self-checks its own rows; the cap applies to the consolidated seat answer after merging the calls.
- [DETAIL] **S3-7 (provisional agent decision):** Reading A — with one seat per lens no share exists, so no positive trigger; the round-2 decision then follows only the early-end and minor rules; the report says the estimator is off.
- [DETAIL] **S3-8 (provisional agent decision):** Reading A — the night exception adds one check beyond the configured limit; with `phase6_rechecks: 0` phase 6 runs once and the night exception allows one re-check.
- [DETAIL] **S3-9 (provisional agent decision):** `round_order` is derived from `rounds` and is no key of its own; the contract drops it.
- [DETAIL] **S3-10 (provisional agent decision):** Reading B — the free round's three models are drawn when the free round starts, from the models reachable then; seed and picks are recorded.
- [DETAIL] **S3-11 (provisional agent decision):** `seat1_since` (see S3-1) records when the fixed seat was set; the overtake window starts there.
- [DETAIL] **S3-12 (provisional agent decision):** A check question is valid when it cites Q-13's approved list by its exact text or a phase-6 row id that resolves in a merged change; a reworded question needs a new citation.
- [DETAIL] **S3-13 (provisional agent decision):** "Maintainability" is the nature of the defect, assigned by the orchestrator in triage, not the reporting lens.

## Decided by the agent — the ADR number

[DETAIL] **The ADR draft of this change is ADR 0027**
(`docs/adr/0027-focused-review-with-a-shadow-period.md`), renamed from 0026 on
2026-11-10. Reason: the change central-config (bead coding-harness-twvx)
drafted `docs/adr/0026-one-central-harness-configuration.md`, and this change
waits for its skeleton (Q-4), so central-config merges first and keeps 0026.
The maintainer was told at the central-config plan card. The runner's audit
lines in `findings.md` keep the old file name as recorded.

## Open — not counted

- The research questions of 2026-11-08 are not answered: (a) evidence for
  lens-based against unfocused review; (b) capture-recapture estimators for
  three reviewers per lens and a defensible threshold; (c) evidence on
  ensembles and model diversity of LLM reviewers; (d) cost of 15 round-1
  calls against today's rounds and verify runs. The stage-1 exploration of
  2026-11-09 (research.md) did not read the bead and covers the repository
  only. Answered on 2026-11-09 by the Opus research section of research.md.
- Open after the answers of 2026-11-10 and answered the same day: who sits in
  the free second round (Q-14) and what triggers it on a small change (Q-15).
