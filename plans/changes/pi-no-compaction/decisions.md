---
title: "Decisions — pi-no-compaction"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, runner, pi]
---

# pi-no-compaction — Decisions

Class: bounded (bead coding-harness-mwzv.2).

## SKIP · interview

status: skipped
reason: The bead (coding-harness-mwzv.2) fixes the whole change from a measurement (docs/research/2026-11-03-pi-context-overflow.md, PR #321): the runner adds {"compaction": {"enabled": false}} to the per-call Pi settings.json it already writes, a test pins the file, REVIEW_DIFF_MAX_LINES stays as the cost bound, the runner stays in text mode. The one open fact is a [DETAIL], not a choice: the measurement ran on Pi 1.2.0 and the pinned Pi is 1.5.0 (PR #335), so the draft names a re-check of the overflow behaviour on 1.5.0.
