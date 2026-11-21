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

1. When the two recorded round-3 refusals are investigated, the evidence record identifies for each the captured baseline, attempted test bytes, selector, direct pytest outcome and baseline-proof outcome, or states which evidence is unavailable.
   *Refuted by:* Either refusal is omitted, or an unavailable input or outcome is presented as known.
2. When the recorded inputs are available, the investigation compares the baseline proof with direct pytest on the same captured baseline and attempted `tests/` tree for each refusal.
   *Refuted by:* A comparison uses different baseline or test bytes, or omits either refusal.
3. When an in-scope runner mismatch is reproduced, a self-contained regression detects its measured mechanism without depending on incident objects in a local Git store.
   *Refuted by:* The regression passes with the measured fault planted, misses a distinct reproduced mechanism, or needs an incident object unavailable in a fresh clone.
4. When pytest completes a baseline run, the baseline proof reports its actual exit code and relevant selected-test outcomes, including skip, xfail and collection errors.
   *Refuted by:* The proof reports exit 0 for a run that exited differently, or misreports or conceals a skip, xfail or collection error.
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

## Non-goals

- Changing the tests-only baseline rule for code under test inside a test file (bead coding-harness-bf9m); that separate investigation can bring it back.
- Changing guard-test routing, the qualifying-failure definition, dependency provisioning or the fixed-code proof.
- Treating a different hand test or baseline as proof of a runner mismatch.

## Protected areas

Other change folders, accepted ADRs and tracker data are outside this bounded repair; the private proof repository and ref safeguards remain in force.

## Definition of Done

- `make verify` green; `docs/WORKFLOW.md` accompanies the correction; no ADR or model change.
- The protected areas are untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request records the evidence for both refusals, including commands, inputs, outcomes, measured commits and any unavailable evidence; it records pre-fix and post-fix results for each reproduced in-scope fault.
- If both cases are measured and no runner fault is found, or their cause is outside scope, ship the applicable reporting and workflow corrections with the evidence record and report the outcome on the bead; do not claim that a fault was reproduced. If necessary evidence is unavailable, record that fact, leave the incident unresolved and do not claim the bead is closed on unmeasured cases.
- Once the bead's scope is resolved, the pull request closes bead `coding-harness-7aso` and its last commit carries `Closes-Bead: coding-harness-7aso`.
- Special runs: the incident comparisons above; none otherwise.

## Open decisions

[DETAIL] A self-contained synthetic repository carries each measured mechanism into regression tests; local incident objects are investigation evidence only, so fresh clones can run the suite (spec-review S-5).

[DETAIL] Both recorded refusals are investigated independently; a shared cause must be evidenced, and distinct in-scope causes each need coverage (spec-review S-4).

[DETAIL] The four-hour phase-4 appetite is a reversible stop; report the evidence and remaining work if the limit is reached.
