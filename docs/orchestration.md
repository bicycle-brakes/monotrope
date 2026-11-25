---
title: "Lanes — how one session runs several changes at once"
category: architecture
status: proposed
created: 2026-10-28
last_reviewed: 2026-11-24
updated: 2026-11-25
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [orchestration, lanes, night-run, parallel-work]
---

# Lanes

**One orchestrating session works several queues of changes at once, by day
and by night.** Most of a change's time is spent waiting for a remote model,
so parallel lanes keep the work moving. The trial began with three lanes on
2026-10-27; since 2026-10-31 up to five run, and the run plan of each day or
night names how many. The limits are the machine's memory,
the local verification slots (two since the two-slot change, `HARNESS_VERIFY_SLOTS`;
one before) and the maintainer's attention, not the
number of lanes. This page describes how this repository runs it as of
2026-11-24 (`a5b117f8`). Much of it is still kept by hand.

## What a lane is

- **A lane is an ordered queue of changes.** Each item is one bead, one
  branch and one worktree ([Working in parallel](../README.md#working-in-parallel)).
  The queues are written down before a run starts. The night plan of
  2026-10-28 is an example ([night plan](research/2026-10-28-night-run-plan.md)).
- **One session orchestrates all of them.** It is the only tracker writer. It
  starts the runner's verbs, decides review rows, writes the record and
  commits. Models do the explore, draft, implement, repair and review work
  through `scripts/stage2.py`.
- **Disjoint files.** Only one lane changes a given hot file (for example
  the runner, `scripts/stage2.py`). Two lanes never touch the same one.

## The resource rule

The maintainer's reference machine has 8 GB of memory. Three parallel `make verify` runs drove the
load above 100 and lost two repair attempts to the runner's 30-minute step
limit (2026-10-27/28). One verify beside two runner verbs made Claude Code
stop two background jobs for low memory (2026-10-28, about 19:55 UTC). Since
then:

1. **Up to two verify-bearing steps across all lanes.** Such a step runs
   `make verify`: an implement or repair attempt whose targeted check falls
   back to the full run, the final review's own check, or the orchestrator's
   own full run, which runs at lower priority (`nice -n 10`). The number of test
   workers is sized from the machine: half the logical cores, at most one per
   2 GiB of memory (bead coding-harness-l7sc, #305). This unchanged count is
   per run, so two runs can use twice as many workers in total; per-slot tuning
   remains follow-up work (bead coding-harness-bxxt.11). Each slot checks the
   machine-wide memory floor at admission, an instantaneous reading that may
   precede the first run's peak memory use.
2. **Other lanes can take remote steps.** Explore, draft, review-loop rounds,
   the phase-6 review, CI waits and pull-request text use little local
   memory.
3. **When slots are contested, prioritise:** first a runner attempt, because its
   step limit can kill it; then the lane nearest its pull request; then the
   rest.
4. **No restart after a memory stop without the maintainer's word.** The
   leftovers are committed unchanged, and the lane moves to its next remote
   step.

## Machine facts at the start of a night run

Before the first lane of a night run starts, the orchestrator reads the
machine once and shows the result in the main conversation (bead
coding-harness-yql7):

```sh
python3 scripts/machine_facts.py
```

The command runs from the worktree the night run drives and prints one dated
block: free disk on the worktree's filesystem (the invoking directory's,
labelled so, when Git cannot identify the worktree), host-wide swap used
and total, the repository's registered non-bare worktrees (main checkout
included, stale registrations counted, bare entries not), and the runner and
verification invocations the existing run report recognizes (one `ps`
snapshot; each row carries process id, elapsed time, verb and change
attribution where known, and a verify wrapper and its child are two
invocations, not one logical job). Three lines under `running jobs:` carry no
process: `none matched` when no runner or verification job runs, the source
error of the process table when the snapshot itself failed, and
`runner recognition: not read (…)` when the runner's verb definitions could
not be loaded. Any field may read `not read (…: internal error: <Type>)`: then
the script itself failed on that field, not the source, and the fault belongs
in a bead.

Show the block in the main conversation before any lane starts, and copy it
into the night plan's “State at the start”. The block is an **observation,
not an admission verdict**: nothing is compared against a floor, nothing is
refused, cleaned up, started, stopped or admitted. A source the command
cannot read says `not read` with a short reason — never a zero — and the
readable fields stay. The readings describe the one invocation only;
rerunning the command later, for example the next morning, gives a fresh
observation and adds no automation.

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
- **A further case of the same mechanism** at a phase-6 re-check, but only
  when its remedy would be a `Boundary`, change the spec or its criteria, or
  touch security; otherwise the orchestrator takes the structural remedy at
  one choke point itself (standing grant, maintainer 2026-11-25).

A leak-check block or a security blocker stops the whole run.

## Merges and the morning

Unattended night runs launch through `tools/claude-code/night.py` (which turns
every sourced `ask` rule into a `deny` under `--permission-mode dontAsk` so a
permission prompt cannot stall the session). A pull request is admitted to
the merge queue by the orchestrator itself, by day or night, once phase 6 is clean, `make verify` is green on its head and its last commit carries
the `Closes-Bead` trailer (standing grant, maintainer 2026-11-25); every other
merge asks the maintainer. The morning handover lists the queued and the
remaining ready pull requests with their head
commits, and one word from the maintainer merges them: with the merge
queue active (rule RB-G7), that word admits them to the queue, and each counts
as merged only once GitHub shows it merged; a failing group leaves its pull
request open. Every step is committed and pushed at once, tracker first, so an
interrupted session loses nothing. A lane ledger with UTC times backs the
handover. A lane that ran verification also reports its missed-verification
observations: the slip count and the incomplete or not countable runs beside
it, read from the local history with `python3 -m scripts.verify_duration
slips`, together with the reader's partial status — a diagnosed gap travels
with the numbers, never as a bare zero (bead coding-harness-bxxt.7). Only the
runner's targeted repair checks supply targeted evidence; implement and draft
checks do not, so a zero does not measure misses from those checks. Runs
recorded before the counter existed carry no comparison identity: the reader
reports them on a separate line outside the count, and they do not make the
read partial. A lane reads its change with `--change <name>` and `--since` set
to the lane's start in UTC. This includes other lanes working on the same change;
the outside line holds runs of this repository; the unattributed line can also
include runs of other repositories on the machine. The reader also reports flaky-test signals (a full green then a
full red of one identity) and, when evidence is incomplete, names the
incomplete runs on both sides of a possible pair.

## Stated, enforced, planned

| Rule | Today | Planned |
| --- | --- | --- |
| Machine facts at the start of a night run | kept by hand: the orchestrator runs `python3 scripts/machine_facts.py` and records its snapshot (bead coding-harness-yql7) | — |
| Two protected verify slots, memory floor | enforced for protected work only: two admission slots per machine since the two-slot change (`HARNESS_VERIFY_SLOTS`, default `2`) and a memory floor per admission (beads coding-harness-p6mu, coding-harness-u1ha, #284) cover the `minutes` gates and marked `seconds` gates. The cheap gates and the runner's full-mode preparation run outside it, in every lane at once, so a lane's red lint appears before any wait (bead coding-harness-bxxt.6); the [seconds-gate audit](../plans/changes/verify-cheap-before-admission/seconds-gate-audit.md) found them free of shared writes | a disk bound for concurrent work (bead coding-harness-87b0) |
| The appetite stops the next attempt | kept by hand; the runner keeps trying | the runner stops itself (bead coding-harness-uxa9) |
| A rejected attempt's output is committed | by hand, after the verb | the runner commits it (bead coding-harness-t3s3) |
| Route by measured success | fixed route | measured first (beads coding-harness-o2yc, coding-harness-hleu) |
| Runner step limit, leak check, red first | enforced by the runner | — |
| One tracker writer | stated | the write guard (lakeswitch-ai D-60) |

What the run costs and where its time goes is measured in the night plans
and handovers, not here. `make report CHANGE=<name>` shows a change's runner
attempts, its time against the appetite and the live load, read-only (bead
coding-harness-o2yc, #277).
