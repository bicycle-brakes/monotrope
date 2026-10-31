---
title: "Three lanes — how one session runs three changes at once"
category: architecture
status: proposed
created: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [orchestration, lanes, night-run, parallel-work]
---

# Three lanes

**One orchestrating session works three queues of changes at once, by day
and by night.** Most of a change's time is spent waiting for a remote model,
so three lanes keep the work moving. The limits are the machine's memory,
the one local verification slot and the maintainer's attention, not the
number of lanes. This page describes how this repository runs it as of
2026-10-28. Much of it is still kept by hand.

## What a lane is

- **A lane is an ordered queue of changes.** Each item is one bead, one
  branch and one worktree ([Working in parallel](../README.md#working-in-parallel)).
  The queues are written down before a run starts. The night plan of
  2026-10-28 is an example ([night plan](research/2026-10-28-night-run-plan.md)).
- **One session orchestrates all three.** It is the only tracker writer. It
  starts the runner's verbs, decides review rows, writes the record and
  commits. Models do the explore, draft, implement, repair and review work
  through `scripts/stage2.py`.
- **Disjoint files.** Only one lane changes a given hot file (for example
  the runner, `scripts/stage2.py`). Two lanes never touch the same one.

## The resource rule

The machine has 8 GB of memory. Three parallel `make verify` runs drove the
load above 100 and lost two repair attempts to the runner's 30-minute step
limit (2026-10-27/28). One verify beside two runner verbs made Claude Code
stop two background jobs for low memory (2026-10-28, about 19:55 UTC). Since
then:

1. **One verify-bearing step at a time, across all lanes.** Such a step runs
   `make verify`: an implement or repair attempt, or the orchestrator's own
   full run, which runs at lower priority (`nice -n 10`, `-n 4`).
2. **The other lanes take remote steps.** Explore, draft, review-loop rounds,
   the phase-6 review, CI waits and pull-request text use little local
   memory.
3. **The order of the verify slot:** first a runner attempt, because its
   step limit can kill it; then the lane nearest its pull request; then the
   rest.
4. **No restart after a memory stop without the maintainer's word.** The
   leftovers are committed unchanged, and the lane moves to its next remote
   step.

## Keeping every lane busy

When an item waits for the slot, for an answer or for CI, its lane takes the
next remote step of its next item. Three events park a change, never its
lane:

- **An interview question.** A `feature` change owes the maintainer's
  answers. At night it runs its explore and stops before the interview. A
  `bounded` change records a reasoned skip where the bead already holds the
  direction.
- **The appetite.** It is a stop, not an estimate. At night the orchestrator
  may answer cut, park or drop, never continue.
- **A further case of the same mechanism** at a phase-6 re-check.

A leak-check block or a security blocker stops the whole run.

## Merges and the morning

At night nothing is merged: a merge asks the maintainer, and nobody can
answer it then. A pull request that meets the self-merge rules is marked
ready. The morning handover lists the ready pull requests with their head
commits, and one word from the maintainer merges them: with the merge
queue active (rule RB-G7), that word admits them to the queue, and each counts
as merged only once GitHub shows it merged; a failing group leaves its pull
request open. Every step is committed and pushed at once, tracker first, so an
interrupted session loses nothing. A lane ledger with UTC times backs the
handover.

## Stated, enforced, planned

| Rule | Today | Planned |
| --- | --- | --- |
| One verify-bearing step at a time, memory floor | kept by hand | a machine-wide lock and a memory floor (bead coding-harness-p6mu) |
| The appetite stops the next attempt | kept by hand; the runner keeps trying | the runner stops itself (bead coding-harness-uxa9) |
| A rejected attempt's output is committed | by hand, after the verb | the runner commits it (bead coding-harness-t3s3) |
| Route by measured success | fixed route | measured first (beads coding-harness-o2yc, coding-harness-hleu) |
| Runner step limit, leak check, red first | enforced by the runner | — |
| One tracker writer | stated | the write guard (lakeswitch-ai D-60) |

What the run costs and where its time goes is measured in the night plans
and handovers, not here. A run report is being built (bead
coding-harness-o2yc).
