---
title: "Findings — project-lock"
category: findings
created: 2026-10-06
updated: 2026-10-10
status: accepted
implementation_status: done
date: 2026-10-06
last_reviewed: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-ei0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, dependencies, lock, ci, python]
---

# Findings — project-lock

Phase 6, round 1, on commit `a33e341` (branch `feat/project-lock`, eleven
commits over `origin/main` at `d5813ec`), 2026-10-06. The reviewer ran on
Opus 5.5 in a fresh context, wrote nothing but this file and the regenerated
`plans/INDEX.md`, opened no pull request, wrote nothing to the tracker and
recorded no ADR answer. Measured against `spec.md` (criteria 1–23, the
non-goals and "What other work may rely on") and `decisions.md`; `plan.md`
was read for its deviations, its planted faults and its evidence, not as the
yardstick. `[DECISION] 1` (the class and its ADR answer) is open, so the
gate `adr-answers` is red by design and is no row here. Phase 2a did not run
for this change, so its three questions are answered below as rows of
dimension `SPEC`. `templates/findings.md` does not exist on this branch; the
columns are those of the earlier `findings.md` files.

**Verdict: no BLOCKER, no MAJOR, no `[AMBIGUITY]`, no `[DIVERGENT]`.** Six
MINOR, all open; none stops the pull request. The code does what the spec
asks, live and locally: the check `verify` was red on every run of this
branch, the lock installs and reproduces, and the suite passes under 3.11
and 3.12. Four rows are holes in tests — two of them in the test that guards
the plan's own pre-mortem, the summary check — where a planted fault leaves
every test green. One row is a demand the travelling CI now makes on a kit
instance, and one is a sentence in `docs/WORKFLOW.md` that names the wrong
installer.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | MINOR | SPEC | base | `tests/test_ci.py`, `test_the_summary_check_passes_only_when_every_leg_passed` | The summary check's test feeds the step four results — `success`, `failure`, `cancelled`, `skipped` — so a step that refuses exactly the three bad ones passes it. Planted on `a33e341`: the step's `test … = success` becomes a loop that exits 1 only for `failure`, `cancelled` or `skipped`, `ci.yml` regenerated — no test goes red. GitHub hands out more than these four values. Measured in run 37375079831, attempt 1: the summary job's log (job 111987336085) reads `gates: abandoned` — the 3.11 leg got no runner and was cancelled at 21:33:51 UTC, the 3.12 leg had failed. Under the fault that run's `verify` would have been green. The code is right: `= success` made it red. The plan's evidence calls this "red on a `cancelled` leg"; the job saw `abandoned`, and the 3.12 leg was red as well, so that run does not show a cancelled leg on its own. One value outside the four (`abandoned`) in the test's list closes the hole. [criterion 7] | fixed in `1a4c314` — reviewed at `1dfdb99`, closed: the step is run with six results, `success` (exit 0) and `failure`, `cancelled`, `skipped`, `abandoned` and an empty result (exit 1). Replayed on a scratch clone of `1dfdb99`, `ci.yml` regenerated, each alone: fault 48 (the three-value deny-list) 1 red, 49 (`success\|abandoned`) 1, 50 (`… \|\| test -z …`) 1, each in `test_the_summary_check_passes_only_when_every_leg_passed`. A limit, no row: an own variant, a deny-list naming exactly the five bad values the test feeds, stays green — no finite list rules that out; the plausible fault, a list of the documented values, goes red |
| F-2 | MINOR | SPEC | base | `tests/test_ci.py`, the same test; `scripts/ci_gates.py`, `_summary_job` and the matrix job's header | Nothing holds that the summary job's step, or the matrix job, carries no `continue-on-error`. Planted on `a33e341`, each alone, `ci.yml` regenerated: `continue-on-error: true` on the step "Every leg of the gates passed" — no test goes red; `continue-on-error: true` on the job `gates` — no test goes red. Under the first, the step fails on a red leg and the job `verify` still concludes `success` (GitHub's step-level `continue-on-error` keeps the job from failing): `main` loses its one guard, which is the failure `plan.md` names in its pre-mortem. What the second does to `needs.gates.result` was not measured live. `ci-drift` stops a hand edit of `ci.yml`; an edit of the generator is held by nothing. An assertion that neither the summary job nor its step nor the matrix job carries `continue-on-error` closes it. [criterion 7] | fixed in `1a4c314` — reviewed at `1dfdb99`, closed: the same test refuses the key on the summary step, the summary job and the matrix job. Replayed: faults 51 (the step), 52 (the job `verify`) and 53 (the job `gates`) 1 red each, in that test. The matrix job's steps are left out on purpose — advisory and report gates carry the key; that a blocking gate's step carries none is held by no test, which is older than this change (F-7) |
| F-3 | MINOR | MAINT | base | `tests/test_research_currency.py`, `test_the_gate_reports_in_the_drift_job_only`, its last line | The check that the research-currency gate is not a step of the verify job now reads the summary job. `jobs["verify"]` is the new job `verify`, whose only step has no `id`, so `GATE_ID not in {None}` holds whatever the generator does. Planted on `a33e341`: the generator also writes every drift gate into the matrix job, `ci.yml` regenerated — this test stays green (the fault is caught elsewhere, by `test_every_gate_step_runs_even_after_a_failing_gate`). Phase 4 moved two readers of `jobs.verify` in `tests/test_ci.py` to `ci_gates.MATRIX_JOB` (`plan.md`, deviations) and missed this third one in another file. Reading `ci_gates.MATRIX_JOB` there closes it. [a check over an empty set; no criterion of this spec] | fixed in `8e4378b` — reviewed at `1dfdb99`, closed: the check reads the step ids of `ci_gates.MATRIX_JOB`, drops the missing ones and fails on an empty set. Replayed: fault 59 red in `test_the_gate_reports_in_the_drift_job_only` (and, as in round 1, in `test_every_gate_step_runs_even_after_a_failing_gate` and `test_a_gate_that_needs_history_gets_a_full_checkout_only_in_its_job`); an own variant, only `research-currency` also written into the matrix job, red in the same three |
| F-4 | MINOR | SPEC | base | `tests/test_ci.py`, `test_every_declared_interpreter_gets_a_leg`, `test_every_job_sets_a_declared_interpreter_before_installing`, `test_the_drift_job_runs_once_on_the_last_interpreter` | The matrix tests take their yardstick from `ci_gates.interpreters()`, the function under test, and read only the key `matrix.python`. Planted on `a33e341`, each alone, `ci.yml` regenerated: `interpreters()` returns the list reversed — no test goes red, although the drift job then runs under 3.11, the first declared interpreter, not the last, and the legs run newest first; the matrix gains `include: [{python: "3.13"}]` — no test goes red, although that adds a third leg under an interpreter `tools.python` does not declare. Both need an edit of the generator; `ci-drift` stops hand edits. Reading `tools.python` from the gate file in the tests, and refusing any matrix key besides `python`, closes both. [criteria 4, 6, 9] | fixed in `c9405d4` — reviewed at `1dfdb99`, closed: `_declared()` reads `tools.python` from `decisions/gates.yaml` in the test, `ci_gates.interpreters()` must return the same list, and `_matrix()` refuses any key besides `python`. Replayed: fault 54 (reversed) 2 red, 55 (`include` with 3.13) 2, 56 (an axis `os`) 2, the tests `plan.md` names. Own variants: `interpreters()` gains 3.13 — 3 red (all three matrix tests); `exclude: [{python: "3.11"}]` in the matrix — 2 red |
| F-5 | MINOR | MAINT | base | `.github/workflows/ci.yml`, `scripts/ci_gates.py` (`INSTALL`), `scripts/verify_all.sh` — kit role `mechanismus`; `requirements-ci.txt`, `pyproject.toml`, `Makefile` — kit role `bestand` | The mechanism that travels with the kit now makes a demand on files that stay home. Every CI job installs `requirements-ci.txt` with `--require-hashes`, so a repository built from the kit needs its own lock with a hash on every package, transitive ones included; and the runner's message sends a session to `make venv`, a target of the `Makefile`, which does not travel. Before this change `ci.yml` installed three packages inline and asked nothing of an instance. Measured: LakeSwitch's own `requirements-ci.txt` (lakeswitch-ai `c02f11d`, 2026-09-23: six exact pins, no hashes) is refused by that install line in an empty Python 3.12 venv — "Hashes are required in --require-hashes mode, but they are missing", exit 1. Nothing breaks today: LakeSwitch builds clean-room and takes none of these files, and no repository takes the kit yet. The spec's sentence "LakeSwitch: nothing of this change travels" holds for the two new files and not for the install line and the hint. Recorded for the release builder (bead coding-harness-dj9), which will ship these files to an instance. ["What other work may rely on"] | accepted limit — follow-up bead coding-harness-dj9. Checked at `1dfdb99`: stated honestly — nothing of it was repaired, `plan.md` ("Repair round 1") names the standing rule of 2026-10-06 that lets a maintenance row be accepted, and the spec's LakeSwitch sentence holds today, since LakeSwitch builds clean-room. The bead does not carry the demand yet (round 2). Round 3: the bead carries a note of 2026-10-06 that names the dependency and leaves out the hash demand — F-9 |
| F-6 | MINOR | SPEC | base | `docs/WORKFLOW.md` §8, the `uv`, `mypy` row | The row now says "CI and the local runner install it with pip and never call uv". The local runner (`scripts/verify_all.sh`) installs nothing: it chooses an interpreter and exits 2 when none imports PyYAML. `make venv` installs the lock. The sentence follows the wording of criterion 23, so the spec carried the slip. A reader who takes it at its word expects `make verify` to build the environment. Naming `make venv` where the row names the runner closes it. [criterion 23] | fixed in `50cc050` — reviewed at `1dfdb99`, closed: the row names CI and `make venv` as the installers, says nothing calls uv to install and the local runner installs nothing. Fault 60 replayed with `grep` on the row: `1cb043f` has no `make venv` and "local runner install it with pip", `1dfdb99` the reverse. The row's account of the runner matches `scripts/verify_all.sh` and criterion 11, measured on a scratch clone: `PYTHON=/usr/bin/python3` (no PyYAML) is taken as it is, and the run ends with exit 2 at `ci_gates.py --report` (a `ModuleNotFoundError`, not the message); with no `$PYTHON`, no `.venv` and only a `python3` without PyYAML, the message names `make venv` and `$PYTHON`, exit 2. Criterion 23's amendment is a `[DETAIL]` (round 2) |
| F-7 | MINOR | MAINT | base | `tests/test_ci.py`; `scripts/ci_gates.py`, `_schritt` | No test holds that the step of a blocking gate carries no `continue-on-error`. `_schritt` writes the key for `advisory` and `report` gates only. Planted on a scratch clone of `1dfdb99`: the key on every gate step, `ci.yml` regenerated — the whole suite fails exactly as it does without the fault (the clone's unhydrated tracker and its worktree tests), nothing more. Under it a red `pytest` step no longer turns its leg red — GitHub's rule for the step-level key, as in F-2, read, not measured live — both legs report `success`, and the check `verify` passes: the link from a gate to its leg, one step before the link F-2 now holds. Older than this change: the same fault leaves every test of `tests/test_ci.py` and `tests/test_research_currency.py` green on `d5813ec`, when `verify` was one job. Not produced by repair round 1, so no `fix-r` origin. An assertion that the matrix job's steps carry `continue-on-error` exactly for the gates whose enforcement is `advisory` or `report` closes it; here or in a bead of its own is the orchestrating session's choice. [criterion 7, the link before it] | fixed in `9872724` — reviewed at `b4579a2`, closed: `test_no_blocking_gate_step_carries_continue_on_error` reads every step, in every job, whose id is a `block` gate, and fails on an empty match. Replayed: fault 61 (the key by hand on `pytest`) and 62 (`_schritt` writes it for every gate, `ci.yml` regenerated) each 1 red, the new test alone; both green under the test file of `57d5407`. Own variants: the key on the drift job's `plans-registry-strict` through the generator — 1 red, naming `drift`; every gate step id renamed by hand — the new test red on its empty match. The repair holds the `block` half of the suggested "exactly"; the other half is measured in round 3, no row |
| F-8 | MINOR | MAINT | fix-r1 | `plan.md`, "Repair round 1", first paragraph | The record of the round says "four test files and one sentence changed". `git diff --name-only 1cb043f..1dfdb99 -- tests/` names two, `tests/test_ci.py` and `tests/test_research_currency.py`. The rest of the sentence holds: `git diff --stat 1cb043f..1dfdb99` over `scripts/`, `.github/`, `requirements-ci.txt`, `pyproject.toml`, `Makefile`, `decisions/` and `AGENTS.md` is empty. "two test files" closes it. | fixed in `9872724` — reviewed at `b4579a2`, closed: the paragraph reads "two test files and one sentence changed", which `git diff --name-only 1cb043f..1dfdb99 -- tests/` bears out; `plan.md` says "four test files" nowhere else |
| F-9 | MINOR | MAINT | fix-r2 | bead coding-harness-dj9, its note of 2026-10-06 (the tracker, not the tree) | The note written for F-5 names the dependency — the travelling `ci.yml`, `INSTALL` and `scripts/verify_all.sh` need `requirements-ci.txt`, `pyproject.toml` and the `Makefile`, which the kit marks `bestand` — and asks the release builder to ship or generate them together, "or a receiving repository gets a CI that installs from a lock it does not have". It leaves out the demand F-5 measured: every CI job installs with `--require-hashes`, so the instance's lock needs a hash on every package, transitive ones included, and a lock the instance already has is refused without them — LakeSwitch's six pins without hashes (lakeswitch-ai `c02f11d`) failed exactly so. A release builder that keeps an instance's own `requirements-ci.txt`, as `bestand` suggests, finds the note satisfied and ships a CI that fails at its first install. One sentence added to the note closes it: the lock must carry a hash on every package, transitive ones included, and an existing lock without hashes is refused. Origin `fix-r2`: the note was written after round 2 found the bead silent. Two `fix-r` rounds in a row — the row goes to the maintainer, not to a third round. ["What other work may rely on"; F-5] | decided 2026-10-06 (maintainer: add the sentence) — the hash sentence added to the note on bead coding-harness-dj9 the same day; closed |
| 2a-1 | — | SPEC | base | `spec.md`, criteria 7, 11 and 23 | *Where does the spec admit two plausible readings?* Three candidates, none a real fork. Criterion 7 lists three bad results, and GitHub produced a fourth live (`abandoned`, F-1); the refutation's own words — "whose step passes on a result other than `success`" — settle it: anything but `success` is red, and that is what was built. Criterion 11 says the runner "looks nowhere else", and phase 4 added a `PATH` prepend; the prepend comes after the choice and adds no candidate, so the criterion keeps its one reading. Criterion 23 says "the runner" installs the lock; only `make venv` installs anything, so only one reading builds — the slip is F-6. No `[AMBIGUITY]`. | answered |
| 2a-2 | — | SPEC | base | `spec.md`, the `[DETAIL]`s; `plan.md`, deviations | *What is missing that would have to be decided while building?* Five places; phase 4 met three and recorded each as a deviation with its reason: the `PATH` for tools called by a bare name (`ruff` in `scripts/ramp_valves.py`), the `tools` block that hand-built gate files in `tests/test_gate_machinery.py` now need, and test names that keep the mutation ratchet honest. Two were not recorded: the third reader of the old job name (F-3) and the demand the travelling CI makes on a kit instance (F-5). The spec is also silent on `make venv` when the `python3` on `PATH` is not a declared interpreter; measured below, it fails loudly, so no row. | answered |
| 2a-3 | — | SPEC | base | `spec.md`, criteria 1, 8, 16, 21–23 | *Which acceptance criterion cannot go red?* Criterion 16's refutation (the environment test after `make venv`) cannot see `--require-hashes`: pip checks hashes whenever the file carries one. Phase 4 found this (planted fault 44) and added `test_make_venv_installs_the_lock_in_hash_checking_mode`, which reads the recipe. Criterion 8 is held live only; measured here with one check run `verify` per suite on `14c8a05` and `a33e341`, both push suites — a pull-request suite does not exist yet. Criteria 1, 21, 22 and 23 are one-off reads; read again here, all hold. Criterion 7's test has the holes F-1 and F-2; criteria 4, 6 and 9 have F-4. | answered |

Reviewer session: none — phase 2a did not run for this change (no 2a row in
any of its artefacts); this review ran in a fresh session.

## Checked without a finding

- **The summary check `verify` (criteria 7, 8).** The job needs `gates`,
  runs under `always() && (push || pull_request)`, has no `name:`, and its
  one step runs `test "${{ needs.gates.result }}" = success`; `fail-fast` is
  off. A skipped, cancelled, failed or `abandoned` aggregate makes it red,
  and on a schedule or dispatch run it is skipped, as the old `verify` job
  was. Live, read with `gh run view` and the jobs API on 2026-10-06: run
  37375079831 attempt 1 (`c926bad`) — 3.11 leg `cancelled` without a runner,
  3.12 leg `failure`, `verify` `failure` on `gates: abandoned`; attempt 2 —
  3.11 leg `failure` (three collection errors and the `SyntaxError` the
  plan's evidence names), `verify` `failure`; runs 37376858363 (`14c8a05`)
  and 37377369829 (`a33e341`) — both legs fail in `adr-answers` alone, the
  step "The test suite passes" succeeds in both, `verify` `failure` on
  `gates: failure`. The ruleset `main` requires exactly the context `verify`
  from GitHub Actions (integration 15368), read with `gh api` read-only.
- **The generated workflow.** `python3 scripts/ci_gates.py --check-ci`:
  "ci.yml ist genau die Ableitung der Gate-Datei.", exit 0; `--generate-ci`
  diffed against `ci.yml`: identical; `--check-schema` exit 0. Every job that
  installs runs `actions/setup-python@v5` first and then exactly
  `python3 -m pip install --require-hashes -r requirements-ci.txt`; the
  tracker hydration and the two marketplace actions install nothing with
  pip. The drift job has no matrix and no `needs`, sets `"3.12"`, and keeps
  its `schedule || workflow_dispatch` condition, so the nightly run does not
  depend on the matrix job.
- **The lock installs (criteria 5, 16).** In throwaway venvs under the
  scratchpad, with `--require-hashes --no-cache-dir`: Python 3.11.9 (pip
  24.1.2) and 3.12.4 (pip 24.0) each install the same 13 packages, exit 0;
  `colorama` is skipped by its `win32` marker. The Linux wheels installed in
  every leg of the three runs. `make venv` in a scratch clone builds `.venv`
  and `tests/test_lock.py` passes 13 of 13; `git status` stays empty.
- **The lock reproduces (criterion 3).** The command on line 2 of the lock,
  re-run with uv 0.12.5 on a copy of `pyproject.toml` and `UV_NO_CACHE=1`,
  writes the committed file byte for byte (sha256 `5e786a7e…aa24` both).
  The header does not record uv's version; whether another uv writes the
  same bytes was not measured.
- **The runner (criteria 11–13) and the `PATH` prepend.** The runner
  changes into the root, then takes `$PYTHON`, else `.venv/bin/python3`, else
  `command -v python3`, each only if it imports `yaml`; none → exit 2 with
  `make venv` and `$PYTHON` in the message. The prepend puts the chosen
  interpreter's directory first only if it is not on `PATH` yet, so in CI
  (setup-python's directory is on `PATH`) it does nothing. It does not hide
  a missing tool: in a scratch `.venv` without `ruff`, with another
  `ruff 0.9.10` first on `PATH`, `test_the_environment_matches_the_lock`
  fails with "ruff 0.9.10 is locked but not installed; build the locked
  environment: make venv …". It applies to any interpreter path, not only a
  venv: `PYTHON=/opt/homebrew/bin/python3.11` from a shell without
  `/opt/homebrew/bin` on `PATH` would put every Homebrew tool first (read,
  not measured) — the maintainer's veto on the block stands as `plan.md`
  asks; no row, because the spec does not forbid it and no gate misreads
  through it. Because the runner replaces only the first `python3` of each
  gate command, the prepend is also what makes a bare `python3` inside a
  gate resolve to the chosen interpreter.
- **The local gate.** `GIT_CONFIG_COUNT=1 … make verify` on `a33e341` with
  the portfolio venv (pydantic 2.10.6) first on `PATH`: the runner took the
  worktree's `.venv`; 623 passed, 15 skipped; every blocking gate green but
  `adr-answers` ("project-lock: no answer …"), as expected while
  `[DECISION] 1` is open; `docs-links` and `markdownlint` red, report-only;
  no `.venv` path in any gate's output.
- **Python 3.11 (criterion 18).** In a scratch clone, the whole suite under
  3.11.9 and under 3.12.4: 609 passed, 25 skipped, and the same four
  failures under both, all from the clone's unhydrated tracker.
  `_GLIMPSE` set by attributes is accepted by both.
- **The deviations.** (1) The renames: `tests/test_ci.py` names
  `plans_registry.py` and, before this change, held no test whose name
  matches `MUTATIONS_NAMEN`; a `goes_red` or `refuses` name there would have
  made `test_the_mutation_ratchet_only_turns_one_way` demand that
  `plans-registry` and `plans-registry-strict` leave the ratchet without a
  seeded red run. `tests/test_lock.py` names no gate script, so its three
  `goes_red` names move nothing. (2) The `tools` line in three hand-built
  gate files follows from criterion 10. (3) `pin_problems` ends with the
  `make venv` hint after a `make lock` step. (4) The `PATH` block: above.
- **Kit, export, ignore list, provenance (criteria 19–21).** `probe.rolle`
  gives `bestand` for `pyproject.toml`, `requirements-ci.txt` and
  `tests/test_lock.py` (via `tests/`); only the export catch-all matches the
  two files (test). `git check-ignore -q .venv/bin/python3` exit 0; the gate
  `leerprobe` green with `.venv` present. The longest `provenance.yaml`
  prefix is the new entry for each file — `machine-rendered` for the lock,
  `human-written` or `ai-drafted-reviewed` for the project file, both
  `frontmatter: none`. No touched path is reserved for `human-decided`, so
  the pull request is not a decision pull request.
- **Pins and readers (criteria 1, 17, 22, 23).** `tomllib` on
  `pyproject.toml`: the four dependencies and the two `dev` pins of
  criterion 1, `requires-python = ">=3.11"`, no `[build-system]`;
  `pythonpath = ["."]`. `AGENTS.md` line 151 tells a new checkout to run
  `make venv` before `make verify`; the §8 row carries the uv sentence (F-6
  for its last clause).
- **`make venv` with an undeclared `python3`.** With only `/usr/bin` on
  `PATH` (`python3` 3.9.6), `make venv` exits 2 at the install
  ("No matching distribution found for annotated-types==0.8.0") and leaves a
  package-less `.venv`, which the runner then passes over because it cannot
  import `yaml`. Loud, not silent.
- **Cost.** Runs 37376858363 and 37377369829: each leg about one minute
  (55–64 s), the summary job 3–4 s — about four billed minutes per run
  instead of one or two, inside the spec's estimate of three to five. Noted,
  as the spec asks.
- **Planted faults.** Twelve of the plan's 47 replayed on a scratch clone
  of `a33e341`, each alone, the four test files run, the clone restored with
  `git checkout` (empty `git status` after each); counts are beyond the
  clone's four tracker failures. Every count and test name matched
  `plan.md`: 5 (`--require-hashes` dropped from `INSTALL`) 1 red; 10
  (`always()` dropped) 1; 11 (`!= failure`) 1; 12 (`fail-fast` on) 2; 13
  (no `needs`) 1; 18 (drift on the first interpreter) 1; 21 (the `3.<n>`
  check removed) 1; 25 (`python3` before `.venv`) 1; 30 (the `PATH` block
  removed) 1; 31 (version by prefix) 1; 37 (the `reprlib` keywords back) a
  collection error under 3.11.9, 84 passed under 3.12.4; 39 (a
  `mechanismus` rule for `pyproject.toml`) 1. Own variants: a deny-list in
  the summary step — green (F-1); `continue-on-error` on the summary step,
  and on the matrix job — green (F-2); the drift gates also in the matrix
  job — red in `test_every_gate_step_runs_even_after_a_failing_gate`, green
  in the research-currency test (F-3); `interpreters()` reversed, and a
  matrix `include` with 3.13 — green (F-4); a `.venv` without `ruff` — red,
  naming `ruff` and `make venv`.

## Not checked

- A pull-request suite: no pull request exists, so criterion 8 is measured
  on push suites only.
- A hosted `drift` run of this branch (schedule or dispatch).
- What job-level `continue-on-error` does to `needs.gates.result` (F-2,
  second half).
- Whether a `workflow_dispatch` run on a branch head — whose `verify` is
  skipped, as the old job's was — can satisfy the ruleset after a red push
  suite. The behaviour is older than this change, which keeps the old
  condition.
- `make venv` with a `python3` of 3.13: no such interpreter here. By
  reading, the suite would name "Python 3.13 is not a declared interpreter"
  and send the session to `make venv`, which would rebuild the same.
- A re-lock with another uv version; the plan's other 35 planted faults.

## For phase 7

`plans/INDEX.md` was regenerated with `python3 scripts/plans_registry.py
--index` for this file. No row stops the pull request. Phase 7 waits for the
maintainer's answer to `[DECISION] 1`: until it is recorded by the
orchestrating session, `adr-answers` keeps both legs, the check `verify` and
the local `make verify` red. F-1 to F-4 are a few test lines each and fit
one repair round; F-5 is a sentence for the spec or for bead
coding-harness-dj9; F-6 is one clause in `docs/WORKFLOW.md`. Which to fix
and which to close is the maintainer's choice. The pull request names bead
coding-harness-ei0 in its body (house rule 4) and is not a decision pull
request.

## Round 2 — re-check of repair round 1

On commit `1dfdb99`, 2026-10-06, Opus 5.5 in a fresh context; the repair is
`git diff 1cb043f..1dfdb99` (five commits: three for the tests, one for
`docs/WORKFLOW.md` and `spec.md`, and `1dfdb99`, the record in `plan.md` and
the statuses here). The
reviewer wrote nothing but this file and `plans/INDEX.md`, opened no pull
request, wrote nothing to the tracker and called no external model.

**Verdict: F-1, F-2, F-3, F-4 and F-6 closed; F-5 accepted, its status
honest; two new MINOR rows — F-7 (origin `base`, older than this change) and
F-8 (origin `fix-r1`, one wrong count in `plan.md`). No BLOCKER, no MAJOR,
no `[AMBIGUITY]`, no `[DIVERGENT]`.**

- **Planted faults.** Eleven of the round's thirteen replayed on a scratch
  clone of `1dfdb99`, each alone, `ci.yml` regenerated, both test files run,
  the clone restored with `git checkout` (empty `git status` after each);
  counts are beyond the clone's one tracker failure. 48, 49, 50, 51, 52, 53
  1 red each; 54, 55, 56 2 each; 59 3 (the research-currency test and two
  in `tests/test_ci.py`); 60 replayed with `grep`. Every test name matched
  `plan.md`. Own variants: `interpreters()` gaining 3.13 — 3 red; a matrix
  `exclude` — 2; only `research-currency` in the matrix job — 3; a deny-list
  of exactly the five bad values — green (the limit in F-1's status); the
  key `continue-on-error` on every gate step — green (F-7).
- **No code moved.** `git diff --stat 1cb043f..1dfdb99` over `scripts/`,
  `.github/`, the lock, `pyproject.toml`, `Makefile`, `decisions/` and
  `AGENTS.md` is empty; `tests/test_ci.py` keeps 48 passed, 2 skipped.
- **Criterion 23's amendment is a `[DETAIL]`.** It is appended, dated, names
  F-6 and renumbers nothing — the form of `research-currency`'s amendment of
  its criterion 4. It changes no behaviour and no option: criteria 11, 12
  and 16 already say that the runner only chooses an interpreter and that
  `make venv` builds `.venv` from the lock, and round 1 found one reading
  only (2a-1). What the maintainer approved stands; the spec's own review
  is still `pending`. A wording slip, no row: read literally, "'the runner'
  above reads 'CI and `make venv`'" gives "CI and CI and `make venv`".
- **`$PYTHON`, and a correction of round 1.** The repair's wording is right:
  a set `$PYTHON` is taken as it is (`scripts/verify_all.sh`, the block
  after "The interpreter needs PyYAML"), as criterion 11 says; measured in
  F-6's status. Round 1's bullet "The runner" under "Checked without a
  finding" says each of the three candidates is taken only if it imports
  `yaml` — wrong for `$PYTHON`. `plan.md` puts that reading into "the
  review's row"; it stands in that bullet, not in a row.
- **Python 3.11.** `tests/test_ci.py`, `tests/test_research_currency.py` and
  `tests/test_lock.py`: 145 passed, 2 skipped under 3.11.9 (a scratch venv
  built from the lock with `--require-hashes`, the same 13 packages) and
  under 3.12.4 (the worktree's `.venv`). The local gate under 3.11.9
  (`PYTHON=<that venv> bash scripts/verify_all.sh`): "VERIFY GREEN", 623
  passed, 15 skipped. Live: run 37480817452 on `1dfdb99` (push) — `gates
  (3.11)`, `gates (3.12)` and `verify` `success`, `drift` skipped.
- **The local gate.** `GIT_CONFIG_COUNT=1 … make verify` on `1dfdb99`:
  "VERIFY GREEN", 623 passed, 15 skipped; `adr-answers` green, since the ADR
  answer is recorded (`57ab07f`); `docs-links` and `markdownlint` red,
  report-only.
- **The addendum of 2026-10-06 (LakeSwitch moves to Python 3.12).** Nothing
  in this branch contradicts it: `tools.python` and the generated matrix
  keep 3.11 and 3.12, and the head commit ran both legs. The spec's "LakeSwitch
  requires 3.11 (D-46, D-47)" is the state of its date and holds until the
  LakeSwitch change lands. For the follow-up that reduces the CI to 3.12:
  `test_every_declared_interpreter_gets_a_leg` demands at least two declared
  interpreters, and criteria 4 and 18 name 3.11 — that change amends them,
  as the addendum foresees.
- **F-5 and bead coding-harness-dj9 (the release builder).** Read with
  `tools/bd show` on 2026-10-06: the bead was last updated on 2026-09-21 and
  says nothing of the hashed lock or the `make venv` hint. The acceptance
  points to a bead that does not know of it until the tracker writer adds a
  note there — and the pull request then names that bead.

**For phase 7.** No row stops the pull request: CI green on `1dfdb99`,
`make verify` green under 3.11 and 3.12. Two MINOR rows are open. F-8 is a
false count, one word in `plan.md`. F-7 is a test hole older than this
change, one assertion in `tests/test_ci.py`, or a bead of its own. A further
repair round that produced a `fix-r2` row would make two `fix-r` rounds in a
row — an escalation, not a third round.

## Phase 6, round 3 (2026-10-06)

On commit `b4579a2`, Opus 5.5 in a fresh context; the repair is
`git diff 57d5407..b4579a2` (`9872724`, the test and the count, and
`b4579a2`, the record in `plan.md` and the statuses here). The reviewer
wrote nothing but this file, opened no pull request, wrote nothing to the
tracker and called no external model.

**Verdict: F-7 and F-8 closed. One new MINOR row, F-9, origin `fix-r2`: the
note on the release builder's bead (coding-harness-dj9) leaves out the hash
demand of F-5. This is the second `fix-r` round in a row, so F-9 goes to the
maintainer, not to a third repair round. No BLOCKER, no MAJOR, no
`[AMBIGUITY]`, no `[DIVERGENT]`.**

- **Nothing else changed.** `git diff --stat 57d5407..b4579a2` names three
  files: `tests/test_ci.py` (one test, 20 lines), `plan.md` (the count and
  "Repair round 2") and the two status cells here. No script, workflow,
  lock or gate file.
- **Planted faults**, replayed in the worktree, each alone, `ci.yml`
  regenerated where the generator moved, restored with `git checkout`
  (empty `git status` after each), `tests/test_ci.py` run. 61: 1 failed,
  48 passed, the new test. 62: the same; 14 steps gain the key, 13 in the
  matrix job and 1 in the drift job. Under the test file of `57d5407` both
  give 48 passed, as `plan.md` records. Own variants: the key on the drift
  job's `plans-registry-strict` through the generator — 1 red, "drift: the
  blocking gate plans-registry-strict carries continue-on-error", while
  `--check-ci` stays green, so only this test sees it; the `pytest` step
  renamed by hand to `pytest-suite` and given the key — the new test green,
  the rename red in `test_every_gate_step_runs_even_after_a_failing_gate`
  ("17 of 18 gates appear as steps") and
  `test_every_declared_interpreter_gets_a_leg`, `--check-ci` exit 1; every
  gate step id renamed by hand — the new test red on its empty-match guard,
  with three others.
- **The docstring** is English and true. A failing step without the key
  fails its job; the generator writes the key for `advisory` and `report`
  only; every step whose id is a `block` gate is checked, in every job; an
  empty match fails. "Every `block` gate that runs in CI is checked" holds
  together with `test_every_gate_step_runs_even_after_a_failing_gate`,
  which demands every gate as a step under its own id — the renamed-step
  variant above; the new test alone would pass a step whose id moved. The
  drift job has no leg and no `verify`; there the key would let the nightly
  job pass, and the test covers that job too. No row.
- **The other half of F-7's suggestion is not held.** With `_schritt`
  writing the key for no gate, `ci.yml` regenerated, the whole suite turns
  only `test_the_gate_reports_in_the_drift_job_only` red: `markdownlint`,
  `lychee` and `docs-links` lose the key unnoticed. A missing key makes an
  `advisory` or `report` gate block — louder, never a silent pass. No row.
- **The local gate.** `GIT_CONFIG_COUNT=1 … make verify` on `b4579a2`:
  "VERIFY GREEN", 624 passed, 15 skipped, one test more than round 2;
  `docs-links` and `markdownlint` red, report-only. Live: run 37483451114
  on `b4579a2` (push) — `gates (3.11)`, `gates (3.12)` and `verify`
  `success`, `drift` skipped. Python 3.11 was not run locally this round.
- **Bead coding-harness-dj9.** Read with `tools/bd show` on 2026-10-06: a
  note dated 2026-10-06 names the dependency of the travelling mechanism on
  the three `bestand` files, the `Makefile` among them, which covers the
  `make venv` hint. It does not name `--require-hashes`, nor that a lock the
  instance already has is refused without a hash on every package — F-9.

**For phase 7.** No row stops the pull request: CI and `make verify` green
on `b4579a2`. F-9 is the one open row, a MINOR of origin `fix-r2`; the
maintainer decides whether the tracker writer adds its sentence to the
bead's note or accepts the row as it stands. The pull request names bead
coding-harness-ei0, and coding-harness-dj9, whose note this change added
(house rule 4).
