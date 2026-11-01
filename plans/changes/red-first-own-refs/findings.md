---
title: "Findings — red-first-own-refs"
category: findings
status: draft
implementation_status: partial
date: 2026-11-01
created: 2026-11-01
last_reviewed: 2026-11-01
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-wkxm
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — red-first-own-refs

Stage-2 call, 2026-11-01: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 808 files, 2948 commits, 12 rules.

Stage-2 call, 2026-11-01: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 811 files, 2951 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/red-first-install/spec.md` +9 -1
> - `plans/changes/red-first-own-refs/plan.md` +11 -11
> - `plans/changes/red-first-own-refs/spec.md` +1 -1
> - `scripts/stage2.py` +152 -91
> - `tests/test_stage2.py` +381 -13
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> tests/test_stage2.py:11908:47: ARG001 Unused function argument: `args`
>       |
> 11906 |                     if proof == "baseline":
> 11907 |
> 11908 |                         def failing_copytree(*args, **kwargs):
>       |                                               ^^^^ ARG001
> 11909 |                             raise OSError(28, "planted copy failure")
>       |
>
> tests/test_stage2.py:11908:55: ARG001 Unused function argument: `kwargs`
>       |
> 11906 |                     if proof == "baseline":
> 11907 |
> 11908 |                         def failing_copytree(*args, **kwargs):
>       |                                                       ^^^^^^ ARG001
> 11909 |                             raise OSError(28, "planted copy failure")
>       |
>
> Found 2 errors.
> ```

Stage-2 call, 2026-11-01: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 811 files, 2957 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/red-first-own-refs/plan.md` +10 -10
> - `tests/test_stage2.py` +7 -6
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ........F............                                                    [100%]
> =================================== FAILURES ===================================
> ____________________ test_fixed_proof_refuses_tree_changes _____________________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/red-first-own-refs/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-6564/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-6564/popen-gw2/test_fixed_proof_refuses_tree_0/state'))
>
>     def test_fixed_proof_refuses_tree_changes(world: World) -> None:
>         """Criterion 7 (fixed tree). Planted fault: the named test modifies a Git-visible file of its
>         fixed checkout and still receives passing evidence."""
> >       plant_proof(world, "fixed")
>
> tests/test_stage2.py:11869: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2.py:11641: in plant_proof
>     (world.root / "tests" / "test_fix.py").write_text(FIX_TEST, encoding="utf-8")
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1047: in write_text
>     with self.open(mode='w', encoding=encoding, errors=errors, newline=newline) as f:
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> self = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-6564/popen-gw2/test_fixed_proof_refuses_tree_0/repo/tests/test_fix.py')
> mode = 'w', buffering = -1, encoding = 'utf-8', errors = None, newline = None
>
>     def open(self, mode='r', buffering=-1, encoding=None,
>              errors=None, newline=None):
>         """
>         Open the file pointed to by this path and return a file object, as
>         the built-in open() function does.
>         """
>         if "b" not in mode:
>             encoding = io.text_encoding(encoding)
> >       return io.open(self, mode, buffering, encoding, errors, newline)
> E       FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-6564/popen-gw2/test_fixed_proof_refuses_tree_0/repo/tests/test_fix.py'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1013: FileNotFoundError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_fixed_proof_refuses_tree_changes - FileNotF...
> 1 failed, 20 passed in 16.26s
> ```

Stage-2 call, 2026-11-01: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 811 files, 2958 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2.py` +1 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 54 lines of this gate left out …]
> ........................................................................ [ 84%]
> ........................................................................ [ 86%]
> ........................................................................ [ 88%]
> ........................................................................ [ 89%]
> ........................................................................ [ 91%]
> ........................................................................ [ 92%]
> ........................................................................ [ 94%]
> ........................................................................ [ 96%]
> ........................................................................ [ 97%]
> ........................................................................ [ 99%]
> ..........................                                               [100%]
> =================================== FAILURES ===================================
> ______________ test_no_git_launch_in_the_runner_names_a_bare_git _______________
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/red-first-own-refs/.venv/bin/python3
>
>     def test_no_git_launch_in_the_runner_names_a_bare_git() -> None:
>         """O192-4: source check for the sites no verb in this suite reaches (`show`, `worktree remove` and `prune`)."""
>         tree = ast.parse((REPO_ROOT / "scripts" / "stage2.py").read_text(encoding="utf-8"))
>         bare = [
>             node.lineno
>             for node in ast.walk(tree)
>             if isinstance(node, ast.List)
>             and node.elts
>             and isinstance(node.elts[0], ast.Constant)
>             and node.elts[0].value == "git"
>         ]
>         assert bare == [], f"a command list starts with a bare `git` at line(s) {bare}"
>         named = [
>             node.lineno
>             for node in ast.walk(tree)
>             if isinstance(node, ast.List)
>             and len(node.elts) > 1
>             and isinstance(node.elts[0], ast.Name)
>             and node.elts[0].id == "GIT"
>         ]
> >       assert len(named) >= 8, "fewer git launches name GIT than the eight this check was written against"
> E       AssertionError: fewer git launches name GIT than the eight this check was written against
> E       assert 7 >= 8
> E        +  where 7 = len([2294, 3743, 4022, 5593, 2269, 4761, ...])
>
> tests/test_stage2.py:948: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=94723) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/red-first-own-refs/tests/test_stage2.py:17515: DeprecationWarning: This process (pid=94730) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_no_git_launch_in_the_runner_names_a_bare_git
> 1 failed, 4400 passed, 17 skipped, 5 warnings in 685.26s (0:11:25)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 25252 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 811 files, 2965 commits, 12 rules.

Stage-2 call, 2026-11-01: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 811 files, 2966 commits, 12 rules.
