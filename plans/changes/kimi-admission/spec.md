---
title: "Spec — kimi-admission"
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
tags: [spec, model-terms, opencode-go]
class: bounded
appetite: 1
adr_files: [docs/adr/0007-stage-2-reviews-by-codex-and-glm.md]
---

# Spec — kimi-admission

The OpenCode Go models read on 2026-10-30 are admitted to the review loop
through their data-terms readings, and the Kimi exclusion of 2026-09-30 is
lifted (bead coding-harness-bomd; decisions.md Q-1 to Q-5).

## What holds after the change

1. Every Go model the Go page listed on 2026-10-30 and the Pi catalog
   reaches carries a reading in `model-endpoints.yaml` with its retention,
   training, requests per 5 hours and a `valid_until` of 2026-11-29, whatever
   its retention period — 0 days and 30 days alike (Q-1).
2. Kimi stands under no exclusion; kimi-k3 and kimi-k2.7-code are admitted
   like any other Go model (Q-2). ADR 0007, decision 3, carries the dated
   amendment.
3. The Kimi models serve the review loop (phase 4b) only, ordered by their
   declared requests per 5 hours like every other member; the roles of
   ADR 0007 for explore, implement and repair stay as they are (Q-5).
4. mimo-v2.5, mimo-v2.5-pro and glm-5.2 stay declared, each marked with the
   date and status code of its failed probe (Q-3).
5. The seven models that could not be admitted stand as dated comments with
   their reason in `model-endpoints.yaml` (Q-4).

## Tests

- `tests/test_stage2.py::test_the_kimi_exclusion_is_lifted_and_its_models_carry_terms`
- `tests/test_stage2.py::test_the_real_declaration_excludes_no_declared_model`
