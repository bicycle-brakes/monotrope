---
title: "Plan — findings-per-model"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-18
updated: 2026-11-18
supersedes: null
superseded_by: null
bead: coding-harness-qut1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, measurement]
---

# Plan — findings-per-model

```text
For you:     See findings raised, defects accepted, questions settled and rejected per model in the morning handover.
Done when:   Both report formats agree at each named commit, gaps are visible, and make verify is green.
Appetite:    6 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Changing review execution, model selection, the ladder or the stop rule.
Pre-mortem:  suppose it failed: most likely because historical records cannot be attributed or read reliably.
Starts unless you say stop.
```

Bounded change: no design or ADR. Resolve `REV` once to a full commit, default `HEAD`, and read only committed active and archived findings; never mix lane commits. Read released loop sections and phase-6-like headings, including historical seven-cell tables; only `## Phase 6 — <who>, <date>` is runner-form and eligible for legacy attribution. Other phase-6-like sections are unattributed, heading-less tables are reported outside the count, and rejected-answer sections and `2a-` IDs are excluded. Resolve each change and ID to its latest eligible row. Use the loop Reviewer model and, for phase 6, the nearest preceding Stage-2 call if its verb is exactly `review` and no phase-6 block intervenes; otherwise retain the row in unattributed. The source receives the change, findings file, heading, position and directly preceding call lines, and returns a model ID or unattributed; test a replacement that uses the heading alone. The shared reader owns status interpretation consistent with the vocabulary in `templates/findings.md` and duplicate resolution; distinguish missing identity from unreadable evidence.

Recognize legacy duplicate markers in Status, case-insensitively, only when followed by a row ID; retain ordinary rejected rows without IDs. Follow chains to all non-duplicate roots and credit each root, not duplicates; report missing targets and cycles as gaps. Compare new or changed rows against the merge base with `origin/main` for the exact canonical `rejected — duplicate of <ID>` Status, leaving historical rows untouched. Open contributes to raised but no outcome; leading `taken` and `fixed` mean defects accepted, `resolved`, `answered` and `in spec` mean questions settled, and `rejected` means rejected. Unknown statuses, malformed rows and encoding failures are gaps.

Emit a plain table to standard output and JSON Lines to a file under the state directory in the same invocation; print the file path last. JSONL starts with `{"type":"metadata","commit":"<full hash>","complete":true}`, then one `model` record per model with `model`, `raised`, `defects_accepted`, `questions_settled`, `rejected` fields; use `model: null` for unattributed and include `finding` records with `change` and `id` for its rows. Emit `gap` records with `path`, `id` when known, and `reason`; metadata has `complete: false` for gaps. Both formats name the full commit and gaps, and gaps cause non-zero exit. Order records deterministically.

## Files and steps

1. Create `scripts/findings_reader.py` for shared row parsing, status vocabulary, legacy attribution source interface and duplicate handling.
2. Create `scripts/findings_per_model.py` for commit discovery, report aggregation, JSONL and table output; create `tests/test_findings_per_model.py` for reader, command and format tests below.
3. Create `scripts/check_finding_duplicates.py` and `tests/test_finding_duplicates.py` for the new-row duplicate gate and its historical baseline.
4. Change `Makefile` to expose `findings-per-model` with `REV`, and change `docs/orchestration.md` to require one table and cutoff for main at handover time and each unmerged change branch that gained rows that night.
5. After the accepted attempt, the orchestrator edits held paths `templates/findings.md` to define the canonical duplicate form, `decisions/gates.yaml` to register the gate, and `AGENTS.md` to require the same morning tables, including earlier branches in a lane; the attempt does not edit those paths. The orchestrator runs the targeted duplicate-gate checks after those edits.
6. Update `plans/changes/findings-per-model/plan.md` with actual phase-4 time; the runner manages findings and the plan index.

Do not edit historical findings, model configuration, review execution, or the ladder. The later event-log source and metrics consumer remain separate work. The existing runner row readers can inform the shared reader, but do not change their review behavior.

Verification: `make verify`

## Criterion ledger

- 1: not yet written tests/test_findings_per_model.py::test_scope_at_single_commit — an eligible row is omitted or a rejected answer is included.
- 2: not yet written tests/test_findings_per_model.py::test_latest_row_per_change_and_id — history counts twice or distinct changes collapse.
- 3: not yet written tests/test_findings_per_model.py::test_loop_model_attribution — a loop row receives another model.
- 4: not yet written tests/test_findings_per_model.py::test_phase6_nearest_call_boundary — an intervening block is crossed.
- 5: not yet written tests/test_findings_per_model.py::test_unattributed_rows_are_visible — an unpaired seven-cell row disappears.
- 6: not yet written tests/test_findings_per_model.py::test_replace_attribution_source — replacing the source requires a consumer change.
- 7: not yet written tests/test_findings_per_model.py::test_legacy_duplicate_markers — a valid legacy marker is missed or an ID-less marker is treated as a duplicate.
- 8: not yet written tests/test_findings_per_model.py::test_duplicate_credits_each_named_original — a duplicate gets credit or an unattributed original loses it.
- 9: not yet written tests/test_finding_duplicates.py::test_new_duplicate_form_gate — a new legacy form passes or canonical form fails.
- 10: not yet written tests/test_findings_per_model.py::test_raised_counts_open_and_rejected_once — an open row is omitted.
- 11: not yet written tests/test_findings_per_model.py::test_defects_accepted_statuses — a fixed row is omitted or rejection included.
- 12: not yet written tests/test_findings_per_model.py::test_questions_settled_statuses — a resolved question is omitted.
- 13: not yet written tests/test_findings_per_model.py::test_rejected_status — an open row gets an outcome.
- 14: not yet written tests/test_findings_per_model.py::test_formats_agree_and_name_commit — counts or cutoff differ.
- 15: not yet written tests/test_findings_per_model.py::test_make_entry_point_and_revision — the revision is ignored or one format is missing.
- 16: not yet written tests/test_findings_per_model.py::test_gaps_produce_both_incomplete_outputs_and_nonzero — unreadable evidence is silently accepted.
- 17: not a test — phase-6 review checks both instructions require main at handover time and every unmerged branch that gained rows that night, including an earlier lane item, with cutoff commits.
- 18: not yet written tests/test_findings_per_model.py::test_headingless_tables_outside_count — a heading-less table is silently omitted or counted.
- 19: not yet written tests/test_findings_per_model.py::test_phase2a_ids_excluded — a 2a row increases a total.

## Time used

2026-11-17 22:26:39–22:28:47 UTC, 128 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 12:49:14–12:51:46 UTC, 152 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 13:32:17–13:34:21 UTC, 124 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
