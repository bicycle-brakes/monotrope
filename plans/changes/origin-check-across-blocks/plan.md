---
title: "Plan — origin-check-across-blocks"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-3h96
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, repair, origin]
---

# Plan — origin-check-across-blocks

```text
For you:     Repair stops on invalid provenance in an older selected finding and names where to correct it.
Done when:   Multi-block refusal and successful-repair tests pass, existing validation scopes hold, the workflow agrees, and make verify is green.
Appetite:    One hour of phase 4 including repairs; stop at the limit.
Not now:     Historical backfill, automatic provenance, parser changes or a new repair-brake policy.
Pre-mortem:  suppose it failed: most likely because the new check revalidates completed history instead of selected repair targets.
Starts unless you say stop.
```

## Scope and route

Implement the bounded correction in `spec.md` (bead `coding-harness-3h96`).
No design or ADR is due. Explore used Stage 2, GLM 5.3 Flash, on 2026-11-10;
no Stage-1 exploration fallback is recorded. The orchestrator shows the card
unchanged before implementation; this draft implements no code and commits nothing.

## Build sequence

1. Add a repair-target Origin check in `scripts/stage2.py` over the exact
   `(place, row)` batch returned by `repair_targets`. Reuse `ORIGIN_VALUE`
   full-cell validation after trimming; preserve status case handling,
   `findings_rows`, `record_rows` and the shared `origin_refusal` scope.
   Include selected record/released rows as well as every selected phase-6 row;
   do not sweep unselected historical rows. Per the maintainer's option D
   (2026-11-12, superseding answer A), add one resolver for the latest row of
   each finding ID across tables, the active record after findings history.
   Both repair selection and its target-Origin check ask only that resolver.
   Repeated IDs across tables are history; duplicate IDs within one table refuse.
   Diagnostics name the resolved row's ID and file, with no back-computed location.
2. Invoke that check in `repair` after the existing undecided-row refusal and
   before `time_log`, snapshots, probes, audit appends or `run_attempts`.
   Keep the existing record/newest-block `origin_refusal` call and all later
   admission checks. Aggregate invalid selected rows into one `Refused`
   diagnostic with their IDs, files, allowed values and the
   orchestrator's correction instruction. Never infer or rewrite Origin.
3. In `tests/test_stage2.py`, use `phase6_cells`, `phase6_block`, `World`,
   `origin_state`, `script_repair` and `repair_step` to exercise the real verb
   with local stand-ins. Plant two older blocks and a newest block that is
   empty, says `No finding.`, or has valid rows. Parameterize invalid values
   from `INVALID_ORIGINS`, uppercase/lowercase taken statuses, missing/present
   record and default/Stage-2-off routes. Meet all unrelated preconditions.
   On refusal assert exit 2, no model/probe/verify calls, unchanged findings,
   record, plan, stage state and HEAD; test multiple invalid targets and repeated
   headings for ID-and-file diagnostics. Include invalid selected released rows.
4. Add successful multi-block repairs for `base`, `fix-r1`, `fix-r12`, checking
   the batch and in-place fixed marks with Origins preserved. Keep superseded
   invalid fixed/rejected rows in fixtures to prove they do not block. Pin the
   other three verbs' newest-block scopes with older taken rows; leave their
   existing decision refusals intact. Retain existing legacy-history,
   control-flag, undecided and legacy-completion tests. Scope duplicate-ID tests
   to one table; add latest-row tests for both callers and in-place status writes.
5. Update only the repair guarantee in `docs/WORKFLOW.md`: all selected rows
   need valid Origin before effects, including older phase-6 blocks and selected
   released rows; passive released/superseded history retains its exemptions.
   Preserve the pinned ownership phrases in the row-decision paragraph.

## Files and ownership

- `scripts/stage2.py`: implementation attempt adds the target check and wires it only into repair.
- `tests/test_stage2.py`: implementation attempt adds the ledger tests using existing fixtures.
- `docs/WORKFLOW.md`: implementation attempt states the repair-specific guarantee and historical exemption.
- `plans/changes/origin-check-across-blocks/spec.md`: runner maintains implementation status.
- `plans/changes/origin-check-across-blocks/plan.md`: attempt clears ledger placeholders as tests land; runner records measured time.
- `plans/changes/origin-check-across-blocks/findings.md`: runner appends audits and later review evidence.
- `plans/INDEX.md`: runner regenerates the derived registry, never the implementation attempt.

No deletions or held-path bootstrap edits are needed. Leave `research.md`,
`decisions.md`, other changes, historical findings, prompts, templates,
settings, governance, ADRs, tracker data, README and AGENTS untouched.

## Verification

The implementation worktree needs `make venv` and `bash tools/pi/install.sh`
once before full verification. Run these commands verbatim:

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'origin or repair_lists_every_taken_row or repair_skips_canonical_hand_repairs or undecided_row_holds_the_repair or doubled_taken_id or repair_refuses_legacy_completed'
python3 scripts/check_interview_minimums.py --change origin-check-across-blocks
python3 scripts/check_research_handoff.py --change origin-check-across-blocks
python3 scripts/check_criterion_ledger.py
make verify
```

At `89339cbd` (2026-11-10), `templates/plan.md` and
`scripts/validate_change_artefacts.py` do not exist. Use the phase-3 prompt's
form and the available gates; do not create replacements. The runner regenerates
`plans/INDEX.md`, checks `python3 scripts/plans_registry.py --check`, runs full
verification and makes the commit after this draft.

## Criterion ledger

- 1: tests/test_stage2.py::test_repair_rejects_invalid_origins_in_selected_history — older taken or selected released rows with invalid Origin reach a repair attempt
- 2: tests/test_stage2.py::test_repair_origin_refusal_has_no_effects_across_blocks — a call, audit, time entry, file/state mutation or commit precedes refusal
- 3: tests/test_stage2.py::test_repair_origin_refusal_locates_every_selected_block — a bad target or its source file is omitted, a valid target is accused, or correction guidance is incomplete
- 4: tests/test_stage2.py::test_repair_preserves_valid_origins_across_blocks — valid older targets are refused, omitted, relocated or have their Origins rewritten
- 5: tests/test_stage2.py::test_origin_history_check_is_limited_to_repair_targets — other verbs broaden validation or repair audits unselected historical rows
- 5: tests/test_stage2.py::test_legacy_released_origin_does_not_hold_verbs — completed historical provenance blocks a verb
- 5: tests/test_stage2.py::test_origin_release_controls_keep_distinct_validation_scopes — ordinary release audits superseded rows or control flags check Origin
- 5: tests/test_stage2.py::test_an_undecided_row_holds_the_repair — pending decisions no longer hold repair
- 3: tests/test_stage2.py::test_repair_and_origin_check_resolve_latest_finding — repair selection or Origin admission uses superseded history instead of the latest row
- 3: tests/test_stage2.py::test_resolver_refuses_duplicate_ids_within_one_table — duplicates within one table are admitted
- 4: tests/test_stage2.py::test_repair_marks_only_the_resolved_finding_row — a repair rewrites a historical row
- 4: tests/test_stage2.py::test_repair_marks_only_the_resolved_record_row — a record repair rewrites a historical table
- 6: not a test — phase-6 review reads the repair section of docs/WORKFLOW.md against criterion 6; missing the all-block pre-effect guarantee or demanding passive backfill refutes it

## Runner route — 2026-11-10

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-12

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-10 13:23:26–14:49:30 UTC, 5163 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-10 14:49:48–16:15:50 UTC, 5161 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-10 16:16:04–17:43:31 UTC, 5246 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-10 19:46:37–20:30:52 UTC, 2655 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-10 21:44:52–23:15:55 UTC, 5462 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-10 23:16:10–2026-11-11 03:31:19 UTC, 15308 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-11-11 23:28:06–2026-11-12 00:05:46 UTC, 2260 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-12 00:06:07–01:03:39 UTC, 3451 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-12 01:04:03–01:05:01 UTC, 58 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-12 20:47:03–22:14:41 UTC, 5258 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
