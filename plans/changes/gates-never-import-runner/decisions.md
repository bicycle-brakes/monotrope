---
title: "Decisions — gates-never-import-runner"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7ayv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, gates, ratchet]
---

# gates-never-import-runner — Decisions

Class: bounded (bead coding-harness-7ayv).

## The bead (read from the tracker by the orchestrator, 2026-11-21)

> Rule: no file under scripts/check_*.py imports stage2. Why: a gate is read-only. The runner writes the worktree, calls foreign models, takes the verify admission and reads credentials; a gate that imported it would pull all of that into a check that must not write, and would make the check's verdict depend on machine state. Measured 2026-11-18 at 24632499 and on the fetched origin/main (11:02 UTC): 0 violations. The property holds today; the test locks it in — a ratchet, like RB-G4's mutation ratchet. Shape: tests/test_gate_imports.py — ast-parse every scripts/check_*.py, collect Import and ImportFrom, refuse stage2. A negative control builds a temporary module that imports stage2 and asserts the same checker refuses it, so the checker cannot be vacuous. No new entry in decisions/gates.yaml: the existing pytest gate carries it. Acceptance: the test exists and passes; it goes red when a check_*.py gains 'import stage2'; the negative control proves the checker bites.

## SKIP · interview

status: skipped
reason: The bead fixes the rule, the shape, the file, the negative control and the acceptance; the maintainer asked for no question windows until the block on 2026-11-23 10:00. The explore's open points are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **The forbidden set:** the module `stage2` in every spelling an import can take (`import stage2`, `import scripts.stage2`, `from stage2 import …`, `from scripts import stage2`, `from scripts.stage2 import …`, `importlib.import_module("stage2")` with a literal). The `stage2_*` family is not forbidden by this change. Reason: the bead names stage2; the family is a separate question.
- **The scanned set: `scripts/check_*.py` only,** as the bead says. `scripts/research_census.py` imports stage2 today and is not a `check_*.py`; it is named in the spec as a known neighbour outside the rule, not changed here. Reason: no scope beyond the bead.
- **Tests stay outside the rule:** `tests/` import the runner to test it. Reason: the bead's wording.
- **No Regelwerk row and no valve;** the pytest gate carries the test, as the bead says. Reason: the bead.
