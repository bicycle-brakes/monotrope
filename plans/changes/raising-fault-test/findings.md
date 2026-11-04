---
title: "Findings — raising-fault-test"
category: findings
status: draft
implementation_status: none
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-xrzf
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — raising-fault-test

Stage-2 call, 2026-11-03: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 847 files, 3194 commits, 12 rules.

Stage-2 call, 2026-11-03: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Flash route fails with unrecognized_model since 2026-11-03 (bead coding-harness-ygsw) · leak check clean over 867 files, 3215 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 867 files, 3227 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 867 files, 3228 commits, 12 rules.

Stage-2 call, 2026-11-04: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 867 files, 3229 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/raising-fault-test/plan.md` +1 -1
> - `plans/changes/raising-fault-test/research.md` +3 -1
> - `tests/test_stage2.py` +32 -13
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-3: tests/test_stage2.py::test_implement_prompt_covers_a_fault_that_raises: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - L1-4: tests/test_stage2.py::test_repair_prompts_cover_a_fault_that_raises: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/raising-fault-test/stage2/attempts/raising-fault-test/attempt-1-20261104T073912034365Z-e068e689.md
> ```

Stage-2 call, 2026-11-04: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 867 files, 3233 commits, 12 rules.
