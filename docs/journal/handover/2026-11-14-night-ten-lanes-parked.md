---
title: "Session handover — day and night of 2026-11-13/14, ten lanes, all parked or done"
category: handover
created: 2026-11-14
updated: 2026-11-14
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Fable 5.2 and Opus 5.5, 2026-11-14"
tags: [handover, night-run, lanes, make-verify, review-loop, stage-2]
target_ref: 2a07677a
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

Written at about 01:30 UTC on 2026-11-14 by the orchestrating session, which
ran the evening of 2026-11-13 and the night run 2026-11-13-a on the Mac mini
M6 (12 cores, 24 GiB). It follows the handover
`2026-11-13-day-lanes-stopped.md`. The measured record of the night is
`~/.local/state/coding-harness/night/2026-11-13-a/lane-watch.log`; the lane
file beside it (`lanes.md`) names every lane's state.

## Where we are

Ten lanes ran. Three changes merged on 2026-11-13 evening (pull requests 383,
384, 385 of the afternoon, then 386, 387 and 376), one decision pull request
is open (389), and one pull request fell out of the merge queue (388). Every
other lane is parked with one question for the maintainer in the notes of its
bead; no lane has authorised work left, so the night run ended early. The
flaky swarm test failed main's push run again at 2026-11-13T23:59Z (run
43531079125); the change that repairs it is parked at its appetite.

## Next step

Put the questions under "Needed from the maintainer" to the maintainer from
the top, one at a time, each with its context from the bead notes; each
answer restarts a lane with the command named in `lanes.md`.

## Needed from the maintainer

In the order that frees the most work. Each question stands with its context
and recommendation in the notes of the bead named.

1. **Merge pull request 389** (decision: implement attempts and drafts use
   the targeted check; bead coding-harness-0swp). Full `make verify` green at
   `f589c45b`. Its merge also frees the slip counter (lane 10).
2. **Seconds gates before admission** (bead coding-harness-bxxt.6): review
   round 1 left 13 rows, four of them code faults in the new runner; the
   appetite of six hours is spent. Recommended: four more hours and repair
   all rows.
3. **Flaky swarm test** (bead coding-harness-yb1l): review round 1 left 16
   rows; the guard is too broad (every append-mode open, ten exemptions) and
   misses unlocked reads. Recommended: three more hours and a guard that
   holds reads and appends of stand-in logs, identified by declaration, with
   no exemption list. The natural failure was not reproduced locally (60 of
   60 green on the pre-fix commit) but hit main again that night.
4. **Pull request 388** (truthful research headers, bead coding-harness-g19n):
   the census finds a fifth research file, merged through pull request 387.
   Recommended: one rule in the spec — the header-only correction holds for
   every file the census flags until the merge — instead of a list of files.
5. **Temporary test folders** (bead coding-harness-bxxt.3): the re-check
   found the lost git diagnostic at a second call site (F6-5). Recommended:
   one helper for every git launch of the runner, held by a source test.
6. **Reuse of a green result** (bead coding-harness-bxxt.2): the research
   swarm stayed incomplete twice (topic 3 fails the claims template for two
   different models; qwen3.8-flash timed out). Recommended: resume with
   another online model and read why topic 3 fails.
7. **Plan card, faster swarm tests** (bead coding-harness-wnka): go or veto;
   implementation after the flaky-test change merges.
8. **Data terms** of almost all admitted Go models expire on 2026-11-16; the
   runner refuses them afterwards. Not part of any lane.

## Decisions and preferences

Stated by the maintainer on 2026-11-13 and 14; not to be asked again.

- Hand repairs and hand finishing of a failed runner attempt go to an Opus
  subagent, not to the orchestrator's own conversation.
- longcat models are out for good (pull request 386); the research swarm's
  free rule excludes the contributor and longcat free ids as well.
- Two verify slots stay deferred on the Mac mini until the seconds-gates
  change and the targeted check are merged (bead coding-harness-u1ha).
- Seconds gates before admission: the slot belongs to the heavy gates,
  derived from the cost class with an explicit exception mark; reuse the
  result for an unchanged tree; report every red gate at once; no extra check
  after a merge of main; no switch in kit repositories (its `decisions.md`).
- Kit probe only on kit changes: trigger from the kit manifest; only the
  expensive half is conditional; a field in the gate list; a declared skip
  before phase 6 (its `decisions.md`). Plan card: go.
- Slip counter: derive the count from the run log, no writer; report the
  count beside the incomplete runs. Plan card: go, after pull request 389.
- Faster swarm tests: re-scoped from a shared fixture to the test bodies —
  measured, fixture setup is 23 s of 791 s.
- Targeted check: the slip counter left the change (Q-9); the amendment text
  of ADR 0025 point 6 as approved.
- Origin check: the loop ended after round 9 (merged as pull request 387).
- Temporary test folders: decision Q-6 holds, the spec follows it (Q-7).
- Pull request 371 (an old night plan) was closed.
- A new commit-signing key is in use on the Mac mini
  (`~/.ssh/id_ed25519_signing`, registered at GitHub).

## Open work and blockers

Task status stays in the tracker; this lists where each lane stands at
01:30 UTC.

| Lane | Change (bead) | Head | State |
|---|---|---|---|
| 1 | origin-check-across-blocks (coding-harness-3h96) | merged | pull request 387 merged |
| 2 | explore-provenance (coding-harness-g19n) | `4bd76733` | pull request 388 open, out of the merge queue twice; parked, question 4 |
| 3 | targeted-check-more-verbs (coding-harness-0swp) | `f589c45b` | decision pull request 389 open; question 1 |
| 4 | verify-tmp-cleanup (coding-harness-bxxt.3) | `98fef1fa` | parked, question 5 |
| 5 | flaky-swarm-leak-test (coding-harness-yb1l) | `a2749799` | parked at the appetite, question 3 |
| 6 | verify-cheap-before-admission (coding-harness-bxxt.6) | `ec7629eb` | parked at the appetite, question 2; a decision pull request when it goes out |
| 7 | kit-probe-on-kit-change (coding-harness-w2ay) | `d15fe984` | implement rejected three times; waits for the merge of lane 6, then an Opus subagent |
| 8 | swarm-shared-fixture (coding-harness-wnka) | `d1d81826` | draft done; parked, question 7 |
| 9 | verify-result-reuse (coding-harness-bxxt.2) | `23eaf0d4` | parked, question 6 |
| 10 | slip-counter (coding-harness-bxxt.7) | `62e3a361` | draft done, go given; waits for the merge of pull request 389 |

Beads opened on 2026-11-13: coding-harness-bxxt.6 (seconds gates before
admission), coding-harness-bxxt.7 (slip counter), coding-harness-363r.2
(longcat removal, merged). Not yet filed, each named in a pull request or a
bead note: one shared exclusion list for the two free rules; the date gate
dates a file by a merge commit instead of its last real change; the runner's
cheap check starts pytest without a target after a removal-only repair.

## Working state and parallel-session boundary

Worktrees under `.claude/worktrees/`, one per lane as named above, plus
`remove-longcat` and `p1-rule` (both merged; removable) and
`handover-2026-11-14` (this handover). The main checkout stayed on an old
`main` (`5d70a6aa`) with one untracked folder, `.codex/agents/`, untouched.
Saved, unaccepted runner attempts lie on `refs/stage2/attempts/<change>/…`
(pushed). No other Claude session ran in the repository; the Codex desktop
application was open, its activity in this repository was not read. The
research swarm needs its state store outside the home directory: on this
machine `XDG_STATE_HOME` points to a folder under `/Users/Shared`, set for
swarm calls only. The night run's wake and keep-awake handles are in the state
directory's `handles` file; both were stopped at the run's end.

## Validation

- Full `make verify` green, each on the head named, 2026-11-13/14:
  origin-check-across-blocks `ecc1f26e`; explore-provenance `4bd76733`;
  remove-longcat `37b21043`; targeted-check-more-verbs `f589c45b`;
  flaky-swarm-leak-test `a4359af9`; verify-cheap-before-admission `822e1c4a`.
- Not run after the last merge of origin/main: a full `make verify` on
  flaky-swarm-leak-test `a2749799` and verify-cheap-before-admission
  `ec7629eb` (cheap gates and the touched test files only).
- A full run took 10 to 13 minutes on the Mac mini (pytest about 500 s, kit
  probe 110 to 180 s, the 22 seconds gates about 25 s); waits for the one
  slot were 7 to 39 minutes that evening.
- Main's push run 43531079125 (2026-11-13T23:59Z) is red on the flaky swarm
  test alone; the two merge-group runs of pull request 388 are red on the
  research census.
