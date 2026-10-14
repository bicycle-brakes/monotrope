---
title: "Decisions — haiku-5-5"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-eao
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, models, haiku]
---

# Haiku 5.5 instead of Haiku 4.5 — Decisions

Phase 1a for bead coding-harness-eao. The one question was answered by the
maintainer in the conversation on 2026-10-14 before this file was written.

## Q-1 · Which Haiku the workflow uses

asked: 2026-10-14
answer: always Haiku 5.5 (`claude-haiku-5-5`) instead of Haiku 4.5, wherever the workflow names Haiku — the runner's stage-1 route, the endpoint declaration, the workflow tables, the prompts and AGENTS.md; dated records stay as they are.
answered_by: maintainer
status: answered

The maintainer's words, 2026-10-14: "nehme immer haiku 5.5. statt 4.5",
said when the session explained that `--stage2-off` explores with Haiku 4.5.

In the context of Haiku 4.5 named as the stage-1 model for explore and commit,
facing the choice between keeping 4.5 and moving to 5.5, we decided on Haiku
5.5 to achieve the newer model wherever Haiku runs, accepting one more
model-name change across the doctrine before bead coding-harness-ylu makes
such changes central. — 2026-10-14
