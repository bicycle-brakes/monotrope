---
title: "Findings — venv-pycache"
category: findings
status: draft
implementation_status: none
date: 2026-10-24
created: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-q94b
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — venv-pycache

Stage-2 call, 2026-10-24: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 533 files, 1929 commits, 12 rules.

Stage-2 call, 2026-10-24: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 536 files, 1930 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 536 files, 1931 commits, 12 rules.

Stage-2 call, 2026-10-24: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1931 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +7 -5
> - `tests/test_stage2.py` +33 -7
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-4: no fixed line
> - L1-6: no fixed line
> - L1-10: no fixed line
> ```

Stage-2 call, 2026-10-24: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1931 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/INDEX.md` +5 -5
> - `plans/changes/venv-pycache/decisions.md` +1 -1
> - `plans/changes/venv-pycache/findings.md` +2 -2
> - `plans/changes/venv-pycache/plan.md` +8 -7
> - `plans/changes/venv-pycache/research.md` +1 -1
> - `plans/changes/venv-pycache/spec.md` +1 -1
> - `scripts/stage2.py` +13 -9
> - `tests/test_stage2.py` +6 -2
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-1: tests/test_stage2.py::test_venv_cache_cleanup_precedes_runner_tools: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - L1-3: tests/test_stage2.py::test_venv_cache_cleanup_never_follows_symlinks: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - L1-7: tests/test_stage2.py::test_venv_cache_cleanup_precedes_runner_tools: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> ```

Stage-2 call, 2026-10-24: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 536 files, 1931 commits, 12 rules.
