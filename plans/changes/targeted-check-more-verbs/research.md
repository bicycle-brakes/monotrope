---
title: "Research — targeted-check-more-verbs"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-0swp
owner: Data Architect
provenance: human-written
class: bounded
tags: [research]
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
---

# targeted check more verbs — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-0swp, class bounded. Today every implement attempt and
every draft post-check waits for the machine-wide verify lock: on 2026-11-10
runner jobs waited 44 to 59 minutes for a full check of about 28 minutes, and
a draft waited 92 minutes for a documents job of 30 seconds. A repair already
runs a targeted check through the touch map (bead coding-harness-gxwg); the
full check runs before phase 6 and in CI. Wanted: implement attempts and the
draft post-check use the same targeted selection; the review verb keeps its
fresh full check before its model call; CI keeps the full suite. No new
guarantee is given up: phase 6 and CI still run everything. The maintainer
lifted the note "wait for the testing-strategy report" on 2026-11-10 and
asked for the speed-up of the full check as fast as possible.

Questions for the exploration: how the targeted check of the repair verb
selects gates and tests (`run_targeted`, `targeted_selection`, the touch map)
and where implement and draft call the full check instead; why a change that
touches `scripts/stage2.py` always fell back to the full check (bead note of
2026-11-07: three timeouts at five minutes, nineteen fallbacks) and what a
selection for such a change would need; whether the documents job of the
draft needs the machine-wide lock at all; which tests pin today's behaviour.
