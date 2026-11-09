---
title: "Research — interview-fenced-examples"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-k2r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, gate, interview-minimums]
---

# interview-fenced-examples — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `f8a6b33`
(2026-10-25).

## The finding

`scripts/check_interview_minimums.py` `_parse_records` splits
`decisions.md` on `## ` without fence awareness, so a `## Q-n` or
`## SKIP · interview` block inside a code fence (an example) counts toward
a class minimum. The question-context gate skips fenced content. An
example could satisfy a minimum the interview never met (bead
coding-harness-k2r, found by the phase-6 review of `interview-context`,
2026-10-15). As of `7b7f9ad` no `decisions.md` held such a block; on
`f8a6b33` the gate still measures 23 changes green after the fix.

## What exists today

- `check_criterion_ledger.py` `_fenced` and `check_question_context.py`
  `_fenced` apply the same CommonMark fence rule; each script keeps its
  own copy, because the kit carries gate scripts one by one.

## Sources

- Bead coding-harness-k2r; `scripts/check_interview_minimums.py`,
  `scripts/check_question_context.py`, `scripts/check_criterion_ledger.py`.
