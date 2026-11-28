---
title: "Findings — verify-lock-handle"
category: findings
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-42em
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-lock-handle

Stage-2 call, 2026-11-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1325 files, 6177 commits, 12 rules.

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6178 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:cea8c561bedd64740010bc030f551229881ee93249acffe1ec65ebe4e5dccd13

Spec review commit: 58b7c0ce1a7b9beb1e7aa1243bc01b51d5d0700a

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S1-1 | [AMBIGUITY] | SPEC | base | spec.md, Acceptance criterion 8 | "When no owned admission is supplied" can be read two ways. (a) Strict: `inherit_env` without a handle never uses this process's own held admission, even when it holds exactly one. Then every call site that relies on the implicit active admission today must change, or its children lose the marker and queue for a fresh slot: `scripts/verify_run.py:928` (`inherit_env(gate_env)` inside `hold_admission`) and `scripts/stage2.py:8518` ("Full verification carries its admission"). (b) Lenient: without a handle the call falls back to the process's admission when exactly one is held, and drops the marker only when concurrent admissions make the choice ambiguous. Then unchanged callers keep working, but whether a child gets a marker depends on what else the process holds at that moment. The refutation ("inherits an arbitrary concurrent admission") is satisfied under both readings, so it cannot tell them apart. | Opus | in spec — reading b (one held admission is used, two or more refuse); [DETAIL] S1-1..S1-5 (bounded standing grant) | — |
| S1-2 | MAJOR | SPEC | base | spec.md, Acceptance criterion 3; `scripts/verify_lock.py:671` `admission_context()` | The spec says nothing about the measurement context read inside the process. `admission_context()` takes no argument and reads the single global `_ACTIVE`. Callers: `scripts/verify_run.py:948` and `:963` call it while holding an admission to record the run's context, and `scripts/verify_duration.py:283` calls it too. Criterion 3 covers only what a child receives. With two concurrent admissions in one process, the builder has to invent the answer: take the handle, resolve per thread or context, return unknown, or keep the latest. Each choice records a different `admission_id` and wait for the same run. | Opus | in spec — admission_context takes the same optional handle and rule; [DETAIL] S1-1..S1-5 | — |
| S1-3 | MAJOR | SPEC | base | spec.md, Acceptance criteria 2 and 7; Problem ("refuses a second independent admission") | Once the refusal is lifted, the spec does not say what happens when a new admission is waiting only on the same process's own held admission. Examples: under `HARNESS_VERIFY_SLOTS=1`, a second admission requested on the same call stack as the first; a setting-`1` request while the process holds a slot; a third request on one call stack while that process already holds both slots. `_queue_wait` (`verify_lock.py:1041`) has no deadline, and only the queue head may reserve, so such a request waits forever and stalls every later waiter on the machine. Today `_independent_admission_guard` refuses it promptly. Criterion 2 forbids a refusal "solely because of the process" and covers only two eligible setting-`2` admissions. Whether this case is refused, detected or left to wait has to be decided while building. | Opus | in spec — self-wait refused at once with the held admissions named; [DETAIL] S1-1..S1-5 | — |
| S1-4 | [AMBIGUITY] | SPEC | base | spec.md, Acceptance criterion 5 | "Specific to its token" can be read two ways. (a) The temporary name contains the raw token, as the bead says ("named by the admission token"). That puts the ownership secret into a file name in the state root, visible to any process that can list it, although the module promises that no unrelated process knows the token and that the token is never part of the context (`verify_lock.py:45`, `:58`). (b) The name is only unique per admission: derived from the token, or from the non-secret `admission_id`. The refutation (two admissions with the same pid choose the same name) passes under both readings, so it does not settle whether the secret may appear in a file name. | Opus | in spec — reading b (names from admission_id, never the token); [DETAIL] S1-1..S1-5 | — |
| S1-5 | MINOR | SPEC | base | spec.md, Acceptance criteria 1 and 3 | Once `hold_admission` yields a handle object instead of a short-lived tuple, the spec does not say what the handle does after its admission is released. `release()` closes its descriptors (`verify_lock.py:775`-`777`). The next concurrent admission in the same process to open its state usually gets the same descriptor numbers, so a child launched with a stale handle would inherit the other admission's locks, which criterion 3 forbids. The spec also does not say whether `inherit_env` or the descriptor accessor of a released handle refuses, returns nothing, or still hands out the stale marker. | Opus | in spec — released handle accessors raise; [DETAIL] S1-1..S1-5 | — |
