---
title: "Spec — attempt-diagnostics"
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
tags: [spec, stage-2, runner, implement, diagnostics]
class: bounded
appetite: 3
---

# Spec — `attempt-diagnostics`

After this change, every implement attempt that fails its post-run checks
leaves in `findings.md`, right below its own audit line, why it failed and
which files its model changed (bead coding-harness-cit). Research:
[`research.md`](research.md). Decisions: [`decisions.md`](decisions.md) —
Q-1, answered by the maintainer: both the diagnostics and a per-attempt file
list with lines changed per file.

## Problem

Each point read in `research.md` ("Runner exploration — 2026-10-11", against
`scripts/stage2.py` at `a6b7150`; "Readers of findings.md — phase 2",
at `b48e740`).

- `implement` builds a failed attempt's diagnostics — the red gates with
  their last lines, a preparation failure, a missing `## Time used` line —
  only for the next attempt's prompt, then drops them. On 2026-10-11 the
  implement run of change criterion-test-ledger failed twice on GLM 5.3 Flash;
  its `findings.md` says only "first Flash post-run check failed" and "two
  Flash post-run checks failed".
- When every attempt fails, the runner exits 1 with "implementation post-run
  checks failed after the allowed attempts"; the diagnostics are in neither
  the message nor any file.
- Which attempt wrote which file is unrecorded: a failed post-run check does
  not restore the tree, the next attempt builds on it, and one checkpoint
  commit follows the passing attempt. Whether GLM can implement (bead
  coding-harness-rwa) cannot be judged from what is left.
- Three readers of `findings.md` match their marker anywhere in the text, not
  at the start of a line (`release`, `released_rows`, `fill_marks`); quoted
  gate output that holds the marker would be taken for the runner's own line.

## Terms

- **Attempt**: one route of `implement` — the model call, then the runner's
  post-run checks (derived-file preparation, `make verify`, the
  `## Time used` check).
- **Audit line**: the `Stage-2 call, …` line the runner writes into
  `findings.md` before each attempt.
- **Files the attempt's model changed**: the difference between the worktree
  right before the attempt's model call and right after it, as git counts it
  for files git does not ignore.
- **Block**: what one failed attempt leaves in `findings.md`. Every line of it
  begins with `>` (a Markdown quote); an empty line is `>` alone. Its shape:

  ````text
  > Attempt 2 (flash-repair) failed its post-run checks.
  >
  > Files the attempt changed (lines added, removed):
  > - `src/app.py` +1 -1
  > - `assets/logo.png` binary
  > - … and 3 more files
  >
  > Diagnostics:
  > ```text
  > - `make verify` exited 1
  > The gates that blocked, each with its last lines:
  > ── [pytest] $ python3 -m pytest tests/ -q
  > …
  > - `plan.md` did not add a measured line below `## Time used`
  > ```
  ````

  With no file changed, the file part is the one line `Files the attempt
  changed: none.`; when it cannot be measured, `Files the attempt changed: not
  measured — <reason>.` The diagnostic lines are those the next attempt's
  prompt receives for the attempt, after its `Attempt <n> (<route>):` line;
  their count stays what `verify_attempt` bounds today (at most 80 lines for a
  preparation failure; red sections at most 200 lines plus 40 of standard
  error; otherwise the last 80 lines).

## Acceptance criteria

1. When an implement attempt fails its post-run checks, `findings.md` holds
   that attempt's block directly below its audit line, and the block quotes
   every line of the diagnostics the next attempt's prompt receives for it.
   *Refuted by:* a run whose first two attempts fail, where a red gate's
   section or the missing `## Time used` line reaches the third prompt but not
   `findings.md`, or where both blocks stand after the last audit line.
2. When an attempt fails its post-run checks, its block lists every file the
   attempt's model created, changed or deleted, each with the lines added and
   removed as `git diff --numstat` counts them (`binary` where git counts
   none), and no other file.
   *Refuted by:* attempt 2's list naming a file only attempt 1 changed,
   missing a file attempt 2 deleted, naming `plans/INDEX.md` that the
   derived-file preparation rendered, or counting the runner-route block in
   `plan.md` for the Stage-1 attempt.
3. When a failed attempt's model changed no file, its block says the attempt
   changed none.
   *Refuted by:* a file heading with no entry under it.
4. If an attempt's files cannot be measured, its block says `not measured`
   with the reason, and the run goes on and exits as it would have without
   the file list.
   *Refuted by:* a measurement failure that stops the run, changes its exit
   code or its commit, or reads as `none`.
5. When an attempt passes its post-run checks, `findings.md` gains that
   attempt's audit line and nothing else from that attempt.
   *Refuted by:* a block or any other line after the passing attempt's audit
   line, whether it passed first or after a failed attempt.
6. If every allowed attempt fails its post-run checks, `findings.md` holds the
   block of each attempt, the last one included, and the runner exits 1 with a
   message that names `findings.md`.
   *Refuted by:* three failed attempts leaving two blocks, or a failure
   message that does not name `findings.md`.
7. If a later attempt's model process fails and the runner restores the
   worktree to the baseline, the blocks of the earlier failed attempts stay in
   `findings.md`.
   *Refuted by:* the restore removing a block an earlier attempt wrote.
8. If the GLM key, whole or as a fragment of 8 or more characters, occurs in
   an attempt's diagnostics or in the name of a file it changed,
   `findings.md` holds `[credential]` in its place and no 8-character fragment
   of the key.
   *Refuted by:* any 8-character window of the planted key in `findings.md`
   after a run whose gate printed the key and whose model created a file named
   with a fragment of it.
9. If a GLM attempt writes the key into a file's content, the runner refuses
   as today before it measures that attempt's files, and no object in the
   repository holds a fragment of the key.
   *Refuted by:* `git cat-file --batch-all-objects --batch` showing an
   8-character window of the planted key after the refusal.
10. When the runner measures an attempt's files, the repository's index file,
    its stash and its refs are unchanged.
    *Refuted by:* a staged change lost or added, a stash entry added or
    dropped, a ref moved, or other bytes in the index file.
11. When a block quotes a line a reader of `findings.md` looks for — one that
    starts `Stage-2 call, `, `Stage-2 session, `, `Phase 6 verdict:`,
    `Reviewer session: codex` or `Rounds run:`, a `## ` heading or a table
    row — `scripts/stage2_runs.py` counts and the runner reads `findings.md` as
    if the block were absent, also when the quoted line follows `\n` or U+2028
    inside a file name.
    *Refuted by:* `stage2_runs.measure` returning other counts with the block
    than without it, or `SESSION_LINE`, `ROUNDS_LINE`, `VERDICT_LINE`,
    `VERDICT_START` or `ROUND_HEADING` matching inside the block.
12. When a block quotes the release heading or the no-loop line, release-loop
    still appends the no-loop line for a change without a loop record, and the
    loop rows are read from the release block the runner wrote.
    *Refuted by:* release-loop leaving out the no-loop line because a block
    holds it, or `released_rows` returning no row because a block after the
    release block quotes its heading.
13. When a diagnostic line or a file entry is longer than 500 characters, its
    line in the block keeps the first 500 and then says how many characters it
    left out.
    *Refuted by:* a 5,000-character gate line reaching `findings.md` whole, or
    cut without the marker.
14. When an attempt changed more than 40 files, its block lists 40 and then
    says how many more there are.
    *Refuted by:* 60 changed files all listed, or 40 listed without the count.
15. While `--stage2-off` is given, the runner does not read the GLM key, and a
    failed attempt still leaves its block.
    *Refuted by:* `read_secret` called on that route, or a failed
    Stage-1-only attempt without a block.
16. When the next attempt starts, its prompt, its leak check and its route are
    those of today, so the five tests that pin the retry chain pass with their
    text unchanged: `test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics`,
    `test_sonnet_fallback_starts_with_both_diagnostics_when_both_flash_attempts_deleted_the_heading`,
    `test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason`,
    `test_a_leak_between_work_attempts_stops_before_fallback` and
    `test_a_key_in_the_gate_output_never_reaches_the_next_attempt`.
    *Refuted by:* one of the five failing, or the pull request editing one.

## Non-goals

- **The passing attempt's file list.** The bead's acceptance asks that a
  passing attempt leave only its audit line; the checkpoint commit shows the
  result.
- **A failed model process.** It keeps today's record: its standard-error tail
  on the runner's standard error and the restore message in the exit-1 line.
  A bead brings it back if a dead process's reason must outlive the terminal.
- **Explore and the review loop.** Explore makes one call and runs no
  post-run check; the loop runs one round per invocation and keeps no failed
  round (`research.md`, "Runner exploration").
- **The prompt.** What the next attempt receives and how `verify_attempt`
  bounds it stay as they are; the 500-character cut and the quote apply to
  `findings.md` only.
- **Cleaning up after a failed run.** A failed post-run check still leaves
  the tree as the attempt left it; nothing is restored or committed.
- **Ignored files and file names in the credential scan.** A file git ignores
  is not listed; the scan still covers it as today. The scan reads contents,
  not names, here as at the checkpoint: a key in a file *name* is scrubbed
  from `findings.md` (criterion 8) but may stand in the repository's objects.
- **Rewriting the diagnostics.** Beyond the scrub, the cut and the quote,
  their text is kept as the gate printed it; an absolute path stays one.

## Protected areas

- `prompts/` — `human-written` in `provenance.yaml`; the implement prompt
  needs nothing from this change.
- `scripts/stage2_runs.py`, `scripts/stage2_session.py`,
  `scripts/leakcheck.py` — the block is shaped for their reading; none of them
  changes.
- `verify_attempt`, `red_sections`, `prepare_derived` and
  `implementation_prompt` in `scripts/stage2.py` — the prompt stays as today
  (criterion 16).
- `decisions/` and `docs/adr/` — nothing here is a maintainer's decision.

## Definition of Done

- `verify` green.
- Moved in the same pull request: `docs/WORKFLOW.md`, section "The routing" —
  one sentence on the block; the module docstring of `scripts/stage2.py`.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes coding-harness-cit, and its last commit
  carries the trailer `Closes-Bead: coding-harness-cit`
  (`prompts/07-commit.md`).
- Special runs: none.

## Open decisions

None open. Q-1 is answered (`decisions.md`). The points below are reversible
and bind nothing beyond this change, so this phase decided them; each carries
its reason.

- `[DETAIL]` **Every line of the block begins with `>`**, after splitting with
  `str.splitlines()`. One mark defeats every line-anchored reader at once — a
  call line, a heading, a verdict, session or rounds line, a table row that
  `split_row` would read after stripping — without changing them, and the
  split covers every line boundary any reader uses.
- `[DETAIL]` **The diagnostics stand in a fenced code block inside the
  quote**, its fence one backtick longer than the longest backtick run they
  contain. Gate output holds `<…>`, `__x__`, `*` and `|`, which Markdown would
  hide or reformat.
- `[DETAIL]` **Files first, diagnostics second.** The list is at most 42
  lines, the diagnostics up to about 250; the long part last cannot bury the
  short one.
- `[DETAIL]` **The files are measured as git trees**: one snapshot right
  before the model call, one right after it and after the existing credential
  scan, each written through a temporary index (`GIT_INDEX_FILE`) seeded from
  `HEAD`, compared with `git diff-tree --numstat`. The counts are git's own;
  the real index, the stash and the refs are never touched; the runner's
  writes before the call (audit line, route block) and after it (preparation,
  block) fall outside both snapshots.
- `[DETAIL]` **The snapshots leave unreachable objects in the object store.**
  Accepted: the checkpoint's own `git add -A` writes the same kind, git's
  garbage collection prunes them, the leak check's stated scope excludes
  objects no ref reaches, and the second snapshot runs after the credential
  scan, so no blob holds the key (criterion 9).
- `[DETAIL]` **Bounds: 500 characters a line, 40 files.** A gate can print one
  line of megabytes; a pytest assertion line with its values rarely passes
  500. Forty files cover a bounded change; more is itself the finding.
- `[DETAIL]` **Under `--stage2-off` the block is not scrubbed of the GLM key.**
  The rule that a Stage-1-only run never reads the key is pinned by two tests,
  and no process of that run is given the key.
- `[DETAIL]` **The three readers that match anywhere read only at the start of
  a line.** The runner writes those markers only at line starts; a pytest
  failure quoting them is realistic exactly when the runner implements a
  change to itself.
- `[DETAIL]` **The block is written right after `verify_attempt`, before the
  post-run credential scan.** The scan then covers the block too, and an
  attempt refused for a key its gate wrote keeps its diagnostics.
- `[DETAIL]` **The exit-1 message names `findings.md` and prints no
  diagnostics.** Three blocks can reach about 900 lines; the maintainer chose
  the file as their place.
