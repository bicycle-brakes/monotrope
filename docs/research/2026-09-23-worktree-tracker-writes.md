---
title: "Tracker writes from worktrees — the five-check verification of D-5"
category: research
status: accepted
created: 2026-09-23
last_reviewed: 2026-09-23
updated: 2026-09-29
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-23"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [beads, worktrees, concurrency, d-5, verification]
---

# Tracker writes from worktrees — verification protocol

**Result: all five checks are green with the pinned bd 1.3.0 in embedded
Dolt mode.** A worktree resolves the main checkout's tracker through the
shared git directory. Its writes are visible at once in the main checkout.
Concurrent writers from several worktrees lose nothing, and a contested claim
has exactly one winner. D-5's write ban on worktrees therefore lifts. The
one-writer rule for a session (AGENTS.md house rule 4, ADR 0002) is a
separate rule and stays (bead `coding-harness-m34`, measured 2026-09-23).

## Setup

A throwaway repository with its own tracker and its own remote. The real
tracker was only read.

- The binary is `~/.local/bin/bd-1.3.0`, the version `tools/beads/VERSION`
  pins. Embedded Dolt mode is the default, as in this repository.
- The layout is a bare git repository `remote.git` and a main checkout
  `probe-main`, initialised with `bd init --prefix m34-probe-repo`. The
  prefix is deliberately long and hyphenated, which is the shape that broke
  in portfolio (wp-p0.1).
- There were three worktrees, one per placement:
  - `.claude/worktrees/wt-a`, the path Claude Code uses (`git worktree add`),
  - `wt-b`, made by `bd worktree create wt-b`, which places it at the
    repository root,
  - `../sibling-wt`, the retired sibling placement, measured for comparison.
  Each worktree's directory name differs from the repository name.
- All commands ran in a Claude Code sandboxed shell.

**A finding from the setup.** Under `/private/tmp`, `bd worktree create`
refuses with "BEADS_DIR points to unsafe location", although `BEADS_DIR` was
not set in the environment; bd sets it internally. The probe was therefore
repeated under the home directory, where the real repositories live. A
tracker in a temporary directory cannot use `bd worktree create`.

## The five checks

| # | Check | Command, in each worktree | Result |
|---|---|---|---|
| 1 | Same list as the main checkout | `bd list --all --json`, ids compared | green in all three worktrees; `bd where` resolves to `probe-main/.beads` |
| 2 | Variables and visibility | see below | green for bd; the Omnigent passthrough is not tested |
| 3 | A bead made in the worktree is visible in the main checkout | `bd create …`, then `bd list` in `probe-main` | green in all three: `m34-probe-repo-fit`, `-9h8`, `-1nx` |
| 4 | Two writers at the same time | parallel bursts, and a contested claim | green, details below |
| 5 | The full prefix | the ids of every create | green: all 136 ids start with `m34-probe-repo-` |

### Check 2 — variables and the sandbox

- **Discovery needs no variable.** bd found the tracker in every worktree
  with no `BEADS_DIR` set, through the git common directory.
- **An explicit `BEADS_DIR` is honoured.** From `wt-a`,
  `BEADS_DIR=<main>/.beads bd where` resolves to the main tracker.
- **The actor arrives through the environment.**
  `BD_ACTOR=role-worker bd update <id> --claim` set the assignee to
  `role-worker`. A role can therefore travel as a variable, as long as the
  harness passes it through.
- **Variables reach child processes in the sandboxed shell**
  (`LS_ROLE=worker sh -c 'echo $LS_ROLE'` prints `worker`), and `.beads/`
  is readable and writable from the Claude Code sandbox, in the probe and in
  this repository.
- **A Claude Code subagent in its own worktree** (`isolation: worktree`,
  under `.claude/worktrees/agent-…` of this repository, read-only run)
  resolved `tools/bd where` to `/Users/mikypiky/coding-harness/.beads` and
  listed the same 18 open beads. The tracked `.beads/` files in the worktree
  did not mislead it, and no tracker variable was set.
- **Not tested:** Omnigent's deny-by-default environment and its
  `env_passthrough` (the arc42 document, §5.2.6). Omnigent is not installed
  here, so this belongs to the M0 proof of concept (`coding-harness-eev`).
  Since bd needs no variable to find the tracker, only the role variable
  depends on that passthrough.

### Check 4 — concurrency

- **Contested claim.** `wt-a` and `wt-b` ran
  `bd update <id> --claim --actor agent-…` at the same moment. `agent-b`
  won. `agent-a` got exit 1 with "issue already claimed by agent-b", and
  the bead ended `in_progress` with assignee `agent-b`.
- **Two writers.** `wt-a` and `wt-b` each ran 15 × (`bd create` + `bd update
  --notes`) at the same time: 30 of 30 creates, 30 of 30 notes, 0 errors,
  no duplicate titles.
- **Four writers.** `wt-a`, `wt-b`, `sibling-wt` and the main checkout each
  ran 25 × (create + update) at the same time. That was 100 of 100 creates
  and 100 of 100 notes with 0 errors and no duplicates, in 98 seconds. bd
  serialises embedded writers rather than failing them, at roughly half a
  second per write. The shared-server fallback of arc42 §5.2.6 is not
  needed at this load.
- **Transport.** `bd dolt push` from `wt-a` reached the remote. A fresh
  clone of the remote, after `bd bootstrap --yes` ("Bootstrap plan: clone
  from remote"), listed all 136 beads.

## Consequence

- **D-5's write ban on worktrees lifts.** Beads may be created, updated,
  claimed and closed from a worktree placed in the repository, through
  `.claude/worktrees/` or `bd worktree create`. AGENTS.md says so.
- **The one-writer rule stays.** Technically safe concurrent writes do not
  change who may write. While another session runs, none writes (house rule
  4), until ADR 0002's exclusive coordinator exists with its enforcer
  (`coding-harness-36z`, which this bead unblocks).
- **Placement.** Sibling directories work technically, but D-5 retired them.
  They stay retired.

## Reproduce

The commands are in the order used on 2026-09-23. `$R` is a scratch
directory **outside** `/tmp`, and `bd` is the pinned 1.3.0 binary.

```bash
git init -q --bare $R/remote.git && git init -q -b main $R/probe-main
cd $R/probe-main && echo '.claude/worktrees/' > .gitignore && git add -A \
  && git commit -qm init && git remote add origin $R/remote.git && git push -qu origin main
bd init --prefix m34-probe-repo --quiet && git push -q
git worktree add -q -b wt-a .claude/worktrees/wt-a main
bd worktree create wt-b
git worktree add -q -b wt-sibling ../sibling-wt main
# checks 1, 3, 5: in each worktree — bd where; bd list --all --json; bd create "…" --silent
# check 4: two or four background loops of bd create + bd update --notes, then count
# claim race: bd update <id> --claim --actor agent-a & bd update <id> --claim --actor agent-b & wait
bd dolt push   # from a worktree
git clone -q $R/remote.git $R/fresh && cd $R/fresh && bd bootstrap --yes && bd list --all
```
