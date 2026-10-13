---
title: "Decisions — ci-minutes"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-cac
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, ci, github-actions]
---

# Cut hosted CI minutes — Decisions

Phase 1a for bead coding-harness-cac, on 2026-10-13, after `research.md`.

## Settled before this change

The maintainer approved three measures on 2026-10-13, before this change
folder existed (bead coding-harness-cac, description): (1) a push starts CI
only on `main`; (2) a pull request runs only Python 3.12, push to `main`
keeps both interpreters; (3) a newer pull-request run cancels the older one
of the same pull request, and no run on `main` is ever cancelled. A
self-hosted runner was rejected for now. These are not asked again.

## SKIP · interview

status: skipped
reason: A bounded change whose three intent decisions the maintainer took on 2026-10-13 before the change opened; what remains is mechanics, decided below with reasons.

## Decided by the agent

[DETAIL] **Class `bounded`.** The change edits one existing, readable flow —
the generator `scripts/ci_gates.py` and its derived `ci.yml` — and decides
nothing the maintainer has not decided. No ADR, no design phase.

[DETAIL] **The nightly schedule stays as it is.** The bead says both legs
"stay" on the nightly schedule, but the schedule runs neither leg today: it
runs only the `drift` job, on 3.12 (`research.md`, "The nightly schedule does
not run the two legs today"). Adding both gate legs to the night would spend
minutes the change exists to save, and it would see nothing new: every merge
to `main` already runs both legs on the same commit. So the schedule is not
changed. Reversible by one line in the generator.

[DETAIL] **The pull-request interpreter is the last declared one**
(`tools.python[-1]`, today 3.12) — the same rule the `drift` job already
follows. No new key in `decisions/gates.yaml`, so its schema stays at
version 2, and a later move to 3.13 moves the pull-request leg with it.

[DETAIL] **The push filter names `main` literally**, as a constant in the
generator beside `MATRIX_JOB` and `SUMMARY_JOB`. The ruleset test already
treats `main` as the default branch. A repository taking the kit whose
default branch is not `main` would get no main-line runs; that is named in
the spec as a known limit, not solved here.

[DETAIL] **One expression picks the legs per event**, inside the matrix
(`fromJSON`), rather than a second job: the summary check `verify` keeps
needing exactly one matrix job, and the ruleset's required check is
unchanged.

[DETAIL] **A cancelled pull-request run may show a red `verify` on the
superseded commit.** The summary job runs under `always()`. Only the newest
commit's check gates the merge, so this is accepted and not worked around.

## Addendum — 2026-10-13 (amended 2026-10-13: maintainer decided 3.12 only)

The maintainer stopped the per-event matrix on 2026-10-13 and decided Python
3.12 only for coding-harness ("ich will 3.12 bei lakeswitch enforcen. Keine
doppelte Arbeit" — 3.12 is enforced in lakeswitch-ai too, so no work is done
twice; lakeswitch-ai moves under its bead lakeswitch-ai-6sj). This replaces
measure 2 above. Measures 1 and 3 stand. The skip record stands: the decision
was the maintainer's, not asked here.

Superseded by this addendum: the `[DETAIL]` points "The nightly schedule
stays as it is" (moot — there is one interpreter), "The pull-request
interpreter is the last declared one" and "One expression picks the legs per
event" (no per-event matrix any more).

[DETAIL] **Class stays `bounded`.** Dropping 3.11 edits declarations that
already exist (`tools.python`, `requires-python`, the ruff target) and decides
nothing the maintainer did not decide.

[DETAIL] **The matrix job keeps its shape with one leg.** The summary check
`verify` and the ruleset's required check stay unchanged; restructuring the
generator would be work this change does not need.

[DETAIL] **The ruff target moves to `py312`.** It names the oldest interpreter
the code must run on; measured with no new finding (`research.md`,
amendment).

[DETAIL] **The lock is not regenerated.** It carries no interpreter marker and
already installs on 3.12 in CI and in `make venv` (`research.md`, amendment).

[DETAIL] **Sample lists in tests keep `3.11`.** Where a test feeds the schema
or the lock check an invented interpreter list, 3.11 is data, not a claim
about this repository; rewriting it would change nothing the tests show.

[DETAIL] **`tools/cloud-env/` is not touched.** It installs lakeswitch's
interpreter, which changes with lakeswitch-ai-6sj.
