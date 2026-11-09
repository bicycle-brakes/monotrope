---
title: "Findings — outcome-test"
category: findings
status: draft
implementation_status: partial
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-3nm5
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — outcome-test

Stage-2 call, 2026-11-06: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 910 files, 3408 commits, 12 rules.

Stage-2 call, 2026-11-06: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 913 files, 3418 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +30 -1
> - `plans/changes/outcome-test/plan.md` +9 -9
> - `scripts/outcome_test.py` +824 -0
> - `scripts/outcome_test_questions.json` +61 -0
> - `tests/test_outcome_test.py` +736 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_outcome_test.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> scripts/outcome_test.py:232:20: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>     |
> 230 |             not isinstance(literal, ast.Constant)
> 231 |             or isinstance(literal.value, bool)
> 232 |             or not isinstance(literal.value, (int, float))
>     |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 233 |         ):
> 234 |             return Reading.unread(f"'{name}' is not a plain numeric literal")
>     |
>     = help: Convert to `X | Y`
>
> scripts/outcome_test.py:348:44: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>     |
> 346 |     """One verdict: exact per shape, no substring, no synonyms, no partial credit."""
> 347 |     if answer_type == "number":
> 348 |         if isinstance(answer, bool) or not isinstance(answer, (int, float)):
>     |                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 349 |             return False
> 350 |         if not math.isfinite(answer):
>     |
>     = help: Convert to `X | Y`
>
> Found 2 errors.
> No fixes available (2 hidden fixes can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-06: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 916 files, 3421 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/outcome_test.py` +2 -2
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ...F.....                                                                [100%]
> =================================== FAILURES ===================================
> ____________________ test_tool_only_writes_explicit_history ____________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/outcome-test/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-55/popen-gw0/test_tool_only_writes_explicit0')
>
>     def test_tool_only_writes_explicit_history(tmp_path: Path) -> None:
>         """The tool's only repository write is the explicit history append: no tracker, no git mutation, no substituted output path, no model shortcut.
>     
>         Fault this pins: a side effect through a substituted result path, a
>         tracker or git write, or a model/API client in the measurement path.
>         """
>         root = _write_repo(tmp_path / "repo")
>         outside = tmp_path / "outside"
>         outside.mkdir()
>     
>         def _tree() -> dict[str, bytes]:
>             found: dict[str, bytes] = {}
>             for path in sorted(root.rglob("*")):
>                 if path.is_file():
>                     found[str(path.relative_to(root))] = path.read_bytes()
>             return found
>     
>         before = _tree()
>         head_before = _head_of(root)
>         done = _record(
>             root,
>             tmp_path,
>             _export(root),
>             dict(SENTINELS),
>             env_extra={"OUTCOME_TEST_RESULTS": str(outside / "substituted.jsonl")},
>         )
>         assert done.returncode in (0, 1)
>         assert list(outside.iterdir()) == [], "an env-var substitution took the write"
>     
>         after = _tree()
>         changed = {name for name in set(before) | set(after) if before.get(name) != after.get(name)}
>         assert changed == {HISTORY_REL}, f"unexpected repository writes: {sorted(changed)}"
>         assert not any(element.is_dir() and element.name == "__pycache__" for element in root.rglob("*"))
>         assert _head_of(root) == head_before
>         status = subprocess.run(
>             ["git", "-C", str(root), "status", "--porcelain"],
>             check=True,
>             capture_output=True,
>             text=True,
>             timeout=60,
>         )
> >       assert status.stdout.splitlines() == [f"?? {HISTORY_REL}"]
> E       AssertionError: assert ['?? docs/research/'] == ['?? docs/res...esults.jsonl']
> E         
> E         At index 0 diff: '?? docs/research/' != '?? docs/research/outcome-test-results.jsonl'
> E         Use -v to get more diff
>
> tests/test_outcome_test.py:692: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_outcome_test.py::test_tool_only_writes_explicit_history - A...
> 1 failed, 8 passed in 7.21s
> ```

Stage-2 call, 2026-11-06: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 916 files, 3423 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_outcome_test.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-67/popen-gw0/test_tool_only_writes_explicit0')
>
>     def test_tool_only_writes_explicit_history(tmp_path: Path) -> None:
>         """The tool's only repository write is the explicit history append: no tracker, no git mutation, no substituted output path, no model shortcut.
>     
>         Fault this pins: a side effect through a substituted result path, a
>         tracker or git write, or a model/API client in the measurement path.
>         """
>         root = _write_repo(tmp_path / "repo")
>         outside = tmp_path / "outside"
>         outside.mkdir()
>     
>         def _tree() -> dict[str, bytes]:
>             found: dict[str, bytes] = {}
>             for path in sorted(root.rglob("*")):
>                 if path.is_file():
>                     found[str(path.relative_to(root))] = path.read_bytes()
>             return found
>     
>         before = _tree()
>         head_before = _head_of(root)
>         done = _record(
>             root,
>             tmp_path,
>             _export(root),
>             dict(SENTINELS),
>             env_extra={"OUTCOME_TEST_RESULTS": str(outside / "substituted.jsonl")},
>         )
>         assert done.returncode in (0, 1)
>         assert list(outside.iterdir()) == [], "an env-var substitution took the write"
>     
>         after = _tree()
>         changed = {name for name in set(before) | set(after) if before.get(name) != after.get(name)}
>         assert changed == {HISTORY_REL}, f"unexpected repository writes: {sorted(changed)}"
>         assert not any(element.is_dir() and element.name == "__pycache__" for element in root.rglob("*"))
>         assert _head_of(root) == head_before
>         status = subprocess.run(
>             ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"],
>             check=True,
>             capture_output=True,
>             text=True,
>             timeout=60,
>         )
>         assert status.stdout.splitlines() == [f"?? {HISTORY_REL}"]
>     
>         source = (REPO_ROOT / "scripts" / SCRIPT_NAME).read_text(encoding="utf-8")
>         imported: set[str] = set()
>         for node in ast.walk(ast.parse(source)):
>             if isinstance(node, ast.Import):
>                 imported.update(alias.name.split(".")[0] for alias in node.names)
>             elif isinstance(node, ast.ImportFrom) and node.module:
>                 imported.add(node.module.split(".")[0])
> >       assert imported <= {
>             "argparse",
>             "ast",
>             "collections",
>             "datetime",
>             "fcntl",
>             "hashlib",
>             "json",
>             "math",
>             "os",
>             "pathlib",
>             "re",
>             "subprocess",
>             "sys",
>             "time",
>             "typing",
>             "uuid",
>         }, f"the measurement path carries a foreign client: {sorted(imported)}"
> E       AssertionError: the measurement path carries a foreign client: ['__future__', 'argparse', 'ast', 'collections', 'datetime', 'fcntl', 'hashlib', 'json', 'math', 'os', 'pathlib', 're', 'subprocess', 'sys', 'time', 'typing', 'uuid']
> E       assert {'__future__'... 'fcntl', ...} <= {'argparse', ...hashlib', ...}
> E         
> E         Extra items in the left set:
> E         '__future__'
>
> tests/test_outcome_test.py:701: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_outcome_test.py::test_tool_only_writes_explicit_history - A...
> 1 failed, 8 passed in 7.60s
> ```

Stage-2 call, 2026-11-06: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Flash failed twice and Sonnet attempt 3 failed only on its own import allowlist in tests/test_outcome_test.py (missing __future__); attempt 3 is saved at refs/stage2/attempts/outcome-test/orchestrator-saved-20261106 · leak check clean over 913 files, 3438 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 5
> bringing up nodes...
> bringing up nodes...
>
>
> no tests ran in 0.49s
> ```

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model beam-free · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 929 files, 3558 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 929 files, 3594 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 929 files, 3595 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 929 files, 3595 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 929 files, 3602 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 929 files, 3607 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 929 files, 3609 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model hy3 · leak check clean over 929 files, 3626 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 929 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 929 files, 3664 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 929 files, 3674 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model hy4-preview · leak check clean over 929 files, 3689 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 929 files, 3692 commits, 12 rules.
