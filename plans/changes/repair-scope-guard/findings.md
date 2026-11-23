---
title: "Findings — repair-scope-guard"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-23
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
| S-1 | BLOCKER | SPEC | base | spec.md, criterion 6 and Terms "New file"; decisions.md, third [DETAIL] item | [AMBIGUITY] "Restored to the pre-attempt baseline using the existing failure handling" fits two existing paths, and they behave differently. Reading A: the refusal is a post-run problem like a failing test. `run_attempts` then writes the diagnostic block into findings.md and puts back only the snapshotted inputs (`scripts/stage2.py:10141-10151`). The next route starts on the tree the refused attempt left, and after the last route `CallFailed(closing)` leaves the files in place (`:10201`). So the stray file stays, which is criterion 6's own refutation. And because Terms measures "absent before the attempt", attempt 2 does not count attempt 1's leftover as new, so attempt 2's checkpoint `git add -A` commits it. Reading B: the refusal works like the held-path refusal in `checkpoint` (`:7640-7652`, handler `:10108-10134`). `restore_baseline` runs on everything except findings.md, the run stops with no retry, and findings.md goes back to its pre-call snapshot, so the diagnostic is left only in the raised error text. A gives up to three attempts and a dirty tree or a committed stray file; B gives one attempt and a clean tree. The decisions text "fails the post-run check, is stored and restored like a held-path attempt" mixes both. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading B — an out-of-scope new file is classified at the checkpoint, beside uncommittable, so it takes the held-path path: the attempt is stored under refs/stage2/attempts, the worktree and findings.md are restored to the snapshot, and the next route starts clean. Reason: the stray file must not survive the attempt (criterion 6) | — |
| S-2 | MAJOR | SPEC | base | spec.md, Terms "New file" ("including an untracked, ignored …"); criterion 3 | Missing: which ignored additions count, and when "afterwards" is measured. The definition takes in every ignored addition. But a repair that runs tests, and the runner's own targeted check or `make verify`, create ignored files outside the scope: `__pycache__/*.pyc` beside a module imported for the first time, tool caches, `.DS_Store`, entries under `.venv/` or `.stage2-sessions/`. `derived_leftover` exempts only bytecode the runner's renderer wrote. The spec does not say whether tool- and runner-derived ignored files are exempt, or whether the guard measures right after the model call (`after = worktree_tree`) or after verification. A builder has to invent both. One choice refuses ordinary test-running repairs; the other lets ignored stray files through. As written, criterion 3 forbids any exemption ("an ignored … out-of-scope new file is accepted" refutes it). | Opus | in spec — [DETAIL] decided by the orchestrator: ignored files are not new files for this guard; only untracked files that git does not ignore and files added to the index count, measured at the checkpoint after the runner's own checks. Reason: test runs and tool caches create ignored files outside every scope | — |
| S-3 | MAJOR | SPEC | base | spec.md, Terms "Repair scope" ("the individual paths named in … the accepted plan"); criterion 4 | [AMBIGUITY] Reading A: every path that appears anywhere in plan.md is in scope. That includes the "What you do not touch" list that `prompts/03-plan.md` requires and the held paths a plan sends to the orchestrator, so the files the plan forbids become files the guard permits. Reading B: only the plan's list of files to create, change or delete is in scope. That needs a parser for one plan section, and the spec does not name it. The two readings permit different new files and need different tests for criterion 4. | Opus | in spec — [DETAIL] decided by the orchestrator: plan.md leaves the repair scope; the scope is the change folder, tests/ and the paths the taken rows' Where cells name. decisions.md is corrected. Reason: no plan-section parser, and the plan's do-not-touch list must not become permission | — |
| S-4 | MAJOR | SPEC | base | spec.md, Terms "Repair scope" ("named in a taken row's Where cell") | Missing: how a path is read from a Where cell. The cells in the repository take forms like `` `scripts/x.py`, `symbol` ``, `tests/test_model_endpoints.py:312`, bare `spec.md` or `plan.md` meant relative to the change folder, and prose with no path at all. The spec does not say whether a `:line` suffix is stripped, whether a bare file name resolves against the change folder or the repository root, or whether a directory named in a cell (for example `scripts/kit/`) grants the files below it. "Does not grant its siblings" covers siblings, not descendants. | Opus | in spec — [DETAIL] decided by the orchestrator: one extraction shared with repair-hand-held-rows (bead coding-harness-0zhf, its S-1, S-12, S-13): path-like tokens and Markdown link text and target, a trailing :line or :line-line dropped, a bare file name resolved against the change folder first and then the repository root, a token that is an existing tracked directory or ends in a slash grants its descendants; whichever change merges second reuses the helper. Reason: one rule for what a Where cell names | — |
| S-5 | MINOR | SPEC | base | spec.md, criterion 2 ("states the repair scope") | [AMBIGUITY] Reading A: both prompts state the rule in words (change folder, `tests/`, the paths in the taken Where cells and the plan), and the model applies the extraction itself. A fixed-text test then proves the criterion. Reading B: the prompts list the resolved paths the guard will accept, as decisions.md's "the scope named below" suggests. The prompt and the guard must then share one extraction, and the test must find concrete paths from a fixture row and plan in the prompt. The refutation ("either prompt omits the scope") does not tell the two apart. | Opus | in spec — [DETAIL] decided by the orchestrator: Reading A — both prompts state the rule in words (change folder, tests/, the paths the taken rows name, no handover or journal files); a fixed-text test proves it. Reason: the guard is the enforcement, the prompt the warning | — |
| S-6 | MINOR | SPEC | base | spec.md, criterion 6, refutation "the failure record lacks the diagnostic" | Cannot go red as written, because "failure record" is not defined. It could be the attempt block in findings.md (post-run path), the `CheckpointRolledBack` text on stderr (held-path path, which puts findings.md back to its snapshot), the saved attempt ref under `refs/stage2/attempts/`, or the loop record. A test cannot know which one to read and so cannot show the diagnostic missing. | Opus | in spec — [DETAIL] decided by the orchestrator: the failure record is the checkpoint refusal text the runner prints and stores with the attempt ref; the test reads that text and requires each out-of-scope path in it. Reason: the S-1 path defines where the record lives | — |
| S-7 | MINOR | SPEC | base | spec.md, Definition of Done, second bullet; criterion 1 | Missing: who writes the `prompts/03-plan.md` edit. `prompts/` is in `RUNNER_HELD`, so no phase-4 attempt can commit it. `test_the_plan_prompt_names_every_runner_held_path` (`tests/test_stage2.py:977`) checks drift in both directions, so adding `docs/journal/` to `RUNNER_HELD` turns that test red unless the prompt changes in the same tree. An implement attempt therefore cannot go green on its own. The spec says the two "move together" but does not say the prompt edit is the orchestrator's hand edit, or in what order the commits land. | Opus | in spec — [DETAIL] decided by the orchestrator: the orchestrator adds docs/journal/ to RUNNER_HELD and the matching line to prompts/03-plan.md in one hand commit on this branch before implement, so test_the_plan_prompt_names_every_runner_held_path stays green throughout; implement does the rest. Reason: prompts/ is runner-held, and splitting the pair turns that test red | — |

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1153 files, 5135 commits, 12 rules.

Stage-2 call, 2026-11-23: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1177 files, 5423 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +22 -0
> - `plans/changes/repair-scope-guard/plan.md` +9 -9
> - `scripts/stage2.py` +161 -7
> - `tests/test_stage2.py` +314 -8
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_stage2.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> E           AssertionError: an ignored file stays on disk through the restore
> E           assert False
> E            +  where False = exists()
> E            +    where exists = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3265/popen-gw1/test_repair_scope_ignores_untr0/repo/cache/pycache.bin').exists
>
> tests/test_stage2.py:16902: AssertionError
> _______ test_repair_scope_refusal_restores_attempt_and_keeps_diagnostic ________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/repair-scope-guard/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3265/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3265/popen-gw2/test_repair_scope_refusal_rest0/state'))
> capsys = <_pytest.capture.CaptureFixture object at 0x10b5271a0>
>
>     def test_repair_scope_refusal_restores_attempt_and_keeps_diagnostic(
>         world: World, capsys: pytest.CaptureFixture[str]
>     ) -> None:
>         """Criterion 6 (bead coding-harness-t83): the refusal names the stray path and the saved attempt,
>         restores the baseline and the pre-call findings, and stops the run without a retry."""
>         seed_tests(world)
>         world.write_record([("L1-1", "taken — test_a", "no")])
>         script_repair(
>             world,
>             [
>                 repair_step(plant={"src/app.py": "value = 2\n", "tests/test_fix.py": FIX_TEST, "src/stray.txt": "s\n"}),
>                 repair_step(plant={"src/app.py": "value = 3\n", "tests/test_fix.py": FIX_TEST}),
>             ],
>             make=[GREEN, GREEN],
>         )
>         baseline = git(world.root, "rev-parse", "HEAD")
>         assert world.run("repair") == 1
>         error = capsys.readouterr().err
>         assert len(repair_calls(world)) == 1, "a refused scope guard started another route"
>         assert len(world.calls("make")) == 1, "the refused run kept no second full check"
>         assert "the repair left new files outside its scope" in error
>         assert "`src/stray.txt`" in error
>         assert "the attempt is saved at refs/stage2/attempts/demo/repair-attempt-1" in error
>         assert git(world.root, "rev-parse", "HEAD") == baseline
>         assert (world.root / "src" / "app.py").read_text(encoding="utf-8") == "value = 1\n"
>         assert not (world.root / "src" / "stray.txt").exists()
>         assert "fixed — tests/test_fix.py::test_fix" not in world.text()
>         saved = git(world.root, "for-each-ref", "--format=%(refname)", "refs/stage2/attempts/demo")
>         assert any(name.startswith("refs/stage2/attempts/demo/repair-attempt-1-") for name in saved.split("\n")), saved
>         # The restored baseline takes a fresh run: the record is re-seeded, the repair commits once.
>         world.write_record([("L1-1", "taken — test_a", "no")])
>         script_repair(world, [repair_step()], make=[GREEN])
> >       assert world.run("repair") == 0, "the restored baseline takes a fresh repair"
> E       AssertionError: the restored baseline takes a fresh repair
> E       assert 1 == 0
> E        +  where 1 = run('repair')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3265/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-3265/popen-gw2/test_repair_scope_refusal_rest0/state')).run
>
> tests/test_stage2.py:16819: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 34 files, 3 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> failed: the repair left new files outside its scope: `plans/INDEX.md`. No commit was made; the attempt is saved at refs/stage2/attempts/demo/repair-attempt-1-20261123T070721558668Z (6ee754a750db); `git diff 2bdc341448ff refs/stage2/attempts/demo/repair-attempt-1-20261123T070721558668Z` shows it; the runner restored the worktree to 2bdc341448ff (undone: plans/INDEX.md, plans/changes/demo/plan.md, plans/changes/demo/research.md, src/app.py, tests/test_fix.py); rerun the verb or add --stage2-off.;  [… 170 characters left out …]
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_repair_prompts_state_scope_restrictions[endpoint1]
> FAILED tests/test_stage2.py::test_repair_prompts_state_scope_restrictions[endpoint0]
> FAILED tests/test_stage2.py::test_stage2_journal_paths_are_held[repair-case-variant]
> FAILED tests/test_stage2.py::test_stage2_journal_paths_are_held[repair-edit]
> FAILED tests/test_stage2.py::test_stage2_journal_paths_are_held[repair-add]
> FAILED tests/test_stage2.py::test_repair_allows_new_paths_within_scope - Asse...
> FAILED tests/test_stage2.py::test_repair_scope_guard_allows_existing_tracked_edits
> FAILED tests/test_stage2.py::test_each_repair_retry_must_add_its_own_time_entry[False-2]
> FAILED tests/test_stage2.py::test_each_repair_retry_must_add_its_own_time_entry[True-2]
> FAILED tests/test_stage2.py::test_repair_scope_ignores_untracked_ignored_files[False]
> FAILED tests/test_stage2.py::test_stage2_journal_paths_are_held[implement-case-variant]
> FAILED tests/test_stage2.py::test_idle_retry_cannot_reuse_previous_work[repair]
> FAILED tests/test_stage2.py::test_each_repair_retry_must_add_its_own_time_entry[True-3]
> FAILED tests/test_stage2.py::test_each_repair_retry_must_add_its_own_time_entry[False-3]
> FAILED tests/test_stage2.py::test_repair_scope_ignores_untracked_ignored_files[True]
> FAILED tests/test_stage2.py::test_repair_scope_refusal_restores_attempt_and_keeps_diagnostic
> 16 failed, 7 passed in 14.94s
> ```
