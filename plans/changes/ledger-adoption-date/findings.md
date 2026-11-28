---
title: "Findings — ledger-adoption-date"
category: findings
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-64fa
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — ledger-adoption-date

Stage-2 call, 2026-11-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1325 files, 6215 commits, 12 rules.

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6217 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:2d47815fd2c734ddbc9c48035c5c7188b9a27fce80b8dd482f6cfa88a94a3c35

Spec review commit: f6ec03e28d8d19ffeea1bf3fee230a9334179bff

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | `spec.md`, criterion 8 | Criterion 8 says the workflow "identifies the repository's recorded adoption date". This has two readings. Reading A: the "Criterion tests" row (`docs/WORKFLOW.md:538`) gives this repository's value as a literal: "archived plans dated before 2026-10-29 without one are exempt". The interview-minimums paragraph does the same with "here **2026-10-08**" (`docs/WORKFLOW.md:107`), and the row test then checks that "2026-10-29" is in the row. Reading B: the row names no date but says where it comes from: the `criterion-ledger` entry of `decisions/adoption.yaml`, read per repository through `scripts/adoption.py`. The reason would be that `docs/WORKFLOW.md` and `tests/test_check_criterion_ledger.py` travel as mechanism (`scripts/kit/manifest.yaml:62`, `:234`) while the record stays as stock (`:383`). The row test then checks for the record's path. Under A, every instance's workflow states a date that is not its own. Under B, the workflow never states this repository's governing day. | Opus | in spec — reading A, criterion 8 names source and current value (bounded standing grant) | — |
| S-2 | MINOR | SPEC | base | `spec.md`, criterion 8 | The refutation catches only two cases: the old date still shown as the governing boundary, or a missing decision requirement. Take a row that drops the date and names no source, such as "archived plans dated before the cut-off without one are exempt; moving it is a decision pull request". It triggers neither clause, but it does not identify the recorded adoption date. So the positive half of the criterion cannot go red as written. | Opus | in spec — criterion 8 refutation covers a row without source or value | — |
| S-3 | MINOR | SPEC | base | `spec.md`, criterion 6 | The gate already has its own exit-3 cases: a root that is not a directory, a root without `plans/changes/`, and a `plans/changes/` that cannot be listed (`scripts/check_criterion_ledger.py:313-324`). The spec does not say whether the record check runs before or after them. An empty or missing root has no record either. So it could report "has no plans/changes/ directory" or the `decisions/adoption.yaml` remedy, and the refutation clause "the diagnostic or exit differs" would fail one of them. The spec also does not say what happens to ledger findings when the record cannot be read: are they still listed next to the not-measured line, or does that line stand alone? The builder has to decide both. | Opus | in spec — criterion 6: root checks first, record check after | — |
| S-4 | MINOR | SPEC | base | `spec.md`, Definition of Done | The Definition of Done asks the pull request to disclose only the widening from 2026-10-11 to 2026-10-29. It says nothing about the second behaviour change that criterion 6 brings. Before, a repository whose `decisions/adoption.yaml` has no `criterion-ledger` entry was measured against the constant. Now that repository gets exit 3 from a blocking gate, so `make verify` turns red. `research.md` names this effect ("An instance without the record is red, not green"), and the gate travels as mechanism to instances such as LakeSwitch. The builder is left to decide whether the pull request and the workflow row tell such a repository to add the entry. | Opus | in spec — Definition of Done states the exit-3 change | — |
