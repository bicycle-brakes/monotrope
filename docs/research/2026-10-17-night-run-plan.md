---
title: "Bounded night-run plan — 2026-10-17"
category: research
created: 2026-10-17
updated: 2026-10-17
last_reviewed: 2026-10-17
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Codex, version: "2026-10-17"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw.1
tags: [night-run, plan, stage-2, handover]
---

# Bounded night-run plan — 2026-10-17

**Proposed operational plan, not an execution report.** The maintainer asked
what could be done autonomously over 18 hours, announced a Codex allowance
reset in about half an hour, then requested this plan. Existing approved work
continues under its existing authorization. This file grants no new model,
architecture, merge or deployment permission.

The source is the existing [night-run convention](2026-10-12-night-run.md):
an active orchestrating session rehearses a bounded queue sequentially, pushes
green checkpoints, and leaves a short morning handover. Routine unattended
operation is not qualified by this plan. No scheduler or service is added.
Task state stays in Beads; this file specifies order, limits and evidence.

## Three priorities

1. Finish the reachable review ladder: repair the remaining protocol-resolution
   case, verify it, and obtain a fresh independent review (coding-harness-4fk,
   [PR #157](https://github.com/MPAdesso/coding-harness/pull/157)).
2. Implement the prepared research-swarm contract in bounded green steps,
   using offline tests for the amended graph and catalog boundaries
   (coding-harness-icw, [PR #158](https://github.com/MPAdesso/coding-harness/pull/158)).
3. Leave restartable commits, accurate PRs and one current handover. If the
   first two items finish or stop early, scope the separate runner refactor
   through research only (coding-harness-vg9).

These move the current roadmap theme **Stage 2 that can be trusted**.
The refactor is a reserve, not permission to mix it into either active change.
Leantime remains a separately recorded, unstarted qualification proposal
(coding-harness-al8); no installation or tracker replacement is in this queue.

## Time envelope

T0 is the recorded start of the proposed run after the allowance reset is
actually observed. Record both UTC and Europe/Berlin; use relative limits
until then. A running conversation, available execution tools and allowance
are prerequisites, not a guarantee of 18 hours of uninterrupted operation.

| Relative window | Work | Required result or stop |
|---|---|---|
| T0 to T0 + 3 h | Reachable review ladder | Tested correction and fresh independent verdict; otherwise a pushed draft checkpoint with the blocker named. |
| Next, no later than T0 + 15 h | Research-swarm implementation, up to 12 h of the operational window | Green slices and explicit remaining acceptance gaps; stop at the change's own remaining phase-4 appetite if earlier. |
| Reserve, no later than T0 + 17 h | Runner-refactor research, up to 2 h | Cohesive module boundaries, dependency risks and a proposed first slice; no implementation or new architectural decision. |
| Final hour, or earlier at any hard stop | Recovery check and handover | Tracker synchronized before Git, clean/pushed checkpoints, current PRs and one-page morning entry point. |

These windows are upper bounds and move earlier when work finishes or stops;
do not wait to fill them. The 18-hour envelope does not increase a change's
appetite. The research-swarm total remains **13 hours 20 minutes**, including
historical measured work and later repair/verification waits. Its historical
gap remains unmeasured, not zero. Read its current plan before calculating
the remainder and record every new span.

At 10 percent remaining in the active five-hour allowance, stop starting large
new calls and prepare the checkpoint/handover. At about 5 percent remaining,
end work as the maintainer requested. A future reset is used only after it
is observed; it never resets a change's appetite or completed review stages.

## Queue entry 1 — reachable review ladder

Start from the checked review worktree and current PR head, not main's old
runner. At this plan's preparation on 2026-10-17, `20f976e` passed the complete
runner verification in the first fresh Sol repair attempt. `bb8b5e1` adds a
reproduced remaining fault: copying Pi's fresh model store still loses new
definitions when its server modification date is absent/invalid or older
than Pi's shipped model data (P6-14; reopens P6-12 with new evidence).

1. Repair only the taken remaining fault through the worktree's
   `.venv/bin/python scripts/stage2.py repair loop-until-clean`. Require a
   real-pinned-runtime regression proving actual API/endpoint resolution,
   including missing and older dates, without inventing server-date evidence.
2. Require full local verification and preserve its measured evidence. Push
   the tracker first, then the green source checkpoint.
3. Run a **fresh read-only** Sol review through `stage2.py review`; its own
   reviewer session never repairs. Triage real findings, repeat within the
   limits, and keep the PR draft until the expanded scope is reviewed.
4. Stop at a reviewed, CI-green PR awaiting the maintainer, or a clearly named
   blocker. No merge; close the implementation bead only after the intended
   merge condition is met.

The existing phase-4b run is spent and released. Do not reset it to replay the
new preparation logic. General availability preflight is proposed in this
decision PR; a catalog-listed id gains no new terms or data permission.

## Queue entry 2 — research swarm

Resume `explore/research-swarm` at its checked head. At preparation it is
`e9ec953`, with a green wrapper/fixture checkpoint, not the completed amended
subsystem. Follow its accepted spec/design/plan rather than the old six-pair
implementation or its obsolete passing tests.

1. Write the plan's red-first amended-graph fixtures: **39 + 3N** slots,
   finder barrier, 24 repository contributions, 9 + 3N online contributions,
   identical per-topic tasks, N=0 and no free-model private roles.
2. Build the fresh Go-only catalog and exact models.dev capability intersection
   with real-pinned-Pi offline fixtures, one shared 60-second bound, explicit
   missing/malformed/duplicate/deprecated cases and audited exclusions.
3. Continue frozen packets, finder/merge stages, typed evidence, provider queues
   and the research-to-interview-to-spec checks in the plan's order. Every
   completed slice gets relevant tests, full verification where required,
   measured time, a commit/push and a `Resume:` line.

Do not call the partial feature complete because its earlier tests pass.
Keep PR #158 draft until the amended acceptance criteria and required reviews
hold. Live roles still requiring exhausted Claude budget are a stop for live
qualification. The attended real-Pi isolation capture still requires the
maintainer present; do not silently waive it overnight. Offline concurrency
tests may use local doubles; the night orchestrator starts only one actual
foreign-model call at a time and does not activate a live parallel swarm.

## Execution and stop rules

- Work only in separate worktrees under `.claude/worktrees/`, from a freshly
  fetched base for each new change. Preserve existing branch ancestry.
  Never edit the main checkout or the customer instance.
- All implementation uses Sol 6.1 while Claude budget is exhausted. Foreign
  calls go exclusively through the worktree's `stage2.py`. Prevent its
  automatic Claude fallback for this run; if that guard is unavailable, do
  not start a verb that can call Claude. No GLM call or probe before
  **2026-10-21 20:34 Asia/Singapore (12:34 UTC)**.
- Check actual availability and report the admitted selection in the main
  conversation where the applicable approved runner policy requires it.
  Reachability is dated evidence, not admission, billing or quality proof.
- One queue item and one worker/model invocation at a time. No new agent
  swarm. Parent orchestration does not become another tracker writer.
- Before tracker writes, check for another writing session. If one exists,
  respect the one-writer rule and leave tracker updates to its owner.
- A leak BLOCK ends foreign calls immediately, without fallback. Preserve
  evidence; continue only independent offline work that does not repeat the
  blocked action. Never read/print credential files or run auth-export commands.
- Two failed repairs, an exhausted appetite, unavailable required runtime,
  missing human decision, or an unresolved ambiguity stops that queue item.
  Record the reason and move to the next independent prepared item. Do not
  ask unattended questions or make up an answer.
- No merge, force push, amend, bare stash, customer access, paid installation,
  new model admission or architectural decision. No automatic Zen admission.
- Before restarting after a pause: read the latest handover/addenda, fetch,
  inspect PR states, local/upstream commits, worktrees and tracker ownership.
  Resume the last green step; never assume a process or budget reset occurred.

## Final handover and acceptance

Use the repository handover convention in its own worktree and PR; preserve
all earlier entries and append a dated addendum. The morning entry point has
at most three priorities, PRs awaiting merge, blockers and their reasons,
the roadmap theme moved, and one concrete resumption action. Link the source
evidence rather than duplicate the tracker. Show what is proposed,
implemented, tested and still not read/measured.

Each active worker record names its branch, last pushed commit and next step,
ending with `Resume:`. Check Git status and upstream distance for every touched
worktree, push tracker data before Git, and record any remaining uncommitted
or unpushed work explicitly. A stopped item is an accurate checkpoint, not a
claim of completion. The maintainer performs every merge.
