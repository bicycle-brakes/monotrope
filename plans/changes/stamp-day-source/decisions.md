---
title: "Decisions — stamp-day-source"
category: decisions
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5v6t
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# Decisions — stamp-day-source

Phase-1a record for `stamp-day-source` (bead `coding-harness-5v6t`).

## SKIP · interview

status: skipped
reason: "Bounded bug fix the bead specifies (measured 2026-11-09), run autonomously under the bounded standing grant (2026-11-25): stamping and checking the updated: date use one day source, with a test that commits at 00:30 +0100. Which source (the commit's own recorded offset, or UTC on both sides) is a reversible [DETAIL] the spec settles; preferring the commit's offset because check_frontmatter_current.py already documents it. No product or architectural choice is open."
