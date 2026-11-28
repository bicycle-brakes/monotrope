---
title: "Decisions — export-import-closure"
category: decisions
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, kit, export]
---

# Decisions — export-import-closure

Phase-1a record for `export-import-closure` (bead `coding-harness-5ane.7`).

## SKIP · interview

status: skipped
reason: "Bounded fix from the verified PR #437 audit (C-7), run autonomously under the bounded standing grant (2026-11-25): an exported instance must not fail on import; export scripts/bead_render.py (or cut the import) and add a test that every exported Python script imports only exported modules. Which of the two remedies is a reversible [DETAIL] for the spec. No product or architectural choice is open."
