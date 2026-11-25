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

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5816 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1206 files, 5817 commits, 12 rules.
## Phase 2a — fallback deepseek-v4.1-flash, 2026-11-25

Spec fingerprint: sha256:c0eda160ef295b1f4d0c8e4a83997e3b98679f681efcbd9d8da2bad8b816345f

Spec review commit: 4d794698ccca32c47854166907ddf738d9beb7bc

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] MAJOR | SPEC | spec.md | spec.md \u00a7Acceptance criteria 4, 5 and \u00a7Open decisions (D-4) | Identity is stated as "the log device and inode". Reading A: tag equality alone decides whether the counter describes the current log, so a log recreated after unlink that is handed the just-freed inode number (usual on ext4/tmpfs, and the reset path in criterion 4 is exactly unlink-then-create) matches the stale counter, the key starts at a later step, and criteria 4 and 6 are refuted in normal use. Reading B: identity must also change on recreation (compare the log's own size or line count, or mint a fresh token per log), which goes beyond the stated device-and-inode tag. The human settles which; the implementation differs. | deepseek-v4.1-flash | in spec — [DETAIL] decided by the orchestrator: decisions.md D-6 (2026-11-25) | — |
| S-2 | MAJOR | SPEC | spec.md | spec.md \u00a7Acceptance criteria 3 | Criterion 3 compares against "the former log-based counting", which this change deletes, and the spec does not say where that reference lives. An implementer can satisfy it by re-deriving the count from the counter's own formula inside the test, in which case the parity assertion holds by construction and criterion 3 can never go red. Only a frozen copy of the pre-change expression (the sum over records whose key is the selected one) makes the criterion refutable, and the spec does not require one. | deepseek-v4.1-flash | in spec — [DETAIL] decided by the orchestrator: decisions.md D-7 (2026-11-25) | — |
| S-3 | [AMBIGUITY] MAJOR | SPEC | spec.md | spec.md \u00a7Acceptance criteria 7, \u00a7Open decisions; decisions.md D-5 | Criterion 7 and D-5 say the counter is read and written only while the caller holds the lock on the log's own inode. That serializes writers of the same log but not a writer still holding the removed inode against a writer of the new one, which is precisely the case criterion 6 constructs and which no shared lock covers. Reading A: the log-inode lock is sufficient, so an in-place write of the counter is conforming and a concurrent reader can see half a counter, refuting criterion 7. Reading B: the counter needs its own atomic publication (write then rename) and a stated behaviour for a lost update. The choice fixes the write primitive. | deepseek-v4.1-flash | in spec — [DETAIL] decided by the orchestrator: decisions.md D-8 (2026-11-25) | — |
| S-4 | MINOR | SPEC | spec.md | spec.md \u00a7Acceptance criteria 5 | Criterion 5 rebuilds only when the counter is missing or belongs to a different log identity. A counter that exists, parses and carries the current identity but holds a foreign shape (an older key set, or a payload truncated by a writer outside the helper) is neither missing nor mismatched, so the implementer must choose between rebuilding and raising, and a raise would break every swarm run. The spec does not say which. | deepseek-v4.1-flash | in spec — [DETAIL] decided by the orchestrator: decisions.md D-9 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5818 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5819 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:a8d6f3eacd0e2469dd542a33a2ba361933d7be441bce1db2ae48c585aac8943e

Spec review commit: f709bf35caa7b3d911f843e5dff6e9a13d1c25f3

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] MINOR | SPEC | spec | spec.md Acceptance criterion 5; decisions.md D-9; tests/atomic_test_log.py:27-32 | Two readings of what D-9's "the stand-in never raises on it" covers once a rebuilt counter has to be published by temporary file and replacement. Reading A: only reading the bad counter is exempt. A failed publish then propagates, as the helper's own contract requires ("Other I/O errors ... propagate", "Nothing is retried or suppressed"). Reading B: every error on the counter is exempt, including a failed replacement. The call then answers with the rebuilt count and leaves no valid counter behind. The two readings part on criterion 5's "unreadable" input when it is built as a directory at the counter's path. That is the construction that still works where the suite runs as root, since `chmod 000` blocks no read there. Reading the counter fails, the rebuild from the log succeeds, and `os.replace` onto the directory fails with EISDIR. Under A that call and every later one raises, which criterion 5's refutation names. Under B every call succeeds. A counter path in a non-writable directory splits the two readings the same way. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-10 (2026-11-25) | — |
