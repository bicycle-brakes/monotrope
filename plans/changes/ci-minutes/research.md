---
title: "Research — ci-minutes"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-cac
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, ci, github-actions]
---

# Cut hosted CI minutes — Research

Phase 1 for bead coding-harness-cac, read against `origin/main` at `14f6e1a`
on 2026-10-13. GitHub stopped starting jobs on 2026-10-13 (failed payment or
spending limit). The bead records the measurement the maintainer took on
2026-10-13 over the last 100 runs: 61 push runs against 8 pull_request runs
among the successful ones, about 3.5 minutes each, two matrix legs (3.11 and
3.12), and a push to a branch with an open pull request runs twice. The
maintainer approved three measures the same day: push triggers CI only on
`main`; a pull request runs only Python 3.12 while push to `main` and the
nightly schedule keep both legs; concurrency cancels superseded pull-request
runs and never runs on `main`. A self-hosted runner was rejected for now.

## Route of this exploration

Written by the planning session itself (Claude Opus 5.5), not through
`python3 scripts/stage2.py explore ci-minutes`. The change is a handful of
lines in one generator; the facts below had to be read anyway to write the
spec, and a second explorer would have read the same five files. Stage 2 is
also blocked for GLM (Claude Code 2.1.296 refused glm-5.3(-flash) as an
unrecognized model before any call, bead coding-harness-6th), so the runner
would have taken its Stage-1 route (`--stage2-off`, Haiku 4.5). No foreign
model was started.

## What exists today

**`ci.yml` is generated, and the generator hard-codes triggers and
concurrency.** `scripts/ci_gates.py`, function `generate_ci`, writes the
whole workflow as literal lines: `on:` with a bare `push:`, a bare
`pull_request:`, `schedule` (`cron: "23 4 * * *"`) and `workflow_dispatch:`;
then `concurrency:` with `group: verify-${{ github.event_name }}-${{
github.ref }}` and `cancel-in-progress: false`. None of this comes from
`decisions/gates.yaml`. The `ci-drift` gate (`ci_gates.check_ci`, gate
`ci-drift` in `decisions/gates.yaml`) compares the committed
`.github/workflows/ci.yml` byte for byte with `generate_ci()`.

**The matrix comes from the gate file.** `decisions/gates.yaml`,
`tools.python: ["3.11", "3.12"]`, read by `ci_gates.interpreters()`.
`generate_ci` writes it as the literal list `python: ["3.11", "3.12"]` in the
job `gates` (`ci_gates.MATRIX_JOB`), with `fail-fast: false`. The schema
(`ci_gates._tools_fehler`) allows only the key `python` under `tools`.

**Which job runs on which event.** Job `gates` (the matrix):
`if: github.event_name == 'push' || github.event_name == 'pull_request'`.
Job `verify` (`ci_gates.SUMMARY_JOB`, `ci_gates._summary_job`): needs
`gates`, `if: always() && (push || pull_request)`, fails unless
`needs.gates.result` is exactly `success`. Job `drift`:
`if: github.event_name == 'schedule' || github.event_name ==
'workflow_dispatch'`, one interpreter, the last declared one
(`versionen[-1]` in `generate_ci`), running only the `job: drift` gates
(`plans-registry-strict`, `research-currency`).

**The nightly schedule does not run the two legs today.** On `schedule` the
matrix job and the summary job are skipped by their `if`; only `drift` runs,
on 3.12. The bead's wording "both legs stay on push to main and the nightly
schedule" therefore holds for push to `main`, but the nightly run has no
3.11 leg to keep (`generate_ci`, the three `if:` lines above;
`tests/test_ci.py`, the drift-job test asserting `push` and `pull_request`
are not in the drift job's condition).

**The required check.** `tests/test_repo_settings.py` (module docstring,
`REQUIRED_CHECK = "verify"`) holds the ruleset on the default branch: a pull
request is required, the check `verify` is required and pinned to GitHub
Actions, and branches must be up to date before merging
(`strict_required_status_checks_policy`, RB-G7). The check is the summary
job, reported on the pull request's head commit by the `pull_request` run.
Nothing found requires a check from a `push` run on a non-`main` branch.

**Tests that read the trigger, matrix and concurrency** (`tests/test_ci.py`):

- `test_concurrency_group_carries_the_event` — the group contains
  `event_name`.
- `_merge_ref_findings` / `test_the_verification_runs_against_the_merge_ref`
  / `test_the_merge_ref_check_flags_a_planted_fault` — a `pull_request`
  trigger without `branches`, `paths` or `types` filters, no
  `pull_request_target`, the matrix job's `if` names `pull_request`, no
  checkout `ref`. They do not look at the `push` block.
- `_matrix` — asserts `strategy.matrix` has only the key `python` and returns
  `list(matrix["python"])`; it assumes a literal list.
- `test_every_declared_interpreter_gets_a_leg` — the matrix equals
  `tools.python`, and with `interpreters()` monkeypatched to three versions the
  generated matrix equals those three.
- `test_every_job_sets_a_declared_interpreter_before_installing` — the matrix
  job's `python-version` is `${{ matrix.python }}` and `set(_matrix(job))`
  lies within the declared list.
- `test_the_summary_check_passes_only_when_every_leg_passed` — the summary
  job's condition contains `always()`, `push` and `pull_request`, not
  `schedule`.
- The drift-job test near the end of the file (the assertion message "The
  drift job hangs on the pull request") — the drift job's condition names
  `schedule` and `workflow_dispatch`, not `push` or `pull_request`; the
  matrix job's names `push` and `pull_request`.

Other readers of the generated workflow: `tests/test_research_currency.py`
(the research-currency step stands in `drift`, not in the matrix job) and
`tests/test_gate_machinery.py`, `test_ci_drift_gate_goes_red_when_the_workflow_is_hand_edited`
(replaces `cron:` in the derivation). Neither depends on the push trigger or
the matrix form.

**The main-line run is still needed.** `scripts/check_interview_minimums.py`
compares against the first parent when `GITHUB_REF == "refs/heads/main"` —
"the hosted main-line run" in `docs/WORKFLOW.md` §3, table "What stands in the
repository for it", row "Interview". That run is a `push` run on `main` and
survives measure 1.

**Text-only changes.** `AGENTS.md`, "Sessions across checkouts": a text-only
change skips the local `make verify`, "the CI is its gate". The pull-request
run remains that gate; a branch pushed without a pull request gets no CI run
after measure 1.

**Provenance.** The only `provenance.yaml` in the tree is at the root. It maps
`.github/` to `human-written`, `docs/WORKFLOW.md` to `human-written` or
`ai-drafted-reviewed`, `tests/` to `human-written`. `scripts/` and
`decisions/gates.yaml` have no entry (unmapped). No path this change touches
is reserved for `human-decided`, so house rule 8 (decision pull request) does
not apply.

**The kit.** `scripts/kit/manifest.yaml` carries `decisions/`,
`.github/workflows/ci.yml` and `scripts/ci_gates.py` as `mechanismus` (they
travel into other repositories as a pair, D-10). A repository that takes the
kit takes the new triggers with it, including a push filter on the branch
name `main`.

**Documentation that states the trigger or the legs.** `decisions/gates.yaml`
header comment: "job verify (per push/PR) or drift (per schedule/dispatch)",
and the `tools` comment: "The verify job runs once per entry, as one leg
each; the drift job runs once, on the last." `docs/WORKFLOW.md` §3, "Verification
runs through git and CI, not through the harness", says what `make verify`
and the CI run, not on which events. No other document found states the
events (searched `AGENTS.md`, `README.md`, `docs/WORKFLOW.md`, `prompts/`,
`docs/governance/quality-gates.md` for push, matrix, schedule, 3.11).

**What GitHub Actions accepts** (documented behaviour, not measured here):
`on.push.branches` filters push runs by branch; `strategy.matrix` values may
be expressions over the `github` context, so `fromJSON(...)` can yield a
different interpreter list per event; workflow-level `concurrency.cancel-in-progress`
accepts an expression such as `${{ github.event_name == 'pull_request' }}`.

## What is unclear

- Whether the summary job `verify` of a run cancelled by concurrency still
  runs: it carries `always()`, and GitHub runs `always()` jobs after a
  cancellation. If so, the superseded commit shows a red `verify`; the newest
  commit's check is unaffected. Not measured.
- The default branch names of the repositories that take the kit
  (`portfolio-agentic-engineering`, `lakeswitch-ai`): not read.
- `scripts/validate_change_artefacts.py`, named as the phase 2 and 3 gate in
  `prompts/02-spec.md` and `prompts/03-plan.md`, does not exist in this tree
  (not found under `scripts/`); `docs/WORKFLOW.md` §2 says it is pending (bead
  coding-harness-jc3). The gates that do run are `make verify`'s.

## Files a change would have to touch

- `scripts/ci_gates.py` — `generate_ci`: the `push` block, the matrix
  expression, `cancel-in-progress`.
- `.github/workflows/ci.yml` — regenerated, never by hand.
- `tests/test_ci.py` — `_matrix` and the tests that read the matrix as a list;
  new tests for the three measures.
- `decisions/gates.yaml` — the two comments that state events and legs; no
  schema change is needed if the pull-request interpreter is the last
  declared one, as the drift job already does.
- `docs/WORKFLOW.md` — one sentence on which event runs what.

## Amendment — 2026-10-13 (amended 2026-10-13: maintainer decided 3.12 only)

The maintainer stopped the per-event matrix on 2026-10-13 and decided that
coding-harness drops Python 3.11 entirely ("ich will 3.12 bei lakeswitch
enforcen. Keine doppelte Arbeit"); lakeswitch-ai moves to 3.12 under its own
bead (lakeswitch-ai-6sj). Measures 1 (push only on `main`) and 3 (cancel
superseded pull-request runs, never on `main`) stand. The per-event matrix
expression and the nightly-legs point above are moot. Read again against
`origin/main` at `14f6e1a`.

**Where 3.11 is named as a supported or checked interpreter:**

- `decisions/gates.yaml`, `tools.python: ["3.11", "3.12"]` — the matrix
  source (`ci_gates.interpreters()`), and so `.github/workflows/ci.yml`'s
  `python: ["3.11", "3.12"]`.
- `pyproject.toml`, `requires-python = ">=3.11"`; its comment says the tested
  interpreters are `tools.python`.
- `ruff.toml`, `target-version = "py311"`. Measured 2026-10-13 at `8df968d`:
  `ruff check --target-version py312 scripts/ tests/` → "All checks passed!",
  `ruff format --check --target-version py312` → "61 files already
  formatted". Raising the target produces no finding.
- `scripts/check_research_currency.py`, the comment above `_GLIMPSE`: "the
  repository is checked under 3.11 too" — the reason `reprlib.Repr` limits
  are set as attributes.
- `tests/test_ci.py`, `test_every_declared_interpreter_gets_a_leg`: asserts
  `len(declared) >= 2` ("a matrix of one is not the second interpreter").
  This assertion goes red on `["3.12"]`.

**Where 3.11 appears only as sample data** — schema and lock tests that feed
an invented list, not a statement about this repository:
`tests/test_ci.py` (the monkeypatched `["3.11", "3.12", "3.13"]`, the schema
rejection list, a sample gate file), `tests/test_gate_machinery.py` (three
sample gate files), `tests/test_lock.py` (`environment_problems` fed sample
lists), `scripts/ci_gates.py` (the `_INTERPRETER` comment and the schema
error's example text). Archived and other changes' plans mention 3.11 as
history (`plans/changes/criterion-test-ledger/plan.md`,
`plans/changes/research-currency/plan.md`).

**The lock stays valid for 3.12.** `requirements-ci.txt` is compiled with
`uv pip compile … --universal --generate-hashes` and carries no
`python_version` marker (0 occurrences); its only marker is
`sys_platform == 'win32'` on colorama. The CI's 3.12 leg has installed it with
`--require-hashes` on every run since bead coding-harness-ei0, and this
checkout's `.venv` (Python 3.12.4) was built from it by `make venv` on
2026-10-13. No regeneration is needed; whether `uv pip compile` would print
byte-identical output under `>=3.12` was not run (it needs the network).

**One leg in the matrix.** The schema (`ci_gates._tools_fehler`) accepts a
one-entry list. The generator keeps the matrix job and the summary check
`verify` unchanged with one leg; the drift job already runs on the last
declared interpreter, which stays 3.12.

**Outside this repository's interpreter.** `tools/cloud-env/README.md` and
`tools/cloud-env/setup.sh` install Python 3.11 because lakeswitch-ai requires
`>=3.11,<3.12`. That is lakeswitch's interpreter, and it changes with
lakeswitch-ai-6sj, not here.

**Provenance, rechecked.** `pyproject.toml` is mapped to `human-written` or
`ai-drafted-reviewed`; `ruff.toml` and `scripts/` have no entry;
`requirements-ci.txt` (`machine-rendered`) is not touched. Still nothing
`human-decided`: no decision pull request.

**The kit.** `decisions/` travels as `mechanismus`, so a repository taking the
kit gets `tools.python: ["3.12"]`, and `ruff.toml` travels as `mechanismus`
too (`scripts/kit/manifest.yaml`), so it brings `target-version = "py312"`.
`pyproject.toml` and the lock do not travel (`pyproject.toml` header
comment). lakeswitch-ai moving to 3.12 matches.
