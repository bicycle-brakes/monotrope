---
title: "Session handover — night queue after stage-2 run counts (kw0), as of 2026-10-09"
category: handover
created: 2026-10-09
updated: 2026-10-09
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-09"
tags: [handover, stage-2, night-run, tracker-claim, parallel-session]
target_ref: 3692a42
bead: coding-harness-kw0
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

As of 2026-10-09, `main` is at `0fddb33` (pull request #104 merged). Three
pull requests are open: #105 (`decide(stage2)`, the MiMo review loop, a
decision pull request, CI green, merge state BLOCKED, cause not read), #106
(bead coding-harness-kw0, stage-2 run counts, CI green at `3692a42`, merge
state BEHIND `main`) and #107 (cloud environment setup script, not written by
this session). Of the night queue, only item 1 (kw0) was done; items 2 to 4
were not started. The night agent for kw0 stopped twice on the session budget
and its last commit is `3692a42`; no live agent of this session was found when
this file was written.

## Next step

Read pull request #105 and its blocking check (`gh pr view 105 --json
mergeStateStatus,statusCheckRollup`), then start queue item 2 (bead
coding-harness-0al, `stage2.py session` under OpenCode 2.x): create a worktree
from a freshly fetched `origin/main`, run `make venv`, and reproduce the
failure by calling `opencode --pure debug agent <agent>` with both binaries
(`~/.opencode/bin/opencode`, v2.0.24, and `/opt/homebrew/bin/opencode`,
1.18.35), so that the failure is measured before any fix.

## Needed from the maintainer

1. **Merge order.** #106 (kw0) has no dependency on #105 and can merge first.
   #105 is a decision pull request: it takes effect only when you merge it
   (ADR 0008). Recommended: merge #106 after a rebase onto `main`, then decide
   #105. Consequence: each merge makes the other pull request's branch stale.
2. **Bead coding-harness-kw0 status.** This session claimed it in the tracker
   on 2026-10-09 (`tools/bd update --claim`). Closing it belongs with the
   merge of #106. Nothing else in the tracker was written by this session.
3. **Items 3 and 4 need a decision first, not overnight work:**
   - coding-harness-36z (P1, D-60 write guard) waits for ADR 0005 to be
     accepted by you before any policy is used.
   - coding-harness-rwa (P3, GLM through Pi) needs a decision pull request,
     because ADR 0007 binds GLM to Claude Code, and a measured confinement
     before any write-capable run.

## Decisions and preferences

- The maintainer's rules from the night: one change at a time, few agents,
  visible queue; nothing is merged by an agent; handovers come as pull
  requests; the Haupt-Checkout of `coding-harness` is not written while another
  session is in it (house rule 4 and the parallel-session rule of AGENTS.md).
- Queue for the night, in this order: 1 kw0 (done), 2 coding-harness-0al,
  3 coding-harness-rwa, 4 coding-harness-36z. Items 3 and 4 wait for the
  decisions named above.
- Phase-6 review (Codex) stays after the loop: the stage-2 runs so far show
  Codex finding BLOCKERs the loop did not.

## Open work and blockers

Task status is in Beads. Relevant beads, with their titles:

- coding-harness-kw0 — Stage 2: measure the first three runs. Claimed by this
  session; pull request #106 open; the bead's acceptance also asks for tokens
  and cost per vendor, which the runner does not record (open gap).
- coding-harness-0al — stage2.py session: the OpenCode path fails under
  OpenCode 2.x (P2, not started).
- coding-harness-rwa — Stage 2: GLM through Pi instead of Claude Code (P3, not
  started; needs decision).
- coding-harness-36z — D-60 write guard (P1, not started; needs ADR 0005
  accepted).
- coding-harness-ymx — Stage 2: MiMo as an additional reviewer, pull request
  #105 open, waiting for your merge.

## Working state and parallel-session boundary

- **For the remote session:** this file is the handover for the remote session
  of the maintainer. That session reads only `origin`: it does not see the
  local worktrees named below, the local scratchpad ledger or the local
  primary checkout. Start from `git fetch` and the pull requests #105, #106
  and this handover's pull request. Use `gh` for pull request state, and
  `tools/bd show <id>` (read only) for beads.

- Primary checkout `/Users/mikypiky/coding-harness`: branch `main`, HEAD
  `2dd8e96` at session start; not touched by this session during the night.
  A session scan at the time of writing showed a second session named
  `coding-harness-70` in this same checkout in state "wartet" (waiting). Its
  work is not read by this session; PR #107 (cloud environment script, created
  2026-10-09 09:52) may be its work, which is not verified.
- Other sessions in `lakeswitch-ai` (three rows of the scan, state "wartet")
  were not touched.
- Worktrees made by this session: `.claude/worktrees/stage2-runs-count`
  (branch `feat/stage2-runs-count`, PR #106) and
  `.claude/worktrees/handover-2026-10-09-night` (branch
  `docs/handover-2026-10-09-night`, this file's pull request).
- Night agent ledger (scratchpad, not in the repository): one row, the kw0
  agent, last pushed commit `3692a42`, next step closed.
- Uncommitted changes in the primary checkout: not read by this session.

## Validation

- `make verify` on `feat/stage2-runs-count` at `3692a42`, measured 2026-10-09:
  green, 1291 passed, 16 skipped.
- CI on #106 at `3692a42`, 2026-10-09: `gates (3.11)`, `gates (3.12)` and
  `verify` passed.
- CI on #105 at `80df3ff`, 2026-10-09: `gates` and `verify` passed; the merge
  state is BLOCKED, the reason was not read.
- Not run: any test of items 2 to 4 (not started); the session smoke of
  `stage2.py session` under a real Terminal (not run); the cost measurement
  (not possible with the runner as it is).
- `python3 -m pytest tests/test_feedback_channel.py -q` on this handover:
  see the pull request text for the result.

## Addendum 2026-10-09 (later, remote session): the next step above is superseded

Written by the maintainer's remote session after the merges; the text above
stays as it was.

- **Do not start with coding-harness-0al.** The maintainer decided on
  2026-10-09 to use no more OpenCode CLI ("ich will keine opencode mehr
  benutzen") and to move `stage2.py session` to Pi. The measurement against
  the two OpenCode binaries is no longer needed. Queue item 2 is now the Pi
  port: plan in `docs/research/2026-10-09-session-verb-on-pi-plan.md`
  (proposed, not yet approved, six interview questions open), assessment in
  the addendum of `docs/journal/handover/2026-10-09-0al-local-start.md`.
- **The merges are done**, in the order this file recommended and asked for
  by the maintainer: #108, #107, #106 and #105. `main` is at `7afa5b8`.
- **coding-harness-kw0** is decided: cost tracking is not needed because the
  work runs on subscriptions, so it closes with that gap named.
- **#107 was not the parallel session's work.** It came from the maintainer's
  remote session (the cloud environment's setup script).
- **The tracker on origin does not show any of this yet.** The remote session
  closed coding-harness-ymx, coding-harness-6yg and coding-harness-kw0,
  superseded coding-harness-0al and created the Pi bead in its own container,
  but `tools/bd dolt push` failed there (HTTP 403). Until the commands in
  `docs/journal/handover/2026-10-09-remote-session-merges-tracker-and-pi-plan.md`
  ("Pending tracker writes") are replayed where the push works, `tools/bd
  ready` still lists 0al and kw0 as open. Read that file next.
