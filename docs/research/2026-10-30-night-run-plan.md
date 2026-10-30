---
title: "Night-run plan — 2026-10-30/31, extended to 14:00 UTC"
category: research
created: 2026-10-30
updated: 2026-10-30
last_reviewed: 2026-10-30
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-4emv
tags: [night-run, plan, lanes, stage-2]
---

# Night-run plan — 2026-10-30/31

**This is the plan for tonight. It does not report a run.** The maintainer
asked for it on 2026-10-30 at about 22:05 UTC ("Bitte mache einen Nachtplan
für alle fünf Lanes") and extended it at about 22:20 UTC to 15:00
Europe/Berlin the next day ("Mach den Plan bis morgen 15 Uhr"), which is
14:00 UTC on 2026-10-31. It follows the
[plan of 2026-10-29](2026-10-29-night-run-plan.md) and keeps its rules except
where this page says otherwise. One orchestrating Claude Code session works
five lanes until 14:00 UTC on 2026-10-31, then hands over. The plan grants no new model,
architecture or deployment permission. Task state stays in Beads.

## State at the start

Measured 2026-10-30 at about 22:07 UTC against `main` `199e2ff4`. This
session is the only tracker writer; no other session runs in this
repository.

| Lane | Change (bead) | Branch, head | State |
| --- | --- | --- | --- |
| A | `pi-neutral-paths` (coding-harness-xul8) | `fix/pi-neutral-paths`, `216932e7` | plan card accepted (maintainer, 2026-10-30), 2 h phase 4 |
| A | `review-diff-order` (coding-harness-ut8q) | `fix/review-diff-order`, `d9fd13bd` | +1.5 h granted (maintainer, 2026-10-30) |
| B | `verify-worker-cap` (coding-harness-l7sc) | `fix/verify-worker-cap`, `ef30be52` | was waiting on the machine admission, which merged in PR #284 |
| C | `pi-catalog-redirect` (coding-harness-j2wb) | `fix/pi-catalog-redirect`, `08a1514a` | review round 7 returned two rows |
| D | tracker and worktree hygiene; data terms | — | several beads stay open after their PRs merged |
| E | `merge-queue` (coding-harness-eh42) | `fix/merge-queue`, `c5d69319` | review round 7 running |

Waiting on the maintainer, not merged tonight:

- PR #292: the appetite extends once by itself, at night too (bead
  coding-harness-6fdk). It is green, and it is the first merge in the
  morning.
- PR #286: the handover of the night of 2026-10-29/30.

## Rules tonight

The rules of the 2026-10-29 plan hold:

- the appetite is a stop;
- a feature change runs explore only;
- no merges until 07:00 UTC (the night);
- a leak-check BLOCK or a security BLOCKER stops the run;
- no lane sub-agents.

Four changes from the day:

1. **The verify slot is the machine admission, not a file lock.** Since
   PR #284 (`199e2ff4`), every `make verify` and every runner check takes one
   machine-wide admission and queues behind the holder. The outer
   `lockf` around implement and repair is dropped. A full verify still runs
   only before phase 6 and before a pull request leaves draft.
2. **A hand repair gets a targeted check** (PR #291): the touched and linked
   tests, ruff and the gates its files feed. A change under `prompts/`
   still owes a full verify.
3. **The appetite extends once by itself, up to twice the card's appetite**
   (maintainer, 2026-10-30; PR #292 not merged yet). At night, the three
   cases that would be a question by day are decided by the night rules:
   cut, park or drop.
4. **Hot files, re-assigned for tonight.**
   - Only lane A changes `scripts/stage2.py`.
   - Only lane B changes `scripts/verify_all.sh`. Lane A has no item on it
     tonight.
   - Lane E reads the three stale runner drafts but does not edit
     `scripts/stage2.py`.

The two standing night rules of `docs/WORKFLOW.md` ("Night runs") hold.
When Codex is at capacity, wait four minutes and retry once, then let Sonnet
5.5 take that step. When a phase-6 re-check finds a further case of the same
mechanism, park that pull request.

## Lanes

**Lane A — the runner.**

1. `pi-neutral-paths` (2 h): implement, review loop, full verify, phase 6,
   pull request.
2. `review-diff-order` (1.5 h):
   - the orchestrator's edit of `prompts/04b-review-loop.md`;
   - review loop, full verify, phase 6, pull request.
3. If time remains: the repair verb's targeted check
   (coding-harness-gxwg), explore and draft only.

**Lane B — machine load.**

1. `verify-worker-cap`: merge `main` in, implement, review loop, full
   verify, phase 6, pull request.
2. Measure the test suite's run time and speed up its slowest tests
   (coding-harness-dca4): bring `perf/swarm-test-speed` onto `main` and
   record the measured times. No edit to `scripts/verify_all.sh` unless it
   is the only remedy.

**Lane C — the Go catalog and data terms.**

1. `pi-catalog-redirect`:
   - decide the round-7 rows;
   - review rounds until clean;
   - full verify, phase 6, release loop, pull request.
2. Model data terms stay current (coding-harness-3g53, a feature):
   `prepare-explore` only. Its report goes into the handover for the
   maintainer; the explore itself starts after that report is shown.

**Lane D — hygiene and terms.**

1. Close the beads whose pull requests merged, after reading each one's
   merge (for example, the plan template names the held paths,
   coding-harness-h5tj, PR #285). Remove the worktrees of merged branches
   once their trees are clean. Nothing unmerged is removed.
2. The data terms of `deepseek-v4-pro` and `deepseek-v4.1-flash` expire on
   2026-10-31. After 00:00 UTC, record whether `prepare-loop` drops them, and
   which rungs remain, in bead coding-harness-3g53. Re-reading the Go page
   stays dated 2026-11-01.
3. If time remains: the test-strategy docs (coding-harness-vxwp), which are
   text only and gated by CI.

**Lane E — the merge queue.**

1. `merge-queue`:
   - decide the round-7 rows;
   - review rounds until clean;
   - full verify, phase 6, release loop;
   - the decision pull request (`decide(merge-queue): …`, label `decision`,
     decision template).

   The maintainer merges it. The ruleset switch and its read-back follow
   the merge, not tonight.
2. The three stale runner drafts (PRs #235, #236, #238; beads
   coding-harness-6jg, -2i9j, -vque): read each against `main` and record a
   proposal in its bead (close, fold into one, or rebase in lane A). No
   edit tonight.

Fallback when a lane runs dry: lane D's item 3.

## The day part, 07:00–14:00 UTC

From 07:00 UTC the day rules apply to the same five lanes:

1. The first merge is PR #292 (the appetite rule), then the plan and handover
   pull requests stay the maintainer's.
2. A non-decision pull request with green CI merges through a Haiku merge
   agent, with `--match-head-commit` and the full head SHA, one at a time,
   never `--admin`. A decision pull request (the merge queue) waits for the
   maintainer's word.
3. The appetite rule holds by day: the session extends once, up to twice, and
   asks only at twice the appetite, at an open `[DECISION]`, or at a
   structural choice after a second finding of one mechanism.
4. Questions are collected for the 15:00 Europe/Berlin block, apart from a
   stop that blocks every lane.
5. Each lane takes its next item from `tools/bd ready` once its plan items
   are done; the queue stays visible in the beads.

## Handover

At 07:00 UTC, a short status goes to the maintainer in the conversation.
By 14:00 UTC, a handover from its own worktree lists:

- the ready pull requests, each with its full head SHA;
- the parked items, each with a proposal;
- the `prepare-explore` report of lane C;
- one question block.
