---
title: "Session handover — day of 2026-11-24: interviews, spec reviews, PR #437 audit check"
category: handover
created: 2026-11-24
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-11-24"
tags: [handover, lanes, interviews, spec-review, audit]
target_ref: b9ce3ac0
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
updated: 2026-11-25
---

# Resume here

## Where we are

Session c820a13d (profile `~/.claude-mp`) continued after the night-run handover of this morning (PR #441, merged). Merged today: #439 (GLM 5.4 route), #440 (phase-6 answers in English), #441 (night handover), #442 (close-budget-clock, bead coding-harness-0n4s). #443 (drift-lane-branches, bead coding-harness-l54q) is in the merge queue after a regenerated `plans/INDEX.md` (b3a2d89a). The maintainer answered the interviews of three feature lanes and the open spec questions of four lanes; those lanes are now in phase 2a. The PR #437 audit was checked and turned into epic coding-harness-5ane. Lane log: `~/.local/state/coding-harness/night/2026-11-23-a/lane-watch.log`.

## Next step

1. Read the result of the last phase-6 re-check of repair-scope-guard (bead coding-harness-t83, job started about 15:35 CET, log in the session scratchpad `t83-review-last.log`; the record lands in `plans/changes/repair-scope-guard/findings.md`). Clean: commit the record and open the PR with `Closes-Bead: coding-harness-t83`. The maintainer allowed this one last re-check only.
2. Triage the spec-review rows that arrived at the end of the session (committed unchanged): advance-verb round 2 (13 rows, f016356f) and review-fewer-rounds round 4 (11 rows, 7af30db3; no fifth round exists — after this round the runner requires a re-slice). Design ambiguities go to the maintainer as bundled questions; provisional agent decisions do not count as answers.
3. Run spec-review on the two fresh drafts: isolated-attempts (ad7cf76b) and detached-job-launcher (81248ba2).

## Needed from the maintainer

1. **Bead coding-harness-5ane.1 (P0, due 2026-11-28):** twelve ramp valves in `scripts/ramp_valves.py` fall due on 2026-11-30; from then `tests/test_ramp_valves.py` turns every `make verify` red. Per valve: close, re-date with a reason, or drop.
2. **P1 cap:** 19 non-epic P1 beads against the cap of 10 (AGENTS.md "P1 means planned for the next two weeks, at most 10 beads"); nine need to go back to P2.
3. **PR #437 (audit):** recommendation: append the re-check result (what is wrong or stale, pointer to epic coding-harness-5ane) and merge as research; alternative: close.
4. **Bead coding-harness-5ane.2 priority:** hooks and status line run a repository's own `tools/bd` without a trust check; recommendation P1.
5. Still open from earlier: the provisional decisions of commit-hook-stamp (coding-harness-yv9i.2) and runner-preflight-gates (coding-harness-yv9i.3).

## Decisions and preferences

Recorded today in the change folders (all `answered_by: maintainer`):

- **advance-verb (coding-harness-z40g):** own command `scripts/lanes.py advance`, not a runner verb (modularity); it starts the next step (ADR 0021 amendment); hwll lands first; no lifecycle writes; local state plus an optional change argument; per lane at most two verify-bearing steps (central setting), lanes in sequence, a failure stops only its lane; each step a child process; `next:` line written into the loop record by hwll; own `lanes.yaml` in the runner state directory with park marks (decisions Q-1..Q-12).
- **isolated-attempts (coding-harness-s9r):** new ADR partially superseding ADR 0017 decision 2; writing verbs plus phase-6 `review` through the attempt module; attempt worktrees under `$XDG_STATE_HOME/coding-harness/attempts/` (harness-neutral; supersedes Q-4's $TMPDIR); the module keeps its own CLI offering lifecycle steps only; detect, not prevent, tampering with the linked .venv/Pi; failed attempts are rejected when the lane moved (Q-8..Q-21).
- **detached-job-launcher (coding-harness-a6ns.1):** `scripts/jobs.py` (start/list/stop), each job a window of an own tmux server `coding-harness`; records in `$XDG_STATE_HOME/coding-harness/jobs/`, 14 days; shared verify admission; required for verify-bearing runner jobs; a new ADR (Q-1..Q-11).
- **review-fewer-rounds (coding-harness-3rtn):** one extra phase-6 re-check per confirmed repair (Q-31); all other provisional decisions confirmed (Q-32..Q-36); a fourth spec review authorised (Q-37).
- **repair-scope-guard (coding-harness-t83):** the spec governs (only a trailing `/` grants descendants); P6-11..P6-13 repaired (973e81d0); one last re-check.
- General: the maintainer wants modularity and transferability to all harnesses; a location must be valid for every harness, not Claude-specific.

## Open work and blockers

| Lane | Bead | Branch @ head | State |
|---|---|---|---|
| drift-lane-branches | coding-harness-l54q | fix/drift-lane-branches @ b3a2d89a | PR #443 in merge queue |
| repair-scope-guard | coding-harness-t83 | fix/repair-scope-guard @ 973e81d0 | last phase-6 re-check running |
| advance-verb | coding-harness-z40g | feat/advance-verb @ f016356f | spec review round 2: 13 rows to triage |
| review-fewer-rounds | coding-harness-3rtn | feat/review-fewer-rounds @ 7af30db3 | spec review round 4: 11 rows to triage |
| isolated-attempts | coding-harness-s9r | feat/isolated-attempts @ ad7cf76b | redraft done, spec review next |
| detached-job-launcher | coding-harness-a6ns.1 | feat/detached-job-launcher @ 81248ba2 | redraft done, spec review next |
| address-notice-once | coding-harness-zywb | fix/address-notice-once @ 68a44f53 | parked: the attempt's own test conflicts with its fixtures |

New beads: epic coding-harness-5ane with 5ane.1..5ane.15 (audit follow-ups: P0 valves, security, kit, state-first ADR).

## Working state and parallel-session boundary

- This session was the only tracker writer until the maintainer said "bitte schreibe keine beads mehr" (2026-11-24, end of session); since then it wrote no beads. Use `tools/bd` (pinned 1.3.4), never the bare `bd` on PATH (1.1.2): the bare one refuses with a schema-version message that looks like a broken database.
- Worktree `.claude/worktrees/audit-verify` (detached at b9ce3ac0) was only for the audit check; it can be removed.
- The runner jobs run detached with nohup; their logs are in the session scratchpad, their records in each change's findings.md.

## Orchestrator mistakes

- A launch chain ran `git add -A` after a failed implement and committed the attempt's code under "runner records, unchanged" (f9f408f4, address-notice-once, pushed). Reverted by 8bdd9979, which wrongly deleted `scripts/stage2_go.py`; restored by 68a44f53. The tree now equals f9f408f4~1 except findings.md.
- Called the bare `bd` and reported a broken tracker; the database was fine.
- Set phase-6 Origin cells to `implementation`/`test` instead of `base` (refused once); wrote the fourth-spec-review authorisation in a form the runner did not accept (fixed: heading "Fourth spec-review round", answer starting "authorized").

## Validation

- Each runner step above carries its own result line in the lane log and findings.md; research-handoff and interview-minimums checks were green after each decisions.md edit.
- PR #437 check: five read-only Haiku agents against main b9ce3ac0; the P0 valve count (12 on 2026-11-30) and the hook trust gap were re-read directly.
- Not read: the outcome of the last t83 re-check (still running at hand-over).
