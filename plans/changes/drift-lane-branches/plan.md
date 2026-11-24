---
title: "Plan — drift-lane-branches"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-24
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

1. In `scripts/plans_registry.py`, add opt-in `--branches` to the reverse in-progress-bead coupling only; enumerate origin remote-tracking refs once, exclude symbolic `origin/HEAD`, and inspect eligible `plans/changes/**/*.md` blobs without checkout, applying `parse_frontmatter` and the existing filename exclusions, including archive files; search only if running beads remain unresolved after the tree check. Keep the existing tree-only path unchanged without the flag, and retain the existing missing-artefact DRIFT message and ramp. A failed enumeration or blob read, missing Git, or non-repository root produces BLOCK with the unresolved count, credits completed matches, withholds missing DRIFT lines and omits the complete-search summary; no refs keeps the existing summary and adds INFO. Count malformed frontmatter once per branch and path in INFO. Count distinct branch-only beads, choose each bead's first sorted matching branch, sort those selections, and show the first three or fewer, retaining duplicate names; the summary also gives the checked and still-missing counts.
2. Read all eligible branch blobs with bounded Git subprocesses and no checkout; do not filter on literal bead lines, since YAML aliases, merge keys and escaped values can encode an identity without one. Use a batched Git object reader and reuse parsing by blob identity where possible; count each branch and path separately even for reused blobs. A safe optimization must preserve every eligible match and the specified malformed-file count. Preserve the existing tracker-unavailable and no-running-beads reports.
3. Add `tests/test_plans_registry_branches.py` with temporary Git repositories and tracker fixtures for the criterion ledger, including duplicates, branch ordering, malformed frontmatter, quoted and aliased YAML values, archive and excluded files, injected Git failures, and an unchanged checkout and worktree. Add tests in `tests/test_gate_machinery.py` using a temporary gate declaration and generated workflow plus an executable shell fixture to check the fetch, strict flag, order and failed-fetch short circuit on both the generated and local command paths. The attempt must not edit held files.
4. After the accepted attempt, the orchestrator edits held `decisions/gates.yaml`: set the existing `plans-registry-strict` command to `git fetch --prune origin '+refs/heads/*:refs/remotes/origin/*' && python3 scripts/plans_registry.py --check --strict --branches`. This one declared command supplies both the local drift gate and the generated hosted step; no gate schema or `scripts/ci_gates.py` change is needed. The orchestrator regenerates held `.github/workflows/ci.yml` with `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`, then runs the targeted tests and full verification. The runner updates `plans/changes/drift-lane-branches/plan.md` ledger markers and time evidence and `plans/changes/drift-lane-branches/findings.md` call evidence, and regenerates `plans/INDEX.md` through its existing entry point.

No files are deleted. Leave the tracker, branch contents, other coupling checks and branch synchronisation untouched. This bounded change has no design or ADR. Phase-2a findings and their dispositions are recorded in `findings.md`; S-9’s literal-line narrowing is rejected because it contradicts the existing YAML identity criterion.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_plans_registry_branches.py tests/test_gate_machinery.py
make verify
```

After merge, the tracker writer handles stale claims, records the first scheduled run and its commit on the bead, and opens follow-up work if real drift remains; a green scheduled job requires all other drift findings to be absent too.

## Criterion ledger

- 1: tests/test_plans_registry_branches.py::test_branch_only_artefact_satisfies_running_bead — a branch-only bead is reported missing.
- 2: tests/test_plans_registry_branches.py::test_missing_artefact_remains_drift — a missing bead is suppressed or its existing message changes.
- 3: tests/test_plans_registry_branches.py::test_branch_summary_counts_distinct_branch_only_beads — duplicate or tree matches inflate the count or the missing count is wrong.
- 4: tests/test_plans_registry_branches.py::test_no_remote_refs_preserves_tree_only_check — missing drift is suppressed or the INFO explanation is absent.
- 5: tests/test_gate_machinery.py::test_strict_drift_gate_fetches_all_branches_before_registry — local or generated command lacks pruning, the refspec, branch flag or correct order.
- 6: tests/test_plans_registry_branches.py::test_git_read_failure_blocks_incomplete_search — missing Git, non-repository root or failed enumeration or blob reading does not BLOCK, a completed match is lost, an unresolved bead is reported missing, or a complete summary appears.
- 7: tests/test_gate_machinery.py::test_failed_branch_fetch_prevents_strict_registry — the local or generated command invokes the check or succeeds after a failed fetch.
- 8: tests/test_plans_registry_branches.py::test_branch_scan_preserves_checkout_and_worktree — the check switches the branch or changes files.
- 9: tests/test_plans_registry_branches.py::test_default_check_never_searches_branches — ordinary checks change their verdict or invoke Git for branches.
- 10: tests/test_plans_registry_branches.py::test_malformed_branch_frontmatter_is_counted_as_info — malformed metadata satisfies a bead, is not counted per branch and path, or BLOCKs.
- 11: tests/test_plans_registry_branches.py::test_branch_sample_is_sorted_and_bounded — the sample differs from the first three sorted per-bead selections, drops repeated names, or selects a later branch for a bead.
- 12: tests/test_plans_registry_branches.py::test_branch_scan_excludes_head_and_includes_main — HEAD is counted or main is ignored.
- 13: tests/test_plans_registry_branches.py::test_branch_artefacts_use_tree_frontmatter_semantics — a YAML alias, merge key, escaped or quoted value is missed, body-only text matches, an excluded file matches, or an archive file is ignored.
- 14: tests/test_plans_registry_branches.py::test_search_skipped_when_nothing_unresolved — a tracker-unavailable, no-running-beads, or fully resolved run reads refs or emits branch messages.

## Runner route — 2026-11-23

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM Flash: Z.ai 5-hour limit until 22:33 CET (bead coding-harness-363r.4); Sonnet answers on the default profile again.

## Runner route — 2026-11-24

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-21 15:23:58–15:26:10 UTC, 132 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:30:13–15:32:57 UTC, 165 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:37:05–15:39:43 UTC, 157 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-23 20:49:17–20:53:21 UTC, 243 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-23 21:41:01–21:50:56 UTC, 595 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_plans_registry_branches.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-24 00:51:14–00:52:38 UTC, 84 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-24 00:53:04–01:16:56 UTC, 1433 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-24 01:17:14–01:42:33 UTC, 1519 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-24 08:28:59–08:36:59 UTC, 481 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_archive_closed_changes.py`, `tests/test_bead_render.py`, `tests/test_gate_machinery.py`, `tests/test_plans_registry_branches.py`, `tests/test_pr_sync.py`, `tests/test_stage2_swarm.py`, `tests/test_templates.py`, `tests/test_workflow_entry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
