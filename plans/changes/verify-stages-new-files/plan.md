---
title: "Plan — verify-stages-new-files"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-fdz
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, verify]
---

# Plan — verify-stages-new-files

```text
For you:     An attempt that adds a new script no longer fails leerprobe only because the file was not in git yet.
Done when:   make verify sees the new file in git ls-files under implement and repair (test red first), and make verify is green.
Appetite:    1 hour of phase 4; stop at the limit.
Not now:     The draft verb; the probe itself.
Pre-mortem:  suppose it failed: most likely because an intent-to-add entry survived a restore and blocked the next run.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: the test named in the ledger.
2. `scripts/stage2.py`: `intend_new_files(root, env)`; `verify_attempt`
   calls it right before `make verify`.
3. This plan, `findings.md`, `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k "sees_the_attempts_new_files or leaves_no_intent_to_add or no_file_name_on_the_command or oserror_from_the_intent or reads_names_as_paths or pathspec_magic"
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_make_verify_sees_the_attempts_new_files_in_git — a new file is missing from git ls-files during make verify.
- 2: tests/test_stage2.py::test_make_verify_sees_the_attempts_new_files_in_git — the new file is missing from the checkpoint commit.
- 3: tests/test_stage2.py::test_a_failed_run_leaves_no_intent_to_add_entry — an intent-to-add entry or a changed staged state remains after a failed run.
- 3: tests/test_stage2.py::test_intend_new_files_passes_no_file_name_on_the_command_line — a file name is on the command line, so a very large untracked set overflows the argument list.
- 3: tests/test_stage2.py::test_an_oserror_from_the_intent_to_add_call_becomes_a_diagnostic — an OSError from the git call ends in a traceback instead of a diagnostic.
- 3: tests/test_stage2.py::test_intent_to_add_reads_names_as_paths_and_leaves_the_callers_index_alone — the caller's staged state changes after the drop.
- 3: tests/test_stage2.py::test_a_new_file_named_like_pathspec_magic_is_added_and_dropped — a file named like pathspec magic fails to be added or stays in the index.

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction. The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 12:30:39–12:34:34 UTC, 235 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
2026-10-25 20:47:10–20:57:56 UTC, 646 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-25 20:59:56–21:10:56 UTC, 660 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
