---
title: "Decisions — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
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
