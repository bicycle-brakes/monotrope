---
title: "Session handover — night run with twelve lanes, 2026-11-11"
category: handover
created: 2026-11-11
updated: 2026-11-11
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Fable 5, 2026-11-11"
tags: [handover, night-run, lanes, make-verify, review-loop, stage-2]
target_ref: 0e7961e8
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

Written between 06:15 and 08:15 UTC on 2026-11-11 by the orchestrating session, which ran
the day of 2026-11-10 and the night after it without a restart. The measured
record is `~/.local/state/coding-harness/night/2026-11-08-a/lane-watch.log`.

## Where we are

On 2026-11-10 the maintainer merged eight pull requests (#359 to #365 and
#367) and closed #366; no pull request is open at 06:11 UTC. In the evening
the maintainer set the speed-up of the full check (`make verify`) as first
priority and widened the night from six to ten, then twelve lanes. Twelve
changes moved; none reached a pull request in the night, because every step
queues at the one verify slot: twelve full checks started between 22:00 and
06:04 UTC, their median wait was 96 minutes and the longest 147 minutes.
The first full check in the new cheap-first order is green
(verify-cheap-first, 2026-11-11). Two jobs run at 08:15 UTC (see "Working
state"). Eight changes wait for the maintainer.

## Next step

Read the two running jobs first: review round 1 of verify-cheap-first and
the repair of decision-statement-skeleton. Then put the questions under
"Needed from the maintainer" to the maintainer from the top, one at a time,
each with its context.

## Needed from the maintainer

In the order that frees the most work. Every question stands with its
context in the notes of the bead named.

1. **verify-slots** (two full checks at once, bead coding-harness-u1ha).
   Review round 3 found two more faults where two admissions overlap in one
   process. Recommended: a Boundary "one admission per process; a second one
   is refused" instead of a further repair. Second question: may the plan
   record that the appetite (4 h) was passed about three times over and that
   the change went on because the verify speed-up was made first priority?
2. **Plan cards, veto or go**, each with a skipped interview to confirm:
   verify-tmp-cleanup (bead coding-harness-bxxt.3, appetite 4 h),
   no-work-ledger-marker (bead coding-harness-twbl, 2 h),
   midnight-stamp-test (bead coding-harness-bxxt.5, 2 h).
3. **targeted-check-more-verbs** (bead coding-harness-0swp): the interview,
   five questions, because it amends ADR 0025. The quickest gain is question
   2: may the 30-second documents job of a draft run outside the verify lock?
   It waited between 46 and 152 minutes in the night.
4. **swarm-report-format** (bead coding-harness-4q9y): the one free reviewer
   reached its output limit twice. May the review loop of this change start
   at the Flash round?
5. **origin-check-across-blocks** (bead coding-harness-3h96): fourth finding
   on how the refusal names a block. Recommended: a Boundary that narrows the
   promise to the row id and its place.
6. **central-config** (bead coding-harness-twvx): four implement attempts
   failed; the fourth broke 23 existing tests around repair prompts.
   Recommended: redraft the plan so the placeholder is filled outside the
   shared prompt snapshot.
7. **explore-provenance** (bead coding-harness-g19n): its sixth phase-6
   pass could not start — the Codex call ended with exit 1 at about 07:00
   UTC, as two repair calls did in the night (the full check before it was
   green at `478404c0`). Is Codex out of budget, and may phase 6 run on
   Opus 5.5 meanwhile?
8. **review-fewer-rounds** (bead coding-harness-3rtn): the spec review left
   21 rows; eleven are ambiguities for the maintainer. Its implementation
   also waits for central-config.

## Decisions and preferences

Given by the maintainer on 2026-11-10 and recorded where named; not to be
asked again.

- The speed-up of the full check comes first ("so schnell wie möglich").
- verify-cheap-first: every gate declares a cost class in the one gate list;
  the mechanism sorts and stops early; it must hold in kit repositories
  (`plans/changes/verify-cheap-first/decisions.md`, Q-1). Plan card: go.
- swarm-report-format: five interview answers; the invocation ceiling of the
  research swarm may rise to `72 + 6N` (its `decisions.md`). Plan card: go.
- explore-provenance: the census gets an adoption day (its `decisions.md`,
  Q-5).
- triage-verb: a Boundary for the spellings of a `Where` cell; structured
  finding locations are separate work (bead coding-harness-k7tv).
- review-fewer-rounds: the fifteen check questions hold; the free second
  round is a team of three; a small change always gets one (Q-13 to Q-15).
- decision-statement-skeleton: one more hour, the orchestrator writes the
  interview prompt text and its two tests (done, `47271bce`).
- origin-check-across-blocks: go on with the review loop despite the spent
  appetite.
- The note "wait for the testing-strategy report" is lifted from bead
  coding-harness-0swp.
- Plan cards given a go on 2026-11-10: origin-check-across-blocks,
  decision-statement-skeleton, central-config, swarm-report-format,
  verify-cheap-first.

## Open work and blockers

Task status stays in the tracker; this lists where each lane stands.

| Change (bead) | State at 06:15 UTC |
|---|---|
| verify-cheap-first (coding-harness-bxxt.1) | Runner attempt accepted (`19b3e1c3`); orchestrator bootstrap done by hand as planned: gate list on schema 3 with a cost per gate, version-2 reading removed, fixtures migrated (`d289afcd`); full check green in the new order (1515 s after 2795 s of waiting); review round 1 running |
| verify-slots (coding-harness-u1ha) | Two repair rounds accepted (`bb1c93ca`); round 3 not triaged; parked on question 1 |
| explore-provenance (coding-harness-g19n) | Repair of EP6-9 and EP6-10 accepted (`478404c0`), full check green; the phase-6 reviewer call failed (Codex, exit 1); parked on question 7 |
| decision-statement-skeleton (coding-harness-nr6h) | Accepted by hand; round 1 repaired; round 2 repair failed five times on other grounds — two failed Codex calls, and three full checks red on the stamp gate alone because the orchestrator edited `decisions.md` after local midnight without moving its stamp (corrected, `chore` commit of 2026-11-11); rerun on the fallback route running |
| origin-check-across-blocks (coding-harness-3h96) | Two repair rounds accepted (`a3a1a9d0`); round 3 not triaged; parked on question 5 |
| swarm-report-format (coding-harness-4q9y) | Accepted by hand after a green full check (`f5c76774`); review loop cannot pass its free round; parked on question 4. The orchestrator's plan step (WORKFLOW wording, a live explore as proof) is not done |
| central-config (coding-harness-twvx) | Four attempts kept as work in progress (`011de833`); parked on question 6 |
| review-fewer-rounds (coding-harness-3rtn) | Redraft with ADR draft 0027 (`07cf56c8`), spec review recorded (`1ddb0b26`); parked on question 7 |
| targeted-check-more-verbs (coding-harness-0swp) | Explored (`11860cb1`); parked for the interview |
| verify-tmp-cleanup (coding-harness-bxxt.3) | Draft committed (`e6894adc`); plan card waits |
| no-work-ledger-marker (coding-harness-twbl) | Draft committed (`00d3a67e`); plan card waits |
| midnight-stamp-test (coding-harness-bxxt.5) | Draft committed (`e3a7083a`); plan card waits |

The measurement of the slowest tests (bead coding-harness-dca4, step 1) is
in the bead's notes: one run of the suite at `be39e01d` took 1069 s; the
sixty slowest tests are mostly research-swarm tests (700 s summed over 35
listed tests) and Pi contract tests (243 s over 7).

## Working state and parallel-session boundary

- One session orchestrated everything; it is the tracker writer. The start
  hook once reported a second session in the review-fewer-rounds worktree
  while the runner's spec review ran there; whether that was the runner's own
  model call was not checked.
- `main` is at `0e7961e8` (2026-11-11 06:11 UTC). No pull request is open.
- Every lane has its worktree under `.claude/worktrees/<change>` and its
  branch pushed: feat/verify-slots `d2ef1846`, fix/verify-cheap-first
  `d289afcd`, fix/explore-provenance (head moved after `478404c0` by one
  record commit),
  fix/origin-check-across-blocks `04fdc68e`,
  feat/decision-statement-skeleton (head moved after `2693c699` by one
  stamp commit), feat/review-fewer-rounds
  `1ddb0b26`, fix/swarm-report-format `de99840e`, feat/central-config
  `011de833`, feat/targeted-check-more-verbs `11860cb1`,
  fix/verify-tmp-cleanup `e6894adc`, fix/no-work-ledger-marker `00d3a67e`,
  fix/midnight-stamp-test `e3a7083a`.
- Running at 08:15 UTC, started by this session: `stage2.py review-loop
  verify-cheap-first` and `stage2.py --stage2-off … repair
  decision-statement-skeleton`. Their worktrees are not to be touched while
  they run.
- A session cron (minute 17 and 47) and a keep-awake process run only while
  this session lives.
- Seven clean worktrees of merged branches were removed on 2026-11-10; 11 GiB
  were free at 06:03 UTC.

Hand interventions counted per change: verify-slots 2 (draft and
implementation accepted by hand); decision-statement-skeleton 2 (acceptance,
one corrected answer line) beside the planned prompt edit;
swarm-report-format 1 (acceptance); explore-provenance 3, the third asked
before (the adoption-day boundary); verify-cheap-first none beside the
planned bootstrap.

## Validation

Measured from the local run log unless said otherwise.

- Full checks started from 2026-11-10 22:00 to 2026-11-11 06:04 UTC: twelve.
  Green: verify-slots 22:49, swarm-report-format 00:10,
  origin-check-across-blocks about 02:10, explore-provenance about 03:05,
  verify-cheap-first about 03:30. Red: origin-check-across-blocks 23:15 and
  explore-provenance 23:42 (both only the stamp gate after local midnight),
  central-config 00:37 (23 failed tests), verify-cheap-first about 01:05
  (one test), decision-statement-skeleton about 01:45 (the stamp gate),
  explore-provenance about 02:36. One was still running.
- verify-cheap-first at `d289afcd`: schema check and CI-derivation check
  green, 252 targeted tests passed, and the full check green — VERIFY GREEN,
  1515 s of execution (2026-11-11, ended before 07:49 UTC). It is the first
  full check that ran every seconds gate before the test gate.
- Not run: any check on `main` itself; the live research-swarm run that
  swarm-report-format owes.

What the night showed:

- More lanes did not mean more results. Waits at the verify slot grew from
  35 to 147 minutes; a draft waited up to 152 minutes for a documents job of
  30 seconds.
- A repair of a change that touches `scripts/stage2.py` runs the full check,
  not a targeted one.
- A run whose documents were stamped before local midnight and checked after
  it fails the stamp gate after the whole test gate has run; three runs were
  lost to it (noted on bead coding-harness-bxxt.5). A hand edit after
  midnight that does not move the stamp does the same: it cost
  decision-statement-skeleton three more runs.
- The session did nothing from about 03:05 to 06:03 UTC and again from
  about 06:15 to 07:49 UTC although the cron was set; two runner calls to Claude and Codex failed with exit 1 between
  01:01 and 02:39 UTC. The cause was not read; a usage limit is the guess.
- A missing Pi in a worktree, a plan ledger that named tests on a held path,
  and the runner's 30-minute step limit each cost a change its attempts on
  2026-11-10; none was a fault of the code under test.
- The sub-agent that synced a branch wrote the `Closes-Bead` line into a
  paragraph before the attribution lines; git does not read it as a trailer
  there and the bead had to be closed by hand.
