---
title: "Research — criterion-test-ledger"
status: draft
implementation_status: none
date: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-11
supersedes: null
superseded_by: null
bead: coding-harness-909
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, gates, tests, acceptance-criteria]
---

# Criterion test ledger — Research

Read on 2026-10-11 against `origin/main` at `0c71403`. This change answers the
bug that deleting 29 of the 30 tests in `tests/test_research_currency.py` left
`make verify` green (measured on `main` at `d5813ec`, 2026-10-06; bead
coding-harness-909). The options and their consequences were already
researched; this file collects the facts the spec needs and does not repeat
that comparison
(`docs/research/2026-10-08-holding-criterion-tests.md`, merged in PR #96).
Written by the orchestrating Claude Code session on that earlier research; no
runner explore (`stage2.py explore`) was started for this change.

## What exists today

- `pytest` runs `tests/` as a whole; a deleted test simply stops running and
  nothing counts it (`docs/research/2026-10-08-holding-criterion-tests.md`,
  "What holds tests today").
- The ratchets in `tests/test_ci.py` hold the shape of the suite, not its
  content: one test file per script and one named mutation test per gate
  (same note, same section).
- `scripts/ramp_valves.py` has `_enforcer_exists(ref)`: it takes
  `<file>` or `<file>::<function>` and answers whether the file exists or
  whether the file contains a line starting `def <function>(`. It searches
  text on purpose and never imports, because the script runs in every run
  (its docstring). It is used only for the valves' enforcers.
- What ties an acceptance criterion to its tests is prose. Each spec
  criterion ends with a *Refuted by:* line; the plans name their checks in no
  fixed form.
- After the archive move of PR #116 (`0c71403`, 2026-10-10), four change
  folders are live under `plans/changes/`: `harness-decide-adr`,
  `hermes-runner`, `research-currency` and `stage2-session`. Occurrences of
  `test_` in their `plan.md` on 2026-10-11: 73, 46, 90 and 6. The other
  changes sit under `plans/changes/archive/<date>-<name>/`.
- The phase-3 prompt (`prompts/03-plan.md`) and the phase-4 prompt
  (`prompts/04-implement.md`) and the phase-6 reviewer are today the only
  holders of a criterion's tests.

## What is unclear

- `_enforcer_exists` matches only a top-level `def` at the start of a line:
  a test method inside a class, an `async def` or a parametrised id
  (`test_x[case]`) does not match. Whether any live plan names such a test is
  not measured yet.
- Whether the four live plans name their tests in a form a parser can read
  without a migration is not measured; the 2026-10-08 note says they do not
  share one form.
- The open questions of the 2026-10-08 note stand: whether archived changes'
  ledgers keep being checked, and whether the form admits non-pytest checks
  (shell commands) as an unchecked second kind of entry.

## Files a change would touch

- A new gate script under `scripts/` with its test and its mutation test
  (`tests/test_ci.py` demands both), and its entry in the gate list that
  `make verify` and CI run.
- `prompts/03-plan.md` for the ledger form; possibly `templates/` if a plan
  template exists for it (none named `plan.md` under `templates/` on
  2026-10-11).
- The four live `plan.md` files, migrated to the form.
- `docs/WORKFLOW.md` where it lists the gates.
