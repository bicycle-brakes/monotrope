---
title: "Plan — midnight-stamp-test"
status: draft
implementation_status: none
date: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3, 2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, tests, make-verify]
---

# Plan — midnight-stamp-test

```text
For you:     The tests around the runner's date stamps no longer fail when one
             verify run crosses local midnight; production stays untouched.
Done when:   All nine stamp tests compare against one date they set, the new
             guard test holds that pin, and make verify is green.
Appetite:    2 hours of phase 4 in total, repairs included — a stop, not an
             estimate.
Not now:     Production stamp changes, the review-audit seconds-window (a
             follow-up bead is proposed instead), any clock framework.
Pre-mortem:  suppose it failed: most likely because the subprocess stand-in
             still read its own clock and clashed with the pinned date.
Starts unless you say stop.
```

## Scope and prerequisites

Implements criteria 1-6 of `spec.md`. Baseline read: `9314f5b9`, 2026-11-11.
Class remains `bounded`; no design phase and no ADR are due (`adr_files: []`).
`findings.md` holds only stage-2 attempt records, no phase-2a rows. Phase 1
used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash`; `research.md` records no Explore fallback, so none is carried
here. No held path is edited: nothing under `prompts/`, `templates/`,
`.github/` or the other held prefixes changes with this fix.

## Build sequence

1. Add the pin helper next to `updated_of` (`tests/test_stage2.py:1729`):
   `pinned_stamp_date(monkeypatch, day)` returns a small holder and patches a
   `dt.date` subclass — overriding only `today()`, the
   `tests/test_stage2_terms_expiry.py:159-160` precedent — onto the shared
   `datetime` module via `monkeypatch.setattr(stage2.dt, "date", …)`, so the
   runner's stamp reads and the test's reads resolve one settable date. Add
   the `monkeypatch` argument to the fixed tests that lack it.
2. Fix the bead's test (criterion 1): pin a first day, run `spec-review`,
   assert that day's stamp; rewrite the header with the day just asserted;
   move the holder to a second day, run `review-loop`, assert; rewrite; move
   to a third day, run `review`, assert. The two rewrites replace the day
   currently in the header, which the original `f"updated: {today}"` replace
   silently missed once the day moved.
3. Fix the five in-process siblings (criterion 2) to pin one day each and
   assert against the pinned value: `verify_attempt` (`:1950`), `fill_marks`
   (`:5775`), `persist_time_entry` (`:11884`), the release reconcile
   (`:21256`) and the review-audit test (`:24736-24764`, whose `yesterday`
   becomes the pinned day minus one and whose `stage2.today()` reads the
   pinned day through the patch).
4. Fix `checking_derived_make` (criterion 3): take the pinned day as an
   argument and bake `"updated: <that day>"` into the planted stand-in script
   as a literal, dropping the subprocess's own `datetime.date.today()` read;
   the two tests using the helper pin their day before planting it.
5. Fix `tests/test_workflow_entry.py::test_new_change_creates_the_folder_and_a_current_index`
   (criterion 4): pin the day the same way through the shared module and
   assert the scaffold's `updated:` against that pinned value — the module's
   own `date` name is import-bound, so the test must not go through it.
6. Add the guard test (criterion 5): read `tests/test_stage2.py` and
   `tests/test_workflow_entry.py` as text, extract the nine named bodies and
   the helper from each `def` line to the next top-level `def`/`class`, and
   assert none of them contains `date.today(`. Name the nine functions and
   the helper in a list, so a rename updates the guard with it.
7. Run the verification below; once the guard test exists, drop the `not yet
   written` prefix from its ledger entry. Phase 4 records its time under
   `## Time used`; the header dates and `plans/INDEX.md` belong to the
   runner.

## Files and ownership

- `tests/test_stage2.py` — the pin helper, the guard test, and the seven
  fixed tests plus `checking_derived_make`.
- `tests/test_workflow_entry.py` — the one fixed test and its local pin
  lines.
- `plans/changes/midnight-stamp-test/spec.md` — implementation status moves
  with the code, criteria unchanged.
- `plans/changes/midnight-stamp-test/plan.md` — time and ledger progress.
- `plans/INDEX.md` — runner-owned regeneration; no session edits it.

No deletions. Not touched, where the obvious reading would include them:
everything under `scripts/` (criterion 6), `docs/`, `prompts/`, `templates/`,
`AGENTS.md`, `README.md`, other change folders, the tracker and every test
file except the two named ones.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'stamp or preparation or first_implement or each_retry or release_reconcile'
.venv/bin/python3 -m pytest tests/test_workflow_entry.py -q
python3 scripts/check_criterion_ledger.py
python3 scripts/check_interview_minimums.py --change midnight-stamp-test
python3 scripts/plans_registry.py --check
make verify
```

The first line also runs unrelated stamp tests in the same file; they stay
green. Full verification belongs to the runner.

## Criterion ledger

- 1: tests/test_stage2.py::test_every_write_to_findings_keeps_its_updated_stamp_current — the runner stamps a date other than the one current at that write, or the compared date stops following a mid-test move (the form that failed on 2026-11-09)
- 2: tests/test_stage2.py::test_preparation_stamps_only_changed_held_documents — verify_attempt stamps a date other than the one the test pinned
- 2: tests/test_stage2.py::test_filling_the_marks_keeps_the_updated_stamp_current — fill_marks leaves a stamp other than the one the test pinned
- 2: tests/test_stage2.py::test_runner_detaches_matching_hardlinked_plan_before_stamp — persist_time_entry stamps a date other than the one the test pinned
- 2: tests/test_stage2.py::test_the_release_reconcile_refreshes_the_findings_date — the release reconcile leaves a stamp other than the one the test pinned
- 2: tests/test_stage2.py::test_review_accepts_runner_audit_date_stamp — append or the review audit check accepts or writes a date other than the one the test pinned
- 3: tests/test_stage2.py::test_first_implement_refreshes_derived_files_without_a_model_repair — the make stand-in refuses the plan stamp because it expects a date other than the pinned one
- 3: tests/test_stage2.py::test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics — the make stand-in refuses the plan stamp because it expects a date other than the pinned one
- 4: tests/test_workflow_entry.py::test_new_change_creates_the_folder_and_a_current_index — the scaffold's updated date differs from the one the test pinned
- 5: tests/test_stage2.py::test_stamp_tests_pin_the_date_they_compare — a date.today( read reappears in one of the nine bodies or the helper and stays uncaught
- 6: not a test — the pull request's file list shows no path under scripts/

## Time used

2026-11-11 12:26:41–13:20:04 UTC, 3203 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
