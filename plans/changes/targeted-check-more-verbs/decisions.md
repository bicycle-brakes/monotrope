---
title: "Decisions — targeted-check-more-verbs"
category: decisions
status: draft
implementation_status: none
date: 2026-11-11
created: 2026-11-11
last_reviewed: 2026-11-12
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-0swp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, make-verify, targeted-check, adr-0025]
---

# targeted-check-more-verbs — Decisions

Class: bounded (bead coding-harness-0swp), amending ADR 0025 (targeted check
after a repair), so five answered questions are owed. The maintainer answered
all five in the orchestrating conversation on 2026-11-11 by dialog choice;
each record carries the context the dialog showed. For question 4 the
maintainer first asked for the long-term, efficient solution; the record
holds the answer to the question as asked again with that solution.

## Q-1 · Whether implement and draft use the targeted check

asked: 2026-11-11
answer: Yes, with two gates — implement attempts and the draft post-check use the targeted check; the full check stays before phase 6 and in CI.
answered_by: maintainer
status: answered
context: |
  Topic: whether implement attempts and the draft post-check may use the targeted check instead of the full one.
  Intention: ADR 0025 allows the targeted check (only the tests linked to the changed files) after a repair alone; every implement attempt and draft post-check runs the full check of about 25 minutes plus its wait. The neighbour report of 2026-11-09 counted 151 full runs with 77 hours of wait in five and a half days.
  Today: repair targeted; implement, draft, phase 6 and CI full.
  Repository change: ADR 0025 is amended; scripts/stage2.py routes implement and the draft post-check to the targeted selection; the full check stays before phase 6 and in CI.
  Architecture change: the full check moves from every step to two fixed gates — before the review and before the merge.

In the context of implement attempts and draft post-checks that each wait
for a full check, facing waits of one to two hours per step, we decided that
both use the targeted check while the full check stays before phase 6 and in
CI, to achieve that each step is checked fully once before it is judged or
merged without paying for every intermediate run, accepting that a fault
outside the targeted selection surfaces only before phase 6 and then costs
one more attempt — 2026-11-11

## Q-2 · Whether the draft's documents job needs the verify lock

asked: 2026-11-11
answer: No — the documents job of a draft (text checks only, no tests) runs without the verify lock.
answered_by: maintainer
status: answered
context: |
  Topic: whether the short documents check of a draft may run outside the verify-slot lock.
  Intention: in the night of 2026-11-10 to 11 a draft waited up to 152 minutes for a documents check of about 30 seconds, because it queues at the one lock meant for the 25-minute runs.
  Today: every run, the documents job included, takes the one verify slot; the lock guards against too many memory-hungry runs at once.
  Repository change: the documents job runs without the lock, or gets a small slot of its own, or stays as it is.
  Architecture change: admission separates light checks from heavy ones; ADR 0025 records it.

In the context of a draft whose documents check takes seconds but waits for
hours, facing one machine-wide lock built for the full check, we decided that
the documents job runs without the lock, to achieve that a draft is checked
when it is written, accepting that nothing bounds how many documents jobs run
at once and that a future heavy documents gate would run unlocked unless its
cost class is checked — 2026-11-11

## Q-3 · How a change touching scripts/stage2.py is checked

asked: 2026-11-11
answer: The full check stays for any change touching scripts/stage2.py until bead coding-harness-vg9 splits the file.
answered_by: maintainer
status: answered
context: |
  Topic: what happens when a change touches the central runner script scripts/stage2.py.
  Intention: today such a change always falls back to the full check — the script is shared infrastructure, its test file alone exceeds the five-minute bound of the targeted check (250 s for its 13 slowest tests), and much depends on it; many changes touch it.
  Today: scripts/stage2.py changed means a full check; bead coding-harness-vg9 (split it into runner modules) is open, not started.
  Repository change: keep the fallback until the split, or raise the bound for this file and run only tests/test_stage2.py.
  Architecture change: raising the bound would loosen the rule that shared infrastructure is always checked fully, for one file.

In the context of a runner script on which every lane depends, facing a test
file that alone exceeds the targeted bound, we decided that a change touching
scripts/stage2.py keeps the full check until the file is split, to achieve
that a runner fault cannot reach the other lanes through a narrow check,
accepting that runner changes stay the most expensive steps until the split
— 2026-11-11

## Q-4 · What happens to new code without a linked test

asked: 2026-11-11
answer: Refuse at once, following import chains — an implement attempt whose new code is linked to no test, directly or through a chain of imports, is refused in seconds with the instruction to write the test; coverage measurement is not used.
answered_by: maintainer
status: answered
context: |
  Topic: what to do, lastingly and cheaply, when new code has no linked test.
  Intention: the targeted check selects tests through links derived from text (scripts/touch_map.py: a test that imports or names a file belongs to it); a new file without such a link means code without a test or code tested only through an importer. Whether the selection follows import chains today was not read.
  Today: for a repair, a missing link falls back to the full check — 25 minutes plus its wait.
  Repository change: scripts/stage2.py (selection and refusal) and its tests; coverage measurement would add a dependency.
  Architecture change: "new code brings its test" becomes a duty the runner enforces.

In the context of implement attempts that may add code no test reaches,
facing a fallback that finds this only after a full check, we decided that
such an attempt is refused at once unless a test reaches the code directly or
through a chain of imports, to achieve that a missing test costs seconds and
a retry instead of a full check, accepting one extra attempt whenever the
model forgets the test and new selection code for following import chains
— 2026-11-11

## Q-5 · Who measures faults the targeted check lets through

asked: 2026-11-11
answer: The runner records every slip automatically in the local run log, and the night handover names the count.
answered_by: maintainer
status: answered
context: |
  Topic: who counts faults a targeted check let through, and where it is written.
  Intention: ADR 0025 point 4 requires measuring slips — a fault the targeted check called green that only the full check before phase 6 or CI found; no result of that measurement was found in the tree. With these answers far more steps are checked narrowly.
  Today: every full check writes its verdict and duration to a local log (verify-duration.jsonl); whether it was red after a green targeted check of the same tree is not recorded.
  Repository change: the runner records the slip with its red tests in the same log and the night handover names the count; or a hand count in findings.md; or no measurement.
  Architecture change: one field more in the run log, no new service.

In the context of a targeted check that will cover most steps, facing a
measurement duty nobody carries out, we decided that the runner records each
slip automatically in the local run log and the night handover names the
count, to achieve that a rising slip rate is seen without a dashboard,
accepting more runner code and a count that is local to one machine and
leaves CI finds out — 2026-11-11

## Q-6 · Where the runner writes the check scope

asked: 2026-11-12
answer: "A: Lauf mit Entwurfskorrektur (Empfohlen)" — the check scope is written into a line the runner writes anyway; the extra quote block after every attempt goes. The one test that encodes the old rule is rewritten to the new rule, three test fixtures are adapted, the ruff start on a text-only attempt is explained or repaired, and the appetite rises to 7.5 hours.
answered_by: maintainer
status: answered
context: |
  Topic: the change targeted-check-more-verbs (bead coding-harness-0swp), the runner checks only what an implement or draft attempt touched.
  Intention: the fourth implement run was rejected with 13 red tests in the full check; the maintainer asked whether those older tests are still relevant. Twelve are, one is superseded.
  Today: eight of them guard that a passing attempt leaves only its audit line in findings.md and a failed one exactly one diagnostics block; the attempts' code writes an extra block "Runner verification scope" after every attempt, which the spec does not mention. 5.2 of 6 hours are used.
  Repository change: a fifth implement run from the saved state with that correction; one sentence in spec criterion 8 and one plan step.
  Architecture change: none.

In the context of a targeted check whose scope must be visible afterwards,
facing an extra block in findings.md that breaks the standing guarantee of
one audit line per passing attempt and one diagnostics block per failed one,
we decided that the runner writes the scope into lines it writes anyway and
adds no block, to achieve the evidence of criterion 8 without growing
findings.md by a block per attempt, accepting a longer time line in plan.md
and an appetite raised from 6 to 7.5 hours — 2026-11-12

## Q-7 · Appetite for the review loop

asked: 2026-11-12
answer: "a" — option A: the appetite rises by three hours to ten and a half; the review loop starts when the verify lock has a free place.
answered_by: maintainer
status: answered
context: |
  Topic: the time budget of the change targeted-check-more-verbs (bead coding-harness-0swp).
  Intention: 7.4 of 7.5 hours are used; the review loop starts with a full make verify of about 25 minutes of its own and passes the limit for certain.
  Today: the implementation is accepted at 2c561a88 with a green full make verify; about 1.6 of the 7.4 hours were waiting at the verify lock.
  Repository change: the appetite figure in plan.md and this entry.
  Architecture change: none.

In the context of an accepted implementation whose appetite is spent,
facing a review loop that cannot fit into the remaining six minutes,
we decided to raise the appetite from 7.5 to 10.5 hours,
to achieve a looped review before phase 6,
accepting three more hours on a change planned at six — 2026-11-12

## Q-8 · How the change goes on without a working free review round

asked: 2026-11-12
answer: "A" — option A: straight to phase 6, once the Omnigent list repair (pull request 379) is merged; the pull request names the skipped review loop.
answered_by: maintainer
status: answered
context: |
  Topic: the change targeted-check-more-verbs (bead coding-harness-0swp) and its review loop.
  Intention: the loop failed twice in round 1 on 2026-11-12; the only free model, longcat-2.5-free, cuts its answer at its output limit each time.
  Today: the runner then writes no round and cannot retire the stage (no stage snapshot); this is the known fault of bead coding-harness-1gzo. For the change no-work-ledger-marker the maintainer decided the same case the same way today. About 7.5 of 10.5 hours are used.
  Repository change: none in code; the pull request names the skipped loop.
  Architecture change: none.

In the context of a review loop whose first stage cannot complete,
facing a free model that truncates every answer and a runner that cannot retire the stage,
we decided to go straight to the phase-6 review,
to achieve a reviewed change without waiting days for the loop repair,
accepting that no swarm round read this change — 2026-11-12

## Decided by the agent

[DETAIL] **The scope of a passing attempt goes into the runner's time line in
plan.md ("Time used"), not into the "Stage-2 call" audit line.** Reason: the
audit line is written when the call starts, before any check has run; the
time line is written after the verdict and is runner-owned already. A failed
attempt names the scope inside its one diagnostics block, as the repair route
does today. The run log (verify-duration.jsonl) keeps the scope as before.
