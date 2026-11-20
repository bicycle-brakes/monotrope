---
title: "Plan — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-18
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: [{kind: llm-session, name: claude-code, model: glm-5.3, version: "2026-11-16"}, {kind: llm-session, name: codex, version: "2026-11-20", model: "gpt-6.1-terra"}]
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, provenance]
---

# Plan — runner-stamps-provenance

```text
For you:     The runner records the actual producer, checks headers field-by-field, migrates active changes' legacy producer records once, and keeps them valid via plans-registry.
Done when:   Route, field-level, gate and failure tests pass and make verify is green.
Appetite:    16 hours of phase 4, repair rounds and active-change migration included; raised from 3 h per maintainer decision (2026-11-20, Q-19).
Not now:     Archived-header migration and tree-wide check (coding-harness-2i7x).
Pre-mortem:  suppose it failed: most likely because a route checks different files from those it publishes.
Starts unless you say stop.
```

## Files and steps

1. `scripts/stage2.py`: stamp the actual producer of each measured model-call contribution retained by explore, draft or repair before its checks; preserve pre-run committed producer records, allowing the compact block-mapping conversion specified in criterion 7, discard attempt-written self-descriptions, record approval resets in the attempt findings, fail unmeasured drafts and continue to the next available route, and route every file-writing verb, including future verbs, through one shared post-run check; compare provenance and approval with the committed baseline and reject invented approvals, including on implement; preflight explore and spec-review output and stop on committed-record faults without another route; judge committed headers field-by-field outside active research so untouched legacy fields never block unrelated writes while changed or new faults are always refused (criterion 16); name `stage2` as producer in `findings_header` (L9-3). Include new ADRs without changing their provenance class and exclude restored files.
2. `scripts/stage2_research_run.py` and `scripts/stage2_research_snapshot.py`: retain swarm attribution and its frozen publication binding across resume; preserve earlier record bytes on explore apart from the specified compact conversion, and reset explore publication class and review as specified.
3. `scripts/plans_registry.py` and `scripts/research_census.py`: hold the one shared producer-record contract in `scripts/plans_registry.py` (re-exported by `scripts/research_census.py` and consumed by `scripts/stage2.py`), enforce it in `plans-registry` as a blocking check over active changes under `plans/changes/<name>/` outside `archive/` (criterion 17), and keep the unchanged active-research publication contract in the census.
4. Active change artifacts under `plans/changes/<name>/` (outside `archive/`): migrate the 21 legacy `produced_by` headers once into the shared producer-record form, preserving program, model and ISO publication date and stamping `updated: 2026-11-20`.
5. `tests/test_runner_stamps_provenance.py` (new): cover route identity, attempt attribution and failures, the full decided contract, approval resets, byte preservation, unsafe headers, field-level classification (L9-1, L9-2, L9-4), `findings_header` producer (L9-3), and the active-change `plans-registry` producer gate.
6. `tests/test_explore_provenance.py` and `tests/test_stage2.py`: replace normalization expectations with preservation and refusal cases for earlier records, and update `findings_header` producer assertions to `stage2`.
7. `plans/changes/runner-stamps-provenance/decisions.md`, `spec.md`, `findings.md`, and `plan.md`: record Q-19, phase-4 time and implementation findings below. The runner regenerates `plans/INDEX.md` if required.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_runner_stamps_provenance.py
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_runner_stamps_provenance.py::test_explore_stamps_actual_producer — an incorrect route, model or day is accepted.
- 2: tests/test_runner_stamps_provenance.py::test_draft_stamps_retained_artifacts_before_checks — a retained draft artifact or new ADR has a wrong producer when checked.
- 3: tests/test_runner_stamps_provenance.py::test_repair_stamps_retained_artifacts_before_checks — a repair artifact has a wrong producer when checked.
- 4: tests/test_runner_stamps_provenance.py::test_each_verb_rejects_invalid_touched_header — an invalid producer-bearing touched header passes, or a restored file or file without `produced_by` causes a failure.
- 5: tests/test_runner_stamps_provenance.py::test_stamping_preserves_other_bytes — prose or unrelated header bytes change.
- 6: tests/test_runner_stamps_provenance.py::test_unsafe_header_refuses_attempt — an unsafe header is accepted or its file is omitted from the diagnostic.
- 7: tests/test_runner_stamps_provenance.py::test_preserves_prior_contributions — a committed earlier record is rewritten or a session self-description survives.
- 8: tests/test_runner_stamps_provenance.py::test_body_change_resets_approval — approval survives any change outside the two exempt fields or a failed or accepted attempt omits its approver.
- 9: tests/test_runner_stamps_provenance.py::test_header_only_keeps_approval — changing only producer and updated fields resets approval.
- 10: tests/test_runner_stamps_provenance.py::test_unmeasured_attempt_refused — an unmeasured draft or repair is accepted or the next available route is skipped.
- 11: tests/test_runner_stamps_provenance.py::test_new_files_require_pending_review — a new file approves itself or a new human-decided ADR is refused.
- 12: tests/test_runner_stamps_provenance.py::test_committed_baseline_controls_approval — a session invents an approval or an unchanged compatible committed approval is refused.
- 13: tests/test_runner_stamps_provenance.py::test_explore_resets_class_and_approval — a skeleton stays human-written or an approval survives publication.
- 14: tests/test_runner_stamps_provenance.py::test_active_research_contract_matches_census — a post-run check accepts research that the census rejects for class or review.
- 15: tests/test_runner_stamps_provenance.py::test_prepublication_failure_routing — invalid output is published or a committed-record fault spends another route.
- 16: tests/test_runner_stamps_provenance.py::test_field_level_header_check_ignores_untouched_legacy_and_rejects_new_faults — an untouched legacy field blocks an unrelated update, hides a new fault, or a rewritten faulty field is misclassified as a committed fault.
- 17: tests/test_runner_stamps_provenance.py::test_plans_registry_blocks_legacy_active_producers_only — an active change with a legacy or duplicate producer record passes `plans_registry.check()`, or an archived change is blocked.

## What is not touched

No archived-header migration, tree-wide producer gate outside active changes, skeleton writer, approval automation or held path (`decisions/gates.yaml`, `provenance.yaml`, `prompts/`, `templates/`, `AGENTS.md`) is part of this implementation. A bounded change has no design phase or ADR.

## Route

Explore used Stage 2, Flash route, endpoint `glm-coding-plan`, model `glm-5.3-flash`, on 2026-11-16; no Stage-1 fallback is recorded.

## Runner route — 2026-11-18

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-18

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed and the Sonnet attempt ended after 29 s with 24 tests red; continues from the saved tree.

## Runner route — 2026-11-18

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM via Z.ai refuses glm-5.3-flash (bead coding-harness-b5pu); the previous Sonnet call ended at claude exit 1; continues from the saved tree.

## Runner route — 2026-11-18

Stage-1 route: implement · model claude-sonnet-5-5 · reason: the previous Sonnet pass left 6 of 29 new tests red (ValueError unpacking at scripts/stage2.py:9985 among them); continues from that tree.

## Runner route — 2026-11-18

Stage-1 route: implement · model claude-sonnet-5-5 · reason: one targeted test still red after two Sonnet passes (test_unsafe_header_refuses_attempt); continues from that tree.

## Runner route — 2026-11-19

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Hand finish — 2026-11-19

The maintainer chose an orchestrator hand finish by an Opus subagent (bead notes, answer A of
2026-11-19) after the full `make verify` of 2026-11-19 stood at 334 failed. What the hand finish
found and changed:

- The diagnosis "the implement commit made `run_codex` require a `thread.started` event" did not
  hold: `run_codex` is byte-identical to the merge base, and a missing thread event is a specified
  transport failure there (`test_codex_repair_transport_failures_stop_the_chain[no-thread]`). The
  message came from the fake Codex running out of scripted steps once the new header check had
  refused an earlier attempt. `run_codex` therefore stays unchanged; no thread id is recorded as
  "unknown".
- Test fixtures, not the contract, were out of date: the shared test worlds planted new `spec.md`
  and `plan.md` files without `provenance` and `review`, and committed `research.md` files without
  the dates the census contract reads. They now carry what criteria 11, 14 and 15 require
  (`DRAFTED_HEADER`, `DRAFTED_SPEC` in `tests/test_stage2.py`; `SEED` in
  `tests/test_stage2_swarm.py`).
- Four code faults in this change, each reproduced by an existing test, were repaired in
  `scripts/stage2.py`: the no-work measurement counted the runner's own stamp as model work (the
  `produced_by`, `review` and `updated` fields are now cut out together, an inserted field
  included); `committed_bytes` inferred absence from git's error text, which renders a path with a
  line break differently (now a literal `ls-tree` lookup, as review row L6-1 asks); a failed
  changed-file measurement in implement and repair ended the verb instead of failing the attempt
  (criterion 10); and the repair stamp wrote into the change folder without the recovery preflight,
  so a parent swapped for an outside link was written through (new test
  `test_repair_stamp_refuses_a_replaced_parent_unwritten`).
- Loop row L1-2 (duplicate key inside a record of a list-shaped `produced_by`): the committed side
  was repaired in the saved repair tree (8b49b3d3); the output side, the shared post-run check for
  files outside active research, still let it pass and now refuses it
  (`test_duplicate_key_in_producer_list_is_output_fault`).
- Full `make verify` at f8736e23 (2026-11-19): 1 failed, 6349 passed, 17 skipped. The one red is
  `tests/test_provenance.py::test_journal_is_never_cited_without_a_date` on row F-35 of this
  change's `findings.md` (the glob `docs/journal/handover/*.md`, committed unchanged from the
  phase-2a review in f9f7f070). It is not a hand-finish change; whether the row text or the gate
  changes is left to the orchestrator.
- Loop row L1-2 is marked `fixed — tests/test_runner_stamps_provenance.py::test_duplicate_key_in_producer_list_is_output_fault`,
  Broke a test `no`, in the loop record (backup beside it).

## Runner route — 2026-11-19

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-19

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-20

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-16 16:05:48–16:16:58 UTC, 670 s — draft · attempt 3 · route glm · model glm-5.3 · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 16:30:43–16:33:10 UTC, 147 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 16:39:46–16:40:52 UTC, 66 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 16:51:25–16:54:12 UTC, 167 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 23:49:33–23:50:58 UTC, 86 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-17 22:23:56–22:25:48 UTC, 113 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 12:48:47–12:51:09 UTC, 141 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 13:28:53–13:30:46 UTC, 113 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 13:32:41–15:35:09 UTC, 7347 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-18 15:35:20–15:52:38 UTC, 1038 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-18 15:52:46–15:53:15 UTC, 29 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-18 21:56:19–22:02:36 UTC, 377 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-18 22:03:06–22:03:34 UTC, 29 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-18 22:04:11–22:05:29 UTC, 78 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_runner_stamps_provenance.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-18 22:12:21–22:27:16 UTC, 895 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-18 22:27:25–23:04:11 UTC, 2206 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-18 23:04:19–23:13:51 UTC, 571 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-19 15:31–15:59 and 16:17–16:38 UTC, 49 min — implement · orchestrator hand finishing (Opus subagent, maintainer's answer A of 2026-11-19): fixtures, four stamp faults, loop row L1-2 output side, full `make verify` · measured by hand from the scratch files and test-run timestamps; a session pause lies between the two spans
2026-11-19 17:28:20–17:53:06 UTC, 1487 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-19 17:53:17–17:54:14 UTC, 57 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-19 17:54:25–17:59:42 UTC, 317 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-19 about 18:02–18:56 UTC, about 54 min — repair · orchestrator hand finishing of round 2 (Opus subagent): committed-fault stop narrowed to unreadable headers (criterion 14, loop row L2-12), three fixtures meet the checks L2-4 and L2-10 added, two full `make verify` runs · measured by hand from commit and log times; the start is approximate
2026-11-19 21:59:08–22:00:33 UTC, 85 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-19 22:00:46–22:01:48 UTC, 62 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-19 22:02:00–22:05:04 UTC, 185 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-19 about 22:06–23:07 UTC, about 61 min — repair · orchestrator hand finishing of round 3 (Opus subagent): ruff findings of the Sonnet attempt fixed, one post-run findings check at the verb dispatch and one judged findings writer (loop row L3-5), one shared frontmatter pattern for the check's file selection (L3-6), rows L3-2..L3-7 marked fixed, one full `make verify` (red only on the journal-date test owned by the journal-citation-gate change) · measured by hand from commit and log times; the start is approximate
2026-11-20 06:14:04–06:15:20 UTC, 76 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files none; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-20 06:37:44–07:32:08 UTC, 3264 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 07:32:17–07:33:15 UTC, 58 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 07:33:26–07:34:22 UTC, 56 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-20 about 10:38–11:46 UTC, about 68 min including a budget pause of unmeasured length — repair · orchestrator hand finishing of round 6 (Opus subagent): origin/main merged (journal-date gate repaired there by journal-citation-gate), loop row L6-1's test extended to drive the implement route (red without the route's wiring), L6-3's test named, L6-4's spec [DETAIL] text corrected, rows L6-1, L6-3, L6-4 marked fixed, one full `make verify` green at a72a3928 (6499 passed, 17 skipped) · measured by hand from command and commit times; the start is approximate
2026-11-20 12:55:18–14:39:51 UTC, 6273 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
2026-11-20 16:51:19–17:19:17 UTC, 1678 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-20 19:22–19:48 UTC, 26 min — repair · orchestrator hand finishing of round 9 (maintainer Option 2, Q-19): appetite raised to 16 h in decisions/spec/plan, L9-3 kept (`findings_header` names `stage2`), L9-1/L9-2/L9-4 repaired with field-level header classification in `scripts/stage2.py`, shared producer-record contract hoisted to `scripts/plans_registry.py` with blocking active-change gate, 21 legacy active-change headers migrated once, rows L9-1 and L9-3 marked fixed; targeted ruff, pytest (265 + 8 passed) and fast document/schema gates green (full `make verify` deferred until verify slot clears) · measured by hand from task timestamps
