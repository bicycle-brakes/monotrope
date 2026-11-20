---
title: "Spec — ledger-ids-before-pytest"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-20
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

The runner identifies missing criterion tests before pytest, permits a repair to address its own findings, and holds unwritten tests at phase 6 (bead `coding-harness-bxxt.9`). Research: `research.md`. Decision: `decisions.md#Q-1`.

## Problem

- At commit `5c7bce46` the runner passes ledger test references to pytest without checking whether they stand; a missing reference can stop collection of all selected tests (`research.md`, “What exists today”).
- On 2026-11-18 repairs failed on unrelated unwritten tests, with pytest reporting no tests ran without naming them; phase 6 had no checkpoint for that debt (`decisions.md#Q-1`).

## Terms

**Ledger test:** a test reference in either test form of the accepted plan's criterion ledger. **Standing:** the runner's parsed-name check finds the referenced name in the file; it recognizes top-level async functions and ignores definitions inside strings. **Attempt record:** for an accepted attempt, its line under `## Time used` in `plan.md`; for a failed attempt, its diagnostics block in `findings.md`. **Ledger-debt finding:** a taken finding whose status is `taken — ledger test — tests/<path>::<function>`, naming exactly one still-marked entry in the accepted plan.

## Acceptance criteria

1. When an implement or repair attempt selects tests, the runner checks every ledger test for existence before invoking pytest.
   *Refuted by:* a missing ledger test reaches pytest as a test ID.
2. When test selection finds one or more missing ledger tests, the attempt record names each missing test ID.
   *Refuted by:* a missing ID is absent from the record, including for an otherwise successful repair.
3. When missing ledger tests coexist with other selected targets, pytest runs the standing selected targets without the missing IDs.
   *Refuted by:* a missing ID prevents a standing selected test from running or is passed to pytest.
4. When no selected target stands, the runner skips pytest.
   *Refuted by:* pytest is launched with no standing target.
5. When an implement attempt has a missing ledger test, the attempt fails even if all standing selected tests pass.
   *Refuted by:* an implement attempt with a missing ledger test is accepted.
6. When a repair attempt finds a missing test of a ledger entry still marked `not yet written`, that missing test alone does not fail the attempt regardless of whether a later finding-proof check claims it.
   *Refuted by:* the cheap check rejects an otherwise successful repair solely for a missing test of an unwritten entry.
7. When a repair attempt finds a missing test of a written ledger entry, the attempt fails.
   *Refuted by:* a repair that removed a written ledger test is accepted.
8. When a selected standing test fails, the attempt fails even if missing ledger tests were also reported.
   *Refuted by:* a repair or implement attempt accepts a failing selected test.
9. When the current plan contains a ledger entry marked `not yet written`, phase 6 refuses before full verification and reviewer invocation and names each such entry and the next step: take one ledger-debt finding per entry, then run `python3 scripts/stage2.py repair <change>`.
   *Refuted by:* full verification or the reviewer starts, an entry is omitted, or the refusal omits that repair route; the marker still refuses even if the test already exists.
10. When the current plan has no `not yet written` ledger entry, this checkpoint does not refuse phase 6.
    *Refuted by:* a plan with only written tests and non-test entries is refused by this checkpoint.
11. If the runner cannot read or parse the ledger or an existing selected test file, it fails and identifies the input and fault instead of treating the tests as absent or the checkpoint as clear.
    *Refuted by:* an unreadable or unparseable input yields a successful check or a missing-test-only diagnosis.
12. When a repair claims a test as a finding's proof, the existing post-verification answer check rejects a test that it finds undefined.
    *Refuted by:* the answer check accepts an undefined test named in a `fixed —` or `fixed — guard test —` claim.
13. When a repair addresses a finding other than a ledger-debt finding, its existing required proof remains an obligation.
    *Refuted by:* a repair is accepted without the required proof of its finding.
14. When an implement prompt describes the ledger tests, it requires every ledger test, including entries marked `not yet written`.
    *Refuted by:* the implement prompt permits a missing unwritten ledger test.
15. When a repair prompt describes the ledger tests, it requires the tests of its findings and written ledger entries and says missing unwritten ledger tests are named but otherwise not owed.
    *Refuted by:* the repair prompt requires all unwritten ledger tests, omits the finding or written-entry obligation, or omits that other missing unwritten tests are named without being owed.
16. When a repair prompt asks the model to run pytest, its ledger test list excludes IDs that do not stand.
    *Refuted by:* a missing ledger ID is included in the repair's pytest command list.
17. If a selected ledger test file does not exist, the runner reports its ledger IDs as missing tests.
    *Refuted by:* an absent file is diagnosed as an unreadable existing file and fails an otherwise successful repair.
18. If a ledger test file cannot be read or parsed while building a repair prompt, the prompt still builds and identifies that input as unreadable or unparseable.
    *Refuted by:* prompt construction refuses the call or silently lists the affected ID as standing.
19. When a ledger-debt finding is repaired, its fixed claim names exactly the test in its status and that test passes on the repaired tree.
    *Refuted by:* a mismatched, absent, uncollectable, or failing test is accepted as that finding's proof.
20. When a ledger-debt finding's matching test passes, the repair does not require that test to fail on the baseline.
    *Refuted by:* a passing test rejected solely because it also passed on the baseline.
21. If a finding is not a ledger-debt finding naming a still-marked entry in the accepted plan, it cannot use the ledger-debt proof exception.
    *Refuted by:* an arbitrary or already-written test bypasses the existing proof requirement through that status.
22. When a ledger-debt repair is accepted, the corresponding marker is cleared through the existing ledger clearing.
    *Refuted by:* an accepted repair leaves its claimed entry marked `not yet written`, including when the original test is an async definition.

## Non-goals

- Changing criterion-ledger entry forms, the archive rule, or the runner's ledger clearing.
- Measuring pytest startup time, changing worker counts, or changing the scope of changed-test and retry selection.
- Relaxing phase-6 verification or review, or the existing proof required for findings other than ledger-debt findings.

## Protected areas

The ledger gate and its governance remain unchanged: the new phase-6 checkpoint belongs to the runner, not a second ledger format or a change to archive policy. Held paths remain untouched by the implementation attempt.

## Boundary

The runner's parsed-name check and the ledger gate's existing text-based check can disagree on async definitions and text inside strings; reconciling those checks is outside this change. A ledger-debt repair must provide a test recognized by both checks, for example by rewriting an async test into a valid top-level synchronous test, before the existing clearing can remove its marker.

## Definition of Done

- `make verify` green; focused checks exercise implement, repair and phase 6.
- `docs/WORKFLOW.md` describes the changed runner contract in the same pull request; no ADR is due.
- Protected areas and non-goals are checked against the pull request's file list.
- The pull request closes bead `coding-harness-bxxt.9`; its last commit carries `Closes-Bead: coding-harness-bxxt.9`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The phase-4 appetite is four hours including repairs: neither research nor the answered decision specifies one, and a finite stop makes the card actionable. [DETAIL] Use the runner's existing parsed-name check for selected IDs; read or parse faults fail separately, and collection and execution errors remain pytest's responsibility. [DETAIL] Selection follows the existing lint checks, so an earlier lint failure does not also report missing ledger IDs. [DETAIL] The record locations and repair route above follow the existing runner-owned evidence and repair paths. [DETAIL] A missing file is a missing test, while a read or parse error in an existing file is a fault. [DETAIL] The ledger-debt status names one marked entry, so its exception cannot apply to unrelated findings; it proves an already-built behavior by a passing test rather than a baseline failure.
