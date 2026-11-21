---
title: "Test strategy for the repository and the kit — draft"
category: research
created: 2026-11-12
updated: 2026-11-12
last_reviewed: 2026-11-12
status: draft
implementation_status: none
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5.2, 2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [testing, make-verify, kit, strategy, proposal]
---

# Test strategy for the repository and the kit — draft

The maintainer asked on 2026-11-12 for a solid test strategy for this
repository and for the kit that carries the workflow into other repositories
("entwerfe eine solide Test Strategie für das repo und Kit"). This page is the
orchestrator's draft. It is a proposal, not a decision: the research of bead
coding-harness-1ga5 (testing strategy, class feature) still owes its swarm
run, and the rules below take effect only through an ADR the maintainer
merges. Nothing here was built or tested.

## What was measured

| Fact | Value | Cut-off |
|---|---|---|
| Production code (`scripts/`, `tools/`, Python) | 36,731 lines | `origin/main`, 2026-11-12 |
| Test code (`tests/*.py`) | 76,299 lines in 77 test files | same |
| Tests in the full run | 5,657 passed, 17 skipped | 2026-11-12, `f1b42a43` |
| Suite growth | 4,082 tests in 520 s → 5,604 in 1,270 s | 2026-10-28 → 2026-11-12 |
| Largest test file | `tests/test_stage2.py`, 25,107 lines, 877 test functions, 631 sites that start a process or call git | 2026-11-12 |
| 60 slowest tests | 792 s; 438 s of them in `tests/test_stage2_swarm.py` | 2026-11-12, bead coding-harness-dca4 |
| Other gates | seconds each, except `leerprobe` at 204 s | same |
| Slow or integration markers in `tests/` | none | 2026-11-12 |

Not measured: how many tests assert the wording of a document, how many are
duplicates, how many can never fail, and the run time per test file.

## What goes wrong today

1. **One tier.** Every test runs every time. A unit test of a pure function
   and a test that builds three git repositories sit in the same file and the
   same run, so the fast ones cannot give fast feedback.
2. **Tests grow, nothing retires.** Each review finding adds a test (the
   red-first proof); no rule says when a test may go. Test code doubled in
   five weeks.
3. **Tests pin details, not behaviour.** On 2026-11-12 thirteen tests went
   red because an output format changed (bead coding-harness-0swp). Twelve
   guarded real guarantees, but through the exact shape of a text block.
4. **One 25,000-line file defeats the targeted check.** A change that touches
   `tests/test_stage2.py` falls back to the full run (bead coding-harness-vg9).
5. **Wall-clock tests flake under load.** Two tests failed only because
   another run was active or midnight passed (beads coding-harness-gxcj,
   coding-harness-bxxt.5).
6. **Limits kill correct work.** A targeted run of the swarm tests cannot end
   inside the runner's 5-minute tool limit (bead coding-harness-dq4u).

## Principles

1. **A test earns its place by the fault it would catch.** Every test names
   its planted fault in one line (most already do). A test that cannot name
   one is a candidate for removal.
2. **Test the contract, not the rendering.** A guarantee such as "a passing
   attempt adds nothing to the record" is asserted through a parsed structure
   (a helper that reads the record into attempts and blocks), not through
   line positions or literal text. One helper per record format; when the
   format changes, one helper changes.
3. **Speed is a budget, not a hope.** Each tier has a time budget that a gate
   measures. Exceeding it is a red gate with the slowest tests named.
4. **No real time, no shared machine state.** Clocks, dates, temporary roots
   and process ids are injected or pinned.
5. **The kit's tests must pass in a repository that is not this one.**

## Three tiers

| Tier | What belongs in it | Target budget | Runs |
|---|---|---|---|
| **fast** | Pure logic: parsing, selection, validation, rendering. No process, no git, no network, no sleep. | 60 s for the whole tier, 0.5 s per test | on every targeted check and every runner attempt |
| **integration** | One real boundary: a git repository from a prepared template, one subprocess, the verify lock, a stand-in model. | 8 minutes for the tier, 10 s per test | when the touched code maps to the test (touch map), and always before phase 6 and in CI |
| **system** | Whole runner verbs end to end, the swarm, the pinned Pi's real data, the kit probe in a throw-away repository. | 15 minutes, 60 s per test | before phase 6, in CI, and nightly — never inside a runner attempt |

How a test gets its tier (maintainer, 2026-11-12, answer C): it is derived
from what the test asks for, not stored in a folder or a hand-set marker. One
rule in `tests/conftest.py` blocks process starts and network access for
every test. A test that needs a process or git requests the fixture that
lifts the block, and requesting it is what makes the test `integration`; the
fixtures for the swarm, the pinned Pi's real data and the kit probe make it
`system`. A test that starts a process without the fixture fails. No file
moves, a new test cannot be classified wrongly, and the rule travels with the
kit in one file. Its limit: "starts a process" does not separate integration
from system, so that boundary rests on the named fixtures and on the
per-test budget. First step, before anything is built: one run with the block
switched on, counting the tests that fail on it — that gives the size of the
fast tier and shows whether the rule carries.

Budgets (maintainer, 2026-11-12, answer A): measure first; each tier's budget
starts at its measured time plus 10 % and may only go down from there; the
values in the table are the targets worked towards. A gate turns red when a
tier passes its budget and names the slowest tests. The budgets are values of
the central configuration.

The system tier never runs inside a runner attempt (maintainer, 2026-11-12,
answer A): an attempt runs the fast tier and the touched integration tests;
the system tier runs before phase 6, in CI and nightly. A fault it finds that
an attempt called green is counted as a slip.

## Rules for adding and retiring tests

- **Adding.** A review finding still gets its red-first proof. The proof goes
  into the lowest tier that can show the fault. If an existing test covers
  the guarantee, it is extended (a new parameter case) instead of a new
  function.
- **Retiring.** A test may be removed when (a) the code or guarantee it
  guards is gone, (b) another test guards the same guarantee at a lower tier,
  or (c) it cannot fail — shown by a mutation check on the lines it claims
  (ADR 0023 material, bead coding-harness-1ga5 notes). The removal names the
  reason in the commit; the criterion-ledger entry moves to the surviving
  test. Today the ledger makes every listed test permanent; this rule gives
  it an exit. The maintainer agreed on 2026-11-12 (answer A): the agent applies
  (a) and (b) itself and names them in the pull request; (c) needs the
  mutation evidence.
- **Transition tests end with their bead** (maintainer's idea, 2026-11-12). A
  test is either a lasting guarantee or a transition test: one that guards a
  migration, an intermediate state or a one-off condition. A transition test
  is marked "until bead X closes". A gate reads the bead's state through the
  existing render; once the bead is closed it reports the test, which is then
  deleted or deliberately promoted to a lasting guarantee. Every new test
  chooses one of the two. A lasting guarantee never expires with a bead: its
  work starts at the merge.
- **Wording tests.** A test may pin the wording of a document only where
  another program reads that wording (a marker, a heading a gate parses, a
  command line). Prose is checked by review, not by assertion.
- **Budget per change.** The size gate (bead coding-harness-g8g7) reports
  test lines and code lines of a change separately; a change whose test lines
  pass three times its code lines states why in its plan.
- **Flaky tests.** A test that fails without a code change gets a bead the
  same day and is repaired or quarantined (moved to the system tier's nightly
  set) within a week; it never stays in the blocking set unrepaired.

## Shared fixtures

- One prepared git repository template per session, copied per test, instead
  of `git init` and commits in each test.
- One fake clock and one pinned date fixture; no test reads the real time.
- One record parser for `findings.md` and the loop record (principle 2).
- Stand-ins for `make`, `ruff`, models and `bash` live in one module with
  their own fast tests; a test scripts steps, never the stand-in's internals.

## The kit

The kit (`scripts/kit/manifest.yaml`) decides which files make up the
workflow in another repository. For tests this means:

1. **Each test file is classified**: travels with the kit, or describes only
   this repository. The manifest already does this per file (35 lines name a
   path under `tests/`, 2026-11-12); the derived tiers leave it untouched.
2. **A travelling test may not depend on this repository's stock** (its
   plans, its beads, its ADR numbers). It gets what it needs from fixtures.
   A gate runs the travelling tests inside the kit probe's throw-away
   repository; a test that passes only here is red there.
3. **The receiving repository gets the tiers and budgets with the kit**, with
   the budgets as values of the central configuration (bead
   coding-harness-twvx), so a slower machine changes a number, not code.
4. **Contract tests guard the seams** between kit and repository: the gate
   list, the manifest roles, the pinned tool versions. They are system tier.
5. **The kit carries no test of this repository's history** (archived plans,
   one-time migrations).

## What to measure

One line per full run in the existing run log (`verify-duration.jsonl`):
tests per tier, wall time per tier, the ten slowest tests, tests added and
removed since the last run on main. The morning handover names three numbers:
total tests, full-run minutes, and slips (a fault the targeted check called
green that the full run found, bead coding-harness-0swp Q-5).

## Order of work

1. Measure durations per test file once, isolated, and run once with the
   process block switched on (extends bead coding-harness-dca4).
2. Split `tests/test_stage2.py` along `scripts/stage2.py`'s modules (bead
   coding-harness-vg9) — the single largest lever, because the targeted check
   then covers runner changes.
3. Introduce the blocking rule and the tier fixtures in `tests/conftest.py`;
   set the budgets from step 1.
4. Shared fixtures: git template, fake clock, record parser (bead
   coding-harness-dca4, second half).
5. The targeted check's own time limit (bead coding-harness-dq4u).
6. The retirement rule and the first audit: duplicates, wording tests,
   tests that cannot fail (bead coding-harness-1ga5).
7. Kit: run the travelling tests in the probe repository as a gate.

## Decisions of 2026-11-12

The maintainer answered the draft's four questions on 2026-11-12; they are
worked into the sections above. They are input for the ADR, which takes
effect when its pull request merges.

1. Tier: derived from the fixtures a test requests (answer C), with the
   measurement run as the first step.
2. Budgets: measured value plus 10 %, only downwards, with target values
   (answer A).
3. Retiring: allowed under the three conditions with the reason in the commit
   (answer A), and transition tests end with their bead.
4. The system tier leaves the runner's attempts (answer A).

## Sources

- Bead notes: coding-harness-dca4 (durations, 2026-11-12), coding-harness-1ga5
  (growth, 2026-11-07), coding-harness-0swp (the thirteen tests, 2026-11-12).
- [make verify in the long term](2026-11-09-make-verify-long-term.md)
- [verify duration baseline](2026-11-04-verify-duration-baseline.md)
