---
title: "Decisions — restore-keeps-runner-entries"
category: decisions
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-7awf
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, runner]
---

# Decisions — restore-keeps-runner-entries

Phase-1a record for `restore-keeps-runner-entries` (bead `coding-harness-7awf`).

## SKIP · interview

status: skipped
reason: "Bounded runner bug fix seen twice (bead coding-harness-5tyh, loop rows L1-2 and L9-3), run autonomously under the bounded standing grant (2026-11-25): when the runner restores findings.md after a rejected attempt, the entries the runner itself wrote (scan and audit lines) survive. The bead names two remedies (restore only model-written content, or re-append the runner's entries after the restore); which one is a reversible [DETAIL] for the spec. No product or architectural choice is open."
