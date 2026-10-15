---
title: "Decisions — repair-fixed-lines"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-ugi
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# repair-fixed-lines — Decisions

## SKIP · interview

status: skipped
reason: A bounded bug fix whose requirement the bead already states (coding-harness-ugi: rows already repaired are not demanded again, and only lines whose id is a taken row's id count). The maintainer pre-approved the night merge of this bead's pull request on 2026-10-15 under two conditions (no open BLOCKER after the phase-6 Opus review, green CI). What stays open is mechanics, decided below as details with their reasons.

## Details the orchestrating session decides

These are `[DETAIL]` items (the agent decides and writes its reason down);
none of them changes a decision of record.

1. **Which answer lines count.** A line counts as a fixed line when its left
   part (before the first colon) is the id of a taken row. A line whose left
   part has the shape of a finding id — `L<n>-<m>` (`LOOP_ID`) or letters, a
   hyphen and digits such as `F-12` — but names no taken row still fails the
   attempt with `<id>: no taken row carries this id`, so a mistyped id is
   caught as today (criterion 15 of `plans/changes/stage2-repair/spec.md`).
   Every other line is ignored. Reason: the repair prompt embeds
   `prompts/04-implement.md`, which itself asks for the report lines
   `expected:`, `found:`, `relevant:`, `proposal:` and a closing `Resume:`;
   both recorded failures (haiku-5-5 and pi-pin, 2026-10-15) were exactly
   these words. A taken row without its fixed line still fails with
   `<ID>: no fixed line`, so an answer of prose alone is never clean.
2. **How a hand repair is recorded.** A row the orchestrating session repairs
   by hand gets the Status form the runner writes itself:
   `fixed — tests/<path>::<function>` or `fixed — not a test — <reason>`,
   with its `Broke a test` mark. `repair_targets` already skips a Status
   that begins `fixed`. Before any call, the runner refuses when a taken
   row's Status already names a fix (`; fixed by` or `; fixed:` after the
   `taken — …` part), names the row and the form to write, so the old form
   is caught at once instead of failing an attempt after `make verify`.
   Reason: one form for both writers, and no new status vocabulary. The
   records already merged with the old form (haiku-5-5, pi-pin) stay as they
   are; their repairs are complete.
3. **Where the rule is written.** `REPAIR_ANSWER` names both rules in one
   sentence each; `docs/WORKFLOW.md` §4 ("Repairing taken findings") states
   the hand-repair form. Reason: the prompt and the doctrine must agree with
   the parser.
