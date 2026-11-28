---
title: "Decisions — stage2-off-reason"
category: decisions
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-73gi.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, runner]
---

# Decisions — stage2-off-reason

Phase-1a record for `stage2-off-reason` (bead `coding-harness-73gi.6`).

## SKIP · interview

status: skipped
reason: "Bounded fix the bead fully specifies, run autonomously under the bounded standing grant (2026-11-25): --stage2-off takes a mandatory reason value (no nargs='?'), the after-the-fact guard in scripts/stage2.py and its test are removed, and the recorded reason stays where it is. No product or architectural choice is open."
