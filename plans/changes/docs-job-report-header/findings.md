---
title: "Findings — docs-job-report-header"
category: findings
status: draft
implementation_status: partial
date: 2026-11-02
created: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-ooj5
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — docs-job-report-header

Stage-2 call, 2026-11-02: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 816 files, 3018 commits, 12 rules.

Stage-2 call, 2026-11-02: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 819 files, 3023 commits, 12 rules.

Stage-2 call, 2026-11-02: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 819 files, 3027 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 819 files, 3029 commits, 12 rules.

Stage-2 call, 2026-11-02: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 819 files, 3029 commits, 12 rules.

## Regression evidence — 2026-11-02

The two new runner tests, run by the orchestrator on 2026-11-02 with
`pytest -q -p no:cacheprovider`:

- On the baseline (`scripts/verify_all.sh` of df326e26, the commit before the
  implementation): `test_runner_report_matches_selected_job` and
  `test_runner_report_keeps_gate_verdict` both fail (2 failed).
- On the implementation (c5317952): both pass (2 passed).

Stage-2 call, 2026-11-02: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 819 files, 3033 commits, 12 rules.

Stage-2 call, 2026-11-02: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 819 files, 3033 commits, 12 rules.
