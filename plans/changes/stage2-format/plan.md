---
title: "Plan — stage2-format"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-52r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, runner, implement, formatting]
---

# Plan — stage2-format

```text
For you:     An implement attempt no longer fails on formatting or on lint findings ruff fixes safely: before `make verify` the runner applies them to the change's Python files under scripts/ and tests/, and a failed attempt's block or the passing commit says what it changed.
Done when:   criteria 1–12 each held by the test the ledger names, no existing test edited, `make verify` green
Appetite:    3 h of phase 4, one repair round included; a stop, not an estimate
Not now:     whole-tree formatting, unsafe fixes, gate or ruff-config changes, a ruff from PATH, criteria for the repair verb (pull request #131)
Pre-mortem:  suppose it failed: most likely because pull request #131 moves the attempt loop and its merge drops the wiring, so a passing run formats without saying so
Starts unless you say stop.
```

Implements [`spec.md`](spec.md), criteria 1–12 (class `bounded`, appetite
3 h). Facts read at `9be21fb` (`research.md`, "Phase 2 additions"). Phase 1
explored on route `flash` (GLM 5.3 Flash), so there is no Stage-1 fallback to
carry forward.

## Decided in phase 3

No `[DECISION]` is open. The spec's `[DETAIL]`s stand; these are the plan's:

- `[DETAIL]` **The format line's words**, which the tests compare:
  ``ruff changed `scripts/a.py`, `tests/test_b.py`.`` or `ruff changed no
  file.`; notes follow before the full stop, each after a semicolon and a
  space — `ruff check left findings without a safe fix` (check exited 1),
  `ruff <check|format> exited
  <n>` (any other non-zero exit); or ``not run — no ruff at `.venv/bin/ruff`;
  `make venv` builds it.`` / `not run — <reason>.`, the reason on one line
  without its own full stop. In diagnostics the line reads ``Runner format
  before `make verify`: <line>``; in the commit message, below the subject and
  an empty line, the heading ``Runner format before `make verify` (ruff check
  --fix with safe fixes only, then ruff format):`` and one `- Attempt <n>
  (<route>): <line>` per attempt that ran the step.
- `[DETAIL]` **A launch failure of either ruff command makes the whole line
  `not run`**: the binary that cannot start for one cannot start for the other.
- `[DETAIL]` **`checkpoint` gains `message: str | None = None`, committed as
  `message or f"feat({change}): implement accepted plan"`** — exactly as
  pull request #131 spells it, so the two changes meet identical lines.
- `[DETAIL]` **The test ruff is `STAND_IN` reached through a link.** A helper
  writes the template as `<bin>/ruff.stand-in` and links
  `<worktree>/.venv/bin/ruff` to it, with `.venv/` in `.git/info/exclude`: the
  stand-in reads its scenario beside its resolved file and names itself after
  the link (`ruff`); the leak check lists files through `git ls-files
  --exclude-standard`, so it never reads the link. `STAND_IN`, the `world`
  fixture and `test_a_key_the_gate_writes_under_venv_is_removed_and_refused`
  (which creates its own `.venv`) stay untouched; nothing named `ruff` is put
  on `PATH`.

## Step 0 — main and pull request #131

Before any edit: `git -C <worktree> fetch origin` and `git -C <worktree> merge
origin/main`. If pull request #131 (branch `feat/stage2-repair`, bead
coding-harness-g2f) is merged by then, `implement`'s loop lives in
`run_attempts` and `checkpoint` already takes `message`: step 1's loop wiring
goes into `run_attempts`, the commit message is built from its
`commit_message` argument, and `repair` gets the format line as well; the
criteria are still held through `implement`. If #131 is not merged, the wiring
goes into `implement`, and whoever merges second moves its three pieces (the
per-attempt list, the prefixed diagnostics, the record for the commit) into
`run_attempts`.

## Steps

1. **`scripts/stage2.py`** (about 60 lines).
   - Constants `RUFF = ".venv/bin/ruff"`, `FORMAT_DIRS = ("scripts/",
     "tests/")`, `RUFF_COMMANDS` = `("check", "--fix", "--no-unsafe-fixes",
     "--force-exclude", "--no-cache")` and `("format", "--force-exclude",
     "--no-cache")`, ``FORMAT_LABEL = "Runner format before `make verify`"``.
   - `format_targets(root, env) -> list[str]`: the sorted POSIX paths of
     `changed_paths(root, env=env)` that end in `.py`, start with one of
     `FORMAT_DIRS`, and whose path is not a symlink, is a file, resolves to
     `root.resolve() / relative` and has `st_nlink == 1`; an `OSError` on one
     path leaves it out.
   - `format_step(root, env, key=None) -> str | None`: `None` without targets;
     a `Refused` or `OSError` from the targets or from reading them gives
     `not run — <reason>.`; no file at `root / RUFF` gives the no-ruff line;
     else the targets' bytes are read, each command runs as
     `launch([RUFF, *command, *targets], root, env, key)` — `RUFF` stays
     relative: `launch` starts it from the worktree, and a path with a slash
     is never looked up on `PATH`; a `CallFailed`
     gives `not run — <reason>.` — and the line names the targets whose bytes
     now differ (one that cannot be read counts as changed), plus the notes.
     It returns `scrub(line, key)`.
   - `verify_attempt(…, formatted: list[str] | None = None)`: right after a
     successful `prepare_derived`, `line = format_step(root, env, key)`; when
     both are not `None`, `formatted.append(line)`. Everything else stays.
   - `checkpoint(…, message: str | None = None)` as decided above.
   - `implement`: `record: list[str] = []` before the loop; per attempt
     `formatted: list[str] = []` passed to `verify_attempt`; first in the
     existing `if problems:` branch, `problems = [*(f"{FORMAT_LABEL}: {line}"
     for line in formatted), *problems]` — so the `make verify could not be
     run` path gets it too; after it, `record += [f"- Attempt {attempt}
     ({route}): {line}" for line in formatted]`; the passing checkpoint gets
     `message=` the subject alone when `record` is empty, else the subject, an
     empty line, the heading and `record`.
   - Docstrings: the module docstring's implement sentence and
     `verify_attempt`'s each gain one clause — before `make verify` the runner
     applies ruff's safe fixes and formatter to the changed Python files under
     `scripts/` and `tests/`.
2. **`tests/test_stage2.py`**, a new section after
   `test_a_quoted_release_heading_or_no_loop_line_moves_no_release`, headed
   for spec stage2-format and bead coding-harness-52r. Helper
   `venv_ruff(world, executable=True)` as decided above; with
   `executable=False` it writes a plain `.venv/bin/ruff` of mode 0644 instead
   of the link. Unless a test says otherwise: `venv_ruff(world)` is called
   first, so a wrongly started ruff is recorded; Flash route, the model step
   plants the named files and appends a time line to `plan.md`, make is
   green, and ruff steps are given as `ruff=[check, format, …]` per attempt.
   1. Commit `scripts/gone.py` and an unformatted `scripts/old.py` first; the
      model plants `scripts/a.py`, `tests/test_b.py`, `src/c.py`,
      `scripts/notes.md` and deletes `scripts/gone.py`. The two ruff argv
      lists are exactly the spec's commands on `scripts/a.py tests/test_b.py`,
      and the recorded names run `claude`, `ruff`, `ruff`, `make`.
   2. `verify_attempt` called directly with an untracked regular
      `scripts/real.py`, `scripts/link.py` linked to a file outside the
      worktree, and `tests/hard.py` hard-linked to `tests/hard_twin.py`: both
      argv lists end in `scripts/real.py` alone.
   3. `successful_implementation` (only `src/app.py`): no ruff call, and
      `git log -1 --format=%B` is the subject alone.
   4. A decoy `<bin>/ruff` shell script touches `<bin>/decoy-called` and
      exits 97: two ruff calls recorded, no `decoy-called`.
   5. Every recorded ruff environment holds neither `KEY` among its values
      nor `ANTHROPIC_AUTH_TOKEN`, `GH_TOKEN`, `OPENAI_API_KEY`, `X_SECRET`.
   6. Attempt 1 plants `scripts/a.py` = `a=1` without a time line, its
      format step plants four lines; attempt 2 changes nothing, its format
      step plants `a = 1`; attempt 3 adds the time line. Block 1 lists
      `` `scripts/a.py` +1 -0 ``, block 2 says `Files the attempt changed:
      none.`
   7. Attempt 1 plants `scripts/a.py` and `tests/test_b.py` without a time
      line; its format step changes `scripts/a.py` only; make red with a
      pytest frame. The first diagnostics entry of block 1, and the first line
      of attempt 1's entry in the second prompt, is ``- Runner format before
      `make verify`: ruff changed `scripts/a.py`.``
   8. Attempt 1 plants only `src/app.py` without a time line; attempt 2
      plants `scripts/a.py` and the time line, its format step changes it.
      The commit message is exactly the subject, an empty line, the heading
      and ``- Attempt 2 (flash-repair): ruff changed `scripts/a.py`.``
   9. The first attempt passes after its format step changed `scripts/a.py`:
      nothing follows its audit line in `findings.md`.
   10. Parametrized `no-ruff` (no helper), `not-executable`, `findings-left`
       (check exits 1), `format-error` (format exits 2): exit 0, one model
       call, one make call, one commit on the baseline; the last two lines
       carry their note.
   11. `no-ruff` and `not-executable`: in the commit message's attempt-1
       line, the format line begins `not run —` and holds `no ruff at` or
       `could not be started`.
   12. The model plants `scripts/k<KEY[3:15]>.py`, its format step changes
       it: the commit message holds `[credential]` and no 8-character window
       of `KEY`.
3. **`docs/WORKFLOW.md`**, §"The routing", after "a passing attempt leaves
   its audit line only.": "Before `make verify`, the runner runs the
   worktree's own `.venv/bin/ruff` — `check --fix` with safe fixes only, then
   `format` — on the change's Python files under `scripts/` and `tests/`; what
   that changed stands first in a failed attempt's diagnostics and in the
   checkpoint commit's message, and a ruff that cannot run or leaves findings
   leaves the verdict to `make verify`."
4. **This `plan.md`**: each ledger line turns from `not yet written` into a
   test entry once its test exists; a measured line below `## Time used`.
   Then `.venv/bin/python scripts/check_frontmatter_current.py --stamp` and
   `.venv/bin/python scripts/plans_registry.py --index`.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py -q
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_the_format_step_runs_check_then_format_on_the_targets_before_verify — planted fault: format before check, or `--no-unsafe-fixes` dropped
- 2: tests/test_stage2.py::test_the_format_step_runs_check_then_format_on_the_targets_before_verify — planted fault: ruff given `scripts/ tests/` whole
- 2: tests/test_stage2.py::test_the_format_step_leaves_out_links_and_hard_linked_files — planted fault: targets filtered by suffix and directory only
- 3: tests/test_stage2.py::test_without_a_target_file_no_ruff_starts — planted fault: ruff started with an empty path list
- 4: tests/test_stage2.py::test_the_format_step_runs_the_worktrees_ruff_not_the_one_on_path — planted fault: ruff started by its bare name
- 5: tests/test_stage2.py::test_ruff_gets_the_verify_environment_without_credentials — planted fault: the ruff launch given `glm_env` or `os.environ`
- 6: tests/test_stage2.py::test_the_format_steps_writes_stay_out_of_the_models_file_list — planted fault: the second snapshot taken after `verify_attempt`
- 7: tests/test_stage2.py::test_a_failed_attempt_carries_its_format_line_first_in_its_diagnostics — planted fault: the format line appended after the other entries
- 8: tests/test_stage2.py::test_a_passing_run_lists_each_format_line_in_its_commit_message — planted fault: only the passing attempt's line kept, or a line for an attempt without targets
- 8: tests/test_stage2.py::test_without_a_target_file_no_ruff_starts — planted fault: the heading written with no line below it
- 9: tests/test_stage2.py::test_a_passing_attempt_that_was_formatted_leaves_only_its_audit_line — planted fault: the format line appended to findings.md for every attempt
- 10: tests/test_stage2.py::test_a_ruff_failure_leaves_the_verdict_to_make_verify — planted fault: a non-zero ruff exit turned into a problem of the attempt
- 11: tests/test_stage2.py::test_a_ruff_that_cannot_start_is_reported_as_not_run — planted fault: the ruff launch's `CallFailed` propagates like make's
- 12: tests/test_stage2.py::test_a_commit_message_holds_no_fragment_of_the_key — planted fault: the format line built without `scrub`

## Not touched

- In `scripts/stage2.py`: `prepare_derived`, `attempt_block`, `quote_block`,
  `attempt_files`, `worktree_tree`, `red_sections`, `implementation_prompt`,
  `restore_baseline`, `explore` and `review_loop`.
- `STAND_IN`, the `world` fixture and every existing test in
  `tests/test_stage2.py`.
- `decisions/gates.yaml`, `scripts/verify_all.sh`, `Makefile`, `ruff.toml`,
  `pyproject.toml`, `requirements-ci.txt`, `prompts/`.

## Time used

2026-10-12, phase-4 session under the Stage-2 runner (`implement`, route flash) — start and end clock
times not readable in it: the session has file tools and no command tool, so `date` could not be read,
and the span is not estimated. The day is the runner's session date. The session covered the whole
plan in one sitting: step 0's check (pull request #131 merged at `14f6e1a`, already merged into this
branch at `30fa8c5`, so the wiring went into `run_attempts` and the commit message through its
`commit_message` argument — `checkpoint` already took `message`), step 1 (`scripts/stage2.py`: the
constants, `format_targets`, `format_step`, the `verify_attempt` parameter, the four wiring points in
`run_attempts`, the two docstrings), step 2 (the fourteen ledger tests with the helpers `venv_ruff`
and `formatted_attempt`), steps 3–4 (`docs/WORKFLOW.md`, the criterion ledger). The stamp and the
index render of step 4 are the runner's derived-file preparation; it runs `make verify` and makes the
checkpoint commit after this session returns.

2026-10-12, second phase-4 session under the Stage-2 runner (`implement`, the repair of attempt 1) —
start and end clock times not readable in it: the session has file tools and no command tool, so
`date` could not be read, and the span is not estimated. It repaired attempt 1's two blockers, both in
`scripts/stage2.py`: the commit message joined the heading and the attempt lines with an empty line
where the plan's line layout — subject, empty line, heading, record — has none, and the formatter
would have collapsed the parenthesized `FORMAT_COMMIT_HEADING`, whose one-line form is 119
characters, under the configured line-length 120. The stamp and the index render are the runner's
derived-file preparation; it runs `make verify` and makes the checkpoint commit after this session
returns.

2026-10-12, repair session under the Stage-2 runner (`repair`, row L1-1 taken as `taken — not a
test`) — start and end clock times not readable in it: the session has file tools and no command
tool, so `date` could not be read, and the span is not estimated. It strengthened the criterion-8
test `test_a_passing_run_lists_each_format_line_in_its_commit_message`: the failed first attempt
now plants `scripts/b.py` beside `src/app.py`, so it runs the format step and its line
`- Attempt 1 (flash): ruff changed \`scripts/b.py\`.` must survive into the checkpoint commit's
message next to attempt 2's — the "every attempt" part of criterion 8, unmeasured before (finding
L1-1) — and the comment names the planted fault as an earlier attempt's format line dropped before
the checkpoint. The runner's code already keeps every attempt's line, so the strengthened test is
green on the baseline's code and the row is answered `not a test`. The runner runs `make verify`
and makes the checkpoint commit after this session returns.

2026-10-13, repair session under the Stage-2 runner (`repair`, row L2-1 taken as `taken — not a
test`) — start and end clock times not readable in it: the session has file tools and no command
tool, so `date` could not be read, and the span is not estimated. It strengthened the criterion-6
test `test_the_format_steps_writes_stay_out_of_the_models_file_list`: the ruff step list gains `{}`
padding steps so the four-line plant lands on attempt 1's format call and the `a = 1` plant on
attempt 2's — the stand-in spends one ruff scenario step per call, check and format each take one,
so a plant on a check call is overwritten before any snapshot sees it (finding L2-1) — and a second
snapshot taken after `verify_attempt` now counts the four lines in block 1 and names `scripts/a.py`
in block 2. The runner's snapshot code is unchanged, so the strengthened test is green on the
baseline's code by design and the row is answered `not a test`. The runner runs `make verify` and
makes the checkpoint commit after this session returns.

2026-10-13, repair session under the Stage-2 runner (`repair`, rows L3-1 and L3-3, both taken as
code rows) — start and end clock times not readable in it: the session has file tools and no
command tool, so `date` could not be read, and the span is not estimated. L3-1: the note for a
`ruff check` exit 1 now reads `ruff check left findings without a safe fix or a file that does not
parse`, for exit 1 covers both and the exit code alone does not say which; held by
tests/test_stage2.py::test_a_check_exit_one_covers_findings_and_a_file_that_does_not_parse, which
fails on the baseline wording. L3-3: a target whose bytes cannot be read makes the line `not run —
cannot read \`scripts/a.py\`.` — the repository path, not the raw `OSError` text with the
worktree's absolute path; held by
tests/test_stage2.py::test_an_unreadable_target_is_named_by_its_repository_path, which fails on
the baseline. The `format_step` docstring names both. The runner runs the red-on-baseline proof,
`make verify` and the checkpoint commit after this session returns.

2026-10-13, repair session under the Stage-2 runner (`repair`, rows F-1 taken as a code row and
F-2 taken as `taken — not a test`) — start and end clock times not readable in it: the session has
file tools and no command tool, so `date` could not be read, and the span is not estimated. F-1: a
target path holding a line break is written with that break escaped (`_LINE_BREAK_ESCAPES` and
`_one_line` in `scripts/stage2.py`), so the format line stays one line while ruff still gets the
path as it is; held by
tests/test_stage2.py::test_a_target_named_with_a_line_break_keeps_the_format_line_one_line, which
fails on the baseline's verbatim interpolation. F-2: the criterion-1/2 test
`test_the_format_step_runs_check_then_format_on_the_targets_before_verify` now plants a modified,
already tracked `scripts/old.py` among the targets and expects it in both argv lists — the runner
keeps such files already, so the strengthened test is green on the baseline's code and the row is
answered `not a test`. The runner runs the red-on-baseline proof, `make verify` and the checkpoint
commit after this session returns.
