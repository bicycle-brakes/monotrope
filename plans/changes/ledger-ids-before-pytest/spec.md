---
title: "Spec — ledger-ids-before-pytest"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.9
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, criterion-ledger]
class: bounded
appetite: 4
adr_files: []
---

# Spec — ledger-ids-before-pytest

The runner names missing criterion-ledger tests before pytest while letting repairs address their own findings (bead `coding-harness-bxxt.9`). Research: `research.md`. Decisions: `decisions.md#Q-1` and `decisions.md#Q-2`.

## Problem

- At commit `5c7bce46` the runner passes ledger test references to pytest without checking whether they stand; a missing reference can stop collection of all selected tests (`research.md`, “What exists today”).
- On 2026-11-18 repairs failed on unrelated unwritten tests, with pytest reporting no tests ran without naming them (`decisions.md#Q-1`).

## Terms

**Ledger test:** a test reference in either recognized test form of the accepted plan's criterion ledger. **Standing:** the runner's parsed-name check finds the referenced name in the file; it recognizes top-level async functions and ignores definitions inside strings. **Attempt record:** for an accepted attempt, its line under `## Time used` in `plan.md`; for a failed attempt, its diagnostics block in `findings.md`.

## Acceptance criteria

1. When an implement or repair attempt selects tests, the runner checks every ledger test for existence before invoking pytest.
   *Refuted by:* a missing ledger test reaches pytest as a test ID.
2. When test selection finds one or more missing ledger tests, the attempt record names the missing test IDs in bounded diagnostic sections, including for an otherwise successful repair. Each section retains at most 80 lines; when it exceeds that bound, the record counts the omitted diagnostic lines.
   *Refuted by:* a missing ID is absent from an untruncated section, or a truncated section omits the count of diagnostic lines left out.
3. When missing ledger tests coexist with other selected targets, pytest runs the standing selected targets without the missing IDs.
   *Refuted by:* a missing ID prevents a standing selected test from running or is passed to pytest.
4. When no selected target stands, the runner skips pytest.
   *Refuted by:* pytest is launched with no standing target.
5. When an implement attempt has a missing ledger test, the attempt fails even if all standing selected tests pass.
   *Refuted by:* an implement attempt with a missing ledger test is accepted.
6. When a repair attempt finds a missing test referenced only by ledger entries still marked `not yet written`, that missing test alone does not fail the cheap check, even if a later finding-proof check claims it.
   *Refuted by:* the cheap check rejects an otherwise successful repair solely for that missing test.
7. When a repair attempt finds a missing test referenced by a written ledger entry, the attempt fails, including when an unwritten entry also names that test.
   *Refuted by:* a repair with a missing written ledger test is accepted because the same test also has an unwritten entry.
8. When a selected standing test fails, the attempt fails even if missing ledger tests were also reported.
   *Refuted by:* a repair or implement attempt accepts a failing selected test.
9. If the accepted plan cannot be read or decoded, or an existing selected test file cannot be read or parsed, the cheap check fails and identifies the input and fault.
   *Refuted by:* an unreadable or unparseable input yields a successful check or a missing-test-only diagnosis.
10. When a repair claims a test as a finding's proof, the existing post-verification answer check rejects a test that it finds undefined.
    *Refuted by:* the answer check accepts an undefined test named in a `fixed —` or `fixed — guard test —` claim.
11. When a repair addresses a finding, its existing required proof remains an obligation.
    *Refuted by:* a repair is accepted without the required proof of its finding.
12. When an implement prompt describes the ledger tests, it requires every ledger test, including entries marked `not yet written`.
    *Refuted by:* the implement prompt permits a missing unwritten ledger test.
13. When a repair prompt describes the ledger tests, it requires the tests of its findings and written ledger entries and says missing unwritten ledger tests are named but otherwise not owed.
    *Refuted by:* the repair prompt requires all unwritten ledger tests, omits the finding or written-entry obligation, or omits that other missing unwritten tests are named without being owed.
14. When a repair prompt asks the model to run pytest, its ledger test list excludes IDs that do not stand.
    *Refuted by:* a missing ledger ID is included in the repair's pytest command list.
15. If a selected ledger test file does not exist, the runner reports its ledger IDs as missing tests.
    *Refuted by:* an absent file is diagnosed as an unreadable existing file and fails an otherwise successful repair.
16. If a ledger test file cannot be read or parsed while building a repair prompt, the prompt still builds and identifies that input as unreadable or unparseable.
    *Refuted by:* prompt construction refuses the call or silently lists the affected ID as standing.
17. When a ledger line matches none of the recognized entry forms, the cheap check neither selects nor names it as a ledger test.
    *Refuted by:* a malformed entry is sent to pytest or reported as a missing ledger test by the cheap check.

## Non-goals

- A phase-6 checkpoint for unwritten ledger entries and a route to clear their debt: these move to a separately interviewed change (bead `coding-harness-bxxt.10`, `decisions.md#Q-2`).
- Changing criterion-ledger entry forms, the archive rule, the runner's ledger clearing, or the existing finding-proof requirements.
- Measuring pytest startup time, changing worker counts, or changing the scope of changed-test and retry selection.

## Protected areas

The criterion-ledger gate and its governance remain unchanged. Held paths remain untouched by the implementation attempt.

## Boundary

The runner's parsed-name check and the ledger gate's existing text-based check can disagree on async definitions and text inside strings; reconciling those checks is outside this change.

## Definition of Done

- `make verify` green; focused checks exercise implement and repair.
- `docs/WORKFLOW.md` describes the changed runner contract in the same pull request; no ADR is due.
- Protected areas and non-goals are checked against the pull request's file list.
- The pull request closes bead `coding-harness-bxxt.9`; its last commit carries `Closes-Bead: coding-harness-bxxt.9`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The phase-4 appetite is four hours including repairs: neither research nor the answered decisions specify one, and a finite stop makes the card actionable. [DETAIL] Use the runner's existing parsed-name check; read or parse faults fail separately, and collection and execution errors remain pytest's responsibility. [DETAIL] Selection follows lint, so an earlier lint failure does not also report missing IDs. [DETAIL] An absent file means a missing test; a read or parse error in an existing file is a fault. [DETAIL] A duplicate ID with any written entry is owed by repair because that written proof already exists in the accepted plan; the stricter obligation avoids losing it. [DETAIL] Malformed ledger lines are left to the existing criterion-ledger gate, which already reports them.
