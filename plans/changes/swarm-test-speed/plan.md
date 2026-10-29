---
title: "Plan — swarm-test-speed"
status: draft
implementation_status: partial
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-dca4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, performance, stage2]
---

# Plan — swarm-test-speed

```text
For you:     Swarm tests and real runs spend less time rereading unchanged model declarations; admission checks stay current.
Done when:   Three matched before/after runs show a lower median, regression checks pass, existing coverage is preserved, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Leak-check optimisation, fixture rewrites, test consolidation, new dependencies or verification-gate changes.
Pre-mortem:  suppose it failed: most likely because reuse hides a declaration edit at the next call boundary.
Starts unless you say stop.
```

Baseline `ae855930`, inspected 2026-10-28. Implements `spec.md` and the
maintainer's production-scope answer (`decisions.md#Q-1`). Bounded: no design
phase or ADR. No `templates/plan.md` exists; this follows `prompts/03-plan.md`.
Explore used Stage 2, GLM 5.3 Flash via `glm-coding-plan`; no Stage-1 fallback
is recorded. The card was shown to the maintainer unchanged before phase 4;
implementation was accepted at `e7046a39` (runner, attempt 2).

## Files and steps

1. Before editing production code, collect the existing pytest node IDs to
   a temporary file and measure the command below three times, alone on the
   machine, using the pinned environment. Record each successful elapsed
   time and the median here. Historical evidence (520.43 s suite at
   `dbef390f`, 32.9 s slowest call, 2026-10-28) is context only.
2. Create `tests/test_stage2_declaration.py` with the ledger's focused reader
   regressions. Use temporary roots and real file reads; count actual YAML
   parses, not timing in unit assertions. Compare results to the old
   `yaml.safe_load(path.read_text(encoding="utf-8")) or {}` contract,
   normalising its existing read/decode/YAML/non-mapping failures. Cover
   nested values, dates, Unicode, aliases, empty/falsy and non-mapping roots,
   unsafe tags and invalid inputs under both available safe loaders. Prove
   loader selection falls back when `CSafeLoader` is absent. Run the new
   reuse regression against the old reader and record its assertion failure.
3. Change `scripts/stage2_availability.py` only at the shared declaration
   reader and private helpers/imports: read current bytes on every call,
   decode UTF-8, parse with `CSafeLoader` when available and `SafeLoader`
   otherwise. Reuse successful parses with a process-local bounded cache
   (eight entries keyed by contents and loader); never key by path/mtime,
   cache read failures, or return the private cached object. Deep-copy the
   result for each caller, including the initial miss. Preserve the exact
   dictionary-or-error-string contract, empty/falsy normalisation and safe
   tags. Ordinary concurrent cache misses may parse twice; they must not
   corrupt results. No persistent cache or cached admission verdict.
4. In the new test file, warm the cache before same-size/same-mtime edits,
   atomic replacement, switching roots, deletion, injected `OSError`, bad
   UTF-8/YAML and recovery. Mutate nested returned data and exercise concurrent
   callers using barriers, not sleeps. Check cache capacity is bounded and
   that a warm declaration still gets current terms evaluated after moving
   the terms clock past expiry. Use the production research send guard for
   the declaration-change check; retain existing expiry/leak integration tests.
5. Repeat the isolated command three times after the change with identical
   Python, environment, worker settings and test input. Record times, medians,
   date and source revisions here; if noise or concurrent load invalidates
   the comparison, repeat both sides rather than asserting a speedup.
   Collect node IDs again; review old tests/guards/gates against the baseline
   and compare pre-existing cases. Run full verification once with timing.
6. Change this `plan.md` only to turn written ledger entries into test entries
   and record phase-4 evidence/time. The runner manages `findings.md` evidence,
   the generated `plans/INDEX.md`, full verification and the final commit.
   No other implementation files are created, changed or deleted.

The bounded cache, defensive copies, safe-loader fallback and median comparison
are reversible implementation details chosen to retain freshness and portability.

## Criterion ledger

- 1: tests/test_stage2_declaration.py::test_reader_matches_safe_load_contract — values, types or refusal differ from the old reader.
- 1: tests/test_stage2_declaration.py::test_reader_preserves_safe_loader_contract — the reader accepts a tab separator or refuses an escaped surrogate pair differently from the old pure-SafeLoader reader, or rejects valid tabs in scalar content or comments.
- 1: tests/test_stage2_declaration.py::test_reader_parses_with_the_pure_safe_loader — the reader parses with another loader than the pure SafeLoader, or loads an unsafe tag.
- 2: tests/test_stage2_declaration.py::test_unchanged_contents_reuse_a_bounded_parse_cache — repeated reads parse again or distinct inputs grow the cache beyond its bound.
- 3: tests/test_stage2_declaration.py::test_changed_contents_are_read_without_metadata_shortcuts — edits, replacement or a different root return stale data.
- 4: tests/test_stage2_declaration.py::test_read_failure_never_returns_a_cached_declaration — a bad/missing/unreadable current file returns an earlier mapping or recovery fails.
- 5: tests/test_stage2_declaration.py::test_returned_declarations_are_isolated_across_threads — nested mutation leaks to another caller or a later read.
- 6: tests/test_stage2_declaration.py::test_warm_cache_preserves_live_research_admission — a declaration edit or UTC expiry is ignored by the production guard.
- 6: tests/test_stage2_terms_expiry.py::test_research_probes_and_dispatch_recheck_expiry — research launches after expiry, including a cutoff during a leak scan.
- 6: tests/test_stage2_swarm.py::test_launch_record_keeps_individual_leak_check_before_launch — a launch lacks its own preceding clean scan.
- 6: tests/test_stage2_swarm.py::test_leak_block_cancels_queued_dispatch — queued calls launch after a BLOCK.
- 7: not a test — three successful matched runs on each side, recorded here; after median at least before median or unmatched conditions refute the speedup.
- 8: not a test — baseline diff and collected node-ID comparison; removed cases, renames, weakened assertions, skips/xfails or changed gates refute preservation.

## Verification and boundaries

Use the pinned environment, with no other verification or benchmark running.
The orchestrator ensures prerequisites are installed before phase 4.
For each of the three before and three after measurements, run verbatim:

```bash
PYTEST_ADDOPTS= /usr/bin/time -p .venv/bin/python -m pytest -p no:xdist tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons -q
```

Full verification, timed with the existing eight-core `-n auto` configuration:

```bash
PYTEST_ADDOPTS=--durations=50 /usr/bin/time -p make verify
```

Do not edit old tests, model declarations, leak checks, dispatch/call boundaries,
dependencies, gates, generated CI or neighbouring change ledgers. Stop at the
appetite and report unmet criteria; do not weaken them. The advertised
`scripts/validate_change_artefacts.py` is absent, so it cannot be reported green;
index generation and tracker-dependent gates remain the runner's responsibility.

## Measurement — 2026-10-28

All runs by the orchestrator on 2026-10-28, macOS, 8 cores, Python 3.12.15,
the pinned `.venv`, with the verbatim single-test command above. "Before" is
the baseline commit `5c4ddcbd` (the plan with no production change; spec and
plan as drafted at `7bc010f0`); "after" is `e7046a39`, the accepted
implementation. The header's `ae855930` is the commit the drafter inspected;
the code under test is identical at all three baseline commits, which differ
only in this folder's documents.

**Matched comparison** (finished 18:05 UTC). Before and after alternated in
one sequence, before first, so both sides ran under the same load: one other
lane's `make verify` was running throughout, so the machine was shared, not
isolated. pytest's reported time per run:

| Run | Before (`5c4ddcbd`) | After (`e7046a39`) |
|---|---|---|
| 1 | 49.27 s | 22.48 s |
| 2 | 45.42 s | 22.76 s |
| 3 | 39.13 s | 15.27 s |
| Median | **45.42 s** | **22.48 s** |

Wall times (`/usr/bin/time -p`, real) were 129.94 / 45.81 / 39.47 s before
and 22.97 / 23.13 / 15.59 s after; the first before-run includes a cold start
after the worktree was created. The median falls by about half.

An earlier, unmatched set (`7bc010f0`, before only, 16:3x UTC, also beside a
running `make verify`: 22.22 / 16.70 / 15.48 s real) is superseded by the
matched set above; it is kept here because review rows L1-1 and L1-2 refer
to it.

**The new regressions against the old reader** (plan step 2; review rows
L1-8, L1-11). `tests/test_stage2_declaration.py` from `e7046a39`, run against
the scripts of `5c4ddcbd`: 5 failed, 19 passed. The five failures:
`test_reader_selects_safe_loader_with_fallback` ("the C safe loader was not
chosen although it is available"), `test_unchanged_contents_reuse_a_bounded_parse_cache`
("an unchanged declaration was parsed again on an immediate repeat"),
`test_changed_contents_are_read_without_metadata_shortcuts` ("an unchanged
declaration was parsed again"), `test_read_failure_never_returns_a_cached_declaration`
(the injected read failure did not reach the old reader, which reads with
`read_text`), and `test_warm_cache_preserves_live_research_admission` ("an
unchanged declaration was parsed again at the guard"). At `e7046a39`: 24
passed.

**Preserved tests** (criterion 8). `pytest --collect-only` over `tests/`:
4079 node ids at `5c4ddcbd`, 4103 at `e7046a39`; none removed or renamed,
and all 24 new ids are in `tests/test_stage2_declaration.py`. The
implementation diff changes no existing test file, gate or pytest option.

**Full suite.** Full `make verify` at `cf71a96c` (after the round-1
repairs), 2026-10-28 21:14–21:25 UTC, run `nice -n 10` with `-n 4` while one
review loop ran remotely: green; pytest 4086 passed, 17 skipped in 514.89 s;
wall time 648 s. The slowest test calls are still in `tests/test_stage2_swarm.py`
(the slowest 29.61 s). An earlier full run at the same stand under memory
pressure (1861 s, 12 `TimeoutExpired`) is void and not counted. No full-suite
baseline before the change was taken under the same conditions, so this is a
reading, not a before/after comparison; the matched comparison above stays the
evidence for the speed criterion.

## Isolated re-measurement — 2026-10-29

Phase-6 row F6-2 (the 2026-10-28 runs shared the machine with another
lane's `make verify`). Repeated by the orchestrator on 2026-10-29,
07:42:13–07:43:34 UTC, macOS, 8 cores, Python 3.12.15 with this worktree's
pinned `.venv` for both sides, the verbatim single-test command of
"Verification and boundaries", `nice -n 10`. All six runs ran inside one
hold of the machine's verify lock (`lockf` on
`~/.local/state/coding-harness/verify.lock`), so no `make verify`, runner
implement, repair or draft of any lane ran meanwhile; remote model calls of
other lanes did, and the one-minute load average stayed between 2.77 and
3.54 throughout. Before and after alternated, before first, each in its own
detached checkout: "before" is `5c4ddcbd` (no production change), "after" is
`703869a3` (the accepted implementation plus round-1 repairs, unchanged
reader since `cf71a96c`). pytest's reported time, all six runs `1 passed`:

| Run | Before (`5c4ddcbd`) | After (`703869a3`) |
|---|---|---|
| 1 | 18.44 s | 12.73 s |
| 2 | 14.91 s | 9.05 s |
| 3 | 14.66 s | 9.51 s |
| Median | **14.91 s** | **9.51 s** |

Wall times (`/usr/bin/time -p`, real): 18.64 / 15.11 / 14.84 s before,
12.95 / 9.25 / 9.70 s after. The median falls by about 36 % (5.40 s). This
set replaces the shared-machine set of 2026-10-28 as the evidence for
criterion 7; the earlier set stays above because review rows refer to it.

## C loader against pure loader — 2026-10-29

Measured by the orchestrating session (lane coordinator), not by this lane,
and recorded here with that provenance: at `d58005fe`, the single test
`tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons`
with `-p no:xdist`, three alternating runs each, about 09:33 UTC on
2026-10-29, one-minute load about 2.3. With libyaml's C loader: 9.09 / 9.02 /
9.01 s (median 9.02 s). With the pure `SafeLoader`: 8.99 / 9.05 / 9.11 s
(median 9.05 s). 134 `yaml.load` calls either way. The whole speedup comes
from the content-keyed cache; the C loader adds nothing measurable. On this
basis the maintainer chose option A for phase-6 row F6-3 (2026-10-29): drop
the C loader, keep the cache.

## Runner route — 2026-10-28

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-10-28 16:40:39–17:18:51 UTC, 2291 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-28 17:18:59–17:40:17 UTC, 1278 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
2026-10-28 18:07:44–18:19:38 UTC, 713 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-28 18:19:45–18:37:47 UTC, 1083 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-28 18:38:00–18:53:02 UTC, 902 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-29 08:10:21–08:22:09 UTC, 708 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner

## Appetite stop — 2026-10-28

At 21:47 UTC, after phase 6 (Codex session 01a18477) found two MAJOR rows. The
measured spans under Time used sum to 6267 s, 1.74 h of the 2-hour appetite.
The orchestrator's hand repairs of review round 1 were not timed, so the
real use is higher. The two rows need more than the time left: F6-1
(CSafeLoader accepts a tab before a comment that SafeLoader refuses,
criterion 1) and F6-2 (the before/after runs were not isolated,
criterion 7). Both need a code or scope change, an isolated
re-measurement in the verify slot and a full `make verify`.

Answer (orchestrator, night rule of 2026-10-28/29, which allows cut, park
or drop but never continue): **park**. Proposed for the maintainer: a cut
that keeps only the parse cache, drops the C loader (and with it F6-1),
re-measures three isolated runs per revision for F6-2, and comes with a new
appetite of 1 hour.
