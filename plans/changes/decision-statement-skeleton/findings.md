---
title: "Findings — decision-statement-skeleton"
category: findings
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-nr6h
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — decision-statement-skeleton

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 994 files, 3832 commits, 12 rules.

Stage-2 call, 2026-11-10: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 997 files, 3846 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/decision-statement-skeleton/plan.md` +5 -5
> - `scripts/check_question_context.py` +19 -0
> - `scripts/stage2.py` +33 -2
> - `tests/test_check_question_context.py` +53 -0
> - `tests/test_stage2.py` +239 -5
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_check_question_context.py`, `tests/test_stage2.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 5
> bringing up nodes...
> bringing up nodes...
>
>
> no tests ran in 14.20s
> ```

Stage-2 call, 2026-11-10: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 997 files, 3852 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 5
> bringing up nodes...
> bringing up nodes...
>
>
> no tests ran in 11.46s
> ```

Stage-2 call, 2026-11-10: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 997 files, 3858 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +9 -0
> - `plans/changes/decision-statement-skeleton/plan.md` +5 -5
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 5
> bringing up nodes...
> bringing up nodes...
>
>
> no tests ran in 7.21s
> ```

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: review-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 997 files, 3877 commits, 12 rules.

Stage-2 call, 2026-11-10: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 997 files, 3878 commits, 12 rules.

> Runner verification scope:
> - Attempt 1 (codex): full `make verify` ran (result: green) because the targeted coverage was not safe: the whole tests/test_stage2.py requires full verification until coding-harness-vg9 splits it

Runner restoration, 2026-11-10: repair · attempt 1 · route codex — lifecycle fields: plans/changes/decision-statement-skeleton/plan.md, plans/changes/decision-statement-skeleton/spec.md — unchanged

Stage-2 call, 2026-11-10: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 997 files, 3893 commits, 12 rules.

Stage-2 call, 2026-11-10: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 997 files, 3893 commits, 12 rules.

Stage-2 call, 2026-11-10: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 997 files, 3893 commits, 12 rules.

Stage-2 call, 2026-11-11: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 997 files, 3899 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +8 -3
> - `plans/changes/decision-statement-skeleton/research.md` +2 -6
> - `scripts/stage2.py` +3 -3
> - `tests/test_stage2.py` +5 -2
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/decision-statement-skeleton/plan.md, plans/changes/decision-statement-skeleton/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/decision-statement-skeleton/decisions.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (7414b824)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 36382 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/decision-statement-skeleton/stage2/attempts/decision-statement-skeleton/attempt-1-20261110T230903185300Z-85f06a9a.md
> ````

Stage-2 call, 2026-11-11: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 997 files, 3902 commits, 12 rules.

Runner restoration, 2026-11-11: repair · attempt 2 · route codex-repair — lifecycle fields: plans/changes/decision-statement-skeleton/plan.md, plans/changes/decision-statement-skeleton/spec.md — unchanged

Stage-2 call, 2026-11-11: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 997 files, 3907 commits, 12 rules.

Runner restoration, 2026-11-11: repair · attempt 1 · route codex — lifecycle fields: plans/changes/decision-statement-skeleton/plan.md, plans/changes/decision-statement-skeleton/spec.md — unchanged

Stage-2 call, 2026-11-11: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex repair calls ended with exit 1 on 2026-11-11 (01:45 and 02:39 UTC) · leak check clean over 997 files, 3912 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +7 -3
> - `plans/changes/decision-statement-skeleton/research.md` +1 -12
> - `scripts/stage2.py` +3 -1
> - `tests/test_stage2.py` +3 -2
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/decision-statement-skeleton/plan.md, plans/changes/decision-statement-skeleton/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/decision-statement-skeleton/decisions.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (7414b824)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 36432 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/decision-statement-skeleton/stage2/attempts/decision-statement-skeleton/attempt-1-20261111T060431622252Z-4787af23.md
> ````

Stage-2 call, 2026-11-11: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Codex repair calls ended with exit 1 on 2026-11-11 · leak check clean over 997 files, 3918 commits, 12 rules.

> Runner verification scope:
> - Attempt 1 (stage-1): full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure

Runner restoration, 2026-11-11: repair · attempt 1 · route stage-1 — lifecycle fields: plans/changes/decision-statement-skeleton/plan.md, plans/changes/decision-statement-skeleton/spec.md — unchanged
