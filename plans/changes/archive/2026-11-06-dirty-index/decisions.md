---
title: "Decisions — dirty-index"
status: accepted
implementation_status: done
date: 2026-10-25
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-0c8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# dirty-index — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).

## SKIP · interview

status: skipped
reason: a reproduced bug with one named fix and its test; the bead (coding-harness-0c8) states the direction — the pre-check also compares the index with HEAD and refuses, a test stages a change, reverts the file and expects a refusal — and the maintainer handed this session the whole workflow for it on 2026-10-25 (conversation), including spec, plan and implementation.
