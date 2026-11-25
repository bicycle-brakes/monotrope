---
title: "Research — availability-scrub-import"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-vg9.2
owner: Data Architect
provenance: human-written
tags: [research]
class: bounded
neighbours: []
---

# availability scrub import — Research

## Topic (bead coding-harness-vg9.2, copied by the orchestrator 2026-11-25)

Class: bounded.

Why: scripts/stage2_availability.py:145 does 'from stage2 import scrub'
inside an except block of a function, while the module otherwise receives
the runner module as a parameter. It is the one import that closes the
stage2 <-> stage2_availability cycle and a second path to the same function,
so a monkeypatched or moved scrub is missed there.

What: use the runner parameter's scrub (or the shared secrets home once vg9
decides it) and add a test that the module does not import stage2.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp), from an external stage2.py modularization analysis.



PARENT
↑ ○ coding-harness-vg9: Refactor stage2.py into cohesive runner modules P2

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
