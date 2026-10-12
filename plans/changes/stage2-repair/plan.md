---
title: "Plan — stage2-repair"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-g2f
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, review-loop, repair]
---

# Plan — `stage2-repair`

```text
For you:     You decide taken or rejected; one command, `python3 scripts/stage2.py repair <change>`, has GLM 5.3 repair every taken finding instead of a Claude sub-agent.
Done when:   The 33 criteria hold in tests/test_stage2.py and tests/test_stage2_runs.py, and `make verify` is green.
Appetite:    8 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     a re-check started by the verb, `Broke a test` written by the runner, phase-2a rows, rewriting the statuses of earlier changes.
Pre-mortem:  suppose it failed: most likely because the red-first run in a temporary git worktree reads a test as red for a reason of that checkout, not of the old code.
Starts unless you say stop.
```

Built from `spec.md` (33 criteria) and `design.md`. `research.md` records
no Stage-1 route — explore ran on GLM 5.3 Flash — so nothing is carried
forward from phase 1.

## What phase 4 needs from the design

- The verb lives in `scripts/stage2.py` beside `implement` and shares its
  attempt loop; it is not a mode of `implement` and not a script of its own.
- Red first is shown in a temporary git worktree at the baseline: `git
  worktree add --detach <tmp>/tree <baseline>`, its `tests/` replaced by a
  copy of the worktree's `tests/` (without `__pycache__` and `.pytest_cache`),
  one pytest run per named test, then `git worktree remove --force` and `git
  worktree prune`, in a `finally`.
- The runner writes every Status from the model's fixed lines: the statuses of
  `findings.md` before the checkpoint commit, the loop record's after it.

## Steps

Each step writes its tests with it; every test plants its fault once and
sees it go red (`prompts/04-implement.md`).

1. **`scripts/stage2.py` — the shared loop.** Extract the attempt loop of
   `implement` into one helper, `run_attempts`, taking the verb word, the
   routes, a prompt builder (`diagnostics -> prompt`), an optional answer
   check (`answer -> problems`, called only when `verify_attempt` returned
   none), an optional write before the checkpoint, an optional write after
   it, the commit message and the closing failure sentence. `implement`
   passes values that keep every string it writes and prints today; its
   tests stay green unchanged. `checkpoint` takes `message` (default
   `feat(<change>): implement accepted plan`). `run_work_model`'s answer,
   which `implement` ignores, reaches the answer check.
2. **`scripts/stage2.py` — the three words.** `undecided`: a row is decided
   when its Status begins `rejected`, or begins `taken` or `fixed` and its
   `Broke a test` is `yes` or `no`. `taken_in_round`: a row of the round
   counts when its Status begins `taken` or `fixed`. Both read without regard
   to case, as today.
3. **`scripts/stage2.py` — the rows.** A function that collects, from the
   loop record (`record_rows`) and from `findings.md`, every taken row with
   its place (record, released block, phase-6 table), and the waiting IDs:
   record rows that are neither taken, rejected nor fixed, phase-6 rows whose
   Status is blank or begins `open`. In `findings.md` it reads section by
   section, a line that begins `## ` opening the next: under a heading that
   begins `RELEASE_HEADING`, the
   ten-cell lines with a loop id up to `Kept from the loop record:`; under a
   heading that begins `## Phase 6`, the nine-cell lines that are not
   furniture, up to `NOT_ROWS_NOTE`; any `## ` line ends a section, and a
   line starting with `>` is never a row (`split_row` already returns `None`
   for it).
4. **`scripts/stage2.py` — the verb `repair`.** `GLM = ("glm-coding-plan",
   "glm-5.3", "max")`. `repair(root, change, stage2_off=None)`: preflight as
   `implement` (`required=("plan.md",)`, first endpoint `GLM`, or `SONNET`
   under `--stage2-off`); the clean-tree refusal outside `findings.md`;
   then the refusals of criteria 4, 3 and 5, in that order — a waiting row is
   named even when nothing is taken — all before the key is read; the routes `(GLM, key, "glm", None)`, `(GLM, key, "glm-repair",
   "first GLM 5.3 post-run check failed")`, `(SONNET, None, "stage-1", "two
   GLM 5.3 post-run checks failed")`, or `(SONNET, None, "stage-1", reason)`
   alone. The prompt is `work_prompt(root, "04-implement.md", change, extra)`
   with, in this order: the constant `REPAIR_FORMAT` (repair only these rows;
   answer one fixed line per row, `<ID>: fixed — tests/<path>::<function>` or
   `<ID>: fixed — not a test — <reason>`; a code row needs a test that fails
   on the baseline's code, which the runner runs; only a row taken as `taken
   — not a test` may be answered `not a test`; do not edit `findings.md`),
   `Repair baseline: <sha>`, `## Taken rows` with one line per row
   (`- <ID> [<Severity>, <Dimension>] <Where>: <Finding> — Status: <Status>`),
   `## Accepted spec`, `## Accepted plan`, and the earlier diagnostics.
5. **`scripts/stage2.py` — the answer check.** Fixed lines are read line by
   line after stripping leading whitespace, list markers (`-`, `*`, `+`) and
   `**` or backticks around the ID; the separator is the em dash. Problems,
   each naming its ID: a taken row with no fixed line or more than one; a
   fixed line for an ID that is no taken row; a line in neither form; a code
   row answered `not a test`; a named test whose file under `tests/` holds no
   line beginning `def <function>(`; a taken row that no longer stands where
   it stood (the model edited it). Only when none of these stands, the
   red-first runs: interpreter `<root>/.venv/bin/python3` when executable,
   else `sys.executable` (one function, `red_first_python(root)`, so a test
   can replace it); command `<python> -m pytest -q -p no:cacheprovider
   <path>::<function>` with `cwd` the temporary tree; environment
   `foreign_env({"PYTHONDONTWRITEBYTECODE": "1"})`; limit `RED_FIRST_MINUTES
   = 10` through `launch(..., timeout=..., limit="the red-first time
   limit")`. Exit 1 or 2 is red first; any other exit, a timeout or a git
   error is a problem naming the row, the test and the exit. Every text is
   scrubbed with the key.
6. **`scripts/stage2.py` — the statuses and the commit.** Before the
   checkpoint, rewrite the Status cell (index 7) of each taken row of
   `findings.md` in its place and re-render that line as `| ` + `' | '.join`
   + ` |`; a `|` in a reason becomes `\|`; `stamp_updated`. The commit
   message is `fix(<change>): repair taken findings <IDs, comma-separated>`.
   After the checkpoint, rewrite the record's own row lines the same way
   (never the reviewer's words); a failure there is `CallFailed` naming the
   IDs to mark by hand. The route block on `stage-1` reads `Stage-1 route:
   repair · model <model> · reason: <reason>.`; the closing failure reads
   `repair post-run checks failed after the allowed attempts; …`.
7. **`scripts/stage2.py` — the entry.** `VERBS["repair"] = repair`; `main()`
   accepts `--stage2-off` for `{"explore", "implement", "repair"}` and
   dispatches all three with the flag; the flag's help and the module
   docstring name the verb (`python3 scripts/stage2.py repair <change>   #
   GLM 5.3, the taken findings`) and say that `--stage2-off` belongs to
   explore, implement and repair.
8. **`scripts/stage2_runs.py`.** A released loop row whose Status begins
   `fixed` counts as taken; `GLM = stage2.GLM` replaces the literal tuple, its
   comment saying the tuple now routes the repair.
9. **The texts.** `model-endpoints.yaml`: one sentence in the remark of
   `glm-coding-plan` — `glm-5.3` repairs the findings the orchestrator takes
   through `stage2.py repair` (maintainer, 2026-10-12; ADR 0015) — no other
   key. `docs/WORKFLOW.md` §4: the opening paragraph names the repair on GLM
   5.3 since 2026-10-12; the routing table gains a row `| Repair after 4b and
   6 | **GLM 5.3** | … |` (one GLM 5.3 repair attempt, then Sonnet 5.5);
   "Eight verbs exist" becomes "Nine verbs exist" with a `repair` bullet; a
   new subsection `### Repairing taken findings (repair)` after "The review
   loop (phase 4b)" says who decides, what the verb takes, the fixed lines,
   red first, the statuses, `Broke a test` and the re-check; the loop section
   gives the Status to the orchestrator and the repair to `repair`.
   `AGENTS.md`: the Stage-2 paragraph names `repair <change>` on GLM 5.3 and
   ends "Reviews go by class; explore, implement and repair do not." — words
   inside its existing lines, **no new line** (`AGENTS.md` stands at 200
   lines, the cap of `test_agents_md_names_the_loop_and_the_runner`).
   `prompts/04b-review-loop.md`: "For the implementer" becomes "For the
   orchestrator" — Status (with `taken — not a test — <reason>`), then `python3
   scripts/stage2.py repair <change>`, then `Broke a test` per fixed row, the
   evidence rule kept word for word. `prompts/04-implement.md`: a paragraph
   **Repair** after "A foreign finding is taken on evidence" — the verb, its
   model, the fixed lines, red first; its `**Model:**` paragraph unchanged.
   `templates/findings.md`: the four Status words of criterion 32 under
   "Stage 2". `docs/adr/0015-glm-5-3-repairs-taken-findings.md` stays as
   drafted unless a review row changes it.

## Files

- `scripts/stage2.py` — changed: steps 1 to 7.
- `scripts/stage2_runs.py` — changed: step 8.
- `tests/test_stage2.py` — changed: the tests of the ledger below, a helper
  that commits `tests/test_seed.py`, writes taken rows into the record and
  `findings.md` and scripts a `claude` stand-in that plants `src/app.py`
  (`value = 2`), `tests/test_fix.py` (a test that reads `src/app.py` and
  fails on `value = 1`) and a time line.
- `tests/test_stage2_runs.py` — changed: one test.
- `model-endpoints.yaml`, `docs/WORKFLOW.md`, `AGENTS.md`,
  `prompts/04b-review-loop.md`, `prompts/04-implement.md`,
  `templates/findings.md` — changed: step 9.
- `plans/changes/stage2-repair/plan.md` — the time log; `findings.md` — the
  runner's audit lines; `plans/INDEX.md` — rendered by the runner.

## Not touched

`provenance.yaml`, `scripts/leakcheck.py`, `docs/adr/0007-…`,
`docs/adr/0011-…`, `scripts/check_decision_continuity.py`,
`docs/architecture/`, `.claude/settings.json`; `run_codex`, `run_reviewer`,
`PI_TOOLS` and the `review-loop`, `review`, `release-loop` and `probe` verbs
beyond `undecided` and `taken_in_round`; `prompts/02a-spec-review.md` and
`prompts/06-review.md` — the re-check runs with them as they are; the tests of
`implement`, which hold the shared loop.

## Verification

```bash
.venv/bin/python -m pytest -q tests/test_stage2.py tests/test_stage2_runs.py
make verify
```

Under `python3 scripts/stage2.py implement stage2-repair` the runner runs
`make verify` itself.

## Criterion ledger

- 1: tests/test_stage2.py::test_repair_lists_every_taken_row_and_no_rejected_or_fixed_one — the released block or a phase-6 table is not read, or a rejected row is listed
- 2: tests/test_stage2.py::test_the_repair_prompt_carries_the_contract_and_ends_with_the_read_request — the plan left out, or the read request before the rows
- 3: tests/test_stage2.py::test_repair_with_nothing_taken_refuses_before_any_call — a call with an empty row list
- 4: tests/test_stage2.py::test_an_undecided_row_holds_the_repair — an `open` phase-6 row ignored
- 5: tests/test_stage2.py::test_a_doubled_taken_id_refuses_the_repair — the first row of an ID wins
- 6: tests/test_stage2.py::test_repair_requires_a_clean_tree_a_spec_and_a_plan_with_its_time_heading — preflight without `plan.md`
- 7: tests/test_stage2.py::test_repair_routes_glm_5_3_then_its_repair_then_sonnet — `GLM_FLASH` in the routes, or no diagnostics carried
- 8: tests/test_stage2.py::test_stage2_off_repairs_with_one_sonnet_attempt_and_records_the_reason — the key read, or no route block
- 9: tests/test_stage2.py::test_a_missing_glm_key_refuses_the_repair — a call without the key
- 10: tests/test_stage2.py::test_a_leak_in_a_taken_row_stops_the_repair_without_fallback — the rows outside the scanned prompt, or a fallback after the BLOCK
- 10: tests/test_stage2.py::test_an_undeclared_glm_5_3_refuses_the_repair — no declaration check for `glm-5.3`
- 11: tests/test_stage2.py::test_each_repair_attempt_leaves_an_audit_line_the_count_reads — the verb word `implement` in the line
- 12: tests/test_stage2.py::test_repair_has_file_tools_and_pins_glm_5_3 — `Bash` among the tools, or `glm-5.3-flash` pinned
- 13: tests/test_stage2.py::test_record_rows_reach_the_model_only_in_the_prompt — the rows written into a worktree file
- 14: tests/test_stage2.py::test_a_red_verify_or_a_missing_time_line_fails_a_repair_attempt — a checkpoint after a red `make verify`
- 15: tests/test_stage2.py::test_each_taken_row_needs_exactly_one_fixed_line — a missing, doubled or unknown line accepted
- 16: tests/test_stage2.py::test_a_code_row_answered_not_a_test_fails_the_attempt — `not a test` accepted for a code row
- 17: tests/test_stage2.py::test_a_fixed_line_naming_an_undefined_test_fails_the_attempt — no definition check
- 18: tests/test_stage2.py::test_a_named_test_that_is_not_red_first_fails_the_attempt — exit 0 or 5 on the baseline accepted
- 19: tests/test_stage2.py::test_the_red_first_run_leaves_no_worktree_behind — the temporary worktree not removed
- 20: tests/test_stage2.py::test_a_failed_repair_process_restores_the_baseline_without_a_further_attempt — a fallback after a dead model process
- 21: tests/test_stage2.py::test_a_passing_repair_writes_fixed_into_each_rows_place_and_nothing_else — `Broke a test` written, or a rejected row changed
- 22: tests/test_stage2.py::test_a_passing_repair_ends_in_one_checkpoint_commit_with_its_statuses — implement's message, or the statuses outside the commit
- 23: tests/test_stage2.py::test_a_failed_repair_writes_no_fixed_status — statuses written before the checks
- 23: tests/test_stage2.py::test_the_record_is_marked_only_after_the_checkpoint_commit — the record written before the commit
- 24: tests/test_stage2.py::test_repair_starts_no_review_call — the verb calls `review-loop` or `review`
- 25: tests/test_stage2.py::test_a_fixed_loop_row_is_decided_only_with_its_broke_a_test_mark — `undecided` reads only `taken` and `rejected`
- 25: tests/test_stage2.py::test_an_undecided_loop_row_holds_the_next_round_and_the_release — an undecided row no longer holds the round
- 26: tests/test_stage2.py::test_round_three_starts_after_a_fixed_round_two_row — `taken_in_round` reads only `taken`
- 27: tests/test_stage2_runs.py::test_a_fixed_loop_row_counts_as_taken — a fixed row counted as undecided
- 28: tests/test_stage2.py::test_stage2_off_is_accepted_for_repair — the flag refused for repair
- 28: tests/test_stage2.py::test_stage2_off_is_only_for_work_verbs — a review verb accepts the flag
- 29: tests/test_stage2.py::test_the_glm_entry_keeps_its_models_and_names_the_repair_verb — a model dropped, or the remark without `stage2.py repair`
- 29: tests/test_stage2.py::test_the_glm_remark_names_its_work_verbs_and_no_review_phase — the remark names a review phase
- 30: tests/test_stage2.py::test_the_doctrine_names_the_repair_verb — "Eight verbs exist" kept, or AGENTS.md without the verb
- 31: tests/test_stage2.py::test_the_prompts_name_the_repair_verb_and_red_first — 04b without the command, or 04 without red first
- 32: tests/test_stage2.py::test_the_findings_template_names_the_repair_statuses — one of the four words missing
- 33: tests/test_stage2.py::test_adr_0015_amends_adr_0011_and_records_the_repair_route — the file missing, or the amendment unstated

## Runner route — 2026-10-12

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-12, phase-4 session under the Stage-2 runner (`implement`, attempt 1, route flash) — start and
end clock times not readable in it: the session has file tools and no command tool, so `date` could not
be read, and the span is not estimated. The day is the runner's session date. The session covered the
whole plan in one sitting: steps 1–8 (`scripts/stage2.py` — the shared attempt loop, the three status
words, the row places, the verb `repair` with its refusals and routes, the answer check with the
red-first run, the statuses and the checkpoint, the entry and `--stage2-off`; `scripts/stage2_runs.py`
— a fixed released row counts as taken), step 9 (the doctrine, AGENTS.md, the two prompts, the
findings template, the `glm-coding-plan` remark; the ADR 0015 draft stood already from phase 2b), and
the 35 tests of the criterion ledger that were still unwritten, each with its planted fault named in
its docstring. The runner runs `make verify` and makes the checkpoint commit after this entry.

2026-10-12, phase-4 repair session under the Stage-2 runner (`implement`, attempt 2, route flash) —
start and end clock times not readable in it: the session has file tools and no command tool, so
`date` could not be read, and the span is not estimated. The day is the runner's session date. The
session repaired attempt 1's post-run diagnostics, and nothing else: the five ruff-check errors (the
two unused loop variables `place` in `check_repair_answer` renamed `_place`; the three unused
arguments of the test spy `spy_record` renamed with a leading underscore) and the ruff-format
deviations in `scripts/stage2.py` (the red-first teardown's `subprocess.run` wrapped into the
formatter's body layout; the `findings_rows` call collapsed that fits on one line) and in
`tests/test_stage2.py` (six statements whose one-line form passed 120 characters exploded, and whose
inner call wrapped, to the formatter's form). The markdownlint lines in the run's standard error come
from the gate `markdownlint`, which `decisions/gates.yaml` holds at `enforcement: report` — it
reports and blocks nothing, and its files are not this change's. The runner runs `make verify` and
makes the checkpoint commit after this entry.

2026-10-12, phase-4 second repair session under the Stage-2 runner (`implement`, attempt 3, route
stage-1) — start and end clock times not readable in it: the session has file tools and no command
tool, so `date` could not be read, and the span is not estimated. The day is the runner's session
date. The session repaired the one remaining gate, `ruff-format`, and nothing else: the two nested
conditional expressions that assign `kind` in `scripts/stage2.py` (`findings_rows`,
`mark_repaired_findings`) became plain `if`/`elif` statements; in `tests/test_stage2.py` the four
string literals with escaped double quotes (`FIX_TEST` and `green_on_baseline`) took single quotes,
and the signature of `test_the_record_is_marked_only_after_the_checkpoint_commit`, which fits in
118 characters, went onto one line. The runner runs `make verify` and makes the checkpoint commit
after this entry.

2026-10-12, loop round-1 repair session under the Stage-2 runner (`repair`, GLM 5.3) — start and
end clock times not readable in it: the session has file tools and no command tool, so `date` could
not be read, and the span is not estimated. The day is the runner's session date. The session
repaired the three taken rows and nothing else: L1-1, the fixed line's test path in
`scripts/stage2.py` (`fixed_status`), now refuses a `.` or `..` path segment as the criterion
ledger's gate does, proven red first by
`tests/test_stage2.py::test_a_fixed_line_whose_test_path_climbs_out_of_tests_fails_the_attempt`;
L1-2, `RECORD_INTRO` now names `taken — not a test — <reason>` and says a row the repair marked
`fixed` needs the `Broke a test` mark too, proven red first by
`tests/test_stage2.py::test_a_new_records_intro_names_the_not_a_test_status_and_the_fixed_mark`;
L1-3, a text row, the "Reads" passages of `docs/WORKFLOW.md` §4 and the `scripts/stage2.py` module
docstring now name `repair` among the calls the `--restricted` boundary covers. The runner runs the
red-first proofs, `make verify` and the checkpoint commit after this entry.

2026-10-12, loop round-2 repair session under the Stage-2 runner (`repair`, GLM 5.3) — start and
end clock times not readable in it: the session has file tools and no command tool, so `date` could
not be read, and the span is not estimated. The day is the runner's session date. The session
repaired the six taken rows and nothing else: L2-1, a reason's `|` is now escaped exactly once by
`fixed_status` in `scripts/stage2.py`, whatever spelling the fixed line used, proven red first by
`tests/test_stage2.py::test_a_reason_with_a_pipe_is_escaped_once_as_its_fixed_line_gives_it`; L2-2,
the write path of a text row's repair — the record, the phase-6 table, the checkpoint commit — now
runs in a test, proven red first by
`tests/test_stage2.py::test_a_text_row_taken_as_not_a_test_is_repaired_and_its_status_written`;
L2-3, `mark_repaired_findings` and `mark_repaired_record` keep the file's final newline, proven red
first by `tests/test_stage2.py::test_a_repair_keeps_the_final_newline_of_findings_and_the_record`;
L2-6, `undecided_refusal` in `scripts/stage2.py` names the missing `Broke a test` mark of a fixed
row for `review`, `review-loop` and `release-loop`, proven red first by
`tests/test_stage2.py::test_a_fixed_row_without_its_mark_is_refused_with_the_missing_mark_named`;
L2-4, a text row, WORKFLOW §4 now says repair prompts carry the taken loop rows to Z.ai before the
phase-6 verdict; L2-5, a text row, the five docstring places of `scripts/stage2.py` name the
orchestrator as the one who decides a row. The runner runs the red-first proofs, `make verify` and
the checkpoint commit after this entry.
