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

1. When a runner checkpoint commits a changed document with a runner-maintained `updated:` stamp, its stamp equals the checkpoint commit's calendar date in the commit's recorded offset.
   *Refuted by:* a stamp later than that date (S-11), or the checkpoint commits a runner-maintained stamp older than its own recorded day.
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

[DETAIL] Spec-review S-1..S-6 (round 1, decided by the orchestrator under the bounded standing grant, 2026-11-28): S-1 reading A — the runner takes one clock reading at the checkpoint and uses it for the stamp and for `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` of the checkpoint commit (with the local offset), so the recorded commit day and the stamp cannot differ. S-2 reading A — every held document the checkpoint changes is covered, also those the model edited. S-3 — the stamp equals the commit day exactly; a later `updated:` in a changed document is lowered to it (AC 3 governs over AC 1). S-4 — AC 5's failures are: a held document that is not valid UTF-8 (`CannotStamp`), one without frontmatter, and one with two `updated:` lines. S-5 — such a refusal raises `CheckpointRolledBack`, saves the attempt through `save_attempt`, counts as a failed attempt and names the file and the reason. S-6 — a stamp-only difference after verification is accepted; only the frontmatter-current gate runs again on the refreshed tree before the commit.

[DETAIL] Spec-review S-7..S-11 (round 2, orchestrator under the bounded standing grant, 2026-11-28): S-7 reading A — the gate rerun receives the checkpoint's own clock reading as `today` and `utc_today`; a red rerun is a refusal like AC 5 (`CheckpointRolledBack`, attempt saved). S-8 reading A — the refusal ends the run as every `CheckpointRolledBack` does today, no next route runs, and the attempt's already persisted time line is rewritten from `accepted` to `rejected`. S-9 — documents under a `human-decided` prefix are not refreshed (Protected areas governs); their own `updated:` stays as written. S-10 — `ClockReading` gains the local offset, computed in `clock_now()` from the same single read (the process time zone applied to `utc`), so no second raw clock read is added. S-11 — AC 1 now requires the stamp to equal the commit day, and a later stamp refutes it.

[DETAIL] Spec-review S-12..S-14 (round 3, fallback reviewer; orchestrator under the bounded standing grant, 2026-11-28): S-12 — a "runner-maintained stamp" is the `updated:` of a changed held document with `frontmatter: required` outside every `human-decided` prefix; AC 1 and AC 2 apply only to those, and human-decided documents keep their date as written (S-9). S-13 — `clock_now()` takes one raw reading, `dt.datetime.now(dt.UTC)`, and derives the local date and offset from it with the process time zone; the stamp reads that local date, the commit dates use that instant and offset. S-14 — only the work-loop caller of `checkpoint()` has an attempt: there a refusal saves the attempt and rewrites its time line; the other callers raise `CheckpointRolledBack` without either. Final draft after round 3; no fourth review.

[DETAIL] Correction of S-4 by the orchestrator (2026-11-28, after implement attempt 1 was rejected): S-4's refusal for a document "without frontmatter" applies only to documents S-12 calls runner-maintained (held, `frontmatter: required`, outside every `human-decided` prefix). Generated or frontmatter-free held files such as `plans/INDEX.md` are not stamped and never refuse a checkpoint. Attempt 1 refused every checkpoint on `plans/INDEX.md` for exactly this reason.
