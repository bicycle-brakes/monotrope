---
title: "Research — research-seat-substitute"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-0ysc
owner: Data Architect
provenance: human-written
tags: [research]
---

# research seat substitute — Research

## Topic (bead coding-harness-0ysc)

Class: bounded. Maintainer 2026-11-25 (session 9200c6b1), step 1 of the swarm
optimisation. Measured 2026-11-25 on every v2 run in the repository: 2 of 10
runs complete (detached-job-launcher 1/4, ontology-relation-layer 1/4,
pi-work-route 0/2), mostly because single seats time out
(deepseek-v4.1-flash on repository topics). Change
`scripts/stage2_research_run.py`: a seat that times out or fails gets exactly
one substitute from its own trio (the next reachable admitted model of that
seat's class, recorded in the run's history with the reason); only a seat
whose substitute also fails leaves the run incomplete. Together with
`coding-harness-n76m` (finder limit follows the measured repository size).
Measure: completion rate of the next runs.

Further evidence (orchestrator, 2026-11-27): `state-first-records` runs 4
(`355d1c04`) and 5 (`a6cd8479`) ended incomplete because finder slot
`finders-0-2` (repository seat 2, `mimo-v2.6-flash`) returned a tool-call
text instead of finder JSON (`invalid-report`); run 6 completed after the
orchestrator moved that seat to `glm-5.3-flash` by hand. An invalid report is
a failure of the same kind as a timeout for this change.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
