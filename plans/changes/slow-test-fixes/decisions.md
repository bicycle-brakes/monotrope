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
