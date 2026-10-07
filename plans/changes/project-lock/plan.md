---
title: "Plan — project-lock"
status: draft
implementation_status: partial
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-06
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

## Planted faults

Every test has its counterpart: a fault planted on its own, the named test run,
the file restored (`git status` empty after each). Controls: before the faults
`python3 -m pytest tests/test_lock.py tests/test_ci.py tests/test_gate_machinery.py -q`
was green. Result: **47 faults, 47 red, none green.** Planted on `14c8a05`, the
head after the tests were written; the script is a scratch file
(`project-lock-plant.py`, the scratchpad of the session), not part of the change.

"Red" is the number of failing tests of the run named in the last column (for
faults run under Python 3.11.9, a collection error). Faults 1 to 42 were planted
by that script; 43 to 47 by hand (the lock, the `make venv` target, two reads).
Criteria 22 and 23 carry no planted fault (the plan's table has "—": a `grep`).

Two faults of the plan's table behave differently than it says:

- **Criterion 16, `--require-hashes` dropped (fault 44):** evidence 4 alone does
  **not** go red — pip checks hashes by itself as soon as the file carries one,
  so the same environment results. The plan's refutation ("`pytest
  tests/test_lock.py` failing right after `make venv`") cannot see the flag.
  `test_make_venv_installs_the_lock_in_hash_checking_mode` (added in phase 4,
  reads the recipe) is what goes red; fault 45 is the one evidence 4 catches.
- **Criterion 8:** the live check (evidence 2) shows the count of check runs
  named `verify`; the planted faults (15, 16) are held by the summary-check
  test, which reads the generated `ci.yml`.

| # | Crit. | File | Fault | Red | Tests that went red |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | test_lock | pin_problems: the exact-== check removed | 1 | `test_a_range_or_a_stale_pin_goes_red` |
| 2 | 2 | test_lock | pin_problems: the version comparison removed | 1 | `test_a_range_or_a_stale_pin_goes_red` |
| 3 | 4 | ci_gates | the matrix written as a literal in the generator | 1 | `test_every_declared_interpreter_gets_a_leg` |
| 4 | 5 | ci_gates | a package named in INSTALL (generator, ci.yml regenerated) | 1 | `test_the_toolchain_comes_only_from_the_lock` |
| 5 | 5 | ci_gates | --require-hashes dropped from INSTALL (generator, ci.yml regenerated) | 1 | `test_the_toolchain_comes_only_from_the_lock` |
| 6 | 5 | ci.yml | --require-hashes dropped by hand from one install line of ci.yml | 1 | `test_the_toolchain_comes_only_from_the_lock` |
| 7 | 6 | ci_gates | setup-python after setup-deps in the matrix job | 1 | `test_every_job_sets_a_declared_interpreter_before_installing` |
| 8 | 6 | ci_gates | setup-python missing in the drift job | 1 | `test_every_job_sets_a_declared_interpreter_before_installing` |
| 9 | 6 | ci_gates | setup-python with a version outside tools.python (drift: 3.13) | 1 | `test_every_job_sets_a_declared_interpreter_before_installing` |
| 10 | 7 | ci_gates | always() dropped from the summary job's if | 1 | `test_the_summary_check_passes_only_when_every_leg_passed` |
| 11 | 7 | ci_gates | the summary step passes on `!= failure` instead of `= success` | 1 | `test_the_summary_check_passes_only_when_every_leg_passed` |
| 12 | 7 | ci_gates | fail-fast on in the matrix job | 2 | `test_the_summary_check_passes_only_when_every_leg_passed`, `test_every_declared_interpreter_gets_a_leg` |
| 13 | 7 | ci_gates | the summary job does not need the matrix job | 1 | `test_the_summary_check_passes_only_when_every_leg_passed` |
| 14 | 7 | ci_gates | the summary job's if names no event (always() alone) | 1 | `test_the_summary_check_passes_only_when_every_leg_passed` |
| 15 | 8 | ci_gates | a second job named verify (the matrix job gets `name: verify`) | 1 | `test_the_summary_check_passes_only_when_every_leg_passed` |
| 16 | 8 | ci_gates | no job named verify (SUMMARY_JOB renamed) | 1 | `test_the_summary_check_passes_only_when_every_leg_passed` |
| 17 | 9 | ci_gates | a matrix in the drift job | 1 | `test_the_drift_job_runs_once_on_the_last_interpreter` |
| 18 | 9 | ci_gates | the drift job on the first interpreter | 1 | `test_the_drift_job_runs_once_on_the_last_interpreter` |
| 19 | 10 | ci_gates | validate_schema: the duplicate check removed | 1 | `test_the_schema_rejects_a_malformed_interpreter_list` |
| 20 | 10 | ci_gates | validate_schema: the key check (only python) removed | 1 | `test_the_schema_rejects_a_malformed_interpreter_list` |
| 21 | 10 | ci_gates | validate_schema: the 3.<n> form check removed | 1 | `test_the_schema_rejects_a_malformed_interpreter_list` |
| 22 | 10 | ci_gates | validate_schema: the non-empty list check removed | 1 | `test_the_schema_rejects_a_malformed_interpreter_list` |
| 23 | 10 | ci_gates | validate_schema: the tools block not checked at all | 1 | `test_the_schema_rejects_a_malformed_interpreter_list` |
| 24 | 11 | verify_all | the old candidate list back ($HOME/.venvs/*) | 1 | `test_the_runner_never_searches_other_environments` |
| 25 | 11 | verify_all | python3 on PATH before .venv/bin/python3 | 1 | `test_the_runner_prefers_the_checkouts_own_environment` |
| 26 | 12 | verify_all | another exit code (1) when no interpreter is found | 1 | `test_the_runner_never_searches_other_environments` |
| 27 | 12 | verify_all | the message without make venv | 1 | `test_the_runner_never_searches_other_environments` |
| 28 | 12 | verify_all | the message without $PYTHON | 1 | `test_the_runner_never_searches_other_environments` |
| 29 | 13 | verify_all | export PYTHON removed | 1 | `test_the_runner_hands_its_interpreter_to_every_gate` |
| 30 | 13+ | verify_all | the PATH block of the runner removed (my addition, step 5) | 1 | `test_the_runner_puts_the_chosen_environments_tools_on_the_path` |
| 31 | 14 | test_lock | a version compared by prefix | 1 | `test_a_version_is_compared_whole_not_by_prefix` |
| 32 | 14 | test_lock | a missing package skipped | 1 | `test_a_drifted_package_goes_red` |
| 33 | 14 | test_lock | the make venv hint dropped from the messages | 2 | `test_a_drifted_package_goes_red`, `test_an_undeclared_interpreter_goes_red` |
| 34 | 15 | test_lock | the interpreter check removed | 1 | `test_an_undeclared_interpreter_goes_red` |
| 35 | 16 | Makefile | --require-hashes dropped from the venv target | 1 | `test_make_venv_installs_the_lock_in_hash_checking_mode` |
| 36 | 17 | pyproject | pythonpath removed from pyproject.toml | 1 | `test_the_repository_root_is_on_pytests_path` |
| 37 | 18 | currency | the reprlib keywords back (run under Python 3.11) | collection error | `tests/test_research_currency.py` under 3.11.9 |
| 38 | 18 | ci_gates | a 3.12-only f-string in ci_gates.py (the nested quotes of the first push; run under 3.11) | collection error | `tests/test_ci.py` under 3.11.9 (SyntaxError) |
| 39 | 19 | kit manifest | a mechanismus rule for pyproject.toml in the kit manifest | 1 | `test_the_lock_and_the_project_file_stay_home[pyproject.toml]` |
| 40 | 19 | export manifest | an export rule that carries requirements-ci.txt | 1 | `test_the_lock_and_the_project_file_stay_home[requirements-ci.txt]` |
| 41 | 20 | .gitignore | .gitignore line .venv/ removed (git check-ignore) | exit 1 | `git check-ignore -q .venv/bin/python3` |
| 42 | 20 | .gitignore | .gitignore line .venv/ removed (probe --strict) | exit ≠ 0 | `python3 scripts/kit/probe.py --strict` |
| 43 | 3 | `requirements-ci.txt` | `pluggy==1.6.0` edited to `1.6.1` and staged (a hand edit), then evidence 3 run | `git diff --exit-code` exit 1 | evidence 3 |
| 44 | 16 | `Makefile` | `--require-hashes` dropped from `venv`, then evidence 4 (`rm -rf .venv && make venv && pytest tests/test_lock.py`) | 1 of 13 | `test_make_venv_installs_the_lock_in_hash_checking_mode` — the environment tests stay green: pip checks hashes by itself when the file carries them |
| 45 | 16 | `Makefile` | `venv` installs `pytest==8.3.4 PyYAML ruff==0.9.10 jinja2 pydantic` instead of the lock, then evidence 4 | 2 of 13 | `test_the_environment_matches_the_lock`, `test_make_venv_installs_the_lock_in_hash_checking_mode` |
| 46 | 1 | `pyproject.toml` (a copy) | `pydantic==2.13.5` → `2.13.4`, read once with `tomllib` against the six pins | read RED | the one-off read |
| 47 | 21 | `provenance.yaml` (a copy) | the `requirements-ci.txt` entry removed, longest-prefix read | read RED (no class) | the one-off read |

## Evidence

How GitHub names a leg (research 4 had not read it): `gates (3.11)` and
`gates (3.12)` — the matrix job's id and the version in parentheses.

**1. The push of step 4** (`c926bad`, run 37375079831; no pull request exists,
so one event only). Attempt 1 got no runner for the 3.11 leg in 15 minutes
(GitHub Actions degraded, an incident open that evening) and GitHub cancelled
it at 21:33:51 UTC: leg 3.11 `cancelled` (job 111981572725), leg 3.12 `failure`
(job 111981572478, one failed step: `adr-answers`), `verify` `failure` (job
111987336085). Attempt 2 is a rerun of that one job (`gh run rerun 37375079831
--job 111981572725`), same commit; it ran:

```text
$ gh api repos/MPAdesso/coding-harness/commits/c926bad6aa62c255da2bdabfb354409319ed09ac/check-runs --jq '.check_runs[] | [.name, .conclusion] | @tsv'
verify	failure
drift	skipped
gates (3.12)	failure
gates (3.11)	failure
```

The 3.11 leg (job 111987543865) failed in `The test suite passes` with three
collection errors — `tests/test_research_currency.py` (`TypeError:
Repr.__init__() got an unexpected keyword argument 'maxlevel'`, the known case)
and, **new**, `tests/test_ci.py` and `tests/test_lock.py` (`SyntaxError: f-string:
unterminated string`: the matrix line of `generate_ci` in `c926bad` reused its
own quotes inside an f-string, which Python 3.12 accepts and 3.11 does not) —
and in the kit probe, `gate-schema` and `ci-drift` on the same `SyntaxError`,
and in `adr-answers`. The 3.12 leg failed in `adr-answers` alone. `verify`
(job 111987814719) failed. The `SyntaxError` was found by the 3.11 check on the
laptop minutes before this run was read, and fixed in `5fb58a2` together with
`_GLIMPSE`.

**2. The push of step 6** (`14c8a05`, run 37376858363, both legs ran in about
a minute each):

```text
$ gh api repos/MPAdesso/coding-harness/commits/14c8a05b03901cfe4a18148fa58218e98e2f7598/check-runs --jq '.check_runs[] | [.name, .conclusion] | @tsv'
verify	failure
drift	skipped
gates (3.12)	failure
gates (3.11)	failure
$ gh api … --jq '[.check_runs[] | select(.name == "verify") | .check_suite.id] | group_by(.) | map(length)'
[1]
```

In both legs (jobs 111988040029 for 3.11, 111988040324 for 3.12) the step
`The test suite passes` is `success` and the only failed step is
`Every feature has the maintainer's answer to the ADR question`
(`adr-answers`: `[DECISION] 1` is open, the answer is not recorded — house
rule 8). `verify` is `failure` because the legs are; one check run named
`verify`. What is **not** shown live: a push whose 3.11 leg alone is red while
3.12 is green — `adr-answers` makes both red until the answer is recorded; the
summary check's reaction to `failure`, `cancelled` and `skipped` is held by
`test_the_summary_check_passes_only_when_every_leg_passed`, and attempt 1 of
evidence 1 showed it red on a `cancelled` leg.

**3. The lock reproduces itself** (at `14c8a05`):

```text
$ eval "$(sed -n '2s/^#    //p' requirements-ci.txt)" && git diff --exit-code requirements-ci.txt
Resolved 14 packages in 172ms
exit 0
```

**4. A fresh `.venv`** (at `14c8a05`):

```text
$ rm -rf .venv && make venv && .venv/bin/python3 -m pytest tests/test_lock.py -q
Successfully installed annotated-types-0.8.0 iniconfig-2.3.0 jinja2-3.1.6 markupsafe-3.0.4 packaging-26.3 pluggy-1.6.0 pydantic-2.13.5 pydantic-core-2.46.5 pytest-8.3.4 pyyaml-6.0.2 ruff-0.9.10 typing-extensions-4.16.0 typing-inspection-0.4.4
13 passed
```

**The local gate, 2026-10-05 at 23:37 on `14c8a05` plus this file's edits.**
`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false
make verify` from a shell with no `PYTHON` and no virtual environment on
`PATH`: the runner took the checkout's own `.venv`; **623 passed, 15 skipped**;
`ruff-check`, `ruff-format`, `leerprobe`, `plans-registry`, `frontmatter-current`,
`bead-export`, `dangling-beads`, `decision-continuity`, `gate-schema`,
`ci-drift` and `ramp-valves` green. **Red: `adr-answers` (block) alone** —
`project-lock: no answer — … decisions/answers/project-lock/adr.yaml does not
exist` — until the maintainer answers `[DECISION] 1`; recorded by the
orchestrating session, not here. `docs-links` (51 findings, the same count as
the evidence of `research-currency` the same day; none in a line this change
wrote) and `markdownlint` are report-only and red. The same run under Python
3.11.9 (`PYTHON=<venv built from the lock> bash scripts/verify_all.sh`):
623 passed, 15 skipped, the same single blocking red.

Criteria 1 (read once with `tomllib`), 21 (longest `provenance.yaml` prefix)
and 22, 23 (`grep`) read on 2026-10-05 and hold. `scripts/kit/probe.py`,
`scripts/export/manifest.yaml`, `OHNE_AUFRUFER`, `OHNE_TEST`,
`OHNE_MUTATIONSTEST`, `ruff.toml`, `README.md`, `tools/` and
`scripts/new_change.py` are untouched (`git diff d5813ec..HEAD` names none of
them).

## Repair round 1

Origin: the phase-6 review in `findings.md` (reviewed at `a33e341`); this round
starts at `1cb043f`, 2026-10-06. The maintainer's standing rule of that day —
MINOR rows on tests, security or false statements are repaired without asking —
covers F-1, F-2, F-3, F-4 and F-6. F-5 (the demand the travelling CI makes on a
kit instance) is not repaired: its status reads "accepted limit — follow-up
bead coding-harness-dj9", the release builder. Each row is set to "fixed in
`<commit>`, not reviewed"; the reviewer closes them. No code of the change
moved: two test files and one sentence changed, the generator, `ci.yml` and
the lock are as they were.

| Row | Commit | What changed |
| --- | --- | --- |
| F-1 | `1a4c314` | The summary step is run with six results, not four: `success` (exit 0) and `failure`, `cancelled`, `skipped`, `abandoned` and an empty result (exit 1). `abandoned` is the value run 37375079831 produced live; a step that refuses a list of bad results passes the last two. |
| F-2 | `1a4c314` | The same test holds that `continue-on-error` is absent from the summary step, the summary job and the matrix job (the job, not the steps: the matrix job's steps carry it on purpose for the report and advisory gates). |
| F-3 | `8e4378b` | `test_the_gate_reports_in_the_drift_job_only` reads `ci_gates.MATRIX_JOB`, the job where the gates run, and fails on an empty set of step ids. |
| F-4 | `c9405d4` | The three matrix tests take `tools.python` from `decisions/gates.yaml` read in the test (`_declared()`), and `ci_gates.interpreters()` must return the same list. `_matrix()` refuses any matrix key besides `python`. |
| F-6 | `50cc050` | `docs/WORKFLOW.md` §8, the `uv`/`mypy` row: CI and `make venv` install the lock with pip, nothing calls uv to install, and the local runner installs nothing — it takes `$PYTHON`, else the first of `.venv/bin/python3` and `python3` on `PATH` that imports PyYAML, and exits 2 when none does. |

Deviation: `spec.md` criterion 23 carried the same slip ("CI and the runner
install it with pip"). It gets a dated amendment, appended, nothing renumbered,
in the form earlier changes used; its refutation is extended by one line. The
wording of the row is mine, from `scripts/verify_all.sh`: where the review's
row says the runner takes `$PYTHON` only if it imports PyYAML, the script takes
a set `$PYTHON` as it is and tests the other two candidates.

### Planted faults of the round

Each fault planted on its own, `ci.yml` regenerated where the generator was
changed, the test file run, the tree restored with `git checkout` (`git status`
empty after each). **Before** is the suite of the parent of the row's commit
(`tests/test_ci.py`: 48 passed, 2 skipped, so 0 red of 50); **after** is the
suite of the row's commit. 48 to 55 are the reviewer's own variants and mine;
57 and 58 replay faults 3 and 18 of the table above, to show the stricter tests
still hold what they held. The script is a scratch file (`plant_r1.py` in the
scratchpad of the session), not part of the change.

| # | Row | Fault | Before (red) | After (red) | Tests that went red |
| --- | --- | --- | --- | --- | --- |
| 48 | F-1 | the summary step refuses `failure`, `cancelled` and `skipped` in a loop, nothing else (the reviewer's fault) | 0 of 50 | 1 | `test_the_summary_check_passes_only_when_every_leg_passed` |
| 49 | F-1 | the step passes on `success` and on `abandoned` (`case … in success\|abandoned`) | 0 of 50 | 1 | the same |
| 50 | F-1 | the step passes on `success` and on an empty result (`… = success \|\| test -z …`) | 0 of 50 | 1 | the same |
| 51 | F-2 | `continue-on-error: true` on the step "Every leg of the gates passed" | 0 of 50 | 1 | the same |
| 52 | F-2 | `continue-on-error: true` on the job `verify` | 0 of 50 | 1 | the same |
| 53 | F-2 | `continue-on-error: true` on the job `gates` | 0 of 50 | 1 | the same |
| 54 | F-4 | `interpreters()` returns the list reversed | 0 of 50 | 2 | `test_every_declared_interpreter_gets_a_leg`, `test_the_drift_job_runs_once_on_the_last_interpreter` |
| 55 | F-4 | the matrix gains `include: [{python: "3.13"}]` | 0 of 50 | 2 | `test_every_declared_interpreter_gets_a_leg`, `test_every_job_sets_a_declared_interpreter_before_installing` |
| 56 | F-4 | the matrix gains a second axis `os: [ubuntu-latest]` | 0 of 50 | 2 | the same two |
| 57 | F-4 | replay of 3: the matrix written as a literal in the generator | 1 | 1 | `test_every_declared_interpreter_gets_a_leg` |
| 58 | F-4 | replay of 18: the drift job on the first interpreter | 1 | 1 | `test_the_drift_job_runs_once_on_the_last_interpreter` |
| 59 | F-3 | the generator also writes every drift gate into the matrix job (the reviewer's fault) | 0 of 1 (the one test) | 1 | `test_the_gate_reports_in_the_drift_job_only` |
| 60 | F-6 | the old row back (`docs/WORKFLOW.md` of `1cb043f`), read with `grep`: the sentence "installs nothing" with `make venv` in the row, and no "local runner install it with pip" | read RED | read GREEN on `50cc050` | the read |

The fault of F-3 is also caught by `test_every_gate_step_runs_even_after_a_failing_gate`
(the reviewer's note); that test was green before and after and is not counted
here. Every "before" is the suite as it stood without the fix, so 48 to 56 and
59 show the hole, 57 and 58 show nothing lost.

Measured on `50cc050` (2026-10-06): `make verify` green, with
`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`;
`tests/test_ci.py` and `tests/test_research_currency.py` together 132 passed,
2 skipped. Tested under Python 3.12 (the worktree's `.venv`); the 3.11 run
is the push suite's leg, not read here.

## Repair round 2

Rows F-7 (MINOR, origin `base`) and F-8 (MINOR, origin `fix-r1`) from review
round 2, repaired by the orchestrating session under the maintainer's rule of
2026-10-06 (MINOR rows on tests and false statements are repaired without
asking).

- **F-7:** `tests/test_ci.py::test_no_blocking_gate_step_carries_continue_on_error`
  checks every step whose id is a `block` gate, in every job, and fails on an
  empty match.
- **F-8:** "four test files" in "Repair round 1" now reads "two test files"
  (`git diff --name-only 1cb043f..1dfdb99 -- tests/`).

Planted faults, each on the repaired tree and reverted:

| # | Fault | Before the repair | After |
|---|---|---|---|
| 61 | `continue-on-error: true` added by hand to the `pytest` step in `ci.yml` | green (review round 2) | RED, the new test |
| 62 | `_schritt` writes the key for every gate, `ci.yml` regenerated (`--generate-ci`) | the suite green (review round 2) | RED, the new test alone (1 failed, 48 passed) |

## Time used

Appetite: 5 h of phase 4, one repair round included. Read from `date`; the
repair round was not used (the 3.11 repair is step 6).

- 2026-10-05 23:08–23:39, 31 min, break counted (the waits for GitHub's
  runners are inside it)
- Repair round 1, 2026-10-06 16:28–16:40, 12 min of an appetite of 40 min (given
  by the orchestrating session), no break. `date` read at the start (16:28), at
  each step boundary (16:29, 16:32, 16:33, 16:35, 16:36, 16:38) and before each
  commit; the stop was not reached.
- Repair round 2, 2026-10-06, about 10 min, by the orchestrating session; no appetite set beyond the round's two rows.
