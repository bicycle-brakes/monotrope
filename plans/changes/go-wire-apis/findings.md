---
title: "Findings — go-wire-apis"
category: findings
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
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
