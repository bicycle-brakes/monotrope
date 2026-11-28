---
title: "Plan — verify-lock-handle"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-42em
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verify-lock]
---

# Plan — verify-lock-handle

```text
For you:     Two verification admissions in one process keep their ownership and children separate.
Done when:   Overlap, inheritance and existing protection tests pass, and make verify is green.
Appetite:    4 hours of phase 4, repairs included — a stop, not an estimate.
Not now:     Changing capacity, queue or memory policy, foreign-model access, or holder record format.
Pre-mortem:  suppose it failed: most likely because a child still picks up another admission's state.
Starts unless you say stop.
```

## Build sequence and files

1. Change `scripts/verify_lock.py`: return the owned admission handle from `hold_admission`, remove the process-wide independent-admission guard and active singleton, and derive descriptors, token and fresh measurement context from the explicitly supplied handle. Preserve validated inherited nesting when there is no owned handle, existing cleanup and all capacity and security checks; publish through a token-specific temporary name. Ensure concurrent acquisitions and releases have independent state and do not select an implicit active admission.
2. Change `scripts/stage2.py` and `scripts/verify_run.py`: carry the particular handle through every protected child launch and measurement; use its descriptors and pass it to environment/context helpers. Calls outside an owned admission retain only validated ancestor inheritance, including cheap checks and formatting; preserve foreign environment filtering. Update the internal supervisor to use the same explicit ownership contract.
3. Change `scripts/verify_duration.py` only where necessary to retain context from a validated inherited environment without assuming a process-global owner.
4. Change `tests/test_verify_lock.py`: replace the single-process refusal assertions with concurrent two-slot ownership, release and failure isolation tests, token-specific publication, nested and forged-marker tests, and retain capacity, queue, memory and surviving-descendant coverage. Exercise real lock descriptors and holder records; use bounded waits so a self-deadlock fails.
5. Change `tests/test_stage2.py`, `tests/test_verify_before_admission.py`, and `tests/test_verify_duration.py`: update admission stubs and test the actual child descriptors, markers and context for their own admission, inherited and unowned paths, and foreign filtering.
6. Change `docs/WORKFLOW.md` and `docs/how-it-works.md`: replace any present-tense single-process boundary with explicit per-admission ownership and preserve the documented protection rules.
7. Change `plans/changes/verify-lock-handle/plan.md`: replace not-yet-written ledger entries with actual test names once defined and record phase-4 time.

Do not edit the archived predecessor, `scripts/kit/manifest.yaml` or `scripts/ci_gates.py` merely because they name the module; neither its path nor gate membership changes. No held path is assigned to the implementation attempt.

Explore used Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`, because GLM via Z.ai had reached its weekly limit until 2026-11-29.

## Criterion ledger

- 1: not yet written tests/test_verify_lock.py::test_hold_admission_returns_owned_handle — a tuple or missing ownership fields is returned.
- 2: not yet written tests/test_verify_lock.py::test_two_admissions_in_one_process_are_independent — the second is refused, deadlocks, or overwrites the first holder.
- 3: not yet written tests/test_verify_lock.py::test_concurrent_children_inherit_their_own_admission — descriptors, marker or context belong to the other admission.
- 3: not yet written tests/test_stage2.py::test_child_launch_uses_explicit_admission — a protected launch selects another handle.
- 4: not yet written tests/test_verify_lock.py::test_releasing_or_failing_one_admission_preserves_the_other — one admission invalidates the other.
- 5: not yet written tests/test_verify_lock.py::test_holder_publication_temporary_name_uses_token — equal process IDs select the same temporary name.
- 6: not yet written tests/test_verify_lock.py::test_nested_admission_reuses_only_valid_ancestor — a valid descendant queues or a forged marker nests.
- 7: not yet written tests/test_verify_lock.py::test_concurrent_handles_preserve_admission_protections — capacity, queue, floor, exclusive or surviving-child protection fails.
- 8: not yet written tests/test_stage2.py::test_unowned_and_foreign_children_do_not_inherit_an_owned_admission — an unrelated or foreign child receives an owned marker.

## Verification

```sh
python3 scripts/jobs.py start -- env -u HARNESS_JOB_RECORD make verify
```

Inspect the detached job's exit and output with `python3 scripts/jobs.py list`; phase 6 needs a green full verification on its head.

## Time used

2026-11-28 03:47:24–03:49:34 UTC, 130 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
