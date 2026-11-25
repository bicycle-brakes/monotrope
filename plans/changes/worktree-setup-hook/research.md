---
title: "Research — worktree-setup-hook"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-wg4z
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-25", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
neighbours: []
---

# worktree setup hook — Research

## Topic (bead coding-harness-wg4z)

Class: bounded. 2026-11-25: a new lane worktree lacked .venv and the pinned Pi; scripts/new_change.py failed with 'No module named yaml' and the rule lived only in tracker memory new-worktree-needs-pi (2026-11-22: about 110 tests fail without Pi). Extend the versioned hook .beads/hooks/post-checkout (core.hooksPath), outside the managed beads section: when git runs it for a new worktree (previous HEAD is the null SHA, branch checkout flag 1), run make venv and bash tools/pi/install.sh in that worktree, then a short check (the venv imports yaml, tools/pi/pi --version matches the pin); on failure print a loud message naming the step, without failing the checkout. HARNESS_NO_LANE_SETUP=1 skips it. The runner adds no worktrees itself (measured: no 'worktree add' in scripts/). Harness-neutral: Claude Code, Codex and Antigravity get set-up worktrees. Then retire memory new-worktree-needs-pi in favour of the hook.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29; bounded change · leak check clean over 1235 files, 5898 commits, 12 rules.

## Runner exploration — 2026-11-25

I ran the read-only exploration for `worktree-setup-hook`. Nothing was edited. The findings below are ready to append to `plans/changes/worktree-setup-hook/research.md`. Paths are relative to the repository root.

## What exists today

**The versioned beads hook.** `.beads/hooks/post-checkout` is a POSIX shell script with two parts. Its first line puts `tools/beads/bin` on `PATH`. Between the `BEGIN BEADS INTEGRATION v1.1.2` and `END BEADS INTEGRATION v1.1.2` markers it runs `bd hooks run post-checkout "$@"` under a timeout, which is managed by beads. The header comment says the first line sits outside that managed section so that `bd hooks install` preserves it. No other hook under `.beads/hooks/` is touched by this change. The five hook files (`post-checkout`, `post-merge`, `pre-commit`, `pre-push`, `prepare-commit-msg`) share the same managed block.

**The Pi install and pin check.** `tools/pi/install.sh` checks for `package.json`, `package-lock.json` and `.node-version`, verifies that `node` and `npm` are on `PATH`, and checks that the Node major matches `tools/pi/.node-version`. It reads the exact `@earendil-works/pi-coding-agent` pin from `package.json`, then runs `npm ci --ignore-scripts` inside `tools/pi/`. It exits non-zero on any failure. `tools/pi/pi` is the only sanctioned launcher. It refuses to start unless `node_modules/@earendil-works/pi-coding-agent/package.json` reports the pinned version, and it then runs the Pi bin with `exec node`. Its error messages tell the reader to run `bash tools/pi/install.sh`.

**The venv target.** The `Makefile` target `venv` (with the `PYTHON ?=` default at the `PYTHON` assignment) checks the `requires-python` value in `pyproject.toml` against the interpreter, then runs `python -m venv .venv` and `pip install --require-hashes -r requirements-ci.txt`. The `help` target lists `make venv [PYTHON=<interpreter>]`.

**The yaml dependency.** `pyproject.toml` pins `PyYAML==6.0.2`, and `requirements-ci.txt` carries it with hashes. `scripts/new_change.py` imports `plans_registry`, and other scripts import `yaml` directly. The `'No module named yaml'` failure named in the bead therefore fits a worktree whose `.venv` does not exist yet. The worktree's own `.venv` is the only place that module is installed.

**The opt-out name.** `HARNESS_NO_LANE_SETUP` appears nowhere in the tracked tree. It is a new name.

**Existing worktree guidance.** `AGENTS.md` (the repository agent rules) requires every new checkout or worktree to run `make venv` and `bash tools/pi/install.sh` once before `make verify`. `docs/WORKFLOW.md` §3 describes the worktree procedure, and at its line 800 it describes `git worktree add -b <branch>`. Several handovers record the manual step (for example `docs/journal/handover/2026-10-15-night-run-fifth.md`, which says every new worktree runs `make venv`, and `docs/journal/handover/2026-10-19-night-run-eighth.md`, which records a fresh worktree failing without Pi). The manual step is therefore documented in prose only.

**Worktree creation by the harness.** A search for `worktree add` in `scripts/` found no match, which matches the bead's measurement. Worktrees are created by the agent harness, by Claude Code and by hand. `docs/research/2026-09-23-worktree-tracker-writes.md` describes the same `git worktree add` shape.

**Tests on hooks.** No file under `tests/` references `post-checkout`, `.beads/hooks` or `hooksPath`, except the `core.hooksPath=/dev/null` uses listed below. Nothing pins the content of the versioned hook files.

**`core.hooksPath` callers that disable hooks.** `scripts/pr_sync.py` (around the lines that run `merge --ff-only` and `merge --quiet`), `scripts/research_capture.py`, `scripts/stage2_research_history.py` and `tests/test_stage2_research_history.py` all pass `-c core.hooksPath=/dev/null` to git. Those calls run git commands that must not trigger hooks. They are named here because the new hook, if it runs on any checkout, would not run on those paths.

**The closest neighbour.** `plans/changes/venv-guard/` (bead `coding-harness-s55e`, status draft, updated 2026-11-18) addresses a related problem: the suite must run on the locked environment, and `tests/test_lock.py` checks that the environment matches the lock. It is the test side. This change is the setup side.

**Neighbours.** The `neighbours:` header in `research.md` is `[]`. The most relevant specs in the tree are `plans/changes/venv-guard/` (draft, above) and `plans/changes/pi-pin/` in the archive (`plans/changes/archive/2026-11-06-pi-pin/`), which created the Pi pin. The runner should decide whether to add them.

## What is unclear

- **Where `core.hooksPath` is set.** Nothing in the worktree's tracked files sets `core.hooksPath` to `.beads/hooks`. The repository's git config is outside this worktree, and the explorer may not read it. Whether `bd hooks install`, `tools/bd bootstrap` or a manual step sets it is therefore not verified. Until someone runs `git config --get core.hooksPath` in the repository, it stays open which hook directory git actually uses in a worktree.
- **Whether `.beads/hooks/*` is tracked by git** or generated locally was not verified for the same reason.
- **The memory note `new-worktree-needs-pi`** lives in the tracker memory, not in files under this worktree. It was not read. Its wording (the 2026-11-22 "about 110 tests fail without Pi" figure) comes only from the bead description.
- **Whether git calls `post-checkout` for `git worktree add`.** The bead assumes it does, with the previous HEAD as the null SHA and the branch-checkout flag `1`. The git documentation for `post-checkout` supports those arguments. Whether the repository's own tooling triggers a new worktree through that path was not measured.
- **Whether `tools/pi/pi --version` is a valid check.** The launcher `exec`s the Pi bin with its arguments, so `--version` reaches Pi unchanged. Whether Pi's `--version` exits zero without starting a session was not run.
- **Whether `make venv` and `install.sh` succeed on a fresh worktree from inside a hook.** This was not run. The hook would run in the new worktree's root, where `Makefile` and `tools/pi/` exist only after checkout completes.
- **Whether `bd hooks run` and the new section can coexist** when `bd hooks install` regenerates the file. The header comment asserts that the section above the managed markers survives. That was not checked against the beads installer.

## Files a change would have to touch

- `.beads/hooks/post-checkout`: add the lane-setup section above the `BEGIN BEADS INTEGRATION` marker, outside the managed block.
- A new test under `tests/` (for example beside `tests/test_lock.py`) to pin the hook's behaviour: the null-SHA detection, the `HARNESS_NO_LANE_SETUP=1` skip, and the failure message. None exists today.
- `AGENTS.md` and `docs/WORKFLOW.md` §3, which document the manual `make venv` and `bash tools/pi/install.sh` step: they would need to say the hook now does this, and the manual step becomes the fallback.
- `docs/journal/handover/` gets no edit from this change. Handovers are history.
- The tracker memory `new-worktree-needs-pi` is retired. That is a tracker write, not a file.
- `plans/changes/worktree-setup-hook/` (`research.md`, `decisions.md`) is the change's own folder.

## Open questions for the runner

1. Does the maintainer's git config point `core.hooksPath` at `.beads/hooks`? That decides whether the versioned file runs at all.
2. Should `venv-guard` and `pi-pin` be listed as `neighbours:`?
