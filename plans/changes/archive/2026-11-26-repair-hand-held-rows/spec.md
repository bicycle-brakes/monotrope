---
title: "Spec — repair-hand-held-rows"
status: accepted
implementation_status: done
date: 2026-11-21
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-0zhf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, repair]
class: bounded
adr_files: []
---

# Spec — repair-hand-held-rows

Before a repair attempt, separate taken findings whose named paths the runner cannot commit and hand them to the orchestrator (bead `coding-harness-0zhf`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-20/21, three repair attempts encountered paths the runner does not commit; the morning handover reports that whole attempts were restored (`research.md`, “The night's evidence”).
- At baseline `7b531fd0`, the checkpoint detects held paths only after an attempt and restores the attempt rather than advancing to another route; an existing rollback test pins that outcome (`research.md`, “The rollback” and “A rollback consumes the attempt and ends the run”).

## Terms

**Held path:** a repository path the repair checkpoint cannot commit under its existing case-insensitive prefix rules, including committed human-decided prefixes and its existing exceptions.

**Taken row:** the current finding selected for repair by the existing resolver, whether in the active loop record or findings.

**Named path:** a repository-relative path-like token in `Where`, including both the text and target of a Markdown link. Split the cell on whitespace, commas and semicolons; strip surrounding backticks, quotes and brackets and trailing punctuation. Remove a trailing `:line`, `:line-line`, `#L<line>` or `#L<line>-L<line>` location, including ranges with an en dash. An initial `./` is removed; absolute paths inside the checkout are made relative to its root. A relative link target is interpreted from the repository root, with `.` and `..` collapsed only when it remains inside that root; an external URL, an absolute path outside the checkout or a path escaping the root is not a named repository path. Case-insensitive matches to tracked paths use their tracked spelling; other paths retain their normalized spelling. A tracked file is not required. A token naming an existing directory containing at least one tracked file is matched as that directory followed by `/`, even when the token has no trailing slash; a bare word that equals a held directory prefix names that directory, tracked or not; any other untracked bare word remains literal. An opening wrapper (bracket, quote, backtick) whose closing partner sits on a later token is stripped alone.

## Acceptance criteria

1. When repair selects taken rows, each row whose `Where` names any held path is classified for an orchestrator hand step before a model call.
   *Refuted by:* A row naming both a committable path and a held path enters the model batch, or a held prefix accepted by the checkpoint is missed because of case or the committed provenance map.
2. When a taken row's `Where` names no held path, it remains eligible for the model as it is today.
   *Refuted by:* A pathless row, an unknown non-held path, or a non-held directory is handed off or refused solely because of its `Where`.
3. When a batch contains both held and committable rows, the model receives only the committable taken rows for repair.
   *Refuted by:* The model receives a held row or does not receive an eligible committable row.
4. If every taken row is held and the existing pre-call checks pass, repair makes no model call; it exits 0 with the hand-step listing on standard output when the repository's blocking document gates are green, and exits 1 without a commit when one is red.
   *Refuted by:* A model is called, the exit is nonzero with green gates, a red gate still commits, or standard output does not identify the rows and their held paths.
5. When held rows are classified, the runner reports each row's identifier, each named held path and the reason `runner-held path` in its answer and in a listing appended to `findings.md`.
   *Refuted by:* Either listing omits an affected row, a named held path, or the reason, including when no model call is made.
6. While handing off held rows, the runner leaves their Status and `Broke a test` cells unchanged.
   *Refuted by:* A held row is marked fixed or its test mark is changed by the runner.
7. If an attempt nevertheless changes a held path, the existing checkpoint restores the attempt and refuses it.
   *Refuted by:* An unexpected held-path edit is committed or survives the existing rollback.
8. When a mixed batch's committable rows pass the existing repair checks, repair commits and books those rows as fixed and exits 0 even while held hand steps remain open.
   *Refuted by:* The answer check demands a fixed line for a held row, or an eligible fixed row is not booked and committed.
9. When repair selects rows, the existing waiting, origin and legacy-marker pre-call checks apply to all selected rows before classification or handoff.
   *Refuted by:* A held row with a legacy completion marker bypasses the booking refusal or a waiting or invalid-origin row is bypassed.
10. When repair hands off held rows, it appends one listing before the attempt loop and preserves that listing through a failed or rolled-back attempt.
    *Refuted by:* The listing disappears on rollback or is duplicated by retries in the same invocation.
11. When every selected row is held and the blocking document gates are green, repair commits the hand-step listing without a model attempt, including a listing a failed mixed run left uncommitted; a red gate exits 1 with no commit.
    *Refuted by:* A successful handoff leaves the listing uncommitted or admits a pre-existing change that the existing preflight and checkpoint would refuse; the existing allowances for this change's findings and derived leftovers remain in force.
12. When the runner writes a hand-step listing to `findings.md`, it uses a dated `Hand steps for the orchestrator` heading and one bullet per row with its identifier, normalized held paths and reason.
    *Refuted by:* The listing is a table, lacks the date, or loses a row identifier, path or reason.
13. When a later repair resolves findings, a hand-step listing is not parsed as a finding row.
    *Refuted by:* A previously listed identifier causes a duplicate-row refusal or becomes a repair target solely from the listing.
14. When a mixed repair commits, its subject names only the repaired row identifiers and its body names the held identifiers as hand steps.
    *Refuted by:* A held identifier is claimed as repaired in the subject or omitted from the hand-step body.
15. When the runner writes a hand-step listing, its booking hint uses the existing valid status forms, including `fixed — not a test — orchestrator hand edit <sha>` only for a row taken as `not a test`.
    *Refuted by:* The hint proposes `fixed — orchestrator hand edit <sha>`, omits a valid test form or the option to retake a row as `taken — not a test` when no test fits, or allows the not-a-test form without that status.
16. When a held-only handoff commits, its subject is `docs(<change>): hand steps for the orchestrator <ids>`.
    *Refuted by:* Its subject claims the held identifiers were repaired or uses the repair subject.
17. When a model answer mentions a held row of the current run, the answer check ignores that line without booking the row.
    *Refuted by:* The mention fails the attempt or marks the held row fixed.
18. When a mixed batch is dispatched, the model is told that the held rows are not its work.
    *Refuted by:* The prompt gives no such instruction.
19. When the workflow describes booking a handed-off row, it retains the existing test-based forms and requires a row to be taken as `not a test` before the corresponding fixed form is used.
    *Refuted by:* The workflow treats every hand edit as automatically eligible for `fixed — not a test` or omits the test-based forms.

## Non-goals

- Changing `implement` or `draft` routing, retry limits, model selection, or the checkpoint's held-path policy.
- Inferring required edits from a finding's prose when its `Where` does not name a held path.
- Performing or booking the orchestrator's hand repair, or changing the hand-repair status vocabulary.

## Protected areas

Held paths, including `provenance.yaml`, endpoint configuration, agent instructions, prompts, templates, ADRs and the tracker, remain outside the implementation attempt; the checkpoint remains authoritative for their protection.

## Definition of Done

- `make verify` green.
- Moved in the same pull request: `docs/WORKFLOW.md` and the change artifacts, alongside the runner and its tests; no ADR.
- The protected areas untouched and the non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead `coding-harness-0zhf` and its last commit carries `Closes-Bead: coding-harness-0zhf`.
- Special runs: none.

## Open decisions

None open. The reversible scope, batch split, hand-step format and preserved checkpoint are decided with reasons in `decisions.md` and the phase-2a findings. [DETAIL] Path normalization treats link targets as repository-root-relative and ignores outside paths: this gives an unambiguous, reversible interpretation without requiring a tracked file. [DETAIL] The tokenizer splits on whitespace, commas and semicolons and removes surrounding punctuation and location suffixes: it recognizes the forms accepted by the runner's existing `Where` guidance. [DETAIL] Link text as well as link targets can name a path, and a tracked directory is matched with a trailing slash: these catch the observed held-path shapes. [DETAIL] A held-only commit uses the existing checkpoint and its existing allowances, and its subject names hand steps: this keeps one commit path and does not claim a repair. [DETAIL] Held-row answer lines are ignored and the prompt excludes those rows from the model’s work: the model can still read the findings record. [DETAIL] The booking hint retains all existing forms and restricts the not-a-test example to rows that authorize it, so the handoff cannot suggest an invalid status.
