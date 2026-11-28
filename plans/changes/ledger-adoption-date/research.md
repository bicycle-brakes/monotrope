---
title: "Research — ledger-adoption-date"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-64fa
owner: Data Architect
provenance: human-written
tags: [research]
---

# ledger adoption date — Research

## Topic (bead coding-harness-64fa)

Class: bounded. check_criterion_ledger.py exempts plans before a hard-coded CUTOFF = 2026-10-11; decision PR #276 (bead coding-harness-wpv) records criterion-ledger: 2026-10-29 in decisions/adoption.yaml, which no code reads yet. Make the gate read the adoption entry (one source). Note: moving from 10-11 to 10-29 widens the exemption to archived plans of 10-11..10-28 without a ledger — state that in the PR.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
