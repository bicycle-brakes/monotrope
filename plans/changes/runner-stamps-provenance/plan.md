---
title: "Plan — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3, version: "2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, provenance]
---

# Plan — runner-stamps-provenance

```text
For you:     The runner records the actual producer and checks producer headers in files a run touched.
Done when:   Route and failure tests pass and make verify is green.
Appetite:    3 hours of phase 4, repair rounds included; stop at the limit.
Not now:     Existing-header migration and a tree-wide check.
Pre-mortem:  suppose it failed: most likely because a route checks different files from those it publishes.
Starts unless you say stop.
```

## Prerequisite

Do not implement until the maintainer answers the remaining review ambiguities F-10, F-15, F-16 and F-17 and the spec, findings and plan are reconciled. Q-11 preserves provenance and permits valid retained approvals; Q-12 limits the per-run check to touched files carrying `produced_by`.

## Files and steps

1. `scripts/stage2.py`: stamp the actual producer of each measured model-call contribution retained by explore, draft or repair before its checks; preserve pre-run committed producer records byte-for-byte, discard attempt-written self-descriptions, record approval resets in the attempt findings, fail unmeasured drafts and continue to the next available route, and apply the decided touched-file contract to every verb. Include new ADRs without changing their provenance class and exclude restored files.
2. `scripts/stage2_research_run.py` and `scripts/stage2_research_snapshot.py`: implement the decided swarm attribution while retaining the frozen publication binding across resume.
3. `scripts/research_census.py`: reuse the publication contract for the per-run check, checking all earlier records, while allowing preserved provenance and valid retained approval; check only touched files carrying `produced_by` and do not create a tree-wide gate.
4. `tests/test_runner_stamps_provenance.py` (new): cover route identity, attempt attribution and failures, the full decided contract, approval resets, byte preservation and unsafe headers.
5. `plans/changes/runner-stamps-provenance/spec.md`, `findings.md`, and `plan.md`: incorporate the outstanding answers, resolve the review rows, align this plan and ledger, and record phase-4 time below. The runner regenerates `plans/INDEX.md` if required.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_runner_stamps_provenance.py
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: not yet written tests/test_runner_stamps_provenance.py::test_explore_stamps_actual_producer — an incorrect route, model or day is accepted.
- 2: not yet written tests/test_runner_stamps_provenance.py::test_draft_stamps_retained_artifacts_before_checks — a retained draft artifact or new ADR has a wrong producer when checked.
- 3: not yet written tests/test_runner_stamps_provenance.py::test_repair_stamps_retained_artifacts_before_checks — a repair artifact has a wrong producer when checked.
- 4: not yet written tests/test_runner_stamps_provenance.py::test_each_verb_rejects_invalid_touched_header — an invalid producer-bearing touched header passes, or a restored file or file without `produced_by` causes a failure.
- 5: not yet written tests/test_runner_stamps_provenance.py::test_stamping_preserves_other_bytes — prose or unrelated header bytes change.
- 6: not yet written tests/test_runner_stamps_provenance.py::test_unsafe_header_refuses_attempt — an unsafe header is accepted or its file is omitted from the diagnostic.
- 7: not yet written tests/test_runner_stamps_provenance.py::test_preserves_prior_contributions — a committed earlier record is rewritten or a session self-description survives.
- 8: not yet written tests/test_runner_stamps_provenance.py::test_body_change_resets_approval — approval survives a draft or repair body change or the attempt findings omit its approver.
- 9: not yet written tests/test_runner_stamps_provenance.py::test_header_only_keeps_approval — a header-only stamp resets approval.
- 10: not yet written tests/test_runner_stamps_provenance.py::test_unmeasured_attempt_refused — an unmeasured draft attempt is accepted or the next available route is skipped.

## What is not touched

No migration, tree-wide producer gate, skeleton writer, approval automation or held path is part of this implementation. A bounded change has no design phase or ADR.

## Route

Explore used Stage 2, Flash route, endpoint `glm-coding-plan`, model `glm-5.3-flash`, on 2026-11-16; no Stage-1 fallback is recorded.

## Time used

2026-11-16 16:05:48–16:16:58 UTC, 670 s — draft · attempt 3 · route glm · model glm-5.3 · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 16:30:43–16:33:10 UTC, 147 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 16:39:46–16:40:52 UTC, 66 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 16:51:25–16:54:12 UTC, 167 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 23:49:33–23:50:58 UTC, 86 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-17 22:23:56–22:25:48 UTC, 113 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
