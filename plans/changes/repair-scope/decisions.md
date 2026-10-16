---
title: "Decisions — repair-scope"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-t83
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# repair-scope — Decisions

## SKIP · interview

status: skipped
reason: A bounded fix whose requirement the bead already states (coding-harness-t83: the repair prompt forbids handover and journal files, and the post-run check puts back or refuses new files outside the change's scope). The maintainer pre-approved the night merge of this bead's pull request on 2026-10-15 under two conditions (no open BLOCKER after the phase-6 Opus review, green CI). What stays open is mechanics, decided below as details with their reasons.

## Details the orchestrating session decides

These are `[DETAIL]` items (the agent decides and writes its reason down);
none of them changes a decision of record.

1. **Put back, not refuse.** Before `make verify`, the runner puts back to
   the baseline every path a repair or implement attempt changed in a
   denied area and names each path in `findings.md`, in the form the draft
   already uses (`put_back`, `put_back_lines`); the attempt's other work
   stays and is verified. Reason: the draft's put-back is measured and
   tested, and a refusal would throw away a correct repair for one stray
   file.
2. **A deny list, not an allow list.** A repair may rightly touch any code,
   test or doctrine file, so an allow list cannot be written. The denied
   areas: `docs/journal/**` (handovers and journal entries), every change
   folder under `plans/changes/` other than the change's own, `.beads/**`,
   `.claude/**`, `decisions/**`, `docs/adr/**`, `AGENTS.md`, and the change's
   own `decisions.md`. The runner's own writes (`plans/INDEX.md`, `updated:`
   stamps, ruff rewrites, the `plan.md` route block, `findings.md` Status
   cells) happen after the put-back or are outside the denied areas, and
   stay. Reason: each denied area is either the orchestrator's (handover,
   tracker, settings, decisions, ADRs, other changes) or a governance file a
   model must not change in passing.
3. **The same scope for `implement`.** Both verbs share `run_attempts` and
   the `git add -A` checkpoint, and the research shows the same gap. Reason:
   one guard in the shared loop closes both.
4. **The prompts say it.** `REPAIR_FORMAT`, `REPAIR_FORMAT_FILE_TOOLS` and the
   implement prompt name the denied areas in one sentence and say that the
   orchestrating session writes handovers; `prompts/04-implement.md`'s two
   handover mentions say "the orchestrating session's handover". `AGENTS.md`
   stays untouched: the rule binds the runner's calls, not every session.
   Reason: the embedded house rule 5 is what taught the model to write a
   handover; a prompt sentence answers it where it is read.
