---
title: "Research — kimi-admission"
status: draft
implementation_status: partial
date: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-bomd
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, model-terms, opencode-go]
---

# kimi-admission — Research

What was measured on 2026-10-30, by the orchestrating session; no explore
run, because the change admits models and amends one ADR decision and adds
no mechanism.

- **The Go page (https://opencode.ai/docs/go), read 2026-10-30 13:54 UTC.**
  Its privacy and estimated-requests tables name nine models the declaration
  did not carry. Two of them, kimi-k3 (110 requests per 5 hours) and
  kimi-k2.7-code (1350), are reachable through the Pi catalog's
  chat-completions endpoint. Seven are not: grok-4.7 and gpt-5.6-luna answer
  only on the Responses endpoint, which Pi does not speak; gemini-4-argon
  answers on the Google endpoint, and the catalog has only its contributor
  variant; kimi-k3.1-pro, minimax-m3.1-flash, step-5-preview and beam-free
  are not in the catalog.
- **prepare-loop, 2026-10-30.** The static, tool-free reachability probes
  got 410 (deprecated) from mimo-v2.5 and mimo-v2.5-pro and 403 (access
  disabled) from glm-5.2.
- **ADR 0007, decision 3** (`docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`)
  still dropped Kimi on 2026-09-30, and `model-endpoints.yaml` carried Kimi
  under `ausgeschlossen`; the tests pinned that exclusion.
