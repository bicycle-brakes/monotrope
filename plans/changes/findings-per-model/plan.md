---
title: "Plan — findings-per-model"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-qut1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, measurement]
---

# Plan — findings-per-model

```text
For you:     See raised, taken, fixed and rejected review findings per recorded model in the morning handover.
Done when:   Both report formats agree at a named commit, duplicates and unknown reviewers are accounted for, and make verify is green.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Changing review execution, model selection, the ladder or the stop rule.
Pre-mortem:  suppose it failed: most likely because historical records do not identify every reviewer or duplicate reliably.
Starts unless you say stop.
```

Bounded change: no design or ADR; no plan template exists in this tree. The report reads committed evidence, not a mixed working tree. Resolve a requested revision once to a full commit, defaulting to HEAD; enumerate active and archived findings at that commit. Use the existing row grammar and section boundaries in `scripts/stage2.py` and `scripts/stage2_runs.py`; include released loop rows and phase-6 rows, not phase-2a rows. Use the row reviewer where present and the phase-6 section's recorded identity only when it unambiguously identifies a model; expose otherwise unattributed rows separately with their source. Never infer a model id from a vendor or a session id.

Resolve explicit `same as` references within the change before counting: credit the referenced original once and exclude the duplicate from all four totals; reject missing, ambiguous or cyclic references with the file and row. Match statuses by their leading word, treating fixed as taken as well. A missing or unreadable committed input is an error, not a zero. Emit deterministic JSONL and a plain table from the same counts, each carrying the full commit; diagnostics and unattributed rows must remain visible. Do not read live external loop state: released records are the committed evidence.

## Files and steps

1. Create `scripts/findings_per_model.py` for the single report entry point, committed-tree discovery, attribution, duplicate resolution and both output formats.
2. Create `tests/test_findings_per_model.py` with temporary git repositories and representative released and phase-6 tables, including older and malformed records; implement the ledger tests below.
3. Change `Makefile` to expose the report through one target, forwarding an optional revision and emitting both formats.
4. Change `docs/WORKFLOW.md` to require the generated table and commit in future morning handovers and document the make invocation and unattributed evidence.
5. Update `plans/changes/findings-per-model/plan.md` with test names and measured phase-4 time; the runner manages `findings.md` and the plan index.

Do not change review parsing contracts, historical findings, model configuration, or the ladder. No held paths are scheduled for implementation; the existing `Makefile` and `docs/WORKFLOW.md` are not held paths. If a duplicate or reviewer cannot be resolved from the evidence, report that limitation rather than inventing data.

Verification: `make verify`

## Criterion ledger

- 1: not yet written tests/test_findings_per_model.py::test_report_reads_active_and_archived_at_one_commit — a committed finding is omitted or a later edit changes the result.
- 2: not yet written tests/test_findings_per_model.py::test_attribution_for_loop_and_phase6 — a recorded reviewer receives the wrong finding.
- 3: not yet written tests/test_findings_per_model.py::test_unknown_reviewer_is_exposed — missing identity is hidden or guessed.
- 4: not yet written tests/test_findings_per_model.py::test_duplicate_credits_original_only — both models or the later model receive credit.
- 5: not yet written tests/test_findings_per_model.py::test_raised_includes_all_dispositions_once — rejected or undecided rows disappear or are duplicated.
- 6: not yet written tests/test_findings_per_model.py::test_taken_statuses — a fixed or taken row is omitted or an unaccepted row is included.
- 7: not yet written tests/test_findings_per_model.py::test_fixed_status — taken without repair counts as fixed.
- 8: not yet written tests/test_findings_per_model.py::test_rejected_status — a rejected row is omitted or another status is included.
- 9: not yet written tests/test_findings_per_model.py::test_formats_agree_and_name_commit — outputs disagree or omit the full commit.
- 10: not yet written tests/test_findings_per_model.py::test_make_entry_point — the make target does not produce both formats.
- 11: not a test — phase-6 review checks the morning-handover instructions require the generated table and cut-off.
- 12: not yet written tests/test_findings_per_model.py::test_incomplete_evidence_fails — an unreadable input or unresolved duplicate yields a complete-looking report.

## Time used

2026-11-17 22:26:39–22:28:47 UTC, 128 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
