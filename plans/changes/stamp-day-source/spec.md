---
title: "Spec — stamp-day-source"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5v6t
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, frontmatter]
class: bounded
appetite: 3
adr_files: []
---

# Spec — stamp-day-source

Runner checkpoint stamps and the frontmatter check agree on the commit's calendar day, including across midnight (bead `coding-harness-5v6t`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-09 commit `6bf5c6fc` changed `docs/WORKFLOW.md` on the 9th with an `updated:` date of the 8th; the frontmatter check rejected it and three later repair attempts failed on that gate. The precise cause of the original mismatch was not established (`research.md`).
- At baseline `9dec171e`, runner stamps use the local day when written, whereas the check uses a clean file's last non-merge commit day in that commit's recorded offset. A midnight crossing between stamp and commit can therefore make a previously current stamp stale (`research.md`).

## Acceptance criteria

1. When a runner checkpoint commits a changed document with a runner-maintained `updated:` stamp, its stamp is at least the checkpoint commit's calendar date in the commit's recorded offset.
   *Refuted by:* the checkpoint commits a runner-maintained stamp older than its own recorded day.
2. When stamping occurs before local midnight and the checkpoint commits after it, the resulting committed document passes the frontmatter-current check.
   *Refuted by:* the committed document is reported stale after that crossing.
3. When a checkpoint is made at 00:30 at offset +0100, its runner-maintained stamp uses that commit's calendar day even though UTC is still on the preceding day.
   *Refuted by:* the stamp is the preceding UTC day or the check reports it stale.
4. When the check dates a clean document, it continues to use the most recent non-merge commit's calendar day in that commit's own recorded offset.
   *Refuted by:* the existing offset example uses the UTC day or a merge's day instead.
5. If the runner cannot establish or apply a consistent checkpoint day to a document it must stamp, it does not create that checkpoint.
   *Refuted by:* a checkpoint is created after that failure.
6. When the runner refreshes a stamp for a checkpoint, it preserves the document's other content and the existing protected-path rules.
   *Refuted by:* another document field changes or a held path enters the checkpoint because of the refresh.

## Non-goals

- Changing the recorded-offset rule for existing history, the future-date allowance, or manual Git commits outside the runner.
- Redesigning clocks, duration measurement, or unrelated date-bearing fields.

## Protected areas

Runner-held paths and human-decided content retain their existing protections; the fix does not commit their derived stamps.

## Definition of Done

- `make verify` green.
- No ADR or other accompanying document change is due.
- The pull request file list shows the protected areas and non-goals respected.
- The pull request closes `coding-harness-5v6t`; its last commit carries `Closes-Bead: coding-harness-5v6t`.
- Special runs: none.

## Open decisions

- [DETAIL] Retain the commit's recorded offset as the shared day source: the checker already promises it, so existing history keeps its meaning. A checkpoint must bind its stamp to its own commit day, not merely read the same clock at two different instants.
- None open.
