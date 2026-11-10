---
title: "Research — origin-check-across-blocks"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-3h96
owner: Data Architect
provenance: human-written
tags: [research]
---

# origin check across blocks — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Intent of the change — from the bead, 2026-11-10

Written by the orchestrator before the first exploration, because an
explorer cannot read the tracker (bead coding-harness-3h96).

Class: bounded.

The Origin check of the repair brake validates only the newest phase-6 block
of `findings.md`. Once a newer phase-6 block exists, an older phase-6 row
with an invalid Origin cell escapes validation: `origin_refusal(None, text)`
returns `None` while `repair_targets` still selects the earlier row. The
`repair` verb can then call a model on an accepted finding whose provenance
is invalid. This was phase-6 finding F-1 of the change origin-cell (bead
coding-harness-ywbh; Codex, 2026-11-09, reproduced with the source
functions); that change is merged (pull request #359).

Wanted: every outstanding repair target is validated across all phase-6
blocks before any effect — before a model call and before a write.

To explore: where `origin_refusal` and `repair_targets` live in
`scripts/stage2.py`, how each reads the phase-6 blocks, which tests pin the
Origin check today, and which other callers rely on the newest-block
reading.
