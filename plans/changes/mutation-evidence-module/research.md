---
title: "Research — mutation-evidence-module"
status: draft
implementation_status: partial
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-diic
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, ci, ratchet]
---

# mutation-evidence-module — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `ab3bd415`
(2026-10-26).

## The finding

The repair of PR #248 (rows R6-1..R6-3 of its phase 6) failed the runner's
red-first check: the analyzer under repair lives in `tests/test_ci.py`, the
same file as its new tests, so the tests always run against the repaired
copy and can never be shown red against the old one (bead
coding-harness-diic).

## What exists today

- `tests/test_ci.py` holds `MUTATIONS_NAMEN`, `_pruefling` and, inline in
  `test_every_gate_step_has_a_mutation_test`, the evidence check.
- `test_every_script_has_a_caller_or_a_declared_reason` requires every
  script under `scripts/` to have a CI caller or a reason in
  `ci_gates.OHNE_AUFRUFER`.
- `scripts/kit/probe.py` (the empty-repository probe) runs the travelling
  tests in a throwaway repository built from `scripts/kit/manifest.yaml`.

## Sources

- `tests/test_ci.py`, `scripts/ci_gates.py`, `scripts/kit/manifest.yaml`,
  `scripts/kit/probe.py` at `ab3bd415`.
