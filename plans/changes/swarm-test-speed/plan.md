---
title: "Plan — swarm-test-speed"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
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
is recorded. This runner draft stops before implementation; the orchestrator
shows the card unchanged before phase 4.

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
- 1: tests/test_stage2_declaration.py::test_reader_selects_safe_loader_with_fallback — unsafe loading or missing C support breaks a valid read.
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

## Baseline measurement — 2026-10-28

Measured by the orchestrator at `7bc010f0` (before any production change),
with the verbatim single-test command above, three times in a row:
22.22 s, 16.70 s, 15.48 s real; median 16.70 s. **Not alone on the
machine:** another worktree's `make verify` (a runner attempt) ran during
all three runs, so these numbers are disturbed. The after-measurement
repeats both sides under the same load, or both alone, before any speedup
is claimed.

## Time used

2026-10-28 16:40:39–17:18:51 UTC, 2291 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-28 17:18:59–17:40:17 UTC, 1278 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
