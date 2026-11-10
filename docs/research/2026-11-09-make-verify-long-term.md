---
title: "make verify in the long run — what the run log says, what the bead structure misses, and an order of work"
category: research
created: 2026-11-09
updated: 2026-11-09
last_reviewed: 2026-11-09
owner: framework-architect
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-bxxt
tags: [verify, make-verify, lanes, test-strategy, proposal]
---

# make verify in the long run

**Result: the wait at the full check (`make verify`) is a demand problem, not
a lock problem. Since 2026-11-07 the lanes start 34 to 43 full checks a day,
each about 22 minutes long, on a machine that can run one at a time; in five
and a half days they waited 77 hours for 57 hours of execution. The work so
far tunes the queue (lock, order, slots). The lasting repair is to need the
full check about once per change, make that one run short, and run it where
parallel capacity is free (hosted CI). Most of the pieces already exist as
beads — but six of them are parked behind one research task that is itself
blocked.** Everything below is a proposal; nothing is implemented by this
note.

The maintainer asked for this on 2026-11-09 ("wie das Problem mit make verify
langfristig und nach best practice gelöst werden kann … was muss besser
gemacht werden").

## What was measured

Source: the run log the duration spike added
(`~/.local/state/coding-harness/verify-duration.jsonl`, bead
coding-harness-1um6), read on 2026-11-09 at 22:10 UTC. It covers
2026-11-04 13:13 UTC to 2026-11-09 21:42 UTC, one machine (Darwin arm64,
8 logical cores, 8 GiB — the machine figures are from bead coding-harness-351h,
not re-read today). Only the full job is counted (`job: verify`, 151 runs);
the 27 document-only runs are left out.

| Day (UTC) | Full runs | Green | Red | No end record | Wait, hours | Execution, hours | Median wait, min |
|---|---|---|---|---|---|---|---|
| 2026-11-04 (from 13:13) | 3 | 3 | 0 | 0 | 1.3 | 1.0 | 25 |
| 2026-11-05 | 7 | 7 | 0 | 0 | 1.2 | 2.5 | 15 |
| 2026-11-06 | 25 | 20 | 5 | 0 | 13.2 | 9.8 | 30 |
| 2026-11-07 | 39 | 30 | 9 | 0 | 21.4 | 14.2 | 30 |
| 2026-11-08 | 43 | 31 | 12 | 0 | 21.5 | 16.2 | 22 |
| 2026-11-09 (to 21:42) | 34 | 18 | 10 | 6 | 18.7 | 13.3 | 28 |
| **Sum** | **151** | **109** | **36** | **6** | **77.3** | **57.1** | 26 (all runs) |

Further readings from the same log:

- **Runs per change.** The 151 runs belong to 21 worktrees: median 7 full
  runs per worktree, 11 worktrees with 7 or more, the largest 19
  (`go-wire-apis`). A change that is checked seven times costs about two and
  a half hours of execution before any waiting.
- **Duration.** A green run took 1,230–1,250 s (median per day) on
  2026-11-04/05 and 1,374 s on 2026-11-09 — about 10 % more in five days.
  The pytest gate is about four fifths of it
  ([baseline note](2026-11-04-verify-duration-baseline.md)).
- **Growth.** `tests/*.py` held 13,168 lines on 2026-10-07, 66,501 on
  2026-11-07 (both from bead coding-harness-1ga5) and 73,080 lines in 77
  files at `01fb3e38` (2026-11-09). The full check took about 3 minutes on
  2026-10-14 (bead coding-harness-7so) and takes about 22 now. No gate holds
  either number.
- **Dirty trees.** 129 of 151 runs checked a tree with uncommitted changes
  (the runner checks an attempt before it commits). A result cache keyed by
  commit would therefore miss six runs of seven; a key has to come from the
  content.
- **Order of gates.** 11 red runs had a green pytest gate and failed on a
  cheap gate that ran after it (`frontmatter-current` eight times,
  `question-context` three times): 3.3 hours of test execution for a result a
  few seconds could have given.
- **Kit probe.** The `leerprobe` gate took 200 s (median) and 8.3 hours in
  total over the 151 runs.
- **Side effect, 2026-11-09 about 21:40 UTC.** The data volume ran full
  (1.0 GiB free). A test run outside the lock ended with "No space left on
  device" and 239 errors. Two finished runs had left 1.3 and 1.5 GiB of pytest
  temporary folders behind; the 91 worktrees hold 16 GiB. Removing the two
  stale folders gave 3.6 GiB free.

### What the figures say together

One slot at about 22 minutes can serve at most about 65 runs a day. The lanes
ask for 34 to 43, so the slot is busy about 60 % of the time, and arrivals
come in bursts (several lanes finish a repair in the same quarter hour). A
single server at that load makes waits of the size of a run — which is what
the log shows (median 22–30 minutes, maximum 90 minutes).

A second slot (bead coding-harness-u1ha, decided 2026-11-09) halves the load
per slot, but on this machine two runs share 8 cores and 8 GiB: three
concurrent runs once took more than 30 minutes each against 11–12 alone (bead
coding-harness-p6mu). Slots buy relief only as far as the machine has room.
They do not change the three numbers that set the cost: **runs per change,
seconds per run, and where a run executes.**

## How the approach is structured today

The theme is spread over the tracker like this (state read 2026-11-09):

| Where | Beads | State |
|---|---|---|
| Epic "Verify speed and machine load" (coding-harness-bxxt), P2, rank 8 of 15 | slow tests (dca4), hosted full check (u3qg), cache for non-test gates (43iz), hosted CI speed (7so), worker memory (351h), two flaky tests, noisy lint output | 1 of 9 closed |
| Epic "Lanes, night runs and orchestration" (coding-harness-bw73), P1 | admission order and wait alarm (ofmz), admission for all runner jobs (wpb0), disk check at admission (87b0) | open |
| Other epics or none, P1 | targeted check after implement and draft (0swp), fast pre-check (csm, in the runner-robustness epic yv9i), formalities gate (7ftj, in the night-run epic a6ns), two slots (u1ha), testing strategy (1ga5) | open |
| Loose, P2/P3 | kit probe only when kit files change (w2ay), coverage-based test selection (s3kf), shared fixture for swarm tests (wnka), wait time outside appetite (po0a), event log report (zaqf) | open |
| Closed | one run per machine (p6mu), worker cap (l7sc), xdist (d5a), docs-only check for draft (77qj), targeted check for repair (gxwg, 24ag), duration spike (1um6) | done |

## What has to be better

1. **The speed work is parked behind a blocked task.** On 2026-11-07 six
   beads (u3qg, 43iz, s3kf, w2ay, 351h, 7so) received the note "wait for the
   testing-strategy report" (coding-harness-1ga5). That report needs the
   research swarm, whose two runs on 2026-11-08 ended incomplete, and the
   repair of the swarm's report format (coding-harness-4q9y) is not drafted
   yet. So the cluster stands still while the load rose from 7 to about 40
   runs a day. Several parked pieces do not depend on the strategy question
   at all: they are backed by a measurement and easy to undo.
2. **The queue is managed; the demand is not.** Seven beads shape admission
   (one slot, worker cap, order, alarm, disk check, two slots, admission for
   all jobs). Only three reduce how often the full check runs (77qj and gxwg
   done, 0swp open) — and 0swp, the one covering implement attempts, has
   stood open at P1 since 2026-11-03.
3. **No target number.** There is a warning proposal for execution time
   (1,400 s, baseline note) but no budget for the suite, no limit on full
   runs per change, no target for the wait. Without one, every change adds
   tests and nothing pushes back; the suite grew fivefold in a month.
4. **No single ordered list.** The theme lives in four epics and several
   beads without one, with priorities from P1 to P3. The epic that carries the
   name is P2, while the wait it describes was the largest single cost of
   the last three nights.
5. **The log is written but not read.** The run log has every figure of this
   note. No report reads it, so the growth from 7 to 40 runs a day was seen
   as "lanes wait" and not as a number. Runs per change is not tracked
   anywhere.
6. **Cheap checks run last.** Inside one run the 17-minute test gate runs
   before the gates that take seconds.
7. **Housekeeping is missing.** Temporary test folders and merged worktrees
   pile up until the disk is full, which then fails runs for a reason no
   gate names.
8. **Stale claims.** Slow tests (dca4, claimed 2026-10-28, lease expired),
   the worker count record (xay1, claimed 2026-11-06, lease expired) and the
   fast pre-check (csm, claimed 2026-10-20, last updated 2026-11-01) show
   "in progress"; the list overstates what is moving.

## The target picture

This is the usual layering of checks in larger code bases — fast checks near
the edit, the full suite once before integration on shared infrastructure,
results reused when inputs did not change, a time budget that is enforced.
It is stated here from general knowledge; **no outside source was read for
this note** — the literature belongs to the testing-strategy research
(coding-harness-1ga5).

| Layer | When | Budget (proposal) | What runs | Where |
|---|---|---|---|---|
| 1 · Formalities | after every runner attempt, before anything else | seconds | formatter, linter, front matter, question context, registry | local, no lock |
| 2 · Targeted | after every implement, draft and repair attempt | under 2 minutes | the tests the change touches and names | local, no lock |
| 3 · Full | once per change before phase 6; again only when the tree changed | under 10 minutes of execution | every gate | hosted CI first; the local slots as fallback |
| 4 · Merge | on the pull request and in the merge queue | as layer 3 | every gate | hosted CI (today already) |

Four rules hold the picture together:

- **A full result is reused.** A green full check is recorded under a key
  made from the tree content, the gate file and the lock file. Phase 6, the
  orchestrator and a rerun ask for the key first. Today the review verb runs
  its own full check on a tree the orchestrator has just checked.
- **The suite has a budget.** A number for the full check (proposal: 10
  minutes of execution on this machine) and one per test (proposal: 5 s
  without a marker). A change that breaks the budget either speeds something
  up or moves tests into a slower, rarer layer — decided in the pull request,
  not silently.
- **Full runs per change are counted.** Target: three or fewer (attempt
  accepted, phase 6, pull request); today the median is seven.
- **Capacity comes from outside.** The repository is public, so hosted
  runs cost nothing and run side by side (bead coding-harness-u3qg). The
  local machine keeps layers 1 and 2, which need no lock.

## Proposed order of work

Ordered by effect per effort, from the figures above. Each step names the
bead that already holds it.

1. **Now, small and independent of the strategy research.**
   - Cheap gates before the test gate inside `make verify`, and stop at the
     first red blocking gate. No bead yet. Saves the 3.3 hours seen above and
     shortens every red run.
   - Clean up after a run: remove the run's own temporary folders; refuse
     admission under a free-disk bound (bead coding-harness-87b0, open).
   - Remove merged worktrees (the rule exists in `AGENTS.md`; 91 stand).
   - Two slots (bead coding-harness-u1ha) as decided — a stopgap, measured
     as its decisions record demands.
2. **Fewer full runs (the largest lever).**
   - Targeted check after implement and draft (bead coding-harness-0swp,
     P1). With the median of seven runs per change, moving the attempts to
     layer 2 removes most of the demand.
   - Reuse of a green full result by content key (extends bead
     coding-harness-43iz from "non-test gates per commit" to "the whole
     verdict per tree content").
   - Formalities fixed and checked before anything else (bead
     coding-harness-7ftj).
3. **A shorter full run.**
   - Shared fixture for the research-swarm tests (bead coding-harness-wnka):
     eleven of the twelve slowest tests are in that one file (baseline note).
   - Kit probe only when kit files changed, hosted CI keeps it always (bead
     coding-harness-w2ay): 200 s per run.
   - Worker memory measured, so the cap of four may rise (bead
     coding-harness-351h).
4. **Capacity outside the machine.**
   - Full check in hosted CI as the evidence for phase 6 (bead
     coding-harness-u3qg; its blocker, coding-harness-wkxm, is closed). It
     needs a workflow change, which is the maintainer's file.
5. **Hold the gain.**
   - Budget and test layers as a decision (the ADR proposal of bead
     coding-harness-1ga5), with a gate that fails when the budget is broken.
   - A weekly reading of the run log — runs per day, runs per change, wait,
     duration — in the handover (bead coding-harness-zaqf).
   - Coverage-based selection (bead coding-harness-s3kf) only if layer 2
     still misses tests after step 2.

Admission order and the wait alarm (bead coding-harness-ofmz) and a general
job admission (bead coding-harness-wpb0) stay useful for machine load, but
they lose urgency for the full check once steps 1 and 2 hold.

## Proposed tracker changes

Not made — the maintainer decides, then the orchestrating session writes
them:

1. One epic owns the theme: move 0swp, csm, 7ftj, u1ha, w2ay, wnka, s3kf,
   87b0 and ofmz under "Verify speed and machine load"
   (coding-harness-bxxt) and raise the epic to P1.
2. Lift the note "wait for the testing-strategy report" from w2ay, 43iz,
   351h and u3qg. The testing-strategy bead (1ga5) keeps the questions only
   it can answer: budget, layers, retiring tests, mutation check.
3. New beads: gate order with stop at the first red gate (bounded);
   reuse of the full verdict by content key (feature, or 43iz widened);
   cleanup of temporary test folders after a run (bounded).
4. State the target in the epic: three or fewer full runs per change, full
   check under 10 minutes of execution, median wait under 5 minutes.
5. Release the three expired claims (dca4, csm, xay1) or name who continues.

## Limits

- One machine, five and a half days, nights with five to six lanes; a day
  without lanes is not in the log.
- The log has no change name; "per change" is read from the worktree folder
  name, and a worktree that ran outside the lock (a second test run started
  by hand on 2026-11-09) is not in it.
- Six runs of 2026-11-09 have no end record (still running at the reading,
  or ended without one — not separated).
- Whether the 43 runs that repeated a worktree-and-commit pair checked an
  identical tree is not readable: the log records "dirty", not a content
  hash. The saving from verdict reuse is therefore not quantified.
- The budget numbers (10 minutes, 5 s, three runs) are proposals without a
  measurement behind them.
- Hosted CI duration was not re-read today (994 s for the suite on
  2026-11-07, from bead coding-harness-1ga5).
