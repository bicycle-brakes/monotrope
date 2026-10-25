---
title: "Plan — dirty-index"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-0c8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, dirty-tree]
---

# Plan — dirty-index

```text
For you:     A change you staged and then reverted in the file stops the runner before a model call instead of being overwritten by its commit.
Done when:   changed_paths lists index-only changes, the three writing verbs refuse them, the tests were red first, and make verify is green.
Appetite:    1 hour of phase 4, repairs included; stop at the limit.
Not now:     Which paths an attempt may commit (coding-harness-wqw, coding-harness-qr03).
Pre-mortem:  suppose it failed: most likely because --cached was run without the compared commit and listed the wrong base.
Starts unless you say stop.
```

## Files and steps

1. Change `tests/test_stage2.py`: add the regression functions named in the
   ledger, next to `test_a_draft_refuses_changes_outside_findings`.
2. Change `scripts/stage2.py`: in `changed_paths`, add
   `git diff --cached --no-renames --name-only -z <against>` to the tracked
   listing; update its docstring.
3. Update `plans/changes/dirty-index/plan.md` (ledger, time) and
   `plans/changes/dirty-index/findings.md`; regenerate `plans/INDEX.md`.

## Implementation contract

- `--cached <against>` compares the index with the same commit as the
  working-tree diff, so `against=base` callers keep their meaning.
- The tests stage a change to `src/app.py`, restore the working file with
  `git checkout -- src/app.py` semantics (write the committed content back),
  and assert the staged blob (`git diff --cached`) and the file afterwards.
- Do not touch `checkpoint`, prompts, endpoints or other verbs.

## Verification

Run the new tests before the production edit to show them red, then:

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'index_only or changed_paths_lists'
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_changed_paths_lists_an_index_only_change — an index-only change is missing from the result.
- 2: tests/test_stage2.py::test_writing_verbs_refuse_an_index_only_change — a model call, another exit or a diagnostic without the path.
- 3: tests/test_stage2.py::test_writing_verbs_refuse_an_index_only_change — the staged blob or the working file changed.
- 4: tests/test_stage2.py::test_changed_paths_lists_each_kind_once — a working-tree or untracked path missing or listed twice.

## Route

Spec, plan, implementation and self-review by the orchestrating Claude Code
session in a cloud container on 2026-10-25, at the maintainer's instruction
(conversation 2026-10-25): Codex, GLM and OpenCode Go are unreachable there.
The review loop and the phase-6 Codex review are still owed.

## Time used
2026-10-25 10:48:42–11:04:10 UTC, 928 s — research, spec, plan, implement and self-review · orchestrating session · model claude-opus-5-5 · accepted · measured by the orchestrator
