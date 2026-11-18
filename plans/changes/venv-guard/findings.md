---
title: "Findings — venv-guard"
category: findings
status: draft
implementation_status: none
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-18
supersedes: null
superseded_by: null
bead: coding-harness-s55e
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — venv-guard

Stage-2 call, 2026-11-17: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1111 files, 4545 commits, 12 rules.

Stage-2 call, 2026-11-17: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1114 files, 4551 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/venv-guard/plan.md` +8 -8
> - `plans/changes/venv-guard/spec.md` +1 -1
> - `scripts/adoption.py` +5 -1
> - `scripts/archive_closed_changes.py` +5 -1
> - `scripts/check_adr_answers.py` +5 -1
> - `scripts/check_frontmatter_current.py` +5 -1
> - `scripts/check_interview_minimums.py` +5 -1
> - `scripts/check_question_context.py` +5 -1
> - `scripts/check_research_currency.py` +5 -1
> - `scripts/check_research_handoff.py` +5 -1
> - `scripts/ci_gates.py` +10 -1
> - `scripts/harness.py` +8 -4
> - `scripts/kit/manifest.yaml` +3 -0
> - `scripts/kit/probe.py` +5 -2
> - `scripts/omnigent_policy.py` +4 -0
> - `scripts/plans_registry.py` +5 -1
> - `scripts/pr_sync.py` +6 -2
> - `scripts/ramp_valves.py` +4 -0
> - `scripts/research_capture.py` +5 -1
> - `scripts/research_census.py` +5 -1
> - `scripts/stage2.py` +5 -1
> - `scripts/stage2_availability.py` +9 -5
> - `scripts/stage2_go.py` +5 -1
> - `scripts/stage2_research_limits.py` +5 -1
> - `scripts/stage2_research_refs.py` +5 -1
> - `scripts/stage2_session.py` +6 -2
> - `scripts/venv_guard.py` +152 -0
> - `tests/test_venv_guard.py` +489 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_venv_guard.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
>
> ==================================== ERRORS ====================================
> __________________ ERROR collecting tests/test_venv_guard.py ___________________
> ImportError while importing test module '/Users/mikypiky/coding-harness/.claude/worktrees/venv-guard/tests/test_venv_guard.py'.
> Hint: make sure your test modules/packages have valid Python names.
> Traceback:
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importlib/__init__.py:90: in import_module
>     return _bootstrap._gcd_import(name[level:], package, level)
> tests/test_venv_guard.py:41: in <module>
>     import probe  # noqa: E402
> E   ModuleNotFoundError: No module named 'probe'
> =========================== short test summary info ============================
> ERROR tests/test_venv_guard.py
> 1 error in 0.42s
> ```

Stage-2 call, 2026-11-17: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1116 files, 4561 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/venv-guard/plan.md` +8 -8
> - `tests/test_venv_guard.py` +1 -0
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/ci_gates.py` is shared execution infrastructure
> - `make verify` exited 2
> templates/design.md:16 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/design.md:97 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Added"]
> templates/design.md:101 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Changed"]
> templates/design.md:105 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Removed"]
> templates/findings.md:18 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/findings.md:45:5 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:9 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:13 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:21 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:25 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> templates/findings.md:46:7 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:15 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:22 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:54 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:99 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:106 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:63 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Severity"]
> templates/findings.md:71 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Dimension"]
> templates/findings.md:77 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Origin"]
> templates/findings.md:84 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Markers that override everythi..."]
> templates/findings.md:111:81 error MD013/line-length Line length [Expected: 80; Actual: 91]
> templates/findings.md:112:81 error MD013/line-length Line length [Expected: 80; Actual: 101]
> templates/findings.md:126:81 error MD013/line-length Line length [Expected: 80; Actual: 125]
> templates/handover.md:20:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 162]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/repo-settings.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 83]
> templates/repo-settings.md:23:81 error MD013/line-length Line length [Expected: 80; Actual: 85]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> templates/spec.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 122]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
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
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-11-18: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1116 files, 4561 commits, 12 rules.
