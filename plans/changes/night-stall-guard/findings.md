---
title: "Findings — night-stall-guard"
category: findings
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-ibde
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — night-stall-guard

Stage-2 call, 2026-11-09: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 960 files, 3724 commits, 12 rules.

Stage-2 call, 2026-11-09: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 963 files, 3725 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +37 -6
> - `plans/changes/night-stall-guard/plan.md` +7 -7
> - `scripts/merge_guard.py` +29 -8
> - `tests/test_merge_guard.py` +130 -10
> - `tests/test_night_profile.py` +378 -0
> - `tools/claude-code/README.md` +39 -5
> - `tools/claude-code/install.sh` +2 -0
> - `tools/claude-code/night-settings.json` +5 -0
> - `tools/claude-code/night.py` +181 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_merge_guard.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ......F.......................                                           [100%]
> =================================== FAILURES ===================================
> ________________ test_the_omnigent_render_keeps_the_merge_rules ________________
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/night-stall-guard/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1319/popen-gw3/test_the_omnigent_render_keeps0')
>
>     def test_the_omnigent_render_keeps_the_merge_rules(tmp_path: Path) -> None:
>         target = tmp_path / ".claude" / "settings.json"
>         target.parent.mkdir(parents=True)
>         target.write_text(SETTINGS.read_text(encoding="utf-8"), encoding="utf-8")
>     
>         op.write(tmp_path)
>         rendered = json.loads(target.read_text(encoding="utf-8"))
>         ask = rendered["permissions"]["ask"]
> >       assert [rule for rule in ask if rule in mg.MERGE_ASK_RULES] == list(mg.MERGE_ASK_RULES)
> E       AssertionError: assert ['Bash(gh pr ...pull_request'] == ['Bash(gh pr ...quest*)', ...]
> E         
> E         At index 3 diff: 'Bash(gh alias set *)' != 'Bash(gh api *PUT*pulls/*/merge*)'
> E         Right contains 5 more items, first extra item: 'Bash(gh api *query=*enablePullRequestAutoMerge*)'
> E         Use -v to get more diff
>
> tests/test_merge_guard.py:264: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_merge_guard.py::test_the_omnigent_render_keeps_the_merge_rules
> 1 failed, 29 passed in 1.93s
> ```

Stage-2 call, 2026-11-09: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 966 files, 3728 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +1 -1
> - `plans/changes/night-stall-guard/plan.md` +7 -7
> - `tests/test_merge_guard.py` +17 -5
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 58 lines of this gate left out …]
> ........................................................................ [ 78%]
> ........................................................................ [ 80%]
> ........................................................................ [ 81%]
> ........................................................................ [ 83%]
> ........................................................................ [ 84%]
> ........................................................................ [ 85%]
> ........................................................................ [ 87%]
> ........................................................................ [ 88%]
> ........................................................................ [ 90%]
> ........................................................................ [ 91%]
> ........................................................................ [ 92%]
> ........................................................................ [ 94%]
> ........................................................................ [ 95%]
> ........................................................................ [ 97%]
> ........................................................................ [ 98%]
> ........................................................................ [ 99%]
> .....                                                                    [100%]
> =================================== FAILURES ===================================
> _____________________ test_settings_ask_before_every_merge _____________________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/night-stall-guard/.venv/bin/python3
>
>     def test_settings_ask_before_every_merge() -> None:
>         ask = _settings()["permissions"]["ask"]
>         missing = [rule for rule in mg.MERGE_ASK_RULES if rule not in ask]
> >       assert not missing, f".claude/settings.json does not ask before: {missing}"
> E       AssertionError: .claude/settings.json does not ask before: ['Bash(gh api *PUT*pulls/*/merge*)', 'Bash(gh api *pulls/*/merge*PUT*)', 'Bash(gh api *query=*mergePullRequest*)', 'Bash(gh api *query=*enablePullRequestAutoMerge*)', 'Bash(gh api *query=*enqueuePullRequest*)']
> E       assert not ['Bash(gh api *PUT*pulls/*/merge*)', 'Bash(gh api *pulls/*/merge*PUT*)', 'Bash(gh api *query=*mergePullRequest*)', 'Bash(gh api *query=*enablePullRequestAutoMerge*)', 'Bash(gh api *query=*enqueuePullRequest*)']
>
> tests/test_merge_guard.py:56: AssertionError
> __________________ test_no_deny_or_allow_rule_covers_a_merge ___________________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/night-stall-guard/.venv/bin/python3
>
>     def test_no_deny_or_allow_rule_covers_a_merge() -> None:
> >       assert mg.problems(_settings()) == []
> E       AssertionError: assert ['.claude/set...ld query=...'] == []
> E         
> E         Left contains 5 more items, first extra item: '.claude/settings.json lacks the ask rule Bash(gh api *PUT*pulls/*/merge*) - the REST merge endpoint with the method spelled before the path (-X PUT, --method PUT); a GET, also on this endpoint, names no PUT and passes'
> E         Use -v to get more diff
>
> tests/test_merge_guard.py:60: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=99884) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/night-stall-guard/tests/test_stage2.py:20332: DeprecationWarning: This process (pid=99887) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_merge_guard.py::test_settings_ask_before_every_merge - Asse...
> FAILED tests/test_merge_guard.py::test_no_deny_or_allow_rule_covers_a_merge
> 2 failed, 5098 passed, 17 skipped, 5 warnings in 1171.12s (0:19:31)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 34297 earlier lines left out …]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:133:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:133:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:133:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:133:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:133:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:133:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-11-09: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 966 files, 3730 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/night-stall-guard/plan.md` +7 -7
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ......F.F.......................                                         [100%]
> =================================== FAILURES ===================================
> _____________________ test_settings_ask_before_every_merge _____________________
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/night-stall-guard/.venv/bin/python3
>
>     def test_settings_ask_before_every_merge() -> None:
>         ask = _settings()["permissions"]["ask"]
>         missing = [rule for rule in mg.MERGE_ASK_RULES if rule not in ask]
> >       assert not missing, f".claude/settings.json does not ask before: {missing}"
> E       AssertionError: .claude/settings.json does not ask before: ['Bash(gh api *PUT*pulls/*/merge*)', 'Bash(gh api *pulls/*/merge*PUT*)', 'Bash(gh api *query=*mergePullRequest*)', 'Bash(gh api *query=*enablePullRequestAutoMerge*)', 'Bash(gh api *query=*enqueuePullRequest*)']
> E       assert not ['Bash(gh api *PUT*pulls/*/merge*)', 'Bash(gh api *pulls/*/merge*PUT*)', 'Bash(gh api *query=*mergePullRequest*)', 'Bash(gh api *query=*enablePullRequestAutoMerge*)', 'Bash(gh api *query=*enqueuePullRequest*)']
>
> tests/test_merge_guard.py:56: AssertionError
> __________________ test_no_deny_or_allow_rule_covers_a_merge ___________________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/night-stall-guard/.venv/bin/python3
>
>     def test_no_deny_or_allow_rule_covers_a_merge() -> None:
> >       assert mg.problems(_settings()) == []
> E       AssertionError: assert ['.claude/set...ld query=...'] == []
> E         
> E         Left contains 5 more items, first extra item: '.claude/settings.json lacks the ask rule Bash(gh api *PUT*pulls/*/merge*) - the REST merge endpoint with the method spelled before the path (-X PUT, --method PUT); a GET, also on this endpoint, names no PUT and passes'
> E         Use -v to get more diff
>
> tests/test_merge_guard.py:60: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_merge_guard.py::test_settings_ask_before_every_merge - Asse...
> FAILED tests/test_merge_guard.py::test_no_deny_or_allow_rule_covers_a_merge
> 2 failed, 30 passed in 1.71s
> ```

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 966 files, 3734 commits, 12 rules.

Stage-2 call, 2026-11-09: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 966 files, 3741 commits, 12 rules.

Stage-2 call, 2026-11-09: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 966 files, 3744 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_merge_guard.py` +38 -20
> - `tests/test_night_profile.py` +45 -0
> - `tools/claude-code/README.md` +3 -2
> - `tools/claude-code/night.py` +5 -0
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/night-stall-guard/plan.md, plans/changes/night-stall-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `tools/claude-code/README.md` is an input kind the targeted selector does not cover
> - `make verify` did not finish: make was stopped by the runner's step limit after 30 minutes
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/night-stall-guard/stage2/attempts/night-stall-guard/attempt-1-20261109T133011619229Z-322d197f.md
> ```

Stage-2 call, 2026-11-09: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 975 files, 3750 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/merge_guard.py` +3 -0
> - `tests/test_merge_guard.py` +14 -0
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/night-stall-guard/plan.md, plans/changes/night-stall-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `.codex/agents/code-generation-orchestrator.toml` is an input kind the targeted selector does not cover
> - `make verify` did not finish: make was stopped by the runner's step limit after 30 minutes
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/night-stall-guard/stage2/attempts/night-stall-guard/attempt-2-20261109T133011619229Z-322d197f.md
> ```

Stage-2 call, 2026-11-09: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 975 files, 3752 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/night-stall-guard/plan.md, plans/changes/night-stall-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: green) because the targeted coverage was not safe: `.codex/agents/code-generation-orchestrator.toml` is an input kind the targeted selector does not cover
> - L1-7: tests/test_merge_guard.py::test_held_profile_regressions_are_detected: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/night-stall-guard/stage2/attempts/night-stall-guard/attempt-3-20261109T133011619229Z-322d197f.md
> ```
