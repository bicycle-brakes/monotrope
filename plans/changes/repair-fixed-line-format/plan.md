---
title: "Plan — repair-fixed-line-format"
status: draft
implementation_status: partial
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-hgvp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, repair]
---

# Plan — repair-fixed-line-format

```text
For you:     Explanations no longer spoil an unambiguous repair answer, and each attempt's protected answer stays readable.
Done when:   Parser and answer-evidence regressions pass, conflicting fixes remain errors, and make verify is green.
Appetite:    One hour of phase 4 including repairs; stop at the limit.
Not now:     New statuses, model routes, retry rules, historical answer recovery or remote evidence storage.
Pre-mortem:  suppose it failed: most likely because the answer is saved only after a check that can already stop the attempt.
Starts unless you say stop.
```

## Scope and prerequisites

Implement criteria 1–9 of `spec.md`; the class remains bounded, so no design
or ADR is due. Research records no Stage-1 Explore fallback to carry forward;
the rejected Sonnet repairs are incident evidence, not this change's Explore
route. The orchestrator shows this card unchanged; this draft implements no
code and makes no commit. Keep the existing findings audit line.

## Build sequence

1. In `check_repair_answer`, retain current line collection and unknown-id
   handling. For each taken id, select right sides starting `fixed — ` and
   deduplicate their normalized text in encounter order before validation.
   One selected claim goes through `fixed_status`; several distinct claims
   fail and quote their lines. With no selected claim, preserve existing
   missing/malformed diagnostics rather than accepting explanations. Retain
   code-row, test-definition, findings-integrity and red-first checks.
2. Add repair-only answer evidence at the model-return boundary in
   `run_attempts`, before HEAD checks, verification or answer checking can
   stop the run. Preserve available output on `CallFailed` as well, passing
   it through from `run_codex`/`run_work_model` where currently discarded;
   keep failure classification and retry behavior unchanged. Write the full
   `protect_diagnostics`-protected answer using the run's credential context,
   including keyless routes. Use an exclusively created UTF-8 file below
   Git's resolved per-worktree `stage2/attempts/<change>/` evidence directory,
   with a unique invocation token and attempt number; validate the destination
   against aliases and never overwrite an earlier file. This is local
   evidence, like `refs/stage2/attempts/`, with no branch push or tracked path.
   Record an explicit empty/unavailable-output note when appropriate. Saving
   or protection failures fail closed with safe diagnostics and no checkpoint.
3. Carry the answer locator into failure diagnostics, including call/verify
   failures that bypass the parser, and expose it on success. Quote distinct
   conflicting claims with the id and protected locator; keep the locator at
   the end of the existing bounded diagnostic listing so tailing retains it.
   The file holds the full answer even when displayed diagnostics are cut;
   never append the full answer to `findings.md`. Preserve current attempt refs,
   restoration, time logging and findings ownership.
4. Reuse local `World`, `repair_world`, `script_repair` and captured calls in
   the existing repair suite. Cover loop and free-text ids, both fixed-status
   forms, explanation order, malformed competing claims and repeated claims.
   Revise the identical-duplicate expectations in the two existing tests named
   below to use distinct conflicts, retaining their names for older ledgers.
   Exercise evidence before answer checks and on green/red verification,
   transport failure, empty output, moved HEAD, retry, restore and a second
   invocation; use distinctive long output to detect truncation or overwrite.
   Cover Codex and Stage-1 Sonnet with stand-ins and denylist fixtures, plus a
   failed/unsafe evidence destination; no live model calls or credential reads.

## Files

- `scripts/stage2.py`: implement claim selection, protected repair answer retention and locators; align `REPAIR_ANSWER`.
- `tests/test_stage2.py`: add the ledger regressions, revise duplicate fixtures and extend instruction assertions without renaming existing tests.
- `docs/WORKFLOW.md`: update only “Repairing taken findings” with filtering, repetition and local evidence retrieval.
- `plans/changes/repair-fixed-line-format/spec.md`: hold the contract and later its implementation status.
- `plans/changes/repair-fixed-line-format/plan.md`: replace ledger markers as tests land and record measured phase-4 time.
- `plans/changes/repair-fixed-line-format/research.md`: retain the dated draft gap checks added in this phase.
- `plans/changes/repair-fixed-line-format/findings.md`: the runner retains audit, attempt and review evidence.
- `plans/INDEX.md`: the runner refreshes the derived registry; no hand edit.

No deletions. Do not touch other change folders, ADRs, tracker data, endpoint
settings, permissions, gates or other phase prompts; shared transport changes
only preserve repair output and leave other verbs' behavior unchanged.

## Verification

For phase 4, prepare the worktree once with `make venv` and
`bash tools/pi/install.sh`, then run:

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change repair-fixed-line-format
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

At draft baseline `089b13af` (2026-10-26), neither `templates/plan.md` nor
`scripts/validate_change_artefacts.py` exists. Use the phase-3 prompt's form
and the existing gates above; do not create those missing files here.
The runner refreshes the index and performs full verification and the commit.

## Criterion ledger

- 1: tests/test_stage2.py::test_repair_ignores_explanations_for_a_taken_id — prose beside the unique valid claim rejects the answer
- 2: tests/test_stage2.py::test_repair_deduplicates_identical_fixed_claims — identical normalized claims trigger a retry
- 3: tests/test_stage2.py::test_repair_rejects_distinct_fixed_claims — a valid claim hides a second distinct or malformed claim
- 3: tests/test_stage2.py::test_each_taken_row_needs_exactly_one_fixed_line — missing, distinct conflicting or unknown lines pass; revise identical-duplicate fixture
- 4: tests/test_stage2.py::test_repair_prose_alone_still_needs_fixed_lines — prose alone passes; revise repeated-claim fixture to a distinct conflict
- 4: tests/test_stage2.py::test_repair_rejects_malformed_known_fixed_lines — malformed status or empty reason is accepted
- 4: tests/test_stage2.py::test_a_fixed_line_naming_an_undefined_test_fails_the_attempt — undefined test accepted
- 4: tests/test_stage2.py::test_a_code_row_answered_not_a_test_fails_the_attempt — code repair bypasses red-first proof
- 5: tests/test_stage2.py::test_repair_rejects_unknown_finding_shaped_identifiers — an unknown established-prefix id is ignored
- 5: tests/test_stage2.py::test_repair_rejects_unknown_loop_id_without_loop_rows — an unknown loop claim is ignored
- 5: tests/test_stage2.py::test_repair_rejects_unknown_claimed_fixes — an unknown free-text fix is ignored
- 6: tests/test_stage2.py::test_repair_retains_each_attempt_answer — success, early failure, retry, restore or another invocation loses or overwrites full available output
- 7: tests/test_stage2.py::test_repair_conflict_diagnostics_quote_claims_and_answer_location — the failure omits a conflicting claim or a retrievable protected answer locator
- 8: tests/test_stage2.py::test_repair_answer_evidence_is_protected_on_every_route — stored output or quotes expose a denylist secret or credential fragment
- 8: tests/test_stage2.py::test_repair_answer_evidence_failure_stops_safely — protection failure or an unsafe/unwritable destination causes a raw write or successful checkpoint
- 9: tests/test_stage2.py::test_repair_instructions_describe_answer_filtering_and_hand_repairs — extend assertions for unique claims, repetition, conflicts and evidence retrieval in prompt and workflow

## Time used

2026-10-26 20:01:28–20:46:57 UTC, 2729 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-26 20:47:02–21:01:23 UTC, 861 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
2026-10-26 21:58:29–22:19:07 UTC, 1238 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-26 22:19:12–22:34:47 UTC, 934 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
