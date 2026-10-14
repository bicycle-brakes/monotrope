---
title: "Session handover — fourth night run, as of 2026-10-15"
category: handover
created: 2026-10-14
updated: 2026-10-14
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-14"
tags: [handover, session, night-run]
target_ref: origin/main
bead: coding-harness-yuw
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Morning handover — fourth night run, 2026-10-15

This page is written in two steps. Tonight it holds the queue the maintainer
agreed to on 2026-10-14 at about 19:55 ("passt, starte die nacht"); in the
morning the four sections of the night-run form replace the "filled in the
morning" lines (`docs/research/2026-10-12-night-run.md`, "Morning, 08:00").

## The queue (agreed 2026-10-14)

One orchestrating Claude Code session works it strictly in order, one model
call or sub-agent at a time. No merge, no decision that belongs to the
maintainer; every item ends at a pull request or at a written stop. Every
plan card below was shown to the maintainer unchanged before the start.

| # | Bead | Change | Branch | Ends at |
|---|---|---|---|---|
| 1 | coding-harness-yzk | Sol effort per verb (repair medium, draft high, review high), one central setting in `scripts/stage2.py`; appetite 1 hour | `feat/sol-effort-r2` (draft PR #143) | implement, loop (4b), phase-6 review, repairs, decision PR |
| 2 | coding-harness-eao | Haiku 5.5 instead of Haiku 4.5 wherever a Haiku version is pinned; appetite 1 hour | `feat/haiku-5-5` | pull request |
| 3 | coding-harness-zs7 | Every question to the maintainer starts with a fixed context form, checked by a gate for answers recorded from adoption; appetite 4 hours | `docs/interview-context` | decision PR |
| 4 | coding-harness-icw | Phase 1 as a research swarm for feature and architectural changes, free models first on public research with one Opus-written topic sentence (Q-6), Opus 5.5 reconciles; appetite 12 hours | `explore/research-swarm` | decision PR; no live free-model call before the merge |
| 5 | coding-harness-s9r | Each writing attempt runs in its own container (Podman by default); appetite 24 hours, so it runs until the morning and stops there | `explore/isolated-attempts` | partial implementation, pushed, with a written stop |

Drafts only, already queued before the start, plan cards for the morning:

| Bead | Change | Branch |
|---|---|---|
| coding-harness-ni8 | The handover checks the architecture docs, the front page and the vault | `explore/handover-currency` |
| coding-harness-ylu | One central model and effort setting | `explore/central-models` |
| coding-harness-4fk | The review loop runs until clean, on a model ladder | `explore/loop-until-clean` |

### Rules for this night (maintainer, 2026-10-13 and 2026-10-14)

- **Codex still runs at effort max** for drafts, reviews and repairs until
  item 1 merges. When its five-hour limit is spent, the night moves to steps
  that need no Codex and comes back after the reset.
- **Two changes claim ADR 0018** (research swarm, isolated attempts).
  Whichever merges second renumbers; the gate that refuses a double claim
  sees them in separate branches tonight.
- **Most changes touch `scripts/stage2.py`.** Each branch starts from main;
  conflicts surface at merge and are resolved then, not tonight.
- **Stops.** Red `make verify` after two repairs, a leak-check BLOCK, or a
  question only the maintainer can answer: written down here, the next item
  starts.
- **No tracker write while a draft check or `make verify` runs** in any
  worktree: the render byte-equality test reads the live tracker.

### Lessons of 2026-10-14 the night applies

- The macOS keychain hung every HTTPS git call (tracker push included) from
  about 18:55 to 19:15 and recovered by itself. A hanging push is waited for
  once, not retried in a loop.
- Each worktree needs `make venv` once; the runner is called with
  `.venv/bin/python3`.
- Never two drafts at once in one worktree.
- Notes on a bead are appended (`--append-notes`), never replaced.
- macOS has no `timeout` command.

## 1. The three priorities for today

Filled in the morning.

## 2. Done — waiting for your merge

Filled in the morning.

## 3. Stuck: where, and why

Filled in the morning.

## 4. Resume

Filled in the morning.
