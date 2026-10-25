---
title: "Findings — ledger-marker"
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
tags: [findings, stage-2]
---

# Findings — ledger-marker

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: both
new tests failed before the edit (no `clear_written`; the committed plan
kept the marker).

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- `clear_written` reads with the gate's own `read`, `ledger_sections` and
  `parse_entry`, so trailing whitespace, a byte-order mark and fences are
  handled as the gate handles them; it rewrites only the matched lines.
- The runner imports its own copy of the module, like
  `check_frontmatter_current`, never the attempt's.
- `repair` goes through `verify_attempt` too, so it clears markers as well.

## Independent runner review, 2026-10-25

An Opus sub-agent of the orchestrating session reviewed the runner with all
open pull requests merged (read-only, in a separate context). Its row for
this change:

| ID | Severity | Finding | Status |
|---|---|---|---|
| R-1 | MAJOR | `verify_attempt` calls `clear_written` before any alias check, so an attempt that turns `plan.md` into a symlink to another worktree's plan, and writes the test that plan names, gets the runner to rewrite a file outside the worktree (reproduced). | fixed — tests/test_stage2.py::test_clearing_the_ledger_never_writes_through_an_aliased_plan |

The fix refuses a symlinked, alias-resolving or hard-linked plan before
`clear_written`, as `prepare_derived` refuses such documents.

## Pre-review by an Opus 5.5 subagent, 2026-10-25

At the maintainer's request, a read-only Opus 5.5 subagent reviewed this
change before the phase-6 Codex review, which this container cannot reach.
Phase 6 is still owed. It found no blocker and four minor rows, all fixed
by the orchestrating session.

- **P239-1 (MINOR), fixed.** `clear_written` rewrote a fenced example that
  stands under the ledger heading: `ledger_sections` stops only at a heading
  inside a fence and keeps the fenced lines in the section. Criterion 2 says
  a fenced entry is never changed. Lines in a fence are now skipped. Test:
  `tests/test_check_criterion_ledger.py::test_clear_written_leaves_a_fenced_example_inside_the_ledger_section`,
  red before the fix.
- **P239-2 (MINOR), fixed.** Nothing pinned that the marker is cleared
  before `prepare_derived` stamps `updated:`. Test:
  `tests/test_stage2.py::test_the_ledger_is_cleared_before_the_documents_are_stamped`;
  with the call moved after `prepare_derived`, it fails.
- **P239-3 (MINOR), fixed.** The alias guard's parent-folder and hard-link
  branches had no test. Test:
  `tests/test_stage2.py::test_clearing_the_ledger_refuses_an_aliased_parent_or_a_hard_link`;
  removing either branch makes its case fail.
- **P239-4 (NIT), fixed.** The alias refusal is now criterion 4 of the spec
  with its ledger entries; the verification filter names every new test;
  the `verify_attempt` docstring names the ledger step. `repair` reaches the
  same code through `run_attempts`; only `implement` is tested end to end.

## Review loop skipped, 2026-10-25

The review loop (phase 4b) did not run on this change. The maintainer
answered on 2026-10-25 (night-run plan, `docs/research/2026-10-25-night-run-plan.md`,
answer 1) that the small cloud-session fixes get phase 6 only tonight,
because each had the Opus 5.5 pre-review recorded above. Phase 6 follows in
a fresh Codex session.

Stage-2 call, 2026-10-25: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 552 files, 2092 commits, 12 rules.

## Phase 6 — Codex, 2026-10-25

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | Phase 6 | scripts/stage2.py:3963–3971 | Marker clearing runs before formatting. If an attempt writes `def test_new ():` with a matching ledger marker, `clear_written` leaves it untouched; Ruff then formats it to `def test_new():`, so the criterion-ledger gate rejects the now-stale marker during `make verify`. Reproduced with the worktree’s Ruff. Clear markers against the formatted tests before stamping the plan and running verification. [Acceptance criterion 3] | Codex | taken — test: an attempt that writes `def test_new ():` with a matching ledger marker passes the criterion-ledger gate after Ruff formats it to `def test_new():` (orchestrator, 2026-10-25) | — |

Phase 6 verdict: codex 01a174aa-2cf8-7ad1-90e1-01b2b8008e7a, 2026-10-25
Reviewer session: codex 01a174aa-2cf8-7ad1-90e1-01b2b8008e7a — a fresh session reviewed: no phase-2a session was recorded

Loop rows: none — the loop did not run for this change.
