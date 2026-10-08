---
title: "Holding the tests of acceptance criteria — options for the gap no gate covers"
category: research
status: proposed
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-08"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, gates, tests, acceptance-criteria, ratchet]
---

# Holding the tests of acceptance criteria

Research for bead coding-harness-909: deleting 29 of the 30 tests in
`tests/test_research_currency.py` left `make verify` green (measured by the
ponytail research on `main` at `d5813ec`, 2026-10-06; the file was
restored). Facts below read on 2026-10-08 at `origin/main` `b32f488`. The
choice among the options is the maintainer's.

## What holds tests today

- `pytest` runs `tests/` whole; a deleted test simply stops running.
- Ratchets in `tests/test_ci.py` hold the *shape*, not the content:
  `test_every_script_has_a_test_or_a_declared_reason` (one test file per
  script), `test_every_gate_step_has_a_mutation_test` and
  `test_the_mutation_ratchet_only_turns_one_way` (one named mutation test
  per gate).
- `scripts/ramp_valves.py` already checks that a named test function exists
  (`_enforcer_exists`, by text search for `def <name>(` in the named file,
  not by import) — but only for the valves' enforcers.
- What ties a criterion to its tests is prose: each spec criterion ends with
  *Refuted by:* (350 such lines in the specs of the 10 live change folders),
  and the plans say how each is checked, in no fixed form: `adhd-frame` has
  a "Checks per criterion" section of shell commands; `stage2-flash-runner`
  and `research-currency` name test functions under "Tests" and in their
  steps (62 and 90 occurrences of `test_`). Prompts 03 and 04 and the phase-6 reviewer are the
  only holders.

## Options

1. **A criterion ledger per change, checked by a gate (recommended).** Each
   plan's "Checks per criterion" names its tests as pytest node ids in a fixed
   form (`<criterion number>: tests/<file>.py::<function>`); a gate reuses
   `_enforcer_exists` and refuses a named test that no longer exists, for
   every change folder not yet archived. Consequence: the 29-of-30 deletion
   turns red while the change is live; a rename means editing the plan's line
   in the same commit, which is the contract the plan already claims; after
   archiving, nothing holds the tests any more. Cost: a form in
   `prompts/03-plan.md`, one small gate with its mutation test, a migration of
   the live plans.
2. **A test count per file that only falls with a reason.** A checked-in
   ledger of test counts per `tests/` file; a drop needs a reason line, like
   `test_the_mutation_exemption_list_only_shrinks`. Consequence: holds any
   deletion forever, but every refactor that merges two tests needs a ledger
   edit — the freezing the bead asks to avoid.
3. **Fold the map into the change-artefact validator** (bead
   coding-harness-jc3). Consequence: the same check as option 1, inside the
   validator that also checks class and Definition of Done; it waits for that
   validator.
4. **Do nothing mechanical.** Consequence: prompts and phase 6 stay the only
   holders; the measured gap stays.

Recommended: 1 now, moved into the validator when coding-harness-jc3 lands.
It reuses an existing, tested check; it does not freeze refactors beyond what
a live plan already promises.

## Open for the decision

- Whether archived changes' ledgers keep being checked (holds tests longer,
  but makes old plans a refactoring burden).
- Whether the form allows non-pytest checks (shell commands, as in
  `adhd-frame`) as a second kind of entry, unchecked.
