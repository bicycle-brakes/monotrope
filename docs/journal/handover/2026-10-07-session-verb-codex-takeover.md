---
title: "Session handover — Flash runner in PR #89, Codex takes over to build stage2.py session, 2026-10-07"
category: handover
created: 2026-10-07
updated: 2026-10-07
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-07"
tags: [handover, stage-2, session-verb, codex, opencode-go, flash-runner]
target_ref: "1c79860"
bead: coding-harness-amp
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

This handover is written for a **Codex session** that takes over because the
maintainer's Claude five-hour budget is nearly spent (maintainer, 2026-10-07:
Codex takes over whenever that budget is spent — bead coding-harness-amp).

## Where we are

- `main` at `1c79860` (2026-10-07). Merged today: #74–#78, #81–#88, #79, #80,
  #83, #86 (touch map: every code pull request carries a generated "What it
  touches" section from `scripts/touch_map.py`).
- **PR #89** (branch `feat/stage2-flash-runner`, head `11abf42`): the runner
  verbs `explore` and `implement` on GLM 5.3 Flash (bead coding-harness-qcp).
  GLM loop rounds 1–2 decided and repaired; phase 6 on Opus 5.5 (Codex had no
  credit) with recheck — 0 open; `make verify` green at `11abf42`. Waits for
  CI and the maintainer's merge. Do not change that branch.
- Bead coding-harness-9qo (template bundle) is done by #75 but still held by
  the stale actor `coding-harness-e0`; closing needs `--force`, which the
  maintainer runs (Claude Code's safety check refused it).

## Decisions of 2026-10-07 (maintainer, in the conversation)

1. **Reviews through OpenCode Go** (bead coding-harness-ymx): every review —
   2a, 4b, 6 — in rounds: 1 `opencode-go/deepseek-v4.1-flash`, 2
   `opencode-go/mimo-v2.6-flash`, 3 only when needed `opencode-go/mimo-v2.6-pro`.
   An ordered list in `model-endpoints.yaml`, changeable by a one-line pull
   request. Codex leaves the reviewer roles; the loop limit rises to three
   rounds. ADR 0007 needs amending → decision PR. `OPENCODE_GO_KEY` is in
   `~/.config/cc-routing/secrets.env` (name checked, value not read).
2. **Codex when the Claude budget is spent** (bead coding-harness-amp):
   everything in the workflow must run in Claude Code and in Codex.
3. **`stage2.py session`** (recorded on coding-harness-amp, maintainer asked
   to build it): extend — not loosen — "a foreign model starts only through
   `scripts/stage2.py`" to whole interactive sessions.

## Next step — build `stage2.py session` (bead coding-harness-amp)

The maintainer's words for the verb `python3 scripts/stage2.py session
<change> --model <id>`:

1. **Check like every call:** endpoint declared in `model-endpoints.yaml`,
   leak check clean. If either is red, nothing starts.
2. **Start:** the runner opens a new terminal window in the change's worktree
   running OpenCode (or Codex) with the chosen model and the handover file as
   first prompt; the maintainer works in it normally.
3. **Record:** one audit line in the change's `findings.md`: date, model, the
   leak check's three numbers.
4. **Confine:** an OpenCode configuration in the worktree denies reads outside
   it, as far as OpenCode supports that — not yet checked.

Named limit: the leak check covers the state at the session's start only.

How to run it through the workflow (`docs/WORKFLOW.md`):

1. Branch `feat/stage2-session` from a freshly fetched `origin/main`, worktree
   `.claude/worktrees/stage2-session`; `make venv` once.
2. `python3 scripts/new_change.py` (or the documented entry) for change
   `stage2-session`, bead coding-harness-amp; class most likely
   `architectural` (it amends ADR 0007) — decide and reason it.
3. Explore (phase 1): read `scripts/stage2.py` (its `preflight`,
   `begin_work_call`, leak-check call and audit line are the pattern to reuse),
   `scripts/leakcheck.py`, `model-endpoints.yaml`, `tests/test_stage2.py`.
   Check on the machine: `opencode --help` (flags `--model`, `--prompt`
   exist in 1.18.35), OpenCode's permission config for denying reads outside
   a directory, and how to open a macOS terminal window from Python
   (`open -a Terminal` / `osascript`) without the runner holding the session.
   Note: `#89` must merge first if the verb builds on `begin_work_call`; if it
   has not merged when you start, write research and spec, and build after.
4. Spec, plan; then implement with tests (`make verify; echo "exit=$?"`
   green before each commit), commit and push after every green step.
5. Draft the ADR 0007 amendment text in the change folder — `docs/adr/` is
   human-decided, never edit it; the pull request is a decision PR (title
   `decide(stage2): …`, label `decision`, body from
   `.github/PULL_REQUEST_TEMPLATE/decision.md`, with the "What it touches"
   section from `scripts/touch_map.py origin/main HEAD`).

## Rules that bind the taking-over session

- Read `AGENTS.md` first; it is the only instruction file and Codex reads it.
- Repository English; German with the maintainer: result first, one question
  at a time with a recommendation.
- Tracker: this Claude session was the writer. If it has ended, the Codex
  session is the only writing session and may write the tracker with
  `tools/bd` (never bare `bd`), then `tools/bd dolt push` before `git push`.
  If the Claude session still runs, claim only: `tools/bd update
  coding-harness-amp --claim --actor codex`, plus one handover comment.
- Commit signing: prefix commits and `make verify` with
  `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`
  (a signed merge otherwise waits on Touch ID and hangs).
- Never read or edit `~/.config/cc-routing/secrets.env`. Never start a
  foreign model except through `scripts/stage2.py`.
- Never merge; the maintainer merges, after the decision block is restated
  (`prompts/07-commit.md`, "The merge").

## Queue after that (one at a time)

1. OpenCode Go reviewers (coding-harness-ymx, branch `feat/stage2-mimo` at
   `bb67825`): rewrite spec and plan for the decision above. A paste
   handover for an OpenCode session exists in the conversation only; once
   `stage2.py session` exists, start that session through it.
2. RB-G7 merge-freshness valve (coding-harness-34z), due 2026-10-31.
3. Test-holding gap (coding-harness-909).

## Working state

- Worktrees of merged branches under `.claude/worktrees/` can be removed.
- A Codex process started 10:11 runs in the main checkout (paused at its
  credit limit since the morning).
- Tracker pushed after every write today (`tools/bd dolt push`).

## Validation

- `make verify` green on `feat/stage2-flash-runner` at `11abf42`
  (2026-10-07); hosted CI for #89 not yet read at the time of writing.
- Not run: any OpenCode Go call; `stage2.py session` does not exist yet.
