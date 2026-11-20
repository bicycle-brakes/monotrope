---
title: "Plan — ladder-next-step"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-hwll
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, review-loop]
---

# Plan — ladder-next-step

```text
For you:     A consumed review ladder names whether to repair or proceed to review.
Done when:   Both next steps and the existing safety stops are tested, and make verify is green.
Appetite:    4 hours of phase 4, including repairs; stop at the limit.
Not now:     Automatically starting the next step or changing the ladder and its restart rules.
Pre-mortem:  suppose it failed: most likely because released history is mistaken for a fresh run.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: add the ledger's regression tests; adapt existing assertions that expect the old spent-ladder refusal, including the released snapshot, replacement-rung and excluded-paid-model cases. Exercise the command's exit and output, not only a helper.
2. `scripts/stage2.py`: in `review_loop`, preserve the existing row, origin, record, clean and repair-brake checks and the snapshot/history reconstruction. At the consumed-stage branch for a run with a last non-clean round, retain exclusion diagnostics, inspect that last round for `taken` status, print the single corresponding `next:` line and return normally; do not call another verb or change the record. Keep failures without a completed round and other non-exhaustion stops on their existing paths. Do not change clean-stop exit 3 or refusal exit 2.
3. After the accepted implementation attempt, the **orchestrator** updates the held files `prompts/04b-review-loop.md` and `prompts/06-review.md`: replace the spent-ladder maintainer stop with repair first when needed, then full `make verify` and phase-6 review; retain verdict-first release and the separate brake. The attempt must not edit those paths.
4. `docs/WORKFLOW.md`: update the phase table, verb/exit description and review-loop doctrine to the same sequence, preserving the restart and other stop rules. `plans/changes/ladder-next-step/spec.md` and `plans/changes/ladder-next-step/plan.md` are this change's yardstick and execution plan; update only if review requires it. `plans/INDEX.md`: regenerate through the repository's index writer if the artifact headers make it stale.

Do not edit `AGENTS.md`, model declarations, ADRs, tracker data or availability policy. The phase-6 review remains independent and reads the whole diff after a fresh full verification; it is not started by `review-loop`.

## Verification

```sh
.venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/test_stage2.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_spent_ladder_names_review_after_repair — the exit is nonzero or the exact next line is absent, duplicated or names repair.
- 2: not yet written tests/test_stage2.py::test_spent_ladder_names_repair_for_taken_row — a taken row yields review or a nonzero exit.
- 3: not yet written tests/test_stage2.py::test_spent_ladder_next_step_does_not_start_or_mutate — a reviewer or repair starts or the saved run changes.
- 4: not yet written tests/test_stage2.py::test_spent_ladder_next_step_after_release — released fixed or taken rows produce the wrong instruction or admit a stage.
- 5: not yet written tests/test_stage2.py::test_spent_ladder_preserves_prior_stops — a next line bypasses an undecided or unmarked row, invalid origin or record, clean round, or repair brake.
- 6: not yet written tests/test_stage2.py::test_spent_ladder_retains_paid_exclusion_reasons — the result omits an excluded model's reason.
- 7: not yet written tests/test_stage2.py::test_spent_ladder_doctrine_names_next_steps — a workflow or prompt text retains the spent-ladder maintainer stop or loses the verification and review sequence.

## Time used

2026-11-20 14:51:43–14:54:03 UTC, 140 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
