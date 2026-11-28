---
title: "Research — restore-keeps-runner-entries"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-7awf
owner: Data Architect
provenance: human-written
tags: [research]
---

# restore keeps runner entries — Research

## Topic (bead coding-harness-7awf)

Class: bounded. Seen twice in fail-fast-attempts (bead coding-harness-5tyh, loop rows L1-2 and L9-3): when the runner restores findings.md after an attempt that edited a protected file, it also drops the entries the runner itself wrote (scan/audit lines). Case repair ended at the second case; needs a structural fix (restore only model-written content, or re-append runner entries after the restore).

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
