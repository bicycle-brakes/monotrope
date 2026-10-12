---
title: "Decisions — attempt-diagnostics"
status: draft
implementation_status: partial
date: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-cit
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage-2, runner]
---

# Decisions — attempt-diagnostics

Interview for a `bounded` change (at least one counted record).

## Q-1 · What a failed implement attempt leaves behind

asked: 2026-10-11, the directing conversation
answer: option 1 — both: each failed attempt records its post-run
  diagnostics and a short list of the files it changed (lines changed per
  file) in `findings.md`, below that attempt's audit line
answered_by: maintainer
status: answered

In the context of an implement run whose two failed GLM attempts left no
trace of why they failed or what they wrote (change criterion-test-ledger,
2026-10-11), facing recording the diagnostics alone, we decided to record
the diagnostics and a per-attempt file list, to achieve that the maintainer
can tell why a model failed and which model wrote what before the single
checkpoint commit, accepting a longer `findings.md` per failed run. —
2026-10-11
