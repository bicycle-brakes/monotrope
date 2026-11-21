---
title: "Spec — red-against-commit"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-qvf7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, repair, red-first]
class: bounded
appetite: 2
adr_files: []
---

# Spec — red-against-commit

A repair row can name an earlier commit for its red-first proof when the fix is already committed (work item `coding-harness-qvf7`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `aacfe4d4` on 2026-11-21, `research.md` records that a repair uses the run-start HEAD as its red baseline. If saved work containing the fix has since been committed, the named test can already pass there and the proof refuses, even though an earlier commit can show the fault. The recorded workaround was a manual proof. The existing proof already accepts a commit internally but a repair row cannot select one.

## Terms

- **Attempt:** the repair's current Git-visible tree, including uncommitted work.
- **Qualifying red:** the existing red-first outcome: a named test's assertion or pytest failed outcome in its call, with the existing outcome and execution protections satisfied.
- **Saved-attempt ref:** a local ref under `refs/stage2/attempts/<change>/`; its tip and its ancestors are reachable from it, and the ref need not exist on another machine.
- **SHA:** 7–64 hexadecimal characters, uppercase or lowercase, occupying the entire final suffix token; revision expressions and names are not SHAs. Ambiguity means more than one matching commit, regardless of matching objects of other types.

## Acceptance criteria

1. When an ordinary repair's fixed line names `fixed — tests/<path>::<function> — red against <sha>`, the runner accepts that form for validation and, after successful proof, records `fixed — tests/<path>::<function> — red against <full sha>` in the row Status.
   *Refuted by:* a valid line being rejected or the Status retaining an abbreviation instead of the resolved full commit ID.
2. If the supplied SHA is malformed, ambiguous, unavailable, not a commit, or the run-start HEAD itself, or neither a proper ancestor of the run-start HEAD nor reachable from a saved-attempt ref for this change, the runner refuses the repair with a reason and leaves its rows taken.
   *Refuted by:* accepting HEAD itself, a missing object, a tag or tree as the named object, an unrelated commit, another change's saved attempt, `HEAD~1`, trailing text, fewer than 7 or more than 64 hex characters, or a prefix matching multiple commits, or marking a refused row fixed. A prefix matching exactly one commit and a blob or tree must not be refused as ambiguous; a saved-attempt tip is eligible unless it equals HEAD.
3. If the named test file is absent from the selected commit, the runner refuses the repair with a reason and leaves its rows taken.
   *Refuted by:* an attempt-only test file being sufficient for a selected commit that lacks that file.
4. When an eligible commit is selected, the red proof runs the attempt's Git-visible tests against that commit's production tree in the existing isolated proof environment.
   *Refuted by:* exercising HEAD or the attempted production fix instead, or using the old test contents instead of the attempt's test contents.
5. If the selected-commit run is green or otherwise lacks a qualifying red, the runner refuses the repair with a reason and leaves its rows taken.
   *Refuted by:* accepting a passing test, collection or fixture failure, skip, or unrelated exception as red evidence.
6. If the selected-commit red proof succeeds but the named test does not pass the existing fixed-code proof on the attempt, the runner refuses the repair and leaves its rows taken.
   *Refuted by:* a successful red leg alone marking the row fixed, or a failing attempted tree being replaced by committed HEAD for the green leg.
7. When both proof legs succeed, the runner records `yes — red against <full sha> — tests/<path>::<function>` as the Broke-a-test mark only after all repair rows pass their checks.
   *Refuted by:* a success mark without both legs, a mark omitting or misidentifying the commit, or partial fixed statuses when another row fails.
8. When an ordinary fixed line has no selected commit, the existing run-start baseline and evidence behavior remain in force.
   *Refuted by:* changing the baseline, status or evidence of an otherwise identical ordinary repair.
9. When guard-test or `not a test` repair forms are used, their existing authorization and proof rules remain in force, except that a terminal ` — red against <sha>` suffix is refused, including when it is part of a not-a-test reason.
   *Refuted by:* the suffix bypassing guard authorization or allowing a proof-free ordinary code repair.
10. When a selected-commit proof runs, the existing isolation, outcome validation, tool integrity, admission, timeout, diagnostic scrubbing and cleanup protections remain in force.
    *Refuted by:* a source worktree or ref being changed by ordinary proof setup, a nonqualifying outcome passing, a modified tool running, a secret appearing in a refusal, or a failed cleanup being treated as success.
11. When repair instructions describe fixed lines, they explain the optional selected-commit form, its eligibility, its proof requirements and the corresponding success mark.
    *Refuted by:* instructions omitting the form or mark, or claiming that the form bypasses either proof leg.

12. When either repair route receives taken rows, its prompt lists the run-start HEAD and its first-parent ancestors since the merge base with `origin/main`, and this change’s saved-attempt ref tips, with each commit ID and subject; it identifies HEAD as the default baseline, not a selectable SHA.
    *Refuted by:* either route lacking the list, a listed commit lacking its ID or subject, including another change’s saved refs, or presenting HEAD as a selectable SHA.

## Non-goals

- Changing initial implementation proof, the criterion-ledger grammar, guard-test evidence, attempt saving or model routing.
- Proving semantically that the chosen commit lacks the intended fix: a qualifying failure demonstrates the test outcome, and phase 6 still judges whether the test exercises the real fault.
- Making local saved-attempt refs portable, or fetching missing commits.
- An ADR or design phase: this is a bounded extension of the existing repair proof.

## Boundary

The selected commit must contain the test file, but the red run uses the attempt's Git-visible test tree. A qualifying red does not establish by itself that the failure is the intended fault. Existing private-repository isolation is not an operating-system sandbox against a test addressing an external path directly.

## Protected areas

- Accepted ADRs, `decisions/gates.yaml`, `provenance.yaml`, model configuration, other change folders and tracker data: no governance, routing or unrelated work changes.
- Criterion-ledger grammar and saved-attempt lifecycle: the new evidence belongs only to repair rows.

## Definition of Done

- `make verify` green; new regression tests shown red against the missing behavior and green after implementation.
- `scripts/stage2.py`, `tests/test_stage2.py`, `docs/WORKFLOW.md`, `prompts/04-implement.md`, `prompts/04b-review-loop.md` and `templates/findings.md` move with the change; held prompt and template edits are made by the orchestrator after the accepted attempt; the orchestrator regenerates `plans/INDEX.md`.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes `coding-harness-qvf7` (selecting a red-against commit for repairs), with `Closes-Bead: coding-harness-qvf7` in its last commit.
- Special external runs: none.

## Open decisions

None open. The maintainer's answer and the reasoned interview skip are recorded in `decisions.md`.

- [DETAIL] Use a two-hour phase-4 appetite including repairs: the change extends an existing proof and has a bounded regression matrix.
- [DETAIL] Record the resolved full commit ID in both Status and the distinct success mark: an abbreviation can later become ambiguous.
- [DETAIL] List recent first-parent history and same-change saved-attempt tips in both repair prompts so the file-tools route can select a commit; eligibility remains broader than this prompt list.
- [DETAIL] Accept 7–64 hexadecimal characters and resolve ambiguity among commits only; this gives a checkable input boundary. HEAD is excluded because the ordinary form already uses it. Refuse the suffix on `not a test` even as trailing reason text so it cannot be mistaken for proof.
