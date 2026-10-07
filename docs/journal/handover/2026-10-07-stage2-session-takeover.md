---
title: "Session handover — interactive session spec ready, waiting for Flash runner"
category: handover
created: 2026-10-07
updated: 2026-10-07
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
tags: [handover, stage-2, session, codex]
target_ref: "1c79860"
bead: coding-harness-amp
status: pending
review: {status: pending, approved_by: null, approved_at: null}
---

# Resume here

## Objective

Build `python3 scripts/stage2.py session <change> --model <id>` as an
architectural change, with declaration and leak checks, interactive Terminal
dispatch, the checked handover prompt, findings audit and bounded OpenCode
permissions. End in a decision PR; never merge. The takeover request protects
the Flash-runner branch and PR #89 explicitly.

## Completed work and evidence

- Read `AGENTS.md`, the Beads skill and the requested takeover handover from
  `origin/docs/handover-2026-10-07-b` at `a3d5585` (PR #90).
- Fetched origin and created `.claude/worktrees/stage2-session`, branch
  `feat/stage2-session`, from `origin/main` at `1c79860`.
- Claimed the shared bead as actor `codex`, and pushed the tracker.
- Installed this worktree's hash-pinned dependencies with `make venv`.
- Wrote `plans/changes/stage2-session/research.md`, `decisions.md` and
  `spec.md`; regenerated `plans/INDEX.md`. No runner implementation yet.
- Checked help/version only: OpenCode `1.18.35`, Codex CLI `0.160.1`.
  Read official OpenCode permissions/configuration and official Codex CLI
  reference; links and named limits are in research. No model was started,
  no GUI window opened and no credential file read.
- PR #89 at `11abf42` and #90 at `a3d5585` were OPEN with successful hosted
  verify checks when inspected on 2026-10-07. Neither was changed or merged.
- Validation results are recorded in the addendum below before commit.

## Decisions and preferences

- German conversation, English artifacts, result first, one question at a
  time with a recommendation. Previously settled launch requirements are
  in `decisions.md`; do not ask them again.
- Default handover is the change-local `handover.md`; explicit `--handover`
  may select another regular file inside the worktree. No guessing latest
  relevance and no outside-path/symlink prompt loading.
- Model selection has no silent fallback. The session audit must distinguish
  terminal dispatch from a successful or completed model run.
- OpenCode outside-directory tool denials are not OS isolation. Codex
  workspace-write is not a worktree-only read guarantee. The scan covers
  launch only; no ongoing scan or approval for undeclared UI model switches.
- Draft the ADR 0007 amendment inside the change folder only. Do not edit
  `docs/adr/` or the maintainer's global/credential configuration.

## Unfinished work and ownership

The instruction explicitly permits research/spec before PR #89 merges;
implementation depends on its Flash-runner helpers landing on main. Phase 2a,
design (including ADR draft), plan, implementation, review loop, final review
and decision PR are not done. The wider bead also contains workflow parity
work: do not close it merely because the session verb exists.

The prior Claude session's budget is spent; this session claims only this
bead and changes only its own worktree. Other worktrees, notably
`stage2-flash-runner` and `stage2-mimo`, remain untouched. Recheck live session
ownership before any additional tracker mutation. No cleanup of old worktrees.

## One concrete resumption action

After the maintainer merges PR #89 and #90, fetch origin and bring the fresh
main base into `feat/stage2-session`. Reconcile the research/spec against the
merged runner, then run the architectural spec review through the approved
runner route before writing design and plan. Do not silently implement the
separate OpenCode Go reviewer migration to obtain a reviewer.

## Addendum — prerequisite merged and preparation verified, 2026-10-07

The earlier OPEN snapshots above are historical. A fresh GitHub read shows
PR #89 merged at 14:28:43 UTC and #90 at 14:28:47 UTC. Freshly fetched
`origin/main` is `b32f488`. This session did not merge them.

The preparation tree based on `1c79860` passed full `make verify` with network
available: 1,059 tests passed, 16 skipped; writer ruleset 82 passed; final
`VERIFY GREEN`. The first run found the index before regeneration, and the
network-restricted retry could not measure the writer ruleset; neither is
claimed green. Existing unrelated artifact DRIFT and report-only docs-link
and markdownlint findings remain, without broad cleanup here.

Next: commit/push the green preparation, rebase this own branch onto the
merged main, then the runner's spec review. The implementation prerequisite
is now fulfilled; no maintainer action is needed to unblock it.
