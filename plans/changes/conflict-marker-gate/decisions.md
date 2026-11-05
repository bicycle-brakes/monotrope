---
title: "Decisions — conflict-marker-gate"
category: decisions
status: draft
implementation_status: none
date: 2026-11-05
created: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-i76l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, gate, merge]
---

# conflict-marker-gate — Decisions

Class: bounded (bead coding-harness-i76l).

## SKIP · interview

status: skipped
reason: The maintainer answered "Ja" on 2026-11-05 to this item as the orchestrator proposed it: a blocking gate that fails on merge-conflict markers in tracked text files (`git diff --check` and a scan for lines that start with `<<<<<<<`, `=======` or `>>>>>>>`, fixtures excepted by name), and a small helper for merging main into a change branch that stops with the conflicted paths instead of continuing. Trigger the same day: a merge of origin/main into spike/verify-duration conflicted on docs/WORKFLOW.md and the next command committed and pushed the markers (31d35400). The scope is settled; any further choice (for example which paths count as fixtures) is a [DETAIL] the draft decides with its reason.
