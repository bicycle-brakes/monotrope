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

## Route

Research, spec, plan, implementation and self-review by the orchestrating
Claude Code session in a cloud container on 2026-10-25, at the maintainer's
instruction. The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 12:17:12–12:24:31 UTC, 439 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
