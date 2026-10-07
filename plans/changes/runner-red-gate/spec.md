---
title: "Spec — runner-red-gate"
status: draft
implementation_status: partial
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-zci
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, runner]
class: bounded
appetite: 2
---

# Spec — runner-red-gate

An implement repair attempt sees the gate that blocked, not the end of the
log. Inputs: [`research.md`](research.md).

## Acceptance criteria

1. When `make verify` fails and its output frames one or more gates as
   `RED (block)`, the diagnostics handed to the next attempt hold each such
   gate's section — from its `── [<gate>] $` line to its `RED (block)`
   line — in run order, and no report-only section.
   *Refuted by:* a planted pytest failure followed by 500 report-only lines
   whose failing test name does not reach the next prompt.
2. Each red section is bounded to its last 60 lines and the whole to 200
   lines; a cut section says how many lines were left out.
   *Refuted by:* a 1,000-line red section passed through whole, or a cut
   without a marker.
3. When the output carries no `RED (block)` frame, the diagnostics keep
   today's form: the last 80 lines.
   *Refuted by:* a failure of make itself producing empty diagnostics.
4. The GLM key is scrubbed from the diagnostics as today.
   *Refuted by:* the key reaching the prompt from a red section.

## Not in this change

Regenerating derived files (coding-harness-mfv); storing the diagnostics;
the report-only gates themselves.
