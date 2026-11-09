---
title: "Decisions — night-stall-guard"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-ibde
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, night-run, permissions, claude-code]
---

# night-stall-guard — Decisions

Class: bounded (bead coding-harness-ibde).

## Q-1 · How the change prevents a night stall

asked: 2026-11-09
answer: "Ja" — the change ships, in this order: (1) a night settings profile in which every rule that would ask the maintainer denies instead, so a call returns at once and the orchestrator takes another path; (2) a precise merge brake that asks (by day) or denies (at night) only for real merges — `gh pr merge`, the REST merge endpoint and the GraphQL mutations that merge or enqueue — while a read query that only names merge fields passes; (3) the phone alert for an open permission prompt and for a missing heartbeat comes after (1) and (2), as the second safeguard. The push service for (3) is not chosen yet and is asked when (3) is built.
answered_by: maintainer
status: answered
context: |
  Topic: on 2026-11-08 at 22:26 UTC a read-only `gh api graphql` status query that named the fields mergedAt and isInMergeQueue matched the ask rule `Bash(gh api *merge*)` in .claude/settings.json; the orchestrating session waited for approval until 06:04 UTC and every heartbeat, watchdog wake-up and task notification queued behind it (session transcript), so finished lanes idled about 5.5 hours.
  Intention: no single question may hold the night; the maintainer asked first how to stop the blocking at all ("Wie kann ich es erstmal verhindern dass überhaupt alle Prozesse blockiert werden").
  Today: ask rules wait without limit; nothing alerts the maintainer; the watchdog only wakes the chat, which cannot act while a prompt is open.
  Repository change: a night profile under tools/claude-code/ (installed by tools/claude-code/install.sh), narrowed merge rules in .claude/settings.json with tests of the rule set; the alert later.
  Architecture change: none; moving each heartbeat into its own headless, time-limited call (launchd) belongs to the harness-neutral night-run work, not to this change.
