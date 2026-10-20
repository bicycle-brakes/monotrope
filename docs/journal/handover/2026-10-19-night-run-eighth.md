---
title: "Session handover — eighth night run, as of 2026-10-19"
category: handover
created: 2026-10-19
updated: 2026-10-19
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-10-19"
tags: [handover, session, night-run, research-swarm, phase-6]
target_ref: origin/main
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The maintainer restarts the Mac at about 20:30 UTC on 2026-10-19, in the
middle of the night run planned in
[PR #170](https://github.com/MPAdesso/coding-harness/pull/170) (bead
coding-harness-yuw). Queue items 1 to 9 ran; item 10 and the morning page did
not. The research swarm (bead coding-harness-icw, draft
[PR #158](https://github.com/MPAdesso/coding-harness/pull/158)) went through
fresh read-only Codex phase-6 rounds 4, 5 and 6; every row through F-37 is
repaired with a red-first test and `make verify` was green at `96a747c`
(3032 passed, 16 skipped, 19:08 UTC). No round has come back clean yet.

## Next step

Check the hosted CI run on #158 at `b57d109` (it was pending at 20:27 UTC;
the previous run was red only on the spec's stale `updated` date, now
restamped). Then ask the maintainer whether phase-6 round 7 runs.

## Needed from the maintainer

1. **Round 7 for the research swarm (#158)?** Recommended: yes, one more
   fresh read-only Codex round (`stage2.py review research-swarm`) before any
   merge. Rounds 1 to 6 found 8, 5, 3, 3, 3 and 4 rows; F-35 came from a
   round-4 repair, so the repairs themselves still need a reviewer. Merging
   without it risks another interruption-ordering row like F-31 or F-35.
2. **Archive proposal ([PR #173](https://github.com/MPAdesso/coding-harness/pull/173)):**
   17 finished changes behind the red nightly drift gate, measured 91 DRIFT
   lines at `59630b7`; proposed 12 plain archive, 4 living spec, 0 ADR. Each
   row is decided separately; nothing is moved yet.
3. **Where the untracked-files fix lives** (bead coding-harness-fdz, research
   in `plans/changes/probe-untracked-files/research.md` on branch
   `explore/probe-untracked-files`): the runner marks new files
   intent-to-add before `make verify` (recommended: the gate keeps its
   meaning "the tracked tree") or the kit probe also copies untracked files
   (the gate's meaning changes). The research's second question is settled:
   PR #138 merged. No spec is drafted before this answer.
4. **Plan card of bead coding-harness-8hr** (failed-check diagnostics copy
   test secrets into `findings.md`), unchanged from
   `plans/changes/failed-check-secrets/plan.md` on branch
   `explore/failed-check-secrets`:

   ```text
   For you:     A fixture secret printed by a failed check no longer blocks the runner's retry; other leak-check violations still stop it.
   Done when:   Regression tests hold criteria 1–7, including a successful retry through the real leak check, and make verify is green.
   Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
   Not now:     Earlier findings, source/history cleanup, leak-check exemptions, routing or model-answer redaction.
   Pre-mortem:  suppose it failed: most likely because findings.md was cleaned but the retry kept the original diagnostic string.
   Starts unless you say stop.
   ```

   No implementation started; the night plan reserved it for the
   maintainer's reading.

## Decisions and preferences

- The maintainer asked for phase-6 round 6 explicitly ("run round 6",
  2026-10-19); round 7 is not yet asked for.
- Herdr and tmux are recorded as candidate front ends for a harness-neutral
  view of every started agent; a dashboard comes "at some point", not before
  about 2026-10-26 (the 2026-10-12 rule: no visual tools for the night run
  until the simple form held two weeks). New bead coding-harness-326, related
  to coding-harness-0tc. Neither tool goes into the stage-2 runner or the
  swarm's security path (assessment from third-party descriptions; Herdr's
  own repository not read).
- The maintainer had the Podman machine VM stopped (2026-10-19, about
  20:15 UTC). It had run since 2026-10-14 16:43 UTC with 2 GB RAM and four
  cores: session `f3f1f2a8` ran `podman machine init && podman machine
  start` for a smoke container after decision Q-5 of the isolated-attempts
  change, and nothing stopped it. The isolated-attempts plan says how to
  start the machine, not who stops it.
- Standing: Codex usable including implementation; GLM through Z.ai off until
  2026-10-21 20:34 Asia/Singapore, through OpenCode Go fine; merges only on
  the maintainer's explicit request.

## Open work and blockers

Task status lives in Beads. Pointers only:

- Research swarm (coding-harness-icw): round-7 decision; then merge decision
  on #158 (draft).
- `make venv` refuses a too-old interpreter (coding-harness-y9q):
  [PR #174](https://github.com/MPAdesso/coding-harness/pull/174), CI green;
  close the bead after the merge.
- CI time (coding-harness-7so): kit probe single-process 72 s, measured
  19:39 UTC at `df7d2a5`; the `-n auto` run was killed by Claude Code's
  memory reaper (swap 8.3 of 9.2 GB) and not repeated. That probe run was
  BLOCK on two `tests/test_ci.py` cases, while the hosted CI of #174 was
  green: unexplained, probably memory pressure. Not yet written into the
  bead.
- Untracked files and the kit probe (coding-harness-fdz): item 10 not done;
  its two [GAP]s (does the probe collect an intent-to-add file; how
  `git add -N` treats a symlink, an empty directory, a forced ignored path)
  are unmeasured.
- Two load-sensitive tests were hardened in round 6 (`3b72968`,
  `1166e4a`); the round-6 green verify is their only evidence so far.
- The handover of #169 has two known errors (the "no interpreter" claim was
  dangling symlinks; bead omp is the red-first-install baseline fault, not
  the Pi install) — confirmed by the #173 agent.

## Working state and parallel-session boundary

- Research swarm: worktree `.claude/worktrees/research-swarm`, branch
  `explore/research-swarm`, `b57d109`, pushed, clean.
- New worktrees tonight: `archive-proposal-2026-10-19` (#173),
  `make-venv-python` (#174, Pi installed there), this handover's
  `handover-2026-10-19-night-eighth`.
- Removed tonight: 19 worktrees whose branch was merged into origin/main,
  clean and with nothing unpushed (branches kept). 23 others are kept, among
  them `failed-check-secrets` (clean since its call records were committed
  at `f3399b4`), `guard-test` (uncommitted `plans/changes/guard-test/findings.md`,
  not read) and `glm-smoke` (two commits ahead of its upstream
  `origin/main`, unpushed).
- Main checkout: `main` at `59630b7`, untracked `.codex/agents/` untouched.
- Parallel sessions: an OpenCode session ran in the main checkout from
  13:38 local time (read-only per #169); it ends with the restart. While it
  ran, the only tracker writes were the maintainer-requested bead
  coding-harness-326 and its relation, pushed with `tools/bd dolt push`.
- Nothing of this session runs now.

## Validation

- `make verify` on `explore/research-swarm`: GREEN at `ed5ae6b` (15:39 UTC,
  3023 passed), RED at `3353a8b` (18:38 UTC, one flaky catalog timing test),
  GREEN at `96a747c` (19:08 UTC, 3032 passed, 16 skipped).
- After `96a747c` only Markdown and frontmatter changed (`c72ae2c`,
  `b57d109`): spec and research-handoff tests 197 passed, criterion-ledger
  tests 38 passed, `check_frontmatter_current.py` green.
- #174: the agent's full verify was RED only on 16 `tests/test_pi_contract.py`
  errors (Pi not installed in the fresh worktree); after the Pi install 31 of
  31 passed; hosted CI green.
- This handover is text-only; `tests/test_feedback_channel.py` was run before
  the commit.
