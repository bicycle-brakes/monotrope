---
title: "Research — ledger-marker"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-7g6h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, criterion-ledger]
---

# ledger-marker — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `f8a6b33`
(2026-10-25).

## The finding

On 2026-10-23, implement attempt 3 of `restore-symlink-parent`
(coding-harness-10w, Sonnet 5.5) failed only the criterion-ledger gate:
its tests existed, while `plan.md` still said `not yet written`. With no
attempt left, the orchestrator removed the marker by hand (`2adc114`)
(bead coding-harness-7g6h).

## What exists today

- `scripts/check_criterion_ledger.py` reads the ledger section of each
  plan. A `not yet written` entry whose named test file holds the named
  function is a finding: "remove `not yet written` from the entry".
  Helpers: `ledger_sections` (fence-aware), `parse_entry`, `read`,
  `_defined`.
- `scripts/stage2.py` `verify_attempt` already renders `plans/INDEX.md`
  and stamps `updated:` dates (`prepare_derived`) before `make verify`:
  derivable state is the runner's, not the attempt's.

## Sources

- Bead coding-harness-7g6h, with the maintainer's choice of route
  (2026-10-23, conversation).
- `scripts/check_criterion_ledger.py`, `scripts/stage2.py` at `f8a6b33`.
