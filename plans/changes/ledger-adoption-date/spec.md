---
title: "Spec — ledger-adoption-date"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-64fa
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, gates]
class: bounded
appetite: 2
adr_files: []
---

# Spec — ledger-adoption-date

The criterion ledger gate uses each repository's recorded adoption date for its archive exemption (bead `coding-harness-64fa`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-28, research found that `scripts/check_criterion_ledger.py` hard-codes 2026-10-11, while `decisions/adoption.yaml` records 2026-10-29 for this gate. The existing adoption reader already checks that repository-specific record, but this gate does not use it. The earlier hard-coded boundary incorrectly holds archive plans without a ledger dated 2026-10-11 through 2026-10-28 under the recorded policy.

## Acceptance criteria

1. When the gate measures a repository, it uses that repository's recorded `criterion-ledger` adoption date as its exclusive archive exemption boundary.
   *Refuted by:* changing the recorded date leaves the boundary unchanged, or a ledgerless archived plan dated on the recorded day is exempt.
2. When an archived plan has no ledger and has exactly one valid, unquoted header date before the recorded adoption date, the gate exempts it.
   *Refuted by:* such a plan is reported missing its ledger.
3. When an archived plan has no ledger and its header date is missing, invalid, quoted, commented or repeated, the gate does not exempt it.
   *Refuted by:* one of those plans is exempted.
4. When a live plan has no ledger, the gate reports it regardless of its date.
   *Refuted by:* a live plan before the adoption day is exempt.
5. When an archived plan has a ledger, the gate checks it regardless of its date.
   *Refuted by:* an old archived ledger with a missing test is ignored.
6. If the adoption record or the gate's entry cannot be read as a valid recorded date, the gate reports not measured with the record's remedy and exits 3. The existing root checks (a root that is not a directory, without `plans/changes/`, or whose `plans/changes/` cannot be listed) run first and keep their own diagnostics; the record check runs only after them (S-3).
   *Refuted by:* a missing, unreadable, malformed, absent, quoted or impossible entry is accepted, or the diagnostic or exit differs; or a root without `plans/changes/` reports the adoption-record remedy instead of its own diagnostic.
7. When the gate reports its exemption summary, it names the recorded adoption date.
   *Refuted by:* the summary names the old constant or another date.
8. When the workflow describes the exemption, the "Criterion tests" row of `docs/WORKFLOW.md` names the source (the `criterion-ledger` entry of `decisions/adoption.yaml`), this repository's current value 2026-10-29, and that changing it takes a decision pull request (S-1 reading A).
   *Refuted by:* the row names the old date 2026-10-11 as the boundary, omits the source file, omits the current value, or omits the decision requirement (S-2).

## Non-goals

Changing adoption dates, the exemption rules apart from their date source, other gates, gate configuration, or historical ADR decisions is outside this change. This bounded change has no design phase or ADR draft.

## Protected areas

`decisions/adoption.yaml` holds the maintainer's recorded dates; this change reads it without editing it. Historical ADRs record decisions at their time and are not amended here.

## Definition of Done

- `make verify` green; `docs/WORKFLOW.md` moves with the code and tests.
- The pull request states that using 2026-10-29 expands the exemption to ledgerless archived plans dated 2026-10-11 through 2026-10-28, and that a repository whose `decisions/adoption.yaml` has no `criterion-ledger` entry now gets exit 3 from this blocking gate instead of being measured against the constant (S-4).
- Protected areas and non-goals remain untouched, as shown by the pull request's file list.
- The pull request closes bead `coding-harness-64fa` and its last commit carries `Closes-Bead: coding-harness-64fa`.
- Special runs: none.

## Open decisions

[DETAIL] Keep historical ADR wording intact: it describes the earlier arrangement, while the current workflow states the operative rule. This avoids treating a bounded fix as an ADR change. No maintainer decision is open.
