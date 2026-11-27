---
title: "Research — venv-guard"
status: accepted
implementation_status: done
date: 2026-11-17
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-s55e
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-17", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# venv guard — Research

Stage-2 call, 2026-11-17: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1109 files, 4530 commits, 12 rules.

## Runner exploration — 2026-11-17

Research complete. Below is the prose ready to append to `plans/changes/venv-guard/research.md` (all paths relative to the repository root; every statement names its source; nothing designed, recommended or judged).

---

## What exists today

**The promise and its three checks.** `tests/test_lock.py` (module docstring, lines 1–18, bead coding-harness-ei0) states the contract as one sentence: the suite runs on exactly the packages the lock names, under an interpreter the CI also runs. It checks (1) every pin of `pyproject.toml` is an exact `==` pin that the lock holds (`pin_problems`, tests/test_lock.py:67), (2) the running environment holds what the lock holds (`environment_problems`, tests/test_lock.py:91 — every marker-applying lock entry installed at exactly the locked version; packages beyond the lock are tolerated, docstring lines 99–102), and (3) the interpreter is a declared one (the `interpreter not in declared` branch, tests/test_lock.py:104). Every problem message ends in the `HINT` constant ("build the locked environment: make venv …", tests/test_lock.py:47). The real-environment check runs as `test_the_environment_matches_the_lock` (tests/test_lock.py:187) inside the gate `pytest`, which `decisions/gates.yaml` declares with `cost: minutes` (gates.yaml:65–71) — this is the only place in the tree where a chosen environment is compared against the lock.

**Building the venv.** `make venv` (Makefile:42–52) reads `requires-python` from `pyproject.toml` (the only place the minimum is declared, pyproject.toml:17 `requires-python = ">=3.12"`), refuses an interpreter below that floor *before* `.venv` is created (Makefile:43–50, bead coding-harness-y9q; refusal test `test_make_venv_refuses_an_interpreter_below_the_declared_minimum`, tests/test_lock.py:256), then runs `'$(PYTHON)' -m venv .venv` and `.venv/bin/python3 -m pip install --require-hashes -r requirements-ci.txt` (Makefile:51–52, recipe pinned by `test_make_venv_installs_the_lock_in_hash_checking_mode`, tests/test_lock.py:238). Line 51 carries no `--clear` and no removal of a pre-existing `.venv`. `PYTHON` defaults to the first of `python3.12`, `python3` on PATH (Makefile:40). `make lock` regenerates the lock with uv; only the machine that changes a pin needs uv (Makefile:11–15, 54–55).

**Choosing the interpreter at verify time.** `scripts/verify_all.sh` changes to the repository root before anything is chosen (verify_all.sh:40–43), absolutizes a relative `$PYTHON` against the caller's directory (verify_all.sh:31–38, bead coding-harness-4x2c), then takes `$PYTHON` if set, else the first of `$PWD/.venv/bin/python3` and the `python3` on PATH **that imports PyYAML** — the only fitness test a candidate must pass (verify_all.sh:51–63). No candidate imports PyYAML → exit 2 before any gate, message names `make venv` and `$PYTHON` (verify_all.sh:60–63). The chosen interpreter's directory goes first on PATH so bare-name tools (`ruff`) resolve to the locked ones (verify_all.sh:68–78), and in the gate loop the word `python3` in each gate command is replaced by the quoted chosen interpreter (verify_all.sh:503–506). The declaration for this behavior is the archived spec `plans/changes/archive/2026-10-05-project-lock/spec.md`, criteria 11–16 (bead coding-harness-ei0).

**Declared interpreters and CI.** `decisions/gates.yaml` declares `tools: python: ["3.12"]` (gates.yaml:61–62); `ci_gates.interpreters()` reads it with a schema check (scripts/ci_gates.py:490–501), the schema allows only the key `python` there (scripts/ci_gates.py:331–337), and the one CI install line is `python3 -m pip install --require-hashes -r requirements-ci.txt` (`INSTALL`, scripts/ci_gates.py:65). The generated workflow `.github/workflows/ci.yml` carries a matrix `python: ["3.12"]` with `setup-python` and the `INSTALL` line (ci.yml:23–39); a second job block installs under a fixed `"3.12"` (ci.yml:171–177 — its owning job name was not read). Since the ci-minutes change, the pull-request interpreter is the last declared one, `tools.python[-1]`, and the former 3.11 leg is dropped (plans/changes/archive/2026-11-06-ci-minutes/decisions.md:50–53, 84–86). `test_one_version_is_the_interpreter_floor` binds `requires-python`, the single declared interpreter and the ruff target together (tests/test_ci.py:826–828); `test_the_cloud_environment_builds_the_venv_with_the_floor` reads `tools/cloud-env/setup.sh` for the `uv venv --python` line (tests/test_ci.py:831–839).

**The runner tests.** A block of `tests/test_ci.py` (comment at 1313–1317, bead coding-harness-ei0) builds throwaway runner trees and holds the interpreter-selection contract: `test_the_runner_never_searches_other_environments` (tests/test_ci.py:1403 — no `$HOME/.venvs` probing, exit 2 with the `make venv` message), `test_the_runner_exports_a_relative_python_as_an_absolute_path` (tests/test_ci.py:1426), `test_a_python_path_with_a_space_still_starts_the_gate` (tests/test_ci.py:1447), `test_the_runner_prefers_the_checkouts_own_environment` (tests/test_ci.py:1486), `test_the_runner_hands_its_interpreter_to_every_gate` (tests/test_ci.py:1512), `test_the_runner_puts_the_chosen_environments_tools_on_the_path` (tests/test_ci.py:1523).

**The stage-2 runner's own venv guards.** `scripts/stage2.py` hardcodes the worktree's own paths: `RUFF = ".venv/bin/ruff"` (stage2.py:4806) and `PYTEST = (".venv/bin/python3", "-m", "pytest", "-q", "-n", "auto")` (stage2.py:4826); every missing-interpreter branch says "`make venv` builds it" (stage2.py:6329, 6409, 6630, 7008, 7056). Before each model call it digests the whole `.venv/` tree (`tool_state`, stage2.py:4971, rule R-21: the venv is git-invisible, so the digest is the only detector of an overwritten tool, planted `*.pth` or replaced package) and refuses the call on any difference (`tool_problem`, stage2.py:5054), except pytest bytecode caches, which are normalized away (`_is_cache_path`/`_unlink_cache`, stage2.py:5012–5051, bead coding-harness-q94b). `red_first_python` (stage2.py:7536) uses `.venv/bin/python3` when executable, else `sys.executable`. The test fixtures `venv_ruff`/`venv_pytest` (tests/test_stage2.py:5945, 5973) plant stand-ins at exactly these paths, and `test_a_key_the_gate_writes_under_venv_is_removed_and_refused` (tests/test_stage2.py:3204) holds the write-refusal behavior. `.venv` and `venv` are also in `FREE_DIFF_SKIP_PARTS` (stage2.py:2916).

**Cloud environment.** `tools/cloud-env/setup.sh` installs Python 3.11 and 3.12 via uv (setup.sh:13–14), appends the **lakeswitch-ai** venv to `~/.bashrc` PATH (setup.sh:35–36), and for coding-harness rebuilds with `uv venv --allow-existing --python 3.12` plus a hash-checked install (setup.sh:46–50); the README calls that `.venv` "what `make venv` builds" (tools/cloud-env/README.md:24–25).

**What readers are told.** `AGENTS.md` line 151: each new checkout or worktree runs `make venv` and `bash tools/pi/install.sh` once before `make verify`. `docs/WORKFLOW.md` §8 row (docs/WORKFLOW.md:2197): the local runner installs nothing and chooses only between the checkout's `.venv/bin/python3` and a PATH `python3` with PyYAML. `make help` must list the `venv` and `lock` targets (tests/test_workflow_entry.py:402). `.venv/` is gitignored (.gitignore:30), and neither `pyproject.toml` nor `requirements-ci.txt` travels with the kit — role `bestand`, export verdict `drop` (`test_the_lock_and_the_project_file_stay_home`, tests/test_lock.py:285–293).

**State of this worktree.** `.venv/pyvenv.cfg` exists and reads: built by `/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv` into this worktree, CPython 3.12.15, `include-system-site-packages = false` — the same shape the `make venv` recipe produces. `.venv/bin/` holds the console scripts `pip`, `ruff`, `pytest` (Glob); the `python3` entries did not appear in that listing because Glob does not list symlinks, so the presence of `.venv/bin/python3` is unverified, not denied.

## Where it lives

Mechanism holders, in one place: `Makefile` (venv target 42–52, PYTHON default 40) · `scripts/verify_all.sh` (choice 31–78, gate substitution 503–506) · `tests/test_lock.py` (environment-vs-lock comparison, whole module) · `tests/test_ci.py` (runner interpreter tests 1313–1538; floor tests 826–839) · `scripts/ci_gates.py` (`interpreters` 490–501, `INSTALL` 65) · `decisions/gates.yaml` (`tools.python` 61–62) · `.github/workflows/ci.yml` (generated, matrix 23–39) · `scripts/stage2.py` (runner-side venv paths and digest) · `tools/cloud-env/setup.sh` (46–50) · `AGENTS.md`:151, `docs/WORKFLOW.md`:2197 (reader text) · `scripts/kit/probe.py` (known-test map pins the venv-related test ids at probe.py:94–99 and 188–196, so new tests reading files the kit does not carry must be mapped there).

## What is unclear about it

**Not read (unreadable with the tools of this phase):**

1. The text of bead coding-harness-s55e — the change's own bead. The tree carries only `.beads/metadata.json`, `.beads/config.yaml` and `.beads/interactions.jsonl`; the tracker data lives in Dolt under `refs/dolt/data` on origin and is not hydrated in this worktree (house rule 2, AGENTS.md). What the bead demands — the guard's behavior, its class, its scope — is therefore unknown to this research. The latest handover (`docs/journal/handover/2026-11-16-night-run-2026-11-14-a-morning.md` and earlier files) does not mention `s55e` or "venv" in connection with it (grep over `docs/journal` returned no `s55e` match).
2. Which job owns `.github/workflows/ci.yml` lines 171–177 (fixed `"3.12"`, same `INSTALL` line) — the job header above the read range was not read.

**Not found (searched, nothing there):**

3. No mechanism in `scripts/` compares the chosen environment against the lock *before* the pytest gate: the interpreter probe in `verify_all.sh` tests only `import yaml` (verify_all.sh:53–54), and a search for `requirements-ci` across `scripts/` matches only `scripts/ci_gates.py` (the `INSTALL` line, 65), `scripts/new_change.py` and `scripts/kit/manifest.yaml` — none of them a freshness or lock-digest check.
4. No session-start, status-line or hook component in `tools/claude-code/` is venv-aware: a case-insensitive grep for "venv" over `tools/` matches only `tools/cloud-env/` and `tools/pi/README.md`.

**Open questions (need reading or the maintainer, not guessing):**

5. What `python3 -m venv .venv` (Makefile:51, no `--clear`) does on top of an existing `.venv` — re-used interpreter, stale packages, `pyvenv.cfg` rewrite — is standard-library behavior not decidable from this tree; the lock staleness question behind "a venv built before the last `make lock`" is unexamined.
6. Whether the intended guard attaches at verify time (`verify_all.sh` preflight), at build time (`make venv`), at session start (`tools/claude-code/` display), or in the cloud setup — the bead text decides this, and it was not read (see 1).
7. `tests/test_stage2.py` and `tests/test_stage2_fail_fast.py` reference the venv chiefly through the `venv_ruff`/`venv_pytest` fixtures and the write-refusal test (read: tests/test_stage2.py:730–733, 3204–3228, 5945–5974; tests/test_stage2_fail_fast.py:31–35, 56–58, 115) — whether further stage-2 assertions would be affected by a guard change was not exhaustively read.

## Which files a change would have to touch

Derived strictly from the holders listed above — the concrete set depends on the bead's scope, which is open question 1:

- A guard at verify time: `scripts/verify_all.sh` plus its behavioral home `tests/test_ci.py` (the runner-test block and its `_runner_tree` fixtures).
- A guard at build time: `Makefile` (the `venv` target) plus `tests/test_lock.py` (the recipe-pinning and refusal tests).
- A new or moved gate: `decisions/gates.yaml`, `scripts/ci_gates.py` (schema, catalog rendering — `tests/test_gate_catalog.py` holds the committed inventory, per the `catalog_rows` docstring at scripts/ci_gates.py:509), and the regenerated `.github/workflows/ci.yml`.
- Anything touching the stage-2 runner's view of the venv: `scripts/stage2.py` and the fixtures in `tests/test_stage2.py` / `tests/test_stage2_fail_fast.py`.
- New tests that read files the kit does not carry must be entered in the known-test map in `scripts/kit/probe.py` (examples at probe.py:94–99, discipline comment at 188–196).
- Reader text would follow in `AGENTS.md` (line 151) and the `docs/WORKFLOW.md` §8 row (line 2197) only if the behavior those sentences describe changes.
- Boundary note: `scripts/verify_all.sh` and `tests/` still carry German strings (e.g. the gate-frame words `gruen`/`rot`); house rule 1 (AGENTS.md) forbids translating them in passing inside this change.

## Neighbours (for the header)

- `plans/changes/archive/2026-10-05-project-lock/spec.md` — the accepted spec that introduced project file, lock, `make venv`, the runner's interpreter choice and the environment check in the suite (bead coding-harness-ei0).
- `plans/changes/archive/2026-11-06-ci-minutes/` — dropped the 3.11 leg; pull-request interpreter = `tools.python[-1]`.
- `plans/changes/archive/2026-11-06-red-first-install/` — the stage-2 runner's red-first path and how a scratch checkout gets `.venv`-equivalents.
- `plans/changes/archive/2026-11-06-pi-pin/` — the other half of the before-verify setup named in `AGENTS.md`:151 (`tools/pi/install.sh`, bead coding-harness-hs0o).

`plans/specs/` holds no living specs (only `.gitkeep`), and sibling change folders include `bd-1-3-4`, `flaky-swarm-leak-test`, and `swarm-test-speed` (2026-11-18).
