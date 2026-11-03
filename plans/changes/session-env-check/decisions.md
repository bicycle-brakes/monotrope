---
title: "Decisions — session-env-check"
category: decisions
status: draft
implementation_status: none
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-cjf9
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, environment, hooks]
---

# session-env-check — Decisions

Class: bounded (one counted answer owed). The bead's description (read
2026-11-03 with `tools/bd show`) fixes what is checked: a missing or broken
`.venv` (ruff and pytest importable) and a missing pinned Pi, each reported
with the exact fix `make venv && bash tools/pi/install.sh`. It was split from
the stop-hook interview (bead coding-harness-788, spec-review row S-4) on
2026-11-03; the stop hook blocks once with the same fix when its probe cannot
start. This closes the explore's open question on scope.

## Q-1 · Where the check lives

asked: 2026-11-03
answer: "Skript im Repo + Hook" — a repository script (working name `scripts/check_checkout.py`) checks `.venv` with ruff and pytest and the pinned Pi and names the fix; it is wired as a SessionStart hook in `.claude/settings.json` and can be run by hand and by other harnesses.
answered_by: maintainer
status: answered
context: |
  Topic: where the checkout-readiness check lives.
  Intention: it decides who gets it; on 2026-10-19 a broken .venv let verify_all.sh fall back to another repository's virtualenv, and on 2026-11-03 a fresh worktree lacked the pinned Pi.
  Today: at session start the repository runs only `bd prime`; no readiness check exists (the explore read the four user-level hooks and listed scripts/).
  Repository change: Options: a repository script plus a SessionStart entry in .claude/settings.json, callable by hand and by other harnesses; only the user-level handover.sh under ~/.claude.
  Architecture change: none.

In the context of checkouts that start without a working environment, facing a user-level hook or a repository script, we decided on a repository script wired as a SessionStart hook and callable by hand, to achieve the same check in every checkout and harness, accepting one more entry in the held settings file. — 2026-11-03
