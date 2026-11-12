---
title: "Research — verify-tmp-cleanup"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-12
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3-flash, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
---

# verify tmp cleanup — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). The
intent below was written by the orchestrator (Claude Code) before the first
call; the runner exploration (GLM 5.3 Flash) follows it unchanged, its
German opening sentence included.

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-bxxt.3, class bounded. On 2026-11-09 about 21:40 UTC the
data volume ran full (1.0 GiB free); a test run ended with "No space left on
device" and 239 errors. Two finished runs had left 1.3 and 1.5 GiB under the
pytest temporary root. Wanted: each run of the full check uses a base
temporary folder of its own and removes it when it ends, green or red, also
after an interrupt; a red run may keep it only on request. Related: the
free-disk check at admission (bead coding-harness-87b0).

Questions for the exploration: where the test gate gets its temporary root
today (`decisions/gates.yaml`, `scripts/verify_all.sh`, pytest configuration)
and whether a base folder can be set without editing the held gate list; how
the runner's own targeted and cheap test runs get theirs; what cleans up
after a killed run, given that the verify lock already supervises process
groups (`scripts/verify_lock.py`); which tests would misread a removed
folder.

Stage-2 call, 2026-11-10: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1007 files, 3889 commits, 12 rules.

## Runner exploration — 2026-11-10

Research complete. Hier das Fazit in einem Satz: **Keine Stelle im Baum setzt heute eine pytest-Basis-Temp-Folder — jedes pytest läuft unter dem pytest-eigenen Default-Root, Aufräumen nach Laufende existiert nur für Prozessgruppen, nicht für Dateien** — und die W-6-Pin-Tests halten die Gate-Kommandozeile byte-genau fest. Der vollständige Befund, ready to append:

---

## What exists today

**The verify chain and its one list.** `make verify` runs `bash scripts/verify_all.sh` (Makefile, target `verify`). The runner holds no gate command of its own: it asks `scripts/ci_gates.py`, which reads `decisions/gates.yaml` (verify_all.sh header comment; the gate loop reading `gid/enf/cmd` from TSV). The pytest gate is id `pytest`, command `python3 -m pytest tests/ -q -n auto`, job verify, enforcement block, floor true, placement both (decisions/gates.yaml, gate `pytest`). `make test` duplicates that command verbatim, and `test_the_makefile_runs_what_the_one_list_runs` (tests/test_ci.py:507, W-6) compares the **whole recipe line** between Makefile and gate list — a flag added to one side only turns this test red.

**Nothing in the repository sets a base temporary folder.** Pytest configuration is `pyproject.toml` `[tool.pytest.ini_options]` with `pythonpath = ["."]` only (pyproject.toml:32); there is no `conftest.py` at the root or under `tests/`, no pytest.ini/setup.cfg/tox.ini (Glob over those names matched only pyproject.toml). A repo-wide Grep for `basetemp` and for `PYTEST_DEBUG_TEMPROOT` returns no matches — both are "not there" statements, searched 2026-11-10 over this worktree.

**What the default root therefore is (pytest 8.3.4, pinned in pyproject.toml dev group).** `TempPathFactory.getbasetemp()` in the locked install (`.venv/lib/python3.12/site-packages/_pytest/tmpdir.py:140-197`): temp root = `PYTEST_DEBUG_TEMPROOT` or `tempfile.gettempdir()` (i.e. `$TMPDIR`), then `pytest-of-<user>/pytest-<N>`, created through `make_numbered_dir_with_cleanup(prefix="pytest-", ..., keep=self._retention_count)`; the ini options `tmp_path_retention_count` (default 3) and `tmp_path_retention_policy` (default "all") are declared in the same file (`pytest_addoption`, lines 225-237). Older numbered roots are pruned **only when a later pytest session starts** — never at run end, and not at all if no further run happens. Two side facts from the same function: a *given* basetemp is `rm_rf`'d at session start (lines 149-153), so a per-run folder gets a clean start for free; and the rootdir ownership is checked (st_uid must match, lines 174-183).

**Evidence of that root on this machine.** Recorded failures across many changes quote `/private/var/folders/.../T/pytest-of-mikypiky/pytest-<N>/popen-gw*/...` paths — e.g. plans/changes/status-fields-restore/findings.md:51-53, plans/changes/red-first-own-refs/findings.md:80 (pytest-6891), and a historical `OSError: [Errno 28] No space left on device` under that root in plans/changes/archive/2026-11-06-beads-close-themselves/findings.md:121. The 2026-11-09 event's figures (1.0 GiB free, 239 errors, 1.3/1.5 GiB left) are the orchestrator's bead-intent statement above; the repository holds no artifact recording that run.

**How the runner's own test runs get their temp root — the same default, everywhere.** `scripts/stage2.py` runs targeted tests with `PYTEST = (".venv/bin/python3", "-m", "pytest", "-q", "-n", "auto")` (stage2.py:4220) via `run_targeted()` (stage2.py:6100); `targeted_pytest_env()` (stage2.py:6063-6097) sets only `PYTEST_XDIST_AUTO_NUM_WORKERS`, mirroring verify_all.sh's worker sizing (verify_all.sh:89-162). The cheap checks run the same constant over selected tests (stage2.py:5872); the red-first proofs run pytest under `verify_lock.hold_admission(["pytest", ...])` (stage2.py:6949, 7139-7166). The kit probe (leerprobe gate) runs pytest in a throwaway copy made by `tempfile.mkdtemp(prefix="kit-probe-")` (scripts/kit/probe.py:375) writing `--junit-xml` into that scratch (probe.py:346-355), inheriting the environment minus `BEAD_RENDER` (probe.py:351). `PYTEST_ADDOPTS` is written by no script — it appears only as a hand-set measurement knob in past plan cards (plans/changes/swarm-test-speed/plan.md:106, 112; plans/changes/archive/2026-11-06-verify-duration/plan.md:111; docs/research/2026-11-04-verify-duration-baseline.md:31) and inside `tests/test_repo_settings.py:1251` for the live ruleset gate.

**What cleans up today — process groups, not files.** `scripts/verify_lock.py` already owns guaranteed end-of-run work: `supervise()` (verify_lock.py:923-959) spawns the protected command in its own session (`_spawn_child`, `start_new_session=True`, line 870), traps SIGINT/SIGTERM/SIGHUP/SIGQUIT (`_install_signal_handlers`, 796-812), stops the child's whole process group SIGTERM-then-SIGKILL (`_stop_child`, 882-890), ends leftover grandchildren (`end_lingering_group`, 903-921), and releases in a `finally` on every ending (949-958); the module docstring's "Boundary" names the one accepted overlap — an intermediate process killed hard while descendants run in another group (verify_lock.py:44-49). **No component removes the pytest temporary root**: verify_all.sh (read in full) has no `trap` and no temp handling; stage2.py removes only its own structures (worktree/mirror/attempt scratch `rmtree` sites, stage2.py:4828, 5330, 5387-5388, 7113); pytest prunes old roots only at the next session start. This matches the neighbour note's diagnosis "Housekeeping is missing. Temporary test folders … pile up until the disk is full" (docs/research/2026-11-09-make-verify-long-term.md, "What has to be better" item 7) and its proposed step "Clean up after a run: remove the run's own temporary folders; refuse admission under a free-disk bound (bead coding-harness-87b0, open)" (same note, "Proposed order of work" step 1).

**A per-run identity already exists.** verify_all.sh creates `RUN_ID` before gate selection (`dur_call RUN_ID start --job …`, verify_all.sh:226) and `scripts/verify_duration.py` stores under the shared state root `verify_lock.state_root()` = `${XDG_STATE_HOME:-~/.local/state}/coding-harness/` (verify_duration.py:80, 132; verify_lock.py:182-198).

**Constraints a base folder must respect.** The admission state root is deliberately *not* TMPDIR: the verify-machine-lock change weighed `$TMPDIR` and chose the XDG state root because TMPDIR is per-boot (plans/changes/archive/2026-11-06-verify-machine-lock/decisions.md:41 and research.md:54). TMPDIR already has other writers/readers in this tree: the maintainer's statusline cache `${TMPDIR:-/tmp}/claude-statusline` (tools/claude-code/statusline.sh:37; hooks/handover.sh:147; tools/claude-code/README.md:137 "until the machine clears it"), hook temp files `mktemp "${TMPDIR:-/tmp}/beads-start.XXXXXX"` (tools/claude-code/hooks/beads-start.sh:96, 117-118, 140-142), and the kit probe's `kit-probe-*` scratch (probe.py:375) — a cleanup that removes more than its own subfolder would destroy these. `ENV_ALLOW` for foreign programs names `TMPDIR` (stage2.py:391-404), the renderer runs with a scratch `HOME`/`TMPDIR` under the attempt scratch (stage2.py:5296-5297, 5381), `research_capture.py` preserves `TMPDIR` in saved environments (scripts/research_capture.py:641), `pr_sync.py` sets `TMPDIR` to a scratch subfolder (scripts/pr_sync.py:587), and `close_merged_beads.py` warns about TMPDIR inside a checkout (scripts/close_merged_beads.py:220).

**The disk boundary is a separate bead.** The admission has a memory gate only (`_memory_gate` and `read_available_memory`, verify_lock.py:706-730 and 354-387); no disk check exists in verify_lock.py. The free-disk floor is bead coding-harness-87b0, open (docs/research/2026-11-09-make-verify-long-term.md:107, 192; the 2026-11-02 five-lane-night handover, "Needed" section lines 90 and 134; plans/changes/night-machine-facts/research.md:54 states the boundary explicitly: -yql7 is facts at start, -87b0 a floor in the admission). Cleanup and floor are adjacent, not the same work.

**Which tests would misread a removed folder — none found that read a persistent temp path.** A Grep over `tests/` for `gettempdir|TMPDIR|tempfile\.mkdtemp|pytest-of` matches only two monkeypatches of `stage2.tempfile.mkdtemp` (tests/test_stage2.py:13965, 14929), which intercept the call, not a real path. Suite isolation is `tmp_path`/`World(root=…)` inside a single run's basetemp, so end-of-run removal after the session ended cannot misread them. What *will* execute a runner-side mechanism is the set of tests that run the real runner in a throwaway tree: tests/test_ci.py:1297, 1364, 1410, 1431, 1449, 1475, 1810, 1830 copy and invoke `verify_all.sh`, and the nested-admission marker test at tests/test_verify_lock.py:338 asserts on the child environment; the runner-env seam strips inherited worker env (`_runner_env`, around tests/test_ci.py:1516, plus worker pass-through tests at 1568-1656 and 2278). If the base folder were delivered via `PYTEST_ADDOPTS`, the live ruleset gate at tests/test_repo_settings.py:1251 combines its own value with it. `targeted_pytest_env` is pinned by tests/test_stage2.py:23758-23762.

## Where it lives

Gate source: `decisions/gates.yaml` (gate `pytest`). Runner: `scripts/verify_all.sh` (worker sizing 89-162, admission re-exec 178-190, duration block 192-298, gate loop 254-288). Guaranteed-cleanup hook: `scripts/verify_lock.py` (`supervise` finally-block 949-958). Other pytest callers: `scripts/stage2.py` (4220, 5872, 6063, 6100, 6949, 7139-7166), `scripts/kit/probe.py` (344-371, 375). Pytest config: `pyproject.toml` `[tool.pytest.ini_options]`. Pins: tests/test_ci.py:507 (W-6), tests/test_ci.py:1256-1267 (verify_all.sh must stay command-free; allowed callees only `ci_gates.py` and `verify_duration.py`), tests/test_stage2.py:23758-23762, tests/test_verify_lock.py:338, tests/test_repo_settings.py:1251.

## What is unclear about it

- The tracker is unreadable in this phase: whether beads coding-harness-bxxt.3 and coding-harness-87b0 carry maintainer notes beyond the intent above is an open question.
- Whether the 239 errors were all ENOSPC or partly knock-on failures is not recorded in the tree — the intent's summary is the only source. `[GAP]`, not asked.
- Whether hosted CI needs the same per-run guarantee is stated nowhere in the tree; that hosted runners clean `$TMPDIR` per job is general GitHub-runner knowledge, unverified here. `[GAP]`.
- Whether `PYTEST_DEBUG_TEMPROOT` is set on the maintainer's machine (outside the tree) is unknown; within the tree nothing sets it.
- No repository artifact states the removal policy (per-run removal vs. keep-on-red-on-request) — the only wording is the bead intent above. That is the interview's question, not a fact.

## Which files a change would have to touch

`decisions/gates.yaml` and `Makefile` **together** if the gate command line changes (W-6 pin, tests/test_ci.py:507-534); a mechanism that avoids editing the command line bypasses that pin. `scripts/verify_all.sh` for a runner-side mechanism, held command-free by tests/test_ci.py:1256-1267. `scripts/verify_lock.py`'s `supervise()` cleanup path is the only in-tree hook that provably runs on normal exit, red gates, cancellation and trapped signals — and its "Boundary" (verify_lock.py:44-49) states that a SIGKILLed supervisor leaves nothing to clean with; no in-process design escapes that case. `scripts/stage2.py` (targeted/cheap/proof launch sites) and `scripts/kit/probe.py` if their pytest runs must share the guarantee. `pyproject.toml` is the only existing in-tree pytest config point (retention ini options available there). Existing tests that must stay green: the ones listed under "Where it lives".

**Neighbours.** The header's one neighbour, docs/research/2026-11-09-make-verify-long-term.md, carries the parent diagnosis and proposes exactly this cleanup step beside bead 87b0 (its "How the approach is structured today", "What has to be better" 7, "Proposed order of work" 1). Suggested additions from this pass: `plans/changes/archive/2026-11-06-verify-machine-lock/` (the state-root-vs-TMPDIR precedent, decisions.md:41) and `plans/changes/night-machine-facts/research.md` (the 87b0 boundary statement, line 54).

## Redraft baseline — 2026-11-12

Repository-only follow-up at `2fd91ebc`, after the maintainer answered Q-1
in `decisions.md`. The 2026-11-10 exploration above describes the original
baseline; it must not be read as a description of the rejected-attempt code
now present in this checkout.

- `scripts/verify_all.sh` still re-execs through `--tmp-scope` and queries
  `--tmp-held` before its ordinary admission block. `scripts/verify_lock.py`
  contains `_TempScope` and associated lifecycle code. Read-only comparison
  against the checkout's `origin/main` reports 606 added and 15 removed
  lines in that module. The new decision requires leaving this module
  unchanged and replacing the runner's use of that lifecycle.
- `tests/test_ci.py` already has real copied-runner placement, nesting,
  verdict, option and entry-contract tests; they currently read the old
  scope marker and container naming. `tests/test_verify_lock.py` ends with
  the rejected architecture's temporary-scope block; the ordinary admission
  and process-group tests precede it. Replacement behavioral proofs belong
  at the runner entry Q-1 selected, without removing those ordinary tests.
- `findings.md` records three rejected implementation attempts, with red
  temporary-scope tests. It contains no open phase-2a review rows. Its
  latest call record identifies this redraft; earlier green draft checks
  are historical evidence, not a claim about the current implementation.
- `templates/plan.md` and `scripts/validate_change_artefacts.py` were not
  found in this worktree. The spec template, phase-3 prompt and available
  interview, criterion-ledger, research-handoff and frontmatter checks are
  present. No external source is needed for this bounded redraft.

External session-registry and live pull-request state were not read under
this attempt's worktree-and-git-directory restriction. No tracker write or
repository-changing git command was made.

### Draft retry diagnosis — 2026-11-12

The first decision-aligned draft's post-run document check failed before
executing a gate. At `2fd91ebc`, `scripts/verify_all.sh` still invokes
`scripts.verify_lock --tmp-scope` before admission. In that module,
`_flock_descriptor` yields but has no context-manager decorator;
`_TempScope.start` uses its generator in a `with` statement, matching the
reported `TypeError`. This is a source-code baseline failure, not a failed
document criterion. No fresh full-run result is claimed from this reading.

Q-1 already requires replacing that runner entry and leaving the module
unchanged. Phase 4 therefore removes the obsolete entry while implementing
the runner-local lifecycle; it does not repair or reactivate `_TempScope`.
Until then, the runner's document-job post-check remains blocked even when
the directly invoked document checks pass. This draft cannot remove that
blocker within its permitted artifact-only writes.
