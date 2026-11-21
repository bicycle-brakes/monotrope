---
title: "Plan — drift-lane-branches"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-l54q
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, plans-registry, drift]
---

# Plan — drift-lane-branches

```text
For you:     Running work on pushed branches no longer appears as a missing change folder; truly missing folders remain visible.
Done when:   Branch, missing-folder and failure regressions pass, make verify is green, and a later drift run confirms the live result.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Cleaning up stale claims or synchronising branches with main.
Pre-mortem:  suppose it failed: most likely because an incomplete branch read is mistaken for a complete search.
Starts unless you say stop.
```

## Build sequence and files

1. In `scripts/plans_registry.py`, extend only the reverse in-progress-bead coupling: enumerate `refs/remotes/origin/*` once and inspect each ref's `plans/changes/` Markdown artefacts without a checkout, using the existing frontmatter interpretation for bead identity. Bound Git reads to one per ref or a batched equivalent, distinguish no refs from failed reads, and emit a BLOCK on an incomplete search; retain the existing tree matches, ramp, DRIFT message and other coupling checks. Count distinct branch-only running beads, show a bounded sample of their branch names, and report absent refs as INFO.
2. In `tests/test_plans_registry_branches.py`, create temporary Git repositories and tracker fixtures to test the ledger below, including multiple refs, duplicate matches, exact frontmatter identity rather than body text, and an injected Git failure. Verify the branch and worktree before and after the check. Do not use the real tracker or change the current checkout.
3. In `scripts/ci_gates.py`, generate a drift-job fetch of `+refs/heads/*:refs/remotes/origin/*` before the strict registry check, with failure preventing that check from reporting a complete result even though gate steps currently use `if: !cancelled()`; leave other jobs unchanged. In `tests/test_gate_machinery.py`, test the generated drift job's refspec, ordering and failure dependency.
4. The orchestrator, after the accepted implementation attempt, regenerates held path `.github/workflows/ci.yml` with `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`; the implementation attempt must not edit or commit that path. Run the targeted tests and full verification after regeneration. The runner updates `plans/changes/drift-lane-branches/plan.md` ledger markers and time evidence, `plans/changes/drift-lane-branches/findings.md` call evidence, and regenerates `plans/INDEX.md` through its existing entry point.

No files are deleted. Leave `plans/changes/drift-lane-branches/decisions.md`, the tracker, branch contents, other coupling checks, and branch synchronisation untouched. This bounded change has no design or ADR. No phase-2a rows were open in `findings.md` on 2026-11-21.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_plans_registry_branches.py tests/test_gate_machinery.py
make verify
```

After merge, the tracker writer handles remaining stale claims; record a scheduled drift run's result and commit separately. A green run requires all other drift findings to be absent too.

## Criterion ledger

- 1: not yet written tests/test_plans_registry_branches.py::test_branch_only_artefact_satisfies_running_bead — the branch-only bead is reported missing.
- 2: not yet written tests/test_plans_registry_branches.py::test_missing_artefact_remains_drift — a missing bead is suppressed or its existing message changes.
- 3: not yet written tests/test_plans_registry_branches.py::test_branch_summary_counts_distinct_branch_only_beads — duplicates or tree matches inflate the count or branch examples are missing.
- 4: not yet written tests/test_plans_registry_branches.py::test_no_remote_refs_preserves_tree_only_check — missing drift is suppressed or the INFO explanation is absent.
- 5: not yet written tests/test_gate_machinery.py::test_drift_job_fetches_all_branches_before_registry — the generated fetch or its ordering is wrong.
- 6: not yet written tests/test_plans_registry_branches.py::test_git_read_failure_blocks_incomplete_search — failed enumeration or branch reading does not BLOCK.
- 7: not yet written tests/test_gate_machinery.py::test_failed_branch_fetch_prevents_strict_registry — the generated job allows the strict check after a failed fetch.
- 8: not yet written tests/test_plans_registry_branches.py::test_branch_scan_preserves_checkout_and_worktree — the check switches the branch or changes files.

## Time used

2026-11-21 15:23:58–15:26:10 UTC, 132 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
