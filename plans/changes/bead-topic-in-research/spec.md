---
title: "Spec — bead-topic-in-research"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5vts
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research]
class: bounded
appetite: 2
adr_files: []
---

# Spec — bead-topic-in-research

A new change's research skeleton carries its tracker description so an explorer can read the intended topic (bead `coding-harness-5vts`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-25 an explorer guessed the topic from the change name and had to run again; later descriptions were copied by hand (`research.md`, topic).
- At commit `077519cd`, change creation reads tracker status but its research skeleton contains no description (`research.md`, runner exploration).

## Acceptance criteria

1. When a change is created for an existing open bead with a non-empty description, its research skeleton contains that description under `## Topic (bead <id>)` below the research title.
   *Refuted by:* the heading identifies another bead, is absent, or the description differs from the tracker text.
2. When the bead description is absent, empty or whitespace-only, the topic section explicitly says the description is missing or empty.
   *Refuted by:* the section is absent, contains an invented description, or does not name the missing or empty description.
3. When change creation is run with `--dry-run`, its research preview contains the same topic section that creation would write.
   *Refuted by:* the preview omits or changes the topic for the same tracker record.
4. When exploration publishes research from a generated skeleton, the topic section and its description remain in the published research.
   *Refuted by:* publication removes or changes the topic section.
5. When exploration publishes research from a generated skeleton, the generated opening notices are removed as before.
   *Refuted by:* either generated opening notice remains after publication.
6. When the bead export is missing, the bead is absent, or the bead is closed, change creation retains its existing refusal.
   *Refuted by:* any such case creates a change or no longer reports the refusal.

## Non-goals

- Backfilling or correcting existing research files or tracker descriptions.
- Changing tracker creation, export, access permissions, or exploration model routing.

## Protected areas

The tracker and its renderer remain unchanged: this change consumes the existing export. No ADR is changed.

## Definition of Done

- `make verify` green.
- Documents, models and ADRs moved with the code: none beyond this change's artifacts.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes `coding-harness-5vts`, and its last commit carries `Closes-Bead: coding-harness-5vts`.
- Special runs: none.

## Open decisions

- [DETAIL] Place generated notices before the topic section: the existing publication boundary removes notices before the first section, preserving the topic without making it a notice.
- [DETAIL] Use an explicit missing-or-empty message for absent, empty and whitespace-only descriptions; the exact wording is revisable and must not invent a topic.

[DETAIL] Spec-review S-1..S-3 (round 1, decided by the orchestrator under the bounded standing grant, 2026-11-28): S-1 — the description is written as a Markdown blockquote (every line prefixed with `> `, blank lines as `>`), so no fence, heading or runner line in it can change the structure of `research.md` or hide later lines from `stage2.research_visible_text`; a test plants an unclosed fence and a `Stage-2 call` line in a description. S-2 reading A — every status other than `closed` gets the topic section, matching AC6. S-3 — the text comes from the `description` key of the bead's row in the rendered tracker export only (no design, acceptance or notes fields); a row without that key, or with an empty value, is named in the section ("the tracker export holds no description for <id>"), never invented.
