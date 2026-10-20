---
title: "Decisions — review-loop-row-ids"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-6jg
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# review-loop-row-ids — Decisions

Class: bounded (one interview answer owed; it is given below).

## Q-1 — Refuse or renumber?

- **Topic:** a review-loop round whose member answers in row-shaped lines
  that the runner cannot read as findings.
- **Why now:** the night run of 2026-10-15 lost a real finding this way; the
  runner reported a clean round.
- **Today:** the round was counted clean and the loop ended.
- **Repository change:** the runner's handling of malformed member answers.
- **Architecture change:** none; ADR 0021's rule for a clean round stays.

Question: should such a round refuse and name the lines, or renumber them?

**Answer (maintainer, 2026-10-16, in conversation, recorded in bead
coding-harness-6jg):** "(a) refuse — a round whose answer holds row-shaped
lines with non-conforming ids fails, and the refusal names the ids; no
renumbering."

Reading for this change (orchestrator, 2026-10-20): the runner has since
assigned loop ids to every valid six-cell row itself (`6e3df16`), so the
answer applies to malformed answers: a member answer with row-shaped lines
but no readable row refuses the round and names the member and the lines.
The maintainer confirms this reading when reading the plan card.
