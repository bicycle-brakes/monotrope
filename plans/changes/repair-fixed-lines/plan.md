---
title: "Plan — repair-fixed-lines"
status: draft
implementation_status: partial
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-ugi
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, repair]
---

# Plan — repair-fixed-lines

```text
For you:     Repair accepts incidental answer prose and stops before a model call when an old taken status already names a fix.
Done when:   Parser and completed-row regressions pass, instructions agree, and make verify is green.
Appetite:    One hour of phase 4 including repairs; stop at the limit.
Not now:     Historical findings migration, new statuses, model routes, retry or red-first rule changes.
Pre-mortem:  suppose it failed: most likely because filtering by identifier shape discards a real phase-6 identifier.
Starts unless you say stop.
```

## Scope and prerequisites

Implement criteria 1–9 of `spec.md`, preserving the bounded class and the
three details in `decisions.md`. No design or ADR is due. Phase 1 used route
`flash`, endpoint `glm-coding-plan`, model `glm-5.3-flash`, on 2026-10-15;
no Stage-1 fallback was recorded. This draft writes artifacts only; the
orchestrator shows this card unchanged before phase 4, and the runner owns
verification and the commit.

## Build sequence

1. In `check_repair_answer`, construct the set of active row identifiers.
   Retain current line trimming, leading-list-marker removal and identifier
   decoration stripping. Ignore lines without a colon; for colon lines,
   collect exact active identifiers first. Collect unknown identifiers only
   when a full match of `L\d+-\d+` holds, or `[A-Za-z]+-[0-9]+` holds
   and its prefix occurs in the change's row ids (including rejected and fixed
   rows); ignore the rest. Leave missing, duplicate, unknown and malformed-status diagnostics,
   findings integrity checks and red-first execution in their existing order.
2. After `repair_targets` returns and before any attempt starts in `repair`,
   inspect every selected row's Status for the case-insensitive patterns
   `; fixed by`, `; fixed:` and `; repaired by`. Refuse with the affected
   identifiers and the instructions to replace Status with `fixed — tests/<path>::<function>`
   or `fixed — not a test — <reason>` and set the loop row's test mark.
   Do not rewrite or silently skip legacy rows. Keep canonical fixed-row
   selection and the undecided/duplicate refusals intact.
3. Update `REPAIR_ANSWER` to state which lines count and that unknown
   finding-shaped identifiers still fail; remove its conflicting prohibition
   of all other text. State the canonical hand-repair rule and early refusal.
   Update only the repair subsection of the workflow with the same rules and
   the hand writer's responsibility for `Broke a test`.
4. In the existing repair-test section, reuse `repair_world`, `script_repair`,
   row builders and captured calls. Add the tests named below, parameterizing
   row location, status form and answer variant. Mixed-prose successes assert
   one attempt and one checkpoint; failure cases inspect diagnostics and
   exclude a premature checkpoint. Legacy-status tests assert no model or
   make calls, unchanged rows, and a refusal naming each affected identifier
   and both corrective forms. Include normal taken reasons without a marker
   as controls. Keep all existing ledger-referenced test names.

## Files

- `scripts/stage2.py`: change answer filtering, add pre-call legacy-status refusal and align the shared answer prompt.
- `tests/test_stage2.py`: add parser, completed-row, legacy-status and instruction regression tests.
- `docs/WORKFLOW.md`: clarify answer filtering and canonical hand-repair bookkeeping in the repair subsection.
- `plans/changes/repair-fixed-lines/spec.md`: hold the contract and later the implementation status.
- `plans/changes/repair-fixed-lines/plan.md`: update ledger markers when tests exist and record measured phase-4 time.
- `plans/changes/repair-fixed-lines/research.md`: append the dated local gap checks supporting this draft.
- `plans/changes/repair-fixed-lines/findings.md`: retain the existing draft audit line; the runner adds review and attempt evidence.
- `plans/INDEX.md`: the runner refreshes this derived registry; do not hand-edit it.

No implementation-time deletions or new modules are planned. Do not touch
other change folders, ADRs, other prompts, `AGENTS.md`, tracker
data, endpoint settings, permissions or gates. `prompts/04-implement.md`
already describes fixed lines without forbidding incidental text.

The accepted loop-round-1 repairs also update implementation metadata in this
change's artifacts, including `decisions.md`, and regenerate the index. The
runner retains ownership of the finding rows in `findings.md`; only the
explicitly requested frontmatter implementation status changes in this repair.

## Verification

Prepare the implementation worktree with `make venv` once, then run:

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change repair-fixed-lines
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

The requested `python3 scripts/validate_change_artefacts.py --check` cannot
run: that file is absent at draft baseline `b3e5810`. There is also no plan
template under `templates/`; use the phase-3 prompt's required form here.
Do not create either missing file in this fix. The runner performs the full
checks; this draft's local checks stay inside the worktree and git directory.

## Criterion ledger

- 1: tests/test_stage2.py::test_repair_ignores_incidental_answer_prose — headings, fences or report labels trigger a retry after valid fixed lines
- 1: tests/test_stage2.py::test_repair_ignores_l_prefix_prose_without_loop_rows — L-3 report prose fails when only phase-6 rows exist
- 2: tests/test_stage2.py::test_repair_accepts_exact_free_text_identifiers — a custom or report-like phase-6 identifier is filtered out
- 3: tests/test_stage2.py::test_repair_rejects_unknown_finding_shaped_identifiers — an unknown loop or letters-hyphen-digits identifier is ignored
- 3: tests/test_stage2.py::test_repair_rejects_unknown_claimed_fixes — a claimed fix with an unknown free-text identifier checkpoints
- 4: tests/test_stage2.py::test_each_taken_row_needs_exactly_one_fixed_line — a missing or doubled fixed line passes
- 4: tests/test_stage2.py::test_repair_prose_alone_still_needs_fixed_lines — prose alone passes or duplicates separated by prose escape detection
- 5: tests/test_stage2.py::test_repair_rejects_malformed_known_fixed_lines — a known identifier with an invalid status or empty reason is treated as prose
- 6: tests/test_stage2.py::test_repair_lists_every_taken_row_and_no_rejected_or_fixed_one — a completed released or phase-6 row is sent again
- 6: tests/test_stage2.py::test_repair_skips_canonical_hand_repairs_in_every_location — either canonical status is demanded again in any location, including fixed-only batches
- 7: tests/test_stage2.py::test_repair_refuses_legacy_completed_taken_statuses_before_call — a marker starts an attempt, rewrites a row or lacks corrective diagnostics
- 8: tests/test_stage2.py::test_a_fixed_line_naming_an_undefined_test_fails_the_attempt — an undefined test is accepted
- 8: tests/test_stage2.py::test_a_fixed_line_whose_test_path_climbs_out_of_tests_fails_the_attempt — an escaping test path is accepted
- 8: tests/test_stage2.py::test_a_code_row_answered_not_a_test_fails_the_attempt — a code row bypasses the required test
- 8: tests/test_stage2.py::test_a_named_test_that_is_not_red_first_fails_the_attempt — a baseline-green test is accepted as evidence
- 9: tests/test_stage2.py::test_repair_instructions_describe_answer_filtering_and_hand_repairs — prompt and workflow omit or contradict the filtering or hand-repair rule

## Time used

2026-10-16 — both phase-4 sessions so far (attempt 1, route flash, and this
repair session) ran under the Stage-2 runner with file tools and no command
tool: `date` could not be read, so no start, end or span is claimed and none
is estimated. The runner's clock measures both against the one-hour appetite;
its audit lines in `findings.md` carry each attempt's day and order.

2026-10-16 01:00:03–01:11:23 +0200, 11m 20s — Codex repair of loop-round-1 rows L1-1, L1-2 and L1-3; no break. Start and end read from `date`; earlier unmeasured spans above remain unestimated.

Verification at repair baseline `8542e0611118cec8ab95c01c732353de6630416e` plus this working diff, 2026-10-16:

- Red first, before the code repair: the two named regression functions produced three failing cases and two passing controls. After the repair all five cases passed.
- `.venv/bin/python3 -m pytest tests/test_stage2.py -q`: 530 passed. Ruff check and format check, interview minimums, criterion ledger, metadata assertions and `git diff --check` passed. All five implementation-status fields read `partial`; the index was regenerated.
- `make verify`: exit 2, not green. Its main pytest run reported 14 failed, 2086 passed, 17 skipped and 15 errors. Failures include unavailable tracker access, forbidden local-server binds and signing failures in temporary fixture repositories. The kit probe also failed on fixture commits; the live ruleset check could not reach GitHub. The separate registry check could not measure tracker state. These are verification limits, not accepted passing evidence; no out-of-scope repairs or permission changes were made.
- The findings body and all finding statuses remain unchanged; only its explicitly requested implementation-status metadata was updated. No repository commit was made; the runner owns status booking, full verification and the checkpoint.

Verification evidence added on 2026-10-16 for the loop-round-1 runner
checkpoint `cc424575f866593e7110e765053471a2ae6bdfd7`:

- The runner's repair checkpoint `cc42457` records a green `make verify`.
  This is the accepted full-verification evidence for the Definition of Done,
  alongside the sandboxed red run above. The checkpoint exists only after
  all post-run checks pass: `scripts/stage2.py` calls `checkpoint` in the
  `if not problems` branch, after `make verify` has returned successfully.
  Its commit subject records the repair of L1-1, L1-2 and L1-3; its body
  records that runner formatting changed no file. The earlier sandboxed
  failure remains a measured limit of that local run.

2026-10-16 02:11:43–02:17:15 +0200, 5m 32s — Codex repair of loop-round-2 rows L2-1, L2-3 and L2-4; no break. Start and end read from `date`; earlier unmeasured spans remain unestimated.

- Red first at baseline `9f494ef`: the extended unknown-identifier regression failed for `L-3` (1 failed, 2 passed); after the parser repair all three cases passed.
- `.venv/bin/python3 -m pytest tests/test_stage2.py -q`: 531 passed in 283.83s (0:04:43).
- Ruff check, Ruff format check, criterion ledger and `git diff --check` passed. Markdownlint reports no diagnostic on the rewrapped workflow lines; existing diagnostics elsewhere remain.
- The runner checkpoint evidence is recorded above alongside the earlier sandboxed red run. This session did not run `make verify` or commit; the runner owns the full verification, row statuses and checkpoint. `findings.md` was not edited by this repair.

2026-10-16 02:48:19–02:55:26 +0200, 7m 7s — Codex repair of loop-round-3 rows L3-1 (unknown claimed fixes), L3-2 (legacy-marker instruction coverage) and L3-3 (conditional loop prefix); no break. Start and end read from `date`; earlier unmeasured spans remain unestimated.

- Red first at baseline `599853e`: the new unknown-claimed-fix test failed in all three cases, and the phase-6-only L-prefix prose regression failed. After the repair the targeted selection passed all eight cases.
- The instruction regression fails against the baseline shared answer prompt because it lacks the claimed-fix rule. Removing `; repaired by` from either the repaired shared prompt or the workflow independently also makes the regression fail; the unmutated instructions pass.
- `.venv/bin/python3 -m pytest tests/test_stage2.py -q`: 535 passed in 288.19s. Ruff check, Ruff format check, criterion ledger and `git diff --check` passed. The ledger now names both new regression functions.
- No `make verify` or repository commit was run by this repair session; the runner owns full verification, finding-status booking and the checkpoint. The pre-existing `findings.md` changes were not edited.
