---
title: "Spec — mutation-evidence-module"
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
tags: [spec, ci, ratchet]
class: bounded
appetite: 1
adr_files: []
---

# Spec — mutation-evidence-module

The mutation-evidence analyzer moves unchanged from `tests/test_ci.py` into
`scripts/mutation_evidence.py` (bead coding-harness-diic). Research:
`research.md`. Decisions: `decisions.md`, Q-1.

## Acceptance criteria

1. The ratchet reports the same gates with and without evidence as before.
   *Refuted by:* `test_every_gate_step_has_a_mutation_test` or
   `test_the_mutation_ratchet_only_turns_one_way` failing.
2. The new module has a declared reason in `ci_gates.OHNE_AUFRUFER`.
   *Refuted by:* `test_every_script_has_a_caller_or_a_declared_reason` naming it.
3. `tests/test_ci.py` still runs in a repository that received the kit.
   *Refuted by:* the empty-repository probe naming `tests.test_ci` as red.

## Out of scope

- Any change to what counts as evidence (that is PR #248).
