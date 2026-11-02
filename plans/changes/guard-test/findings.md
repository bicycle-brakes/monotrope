---
title: "Findings — guard-test"
category: findings
status: draft
implementation_status: none
date: 2026-10-29
created: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-0ho
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — guard-test

Stage-2 call, 2026-10-29: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 733 files, 2624 commits, 12 rules.

ADR answer owed: decisions/answers/guard-test/adr.yaml does not exist and the gate tolerated that for this run; the answer is the maintainer's (python3 scripts/harness.py decide adr).

Stage-2 call, 2026-11-01: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 808 files, 2981 commits, 12 rules.

Stage-2 call, 2026-11-01: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 808 files, 2991 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/guard-test/design.md` +2 -2
> - `plans/changes/guard-test/plan.md` +18 -18
> - `plans/changes/guard-test/spec.md` +2 -2
> - `scripts/check_guard_test_environment.py` +45 -0
> - `scripts/stage2.py` +217 -53
> - `tests/test_ci.py` +58 -0
> - `tests/test_stage2.py` +478 -4
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `scripts/check_guard_test_environment.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> scripts/stage2.py:6157:12: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>      |
> 6155 |         return ""
> 6156 |     for node in ast.walk(tree):
> 6157 |         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function:
>      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 6158 |             start = min([node.lineno, *(item.lineno for item in node.decorator_list)])
> 6159 |             return "\n".join(body.splitlines()[start - 1 : node.end_lineno])
>      |
>      = help: Convert to `X | Y`
>
> tests/test_stage2.py:12992:16: F821 Undefined name `check_criterion_ledger`
>       |
> 12990 |         "- 3: taken — guard test — a reason",
> 12991 |     ):
> 12992 |         assert check_criterion_ledger.parse_entry(line) is None, line
>       |                ^^^^^^^^^^^^^^^^^^^^^^ F821
> 12993 |     for line in (
> 12994 |         "- 3: tests/test_fix.py::test_fix",
>       |
>
> tests/test_stage2.py:12998:16: F821 Undefined name `check_criterion_ledger`
>       |
> 12996 |         "- 3: not a test — phase 6 reads every guard test a change adds",
> 12997 |     ):
> 12998 |         assert check_criterion_ledger.parse_entry(line) is not None, line
>       |                ^^^^^^^^^^^^^^^^^^^^^^ F821
>       |
>
> Found 3 errors.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-01: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 809 files, 3001 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/guard-test/plan.md` +16 -16
> - `scripts/stage2.py` +1 -1
> - `tests/test_stage2.py` +1 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
>
> ==================================== ERRORS ====================================
> ____________________ ERROR collecting tests/test_stage2.py _____________________
> tests/test_stage2.py::test_guard_answer_requires_explicit_row_authorisation: in "parametrize" the number of names (2):
>   ('status', 'why')
> must be equal to the number of values (1):
>   ('taken — test_a',)
> ____________________ ERROR collecting tests/test_stage2.py _____________________
> tests/test_stage2.py::test_guard_answer_requires_explicit_row_authorisation: in "parametrize" the number of names (2):
>   ('status', 'why')
> must be equal to the number of values (1):
>   ('taken — test_a',)
> ____________________ ERROR collecting tests/test_stage2.py _____________________
> tests/test_stage2.py::test_guard_answer_requires_explicit_row_authorisation: in "parametrize" the number of names (2):
>   ('status', 'why')
> must be equal to the number of values (1):
>   ('taken — test_a',)
> ____________________ ERROR collecting tests/test_stage2.py _____________________
> tests/test_stage2.py::test_guard_answer_requires_explicit_row_authorisation: in "parametrize" the number of names (2):
>   ('status', 'why')
> must be equal to the number of values (1):
>   ('taken — test_a',)
> ____________________ ERROR collecting tests/test_stage2.py _____________________
> tests/test_stage2.py::test_guard_answer_requires_explicit_row_authorisation: in "parametrize" the number of names (2):
>   ('status', 'why')
> must be equal to the number of values (1):
>   ('taken — test_a',)
> ____________________ ERROR collecting tests/test_stage2.py _____________________
> tests/test_stage2.py::test_guard_answer_requires_explicit_row_authorisation: in "parametrize" the number of names (2):
>   ('status', 'why')
> must be equal to the number of values (1):
>   ('taken — test_a',)
> ____________________ ERROR collecting tests/test_stage2.py _____________________
> tests/test_stage2.py::test_guard_answer_requires_explicit_row_authorisation: in "parametrize" the number of names (2):
>   ('status', 'why')
> must be equal to the number of values (1):
>   ('taken — test_a',)
> ____________________ ERROR collecting tests/test_stage2.py _____________________
> tests/test_stage2.py::test_guard_answer_requires_explicit_row_authorisation: in "parametrize" the number of names (2):
>   ('status', 'why')
> must be equal to the number of values (1):
>   ('taken — test_a',)
> =========================== short test summary info ============================
> ERROR tests/test_stage2.py - Failed: tests/test_stage2.py::test_guard_answer_...
> ERROR tests/test_stage2.py - Failed: tests/test_stage2.py::test_guard_answer_...
> ERROR tests/test_stage2.py - Failed: tests/test_stage2.py::test_guard_answer_...
> ERROR tests/test_stage2.py - Failed: tests/test_stage2.py::test_guard_answer_...
> ERROR tests/test_stage2.py - Failed: tests/test_stage2.py::test_guard_answer_...
> ERROR tests/test_stage2.py - Failed: tests/test_stage2.py::test_guard_answer_...
> ERROR tests/test_stage2.py - Failed: tests/test_stage2.py::test_guard_answer_...
> ERROR tests/test_stage2.py - Failed: tests/test_stage2.py::test_guard_answer_...
> 8 errors in 11.91s
> ```

Stage-2 call, 2026-11-01: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 809 files, 3001 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2.py` +5 -5
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         proofs: list[tuple[str, dict[str, str]]] = []
>     
>         def spy(command: list[str], cwd: Path, env: dict[str, str], key: str | None, **kwargs: object):
>             if len(command) > 1 and command[1] == "-c":
>                 proofs.append((str(cwd), dict(env)))
>             return real_launch(command, cwd, env, key, **kwargs)
>     
>         monkeypatch.setattr(stage2, "launch", spy)
> >       assert world.run("repair") == 0
>
> tests/test_stage2.py:12685: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2.py:361: in run
>     return stage2.main([*argv, *options, "--root", str(self.root)])
> scripts/stage2.py:8626: in main
>     return _run(args)
> scripts/stage2.py:8679: in _run
>     repair(Path(args.root), args.change, args.stage2_off)
> scripts/stage2.py:7934: in repair
>     run_attempts(
> scripts/stage2.py:7070: in run_attempts
>     answer, _ = run_codex(ctx, prompt, writable=True, verb=verb)
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> ctx = Context(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-6786/popen-...pen-gw6/test_guard_proof_uses_attempt_0/repo/plans/changes/demo'), bead='demo-1', models_store=None, go_admission=None)
> prompt = "# Phase 4 · Implement\n\n**Model:** GLM 5.3 Flash — a solid worker given a clear plan; through\n`python3 scripts/stag...ead: demo-1\n---\n\n# Plan\n\n## Time used\n\n\nRead nothing outside this worktree and the repository's git directory."
> resume = None, writable = True
>
>     def run_codex(
>         ctx: Context, prompt: str, resume: str | None = None, writable: bool = False, *, verb: str
>     ) -> tuple[str, str]:
>         """One Codex call, first or resumed, pinned the same way. Returns (answer, thread id).
>     
>         A review reads in the CLI's `read-only` sandbox; a draft writes in
>         `workspace-write`, and the runner puts back what lands outside the change
>         folder. No call takes a bypass flag (spec, criterion 1). The reasoning
>         effort is the caller verb's entry of `CODEX_EFFORTS`, passed explicitly on
>         every argv, a resumed call included; that a resumed thread actually runs at
>         that effort inside Codex is not asserted (bead coding-harness-yzk, Q-6).
>         Only the verbs `CODEX_EFFORTS` names (draft, repair, review) may carry a
>         Codex route; any other verb stops with a `KeyError` before the call.
>         """
>         _, model, _ = CODEX
>         effort = CODEX_EFFORTS[verb]
>         with tempfile.TemporaryDirectory(prefix="stage2-") as tmp:
>             answer_file = Path(tmp) / "answer.md"
>             command = ["codex", "exec"]
>             if resume:
>                 command += ["resume", resume]
>             command += [
>                 "--json",
>                 "-m",
>                 model,
>                 "-c",
>                 f'model_reasoning_effort="{effort}"',
>                 "-c",
>                 f'sandbox_mode="{"workspace-write" if writable else "read-only"}"',
>                 "--disable",
>                 "hooks",
>                 "--disable",
>                 "memories",
>                 "-o",
>                 str(answer_file),
>                 prompt,
>             ]
> >           done = launch(command, ctx.root, foreign_env({}))
> E           TypeError: test_guard_proof_uses_attempt_code_and_planted_switch.<locals>.spy() missing 1 required positional argument: 'key'
>
> scripts/stage2.py:2520: TypeError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 30 files, 3 commits, 1 rules, 1 prompt texts
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_guard_environment_gate_goes_red_when_the_switch_is_present
> FAILED tests/test_stage2.py::test_guard_form_keeps_other_repair_forms_and_environments_strict
> FAILED tests/test_stage2.py::test_guard_proof_preserves_outcome_and_execution_guards[expected-fail]
> FAILED tests/test_stage2.py::test_guard_repairs_write_statuses_and_marks_only_after_complete_proof
> FAILED tests/test_stage2.py::test_guard_proof_requires_clean_green_without_the_switch
> FAILED tests/test_stage2.py::test_guard_proof_uses_attempt_code_and_planted_switch
> 6 failed, 27 passed in 40.02s
> ```
