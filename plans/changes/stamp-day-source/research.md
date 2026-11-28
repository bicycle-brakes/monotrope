---
title: "Research — stamp-day-source"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5v6t
owner: Data Architect
provenance: human-written
tags: [research]
---

# stamp day source — Research

## Topic (bead coding-harness-5v6t)

Class: bounded.

Measured 2026-11-09: the outcome-test round-5 repair committed 6bf5c6fc at 2026-11-09 01:30:27 +0100 with docs/WORKFLOW.md changed and its header still 'updated: 2026-11-08'. check_frontmatter_current.py takes 'the committer date (in the offset recorded in the commit) of the newest non-merge commit' (its docstring), i.e. 2026-11-09, so the gate went red; every later repair attempt of the change failed only on that gate (three attempts of F6-2..F6-4, about 3 h lost, attempt saved at refs/stage2/attempts/outcome-test/orchestrator-saved-20261109). The runner's stamp before its checkpoint evidently used a different day than the commit's recorded offset. Do: one day source for stamping and checking (the commit's own offset, or UTC on both sides), with a test that commits at 00:30 +0100.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
