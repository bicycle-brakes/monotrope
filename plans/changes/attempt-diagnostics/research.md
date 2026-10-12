---
title: "Research — attempt-diagnostics"
status: draft
implementation_status: partial
date: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-cit
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, runner, implement, diagnostics]
---

# Attempt diagnostics — Research

Read on 2026-10-11 against `origin/main` at `a6b7150`. This change answers
bead coding-harness-cit: the implement verb of the stage-2 runner
(`scripts/stage2.py implement`) discards why a failed attempt failed.

## What happened

On 2026-10-11 the implement run for change criterion-test-ledger (bead
coding-harness-909) failed its post-run check twice on GLM 5.3 Flash and
passed on the third attempt, the Sonnet 5.5 fallback (commit `1d179c9` on
branch `feat/criterion-test-ledger`). Its `findings.md` holds three audit
lines; the only reasons recorded are "first Flash post-run check failed" and
"two Flash post-run checks failed". Nothing under `~/.local/state/coding-harness/`
was written by the run (looked at 2026-10-11).

Indirect evidence, measured by the orchestrating session during the run: the
worktree held `scripts/check_criterion_ledger.py` but no
`tests/test_check_criterion_ledger.py`; the ratchet in `tests/test_ci.py`
demands a test file per script, which alone turns `make verify` red. Which
attempt wrote which file cannot be told: the runner makes one checkpoint
commit after the passing attempt.

## What exists today

- `scripts/stage2.py`, `implement()` (around line 1522): runs up to three
  routes (Flash, Flash repair, Sonnet). After each attempt
  `verify_attempt()` returns a list of problems: preparation failures, a red
  `make verify` with the blocking gates and their last lines
  (`red_sections`, `TAIL_LINES`, `STDERR_LINES`), scrubbed of the key by
  `scrub()`, and a missing measured line under `## Time used` in `plan.md`.
- Those problems are appended to a local list `diagnostics` and passed into
  the next attempt's prompt through `implementation_prompt()` under
  "Earlier post-run diagnostics"; the list is not written anywhere.
- `begin_work_call()` writes the audit line per attempt into the phase's
  durable artefact (`findings.md` for implement).
- When all attempts fail, `implement()` raises `CallFailed("implementation
  post-run checks failed after the allowed attempts")` without the
  diagnostics.

## What is unclear

- Where in `findings.md` the diagnostics belong (under the attempt's audit
  line, or a section of their own) and how long they may be.
- Whether the per-attempt diff stat should be kept too, so it is visible
  which model wrote what.
- Whether the explore verb and the review loop have the same gap.

Stage-2 call, 2026-10-11: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 347 files, 817 commits, 12 rules.

## Runner exploration — 2026-10-11

Verified on 2026-10-11 in the worktree `feat/attempt-diagnostics` against the tree as it stands; every claim in the sections above was checked against `scripts/stage2.py`.

**The three routes and what survives a failed attempt, verified.** The routes are literal in `scripts/stage2.py`, function `implement`: `(GLM_FLASH, key, "flash", None)`, `(GLM_FLASH, key, "flash-repair", "first Flash post-run check failed")`, `(SONNET, None, "stage-1", "two Flash post-run checks failed")` when Stage 2 is on, and one `(SONNET, None, "stage-1", stage2_off)` route under `--stage2-off`. What a failed attempt leaves is exactly three things. First, the audit line `begin_work_call` appends to the phase artefact (`ctx.findings` for implement): verb, attempt number, route, endpoint, model, optional reason, leak-check counts — no problem text. Second, for the `stage-1` route only, `implement` calls `insert_before_time`, which writes a `## Runner route — <date>` block into `plan.md`; the two Flash attempts leave no such block. Third, whatever the attempt's edits left in the worktree: the problems path after `verify_attempt` does not restore the tree — only a failed model call does, through the `except CallFailed` branch around `run_work_model`, which calls `restore_baseline` and keeps only the change's `findings.md`. A later attempt therefore builds on the earlier attempt's half-done tree, and `checkpoint` afterwards stages everything with `git add -A` into one commit that must be exactly one descendant of the baseline; which attempt wrote which file is unrecorded.

**What the diagnostics contain and where they go, verified.** `verify_attempt` returns bounded strings: preparation failures from `prepare_derived` ("Derived-file preparation failed: …", bounded by `TAIL_LINES` = 80), a red `make verify` rendered by `red_sections` (each blocking gate keeps its start frame and its last lines, `RED_SECTION_LINES` = 60 per gate within `RED_TOTAL_LINES` = 200; unframed standard error tail `STDERR_LINES` = 40; when nothing is framed, the plain output tail of `TAIL_LINES`), credential-scrubbed by `scrub`, plus the missing measured line from the `time_log` comparison against `baseline_time`. `implement` collects these into the local list `diagnostics` under `Attempt <n> (<route>):` and passes them only into the next attempt's prompt through `implementation_prompt` under `## Earlier post-run diagnostics`. When all routes are exhausted, `implement` raises `CallFailed("implementation post-run checks failed after the allowed attempts")` — the collected problems are in neither the exception nor any file. For contrast, a model-process failure goes through `fail`, which prints the last 40 lines of the program's standard error, scrubbed, to the runner's own standard error and raises `CallFailed("<program> call failed: <reason>")` — equally undurable. The exit contract is the module docstring's line "Exit: 0 done, 1 a call or implementation post-check failed, 2 refused"; class `CallFailed` carries "exit 1".

**The explore verb has no attempt chain at all.** `explore` makes exactly one call (`begin_work_call` with the attempt fixed at 1), runs no post-run checks — no `make verify`, no time-log check — and appends the answer wholesale under `## Runner exploration — <date>` via `append`; a failed call raises `CallFailed` and nothing lands in `research.md`. The review loop has no in-process retry whose diagnostics could be lost: `review_loop` runs one round per invocation through Pi, the module docstring states that a failed call, an empty answer or a reviewer-timeout call "is no round", `run_reviewer` fails through the same `fail`, and the loop record (`record_dir`, `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md` — the runner's only out-of-repo write target) is written only on success. The reviewer verbs `spec_review` and `review` fail the same way through `run_codex` and `fail`. The observation that an implement run writes nothing under `~/.local/state/coding-harness/` is consistent with the code: only the loop record ever writes there.

**Counting neighbours and pinned tests.** `scripts/stage2_runs.py` (`measure`, `CALL_LINE`, `CALL_PREFIXES`) counts call lines from findings.md and research.md: only lines starting with `Stage-2 call, ` or `Stage-2 session, ` are counted, clean = contains `leak check clean over`; any other prose line is invisible to the counter. Today's behavior is pinned in `tests/test_stage2.py`: `test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics`, `test_sonnet_fallback_starts_with_both_diagnostics_when_both_flash_attempts_deleted_the_heading` (asserts the fallback prompt carries `Attempt 1 (flash)` and `Attempt 2 (flash-repair)`), `test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason`, `test_a_leak_between_work_attempts_stops_before_fallback`, `test_a_key_in_the_gate_output_never_reaches_the_next_attempt`, plus the audit-line assertions (`attempt 2 · route flash-repair`, `attempt 3 · route stage-1`, `reason two Flash post-run checks failed`). The doctrine names the runner's failure behavior only in `docs/WORKFLOW.md`, section "The routing": restore on a failed model process and `implement <change> --stage2-off` as the next step; the three routes and the diagnostics chain are documented nowhere outside `stage2.py`'s docstrings (`implement`: "Phase 4: Flash, one Flash repair and Sonnet fallback").

**Files a change would have to touch, as far as today's code shows.** `scripts/stage2.py` (`implement`, `verify_attempt`, `begin_work_call`, `implementation_prompt`, possibly `explore`); `tests/test_stage2.py` for the pinned behavior above; `scripts/stage2_runs.py` and `tests/test_stage2_runs.py` only if findings.md gains line shapes the call counter could trip over; `docs/WORKFLOW.md` §"The routing" if the doctrine is to name the routes or durable diagnostics. A new script would additionally answer the ratchet `test_every_script_has_a_test_or_a_declared_reason` in `tests/test_ci.py` or stand with a reason in `ci_gates.OHNE_TEST`.

*Note by the orchestrating session (2026-10-11): GLM's answer opened with a German preamble and a duplicate heading, both removed here (house rule 1); the text below the heading is unchanged.*

**Not read here.** The bead coding-harness-cit itself was not read: the tracker is the Dolt database under `.beads/`, and this session has no shell. `plans/changes/criterion-test-ledger/` does not exist in this worktree (its branch is unmerged), so the audit lines quoted under "What happened" stand as the orchestrating session recorded them and were not re-verifiable here. `~/.local/state/coding-harness/` is outside this worktree and was not read; what the runner may write there is stated from `record_dir` and the module docstring, not from a look at the directory.

## Readers of findings.md — phase 2, 2026-10-11

Read on 2026-10-11 at `b48e740` by the phase-2 session, to settle where a
failed attempt's record may stand in `findings.md` without a reader taking it
for its own. The bead (`tools/bd show coding-harness-cit`) was read this time:
its acceptance asks that a passing attempt leave only its audit line.

- **Line-anchored readers.** `scripts/stage2_runs.py`, `measure`: call lines
  by `CALL_PREFIXES` at column 0, sections by `## ` at column 0, phase-6
  rounds by `stage2.VERDICT_LINE`, rows through `stage2.split_row`, which
  strips whitespace before it looks for `|` at both ends — an indented table
  line is still a row. It splits with `str.splitlines()`, which also breaks at
  U+2028, U+0085 and the other line boundaries Python knows. `scripts/stage2.py`:
  `VERDICT_LINE`, `VERDICT_START` (case-insensitive), `SESSION_LINE`,
  `ROUNDS_LINE`, `ROUND_HEADING`, all `^` with `re.M`, which breaks at `\n`
  only.
- **Readers that match anywhere.** `release` appends `NO_LOOP_LINE` only when
  neither it nor `RELEASE_HEADING` occurs anywhere in the text (`in`);
  `released_rows` and `fill_marks` start at `rfind(RELEASE_HEADING)`. A pytest
  failure that quotes either constant is enough: `tests/test_stage2.py` asserts
  on both, and a runner change implemented through the runner prints them.
- **`scripts/stage2_session.py`, `finalize`**, matches its pending line by
  `attempt <id> ·` and the line's ending; the id is `uuid4().hex[:12]`, fresh
  per launch, so no earlier text can hold it.
- **Gates.** No blocking gate of `decisions/gates.yaml` reads the body of a
  change's `findings.md`: `dangling-beads` reads `docs/` only,
  `plans-registry` and `frontmatter-current` read the header.
- **The leak check** scans every file under the change folder
  (`scripts/leakcheck.py`, docstring item a), so `findings.md` is in every
  later call's scanned set; it does not scan objects no ref reaches.
- **The credential scan** (`remove_changed_credential`) reads the contents of
  changed files, never their names; the checkpoint's `git add -A` runs after
  it.
- **Stage 1 reads no key.** `test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason`
  and `test_explore_stage2_off_uses_haiku_without_reading_the_glm_key` fail
  when `read_secret` is called under `--stage2-off`.
- **`implement` keeps `findings.md` through a restore**: `restore_baseline`
  puts every path back except the change's `findings.md`.
- **The validator** `scripts/validate_change_artefacts.py`, named as the gate
  of phases 2 and 3 in `prompts/02-spec.md` and `prompts/03-plan.md`, does not
  exist in this tree (searched 2026-10-11); `make verify` is the measured gate.
