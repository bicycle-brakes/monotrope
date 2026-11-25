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

## Q-1 · Ambiguity S-1 (foreground or background setup)

asked: 2026-11-25
answer: "Foreground: git worktree add returns only after setup and its check; failures reach the caller at once."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-1 of worktree-setup-hook.
  Intention: no agent starts in a half-prepared worktree.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/worktree-setup-hook/spec.md in the final draft.
  Architecture change: none.

In the context of setting up new worktrees, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting about a minute longer per new worktree. — 2026-11-25

## Details decided by the orchestrator (spec-review round 2)

[DETAIL] S-7 (standing grant for bounded changes, maintainer 2026-11-25): every failed check prints its own `LANE SETUP FAILED:` line naming the step and the log path; a separate summary line ends the output: `lane setup: ok` or `lane setup: failed (N checks)`; the first line is `lane setup: start`.

[DETAIL] S-8: `HARNESS_LANE_SETUP_TIMEOUT` is a positive whole number of seconds; unset or empty means 600; `0`, a negative or a non-numeric value falls back to 600 and prints one warning line.

[DETAIL] S-9: a test compares the text between the `BEGIN` and `END BEADS INTEGRATION` markers of `.beads/hooks/post-checkout` with `origin/main` and fails on any change.
