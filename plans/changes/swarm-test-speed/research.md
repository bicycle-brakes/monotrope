---
title: "Research — swarm-test-speed"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-dca4
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
---

# swarm test speed — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-28: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 714 files, 2461 commits, 12 rules.

## Runner exploration — 2026-10-28

Translated into English by the orchestrator on 2026-10-28; the runner's
German answer is preserved unchanged at commit `7d4f80ed`. Content, sources
and counts are the runner's; only the language and the framing sentences
around the report changed (bead coding-harness-g19n).

Proposed header line (the runner adds what its finders propose):

```yaml
neighbours:
  - plans/changes/research-swarm/spec.md
  - plans/changes/terms-test-fixtures/research.md
  - plans/changes/terms-expiry/spec.md
  - plans/changes/runner-time-line/spec.md
  - plans/changes/free-member-rate-limit/spec.md
  - plans/changes/pi-pin/research.md
```

### What exists today

**The change folder is a skeleton.** `plans/changes/swarm-test-speed/` holds
only `research.md` (class `bounded`, bead `coding-harness-dca4`, owner Data
Architect, `provenance: human-written`); no spec, plan or decisions exist yet.
The registry row exists (`plans/INDEX.md`, row
`changes/swarm-test-speed/research.md`, Draft, 2026-10-28). The opening commit
names the bead in its subject: `change(swarm-test-speed): open the change
folder, class bounded (bead coding-harness-dca4)` (branch
`perf/swarm-test-speed`, commit `e8da4068`).

**The suite has exactly one speed lever, and it is pinned in three places.**
The pytest call is `python3 -m pytest tests/ -q -n auto`, declared once in
`decisions/gates.yaml` (gate id `pytest`, job `verify`, enforcement `block`),
run locally by `scripts/verify_all.sh` (which takes its commands only from
that one gate list) and generated into `.github/workflows/ci.yml` (step id
`pytest`; the workflow header says hand edits trip the `ci-drift` gate).
`Makefile` `make test` runs the same command, and `tests/test_ci.py` pins the
string mapping `"python3 -m pytest tests/ -q -n auto": "make test"`. The dev
dependencies are `pytest==8.3.4`, `pytest-xdist==3.8.0`, `ruff==0.9.10`
(`pyproject.toml`): there is no timeout plugin, no test markers, no
`--durations` reporting and no `conftest.py` anywhere under `tests/` (a glob
and the terms-test-fixtures research reach the same conclusion). CI runs one
leg on Python 3.12 (`tools.python` in `gates.yaml`); the job has no
`timeout-minutes`.

**The swarm test file is the suite's second-largest behavioural file and the
most expensive per test.** `tests/test_stage2_swarm.py` has 3051 lines with
123 test functions before parametrisation (parametrisation adds dozens: for
example `test_invalid_given_neighbours_refuse_before_models` runs 8 cases,
`test_failed_pi_calls_preserve_partial_evidence` 2×3,
`test_free_model_storage_keys_preserve_best_effort_completion` 3×2). Its
structure:

- The `sworld` fixture (dataclass `SwarmWorld`) builds a temporary
  repository per test: `git init` plus a first commit (two git subprocesses
  through `SwarmWorld.commit`), seeds `research.md`/`spec.md`/`plan.md`, an
  `AGENTS.md` and `src/app.py`; copies the repository's real `prompts/`
  (12 files) and `model-endpoints.yaml` (578 lines) into it; rewrites the
  real declaration's seat models with `admissible_terms` from
  `tests/terms_fixtures.py`; compiles the two stand-in programs `pin-pi` and
  `claude` from the embedded `STAND_IN` source plus a failing bare `pi` trap;
  restricts `PATH`, `HOME`, `XDG_STATE_HOME`, secrets and denylist; and
  monkeypatches `stage2_availability.consume_research` to return a consumed
  selection.
- Every behavioural test calls `sworld.run()`, which runs
  `stage2.main(["explore", "demo", ...])` *in process*. A full dispatch has
  39 + 3N slots — the tests assert `len(sworld.calls()) == 39 + 3*len(FREE)`
  (`test_selected_free_models_cover_all_online_topics_on_identical_briefs`) —
  and every slot is a real subprocess: a new CPython interpreter running the
  stand-in script (`Run.launch`, `scripts/stage2_research_run.py`,
  `subprocess.Popen(..., start_new_session=True)`).
- The file makes roughly 130 `sworld.run()`/`fx.prepare()` calls (counted by
  grep); about 60+ of them are full runs, the rest short runs (refusals end
  with exit 2 before any model starts and cost only fixture work) and two- or
  three-run loops for resume and store-fault cases
  (`test_a_resumed_run_is_a_new_run_within_its_slot_budget`, the store-fault
  cluster around
  `test_a_failed_store_write_keeps_every_outcome_and_still_publishes_incomplete`).
  As arithmetic, not a measurement: ~60 full runs × ~40–45 subprocesses give
  several thousand interpreter starts in this file alone, plus a few hundred
  short runs.
- Deliberate wall-clock sleeps in the stand-ins' scenarios: `sleep: 20` in
  `test_leak_block_cancels_queued_dispatch` (cut short, because the
  dispatcher stops running children on a leak BLOCK — `supervise` in
  `scripts/stage2_research_dispatch.py` calls `_stop_and_reap` when
  `stop.is_set()`; the 20 s are a safety margin, not run time), `sleep: 5` on
  the finder trio in `test_stages_dispatch_concurrently_within_provider_limits`
  (expected in full, ≈5 s run time), `sleep: 0.2–0.4` on all topic slots in
  `test_concurrent_slots_keep_distinct_audits_and_outcomes` and
  `test_provider_limit_is_shared_across_topics_and_roles` (passed through the
  Go queue of width ≤4, each around 2–3 s), and `sleep: 30` timeout failures
  bounded to ≈1.8 s by
  `monkeypatch.setitem(stage2_research_run.MINUTES, "topics", 0.03)` (two
  parametrised cases of `test_failed_pi_calls_preserve_partial_evidence`,
  plus `test_a_receipt_without_output_survives_a_complete_run`). The tests
  confirm the timing indirectly: `stage2_research_run.MINUTES == {"finders":
  10.0, "merge": 10.0, "sentence": 5.0, "topics": 10.0, "judge": 15.0}` and
  `RUN_MINUTES == 150.0` (`test_amended_graph_and_deadlines_bound_every_launch`),
  and the `CLOCK` monkeypatches move fake time instead of waiting
  (`test_required_slots_precede_free_and_reserve_judge_time`,
  `test_no_call_starts_once_the_run_deadline_is_spent`).

**Per-slot costs in the dispatch that each of these ~40-call runs pays.**
Before every launch `Run.gate` (`scripts/stage2_research_run.py`) runs
`stage2_availability.read_declaration` — a full re-read and YAML parse of the
578-line declaration — plus up to two `research_terms_problem` calls and a
leak check over files, commits and rules (`runner.leakcheck.check`); the free
admission reads the declaration again (`free_admission` in `Run.launch`).
Each slot gets its own `tempfile.TemporaryDirectory` and writes a launch and a
result record through the sealed store (`stage2_research_store`, sha256
`_seal`/`_read_sealed`). The dispatcher supervises each child with
`communicate(timeout=TICK)` where `TICK = 0.05`
(`scripts/stage2_research_dispatch.py`), and waiting workers sleep 0.01 s.

**Neighbouring test files share this world.**
`tests/test_stage2_terms_expiry.py` imports the fixture (`from
test_stage2_swarm import sworld as research_world`) and
`tests/test_stage2_research_deep_review.py` imports `SwarmWorld`,
`manifest_of` and `status_line`; both run the same temporary-repository runs.
`tests/test_stage2_research_dispatch.py` (31 tests) exercises the dispatcher
directly with real child processes and its own `sleeper()` scripts (sleeps of
0.05–0.4 s, with 30/60 s failures ended early by slot allowances). The wider
suite: 2142 test functions in 58 files (counted by grep);
`tests/test_stage2.py` has 691 with large sleeps of its own and is the suite
of the single-explorer runner, not the swarm; `tests/test_pi_contract.py`
starts the real installed Pi against loopbacks since ADR 0019
(`docs/WORKFLOW.md`, section "Review-loop Pi flags").

**Couplings that constrain any speed change.** The criterion-ledger gate
(`scripts/check_criterion_ledger.py`; gate `criterion-ledger`, reason in
`gates.yaml`: deleting 29 of 30 criterion tests left `make verify` green,
bead coding-harness-909) — `plans/changes/research-swarm/plan.md` pins ~80
named tests in `test_stage2_swarm.py` (ledger block, lines ~779–911), and a
renamed or deleted entry turns RED while that change lives and after it is
archived. A grep over `plans/` shows that only the research-swarm change's
artefacts reference these test names. The synthetic run-time seat terms must
satisfy the full ADR 0022 admission rule — the exact trap the commissioned
neighbour `terms-test-fixtures` (bead hxkw, `implementation_status: partial`)
documents; its research already maps the same fixture sites, including this
file's `sworld` fixture.

### Where it lives

- The suite itself: `tests/test_stage2_swarm.py` (`SwarmWorld`, `sworld`,
  `STAND_IN`, `SwarmWorld.run/rewind/commit/complete`); shared builder
  `tests/terms_fixtures.py`; fixture reuse in
  `tests/test_stage2_terms_expiry.py`,
  `tests/test_stage2_research_deep_review.py`; dispatcher level
  `tests/test_stage2_research_dispatch.py`.
- Production cost path (read only, in case the machinery is in scope):
  `scripts/stage2_research_run.py` (`Run.gate`, `Run.launch`,
  `Run.on_terminal`), `scripts/stage2_research_dispatch.py` (`TICK`,
  `supervise`, `worker`), `scripts/stage2_availability.py`
  (`read_declaration`, `research_terms_problem`),
  `scripts/stage2_research_store.py` (`_seal`, `_read_sealed`,
  `write_launch`, `write_result`).
- Suite wiring: `decisions/gates.yaml` (gate `pytest`), `Makefile`,
  `scripts/verify_all.sh`, generated `.github/workflows/ci.yml`, the pin in
  `tests/test_ci.py` (~line 459), `pyproject.toml`
  `[tool.pytest.ini_options]`.
- Ledger constraint: `plans/changes/research-swarm/plan.md` (criterion-ledger
  block), enforced by `scripts/check_criterion_ledger.py`.

### What is unclear

- The bead's exact motivation and scope: the title and description of bead
  `coding-harness-dca4` could not be read in this phase (the tracker is the
  Dolt database under `.beads/`; reading needs `tools/bd show`, which the
  runner runs, not the explorer). Whether "swarm test speed" means only
  `tests/test_stage2_swarm.py` or also the dispatch, deep-review and terms
  files that reuse the same world is an interview question.
- Whether `plans/changes/research-swarm/plan.md` (bead icw, itself still
  Draft per `plans/INDEX.md`) may change — that decides whether tests in the
  ledger file may be renamed or merged, or only sped up in place.
- No baseline measurement exists in the repository: no gate or artefact
  records suite or test durations (no `--durations` flag, no benchmark note
  in `docs/research/`; checked in `gates.yaml`, `Makefile` and
  `docs/WORKFLOW.md` — not found). Any "faster" target has no number to
  compare against today.
- No handover in `docs/journal/handover/` names `swarm-test-speed` or `dca4`
  (grep over the directory — no match), so the motive is not recorded in the
  journal; the change was opened on this branch after the last handover was
  written.

### Which files a change would have to touch

- Unavoidable: `tests/test_stage2_swarm.py` (fixture, stand-in, sleeps,
  number of runs per case).
- Likely: `tests/terms_fixtures.py` and the two reusing files
  `tests/test_stage2_terms_expiry.py`,
  `tests/test_stage2_research_deep_review.py` (if the fixture or setup gets a
  shared optimisation).
- Only if the gate itself is touched: `decisions/gates.yaml` plus the pin in
  `tests/test_ci.py` plus the regenerated `.github/workflows/ci.yml` (any
  change to the pytest call, for example duration reporting or sharding,
  touches all three).
- Only if a pinned test name changes: `plans/changes/research-swarm/plan.md`
  (criterion ledger).
- Only if per-slot costs (re-parsing the declaration, leak-check scope,
  `TICK`) are in scope: `scripts/stage2_research_run.py`,
  `scripts/stage2_research_dispatch.py`, `scripts/stage2_availability.py` — a
  behaviour change there would be more than a test-only bounded change and
  should be named in the interview.

The runner's closing note: this was phase 1 for `swarm-test-speed` (class
`bounded`, GLM 5.3 Flash route); nothing was designed, recommended, rated or
changed. Open for the interview are the bead text and the missing baseline
measurement.

## Orchestrator addendum — 2026-10-28

Answers to two of the open points above, read from the tracker and from a
measurement the explorer could not see.

- **The bead's scope** (bead coding-harness-dca4, "Measure the test suite's
  run time and speed up its slowest tests", read with `tools/bd show` on
  2026-10-28): class bounded, test-only speedups; no gate, criterion or test
  is deleted. Step 2 asks for concrete speedups of the slowest tests, for
  example a prepared git template copied instead of built per test. A
  duplicate-test audit is a separate question after the measurement.
- **Baseline** (measured 2026-10-28 at `dbef390f`, one full `make verify`
  with no other verify running, `PYTEST_ADDOPTS=--durations=50`): pytest
  4082 passed, 17 skipped in 520.43 s wall (`-n auto`, 8 cores). The 50
  slowest calls sum to 695.4 s; 45 of them are in
  `tests/test_stage2_swarm.py` (615.5 s together; slowest 32.9 s,
  `test_research_carries_practice_architecture_and_adjacent_spec_comparisons`),
  then `test_stage2_research_deep_review.py` 35.4 s, `test_pi_contract.py`
  22.8 s, `test_stage2_research_catalog.py` 11.7 s, `test_bead_render.py`
  10.0 s. `tests/test_stage2.py` (1230 tests) has none in the top 50. The
  raw list is not in the repository; the numbers are in the bead's notes.

## Orchestrator profile — 2026-10-28

One profile of the slowest swarm test, measured 2026-10-28 at `bb1585c7`
(`python3 -m cProfile -m pytest -p no:xdist tests/test_stage2_swarm.py -k
test_research_carries_practice_architecture_and_adjacent_spec_comparisons`;
the profiler roughly doubles wall time: 69.9 s here against 32.9 s in the
baseline):

- `yaml.safe_load`: 509 calls, 46.8 s cumulative (0.092 s each), of which
  `stage2_availability.read_declaration` 376 calls, 37.3 s — the 578-line
  declaration parsed again before every slot (`Run.gate`, 156 calls) and in
  `research_terms_problem` (312 calls, 24.8 s, overlapping).
- `leakcheck.check`: 156 calls, 20.1 s, of which `leakcheck._git` 468
  subprocess calls, 15.8 s.
- The store's sealing (`_seal`, 327 calls) costs 0.05 s in total; it is not
  a cause.
- PyYAML 6.0.2 in the venv is built with libyaml
  (`yaml.__with_libyaml__ == True`), but `read_declaration` uses the
  pure-Python `safe_load`.

So the cost sits in production code the tests drive (`scripts/`), not in
the test fixtures: the per-slot re-read of the declaration dominates, the
per-slot leak check comes second. A test-only change can shrink the
declaration the fixture copies; a production change could parse with the
C loader or reuse a parse while the file bytes are unchanged. Which of the
two is in scope is a maintainer question (the bead says test-only).
