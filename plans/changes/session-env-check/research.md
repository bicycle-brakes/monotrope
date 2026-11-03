---
title: "Research — session-env-check"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-cjf9
owner: framework-architect
provenance: human-written
tags: [research]
---

# session env check — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-03: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 842 files, 3173 commits, 12 rules.

## Runner exploration — 2026-11-03

Phase-1 exploration complete. Here is the research, ready to append to `plans/changes/session-env-check/research.md`.

---

## What exists today

**The setup a session needs is documented as manual steps; nothing measures it at session start.** `AGENTS.md` ("Sessions across checkouts", bullet on worktrees) requires each new checkout or worktree to run `make venv` and `bash tools/pi/install.sh` once before `make verify`, and house rule 2 ("Beads only") requires `tools/beads/install.sh && tools/bd bootstrap --yes` in a fresh clone before any tracker-reading gate can measure. These are prose rules; no hook or script verifies they were run.

**Environment checks exist only inside the gates, so they surface at `make verify`, not earlier.**

- `Makefile`, target `venv`: reads `requires-python` from `pyproject.toml`, refuses an interpreter below it *before* `.venv` is created (the bead coding-harness-y9q refusal), then builds `.venv` and installs `requirements-ci.txt` with `--require-hashes`. `PYTHON` defaults to the first of `python3.12`/`python3` on PATH.
- `scripts/verify_all.sh`: picks the interpreter — `$PYTHON` if set (a relative path with a `/` is made absolute against `$PWD`), else the first of `$PWD/.venv/bin/python3` and PATH `python3` that imports `yaml`; with neither it exits 2 with "no python3 with PyYAML — build the locked environment with make venv, or set `$PYTHON`". It also fronts the machine-wide verify admission (`scripts/verify_lock.py`) and sizes pytest workers from cores/memory.
- `tests/test_lock.py`: `environment_problems()` compares the running environment against the lock and the declared interpreters (`tools.python: ["3.12"]` in `decisions/gates.yaml`, read through `ci_gates.interpreters()`); `test_the_environment_matches_the_lock` runs it for real, and every problem message ends in the `HINT` "build the locked environment: make venv …". `test_make_venv_refuses_an_interpreter_below_the_declared_minimum` and `test_make_venv_installs_the_lock_in_hash_checking_mode` pin the Makefile recipe. All of these run when pytest runs — a session that never starts `make verify` never sees them.
- `tools/pi/install.sh` checks Node/npm and the Node major against `tools/pi/.node-version`, then installs with `npm ci --ignore-scripts`; `tools/pi/pi` (the wrapper) re-checks Node major, manifest pin and installed version at every start and never installs or falls back (`tools/pi/README.md`, "Fresh clone" and "Verify an install"). When Pi or Node is missing, `tests/test_pi_contract.py` fails — it never skips (`tools/pi/README.md`, "What the tests install versus what they run").
- `tools/bd` refuses a version that does not match `tools/beads/VERSION`, exits 127 with an install hint when no `bd` binary exists, and refuses `init`/`migrate`/`upgrade`; `tools/beads/install.sh` installs the pinned binary checksum-verified to `~/.local/bin/bd-<version>`.

**What a session sees at start today, mechanically:**

- Repository-level: `.claude/settings.json` registers exactly one SessionStart hook — `"$CLAUDE_PROJECT_DIR"/tools/bd prime --hook-json`. A fresh clone without the tracker bootstrap makes this fail or return nothing about readiness.
- User-level (installed into `~/.claude` by `tools/claude-code/install.sh`): `tools/claude-code/hooks/handover.sh start` (SessionStart) shows the latest handover, its next step and a measured block — git facts only: branch, HEAD, uncommitted-file count, upstream distance, beads in progress (the `render` function's `facts` array). `tools/claude-code/hooks/parallel-sessions.sh` reports same-checkout clashes through `hooks/session-scan.sh`; `tools/claude-code/statusline.sh` shows repo/branch/model/context/beads/sessions/recap plus a "⚠ cwd moved" warning. **None of these measures the development environment** — venv, Pi, bd, node are not among the measured facts; git state and beads are.

**The hosted CI and the cloud environment build what a local session must build by hand.**

- `scripts/ci_gates.py` generates the CI setup steps: `setup-tracker` (`bash tools/beads/install.sh` + `bd bootstrap`), `setup-python` (`actions/setup-python`), `setup-deps` (the one hash-checked lock install), `setup-node` (from `tools/pi/.node-version`), `setup-pi` (`bash tools/pi/install.sh`). Checkout and setup-deps deliberately carry no `if` (comment in `scripts/ci_gates.py`; asserted in `tests/test_ci.py`, "checkout and setup-deps deliberately do not carry the `if`").
- `tools/cloud-env/setup.sh` (pasted into the cloud platform, runs before Claude Code starts; idempotent) installs Python 3.11/3.12, the pinned bd, builds `.venv` with `uv venv --python 3.12`, installs the lock with `--require-hashes`, and runs `tools/bd bootstrap --yes` per repository, restoring the two files bootstrap rewrites. Its known limits are recorded in `tools/cloud-env/README.md` ("Known limits": the copied bd checksum is not held to the repository's by any check; clone-order in a fresh environment not observed).

**The nearest existing "preflight" mechanisms are for models, not the dev environment:** `scripts/stage2_availability.py` (tool-free probes `probe_go`, `probe_claude`, receipt `seal`/`verify` for `prepare-loop`/`prepare-explore`) and the `preflight` in `scripts/stage2.py` used by `scripts/stage2_session.py` (executables must exist before a foreign call). Neither touches `.venv`, Pi or the tracker.

## What is unclear

- **The bead's intent is unreadable from tracked files.** The description of bead coding-harness-cjf9 lives in the Dolt tracker (`.beads/`), which a read-only file explorer cannot query; it was not read. What "session env" should cover (venv only? Pi? bd/tracker? node?) and where the check should live are open questions for the interview.
- **Recorded pain this name plausibly refers to** (facts, not judgement): `docs/journal/handover/2026-10-19-optimization-exploration.md` measured `.venv/bin/` without an interpreter (state since 2026-10-07), `scripts/verify_all.sh` silently falling back to *another repository's* virtualenv on PATH, `test_the_environment_matches_the_lock` red, and 10 Pi-contract errors without `node_modules`; the repair list there was `make venv` + `tools/pi/install.sh`. `docs/journal/handover/2026-10-15-night-run-fourth.md`: every worktree needs `make venv` once. `docs/journal/handover/2026-10-22-night-run-claude.md`: a relative `PYTHON` broke the leerprobe gate (became bead coding-harness-4x2c).
- **A namesake to keep apart:** the planned `guard-test-environment` entry in `decisions/gates.yaml` (open interview question 5 in `docs/journal/handover/2026-11-02-five-lane-night.md`; acceptance criterion 11 in `plans/changes/guard-test/spec.md`) guards the `STAGE2_PLANT_FAULT` switch in the *verification* environment; it does not exist in `decisions/gates.yaml` on this branch yet and is unrelated to checkout readiness.
- **"Not found" vs "not there":** I found no session-start environment check in the four user-level hooks (all read in full) or in `.claude/settings.json` beyond `bd prime`; no script in `scripts/` (full file listing reviewed by name) checks checkout readiness. A `guard-test-environment` gate is *not there yet* (confirmed by reading `decisions/gates.yaml`'s `tools:` block and gate list head).

## Which files a change would have to touch (candidates from evidence)

- The check's logic would sit near the existing environment machinery: `Makefile` (target `venv` as the guarded-recipe model), `scripts/verify_all.sh` (interpreter choice and its exit-2 message), `tests/test_lock.py` (`environment_problems`, the `HINT`), `decisions/gates.yaml` (`tools.python`).
- If it reports at session start in this repository: `.claude/settings.json` (the SessionStart hook list).
- If it reports through the maintainer's display: `tools/claude-code/hooks/handover.sh` (the `render`/measured block), `tools/claude-code/statusline.sh`, plus `tools/claude-code/install.sh`, `tools/claude-code/settings.json` and `tools/claude-code/README.md` (install and merge of a new hook).
- Docs that state the manual steps: `AGENTS.md` (house rule 2; "Sessions across checkouts"), `docs/WORKFLOW.md` ("Worktrees — one per change"; the toolchain table row for `uv`/`mypy`/`python3`/`ruff`/`pytest`).
- Tracker readiness: `tools/bd`, `tools/beads/install.sh`, `tools/beads/VERSION`.

## Neighbours (for the header)

`plans/changes/archive/2026-10-05-project-lock/spec.md` (read; introduced the project file, the hash-checked lock, declared interpreters and the environment checks) · `plans/changes/venv-pycache/spec.md` (read; runner tool-integrity baseline over `.venv`) · `plans/changes/verify-absolute-python/spec.md` (read; absolute `$PYTHON` through verify) · `plans/changes/verify-machine-lock/spec.md` (path known, not read; machine-wide verify admission) · `plans/changes/pi-pin/spec.md` (path known, not read; the Pi pin) · `plans/changes/guard-test/spec.md` (read; the `guard-test-environment` namesake).
