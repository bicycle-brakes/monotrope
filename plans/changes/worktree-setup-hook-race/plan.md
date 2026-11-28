---
title: "Plan — worktree-setup-hook-race"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-1ba3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, worktree, tests]
---

# Plan — worktree-setup-hook-race

```text
For you:     Worktree setup gets its budget after the trust check, and its timeout tests check the intended outcomes.
Done when:   Controlled-clock and timeout regressions pass, as does make verify.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Sub-second clocks, trust-policy changes, or a timeout redesign.
Pre-mortem:  suppose it failed: most likely because the tests still depend on an uncontrolled clock boundary.
Starts unless you say stop.
```

## Build sequence

The orchestrator owns steps 1–4 together as a bootstrap edit after the accepted attempt: the held hook and the tests must change together for the regression to pass.

1. In `tests/test_worktree_setup_hook.py`, add a controlled-clock regression for a trusted automatic setup: wrap `git` so a successful `merge-base` marks the end of the trust check, and stub `date` to advance beyond a two-second budget at that marker; assert `make venv` starts. Keep the real Git command for all other operations and isolate the stubs to this invocation.
2. In the same file, make `test_a_step_never_started_names_the_step_that_used_the_budget` use a two-second budget and an invocation-local `date` stub returning a fixed start second until the make stub records its run, then a second at or beyond the deadline. Let make finish successfully; require one failure naming the next step, `not started`, and `used up by make venv`, and assert later steps did not run. Do not accept a timeout as an alternative.
3. In the same file, make `test_setup_timeout_stops_and_reports_step_and_limit` use a two-second budget and a sufficiently longer sleeping make stub; require that make actually started, the failure says `make venv timed out` and `2s`, subsequent steps did not run, and the overdue process did not wake. Preserve its exit, log and summary checks.
4. The orchestrator edits the held path `.beads/hooks/post-checkout`: move the deadline calculation to immediately after the successful trust check or deliberate-run bypass, immediately before the first setup step. Keep whole-second arithmetic and the managed Beads block unchanged; run the targeted tests again after this bootstrap edit.
5. Update the criterion ledger in `plans/changes/worktree-setup-hook-race/plan.md` when the new test exists. The runner records its evidence in `plans/changes/worktree-setup-hook-race/findings.md`; the orchestrator regenerates `plans/INDEX.md` if required. No file is deleted. Do not change trust rules, the Beads-managed block, or introduce sub-second clock dependencies. This bounded change has no design or ADR.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_worktree_setup_hook.py
python3 scripts/jobs.py start -- make verify
```

Check the detached verification job's exit with `python3 scripts/jobs.py list` before phase 6.

## Criterion ledger

- 1: tests/test_worktree_setup_hook.py::test_trust_check_does_not_consume_setup_budget — moving the deadline back before a controlled slow trust check prevents make from starting.
- 2: tests/test_worktree_setup_hook.py::test_a_step_never_started_names_the_step_that_used_the_budget — accepting a timeout or omitting the next step or preceding step name fails the strengthened test.
- 3: tests/test_worktree_setup_hook.py::test_setup_timeout_stops_and_reports_step_and_limit — a not-started report or wrong limit fails the strengthened test.
- 4: tests/test_worktree_setup_hook.py::test_a_step_never_started_names_the_step_that_used_the_budget — a later setup step running after the controlled deadline fails.
- 4: tests/test_worktree_setup_hook.py::test_setup_timeout_stops_and_reports_step_and_limit — a later setup step running after timeout fails.
- 5: tests/test_worktree_setup_hook.py::test_managed_beads_block_matches_origin_main — a changed managed block fails comparison.

## Explore route

On 2026-11-27, Explore used the Stage-1 route with `claude-haiku-5-5` because GLM through Z.ai had reached its weekly limit until 2026-11-29, as recorded in `research.md`.

## Runner route — 2026-11-27

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Runner route — 2026-11-27

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Runner route — 2026-11-27

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Time used

2026-11-27 07:10:08–07:12:42 UTC, 154 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-27 09:10:27–09:11:05 UTC, 38 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-27 10:40:46–10:42:53 UTC, 127 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-27 11:14:46–11:15:20 UTC, 34 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
