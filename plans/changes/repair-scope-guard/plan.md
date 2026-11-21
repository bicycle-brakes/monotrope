---
title: "Plan — repair-scope-guard"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
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

1. In `scripts/stage2.py`, add `docs/journal/` to `RUNNER_HELD` and tell both repair prompt variants the scope and the two prohibitions. Preserve existing case-folded held-prefix and restoration behavior for every writing verb.
2. In the same file, derive repair scope once from the selected taken rows' Where cells and the accepted plan snapshot, before model calls. Recognize repository-relative individual file paths in plain text, Markdown code spans and links, including line or test selectors; normalize safely without treating a named file as its directory or accepting parent traversal. The change folder and `tests/` admit descendants; held paths take precedence. Use the same frozen scope on retries, never attempt-edited inputs.
3. Compare files present at model handback with the pre-attempt baseline, including staged, untracked, ignored and rename destinations, while preserving pre-existing ignored files and distinguishing subsequent runner-created verification artifacts. Refuse and list every out-of-scope new file through the existing failed-attempt evidence and safe rollback before any commit; leave edits to existing tracked files to the existing checks. Do not arm this new-file rule for other verbs. Keep the existing restoration safety preflight, findings preservation and lifecycle handling.
4. Add focused behavior tests in `tests/test_stage2.py`, including actual attempt failure and rollback, all admitted scope sources, prefix lookalikes, both prompt routes, journal writes across writing verbs, and staged, ignored and renamed additions. Test plan and row tampering, baseline ignored leftovers and existing tracked edits. Reuse the existing runner test fixtures and avoid provider calls.
5. Update `docs/WORKFLOW.md` for the held journal and repair-only new-file boundary. After the accepted attempt, the orchestrator updates `prompts/03-plan.md`'s held-path list to include `docs/journal/`, and runs the held-list drift test and full verification; this held path is never assigned to the Stage-2 attempt.

## Files and limits

- `scripts/stage2.py`: runner protection, frozen scope, diagnostics and repair prompts.
- `tests/test_stage2.py`: behavioral and failure-path regressions.
- `docs/WORKFLOW.md`: describe the new runner boundary and its limits.
- `prompts/03-plan.md`: orchestrator-only bootstrap edit to synchronize the held-path list.
- `plans/changes/repair-scope-guard/spec.md`, `plans/changes/repair-scope-guard/plan.md`: update only if implementation evidence requires an authorized correction; the runner records attempt time in the plan.
- `plans/changes/repair-scope-guard/findings.md`: runner-owned evidence and review rows; `plans/INDEX.md`: regenerate only if required by header edits.

No files are deleted. Keep the provenance map, ADRs, existing tracked-file scope, hand repairs and other changes untouched. This bounded change has no design or ADR. The adjacent held-row routing change uses the same held list; whichever change merges second rebases on the other.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_stage2_journal_paths_are_held — a writing attempt commits a journal path or fails to restore it.
- 2: not yet written tests/test_stage2.py::test_repair_prompts_state_scope_restrictions — either tool route omits the scope or a prohibition.
- 3: not yet written tests/test_stage2.py::test_repair_refuses_all_new_paths_outside_scope — an added, untracked, ignored or renamed path escapes the diagnostic.
- 4: not yet written tests/test_stage2.py::test_repair_allows_new_paths_within_scope — a legitimate new file from any scope source is rejected.
- 5: not yet written tests/test_stage2.py::test_repair_scope_guard_allows_existing_tracked_edits — an existing non-held edit is rejected solely for its path.
- 6: not yet written tests/test_stage2.py::test_repair_scope_refusal_restores_attempt_and_keeps_diagnostic — attempt edits remain, prior findings are lost, or the diagnostic is missing.
- 7: not yet written tests/test_stage2.py::test_repair_scope_uses_pre_attempt_plan_and_rows — attempt edits authorize their own new file.

## Time used

2026-11-21 15:17:34–15:20:22 UTC, 168 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
