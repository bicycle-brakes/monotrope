---
title: "Findings — verify-stages-new-files"
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
tags: [findings, stage-2]
---

# Findings — verify-stages-new-files

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: both
cases of the new test failed before the edit (`git ls-files` during
`make verify` lacked `scripts/new_tool.py`). All 923 tests in
`test_stage2.py`, `test_stage2_runs.py` and `test_kit.py` pass except the
root-only one.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- `restore_baseline` runs `git restore --staged --worktree`, which drops
  an intent-to-add entry whose path the baseline lacks, and `git clean`
  removes the file; no entry outlives a restore.
- When a run fails without a restore, the entries stay; the next run's
  pre-existing-change check lists those paths as it listed the untracked
  files before, so nothing new slips through.
- `changed_paths` and the credential scans list the same paths as before:
  an intent-to-add file is still a change against `HEAD`.

## Independent runner review, 2026-10-25

An Opus sub-agent of the orchestrating session reviewed the runner with all
open pull requests merged (read-only, in a separate context). Its row for
this change:

| ID | Severity | Finding | Status |
|---|---|---|---|
| R-5 | MINOR | When every attempt fails at `make verify`, no `restore_baseline` runs, so the intent-to-add entries stay in the operator's index: `git stash -u` refuses ("not uptodate"), and a new file deleted by hand leaves an entry `changed_paths` cannot see (reproduced). | fixed — tests/test_stage2.py::test_a_failed_run_leaves_no_intent_to_add_entry |

`verify_attempt` now drops the entries with `git reset` in a `finally`
right after `make verify`; the checkpoint still stages the content whole.
The self-review line above that said "no entry outlives a restore" was
true but missed the failure without a restore.

## Pre-review by an Opus 5.5 subagent, 2026-10-25

At the maintainer's request a read-only Opus 5.5 subagent reviewed the change
before phase 6 (Codex, unreachable here); phase 6 is still owed. Repairs by a
Sonnet 5.5 subagent at the orchestrator's direction.

| ID | Severity | Finding | Status |
|---|---|---|---|
| P242-1 | MINOR | Every name was a command-line argument, so about 30,000 untracked files raised an uncaught `OSError: Argument list too long`. Names now go via stdin (`--pathspec-from-file=- --pathspec-file-nul`) and an `OSError` becomes a diagnostic. | fixed — tests/test_stage2.py::test_intend_new_files_passes_no_file_name_on_the_command_line, tests/test_stage2.py::test_an_oserror_from_the_intent_to_add_call_becomes_a_diagnostic |
| P242-2 | MINOR | Names were read as pathspec patterns and the drop reset to HEAD: `[i].md` matched the caller's staged `i.md` and unstaged it, `:notes.md` made `git add -N` fail, a caller's `git rm --cached` was undone. Now `--literal-pathspecs` with `rm --cached --ignore-unmatch -f`. | fixed — tests/test_stage2.py::test_intent_to_add_reads_names_as_paths_and_leaves_the_callers_index_alone, tests/test_stage2.py::test_a_new_file_named_like_pathspec_magic_is_added_and_dropped |
| P242-3 | NIT | The `intend_new_files` docstring said `restore_baseline` drops the entry. | fixed — docstring now names `verify_attempt` right after `make verify`; no test |
| P242-4 | NIT | spec.md lacked the criterion that no entry outlives `make verify`, and plan.md lacked ledger rows for the later tests. | fixed — spec.md criterion 3, plan.md ledger rows; checked by scripts/check_criterion_ledger.py |
| P242-5 | NIT | A nested repository without a commit makes `git add --intent-to-add` fail, so the attempt gets a diagnostic before `make verify` instead of failing later at the checkpoint's `git add -A`. The outcome barely changes; no code change. | accepted — no test |

## Review loop skipped, 2026-10-25

The review loop (phase 4b) did not run on this change. The maintainer
answered on 2026-10-25 (night-run plan, `docs/research/2026-10-25-night-run-plan.md`,
answer 1) that the small cloud-session fixes get phase 6 only tonight,
because each had the Opus 5.5 pre-review recorded above. Phase 6 follows in
a fresh Codex session.

Stage-2 call, 2026-10-25: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 552 files, 2110 commits, 12 rules.

## Phase 6 — Codex, 2026-10-25

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MAJOR | SPEC | Phase 6 | scripts/stage2.py:4033–4038 | If index cleanup fails—for example because an interrupted Git operation leaves `index.lock`—the exception is silently suppressed. A failed final attempt leaves the new files intent-to-add; a green verifier returns no cleanup diagnostic. Report the failure and require successful cleanup before accepting the attempt. [Acceptance criterion 3] | Codex | taken — test: when dropping the intent-to-add entries fails (an `index.lock` left by an interrupted Git operation), the attempt is not accepted and the failure is named in the diagnostics (orchestrator, 2026-10-25) | — |

Phase 6 verdict: codex 01a174cf-5a9e-7441-a9e2-72695c87a35c, 2026-10-25
Reviewer session: codex 01a174cf-5a9e-7441-a9e2-72695c87a35c — a fresh session reviewed: no phase-2a session was recorded

Loop rows: none — the loop did not run for this change.
