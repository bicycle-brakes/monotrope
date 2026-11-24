---
title: "Plan — repair-scope-guard"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-t83
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, repair, stage2-runner]
---

# Plan — repair-scope-guard

```text
For you:     Repair attempts cannot keep new files outside their stated scope; journal files stay with the orchestrator.
Done when:   The scope, journal, prompt and restoration regressions and make verify pass.
Appetite:    4 hours of phase 4 including repairs; stop at the limit.
Not now:     Restricting edits to existing tracked files or guarding the orchestrator's hand repairs.
Pre-mortem:  suppose it failed: most likely because an attempt can change the scope used to judge itself.
Starts unless you say stop.
```

## Build sequence

1. The orchestrator already added `docs/journal/` to the runner-held list and synchronized the held plan prompt in one hand commit (`f1fc1836`); retain both edits. Tell both repair prompt variants the scope rule and prohibitions in `scripts/stage2.py`.
2. In `scripts/stage2.py`, freeze scope before model calls from selected taken Where cells, the change folder and `tests/`; never use the plan as authorization. Extract path-like tokens and Markdown link text and target, strip trailing line or line-range selectors, resolve bare names against the change folder first then the root, grant descendants only for slash-ended directories, and reject repository escapes. Reuse the shared Where-path helper if the adjacent held-row routing change has landed; otherwise make the same rule available for it to reuse.
3. At the checkpoint after verification, compare non-ignored untracked and indexed additions with the pre-attempt baseline, including rename destinations and explicitly indexed ignored files. Apply this guard only to repair, with held paths taking precedence; retain normal behavior for existing tracked edits and ignored untracked files. Report all offending paths, save the refused attempt and diagnostic with its local attempt ref, and use the held-path safe rollback and pre-call findings restoration; stop this run without a retry. Keep the existing restoration safety preflight and lifecycle protection.
4. Add behavioral tests in `tests/test_stage2.py` for the complete path grammar, boundaries and lookalikes, both prompt routes, all Stage-2 writing verbs' journal protection, staged and unstaged additions, rename destinations, ignored files, frozen scope, and checkpoint refusal with saved evidence and rollback. Exercise a subsequent fresh run on the restored baseline and keep tests independent of provider calls.
5. Update `docs/WORKFLOW.md` to describe the held journal, repair-only new-file boundary, ignored-file limit and refusal behavior.

## Files and limits

- `scripts/stage2.py`: existing orchestrator journal-held edit; repair prompts, frozen scope, checkpoint refusal and evidence.
- `tests/test_stage2.py`: behavioral and failure-path regressions.
- `docs/WORKFLOW.md`: describe the new runner boundary and its limits.
- `prompts/03-plan.md`: existing orchestrator-only bootstrap edit synchronizing the held-path list; no implement attempt edits this held path.
- `plans/changes/repair-scope-guard/spec.md`, `plans/changes/repair-scope-guard/plan.md`: update only for an authorized correction; the runner records phase-4 time in the plan.
- `plans/changes/repair-scope-guard/findings.md`: runner-owned evidence and review rows; `plans/INDEX.md`: regenerate only if required by header edits.

No files are deleted. Keep the provenance map, ADRs, existing tracked-file scope, hand repairs and other changes untouched. This bounded change has no design or ADR. The adjacent held-row routing change shares the Where-path rule and held list; whichever change merges second rebases and reuses the first helper.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_stage2_journal_paths_are_held — a writing attempt commits or fails to restore a journal path.
- 2: tests/test_stage2.py::test_repair_prompts_state_scope_restrictions — either tool route omits the scope rule or a prohibition.
- 3: tests/test_stage2.py::test_repair_refuses_all_new_paths_outside_scope — an added, untracked or renamed path escapes the refusal or diagnostic.
- 4: tests/test_stage2.py::test_repair_allows_new_paths_within_scope — a non-held new file from a permitted scope source is rejected.
- 5: tests/test_stage2.py::test_repair_scope_guard_allows_existing_tracked_edits — an existing non-held edit is rejected solely for its path.
- 6: tests/test_stage2.py::test_repair_scope_refusal_restores_attempt_and_keeps_diagnostic — work or findings are not restored, a retry starts, or saved evidence and refusal text are missing.
- 7: tests/test_stage2.py::test_repair_scope_uses_pre_attempt_rows — attempt-edited rows or plan authorize a new file.
- 8: tests/test_stage2.py::test_repair_where_paths_resolve_with_shared_rules — a selector, link, bare name, directory, prose or escaping path resolves incorrectly.
- 9: tests/test_stage2.py::test_repair_scope_ignores_untracked_ignored_files — an ignored untracked cache triggers the guard or an indexed ignored addition escapes it.

## Runner route — 2026-11-23

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-23

Stage-1 route: repair · model claude-sonnet-5-5 · reason: Codex usage-limited until 2026-11-23 16:40; maintainer: repairs to Sonnet meanwhile.

## Runner route — 2026-11-23

Stage-1 route: repair · model claude-sonnet-5-5 · reason: Codex usage-limited until 2026-11-23 16:40; maintainer: repairs to Sonnet meanwhile.

## Runner route — 2026-11-23

Stage-1 route: repair · model claude-sonnet-5-5 · reason: Codex usage-limited until 2026-11-23 16:40; maintainer: repairs to Sonnet meanwhile.

## Time used

2026-11-21 15:17:34–15:20:22 UTC, 168 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:25:41–15:28:10 UTC, 149 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-23 09:19:53–10:15:07 UTC, 3313 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-23 10:15:16–10:41:12 UTC, 1557 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-23 10:41:22–11:02:20 UTC, 1258 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-23 11:08:53–11:30:10 UTC, 1277 s — repair · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-23 13:28:02–13:46:55 UTC, 1133 s — repair · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-23 14:17:50–14:20:42 UTC, 172 s — repair · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-23 15:43:02–16:05:42 UTC, 1360 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-23 16:26:18–16:43:48 UTC, 1050 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-23 16:43:58–17:06:44 UTC, 1366 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-23 18:20:09–18:48:59 UTC, 1730 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-24 13:13:09–13:35:30 UTC, 1341 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-24 13:35:48–14:06:18 UTC, 1831 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-24 15:16:45–15:40:03 UTC, 1398 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-24 18:06:03–18:39:40 UTC, 2017 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-24 19:14:33–19:52:30 UTC, 2277 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
