---
title: "ADR 0013 — Every acceptance criterion names its proof in its plan, and a gate holds that the proof still exists"
category: adr
status: accepted
created: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-11
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, gates, tests, acceptance-criteria, kit]
---

# ADR 0013 — Every acceptance criterion names its proof in its plan, and a gate holds that the proof still exists

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends no decision and supersedes no ADR.
* Review: the maintainer's answers of 2026-10-11 in the directing
  conversation, recorded as Q-1 to Q-5 in
  `plans/changes/criterion-test-ledger/decisions.md` — a ledger per change,
  checked by a gate (Q-1); ledgers stay held after archiving, the changes
  archived before stay exempt (Q-2); the four live plans are migrated (Q-3);
  the principle and its two reasons, asked after the maintainer's "Doch, mach
  es als adr" (Q-4); the gate travels with the kit at once (Q-5) — and the
  answer "yes" to the ADR question
  (`decisions/answers/criterion-test-ledger/adr.yaml`) · the acceptance is the
  merge commit and is written nowhere else, so the header's `review` stays
  empty (ADR 0008) · Decider: maintainer · prepared by a Claude Code session
* Date: 2026-10-11 · takes effect on merge

## Context

* **A deleted criterion test went unseen.** Deleting 29 of the 30 test
  functions in `tests/test_research_currency.py` left `make verify` green
  (measured on `main` at `d5813ec`, 2026-10-06; bead coding-harness-909).
* **Nothing counts the tests.** `pytest` runs `tests/` whole, so a deleted
  test simply stops running. The ratchets of `tests/test_ci.py` hold the
  shape of the suite — one test file per script, one named mutation test per
  gate — not its content
  (`docs/research/2026-10-08-holding-criterion-tests.md`, read at `b32f488`).
* **What ties a criterion to its tests is prose.** The four live plans name
  their tests in four forms, one of them without a single function name, and
  no parser reads them (`plans/changes/criterion-test-ledger/research.md`,
  "Measured for the spec", at `e31100f`). Only the phase-3 and phase-4
  prompts and the phase-6 reviewer hold a criterion's tests.
* **The workflow runs beyond this repository.** The kit carries the gate list
  and the phase prompts into new repositories, and LakeSwitch runs an
  instance of the workflow (`AGENTS.md`, "Sibling repositories"). An instance
  receives the kit through a pinned release, which the release builder is to
  provide (bead coding-harness-dj9, open on 2026-10-11).
* **Models write the tests.** The maintainer names the risk this record is
  meant to bind: models that "repair" a red test by deleting it
  (`decisions.md` Q-4).

## Decision Drivers

* A deleted criterion test turns the run red (Q-1).
* A rename costs one line of the plan in the same commit, not a freeze of
  every refactoring (Q-1; the cost of the count ratchet in the research
  note's option 2).
* The rule holds wherever the workflow runs, also where a gate alone could be
  switched off unnoticed (Q-4, reason a).
* A model cannot make a red test disappear without a visible edit of the plan
  (Q-4, reason b).
* Plans archived before the rule are not made a burden after the fact (Q-2).

## Considered Options

On the mechanism, from the research note's section "Options":

* (1) **A criterion ledger per change, checked by a gate.** The plan names
  each criterion's tests in a fixed form; a gate refuses a named test that no
  longer exists. A rename edits the plan's line in the same commit.
* (2) **A test count per file that only falls with a reason.** Holds every
  deletion forever, but every refactoring that merges two tests needs a
  ledger edit.
* (3) **Fold the check into the change-artefact validator** (bead
  coding-harness-jc3). The same check, inside a validator that does not exist
  yet; it waits for that validator.
* (4) **Nothing mechanical.** The prompts and phase 6 stay the only holders;
  the measured gap stays.

On how long a ledger is held (Q-2): live changes only; every ledger written
from now on, also after archiving, with the older archive exempt; or the
older archive migrated as well.

On the form of the decision (Q-4): a gate without a recorded principle, or
the principle recorded as an ADR.

On its reach (Q-5): the gate tried here first, kept local behind a later
ADR, or carried with the kit from this change on.

## Decision

Chosen: option (1), held after archiving for every ledger written from
2026-10-11, recorded as a principle, and carried with the kit at once —
because a gate alone could be switched off unnoticed where the workflow runs
beyond this repository, and because the rule is a trust rule against models
that delete a red test (Q-4).

**The principle**, in three parts:

1. Every acceptance criterion names in its plan what proves it.
2. A gate checks that this proof still exists.
3. A test disappears only through a visible edit of the plan.

**How it holds from this change on:**

* The proof is named in a criterion ledger, a section of the change's
  `plan.md`; the gate `criterion-ledger`
  (`scripts/check_criterion_ledger.py`, job `verify`, enforcement `block`)
  holds it.
* A ledger is held while its change is live and after the change is
  archived. An archived plan without a ledger is exempt only when its header
  dates it before 2026-10-11, the day of the maintainer's answers; that
  exempts the changes archived before this one (Q-2).
* The four live plans are migrated in the pull request that carries this
  record (Q-3).
* The gate script and its test travel with the kit as mechanism
  (`scripts/kit/manifest.yaml`). An instance such as LakeSwitch receives them
  with its next pinned Coding Harness release (bead coding-harness-dj9; Q-5).

**What this record does not fix.** The entry form, the heading, the gate's
messages and the place of the check are the change's design, not the
decision: they change in an ordinary change as long as the three parts hold.
The check moves into the change-artefact validator when that validator lands
(bead coding-harness-jc3), as the research note recommends.

This record amends no decision. It gives a workflow rule an enforcer, as D-9
asks of every retained rule, and the enforcer travels as mechanism, as D-11
says of the change-artefact validator (the "Decision continuity" table of
`docs/architecture/2026-09-17-omnigent-first-target.md`, read 2026-10-11).

## Consequences

* **A rename costs one plan line in the same commit** (Q-1), and a test no
  longer needed costs an edit in an archived plan (Q-2).
* **The migration is the largest part of the work** (Q-3): 106 criteria over
  four plans on 2026-10-11, one plan without a single function name.
* **Changing the principle takes a decision pull request** (Q-4).
* **An instance runs the gate without a trial period here first** (Q-5). When
  the gate arrives there, every live plan of the instance needs a ledger, and
  an archived plan there without one is reported unless its header dates it
  before 2026-10-11; how the instance's plans are laid out was not read for
  this record.
* **What stays unheld.** A test that no ledger names can still be deleted
  unseen (option 2 was not taken). Whether a named test is collected, passes,
  is skipped or really tests its criterion stays with `pytest` and the
  phase-6 review: the gate holds that it is there. A criterion held by a
  review, a gate or a command is named in the ledger, but that text is not
  checked.
* **One escape is left, and it is visible.** A plan dated before 2026-10-11
  that loses its whole ledger section after it is archived falls back to the
  exemption — an edit of every line of the section, the price Q-2 names.
* **The 17 archived plans dated before 2026-10-11** (counted at `e31100f`)
  hold nothing and get no ledger.

## Validation

* The gate `criterion-ledger` is green at the head of the pull request that
  carries this record: it holds the four migrated plans and the plan of
  `criterion-test-ledger`, and exempts the 17 earlier archived plans.
* The gate has its mutation test, and the ratchets of `tests/test_ci.py` find
  it without an exemption.
* The measured failure is replayed: on a copy of the tree, the deletion of 29
  of the 30 test functions of `tests/test_research_currency.py` turns the gate
  red, naming each deleted function the ledger names; the command and its
  output stand in the pull request's body.
* The empty-repository probe (gate `leerprobe`) is green with the gate's test,
  which shows the mechanism travels.
* Not validated by this record: an instance running the gate. That comes with
  the release of bead coding-harness-dj9.
