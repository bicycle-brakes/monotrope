---
title: "Decisions — test-ci-shared-tree"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.12
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, tests, xdist]
---

# test-ci-shared-tree — Decisions

## SKIP · interview

status: skipped
reason: The change is a test-only fix with one stated remedy and no open design choice: the bead (coding-harness-bxxt.12, filed at the maintainer's request on 2026-11-24 from a checked analysis) says to build the orphan-script case in a temporary copy instead of writing into the shared scripts/ directory; behaviour of scripts/ and of every gate stays unchanged.

## Details decided by the orchestrator

[DETAIL] **D-1 (where the orphan case lives)**: the test builds a throwaway tree (tmp_path) holding the files the orphan check reads, writes the orphan script there and points the glob at that tree, so no file is ever created under the repository's scripts/. Reason: the bead's remedy; it keeps parallel workers and the kit probe's cached file list from ever seeing the file.

[DETAIL] **D-2 (the probe's dated test count)**: scripts/kit/probe.py line 259 counts this test by name; the test keeps its name so the count stays true, or the count moves with the rename in the same change. Reason: the explore found the dated count (research.md).

[DETAIL] **D-3 (scope)**: --dist worksteal (coding-harness-bxxt.18) and a parallel kit probe are not part of this change; it only removes the shared-tree write they depend on. Reason: bead scope.

[DETAIL] **D-4 (spec review S-1, the glob under test)**: Reading A — the control test calls the real `_scripts()` aimed at its temporary tree through a root parameter (default: the repository's scripts/), and the real `_heimatlose_namen()`, so dropping `*.sh` from `_scripts()` turns the control test red. Reason: the test exists to prove the real glob sees shell scripts.

[DETAIL] **D-5 (spec review S-2, today's inventory)**: Reading A — "a real script" means today's set: top-level `*.py` and `*.sh` in scripts/ whose names do not start with `test_`; the glob stays non-recursive. Reason: a recursive glob would change the inventory policy, a non-goal.

[DETAIL] **D-6 (spec review S-3, a check on where the file is written)**: the control test records the listing of the repository's scripts/ before and after its run and asserts it is unchanged; a guard test plants a write into the repository's scripts/ and shows the control test then fails. Reason: criterion 1 needs a test that turns red when the write goes back into the shared tree.

[DETAIL] **D-7 (spec review S-4, no empty inventory)**: both inventory tests (`test_every_script_has_a_caller_or_a_declared_reason`, `test_every_script_has_a_test_or_a_declared_reason`) assert that the default `_scripts()` list is non-empty and contains `stage2.py`, so a default pointed at an empty or temporary tree turns them red. Reason: the spec's purpose is not to weaken the real inventory checks.

[DETAIL] **D-8 (spec review S-5, the test id)**: the change concerns `tests/test_ci.py::test_the_glob_itself_finds_a_real_orphan_shell_script`; `test_an_orphan_shell_script_gets_flagged` already writes no file and stays as it is. Reason: only the first creates a file.

[DETAIL] **D-9 (spec review S-6, what the classification reads)**: the isolated case reads the real `.github/workflows/ci.yml`, `scripts/verify_all.sh` and `OHNE_AUFRUFER` in place, read-only; only the orphan script lives in the temporary tree. Reason: the check keeps judging against the real callers.

