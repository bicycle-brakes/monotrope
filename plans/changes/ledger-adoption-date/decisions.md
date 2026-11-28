---
title: "Decisions — ledger-adoption-date"
category: decisions
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-64fa
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, gates]
---

# Decisions — ledger-adoption-date

Phase-1a record for `ledger-adoption-date` (bead `coding-harness-64fa`).

## SKIP · interview

status: skipped
reason: "Bounded fix the bead fully specifies, run autonomously under the bounded standing grant (2026-11-25): check_criterion_ledger.py reads its cutoff from the criterion-ledger entry of decisions/adoption.yaml (decided in PR #276, bead coding-harness-wpv) instead of the hard-coded CUTOFF; the PR states that moving from 2026-10-11 to 2026-10-29 widens the exemption to archived plans of 10-11..10-28 without a ledger. No product or architectural choice is open."
