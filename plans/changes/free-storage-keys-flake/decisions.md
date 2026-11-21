---
title: "Decisions — free-storage-keys-flake"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-068l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, flaky-test, research-swarm]
---

# free-storage-keys-flake — Decisions

Class: bounded (bead coding-harness-068l).

## The bead and a first measurement (orchestrator, 2026-11-21)

> tests/test_stage2_swarm.py::test_free_model_storage_keys_preserve_best_effort_completion[False-vendor/aaaa…] failed (assert 1 == 0, line 3293) in the merge-queue run of PR #351 on base 8f740e13 at 2026-11-08 14:21 UTC, while PR #348 passed the same suite on the same base minutes later; #351 touches no swarm code. Reproduce locally (repeat runs, random order), find the nondeterminism and fix it.

`assert 1 == 0` is the test's first assertion, `sworld.run() == 0`: the swarm run exited 1 although no member was scripted to fail (`failed=False`), with the 130-character model name. Measured by the orchestrator on 2026-11-21 at `ee349b78`: 25 serial runs of the test's six cases, all green; one run with random order, green. So the fault needs load or ordering the serial runs do not produce.

## SKIP · interview

status: skipped
reason: The bead fixes the goal (reproduce, find the nondeterminism, fix it); the maintainer asked for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Reproduce first, under load.** The attempt runs the failing case under the conditions CI had — the full swarm test file with `-n auto` and random order, repeated, beside a CPU load — and records how often it fails and the swarm run's own stderr for a failing run. Reason: serial runs do not fail (measured above).
- **Then fix the cause, not the symptom.** A forced reproduction of the found interleaving is the regression test, red before the fix. No retry, no wider timeout, no skip. Reason: the bead, and the oag7 precedent.
- **If no cause is found within the appetite,** the attempt stops and reports what it tried and measured in a `findings.md` section 'Stopped without a cause'; no speculative change. Reason: a fix without a reproduced cause hides the flake.
- **The archived research-swarm plan's ledger rows** for this test stay valid; a rename of the test is avoided. Reason: the criterion-ledger gate pins them.
