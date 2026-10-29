---
title: "Night-run plan — 2026-10-29/30"
category: research
created: 2026-10-29
updated: 2026-10-29
last_reviewed: 2026-10-29
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-4emv
tags: [night-run, plan, lanes, stage-2]
---

# Night-run plan — 2026-10-29/30

**This is the plan for tonight. It does not report a run.** The maintainer
asked for it on 2026-10-29 at about 22:00 UTC ("erstelle einen Nachtplan und
ziehe diesen durch"). It follows the
[plan of 2026-10-28](2026-10-28-night-run-plan.md) and keeps its rules. One
orchestrating Claude Code session works three lanes until 07:00 UTC, then
hands over. The plan grants no new model, architecture or deployment
permission. Task state stays in Beads.

## State at the start

Measured 2026-10-29 at about 22:05 UTC against `main` `635e9bd1`. The day's
orchestrating session stopped at 20:05 UTC at the Claude five-hour limit,
with three lane sub-agents. This session takes over as the only tracker
writer; no other session runs in this repository.

| Lane | Change (bead) | Branch, head | State |
| --- | --- | --- | --- |
| A | `fail-fast-attempts` (coding-harness-5tyh) | `fix/fail-fast-attempts`, `4dfccd10` | PR #279; a CI-only test fault fixed, full `make verify` green; push and CI pending |
| A | `verify-machine-lock` (coding-harness-p6mu) | `fix/verify-machine-lock`, `428c9c1c` | review round 1 decided and repaired by hand; appetite 6.0 h (maintainer, 2026-10-29) |
| A | `review-diff-order` (coding-harness-ut8q) | `fix/review-diff-order`, `fdcaaa4b` | parked; maintainer: the plan drops the prompt edit, +45 min |
| B | `run-report` (coding-harness-o2yc) | `feat/run-report`, `48805a1e` | PR #277; phase-6 rows R6-4, R6-5 repaired, not pushed, not verified; +40 min granted |
| C | `index-merge-regenerates` (coding-harness-njtm, -hfsz, -eq6y) | `fix/index-merge-regenerates`, `7d2f7399` | round 6 rows repaired; a round-7 call was cut off when the session stopped |

Waiting on the maintainer, not worked tonight: the decision PRs #280 (a
`docs` gate job, bead coding-harness-77qj) and #281 (guard test, ADR 0023,
beads coding-harness-0ho and -y17), and the plan card of `pi-neutral-paths`
(coding-harness-xul8).

## Rules tonight

The rules of the 2026-10-28 plan hold unchanged:

- one verify-bearing step at a time;
- the appetite is a stop;
- a feature change runs explore only;
- no merges;
- a leak-check BLOCK or a security BLOCKER stops the run.

Three additions from the day:

1. **The verify slot is a file lock.** Every verify-bearing step (implement,
   repair, draft, the orchestrator's full verify) runs under
   `/usr/bin/lockf -k ~/.local/state/coding-harness/verify-manual.lock`, as
   the day's lanes did. A second one queues on the lock instead of
   overlapping.
2. **No lane sub-agents.** The day's three sub-agents and the orchestrator
   used the Claude budget up by 20:05 UTC. Tonight the orchestrator starts
   the runner's verbs itself as background calls and decides rows itself.
3. **Hot files.**
   - Only lane A changes `scripts/stage2.py` and `scripts/verify_all.sh`
     (verify-machine-lock changes the latter).
   - Lane B's later item is explored and drafted only, because it touches
     `scripts/verify_all.sh`.

## Lanes

**Lane A — the runner.**

1. `fail-fast-attempts`: push, CI green, PR #279 marked ready.
2. `verify-machine-lock`:
   - a full verify of the round-1 repairs;
   - review round 2 and further rounds while the appetite holds;
   - phase 6, then the PR.
3. `review-diff-order`:
   - revise the plan as the maintainer decided;
   - implement within the 45 minutes;
   - loop, phase 6, PR.

**Lane B — reports and machine load.**

1. `run-report`:
   - full verify of `48805a1e`, then push;
   - phase-6 re-check, then PR #277 marked ready.
2. `make verify` caps pytest workers per machine (coding-harness-l7sc,
   bounded): explore, then draft. Implement waits for lane A's
   verify-machine-lock, which changes the same script.

**Lane C — merges and plans.**

1. `index-merge-regenerates`:
   - the cut-off call's output committed unchanged;
   - review rounds until clean or the appetite;
   - phase 6, PR.
2. The plan template names the paths a stage-2 run does not commit
   (coding-harness-h5tj, bounded): explore, draft, implement, PR.

Fallback when a lane runs dry: the explore of model data terms
(coding-harness-3g53, a feature, explore only) in lane C.

## Morning

By 07:00 UTC a handover from its own worktree lists:

- the ready PRs with their full head SHAs;
- the parked items, each with a proposal;
- one question block.
