---
title: "Decisions — pi-work-route"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-363r.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, routing, pi, opencode-go, interview]
---

# pi-work-route — Decisions

Phase-1a interview with the maintainer, 2026-11-25 (session 9200c6b1), on the partial research of explore run 2 (run f171ca7b…; repository topics 1, 2 and 4 timed out, every other slot valid; the maintainer chose to go on with the partial research).

## Q-1 · Scope of the change

asked: 2026-11-25
answer: "All three parts: (1) fallback — when the normal implement/repair route fails, implement and repair run through Pi on OpenCode Go; (2) model choice — GLM 5.3 Flash or DeepSeek V4.1 Flash as a declared parameter of the one route (house rule 9), not a second verb; (3) GLM off Claude Code — GLM 5.3 / 5.3 Flash for explore, implement and loop start through Pi instead of Claude Code."
answered_by: maintainer
status: answered
context: |
  Topic: what this change delivers.
  Intention: implement and repair keep running when Claude Code or Z.ai is exhausted (both were on 2026-11-25).
  Today: GLM 5.3 Flash starts only through Claude Code on Z.ai; DeepSeek through Pi only interactively (session verb).
  Repository change: scripts/stage2.py routes, model-endpoints.yaml (opencode-go widened to work verbs), tests.
  Architecture change: the work verbs gain a Pi route on OpenCode Go (new ADR, Q-4).

In the context of work verbs that stop when Claude Code or Z.ai is exhausted, facing a narrow or a full scope, we decided to build all three parts (fallback, model choice, GLM off Claude Code), to achieve one Pi route for every work verb, accepting a larger architectural change. — 2026-11-25

## Q-2 · Fallback order for implement and repair

asked: 2026-11-25
answer: "Go first, then Codex, then Claude: the Pi route on OpenCode Go first, then Codex (bead coding-harness-363r.4 is taken up here), Sonnet through Claude last, so the scarce Claude budget is spared."
answered_by: maintainer
status: answered
context: |
  Topic: the order of routes when one is unavailable.
  Intention: no lane stops while any route has capacity; on 2026-11-25 Codex had capacity all day, Claude was exhausted twice.
  Today: implement falls back from GLM-through-Claude-Code to Sonnet only; no Codex implement route.
  Repository change: the route order in scripts/stage2.py and its documentation.
  Architecture change: Codex becomes an implement/repair route.

In the context of choosing the order of implement and repair routes, facing a scarce Claude budget and an available Codex, we decided Go first, then Codex, then Claude, to achieve lanes that keep running while any route has capacity, accepting a new Codex implement route. — 2026-11-25

## Q-3 · Default Go model

asked: 2026-11-25
answer: "DeepSeek V4.1 Flash is the default for implement and repair on Go, as originally wanted (2026-10-20); when its data terms lapse (valid_until in model-endpoints.yaml, today 2026-11-30, renewed monthly) the route falls back to GLM 5.3 Flash automatically."
answered_by: maintainer
status: answered
context: |
  Topic: which Go model the runner uses by default.
  Intention: the maintainer's preferred model, with no gap when its terms lapse.
  Today: DeepSeek's zero-retention agreement is valid through 2026-11-30 (OpenCode Go page, read 2026-11-25); GLM 5.3 Flash has no end date.
  Repository change: the default and its fallback in the route declaration.
  Architecture change: none beyond Q-4.

In the context of the default Go model for implement and repair, facing DeepSeek's monthly data terms and GLM's open-ended ones, we decided DeepSeek V4.1 Flash with an automatic fallback to GLM 5.3 Flash when its terms lapse, to achieve the preferred model without a gap, accepting a fallback that depends on valid_until. — 2026-11-25

## Q-4 · How the decision is recorded

asked: 2026-11-25
answer: "A new ADR 'Work verbs through Pi on OpenCode Go' records route, order Go → Codex → Claude, default model and write boundary; it explicitly supersedes the affected parts of ADR 0007, 0011 and 0015, which each get a pointer."
answered_by: maintainer
status: answered
context: |
  Topic: the decision record.
  Intention: one place that states the work-verb routing.
  Today: model routing is spread over ADR 0007, 0011 and 0015.
  Repository change: docs/adr/<next>-work-verbs-through-pi.md and three pointer lines.
  Architecture change: the routing decision moves into the new ADR.

In the context of recording the work-verb routing, facing three ADRs that each hold a part, we decided one new ADR that supersedes the affected parts with pointers, to achieve one place for the routing decision, accepting three pointer edits. — 2026-11-25

## Q-5 · Write boundary for a write-capable Pi run

asked: 2026-11-25
answer: "It must work on macOS, Linux and Windows. First our own write tools: Pi gets no shell and not its built-in write tools but our own read/edit/write tools, which refuse every path outside the lane worktree (symlinks resolved), in plain Python with tests, plus the existing runner checks. Containers (Docker or Podman) are considered later (bead coding-harness-363r.6). Herdr was checked first and offers no isolation of its own."
answered_by: maintainer
status: answered
context: |
  Topic: how a model that writes through Pi is confined.
  Intention: no write outside the lane worktree, on every platform the kit runs on.
  Today: Pi has no permission system; macOS sandbox-exec was rejected as macOS-only; Herdr is a multiplexer without isolation (web check 2026-11-25).
  Repository change: a small tool module for Pi with path checks, and its tests.
  Architecture change: the write boundary of foreign-model runs is ours, in code.

In the context of confining a write-capable Pi run on macOS, Linux and Windows, facing an OS sandbox that exists only on macOS and a multiplexer without isolation, we decided our own path-checked write tools first and containers later, to achieve the same boundary on every platform, accepting a tool module to build and test. — 2026-11-25
