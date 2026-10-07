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

## Spec-review decision — start-success boundary (answered)

Source: phase-2a finding F-2, 2026-10-07. Asked once through the user-input
question. The maintainer subsequently replied "mach weiter" directly after
the recommendation and confirmation question (2026-10-07). This is recorded
as assent to option 1, not a new decision made by the agent.

Goal in one sentence: make the returned launch status tell the maintainer
exactly what has been confirmed.

Options:
1. Terminal accepted the start request after the runner checked the CLI
   prerequisite. Later login/model/start errors appear in the new window.
   The runner returns promptly and does not supervise the interactive session.
2. Require a separate program-start acknowledgment before returning success.
   The runner must supervise that acknowledgment and fail on a bounded timeout;
   it still cannot prove login or a successful model answer.

Recommendation: option 1, because the maintainer asked for an independent
interactive window, and success can explicitly mean dispatch rather than a
completed model call.

If accepted: distinguish missing-program preflight refusal, failed Terminal
dispatch and accepted dispatch in help, audit and tests.

What is lost: immediate confirmation that the selected CLI actually started
after Terminal accepted the command.

Answer: "mach weiter" (maintainer, 2026-10-07), accepting the immediately
preceding recommendation: Terminal acceptance after CLI prerequisite checks.
The session is not supervised for program-start acknowledgment or model success.

## Further reversible details for the plan

- [DETAIL] A helper module holds interactive launch mechanics; the sole public
  model entry stays `scripts/stage2.py`, avoiding reviewer-migration overlap.
- [DETAIL] Runtime policy files live in a fresh private directory under
  `.stage2-sessions/` in the worktree. Failed preparation removes only that
  directory; accepted dispatch retains it for the new CLI to load. No keys.
- [DETAIL] OpenCode uses a dedicated primary agent and no external plugins.
  Effective permission diagnostics are checked before dispatch. Subagents are
  denied initially to avoid bypassing the checked primary agent.
- [DETAIL] Initial prompts are capped at 32 KiB UTF-8, complete shell dispatch
  commands at 64 KiB: refuse oversized arguments before GUI dispatch.

## Implementation route after the unanswered attempt

Maintainer, 2026-10-07: "kannst du mit glm implementieren?" following the
offer of direct Codex implementation or another GLM attempt. Continue with
the existing GLM Flash runner route, not a direct Codex implementation.
This requests another attempt; it is not evidence that the endpoint works.
Keep declaration/leak checks, post-run gates, review phases and no-merge rule.
