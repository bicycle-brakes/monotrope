---
title: "Plan — origin-cell"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-ywbh
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, repair-brake]
---

# Plan — origin-cell

```text
For you:     The orchestrator supplies finding provenance, and invalid accepted rows stop before the repair brake can be bypassed.
Done when:   Refusal, provenance preservation and brake regressions pass, ownership is documented, and make verify is green.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Prompt changes, automatic provenance, historical backfill or a new brake or restart policy.
Pre-mortem:  suppose it failed: most likely because release reconciliation deletes a record before checking its Origin cells.
Starts unless you say stop.
```

## Scope and prerequisites

Implement criteria 1–8 of `spec.md` as a bounded correction to the existing
repair brake (bead coding-harness-ywbh). No design or ADR is due. Explore ran
on Stage 2 through GLM 5.3 Flash on 2026-11-07; no Stage-1 fallback is recorded.
The orchestrator presents this card unchanged before phase 4. This draft
writes no implementation and makes no commit.

## Build sequence

1. Add one shared Origin-refusal helper in `scripts/stage2.py`, using
   `accepted_row` and the existing row parsers. Validate the trimmed complete
   cell against `base` or `fix-r[1-9][0-9]*`, case-sensitively. Collect every
   invalid accepted row with its source (loop record, released loop block or
   phase-6 table) and ID; return a `Refused` diagnostic explaining that the
   orchestrator must write the causal value. Do not change status parsing,
   `undecided`, `marks_a_test`, `fix_r_only` or row layouts.
2. Invoke that helper over the selected change's record and both groups from
   `findings_rows` at `review_loop`, `review`, `release` and `repair` before
   model/probe calls, audit appends, attempt execution, consumption or data
   mutation. In `release`, place it before the already-released digest/identity
   branch: both reconciliation and ordinary release must validate before any
   rewrite or removal. Reuse the same check for `review`'s internal release.
   Check all authoritative accepted rows, including earlier released rows;
   leave parsers permissive and restart/stage-retirement semantics unchanged.
3. Extend local `World` fixtures in `tests/test_stage2.py` to model the real
   orchestrator: `decide_record` explicitly sets Origin when deciding an
   accepted row (default `base`, overridable), and `World.write_record` seeds
   valid decided rows. Preserve deliberately arbitrary reviewer output in
   `rows()` and dedicated negative fixtures. Audit direct accepted-row
   literals in affected tests; give them explicit causal values rather than
   relaxing validation. Retain all existing test names used by other ledgers.
4. Add the ledger tests below with local stand-ins. Parameterize all four
   verbs against all three row locations, taken/fixed statuses and invalid
   values. Meet other preconditions so failures reach the Origin guard; assert
   exit 2, no calls, unchanged record/findings bytes and unchanged stage state.
   Exercise an already-released record with matching digest, and a changed
   record with matching identity that would reconcile. Test valid values,
   status case handling, rejected/open exemptions, quoted non-rows, unchanged
   intake and preservation through repair/release. Retain existing evidence
   refusals; a valid Origin must not make an unmarked accepted row decidable.
5. Extend the existing two-round brake regression with split released/record
   history, both accepted statuses and a rejected row with arbitrary Origin;
   an accepted base row in either round must admit continuation under otherwise
   valid preconditions. Update only the row-decision paragraph in
   `docs/WORKFLOW.md`: the orchestrator sets causal Origin, accepted rows need
   canonical values, and an invalid row must be corrected before continuation,
   review, release or repair. No prompt, answer-format or template changes.

## Files and ownership

- `scripts/stage2.py`: the implement attempt adds and wires Origin validation at the four action boundaries.
- `tests/test_stage2.py`: the implement attempt updates orchestrator fixtures and adds refusal, preservation, brake and workflow assertions.
- `docs/WORKFLOW.md`: the implement attempt documents Origin ownership and correction in the existing row-decision paragraph.
- `plans/changes/origin-cell/spec.md`: the runner maintains implementation status against this contract.
- `plans/changes/origin-cell/plan.md`: the attempt replaces not-yet-written ledger entries as tests land; the runner records phase-4 time.
- `plans/changes/origin-cell/findings.md`: the runner retains audit, attempt and later review evidence without rewriting existing entries.
- `plans/INDEX.md`: the runner regenerates the derived registry; no hand edit.

No files are deleted. No held-path bootstrap edit is needed: prompts,
templates, ADRs, governance, endpoint declarations, settings, tracker data,
README and AGENTS remain untouched. Preserve `decisions.md`, `research.md`,
other changes and quoted reviewer evidence. No historical Origin migration.

## Verification

The implementation worktree first needs `make venv` and
`bash tools/pi/install.sh` once. Then run:

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change origin-cell
python3 scripts/check_research_handoff.py --change origin-cell
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

At baseline `ec375553` (2026-11-07), `templates/plan.md` and
`scripts/validate_change_artefacts.py` are absent. Use the phase-3 prompt's
card, file list and ledger, and the existing gates above; do not create those
missing files. The runner regenerates the index, runs full verification and
makes the commit; draft checks do not claim implementation evidence.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_origin_workflow_assigns_provenance_to_the_orchestrator — removing ownership or either causal meaning from the workflow passes
- 2: not yet written tests/test_stage2.py::test_invalid_accepted_origins_hold_all_consuming_verbs — a taken/fixed row at any authoritative location permits a call, write, deletion or consumption
- 2: not yet written tests/test_stage2.py::test_invalid_origin_holds_release_reconciliation — either already-released retry branch rewrites findings or removes the record before validation
- 3: not yet written tests/test_stage2.py::test_origin_refusal_identifies_rows_sources_and_correction — one offending ID, source, allowed value or orchestrator instruction is omitted
- 4: not yet written tests/test_stage2.py::test_valid_origins_preserve_existing_admission_checks — canonical values are refused or permit continuation without existing decision/test evidence
- 5: not yet written tests/test_stage2.py::test_nonaccepted_rows_need_no_origin — arbitrary Origin on rejected/open rows triggers the new refusal, or bypasses the old undecided-row refusal
- 6: not yet written tests/test_stage2.py::test_reviewer_origin_is_not_filled_automatically — initial intake changes arbitrary/blank Origin or the retained answer
- 7: not yet written tests/test_stage2.py::test_origin_survives_repair_and_release — fixed marking, ordinary release or release reconciliation overwrites valid Origin
- 8: tests/test_stage2.py::test_two_fix_r_rounds_stop_the_loop — accepted repair findings do not stop the next round, or an accepted base row fails to quiet this brake
- 8: not yet written tests/test_stage2.py::test_origin_brake_survives_released_history — releasing earlier rounds or changing taken to fixed resets the brake, or rejected arbitrary Origin counts as accepted

## Time used
