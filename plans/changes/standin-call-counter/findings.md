---
title: "Findings — standin-call-counter"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.14
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — standin-call-counter

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5814 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5815 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:0deae4698aa7f9afe5fe2cdc9d3cde467646821e66c59798625e91f81aed42f9

Spec review commit: 7b66c7e428eba0fc98d47409bc985a094cbfebc4

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | spec | spec.md Acceptance criteria 3 and 4; Non-goals ("other suites' log readers") | Two readings of what resets the counter. Reading A: only `SwarmWorld.rewind` resets it, as criterion 4 says. Today 32 places reset the step count by unlinking calls.jsonl directly: 25 in tests/test_stage2_swarm.py (e.g. 1645, 1661, 2222, 2247) and 7 in tests/test_stage2_research_deep_review.py (e.g. 58, 82). Under reading A each of them keeps a stale count. At tests/test_stage2_swarm.py:1661-1663, for example, the first `repository:4:mimo-v2.6-pro` call after the unlink then answers a later step (`good`) instead of step 0 (`bad`). Every site would have to be edited, and one of the two files belongs to another suite that the non-goals may exclude. Reading B: any removal of calls.jsonl resets the count, so the counter follows the log's existence or identity. No caller changes, but it needs a different mechanism. Criterion 3's parity covers only sequences without such a clear, so the spec rules out neither reading. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-4 (2026-11-25) | — |
| S-2 | MAJOR | SPEC | spec | spec.md Acceptance criteria 2, 4 and 5; decisions.md D-2 | Criterion 5 invokes the shared locked protocol, but the spec does not say how the counter keeps that protocol's clear-by-removal guarantee. The protocol locks the data file's own inode and clears a log by removing the file. A late writer of the cleared run therefore finishes on the removed file and never reaches the next run (plans/changes/flaky-swarm-leak-test/spec.md [DETAIL] L2-2; tests/test_atomic_test_log.py:724). D-2 puts the counter in a separate file updated under calls.jsonl's lock, and removing calls.jsonl does not split that file. A late writer still holding the old calls.jsonl lock and a new-run writer holding the new lock do not exclude each other on the counter file. The late increment can then land in the next run's counts, or one update can be lost. The spec leaves to the implementer whether the counter must give the same guarantee, and how. No criterion names the refuting input: a writer that holds the old lock across a clear. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-5 (2026-11-25) | — |
