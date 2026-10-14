---
title: "Research — probe-untracked-files"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-fdz
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, runner, kit-probe, untracked-files]
---

# The kit probe misses an attempt's new files — Research

Phase 1 for bead coding-harness-fdz, read on 2026-10-14 against `origin/main`
at `3199a28` and the unmerged branch `origin/feat/codex-repairs` (pull
request #138) at `135cb8e`. Exploration only, during the night run; the
questions below wait for the maintainer.

## Result first

- The runner runs `make verify` on the attempt's worktree **before** anything
  is staged; the kit probe copies only what `git ls-files --cached` lists. A
  new file the model created is therefore absent from the probe's foreign
  repository, while the tracked test that imports it is present.
- The bug is the same on `main` and on pull request #138: that branch rewrites
  the attempt loop but keeps the order "verify, then `git add -A` in the
  checkpoint" unchanged.
- The smallest fix candidate is an intent-to-add (`git add -N`) of the
  attempt's untracked, non-ignored files right before `make verify`; measured
  in a scratch repository on git 2.55.0, it makes the file visible to
  `ls-files --cached` and keeps `restore` and `diff HEAD` working as today.

## The observed failure

Change adr-owning-change, 2026-10-13 (bead text; `plans/changes/adr-owning-change/findings.md`,
attempt block with "`make verify` exited 2"; `plan.md`, "Phase 4, 2026-10-13"):

- The Sonnet attempt under `--stage2-off` created `scripts/adoption.py`
  (untracked) and edited the tracked `tests/test_check_interview_minimums.py`,
  which imports it.
- The `leerprobe` gate reported "1 rote(r) Fall/Faelle ohne deklarierten
  Grund" (the module `::tests.test_check_interview_minimums` — a collection
  error) and "35 Eintrag/Eintraege in REIST_NICHT haben keinen Fall mehr".
  The 35 is a consequence: a collection error stops the whole pytest session,
  so no declared case was collected at all.
- The probe's own hint ("Nachtragen mit: python3 scripts/kit/probe.py
  --messen") points toward declaring the case as not travelling — the wrong
  repair.
- The plan records that staging the files made the gate green with no code
  change.

## What exists today

### The probe (`scripts/kit/probe.py`, same on both branches)

- `_ls_files` returns two sets: `--cached` (the index) and `--others
  --exclude-standard` minus the index. Its comment names the design: what is
  in the index is "what the commit will contain"; untracked files are only
  DRIFT, so a scratch note does not turn the gate red.
- `getrackte_dateien` → `nach_rolle` → `_baue`: only index entries with role
  `mechanismus` are copied into the foreign repository. Untracked files are
  classified (DRIFT when unclassified) but never copied.
- `decisions/gates.yaml`, gate `leerprobe`: title "The kit probe holds over
  the tracked tree", command `python3 scripts/kit/probe.py --strict` (DRIFT
  blocks too).
- The other gates that list files include untracked ones:
  `scripts/check_frontmatter_current.py` (`--cached --others`),
  `scripts/leakcheck.py` (`--cached --others`),
  `scripts/check_interview_minimums.py` (`--others`). The probe is the only
  one that leaves untracked files out of what it measures.

### The runner (`scripts/stage2.py`)

| Step | `main` @ `3199a28` | PR #138 @ `135cb8e` |
|---|---|---|
| attempt loop calls the check | `run_attempts`, `verify_attempt(...)` | `run_attempts`, `verify_attempt(...)` |
| `make verify` launched | `verify_attempt`, `launch(["make", "verify"], …)` | same function, unchanged order |
| first staging of the real index | `checkpoint`, `_git_output(root, "add", "-A")` | same |
| draft verb | `verify_draft`, `launch(["make", "verify"], …)`, no staging | same |

- `prepare_derived` and `format_step` run before `make verify`; neither
  stages anything.
- `worktree_tree` uses a temporary index (`GIT_INDEX_FILE`, seeded with
  `read-tree HEAD`, then `add -A`) to snapshot the tree; the real index is
  untouched. So the runner already knows how to see untracked files without
  staging them, but only for the "files this attempt changed" listing.
- `changed_paths` = `git diff --name-only HEAD` ∪ `ls-files --others
  --exclude-standard`; `restore_baseline` = `git restore
  --source=<baseline> --staged --worktree -- .` then `git clean -fdq`.
- `checkpoint` stages everything (`add -A`), so whatever untracked file
  `make verify` did not see does go into the commit — the gate measured a
  different tree than the one committed.

### Tests

- `tests/test_kit.py`: no test drives the probe over an untracked
  `mechanismus` file (searched for `unversion`, `untracked`, `others`).
- `tests/test_stage2.py`: `make` is a stand-in (`STAND_IN`, fixture `world`);
  it does not run the real probe. No test asserts what the index holds when
  `make verify` starts.

## Measured: intent-to-add on git 2.55.0

Scratch repository, 2026-10-14, one committed file `a`, one new file
`new.py` marked with `git add -N`:

- `git ls-files --cached` lists `new.py`; `git ls-files --others
  --exclude-standard` no longer does.
- `git diff --name-only HEAD` lists `new.py`, so `changed_paths` still
  returns it (from the other half of its union).
- `git status --porcelain` shows ` A new.py`.
- `git restore --source=HEAD --staged --worktree -- .` removed `new.py` from
  index and disk — the effect `restore_baseline` has today with its
  `git clean`.

Not measured: the probe itself over an intent-to-add file (it copies from the
worktree path, `REPO_ROOT / pfad`, so the content would be the current one;
read, not run), and `git add -N` on a path that is a symlink or a directory.

## Candidate fixes

1. **Runner marks new files intent-to-add before `make verify`**
   (`verify_attempt` and `verify_draft`).
   - For: the gate keeps its meaning ("the tracked tree"); the tree it
     measures equals the tree `checkpoint` commits; one small change in one
     file; the probe stays untouched.
   - Against: the runner now writes the real index before the commit; a
     failed run leaves ` A` entries instead of `??` (bead coding-harness-b5w,
     derived-leftovers, is about exactly those leftovers); a model-created
     file that should not be committed is still committed — that is true today
     as well.
2. **The probe copies untracked, non-ignored `mechanismus` files too.**
   - For: fixes the same class for a human who runs `make verify` before
     `git add`; no runner change.
   - Against: changes the declared meaning of the gate ("holds over the
     tracked tree"); a human's forgotten `git add` then goes green locally and
     red in CI — the class the `_ls_files` comment was written against
     (2026-09-08).
3. **The runner runs `make verify` under a temporary index**
   (`GIT_INDEX_FILE` with `add -A`, as `worktree_tree` does).
   - For: the real index stays untouched.
   - Against: the variable is inherited by every gate and by the pytest suite,
     whose tests run `git` in their own temporary repositories — a git in a
     test repository would read and write the runner's temporary index
     (reasoned from git's documented variable, not measured); `foreign_env`
     would have to pass it explicitly.
4. **An opt-in switch for the probe** (an environment variable the runner
   sets): copies untracked files only under the runner.
   - For: human behaviour unchanged.
   - Against: two modes of one acceptance gate; the probe's verdict then
     depends on who started it.

## Which files a change would touch

- Candidate 1: `scripts/stage2.py` (`verify_attempt`, `verify_draft`, maybe a
  helper next to `changed_paths`), `tests/test_stage2.py` (the `make`
  stand-in records `git ls-files --cached` when it starts), possibly
  `docs/WORKFLOW.md` where it describes the runner's post-run check.
- Candidate 2 or 4: `scripts/kit/probe.py` (`_ls_files`, `nach_rolle`,
  `_baue`), `tests/test_kit.py`, `decisions/gates.yaml` (gate title and
  reason).
- Either way, with PR #138 unmerged: whichever lands second rebases onto the
  rewritten `run_attempts`; `verify_attempt` itself is barely changed there,
  so the conflict surface is small.

## Questions this change has to answer

- [DECISION] Where the fix lives: the runner stages new files intent-to-add
  before `make verify` (candidate 1, recommended — the gate keeps its
  meaning and the measured tree equals the committed one), or the probe
  copies untracked files (candidate 2) with the gate's title changed.
- [DECISION] Whether this change waits for pull request #138 to merge, or
  lands first and #138 rebases (recommended: wait — #138 rewrites
  `run_attempts`, and this change is a few lines in `verify_attempt`).
- [GAP] Whether the probe, run for real over an intent-to-add `mechanismus`
  file, copies and collects it — one run in a scratch worktree settles it.
- [GAP] Whether `git add -N` behaves on a symlink, an empty directory or an
  ignored-but-forced path the model created; the runner's credential and
  hard-link guards may need to run first.
- [DETAIL] The intent-to-add covers `ls-files --others --exclude-standard`
  as `changed_paths` already computes it, nothing ignored — ignored files
  never go into the checkpoint either.
- [DETAIL] The test drives an attempt that adds a new imported module and
  asserts what the index lists when the `make` stand-in starts; the real
  probe is not run inside `tests/test_stage2.py`, because that suite fakes
  `make`.
