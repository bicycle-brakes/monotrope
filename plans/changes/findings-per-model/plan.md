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

Bounded change: no design or ADR. Resolve `REV` once to a full commit, default `HEAD`, and read only committed active and archived findings; never mix lane commits. Read released loop sections and headings starting `## Phase 6`, including historical seven-cell tables; exclude rejected-answer sections and phase 2a. Resolve each change and ID to its latest eligible row. Use the loop Reviewer model and, for phase 6, the nearest preceding review call without an intervening phase-6 block; otherwise retain the row in unattributed. Provide a source interface and legacy implementation so a future event source can replace attribution without changing consumers. The shared reader owns status interpretation consistent with the vocabulary in `templates/findings.md` and duplicate resolution; distinguish missing identity from unreadable evidence.

Recognize legacy duplicate markers in Status, case-insensitively, only when followed by a row ID; retain ordinary rejected rows without IDs. Credit every named original, not the duplicate; report missing targets and cycles as gaps. Compare new or changed rows against the base revision for the canonical `duplicate of <ID>` rule, leaving historical rows untouched. Open contributes to raised but no outcome; leading `taken` and `fixed` mean defects accepted, `resolved`, `answered` and `in spec` mean questions settled, and `rejected` means rejected. Unknown statuses, malformed rows and encoding failures are gaps.

Emit a plain table to standard error and JSON Lines to standard output in the same invocation. JSONL starts with `{"type":"metadata","commit":"<full hash>","complete":true}`, then one `model` record per model with `model`, `raised`, `defects_accepted`, `questions_settled`, `rejected` fields; use `model: null` for unattributed and include `finding` records with `change` and `id` for its rows. Emit `gap` records with `path`, `id` when known, and `reason`; metadata has `complete: false` for gaps. Both formats name the full commit and gaps, and gaps cause non-zero exit. Order records deterministically.

## Files and steps

1. Create `scripts/findings_reader.py` for shared row parsing, status vocabulary, legacy attribution source interface and duplicate handling.
2. Create `scripts/findings_per_model.py` for commit discovery, report aggregation, JSONL and table output; create `tests/test_findings_per_model.py` for reader, command and format tests below.
3. Create `scripts/check_finding_duplicates.py` and `tests/test_finding_duplicates.py` for the new-row duplicate gate and its historical baseline.
4. Change `Makefile` to expose `findings-per-model` with `REV`, and change `docs/orchestration.md` to require one table and cutoff for main and each relevant unmerged lane.
5. After the accepted attempt, the orchestrator edits held paths `templates/findings.md` to define the canonical duplicate form, `decisions/gates.yaml` to register the gate, and `AGENTS.md` to require the same morning tables; the attempt does not edit those paths. The orchestrator runs the targeted duplicate-gate checks after those edits.
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
- 17: not a test — phase-6 review checks both named instruction files require the separate main and lane tables and cutoff commits.

## Time used

2026-11-17 22:26:39–22:28:47 UTC, 128 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-18 12:49:14–12:51:46 UTC, 152 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
