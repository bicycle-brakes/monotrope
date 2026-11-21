---
title: "Plan — red-against-commit"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-qvf7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, repair, red-first]
---

# Plan — red-against-commit

```text
For you:     A repair can prove its test red at an earlier eligible commit even when the fix is already committed.
Done when:   Selected commits prove qualifying red and attempted code proves green; invalid selections refuse and existing repair forms keep their protections.
Appetite:    2 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Initial implementation, criterion-ledger evidence, guard-test changes and portable saved-attempt refs.
Pre-mortem:  suppose it failed: most likely because a selected commit is accepted without a real red proof.
Starts unless you say stop.
```

## Build sequence

1. In `scripts/stage2.py`, extend ordinary fixed-line parsing with the optional ` — red against <sha>` suffix; preserve all existing forms and reject the suffix on guard and not-a-test forms. Resolve an unambiguous hexadecimal commit ID to the full object ID without accepting revision expressions, tags, trees or blobs. At repair validation check it is an ancestor of the run-start HEAD or a ref under `refs/stage2/attempts/<change>/`, and that the selected commit contains the named test file; fail closed with scrubbed reasons if resolution, reachability or inspection fails. Use the selected full ID only for that row's existing `red_first` baseline; retain attempt tests, fixed-tree green proof, all isolation and all-or-nothing bookkeeping. Preserve ordinary marks unchanged and include the full selected ID in the selected form's status and evidence mark.
2. In `tests/test_stage2.py`, add the ledger regressions using real temporary Git history and proof runs where needed: a fix committed after an earlier faulty commit, an uncommitted attempt test, eligibility via HEAD and same-change saved ref, bad objects and other-change refs, an absent old test file, red/green failures, multiple rows and existing forms. Demonstrate each new behavior test red with the corresponding fault, then green after restoring the implementation.
3. Orchestrator, as a bootstrap edit after the accepted attempt: update held `prompts/04-implement.md` to explain the form and requirements. Update `docs/WORKFLOW.md` alongside it with the same contract. In `scripts/stage2.py` update the runner-owned repair answer instructions so the repair model actually receives the form. Do not delegate the held prompt edit to the implementation attempt.
4. The orchestrator regenerates `plans/INDEX.md` using `python3 scripts/plans_registry.py` after header changes. Run the verification below and record results against the implementation commit; remove `not yet written` from ledger entries when their named tests exist.

## Files and ownership

- `scripts/stage2.py` — implementation attempt: parse, authorize, resolve, prove and record the selected commit; update runner-owned repair instructions.
- `tests/test_stage2.py` — implementation attempt: regression tests for every criterion.
- `docs/WORKFLOW.md` — orchestrator: document selected-commit repair evidence.
- `prompts/04-implement.md` — orchestrator only: update the held repair instructions.
- `plans/changes/red-against-commit/spec.md`, `plan.md`, `findings.md` — orchestrator: maintain phase artifacts and review evidence.
- `plans/INDEX.md` — orchestrator: regenerate the registry, not by hand.

Do not change accepted ADRs, gate definitions, criterion-ledger grammar, saved-attempt lifecycle, initial implementation behavior or other changes. The selected commit's test file must exist even though the red run overlays the attempt's tests. A red result alone cannot prove the failure's semantic cause; phase 6 assesses the actual fault. Phase 1 used Stage 2, route `flash`, endpoint `glm-coding-plan`, model `glm-5.3-flash`; no Stage-1 fallback is recorded.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_red_against_commit_fixed_line — valid selected status is rejected or loses the commit.
- 2: not yet written tests/test_stage2.py::test_red_against_commit_refuses_ineligible_objects — an invalid, unrelated or other-change object is accepted.
- 3: not yet written tests/test_stage2.py::test_red_against_commit_requires_old_test_file — a test file only in the attempt is accepted.
- 4: not yet written tests/test_stage2.py::test_red_against_commit_uses_old_code_and_attempt_tests — HEAD production or old tests are exercised.
- 5: not yet written tests/test_stage2.py::test_red_against_commit_requires_qualifying_red — green or nonqualifying failure passes.
- 6: not yet written tests/test_stage2.py::test_red_against_commit_requires_attempt_green — a failing attempted tree is accepted.
- 7: not yet written tests/test_stage2.py::test_red_against_commit_records_only_complete_proofs — a partial batch or misidentified commit is recorded.
- 8: not yet written tests/test_stage2.py::test_red_against_commit_preserves_default_baseline — ordinary repair changes baseline or evidence.
- 9: not yet written tests/test_stage2.py::test_red_against_commit_does_not_extend_other_forms — guard or not-a-test suffix is accepted.
- 10: not yet written tests/test_stage2.py::test_red_against_commit_preserves_proof_protections — selected proof bypasses existing isolation or execution checks.
- 11: not yet written tests/test_stage2.py::test_red_against_commit_repair_instructions — model-facing or held prompt omits the selection contract.

## Verification

```sh
python3 scripts/check_interview_minimums.py --change red-against-commit
python3 scripts/check_criterion_ledger.py
make verify
```

## Time used

2026-11-21 17:15:42–17:18:32 UTC, 171 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
