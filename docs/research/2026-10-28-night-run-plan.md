---
title: "Night-run plan — 2026-10-28/29"
category: research
created: 2026-10-28
updated: 2026-10-28
last_reviewed: 2026-10-28
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [night-run, plan, lanes, stage-2]
---

# Night-run plan — 2026-10-28/29

**This is the plan for tonight. It does not report a run.** The maintainer
asked for it on 2026-10-28 at about 20:45 UTC: three lanes, always occupied,
running through the night. It follows the
[plan of 2026-10-26](2026-10-26-night-run-plan.md). One orchestrating Claude
Code session works the three lanes below. The plan grants no new model,
architecture or deployment permission. Task state stays in Beads.

## State at the start

Measured 2026-10-28 at about 20:47 UTC against `main` `0369816f`.

| Lane | Change (bead) | Branch | State |
| --- | --- | --- | --- |
| A | `fail-fast-attempts` (coding-harness-5tyh) | `fix/fail-fast-attempts` | implement: one cheap-check test left red; 4.48 h of the 5.5 h appetite used (maintainer, 2026-10-28); the last Sonnet attempt was stopped for low memory |
| B | `swarm-test-speed` (coding-harness-dca4) | `perf/swarm-test-speed` | review round 1 decided and repaired; full `make verify` running; then round 2 |
| C | `index-merge-regenerates` (coding-harness-njtm, -hfsz, -eq6y) | `fix/index-merge-regenerates` | implement: the last attempt failed only ruff, fixed by hand at `404d9a64`; full `make verify` queued |
| (B next) | `run-report` (coding-harness-o2yc) | `feat/run-report` | explore stopped for low memory; restart queued |

Open pull requests: #235, #236, #238 (drafts, the parked finding-table
stack, bead coding-harness-s05q). Nothing else is open.

## The resource rule tonight

The machine has 8 GB of memory. On 2026-10-28 at about 19:55 UTC Claude Code
stopped two background jobs for critically low memory while one
`make verify` and two runner verbs ran (bead coding-harness-4emv, note of
that day). So tonight:

1. **One verify-bearing step at a time, across all lanes.** A step bears a
   verify when it runs `make verify`: `implement`, `repair`, and the
   orchestrator's own full verify. A second such step waits in a queue.
   The orchestrator's own verify runs `nice -n 10` with `-n 4`.
2. **The other two lanes stay busy with remote steps** that need little
   local memory: `explore`, `draft`, `prepare-loop` and `review-loop`
   rounds, phase 6 through Codex, CI waits, pull-request text. Interviews
   are not remote steps: they need the maintainer (below).
3. **Queue order for the verify slot:** a runner attempt first (its
   30-minute step limit can kill it), then the lane nearest its pull
   request (finish first), then the rest.
4. **No restart after a memory stop without the maintainer's word,** as
   Claude Code's notice asks. A stopped job is recorded, its leftovers are
   committed unchanged, and the lane moves to its next remote step.

## Merge rules tonight

**No merges tonight.** A merge command asks the maintainer
(`.claude/settings.json`), and nobody can confirm it at night
(2026-10-28: a background merge was refused that way). A pull request that
meets the self-merge rules is marked ready instead:

- CI green, `--match-head-commit` named in the morning list;
- after phase 6, no BLOCKER or MAJOR open;
- not a decision pull request.

The morning handover lists every ready pull request with its head commit,
so the maintainer can say "merge all" once (bead coding-harness-m254: the
merge then goes through GitHub's auto-merge, one prompt).

## Standing night rules

Unchanged (`docs/WORKFLOW.md`, "Night runs"; maintainer, 2026-10-26):

1. **Codex at capacity:** wait four minutes and retry once; then Sonnet 5.5
   takes that one step, with the reason recorded.
2. **A further case of the same mechanism at a phase-6 re-check:** record
   it, park that pull request, continue with the next queue item.

Also tonight:

3. **An interview question parks the change, not the lane.** A `feature`
   change owes at least three maintainer answers. At night such a change
   runs its explore and stops before the interview; the lane takes its next
   item. A `bounded` change takes a reasoned skip or details where the
   decision is the agent's, and parks on a real `[DECISION]`.
4. **An appetite stop parks the change.** The orchestrator may answer cut,
   park or drop, never continue; the lane takes its next item.
5. **Only one lane changes `scripts/stage2.py`** (lane A).

## The three queues

Each lane works its queue top to bottom. When a lane's item parks or waits
for the verify slot, the lane takes the next remote step of its next item,
so no lane is idle while the queue has work.

### Lane A — the runner (`scripts/stage2.py`)

1. `fail-fast-attempts` (coding-harness-5tyh): restart the Sonnet implement
   attempt for the one red test; then the review loop (4b), phase 6, pull
   request. At 5.5 h the change parks (rule 4).
2. The finding-table package (coding-harness-s05q, led by
   coding-harness-6jg, with coding-harness-2i9j and coding-harness-vque;
   one pull request, maintainer 2026-10-27): decide keep, rebase or close as
   superseded for #235, #236 and #238 against `main`'s own malformed-answer
   handling; then merge `main` in, `make verify`, phase 6.
3. coding-harness-k93f (bounded): the runner writes the fixed-line skeleton
   per taken row; the model fills only the test or the reason.

### Lane B — test speed, then monitoring

1. `swarm-test-speed` (coding-harness-dca4): when the full verify is green,
   record the full-suite timing in `plan.md`, run review round 2, then
   phase 6 and the pull request.
2. `run-report` (coding-harness-o2yc, bounded; maintainer 2026-10-28:
   "schnell"): restart the explore, then the interview (reasoned skip or
   details), draft, implement, review loop, phase 6, pull request.
3. Explore only, for the morning interview: coding-harness-0ho with
   coding-harness-y17 (a red-first form for fixes that live only in test
   code; seen twice on 2026-10-28), class feature.

### Lane C — merges and machine rules

1. `index-merge-regenerates` (coding-harness-njtm, -hfsz, -eq6y): full
   `make verify` in its slot; then the review loop, phase 6, pull request.
2. coding-harness-p6mu (bounded): one `make verify` per machine — parallel
   lanes queue the full run instead of overloading the machine. Tonight's
   resource rule, built into the tooling.
3. coding-harness-xul8 (bounded): the research swarm sends local absolute
   paths to online models through Pi's system prompt.
4. Explore only, for the morning interview: coding-harness-3g53 (re-read
   the Go terms table at every availability preparation), class feature.

## Not tonight

- Decision pull requests (coding-harness-eh42, -fctf, -pwdi, -k0ub and
  others): they need the maintainer.
- The DeepSeek terms renewal (coding-harness-bomd): re-read on 2026-11-01.
- The runner's own event log (coding-harness-zaqf, step 2): it changes
  `scripts/stage2.py` and waits for lane A.

## In the morning

A one-page handover under `docs/journal/handover/` as a pull request: per
lane what finished, what parked and why, the ready pull requests with their
head commits, the questions for the maintainer in one block (one decision
block a day, 15:00 local), and each lane's next action. The lane ledger with
UTC timestamps backs it.
