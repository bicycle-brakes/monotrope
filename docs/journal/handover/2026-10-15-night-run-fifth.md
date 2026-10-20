---
title: "Session handover — fifth night run, as of 2026-10-15"
category: handover
created: 2026-10-15
updated: 2026-10-15
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-15"
tags: [handover, session, night-run]
target_ref: origin/main
bead: coding-harness-yuw
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Morning handover — fifth night run, 2026-10-16

This page is written in two steps, like the fourth night's. Tonight it holds
what the day finished and the queue the night works; in the morning the four
sections of the night-run form replace the "filled in the morning" lines
(`docs/research/2026-10-12-night-run.md`, "Morning, 08:00"). Later facts are
added as dated addenda; nothing above them is rewritten.

## Done on 2026-10-15, before the night

- **The runner's own pinned Pi is merged** (PR #149, merge commit `135f029`,
  merged by the maintainer at about 23:27). `scripts/stage2.py` starts Pi only
  through `tools/pi/pi`: an exact pin of `@earendil-works/pi-coding-agent`
  1.2.0 in a lock-file install with lifecycle scripts off. A contract suite
  runs the real Pi offline, locally and in CI, and never skips. ADR 0019
  amends ADR 0011 decision 6 and ADR 0012 (bead coding-harness-agx, closed).
- **How it got there.** The runner's implement failed three attempts (GLM
  5.3 Flash twice, Sonnet 5.5 once): the wrapper was not executable, the lock
  file and the install were missing. A Sonnet sub-agent finished phase 4; it
  hit the session limit before it reported, but every step was committed and
  pushed. Phase 6 (Opus 5.5, high) found one BLOCKER (the discovery-trap test
  could not fail), three MAJOR and ten smaller rows. The runner's repair
  failed three attempts; the maintainer chose (option A, 2026-10-15) that the
  orchestrating session completes the rows by hand. Round 2 (Opus 5.5)
  confirmed every row fixed by mutation runs and left no open BLOCKER. The
  record is `plans/changes/pi-pin/findings.md` on `main`.
- **Earlier in the day:** PRs #143, #144 to #147 and #148 (ADR 0018, every
  question carries its context) were merged; beads coding-harness-yzk,
  coding-harness-eao and coding-harness-zs7 closed.
- **New bead from the review:** the runner's red-first check counts a missing
  Pi install as red, so a test-only repair of a real-Pi test passes it without
  any red run (bead coding-harness-omp, P1).

## The queue (maintainer, 2026-10-15)

The maintainer asked at about 23:30 to "continue with the most sensible" and
to hand over at the end of the session. Earlier the same day the maintainer pre-approved
the night merge of the pull requests of five beads (items 1 to 5): a Haiku 5.5
sub-agent merges with `gh pr merge <n> --merge --match-head-commit <sha>` on
two conditions, no open BLOCKER after the phase-6 Opus review and green CI;
never a decision PR; merges in sequence, each branch from the previous merge.

One orchestrating Claude Code session works the queue strictly in order, one
model call or sub-agent at a time. Each plan card stands in its branch's
`plan.md` ("starts unless you say stop") and is listed in the morning.

| # | Bead | Change | Branch | Ends at |
|---|---|---|---|---|
| 1 | coding-harness-ugi | The repair answer parser counts only lines whose id is a taken row's id, and a hand-repaired row is not demanded again | `explore/repair-fixed-lines` | merge (pre-approved) |
| 2 | coding-harness-t83 | The repair prompt forbids handover and journal files; stray paths are put back or refused | — | merge (pre-approved) |
| 3 | coding-harness-6jg | A review-loop round with non-conforming row ids refuses or renumbers, never reports a clean round | — | merge (pre-approved) |
| 4 | coding-harness-ll5 | The `Broke a test` cell: name the allowed values, or accept a reason | — | merge (pre-approved) |
| 5 | coding-harness-k2r | The interview-minimums gate ignores fenced examples | — | merge (pre-approved) |
| 6 | coding-harness-omp | The red-first check sees the pinned install | — | pull request |
| 7 | coding-harness-8hr | Failed-check diagnostics stop copying test secrets into `findings.md` | — | pull request |

Why this order: the repair path (items 1 and 2) failed every runner repair
of 2026-10-15, and each later change needs it; items 3 to 5 follow the
pre-approval's priorities; items 6 and 7 are P1 but not pre-approved, so
they end at a pull request. Estimate, not measured: a small change takes
1.5 to 3 hours, so the night reaches two or three items.

### Waiting for the maintainer (not in the night)

- **coding-harness-0ho** (red-first exception for fixes that live only in
  test code; branch `explore/guard-test` at `4697c4e`, 24 commits behind
  `main`): its plan owes four interview answers (Q-2 to Q-5) for an ADR 0017
  addendum before phase 4.
- **coding-harness-6ie with coding-harness-s9r** (attempts keep the earlier
  attempt's edits; isolated attempts): one shared design; open question
  whether a failed GLM call falls through to Sonnet 5.5 instead of reverting.
- **coding-harness-icw** (phase 1 as a research swarm, branch
  `explore/research-swarm` at `afdc993`): merge `main` in, `make verify`,
  then phase 2a.

### Rules for this night

- **Stops.** Red `make verify` after two repairs, a leak-check BLOCK, or a
  question only the maintainer can answer: written down here, the next item
  starts.
- **No tracker write while a draft check or `make verify` runs** in any
  worktree; the tracker goes first, git second (house rule 4).
- **Every new worktree** runs `make venv` (or the pinned venv command) and,
  since PR #149, `bash tools/pi/install.sh` once (Node 26; about 148 MB);
  without the install the real-Pi contracts fail `make verify`.
- **Merges** only through a Haiku 5.5 sub-agent and only for items 1 to 5;
  `.claude/settings.json` may ask before a merge, and that brake is not
  bypassed.

### Lessons of 2026-10-15 the night applies

- The repair runner cannot pass a fix that lives only in test code (red
  first), misreads report words such as `expected:` and `Resume:` as finding
  ids, and demands hand-repaired rows again (items 1 and 6, bead 0ho).
- A sub-agent can stop on the session limit mid-work; its pushed commits
  stay, and the orchestrator re-runs the gate before trusting the state.
- The disk ran full earlier in the day; 15 GiB were free at about 23:55.

## 1. The three priorities for today

Filled in the morning.

## 2. Done — waiting for your merge

Filled in the morning.

## 3. Stuck: where, and why

Filled in the morning.

## 4. Resume

Filled in the morning.
