---
title: "Research — codex-takeover"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-nsm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, codex, cost]
---

# Which workflow tasks Codex can take over — Research

Phase 1 for bead coding-harness-nsm, read against `origin/main` on
2026-10-12. The maintainer asked (2026-10-12) which tasks of the seven-phase
workflow, and of the orchestration around it, can move from Claude to Codex
to save Claude tokens. Today Codex runs only spec-review (phase 2a) and
review (phase 6) through `scripts/stage2.py`. The maintainer wanted Codex to
research this; the runner has no Codex research verb (ADR 0007), so GLM
explores through the explore verb and the answer is checked by the
orchestrating session. A related feature bead covers a repair verb for GLM
(coding-harness-g2f).

## Questions for the exploration

1. Which tasks does Claude do today, per phase and around the phases, as the
   repository records them (`docs/WORKFLOW.md`, `prompts/`, `AGENTS.md`,
   `model-endpoints.yaml`, `scripts/stage2.py`): spec and plan writing,
   orchestration, repairs of review findings, pull-request review, tracker
   hygiene, handover drafts, commit and PR text.
2. For each: could Codex do it under the repository's rules (ADR 0007 leak
   check and runner-only start, ADR 0008 maintainer decisions, ADR 0011
   review loop, house rules in `AGENTS.md`)? What would the runner need (a
   new verb, a write scope, a session), and what must stay with Claude or the
   maintainer (interviews, ADR answers, merges, tracker writes)?
3. What does the repository say about Codex's limits and cost today (the
   `openai-codex` entry in `model-endpoints.yaml`, data residency, plan
   limits, measured runs in findings files and `scripts/stage2_runs.py`)?
4. Which candidates give the largest saving for the smallest rule change,
   ranked, with the files each would touch.

This file stops at the findings; a decision on any candidate is the
maintainer's.
