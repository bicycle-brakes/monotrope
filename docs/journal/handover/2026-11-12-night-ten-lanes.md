---
title: "Session handover — night run with ten lanes, 2026-11-12"
category: handover
created: 2026-11-12
updated: 2026-11-12
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-11-12"
tags: [handover, night-run, lanes, make-verify, review-loop, beads]
target_ref: 5d70a6aa
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

Written at about 05:10 UTC on 2026-11-12 by the orchestrating session that
ran the night of 2026-11-11/12 (run id `2026-11-11-a`, state folder
`~/.local/state/coding-harness/night/2026-11-11-a/`; the measured record is
its `lane-watch.log`, the tracker cleanup record its `grooming.md`). It
follows the day handover of 2026-11-11 (pull request #370, not merged at
05:06 UTC), which stays unchanged.

## Where we are

The maintainer asked at about 20:40 UTC for a night with ten lanes, at most
three runner jobs that run `make verify` at once (plan: pull request #371), and
added two lanes later: an isolated measurement of the test suite and a pass
over the tracker. Four changes reached a pull request: the midnight stamp
test (#372), cheap gates first (#373, a decision pull request), the
45-minute step limit (#374) and the night plan (#371). Six lanes parked, each
with one question in its bead. Nothing was merged in the night; `main` is at
`5d70a6aa` (05:06 UTC), and its push CI is red on a flaky test (see
"Validation").

## Next step

Put the questions under "Needed from the maintainer" to the maintainer from
the top, one at a time with their context, after the merge decisions on
#372, #373 and #374.

## Needed from the maintainer

1. **Merge #372, #373, #374** (all `CLEAN` at 05:06 UTC). #373 is a decision
   pull request: merging it makes the cheap-first gate order binding
   (`decisions/gates.yaml` version 3). Its lane used about 10 h of a 3 h
   appetite; the overrun was known on 2026-11-11 and is stated in the pull
   request. Recommended: merge #374 first (it raises the limit the others
   need), then #373, then #372.
2. **Two CI runs stuck in the queue since 20:45/20:52 UTC**: the merge-queue
   run of #370 and the pull-request run of #371 stayed `queued` all night
   while #372's run went through at 22:23 UTC. Recommended: cancel and rerun
   both (a maintainer action; the night avoided `gh api`).
3. **targeted-check-more-verbs** (bead coding-harness-0swp): three implement
   attempts converged to 3 red tests (72, 14, 3); 4.2 h of 6 h used. The last
   attempt's code is saved on
   `refs/stage2/attempts/targeted-check-more-verbs/implement-attempt-3-20261112T010735Z`
   and is still in the worktree. Recommended: A — one more run from that state
   with the three failures in its brief, inside the 1.8 h left.
4. **origin-check-across-blocks** (bead coding-harness-3h96): the repair to
   answer A failed three times on the same 3 tests; the new duplicate-id
   refusal most likely fires on a phase-6 re-check whose tables repeat ids.
   Recommended: A — uniqueness per block kind (loop and released rows apart
   from phase-6 tables). Code saved on
   `refs/stage2/attempts/origin-check-across-blocks/repair-attempt-3-20261112T010733Z`.
5. **explore-provenance** (bead coding-harness-g19n): the re-check found
   EP6-13 (a post-adoption date inside the legacy producer spelling is
   ignored) and EP6-14 (a recursive YAML alias aborts the scan) — further
   cases of two mechanisms. Recommended: A — repair at the mechanism (one
   helper reads every date in the producer block; each file's header reading
   is wrapped so any error is reported for that file and the scan goes on).
6. **swarm-report-format** (bead coding-harness-4q9y): two repair runs could
   not prove rows L1-1 and L1-2 (first stopped by the 5-minute tool limit
   under load, then the red-first tests passed on the old code).
   Recommended: A — reject both as not reproduced and end the loop.
7. **verify-tmp-cleanup** (bead coding-harness-bxxt.3): three implement
   attempts failed on the change's own new tests; one attempt grew
   `scripts/verify_lock.py` by 606 lines. Recommended: A — re-plan smaller
   (first slice: one run-specific pytest temporary folder that
   `verify_all.sh` removes on exit; orphan recovery later).
8. **verify-slots** (bead coding-harness-u1ha): the boundary repair went
   green alone at the lock, but review round 4 gave 9 rows, one BLOCKER (the
   serial-versus-paired trial of criterion 11 is still "Pending"). Appetite
   long spent. Question: does the lane continue (a real paired trial of about
   30 minutes with the machine otherwise idle, then hand fixes of 8
   documentation rows)?
9. **no-work-ledger-marker** (bead coding-harness-twbl): implemented
   (`92dd557d`, Sonnet 5.5 on attempt 3, 69 min of 2 h), but its review loop
   wrote no round twice — the only free reviewer first truncated its answer,
   then hit the 45-minute round limit, and the loop cannot leave the free
   stage. Needed: bead coding-harness-1gzo (free and Flash reviewers in one
   round) first, or a phase-6-only path for this bounded change (bead
   coding-harness-fctf).
10. **central-config** (bead coding-harness-twvx): the redraft was not
    started — answer A names no accepted downside, and the draft refuses a
    record without one. Proposal in the bead notes.
11. **Tracker proposals** from the cleanup pass, listed in
    "Decisions and preferences" below under "Tracker"; none was carried out.

## Decisions and preferences

Given by the maintainer on 2026-11-11 evening; recorded in the bead notes
named. Not to be asked again.

- **Ten lanes tonight**, widening the six-lane limit of the day; at most three
  verify-bearing runner jobs at once (night plan, #371).
- **Plan cards approved unchanged**: targeted-check-more-verbs, verify-tmp-cleanup,
  no-work-ledger-marker, verify-step-limit.
- **verify-step-limit is stage 1 only**: 45 minutes; the central value goes to
  bead coding-harness-twvx, the measured default to a follow-up
  (`plans/changes/verify-step-limit/decisions.md` Q-1).
- **Every plan card explains in plain words what the change does** — the
  problem with one example, what changes, the main risk (maintainer: "das muss
  jetzt immer in die plankarte"; bead coding-harness-kg8n). Until it lands, the
  orchestrator adds this by hand to every card it shows.
- **Lane 11 (test-suite measurement) and lane 12 (tracker pass)** added by the
  maintainer. Tracker rule used: close only clear cases with a reason, list
  everything else as a proposal.

Tracker, carried out tonight (every change carries its reason in the bead):

- 21 claims released, in progress -> open, no activity and not a lane:
  coding-harness-9ycy, -c99h, -uxa9, -mfth, -k93f, -p3xq, -xul8, -ut8q, -1gzo,
  -3g53, -680l, -6ie, -3ar, -2ym2, -cjf9, -8v2c.1, -tlr4, -bvy, -788, -t83,
  -363r.1.
- P2 -> P1: the pytest speed-up (coding-harness-dca4), the midnight flake
  (coding-harness-bxxt.5), the cache of the non-pytest gates
  (coding-harness-43iz), the main-CI flake (coding-harness-yb1l).
- Closed: the ADR 0016 document-check wording, merged in `d5645b01`
  (coding-harness-v9xx); a duplicate flake bead opened tonight
  (coding-harness-9pib, into coding-harness-yb1l).
- Opened: the plan-card explanation line (coding-harness-kg8n).

Tracker, proposed only (not done):

- Fold the commit-keyed gate cache (coding-harness-43iz) into the content-keyed
  reuse of a green run (coding-harness-bxxt.2).
- One change for saving and isolating runner attempts: coding-harness-c99h,
  -t3s3, -s9r, -znc, -6ie.
- Fold the implement route and model registry (coding-harness-9ycy, -aygo,
  -wq1m) into the central configuration (coding-harness-twvx).
- About 70 open P1 beads (2026-11-11): P1 no longer separates. Proposal: P1
  only for the verify-speed epic (coding-harness-bxxt) and the active lanes.
- Close or re-date "try the ultra review this week" (coding-harness-8j7, from
  2026-10-19); narrow the Monotrope rename (coding-harness-fjr; the GitHub
  owner part is done); defer the untouched P4 group of 2026-10-28 as a block.

## Open work and blockers

Task status stays in the tracker. Lanes at 05:06 UTC:

| Lane | Bead | State |
|---|---|---|
| verify-step-limit | coding-harness-xkvr | done — #374 |
| verify-cheap-first | coding-harness-bxxt.1 | done — #373 (decision) |
| midnight-stamp-test | coding-harness-bxxt.5 | done — #372 |
| night plan | — | #371, CI stuck |
| explore-provenance | coding-harness-g19n | parked — question 5 |
| targeted-check-more-verbs | coding-harness-0swp | parked — question 3 |
| swarm-report-format | coding-harness-4q9y | parked — question 6 |
| origin-check-across-blocks | coding-harness-3h96 | parked — question 4 |
| verify-slots | coding-harness-u1ha | parked — question 8 |
| central-config | coding-harness-twvx | not started — question 10 |
| verify-tmp-cleanup | coding-harness-bxxt.3 | parked — question 7 |
| no-work-ledger-marker | coding-harness-twbl | parked — question 9 |
| test-suite measurement | coding-harness-dca4 | done — result in the bead notes |
| tracker pass | — | done — see above |

What the night showed:

- **The free review stage blocks small changes.** For three changes the only
  free reviewer either found nothing (the loop ends with no Flash reviewer
  having read the change) or failed (truncated answer, 45-minute round limit),
  and a failed free round writes no round, so the loop cannot move on.
  Bead coding-harness-1gzo is the fix.
- **The runner's 5-minute tool limit** stops the targeted pytest run under
  load (swarm-report-format, load about 13 on 8 cores). The 45-minute change
  does not cover it.
- **pytest has more than doubled in two weeks**: see "Validation".

## Working state and parallel-session boundary

- One session; it was the tracker writer. No other session was reported
  (session scan, 05:06 UTC).
- `main` at `5d70a6aa`. The main checkout has the untracked `.codex/agents/`,
  untouched.
- Lane heads (pushed): fix/verify-step-limit `e6dde20c` (#374), fix/verify-cheap-first
  `b5c581d6` (#373), fix/midnight-stamp-test (#372), fix/explore-provenance
  `da59811e`, feat/targeted-check-more-verbs `d7307131`, fix/swarm-report-format
  `621312ff`, fix/origin-check-across-blocks `b81316d5`, feat/verify-slots
  `68d4e5c1`, fix/verify-tmp-cleanup `1b5309db`, fix/no-work-ledger-marker
  `a907bfe3`.
- **Uncommitted attempt code** (saved on the side refs above, not committed to
  the branch on purpose, so a later red-first proof runs on the code without
  the fix): worktrees targeted-check-more-verbs and origin-check-across-blocks.
- Loop records edited by the orchestrator tonight have a backup beside them
  (`loop.md.bak-2026-11-11`): verify-cheap-first, swarm-report-format,
  origin-check-across-blocks.
- Keep-awake (`caffeinate`) runs until 07:00 UTC; the 30-minute wake is a
  background job of this session.

## Validation

- Phase 6 (Codex), no finding, each after a full `make verify` green on its
  head: midnight-stamp-test (2026-11-11), verify-cheap-first and
  verify-step-limit (2026-11-12).
- After merging `origin/main` into each pull-request branch, targeted tests
  green: 51 (#372), 234 (#373), 72 (#374), between 21:45 and 00:45 UTC.
- **Test-suite measurement** (2026-11-12 01:08–01:34 UTC, alone at the lock,
  load about 5, `main` `5d70a6aa` plus the tests-only #374 change,
  `--durations=60`): pytest 5604 passed, 17 skipped, 1 failed in 1270 s
  (2026-10-28: 4082 passed in 520 s). The 60 slowest calls sum to 792 s, 35 of
  them in `tests/test_stage2_swarm.py` (438 s). The one failure,
  `tests/test_machine_facts.py::test_snapshot_is_local_and_read_only`, was not
  seen in the night's other full runs; not read further. Details in bead
  coding-harness-dca4.
- **main's push CI is red** after #369 (run 43062892770, 2026-11-11 16:54 UTC)
  and was red after #367 (run 42914422313), both on the flaky
  `tests/test_stage2_swarm.py::test_a_refused_run_is_printed_before_any_model_call`
  (`assert 2 == 0`); green in between (bead coding-harness-yb1l).
- Not run: a full `make verify` on `main`; CI of #371 (stuck).
