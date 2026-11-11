---
title: "Night-run plan — 2026-11-11 evening to 2026-11-12 07:00 UTC"
category: research
created: 2026-11-11
updated: 2026-11-11
last_reviewed: 2026-11-11
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [night-run, plan, lanes, stage-2, make-verify]
---

# Night-run plan 2026-11-11/12

The maintainer asked on 2026-11-11 at about 20:40 UTC for a night plan with
ten lanes ("erstelle einen nachtplan mit 10 lanes"). That widens the six-lane
limit the maintainer set earlier the same day. The plan keeps the rules of
the [night plan of 2026-11-09](2026-11-09-night-run-plan.md) except where
this page says otherwise. One orchestrating session works the lanes and is
the only tracker writer. The state of every lane below was read from the day
handover of 2026-11-11 (`docs/journal/handover/2026-11-11-day-decisions-six-lanes.md`,
pull request #370) and the bead notes at about 20:45 UTC.

## The one limit that matters: three verify-bearing jobs at a time

Ten lanes are ten worktrees with work queued, not ten jobs running at once.
In the night of 2026-11-10/11, twelve lanes queued at the one verify slot:
the median wait was 96 minutes, and a full run under load passed the
runner's 30-minute step limit (handover of 2026-11-11, night). The day
handover names three jobs at a time as the practical ceiling until the limit
is raised or a second slot exists. So:

- **At most three runner jobs that run `make verify`** (implement, repair, a
  draft's documents job, the full check before phase 6) are started at once.
- Review-loop rounds and phase-6 reviews that run no check do not count
  against the three.
- A lane whose next step would be a fourth verify-bearing job waits; the
  wake serves it when a slot frees.

## Start of the session

1. Start Claude Code through the night profile (`python3 ~/.claude/night.py`),
   so a permission question is denied at once instead of holding the run.
2. Create the run state folder
   `~/.local/state/coding-harness/night/2026-11-11-a/` with `lanes.txt`,
   `busy/` and `lane-watch.log`; record the run id in the morning handover.
3. Arm the 30-minute wake and keep the machine awake (`caffeinate -i -t`
   until 07:00 UTC), both as owned background jobs (`docs/WORKFLOW.md`,
   "Night runs").
4. No phone notification at night.

## Before the maintainer sleeps: four plan cards

A plan card waits for the maintainer; at night it cannot be approved, and its
lane parks at the card. These four are shown before the night starts, one at
a time:

1. verify-step-limit (bead coding-harness-xkvr) — once its draft stands
   (started 20:45 UTC).
2. targeted-check-more-verbs (bead coding-harness-0swp) — draft at `ca6ecc0c`.
3. verify-tmp-cleanup — draft at `e6894adc`.
4. no-work-ledger-marker — draft at `00d3a67e`.

A card not approved before the night leaves its lane parked at the card; the
plan still runs.

## Lanes, in priority order

| # | Lane (bead) | Class | Tonight | Stop |
|---|---|---|---|---|
| 1 | verify-step-limit (coding-harness-xkvr) | bounded | implement → review loop → full check → phase 6 → pull request | pull request, or plan card not approved |
| 2 | verify-cheap-first (coding-harness-bxxt.1) | — | review round 4 → phase 6 → decision pull request (held gate list) | decision pull request |
| 3 | midnight-stamp-test (coding-harness-bxxt.5) | — | review round 2 → full check → phase 6 → pull request | pull request |
| 4 | explore-provenance (coding-harness-g19n) | feature | repair EP6-11 and EP6-12 (answers given) → full check → phase-6 re-check | pull request, or a further finding of the same mechanism |
| 5 | targeted-check-more-verbs (coding-harness-0swp) | — | implement → review loop | plan card not approved |
| 6 | swarm-report-format (coding-harness-4q9y) | bounded | review loop from the Flash round (no free-only round, maintainer 2026-11-11) | clean round, then phase 6 |
| 7 | origin-check-across-blocks (coding-harness-3h96) | bounded | repair to answer A: finding ids unique within a change, a check refuses duplicates, the refusal names id and file only | phase-6 verdict |
| 8 | verify-slots (coding-harness-u1ha) | bounded | read the red test `test_targeted_commands_run_without_verify_admission`; rerun the boundary repair only while it is the only job at the verify slot | green repair, or the 30-minute limit again (then park until lane 1 merges) |
| 9 | central-config (coding-harness-twvx) | architectural | redraft: the placeholder is filled when each runner step starts, outside the shared prompt snapshot; the step limit belongs to its limits | plan card (morning) |
| 10 | verify-tmp-cleanup, then no-work-ledger-marker | — | implement once their plan cards are approved, one after the other | plan card not approved |

Lane classes marked "—" were not read tonight.

Not tonight: review-fewer-rounds (coding-harness-3rtn) waits for bead
coding-harness-1gzo and the central configuration.

## Rules carried over and repeated

- **Park, do not ask, at night.** A finding that needs a decision goes into
  the bead notes and the morning handover; the lane leaves the watch list.
- **A second finding of one mechanism parks the lane** (`AGENTS.md`); its
  appetite is enforced at night too (bead coding-harness-bxxt.5 notes).
- **Codex at capacity:** wait four minutes, retry once, then Sonnet 5.5 for
  that one step (`docs/WORKFLOW.md`, "Night runs").
- **Hot file `scripts/stage2.py`:** lanes 1, 5, 7 and 8 touch it. They run on
  separate branches; at most three pull requests per hot file are opened, and
  the morning handover names the merge order.
- **Commit and push after every green step;** tracker push before git push.
- **No `gh pr merge`, no `gh api`** at night.

## Morning

A handover under `docs/journal/handover/` as a pull request, with the lane
table, every parked question under "Needed from the maintainer", and the
verify-slot waits and run times of the night with their cut-off time.
