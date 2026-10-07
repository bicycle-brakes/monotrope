---
title: "Decisions — stage2-session"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-amp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, session]
---

# Decisions — stage2-session

## Settled maintainer instructions

Source: the takeover handover in PR #90 (`a3d5585`, 2026-10-07),
the notes of the shared bead, and the current takeover request. This record
does not turn the unmerged ADR amendment into accepted repository policy.

1. Extend the runner-only rule to interactive sessions. Keep declared
   endpoints and the clean leak check as prerequisites; no bypass verb.
2. Open a terminal in the change's own worktree with the chosen model and
   handover as its first prompt. Record date, model and leak-check counts
   in `findings.md`.
3. Deny outside-worktree reads in OpenCode as far as its configuration
   supports it; name the remaining limit. Check only the state at launch.
4. Use the existing endpoint declaration. OpenCode Go reviewer ordering
   is separate work, not another routing table in this verb.
5. Draft the ADR 0007 amendment in the change folder; do not edit
   `docs/adr/`. End in a decision PR and never merge.
6. Leave PR #89 and its branch untouched. Research/spec may proceed while
   it is open; implementation waits for its merge onto main.

## Reversible implementation details

- [DETAIL] Class `architectural`: interactive dispatch extends the trusted
  launch boundary and requires the ADR 0007 amendment already requested.
- [DETAIL] Default handover is `plans/changes/<change>/handover.md`; an
  explicit `--handover <path>` accepts an existing file inside the worktree,
  including `docs/journal/handover/`. Refuse a missing default rather than
  guessing relevance from a date or sending another change's handover.
- [DETAIL] Initial platform is macOS Terminal, matching this machine.
  Other platforms refuse before dispatch instead of silently running a
  background noninteractive job.
- [DETAIL] Pin the selected model and permission policy at launch, make no
  automatic fallback. A failed launch must not silently choose another
  endpoint.
- [DETAIL] The implementation appetite proposal is four hours including
  repairs. It is a stop boundary, not a promise of completion time.

None of these details authorizes a model call, merge or credential-file read
outside the takeover instructions.
