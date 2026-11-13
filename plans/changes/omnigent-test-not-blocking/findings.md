---
title: "Findings — omnigent-test-not-blocking"
category: findings
status: draft
implementation_status: none
date: 2026-11-12
created: 2026-11-12
last_reviewed: 2026-11-12
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-i9df
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — omnigent-test-not-blocking

Stage-2 call, 2026-11-12: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1037 files, 4037 commits, 12 rules.

Stage-2 call, 2026-11-13: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1040 files, 4044 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/omnigent-test-not-blocking/plan.md` +4 -4
> - `plans/changes/omnigent-test-not-blocking/spec.md` +1 -1
> - `scripts/omnigent_policy.py` +38 -1
> - `tests/test_omnigent_deny_layers.py` +195 -9
> - `tools/omnigent/README.md` +16 -0
> - `tools/omnigent/install.sh` +13 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/omnigent_policy.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> tests/test_omnigent_deny_layers.py:239:45: ARG001 Unused function argument: `log`
>     |
> 239 | def _fake_reporting_python(directory: Path, log: Path) -> Path:
>     |                                             ^^^ ARG001
> 240 |     """An interpreter that logs each call and answers the merge and report modes like the real ones.
>     |
>
> Found 1 error.
> ```

Stage-2 call, 2026-11-13: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1040 files, 4049 commits, 12 rules.
