---
title: "Session handover — three-lane night 2026-10-29/30, 2026-10-30"
category: handover
created: 2026-10-30
updated: 2026-10-30
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-10-30"
tags: [handover, night-run, three-lanes, review-loop, stage-2]
target_ref: 635e9bd1
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The night of 2026-10-29/30 ran three lanes from one orchestrating session,
from about 21:55 to 03:05 UTC, following the night plan (PR #282, bead
coding-harness-4emv). Four pull requests are ready to merge with green CI:
fail-fast runner attempts (#279), the run report (#277), the plan prompt that
names the held paths (#285) and the night plan itself (#282). Three changes
stopped and are parked, each with a proposal below: the one-verify-per-machine
lock (draft #284), the index merge rule (draft #283) and the review-diff
order (branch only). No merge ran at night, as the plan required. The full
`make verify` ran one at a time under the manual lock all night. Each green
run took 10–13 minutes (2026-10-29/30, ledger below).

## Next step

Merge the four ready pull requests in the order #279, #277, #285, #282, each
against the head SHA listed under "Ready pull requests". Then take the
decision block under "Needed from the maintainer".

## Needed from the maintainer

### Ready pull requests (CI green, measured 2026-10-30 03:02 UTC)

| PR | Change | Head SHA |
|---|---|---|
| #279 | Runner attempts fail fast (bead coding-harness-5tyh) | `b43d14997a0a88aefdc3d1fa179bbd76a29132a2` |
| #277 | Run report (bead coding-harness-o2yc) | `a8d15f610635c2baac3bae167c9ed296766a488e` |
| #285 | Plan prompt names the held paths (bead coding-harness-h5tj) | `d4b2edd098be79cacfa39dad4221b09ca393b5ba` |
| #282 | Night-run plan 2026-10-29/30 (bead coding-harness-4emv) | `4cdab68377348d1ce1e96b0412d695de9fb67eee` |

The diff cut applies to #279. Every review round of that change saw at most
2000 of its lines, so it went to phase 6 and its pull request with the cut
named (the precedent the maintainer set for this bead).

### Parked changes, each with a proposal

1. **One `make verify` per machine** (draft PR #284, bead
   coding-harness-p6mu, head `88a9d2ee9dfe1ccd47a78b0b34387bd579fbd237`;
   verify green at `dfb1058f`, 2026-10-30 01:18 UTC, 4111 passed). About
   4.8 of 6.0 hours used. The case repairs stopped because the findings
   repeat two mechanisms:
   - **A, ownership ends while descendants live**: loop rows L1-11, L3-1,
     L4-2 and phase-6 rows F6-1 (a cancelled waiter deletes the active
     holder record) and F6-5 (a grandchild outlives the protected command and
     the lock is released).
     Proposal: only the owner writes and removes the holder record, and the
     lock is held until the whole process group or session is gone.
   - **B, nested-marker validation**: L1-1, L1-12 and F6-2 (an unrelated pid
     with matching metadata bypasses admission).
     Proposal: validate the nested marker by ancestry or by the inherited
     lock descriptor instead of by metadata.
   Recommendation: one more slot of about two hours for both remedies, then
   phase 6 again.
2. **Index merge rule** (draft PR #283, bead coding-harness-njtm). Phase 6
   found P6-1 and P6-2, both MAJOR. Proposal: 45 more minutes to repair
   both, then the phase-6 re-check.
3. **Review-diff order** (branch `fix/review-diff-order`, bead
   coding-harness-ut8q, head `d9fd13bd0a87d4ec0d0b68b3e4620237dee7cba5`).
   The runner's implement attempt verified and committed on attempt 3, but
   it took 98 minutes (01:23–03:01 UTC) against the 45 minutes that were
   left. Not done yet: the orchestrator's bootstrap edit of the review-loop
   prompt's Input paragraph (`prompts/04b-review-loop.md`, a held path),
   prepare-loop, the review loop, phase 6 and the pull request.
   Proposal: one more slot of about 1.5 hours for those steps.
4. **pytest worker cap** (bead coding-harness-l7sc). Explore, interview skip
   and the drafted plan are committed (`ef30be52`, appetite two hours). The
   implementation waits until #284 merges, because both change
   `scripts/verify_all.sh`. Proposal: start it right after #284.
5. **Model data terms stay current** (branch `explore/model-terms-current`,
   bead coding-harness-3g53). prepare-explore failed twice at 23:16 UTC
   because the OpenCode Go catalog refresh failed (`pi-refresh-failed`).
   Proposal: retry by day. If the catalog fails again, open a runner bead
   for that failure.

### Waiting on the maintainer from before

- Decision PRs #280 (document gates form a docs subset for the draft verb)
  and #281 (a guard test that plants its own fault proves a test-only
  repair, ADR 0023).
- The plan card for bead coding-harness-xul8 (Pi's system prompt sends local
  absolute paths to online models).
- The DeepSeek terms expire on 2026-10-31 and need a renewal decision PR.

### One question for the 15:00 block

Topic: what to continue first after the merges.
Today: three changes are parked at their appetite stop (#284, #283, the
review-diff order).
Recommendation: #284 first, because the pytest worker cap (bead
coding-harness-l7sc) waits on it.
Question: do the parked changes get their proposed extra time, and in which
order?

## Decisions and preferences

- No merges at night. The maintainer merges the ready pull requests.
- The full verify runs one at a time per machine under
  `~/.local/state/coding-harness/verify-manual.lock`. Foreign-model calls run
  beside it.
- An appetite is a stop: at night a change is cut, parked or dropped, never
  extended.
- A second finding of one mechanism ends case-by-case repair. The mechanism
  goes to the handover as a structural remedy.

## Open work and blockers

Task status lives in Beads. In progress after this night: coding-harness-o2yc,
coding-harness-p6mu, coding-harness-h5tj, coding-harness-l7sc,
coding-harness-3g53, coding-harness-ut8q, coding-harness-njtm. Each of those
beads carries a note from this night with its stop point.

Lessons from the night, to be made durable:

1. After a hand repair, the orchestrator sets the loop row's status to
   `fixed — <test>`. Otherwise the next round is refused ("taken rows are not
   repaired yet").
2. A hand edit of a change's header or status needs
   `scripts/plans_registry.py --index`, or verify goes red on a stale
   `plans/INDEX.md`.
3. Runner explore leaves the skeleton banner and a human-written header in
   `research.md` (seen on h5tj, p6mu and l7sc). This adds to bead
   coding-harness-g19n.
4. Frontmatter stamps use the local date. After local midnight, UTC is still
   the day before; `scripts/check_frontmatter_current.py --stamp` runs before
   such commits.

## Working state and parallel-session boundary

- Worktrees under `.claude/worktrees/`: `fail-fast-attempts`, `run-report`,
  `verify-machine-lock`, `plan-held-paths`, `verify-worker-cap`,
  `review-diff-order`, `index-merge-regenerates`, `night-plan-1029`, and this
  handover's `handover-1030`. Every branch is pushed. Remove each worktree
  after its merge.
- The model-terms branch lives in the main checkout
  (`explore/model-terms-current`). The untracked `.codex/agents/` there is
  not this session's and stays untouched.
- No other session ran in this repository during the night. The scan at
  03:03 UTC showed one session in another repository only. This session was
  the only tracker writer; the tracker is pushed.

## Validation

Ledger of the night (UTC, measured with `date -u`):

- Full verify green, one at a time under the lock:
  - o2yc at `48805a1e` (22:14, 4118 passed) and at `786b265a` (23:11, 4119
    passed)
  - p6mu at `2e499188` (23:40), `ecbcf576` (00:22) and `dfb1058f` (01:18,
    4111 passed)
  - h5tj at `ea8b5590` (23:25), `9d1e2ac8` (00:07), `eecb3375` (00:35),
    `22329994` (01:03) and `b0e61fe2` (01:31, 4120 passed)
- Red runs, each repaired:
  - p6mu at `40eeddda`: ruff PTH105, fixed at `dfb1058f`
  - h5tj at `f6b36046`: stale index, regenerated at `9d1e2ac8`
- Phase 6 (Codex), clean:
  - o2yc, re-check 01a189ef
  - h5tj, 01a18a6f
- Phase 6 (Codex), open rows:
  - p6mu, re-check 01a18a63: F6-1, F6-2 and F6-5 open, parked
- CI green on #277, #279, #282, #283, #284 and #285 (2026-10-30 03:02 UTC).
- Not run: verify at the ut8q head `d9fd13bd` outside the runner's own
  post-run check; a review loop for ut8q.

## Addendum — 2026-10-30, maintainer interview (~06:00–06:25 UTC)

The maintainer answered every open question (recorded in the beads named):

- Merges: the session merges the ready pull requests. #279 merged
  (`20af7d00`), #277 merged (`ba131c32`). #285, #282, #280 and #281 follow
  one at a time: each branch is brought up to date with main, CI runs again,
  and the merge goes against the new head.
- One verify per machine (bead coding-harness-p6mu): two more hours for the
  structural remedies A and B, then phase 6 again. This runs first in lane A.
- Index merge rule (bead coding-harness-njtm): 45 more minutes for P6-1 and
  P6-2. Lane C.
- Neutral Pi paths (bead coding-harness-xul8): plan card accepted unchanged.
  Lane A, after p6mu.
- Review-diff order (bead coding-harness-ut8q): 1.5 more hours. Lane A,
  after xul8.
- pytest worker cap (bead coding-harness-l7sc): starts after p6mu merges.
- Model data terms (bead coding-harness-3g53): retry by day. If the
  catalog refresh fails again, open a runner bead.
- Decision PR #280 (docs gate subset): accepted, option 1.
- Decision PR #281 (guard test, ADR 0023): accepted, option 1, so phase 4
  starts. The ADR answer is the maintainer's to state and is still owed.
- DeepSeek zero-retention agreement: renewed through 2026-11-30, as the
  maintainer stated. A decision PR moves `valid_until` in
  `model-endpoints.yaml`.
