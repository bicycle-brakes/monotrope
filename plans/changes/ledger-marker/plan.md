---
title: "Plan — ledger-marker"
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
tags: [plan, stage-2, criterion-ledger]
---

# Plan — ledger-marker

```text
For you:     An attempt whose tests exist no longer fails because the plan still says "not yet written".
Done when:   clear_written and its runner call have tests that were red first, and make verify is green.
Appetite:    1 hour of phase 4; stop at the limit.
Not now:     Any other ledger form or gate finding.
Pre-mortem:  suppose it failed: most likely because a fenced example or a missing test lost its marker.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_check_criterion_ledger.py`, `tests/test_stage2.py`: the
   tests named in the ledger.
2. `scripts/check_criterion_ledger.py`: `clear_written(root, plan)`.
3. `scripts/stage2.py`: import it; call it in `verify_attempt` before
   `prepare_derived`.
4. This plan, `findings.md`, `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_check_criterion_ledger.py -k 'clear_written or clears_the_ledger_marker or clearing_the_ledger or ledger_is_cleared'
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_check_criterion_ledger.py::test_clear_written_removes_the_marker_of_an_existing_test_only — an existing test keeps its marker.
- 2: tests/test_check_criterion_ledger.py::test_clear_written_removes_the_marker_of_an_existing_test_only — a missing test or a fenced line loses its marker, or a second pass changes the plan.
- 2: tests/test_check_criterion_ledger.py::test_clear_written_leaves_a_fenced_example_inside_the_ledger_section — a fenced example under the ledger heading is rewritten.
- 3: tests/test_stage2.py::test_implement_clears_the_ledger_marker_of_a_test_the_attempt_wrote — the committed plan keeps the marker.
- 3: tests/test_stage2.py::test_the_ledger_is_cleared_before_the_documents_are_stamped — the plan is stamped before its marker is cleared.
- 4: tests/test_stage2.py::test_clearing_the_ledger_never_writes_through_an_aliased_plan — a symlinked plan's target outside the worktree changes.
- 4: tests/test_stage2.py::test_clearing_the_ledger_refuses_an_aliased_parent_or_a_hard_link — a symlinked change folder or a hard-linked plan carries the write outside.

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction. The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 11:56:29–12:01:18 UTC, 289 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
2026-10-25 20:07:04–20:17:45 UTC, 640 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
