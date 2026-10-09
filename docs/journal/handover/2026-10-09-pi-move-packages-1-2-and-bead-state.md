---
title: "Session handover — the Pi move after work packages 1 and 2, and the bead changes, as of 2026-10-09"
category: handover
created: 2026-10-09
updated: 2026-10-09
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-09"
tags: [handover, stage-2, pi, session, tracker]
target_ref: 85b90fa
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

As of 2026-10-09, `main` is at `1973c61`: the maintainer merged #109, so the
remote session's handover, the Pi plan and the addendum to the night handover
are on `main`. On top of that, branch `feat/stage2-session-pi` carries the two
first work packages of the plan to move `stage2.py session` from the OpenCode
CLI to Pi (`docs/research/2026-10-09-session-verb-on-pi-plan.md`):

1. **The interview (package 1).** The maintainer answered the six questions
   and approved the plan; the answers are Q-1 to Q-6 in
   `plans/changes/stage2-session/decisions.md`. Two differ from the
   recommendation: Q-2 (the shell asks only on dangerous patterns, not on every
   call) and Q-6 (the session signs in through the maintainer's own
   `~/.pi/agent`, not a dedicated directory). The record says what each costs.
2. **The artefacts (package 2).** Spec, design, plan, research, findings and the
   unmerged ADR 0007 session amendment draft of `plans/changes/stage2-session`
   describe a Pi launch; the first build's record stays as written with dated
   addenda.

**The code is unchanged.** `scripts/stage2_session.py` still starts OpenCode
until package 4. The documents on this branch describe the target, not the
state of the runner.

## Next step

Package 3: the policy extension and its handler tests, run without Pi and
without a model, on a branch of its own from this one (the packages stack: 3 and
4 change code, 1 and 2 are documents). Then package 4 (the runner port),
package 5 (docs), package 6 (the one decision pull request: the ADR amendment
moves to `docs/adr/`, so the five-answer duty of the gate `interview-minimums`
applies and Q-1 to Q-6 meet it) and package 7 (the smoke test on the Mac).

## Needed from the maintainer

1. Merge the pull request of `feat/stage2-session-pi` when CI is green, if the
   documents read right. It decides nothing: the amendment is still a draft in
   its change folder.
2. A way to push the tracker (below). The second attempt on 2026-10-09 failed
   as the first did.
3. The Mac smoke test of package 7, later.

## Decisions and preferences (maintainer, 2026-10-09)

- No more OpenCode CLI; the OpenCode Go service stays.
- Q-1 to Q-6 as recorded. The sign-in through `~/.pi/agent` means a Pi session
  can switch to any provider whose credential is stored there; the existing
  limit that a model switched inside the session is not leak-checked therefore
  matters more than it did with a dedicated directory.
- Cost tracking is not needed (subscriptions).

## Bead changes

The remote session wrote these in its own container only. `tools/bd dolt push`
fails with HTTP 403 on `refs/dolt/data` (exit 1; tried again on 2026-10-09 after
the maintainer's `/clear`, same result). Origin still shows the left column.

| Bead | On origin (GitHub) | In the remote container | What to replay |
|---|---|---|---|
| coding-harness-ymx (MiMo as reviewer, #105) | in progress, assignee `opencode` | closed (`--force`) | close |
| coding-harness-6yg (mandatory interviews, #104) | in progress, assignee `cline-interview-minimums` | closed (`--force`) | close |
| coding-harness-kw0 (measure the first three runs) | open | closed, cost gap named | close |
| coding-harness-0al (OpenCode 2.x bug) | open | closed, superseded by the Pi bead | comment, supersede |
| the Pi bead (local id coding-harness-6h4) | absent | open, not yet claimed | create, then claim and comment |

The exact commands for the first four rows are in
`docs/journal/handover/2026-10-09-remote-session-merges-tracker-and-pi-plan.md`,
"Pending tracker writes" (on `main` since #109). They read the Pi bead's id from
the output of `tools/bd create`, because it is derived and differs on another
machine. After them, claim the Pi bead and leave the handover comment, with the
id in `$NEW`:

```bash
tools/bd update "$NEW" --claim
tools/bd comment "$NEW" "2026-10-09: work packages 1 and 2 of docs/research/2026-10-09-session-verb-on-pi-plan.md are done on branch feat/stage2-session-pi (the six maintainer answers Q-1 to Q-6 in plans/changes/stage2-session/decisions.md; spec, design, plan, research and the ADR 0007 amendment draft re-pointed to Pi). The code is unchanged. Next: package 3, the policy extension and its handler tests. Two answers differ from the recommendation: Q-2 (shell asks only on dangerous patterns) and Q-6 (sign-in through the maintainer's own ~/.pi/agent)."
tools/bd dolt push
```

Not changed in the tracker: coding-harness-rwa (GLM through Pi) and
coding-harness-36z (D-60 write guard) still wait for decisions.

## Working state and parallel-session boundary

- The remote container holds the checkout of `main` and the worktrees
  `.claude/worktrees/0al-prep` (its branch is merged; it can be removed) and
  `.claude/worktrees/stage2-session-pi` (this branch). They go with the
  container; everything that matters is on origin except the tracker writes.
- No other session was running on 2026-10-09, per the maintainer.

## Validation

- `make verify` on this branch at `85b90fa` (main merged in): green, 1365
  passed, 26 skipped; `docs-links` and `markdownlint` red as report-only.
- Not run: any Pi code, the policy extension (not yet written), the runner
  port, the tracker replay.
