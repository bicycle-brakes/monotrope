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

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5802 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5803 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:3afc29b0fdc51f2388d15e89d0968ecb8447272769f0327d14641b5c0d399c90

Spec review commit: 79bd397e3247db9da50e0bbd16e370d5bce2130c

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-4 | [AMBIGUITY] | SPEC | fix-r1 | spec.md AC3; tests/test_stage2_research_catalog.py:134-141 | The refutation "the marker is written before either current-step request starts" has two readings. Reading A: before any of the two has started. The handler appends its own `start` event before it checks and writes the marker, so this state cannot occur, and the refutation never fires. The fault D-5 names also passes: with the overlap step's events still in the list, the first current-step arrival writes the marker. Reading B: before both have started, so the marker comes after one start and before the other. That is exactly the stale-event case, and it can only be refuted if the test sees the marker write ordered against the second current-step `start`. The criterion's main sentence ("recorded starts for both") fits B; the refutation's wording fits A. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-8 (2026-11-25) | — |
| S-5 | MAJOR | SPEC | base | spec.md AC5, AC7; decisions.md D-4; tests/conftest.py:60-68, 109-116; tests/test_atomic_test_log.py:1138-1139, 1157 | AC7's exit-status check cannot go red for a guard that writes the violations header and lines but no longer sets `session.exitstatus` (conftest.py:116). Today 9 of the 12 (outcome, drain) cases catch that fault: skip, xfail, setup and finalizer under both drains, and pass with drain on. In those cases no node fails, so only the audit makes the run exit 1. In a bundle, the `error` node fails on its own ValueError, and with drain off the `pass` node is also forced to fail (conftest.py:62-68), so every bundle exits 1 whatever the audit does. The per-node attribution lines of AC6 are still printed, so neither AC6 nor AC7 turns red. D-4 places the session checks once per bundle, but it does not keep this fault detectable. The spec's "preserving their existing checks" and D-2 therefore do not hold for the audit's failing of the session. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-7 (2026-11-25) | — |
| S-6 | MINOR | SPEC | fix-r1 | spec.md AC6; tests/conftest.py:60-78; tests/test_atomic_test_log.py:1127-1139 | AC6 requires each node to have "the expected result", but neither the spec nor D-4 gives that result per outcome, and today's test asserts no per-node result. Three outcomes have no obvious value. `error` raises ValueError in the body, which pytest reports as failed, not error. `finalizer` passes its call and skips in teardown: the terminal counts it as both passed and skipped, and JUnit records `<skipped>`. `pass` is forced to fail with drain off but passes with drain on. Without a stated table, the implementer takes the oracle from a first run, and "a wrong node result" has nothing to be refuted against. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-9 (2026-11-25) | — |
| S-7 | MINOR | SPEC | fix-r1 | spec.md AC8 | The refutation "materially different load" cannot be shown from the pull request. AC8 does not require load to be recorded with either measurement (for example a load average or the other processes running), and it does not say what counts as material. A before/after pair taken under different load therefore meets AC8 as far as anyone reviewing the pull request can tell. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-10 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5804 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5805 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:fdcfb9486b7ffdee338b7ed49b3fa8d5b8228af8896fa54b464ed738e0c5927e

Spec review commit: c256141e2f873a50fe9abe8c3c9318cbcab5394d

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-8 | MINOR | SPEC | fix-r1 | spec.md AC8; decisions.md D-3, D-10 | AC8 can be refuted by "a different machine or worker setting", but it only requires the pull request to record the duration totals, the load readings and the base revision. It does not require recording the machine or the pytest command and worker setting behind each total. So a reviewer of the pull request cannot tell a before total taken on another machine, or with `-n auto` instead of serial, from a matched pair. Those two refutation clauses cannot turn red from the evidence AC8 asks for. D-10 closed the same gap for load by requiring a recorded number; machine and worker setting still have nothing recorded. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-11 (2026-11-25) | — |
