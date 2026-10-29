---
title: "Session handover — three-lane night 2026-10-28/29, 2026-10-29"
category: handover
created: 2026-10-29
updated: 2026-10-29
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-10-29"
tags: [handover, night-run, three-lanes, review-loop, stage-2]
target_ref: db701a06
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The night of 2026-10-28/29 ran three lanes from one orchestrating session,
following the night plan (`docs/research/2026-10-28-night-run-plan.md`,
merged as PR #270). Lanes were kept busy, but nothing was merged at night.
Three text pull requests are ready (#272, #273, #274). Two changes are
parked at their appetite (swarm-test-speed, run-report). The runner change
fail-fast-attempts is code-complete through eight review rounds and waits on
its last loop stage: OpenCode Go hit its usage limit (`GoUsageLimitError`,
429) at about 02:05 UTC and was still limited at 02:52 UTC. The night's main
finding is the review loop's 2000-line diff bound: on every change tonight,
it cut away the change's tests (PR #274).

## Next step

Put the decision block below to the maintainer, one question at a time,
starting with question 1 (merge the three ready pull requests). Then
continue lane A with the last review-loop stage of fail-fast-attempts, once
OpenCode Go answers again.

## Needed from the maintainer

One decision at a time; each has a recommendation.

1. **Merge the three ready text pull requests?** They are #272 (test
   strategy kit page, three lanes, what sets the workflow apart; head
   `43bf562490e7e25224bde1f954267bc424b1b2cf`), #273 (criterion-ledger trial
   on an instance; head `03ebb5a504caf5514d91a05d0bfc900d64579064`) and #274
   (what reviewers see when the diff is cut; head
   `eb305e5dace53e7f4ee01d73e3885b9645a732bd`). CI is green on all three.
   They are text only and had no phase-6 review. Recommendation: merge
   through auto-merge (bead coding-harness-m254).
2. **The bounded-diagnostic mechanism in fail-fast-attempts** (bead
   coding-harness-5tyh). The second and third finding of one mechanism (rows
   L5-1 and L8-1, after L4-3): the retry's failed test ids and the cheap
   evidence are read from an 80-line tail with stderr after stdout. Case
   repair ended at L5-1 (`docs/WORKFLOW.md` §4). Structural remedy: read the
   failed ids from the full output before it is shortened, and keep stdout
   and stderr apart, as `verify_evidence` already does. Recommendation: fold
   it into 5tyh with 30 more minutes of appetite. About 5.0 of 5.5 hours are
   measured; a few short hand repairs were not timed.
3. **swarm-test-speed** (bead coding-harness-dca4, draft PR #271): parked at
   its appetite after phase 6 found two MAJOR rows. F6-1: the C loader
   accepts a tab before a comment that the safe loader refuses. F6-2: the
   before/after runs were not isolated. Recommendation: cut to the parse
   cache only, drop the C loader, re-measure three isolated runs per
   revision, new appetite of 1 hour.
4. **run-report** (bead coding-harness-o2yc, branch `feat/run-report`):
   implemented, verify green at `e115da06`, parked at 1.79 of 2 hours after
   review round 3 took three rows. L3-1: the orchestrator's own
   `…, N s — …` time lines are not counted. L3-2: `--stage2-off` without a
   reason swallows the change. L3-3: an absolute path is echoed.
   Recommendation: a new appetite of 45 minutes.
5. **guard-test** (beads coding-harness-0ho, coding-harness-y17): the branch
   `explore/guard-test` already holds the maintainer's answers Q-1 to Q-5
   (2026-10-16), a drafted spec and plan, and one failed implement attempt.
   It is 1188 commits behind `main`. Recommendation: redraft spec and plan on
   current `main`, keeping the answers, instead of reviving the old branch.
6. **pi-neutral-paths** (bead coding-harness-xul8, branch
   `fix/pi-neutral-paths`, explored). Pi 1.2.0 always adds `<cwd>` and
   `<docs>`, absolute local paths with the account name, to its system
   prompt. No CLI flag removes them, and the leak check does not see them.
   The review loop, the probes and the session are affected as well as the
   research swarm. Two questions follow, scope first: all Pi launches, or the
   research swarm only? Recommendation: all, since the mechanism is the same.
7. **The review diff order** (bead coding-harness-ut8q, PR #274; touches
   ADR 0021). Options: leave `findings.md` and `plans/INDEX.md` out of the
   diff; put code and tests first; split a large change across reviewers.
   Recommendation: the first two now, as one bounded change; the split later
   if a diff still exceeds the bound.
8. **An adoption day for the criterion-ledger gate** (bead
   coding-harness-wpv, evidence in PR #273): on a pre-ledger instance the
   gate is red at once, and a missing `plans/changes/` blocks.
   Recommendation: add `criterion-ledger` to `decisions/adoption.yaml` and
   read it through `scripts/adoption.py`. That is a decision pull request.
9. **DeepSeek terms expire 2026-10-31** (bead coding-harness-bomd): two days
   left. The renewal reading is a decision pull request.

## Decisions and preferences

- The maintainer said "Mach das" (2026-10-28) to the orchestration
  improvements. Beads created: coding-harness-uxa9 (the runner stops at the
  appetite, lane A after 5tyh), coding-harness-t3s3 (the runner commits a
  rejected attempt's output), coding-harness-hleu (route by measured
  success, after o2yc) and coding-harness-a3a7 (orchestrator evidence before
  review round 1).
- A memory stop must not happen again (maintainer, 2026-10-28). It did not
  happen tonight. The lowest reading was 33 % free, at about 22:30 UTC.
- No merges at night. Pull requests that meet the self-merge rules are
  listed above.

## Open work and blockers

Task status is in Beads. The lane state at about 03:00 UTC:

- **Lane A, fail-fast-attempts** (coding-harness-5tyh), head `21b297c5`.
  - Eight review rounds are written and every row is decided. The
    orchestrator repaired code rows by hand with tests that were red first,
    because the runner has no appetite stop yet and the appetite was tight.
  - Full `make verify` was green at `023823ec`. Every commit since then
    touches only records or text.
  - Blocked on the last loop stage (glm-5.3) by the Go usage limit. A retry
    is scheduled for about 03:55 UTC. Then phase 6 and the pull request
    follow.
- **Lane A next, verify-machine-lock** (coding-harness-p6mu, P0).
  - Spec and plan are drafted (`e66a9975`, appetite 3 hours).
  - Implement waits: the plan changes `scripts/stage2.py`, which the night
    plan gives to lane A alone. It runs after 5tyh is ready, before lane A's
    next item.
- **Lane C, index-merge-regenerates** (coding-harness-njtm, -hfsz, -eq6y),
  head `60cd44f2`.
  - Two review rounds are written and decided; full `make verify` was green
    at `ed4cea23`.
  - Round 3 was blocked by the Go limit.
- **Parked** (questions 3 to 6 above): swarm-test-speed, run-report,
  guard-test, pi-neutral-paths.
- **Not done tonight:**
  - The governance translation (coding-harness-yim), because
    `regelwerk.md` and `quality-gates.md` are parsed by scripts and tests,
    so it is not a text-only change.
  - The explore of coding-harness-3g53 and the spike coding-harness-km1:
    both need OpenCode Go.
- **New tonight:** coding-harness-yb1l (a flaky swarm test; a CI rerun
  passed) and coding-harness-vxwp (the docs change, PR #272).

## Working state and parallel-session boundary

- `main` is at `db701a06`. No other session ran in this repository tonight;
  this session was the only tracker writer.
- Worktrees: every one below is clean and pushed.

  | Worktree | Branch | Head |
  | --- | --- | --- |
  | `fail-fast-attempts` | `fix/fail-fast-attempts` | `21b297c5` |
  | `index-merge-regenerates` | `fix/index-merge-regenerates` | `60cd44f2` |
  | `run-report` | `feat/run-report` | `358472d8` |
  | `swarm-test-speed` | `perf/swarm-test-speed` | `703869a3` |
  | `verify-machine-lock` | `fix/verify-machine-lock` | `e66a9975` |
  | `pi-neutral-paths` | `fix/pi-neutral-paths` | `c7e41301` |
  | `test-strategy` | `docs/test-strategy` | `43bf5624` |
  | `ledger-instance-trial` | `docs/ledger-instance-trial` | — |
  | `review-diff-cut` | `docs/review-diff-cut` | — |
  | `handover-1029` | this file | — |

- Loop records stand outside the repository under
  `~/.local/state/coding-harness/stage2/<change>@<digest>/loop.md` for
  fail-fast-attempts, index-merge-regenerates and run-report.
- The lane ledger with UTC times is in the session scratchpad. It is not in
  the repository; this file carries what it holds.

## Validation

- Full `make verify` green, measured 2026-10-28/29:
  - fail-fast-attempts at `023823ec`: 4087 passed;
  - index-merge-regenerates at `ed4cea23`: 4105 passed;
  - run-report at `e115da06`: 4107 passed;
  - swarm-test-speed at `cf71a96c`: 4086 passed.

  Each ran on its own with `nice -n 10` and `-n 4`.
- CI is green on #271, #272, #273 and #274, measured 2026-10-29 at about
  03:00 UTC.
- Lessons for the next run:
  - **The draft verb runs `make verify`.** It bears a verify, so two drafts
    and a kit probe once overlapped; memory held at 33 % free.
  - **After midnight, stamp `updated:` before committing.** The gate
    `frontmatter-current` failed twice on dates.
  - **`tools/bd update --notes` replaces a bead's notes.** Use
    `--append-notes`. One overwrite was restored from the history.
