---
title: "Research — red-first-install"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-omp
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, red-first]
---

# A missing Pi install counts as red in the red-first check — Research

Phase 1 for bead coding-harness-omp, seeded by the orchestrating session on
2026-10-16 against `origin/main` at `6029bbf`.

## The question

The phase-6 round-2 review of the pi-pin change (2026-10-15) found that
`red_first` in `scripts/stage2.py` checks out the baseline with
`git worktree add`. That checkout has no `tools/pi/node_modules` (ignored by
git), so `require_installed_pi` fails the real-Pi tests with exit 1, and the
check counts that as red. Measured then in a scratch copy:
`test_real_opencode_provider_contracts` ends in ERROR with pytest exit 1 when
`node_modules` is absent. Effect: test-only repairs of real-Pi tests that pass
on the baseline code pass red-first without any real red run. Needed (bead
text): the baseline check must see the pinned install, or count only an
assertion failure as red, with a test that a missing install is not red.

## Known so far (read, not run)

- Related beads: coding-harness-0ho (red-first exception for test-only fixes,
  in phase 4 on `explore/guard-test` since 2026-10-16, which also changes the
  red-first path) and coding-harness-y17 (test-strength findings have no
  red-first form).
- `tools/pi/install.sh` installs the pinned Pi into `tools/pi/node_modules`
  (ADR 0019); the runner's scratch checkouts do not run it.

## To explore

1. Where `red_first` builds the baseline checkout, how it runs the tests there
   and how it decides red versus green (exit code, outcome parsing).
2. Which other ignored files a baseline checkout misses that tests need
   (`.venv`, generated files, `node_modules`), and how other runner checkouts
   (draft, implement attempts) provide them.
3. The two fix directions: give the baseline the pinned install (link or copy
   the main worktree's `node_modules`, or run `install.sh`) versus classify
   outcomes so only a failed assertion is red (setup errors, skips and
   collection errors are not). Which is smaller and which is safer.
4. How the change must coordinate with 0ho's red-first changes on
   `explore/guard-test` to avoid a conflict in the same function.
5. Which tests cover `red_first` today, so a test with a missing install can
   follow them.

Stage-2 call, 2026-10-16: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 463 files, 1314 commits, 12 rules.

## Runner exploration — 2026-10-16
### What exists today

**The red-first proof, end to end.** `red_first` (`scripts/stage2.py`, function `red_first`, called from `check_repair_answer` at the `red_first(ctx.root, baseline, …)` line, with `baseline` taken once as `rev-parse HEAD` of the runner's root before the attempts begin) builds a scratch checkout: a temp directory prefixed `stage2-red-`, then `git worktree add --detach <tree> <baseline>`; it replaces the checkout's `tests/` with the attempt's `tests/` (copytree ignoring `__pycache__` and `.pytest_cache`), snapshots every ref, pre-checks that the interpreter can `import pytest`, then runs exactly the named test with `pytest -q -p no:cacheprovider <file>::<function>` under a `RED_FIRST_MINUTES` (= 10, module constant) limit. Red is `done.returncode in (1, 2)` — the message reads "pytest ended N on the baseline's code; red first is exit 1 or 2". Cleanup removes the worktree, prunes, and any ref difference before/after fails the proof without deleting anything.

**What travels into the scratch and what does not.** The scratch is a git checkout at the baseline commit, so only tracked files are in it; `.gitignore` marks `tools/pi/node_modules/` as never tracked ("rebuildable with `bash tools/pi/install.sh`"). No code copies ignored files into the scratch: a repo search of `scripts/` for `node_modules` finds nothing. The interpreter is the one compensation: `red_first_python(root)` returns the runner's own root `.venv/bin/python3` when executable, else `sys.executable` — pytest availability comes from the worktree, not the scratch. The child environment is `foreign_env`, whose allow-list (`ENV_ALLOW`) passes `PATH` among `HOME`, `TMPDIR`, `TERM` and six others, so `node` is reachable in the scratch run.

**The failing chain, link by link.** `tests/test_pi_contract.py` resolves `REPO_ROOT` from its own file and inserts `scripts/` into `sys.path`, then imports `stage2` — in a scratch run every path resolves into the scratch tree. `require_installed_pi` (same file) fails via `pytest.fail` — the suite never skips — when `node` is off `PATH`, when the wrapper file is missing, or when `tools/pi/pi --version` ends non-zero or prints anything but the pin; it runs the wrapper from a temp cwd, but the wrapper resolves its install from its own directory (`dir=$(dirname "$0")`, then `$dir/node_modules/@earendil-works/pi-coding-agent/…`), so the scratch tree's missing `node_modules` is what fails. The module-scoped fixture `installed_pi` wraps `require_installed_pi`, and ten `@pytest.mark.usefixtures("installed_pi")` sites hang real-Pi tests off it; a fixture failure errors every one of them, and the run ends exit 1 — inside `red_first`'s red window.

**The measurement on record.** The pi-pin phase-6 review measured this in the main tree, not in a scratch checkout: with `node_modules` moved away, `test_real_opencode_provider_contracts` ends in an ERROR with pytest exit 1 (pi-pin `findings.md`, the MINOR row on `red_first` × `require_installed_pi`; its own verdict line: CONFIRMED for the exit-1 mechanism, PLAUSIBLE for the runner path, "which I did not run"). The seed research records a second measurement of the same exit-1 outcome. Nothing in this session ran pytest; the chain above is code-read, the exit code is the two recorded measurements.

**Where the install comes from today.** `tools/pi/install.sh` runs `npm ci --ignore-scripts` into `tools/pi/node_modules` (ADR 0019, decision items 1–4). CI runs it in both toolchain jobs before pytest (`.github/workflows/ci.yml`, the two `bash tools/pi/install.sh` steps); the Makefile has no `install.sh` or `node_modules` reference — local provisioning is the documented fresh-clone step in `tools/pi/README.md`. This worktree itself holds a real install (`tools/pi/node_modules/@earendil-works/*/package.json` present, seven packages) and a `.venv` with pytest, so a repair run from here passes the runner's own wrapper preflight (`stage2.py`, the `PI_WRAPPER --version` check before the loop's first call; `PI_WRAPPER` resolves from `REPO_ROOT` = the running script's parent-of-parent, i.e. the worktree the runner runs in — the scratch tree is never consulted there). `tools/pi/pi`, the wrapper, is tracked, so it exists in the scratch checkout — only its runtime graph does not.

**Existing coverage of `red_first`.** In `tests/test_stage2.py`: the exit-0 fault (criterion 18, "pytest ended 0 … red first is exit 1 or 2"), the interpreter that cannot start pytest (phase-6 F-1, with a planted `.venv` whose python exits 1 — the run fails instead of reading startup failure as red), no worktree left behind (criterion 19), a ref created during the run (F-6), a moved ref (F-7), a failed `worktree remove` named in the outcome (direct call form: `stage2.red_first(world.root, baseline, …)`), and the prompt-text test that pins the words "red first" in the repair prompt. The helper worlds are `repair_world` / `seed_tests` / `repair_step` / `script_repair` (synthetic repos with a committed `tests/`), plus `FIX_TEST` and the comment that a repair standing on an earlier run's commit needs a fix that commit does not carry.

**Related work in the tree.** coding-harness-y17 (test-strength rows have no red-first form) has research on `explore/test-strength-rows` per the 2026-10-14 handover, waiting on the then-open #138. coding-harness-0ho appears nowhere in this worktree except the seed's mention: no `plans/changes/guard-test/` directory exists here, and the branch list in the common git directory is not readable from this worktree (the file tools refused the path outside it). The seed's statement that 0ho also changes the red-first path therefore has no corroboration here.

### What is unclear

1. What 0ho's branch `explore/guard-test` changes inside `red_first` — the branch content is unreadable from this worktree; only the seed states the overlap.
2. The bead text of coding-harness-omp is known only through the seed's quote; the tracker database under `.beads/` was not read.
3. Whether any test needs the other git-ignored paths (`.beads/issues.jsonl`, `.stage2-sessions/`, `lychee/`) inside a scratch checkout is unexamined; of the ignored paths, only `tools/pi/node_modules` is demonstrably read by the suite and only `.venv` is compensated today.
4. The pytest exit code of a fixture-error run in a scratch checkout rests on the two recorded measurements (both exit 1); no statement in code fixes 1 versus 2 — the runner counts both as red either way.
5. How the pi-pin MINOR row became bead coding-harness-omp is tracker history, not in the tree.

### Files a change would have to touch

- `scripts/stage2.py` — `red_first` (the whole function is the seam: the checkout step that builds the scratch, and the outcome classification `if done.returncode not in (1, 2)`); `red_first_python` (the interpreter seam); the `RED_FIRST_MINUTES` constant nearby. A search finds no other reader of `red_first`.
- `tests/test_stage2.py` — a new test beside the existing red-first tests, on the `repair_world`/`script_repair` worlds or the direct-call form.
- `tests/test_pi_contract.py` — where the failing behavior lives (`require_installed_pi`, the `installed_pi` fixture); relevant if a change classifies outcomes rather than provisioning the scratch, not otherwise.

