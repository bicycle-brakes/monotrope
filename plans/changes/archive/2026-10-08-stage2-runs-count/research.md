---
title: "Research — stage2-runs-count"
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
tags: [research, stage-2, measurement]
---

# Research — stage2-runs-count

Phase 1. Facts read on 2026-10-08 at `origin/main` `cc020f5`.

[DETAIL] Explored by the orchestrated Claude Code session (Anthropic,
Opus 5.5), not through `stage2.py explore`: the session had already read
every file this note names to take the task, and a Flash pass would re-read
the same few files; earlier Flash calls in this repository hung for more
than 15 minutes (`plans/changes/stage2-session/findings.md`, first
implement attempt).

## What exists today

- **The typed count.** `docs/research/2026-10-08-stage2-three-runs.md`
  holds one table for the first three stage-2 runs (`stage2-session` #91,
  `runner-red-gate` #92, `touch-map-comments` #93), counted "by a throwaway
  script" that is not in the repository. Its acceptance gap is named in its
  own first paragraph: bead coding-harness-kw0 asks for metrics generated
  rather than typed.
- **The source of every number** is one file per change:
  `plans/changes/<name>/findings.md`, or the same file under
  `plans/changes/archive/<date>-<name>/` once archived. The three runs are
  still under `plans/changes/`; a fourth run, `runner-derived-files` (#102),
  is archived as `plans/changes/archive/2026-10-08-runner-derived-files/`.
  The three findings files on `main` are byte-identical to the commits the
  note measured (`git diff 51acbc3`, `c4d6831`, `a8bc676` over each file:
  empty).
- **What the runner writes there** (`scripts/stage2.py`):
  - `begin_call` / `begin_work_call`: one line per call,
    `Stage-2 call, <date>: <verb>[ · attempt …] · endpoint … · model … ·
    leak check clean over <n> files, <n> commits, <n> rules.` The line is
    written only after `checked_prompt` passed; a refused leak check raises
    `Refused` first, so **a refusal leaves no line**. Explore writes its
    line into `research.md`, not `findings.md`.
  - `stage2_session.audit_line`: `Stage-2 session, <date>: … · leak check
    clean over … · dispatch pending.` (then `accepted`/`failed`).
  - `answer_block`: Codex rows in `ROW_COLUMNS` (nine cells: ID, Severity,
    Dimension, Origin, Where, Finding, Reviewer, Status, Broke a test) under a
    heading `## Phase 2a — Codex, <date>` or `## Phase 6 — Codex, <date>`
    (the heading text is written by `spec_review`/`review`).
  - `review`: the line `Phase 6 verdict: codex <session>, <date>`, matched by
    `VERDICT_LINE`; one per phase-6 round (`touch-map-comments` and
    `runner-derived-files` have two).
  - `release`: the loop rows in `RELEASED_COLUMNS` (ten cells, the last one
    `Phase 6`) under `RELEASE_HEADING`, then `Rounds run: <n>` (`ROUNDS_LINE`,
    loop rounds of phase 4b, not phase-6 rounds), and `Kept from the loop
    record:` for answer text that was no row. `NO_LOOP_LINE` stands where no
    loop ran. Loop ids match `LOOP_ID` (`L<n>-<n>`).
  - `split_row` turns a table line into cells and respects `\|`.
  - `declaration_problem(root, endpoint, model)` says why
    `model-endpoints.yaml` does not clear a route, or `None`; the foreign
    routes are the constants `CODEX`, `GLM`, `GLM_FLASH`.
- **Status vocabulary actually used** (read from the four files): loop rows
  `taken — …` / `rejected — …`; Codex rows `closed — …`, `repaired — …`,
  `in spec — …`, `resolved — …`, `open`. `Broke a test` is `yes`, `no`, or
  `—` for a row not taken. `Phase 6` marks start `agree` or `disagree — …`.
- **D-13's four criteria** (`docs/architecture/target-architecture.md` §9,
  D-13; bead coding-harness-kw0): ≥ 3 full runs with metrics; lakeswitch-ai's
  disclosure decision written; leak check green in every run; the foreign
  endpoint declared with residency. ADR 0007 replaced criterion 1 by the
  three-run measurement, kept 3 and 4 as enforced on every call, and left
  criterion 2 to lakeswitch-ai (it governs content this repository never
  sends). `docs/WORKFLOW.md` §4 states this in prose; it carries none of the
  four as a number.
- **Script registration.** `tests/test_ci.py`
  `test_every_script_has_a_caller_or_a_declared_reason` requires every
  `scripts/*.py` to be called from `ci.yml` / `verify_all.sh` or listed in
  `scripts/ci_gates.py` `OHNE_AUFRUFER` with a reason.

## What is unclear

- **What a `Phase 6` mark agrees with.** `MARK_FORMAT` asks for
  `agree` or `disagree — <reason>` without saying whether the reviewer judges
  GLM's finding or the implementer's decision on it. In
  `runner-derived-files` all seven marks are `disagree`, and each reason
  says the row was resolved — they read as "the finding no longer stands",
  not as disagreement with the decision. A count of `disagree` marks
  therefore measures the mark, not necessarily a disagreement.
- **Text kept from the loop record** (`touch-map-comments`, one line
  `|R-3|…`) is a GLM finding that was not a row; it was neither taken nor
  rejected. A row count does not see it.
- **Not recorded anywhere:** tokens and cost per vendor, wall time per
  phase beyond hand-kept `## Time used` lines, human minutes.

## Files a change would touch

- new `scripts/stage2_runs.py` and `tests/test_stage2_runs.py`;
- `scripts/ci_gates.py` `OHNE_AUFRUFER` (one entry);
- `docs/research/2026-10-08-stage2-three-runs.md` (a dated addendum);
- `docs/WORKFLOW.md` §4, "Measuring the first three stage-2 runs".
