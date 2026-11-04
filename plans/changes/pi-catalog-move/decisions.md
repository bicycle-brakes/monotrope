---
title: "Decisions — pi-catalog-move"
category: decisions
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-vku6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, pi, model-catalog]
---

# pi-catalog-move — Decisions

Class: bounded (bead coding-harness-vku6). The change moves the pinned Pi so that its shipped opencode-go catalog carries the Go models published on 2026-11-04; the admission of those models follows in a decision pull request of its own. The phase-1 explore could not read the bead and named three readings; the bead's description names this one.

## Q-1 · Which Pi version

asked: 2026-11-04
answer: "A: Pi 1.5.0 jetzt (Recommended)" — pin @earendil-works/pi-coding-agent 1.5.0.
answered_by: maintainer
status: answered
context: |
  Topic: the pinned Pi (1.2.0) lacks kimi-k3.1-pro, minimax-m3.1-flash and step-5-preview in its opencode-go catalog, so tests/test_pi_contract.py refuses their admission.
  Intention: the maintainer wants the new Go models used (2026-11-04).
  Today: read from the npm packages of pi-ai on 2026-11-04 — 1.4.0 (2026-10-21) carries step-5-preview only; 1.5.0 (2026-11-02) carries all three on openai-completions at https://opencode.ai/inference/go/openai/v1, and Qwen 3.8 Flash/Max, 3.7 Plus and MiniMax M3 on anthropic-messages at https://opencode.ai/inference/go/anthropic.
  Repository change: tools/pi/package.json and its lock move to 1.5.0; the contract suite passes first.
  Architecture change: none; a version move.

In the context of a pinned Pi whose Go catalog predates the models published on 2026-11-04, facing a choice between a two-day-old version with all three and a two-week-old one with one, we decided to pin Pi 1.5.0, to achieve all three models and the Messages address for the follow-up, accepting a young version guarded by the contract suite, with 1.4.0 as the fallback if it fails. — 2026-11-04
