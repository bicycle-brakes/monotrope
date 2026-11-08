---
title: "Findings — go-wire-apis"
category: findings
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-36za
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — go-wire-apis

Stage-2 call, 2026-11-06: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 910 files, 3407 commits, 12 rules.

Stage-2 call, 2026-11-06: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 913 files, 3418 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/go-wire-apis/plan.md` +4 -4
> - `tests/test_model_endpoints.py` +112 -7
> - `tests/test_pi_contract.py` +321 -25
> - `tests/test_stage2_go_access.py` +82 -0
> - `tests/test_stage2_research_availability.py` +63 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_pi_contract.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> tests/test_pi_contract.py:453:42: ARG002 Unused method argument: `body`
>     |
> 451 |         self._events(handler, frames, named=False)
> 452 |
> 453 |     def _google(self, handler: _Handler, body: dict) -> None:
>     |                                          ^^^^ ARG002
> 454 |         """Answer the Google generateContent route: streamed text chunks ending in a `STOP` finish reason."""
> 455 |         answer = self._next_answer()
>     |
>
> Found 1 error.
> ```

Stage-2 call, 2026-11-06: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 913 files, 3425 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model gpt-6-luna · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model claude-haiku-5-5 · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model gpt-5.6-luna · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 915 files, 3436 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 922 files, 3510 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 922 files, 3510 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 922 files, 3511 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 922 files, 3511 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 922 files, 3511 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 922 files, 3511 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 922 files, 3511 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 922 files, 3511 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 922 files, 3511 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 922 files, 3512 commits, 12 rules.

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 922 files, 3514 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_model_endpoints.py` +23 -13
> - `tests/test_pi_contract.py` +0 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [question-context] $ lauf_cmd
>   - plans/changes/go-wire-apis/decisions.md: Q-2 — no `— YYYY-MM-DD` date ends the decision statement; the recording day cannot be read
> question-context NOT MEASURED: 1 unreadable evidence — exit 3, nothing measured.
> ── [question-context] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 32233 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/go-wire-apis/stage2/attempts/go-wire-apis/attempt-1-20261107T103812616334Z-5f64e324.md
> ````

Stage-2 call, 2026-11-07: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 922 files, 3514 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [question-context] $ lauf_cmd
>   - plans/changes/go-wire-apis/decisions.md: Q-2 — no `— YYYY-MM-DD` date ends the decision statement; the recording day cannot be read
> question-context NOT MEASURED: 1 unreadable evidence — exit 3, nothing measured.
> ── [question-context] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 32277 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/go-wire-apis/stage2/attempts/go-wire-apis/attempt-2-20261107T103812616334Z-5f64e324.md
> ````

Stage-2 call, 2026-11-07: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 922 files, 3516 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [question-context] $ lauf_cmd
>   - plans/changes/go-wire-apis/decisions.md: Q-2 — no `— YYYY-MM-DD` date ends the decision statement; the recording day cannot be read
> question-context NOT MEASURED: 1 unreadable evidence — exit 3, nothing measured.
> ── [question-context] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 32321 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/go-wire-apis/stage2/attempts/go-wire-apis/attempt-3-20261107T103812616334Z-5f64e324.md
> ````

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 922 files, 3525 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 922 files, 3534 commits, 12 rules.

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 922 files, 3539 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 922 files, 3553 commits, 12 rules.

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 922 files, 3556 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/research_capture.py` +1 -0
> - `scripts/stage2_swarm.py` +1 -3
> - `tests/test_pi_contract.py` +29 -5
> - `tests/test_stage2_go_access.py` +9 -2
> - `tests/test_stage2_research_catalog.py` +9 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L3-1: tests/test_pi_contract.py::test_real_go_native_wire_api_exchange: the setup phase of `tests/test_pi_contract.py::test_real_go_native_wire_api_exchange[anthropic-messages]` ended failed; red first needs passing setup and teardown
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/go-wire-apis/stage2/attempts/go-wire-apis/attempt-1-20261107T152519725158Z-2af224d9.md
> ```

Stage-2 call, 2026-11-07: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 922 files, 3567 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L3-1: no fixed line
> - L3-3: no fixed line
> - L3-4: no fixed line
> - L3-5: no fixed line
> - L3-6: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/go-wire-apis/stage2/attempts/go-wire-apis/attempt-2-20261107T152519725158Z-2af224d9.md
> ```

Stage-2 call, 2026-11-07: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 922 files, 3569 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L3-1: tests/test_pi_contract.py::test_real_go_native_wire_api_exchange: the setup phase of `tests/test_pi_contract.py::test_real_go_native_wire_api_exchange[anthropic-messages]` ended failed; red first needs passing setup and teardown
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/go-wire-apis/stage2/attempts/go-wire-apis/attempt-3-20261107T152519725158Z-2af224d9.md
> ```

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 922 files, 3608 commits, 12 rules.

Stage-2 call, 2026-11-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 922 files, 3619 commits, 12 rules.

## Phase 6 — Codex, 2026-11-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MAJOR | SPEC | Phase 6 | scripts/stage2_swarm.py:92; scripts/research_capture.py:827 | The diff changes the production research selector’s required arguments and updates its capture caller, although the specification explicitly protects the swarm implementation and the plan prohibits production-script edits. The final file list therefore violates the promised scope. [Spec: Protected areas; Definition of Done] | Codex | open | — |

Phase 6 verdict: codex 01a1b939-f346-7ac1-9788-2b832a4f1c97, 2026-11-08
Reviewer session: codex 01a1b939-f346-7ac1-9788-2b832a4f1c97 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | BLOCKER | SPEC | change go-wire-apis (model-endpoints.yaml, docs/research/2026-11-06-go-wire-apis.md) | `research_swarm.availability_preflight.measured_wire_apis` and `adresse.apis` in model-endpoints.yaml; the note's `## Open` section | The spec's criteria 3 and 4 and its Definition of Done require all three new APIs measured before completion ("Missing live evidence blocks completion even when offline tests pass"). The change declares only anthropic-messages and openai-responses as measured and records no Google base, while the measurement note leaves "whether it ships with two of three APIs" to the maintainer and decisions.md holds no such answer. Merging settles an open decision in configuration. | deepseek-v4.1-flash | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-2 | MAJOR | MAINT | change go-wire-apis (model-endpoints.yaml) | The `bemerkung` of the `opencode-go` entry ("All four are skipped: wire API not measured") and the comment above `adresse` ("Only the measured wire API is mapped") | The entry's own prose now contradicts the data below it: the same file removes the wire skips for `qwen3.8-flash` and `minimax-m3` and maps three wire APIs, yet the sentences still tell a reader that all four named models are skipped and that one API is mapped. Plan step 8 explicitly required correcting these present-tense sentences while preserving dated history; that was not done. | deepseek-v4.1-flash | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-3 | MAJOR | SPEC | change go-wire-apis (tests/test_model_endpoints.py) | `_measured_apis_problems`, used by `test_the_repository_declaration_carries_six_seats_and_the_rule` | The test named for criterion 4 only requires the measured list to equal the mapped set and to stay inside the supported four. It therefore stays green for the pre-change single-API declaration and for today's three-of-four state, and the criterion's own refutation — "a missing new mapping/list member" — is not refuted: dropping `anthropic-messages` from both the list and the address record passes the check. | deepseek-v4.1-flash | fixed — not a test — declaration check requires exactly completions, Messages and Responses and rejects every proper subset | no — not a test | agree |
| L1-4 | MINOR | MAINT | change go-wire-apis (docs/research/2026-11-06-go-wire-apis.md) | Frontmatter of the new measurement note | The header omits `owner`, which `scripts/check_docs.py` requires of every document frontmatter, and which every other note under `docs/research/` carries. The docs gate reports the new note; it is report-level only, so `make verify` stays green while the finding stands. | deepseek-v4.1-flash | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-5 | MINOR | MAINT | change go-wire-apis (plans/changes/go-wire-apis/spec.md, plan.md, plans/INDEX.md) | Spec header `implementation_status`, plan header, and the five new INDEX rows | Plan step 9 asks for the spec's implementation status to follow the work as it lands, but spec.md and plan.md still declare `implementation_status: none` with `status: draft`, and plans/INDEX.md lists the artefacts as `none`, although two APIs are declared measured, three address mappings and five wire-skip removals have landed. | deepseek-v4.1-flash | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-6 | MINOR | MAINT | change go-wire-apis (tests/test_pi_contract.py) | `test_real_go_native_wire_api_failures_are_mandatory` | The assertion `NATIVE_ANSWER not in done.stdout` can never fail: none of the three scripted failure entries ("error", "malformed", "empty") carries that text, so it does not prove that a decoded answer would be caught. The real guard is the weaker returncode-or-empty check next to it. | deepseek-v4.1-flash | fixed — not a test — removed the ineffective decoded-answer assertion; retained the failure-or-empty-output check | no — not a test | agree |
| L1-7 | MINOR | MAINT | change go-wire-apis (plans/changes/go-wire-apis/research.md) | Frontmatter of research.md | The header still says `provenance: human-written` without `produced_by`, although the file's own note requires `ai-drafted-reviewed` plus `produced_by` and `review` as soon as a language model fills the body, and the appended exploration section is model-drafted. The change ships with a provenance class that misstates its origin. | deepseek-v4.1-flash | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-8 | MAJOR | SPEC | plan step 8 (orchestrator bootstrap) | model-endpoints.yaml, opencode-go `adresse` comment and `bemerkung` | The plan requires correcting the entry's present-tense bemerkung and comments when the wire skips are removed, but neither was touched. The comment directly above the record still says "Only the measured wire API is mapped" while the diff adds two more mappings, and the bemerkung still asserts "All four are skipped: wire API not measured … a probe must measure their real address before use" although two of those four models (qwen3.8-flash, minimax-m3) now carry no skip at all, the other two are skipped for 400/403 reasons, and five further wire skips were removed in this change. The held entry now documents the opposite of its own data. | mimo-v2.6-flash | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-9 | MAJOR | SPEC | spec criteria 3-4, Definition of Done, plan step 9 | plans/changes/go-wire-apis/spec.md vs model-endpoints.yaml `measured_wire_apis` and docs/research/2026-11-06-go-wire-apis.md | The change's completion gate demands three live measurements and four address mappings with a four-name measured list; the shipped state has two measurements (Google has no admitted representative, no mapping), three mappings and a three-name list, and the research note itself says the criterion is not met. The declaration, tests and ledger are nonetheless staged as the completed end state — the plan's ledger even promises phase 6 will find "the three successfully measured APIs", which do not exist — so the change cannot satisfy its own spec as written and the note leaves the decision unresolved for the maintainer. | mimo-v2.6-flash | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-10 | MINOR | MAINT | plan step 9 | plans/changes/go-wire-apis/{spec,plan,decisions,findings,research}.md frontmatter and plans/INDEX.md | All five change artefacts still carry `implementation_status: none` (and plans/INDEX.md repeats it for every row) although the implementation has landed: the offline tests changed, the held declaration was edited, the time ledger records an accepted attempt, and the measurement note in the same change says `implementation_status: partial`. A maintainer reading the folder cannot tell which state is true, and the plan requires the implementation status to be updated as work lands. | mimo-v2.6-flash | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-11 | MAJOR | SPEC | go-wire-apis | model-endpoints.yaml (research_swarm.availability_preflight.measured_wire_apis and adresse.apis) and docs/research/2026-11-06-go-wire-apis.md | The declaration and the measurement note ship only the completions API plus two new native APIs; the third new API has no live measurement, no address mapping and no measured-list entry, so the spec criteria 3 and 4 and the Definition of Done (all three successful live measurements) are not met, and the note itself says the change is not complete and leaves shipping to the maintainer. | longcat-2.0 | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-12 | MAJOR | MAINT | go-wire-apis | model-endpoints.yaml (bemerkung of the opencode-go entry) | Plan step 8 required correcting the entry's present-tense bemerkung after the skip removals and new mappings; the diff leaves it unchanged, so it still describes the old single-API, all-skipped state that the same file now contradicts. | longcat-2.0 | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-13 | MAJOR | MAINT | go-wire-apis | plans/changes/go-wire-apis/research.md (frontmatter) | The research artifact declares provenance: human-written and carries no produced_by or review, while its body is an AI-drafted exploration appended by the runner; the file's own note and provenance.yaml require ai-drafted-reviewed with produced_by and review for such content. | longcat-2.0 | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-14 | MINOR | MAINT | go-wire-apis | plans/changes/go-wire-apis/research.md (frontmatter) | The research file's own closing note says the runner sets the neighbours header when appending the exploration; the frontmatter has no neighbours field, so the proposed neighbour list in the body is not carried into the header. | longcat-2.0 | rejected — the neighbours header is set by the research swarm; this change explored through Flash, which writes none |  | disagree — Bounded Flash exploration does not require the structured neighbour header; the spec records why its neighbour list is empty. |
| L1-15 | MINOR | MAINT | go-wire-apis | plans/changes/go-wire-apis/spec.md, plan.md, decisions.md, findings.md, research.md (frontmatter) and plans/INDEX.md | The implementation was accepted and the research note declares implementation_status: partial, yet the plan artifacts still declare none and the regenerated INDEX repeats none; plan step 9 required updating the status as work lands. | longcat-2.0 | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-16 | MINOR | SPEC | go-wire-apis | tests/test_model_endpoints.py (_measured_apis_problems) | The new declaration check accepts any nonempty subset of the supported API set, so a declaration measuring only the completions API, or any two APIs, passes, while spec criterion 4 requires the measured list to contain exactly the full measured set and criterion 3 requires a successful measurement per new API; the test therefore blesses the incomplete end state it was meant to guard. | longcat-2.0 | fixed — not a test — covered by the exact measured-set check repaired for L1-3 | no — not a test | agree |
| L1-17 | MINOR | SPEC | go-wire-apis | docs/research/2026-11-06-go-wire-apis.md (Result per API) | Plan step 8 and spec criterion 3 require the measurement note to identify the native request route proven offline and the expected route per API; the note lists documented page endpoints but never records the route the offline contracts proved or the Pi-shaped base route suffix, so the note does not stand alone as the measurement record. | longcat-2.0 | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-18 | MINOR | MAINT | go-wire-apis | plans/changes/go-wire-apis/plan.md (criterion ledger, criterion 4) | The ledger still tells phase 6 to verify the final address and measured lists contain the completions API plus the three new APIs, i.e. the full set, while the final declaration carries one fewer; the ledger was not updated when the third new API's measurement was blocked. | longcat-2.0 | fixed — orchestrator hand edit c3d37527 | no | agree |
| L1-19 | MINOR | MAINT | go-wire-apis | tests/test_model_endpoints.py (_address_fixture) | The fixture's docstring says it is the record as the orchestrator's bootstrap will declare it, but it maps the blocked third new API that the bootstrap does not declare, so the fixture no longer matches the declaration it claims to mirror and its new faults test a row the real record lacks. | longcat-2.0 | fixed — not a test — fixture docstring identifies Google as shape coverage only, not the measured declaration | no — not a test | agree |
| L2-1 | MAJOR | SPEC | glm-5.3-flash | docs/research/2026-11-06-go-wire-apis.md § Open | The measurement note still declares the change "not complete as planned" and leaves open "whether it ships with two of three APIs", but decisions.md Q-2 (2026-11-07) already answered that the two measured APIs ship and Google defers to bead coding-harness-twdu; spec.md criteria 3–4 and the plan ledger were narrowed to two API rows, so the note (frontmatter `updated: 2026-11-07`) contradicts the recorded decision and a maintainer reading the live-evidence note alone would wrongly conclude the change is blocked. | glm-5.3-flash | fixed — orchestrator hand edit 1247dc0b | no | agree |
| L2-2 | MAJOR | SPEC | glm-5.3-flash | model-endpoints.yaml `bemerkung` (lines ~580–587) | The entry's present-tense prose says only "`qwen3.8-flash` and `minimax-m3` run" and frames the skipped set as "all four" 2026-10-17 ids; the same change removes the wire skips and admits qwen3.7-plus, qwen3.8-max and grok-4.7, and its remaining skips cover gpt-5.6-luna and gemini-4-argon — none of these five appear in the comment, so the held declaration no longer states which skipped models the measurement qualified and now qualifies none of them in its explanatory text (plan step 8 required correcting the present-tense bemerkung). | glm-5.3-flash | fixed — orchestrator hand edit 1247dc0b | no | disagree — The paragraph describes the four historically named models without claiming an exhaustive list; the measurement note already enumerates all five newly qualifying models. |
| L2-3 | MINOR | SPEC | glm-5.3-flash | tests/test_model_endpoints.py SUPPORTED_WIRE_APIS comment | The comment calls the set "the three native APIs the change measures", but gpt/decisions.md Q-2 defers the Google measurement and the record deliberately does not map or measure google-generative-ai; the set is a supported-shape set, and the comment misstates it in the same file that asserts the measured list contains exactly three names. | glm-5.3-flash | fixed — not a test — Corrected the supported-shape set comment to state that Google is supported but not measured (decisions.md Q-2). | no — not a test | agree |
| L3-1 | MAJOR | SPEC | qwen3.8-flash | `tests/test_pi_contract.py::test_real_go_native_wire_api_exchange`, `StandIn._messages/_responses/_google` | The three new native routes are proven with a plain text answer only, so the path these models are actually admitted for is unproven: every synthetic row sets `"reasoning": False` (so no contract ever sends a thinking field), and the three new handlers ignore a scripted `tool_calls` entry — they answer `content`, or `"No finding."`, whatever the script asked for. The real paid call this change enables runs `--tools read,grep,find,ls` plus `--thinking max` (`scripts/stage2.py:2792-2794`), and the one live Messages failure the change records is a refused thinking field, so neither the offline contract nor the tool-free probe (`--no-tools`) exercises a native tool call or a thinking-bearing request. | qwen3.8-flash | rejected — moved to its own follow-up bead (maintainer 2026-11-08): the reasoning-enabled native exchange test failed in its setup three times; this change ships Messages and Responses proven with plain answers |  | disagree — The acceptance criteria require native streamed text exchanges, not tool exchanges; live probes already use thinking max, and the model that rejected it remains excluded. |
| L3-2 | MAJOR | SPEC | qwen3.8-flash | `plans/changes/go-wire-apis/plan.md:22`, `:80-83`, `:109-110` | The plan still states the scope the change did not ship. Its card reads "Done when: Native offline contracts, three recorded live API measurements…", step 5 tells the orchestrator to declare the Google base `[credential]opencode.ai/inference/go/google/v1beta`, and step 8 says "do not claim this three-API change complete" — while the same change's `decisions.md` Q-2 ships two APIs and the new `_measured_apis_problems` in `tests/test_model_endpoints.py` reports `mapped without being measured`. A maintainer who follows step 5 for the Google follow-up turns `make verify` red; the criterion ledger was narrowed to Q-2, the card, the file sequence and step 8 were not. | qwen3.8-flash | fixed — orchestrator hand edit 805e9984 | no | agree |
| L3-3 | MAJOR | SPEC | qwen3.8-flash | `tests/test_stage2_go_access.py::test_native_api_probes_keep_their_assessed_destinations`, `scripts/stage2_go.py::assess` | The test's docstring promises more than it proves. It says a planted "API/base configuration mismatch … may not send", but the plant rewrites the config artifact *after* the caller's assessment, which the pre-existing destination-vs-artifact comparison in `dispatch_go` already catches; nothing checks a catalog row that simply pairs a wire API with another API's recorded base. `assess` compares paths only, and this change gives the Responses mapping the same base as completions, so a wrong `api` field is admitted — at best with a "same-host move" notice, at worst with no notice at all — and a call Go translated instead of served natively can still be recorded, and measured, as a native call, which is the outcome `decisions.md` Q-1 rejected. | qwen3.8-flash | fixed — not a test — Docstring now limits the claim to a configuration mismatch after assessment and foreign-host refusal. | no — not a test | disagree — The test explicitly plants an artifact change after assessment. Rejecting same-host API/base combinations would introduce routing restrictions beyond the specified address policy; Responses and completions legitimately share a base. |
| L3-4 | MINOR | MAINT | qwen3.8-flash | `tests/test_pi_contract.py::test_real_catalog_move_keeps_messages_catalog_base` (docstring, ~line 810) | A stale statement now contradicts the change that touched this very file: the docstring says the Messages catalog rows are "Catalog evidence for the separate Messages follow-up - no wire exchange is measured or admitted here (spec criterion 3)", although this change measured Messages live and removed the wire skips of the models that test lists. A maintainer reading the test is told the opposite of the declaration. | qwen3.8-flash | fixed — not a test — Messages catalog docstring now states that Messages is measured and admitted. | no — not a test | agree |
| L3-5 | MINOR | MAINT | qwen3.8-flash | `tests/test_pi_contract.py:1500-1503` | The new shipped-catalog flattening drops the `isinstance(model, dict)` guard that both sibling readers in the same file apply (lines 790 and 814-816) — they carry it because Pi's data can hold non-dict entries. Here one raises `AttributeError`/`TypeError` instead of naming the disagreement, and rows without an `id` both key as `None`, so the "the shipped catalog files it under two wire APIs" assertion can fire on two unrelated entries. | qwen3.8-flash | fixed — not a test — Catalog flattening explicitly identifies non-dict entries and invalid ids before checking duplicates. | no — not a test | disagree — Malformed catalog rows already fail visibly. A missing id raises KeyError on the first row, so the claimed collision between unrelated missing-id entries cannot occur. |
| L3-6 | MINOR | MAINT | qwen3.8-flash | `scripts/stage2_swarm.py:93` | `select_research_catalog` keeps the code default `measured_wire_apis=("openai-completions",)`. This change moved that rule to data (the declaration now lists three), so the default silently disagrees with it: any caller that forgets the keyword applies the old single-API gate and reports the other APIs as `wire-api-not-measured`. | qwen3.8-flash | fixed — tests/test_stage2_go_access.py::test_research_selector_requires_declared_measured_wire_apis | yes — tests/test_stage2_go_access.py::test_research_selector_requires_declared_measured_wire_apis | disagree — Production preparation already passes the declared measured list; the omitted arguments belong to completions-only synthetic callers. No incorrect production selection is demonstrated. |
| L3-7 | MINOR | MAINT | qwen3.8-flash | `docs/research/2026-11-06-go-wire-apis.md`, "Routes." block | The live-route evidence that spec criterion 3 depends on is an unlabelled orphan: "Routes." is prose, not a heading, is preceded by a double blank line, and sits directly under the bulleted list of models that stay blocked — with no mention of Google, the one API that list ends with. A reader cannot tell which API's route was proven offline, and markdownlint's MD012 names the stray blank line. | qwen3.8-flash | fixed — orchestrator hand edit 805e9984 | no | disagree — The paragraph explicitly identifies both APIs, bases and route suffixes. Its heading and blank-line formatting do not obscure the claimed measurement evidence. |
| L3-8 | MINOR | MAINT | qwen3.8-flash | `plans/changes/go-wire-apis/plan.md` card `:23` vs "## Time used" | The declared stop was passed without a record: the card states "Appetite: 3 hours of phase 4, repairs included — a stop, not an estimate" and `spec.md` repeats "exceeding it returns the work", while the section totals 14,684 s (4 h 05 m) of measured attempts. The three repair attempts that failed their post-run checks on 2026-11-07 (recorded in `findings.md`) carry no time line at all, so the figure is both over the stop and incomplete. | qwen3.8-flash | fixed — orchestrator hand edit 805e9984 | no | agree |
| L3-9 | MINOR | MAINT | qwen3.8-flash | `tests/test_model_endpoints.py::_address_fixture` | The fixture documented as "A minimal valid record" now maps `google-generative-ai`, a mapping this change's own new check refuses for the repository declaration (`mapped without being measured`). Its docstring explains the difference in prose, so the shape validator's model of a correct record and the measured-API rule disagree — the next person to copy the fixture into a declaration gets a red gate. | qwen3.8-flash | rejected — accepted limit named in the PR: the shape fixture maps google-generative-ai on purpose to test a valid shape, and its docstring says so |  | disagree — Address-shape validation and measured-API admission enforce different contracts; the fixture explicitly tests supported shapes without claiming Google is measured. |

Rounds run: 3

Record digest: sha256:55ab96d99519e55d865b65602784b90bfccc7473e52d3cf81fb270e84d1c2e40

Record identity: sha256:d4cad5c0a7c22e2b0b0183c12f686d79ff4bb8eb6b2719702e77ca420d669724

Loop state: {"availability": {"checked_at": "2026-11-07T09:53:01+00:00", "failed": {"crouton-alpha-free": "pi call failed: exit 1: opencode-go API error (403): {\"type\":\"RegionError\",\"message\":\"This model is not available in your country\"}", "glm-5.2": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated. Use mimo-v2.6-pro instead.\"}"}, "reachable": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "mimo-v2.6-pro", "minimax-m3", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "grok-4.7", "qwen3.8-max", "kimi-k3"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "hy4": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 \"thinking.type.enabled is not supported for this model; use thinking.type.adaptive\" (a Pi adapter setting, bead coding-harness-36za evidence))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free)", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": []}, "consumed": ["flash", "rung:glm-5.3-flash", "rung:qwen3.8-flash"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "crouton-alpha-free", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "pulse-alpha-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "crouton-alpha-free", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-07T09:45:49+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1794044747724, "etag": "W/\"2536099d28f32505b4840b309f9262c7\"", "lastModified": 1793973242000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "crouton-alpha-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 270000, "name": "Crouton Alpha Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": [], "overlay": ["beam-free", "claude-haiku-5-5", "crouton-alpha-free", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}, {"date": "2026-11-06", "id": "iceman-contributor-free", "reason": "New in the live Go catalog on 2026-11-06 and picked as the whole free swarm by prepare-loop; \"contributor\" ids on Go have meant that request data may be used for training, and the maintainer's decision of 2026-10-17 (question Q-12) keeps such models off. The Go page's privacy table, read 2026-11-06, confirms it: 'Iceman Contributor Free | Yes | Not ZDR'. A bridge until one central per-use-case model policy exists (bead coding-harness-k0ub with coding-harness-wq1m); maintainer, 2026-11-06, morning question Q-M9, option A."}, {"date": "2026-11-06", "id": "cat-jam-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it, so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}, {"date": "2026-11-06", "id": "longcat-2.5-preview-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it (only LongCat-2.0), so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": [], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "mimo-v2.6-pro", "minimax-m3", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "grok-4.7", "qwen3.8-max", "kimi-k3"], "rungs": ["glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "mimo-v2.6-pro", "minimax-m3", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "grok-4.7", "qwen3.8-max", "kimi-k3"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor.

<!-- End of released loop record -->

Stage-2 call, 2026-11-08: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 922 files, 3619 commits, 12 rules.
