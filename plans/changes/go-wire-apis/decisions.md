---
title: "Decisions — go-wire-apis"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-08
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

## Q-2 · Ship two of three wire APIs while Google is blocked

asked: 2026-11-07
answer: "Mit 2 von 3 liefern (Recommended)" — ship Anthropic Messages and OpenAI Responses; Google becomes a follow-up change that starts once OpenCode Go offers an admissible Google model (bead coding-harness-twdu)
answered_by: maintainer
status: answered
context: |
  Topic: the measurement of 2026-11-06 18:48 UTC succeeded for Messages (qwen3.8-flash, qwen3.7-plus, qwen3.8-max, minimax-m3) and Responses (grok-4.7); Google is blocked because the live catalog lists only gemini-4-argon-contributor, which trains on submitted data.
  Intention: Q-1 asked for all three APIs; that goal cannot be reached now.
  Today: five more models become usable once this change merges.
  Repository change: spec criteria 3-4 and the Definition of Done name the two measured APIs; Google points to the follow-up bead.
  Architecture change: two new wire APIs in the runner instead of three.

In the context of a Google endpoint without an admissible model, facing waiting for it or shipping what is measured, we decided to ship the two measured APIs and defer Google, to achieve five usable models now, accepting a second, smaller change for Google later. — 2026-11-07

## Q-3 · The research selector's measured-API argument becomes required

asked: 2026-11-08
answer: "Spec erweitern" — the spec's protected areas name the one signature change in scripts/stage2_swarm.py (select_research_catalog takes measured_wire_apis without a default) and its caller in scripts/research_capture.py as an allowed exception; the repair stays.
answered_by: maintainer
status: answered
context: |
  Topic: phase 6 found F6-1 (MAJOR): the loop repair of row L3-6 made measured_wire_apis a required argument of the research selector and updated its capture caller, although the spec protects the swarm code.
  Intention: the lane stood still on a scope question only the maintainer can answer.
  Today: main defaults the argument to openai-completions; the live caller passes the APIs anyway.
  Repository change: one exception paragraph in the spec's protected areas and one clause in the plan's boundaries.
  Architecture change: none; a caller can no longer silently fall back to one wire API.

In the context of a loop repair that touched protected swarm code, facing a choice between reverting it and widening the spec by one signature line, we decided to widen the spec, to achieve that no research selection silently falls back to one wire API, accepting a slightly larger change footprint. — 2026-11-08
