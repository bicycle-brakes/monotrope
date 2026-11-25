---
title: "Spec — red-first-baseline"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7aso
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, red-first]
class: bounded
appetite: 4
adr_files: []
---

# Spec — red-first-baseline

A repair's baseline proof reports the named test's actual outcome and accepts only a qualifying red (bead coding-harness-7aso). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-20 the runner reported two finder-partial-report repair tests green on baseline while a hand check found tests red; whether those checks used the same inputs and why the runner reported green are not established (`research.md`, “What exists today” and “What is unclear about it”; refusal record `ca493614`, hand repair `5121a00c`). Separately, the workflow permits pytest exit 2 although the implementation and governing successor spec require exit exactly 1 (`research.md`, “What is unclear about it”; `decisions.md`, D-1).

## Terms

**Baseline proof:** the runner's `red_first` check, using production code from the captured baseline commit and the attempt's Git-visible `tests/` tree.

## Acceptance criteria

1. When the recorded round-3 refusals are investigated, the evidence record identifies the captured baseline, attempted test bytes, selector, direct pytest outcome and baseline-proof outcome for each of L3-1 attempts 1 and 2 and L3-4 attempt 3, or names unavailable evidence after searching commit `ca493614`, branch `fix/finder-partial-report`, saved-attempt refs and files in the lane's Git directory, and the bead notes; derived inputs carry their provenance and unrecovered test bytes are not invented.
   *Refuted by:* An attempt or required search is omitted, accessible evidence is marked unavailable, a derivation lacks provenance, or an unavailable input or outcome is presented as known.
2. When the recorded inputs are available, the investigation compares this branch's baseline proof with direct pytest in a normal checkout for each attempt, using the same captured baseline, attempted `tests/` tree, selector and this worktree's `.venv` interpreter, and records the difference between this branch's runner and the incident commit's runner.
   *Refuted by:* A comparison uses different baseline, test bytes, selector or interpreter, omits an available attempt or the historical runner comparison, or attributes a historical-only fault to this branch without evidence.
3. When an in-scope runner mismatch is reproduced, a self-contained regression detects its measured mechanism without depending on incident objects in a local Git store.
   *Refuted by:* The regression passes with the measured fault planted, misses a distinct reproduced mechanism, needs an incident object unavailable in a fresh clone, or the post-fix proof still disagrees with direct pytest on available incident inputs.
4. When pytest exits other than 1 and the baseline proof refuses the run, the proof reports the actual exit code and, when a valid probe record provides an outcome, a true outcome such as a pass, empty selection, collection error, skip, xfail or XPASS rather than only the exit status.
   *Refuted by:* Such a refusal omits or misstates the exit code, or substitutes a generic session-status message for an available outcome; reporting the first true outcome suffices when several exist.
5. When a baseline run has a qualifying assertion or pytest failure, exit 1, passing setup and teardown, and no disqualifying outcome, the baseline proof accepts it.
   *Refuted by:* The proof refuses such a run for any reason, including an incorrect outcome, missing record or ref fault, in the absence of actual interference or infrastructure failure.
6. When the named test passes on the baseline, the baseline proof refuses it as not red first.
   *Refuted by:* A passing baseline test is accepted as proof of a repair.
7. When the baseline run has an environment, collection, setup, teardown or nonqualifying call error, the baseline proof refuses it.
   *Refuted by:* A missing dependency, collection failure, fixture error or unrelated exception is accepted as a qualifying red.
8. When any selected case is skipped, xfailed or unexpectedly passes, the baseline proof refuses the run.
   *Refuted by:* A skipped, xfailed or XPASS case is accepted as red, including in a mixed selection.
9. When the baseline proof runs, it uses baseline production code and the attempt's Git-visible tests without changing the source repository's refs, index or worktree.
   *Refuted by:* Attempt production bytes reach the proof, attempt tests are omitted, or the proof changes the source repository.
10. When a reader consults the workflow's red-first exit contract, it states that a qualifying baseline run requires pytest exit exactly 1.
    *Refuted by:* The workflow permits exit 2 or omits the exit-1 requirement.
11. When a measured defect is repaired in a helper shared with the fixed-code or guard proof, both proofs retain their existing contracts.
    *Refuted by:* A passing fixed-code test or clean guard leg is refused, a non-passing fixed-code test or nonqualifying planted guard leg is accepted, or existing source and ref safeguards regress.
12. When pytest exits nonzero before writing a probe record, the refusal includes its actual exit code and a protected diagnostic from combined stdout and stderr, capped at 40 lines and 4,000 characters including a truncation marker when truncated, and fails closed if protection fails.
    *Refuted by:* The exit code is omitted or wrong, a `conftest.py` import error has no diagnostic, the diagnostic exceeds either cap or omits the marker when truncated, or protection failure exposes output.

## Non-goals

- Changing the tests-only baseline rule for code under test inside a test file (bead coding-harness-bf9m); that separate investigation can bring it back.
- Changing guard-test routing, the qualifying-failure definition, external dependency provisioning or the fixed-code proof's contract; a measured defect in a shared helper may be repaired without changing that contract.
- Treating a different hand test or baseline as proof of a runner mismatch.

## Protected areas

Other change folders, accepted ADRs and tracker data are outside this bounded repair; the private proof repository and ref safeguards remain in force.

## Definition of Done

- `make verify` green; `docs/WORKFLOW.md` accompanies the correction; no ADR or model change.
- The protected areas are untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request records the evidence for all three attempts, including searches, commands, inputs, outcomes, measured commits and any unavailable evidence; for each reproduced in-scope fault it records the pre-fix failing regression, the post-fix passing regression and the post-fix comparison on available incident inputs.
- If no runner fault is found, or a cause is outside scope, ship the applicable reporting and workflow corrections with the evidence record and report the outcome on the bead; do not claim a fault was reproduced without evidence. If necessary preserved evidence is unavailable or an out-of-scope bug remains, leave the bead open.
- Overwritten attempt-1 test bytes that were never saved are documented as unavailable but do not alone prevent closure once preserved evidence and measurable checks explain the refusals and the reporting fix is complete. Only when all measured runner causes are fixed or confirmed not to be runner faults, with no unresolved incident or out-of-scope bug remaining, the pull request closes bead `coding-harness-7aso` and its last commit carries `Closes-Bead: coding-harness-7aso`.
- Special runs: the incident comparisons above; none otherwise.

## Open decisions

[DETAIL] A self-contained synthetic repository carries each measured mechanism into regression tests; local incident objects are investigation evidence only, so fresh clones can run the suite (spec-review S-5).

[DETAIL] All three recorded attempts are investigated independently; a shared cause must be evidenced, and distinct in-scope causes each need coverage (spec-review S-4, S-8).

[DETAIL] A mismatch caused by the runner's private checkout or its filtered environment is in scope; missing external packages remain outside it (spec-review S-10). Fixing a shared helper is allowed while preserving the fixed-code proof's contract (S-11). The first true disqualifying outcome suffices (S-12); a pre-record failure uses bounded protected terminal output (S-13).

[DETAIL] The four-hour phase-4 appetite is a reversible stop; report the evidence and remaining work if the limit is reached.

[DETAIL] The current runner and worktree interpreter are compared on recovered inputs; the historical runner diff identifies faults that existed only at the incident. Derived inputs are labelled with their evidence, and unrecovered bytes are never reconstructed from prose (spec-review S-15, S-16).

[DETAIL] Unrecoverable overwritten attempt-1 bytes alone do not block closure once the preserved evidence explains the refusals; each reproduced in-scope fault also needs a post-fix incident comparison and a green synthetic regression (spec-review S-17, S-18).

[DETAIL] Non-exit-1 diagnostics name a recorded outcome rather than the generic session status; existing exit-1 wording and the fixed and guard proof contracts remain in force (spec-review S-19, S-20, S-21). The diagnostic cap includes its truncation marker, so the limit remains measurable (S-22).
