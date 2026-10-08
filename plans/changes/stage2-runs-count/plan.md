---
title: "Plan — stage2-runs-count"
status: draft
implementation_status: partial
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
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
Done when:   Each criterion has a test with a planted fault, make verify is green, Codex reviewed it, a PR is open.
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
