---
title: "Decisions — guard-test"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-0ho
class: feature
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, repair, red-first]
---

# A guard-test mark for test-only repairs — Decisions

Class: feature (proposed in the bead on 2026-10-27: a new mark that changes
how the repair verb accepts rows). The minimum is three counted answers, five
when the change edits an ADR file; five stand below.

## Where these answers come from

The five records below are copied verbatim from
`plans/changes/guard-test/decisions.md` on the branch `explore/guard-test`
at `1d6cd430` (last edited there on 2026-10-16). That branch is 1199 commits
behind `origin/main` at `5f57f4e9` and is dropped; this folder replaces it on
current main. Maintainer decision of 2026-10-29: spec and plan are redrafted
on current main, and the answers Q-1 to Q-5 stand without a new interview
(recorded in the notes of the beads "stage2 repair: red-first exception for
fixes that live only in test code" (coding-harness-0ho) and "stage2 repair: a
test-strength finding has no red-first form" (coding-harness-y17)).

The records still say "class bounded" in their own text where they were
written that way on 2026-10-15/16; the class is now feature, as above. The
maintainer settled on 2026-10-27 that this change also carries bead
coding-harness-y17 (test-strength rows); the third bead of that grouping,
coding-harness-a7m (pytest's DID NOT RAISE counts as red), is already closed
on main (`research.md`, "Refresh against main — 2026-10-29").

Before the interview, the maintainer chose way A in the conversation on
2026-10-15: a guard-test mark whose test plants the fault itself and must be
red with the planted fault and green without it (rejected: a runner-side
mutation check, an exception without proof), built before the implementation
of coding-harness-agx.

## Q-1 · How the runner tells "with fault" from "without fault"

asked: 2026-10-15
answer: "ja" — option A: the runner runs a guard test twice, once with the environment variable `STAGE2_PLANT_FAULT=1`, where it must be red, and once without, where it must be green; the test plants its fault only when the switch is set.
answered_by: maintainer
status: answered
context: |
  Topic: how the runner proves that a guard test really catches the fault it plants, without taking the model's word.
  Intention: the maintainer decided that a guard test plants the fault itself and must be red with it and green without; open was how the runner separates the two runs.
  Today: the runner runs the named test once on the baseline code and demands red; it reads the test file only to see that the function exists; hand-written guard tests of this kind exist (haiku-5-5), but the runner cannot use them as proof.
  Repository change: the repair answer form `fixed — guard test — tests/…::test_…`, `red_first` with two runs, the status words in the findings template, `prompts/04-implement.md`, `docs/WORKFLOW.md`. Options: A — a switch `STAGE2_PLANT_FAULT` (simple; a test that just fails under the switch without planting a real fault must be caught in phase 6; the runner checks only that the switch appears in the test); B — the line names the guarded function and the runner replaces it with one that finds nothing (stricter, but only for checker functions returning a list of problems).
  Architecture change: a second kind of proof beside "red on the baseline"; ADR 0017 gets a [DETAIL] note, no new ADR, because the principle "every finding needs a proof" stays.

In the context of repairs whose right fix is a test over code that is
already right, facing the choice between a switch the test reads and a
runner that disables a named function, we decided on the switch
`STAGE2_PLANT_FAULT` with one red run with it and one green run without, to
achieve a proof for guard tests that matches the maintainer's choice,
accepting that phase 6 must check that the switch plants a real fault. — 2026-10-15

## Q-2 · Who may book a repair as a guard test

asked: 2026-10-16
answer: "Nur markierte Zeilen" — option A: only a row the orchestrator took as `taken — guard test — <reason>` may be answered `fixed — guard test — tests/<path>::<function>`; the repairing model cannot choose the form for any other row.
answered_by: maintainer
status: answered
context: |
  Topic: who decides that a repair is a guard test, the orchestrator when it takes the row or the repairing model when it answers.
  Intention: the guard proof must not become a way for a model to avoid the red-first proof.
  Today: `fixed — not a test` is allowed only for a row the orchestrator took as `taken — not a test`; every code row needs a test that is red on the baseline code.
  Repository change: Options: A — a new taken form `taken — guard test — <reason>`, and the parser accepts the guard answer only for such rows (as for `not a test`); B — the model may choose the guard form for any taken row, and only phase 6 catches a misuse.
  Architecture change: part of the ADR 0017 addendum; no new ADR.

In the context of guard tests that prove a test-only repair, facing the
choice between an orchestrator mark and a free choice of the repairing model,
we decided that only a row taken as `taken — guard test` may be answered as a
guard test, to achieve that no model can sidestep the red-first proof,
accepting that a test-only row the orchestrator does not recognise at triage
fails its repair on the ordinary proof. — 2026-10-16

## Q-3 · How phase 6 checks a guard test

asked: 2026-10-16
answer: "Jeder Test, Pflicht" — option A: phase 6 reads every guard test and writes one line per test naming the real fault it plants and whether the test would catch that fault in the real code without the switch; a bare conditional failure is a BLOCKER.
answered_by: maintainer
status: answered
context: |
  Topic: how phase 6 confirms that a guard test plants a real fault.
  Intention: the runner proves only "red with the switch, green without"; a test that runs `assert False` under the switch passes that proof.
  Today: the spec's non-goals leave the meaning of the planted fault to phase 6, without saying how much of it phase 6 checks.
  Repository change: Options: A — every guard test is checked, one line each, a bare conditional failure is a BLOCKER (in `prompts/06-review.md` or its equivalent and `docs/WORKFLOW.md`); B — phase 6 samples guard tests at its own discretion.
  Architecture change: part of the ADR 0017 addendum; no new ADR.

In the context of a runner that cannot judge whether a planted fault is real,
facing the choice between a mandatory check of every guard test and a
sample, we decided that phase 6 checks every guard test and treats a bare
conditional failure as a BLOCKER, to achieve that no empty guard test
reaches main, accepting more review time per guard repair. — 2026-10-16

## Q-4 · Where the guard test applies

asked: 2026-10-16
answer: "Nur Reparatur" — option A: only `stage2.py repair` knows the guard form; phase 4 and the plan's criterion ledger keep their evidence rules; an extension would be a bead of its own.
answered_by: maintainer
status: answered
context: |
  Topic: whether the guard proof is limited to repairs of taken findings or also used in phase 4 and the criterion ledger.
  Intention: keep bead coding-harness-0ho bounded.
  Today: phase 4 and the criterion ledger have their own evidence rules; the three test-only failures of 2026-10-14/15 all came from repairs.
  Repository change: Options: A — repair only; B — also phase 4 and the criterion ledger (larger, closer to a feature).
  Architecture change: part of the ADR 0017 addendum; no new ADR.

In the context of the test-only repairs that failed the red-first proof,
facing the choice between a repair-only guard form and one for every phase,
we decided to limit the guard form to `stage2.py repair`, to achieve a
bounded change, accepting that phase 4 and the criterion ledger stay without
it until a bead of their own. — 2026-10-16

## Q-5 · What happens to the switch after the merge

asked: 2026-10-16
answer: "Bleibt, CI sichert ab" — option A: the planting branch stays in the guard test so the proof can be repeated later, and a gate in `make verify` fails when `STAGE2_PLANT_FAULT` is set in its environment, so a planted run never counts as a green verify.
answered_by: maintainer
status: answered
context: |
  Topic: whether the `STAGE2_PLANT_FAULT` branch stays in a merged guard test.
  Intention: keep the proof repeatable without letting a planted run pass as a green `make verify`.
  Today: neither `make verify` nor CI sets the switch; nothing stops a session that has it in its environment.
  Repository change: Options: A — the branch stays and a `make verify` gate refuses a set switch; B — the branch stays without a gate; C — the repair removes the branch after the proof (the runner would then check a second state).
  Architecture change: part of the ADR 0017 addendum; no new ADR.

In the context of guard tests that carry their own fault switch, facing the
choice between keeping the switch with a gate, keeping it without, and
removing it, we decided to keep it and to make `make verify` fail when the
switch is set, to achieve a repeatable proof that can never pass as a green
verify, accepting one more gate in `make verify`. — 2026-10-16
