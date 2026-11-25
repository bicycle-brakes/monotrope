---
title: "Research — test-ci-shared-tree"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.12
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-25", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
neighbours: []
---

# test ci shared tree — Research

## Topic (bead coding-harness-bxxt.12, copied by the orchestrator 2026-11-25)

Class: bounded.

Why: test_the_glob_itself_finds_a_real_orphan_shell_script
(tests/test_ci.py:3605-3633) writes
REPO_ROOT/scripts/verwaistes_werkzeug__test_ci_nie_committen.sh (line 3619)
and unlinks it in finally. Parallel workers that glob scripts/ can see it;
scripts/kit/probe.py caches _ls_files() with lru_cache (369-370). What:
build the orphan case in a temporary copy, never in the shared tree.
Prerequisite for --dist worksteal and a parallel kit probe.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp, night run 2026-11-24-a), from an external verify-speed analysis.



PARENT
↑ ○ coding-harness-bxxt: (EPIC) Verify speed and machine load P1

BLOCKS
← ○ coding-harness-bxxt.18: pytest --dist worksteal for make verify, CI and the kit probe (xdist-guarded in the probe) P3

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu) · leak check clean over 1202 files, 5747 commits, 12 rules.

## Runner exploration — 2026-11-25

Research for `test-ci-shared-tree`, prepared for `plans/changes/test-ci-shared-tree/research.md`. I used Read, Grep and Glob only and ran no command.

**The topic is inferred, not stated.** The change folder holds only the skeleton `research.md` (frontmatter `class: bounded`, `neighbours: []`, bead `coding-harness-bxxt.12`, body still "empty until it has run"). Its bead description is not in the repository and I could not read it, so the reading below rests on the change name and on code comments.

## What exists today

- **Test fixture that isolates recipes from the shared checkout.** `tests/test_workflow_entry.py`, `_fixture_tree` (around lines 197–215): builds a full isolated tree with copies of the entry scripts (`ENTRY_SCRIPTS`: `new_change.py`, `plans_registry.py`, `_verdict.py`, `bead_render.py`, `check_worktree_state.sh`, `venv_guard.py`), a copy of the Makefile, `plans/changes` and `plans/specs`, a preset bead export, and its own git init. Its docstring says the recipes run "against this tree, never against the shared checkout or its tracker", and that the bead export is preset through `BEAD_RENDER` "the way CI does it (D-52)".
- **Two-tree naming rule.** The same docstring says a test comparing a recipe with the direct entry must build two trees under different names, because one name aliases both handles to one directory.
- **Controlled interpreter and make runs.** `_controlled_python` (around line 218) writes a `python3` wrapper that logs each invocation and then runs the real interpreter. `_run_make` (around line 230) runs real `make` inside the tree with that wrapper first on the path. A recipe that starts no interpreter leaves the log at zero bytes.
- **CI workflow.** `.github/workflows/ci.yml` exists. I did not read it, so I have not confirmed how it invokes the test suite or whether it hydrates the tracker there.
- **BEAD_RENDER and D-52 in CI.** `docs/governance/gate-catalog.md` (row `bead-export`) and `decisions/gates.yaml` (around line 164) say that in CI the hydration renders once and presets `BEAD_RENDER`, and that locally the access point renders fresh or fails. `docs/adr/0004-tracker-render-is-the-contract.md` records the D-52 conditions.
- **Shared-checkout incidents.** `docs/journal/handover/2026-09-17-tracker-pin-and-session-end-interview.md` (around lines 70–72) says a session committed its handover with git plumbing so "the shared checkout, its index and its hooks stayed untouched". `docs/journal/handover/2026-11-06-heartbeat-night.md` (around lines 150–153) says runner-started sessions shared worktrees and no other session wrote the tracker.
- **No spec yet.** `plans/specs/` holds one spec, `implementation-verification/spec.md`. I did not check it for overlap with this change.
- **Index entry.** `plans/INDEX.md` line 693 lists this change's research as `draft`, implementation status `none`, dated 2026-11-25.

## What is unclear

- The intended change itself. The name suggests CI running tests against a shared tree instead of an isolated one, but no artefact states the problem, the expected behaviour or the failure seen. The bead text would settle this.
- Whether `test_workflow_entry.py` already covers the CI case, or whether `ci.yml` runs the suite in the shared checkout.
- Whether `_fixture_tree` is the only isolation mechanism, or whether other tests read the shared checkout or tracker directly. I did not grep the whole test directory for that.
- The current branch is `fix/test-ci-shared-tree`, and `git status` shows `research.md` already modified before this run. I did not diff it, so the frontmatter may differ from the committed skeleton.

## Files a change would have to touch (as far as read)

- `tests/test_workflow_entry.py` (fixture and helpers)
- `.github/workflows/ci.yml`, if CI's invocation is part of the problem
- `plans/changes/test-ci-shared-tree/` (its research, then the usual phase artefacts)
- Possibly `docs/governance/gate-catalog.md` and `decisions/gates.yaml`, if the bead-export gate changes

## Not done in this run

I did not run `scripts/stage2.py prepare-explore` or `explore`. The phase instructions say the runner, not this explorer, runs those commands, and my tools are read-only. I also did not write `research.md`; the runner does that from this output.

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu); second run with the bead text as topic · leak check clean over 1202 files, 5749 commits, 12 rules.

## Runner exploration — 2026-11-25

## Research for test-ci-shared-tree (bead coding-harness-bxxt.12, class bounded)

This run replaces the earlier draft's "topic inferred" section. The topic now carries the bead text, and I checked each claim in it against the tree. The earlier draft's `_fixture_tree` material in `tests/test_workflow_entry.py` concerns a different isolation mechanism and is not evidence for this bead. I did not re-read it in this run.

### What exists today

- **The orphan-script test writes into the shared `scripts/` directory.** `test_the_glob_itself_finds_a_real_orphan_shell_script` in `tests/test_ci.py` creates `scripts/verwaistes_werkzeug__test_ci_nie_committen.sh` under `REPO_ROOT` (the write is at line 3619, inside the test's body). It removes the file in a `finally` block (lines 3632–3633). The test's own docstring says the file is untracked, so the kit probe in `scripts/kit/probe.py` never copies it. The write uses the real checkout, not a temporary copy.
- **The test runs its assertion through `_scripts()`.** `_scripts()` in `tests/test_ci.py` globs `REPO_ROOT / "scripts"` for `*.py` and `*.sh` and drops names starting with `test_`. The test reads the file list at that moment, so the window in which the orphan exists is the window in which its glob runs.
- **Two other tests in the same module also call `_scripts()` against the real `scripts/`:**
  - the test whose docstring sits just above line 3568 (its `def` line was not read in this run), which asserts that no script without a caller lacks a declared reason;
  - `test_every_script_has_a_test_or_a_declared_reason` (`tests/test_ci.py`, around line 3729), which asserts that every script has a test or a declared reason.
  Both use the same glob and would see the orphan file if they ran while the test is in progress.
- **Parallel runs are the default.** The pytest gate runs `python3 -m pytest tests/ -q -n auto`. The same command appears in `Makefile` (line 22), `.github/workflows/ci.yml` (line 82), `decisions/gates.yaml` (line 82) and `docs/governance/gate-catalog.md` (row `pytest`). With xdist, the orphan-script test and the two `_scripts()` callers may run in different worker processes against one shared directory.
- **The kit probe caches its file list per process.** `_ls_files()` in `scripts/kit/probe.py` (lines 369–370) is decorated with `@functools.lru_cache(maxsize=1)`. It runs `git ls-files -z --cached` and `git ls-files -z --others --exclude-standard`. The first set is what the commit contains; the second is untracked files, classified as drift and not as a block. Each xdist worker is its own process, so each gets its own cache. The cache is not shared between workers.
- **The probe's own test name is recorded in a comment.** `scripts/kit/probe.py` line 259 counts `tests.test_ci::test_the_glob_itself_finds_a_real_orphan_shell_script` in a dated count (61 → 62 on 2026-09-14). A rename or move of that test changes this count.
- **The kit probe is a separate run.** The docstring of `tests/test_kit.py` (lines 6–8) says the probe runs as a step of its own in `ci.yml` and is not a pytest case. I did not read the probe step in `ci.yml`, so this is the docstring's claim, not a verified step.
- **Existing tests that call the probe on the real repo.** `tests/test_kit.py` calls `probe.nach_rolle()` against the real repository at lines 58, 66, 352 and 404. `nach_rolle()` uses only the tracked set, so an untracked orphan file would not reach these calls.
- **The bead's other items.** The string `worksteal` does not occur anywhere in the repository. The sub-bead `coding-harness-bxxt.18` (`--dist worksteal`) is therefore not in the tree. Its text lies outside what I could read.

### Where it lives

- Test: `tests/test_ci.py`, function `test_the_glob_itself_finds_a_real_orphan_shell_script` and helper `_scripts()`.
- Glob callers: `tests/test_ci.py`, `_scripts()` and its two callers above.
- Cache and file list: `scripts/kit/probe.py`, `_ls_files()`, `getrackte_dateien()`, `unversionierte_dateien()`, `nach_rolle()`.
- Parallel-run wiring: `Makefile`, `.github/workflows/ci.yml`, `decisions/gates.yaml`, `docs/governance/gate-catalog.md`.

### What is unclear

- **Which module constant `REPO_ROOT` in `tests/test_ci.py` resolves to.** I read its use in the write and the glob, not its definition in that file. Whether it is the real checkout is inferred from the bead and the docstring, not read.
- **The `def` of the test above line 3568.** The enclosing test's name was not read.
- **Whether an in-process probe call can see the orphan.** `unversionierte_dateien()` is used at `scripts/kit/probe.py` line 502. I did not check whether any pytest test calls that path in-process while the orphan exists. If one does, the per-process cache could capture the orphan file.
- **Whether the bead's stated prerequisites are already met.** The bead names `--dist worksteal` and a parallel kit probe as dependants. Neither is in the tree.
- **Whether `ci.yml` builds the orphan path in a copy.** Not read.

### Possible neighbours (seen in search results, not read)

- `plans/changes/verify-two-slots/findings.md` contains the phrase "shared tree" (matched by the search; not read).
- `plans/changes/archive/2026-11-06-verify-duration/` and `docs/research/2026-11-09-make-verify-long-term.md` cover the xdist and speed work (lines seen in search only).
- `plans/INDEX.md` lists this change's research (line 693).

### Files a change would have to touch (as far as read)

- `tests/test_ci.py`: the orphan test (around lines 3605–3633) and possibly `_scripts()` (line 3532), if the glob is to see only the real inventory.
- `scripts/kit/probe.py`: the comment at line 259 names the test id, so a rename or move touches it.
- `plans/changes/test-ci-shared-tree/` (this research, then the usual phase artefacts).

### Not done in this run

I did not run `scripts/stage2.py prepare-explore` or `explore`; the runner does that. I wrote no file, and the research above is returned for the runner to write into `research.md`.
