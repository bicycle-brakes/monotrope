---
title: "Plan — stage2-runs-count"
status: accepted
implementation_status: done
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-kw0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, measurement]
---

# Plan — stage2-runs-count

```text
For you:     One command repeats the stage-2 run counts at any commit; the note and WORKFLOW §4 carry its output.
Done when:   Criteria 1–9 have tests with planted faults, 10 a git diff, make verify is green, Codex reviewed it, a PR is open.
Appetite:    2 hours; a stop, not an estimate.
Not now:     Tokens and cost per vendor, a runner change, closing the bead.
Pre-mortem:  suppose it failed: most likely because a findings file uses a shape the rows of the four runs do not show.
Starts unless you say stop.
```

## Decided in phase 3

- [DETAIL] Implemented by the orchestrated session (Claude Code with
  Anthropic, Opus 5.5), not through `stage2.py implement`: a new change
  folder still trips the derived-file gap a file-tool worker cannot clear
  where `plans/INDEX.md` must be regenerated, and the session holds the
  formats in context already.

## Steps

1. `scripts/stage2_runs.py`: imports `stage2` and uses `split_row`,
   `ROW_COLUMNS`, `RELEASED_COLUMNS`, `LOOP_ID`, `VERDICT_LINE`,
   `SEVERITIES`, `CODEX`/`GLM`/`GLM_FLASH` and `declaration_problem`; a
   pure `measure(findings, research)` returning the counts, a `locate` for
   the folder, a reader for `--rev` (`git show <rev>:<path>`), and `main`
   printing the table and the criterion lines.
2. `tests/test_stage2_runs.py`: one test per criterion on fixtures in
   `tmp_path` (a temporary git repository for `--rev` and criterion 4);
   each with its planted fault noted in the plan's time log.
3. `scripts/ci_gates.py` `OHNE_AUFRUFER`: the script with its reason (an
   entry point a person runs, not a gate).
4. Run the script over the four runs at `HEAD`; paste the output unchanged
   into a dated addendum of the note; WORKFLOW §4 names the command and
   the criteria numbers with their cut-off.

Verification: `make verify`.

## Time used

2026-10-08 21:31–21:42 UTC, 11 min, orchestrator clock (Claude Code with
Anthropic, Opus 5.5): research, spec, plan, the script, nine tests, the
addendum and WORKFLOW §4. Twelve planted faults (archive suffix match, first
of two archives taken, undecided row dropped, `rejected` read as taken,
`Broke a test` read on loop rows only, a 2a row counted as phase 6, rounds
fixed at one, any mark counted, `research.md` not read, a blocked call
counted clean, `--rev` reading the tree, a route without residency counted
cleared) each turned its test red. Criterion 10 is held by `git diff` of
the note, not by a test.

2026-10-08 21:42–22:05 UTC, 23 min, orchestrator clock, the GLM loop's
two rounds included (their wait is not separated). Repairs in that time: loop
round 1 took L1-1, L1-2, L1-4 and L1-5 (one new test,
`test_rev_decodes_git_output_as_utf_8_whatever_the_locale`); round 2 took
L2-1, L2-2 and L2-3 (two new tests, `test_rev_lists_an_archived_folder_name_whole`
and `test_a_findings_file_that_is_not_utf_8_exits_2_without_a_traceback`),
twelve tests in all. Each new test went red under its planted fault.

Phase 6 round 1 (Codex, 2026-10-09) raised four BLOCKERs, all taken and
repaired with a test each that its planted fault turned red (F-1 every table
with the column, F-2 a prefixed call line that does not parse, F-3 `--rev`
resolved once, F-4 a malformed declaration reported, not raised); seventeen
tests in all. The span of this repair was interrupted by a session limit
and is not clocked.

Phase 6 round 2 (Codex, 2026-10-09) raised two BLOCKERs on the F-1 repair
(F-5 a header without `ID` first, F-6 a header carried past a heading), both
taken and closed by one test red under both planted faults; eighteen tests.
2026-10-09 02:53–03:05 UTC, about 12 min, orchestrator clock, Codex's wait
included.

Phase 6 round 3 (Codex, 2026-10-09) raised F-7 (a body row whose first cell
is `ID`) and F-8 (a body row of dashes, origin `fix-r4`); both taken and
closed by one test, red under both planted faults; nineteen tests. Two
consecutive `fix-r` rounds: escalated by naming the reader's limits in the
spec instead of a fourth round. 2026-10-09 03:06–03:15 UTC, about 9 min,
orchestrator clock, Codex's wait included.
