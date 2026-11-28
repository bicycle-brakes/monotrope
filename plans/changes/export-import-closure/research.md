---
title: "Research — export-import-closure"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.7
owner: Data Architect
provenance: human-written
tags: [research]
---

# export import closure — Research

## Topic (bead coding-harness-5ane.7)

Class: bounded. Why (audit C-7, confirmed): scripts/export/manifest.yaml has no rule for scripts/bead_render.py, while two exported scripts import it, so an exported instance fails on import. What: export bead_render.py (or cut the import), and add a test that every exported Python script imports only exported modules. Acceptance: the import-closure test is green on the export manifest. Source: PR #437 (full codebase audit, base 24632499), re-verified against main b9ce3ac0 on 2026-11-24 by five read-only checks in session c820a13d.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
