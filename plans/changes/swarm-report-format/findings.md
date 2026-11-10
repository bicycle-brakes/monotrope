---
title: "Findings — swarm-report-format"
category: findings
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-4q9y
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — swarm-report-format

Stage-2 call, 2026-11-09: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 981 files, 3792 commits, 12 rules.

> Attempt 1 (codex): the runner put back what a draft may not change:
> - `plans/changes/swarm-report-format/decisions.md`

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/swarm-report-format/decisions.md` +18 -0
> - `plans/changes/swarm-report-format/plan.md` +157 -0
> - `plans/changes/swarm-report-format/research.md` +17 -0
> - `plans/changes/swarm-report-format/spec.md` +184 -0
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/swarm-report-format/findings.md: stale — updated 2026-11-09 is older than its last change 2026-11-10 (uncommitted)
> plans/changes/swarm-report-format/plan.md: stale — updated 2026-11-09 is older than its last change 2026-11-10 (uncommitted)
> plans/changes/swarm-report-format/research.md: stale — updated 2026-11-09 is older than its last change 2026-11-10 (uncommitted)
> plans/changes/swarm-report-format/spec.md: stale — updated 2026-11-09 is older than its last change 2026-11-10 (uncommitted)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 35492 earlier lines left out …]
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
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-10: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 984 files, 3792 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 984 files, 3840 commits, 12 rules.

Stage-2 call, 2026-11-10: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 984 files, 3846 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/swarm-report-format/plan.md` +9 -9
> - `plans/changes/swarm-report-format/spec.md` +1 -1
> - `scripts/stage2_research_run.py` +269 -19
> - `tests/test_stage2_swarm.py` +353 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/stage2_research_run.py`, `tests/test_stage2_swarm.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 26 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> refused: run f2b99f7de3da768b70fa54ecab4d3632 status: incomplete - a declaration or leak check refused a call; every queued call was cancelled.
> failed: the research run 2d9df7955ffb53c03954e0d8e81983a4 is incomplete: incomplete - required topic slots did not finish with a valid report: topic 4 opencode-go:mimo-v2.6-pro (invalid-report); no judge starts.
> failed: the research run 37ec382f5017bfe6d8c769bf3dadfb50 is incomplete: incomplete - required topic slots did not finish with a valid report: topic 9 opencode-go:deepseek-v4.1-flash (invalid-report); no judge starts.
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_topic_report_refuses_ambiguous_or_malformed_objects[bare-beside-fence-<lambda>]
> FAILED tests/test_stage2_swarm.py::test_topic_report_preserves_bare_and_exact_fence[fence-plain-<lambda>]
> FAILED tests/test_stage2_swarm.py::test_topic_report_preserves_bare_and_exact_fence[bare-<lambda>]
> FAILED tests/test_stage2_swarm.py::test_topic_report_preserves_bare_and_exact_fence[fence-json-<lambda>]
> FAILED tests/test_stage2_swarm.py::test_topic_correction_keeps_security_and_time_boundaries
> 5 failed, 17 passed in 79.16s (0:01:19)
> ```

Stage-2 call, 2026-11-10: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 984 files, 3858 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/swarm-report-format/plan.md` +8 -8
> - `scripts/stage2_research_run.py` +36 -11
> - `tests/test_stage2_swarm.py` +14 -2
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - `make verify` did not finish: make was stopped by the runner's step limit after 30 minutes
> ```

Stage-2 call, 2026-11-10: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 984 files, 3862 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/swarm-report-format/plan.md` +8 -8
> - `scripts/stage2_research_run.py` +3 -1
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 67 lines of this gate left out …]
> ........................................................................ [ 88%]
> ........................................................................ [ 90%]
> ........................................................................ [ 91%]
> ........................................................................ [ 92%]
> ........................................................................ [ 94%]
> ........................................................................ [ 95%]
> ........................................................................ [ 96%]
> ........................................................................ [ 98%]
> ........................................................................ [ 99%]
> ....................                                                     [100%]
> =================================== FAILURES ===================================
> ___________________ test_startup_budget_reserves_publication ___________________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/swarm-report-format/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1778/popen-gw1/test_startup_budget_reserves_p0')
>
>     def test_startup_budget_reserves_publication(tmp_path: Path) -> None:
>         """Close part of a slow batch, then publish after the close budget runs out."""
>         ns = _build(tmp_path)
>         stub = ns.klon / "tools" / "bd"
>         # Keep the per-close bound above the one-second admission floor. Five
>         # slow closes cannot all start within this budget, but some must finish.
>         stub.write_text(STUB.replace("  close)", "  close)\n    sleep 0.3"))
>         result = _run_script(ns, {**_env(ns), "CLOSE_MERGED_BD_TIMEOUT": "1.5"}, "--write", "--budget-seconds", "2")
>         assert result.returncode == 1
>         assert "startup budget exhausted" in result.stderr
>         assert "dolt push" in _calls(ns), (result.stdout, result.stderr)
>         assert "published: yes" in result.stdout
>         closed = [
>             json.loads(line)["id"] for line in ns.render.read_text().splitlines() if json.loads(line)["status"] == "closed"
>         ]
>         completed = set(closed) & set(DECLARED)
> >       assert 0 < len(completed) < len(DECLARED), (result.stdout, result.stderr)
> E       AssertionError: ('local closures: 0 (5 refused) · published: yes
> E         ', 'refused: coding-harness-nonpr: startup budget exhausted; retry r...udget exhausted; retry reconciliation
> E         refused: coding-harness-side: startup budget exhausted; retry reconciliation
> E         ')
> E       assert 0 < 0
> E        +  where 0 = len(set())
>
> tests/test_close_merged_beads.py:659: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=25131) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/swarm-report-format/tests/test_stage2.py:20332: DeprecationWarning: This process (pid=25129) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_close_merged_beads.py::test_startup_budget_reserves_publication
> 1 failed, 5258 passed, 17 skipped, 5 warnings in 1358.61s (0:22:38)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 35573 earlier lines left out …]
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
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````
