---
title: "Plan — ci-no-push-run"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-dmmy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, ci, merge-queue]
---

# Plan — ci-no-push-run

```text
For you:     The full hosted check no longer repeats after a queued merge; the merge candidate still gets checked.
Done when:   Tests prove the retained event coverage and first-parent interview check, the generated workflow matches, and make verify is green.
Appetite:    2 hours for phase 4, including repairs; stop at the limit.
Not now:     Changing the live ruleset, queue configuration, gate set, or adding a post-merge run.
Pre-mortem:  suppose it failed: most likely because a merge-group candidate is compared with the wrong parent.
Starts unless you say stop.
```

## Steps

1. Implementer: `scripts/ci_gates.py` removes the push trigger and unused
   `MAIN_BRANCH`, and removes push from the gate and summary event conditions;
   preserve the pull-request and merge-group jobs, checkout, summary semantics,
   drift events and pull-request cancellation grouping.
2. Implementer: `scripts/check_interview_minimums.py` recognises
   `GITHUB_EVENT_NAME == merge_group` for the first-parent hosted base instead
   of using `GITHUB_REF`; retain local main and all other base/error paths.
3. Implementer: `tests/test_ci.py` updates the existing event, trigger,
   summary, drift, path-filter and concurrency checks for the new event set;
   check both generated and committed definitions, and preserve merge-group
   candidate and failure mutants. `tests/test_check_interview_minimums.py`
   tests a detached merge-group candidate whose first-parent diff differs
   from its merge-base diff, plus ordinary branch, main and detached contexts;
   clear inherited GitHub event variables in fixtures.
4. Implementer: `docs/WORKFLOW.md` §3 describes the retained CI events and
   merge-group first-parent base, and states the accepted queue-off risk;
   the existing ruleset gate accepts strict freshness as an alternative and
   cannot be claimed to always detect a disabled queue.
5. Orchestrator, after the accepted implementation attempt: update only the
   header comment in held `decisions/gates.yaml` to name pull-request and
   merge-group verification and schedule/dispatch drift. Regenerate held
   `.github/workflows/ci.yml` from the generator, never by hand:

   ```bash
   .venv/bin/python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml
   ```

6. Runner or orchestrator: regenerate `plans/INDEX.md` through
   `.venv/bin/python3 scripts/plans_registry.py --index` if artifact headers
   changed; keep `plans/changes/ci-no-push-run/spec.md` and this plan aligned
   with the finished implementation. The orchestrator makes a decision pull
   request because `decisions/gates.yaml` is human-decided; the maintainer
   alone merges it.

## Not touched

The live ruleset, `tests/test_repo_settings.py`, gate definitions, queue
configuration, merge instructions, kit manifest, interpreter versions and
manual-dispatch scope stay as they are. No design or ADR is due for this
bounded change.

## Verification

After the held-path edits, run:

```bash
make verify
```

## Criterion ledger

- 1: not yet written tests/test_ci.py::test_push_does_not_start_the_workflow — a push trigger remains in generated or committed YAML
- 2: tests/test_ci.py::test_merge_groups_run_the_gates_on_their_candidate — a merge-group trigger, gate job or candidate checkout is lost
- 2: not yet written tests/test_ci.py::test_pull_requests_run_the_gates_on_their_candidate — the pull-request trigger, gate job or candidate checkout is lost
- 3: tests/test_ci.py::test_merge_groups_require_a_successful_summary — a merge-group summary is absent or accepts a non-success result
- 3: tests/test_ci.py::test_the_summary_check_passes_only_when_every_leg_passed — a pull-request summary is absent or accepts a non-success result
- 4: tests/test_ci.py::test_the_schedule_runs_only_the_drift_job — a scheduled or manual run starts full verification or misses drift
- 5: tests/test_ci.py::test_only_pull_request_runs_cancel_superseded_runs — cancellation or the shared pull-request group is lost
- 6: not yet written tests/test_check_interview_minimums.py::test_merge_group_uses_first_parent — a detached candidate uses the merge base instead
- 7: tests/test_check_interview_minimums.py::test_main_checkout_uses_first_parent — local main uses another base
- 7: tests/test_check_interview_minimums.py::test_worktree_branch_uses_merge_base — a named branch uses another base
- 7: tests/test_check_interview_minimums.py::test_detached_at_tip_without_main_line_env_is_not_measured — detached main silently passes
- 7: not yet written tests/test_check_interview_minimums.py::test_main_ref_alone_does_not_select_first_parent — a detached checkout is treated as main-line solely because of GITHUB_REF
- 8: not a test — phase-6 review compares both current descriptions with the event set and first-parent rule

## Time used

2026-11-21 16:31:06–16:33:36 UTC, 150 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
