---
title: "Research — verify-cheap-first"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.1
owner: Data Architect
provenance: human-written
class: bounded
tags: [research]
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
---

# verify cheap first — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-bxxt.1, class bounded. Between 2026-11-04 and 2026-11-09,
11 red full runs of `make verify` had a green test gate and failed afterwards
on a gate that takes seconds (front-matter currency 8 times, question context
3 times): 3.3 hours of test execution for a result that was available at
once. Wanted: `scripts/verify_all.sh` orders the blocking gates cheapest
first — the order is declared once, not hard-coded twice — and ends a local
run at the first red blocking gate, naming the gates it did not run. Hosted
CI keeps running every gate. Done when a planted red front-matter gate ends a
local run before the test gate starts, a green run still runs every gate, and
tests pin both. Source: `docs/research/2026-11-09-make-verify-long-term.md`.
The maintainer asked on 2026-11-10 for the speed-up of the full check as fast
as possible.

Questions for the exploration: where the gate order is declared today
(`decisions/gates.yaml`, `scripts/ci_gates.py`, `scripts/verify_all.sh`) and
whether the order can change without editing the held file
`decisions/gates.yaml`; how a report-only gate differs from a blocking one in
the run; which callers read the full list of gate results (the runner's
post-run check, the run log `verify-duration.jsonl`, the stop hook) and would
misread a run that ends early; how the `--job docs` subset is ordered.
