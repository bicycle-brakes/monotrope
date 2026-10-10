---
title: "Research — interview-minimums"
status: accepted
implementation_status: done
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-6yg
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: cline, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, interview, gates, workflow]
---

# interview-minimums — Research

What exists today around the phase-1a interview, the gates that could hold it,
and the machinery a check would reuse. Authored by the directing session
(Cline) rather than through the stage-2 explore runner: the maintainer directed
this session to run the workflow end to end, and stage 2 stays reserved for the
prescribed reviews (2a, 4b, 6). Every statement names where it came from; the
tree was read on branch `feat/interview-minimums` at `cc020f5` (2026-10-08).

## What exists today

### The interview phase and its optionality

- `prompts/01a-interview.md`, header block: "**Optional**, and called by a
  human. Where the change fits in one sentence, skip it". Its gate: "every
  `[DECISION]` answered, or the phase recorded as skipped with a reason".
- `docs/WORKFLOW.md`, §2 phase table, row 1a, and the paragraph after it:
  "Phase 1a is **optional and called by a person**. What fits in one sentence
  needs no interview; skipping it is given a one-sentence reason in
  `decisions.md`, not left unsaid."
- `AGENTS.md`, "The workflow in one screen" table, row 1a: "Interview
  *(optional, human-called)* | `plans/changes/<name>/decisions.md` | every
  `[DECISION]` answered — or skipped with a reason".
- The question protocol — `[DECISION]` ask · `[GAP]` read · `[DETAIL]` decide —
  stands twice: `prompts/01a-interview.md` ("How you ask") and
  `prompts/02-spec.md` ("Classify before you ask"). Consequences per
  `docs/WORKFLOW.md`, "Who decides what": intent is the person's, detail is the
  agent's.
- The recorded form: one entry per decision, a Y-statement with its date
  (`prompts/01a-interview.md`, "What you write"); agent decisions belong there
  too, "marked as such". A `decisions.md` template does not exist —
  `templates/` holds adr, arc42, design, findings, gate-record, handover and
  spec only (directory listing, 2026-10-08).
- Real records vary in shape: `plans/changes/harness-decide-adr/decisions.md`
  keeps a numbered "## Answers" list plus "## Details left to the agent";
  `plans/changes/runner-derived-files/decisions.md` records one-line
  `[DETAIL]` paragraphs, among them "[DETAIL] Interview skipped: scope is the
  requested deterministic repair; there is no open human intent question.
  Feature/ADR minimums do not apply." — the proposal is already anticipated in
  practice, nothing measures it.

### Change classes and the ADR question

- `docs/WORKFLOW.md`, §"Change classes, the ADR question and decision pull
  requests": four classes (`spike`, `bounded`, `feature`, `architectural`) in
  the spec header (`class:`); phase 2b goes by class (decision D-14); "Only a
  `feature` owes an answer to the ADR question"; the answer lives in
  `decisions/answers/<change>/adr.yaml`; the gate `adr-answers`
  (`scripts/check_adr_answers.py`, declared in `decisions/gates.yaml`) holds
  every feature, active or archived, to an answer file.
- `scripts/check_adr_answers.py`: `CLASSES` tuple, `_CLASS_LINE` regex reads
  `class:` from the spec frontmatter, walks `plans/changes/` including
  `archive` (`CHANGES_DIR`, `ARCHIVE`); exits 0 (nothing found) / 1 (findings)
  / 3 (`CannotMeasure` — the gate cannot answer). Its docstring states the
  limit this change inherits: it "reads the files of the tree, offline, and
  cannot see who wrote an answer or who merged it. The maintainer's merge … is
  what gives it effect" (ADR 0008).

### Where a check would live

- `decisions/gates.yaml` is the one gate list (D-10; `schema_version: 2`).
  Gate fields: `id`, `title`, `command`/`action`, `job` (verify|drift),
  `enforcement` (advisory|report|block), `floor`, `placement`
  (hosted|writer|both), `needs_tracker`, `needs_history`, `reason`. The
  existing gate `adr-answers` runs `python3 scripts/check_adr_answers.py`,
  job verify, enforcement block, placement both.
- `scripts/ci_gates.py` derives everything from that file: `gates()`,
  `validate_schema()`, `generate_ci()` writes `.github/workflows/ci.yml`, and
  the `ci-drift` gate holds the workflow to the file. `make verify` runs
  `scripts/verify_all.sh`, which asks `ci_gates.py`; the Makefile holds no
  list of its own.
- Test precedents: `tests/test_check_adr_answers.py` (checker exercised with
  `--root` trees), `tests/test_gate_machinery.py`, `tests/test_ci.py`.

### The diff machinery a file-based check would reuse

- `scripts/stage2.py`, `change_diff(root)`: base = `git merge-base HEAD
  origin/main` (raises `Refused` when there is none), then `git diff <base>` —
  which covers committed, staged and unstaged state, because it compares the
  base against the working tree — plus untracked files appended as
  `--no-index` diffs against `/dev/null`. Docstring: "The diff against the
  merge base with origin/main, uncommitted and untracked files included."
- `scripts/stage2.py`, `changed_paths(root)`: a second, HEAD-based variant
  (`diff --name-only HEAD` plus untracked) — not merge-base-aware.
- `scripts/ci_gates.py`, `report()` computes `git merge-base origin/main HEAD`
  — for its report only; it is a base-computing precedent, not a
  changed-files detector.
- `needs_history`: `scripts/ci_gates.py`, `_checkout()` gives gates that
  declare it a `fetch-depth: 0` checkout; without history a gate says so with
  exit 3 instead of guessing (`scripts/check_frontmatter_current.py` message;
  bead coding-harness-qd7).
- On `main` after a merge, `merge-base(HEAD, origin/main)` equals `HEAD`, so a
  base diff would be empty. No gate today derives a base for a post-merge run;
  stage 2 runs on worktrees only. A base rule per context is new and must be
  specified, not assumed.

### What is not there (distinct from not found)

- `scripts/validate_change_artefacts.py` does **not exist** in the tree (find
  over the repository, 2026-10-08) although `prompts/02-spec.md` names it in
  its gate line, `docs/WORKFLOW.md` §"Who decides what" credits it, and
  `scripts/plans_registry.py` (comment near `_praesenz_ramp`) references it.
  The change-artefact validator is an open bead: coding-harness-jc3 (P2).
  Specs are therefore held today by `plans_registry.py --check` plus review,
  not by that validator.
- Nothing in the tree counts interview questions: a grep over `scripts/` and
  `tests/` for "interview" returns no symbol (2026-10-08); the word appears
  only in prompts, docs, journal and research prose.

### Where the maintainer's rules stand

- `docs/journal/handover/2026-10-08-runner-derived-files.md`, closing
  addendum: "the phase-1 research swarm and mandatory feature/ADR interviews
  (at least three/five substantive questions) are not implemented by this PR"
  — the proposal is recorded as separate pending work. This change is that
  work (bead coding-harness-6yg, created and claimed 2026-10-08, actor
  `cline-interview-minimums`).
- The ten rule decisions of 2026-10-08 — three given by the maintainer, seven
  asked and answered in the directing conversation — are recorded in this
  change's `decisions.md`.

### Provenance boundaries for the files to change

- `provenance.yaml`, `paths:`: prefix `prompts/` allows `[human-written]`;
  `AGENTS.md` allows `[human-written]`; `docs/WORKFLOW.md` allows
  `[human-written, ai-drafted-reviewed]`; `docs/adr/` is `[human-decided]`;
  `decisions/answers/` is `[human-decided]`. `decisions/gates.yaml` is
  unmapped, and the file header says an unmapped path is an INFO gap of the
  map, never an error of the file.
- Consequence: prompt and AGENTS text is prepared by this session and confirmed
  by the maintainer; the merge is the confirmation (ADR 0008). `docs/adr/` is
  not touched by this change, so no decision pull request is triggered by the
  provenance map.

## What is unclear

Nothing that blocks the spec. All ten rule decisions are made
(`decisions.md`, 2026-10-08). One limit is stated rather than resolved: the
gate counts documented human answers; their actual origin is unverifiable by
design — the merge confirms them, as `check_adr_answers.py` already states.

## Files a change would have to touch

| File | Why |
|---|---|
| `prompts/01a-interview.md` | mandatory-by-class rules, the minimum counts, the machine-readable question record |
| `prompts/02-spec.md` | the spec gate gains the interview check, run before the spec passes |
| `docs/WORKFLOW.md` | phase table row 1a and the paragraph after it; the "Change classes…" section; the stage-1 table row for enforcement |
| `AGENTS.md` | the workflow table row 1a |
| `scripts/check_interview_minimums.py` | new gate script, modelled on `check_adr_answers.py` (exit 0/1/3) |
| `tests/test_check_interview_minimums.py` | new, modelled on `tests/test_check_adr_answers.py`, including the counterexample matrix |
| `decisions/gates.yaml` | the new gate entry; `.github/workflows/ci.yml` regenerated via `ci_gates.py --generate-ci` |
| `templates/decisions.md` *(spec decides)* | the question-record format needs one authoritative home — a new template, or the prompt alone |
