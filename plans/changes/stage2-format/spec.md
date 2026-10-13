---
title: "Spec — stage2-format"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-52r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, runner, implement, formatting]
class: bounded
appetite: 3
---

# Spec — `stage2-format`

After this change, the runner applies ruff's safe fixes and then its formatter
to the change's Python files under `scripts/` and `tests/` before each
`make verify` of an implement attempt, so that no attempt fails on formatting
a work model cannot run, and a reader sees what the runner changed (bead
coding-harness-52r). Research: [`research.md`](research.md), including its
"Phase 2 additions". Decisions: [`decisions.md`](decisions.md) — Q-1,
answered by the maintainer: `ruff format` and `ruff check --fix` with safe
fixes only, never `--unsafe-fixes`; the ADR question answered no; class
`bounded`.

## Problem

Read in `research.md` against `feat/stage2-format` on 2026-10-12 (`2412930`,
phase 2 additions at `9be21fb`).

- The work models cannot run a formatter: `implement` gives them the file
  tools `Read,Grep,Glob,Edit,Write` (`WORK_WRITE_TOOLS` in
  `scripts/stage2.py`) and no command tool.
- Both ruff gates block, and both only check: `python3 -m ruff check scripts/
  tests/` and `python3 -m ruff format --check scripts/ tests/`
  (`decisions/gates.yaml`). Between the model call and `make verify`,
  `verify_attempt` runs the derived-file preparation and nothing that writes a
  fix.
- In change stage2-repair (bead coding-harness-g2f), every implement attempt —
  GLM 5.3 Flash, its repair, the Sonnet 5.5 fallback — and every attempt of
  the new `repair` verb failed `make verify` on `ruff-format` or `ruff-check`
  alone. The orchestrator then ran `ruff format` by hand, and `make verify`
  went green.
- So a run spends all three attempts on what a tool does in a second, and each
  repair prompt asks the next model for a formatting it cannot run either.

## Terms

- **Target files**: of the paths the runner's `changed_paths` returns —
  tracked changes against `HEAD` and untracked files git does not ignore —
  those that end in `.py`, lie under `scripts/` or `tests/`, and are a regular
  file at their own path: not a symbolic link, resolving inside the worktree
  to that same path, with one hard link. They are what the two ruff gates
  measure, narrowed to the change.
- **Format step**: the two ruff commands of criterion 1, run inside
  `verify_attempt` after the derived-file preparation succeeded and before
  `make verify`. An attempt runs the step when its preparation succeeded and
  it has target files.
- **Format line**: what one format step leaves, in one line — the target files
  whose bytes the step changed, or that it changed none; that `ruff check`
  left findings without a safe fix, when it exited 1; that a ruff command
  exited with another non-zero code, and which; or, instead of all of these,
  `not run` and why.

## Acceptance criteria

1. When an implement attempt's derived-file preparation succeeds and it has
   target files, the runner runs `.venv/bin/ruff check --fix
   --no-unsafe-fixes --force-exclude --no-cache <targets>`, then
   `.venv/bin/ruff format --force-exclude --no-cache <targets>`, and only then
   `make verify`.
   *Refuted by:* the recorded calls in another order, a ruff argument list
   other than these two (a flag added or missing, `--unsafe-fixes` anywhere),
   a third ruff call, or `make` recorded before a ruff call.
2. When the format step runs, the files it names to ruff are exactly the
   attempt's target files.
   *Refuted by:* a ruff argument naming a `.py` file outside `scripts/` and
   `tests/`, a file that is not `.py`, a deleted file, a committed file the
   change did not touch, a directory, a symbolic link or a file with a second
   hard link — or a target file left out.
3. When an attempt has no target file, no ruff process starts.
   *Refuted by:* a recorded ruff call in a run whose model changed only files
   outside `scripts/` and `tests/` (ruff without a path walks the whole tree,
   `research.md`, phase 2 additions).
4. When the format step runs, the ruff it starts is the worktree's own
   `.venv/bin/ruff`, also when another `ruff` stands on `PATH`.
   *Refuted by:* the `ruff` on `PATH` being started.
5. When the format step runs, each ruff process gets the environment
   `make verify` gets, which holds no model credential and no caller variable
   outside the allow-list.
   *Refuted by:* the GLM key, `ANTHROPIC_AUTH_TOKEN`, `GH_TOKEN`,
   `OPENAI_API_KEY` or `X_SECRET` in a recorded ruff environment.
6. When the format step changes a file, that change is not in the failed
   attempt's file list.
   *Refuted by:* attempt 1's entry counting the lines ruff wrote instead of
   those its model wrote, or attempt 2's block naming a file that only the
   format step changed during attempt 2.
7. When an attempt that ran the format step fails its post-run checks, the
   first entry of its diagnostics is its format line, so that its block in
   `findings.md` and the next attempt's prompt both carry it.
   *Refuted by:* a failed attempt's block or the next prompt without the
   format line, the format line as a later entry, or a format line naming a
   target file that ruff left byte for byte as it was.
8. When an implement run passes, its checkpoint commit's message is the
   subject `feat(<change>): implement accepted plan` followed by the format
   line of every attempt of the run that ran the format step, each with its
   attempt number and route — and the subject alone when none did.
   *Refuted by:* a passing run after a format step whose commit message lacks
   that attempt's format line, holds a line for an attempt that ran no format
   step, carries a body although no attempt ran one, or changes the subject.
9. When an attempt passes after its format step changed a file, `findings.md`
   gains nothing after that attempt's audit line.
   *Refuted by:* any line after the passing attempt's audit line.
10. If ruff cannot be started, exits non-zero or leaves findings without a safe
    fix, the attempt passes or fails exactly as `make verify` and the time
    check decide.
    *Refuted by:* a run whose `make verify` is green and whose plan gains its
    time line, but which fails the attempt, starts a further attempt, skips
    `make verify` or exits other than 0.
11. If ruff cannot be started — no `.venv/bin/ruff` in the worktree, or the
    system refuses to run it — the attempt's format line says `not run` and
    why.
    *Refuted by:* a format line for such an attempt that names changed files,
    says no file changed, or gives no reason.
12. If a format line holds the GLM key, whole or as a fragment of 8 or more
    characters, the checkpoint commit message holds `[credential]` in its
    place.
    *Refuted by:* any 8-character window of the planted key in the commit
    message after a run whose formatted target's name holds a fragment of it.

## Non-goals

- **Formatting beyond the targets**: unchanged files, the whole tree, other
  directories, `.pyi` files or notebooks. The gates measure `scripts/` and
  `tests/`, which held no `.pyi` or `.ipynb` file on 2026-10-12 and were clean
  at `9be21fb`; a gate that widens its paths brings this back.
- **Unsafe fixes**, preview rules, and any other ruff option or rule selection
  (Q-1).
- **A ruff outside the worktree's `.venv`**: no fallback to `PATH`, to the
  runner's own interpreter or to another checkout.
- **Changing what measures**: the gates, `ruff.toml`, `scripts/verify_all.sh`,
  the lock and the pinned ruff 0.9.10.
- **Criteria for the `repair` verb** (pull request #131, bead
  coding-harness-g2f, not merged on 2026-10-12). The step lives in
  `verify_attempt`, which `repair` calls too, so its attempts are formatted
  once both changes are merged; the plan says how the format line reaches its
  record. A bead brings repair-specific criteria back.
- **New terminal output.** The format line is written where a reader looks
  afterwards — the block, the commit — and the run prints nothing new.
- **A time limit on ruff**: none, as for the index renderer and `make verify`.

## Protected areas

- `decisions/gates.yaml`, `scripts/verify_all.sh`, `Makefile`, `ruff.toml`,
  `pyproject.toml`, `requirements-ci.txt` — the gates measure as before; the
  step is the runner's, not theirs.
- `prompts/` — `human-written` in `provenance.yaml`; the implement prompt
  needs nothing from this change.
- In `scripts/stage2.py`: `prepare_derived`, `attempt_block`, `quote_block`,
  `attempt_files`, `worktree_tree`, `red_sections` and
  `implementation_prompt` — the block keeps its shape and the prompt its
  builder; the format line arrives as a diagnostic.
- Every existing test in `tests/test_stage2.py`, the `world` fixture and
  `STAND_IN` among them — this change adds tests and one helper and edits
  none.
- `decisions/` and `docs/adr/` — class `bounded`, no ADR (`decisions.md`).

## Definition of Done

- `verify` green.
- Moved in the same pull request: `docs/WORKFLOW.md`, §"The routing" — one
  sentence on the format step; the module docstring of `scripts/stage2.py` and
  the docstring of `verify_attempt`.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes coding-harness-52r, and its last commit
  carries the trailer `Closes-Bead: coding-harness-52r`
  (`prompts/07-commit.md`).
- Special runs: none.

## Open decisions

None open. Q-1 and the ADR question are answered (`decisions.md`). The points
below are reversible and bind nothing beyond this change, so this phase
decided them; each carries its reason.

- `[DETAIL]` **The worktree's `.venv/bin/ruff`, by that relative path, and
  nothing else.** The ruff gates run `.venv/bin/python3 -m ruff`, which
  `verify_all.sh` chooses first and which starts the same binary; a `ruff` of
  another version from `PATH` could write a format the pinned gate rejects. A
  worktree without `.venv` is not ready for `make verify` anyway (`AGENTS.md`:
  `make venv` first). A path with a slash is never looked up on `PATH`, and the
  relative spelling keeps the machine's absolute paths out of the format line.
- `[DETAIL]` **`check --fix` before `format`.** A fix can leave code the
  formatter must settle (an unused import removed, imports re-sorted), and the
  formatter's output is what the `ruff-format` gate measures.
- `[DETAIL]` **`--no-unsafe-fixes` spelled out.** The maintainer's "never
  unsafe" (Q-1) then holds even if a configuration sets `unsafe-fixes = true`.
- `[DETAIL]` **`--force-exclude` spelled out.** `ruff.toml` sets it; on the
  command line it holds whatever the configuration says — the protection the
  comment in `ruff.toml` explains (the vendoring surface was once reformatted
  by a direct call).
- `[DETAIL]` **`--no-cache`.** Measured: the step then leaves no
  `.ruff_cache`; its only writes are the target files, which the checkpoint
  commits and the post-run credential scan covers.
- `[DETAIL]` **Targets are the changes against `HEAD`, not this attempt's file
  list.** The checkpoint commits every change against `HEAD` and the gates
  measure all of it; an attempt's list can be unmeasured; the derived-file
  preparation reads the same set; and formatting is idempotent, so a file an
  earlier attempt's step formatted stays as it is.
- `[DETAIL]` **Links and hard-linked files are left out without a word.**
  Measured: ruff writes through a link, out of the worktree; the preparation
  refuses the same shapes for held documents. The work models' file tools
  cannot create links, and `make verify`'s ruff gates name any such file that
  stays unformatted.
- `[DETAIL]` **What the step changed is measured by comparing each target's
  bytes before and after it** — not from ruff's output, which gives counts,
  and not with git, which would write objects.
- `[DETAIL]` **A failed attempt's format line is the first entry of its
  diagnostics**, not a new part of the block: the block keeps the shape change
  attempt-diagnostics gave it (bead coding-harness-cit), and the next model
  learns that the runner formats and whether ruff left findings it could not
  fix. It stands first because the step ran first.
- `[DETAIL]` **A passing run's format lines go into the checkpoint commit's
  message**, not into `findings.md`: criterion 5 of change attempt-diagnostics
  keeps a passing attempt to its audit line, and the commit is where the
  formatted bytes land.
- `[DETAIL]` **The step runs after the derived-file preparation.** When the
  preparation fails, `make verify` does not run and the step would serve
  nothing; and since no held document is Python, nothing the preparation
  writes depends on the step.
