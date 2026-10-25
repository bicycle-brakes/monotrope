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

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · Refuse or renumber malformed review-loop rows

context: |
  Topic: a review-loop round whose member answers in row-shaped lines the
  runner cannot read as findings.
  Intention: the night run of 2026-10-15 lost a real finding this way; the
  runner reported a clean round and the loop ended.
  Today: the round counted as clean.
  Repository change: how the runner treats a malformed member answer.
  Architecture change: none; ADR 0021's rule for a clean round stays.
asked: 2026-10-16, the night-run conversation (recorded in bead coding-harness-6jg)
answer: (a) refuse — a round whose answer holds row-shaped lines with
  non-conforming ids fails, and the refusal names the ids; no renumbering
answered_by: maintainer
status: answered

In the context of a review-loop round whose member answers in lines the
runner cannot read as rows, facing a choice between refusing and
renumbering, we decided to refuse and name what could not be read, to
achieve a loop that never ends on a silently dropped finding, accepting that
such a round needs a rerun or a person. — 2026-10-20

Reading for this change (orchestrator, 2026-10-20): since the loop rewrite
(`6e3df16`) the runner assigns loop ids to every valid six-cell row itself,
so the answer applies to malformed answers: a member answer with row-shaped
lines but no readable row refuses the round and names the member and its
lines. The maintainer confirms this reading when reading the plan card.

Confirmed by the maintainer on 2026-10-20 after reading the plan card: "ja"
to this reading.
