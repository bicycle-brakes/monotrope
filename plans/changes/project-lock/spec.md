---
title: "Spec — project-lock"
status: draft
implementation_status: partial
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
tags: [spec, dependencies, lock, ci, python]
class: feature
change: project-lock
adr_question: {proposed: "no", answered_by: null, reason: "it carries out LakeSwitch decisions D-46 and D-47, which the maintainer confirmed on 2026-09-21 and 2026-09-22, with a project file, a hash-checked lock and a second CI interpreter; no subsystem, interface or trust boundary changes, and one revert removes it"}
---

# Spec — project-lock

After this change, Coding Harness declares its Python dependencies in one
project file, installs them only from a hash-checked lock — in CI and in the
local `make verify` alike — and checks every change under Python 3.11 and
3.12, while `main` keeps requiring the one check `verify`. Inputs:
[`research.md`](research.md) (read at `d5813ec`) and
[`decisions.md`](decisions.md). The class `feature` is taken provisionally
with the recommendation of `[DECISION] 1`.

## Problem

- **Nothing is pinned as a whole.** There is no project file and no lock;
  the CI installs `pytest==8.3.4 PyYAML ruff==0.9.10` — PyYAML at whatever
  version the day brings, no transitive pin, no hash — from a line
  hard-coded twice in `scripts/ci_gates.py` (research 2).
- **The interpreter is an accident.** The CI takes the runner image's
  `python3`; `decisions/gates.yaml` declares Python 3.12 and nothing reads it
  (research 2, bead coding-harness-tqa). Locally, `scripts/verify_all.sh`
  takes the first interpreter that imports `yaml`, searching
  `~/.venvs/*` — today another repository's environment, with pydantic
  2.10.6 where the decided pin is 2.13.5 (research 2).
- **Python 3.11 is not checked, and it fails.** LakeSwitch requires 3.11
  (D-46, D-47); under 3.11.9 the suite stops at collection, because
  `scripts/check_research_currency.py` uses a 3.12-only `reprlib.Repr`
  signature (research 6).
- **Foundation work waits.** harness.foundation (coding-harness-s6i) needs
  Pydantic 2.13.5 and Jinja2 3.1.6 installed and its digest test run under
  3.11 and 3.12 (D-54, s6i's note).
- **One check guards `main`.** The ruleset requires exactly the status
  check `verify` (research 4). A second interpreter turns one job into two
  legs while the ruleset knows one check name, and a skipped job counts as
  passed.

## Terms

- **The project file** — `pyproject.toml` at the repository root.
- **The lock** — `requirements-ci.txt` at the repository root: every package
  the project file needs, pinned with `==` and its sha256 hashes, generated
  from the project file.
- **The declared interpreters** — `tools.python` in `decisions/gates.yaml`,
  oldest first: `3.11`, `3.12`.
- **A leg** — one run of the verify gates under one declared interpreter.
- **The check `verify`** — the status check the ruleset on `main` requires
  (context `verify`, GitHub Actions, research 4).
- **The suite** — `python3 -m pytest tests/ -q`, the gate `pytest`.

## Acceptance criteria

Each criterion holds one condition and names what refutes it. "Fed" means a
test passes the check a constructed input instead of the repository's.

### The project file and the lock

1. The project file declares as dependencies exactly `PyYAML==6.0.2`,
   `Jinja2==3.1.6`, `pydantic==2.13.5` and `pydantic-core==2.46.5`, and in
   the dependency group `dev` exactly `pytest==8.3.4` and `ruff==0.9.10`.
   *Refuted by:* another version, a range, a missing or an additional entry,
   read with `tomllib`.
2. If a pin of the project file is not an exact `==` pin, or the lock holds
   another version of that package or none, the suite fails and names the
   package.
   *Refuted by:* the check fed `pydantic>=2.13` or `pydantic==2.13.4` against
   the unchanged lock, and passing.
3. When the command recorded in the lock's first lines runs on the committed
   project file, it writes the committed lock byte for byte.
   *Refuted by:* `git diff --exit-code requirements-ci.txt` failing after the
   rerun.

### The CI

4. When the verify job runs on a push or a pull request, every verify gate
   runs once under each declared interpreter.
   *Refuted by:* a generated `ci.yml` whose matrix differs from
   `tools.python` — also after a test changes `tools.python` — or a verify
   gate missing from the matrix job.
5. When a CI job installs its toolchain, it installs the lock and nothing
   else, in hash-checking mode:
   `python3 -m pip install --require-hashes -r requirements-ci.txt`.
   *Refuted by:* any other `pip install` in `ci.yml`, or the flag missing.
6. When a CI job installs its toolchain, `actions/setup-python` has set a
   declared interpreter before.
   *Refuted by:* a job without `setup-python`, with it after `setup-deps`, or
   with a version outside `tools.python`.
7. If a leg fails, is cancelled or is skipped on a push or a pull request,
   the check `verify` fails.
   *Refuted by:* a generated job `verify` that does not need the matrix job,
   whose condition lacks `always()`, or whose step passes on a result other
   than `success`; and, in phase 5, a branch push whose 3.11 leg fails while
   `verify` reports success.
8. While the ruleset on `main` requires the check `verify`, every push and
   pull request run of the workflow reports exactly one check run named
   `verify`.
   *Refuted by:* a check suite of this change's head commit (GET, grouped by
   suite — a pull request's head carries one run per event) holding no check
   run `verify` or two.
9. When the drift job runs, it runs once, under the last declared
   interpreter.
   *Refuted by:* a generated drift job with a matrix or another version.
10. If `tools` holds a key other than `python`, or `tools.python` is not a
    non-empty list of distinct texts of the form `3.<n>`,
    `python3 scripts/ci_gates.py --check-schema` reports it.
    *Refuted by:* such a gate file passing the schema check.

### The local run

11. When `scripts/verify_all.sh` chooses its interpreter, it takes `$PYTHON`
    if set, else the first of `.venv/bin/python3` in the checkout and
    `python3` on `PATH` that imports PyYAML, and looks nowhere else.
    *Refuted by:* a temporary tree without `.venv`, with a `python3` on `PATH`
    that lacks PyYAML and an interpreter with PyYAML under `$HOME/.venvs/`, in
    which the runner does not exit 2.
12. If no candidate imports PyYAML, the runner exits 2 before any gate, and
    its message names `make venv` and `$PYTHON`.
    *Refuted by:* another exit code, a gate started, or a message without
    both.
13. When the runner starts a gate, the gate's environment carries the chosen
    interpreter as `PYTHON`.
    *Refuted by:* a gate of a temporary gate file that prints `$PYTHON` and
    finds it empty.
14. If the interpreter that runs the suite lacks a package of the lock or
    holds another version of one, the suite fails, naming each difference and
    `make venv`.
    *Refuted by:* the check fed an installed set with pydantic 2.10.6 and
    passing, or a message without `make venv`.
15. If the interpreter that runs the suite is not a declared interpreter, the
    suite fails.
    *Refuted by:* the check fed version 3.13 and passing.
16. When `make venv` runs in a checkout, it builds `.venv` there from the lock
    in hash-checking mode.
    *Refuted by:* `.venv/bin/python3 -m pytest tests/test_lock.py` failing
    right after `make venv` in this change's worktree.
17. When the suite runs, pytest's `pythonpath` holds the repository root.
    *Refuted by:* `pythonpath` removed from the project file while the test
    still passes.

### Python 3.11

18. When the suite runs under Python 3.11, it passes as it does under 3.12.
    *Refuted by:* the 3.11 leg of this change's head commit failing; the
    `reprlib` collection error of research 6 is the known case.

### Kit, ignore list, provenance

19. Neither `pyproject.toml` nor `requirements-ci.txt` travels: the kit role
    of each is `bestand`, the export verdict `drop`.
    *Refuted by:* `probe.rolle()` giving another role or none, or an export
    rule carrying either.
20. While `.venv/` exists in a checkout, git ignores it and
    `python3 scripts/kit/probe.py --strict` does not report it.
    *Refuted by:* `git check-ignore -q .venv/bin/python3` exiting 1, or the
    probe naming a `.venv` path.
21. `provenance.yaml` maps `requirements-ci.txt` to `machine-rendered` and
    `pyproject.toml` to a hand-written class, both with `frontmatter: none`.
    *Refuted by:* the longest matching prefix giving another class or none.

### What readers are told

22. When a session starts in a new checkout or worktree, `AGENTS.md` tells it
    to run `make venv` before `make verify`.
    *Refuted by:* no such sentence.
23. `docs/WORKFLOW.md` §8 says that uv only compiles the lock and that CI and
    the runner install it with pip.
    *Refuted by:* the row unchanged.

## What other work may rely on

- **harness.foundation (coding-harness-s6i):** a package `harness/` at the
  root is importable by the suite (criterion 17); Pydantic 2.13.5,
  `pydantic-core` 2.46.5 and Jinja2 3.1.6 are installed in every leg and in
  `.venv`; a test in `tests/` runs under 3.11 and 3.12 on every push and pull
  request (criteria 4, 7). Extending the ruff gates and both manifests to
  `harness/` is s6i's.
- **The release builder (coding-harness-dj9):** the lock and the project file
  are `bestand` and `drop` (criterion 19); a compatibility contract reads the
  pins from the project file.
- **The Hermes job (`feat/hermes-runner`):** a script of this repository that
  needs PyYAML runs under the clone's locked interpreter — `"$PYTHON"`, or
  `.venv/bin/python3` built by `make venv` after each lock change (criterion
  14 says when); the check `verify` keeps its name (criterion 8).
- **A Kubernetes gate runner (proposal):** an image installs the lock with
  `pip install --require-hashes -r requirements-ci.txt` onto a 3.11 or 3.12
  base and sets `PYTHON`; package versions come from the lock, not from
  `decisions/gates.yaml`.
- **LakeSwitch:** nothing of this change travels; its own lock stays its own.

## Non-goals

- The package `harness/`, the foundation, its digest test and the ruff gates
  over `harness/` (coding-harness-s6i).
- `harness.lock.yaml`, the release builder, `verify-pin` and the
  compatibility contract (coding-harness-dj9).
- LakeSwitch's `requirements-ci.txt`, which pins exactly but carries no
  hashes and no transitive packages (research 1).
- What bead coding-harness-tqa lists beyond the pins and the interpreter:
  actions pinned by commit, a `permissions:` block, the double run on push
  and pull request, quoting and unknown keys in the gate file.
- Recording interpreter and lock digest in `ci_gates.py --report`.
- Automatic pin updates, Python 3.13, an upper bound in `requires-python`,
  building or installing the project as a package.
- A change to the ruleset on `main`.
- Code of the Hermes orchestrator (`feat/hermes-runner`, slice 4).
- Translating German text of a touched file beyond the lines this change
  rewrites (house rule 1, coding-harness-yim).

## Open decisions

### `[DECISION]`

`[DECISION] 1` — the class and its ADR answer — is open (`decisions.md`).
Taken provisionally: `class: feature`, ADR proposal "no". If the answer is
"option 2", the header becomes `class: bounded` without `change:` and
`adr_question:`, and nothing else in this spec changes.

### `[GAP]`s — closed by reading

- **The phase gate.** `scripts/validate_change_artefacts.py` does not exist;
  `python3 scripts/plans_registry.py --check` stands in, as for
  `research-currency`.
- **The required check.** Context `verify` from GitHub Actions, the job's
  name; a skipped job reports success (research 4).
- **The lock tools.** uv 0.12.5 is installed and writes one universal,
  hashed file reproducibly; pip's `pip lock` is experimental and
  per-platform; pip-tools is absent (research 6).
- **Python 3.11.** One incompatibility, measured; everything else passes and
  compiles (research 6).
- **The project file's side effects.** pytest keeps rootdir and node ids;
  ruff keeps reading `ruff.toml` (research 6).
- **"The instance lock does not travel."** Either reading gives the same
  build: both files stay (research 7).

### `[DETAIL]`s — decided here, with the reason

Each is reversible and binds nothing beyond this change.

- **The lock is named `requirements-ci.txt`.** The repository already cites
  that name (the runner's message, `docs/WORKFLOW.md` §8, a `bestand` rule in
  the kit manifest), and LakeSwitch uses it for the same role, so a travelling
  mechanism that names it finds each instance's own file.
- **pip's requirements format with `--hash`, not `pylock.toml`.** Every pip
  a runner or a venv brings installs it (pip 24.0 measured); `pylock.toml`
  is experimental in pip and written per platform.
- **uv compiles the lock, pip installs it.** `make lock` runs
  `uv pip compile pyproject.toml --group dev --universal --generate-hashes
  --exclude-newer <today, 00:00 UTC> -o requirements-ci.txt`: one file for
  Linux CI and macOS, reproduced byte for byte by its recorded command
  (research 6). Only the machine that changes a pin needs uv; CI, the runner
  and agents never call it, so the §8 departure from the template's `uv`
  still holds for the toolchain, and the row says so.
- **PyYAML 6.0.2.** The bead asks PyYAML pinned without a version; 6.0.2 is
  what LakeSwitch pins and what the suite runs on today.
- **The project file:** `[project]` with `name = "coding-harness"`,
  `version = "0.0.0"`, `requires-python = ">=3.11"` and the four pins;
  `[dependency-groups]` `dev` with pytest and ruff; `[tool.pytest.ini_options]`
  `pythonpath = ["."]`; no `[build-system]` — nothing installs the project,
  and `harness` is imported from the root (D-46). A lower bound only: the
  tested set is `tools.python`.
- **`tools:` keeps only `python`, now a list.** `ruff` and `pytest` leave the
  gate file: nothing reads them, and the lock holds every version — one place
  per fact.
- **Every verify gate runs in every leg**, the two marketplace actions
  included: one rule is simpler to generate and test than an exception per
  gate, and the two report-only actions cost seconds.
- **The legs are one matrix job `gates`; a job `verify` sums them up.** It
  needs `gates`, runs under `always()` on push and pull request, and fails
  unless `needs.gates.result` is `success`; `fail-fast` is off. The ruleset
  and the Hermes job's check of it stay as they are; `always()` because a
  skipped job would count as passed; no fail-fast because a red leg must not
  cancel the other, the reason bead coding-harness-bl2 gave for steps.
- **The drift job runs once, under the last declared interpreter.** Its
  gates read the outside world, not the interpreter.
- **`actions/setup-python@v5`, minor versions only.** The major LakeSwitch
  uses; D-47 names minors, and the runner's newest patch of each is
  acceptable. Pinning actions by commit is tqa's.
- **`.venv` per checkout, built by `make venv`.** Conventional, visible,
  ignored by git; a shared environment stays possible through `$PYTHON`, and
  criterion 14 says when it is stale. `python3` on `PATH` stays the last
  candidate because the CI's runner calls (`--list` in the suite) find their
  interpreter there.
- **The environment check lives in the suite, not in the runner or a new
  gate.** `tests/test_lock.py` runs in every leg and in every local run
  through the gate `pytest`; a new gate would be a second entry for the same
  verdict and a new script would owe a caller, a test and a mutation test.
  Packages beyond the lock are tolerated: CI installs only the lock, so an
  import of anything else goes red there.
- **`tests/test_lock.py` is `bestand`.** It reads this repository's lock,
  which does not travel (the `tests/` catch-all already says so).
- **The 3.11 repair keeps the limits.** `_GLIMPSE` is built as
  `reprlib.Repr()` and its six limits are set as attributes, which both
  versions accept.
- **Readers are told in two places:** `AGENTS.md` (every harness reads it)
  and the §8 row of `docs/WORKFLOW.md`, which would otherwise be untrue.
  `README.md` names no setup step today and stays.
- **Cost of the second leg.** A push or pull request run bills about 3 to 5
  Actions minutes instead of 1 to 2 (two legs and the summary job, each
  rounded up to a minute; research 4). At the last 30 days' 378 runs that is
  roughly 1,500 minutes a month (estimate), inside GitHub Free's 2,000; the
  account's plan was not readable. If it ever pinches, the second leg can run
  on pull requests only — a change to the generator's matrix line.
