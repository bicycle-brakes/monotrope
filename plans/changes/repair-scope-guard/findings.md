---
title: "Findings — repair-scope-guard"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-t83
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — repair-scope-guard

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5128 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1153 files, 5130 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | BLOCKER | SPEC | base | spec.md, criterion 6 and Terms "New file"; decisions.md, third [DETAIL] item | [AMBIGUITY] "Restored to the pre-attempt baseline using the existing failure handling" fits two existing paths, and they behave differently. Reading A: the refusal is a post-run problem like a failing test. `run_attempts` then writes the diagnostic block into findings.md and puts back only the snapshotted inputs (`scripts/stage2.py:10141-10151`). The next route starts on the tree the refused attempt left, and after the last route `CallFailed(closing)` leaves the files in place (`:10201`). So the stray file stays, which is criterion 6's own refutation. And because Terms measures "absent before the attempt", attempt 2 does not count attempt 1's leftover as new, so attempt 2's checkpoint `git add -A` commits it. Reading B: the refusal works like the held-path refusal in `checkpoint` (`:7640-7652`, handler `:10108-10134`). `restore_baseline` runs on everything except findings.md, the run stops with no retry, and findings.md goes back to its pre-call snapshot, so the diagnostic is left only in the raised error text. A gives up to three attempts and a dirty tree or a committed stray file; B gives one attempt and a clean tree. The decisions text "fails the post-run check, is stored and restored like a held-path attempt" mixes both. | Opus | open | — |
| S-2 | MAJOR | SPEC | base | spec.md, Terms "New file" ("including an untracked, ignored …"); criterion 3 | Missing: which ignored additions count, and when "afterwards" is measured. The definition takes in every ignored addition. But a repair that runs tests, and the runner's own targeted check or `make verify`, create ignored files outside the scope: `__pycache__/*.pyc` beside a module imported for the first time, tool caches, `.DS_Store`, entries under `.venv/` or `.stage2-sessions/`. `derived_leftover` exempts only bytecode the runner's renderer wrote. The spec does not say whether tool- and runner-derived ignored files are exempt, or whether the guard measures right after the model call (`after = worktree_tree`) or after verification. A builder has to invent both. One choice refuses ordinary test-running repairs; the other lets ignored stray files through. As written, criterion 3 forbids any exemption ("an ignored … out-of-scope new file is accepted" refutes it). | Opus | open | — |
| S-3 | MAJOR | SPEC | base | spec.md, Terms "Repair scope" ("the individual paths named in … the accepted plan"); criterion 4 | [AMBIGUITY] Reading A: every path that appears anywhere in plan.md is in scope. That includes the "What you do not touch" list that `prompts/03-plan.md` requires and the held paths a plan sends to the orchestrator, so the files the plan forbids become files the guard permits. Reading B: only the plan's list of files to create, change or delete is in scope. That needs a parser for one plan section, and the spec does not name it. The two readings permit different new files and need different tests for criterion 4. | Opus | open | — |
| S-4 | MAJOR | SPEC | base | spec.md, Terms "Repair scope" ("named in a taken row's Where cell") | Missing: how a path is read from a Where cell. The cells in the repository take forms like `` `scripts/x.py`, `symbol` ``, `tests/test_model_endpoints.py:312`, bare `spec.md` or `plan.md` meant relative to the change folder, and prose with no path at all. The spec does not say whether a `:line` suffix is stripped, whether a bare file name resolves against the change folder or the repository root, or whether a directory named in a cell (for example `scripts/kit/`) grants the files below it. "Does not grant its siblings" covers siblings, not descendants. | Opus | open | — |
| S-5 | MINOR | SPEC | base | spec.md, criterion 2 ("states the repair scope") | [AMBIGUITY] Reading A: both prompts state the rule in words (change folder, `tests/`, the paths in the taken Where cells and the plan), and the model applies the extraction itself. A fixed-text test then proves the criterion. Reading B: the prompts list the resolved paths the guard will accept, as decisions.md's "the scope named below" suggests. The prompt and the guard must then share one extraction, and the test must find concrete paths from a fixture row and plan in the prompt. The refutation ("either prompt omits the scope") does not tell the two apart. | Opus | open | — |
| S-6 | MINOR | SPEC | base | spec.md, criterion 6, refutation "the failure record lacks the diagnostic" | Cannot go red as written, because "failure record" is not defined. It could be the attempt block in findings.md (post-run path), the `CheckpointRolledBack` text on stderr (held-path path, which puts findings.md back to its snapshot), the saved attempt ref under `refs/stage2/attempts/`, or the loop record. A test cannot know which one to read and so cannot show the diagnostic missing. | Opus | open | — |
| S-7 | MINOR | SPEC | base | spec.md, Definition of Done, second bullet; criterion 1 | Missing: who writes the `prompts/03-plan.md` edit. `prompts/` is in `RUNNER_HELD`, so no phase-4 attempt can commit it. `test_the_plan_prompt_names_every_runner_held_path` (`tests/test_stage2.py:977`) checks drift in both directions, so adding `docs/journal/` to `RUNNER_HELD` turns that test red unless the prompt changes in the same tree. An implement attempt therefore cannot go green on its own. The spec says the two "move together" but does not say the prompt edit is the orchestrator's hand edit, or in what order the commits land. | Opus | open | — |
