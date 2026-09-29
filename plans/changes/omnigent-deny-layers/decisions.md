---
title: "Decisions — omnigent-deny-layers"
status: accepted
implementation_status: none
date: 2026-09-29
last_reviewed: 2026-09-29
supersedes: null
superseded_by: null
bead: coding-harness-rex
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# omnigent-deny-layers — Decisions

Phase 1a (interview) was skipped: the maintainer gave the intent and approved
the direction in the session of 2026-09-29; what remains open is mechanics.

What the maintainer decided on 2026-09-29:

1. Omnigent's own file and shell tools bypass Claude Code's hooks and
   permission rules, and no Omnigent policy is configured on the machine. The
   maintainer asked how Omnigent's own deny rules work and whether they span
   harnesses; the answer was "partly: one policy set, enforced through a
   per-harness hook for Claude Code, Codex, Devin, Hermes, Pi and the Cursor
   SDK, not for Goose, Cursor, Qwen, Kiro or Antigravity; stored per machine,
   not per repository".
2. Answered "yes" to: package 1a gets **both layers** — the rule in the
   repository first (`permissions.deny` in `.claude/settings.json` against
   Omnigent's writing tools), and an Omnigent default policy declared as a
   file in this repository as the second layer.
3. "Implement as the workflow intends" — the seven phases, with the model
   routing of `docs/WORKFLOW.md` §3.

Standing constraint: ADR 0006 — nothing may depend on an Omnigent policy
alone. Layer 1 must hold on its own.
