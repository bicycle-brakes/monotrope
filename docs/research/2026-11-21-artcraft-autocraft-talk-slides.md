---
title: "Artcraft and AutoCraft — what a talk's slides state"
category: research
created: 2026-11-21
updated: 2026-11-21
last_reviewed: 2026-11-21
status: draft
implementation_status: none
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [evaluation, outside-practice, software-factory, rust, ci, research-input]
---

# Artcraft and AutoCraft — what a talk's slides state

On 2026-11-21 the maintainer shared twelve screenshots of a conference talk
(slides 26 to 40 of 40, shown in a browser at a local address) and asked how
the team behind it builds its apps, on which technical base, why it succeeds,
and what this repository can use from it. This note is the **source input**
for a research-swarm pass: it records only what the slides show, with no
judgement and no outside reading. Every claim below is the slide's claim, not
a measurement of ours; the numbers carry the dates the slides give.

Who: the last slide names the contact `hello@storyteller.ai`; a CI slide
credits its data to "GitHub Actions · storytold org · Oct 13 – Nov 11, 2026".
The dashboards are served from `artcraft.build`. The app repositories named
on the slides are photocraft, pdfcraft, wordcraft, designcraft, filmcraft,
lightcraft, deckcraft, gridcraft, cadcraft and vectorcraft ("every Craft
app"; one dashboard counts 25 repositories).

## Slide 26 — "Why Rust? Electron may no longer be necessary."

A table compares Rust with Electron for desktop apps on six rows: native
performance, small installers, low memory footprint, memory safety, lower
defect rate, fast cold start. Rust gets a full mark on every row; Electron a
half mark on native performance, memory safety and defect rate, and none on
the other three.

## Slide 29 — "Is Rust GUI Yet?"

Shows the public page `areweguiyet.com` ("The roots aren't deep but the seeds
are planted"): Rust suits native UI, but there is little consensus on the best
abstractions, and mature pure-Rust GUI options are few.

## Slide 31 — "CI is under incredible strain"

Figures for the organisation, 2026-10-13 to 2026-11-11, runner-hours
estimated from sampled job timings:

- 286,884 CI runs in 30 days, about 9,600 a day; 87 % from pull requests;
  542 workflows across 50 repositories.
- 45K runner-hours on pull-request checks alone; 63 machines busy all month.
- 38 min median per push to go green, p90 2.7 h.
- 1 in 2 pushes fail and go round again.
- Every release: 17 jobs on Windows, macOS and Linux, about 2.5 runner-hours,
  up to 6.7 h wall-clock; 415 releases that month.

## Slide 32 — "How agentic is this project?"

Two columns. "Let the agents run — 100 % agentic": web frontend, mobile app
UI/UX, games and game engines. "Keep a human in the loop — human design and
review, recommended or required": backend schema, database migrations, API
design, compliance and regulatory work.

## Slide 33 — "AutoCraft, an open-source software factory"

Five stages: (1) ingest issues — every community issue across every app;
(2) triage — dedupe, classify and route; (3) agentic development — agents
write the fix and open a pull request; (4) post-train and evals — models learn
from what merges; (5) ship — builds, releases and the launcher.

## Slide 34 — "The App Factory" (dashboard `artcraft.build/flow`)

A pipeline board, "Pipeline is On … switched on by cli 2026-11-11 12:46".
24,840 open items. Stages left to right with counts: Synced (14,688 open
issues, 10,152 open PRs; 24 h: 1,988 new, 1,395 closed) → Classify (15,535
settled of 24,840; waiting for a second opinion, waiting for the referee
1,275, scope disagreement 1,457, not classified yet 6,573) → Decide ("people
decide": 447 decisions waiting for an answer; categories such as wanted in
core, small extra, plug-in candidate, out of scope, check the reference app,
backlog) → Labels (1,688 labelled on GitHub; 7,043 "repo not approved") →
Review (660 reviewed: take 238, take with fixes 47, hold 362, close 13) →
Verify (passed 12, "CI is enough" 213, error 1). A "Waiting for people" bar
groups the human queues by reason (duplicates, decide, labels, merge queue,
scope disagreement, hold, held: not a clear fix, held: rounds failed, asked
the contributor, CI fix gave up, error, blocked: conflicts).

## Slide 35 — "Ingest issues" (dashboard `artcraft.build/progress`)

Issues from every Craft app land in one queue; each is parsed into report,
reproduction steps and context; agent-filed issues are labelled. Tracking
since 2026-11-02 across 25 repositories: 24,842 open; 93 done by the
pipeline (89 merged, 4 closed); 11,160 closed by others; 989 decisions
waiting. Of the closed or merged items since tracking began, 1 % were merged
by the pipeline and 89 % closed by others.

## Slide 36 — "Triage"

The factory sorts the queue before a human sees it: duplicates are merged;
issues are classified by risk and type; each is routed to the right
maintainer. A "Next" view lists runnable steps (classify new items, fix up
take-fix pull requests, fix issues, collect fix results, fix failing CI on
wanted pull requests); two steps show "breaker tripped: 2 of the last 10
fix-issue pushes broke a required check, an operator resumes it".

## Slide 37 — "Agentic development" (item page `artcraft.build/items/…`)

Agents pick up triaged issues: each issue gets an agent with the right app
context; agents write the fix and the tests; complex changes are flagged for
human review. The example item shows a step trail — review (Opus, "take with
fixes", $0.65), fix-up running (Sonnet), then verify, merge queue and
post-merge review — with per-step costs, and a pull-request body that states
the root cause with file and line references before the fix.

## Slide 38 — "Post-train and evals" (dashboard `artcraft.build/classifiers`)

Every merged change becomes training data: models are post-trained on
accepted pull requests, evals run on every release, reinforcement learning
improves the factory. The classifier board compares two classifiers on the
type label of 10,013 items (run 2026-11-12, one of them Haiku): 63.8 %
agreement overall (PRs 66.5 %, issues 61.0 %), by label from 30.5 % (small
extra) to 92.1 % (infra), by repository from 56.0 % to 75.8 %.

## Slide 40 — "Come build it with us"

Hiring systems engineers, infrastructure engineers, Rust experience; "100 %
of our code is open source"; 20 % of time on own projects.

## Open for the swarm

Not on the slides and not read here: the talk's spoken content, slides 1–25,
27–28, 30 and 39, the public repositories themselves, the UI framework the
apps use, how the factory is built (its code, scheduler, tracker, model
routing), and any measurement of success beyond the dashboard counts.
