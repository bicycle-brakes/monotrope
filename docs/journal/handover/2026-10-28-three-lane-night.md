---
title: "Session handover — three-lane day and night trial 2026-10-27/28, 2026-10-28"
category: handover
created: 2026-10-28
updated: 2026-10-28
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-10-28"
tags: [handover, night-run, three-lanes, review-loop, stage-2]
target_ref: 047a4e81
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

From the evening of 2026-10-27 to the morning of 2026-10-28 three changes ran
in parallel lanes as the maintainer's three-lane night trial. One reached its
pull request: the shared terms-record test builder and the load-proof sigkill
test (PR #265, phase 6 clean on re-check, auto-merge armed). The other two
stand on their branches: the red-first classifier change is parked by the
maintainer's answer (a ladder model that answers in the wrong format is not to
be retired), and the workflow-promises package is parked at its appetite stop.
The trial's main measurement: three full `make verify` runs at once on the
8-core machine drive the load average above 100 and past the runner's
30-minute step limit; one at a time, a run takes 11–12 minutes.

## Next step

Put the 15:00 decision block to the maintainer (list under "Needed from the
maintainer"), starting with the two parked lanes, then start bead
coding-harness-5tyh (runner attempts fail fast) in its prepared worktree
`fail-fast-attempts`.

## Needed from the maintainer

One decision at a time, at the 15:00 block:

1. **Workflow-promises lane** (bead coding-harness-i0l with 690, 72w, 7bw):
   appetite of four hours used (13971 s of runner time). Round 6 left five
   small rows, one MAJOR (the kit-probe switch `HARNESS_KIT_PROBE` is
   unscoped). Recommendation: continue with one more hour to close round 6
   and run phase 6. Alternative: cut to what holds now.
2. **Red-first lane** (bead coding-harness-a7m): the loop is stuck on
   glm-5.3-flash answering in the wrong format. The maintainer declined to
   retire it on 2026-10-28. Recommendation: wait for bead
   coding-harness-np8z (format is the runner's job) or allow this one loop to
   pass that stage.
3. DeepSeek terms expire 2026-10-31 (renewal, decision PR).
4. The stop hook (bead coding-harness-788): which check, and how long it may
   hold a turn.
5. Explore cleanup mechanism (bead coding-harness-g19n), the swarm rule for
   evaluation spikes (bead coding-harness-4mdn, ADR 0020 amendment), the
   automatic stage skip for malformed answers (lever 1 of the format
   question), and the P4 list of nine untouched beads.

## Decisions and preferences

- Three lanes by day; at night the trial showed that full verification must
  run one at a time (bead coding-harness-p6mu makes it a lock). Foreign-model
  calls may run beside it.
- New appetite of four hours in total for all three lanes (maintainer,
  2026-10-27).
- Evaluation spikes (outside tools, projects, open practice questions)
  explore through the research swarm, not GLM Flash alone (maintainer,
  2026-10-27; bead coding-harness-4mdn). First live run waits for bead
  coding-harness-xul8.
- Models are never dropped for answer format in the long run (maintainer,
  2026-10-28; bead coding-harness-np8z). glm-5.3-flash was not retired.
- Red-first answer of 2026-10-27 stands: AssertionError and pytest's `Failed`
  count as red; a missing helper does not.

## Open work and blockers

Task state lives in Beads. Created or changed this session:

- coding-harness-5tyh — runner attempts fail fast (cheap checks first,
  pre-mortem tests as a must-run, protected-file edits restored). P1, queue 1.
- coding-harness-p6mu — one `make verify` at a time per machine. P1, queue 2.
- coding-harness-k93f — the runner writes the fixed-line skeleton per taken
  row. P1, queue 3, then package 4 (lead coding-harness-6jg).
- coding-harness-np8z — format is the runner's job (architectural).
- coding-harness-g19n — explore leaves the research.md skeleton in place.
- coding-harness-4mdn — research swarm for evaluation spikes.
- coding-harness-owgi — evaluate free-claude-code; coding-harness-mykz —
  research on an X post by Addy Osmani. Both wait for 4mdn.
- coding-harness-788 — stop hook split out of the i0l package.
- Closed: coding-harness-7av1 and coding-harness-yuw.4 (PR #263).
- PR #265 closes coding-harness-hxkw and coding-harness-jik on merge; close
  them in the tracker after it merges.

Lessons the orchestrator applies from now on (also the reason for 5tyh and
k93f):

- A failed attempt's code edits go to a side ref, not onto the working
  branch; on the branch they become the repair baseline and no red-first
  proof is possible.
- A row whose evidence is a measurement or text is taken as `not a test`,
  and the orchestrator records evidence in `findings.md` itself (the repair
  may not write it). A row whose fix lives in a test is `not a test` too.
- Every taken row needs a fixed line and a `Broke a test` mark before the
  next round.

## Working state and parallel-session boundary

| Worktree | Branch | Head | State |
|---|---|---|---|
| `terms-test-fixtures` | `fix/terms-test-fixtures` | `d8c85644` | PR #265, auto-merge armed, a watcher re-arms after main moves |
| `workflow-promises` | `docs/workflow-promises` | `00854084` | parked at the appetite stop, loop round 6 undecided |
| `red-first-pytest-failed` | `fix/red-first-pytest-failed` | `461859de` | parked, loop round 3 failed twice on format |
| `fail-fast-attempts` | `fix/fail-fast-attempts` | `4439ff43` | change folder only, venv and Pi installed |
| `handover-1028` | `docs/handover-2026-10-28` | this file | handover PR |

All worktrees clean at writing. PR #264 (kit working rules) was re-armed on
its updated head `bf4effc5`. Loop records live outside the repository under
`~/.local/state/coding-harness/stage2/<change>@<digest>/loop.md`. The trial
log is in the session scratchpad (not in the repository). No other session
wrote the tracker.

## Validation

- terms-test-fixtures: three consecutive full `make verify` runs green at
  `98682973` (680–703 s each), one more at `550f3caf`; phase 6 re-check by a
  fresh Codex session (01a18155) found nothing.
- workflow-promises: full `make verify` green at `fe85b3e1` and `fa9bfdf3`;
  not run after round 6.
- red-first-pytest-failed: the three new tests fail with `AssertionError` at
  the baseline `0872d0cc` and pass at `b7048d9c`; no full run after the
  text-only round-1 and round-2 fixes.
- This handover: `tests/test_feedback_channel.py` run before the commit.
