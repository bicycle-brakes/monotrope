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

## Measured for the spec

Read on 2026-10-11 at `e31100f` (this branch after merging `origin/main`
`99bbe02`) by the phase-2 session, to close the points above that the
repository can answer.

- **The limits of `_enforcer_exists` touch nothing today.** `tests/` holds
  846 lines beginning `def test_`, none indented, none `async def`, and no
  test class. Every test function the four live plans name and that exists
  is a top-level function: 60 in `harness-decide-adr`, 30 in
  `research-currency`, 2 in `hermes-runner`. Parametrised ids
  (`test_x[case]`) occur three times, each inside the quoted output of a
  planted-fault run (`hermes-runner` plan lines 202 and 299,
  `research-currency` plan line 358), never as a criterion's test. Two
  function names exist in two test files each
  (`test_the_kit_carries_the_script_and_its_test`,
  `test_two_runs_give_the_same_bytes`), so an entry must name its file.
- **The four live plans need a migration; no parser reads them as they
  are.** `harness-decide-adr` maps criteria to tests in a table ("Test per
  criterion") with up to six function names per cell; `research-currency`
  in a table ("Tests"); `stage2-session` in a table ("Tests and faults")
  that names no function at all, only what is tested; `hermes-runner`
  names its tests inside the file lists of its slices, and 39 of the 41
  functions it names are not defined anywhere under `tests/` — slices 4
  and 5 are not built yet (`implementation_status: partial`).
- **A plan names tests before they exist.** Phase 3 writes the plan before
  phase 4 writes the tests (`prompts/03-plan.md`, "Per acceptance criterion
  the test that holds it"), and `hermes-runner` is on `main` in that state.
  A gate that only asks "is the named test defined" is red from every
  phase-3 commit until phase 4 ends.
- **Spec criteria are machine-readable.** In every spec under
  `plans/changes/` and `plans/changes/archive/`, the acceptance criteria
  are the lines beginning with `<n>.` and a space, between
  `## Acceptance criteria` and the next level-2 heading, numbered from 1
  without restart, also where level-3 sub-headings group them
  (`hermes-runner`, 1 to 59 over seven slices).
- **Plan dates.** The 17 archived `plan.md` files carry an unquoted header
  `date:` from 2026-09-21 to 2026-10-08; the four live plans 2026-09-30
  (`harness-decide-adr`), 2026-10-05 (`hermes-runner`,
  `research-currency`) and 2026-10-07 (`stage2-session`). A cut-off on any
  date in the files cannot tell the four migrated plans from the archived
  stock once they are archived themselves.
- **The kit.** `scripts/kit/manifest.yaml` gives the gate list
  (`decisions/gates.yaml`) the role `mechanismus` and, for
  `check_adr_answers.py`, the reason "the gate file travels, so its script
  does"; `check_interview_minimums.py` has no entry and falls to the
  catch-all `scripts/` (`bestand`).
- **The change-artefact validator does not exist.**
  `scripts/validate_change_artefacts.py`, named as the phase-2 and phase-3
  gate in `prompts/02-spec.md` and `prompts/03-plan.md`, is not in the tree
  (bead coding-harness-jc3).

## Corrections after verification

- The counts "73, 46, 90 and 6" above, and the "215 occurrences" in
  `decisions.md` Q-3, are counts of *lines* containing `test_`. Occurrences
  are 107, 62, 138 and 7; distinct names 68, 46, 34 and 3 (file names
  included).
- `plans/changes/archive/` holds 20 change folders, not 13: pull request
  #116 moved 13 (`c96f164`), seven were archived before. 17 of the 20 carry
  a `plan.md`. The maintainer's answer to Q-2 exempts "the changes archived
  before this change", which covers all of them; the decision is not
  reopened.
