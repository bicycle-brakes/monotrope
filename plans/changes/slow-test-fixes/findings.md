---
title: "Findings — slow-test-fixes"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.16
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — slow-test-fixes

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5800 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5801 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:282d7c0f252b512d016c2c2246642a8d198d98a41c38e3f7ce87231279627242

Spec review commit: e8a2aabc85dd6845883ed396ec9eed8a86c66789

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md AC4, AC5; tests/test_atomic_test_log.py:1157-1161; tests/conftest.py:109-116 | AC4 puts all six outcomes into one nested session per worker and drain pair. AC5 still requires each existing assertion to be "independently attributable to that outcome", but four of them check the whole session, not one outcome: `run.returncode == 1`, the `stand-in log access violations` header, `raw read_text` anywhere in the output, and `"1 passed" or "2 passed"`. `pytest_sessionfinish` sets exit 1 when any test in the session recorded a violation, and the `error` outcome fails anyway on its own ValueError. So a bundled run exits 1 even when the guard loses the `skip` or `setup` access, which is the F6-10 fault this test exists to catch. The pass count also becomes a total over six outcomes. Reading A: keep the four checks as they are, once per run. That matches D-2 ("keeps each assertion it has today"), but none of the four can then fail because a single outcome lost its violation, which contradicts AC5. Reading B: replace them with per-node evidence, meaning each outcome's `test_recorded.py::<id>: raw read_text` audit line, its own result, and a clean test checked by node id. That matches AC5 but rewrites the existing assertions, against D-2's "same inputs" and "each assertion it has today". | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-4 (2026-11-25) | — |
| S-2 | MAJOR | SPEC | base | spec.md AC2; tests/test_stage2_research_catalog.py:137-142, 264-274, 928-938 | The AC2 clause "does not hold both requests until the deadline" cannot fail in the test, and reusing the helper as AC2 requires produces exactly that state. `held_collect` writes its marker once every held name appears among the `start` events in `sources.events`. That list is never cleared, and the overlap step earlier in the same test (line 929) has already recorded starts for both `pi` and `metadata`. With both held, the first held request to arrive therefore writes the marker. The controlled deadline then fires after three 5 ms polls (answered=0), whether or not the second request has reached the server. No existing assertion checks how many requests had arrived when the deadline fired. `len(sources.requests) == 2` is read only after the bridge returns, so it passes whenever the second request lands inside that window and fails only under load. That brings back the wall-clock bet that bead jik removed. The spec does not say whether the arrival record must cover only this call (cleared events, a fresh fixture or a per-call arrival count), and it does not name the observable state that shows both requests were held. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-5 (2026-11-25) | — |
| S-3 | MINOR | SPEC | base | spec.md AC6 | [AMBIGUITY] "Before and after durations of each rewritten test" has two readings for the log-guard test, which is 24 parametrised nodes before and four (or one) after. Reading A: one duration per pytest node id, as `--durations` reports it. That gives 24 rows against four that cannot be paired, and each new node looks slower than each old one. Reading B: one total per test function, summed over its parametrised cases and phases. That gives one comparable number per test. AC6 also fixes only "same machine". It says nothing about run conditions: serial or `-n auto`, and machine load. A before/after pair taken on the same machine under different load or worker settings meets AC6 even though the two numbers cannot be compared. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-6 (2026-11-25) | — |
