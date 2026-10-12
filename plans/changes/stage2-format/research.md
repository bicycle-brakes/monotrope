---
title: "Research — stage2-format"
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
tags: [research, stage2, implement, formatting]
---

# Stage-2 runner formats the attempt — Research

Phase 1 for bead coding-harness-52r, read against `origin/main` on
2026-10-12. In change stage2-repair (bead coding-harness-g2f) every attempt
of `implement` (GLM 5.3 Flash, its repair, the Sonnet 5.5 fallback) and every
attempt of the new `repair` verb failed `make verify` on the gates
`ruff-format` or `ruff-check` alone: the work models have file tools and no
command tool, so they cannot run the formatter. The orchestrator then ran
`ruff format` by hand and `make verify` went green. The bead asks the runner
to format the attempt's changed Python files (and apply ruff's safe fixes)
before `make verify`, so that a pure formatting miss no longer burns all
attempts. The change is meant to be small.

## Questions for the exploration

1. How `verify_attempt` and `prepare_derived` in `scripts/stage2.py` run
   today: which paths they read (`changed_paths`), which environment and
   which process launcher they use, and how a failure of the preparation
   becomes a diagnostic.
2. How the `ruff-format` and `ruff-check` gates of `make verify` call ruff
   (`scripts/verify_all.sh`, `Makefile`, `pyproject.toml` or `ruff.toml`):
   the version, the configuration, the paths they cover, and where the ruff
   executable lives in a worktree's `.venv`.
3. Which of ruff's fixes count as safe (`ruff check --fix` without
   `--unsafe-fixes`) under this repository's rule selection, and whether a
   safe fix can change behaviour or a test's meaning.
4. Which tests in `tests/test_stage2.py` pin the preparation step and the
   attempt sequence, and how a stand-in for `make` and for ruff is planted in
   the test world.
5. Whether formatting must run on changed `.py` files only or on the whole
   tree, and what happens to a file the model did not change but ruff would
   reformat.
6. Whether the step must be recorded (in `findings.md` or the commit) so a
   reader sees that the runner, not the model, formatted the code.

Stage-2 call, 2026-10-12: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 370 files, 938 commits, 12 rules.

## Runner exploration — 2026-10-12

Orchestrator note, 2026-10-12: the `repair` verb lives on branch
`feat/stage2-repair` (bead coding-harness-g2f, not merged on 2026-10-12); it
reuses `verify_attempt`, so a format step there serves both verbs once both
changes are merged.

### What exists today

**The runner's post-run path.** `scripts/stage2.py`, function `implement`: the allowed set starts as exactly the change's `findings.md`; changes outside it refuse the run before any model call (`allowed` / `outside` / the `Refused` raise in `implement`). The routes are `(GLM_FLASH, "flash")`, `(GLM_FLASH, "flash-repair")`, `(SONNET, "stage-1")` — three attempts, the list `routes` in `implement`. Per attempt: `begin_work_call` writes the audit line; `run_work_model(..., writable=True)` launches the model with the file tools of `WORK_WRITE_TOOLS` (`"Read,Grep,Glob,Edit,Write"`) and no command tool — the model cannot run a formatter itself; `worktree_tree` snapshots the tree before and after the model call through a temporary index seeded with `git read-tree HEAD` (its docstring: the real index, stash and refs are never touched), and `attempt_files` turns the pair into the bounded `git diff-tree --numstat` list. The comment above that pair states the boundary explicitly: the runner's own writes — audit line, route block, *the preparation*, the findings block — fall outside both snapshots by design. `test_each_failed_attempt_lists_only_the_files_its_model_changed` (tests/test_stage2.py) pins that the list never names `plans/INDEX.md` or `findings.md`.

**`verify_attempt`** (`scripts/stage2.py`) first builds its environment via `foreign_env({"GIT_CONFIG_COUNT": "1", … "commit.gpgsign": "false"})`; `foreign_env` copies only the names in `ENV_ALLOW` (PATH, HOME, USER, LOGNAME, SHELL, TMPDIR, LANG, LC_ALL, LC_CTYPE, TERM, TZ, CODEX_HOST — correction, CODEX_HOME) plus the call's own. Then `prepare_derived(root, env, key)`: any non-empty result is returned verbatim as this attempt's problems — `make` never runs. `prepare_derived` stamps changed held documents (through `check_frontmatter_current.load_map` / `is_held` / `stamp`, refusing paths outside the worktree, aliased paths and hard links, collecting all refusals into one diagnostic) and renders `plans/INDEX.md` via `launch([sys.executable, "scripts/plans_registry.py", "--index"], …)`. Every failure path returns the single string `["Derived-file preparation failed: …"]`, evidence tail cut (`TAIL_LINES = 80`, `_shrink`) and scrubbed (`scrub` replaces the credential and any fragment of ≥ 8 characters). On success, `launch(["make", "verify"], root, env)`: `launch` is a plain `subprocess.run(cwd=root, env=env, stdin=DEVNULL, capture_output=True, check=False)`, no shell. A non-zero exit becomes the diagnostic `` `make verify` exited N `` with `red_sections(done.stdout)` (the framed blocking gates) plus the last `STDERR_LINES = 40` lines of the run's standard error; a `launch` OSError raises `CallFailed`, which `implement` turns into "`make verify` could not be run" and stops with no further attempt. `implement` then appends failed attempts as a quoted block (`attempt_block` → `quote_block` → `append` to findings.md), feeds earlier diagnostics into the next attempt's prompt (`implementation_prompt`, section "Earlier post-run diagnostics"), re-scans for the key, and on green runs `checkpoint`: `git add -A`, exactly one commit `feat(<change>): implement accepted plan` as author `stage2-runner`, then the run refuses unless HEAD is exactly one descendant commit and the worktree is clean.

**The ruff gates.** The one command list is `decisions/gates.yaml`: `ruff-check` = `python3 -m ruff check scripts/ tests/` and `ruff-format` = `python3 -m ruff format --check scripts/ tests/`, both job `verify`, both enforcement `block`. `Makefile`'s `verify` only delegates to `scripts/verify_all.sh` (its header: the list is held against the Makefile by tests/test_ci.py). `verify_all.sh` picks `$PYTHON` (first the checkout's own `.venv/bin/python3` from `make venv`, else a PATH python3 importing PyYAML), substitutes it for `python3` in every gate command, and prepends the interpreter's directory to PATH so a gate calling bare `ruff` resolves into the locked environment — that caller is the `ramp-valves` gate (`scripts/ramp_valves.py`, which runs `ruff check --select <gruppe> --statistics .` over the whole tree, not only scripts/ tests/). ruff is pinned `ruff==0.9.10` (pyproject.toml dev group; requirements-ci.txt). In this worktree `.venv/bin/ruff` exists (Glob). Both ruff gates measure `scripts/` and `tests/` only; nothing in the chain restricts them to changed paths. Neither command carries `--fix`; `ruff format --check` checks, it never writes.

**The ruff configuration** (`ruff.toml`): line-length 120, target py311, `force-exclude = true` (its comment: excludes must also hold for explicitly named files — exactly how the vendoring surface was once reformatted), excludes `templates/dlt-patterns/`, `examples/projekt-repo-mock/`, `docs/archive/`, `docs/patterns/` (the last is the vendoring surface whose bytes must not move — ADR-026 exception, per the file's comment); lint `select = ["E4", "E7", "E9", "F", "I", "W", "ARG", "B", "UP", "SIM", "RET", "C4", "PTH"]`, per-file-ignores `"tests/fixtures/**" = ["F"]`; format `docstring-code-format = true`.

**The tests** (tests/test_stage2.py) pin the sequence: `test_implement_flash_has_file_tools_and_the_complete_contract` (file tools; `make` called exactly `["verify"]`), `test_first_implement_refreshes_derived_files_without_a_model_repair`, `test_preparation_stamps_only_changed_held_documents`, `test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics` (one make call per attempt), `test_renderer_failure_is_bounded_scrubbed_and_prevents_verify` (zero make calls when preparation fails), `test_broken_renderer_uses_existing_repair_limits_and_checkpoints_only_after_green`, the preparation refusal tests (outside-the-worktree, aliased, hard-linked, invalid-UTF-8, git without caller credentials), `test_a_postcheck_failure_gets_one_flash_repair_with_its_diagnostic` and `test_two_failed_postchecks_route_once_to_sonnet` (three make calls), `test_findings_only_dirt_is_allowed_and_committed` (after green, `git status --porcelain` is empty — all residual dirt is committed), and the attempt-block tests (diagnostics below the audit line, bounded file lists). The stand-in machinery: the `world` fixture writes one `STAND_IN` template as `codex`, `claude`, `pi` and `make` into a bin dir placed first on PATH; `world.script(make=[{"stdout": "green\n"}])` writes scenario.json; the stand-in records argv/env/cwd to calls.jsonl and can `plant`/`append`/`delete` files to imitate model edits. **No `ruff` stand-in exists in the fixture** — today the gate's ruff is only reached inside the make stand-in's canned output; a runner calling ruff directly would meet no stand-in in the test world (fact about the fixture, not a recommendation).

### Where it lives

Runner post-run path: `scripts/stage2.py` (`changed_paths`, `ignored_snapshot`, `restore_baseline`, `prepare_derived`, `verify_attempt`, `attempt_files`, `worktree_tree`, `attempt_block`, `checkpoint`, `implement`, `launch`, `foreign_env`, `ENV_ALLOW`, `scrub`, `red_sections`, `TAIL_LINES`/`STDERR_LINES`, `WORK_WRITE_TOOLS`). Gate list: `decisions/gates.yaml` (ids `ruff-check`, `ruff-format`, `ramp-valves`); runner of the list: `scripts/verify_all.sh` + `scripts/ci_gates.py`; Makefile recipes `verify`/`venv`/`lock`; pin: pyproject.toml dev group + requirements-ci.txt; config: `ruff.toml`; whole-tree measure: `scripts/ramp_valves.py`. Prose contract of the runner: `docs/WORKFLOW.md` states in the stage-2 section that the runner "runs `make verify`, checks for a measured line below `## Time used`" and that "a failed post-check gets one fresh Flash repair, then one" fallback — a new post-run step has a prose home there. Tests: `tests/test_stage2.py` (`world` fixture, `STAND_IN`, `successful_implementation`, the tests named above).

### Not found, and not there

- **Not there:** a `repair` verb. `VERBS` in `scripts/stage2.py` holds explore, implement, spec-review, review-loop, release-loop, review, probe; `main` adds `session`. No `repair` function is defined. The research frame ("every attempt of the new `repair` verb failed") and `plans/changes/codex-takeover/research.md` (bead coding-harness-g2f: "no verb exists today" in its question section, "is built" in the maintainer's-choice section of the same day) do not reconcile on this branch; where that work lives is not readable from this worktree.
- **Not found:** a `stage2-repair` folder under `plans/changes/` (glob), and a stage2-repair row in `plans/INDEX.md` (the family lists only stage2-format, research-currency, stage2-session).
- **Not there:** a `ruff` stand-in in the test fixture, and any `--fix` in the gate commands.

### What is unclear (open, not guessed)

- Whether any file under `scripts/` or `tests/` is currently unformatted or lint-fixable: not measurable in this session (file tools only, no command tool). The change cannot assume a clean tree.
- Which rules of the selected groups emit safe fixes, and whether a safe fix can change behavior or a test's meaning: that is ruff 0.9.10 documentation, which this session has not read. The in-repo facts end at the rule selection above.
- If the g2f repair-verb work lands before this change, `prepare_derived`/`verify_attempt` may have moved; this research reads the tree at `feat/stage2-format` HEAD (2412930).

### Files a change would have to touch (observed, not recommended)

`scripts/stage2.py` — a formatting step sits beside `prepare_derived` inside `verify_attempt`'s preparation phase, reusing `launch`, `foreign_env`, `scrub`, `_shrink`; a failure would join the existing diagnostic vocabulary (`Derived-file preparation failed: …` pattern). `tests/test_stage2.py` — the fixture's stand-in name list and the sequence tests named above. `docs/WORKFLOW.md` — only if the post-run contract's prose (the "runs `make verify`" sentence) must name the step. `decisions/gates.yaml` and `scripts/verify_all.sh` hold no runner knowledge; nothing else in the chain references the preparation step by name.
