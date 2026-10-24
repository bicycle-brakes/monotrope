---
title: "Spec — review-release-lock"
status: draft
implementation_status: partial
date: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-751
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, record-lock]
class: bounded
appetite: 1
adr_files: []
---

# Spec — review-release-lock

Phase-6 review respects exclusive ownership of its loop record from its
first read through release, preventing concurrent review and record changes
(bead coding-harness-751). Research: `research.md`. Decisions: `decisions.md`.

## Problem

The audit reproduced a held record lock refusing `release-loop` while
`review` still released and deleted the same record at `378879a`
(2026-10-21). Research confirms at `7586f1a7` (2026-10-24) that `review`
reads the record, invokes Codex, writes its verdict and calls `release`
without the lock used by the other record verbs. A concurrent operation can
therefore change the record between the undecided-row check and release.

## Terms

- **Record:** the temporary loop history for one change in one worktree.
- **Release:** append that history to `findings.md` after the phase-6 verdict,
  then remove the temporary record directory.

## Acceptance criteria

1. When another run holds the same record's lock, `review` refuses promptly
   with exit 2 and the existing record-contention diagnostic before any model call.
   *Refuted by:* waiting for the lock, another exit or diagnostic, or a model invocation.
2. When `review` refuses because the record lock is held, the record directory's
   contents and `findings.md` remain byte-for-byte unchanged, including their existence.
   *Refuted by:* a created, changed, moved or removed record file or findings file.
3. While `review` runs from its first record read through completion of release,
   another run cannot acquire the same record lock.
   *Refuted by:* a competing lock acquisition succeeding at the initial read,
   verdict call, verdict append or release, including after directory removal.
4. When the lock is free and the existing review prerequisites hold, `review`
   retains the verdict-before-release-and-marks flow, including the no-record path.
   *Refuted by:* refusal solely from the new locking, release before the verdict,
   missing or duplicated released rows, a retained record, changed verdict during
   marking, or failure of the no-record path.
5. When `review` returns successfully or exits with an existing refusal or call
   failure, its record lock is available to the next run.
   *Refuted by:* an independent nonblocking acquisition failing after that exit.

## Non-goals

- Change review-answer validation, reviewer selection, prompts or loop policy.
- Add waiting, retries, a new lock protocol, crash recovery or transactional release.
- Change the behavior of other record verbs or protect arbitrary direct edits
  to `findings.md` made outside the runner.
- Run phase 2b or create an ADR: the recorded class is bounded and the existing
  locking contract is being applied to its missing call site.

## Protected areas

Model endpoints, credentials, leak-check rules, governance decisions, ADRs and
other runner verbs stay unchanged because this fix concerns review's ownership
of the existing record only.

## Definition of Done

- Regression tests demonstrate contention refusal and unchanged evidence,
  continuous ownership, normal flow and release of the lock after exits.
- `PYTHON=.venv/bin/python3 make verify` is green.
- No living capability document, model configuration or ADR changes are needed.
- The pull request's file list demonstrates the protected areas and non-goals.
- The pull request closes the missing review-lock fix (bead coding-harness-751)
  and its last commit carries `Closes-Bead: coding-harness-751`.
- Special runs: none; tests use local stand-ins without model calls.

## Open decisions

None open.

- [DETAIL] Hold ownership before the first record read through release rather
  than acquiring it only at release: a late acquisition permits stale checks.
  Other record verbs refuse during the reviewer call, as they do during an
  existing locked loop run; this follows the research's named fix.
- [DETAIL] Use a one-hour phase-4 appetite including repairs, a stop rather
  than an estimate, because this is one missing lock boundary and its regressions.
