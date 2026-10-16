---
title: "Research — repair-scope"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-t83
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair]
---

# What a repair attempt may write — Research

Phase 1 for bead coding-harness-t83, seeded by the orchestrating session on
2026-10-16 against `origin/main` at `135f029`.

## The question

A Codex repair on the research swarm (2026-10-15) wrote its own handover file
`docs/journal/handover/2026-10-15-research-swarm-loop-one-repair.md` into the
branch; the orchestrating session removed it by hand (commit `560160d` on
`explore/research-swarm`). The `repair` verb of `scripts/stage2.py` tells the
model "Repair only the taken rows below" (`REPAIR_FORMAT`, around line 228)
but names no file it must not write, and its post-run checks neither put
back nor refuse a stray path. Needed (bead text): the repair prompt forbids
handover and journal files, and the post-run check puts back or refuses new
files outside the change's scope.

## Known so far (read, not run)

- `DRAFT_RULES` (around line 238) already says what a draft may write and
  that "the runner puts back every changed path outside the change folder";
  the draft verb has that put-back mechanism — find it and say whether the
  repair can reuse it.
- A repair legitimately changes code, tests, doctrine and the change's own
  `plan.md` (its `## Time used` entry); it must not edit `findings.md` beyond
  the runner's own Status writes (`REPAIR_ANSWER`).
- The embedded `prompts/04-implement.md` asks for a report and a `Resume:`
  line; whether it or another embedded prompt invites a handover file is not
  read yet.

## To explore

1. Where the draft's put-back lives, what it compares against (the baseline
   commit, the ignored-file snapshot), and what it reports.
2. What "outside the change's scope" can mean for a repair, which may touch
   any code or test file: a deny list (`docs/journal/**`, handover files,
   `.beads/**`, other change folders, `AGENTS.md`, settings) versus an allow
   list, and which the existing checks already cover (the implement verb's
   pre-existing-change refusal, `ignored_snapshot`).
3. Which prompts embedded in the repair prompt mention handovers, journals or
   session notes, and how the session-handover rules of `AGENTS.md` reach a
   Codex repair at all.
4. The same question for `implement`: does an implement attempt have the
   same gap?
5. Which tests cover the draft's put-back, so the repair's can follow them.
