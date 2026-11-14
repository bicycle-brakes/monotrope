---
title: "Findings — swarm-citation-feedback"
category: findings
status: draft
implementation_status: none
date: 2026-11-14
created: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-t2wm
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — swarm-citation-feedback

Stage-2 call, 2026-11-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1065 files, 4202 commits, 12 rules.

Stage-2 call, 2026-11-14: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1068 files, 4204 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/swarm-citation-feedback/plan.md` +8 -8
> - `scripts/stage2_research_refs.py` +12 -1
> - `scripts/stage2_research_report.py` +15 -1
> - `scripts/stage2_research_run.py` +43 -5
> - `tests/test_stage2_research_refs.py` +42 -0
> - `tests/test_stage2_research_report.py` +53 -0
> - `tests/test_stage2_swarm.py` +151 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> .....................F...F....                                           [100%]
> =================================== FAILURES ===================================
> _________________ test_report_prompt_markdown_example_resolves _________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/swarm-citation-feedback/.venv/bin/python3
>
>     def test_report_prompt_markdown_example_resolves():
>         # Criterion 5. Planted fault: the common contract's Markdown example loses the shown heading or
>         # its bare-title citation, the pair cannot resolve against the illustrated frozen source, a line
>         # number replaces the heading, or the invented example is written as a repository fact.
>         text = (Path(__file__).resolve().parents[1] / "prompts" / "research-swarm" / "report.md").read_text()
>         shown = re.search(r"`(#{1,6}[ \t][^`\n]+)`", text)
> >       assert shown, "the contract illustrates one fictional Markdown heading with its opening marks, in backticks"
> E       AssertionError: the contract illustrates one fictional Markdown heading with its opening marks, in backticks
> E       assert None
>
> tests/test_stage2_research_report.py:364: AssertionError
> _____________________ test_online_brief_names_fetch_budget _____________________
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/swarm-citation-feedback/.venv/bin/python3
>
>     def test_online_brief_names_fetch_budget() -> None:
>         # Criterion 6. Planted fault: the public brief omits the three-fetch budget for the topic
>         # attempt, or the report-from-own-retrievals and unread-record instructions.
>         for topic in range(9, 12):
>             prompt = stage2_research_run.online_topic_prompt(REPO_ROOT, topic, "one shared topic sentence")
>             flat = prompt.replace("`", "")
>             assert "public_fetch" in flat, "the brief names the seat's own fetch tool"
> >           assert re.search(r"at most three public_fetch calls per topic attempt", flat), (
>                 "the brief bounds the fetch budget per topic attempt"
>             )
> E           AssertionError: the brief bounds the fetch budget per topic attempt
> E           assert None
> E            +  where None = <function search at 0x104906e80>('at most three public_fetch calls per topic attempt', '# Public research brief\n\nYou are a public-web researcher. You research publicly available engineering\npractice on ...ntral, runtime or dated. These are proposals\nfor maintaining changing facts; none takes effect as a human decision.\n')
> E            +    where <function search at 0x104906e80> = re.search
>
> tests/test_stage2_swarm.py:1698: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_report.py::test_report_prompt_markdown_example_resolves
> FAILED tests/test_stage2_swarm.py::test_online_brief_names_fetch_budget - Ass...
> 2 failed, 28 passed in 29.96s
> ```

Stage-2 call, 2026-11-14: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1068 files, 4213 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/swarm-citation-feedback/plan.md` +8 -8
> - `plans/changes/swarm-citation-feedback/spec.md` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ........................FF....                                           [100%]
> =================================== FAILURES ===================================
> _________________ test_report_prompt_markdown_example_resolves _________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/swarm-citation-feedback/.venv/bin/python3
>
>     def test_report_prompt_markdown_example_resolves():
>         # Criterion 5. Planted fault: the common contract's Markdown example loses the shown heading or
>         # its bare-title citation, the pair cannot resolve against the illustrated frozen source, a line
>         # number replaces the heading, or the invented example is written as a repository fact.
>         text = (Path(__file__).resolve().parents[1] / "prompts" / "research-swarm" / "report.md").read_text()
>         shown = re.search(r"`(#{1,6}[ \t][^`\n]+)`", text)
> >       assert shown, "the contract illustrates one fictional Markdown heading with its opening marks, in backticks"
> E       AssertionError: the contract illustrates one fictional Markdown heading with its opening marks, in backticks
> E       assert None
>
> tests/test_stage2_research_report.py:364: AssertionError
> _____________________ test_online_brief_names_fetch_budget _____________________
> [gw11] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/swarm-citation-feedback/.venv/bin/python3
>
>     def test_online_brief_names_fetch_budget() -> None:
>         # Criterion 6. Planted fault: the public brief omits the three-fetch budget for the topic
>         # attempt, or the report-from-own-retrievals and unread-record instructions.
>         for topic in range(9, 12):
>             prompt = stage2_research_run.online_topic_prompt(REPO_ROOT, topic, "one shared topic sentence")
>             flat = prompt.replace("`", "")
>             assert "public_fetch" in flat, "the brief names the seat's own fetch tool"
> >           assert re.search(r"at most three public_fetch calls per topic attempt", flat), (
>                 "the brief bounds the fetch budget per topic attempt"
>             )
> E           AssertionError: the brief bounds the fetch budget per topic attempt
> E           assert None
> E            +  where None = <function search at 0x1026eae80>('at most three public_fetch calls per topic attempt', '# Public research brief\n\nYou are a public-web researcher. You research publicly available engineering\npractice on ...ntral, runtime or dated. These are proposals\nfor maintaining changing facts; none takes effect as a human decision.\n')
> E            +    where <function search at 0x1026eae80> = re.search
>
> tests/test_stage2_swarm.py:1698: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_report.py::test_report_prompt_markdown_example_resolves
> FAILED tests/test_stage2_swarm.py::test_online_brief_names_fetch_budget - Ass...
> 2 failed, 28 passed in 24.77s
> ```

Stage-2 call, 2026-11-14: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1068 files, 4213 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; make the change the plan names
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ........................FF....                                           [100%]
> =================================== FAILURES ===================================
> _________________ test_report_prompt_markdown_example_resolves _________________
> [gw6] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/swarm-citation-feedback/.venv/bin/python3
>
>     def test_report_prompt_markdown_example_resolves():
>         # Criterion 5. Planted fault: the common contract's Markdown example loses the shown heading or
>         # its bare-title citation, the pair cannot resolve against the illustrated frozen source, a line
>         # number replaces the heading, or the invented example is written as a repository fact.
>         text = (Path(__file__).resolve().parents[1] / "prompts" / "research-swarm" / "report.md").read_text()
>         shown = re.search(r"`(#{1,6}[ \t][^`\n]+)`", text)
> >       assert shown, "the contract illustrates one fictional Markdown heading with its opening marks, in backticks"
> E       AssertionError: the contract illustrates one fictional Markdown heading with its opening marks, in backticks
> E       assert None
>
> tests/test_stage2_research_report.py:364: AssertionError
> _____________________ test_online_brief_names_fetch_budget _____________________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/swarm-citation-feedback/.venv/bin/python3
>
>     def test_online_brief_names_fetch_budget() -> None:
>         # Criterion 6. Planted fault: the public brief omits the three-fetch budget for the topic
>         # attempt, or the report-from-own-retrievals and unread-record instructions.
>         for topic in range(9, 12):
>             prompt = stage2_research_run.online_topic_prompt(REPO_ROOT, topic, "one shared topic sentence")
>             flat = prompt.replace("`", "")
>             assert "public_fetch" in flat, "the brief names the seat's own fetch tool"
> >           assert re.search(r"at most three public_fetch calls per topic attempt", flat), (
>                 "the brief bounds the fetch budget per topic attempt"
>             )
> E           AssertionError: the brief bounds the fetch budget per topic attempt
> E           assert None
> E            +  where None = <function search at 0x10423ae80>('at most three public_fetch calls per topic attempt', '# Public research brief\n\nYou are a public-web researcher. You research publicly available engineering\npractice on ...ntral, runtime or dated. These are proposals\nfor maintaining changing facts; none takes effect as a human decision.\n')
> E            +    where <function search at 0x10423ae80> = re.search
>
> tests/test_stage2_swarm.py:1698: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_report.py::test_report_prompt_markdown_example_resolves
> FAILED tests/test_stage2_swarm.py::test_online_brief_names_fetch_budget - Ass...
> 2 failed, 28 passed in 25.12s
> ```
