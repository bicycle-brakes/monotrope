---
title: "Session handover — stage 2 live, the Flash runner in its review loop, MiMo through OpenCode Go, 2026-10-07"
category: handover
created: 2026-10-07
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-07"
tags: [handover, stage-2, flash-runner, mimo, opencode-go]
target_ref: "f9fffd5"
bead: coding-harness-qcp
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
updated: 2026-10-07
---

# Resume here

## Where we are

Stage 2 is live on `main` since PR #60 (merge `1952ac8`): Codex reviews
phases 2a and 6 of `bounded`, `feature` and `architectural` changes, GLM 5.3
runs the 4b review loop, all through `python3 scripts/stage2.py` behind the
leak check. On 2026-10-07 the maintainer merged #74–#78, #81, #82, #84, #85;
`main` is at `f9fffd5`. A parallel Codex session built the GLM 5.3 Flash
runner verbs `explore` and `implement` (bead coding-harness-qcp, branch
`feat/stage2-flash-runner`) and repaired round 1 of its GLM review loop, then
stopped at its ChatGPT credit limit; this session committed that repair
unchanged after `make verify` went green (`0aa2559`, 82 passed) and started
round 2 of the GLM loop (six rows). The maintainer decided that MiMo, the planned
additional 4b reviewer, is reached through OpenCode Go (bead
coding-harness-ymx).

## Next step

Decide the six rows of round 2 of the GLM review loop on the Flash runner
(written 2026-10-07 to
`~/.local/state/coding-harness/stage2/stage2-flash-runner/loop.md`, not yet
read): mark each taken or rejected, repair in the worktree
`.claude/worktrees/stage2-flash-runner`, `make verify`, then
`python3 scripts/stage2.py release-loop stage2-flash-runner`. Round 2 is the
last loop round. Then phase 6 (`stage2.py review`, Codex — on Opus 5.5 while Codex has
no credit) and open the pull request.

## Needed from the maintainer

1. **An OpenCode Go key** for MiMo: does a Go subscription exist (Hermes was
   planned on OpenCode Go)? If so, the maintainer adds the key to
   `~/.config/cc-routing/secrets.env` (e.g. `OPENCODE_GO_KEY=…`); agents never
   edit that file. On 2026-10-07 it holds only ANTHROPIC_KEY, GLM_KEY,
   KIMI_KEY, KIMI_BASE_URL (names read, values not).
2. **Codex credit** — while the ChatGPT account has none, stage-2 reviews of
   phases 2a and 6 fall back to Opus 5.5 and cost the Claude budget.
3. Merge the open pull requests when ready: #86 (decision: touch-map, head
   `c9ce9b6`), #83 (diagrams research, `20123f6`), #79, #80 (research notes).

## Decisions and preferences

- No Fable anywhere (#87). Explore and implement on GLM 5.3 Flash once the
  runner verbs merge; fallback when Z.ai is unreachable: Sonnet 5.5 (Haiku
  4.5 for explore); a leak stops the run. The runner checks after building:
  `make verify` green, one commit, a time-log line; red → one more Flash
  attempt, then one Sonnet attempt (decisions of the change folder).
- MiMo through OpenCode Go (2026-10-07, evening) replaces "Xiaomi direct" and
  "Token Plan"; the ADR answer "yes — widen ADR 0007" stands
  (`plans/changes/stage2-mimo/decisions.md`, `bb67825`). OpenCode Go facts
  read the same day: model `opencode-go/mimo-v2.6-pro`, Anthropic-compatible
  endpoint `https://opencode.ai/zen/go/v1/messages`, retention 0 days, a
  $15 monthly cap for MiMo-V2.6-Pro on Go, terms ask for an own user agent
  and an `x-opencode-session` header.
- The leak check stays; all twelve denylist rules are `secret:` rules
  (exempt in `tests/`), clean over the tree on 2026-10-07.
- Spawning reviewers through Pi or OpenCode instead of Claude Code: not
  pursued for now — it would not save Claude budget, ADR 0007 binds GLM to
  Claude Code, and the runner's restrictions would need rebuilding. Measure
  first (bead coding-harness-kw0).
- Work sequentially, sub-agents resumable, findings returned as text are
  committed verbatim, MINOR rows on tests, security or false statements are
  repaired (all in `AGENTS.md` since #82).

## Open work and blockers

Task status is in Beads. The queue, one at a time (2026-10-07):

1. Flash runner (coding-harness-qcp): loop round 2 → release → phase 6 →
   pull request. It touches `docs/WORKFLOW.md`, `AGENTS.md` and the prompts;
   check `decisions/provenance.yaml` whether that makes it a decision PR.
2. MiMo reviewer (coding-harness-ymx, `feat/stage2-mimo` at `bb67825`):
   merge `main`, rewrite the spec for OpenCode Go (spec-planner, Opus 5.5
   xhigh), phase 2a, then build once the key exists.
3. RB-G7 merge-freshness valve (coding-harness-34z), due 2026-10-31.
4. Test-holding gap (coding-harness-909).
5. Hermes slices 2 and 5 minor rows, then slice 4 with F-43
   (`feat/hermes-runner-2` at `faffe99`).

Bead coding-harness-9qo (template bundle, #75 merged) is still in progress
and assigned to another actor (`coding-harness-e0`); closing it needs a
reclaim. Bead coding-harness-5p0 closes after #86 merges.

## Working state and parallel-session boundary

- `main` at `f9fffd5`. Branches pushed: `feat/stage2-flash-runner`
  `0aa2559`, `feat/stage2-mimo` `bb67825`, `feat/hermes-runner-2` `faffe99`
  (no pull requests yet).
- The parallel Codex session worked in `.claude/worktrees/stage2-flash-runner`
  and is paused at its credit limit; its uncommitted work is now committed.
  This Claude session is the tracker writer for coding-harness.
- Worktrees of merged branches under `.claude/worktrees/` still exist and can
  be removed (16 entries in `git worktree list` on 2026-10-07).
- Tracker: beads coding-harness-bma and coding-harness-ei0 closed on
  2026-10-07, pushed with `tools/bd dolt push`.

## Validation

- `make verify` green on `feat/stage2-flash-runner` before `0aa2559`
  (82 passed, 2026-10-07, commit signing off).
- The leak check ran clean on every stage-2 call it guarded on 2026-10-07
  (253 files, 567 commits, 12 rules on the review-loop call).
- A real `stage2.py explore` run on GLM 5.3 Flash completed and appended to
  the change's `research.md` (Codex session's evidence for loop row L1-7).
- GLM loop round 2 completed (6 rows, leak check clean: 253 files, 568
  commits); its rows are not read yet.
- Not run: phase 6 of
  the Flash runner, any MiMo or OpenCode Go call.
