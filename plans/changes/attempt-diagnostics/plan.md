---
title: "Plan — attempt-diagnostics"
status: draft
implementation_status: none
date: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-11
supersedes: null
superseded_by: null
bead: coding-harness-cit
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, runner, implement, diagnostics]
---

# Plan — attempt-diagnostics

```text
For you:     When a GLM implement attempt fails, findings.md shows why and which files it changed, right below that attempt's audit line — also when every attempt fails.
Done when:   criteria 1–16 each held by the test the ledger names, the five pinned tests unchanged and green, `make verify` green
Appetite:    3 h of phase 4, one repair round included; a stop, not an estimate
Not now:     the passing attempt's file list, a dead model process, explore and the review loop, the next attempt's prompt
Pre-mortem:  suppose it failed: most likely because a snapshot is taken at the wrong moment, so a file list blames the model for the runner's own writes
Starts unless you say stop.
```

Implements [`spec.md`](spec.md), criteria 1–16 (class `bounded`, appetite
3 h). Facts read at `b48e740`. Phase 1 explored on route `flash` (GLM 5.3
Flash), so there is no Stage-1 fallback to carry forward.

## Decided in phase 3

No `[DECISION]` is open. The spec's `[DETAIL]`s stand; these are the plan's:

- `[DETAIL]` **The temporary index is seeded with `git read-tree HEAD`**, not
  copied from the real one: a file tracked although ignored stays in the
  snapshot, and the real index is never read or locked.
- `[DETAIL]` **The test stand-in gains a `delete` step key**: without it no
  test can show a deleted file (criterion 2).
- `[DETAIL]` **All new tests go into `tests/test_stage2.py`**, which owns the
  `world` fixture; it imports `stage2_runs` for criterion 11.
  `tests/test_stage2_runs.py` stays as it is.

## Steps

1. **`scripts/stage2.py`** (about 90 lines).
   - Constants `QUOTE_LINE_CHARS = 500`, `ATTEMPT_FILES = 40`;
     `RELEASE_LINE = re.compile("^" + re.escape(RELEASE_HEADING), re.M)` and
     `NO_LOOP = re.compile("^" + re.escape(NO_LOOP_LINE) + r"[ \t]*$", re.M)`.
   - `_last_release(text) -> int`: the start of the last `RELEASE_LINE`
     match, `-1` without one. `released_rows` and `fill_marks` use it in place
     of `rfind(RELEASE_HEADING)`; `release` appends `NO_LOOP_LINE` only when
     neither `NO_LOOP` nor `RELEASE_LINE` matches (criterion 12).
   - `worktree_tree(root) -> str`: in a `tempfile.TemporaryDirectory`, with
     `env = {**os.environ, "GIT_INDEX_FILE": <tmp>/index}`, run
     `read-tree HEAD`, `add -A` and `write-tree` through `_git_output`;
     return the tree id. It raises what `_git_output` raises.
   - `attempt_files(root, before, after) -> list[str]`: `git diff-tree -r -z
     --numstat --no-renames <before> <after>`, one entry per record —
     `` `<path>` +<added> -<removed> ``, or `` `<path>` binary `` for `-`
     counts — and after `ATTEMPT_FILES` entries the single line
     `… and <n> more files`.
   - `attempt_block(attempt, route, listing, files) -> str`, the unquoted
     text of the spec's shape: the header line, the file part (`files` is the
     entry list or a reason string; an empty list reads `none.`), then
     `Diagnostics:` and `listing` inside a fence of backticks one longer than
     the longest run in `listing`, at least three.
   - `quote_block(text, key) -> str`: `scrub`, `splitlines()`, each line
     longer than `QUOTE_LINE_CHARS` keeps its first 500 characters plus a
     space and `[… <n> characters left out …]`, each line prefixed with `>`
     and a space (`>` alone when empty), joined with `\n`, then `scrub` once
     more.
   - `implement`: per attempt, after `begin_work_call` and the route block,
     `before = worktree_tree(root)`; after `run_work_model` and the existing
     credential scan, `after = worktree_tree(root)` — a `Refused` or `OSError`
     from either, or from `attempt_files`, becomes the reason
     `not measured — <message>`. When `verify_attempt` returns problems:
     `listing = "\n".join(f"- {p}" for p in problems)`; append
     `f"Attempt {attempt} ({route}):\n{listing}"` to `diagnostics` exactly as
     today; `append(ctx.findings, quote_block(attempt_block(...), key))` — all
     before the post-run credential scan, which stays where it is. The final
     `CallFailed` reads `implementation post-run checks failed after the
     allowed attempts; why each attempt failed and the files it changed:
     <ctx.findings relative to root>`.
   - The module docstring's implement sentence and the `implement` docstring
     each gain one clause: a failed attempt leaves its diagnostics and the
     files its model changed, quoted, below its audit line in `findings.md`.
2. **`tests/test_stage2.py`**. The stand-in template gains
   `for relative in step.get("delete", []): Path(relative).unlink()`. A new
   section after `test_findings_only_dirt_is_allowed_and_committed` holds the
   tests the ledger names, on these scenarios (`claude` steps, `make` steps):
   1. Flash plants `src/app.py`, repair does nothing, Sonnet adds the time
      line; make red pytest frame, green, green. Every line of each prompt
      entry after its `Attempt` line stands as `> <line>` in findings.md;
      order audit 1 < block 1 < audit 2 < block 2 < audit 3.
   2. Three failing attempts, make red each time: 1 plants `src/a.py` (two
      lines); 2 plants `src/b.py`, rewrites `src/app.py`, plants
      `src/blob.bin` = `"a\x00b"`, deletes `src/a.py`; 3 appends the time line.
      Exact entry sets per block; no block names `plans/INDEX.md` or
      `findings.md`; block 3 has `plan.md` at `+1 -0`.
   3. Attempt 1 changes nothing, attempt 2 passes: block 1 says `none.`
   4. `worktree_tree` monkeypatched to raise `Refused("git add failed:
      planted")`; attempt 1 fails, 2 passes: exit 0, one commit on the
      baseline, block 1 says `not measured — git add failed: planted`.
   5. Parametrized: the first attempt passes, or the second after a failure:
      nothing follows the passing attempt's audit line.
   6. Three attempts without a time line: exit 1, three blocks, standard
      error names `plans/changes/demo/findings.md`.
   7. Attempt 1 fails its check, attempt 2's model exits 1: exit 1, the tree
      restored, block 1 still in findings.md.
   8. Attempt 1 creates `src/k<KEY[3:15]>.txt` and the gate prints the key,
      attempt 2 passes: no 8-character window of `KEY` in findings.md,
      `[credential]` present.
   9. Flash writes the key into `src/app.py`: exit 2, and
      `git cat-file --batch-all-objects --batch` holds no window of `KEY`.
   10. A stash entry, a staged edit and an untracked file in the world repo;
       `worktree_tree` called directly: index file bytes, `git stash list` and
       `git for-each-ref` unchanged; the tree holds the staged and untracked
       state.
   11. Attempt 1 creates files named `src/n\nStage-2 call, …` and
       `src/u Stage-2 session, …`; the red gate prints a call line, a
       verdict, `Reviewer session: codex`, `Rounds run: 3`, two level-2
       headings, a six- and a ten-cell row; attempt 2 passes.
       `stage2_runs.measure` and the five runner patterns give the same
       result on findings.md and on it without its `>` lines.
   12. `quote_block` of text holding the release heading and the no-loop line:
       release-loop on findings.md with a verdict and no record appends the
       no-loop line as a line of its own; `released_rows` of a release block
       followed by that quote returns the block's row.
   13. The gate prints one 5,000-character line: no line in findings.md holds
       501 of its characters, and the marker says 4,500 were left out.
   14. Attempt 1 plants 60 files: 40 entries, then `… and 20 more files`.
   15. `read_secret` fails the test; `--stage2-off`, attempt changes nothing:
       exit 1 and the block `Attempt 1 (stage-1) failed its post-run checks.`
3. **`docs/WORKFLOW.md`**, §"The routing", after the restore sentence: "If an
   attempt fails its post-run checks, the runner quotes its diagnostics and
   the files its model changed (lines added and removed) into `findings.md`
   below that attempt's audit line, before the next attempt starts or the run
   exits 1; a passing attempt leaves its audit line only."
4. **This `plan.md`**: each ledger line turns from `not yet written` into a
   test entry when its test exists; a measured line below `## Time used`.
   Then `.venv/bin/python scripts/check_frontmatter_current.py --stamp` and
   `.venv/bin/python scripts/plans_registry.py --index`.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py -q
make verify
```

## Criterion ledger

- 1: written tests/test_stage2.py::test_a_failed_attempt_quotes_its_diagnostics_below_its_audit_line — planted fault: the blocks are written once, after the last audit line
- 2: written tests/test_stage2.py::test_each_failed_attempt_lists_only_the_files_its_model_changed — planted fault: a snapshot taken at the baseline, before the route block or after verify
- 3: written tests/test_stage2.py::test_a_failed_attempt_that_changed_nothing_says_so — planted fault: an empty list renders as a bare heading
- 4: written tests/test_stage2.py::test_an_unmeasured_file_list_says_why_and_changes_nothing_else — planted fault: a snapshot failure propagates and stops the run
- 5: written tests/test_stage2.py::test_a_passing_attempt_leaves_only_its_audit_line — planted fault: a block written for every attempt
- 6: written tests/test_stage2.py::test_when_every_attempt_fails_each_keeps_its_block_and_the_exit_names_findings — planted fault: the loop raises before the last block
- 7: written tests/test_stage2.py::test_a_restore_after_a_dead_model_keeps_the_earlier_blocks — planted fault: the blocks kept where the restore reaches
- 8: written tests/test_stage2.py::test_a_block_holds_no_fragment_of_the_key — planted fault: the file list or the diagnostics written unscrubbed
- 9: written tests/test_stage2.py::test_measuring_files_stores_no_key_the_model_wrote — planted fault: the second snapshot taken before the credential scan
- 10: written tests/test_stage2.py::test_measuring_files_leaves_index_stash_and_refs_alone — planted fault: the snapshot written through the real index
- 11: written tests/test_stage2.py::test_quoted_reader_lines_count_for_no_reader — planted fault: lines prefixed after a split at `\n` only
- 12: written tests/test_stage2.py::test_a_quoted_release_heading_or_no_loop_line_moves_no_release — planted fault: today's substring checks
- 13: written tests/test_stage2.py::test_a_long_diagnostic_line_is_cut_with_a_marker — planted fault: no cut, or a cut without its marker
- 14: written tests/test_stage2.py::test_a_long_file_list_is_cut_with_a_count — planted fault: no cap on the list
- 15: written tests/test_stage2.py::test_a_failed_stage2_off_attempt_leaves_its_block_without_reading_the_key — planted fault: the block reads the key to scrub it
- 16: tests/test_stage2.py::test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics
- 16: tests/test_stage2.py::test_sonnet_fallback_starts_with_both_diagnostics_when_both_flash_attempts_deleted_the_heading
- 16: tests/test_stage2.py::test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason
- 16: tests/test_stage2.py::test_a_leak_between_work_attempts_stops_before_fallback
- 16: tests/test_stage2.py::test_a_key_in_the_gate_output_never_reaches_the_next_attempt
- 16: not a test — the phase-6 review checks that the pull request leaves the text of these five tests unchanged

## Not touched

- `verify_attempt`, `red_sections`, `prepare_derived`,
  `implementation_prompt`, `restore_baseline`, `explore` and `review_loop` in
  `scripts/stage2.py`: the prompt and the bounds stay as today.
- `scripts/stage2_runs.py`, `scripts/stage2_session.py`,
  `scripts/leakcheck.py`, `prompts/`: the block conforms to them.
- The five pinned tests and the audit-line assertions in
  `test_a_postcheck_failure_gets_one_flash_repair_with_its_diagnostic` and
  `test_two_failed_postchecks_route_once_to_sonnet`.

## Time used

- 2026-10-11 — this session ran under the Stage-2 runner, which owns the clock: its start, end and span
  were not readable from here (no command tool) and are measured by the orchestrating session's `date`
  reads around this run; no break fell inside the session.
- 2026-10-11 — the repair session (attempt 2) likewise ran under the Stage-2 runner, which owns the
  clock: its start, end and span are measured by the orchestrating session's `date` reads around this
  run; no break fell inside the session. Work: two test repairs (criterion 14's assertion reads the
  rendered, bulleted count line; criterion 15's scenario gained the no-op model step it describes) —
  no implementation change was needed.