---
title: "Findings — stage2-runs-count"
category: findings
status: draft
implementation_status: none
date: 2026-10-08
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-09
supersedes: null
superseded_by: null
bead: coding-harness-kw0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — stage2-runs-count

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 310 files, 711 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 311 files, 714 commits, 12 rules.

Stage-2 call, 2026-10-09: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 311 files, 715 commits, 12 rules.

## Phase 6 — Codex, 2026-10-09

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `scripts/stage2_runs.py:125–131` | A nine-cell findings row under `## Follow-up verification` marked `Broke a test=yes` produces a count of 0 instead of 1. Tables of other widths are also skipped despite having that column. Test-break counting must include every table independently of phase and loop classification. [AC 4] | Codex | closed — test_a_yes_counts_in_every_table_that_has_the_column; red under its planted fault | no |
| F-2 | BLOCKER | SPEC | base | `scripts/stage2_runs.py:48,134–136` | A clean call followed by `Stage-2 call, 2026-10-09:review · leak check BLOCK.` reports clean/total as 1/1 instead of 1/2. The regex drops the second record because the colon lacks a following space, although it starts with the required prefix. Such records must remain in the denominator. [AC 7] | Codex | closed — test_a_call_line_not_in_the_runners_form_stays_in_the_count; red under its planted fault | no |
| F-3 | BLOCKER | SPEC | base | `scripts/stage2_runs.py:155–179` | `--rev HEAD` resolves HEAD for the label but reuses the mutable reference for subsequent reads. Simulating HEAD advancing from `cc020f5` to `df69d58` produced a row labelled `cc020f5` for `stage2-runs-count`, whose findings file does not exist at that commit. The label and every read must use one resolved commit. [AC 8] | Codex | closed — test_rev_resolves_its_commit_once; red under its planted fault | no |
| F-4 | BLOCKER | MAINT | base | `scripts/stage2_runs.py:242,289–292`; `scripts/stage2.py:441` | With `model-endpoints.yaml` containing `endpunkte: 42`, declaration checking raises an uncaught `TypeError`; a nonempty sequence at the document root raises `AttributeError`. The counter consequently terminates with a traceback. Invalid declaration structures must produce a controlled diagnostic rather than escape the CLI’s error handling. | Codex | closed — test_a_declaration_of_the_wrong_shape_is_reported_not_raised; red under its planted fault | no |

Phase 6 verdict: codex 01a11d92-1deb-7832-a399-7fb4224bad2c, 2026-10-09
Reviewer session: codex 01a11d92-1deb-7832-a399-7fb4224bad2c — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — GLM loop rows, released 2026-10-09

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MINOR | SPEC | base | `scripts/stage2_runs.py:208` | The first acceptance criterion of the change's own spec promises the change folder in the table row's second cell; `row()` prints the folder inside the first cell beside the change name and puts the measured commit in the second, and the research note's pasted output shows the same — the criterion, as written, is not met by the output the change itself carries. | GLM | taken — spec criterion 1 now says the first cell names the folder; test_an_active_and_an_archived_change_are_both_found asserts it | no | agree |
| L1-2 | MINOR | SPEC | base | `scripts/stage2_runs.py:104` | The column "Taken that broke a test" and the criterion line "taken rows that broke a test" count a `yes` in that cell on every row of every table regardless of the row's Status, so a rejected or never-actioned row carrying `yes` raises both numbers under a label that says taken — the counting and the wording disagree, and the printed governance numbers can overstate what the label claims. | GLM | taken — label and criterion-1 line say rows marked Broke a test yes (any status); spec criteria 4 and 9 reworded; test asserts the line | no | agree |
| L1-3 | MINOR | SPEC | base | `docs/WORKFLOW.md:836` | The typed criteria table in the workflow section reports the measured-runs number for the earliest runs only, at a cut-off commit where another finished run's folder already exists and is counted by the same command in the note's addendum; a reader of the section alone gets a lower number than the named commit supports, and nothing in the section says the further run was measured. | GLM | rejected — WORKFLOW section 4 measures the first three runs by its own rule and says so; the fourth run is counted in the note's addendum, which the section names |  | disagree — WORKFLOW explicitly scopes its table to the first three runs; the four-run addendum has a different stated scope. |
| L1-4 | MINOR | SPEC | base | `plans/changes/stage2-runs-count/plan.md:22` | The plan's "Done when" promises a planted-fault test for each criterion, but the criterion guarding the research note against edits above the addendum has no test at all — it is held by a hand-run git diff, as the time log itself records — so the change's stated completion bar and its delivered verification differ in its own words. | GLM | taken — plan card Done when: criteria 1–9 tests, criterion 10 a git diff | no | agree |
| L1-5 | MINOR | MAINT | base | `scripts/stage2_runs.py:162` | The `--rev` read path decodes `git show` output with the subprocess locale (`text=True`, no `encoding=`), while the working-tree path reads UTF-8 explicitly, so under a non-UTF-8 locale the two modes disagree on the same file: non-ASCII text (this repository's prose carries umlauts) garbles or raises only when `--rev` is used. | GLM | taken — test_rev_decodes_git_output_as_utf_8_whatever_the_locale (red without encoding=utf-8) | no | agree |
| L1-6 | MINOR | MAINT | base | `scripts/stage2_runs.py:113` | The counter reaches into the runner's private `_furniture` helper to reject table header and rule lines — a name the plan's sanctioned import list does not include — so a refactor of the runner's internals silently changes which lines get counted, with no public contract marking the dependency. | GLM | rejected — reusing the runner's own furniture rule is the point (the task and plan: reuse the runner's parsing, do not re-parse); a refactor of it changes what the runner treats as furniture too, and the tests render tables with the runner's own render_table |  | disagree — No incorrect count or forbidden import is demonstrated; private naming and hypothetical refactors alone are not correctness findings. |
| L2-1 | MINOR | MAINT | code | `scripts/stage2_runs.py:171-176` (`Source.children`) | The `--rev` branch of `Source.children` splits `git ls-tree` output on whitespace, while the working-tree branch of the same method lists real directory names: an archived folder whose name contains a space is broken into tokens that can never satisfy the archive match, so the same folder is found without `--rev` and reported as missing with it, and the error message names no path a person could check against the archive. | GLM | taken — test_rev_lists_an_archived_folder_name_whole (ls-tree -z; red when split on blanks) | no | disagree — Archive names containing spaces fail the required exact pattern in both modes; whitespace splitting caused false matches or ambiguity, not the claimed valid-folder disappearance. |
| L2-2 | MINOR | MAINT | code | `scripts/stage2_runs.py:164-167`, `:278-288` | The tool's contract promises a clean exit for a change not found, but `Source.read` decodes the working-tree `findings.md` with no guard: one invalid byte in that file raises an uncaught decoding error and a traceback instead of the stated exit paths, although the runner whose output this script reads catches exactly that error wherever it reads the same kind of file. | GLM | taken — test_a_findings_file_that_is_not_utf_8_exits_2_without_a_traceback, both modes | no | agree |
| L2-3 | MINOR | MAINT | doc | `plans/changes/stage2-runs-count/plan.md:56-62` | The plan's time log stops at the session that wrote the script and names a count of tests one lower than the suite the tree ships, with no measured span for the review-loop repair round that added the extra test; a maintainer resuming from the plan counts a different suite than the log claims and hunts for an account of the repair that does not exist. | GLM | taken — plan time log records the loop rounds, the repairs and twelve tests | no | agree |

Rounds run: 2

Stage-2 call, 2026-10-09: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 311 files, 715 commits, 12 rules.

Stage-2 call, 2026-10-09: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 311 files, 716 commits, 12 rules.

## Phase 6 — Codex, 2026-10-09

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-5 | BLOCKER | SPEC | base | `scripts/stage2_runs.py:117–127` | A table with columns `Finding`, `Broke a test` and row `X-1`, `yes` still reports 0 instead of 1. Headers are recognized only when their first cell is `ID`; the new regression test uses only such headers. This supplies a failing case beyond those repaired for F-1. [AC 4] | Codex | closed — test_a_header_is_the_line_above_the_separator_and_ends_with_its_table; red under its planted fault | no |
| F-6 | BLOCKER | SPEC | fix-r3 | `scripts/stage2_runs.py:110–125` | A table headed `ID, Broke a test` with a `no` row, followed immediately by `## Availability` and a table headed `Name, Available` with row `example, yes`, reports one broken-test row instead of zero. The heading preserves the previous header, so the unrelated availability value is counted. Before this repair the same input returned zero. [AC 4] | Codex | closed — test_a_header_is_the_line_above_the_separator_and_ends_with_its_table; red under its planted fault | no |

Phase 6 verdict: codex 01a11d92-1deb-7832-a399-7fb4224bad2c, 2026-10-09
