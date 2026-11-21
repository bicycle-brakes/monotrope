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

1. In `scripts/plans_registry.py`, add opt-in `--branches` to the reverse in-progress-bead coupling only; enumerate origin remote-tracking refs once, exclude symbolic `origin/HEAD`, and inspect eligible `plans/changes/**/*.md` blobs without checkout, applying `parse_frontmatter` and the existing filename exclusions, including archive files. Keep the existing tree-only path unchanged without the flag, and retain the existing missing-artefact DRIFT message and ramp. A failed enumeration or blob read, missing Git, or non-repository root produces BLOCK; no refs and malformed branch frontmatter produce separate INFO reports. Count distinct branch-only beads, choose each bead's first sorted matching branch and show up to three sorted example names; the summary also gives the checked and still-missing counts.
2. Read branches with bounded Git subprocesses, using `git grep` only as a safe narrowing aid and `git show` for candidate content; enumerate all eligible blobs where necessary to preserve YAML aliases, merge keys and malformed-frontmatter counts. Do not assume a literal `bead:` line proves or exhausts a YAML identity. Preserve the existing tracker-unavailable and no-running-beads reports.
3. Add `tests/test_plans_registry_branches.py` with temporary Git repositories and tracker fixtures for the criterion ledger, including duplicates, branch ordering, malformed frontmatter, quoted and aliased YAML values, archive and excluded files, injected Git failures, and an unchanged checkout and worktree. Add tests in `tests/test_gate_machinery.py` using a temporary gate declaration and generated workflow plus an executable shell fixture to check the fetch, strict flag, order and failed-fetch short circuit on both the generated and local command paths. The attempt must not edit held files.
4. After the accepted attempt, the orchestrator edits held `decisions/gates.yaml`: set the existing `plans-registry-strict` command to `git fetch --prune origin '+refs/heads/*:refs/remotes/origin/*' && python3 scripts/plans_registry.py --check --strict --branches`. This one declared command supplies both the local drift gate and the generated hosted step; no gate schema or `scripts/ci_gates.py` change is needed. The orchestrator regenerates held `.github/workflows/ci.yml` with `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`, then runs the targeted tests and full verification. The runner updates `plans/changes/drift-lane-branches/plan.md` ledger markers and time evidence and `plans/changes/drift-lane-branches/findings.md` call evidence, and regenerates `plans/INDEX.md` through its existing entry point.

No files are deleted. Leave the tracker, branch contents, other coupling checks and branch synchronisation untouched. This bounded change has no design or ADR. Phase-2a rows S-1–S-8 are incorporated into the spec; their existing triage is retained.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_plans_registry_branches.py tests/test_gate_machinery.py
make verify
```

After merge, the tracker writer handles stale claims, records the first scheduled run and its commit on the bead, and opens follow-up work if real drift remains; a green scheduled job requires all other drift findings to be absent too.

## Criterion ledger

- 1: not yet written tests/test_plans_registry_branches.py::test_branch_only_artefact_satisfies_running_bead — a branch-only bead is reported missing.
- 2: not yet written tests/test_plans_registry_branches.py::test_missing_artefact_remains_drift — a missing bead is suppressed or its existing message changes.
- 3: not yet written tests/test_plans_registry_branches.py::test_branch_summary_counts_distinct_branch_only_beads — duplicate or tree matches inflate the count or the missing count is wrong.
- 4: not yet written tests/test_plans_registry_branches.py::test_no_remote_refs_preserves_tree_only_check — missing drift is suppressed or the INFO explanation is absent.
- 5: not yet written tests/test_gate_machinery.py::test_strict_drift_gate_fetches_all_branches_before_registry — local or generated command lacks pruning, the refspec, branch flag or correct order.
- 6: not yet written tests/test_plans_registry_branches.py::test_git_read_failure_blocks_incomplete_search — missing Git, non-repository root or failed enumeration or blob reading does not BLOCK.
- 7: not yet written tests/test_gate_machinery.py::test_failed_branch_fetch_prevents_strict_registry — the local or generated command invokes the check or succeeds after a failed fetch.
- 8: not yet written tests/test_plans_registry_branches.py::test_branch_scan_preserves_checkout_and_worktree — the check switches the branch or changes files.
- 9: not yet written tests/test_plans_registry_branches.py::test_default_check_never_searches_branches — ordinary checks change their verdict or invoke Git for branches.
- 10: not yet written tests/test_plans_registry_branches.py::test_malformed_branch_frontmatter_is_counted_as_info — malformed metadata satisfies a bead, is not counted, or BLOCKs.
- 11: not yet written tests/test_plans_registry_branches.py::test_branch_sample_is_sorted_and_bounded — the sample exceeds three, is unsorted, or selects a later branch for a bead.
- 12: not yet written tests/test_plans_registry_branches.py::test_branch_scan_excludes_head_and_includes_main — HEAD is counted or main is ignored.
- 13: not yet written tests/test_plans_registry_branches.py::test_branch_artefacts_use_tree_frontmatter_semantics — a YAML alias or quoted value is missed, body-only text matches, an underscore file matches, or an archive file is ignored.

## Time used

2026-11-21 15:23:58–15:26:10 UTC, 132 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:30:13–15:32:57 UTC, 165 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
