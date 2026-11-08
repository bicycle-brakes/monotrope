---
title: "Decisions — night-machine-facts"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-yql7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, night-run, machine-facts]
---

# night-machine-facts — Decisions

Class: bounded (bead coding-harness-yql7).

## SKIP · interview

status: skipped
reason: The bead (coding-harness-yql7) states what to build and why, from the measured night of 2026-11-01/02: one read-only command that prints a dated machine-facts block (free disk, swap, worktree count, running jobs) at night-run start, shown before lanes start. It adds no gate and no new guarantee beyond that block; the remaining choices are [DETAIL] items the draft decides with its reasons.
