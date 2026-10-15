---
title: "Decisions — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, phase-1, swarm, opencode-go]
---

# Phase 1 as a research swarm — Decisions

Phase 1a for bead coding-harness-icw. Q-1 and Q-2 were answered by the
maintainer in the conversation on 2026-10-13 and 2026-10-14 before this file
was written (recorded in the bead's notes); this file records them. Later
questions were asked on 2026-10-14 with their context first.

## Q-1 · Who researches, and on which models

asked: 2026-10-13
answer: phase 1 runs as a swarm of OpenCode Go models with different tasks and models; each research topic is worked by one free model and one Flash model; the first stage always uses all free models automatically.
answered_by: maintainer
status: answered

Free models seen in `pi --list-models` on 2026-10-13: longcat-2.5-preview-free,
space-bunny, hy4-preview; Flash: deepseek-v4.1-flash, mimo-v2.6-flash (bead
notes, coding-harness-km1).

In the context of one exploring model that misses what a second view would
find, facing the choice between one explorer and a swarm, we decided on a
swarm of free and Flash OpenCode Go models to achieve two independent views
per topic at low cost, accepting more calls per change. — 2026-10-13

Addendum 2026-10-15: `space-bunny` and `hy4-preview` turned out to be paid
OpenCode Go models (OpenCode Go and Zen documentation and the pinned Pi
1.1.0 registry, read 2026-10-15); the free seats are now
`longcat-2.5-preview-free`, `space-bunny-free` and `big-pickle`. Big Pickle
may use what it receives to improve the model. Asked whether that is
acceptable, the maintainer said: "Es ist für mich okay wenn es nur anhand des
Opus Satzes ist und die Modelle nicht in die repo schauen". The maintainer
also noted that the free models change constantly and the list must keep
being adjusted.

## Q-2 · The research topics

asked: 2026-10-14
answer: six topics, each worked by one free and one Flash model, then a judge reconciles the pair — (1) code today, (2) rules and decisions, (3) history, (4) tests and gates, (5) risks and edge cases, (6) outside world and neighbours.
answered_by: maintainer
status: answered

The maintainer agreed to the six proposed topics with "Ja" on 2026-10-14
(bead notes hold each topic's scope).

In the context of a research that must cover code, rules, history, tests,
risks and neighbours, facing the choice between free-form research and fixed
topics, we decided on six fixed topics to achieve that no area is skipped,
accepting twelve research calls per change. — 2026-10-14

## Q-3 · What the free models may see

asked: 2026-10-14
answer: the free models do the kind of research that needs no repository content — finding best practice, what already exists outside; they are not given repository content. The swarm follows set patterns: the search for best practice, the comparison with the overall architecture, and the comparison with the nearby specs.
answered_by: maintainer
status: answered

Context given with the question: the repository is private (checked
2026-10-14); the data terms of the three paid OpenCode Go models were read
(retention 0 days, no training), those of the free models were not. The
maintainer's words: "nutzte die kostenlosen modelle für die art recherche, für
die die repo nicht gelesen werden muss. sowas wie best practice finden, was
gibt es da draußen schon. der schwarm soll ja auch gewissen mustern folgen,
wie die such nach best practice, den abgleich mit der gesamtarchitektur und
den naheliegenden specs". How the patterns map onto the six topics of Q-2,
and which model takes a repository-bound topic's second seat, is left to the
spec.

In the context of free models whose data terms are unread and a private
repository, facing the choice between waiting for their terms and giving them
no repository content, we decided to give them only outward research to
achieve the free first stage without exposing the repository, accepting that
repository-bound topics need another model for their second view. —
2026-10-14

## Q-4 · Which changes get the swarm

asked: 2026-10-14
answer: changes of class `feature` and `architectural`; a `bounded` change keeps the single exploration.
answered_by: maintainer
status: answered

In the context of twelve research calls and a judge per change, facing the
choice between every change and the larger classes, we decided on feature and
architectural changes to achieve depth where it pays, accepting that a small
change gets one view. — 2026-10-14

## Q-5 · Who judges

asked: 2026-10-14
answer: Opus 5.5 reconciles the pair of each topic into `research.md`.
answered_by: maintainer
status: answered

Options shown: MiMo-V2.6-Pro (recommended by the session: cheap, spares Codex
and Claude quota), Codex Sol (five-hour limit), Opus 5.5 (Claude quota; the
orchestrating session itself, outside the runner's leak check). The
maintainer chose Opus 5.5.

In the context of two views per topic that may contradict each other, facing
the choice between an OpenCode Go model, Codex and Opus as the judge, we
decided on Opus 5.5 to achieve the strongest reconciliation, accepting the
Claude quota it uses. — 2026-10-14

## Q-6 · What the free models learn about the change

asked: 2026-10-14
answer: "Kurzes Thema mitgeben: Die freien Modelle bekommen eine von Opus geschriebene Ein-Satz-Beschreibung ohne Datei- und Codenamen (zum Beispiel „Container-Isolation für KI-Agenten-Läufe“). Die Spec wird vor der Nacht angepasst."
answered_by: maintainer
status: answered

Asked after the first draft (`01ff6d9`), whose spec gave the free models only
fixed generic questions. Context shown: with the topic they find practice that
fits this change; without it the private repository stays entirely local.
Options shown: keep generic questions (recommended by the session while the
free models' data terms are unread), or pass a short topic. The maintainer
chose the short topic. This narrows Q-3: the one-sentence topic is the only
change-derived text a free model receives.

In the context of free researchers whose generic questions yield generic
practice, facing the choice between no change information and a one-sentence
topic, we decided on an Opus-written sentence without file or code names to
achieve best practice that fits the change, accepting that the free providers
learn what the change is about. — 2026-10-14

## Q-7 · How the topics are cut and who works each

asked: 2026-10-15
answer: "ja, finder als schritt 0, ich möchte für jedes thema drei agenten, einmal deepseek, einmal mimo, einmal haiku, jeweils auch eigener blickwinkel, es soll immer einen template gefolgt werden. bei der online recherche möchte ich, dass alle verfügbaren freien modelle zu diesen thema recherchieren, also 1 bis x modelle"
answered_by: maintainer
status: answered

Asked after phase 6 and the F-2 to F-10 repairs, while walking through the
six topics of Q-2. The maintainer first asked for smaller topics; the session
proposed thirteen (ten repository topics, three online topics) and, after an
online search on multi-agent research design (Anthropic's multi-agent
research system, locator-then-analyzer code research, STORM, studies on
model diversity), a step 0 "finder" that maps files, ADRs, tests and
neighbouring specs (`neighbours:` in the header of `research.md`, later the
spec's) for every repository topic. The maintainer had also said, on the
free roster, that the free models change constantly and the list must keep
being adjusted; "all available free models" replaces a fixed roster.

This amends Q-1 (one free and one Flash model per topic) and Q-2 (six
topics): each repository topic is worked by three agents — DeepSeek Flash,
MiMo Flash and Haiku 5.5 — each from its own perspective and on one fixed
template; each online topic is worked by every free model available at run
time. The exact topic list, the perspectives and the template are settled
in the following questions and then in the spec.

In the context of six broad topics shared by two models and a fixed free
roster that goes stale, facing the choice between keeping that cut and
smaller topics with a finder step, we decided on a finder, three agents with
distinct perspectives per repository topic on one template, and every
available free model on each online topic to achieve clear assignments and
independent views, accepting many more calls per run. — 2026-10-15

Addendum 2026-10-15: on where the neighbouring specs are kept, the
maintainer said: "die nachbar specs sollen auch im specs header festgehalten
werden." The finder's neighbours (the ones given in the header of
`research.md` plus its marked suggestions, once accepted) are carried into a
`neighbours:` field in the header of `spec.md`; the exact field form and
its check are settled in the spec.

Addendum 2026-10-15: on the perspectives, the session proposed one fixed
perspective per model (DeepSeek existing state, MiMo critique, Haiku
impact). The maintainer said instead: "ich möchte, das jedes model die
gleichen blcikwinkel am anfang bekommt um deren ergebnisse evaluieren zu
könenn." At the start every model receives the same brief and perspectives
for a topic, so that their results can be compared and evaluated; per-model
perspectives are a later decision on that evidence.

Addendum 2026-10-15: on how the research is used, the maintainer said: "die
recherce ergebnisse sollen dann klar in die interview phase und die spec
definition eingehen. es dürfen gegenfalls auch mehr interview fragen
gestellt werden". The reconciled findings feed phase 1a and phase 2
traceably, and the interview may ask more questions than the class
minimum where the research raises them.

Addendum 2026-10-15: the maintainer accepted ("ja") the report template —
one fixed template; at most seven key claims, each with an id, one-sentence
statement, evidence (`path::symbol` or URL), kind (fact, assumption,
judgement) and confidence with its basis; counter-evidence; what was not
read; relation to the neighbouring specs; questions for the spec — and the
judge's per-model scoring (supported, refuted, unique, off-brief), recorded
in `research.md`. Also accepted: interview questions derive from the
reports' `[DECISION]` claims and from disagreements between models, naming
the claim ids; spec criteria name the claims or answers they rest on; a gate
checks that no research `[DECISION]` is lost.

### Topic walk-through (2026-10-15)

- Topic 0, finder — guiding questions: which files and functions the change
  touches; which ADRs and rules apply; which tests and gates check those
  places; which specs are neighbours (those in `neighbours:` are given,
  further ones are marked suggestions). Boundary: it locates and lists,
  it does not judge. Output: one list per question, each entry
  `path::symbol` with one sentence why. The maintainer chose option A:
  DeepSeek Flash, MiMo Flash and Haiku 5.5 each search, and Opus 5.5 merges
  the three lists into one map (answer: "A").
- Topic 1, code and reuse — guiding questions: which existing functions or
  modules already do part of what the change needs; which pattern in the
  repository serves as a model (a similar script or test); what would have
  to change in existing code to reuse it, and what speaks against it.
  Boundary: only existing code on the finder's map plus what it imports
  directly; no judgement whether the change is sensible; no proposals for
  new code. Three agents on the same brief; template report with every key
  claim backed by `path::symbol` (answer: "ja").
- Topic 2, callers and interfaces — guiding questions: who calls the
  affected functions, scripts or commands (code, tests, Makefile, CI, hooks,
  prompts); which interfaces are affected (signatures, options, file and
  header formats, configuration keys); which callers would have to change
  with an interface and which only read; which interfaces other
  repositories use (lakeswitch, the kit). Boundary: only connections to the
  finder's map; no judgement whether an interface is good (topic 4). Three
  agents on the same brief; every key claim names caller and callee as
  `path::symbol` (answer: "ja").
