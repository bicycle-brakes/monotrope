---
title: "Session handover — AGENTS.md is the only instruction file, ADRs 0001–0003 accepted, Omnigent-first target merged, 2026-09-22"
category: handover
created: 2026-09-22
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-22"
tags: [handover, instructions, adr, omnigent, signing, beads]
target_ref: "998dc3b"
bead: coding-harness-36z
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

This is the second handover of 2026-09-22. The first
(`docs/journal/handover/2026-09-22-export-stage-1-and-interview-d49-d54.md`)
stays as it is; its "needed from the maintainer" list is now half done.

## Where we are

`main` (`998dc3b`) carries three things this session finished: `CLAUDE.md`
is gone and `AGENTS.md` is the only instruction file (pull request #23); the
three amendment ADRs are accepted by the maintainer with review changes and
merged (pull request #12 into #8, then #8 into `main`, which also brought the
Omnigent-first target document and the "Communication and session
continuity" section into `AGENTS.md`); and the maintainer signs Git commits
with an SSH key since today. A second session started this afternoon on the
bug chain the maintainer decided on (scaffold guard, floor gates, session
scan, placeholder owner and agent definitions); it owns the tracker while it
runs. `make verify` is green on `main`.

## Next step

In lakeswitch-ai, prepare the ratification file for cluster 7 (foundation
and tracker: D-45, D-46, D-47, D-48, D-52) as a proposal the maintainer
writes `accept`/`reject`/`amend` into — the first step of that repository's
journal `journal/2026-09-22-decision-interview-d45-d54-and-ratification.md`.
Check for a parallel session there before writing. This session was about to
start it when the handover was written.

## Needed from the maintainer

1. **lakeswitch-ai, `decisions/provenance.yaml`:** admit `plans/` and the
   class `ai-drafted`. Until then the provenance-coverage gate keeps pull
   request #37 red. Only you may edit that file; a session will lay the two
   lines in front of you.
2. **portfolio-agentic-engineering pull request #164** ("point to the
   harness rules for working with the maintainer") is mergeable now that #8
   is on `main`. Not read this session whether its text is still current —
   read once, then merge.
3. **Bug chain, decided today:** for the floor gate `export-identity` you
   chose option A (install the pinned `bd` in CI, fetch `refs/dolt/data`,
   render for real) and for the agent definitions option (a) (rewrite them
   process-generic, keep the RB-A1 clause byte-equal). Both were handed to
   the second session together with one addition: house rule 4 must state
   the order "push the tracker, then push Git", because option A turns a
   forgotten `tools/bd dolt push` into a red CI. Nothing more is needed from
   you on this.

## Decisions and preferences

Decided today, in session, by the maintainer. Not asked again.

- **No `CLAUDE.md`.** `AGENTS.md` is the only instruction file; Claude Code
  reads it itself since 2.1.277 when no `CLAUDE.md` is in the tree
  (verified 2026-09-22 with a fresh `claude -p` session, Claude Code
  2.1.278). A `CLAUDE.md` beside it would silently replace it;
  `tests/test_entry_points.py` forbids one. Known limit, recorded in the
  target architecture (H6) and `docs/WORKFLOW.md`: the direct read is a
  feature flag and is unavailable with telemetry off, on Bedrock/Vertex or
  with a custom base URL — to be proved before Omnigent M0, which runs with
  telemetry off. This went beyond the bead (`coding-harness-21f`), which
  asked for an `@AGENTS.md` import plus addendum.
- **ADR 0001–0003 accepted with review changes** (commit `8ec902e`, on
  `main` through #12 and #8). The changes: the decider is the maintainer, a
  framework-architect session prepared the text; 0001 says what really
  changes (M0's content becomes two coordinated workers, D-3's two-worker
  condition moves to M0) and announces the missing W0/W1 enforcer bead;
  0002's lock sentence is unambiguous and the tracker export stays with the
  one writer; 0003 names the narrowing of D-17's "vendor names" to
  vendor-internal identifiers and becomes a denylist of explicit patterns
  with an exception allowlist — a two-entry tool allowlist would have
  rejected the harness's own pages.
- **Commit signing:** SSH key `~/.ssh/id_ed25519`, registered at GitHub as a
  signing key, `commit.gpgsign true` globally, `allowed_signers` with both
  addresses. Software key, not hardware-backed: any process with the agent
  loaded signs, so a signature alone does not prove "maintainer, not a
  session". The global `user.email` was the placeholder
  `<deine commit-adresse>` until today — the same placeholder the tracker
  bug `coding-harness-xcy` reports.
- **Subagents run on Opus** — every Agent call from a Claude Code session
  carries `model: opus` (maintainer's instruction, 2026-09-22).
- **Bead ids never stand alone** — the maintainer needs the title or a short
  description at every mention, including the closing line of a message.
  Already in the maintainer's user file and in house rule 7; this session
  broke it once.

How the maintainer wants questions put is unchanged from the first handover
of today: one at a time, plain words, alternatives and a recommendation.
Today "explain it in simple words" was asked once after a dense review —
the plain version was the one that led to the decision.

## Open work and blockers

Task status lives in Beads; this list only points.

- New today: enforcers for W0 (isolated worktrees) and W1 (exclusive
  coordinator writer) before any parallel run (`coding-harness-36z`, P1),
  blocked by the worktree write verification (`coding-harness-m34`). This
  is the path to Omnigent M0.
- Closed today: the `CLAUDE.md` import bead (`coding-harness-21f`, merged as
  #23) and the amendment ADRs (`coding-harness-nkr`, merged as #12/#8).
- Claimed by nobody at the time of writing, being worked by the second
  session in this order: scaffold guard script missing
  (`coding-harness-cke`), floor gates passing without measuring
  (`coding-harness-4t8`), session scan dropping sessions
  (`coding-harness-hit`), placeholder owner (`coding-harness-xcy`) and
  agent definitions with instance content (`coding-harness-rqc`). The
  session scan bug is what hid the second session from this one today.
- Tracker export stage 3 (`coding-harness-1jg.3`) likely gets its two
  hosted-runner measurements from option A of `4t8` — not read whether the
  bead means exactly that.
- Unchanged from the previous handover: stage 2 of the tracker export
  (`coding-harness-1jg.2`), the M1 template bundle (`coding-harness-9qo`),
  and the ratification work in lakeswitch-ai.

## Working state and parallel-session boundary

- This file arrives on branch `docs/handover-2026-09-22-agents-md-and-adrs`
  from `main` at `998dc3b`; nothing else is on it.
- Pull requests merged today: #23 (`166e4c3`), #12 (`cd20d79`, into #8's
  branch), #8 (`203b895`). Two direct commits on `main` render the export
  after tracker writes (`2c45758`, `998dc3b`); the tracker was pushed to the
  Dolt remote after each write. Pull request #12's branch was rebased once
  onto the rebased #8 (old tip `67d6f5c` → `8ec902e`, ADR content
  byte-identical, `--force-with-lease`), because #8 had been rebased onto
  `main` meanwhile.
- No open pull request in this repository at the time of writing. Worktrees:
  `~/coding-harness-wt-claude-code` (pull request #10, merged — can be
  removed); the two temporary worktrees of this session were removed.
- **Second session:** the session scan reports one other session
  (`tmp-7a`, working, under `/private/tmp`, not this checkout). It owns the
  tracker while it runs; this session made no tracker write after handing
  the bug-chain decisions over. Do not write to Beads until it has ended.
- Merges by a session are blocked by the Claude Code permission layer
  ("merge without review"); the maintainer merged #23, #12 and #8 by hand.
  #8 needed the asynchronous merge endpoint
  (`gh api -X PUT repos/…/pulls/8/merge-async -f merge_method=merge`)
  because GitHub treated it as a stack with #12.
- Not read: the full research document of lakeswitch-ai pull request #37;
  portfolio #164's text; whether the Beads Dolt documentation link in
  ADR 0002 is reachable.

## Validation

- 2026-09-22, `main` at `998dc3b`: `make verify` VERIFY GREEN — 279 passed,
  15 skipped; `decision-continuity` reports all 21 ids mapped and every
  amendment ADR present (its skip clause for the absent target document is
  now dead code, part of `coding-harness-4t8`).
- 2026-09-22, worktree at `05fb0d3` (pull request #23): VERIFY GREEN — 277
  passed, 15 skipped; the two report-only gates showed the same 23 dead
  links as `main`, none in a changed file; a fresh `claude -p` session in
  the worktree reported exactly `AGENTS.md` loaded.
- 2026-09-22, pull request #12's branch (`8ec902e`): 64 failed, 185 passed,
  4 skipped — identical before and after the ADR changes; the branch
  predates the gate stack and the 2ee triage, so this is the known pre-triage
  set, not a regression. CI on #8 after the merge of #12: `verify` green.
- 2026-09-22, merge of #8 into `main` simulated with `git merge-tree` before
  the maintainer merged: no conflict, `AGENTS.md` keeps the "only
  instruction file" paragraph and gains the communication section, 124
  lines, export file unchanged.
- 2026-09-22: signing verified twice with `git log --show-signature` on
  throwaway commits (`Good "git" signature`); the signing key is listed at
  GitHub.
- Not run: anything in lakeswitch-ai; anything under Python 3.11.
