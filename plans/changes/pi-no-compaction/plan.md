---
title: "Plan — pi-no-compaction"
status: draft
implementation_status: partial
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, runner, pi]
---

# Plan — pi-no-compaction

```text
For you:     Runner-created Pi settings disable automatic summaries, and an overflowing review member fails.
Done when:   All five settings paths are pinned by tests, the installed Pi 1.5.0 overflow contract passes, and make verify is green.
Appetite:    1 hour of phase 4, repairs included — a stop, not an estimate.
Not now:     Interactive/user settings, diff limits, routing, new failure kinds or a Pi version change.
Pre-mortem:  suppose it failed: most likely because one settings writer was missed.
Starts unless you say stop.
```

## Scope and baseline

Implement spec criteria 1–2 from baseline `8a7ada25` (read 2026-11-06).
The bounded interview has a reasoned skip; no design or ADR is due.
Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash`; no Stage-1
fallback was recorded. `findings.md` has no phase-2a rows to incorporate.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent;
use the phase-3 prompt's form and report the validator as unavailable.

## Build sequence and files

1. In `tests/test_stage2.py`, extend the existing reviewer isolation assertion
   and discovery refresh/listing test to check the exact two-key JSON from
   each launch's `agent_settings`; cover both paid and free reviewers.
   In `tests/test_stage2_availability.py`, extend the static-probe test to
   assert that same JSON for every probe. In `tests/test_stage2_swarm.py`,
   add `test_research_pi_settings_disable_compaction` using the launch seam
   to read settings before scratch cleanup, covering repository and public
   seats (the capture route inherits `Run.pi_command`). Record red evidence
   through the runner before editing production writers.
2. In `scripts/stage2.py`, add `compaction: {enabled: False}` beside retry
   at the discovery and reviewer writes; retain the byte-copy listing path.
   Update only the adjacent bound comment: the 2000-line limit now protects
   cost and attention, and compaction is disabled in runner agent settings.
   In `scripts/stage2_research_run.py` (`Run.pi_command`) and
   `scripts/stage2_availability.py` (Go probe), add the identical setting.
   Preserve all flags, environment isolation and `retry.enabled = false`.
3. In `tests/test_pi_contract.py`, align `run_pi`'s scratch settings with
   production. Add `test_real_context_overflow_fails_without_compaction`
   through `stage2.run_reviewer`, the existing guarded transport and loopback
   `StandIn`: script a 400 context-length error that Pi recognises, followed
   by a valid answer to expose any recovery attempt. Assert Pi 1.5.0 via the
   existing installed-runtime prerequisite, exactly one provider request,
   nonzero text-mode exit, the overflow diagnostic and `CallFailed`.
   The transport may repoint the endpoint but must not inject compaction
   settings; the test must read production's file. Temporarily remove only
   the production compaction setting to prove this contract goes red, then
   restore it. Keep synthetic keys, offline guards and mandatory prerequisites.
4. Run verification below, replace the ledger's `not yet written` markers
   when tests exist, and update only this change's `spec.md`/`plan.md`
   implementation status to match evidence. The runner records evidence in
   `plans/changes/pi-no-compaction/findings.md` and measured time below.
   At the one-hour stop, or if Pi 1.5.0 fails the promised contract, return
   evidence to the orchestrator without weakening the criterion or moving the pin.

No deletions or new production modules. Leave `research.md` and `decisions.md`,
interactive sessions, user/project settings, limits/splitting, admissions,
failure classification, the Pi install, other changes and doctrine untouched.
No held path requires an orchestrator bootstrap edit. The runner alone
regenerates `plans/INDEX.md` and commits; do not edit the index by hand.

## Verification

From the worktree root, using its prepared virtual environment and Pi install:

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py tests/test_stage2_availability.py tests/test_stage2_swarm.py tests/test_pi_contract.py -q
.venv/bin/python3 scripts/check_interview_minimums.py --change pi-no-compaction
.venv/bin/python3 scripts/check_research_handoff.py --change pi-no-compaction
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_the_review_loop_launches_pi_isolated — reviewer settings omit or enable compaction, or enable retry
- 1: tests/test_stage2.py::test_free_discovery_forces_live_refresh_before_listing — refresh or listing settings differ from the required JSON
- 1: tests/test_stage2_availability.py::test_preparation_calls_only_static_toolless_probes — a probe uses retry-only settings
- 1: tests/test_stage2_swarm.py::test_research_pi_settings_disable_compaction — a repository or public research launch omits disabled compaction
- 2: tests/test_pi_contract.py::test_real_context_overflow_fails_without_compaction — real Pi summarises/retries or the runner accepts the overflow

## Runner route — 2026-11-06

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Repair verification — 2026-11-07

Repair baseline: `ba80de2ccbb90a9baa39ffecd9626f93cecd2fdd`, installed Pi 1.5.0.
Plan step 3 was repeated with only `compaction` removed from the production
`PI_AGENT_SETTINGS` constant; the transport and stand-in were unchanged.
Command: `.venv/bin/python3 -m pytest -q tests/test_pi_contract.py::test_real_context_overflow_fails_without_compaction`.
The planted run exited 1 (`1 failed in 3.19s`), with this expectation failure:

```text
AssertionError: Regex pattern did not match.
 Regex: 'maximum context length'
 Input: "malformed finding output: the answer is empty; expected six-cell findings or exactly 'No finding.'"
```

The production constant was restored in a `finally` block. The clean verification run after restoration passed all ten selected cases
(`10 passed in 11.77s`), including this overflow contract, the length-finish
contract, all five criterion-ledger tests, the shared-writer test and the
three research-launch cases that failed the previous repair. Ruff check and
format check passed for all seven changed Python files. Full `make verify`
is left to the runner, which owns the checkpoint commit. This proves that
the production setting determines the overflow refusal, rather than the
stand-in alone.

## Time used

2026-11-06 05:25:52–05:49:07 UTC, 1395 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-06 05:49:20–06:21:41 UTC, 1941 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-06 06:21:54–07:30:46 UTC, 4131 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-07 04:32:00–05:21:17 UTC, 2957 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-07 05:21:27–05:45:52 UTC, 1464 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
