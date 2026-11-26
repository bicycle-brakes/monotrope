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

[DETAIL] **D-10 (spec review S-7, the kit probe; amends D-7)**: the inventory tests assert only that the default `_scripts()` list is non-empty; they name no particular script, because `tests/test_ci.py` travels to the kit probe's throwaway repository while `scripts/stage2.py` does not (`scripts/kit/manifest.yaml`, bestand). Reason: a named script would turn the probe red in a foreign repository.

[DETAIL] **D-11 (spec review S-8, writes during the run)**: criterion 1 is held by a test that runs the control case with file writes watched: every write the case attempts (`Path.write_text`, `Path.write_bytes`, `open` for writing) is recorded, and the test asserts none targets the repository's `scripts/`, so a write that is removed again in `finally` still turns it red. Reason: a before-and-after listing cannot see a file that is created and deleted inside the run.

[DETAIL] **D-12 (spec review S-9, where the guard writes; amends D-6)**: Reading B — the guard never writes into the checkout: it runs a planted variant of the control case against a stand-in repository root under tmp_path and shows the watcher of D-11 reports the write. Reason: the guard must not bring back the shared-tree write it exists to forbid.

[DETAIL] **D-13 (spec review S-10, the caller inputs)**: the control test spies on `_heimatlose_namen()` and asserts it received the checkout's `.github/workflows/ci.yml` and `scripts/verify_all.sh` texts and the module's `OHNE_AUFRUFER`, read in place. Reason: otherwise passing blank inputs stays green.

[DETAIL] **D-14 (spec review S-11, what the watcher sees; extends D-11)**: the watcher also records `os.open` with a write or create flag, `os.replace`, `os.rename`, `Path.touch` and `Path.mkdir` whose target lies under the repository's `scripts/`; writes from native code outside Python's file API are a named limit of the test. Reason: the orphan could otherwise be created or moved in without any recorded call.

[DETAIL] **D-15 (spec review S-12, where the guard writes)**: the guard asserts that the planted write target lies under its tmp_path stand-in root and outside the repository root before it runs the planted variant. Reason: a guard that wrote into the checkout would stay green while bringing the race back.

[DETAIL] **D-16 (spec review S-13, copied inputs)**: criterion 7 drops "copied" from its refutation: a byte-identical copy of `ci.yml` and `verify_all.sh` yields the same classification, so only different or blank inputs are refuted; D-9 (read in place) stays the implementation rule. Reason: the clause was not testable and changes no outcome.

