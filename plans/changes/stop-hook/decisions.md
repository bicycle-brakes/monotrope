---
title: "Decisions — stop-hook"
category: decisions
status: draft
implementation_status: none
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-788
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, hooks, verification]
---

# stop-hook — Decisions

Class: bounded (one counted answer owed; two stand). Q-1 is the maintainer's
answer of the 2026-10-28 decision interview, recorded on the bead's notes the
same day; Q-2 was asked on 2026-11-03 through the interview tool.

## Q-1 · Which check the hook runs and how long it may hold a turn

asked: 2026-10-28
answer: "quick probe" — only when Python is changed and uncommitted: ruff plus the tests of the changed files, at most 60 s; it blocks the turn on red.
answered_by: maintainer
status: answered
context: |
  Topic: the stop hook fires at the end of every turn; which check it runs and how long it may hold a turn.
  Intention: the doctrine names the hook (phase 5) and the file is missing; the workflow-promises change split this choice out to the maintainer.
  Today: no hook; the full make verify takes about eleven minutes (CI, 2026-10-27); the doctrine calls the hook a comfort layer that runs only when Python changed.
  Repository change: .claude/hooks/session-stop/check-tests-green.sh, a Stop entry in .claude/settings.json, tests, the WORKFLOW notice and README.
  Architecture change: none; the doctrine already plans it.

In the context of a hook that fires at every turn end, facing the full make verify or a quick probe, we decided on a quick probe — ruff and the changed files' tests, only when Python is changed and uncommitted, at most 60 s, blocking on red — to achieve a hook nobody switches off, accepting that CI stays the real gate. — 2026-10-28 (recorded on the bead the same day)

## Q-2 · When the 60 seconds run out

asked: 2026-11-03
answer: "Durchlassen mit Hinweis" — the hook stops the probe, lets the turn end, and warns that the check did not finish and nothing was confirmed green.
answered_by: maintainer
status: answered
context: |
  Topic: what the hook does when its probe exceeds 60 s.
  Intention: the one edge case the answer of 2026-10-28 leaves open.
  Today: no hook; the doctrine calls it a comfort layer, CI is the gate, and warns that a hook that gets in the way is switched off within a week.
  Repository change: the same files as Q-1. Options: let the turn end with a warning; count the timeout as red and block.
  Architecture change: none.

In the context of a comfort hook with a 60-second budget, facing a timeout that blocks or one that passes, we decided that a timeout lets the turn end with a warning that nothing was confirmed green, to achieve a hook that never holds a session without a red result, accepting that a slow probe proves nothing and CI decides. — 2026-11-03
