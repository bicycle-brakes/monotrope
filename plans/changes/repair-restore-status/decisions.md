---
title: "Decisions — repair-restore-status"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-rcyf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# repair-restore-status — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).

## SKIP · interview

status: skipped
reason: a reproduced bug whose bead (coding-harness-rcyf) names the fix — on a refused or restored attempt the runner restores the status cells of the rows it took to their pre-attempt values — and the existing restore of findings.md on every other failure path does exactly that; the maintainer handed this session the whole workflow on 2026-10-25 (conversation).
