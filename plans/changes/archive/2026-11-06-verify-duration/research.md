---
title: "Research — verify-duration"
status: accepted
implementation_status: done
date: 2026-11-04
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-1um6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# verify duration — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md).
The runner's exploration is preserved below; the draft-stage gap checks are
an addendum, not a replacement of the exploration.

Stage-2 call, 2026-11-04: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 882 files, 3240 commits, 12 rules.

## Runner exploration — 2026-11-04

Phase-1 exploration for `verify-duration` is done — read-only, nothing edited. Here is the research, ready to append to `plans/changes/verify-duration/research.md`.

---

## What exists today

**The verify run itself.** The `verify` target in the `Makefile` (`Makefile`, target `verify`, lines 18–19) runs `bash scripts/verify_all.sh`. That script holds no gate commands of its own: it asks `scripts/ci_gates.py`, and that reads `decisions/gates.yaml` — the one gate list (`scripts/verify_all.sh` header comment, lines 2–7; `ci_gates.py` `report()` docstring, "Bindet den Lauf an einen Weltzustand"). Jobs are `verify`, `drift`, `docs` (`verify_all.sh` argument parse, lines 74–83).

**No duration is measured anywhere in the local runner.** The gate loop (`verify_all.sh` lines 204–224) prints gate id, command and verdict (`gruen` / `RED (block)` / `rot, aber nur <enforcement>`), and the run ends with `VERIFY GREEN`/`VERIFY RED` (lines 227–231). I read the whole file (233 lines, 2026-11-04): there is no start/end timestamp, no per-gate elapsed, no total elapsed. `ci_gates.py report()` (`ci_gates.py:494–505`) binds the run to job, candidate SHA, merge-base SHA, gate-file SHA-256 and gate counts — no duration field. The catalog legend in the generated CI names "⏱ = Drift-Job (Timer)" (`ci_gates.py` `catalog_rows()`, the legend string near line 850) — that "Timer" names the nightly scheduled drift job, not a duration mechanism. Hosted CI step durations exist only in the GitHub Actions UI; no tracked file keeps a copy of them (not found).

**Time around the gates is not gate time.** `scripts/verify_lock.py` queues every protected entry machine-wide (one `verify.lock`, FIFO by registration, `verify.queue/` records) and waits for free memory — floor 25 percent, rechecked every 30 s, refusal after 60 low minutes (module docstring, lines 2–55). Its docstring states the queue and memory waits consume neither `VERIFY_SECONDS` nor a pytest proof's execution timeout (line 70). So wall-clock around a verify contains admission wait that no gate measurement would see.

**The runner's one time budget.** `VERIFY_SECONDS = 30 * 60` (`scripts/stage2.py:3992`) is the `timeout=` of both `verify_attempt`'s and `verify_draft`'s launches (`stage2.py:5561–5562` and `7815–7816`). The decision record of `draft-gates-only` keeps it shared with the reason "no measurement asks for a shorter bound" (`plans/changes/draft-gates-only/decisions.md`, `[DETAIL]` at lines 36–37) — i.e. a recorded gap where a duration measurement was named as the missing input.

**Worker sizing affects duration and is already machine-derived.** Without a caller value, `verify_all.sh` sizes `PYTEST_XDIST_AUTO_NUM_WORKERS` itself: the smaller of half the logical cores and memory in 2-GiB steps (lines 89–162, bead coding-harness-l7sc); the contract lives in `plans/changes/verify-worker-cap/spec.md` (terms at lines 41–48).

**The only machine-written duration records in the repository measure model attempts, not gates.** One writer, `scripts/time_records.py` — the fixed record under `## Time used` in a change's `plan.md`, grammar `RECORD` (lines 36–42: date, start–end UTC, explicit seconds, verb, attempt, route, model, accepted|rejected, marker "measured by the runner"). Writers: the runner (`stage2`), and `harness.py time-log` for an interactive session's own span with `route orchestrator` (`scripts/harness.py` docstring lines 22–37). Reader: `scripts/run_report.py` / `make report` (docstring lines 2–13), which also warns at half the plan card's appetite (`docs/WORKFLOW.md:517–520`). Doctrine: seconds are explicitly supplied, never computed from the timestamps (`docs/WORKFLOW.md:504–515`; `time_records.py` docstring lines 11–12). The sibling change `runner-time-line` (`plans/changes/runner-time-line/spec.md`, bead 9wp) made the runner measure its own implementation/repair attempts for the same reason — a model cannot take the measurement.

**Known duration numbers, all ad-hoc prose, each with its cut-off:**
- about 24 min full `make verify`, sequential run, 2026-10-19 (`docs/journal/handover/2026-10-19-optimization-exploration.md:54`), same file: pytest alone 20:38 for 2285 tests, kit probe `leerprobe` 163 s (lines 55–57); the `-n 4`/`-n 8` figures there are marked load artefacts (lines 165–166).
- PR #168 (`perf/verify-xdist`, merged 2026-10-19 13:49): pytest 3:58 with `-n auto` on an idle machine (same handover, lines 39–42 and 166); hosted CI 5m01s at PR #169 against 10–16 min before (same file, addendum table row 2).
- about 11 min full verify on 2026-10-28, pytest 515–638 s (`docs/how-it-works.md`, "Runs take time", lines 289–290).
- 888 s pytest alone for 4426 tests on 2026-11-02 at `98d58db9` (same section, lines 290–291).
- 12–13 min under the machine's one verify lock, measured 2026-10-30 — the number behind the targeted-check rule after a hand repair (`docs/WORKFLOW.md:1646–1657`, bead coding-harness-24ag).
- pytest baseline 520.43 s with eight workers at `dbef390f` on 2026-10-28; 45 of the 50 slowest calls were swarm tests; a profile attributed 37.3 s cumulatively to 376 declaration reads (`plans/changes/swarm-test-speed/spec.md:31–38`, bead coding-harness-dca4).
- about 12 minutes verify after a draft run — the stated motivation for the `docs` job (`draft-gates-only/decisions.md:28`).
- about 10 minutes, measured 2026-10-16 (`docs/research/2026-10-21-night-run-plan.md:195`).
- The planned `pytest --durations=30` slow-test measurement (bead coding-harness-7so, night-run lane 6) had not run as of 2026-10-21 (`docs/journal/handover/2026-10-21-night-run-codex.md:69`; `docs/research/2026-10-21-night-run-plan.md` lane 6). Bead coding-harness-dca4 (slowest tests) is narrowed and still open (`docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md:66`).

**No pytest duration configuration exists.** `[tool.pytest.ini_options]` in `pyproject.toml` holds only `pythonpath = ["."]` (lines 32–33) — no `addopts`, no `durations`; that is "not there", distinct from "not found".

## Where it lives

- Runner: `scripts/verify_all.sh` (gate loop, worker sizing, admission exec), `scripts/ci_gates.py` (`report()`, `generate_ci()`, gate list reader), `scripts/verify_lock.py` (admission).
- Gate list: `decisions/gates.yaml` (per-gate `id`, `enforcement`, `command`, `placement`; the pytest gate at its lines 57–63).
- Duration records: `scripts/time_records.py`, `scripts/harness.py` (`time-log`), `scripts/run_report.py`, plan files' `## Time used` sections.
- Budget: `scripts/stage2.py` `VERIFY_SECONDS`.
- Prose numbers: `docs/how-it-works.md`, `docs/WORKFLOW.md`, `docs/journal/handover/`, `docs/research/`.
- Tests that pin these: `tests/test_time_records.py`, `tests/test_run_report.py` (e.g. `test_measured_durations_sum_without_audit_or_live_double_counting`, line 246), `tests/test_stage2.py` (e.g. lines 2159, 3818, 5921 pin `VERIFY_SECONDS` on launches).

## What is unclear about it

- **The bead's own goal statement is not readable in this phase.** The tracker is the Dolt database under `.beads/`; the only tracked mentions of `coding-harness-1um6` are `plans/INDEX.md:444` and the research file's own frontmatter. What "verify duration" shall become — a local runner printing per-gate and total time, persisted records, a re-derived budget, or a one-off measurement — is not stated in any tracked file I found (not found). Open question for the interview.
- **No per-gate or per-run duration table exists anywhere in tracked files** (not found). The hosted CI's step timings are outside the repository; every local number above was taken by hand and written as prose.
- Whether a verify duration would join the `## Time used` record grammar is undecided by anything existing: today's `RECORD` fields (verb · attempt · route · model · result) describe a model attempt, not a gate run; the grammar is deliberately single (`time_records.py` docstring lines 3–14) and is read by runner, time-log and report alike, so a second grammar would contradict that contract.
- The handover addendum of 2026-10-19 classifies `scripts/verify_all.sh` as `bestand` ("does not travel", `docs/journal/handover/2026-10-19-optimization-exploration.md` addendum vehicle table). That is outdated: `scripts/kit/manifest.yaml:85–87` today classifies it `mechanismus` (bead bo0), as it does `scripts/verify_lock.py` (lines 88–90) and `scripts/ci_gates.py` (lines 79–81) — a change here travels with the kit.

## Which files a change would have to touch

Any implementation would live on the measured path or the reading path; the placement facts:

- `scripts/verify_all.sh` — the only place where the local run's per-gate and total wall time is observable in one process (loop at lines 204–224).
- `scripts/ci_gates.py` — `report()` (lines 494–505) if a run report should carry durations, and `generate_ci()` (line 655) for the derived `.github/workflows/ci.yml`.
- `decisions/gates.yaml` — if duration were to become a gate-declaration property (schema lives in `ci_gates.py` `validate_schema()`, line 315).
- `scripts/time_records.py`, `scripts/harness.py`, `scripts/run_report.py`, `tests/test_time_records.py`, `tests/test_run_report.py` — only if verify spans joined the fixed record grammar.
- `scripts/stage2.py` (`VERIFY_SECONDS`, line 3992) and `tests/test_stage2.py` — only if a measurement were to re-derive the budget.
- `docs/WORKFLOW.md` (verification section, targeted-check rule at lines 1646–1657) and `docs/how-it-works.md` ("Runs take time", lines 289–294) — where duration statements live as prose today.

## Suggested `neighbours:` for the header

All read and confirmed to exist: `plans/changes/verify-machine-lock/spec.md` · `plans/changes/verify-worker-cap/spec.md` · `plans/changes/draft-gates-only/spec.md` · `plans/changes/swarm-test-speed/spec.md` · `plans/changes/runner-time-line/spec.md` · `plans/changes/run-report/spec.md` · `plans/changes/time-records-data/spec.md` · `plans/specs/implementation-verification/spec.md`.

---

Nothing was designed or recommended above; the interview question about the bead's exact goal is the one open item the maintainer needs to answer.

## Draft-stage gap checks — 2026-11-04

Read at `4d57b1c0`: `decisions.md` now settles the goal in three maintainer
answers: persistent per-gate measurements, local history with machine context,
and at least five baseline runs plus a warning-budget proposal.

- `templates/plan.md` and `scripts/validate_change_artefacts.py` do not exist
  in this worktree; the plan form is specified in `prompts/03-plan.md`.
- `scripts/verify_lock.py` measures queue wait for logging, but its ownership
  record exposes only pid, token, command and start; `_memory_gate()` waits
  separately. Measurement context must cover both and survive CLI supervision
  and inherited `hold_admission` entries without changing admission behavior.
- `tests/test_ci.py::_runner_tree_files` copies the runner, gate reader and
  admission module explicitly. Any new runtime helper must join these fixtures.
- `scripts/kit/manifest.yaml` ships the runner, lock and their existing tests;
  its fallback rules leave unlisted scripts and tests behind. A new runtime
  helper and its tests therefore need explicit mechanism entries.
