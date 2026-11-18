---
title: "Plan — loop-record-other-worktree"
status: draft
implementation_status: none
date: 2026-11-18
last_reviewed: 2026-11-18
updated: 2026-11-18
supersedes: null
superseded_by: null
bead: coding-harness-e82i
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, review-loop]
---

# Plan — loop-record-other-worktree

```text
For you:     A command accounts for and archives an old worktree's loop record so the change can start a fresh review.
Done when:   The old record and its audit history are preserved, unsafe cases refuse, and make verify passes.
Appetite:    6 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Automatic adoption, recovery of genuinely lost records, and changes to research state or model selection.
Pre-mortem:  suppose it failed: most likely because an interrupted archive leaves misleading accounting.
Starts unless you say stop.
```

## Files and steps

1. In `tests/test_stage2.py`, exercise the command through the runner with multiple roots and shared isolated state: discovery, exact same-change keys, truthful accounting of multiple rounds and pending calls, retained bytes, fresh state and round numbering. Add invalid keys, traversal and symlinks, wrong change, missing or unreadable records, active current record, bad flags and blank reason; assert no mutation on refusal. Hold each record lock in a separate process and inject failures before and after archive and accounting; retry must preserve evidence and never duplicate a line. Include research siblings and existing ordinary restart/release isolation as controls.
2. In `scripts/stage2.py`, use one shared helper in all no-record refusals, including restart and triage, to enumerate only active same-change keys in the current state directory, without reading their contents. Add repeatable `--supersedes` arguments solely to the existing maintainer restart route: validate a literal same-change foreign key and nonblank reason, refuse a current record, acquire the current and all selected record locks in a deterministic order without bypassing their normal users, and inspect each selected record only under its lock. Require all active other keys and at least one pending audit call; account for all calls pending since the last release or restart, without attributing calls to individual keys. Record each round-number range and archive path and use the highest superseded round in the standard restart marker. Preserve the old record as an archive outside the active key, leaving research siblings intact. Archive each loop record first under `<state>/coding-harness/stage2-superseded/<change>@<digest>@<UTC timestamp>/`, retaining research siblings; a retry recognizes archives lacking their accounting line, including a partially archived set, and completes it without overwrite or duplication; keep the existing restart marker semantics, carry the old highest round into fresh numbering, and refuse release until a new round has run. Sanitize the reason as for restart, and retain ordinary routes and their refusal behavior.
3. In `docs/WORKFLOW.md`, update the loop-record and restart description to explain key discovery, the exact command, archival, truthful accounting and fresh-run behavior; distinguish a genuinely lost record. This path is not held.
4. Run the targeted tests and `make verify`; the runner performs the full verification and commit. Do not change key construction, `scripts/stage2_research_store.py`, `scripts/stage2_availability.py`, research state, ADRs or held paths.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_lost_record_refusal_names_only_same_change_other_keys — misses a foreign key or reports an unrelated key.
- 2: not yet written tests/test_stage2.py::test_supersede_accounts_for_old_rounds_and_calls — writes incorrect or duplicate accounting.
- 3: not yet written tests/test_stage2.py::test_supersede_archives_only_the_old_loop_record — loses or leaves an active old record.
- 4: not yet written tests/test_stage2.py::test_supersede_starts_fresh_after_old_round_numbers — reuses old state or round numbers.
- 5: not yet written tests/test_stage2.py::test_supersede_rejects_invalid_requests_without_changes — accepts an invalid request or mutates state.
- 6: not yet written tests/test_stage2.py::test_supersede_respects_both_record_locks — permits concurrent mutation.
- 7: not yet written tests/test_stage2.py::test_supersede_recovers_from_interrupted_writes — loses evidence or duplicates accounting on retry.
- 8: not yet written tests/test_stage2.py::test_supersede_preserves_research_siblings — moves or changes research state.
- 9: tests/test_stage2.py::test_release_in_one_worktree_leaves_the_other_worktrees_record — release alters another worktree's record.
- 9: tests/test_stage2.py::test_a_restart_needs_a_reason_a_finished_run_and_no_record — changes existing restart refusals.
- 10: not yet written tests/test_stage2.py::test_supersede_release_requires_a_new_round — writes a false no-loop line.
- 11: not yet written tests/test_stage2.py::test_supersede_requires_a_new_verdict — accepts a verdict before the restart.
- 12: not a test — phase-6 review compares `docs/WORKFLOW.md` with the command and the spec.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py -k 'supersede or lost_record or restart or worktree'
make verify
```

## Time used

2026-11-18 12:34:20–12:36:44 UTC, 144 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 12:49:22–12:51:18 UTC, 116 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
