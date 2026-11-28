---
title: "Research — stage2-off-reason"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-73gi.6
owner: Data Architect
provenance: human-written
tags: [research]
---

# stage2 off reason — Research

## Topic (bead coding-harness-73gi.6)

Class: bounded. The flag takes an optional value, so a change name can be swallowed as the reason; a guard at scripts/stage2.py:11401 catches that after the fact. Make the value mandatory (no nargs='?'), delete the guard and its test, and keep the recorded reason where it is.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
