---
title: "Decisions — definitive-refusal"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-2ym2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, review-loop]
---

# definitive-refusal — Decisions

Class: bounded (bead coding-harness-2ym2).

## Q-1 · Retire the stage, or stop with an instruction

asked: 2026-11-06
answer: "Selbst ausmustern (Recommended)" — on HTTP 403 (access disabled) or 410 (deprecated) for a paid rung, the review-loop round retires that stage itself, records the reason and the provider's answer in the audit, and continues with the next stage, as it already replaces a failed Flash member; a transient error (429, 5xx, timeout) never retires a stage.
answered_by: maintainer
status: answered
context: |
  Topic: Go answers some paid models definitively (403 access disabled, 410 deprecated); on 2026-11-05 a loop (glm-5.2) stood until the maintainer retired the stage by hand (release-loop --stage-failed).
  Intention: the lane is explored; it hits every loop prepared before a deprecation and halts night runs.
  Today: a failed Flash member is replaced automatically, a paid stage is not.
  Repository change: a runner change in review-loop, with tests.
  Architecture change: none; transient errors still never retire a stage.

In the context of loops prepared before a model's deprecation, facing night runs that halt on a definitive refusal, we decided that the round retires such a paid stage itself and records why, to achieve loops that keep running with the retirement visible in the morning, accepting that the maintainer no longer confirms each retirement. — 2026-11-06
