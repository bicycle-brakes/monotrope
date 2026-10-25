---
title: "Plan — explore-role"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-e7m
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, explore]
---

# Plan — explore-role

```text
For you:     A fallback explorer is told it is the explorer, and an answer that is no research is shown and refused instead of landing in research.md.
Done when:   Both criteria have tests that were red first, existing explore tests still pass, and make verify is green.
Appetite:    1 hour of phase 4; stop at the limit.
Not now:     Routing --stage2-off explore to Sonnet (the maintainer's routing decision).
Pre-mortem:  suppose it failed: most likely because real research names paths the check does not recognise.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: the two new tests; existing stand-in answers
   for `explore` name `src/app.py`, as real research names its sources.
2. `scripts/stage2.py`: `EXPLORER_ROLE` in the prompt addition;
   `names_a_repository_file`; `explore` refuses an answer without one.
3. `docs/WORKFLOW.md` §4 `explore` line: one sentence on the new behaviour.
4. This plan, `findings.md`, `plans/INDEX.md`.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'explore'
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_the_explore_prompt_states_the_models_role_and_tools — a prompt lacks the role.
- 2: tests/test_stage2.py::test_an_exploration_answer_without_a_repository_path_fails_and_appends_nothing — the answer is appended or not shown.
- 3: tests/test_stage2.py::test_explore_uses_flash_read_only_and_appends_research — an answer with a path is refused.
- 1: tests/test_stage2.py::test_the_explorer_role_does_not_name_the_runner_script — the role names `scripts/stage2.py` or lacks the Grep and answer clauses.
- 2: tests/test_stage2.py::test_a_refused_exploration_answer_shows_its_last_forty_lines — the head of the answer is shown, or not its tail.
- 3: tests/test_stage2.py::test_an_absolute_path_inside_the_worktree_counts_and_one_outside_does_not — an absolute path inside counts not, or `/etc/passwd` counts.
- 3: tests/test_stage2.py::test_a_path_at_the_end_of_a_sentence_counts — a path followed by a full stop or other punctuation is missed.
- 3: tests/test_stage2.py::test_a_refusal_that_echoes_the_explorer_role_is_refused — the role's own wording passes the check.
- 3: tests/test_stage2.py::test_a_path_after_the_five_thousandth_word_still_counts — filler words hide a later path.
- 3: tests/test_stage2.py::test_a_windows_separator_in_a_path_counts — a backslash path is missed.
- 3: tests/test_stage2.py::test_a_bare_top_level_name_counts_only_if_it_is_a_root_entry — `Makefile` is skipped, or an unknown bare word counts.
- 3: tests/test_stage2.py::test_a_git_internal_path_does_not_count — `.git/config` satisfies the check.

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction. The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 12:17:12–12:24:31 UTC, 439 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
