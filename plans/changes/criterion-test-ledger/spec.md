---
title: "Spec — criterion-test-ledger"
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
tags: [spec, gates, tests, acceptance-criteria]
class: feature
appetite: 8
change: criterion-test-ledger
adr_question: {proposed: "no", reason: "One gate in the shape of the existing check scripts, a plan section described in the phase-3 prompt and the text check scripts/ramp_valves.py already makes; the rule itself is the maintainer's recorded answers, and no subsystem, interface or trust boundary changes."}
---

# Spec — `criterion-test-ledger`

The goal in one sentence: after this change, every test a plan names as
holding an acceptance criterion is held by a gate, so deleting or renaming it
without editing its line in the plan turns `make verify` red — while the
change is live and, for every ledger written from 2026-10-11 on, after it is
archived too (bead `coding-harness-909`). Research: `research.md`. Decisions:
`decisions.md` (Q-1 to Q-3). Options weighed:
`docs/research/2026-10-08-holding-criterion-tests.md`.

## Problem

- **A deleted criterion test goes unseen.** Deleting 29 of the 30 tests in
  `tests/test_research_currency.py` left `make verify` green (measured on
  `main` at `d5813ec`, 2026-10-06; `research.md`, first paragraph).
- **Nothing counts the tests.** `pytest` runs `tests/` as a whole, so a
  deleted test simply stops running; the ratchets in `tests/test_ci.py` hold
  the shape of the suite — one test file per script, one named mutation test
  per gate — not its content (research note, "What holds tests today", read
  at `b32f488`).
- **What ties a criterion to its tests is prose.** The four live plans name
  their tests in four forms: a table with up to six function names per cell
  (`harness-decide-adr`), a table of at most two names per row
  (`research-currency`), a table that names no function at all
  (`stage2-session`), and the file lists of build slices (`hermes-runner`)
  (`research.md`, "Measured for the spec", at `e31100f`). No parser reads
  them, and no gate tries.
- **The one existing check is not used for this.** `scripts/ramp_valves.py`
  already decides by text whether a named test function exists
  (`_enforcer_exists`), but only for the valves' enforcers (`research.md`,
  "What exists today").
- **Today only texts and people hold criterion tests:** the phase-3 and
  phase-4 prompts and the phase-6 reviewer (same section).

## Terms

- **Live change** — a directory directly under `plans/changes/` other than
  `archive/`. **Archived change** — a directory directly under
  `plans/changes/archive/`.
- **Ledger section** — in a `plan.md`, the lines after a level-2 heading that
  reads exactly `## Criterion ledger`, outside a fenced code block, up to the
  next level-1 or level-2 heading or the end of the file.
- **Entry** — a line of the ledger section in one of three forms, where `<n>`
  is a criterion number written without a leading zero:
  - **test entry** — `- <n>: tests/<path>::<function>`
  - **not-yet-written entry** — `- <n>: not yet written tests/<path>::<function>`
  - **not-a-test entry** — `- <n>: not a test — <text>`

  `<path>` is a path below `tests/` whose file name begins `test_` and ends
  `.py`; `<function>` begins `test_` and holds only letters, digits and
  underscores. A test entry and a not-yet-written entry may end in a
  separator and `<text>`, the fault that turns the test red. The separator is
  an em dash (`—`) with one space on each side; `<text>` is not blank.
- **Continuation line** — a line of the ledger section that begins with
  whitespace, follows an entry or another continuation line, and does not
  begin with a dash and a space after its whitespace. It continues the text
  of the entry above it and is not read.
- **Defined** — an entry's function is defined when the named file exists and
  holds a line beginning `def <function>(`: a top-level function, found by
  reading the file as text.
- **Criterion numbers** — the numbers `<n>` of the lines beginning with
  `<n>.` and a space, outside fenced code blocks, in the `spec.md` of the
  same change folder, between its `## Acceptance criteria` heading and the
  next level-2 heading; level-3 headings in between do not end the section.
- **Held plan** — a `plan.md` the gate checks: every live change's; an
  archived change's that has a ledger section; and an archived change's
  without one, unless its header holds the line `date: YYYY-MM-DD` with a
  date before 2026-10-11 (criterion 4).
- **The gate** — `scripts/check_criterion_ledger.py`, gate id
  `criterion-ledger`.

## Acceptance criteria

Criteria 1 to 4 say which plans the gate holds, 5 to 11 what it reads in
an entry, 12 to 14 how a ledger covers its spec, 15 to 18 what the gate
says, 19 to 23 how it is wired and described, and 24 to 28 what the
migration of the four live plans must leave behind.

1. When the gate runs, it holds the `plan.md` of every live change, whatever
   the plan's date and the change's class; a live change without a `plan.md`
   is not examined.
   *Refuted by:* a live `plan.md` without a ledger section exits 0; a live
   change folder holding only `research.md` is reported.
2. If a held plan has no ledger section, or more than one, the gate reports
   the plan.
   *Refuted by:* exit 0 for a held plan without the heading or with the
   heading twice; a `## Criterion ledger` line inside a fenced code block
   taken for the section.
3. When an archived change's `plan.md` has a ledger section, the gate holds
   it as it holds a live plan, whatever its date.
   *Refuted by:* an archived plan dated 2026-10-01 whose ledger names a
   deleted test exits 0.
4. If an archived change's `plan.md` has no ledger section, the gate exempts
   it only when its header holds the line `date: YYYY-MM-DD` with a date
   before 2026-10-11, the day of the maintainer's answers (`decisions.md`
   Q-2); otherwise it reports the missing section.
   *Refuted by:* an archived plan dated 2026-10-11 without a ledger exits 0;
   one whose `date` is quoted, commented, missing or unreadable is exempted;
   one dated 2026-10-10 without a ledger is reported.
5. If a line of the ledger section is neither an entry, a continuation line
   nor blank, the gate reports the plan, the line number and the three entry
   forms.
   *Refuted by:* exit 0 for any of these lines: `* 3: tests/test_a.py::test_b`,
   `3: tests/test_a.py::test_b`, ``- 3: `tests/test_a.py::test_b` ``,
   `- 03: tests/test_a.py::test_b`, `- 3: tests/test_a.py::TestA::test_b`,
   `- 3: tests/test_a.py::test_b[case]`, `- 3: tests/helpers.py::test_b`,
   `- 3: tests/test_a.py::test_b - a hyphen for the dash`, `- 3: not a test`,
   a sentence of prose, or an indented `- 4: tests/test_a.py::test_b`.
6. If a test entry's function is not defined, the gate reports the plan, the
   line, the criterion and the entry.
   *Refuted by:* exit 0 after the named function, or its file, is deleted; a
   function whose name only begins with the named one (`test_b_more` for
   `test_b`) counted as defined; a function defined only indented — in a
   class or inside another function — counted as defined.
7. When the gate decides whether a function is defined, it reads the file as
   text and never imports or runs it.
   *Refuted by:* a named test module whose top-level code writes a file leaves
   that file behind after a gate run.
8. While a change is live, a not-yet-written entry whose function is not
   defined is accepted.
   *Refuted by:* a live plan reported for a not-yet-written entry whose test
   does not exist yet.
9. If a not-yet-written entry's function is defined, the gate reports the
   entry and says to remove the marker.
   *Refuted by:* exit 0 for a not-yet-written entry whose test exists.
10. If an archived change's ledger holds a not-yet-written entry, the gate
    reports it, whether its function is defined or not.
    *Refuted by:* exit 0 for an archived plan with a not-yet-written entry.
11. When a ledger holds a not-a-test entry, the gate accepts it on its form
    alone.
    *Refuted by:* a well-formed not-a-test entry reported — for instance one
    whose text names a test file or function that does not exist.
12. If a criterion number of the change's `spec.md` has no entry in the
    ledger, the gate reports the plan and that number.
    *Refuted by:* exit 0 after the only entry for one criterion is deleted.
13. If an entry names a criterion number the change's `spec.md` does not
    have, the gate reports the entry.
    *Refuted by:* `- 99: …` in the ledger of a change with 16 criteria exits
    0.
14. If a held plan's folder has no `spec.md`, or its `spec.md` yields no
    criterion number, the gate reports the plan.
    *Refuted by:* exit 0 for a held plan beside a missing spec, or beside a
    spec without an `## Acceptance criteria` section.
15. When the gate finds nothing, it exits 0 and prints one line naming how
    many live and archived plans it held, how many entries of each kind it
    read, and how many archived plans the date exempted; when it held no
    plan, that line says it examined nothing.
    *Refuted by:* a green run without those counts; "OK", "pass" or "green"
    printed when no plan was held.
16. If the gate finds anything, it exits 1 and prints one line per finding,
    naming the plan's path, the line number where the finding has one, and
    what to do.
    *Refuted by:* exit 0 or 3 with a finding; a finding line without the path
    or without the remedy.
17. If a plan, a spec or a named test file cannot be read or is not valid
    UTF-8, the gate reports that file as a finding.
    *Refuted by:* exit 0 with such a file in the tree; the run ending in a
    traceback.
18. If the root it is pointed at is not a readable directory or has no
    `plans/changes/` directory, the gate exits 3 and says it could not
    measure.
    *Refuted by:* exit 0 or 1 for an empty directory as the root.
19. When the tree is verified, `decisions/gates.yaml` declares the gate
    `criterion-ledger` (job `verify`, enforcement `block`, placement `both`,
    floor `false`), `.github/workflows/ci.yml` regenerated from it matches,
    and a test asserts the declaration; the ratchets of `tests/test_ci.py`
    find the gate's test and its mutation test without a new exemption.
    *Refuted by:* that test green with the entry removed from
    `decisions/gates.yaml`; the gate `ci-drift` red; an entry for the new
    gate or script in `OHNE_MUTATIONSTEST`, `OHNE_TEST` or `OHNE_AUFRUFER`.
20. When the kit is classified, `scripts/check_criterion_ledger.py` and
    `tests/test_check_criterion_ledger.py` carry the role `mechanismus` in
    `scripts/kit/manifest.yaml`, and the test passes in the empty-repository
    probe.
    *Refuted by:* either file falls to a `bestand` rule; the gate `leerprobe`
    red on the new test.
21. When phase 3 is read, `prompts/03-plan.md` requires the ledger section,
    gives its heading and the three entry forms with one example each, says
    the gate holds it, and its requirement of a test per acceptance criterion
    points to the ledger.
    *Refuted by:* a plan written from the prompt alone without a ledger
    section, or with an entry form the gate refuses.
22. When phase 4 is read, `prompts/04-implement.md` says that writing a test
    removes its not-yet-written marker in the same commit, and that renaming
    or removing a test a ledger names changes that ledger line in the same
    commit.
    *Refuted by:* the prompt without either of the two rules.
23. When `docs/WORKFLOW.md` is read, its stage-1 table names the gate, what
    it holds, and that ledgers stay held after archiving while archived plans
    dated before 2026-10-11 without one are exempt.
    *Refuted by:* no row for the gate; a row without the exemption or its
    date.
24. When the gate runs over this repository at the pull request's head, it
    finds nothing; it holds the four migrated plans (`harness-decide-adr`,
    `hermes-runner`, `research-currency`, `stage2-session`) and this change's
    own plan, and exempts every archived plan dated before 2026-10-11 (17 on
    2026-10-11 at `e31100f`).
    *Refuted by:* any finding; one of those five plans not held; an archived
    plan reported.
25. When a migrated ledger is read beside its plan, every test function the
    plan names as holding one of the change's criteria — in a per-criterion
    table, or among the tests a step or slice builds — stands in the ledger
    for a criterion it holds: as a test entry when it is defined, as a
    not-yet-written entry when it is not.
    *Refuted by:* a function named in `harness-decide-adr`'s "Test per
    criterion" table or in `research-currency`'s "Tests" table missing from
    its ledger; one of the `hermes-runner` tests not built yet (39 on
    2026-10-11) missing, or entered as a test entry.
26. If a migrated plan holds a criterion by a test, its ledger does not hold
    that criterion by not-a-test entries alone.
    *Refuted by:* a `stage2-session` criterion whose row in "Tests and faults"
    describes a test, held only by not-a-test entries.
27. When the migration is done, every migrated plan that carries an earlier
    per-criterion table carries, directly above it, one line saying that the
    ledger is the list the gate holds.
    *Refuted by:* `harness-decide-adr`'s "Test per criterion",
    `research-currency`'s "Tests" or `stage2-session`'s "Tests and faults"
    table without that line.
28. When the deletion of 29 of the 30 test functions of
    `tests/test_research_currency.py` is replayed on a copy of the tree, the
    gate exits 1 and names each deleted function that `research-currency`'s
    ledger names.
    *Refuted by:* exit 0 — the measured failure of bead coding-harness-909
    still stands.

## Non-goals

- **No count of tests per file** (`decisions.md` Q-1, option 2 not taken): a
  test that no ledger names can still be deleted unseen. A finding that such
  a deletion did harm brings the question back.
- **Not folded into the change-artefact validator** (bead coding-harness-jc3,
  `scripts/validate_change_artefacts.py`, not in the tree): the check moves
  there when that validator lands, as the research note recommends.
- **The archived plans dated before 2026-10-11 get no ledger** (`decisions.md`
  Q-2): 17 on 2026-10-11, all left as written.
- **The gate does not run a test.** Whether a named test is collected, passes,
  is skipped or really tests its criterion stays with `pytest` and the
  phase-6 review; the gate holds that it is there.
- **The gate does not judge the kind of an entry.** Whether a criterion held
  by a not-a-test entry should have a test is the phase-6 review's question;
  the text of a not-a-test entry is never run or checked.
- **No class methods, `async` functions or parametrised cases as entries.**
  None is named as a criterion's test today (`research.md`, "Measured for the
  spec"); the first one to be needed widens the form in a change of its own.
- **Living capability specs** (`plans/specs/`) are not held.
- **No per-change option** (`--change`): the gate reads text files only, and
  phase 3 runs it whole.
- **No change to the valves.** `scripts/ramp_valves.py` keeps its behaviour;
  whether the gate shares its text check is the plan's choice.
- **No architecture beyond the ADR:** the change adds one gate in the shape
  of the existing check scripts, one entry in the one gate list and one
  section to an existing artefact; nothing else crosses a boundary or is
  stored beyond plan text. Phase 2b runs only because the maintainer asked
  for an ADR (2026-10-11): its `design.md` carries the ADR draft and nothing
  more (`prompts/02b-design.md`).

## Protected areas

- **`plans/changes/archive/`** — history; this change edits none of the
  archived folders (Q-2 exempts them).
- **Every existing file under `tests/`** — no test is renamed, moved,
  rewritten or deleted to fit a ledger: a ledger records the tests as they
  stand.
- **The four live changes beyond their `plan.md`** — their `spec.md`,
  `research.md`, `decisions.md`, `findings.md` and `design.md` stay as they
  are; in each `plan.md` only the ledger section and the pointer line of
  criterion 27 are added, plus the header stamps a gate demands of an edited
  file.
- **`AGENTS.md`** — 198 lines against a budget of 200 on 2026-10-11
  (`tests/test_entry_points.py`); the rule lives in the phase prompts and
  `docs/WORKFLOW.md`, and the gate's findings say what to do.
- **`plans/_README.md`** — German; house rule 1 forbids translating it in
  passing, and an English paragraph inside it would mix the two.
- **`docs/adr/` and `docs/governance/`** — `human-decided` where
  `provenance.yaml` says so. The maintainer asked for an ADR (answer recorded
  2026-10-11, `decisions.md` Q-4 and Q-5); this change writes its draft
  under `docs/adr/`, and it takes effect only with the maintainer's merge of
  the decision pull request (ADR 0008).
- **`decisions/answers/`** — `human-decided`; exactly one file is written
  there, `decisions/answers/criterion-test-ledger/adr.yaml`, and only through
  `python3 scripts/harness.py decide adr` from the maintainer's stated answer
  (ADR 0008).
- **`.beads/`** — written only by the tracker-writing session, through
  `tools/bd`.
- **The worktrees of parallel sessions.**

## Definition of Done

- `verify` green.
- Moved in the same pull request: `scripts/check_criterion_ledger.py`,
  `tests/test_check_criterion_ledger.py`, `decisions/gates.yaml`,
  `.github/workflows/ci.yml` (regenerated), `scripts/kit/manifest.yaml`,
  `prompts/03-plan.md`, `prompts/04-implement.md`, `docs/WORKFLOW.md`, the
  `plan.md` of `harness-decide-adr`, `hermes-runner`, `research-currency` and
  `stage2-session`, this change's own `plan.md`, `plans/INDEX.md`
  (regenerated), `decisions/answers/criterion-test-ledger/adr.yaml` (the
  maintainer's recorded answer), the ADR draft under `docs/adr/` with its
  index entry, and this change's own workflow artefacts under
  `plans/changes/criterion-test-ledger/` (`research.md`, `decisions.md`,
  `spec.md`, `design.md`, `plan.md`, `findings.md`) — no file beyond these
  in the pull request's file list.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes `coding-harness-909`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-909`
  (`prompts/07-commit.md`).
- Special runs: the replay of criterion 28 — the command, its output and the
  commit it ran on in the pull request body.

## Open decisions

No `[DECISION]` is open: the maintainer settled the five questions this
change raises (`decisions.md` Q-1 to Q-5).

**The ADR question** is answered: the header proposed "no"; the maintainer
answered "yes" on 2026-10-11 (`decisions/answers/criterion-test-ledger/adr.yaml`).
The ADR fixes the principle of Q-4 — every acceptance criterion names in its
plan what proves it, a gate checks that this proof still exists, and a test
disappears only through a visible edit of the plan — and, per Q-5, the gate
travels with the kit from this change on. Design (phase 2b) writes the ADR
draft; the Definition of Done gains that file.

### `[GAP]`s — closed by reading

Each is recorded in `research.md`, "Measured for the spec" and "Corrections
after verification", at `e31100f`.

- *Do the live plans name tests a parser can read?* No — four different
  forms, one of them without any function name; `hermes-runner` names 39
  functions that do not exist yet.
- *Do the limits of `_enforcer_exists` matter?* Not today: 846 top-level test
  functions, none indented, `async` or in a class; no live plan names a
  parametrised case as a criterion's test.
- *Can the gate read a spec's criterion numbers?* Yes: every spec in the tree
  numbers its criteria `<n>.` at the start of a line, from 1, without
  restart.
- *How many archived changes are exempt?* 20 folders, 17 with a `plan.md`,
  all dated 2026-10-08 or earlier — not 13, the number pull request #116
  moved.

### `[DETAIL]`s — decided here, with the reason

Each is reversible and binds nothing beyond this change; a "no" from the
maintainer changes the one criterion it names.

1. **The entry form** — list lines `- <n>: …`, one criterion per line, three
   kinds, an optional trailing text after an em dash. One line per test is
   what a rename edits and what a finding points to; a table cell with
   several names (as in `harness-decide-adr`) or a `|` inside a shell command
   would break either the one-line edit or the parse. It is the research
   note's form (`<criterion number>: tests/<file>.py::<function>`) with a
   list dash, so the section renders as a list.
2. **The heading `## Criterion ledger`** — it differs from the three table
   headings the live plans use ("Test per criterion", "Tests", "Tests and
   faults"), so a migrated plan carries both without a clash, and a search
   finds only the ledger.
3. **The not-yet-written marker** (criteria 8 to 10) — phase 3 names tests
   before phase 4 writes them, and `hermes-runner` sits on `main` that way
   with 39; without the marker every plan is red from phase 3 to phase 4.
   Refusing the marker on a defined function means a test is held from the
   commit that writes it; refusing it in the archive means a change cannot
   be closed over a test it never wrote.
4. **Not-a-test entries as an unchecked second kind** (criterion 11; the
   question the research note left open) — criteria held by a review, a
   gate, a shell command or the maintainer's own hands (`hermes-runner`
   slices 6 and 7) need an honest entry once every criterion must have one
   (detail 5); the gate holds tests (Q-1), so their text is not checked.
5. **Coverage both ways** (criteria 12 to 14) — without it, deleting a test
   together with its only ledger line stays green, and an empty ledger
   passes. `prompts/03-plan.md` already asks for a test per criterion, so
   this checks a duty that exists and adds none.
6. **New against exempt: the section first, then the plan's own `date`**
   (criteria 3 and 4). A cut-off date alone would exempt the four migrated
   plans, dated 2026-09-30 to 2026-10-07, once they are archived — against
   Q-2. The section alone would let a plan written from now on escape by
   being archived without one. A list of the exempt folders would put this
   repository's stock into a script that travels with the kit (detail 9),
   and every new repository would carry 17 foreign names. The cut-off is the
   day of the maintainer's answers; a quoted, commented, missing or
   unreadable date measures instead of exempting, as the gate
   `interview-minimums` does. The
   one escape left — deleting the whole section of a migrated plan after it
   is archived — is a visible edit of every line, the price Q-2 names.
7. **Top-level functions, found by text** (criteria 6 and 7) — measured at
   `e31100f`: 846 top-level test functions, none indented, `async` or in a
   class. The text search is the one `_enforcer_exists` makes, chosen there
   because an import runs foreign code in every run. A method, an `async`
   function or a parametrised case is refused by the form (criterion 5),
   never silently left unchecked.
8. **Test files named `test_*.py` only** — `pytest` collects `test_*.py` by
   default (and `*_test.py`, a form this repository does not use), and
   `pyproject.toml` sets no `python_files`; a function in `tests/helpers.py`
   would be held and never run.
9. **The gate travels with the kit** (criterion 20) — the gate list and
   `prompts/03-plan.md` travel, and a form without its gate is a rule without
   an enforcer; the script of `adr-answers` travels for the same reason. The
   test builds its own trees and reads nothing of this repository.
10. **Names** — `scripts/check_criterion_ledger.py`, gate id
    `criterion-ledger`, `tests/test_check_criterion_ledger.py`: the
    `check_<subject>.py` and `test_check_<subject>.py` pattern of the two
    newest gates (`adr-answers`, `interview-minimums`).
11. **The earlier tables stay, with a pointer** (criterion 27) — their plans'
    steps and repair-round logs refer to them, so swapping them for the
    ledger breaks those references; left unmarked, they would be a second
    list of which only one is held.
12. **Appetite 8 hours** — about 3 for the gate and its tests, 4 for the
    migration (106 criteria over four plans, one of them without a single
    function name), 1 for the texts and the wiring. A stop, not an estimate;
    the plan card may say less.
