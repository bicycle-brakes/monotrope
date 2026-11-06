---
title: "Session handover — seven lanes, night 2026-11-04/05 and day 2026-11-05, 2026-11-05"
category: handover
created: 2026-11-05
updated: 2026-11-05
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-11-05"
tags: [handover, lanes, night-run, review-loop, stage-2, research-swarm]
target_ref: a8e23d17
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The session ran six implementing lanes plus one lane without make verify
(maintainer, 2026-11-04: "Mach 6 plus 1") through the night and day of
2026-11-04/05, until the maintainer's budget ran out at about 14:50 UTC on
2026-11-05. Three changes merged: Pi 1.5.0 (PR #335), the research swarm's
time limits in a file (PR #336) and the make verify measurement spike
(PR #337). Six changes are in flight in their own worktrees; at the hand-over
each had a runner job still running (listed below), whose result is not read.
The research swarm cannot start on main until bead coding-harness-wb40
merges: after Pi 1.5.0 it selects the paid-admitted `beam-free` as free.

## Next step

Read the six job results (logs under the session scratchpad are gone with
the session; read each worktree's `git log -1` and
`plans/changes/<change>/findings.md`, and each loop record under
`~/.local/state/coding-harness/stage2/<change>@*/loop.md`), then continue each
lane from the table below, starting with lane G (bead coding-harness-wb40),
because it unblocks every research-swarm run.

## Needed from the maintainer

- **Question block, parked:** should a test pin the six decided research-swarm
  limit values (then each value change also edits a test) or only check that
  the file loads and stays in range? (swarm-time-limits loop row L3-1, now
  merged; the test pins the values.) Recommendation: check range only; then
  changing a value is a one-line edit of `research-swarm-limits.yaml`.
- **Decision PR to prepare and merge:** admit kimi-k3.1-pro,
  minimax-m3.1-flash and step-5-preview in `model-endpoints.yaml` (Pi 1.5.0
  carries them since PR #335).
- **Due before 2026-11-16:** the weekly collective terms-renewal PR
  (maintainer, 2026-11-04): longcat-2.0 and glm-5.3-flash expire that day;
  a notice on 2026-11-05 also named mimo-v2.6-pro expiring 2026-11-06 in an
  older worktree — check against main, where #329 renewed it to 2026-12-03.

## Decisions and preferences

Recorded this session, not to be asked again:

- Lanes: six implementing plus one without make verify (2026-11-04); not
  fewer when make verify queues ("Nein" to pausing, 2026-11-04).
- Appetite counts working time only, without verify-lock waits (bead
  coding-harness-po0a, "Nur Arbeitszeit"); report an overrun when it happens.
  Lanes B, C, D, F and A were allowed to run to their pull request without a
  limit; lane E had 2 h of working time from 2026-11-05 08:00 UTC.
- Hand acceptance only for bookkeeping and runner self-repairs; ask from the
  third in one change.
- Implement route to come: DeepSeek V4.1 Flash via Pi, then GLM 5.3 via Claude
  Code, then Sonnet (bead coding-harness-aygo, interview owed). GLM 5.3 Flash
  failed implementation in 5 of 6 changes on 2026-11-04 (a hint, one day).
- 30-day retention is acceptable for framework content when training is not
  used (bead coding-harness-36za widened to the Responses API).
- Weekly collective terms-renewal PR; changed terms go separately.
- Measuring points as a trial: beads coding-harness-eqy2 and
  coding-harness-5qqh, due 2026-11-20.
- A declared paid model is never selected free (pi-catalog-move Q-2); one
  central free selection for the review loop and the research swarm, a one-time
  swarm exception for wb40, and an offline contract test of both preparations
  (research-free-paid Q-1 to Q-3).
- Second or third finding of one mechanism: the maintainer chose the mechanism
  repair each time (gxwg L7-1, in27 L2-1, 1um6 F6-3, nxdy L3-1).
- The runner's audit log moves out of findings.md (bead coding-harness-oebl).
- No Rust or TypeScript rewrite of the runner; clear module interfaces and
  Pydantic models in the split (bead coding-harness-vg9); a runtime is
  evaluated first (beads coding-harness-myuc, coding-harness-tdfj Warp,
  coding-harness-v8qa Temporal); a Python lane planner first (bead
  coding-harness-5q2p).

## Open work and blockers

| Lane | Change (worktree `.claude/worktrees/<change>`) | Bead | State at hand-over (2026-11-05 ~14:50 UTC) |
|---|---|---|---|
| B | research-store-home | coding-harness-nxdy | repair of review round 3 running (maintainer's option A for old store folders) |
| C | conflict-marker-gate | coding-harness-i76l | draft running (second time; the first failed on the orchestrator's skip form, fixed) |
| D | repair-targeted-check | coding-harness-gxwg | repair of phase-6 F6-2 running (stale verification wording in runner strings); then phase 6 again, then PR |
| E | explore-provenance | coding-harness-g19n | repair of round 4 running; afterwards the orchestrator corrects four active research.md files (run-report, interview-context, fail-fast-attempts, go-access-point) — loop row L4-1 |
| F | handoff-new-feature | coding-harness-in27 | repair of round 4 running; its PR is a **decision PR** (it edits decisions/adoption.yaml), merged by the maintainer |
| G | research-free-paid | coding-harness-wb40 | implement running (feature: central free selection plus offline contract test); unblocks the swarm runs of coding-harness-0887, -4mdn, -aygo, -myuc, -tdfj, -v8qa |

Backlog in order: coding-harness-o2s1 (triage verb), coding-harness-kgwu
(tracker cleanup round), coding-harness-0swp, coding-harness-vg9 (after
gxwg), coding-harness-36za, coding-harness-phop, coding-harness-y0qm,
coding-harness-oebl (after gxwg), coding-harness-2ym2, coding-harness-firy,
coding-harness-xay1, coding-harness-s3kf, coding-harness-i76x,
coding-harness-n4g5, coding-harness-alq2, coding-harness-068j.

## Working state and parallel-session boundary

- Branches: `feat/research-principle` (bead coding-harness-0887; holds an
  uncommitted incomplete swarm record from 2026-11-04 in research.md, 17,550
  lines, a failed run's envelope — not a result), the six lane branches above,
  this handover branch `docs/handover-2026-11-05`.
- Research-store workaround until nxdy merges:
  `XDG_STATE_HOME=/Users/Shared/mikypiky-stage2-state` for prepare-explore and
  explore together.
- A worktree that merged main after #335 must run `bash tools/pi/install.sh`
  (Pi 1.5.0) before Pi-using steps.
- One session wrote the tracker; no other session was seen (2026-11-05).

## Validation

- Merged with CI green: #335 (full make verify green on 12cc5bd4,
  2026-11-04), #336 (full make verify green on 7aac74ea apart from the
  midnight date stamps; targeted tests after merging main), #337 (five green
  baseline runs on bc2fe411; targeted tests and docs job after merging main).
- Not read: the results of the six runner jobs still running at hand-over.
- Lessons recorded in memory: background jobs only via the harness's
  background mode; appetite checked at every lane status; check a merge's exit
  before committing (merge markers were pushed once, 31d35400, fixed in
  3c4d83eb).

## Addendum — 2026-11-05, ending the session with jobs running

The six runner jobs are children of this Claude Code session; ending the
session most likely stops them mid-attempt (not measured). If a worktree then
shows uncommitted changes and its findings.md has no closing line for the last
attempt, discard the partial attempt (`git checkout -- . && git clean -fd`
inside that worktree only, after reading `git status`) and start the same
verb again; every earlier step is committed and pushed.
