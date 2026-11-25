---
title: "Research — slow-test-fixes"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.16
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-25", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
neighbours: []
---

# slow test fixes — Research

## Topic (bead coding-harness-bxxt.16, copied by the orchestrator 2026-11-25)

Class: bounded.

Why/What, each read at 18a13d3d: (1) tests/test_pi_contract.py:1268-1275
makes 14 real Pi calls, 5 identical baseline repeats -> drop the repeats.
(2) tests/test_stage2_research_catalog.py:936-938 waits a real
deadlineMs=10000 although held_collect (264-274) exists -> use it; the file
also has 66 cold node spawns via collect (185-261). (3)
tests/test_stage2_swarm.py:2489 finder sleep 5 -> a file barrier. (4)
tests/test_atomic_test_log.py:1087-1155 runs 24 nested pytest subprocesses,
12 with -n 2 -> bundle outcomes per (workers, drain). Related: coding-
harness-dca4, coding-harness-76sf, coding-harness-wnka.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp, night run 2026-11-24-a), from an external verify-speed analysis.



PARENT
↑ ○ coding-harness-bxxt: (EPIC) Verify speed and machine load P1

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu) · leak check clean over 1202 files, 5798 commits, 12 rules.

## Runner exploration — 2026-11-25

## Research: slow-test-fixes (phase 1, class `bounded`)

Scope: read-only facts about the four speed items in the bead (coding-harness-bxxt.16), checked against this worktree at `fix/slow-test-fixes` (HEAD `449f1872`). Nothing was run, timed or changed. Line numbers below are for cross-reference; the file and test or function name is the anchor.

### What exists today

**1. Pi contract, real-Pi calls (`tests/test_pi_contract.py`, `test_real_reviewer_ignores_discovery_traps`).** The test defines a local helper `call(omit=None, trusted=True)` that starts the real installed Pi through the `transport` fixture and a `StandIn` server. The test body makes 14 such calls: `call(trusted=False)` once, `call()` once, then a loop over six flags in `checks` (`--no-extensions`, `--no-mcp`, `--no-skills`, `--no-context-files`, `--no-prompt-templates`, `--no-themes`), each iteration making one `call()` and one `call(omit=flag)`. The count of 14 matches the bead. The `transport` fixture's default is `controls = {"trusted": False, "omit": None, "mcp_control": False}` (same file, the transport builder). The loop sets `mcp_control` to `True` only for `--no-mcp`, so five loop iterations plus the assertion before the loop (`call()`) issue the same configuration: six identical baseline calls, not the five the bead states. The bead's "5 repeats" may count only the loop iterations; this is a counting difference, not a contradiction.

**2. Catalog deadline and cold node spawns (`tests/test_stage2_research_catalog.py`).** `collect(tmp_path, sources, **options)` starts a fresh `node` process (`subprocess.run([... "node", "--input-type=module", "-e", script ...])`) on every call and runs the bridge's catalog code under traps. `held_collect(tmp_path, sources, held)` wraps `collect` with `deadlineMs=10000, controlledDeadline=control`; the controlled deadline fires on an event (a marker file and the count of answered bodies) instead of wall-clock time. `test_catalog_shared_deadline_keeps_asymmetric_failure_rules` already uses `held_collect` once (the `{"metadata"}` case, after `pi_delay = metadata_delay = 0.0`), and it also uses plain `collect(..., deadlineMs=10000)` at the "both slow past one shared deadline" step, where `pi_delay = metadata_delay = 60` makes the test wait for the real 10 s deadline. The bead's line 936–938 reference is that wall-clock step. A grep for `collect\(|held_collect\(` in the file returns 66 lines; two are the `def` lines, so about 64 invocations exist, and each invocation is one node spawn. The bead's 66 is the raw grep count and includes the two definitions.

**3. Finder sleep (`tests/test_stage2_swarm.py`, `test_stages_dispatch_concurrently_within_provider_limits`).** The test calls `sworld.complete(finder=[{"stdout": locator_report(), "sleep": 5}])`, then `sworld.run()`. It asserts overlap from the recorded start times (`t0`) and the configured sleeps: `spans = [(c["t0"], c["t0"] + c["sleep"]) ...]`, asserting a peak of at least 2 concurrent spans. The 5 s is the stand-in's scripted sleep, so the test takes about 5 s of wall time. The file has 26 matches for `sleep` in total. The test already has a comment naming criterion 36 and the planted fault (serial dispatch); the overlap check does not depend on the sleep being real wall time, only on the recorded span arithmetic. Whether the overlap is measured or only inferred from the spans was not checked in detail.

**4. Nested pytest subprocesses (`tests/test_atomic_test_log.py`, `test_runtime_check_keeps_every_access_until_session_finish`).** The test is parametrised over `drain` (2) × `workers` (0 and 2) × `outcome` (6: pass, skip, xfail, error, finalizer, setup), giving 24 cases. Each case writes a temporary project (`conftest.py`, `stand_in_log_guard.py`, `runner_clock_guard.py`, `atomic_test_log.py` copied from `tests/`) and runs `python -m pytest -q -p no:cacheprovider -n <workers>` in a subprocess with `timeout=180`. The 12 cases with `workers=2` run xdist; the 12 with `workers=0` run in-process inside the subprocess. The "24 nested subprocesses" in the bead is the parametrisation count. No file in the repository records a per-case duration.

### Where it lives

- `tests/test_pi_contract.py`: `test_real_reviewer_ignores_discovery_traps`, helper `call`, fixture `transport`, class/function `StandIn`.
- `tests/test_stage2_research_catalog.py`: `collect`, `held_collect`, `refuse_redirect_with_hold`, `test_catalog_shared_deadline_keeps_asymmetric_failure_rules`.
- `tests/test_stage2_swarm.py`: `test_stages_dispatch_concurrently_within_provider_limits`, fixture `sworld` (class `SwarmWorld`), `sworld.complete`, `sworld.run`.
- `tests/test_atomic_test_log.py`: `test_runtime_check_keeps_every_access_until_session_finish`, helper `_render`, helper files `tests/atomic_test_log.py`, `tests/stand_in_log_guard.py`.
- Repository timing data: none in the tree. The only baseline is in `plans/changes/swarm-test-speed/research.md`, section "Orchestrator addendum — 2026-10-28": one full `make verify` at `dbef390f`, 4082 passed in 520.43 s wall (`-n auto`, 8 cores), with the 50 slowest calls summing to 695.4 s. In that list, `test_stage2_swarm.py` accounts for 615.5 s (45 calls), `test_stage2_research_deep_review.py` 35.4 s, `test_pi_contract.py` 22.8 s, `test_stage2_research_catalog.py` 11.7 s, and `test_bead_render.py` 10.0 s. `tests/test_atomic_test_log.py` is not named in that addendum's top list.

### What is unclear

- **Measured duration of each cited test.** The bead's arithmetic (14 calls, 66 spawns, 24 subprocesses, 5 s sleep) is from source, not measured. Only `test_pi_contract.py` (22.8 s) and `test_stage2_research_catalog.py` (11.7 s) appear in the 2026-10-28 top-50 list; `test_atomic_test_log.py` does not appear in it, and the `test_stage2_swarm.py` finder test is not named individually there either. Whether the atomic-log test is in the top 50 today is not known.
- **Overlap with the neighbour `swarm-test-speed` (bead coding-harness-dca4, Draft, class `bounded`).** Its research names the same file (`tests/test_stage2_swarm.py`) and the same finder test with the same `sleep: 5` (under "Deliberate wall-clock sleeps"), and it states that this sleep is "expected in full". The two changes therefore reach the same test. Which change owns it is not settled in any artefact read here; it is an interview question.
- **Cost of the real Pi.** Whether `test_pi_contract.py` is skipped or runs in the verify gate depends on the `installed_pi` fixture and the pinned Pi (`tools/pi/install.sh`, referenced in `AGENTS.md`); the fixture was not read.
- **`coding-harness-76sf` and `coding-harness-wnka`** (named in the bead as related) occur in repository files (`ROADMAP.md`, `docs/WORKFLOW.md`, `decisions/gates.yaml`, several `plans/changes/` artefacts, `docs/journal/handover/`), but their meaning was not read; the explorer cannot read the tracker, so the bead texts are not known.
- **Whether any sleep in the cited tests is required by a behaviour the test asserts** (for example the 5 s finder sleep is the only route to the overlap assertion) was not established beyond the code shown above.

### Neighbour candidates (for the `neighbours:` header; not added here)

Matched by the search on the test file names, read only as far as the match:
- `plans/changes/swarm-test-speed/research.md` (same test, same file; strongest)
- `plans/changes/flaky-swarm-leak-test/` (findings, decisions, plan; mentions the catalog and swarm tests)
- `plans/changes/finder-partial-report/` (plan, findings; mentions the swarm tests)
- `plans/changes/venv-guard/` (plan, findings; matched on `test_pi_contract`)
- `plans/changes/review-loop-deep-a/` (research, plan, findings)
- `plans/changes/ledger-ids-before-pytest/` (ledger-related; `scripts/check_criterion_ledger.py` is the gate for criterion-named tests)

Not read beyond the grep match: their status and whether they touch the same functions.

### Which files a change would have to touch

Only as the four cited items locate them: `tests/test_pi_contract.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_swarm.py`, `tests/test_atomic_test_log.py`. Any change to the pytest call itself would also touch `decisions/gates.yaml`, `tests/test_ci.py` and the generated `.github/workflows/ci.yml` (per `plans/changes/swarm-test-speed/research.md`). The criterion ledger (`plans/changes/research-swarm/plan.md`, checked by `scripts/check_criterion_ledger.py`) pins test names in `tests/test_stage2_swarm.py`; whether the cited tests are pinned there was not checked.
