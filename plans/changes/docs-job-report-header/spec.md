---
title: "Spec — docs-job-report-header"
status: draft
implementation_status: partial
date: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-ooj5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification]
class: bounded
appetite: 1
adr_files: []
neighbours: [plans/changes/draft-gates-only/spec.md, plans/changes/verify-machine-lock/spec.md, plans/changes/verify-worker-cap/spec.md, plans/changes/run-report/spec.md]
---

# Spec — docs-job-report-header

The verification report header identifies the gate selection the run measures
(bead `coding-harness-ooj5` — correct the document-subset report header).
Research: `research.md`. Decisions: `decisions.md`.

## Problem

The exploration of 2026-11-02 found that `scripts/verify_all.sh` passes its
selected job to gate selection but omits it from the report request. The
report therefore defaults to `verify` even when the runner selects `docs`
or `drift`. The report and the following job banner disagree. The existing
`report(job)` already counts subset membership through `in_job`; the missing
selection at the caller causes the error, not the counting function.

The existing interview skip and agent details settle the intended repair:
name the document subset and its gate count, retaining the JSON vocabulary.
This report precedes verification gates; it is distinct from the read-only
snapshot produced by `make report`.

## Terms

**Selected gates:** all gates belonging to the requested job or subset in
the canonical gate file, before placement and local-executability filtering.
The report's `gates_job` describes membership, not a count of executed commands.

## Acceptance criteria

1. When the runner selects `docs`, `verify` or `drift`, the initial JSON report's `job` equals that selection, including `verify` when no `--job` is supplied.
   *Refuted by:* a document-subset run reports `verify`, a drift run reports another selection, or the default run ceases to report `verify`.

2. When the runner prints its report, `gates_job` equals the number of selected gates and `gates_total` equals the number of gates in the entire configuration.
   *Refuted by:* a fixture with distinct subset, verify, drift and total counts reports the verify count for `docs`, or either count changes with placement filtering rather than membership.

3. While the selected job is reflected in the report, its JSON field set and the meanings of `candidate`, `base` and `config_sha256` remain unchanged.
   *Refuted by:* a field is added or removed, `candidate` differs from HEAD, `base` differs from the merge base with `origin/main`, or the digest differs from SHA-256 of the gate file's bytes; unavailable git references retain their existing null values.

4. When selected gates run after the report, the existing selection and verdict rules still hold: only eligible selected gates execute, blocking failures yield exit 1, and passing gates or solely nonblocking failures yield exit 0.
   *Refuted by:* an unselected gate executes, an eligible gate is skipped, a later gate is abandoned after a failure, or a blocking/nonblocking failure yields the wrong exit status.

## Non-goals

- Changing report field names, adding fields, or redefining counts as placement-filtered execution totals.
- Changing gate membership, gate schema, hosted CI, admission, worker sizing or Stage-2 command selection.
- Changing `make report`, adding report documentation, or translating existing German code text.
- Phase 2b and an ADR: neither is due for this bounded caller correction.

## Protected areas

`scripts/ci_gates.py` already supports the required report semantics and stays
unchanged. `decisions/gates.yaml`, `.github/`, `Makefile`,
`scripts/stage2.py`, `scripts/verify_lock.py`, `scripts/run_report.py`,
`docs/WORKFLOW.md`, ADRs, prompts, templates and harness configuration remain
outside the correction; the runner's admission and worker-sizing blocks retain
their behavior.

## Definition of Done

- `make verify` is green and the criterion ledger names the implemented regression tests.
- Implementation changes `scripts/verify_all.sh` and `tests/test_ci.py`; this folder's plan and findings retain time and evidence, and the runner regenerates `plans/INDEX.md`. No other document or ADR moves.
- The pull request's file list demonstrates the protected areas and non-goals were respected.
- The pull request closes the document-report-header work item (`coding-harness-ooj5`); its last commit carries `Closes-Bead: coding-harness-ooj5`.
- Regression evidence names its date and revision; no performance measurement is required.

## Open decisions

None open. The reasoned interview skip in `decisions.md` supplies the intent;
this draft adds no maintainer answer.

[DETAIL] Cover default verify, explicit verify, docs and drift in the same
regression matrix: one caller supplies all selections, and this demonstrates
the repair without adding a new selection or changing membership.

[DETAIL] Derive expected counts from a deliberately unequal fixture rather
than freezing the live catalog's counts, so legitimate catalog changes do not
invalidate a header test. Preserve pre-placement counting because that is the
existing report contract.

[DETAIL] Set a one-hour phase-4 appetite, repairs included, as a stop for the
small caller-and-tests change; neither input prescribes an appetite.
