---
title: "Decisions — go-wire-apis"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-36za
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, opencode-go, wire-api]
---

# go-wire-apis — Decisions

Class: bounded (bead coding-harness-36za).

## Q-1 · Measure each wire API, or go through Go's translation

asked: 2026-11-06
answer: "Jede Schnittstelle messen (Recommended)" — one measurement each for Anthropic Messages, OpenAI Responses and Google; the runner then records each wire API in the address record (ADR 0024) and calls the models directly; the Pi contract test widens to the measured APIs.
answered_by: maintainer
status: answered
context: |
  Topic: nine admitted Go models are skipped for "wire API not measured" (among them Qwen, MiniMax M3, GPT 6 Luna, Grok 4.7, Claude Haiku 5.5); they speak Anthropic Messages, OpenAI Responses or Google, not the Chat Completions format the runner knows.
  Intention: the maintainer said "mach das" on 2026-11-05; the lane is explored, only the route is open.
  Today: the runner and the Pi contract test know Chat Completions only.
  Repository change: the address record (ADR 0024) and the contract test widen.
  Architecture change: option A adds wire APIs; option B keeps one and lets Go translate.

In the context of nine admitted models skipped only for an unmeasured wire API, facing a choice between direct calls and Go's own translation, we decided to measure and map each wire API, to achieve calls in the provider's own format with failures that can be attributed, accepting three measurements and more runner code. — 2026-11-06
