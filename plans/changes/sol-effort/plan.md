---
title: "Plan — sol-effort"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-yzk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, codex, effort]
---

# Plan — sol-effort

```text
For you:     Change Sol's effort once per verb; draft and review start at high, repair at medium.
Done when:   Launch arguments follow the central settings, instructions reference them, and make verify is green.
Appetite:    One hour for phase 4 including repairs; stop at the limit.
Not now:     ADR amendments, quota measurements, model or fallback changes, interactive effort defaults.
Pre-mortem:  suppose it failed: most likely because a retry inherits the other verb's effort.
Starts unless you say stop.
```

## Prerequisites

The existing class remains `bounded`: no phase-2b design or ADR draft is due.
The maintainer's Q-3 splits ADR amendments off; Q-4 to Q-6 settle the other
phase-2a rows, now marked `in spec`. The orchestrator reads the revised
artifacts and shows the card unchanged before phase 4. This call drafts only;
the runner owns `make verify` and the single commit. Use `make venv` once
when preparing a worktree for implementation verification.

## Build sequence

1. In `scripts/stage2.py`, declare `CODEX_EFFORTS = {"draft": "high",
   "repair": "medium", "review": "high"}` once. Keep the `CODEX` endpoint
   identity but set its effort slot to `None`, removing the shared default.
   Add a required keyword-only `verb` to `run_codex`; it reads
   `CODEX_EFFORTS[verb]` when forming argv. Draft passes `draft`;
   `run_attempts` passes its existing caller verb for both repair attempts;
   review's verdict and loop-marks calls both pass `review`. Keep endpoint
   equality, retry labels, session selection, sandboxes and audit formats.
2. Replace independent Sol effort literals throughout the active workflow
   tables and prose and the four Model paragraphs with links to the matching
   entry, e.g. `[CODEX_EFFORTS["draft"]](../scripts/stage2.py)` as written
   in `docs/WORKFLOW.md` and the four prompts: from each edited document the
   link target is `../scripts/stage2.py`.
   Include the section-3 Opus rows' Codex clauses, the section-4 repair row,
   and "The draft (phases 2, 2b and 3)"; add a note that the ADR effort text
   awaits its separately agreed amendments. Other models keep their values.
3. Extend the existing argv tests in the ledger using the central entry as
   their expectation; adapt `run_codex` stand-ins to the required keyword.
   Add a parameterized test that substitutes distinct supported efforts,
   runs draft and repair through a retry and review through resume/re-check
   and loop marks, and checks captured argv against the substituted entries.
   This catches ignored settings and crossed verbs without repeating the
   operational defaults in tests; phase 6 checks the shipped defaults.
4. Add doctrine checks for correct links and keys in every active Sol effort
   clause. Change `routing_problems` to check Sol's reference per verb,
   retaining Opus and ladder checks; inspect the repair row separately because
   `routing_rows` currently recognizes only numeric phase labels. Update the
   existing mutation needles so each replacement still matches the real text.
   Plant a missing link, wrong key and independent Sol literal at every
   location, including prose. Accept valid mixed-model clauses, and reject a
   wrong Sol reference even beside a correct non-Sol effort. Update ledger
   markers when tests exist and record measured phase-4 time before verification.

## Files

- `scripts/stage2.py`: add the central mapping and select it by caller verb at all four Codex call sites.
- `tests/test_stage2.py`: extend launch/routing tests and add the three tests marked not yet written in the ledger.
- `docs/WORKFLOW.md`: reference the central keys throughout active Sol effort instructions and identify the deferred ADR amendments.
- `prompts/02-spec.md`: point the Model paragraph to the central `draft` entry.
- `prompts/02b-design.md`: point the Model paragraph to the central `draft` entry.
- `prompts/03-plan.md`: point the Model paragraph to the central `draft` entry.
- `prompts/06-review.md`: point the Model paragraph to the central `review` entry.
- `plans/changes/sol-effort/spec.md`: carry the revised contract and later the implementation status.
- `plans/changes/sol-effort/plan.md`: carry this plan, update ledger markers and record measured time.
- `plans/changes/sol-effort/research.md`: append dated repository evidence without rewriting the earlier observations.
- `plans/changes/sol-effort/findings.md`: resolve the four phase-2a statuses; the runner adds later audit and review evidence.
- `plans/INDEX.md`: the runner regenerates this derived file; do not hand-edit it.

No creations or deletions are planned. Do not touch `scripts/stage2_session.py`,
`scripts/stage2_runs.py`, `model-endpoints.yaml`, `AGENTS.md`, permissions,
gates, provenance, decision answers, any ADR or another change folder.
Preserve this change's six interview answers. Research records no Stage-1
Explore route to carry forward.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py tests/test_stage2_runs.py tests/test_model_endpoints.py tests/test_stage2_session.py -q
python3 scripts/check_interview_minimums.py --change sol-effort
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

The requested `python3 scripts/validate_change_artefacts.py --check` cannot
measure: that file is absent. A plan template is also absent; this plan uses
the phase-3 prompt's form. Neither missing file is created by this change.
Use the existing gates and runner checks. Keep historical test names used by
older ledgers, including `test_repair_uses_codex_at_max_effort`; its updated
assertion follows the repair setting without editing the earlier artifacts.

## Criterion ledger

- 1: tests/test_stage2.py::test_a_draft_starts_codex_with_workspace_write_and_no_bypass — extend to read the draft entry; argv omits or overrides it
- 1: tests/test_stage2.py::test_a_failed_first_draft_gets_one_codex_repair_with_its_diagnostics — extend both argv checks; the retry selects repair's entry
- 1: not a test — phase 6 compares the shipped central draft default with criterion 1; a default other than high refutes it
- 2: tests/test_stage2.py::test_repair_uses_codex_at_max_effort — preserve the name and read the repair entry; the call selects the shared or another verb's effort
- 2: tests/test_stage2.py::test_repair_retry_uses_fresh_codex_with_diagnostics — extend both argv checks; the retry loses the repair setting
- 2: not a test — phase 6 compares the shipped central repair default with criterion 2; a default other than medium refutes it
- 3: tests/test_stage2.py::test_codex_is_pinned_on_first_and_resumed_calls — read the review entry; a historical resume or loop-marks argv omits or overrides it
- 3: tests/test_stage2.py::test_a_fresh_phase_6_session_says_so — extend argv checks; the fresh verdict is unpinned
- 3: tests/test_stage2.py::test_phase6_after_codex_repair_starts_a_fresh_read_only_session — extend argv checks; the re-check inherits repair's setting
- 3: tests/test_stage2.py::test_a_phase6_rerun_without_repair_records_the_actual_recheck_reason — extend argv checks; a repeated review selects the wrong entry
- 3: tests/test_stage2.py::test_the_loop_marks_after_a_recheck_resume_the_fresh_verdict_thread — extend both argv checks; resumed marks lose the review entry
- 3: not a test — phase 6 compares the shipped central review default with criterion 3; a default other than high refutes it, while live thread internals remain unproven under Q-6
- 4: tests/test_stage2.py::test_sol_instructions_reference_the_central_effort_for_each_verb — a missing or wrong reference or independent Sol literal survives in a table, Model paragraph or drafting prose
- 5: tests/test_stage2.py::test_sol_effort_changes_propagate_without_other_edits — distinct planted settings fail to reach any initial, retry or resumed argv
- 6: tests/test_stage2.py::test_sol_effort_checks_allow_other_models_in_the_same_instruction — a valid mixed-model instruction is rejected, or another model's effort masks a wrong Sol reference
- 7: tests/test_stage2_session.py::test_codex_is_dispatched_interactively_with_its_exact_safety_flags — an added interactive effort override changes the exact argv

## Runner handoff — 2026-10-14

This redraft starts at `9943b8f` on `feat/sol-effort`, tracking
`origin/feat/sol-effort-r2`; only the runner's findings audit was dirty.
The recorded PR is #143 (Q-3); its live state was not read because GitHub
could not be reached. No tracker write or git mutation belongs to this call.
The outer session owns tracker changes and the journal handover.

Resume: the runner verifies and commits this redraft; the orchestrator reads
it, shows the card unchanged and starts phase 4 within the one-hour appetite.
Redraft checks, 2026-10-14, before the runner's post-check:

- Interview minimums, criterion ledger, frontmatter freshness and
  `git diff --check`: exit 0; local artifact structure checks also pass.
- `python3 scripts/validate_change_artefacts.py --check`: exit 2, file absent;
  no substitute validator was added.
- `python3 scripts/plans_registry.py --check`: not run, because the unset
  `BEAD_RENDER` would make it read the shared tracker outside this worktree.
  Local frontmatter checks passed; these do not assert tracker or index state.
- `make verify`, derived index regeneration and the commit remain with the
  runner. No implementation test or live model call was started here.

## Time used

2026-10-14, phase-4 implementation session (stage-2 `implement`, route flash):
start, end and span unreadable — this session runs without a command tool, so
`date` could not be read and no time was estimated; the runner's audit line in
`findings.md` dates the session. The one-hour appetite is measured by the
orchestrator's readings, not by this record.

2026-10-15 00:36:27–00:42:13 +0200, 5m 46s — measured repair session
for L1-1. Only the doctrine test helpers and their planted faults changed;
no production logic moved. The current targeted doctrine run passed all 15
cases; criterion-ledger and `git diff --check` passed. The full test-file run
loaded an intermediate version before the prompt mutation was corrected:
511 passed, one failed; the corrected case and the other 14 doctrine cases
passed again afterwards. Running the new mutation against the baseline's
doctrine helpers refuted them on the added independent Sol prose sentence.
The runner owns the final `make verify`, checkpoint commit and handover;
this repair made no git or tracker writes.
