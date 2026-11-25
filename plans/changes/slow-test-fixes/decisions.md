---
title: "Decisions — slow-test-fixes"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.16
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, tests, speed]
---

# slow-test-fixes — Decisions

## SKIP · interview

status: skipped
reason: Test-only speed fixes with remedies stated in the bead (coding-harness-bxxt.16, filed at the maintainer's request on 2026-11-24 from a checked analysis); every fix keeps what its test asserts, so no design choice is left to the maintainer.

## Details decided by the orchestrator

[DETAIL] **D-1 (scope; the finder sleep stays out)**: this change makes three of the bead's four fixes: (1) tests/test_pi_contract.py drops the five identical baseline Pi calls of its flag test and keeps one baseline plus one call per flag; (2) tests/test_stage2_research_catalog.py uses the existing `held_collect` instead of waiting a real 10-second deadline; (4) tests/test_atomic_test_log.py bundles its 24 nested pytest runs into one run per (workers, drain) pair that checks all six outcomes. The 5-second finder sleep in tests/test_stage2_swarm.py stays with the neighbour change swarm-test-speed (bead coding-harness-dca4), whose research names the same test. Reason: no two lanes edit the same test.

[DETAIL] **D-2 (no assertion is lost)**: every rewritten test keeps each assertion it has today, against the same inputs; the plan maps old assertions to new ones. Reason: a speed fix must not weaken a test.

[DETAIL] **D-3 (measure)**: the pull request records each rewritten test's duration before and after (`pytest --durations`, same machine, same commit for the base via the base's test file). Reason: the bead's numbers are counted from source, not measured.

[DETAIL] **D-4 (spec review S-1, attribution in one session)**: inside each bundled session every outcome is its own test node; per-outcome assertions read that node's result from the session's JUnit XML report, so each stays attributable to its outcome; the four whole-session checks (exit status, the violations header, the `raw read_text` text, the pass count) are asserted once per bundle against the value the bundle's known mix of outcomes produces. Reason: AC5 can only ask per-outcome attribution of per-outcome assertions.

[DETAIL] **D-5 (spec review S-2, a fresh held step)**: the deadline step starts from a fresh event list (a new source, or the events cleared after the overlap step), and the test asserts `held_collect`'s marker is written only after both requests of this step have started, so "does not hold both requests until the deadline" can turn red. Reason: the shared, never-cleared event list made the clause untestable.

[DETAIL] **D-6 (spec review S-3, durations)**: Reading B — the pull request reports one total per test function, summed over its parametrised cases, before and after. Reason: 24 old node ids cannot be paired with four new ones.

[DETAIL] **D-7 (spec review S-5, keep the exit-status catch; refines D-4)**: each (workers, drain) pair runs two nested sessions, not one: a quiet session with the outcomes in which no node fails (pass, skip, xfail, setup, finalizer), where exit status 1 can only come from the audit, and a separate session for the failing outcome (error); 8 nested runs instead of 24. Reason: one mixed session would let a guard that no longer sets the exit status pass.

[DETAIL] **D-8 (spec review S-4, the marker's timing)**: Reading B — the test records the current step's two `start` events apart from earlier steps and fails if the marker exists before the second of them; the step starts from a fresh event list (D-5). Reason: only that reading can turn red.

[DETAIL] **D-9 (spec review S-6, per-node results)**: the expected JUnit result of every outcome node is measured once from a run of today's code and written into the test as a table (for example `error` is reported as failed, `finalizer` as passed with a skipped teardown); the plan records the measurement. Reason: the spec cannot name values nobody has measured.

[DETAIL] **D-10 (spec review S-7, comparable load)**: each duration in the pull request carries the one-minute load average (`os.getloadavg()[0]`) taken just before it; before and after count as comparable when those differ by at most 1.0, otherwise both are measured again. Reason: "materially different load" needs a recorded number.

[DETAIL] **D-11 (spec review S-8, record the setting)**: with each before and after total the pull request records the machine (`platform.node()` and `platform.machine()`) and the exact pytest command line including its worker setting; both sides use the same command. Reason: otherwise a mismatched pair cannot be told from a matched one.

