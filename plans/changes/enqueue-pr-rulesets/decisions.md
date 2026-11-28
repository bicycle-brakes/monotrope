---
title: "Decisions — enqueue-pr-rulesets"
category: decisions
status: draft
implementation_status: none
date: 2026-11-27
created: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-3wtk
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-27", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, merge-queue, enqueue]
---

# Decisions — enqueue-pr-rulesets

Phase-1a record for `enqueue-pr-rulesets` (bead `coding-harness-3wtk`).

## SKIP · interview

status: skipped
reason: "Bounded bug fix found on PR #477 (2026-11-27) and run autonomously under the maintainer's bounded standing grant (2026-11-25): no product or architectural choice is open. scripts/enqueue_pr.py must (1) treat the HTTP 404 'Branch not protected' answer of the classic protection endpoint as no classic protection when the branch is protected by a ruleset, and (2) accept exactly the runner's own 'Loop state: ' line (scripts/stage2.py STATE_KEY) inside a released loop block; every other unreadable answer and every other unknown line keeps refusing (fail closed, plans/changes/enqueue-pr/spec.md). The pull request changes enqueue_pr.py itself, so the maintainer merges it (bootstrap exception)."
