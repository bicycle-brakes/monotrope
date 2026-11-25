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
