---
title: "Decisions — failed-check-spans"
status: draft
implementation_status: none
date: 2026-10-22
last_reviewed: 2026-10-22
updated: 2026-10-22
supersedes: null
superseded_by: null
bead: coding-harness-8hr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# failed-check-spans — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · How credential and secret protection combine in failed-check diagnostics

context: |
  Topic: failed-check diagnostics the runner writes into findings.md and the
  retry prompt (rows F-4 and F-5 of pull request #215).
  Intention: the phase-6 re-check of #215 found two ways in which replacing
  the routing credential first destroys a match another pass needs.
  Today: the format line is credential-scrubbed before secret spans are
  looked for, and the non-secret rules read credential-scrubbed text.
  Repository change: every pass reads the original diagnostic; all spans are
  collected first, then replaced once.
  Architecture change: none.
asked: 2026-10-22, conversation 2026-10-22 (joint window, night-run plan item 1)
answer: "collect every secret span on the original text, replace once"
answered_by: maintainer
status: answered

In the context of failed-check diagnostics that hold both the routing
credential and secret- or non-secret-rule matches, facing passes that
replace text before other passes have read it, we decided that every pass
reads the unscrubbed original, all spans are collected first and one
replacement pass applies credential and secret markers, to achieve that no
pass destroys a match another pass needs, accepting that a diagnostic may be
refused where it was silently redacted before. — 2026-10-22

## Details the orchestrating session decides

These are `[DETAIL]` items; none changes a decision of record.

1. **The format line goes through `protect_diagnostics`.** `format_step` and
   `_not_run` return their line through `protect_diagnostics` instead of
   `scrub`. Reason: it is the one function that collects all spans on the
   original; a later second pass over the protected line finds only markers.
2. **A non-secret match wholly inside the credential still does not refuse.**
   Non-secret rules run on the original text; a match that lies wholly inside
   a credential span is skipped (as secret matches already are), every other
   match refuses. Reason: keeps today's measured behaviour for the credential
   itself while F-5's extending match blocks.
