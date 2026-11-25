---
title: "Research — frontmatter-batch-log"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.21
owner: Data Architect
provenance: human-written
tags: [research]
class: bounded
neighbours: []
---

# frontmatter batch log — Research

## Topic (bead coding-harness-bxxt.21, copied by the orchestrator 2026-11-25)

Class: bounded.

Why: scripts/check_frontmatter_current.py:180-189 runs git log -1 --no-
merges per clean held file (184); the external analysis measured the gate at
6-16 s (count of ~893 files not re-counted). What: one batched git log --
name-only pass. Related: coding-harness-y6h0, coding-harness-5v6t.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp, night run 2026-11-24-a), from an external verify-speed analysis.



PARENT
↑ ○ coding-harness-bxxt: (EPIC) Verify speed and machine load P1

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
