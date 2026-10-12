---
title: "Decisions — criterion-test-ledger"
status: draft
implementation_status: partial
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
tags: [decisions, interview, gates, tests]
---

# Decisions — criterion-test-ledger

Interview for a `feature` change that carries an ADR (at least five counted
records; the maintainer asked for the ADR on 2026-10-11). Options and
their consequences: `docs/research/2026-10-08-holding-criterion-tests.md`.

## Q-1 · How the tests of acceptance criteria are held

asked: 2026-10-11, the directing conversation
answer: option 1 — a ledger per change, checked by a gate: the plan names
  every test by name, the gate turns red when one is missing, and whoever
  renames a test updates the plan's line in the same commit
answered_by: maintainer
status: answered

In the context of a suite where deleting 29 of 30 tests of one script left
`make verify` green, facing a count ratchet, waiting for the change-artefact
validator (bead coding-harness-jc3) or doing nothing, we decided a named-test
ledger per change checked by a gate, to achieve that a deleted criterion test
turns the run red, accepting that a rename costs one plan-line edit in the
same commit. — 2026-10-11

## Q-2 · How long the gate holds a change's ledger

asked: 2026-10-11, the directing conversation
answer: option 3 — every ledger written from now on stays checked after its
  change is archived; the changes archived before this change stay exempt
answered_by: maintainer
status: answered

In the context of a ledger that would stop holding anything once its change
moves to `plans/changes/archive/`, facing checking live changes only or
migrating the 13 already archived plans, we decided that ledgers written from
now on stay checked after archiving while the older archived plans stay
exempt, to achieve that a criterion test disappears only by a visible edit of
its ledger line, accepting that a test no longer needed costs an edit in an
archived plan. — 2026-10-11

## Q-3 · The four live changes

asked: 2026-10-11, the directing conversation
answer: option 1 — migrate all four live plans (`harness-decide-adr`,
  `hermes-runner`, `research-currency`, `stage2-session`) to the ledger form
  in this change
answered_by: maintainer
status: answered

In the context of four live plans that name their tests in no fixed form
(215 occurrences of `test_` on 2026-10-11), facing exempting them or migrating
each on its next touch, we decided to migrate all four in this change, to
achieve that `research-currency` — the change whose tests were deleted — is
held at once, accepting that the migration is the largest part of the work. —
2026-10-11

## Q-4 · What the ADR fixes as a principle, and why

asked: 2026-10-11, the directing conversation (after the maintainer's "Doch,
  mach es als adr")
answer: option (c), both reasons — the principle as proposed: every
  acceptance criterion names in its plan what proves it, a gate checks that
  this proof still exists, and a test disappears only through a visible edit
  of the plan. It is a principle rather than a gate alone because (a) it holds
  beyond this repository, in LakeSwitch and in whatever the kit carries into
  new repositories, where a gate alone could be switched off unnoticed, and
  (b) it is a trust rule against models that "repair" a red test by deleting
  it
answered_by: maintainer
status: answered

In the context of a gate that only this repository runs, facing a gate
without a recorded principle, we decided to fix the criterion-proof rule as an
ADR, to achieve that it travels with the kit and binds every model that
writes tests, accepting that changing it later takes a decision PR. —
2026-10-11

## Q-5 · How far the ADR reaches

asked: 2026-10-11, the directing conversation
answer: option 1 — at once with the kit: the gate script travels as kit
  mechanism (`scripts/kit/manifest.yaml`), and an instance such as LakeSwitch
  receives it with its next pinned Coding Harness release (bead
  coding-harness-dj9)
answered_by: maintainer
status: answered

In the context of a principle meant to hold beyond this repository, facing
trying the gate here first or keeping it local behind a later ADR, we decided
that the gate travels with the kit from this change on, to achieve that the
principle is enforced wherever the workflow runs, accepting that an instance
runs the gate without a trial period here first. — 2026-10-11
