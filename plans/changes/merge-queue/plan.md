---
title: "Plan — merge-queue"
status: draft
implementation_status: none
date: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-eh42
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, merge-queue, github-actions, decision-pr]
---

# Plan — merge-queue

```text
For you:     after the decision merge and activation, GitHub queues merges against current main without repeated branch updates; your merge authority stays.
Done when:   make verify is green, the live singleton merge-commit queue is read back after approval, and verify passes on a real merge-group candidate.
Appetite:    2 hours of phase 4 including repairs; a stop, not an estimate.
Not now:     a local queue, sync-helper changes, new merge permissions, unattended decision merges or tracker closure machinery.
Pre-mortem:  suppose it failed: most likely because the required verify summary silently skips the merge-group event.
Starts unless you say stop.
```

Implements `spec.md`, criteria 1–9; class bounded, no design or ADR due.
Explore used Stage 2, GLM 5.3 Flash, on 2026-10-30; no Stage-1 fallback.

## Steps

1. **Implementation attempt — `tests/test_repo_settings.py`:** extend the
   freshness predicate to accept active `merge_queue` rules as well as strict
   required-check rules; include queue suppliers in `_suppliers` so `measure`
   reads their details and checks bypasses even in a separate ruleset.
   Keep rule identity validation, unreadable-answer failures and every other
   floor requirement; report both freshness remedies when neither holds.
   Retain the existing `UP_TO_DATE` constants/tests used by older ledgers;
   their no-queue fixtures must still fail. Add the ledger's new fixtures
   through `measure` as well as `ruleset_findings`, including failed detail
   reads, hidden bypass lists, and a queue in a separate ruleset.
2. **Done by the orchestrator before the second implement run (2026-10-30):** the
   `merge_group` trigger (`checks_requested`) in `generate_ci`, its admission in the
   matrix and summary conditions, the regenerated held file `.github/workflows/ci.yml`
   and the event expectation of `test_the_schedule_runs_only_the_drift_job`. Reason: the
   first implement run's three attempts failed because an attempt that regenerates the
   held `ci.yml` is refused, and one that does not leaves the ci-drift gate red. The
   attempt must not touch `.github/workflows/ci.yml`; the rest of this step stays its own.
   **Implementation attempt — `scripts/ci_gates.py`:** add `merge_group`
   (checks requested) to `generate_ci` and admit it in both the gate matrix
   and `_summary_job`; keep `always()`, the exact-success summary and default
   checkout. Preserve PR/push triggers, schedule/dispatch separation and
   PR-only cancellation. **`tests/test_ci.py`:** add the ledger tests against
   generated and checked-in YAML; exercise missing trigger, excluded job,
   wrong checkout ref and skipped summary faults. Update the exact event
   expectations in `test_the_schedule_runs_only_the_drift_job` and the
   freshness explanation in `_merge_ref_findings`; retain their test names.
3. **Orchestrator, after the accepted attempt — held files:**
   `prompts/07-commit.md` makes the existing exact-head merge command queue
   admission when the queue is active, reports pending versus merged, and
   retains branch-update recovery only for the strict-only alternative.
   `templates/repo-settings.md` describes both alternatives, queue CI
   prerequisites, singleton merge commits and safe activation/readback.
   `docs/governance/regelwerk.md` changes only RB-G7's second and third
   rule sentences to cover PR/group merge refs and queue-or-strict freshness;
   keep its id, level and enforcers. Apply §4's version/history duty: version
   6.0.0 at this base, with the four required impact lines, in English;
   record other-instance adoption as follow-up, without editing instances.
   `docs/governance/quality-gates.md` synchronises only the current MG-2
   explanation with those alternatives; its gate table stays as it is.
4. **Orchestrator — `docs/WORKFLOW.md`:** add the queue admission procedure
   under “Pull requests stay mergeable”, preserving maintainer request,
   restatement, head matching and no admin bypass; queue admission is not a
   completed merge. Refresh modified document dates. **Held generated file
   `.github/workflows/ci.yml`:** regenerate with
   `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`.
5. **Orchestrator — change records:** update `plans/changes/merge-queue/plan.md`
   ledger entries when new tests exist, record implementation time there,
   and retain evidence in `plans/changes/merge-queue/findings.md`.
   **`plans/INDEX.md`:** regenerate with
   `python3 scripts/plans_registry.py --index`. Verify the combined tree;
   intermediate attempt tests may depend on the subsequent held-file edits.
6. **Orchestrator — decision pull request and live activation:** use title
   `decide(merge-queue): test queued merges against current main`, label
   `decision`, and `.github/PULL_REQUEST_TEMPLATE/decision.md` as the body
   form; name bead coding-harness-eh42 — the merge-queue switch. Do not
   change hosting settings before the maintainer merges it. Afterwards read
   `gh api repos/{owner}/{repo}/rulesets` and the current main ruleset detail;
   prepare a reviewed full update preserving conditions, empty bypass list,
   pinned `verify`, PR/force-push/deletion rules and unrelated parameters.
   Apply through `gh api` with the host's merge-queue fields: merge method
   MERGE, minimum/maximum entries to merge 1, maximum entries to build 1;
   remove the strict branch-update requirement only with the queue active.
   Read back the active branch rules and queue settings, run the live command
   below, and record a real group's ref/SHA, event, check result and merged
   outcome in `plans/changes/merge-queue/findings.md`. A behind PR's unchanged
   head should enter the queue without `update-branch`; use only an already
   authorised PR. If no such PR exists, leave operational validation pending.

## Not touched

No source files are deleted. No edits to `scripts/pr_sync.py`,
`tests/test_pr_sync.py`, `scripts/merge_guard.py`, `.claude/settings.json`,
`templates/agents-mergeable-prs.md`, `scripts/kit/manifest.yaml`,
`decisions/gates.yaml`, `AGENTS.md`, existing ADRs, endpoint settings or
tracker data; no sibling-repository writes or CI-economy changes.

## Verification

```bash
python3 -m pytest tests/test_repo_settings.py tests/test_ci.py -q
python3 scripts/ci_gates.py --check-ci
make verify
```

After the maintainer's decision merge and activation, on the writer machine:

```bash
RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs
```

## Criterion ledger

- 1: tests/test_repo_settings.py::test_todays_ruleset_holds — the legacy strict configuration is rejected
- 1: tests/test_repo_settings.py::test_merge_queue_supplies_freshness — a valid queue with strict false is rejected
- 2: tests/test_repo_settings.py::test_the_ruleset_check_goes_red_when_branches_need_not_be_up_to_date — neither alternative holds but measurement passes
- 3: tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass — a separate queue supplier has bypasses or unreadable details and measurement passes
- 4: tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements — a queue masks a removed rule, unpinned check or failed measurement
- 5: tests/test_ci.py::test_merge_groups_run_the_gates_on_their_candidate — trigger, event condition or candidate checkout is broken
- 6: tests/test_ci.py::test_merge_groups_require_a_successful_summary — the summary excludes merge_group or accepts a non-success gate result
- 6: tests/test_ci.py::test_the_summary_check_passes_only_when_every_leg_passed — a failed, skipped or cancelled gate result reports success
- 7: not a test — phase-6 review compares the five current procedure/governance texts with criterion 7; mandatory queue branch updates, missing head protection or expanded merge authority refute it
- 8: not a test — orchestrator records activation time after the maintainer's merge timestamp; an earlier settings mutation refutes it
- 9: not a test — post-merge API readback and a hosted merge_group run identify singleton groups, merge method and successful verify on the candidate SHA; wrong settings or no such run refute it

## Runner route — 2026-10-30

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-30 17:59:50–18:20:22 UTC, 1232 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-30 18:20:27–18:31:00 UTC, 632 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-30 18:31:09–18:45:05 UTC, 836 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
