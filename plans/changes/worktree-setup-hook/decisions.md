---
title: "Decisions — worktree-setup-hook"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-wg4z
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, worktree, git-hooks, environment]
---

# worktree-setup-hook — Decisions

## SKIP · interview

status: skipped
reason: The maintainer decided the direction in the conversation of 2026-11-25 (session 9200c6b1): the versioned post-checkout hook sets up every new worktree (venv and pinned Pi), with HARNESS_NO_LANE_SETUP=1 as the opt-out; answered 'ja'. The bead (coding-harness-wg4z) states the scope; no open human intent question remains.
