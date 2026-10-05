---
title: "Plan — project-lock"
status: draft
implementation_status: none
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-ei0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, dependencies, lock, ci, python]
---

# Plan — project-lock

```text
For you:     one hash-checked lock for CI and `make verify`; every change checked under Python 3.11 and 3.12; run `make venv` once per checkout
Done when:   criteria 1–23 hold (tests, a push with a red 3.11 leg and a red `verify`, then both legs green) and `make verify` is green
Appetite:    5 h of phase 4, one repair round included
Not now:     the harness/ foundation (s6i), the release lock (dj9), pinning actions and the rest of tqa, LakeSwitch's own lock
Pre-mortem:  suppose it failed: most likely because the summary job `verify` reports success while a leg is red, and main loses its one guard unnoticed
Starts unless you say stop.
```

Implements `spec.md` (criteria 1–23). The class is `feature` provisionally
(`decisions.md`, `[DECISION] 1`); the build below does not depend on the
answer, but `make verify` stays red on `adr-answers` until it is recorded.
Stage 1: no model markings. Facts read at `d5813ec`.

## Decided in phase 3

No new `[DECISION]`.

- `[DETAIL]` — **appetite 5 h:** about 4 h 20 min of steps below, the rest
  one repair round.
- `[DETAIL]` — **the CI change is pushed before the 3.11 repair** (steps 4
  and 6), so one push shows a red 3.11 leg and a red `verify` — the live
  evidence criterion 7 asks for. If the ADR answer is not recorded by then,
  the 3.12 leg is red too, on `adr-answers` alone; the step results per leg
  still show `pytest` red only under 3.11.
- `[DETAIL]` — **names:** matrix job `gates`, one leg per interpreter;
  step `setup-python` ("Set up the declared interpreter");
  the summary job keeps the id `verify` and has no `name:` (its id is the
  check's context). Constants in `scripts/ci_gates.py`: `MATRIX_JOB`,
  `SUMMARY_JOB`, `INSTALL`.
- `[DETAIL]` — **the runner changes into the repository root before it
  chooses**, so `.venv/bin/python3` is the checkout's own wherever the
  caller stood.
- `[DETAIL]` — **the committed lock is the one `make lock` writes on the day
  of step 1**; its transitive versions may differ from research 6.
- `[DETAIL]` — **the checks of `tests/test_lock.py` are functions of that
  module**, fed by the tests; no new script, so no caller, test or mutation
  ratchet moves.
- `[DETAIL]` — **the runner tests build their own tree** (copies of
  `scripts/verify_all.sh`, `scripts/ci_gates.py` and a gate file) with
  `HOME` set, `PYTHON` removed and a `PATH` of their own: under `make
  verify` the outer runner exports `PYTHON`, and the developer's `.venv`
  must not decide the result.

## Steps

Read `date` at each step boundary (`prompts/04-implement.md`).

1. **The project file and the lock** (25 min).
   - `pyproject.toml` (new): a comment block (what it is; the lock is made
     from it by `make lock`; nothing installs the project; neither file
     travels — `scripts/kit/manifest.yaml`), then `[project]` `name =
     "coding-harness"`, `version = "0.0.0"`, `requires-python = ">=3.11"`,
     `dependencies` = the four pins of criterion 1;
     `[dependency-groups]` `dev = ["pytest==8.3.4", "ruff==0.9.10"]`;
     `[tool.pytest.ini_options]` `pythonpath = ["."]`.
   - `Makefile`: targets `venv` (`python3 -m venv .venv`, then
     `.venv/bin/python3 -m pip install --require-hashes -r
     requirements-ci.txt`) and `lock` (`uv pip compile pyproject.toml --group
     dev --universal --generate-hashes --exclude-newer "$$(date -u
     +%Y-%m-%dT00:00:00Z)" -o requirements-ci.txt`), both in `.PHONY`, with
     a comment that names the bead and says the lock's first lines record
     the command.
   - `make lock` → `requirements-ci.txt` (new, generated; never edited).
   - `.gitignore`: `.venv/` under `# Python`.
   - `scripts/kit/manifest.yaml`: after the `requirements.txt` rule,
     `pyproject.toml` → `bestand`, reason "this repository's project file —
     its pins and its pytest settings; an instance declares its own, as
     LakeSwitch does (bead coding-harness-ei0)".
   - `provenance.yaml`: after the `CHANGELOG.md` entry, an English comment
     and `pyproject.toml` → `allowed: [human-written, ai-drafted-reviewed]`,
     `requirements-ci.txt` → `allowed: [machine-rendered]`, both
     `frontmatter: none`.
   - `make venv`. Commit.
2. **`tests/test_lock.py`** (new, 40 min). Module docstring: it reads this
   repository's lock, which does not travel. Functions:
   `lock_pins(text) -> dict[str, tuple[str, str | None]]` (normalised name →
   version and marker; entries start in column 0 as `name==version`),
   `pin_problems(specs, locked) -> list[str]`,
   `environment_problems(locked, installed, interpreter, declared) ->
   list[str]` (a marker that does not apply is skipped, with
   `packaging.markers`). Every message ends with "build the locked
   environment: make venv (or set PYTHON to an interpreter built from
   requirements-ci.txt)". `declared` comes from `ci_gates.interpreters()`
   (step 3; until then the test is written against it and fails). Tests in
   the table below. Commit after step 3.
3. **The gate file and the generator** (50 min).
   - `decisions/gates.yaml`: `tools:` becomes `python: ["3.11", "3.12"]`
     with a comment (oldest first; the verify job runs once per entry, the
     drift job on the last; package versions live in `pyproject.toml` and
     `requirements-ci.txt`); `ruff` and `pytest` leave.
   - `scripts/ci_gates.py`: `validate_schema` refuses what criterion 10
     names; `interpreters() -> list[str]`; `generate_ci` writes job `gates`
     (the old verify job's `if:`, `strategy: {fail-fast: false, matrix:
     {python: [...]}}` with quoted versions, checkout, `setup-python` with
     `python-version: ${{ matrix.python }}`, `setup-deps` running `INSTALL`,
     the hydration, the gate steps), then job `verify` (`needs: gates`,
     `if: always() && (github.event_name == 'push' || github.event_name ==
     'pull_request')`, `runs-on: ubuntu-latest`, one step "Every leg of the
     gates passed" whose `run: |` echoes `needs.gates.result` and runs
     `test "${{ needs.gates.result }}" = success`), then `drift` with
     `setup-python` on the last interpreter and the same `setup-deps`. New
     comments in English; existing German ones stay.
   - `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`.
     Commit with step 2.
4. **`tests/test_ci.py` for the CI** (40 min).
   `test_every_gate_step_runs_even_after_a_failing_gate` skips
   `ci_gates.SUMMARY_JOB` and asserts that job holds no gate step; new tests
   in the table. Run the suite, commit, **push**, read the check runs
   (Verification, evidence 1). Expected: the 3.11 leg red at the
   collection of `tests/test_research_currency.py`, `verify` red.
5. **The runner** (45 min). `scripts/verify_all.sh`: the `cd` to the root
   moves above the choice; the choice block becomes English: `$PYTHON` if
   set, else the first of `.venv/bin/python3` and `python3` that imports
   `yaml`; none → stderr "no python3 with PyYAML — build the locked
   environment with make venv, or set $PYTHON", exit 2; then `export
   PYTHON`. The runner tests in the table, in `tests/test_ci.py` section 2.
   Commit.
6. **The 3.11 repair** (10 min). `scripts/check_research_currency.py`:
   `_GLIMPSE = reprlib.Repr()`, then the six limits as attributes, with a
   comment that keyword arguments exist from 3.12 only. Run the 3.11 check
   (Verification). Commit, push; read the check runs (evidence 2).
7. **What readers are told** (15 min). `AGENTS.md`, "Sessions across
   checkouts", the worktree bullet: "Each new checkout or worktree runs
   `make venv` once before `make verify`; the suite fails under an
   interpreter that does not match `requirements-ci.txt` (bead
   coding-harness-ei0)." `docs/WORKFLOW.md` §8, the `uv`, `mypy` row, after
   its sentence: "`uv` only compiles that lock from `pyproject.toml` (`make
   lock`); CI and the local runner install it with pip and never call uv."
   If pull request #60 has merged, also take `requirements-ci.txt` out of
   the "not in this repository" list at the top. Then `python3
   scripts/check_frontmatter_current.py --stamp`.
8. **Close** (25 min). `implementation_status: partial` in the four
   artefacts here, `python3 scripts/plans_registry.py --index`, the
   verification below, evidence under `## Evidence` here. Commit, push.

## Tests

| Criterion | Test | Goes red when (planted fault) |
| --- | --- | --- |
| 1 | read once in phase 5: `tomllib` on `pyproject.toml` against the six pins | one pin edited |
| 2 | `test_every_pin_of_the_project_file_is_exact_and_locked`; `test_a_range_or_a_stale_pin_goes_red` — fed `pydantic>=2.13`, `pydantic==2.13.4` and a pin the lock lacks | the `==` check or the version comparison removed |
| 3 | evidence 3 | the lock edited by hand |
| 4 | `test_every_declared_interpreter_gets_a_leg` — the matrix equals `interpreters()`, also with it monkeypatched to three versions; every verify gate is a step of `gates` | the matrix written as a literal |
| 5 | `test_the_toolchain_comes_only_from_the_lock` — every `run` with `pip install` in `ci.yml` equals `INSTALL`, once per job that installs | a package named, `--require-hashes` dropped |
| 6 | `test_every_job_sets_a_declared_interpreter_before_installing` | `setup-python` after `setup-deps`, or missing in `drift` |
| 7 | `test_the_summary_check_passes_only_when_every_leg_passed` — `needs`, `always()` and the events in its `if`; its step run by `sh` with the result `success`, `failure`, `cancelled`, `skipped`: exit 0 only for `success`; `fail-fast` off — and evidence 1 | `always()` dropped, `!= failure` instead of `= success`, `fail-fast` on |
| 8 | evidence 2 | a second job named `verify`, or none |
| 9 | `test_the_drift_job_runs_once_on_the_last_interpreter` | a matrix in `drift`, the first interpreter |
| 10 | `test_the_schema_rejects_a_malformed_interpreter_list` — `"3.12"`, `[]`, `["3.x"]`, a duplicate, a key `ruff` | one check removed from `validate_schema` |
| 11 | `test_the_runner_never_searches_other_environments` (exit 2 with PyYAML only under `$HOME/.venvs/`); `test_the_runner_prefers_the_checkouts_own_environment` (wrappers log which ran) | the old candidate list back; `python3` before `.venv` |
| 12 | the first test of 11 also reads stderr for `make venv` and `PYTHON` | another exit code or message |
| 13 | `test_the_runner_hands_its_interpreter_to_every_gate` — a one-gate file whose command exits 1 without `PYTHON` | `export PYTHON` removed |
| 14 | `test_the_environment_matches_the_lock`; `test_a_drifted_package_goes_red` — fed pydantic 2.10.6 and no Jinja2 | a version compared by prefix, a missing package skipped, the hint dropped |
| 15 | `test_an_undeclared_interpreter_goes_red` — fed `3.13` | the interpreter check removed |
| 16 | evidence 4 | `--require-hashes` dropped from the target |
| 17 | `test_the_repository_root_is_on_pytests_path` (`pytestconfig.getini("pythonpath")`) | `pythonpath` removed from `pyproject.toml` |
| 18 | the 3.11 check below, and evidence 2 | the `reprlib` keywords back |
| 19 | `test_the_lock_and_the_project_file_stay_home` in `tests/test_lock.py` — `probe.rolle()` is `bestand` for both, and no rule of `scripts/export/manifest.yaml` but the catch-all matches them | a `mechanismus` rule for either |
| 20 | gate `leerprobe` after `make venv`; `git check-ignore -q .venv/bin/python3` | the `.gitignore` line removed |
| 21 | read once in phase 5: the longest `provenance.yaml` prefix for each file | an entry removed |
| 22, 23 | read once in phase 5 (`grep`) | — |

## Verification

```bash
make venv
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
```

Python 3.11 on the laptop (step 6, criterion 18), in a scratch directory:

```bash
python3.11 -m venv "$TMPDIR/v311" && "$TMPDIR/v311/bin/python3" -m pip install -q --require-hashes -r requirements-ci.txt
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false PYTHON="$TMPDIR/v311/bin/python3" bash scripts/verify_all.sh
```

Evidence, pasted under `## Evidence` with the commit:

1. After step 4's push, `gh api repos/MPAdesso/coding-harness/commits/<sha>/check-runs --jq '.check_runs[] | [.name, .conclusion] | @tsv'` —
   the 3.11 leg failure, `verify` failure. How GitHub names a leg was not
   read (research 4); the output records it.
2. After step 6's push, the same, and
   `--jq '[.check_runs[] | select(.name == "verify") | .check_suite.id] | group_by(.) | map(length)'`
   — every count 1; both legs' `pytest` steps succeed.
3. `eval "$(sed -n '2s/^#    //p' requirements-ci.txt)" && git diff --exit-code requirements-ci.txt`.
4. `rm -rf .venv && make venv && .venv/bin/python3 -m pytest tests/test_lock.py -q`.

## Not touched

`scripts/kit/probe.py` (`REIST_NICHT` and `DECKEL` stay: the new tests in
`tests/test_ci.py` build their own trees and hold in the probe copy,
`tests/test_lock.py` is `bestand`), `scripts/export/manifest.yaml` (its
catch-all drops both files), `OHNE_AUFRUFER`, `OHNE_TEST` and
`OHNE_MUTATIONSTEST` (no new script or gate), `ruff.toml` (already
`py311`), `README.md`, `tools/`, the ruleset on `main`, the German text of
`scripts/verify_all.sh` outside the rewritten block and the German reason of
the `requirements-ci.txt` kit rule, `scripts/new_change.py` (its mention of
`requirements-ci.txt` becomes true), `lakeswitch-ai`, and the files of
`feat/hermes-runner`.

## Deviations

- **2026-10-05, orchestrating session — `[DECISION] 1` is still open.** The
  class (`feature` with ADR "no", or `bounded`; `decisions.md`) is not answered
  yet. The build is the same under either answer, so phase 4 starts and
  phase 7 waits for the answer. No ADR answer is recorded in phase 4 (house
  rule 8). `make verify` stays red on the gate `adr-answers` alone until the
  maintainer answers; every other gate must be green.
- **2026-10-05, orchestrating session — Actions may be degraded.** GitHub
  Actions had degraded performance on 2026-10-05 (runs queued without a
  runner). If the live proof of step 4 cannot get a runner, evidence 1 reads
  "not run — Actions degraded" with the run id, and the work continues; it is
  not faked. The live ruleset is not touched.
- **2026-10-05, phase 4 — three tests outside the plan's list had to move
  with the schema** (assumption "only `tests/test_ci.py` reads the CI job
  names and the gate file's shape" did not carry; `[DETAIL]`, no change to the
  solution). The new `tools` check makes `validate_schema` refuse a gate file
  without `tools`, so three hand-made gate files in `tests/test_gate_machinery.py`
  (writer-only, hosted-only, action without a local equivalent) gain a
  `tools: {python: ["3.11", "3.12"]}` line; and two existing tests of
  `tests/test_ci.py` that read `jobs.verify` now read `ci_gates.MATRIX_JOB`
  (`test_a_local_equivalent_derives_its_arguments_from_the_action`,
  `test_drift_job_runs_on_schedule_and_dispatch_only`).
- **2026-10-05, phase 4 — two planned test names renamed** (`[DETAIL]`).
  `test_the_mutation_ratchet_only_turns_one_way` counts a test whose name
  contains `goes_red` or `refuses` as mutation evidence for every gate script
  its file mentions; `tests/test_ci.py` mentions `plans_registry.py`, so the
  two planned names would have struck `plans-registry` and
  `plans-registry-strict` off the ratchet without a seeded red run (a false
  "long since covered"). The names became
  `test_the_summary_check_passes_only_when_every_leg_passed` and
  `test_the_schema_rejects_a_malformed_interpreter_list`; the table below
  carries them.
- **2026-10-05, phase 4 — the hint of `pin_problems`** (`[DETAIL]`). The plan
  says every message ends with the `make venv` hint; a pin problem is mended
  first by `make lock`, so its message reads "regenerate the lock with make
  lock, then build the locked environment: make venv (…)" — it still ends
  with the hint.
- **2026-10-05, phase 4 — the runner also puts the chosen interpreter's
  directory on `PATH`** (step 5; `[DETAIL]`, added, reasoned here). Assumption
  that did not carry: "`make venv`, then `make verify` is green". A `.venv`
  that is not activated is not on `PATH`, and two callers use a bare `ruff`
  (`scripts/ramp_valves.py`, one test of `tests/test_ci.py`): from a plain
  shell the gates `pytest` (`test_the_ramp_valve_check_runs_green_here`) and
  `ramp-valves` went red with `FileNotFoundError: 'ruff'`, while the same
  checkout was green with the venv's `bin` on `PATH` — the laptop of the
  plan's author had the portfolio venv's `bin` there, which hid it. The
  runner now prepends the directory of a chosen interpreter that is not on
  `PATH` already (so `source .venv/bin/activate` is not needed), and the new
  test `test_the_runner_puts_the_chosen_environments_tools_on_the_path` holds
  it. The alternative — `[sys.executable, "-m", "ruff"]` in those two callers
  — was not taken: it fixes two callers, not the class. Reversible by
  deleting the block.

## Time used

2026-10-05 23:08 — span 1 started (read from `date`); the closing line of the
span is appended when it ends.
