---
title: "Decisions — targeted-check-more-verbs"
category: decisions
status: draft
implementation_status: none
date: 2026-11-11
created: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-11
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

## Decided by the agent

None yet.
