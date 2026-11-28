---
title: "Research — bead-topic-in-research"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5vts
owner: Data Architect
provenance: human-written
tags: [research]
---

# bead topic in research — Research

## Topic (bead coding-harness-5vts)

Class: bounded.

Why: a stage-1 explore (--stage2-off, Haiku or Sonnet) cannot read the tracker; on 2026-11-25 the first explore of test-ci-shared-tree guessed its topic from the change name and had to be rerun. For every later lane the orchestrator copied the bead description into research.md by hand. Recorded as tracker memory stage1-explore-needs-topic.

What: scripts/new_change.py already reads the bead's status from the tracker export; it also writes the bead's description under a '## Topic (bead <id>)' heading below the research title, so every harness's explorer sees it. A missing or empty description is named, never invented.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
