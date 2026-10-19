---
title: "Night-run plan — 2026-10-18/19"
category: research
created: 2026-10-18
updated: 2026-10-18
last_reviewed: 2026-10-18
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-18"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [night-run, plan, stage-2, handover]
---

# Night-run plan — 2026-10-18/19

**Proposed operational plan, not an execution report.** The maintainer asked
on 2026-10-18 (about 20:15 UTC) to plan tonight's session. It follows the
[night-run concept](2026-10-12-night-run.md) as a **rehearsal**: one
orchestrating Claude Code session left running, a queue set in advance,
every result a pull request, no merge. It grants no new model, architecture,
merge or deployment permission. Task state stays in Beads. Making this form a
standing routine is its own work item (coding-harness-yuw.2).

## Three priorities

1. Bring the research swarm (coding-harness-icw, draft
   [PR #158](https://github.com/MPAdesso/coding-harness/pull/158)) up to date
   with main, then implement plan step 12: durable per-slot results and resume
   after an abort (decision Q-13).
2. Continue the research swarm's open plan steps in green, pushed slices
   until its appetite or the night ends.
3. Leave pushed checkpoints, accurate pull requests and one morning handover
   by 08:00 Europe/Berlin.

## Starting state (measured 2026-10-18, 20:17 UTC)

- Merged today on the maintainer's request: #157 (loop until clean), #159,
  #160, #161. #162–#164 are being merged by a sub-agent; any one still open
  at 22:30 Europe/Berlin stays open for the morning.
- Research swarm at `f4665fe`: plan step 11 (seat selection with a live
  substitute pool) is done; full `make verify` green at `e386d25`
  (2679 passed, 16 skipped).
- Appetite: 17 h 20 min in total; about 5 h 55 min measured; about
  11 h 25 min remain. Step 12 is estimated at about 2 h; the older open work
  (run wiring, role prompts, handoff gate, doctrine, kit, CI) at 7 to 8 h —
  estimates, not measured.
- Claude session budget: 49 % used at about 19:20 UTC, resets 22:30
  Europe/Berlin; then two five-hour windows cover the night. Codex is
  available again (maintainer, 2026-10-18). GLM through Z.ai stays off until
  2026-10-21 20:34 Asia/Singapore; GLM through OpenCode Go works.

## Queue

| # | Item | Worker | Done when, or stop |
|---|---|---|---|
| 0 | Merge main into `explore/research-swarm`; reconcile the add/add file `scripts/stage2_availability.py` (#157's and step 11's version) | Orchestrator or Sonnet sub-agent | One reconciled module, focused tests and full `make verify` green, pushed |
| 1 | Narrow #157's GLM exclusion in `model-endpoints.yaml` to the Z.ai route only, with its test | Sonnet sub-agent, own worktree from main | Test red first, then green; `make verify` green; pull request open, not merged |
| 2 | Research swarm plan step 12: durable slot results outside the repository, exact-binding reuse, resume | Sonnet sub-agent | Red-first tests for its criteria, green, measured span in `plan.md`, pushed |
| 3 | Research swarm open steps in plan order: wire finder, topics, reports, judge and publication into the run (steps 2–5, 7, 8); handoff gate (step 9); doctrine, kit and CI (step 10) | Sonnet sub-agents, one slice at a time | Each slice green and pushed with a `Resume:` line; stop at the appetite |
| 4 | Reserve, only if 2–3 stop early: measure where hosted CI time goes (coding-harness-7so) — job and test durations, no change | Haiku sub-agent | A dated measurement note in the bead; no CI change |
| 5 | Morning handover | Orchestrator | A dated file under `docs/journal/handover/` as a pull request by 08:00 Europe/Berlin |

Items run strictly one after another. Item 1 may run while item 0's
`make verify` runs, because it lives in its own worktree and branch.

## Not tonight

- No merge of any pull request, including #158 and item 1's.
- No live research swarm run and no real foreign-model call from the swarm;
  offline tests and local doubles only.
- The attended real-Pi isolation capture (plan step 6, finding F-1) needs
  the maintainer present.
- Phase-6 review of #158 only if every plan step is done; then a fresh
  read-only Codex session through `stage2.py review`, its findings triaged in
  the morning.

## Stop rules

- At 10 % of a five-hour window left, start no new large step; at about 5 %
  checkpoint and wait for the reset.
- Two failed repairs, an exhausted appetite, a missing maintainer decision
  or an unresolved ambiguity stop that item; record the reason and go on with
  the next independent item. No question is asked overnight and no answer is
  invented.
- A leak-check BLOCK ends foreign calls without fallback.
- Tracker first, git second. The orchestrator is the only tracker writer; it
  writes a checkpoint comment on coding-harness-icw after each green step
  and only while no `make verify` runs.
- No force push, amend, bare stash, customer instance or secret read.

## Morning page (08:00 Europe/Berlin)

One page: three priorities for the day, pull requests awaiting merge, where
work stopped and why, measured spans against the appetite, and the time the
morning review took.
