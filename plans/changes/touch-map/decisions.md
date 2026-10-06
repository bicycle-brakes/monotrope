---
title: "Decisions — touch-map"
status: draft
implementation_status: none
date: 2026-10-06
last_reviewed: 2026-10-06
updated: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-5p0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# touch-map — Decisions

Phase 1a (interview) was skipped: the maintainer set the direction in the
Claude Code session of 2026-10-06, relayed to this phase by the orchestrating
session, and what stays open is two questions (below), each with a
recommendation in [`research.md`](research.md), section 4.

## What the maintainer decided on 2026-10-06 (Claude Code session)

1. **A pull request convention, not an amendment of ADR 0009.** The diagram
   becomes a rule for pull requests: one line in `prompts/07-commit.md` and a
   section in the pull request template. ADR 0009 (the architecture delta in
   `design.md`) is not amended. Chosen option: "PR-Regel", the recommended
   one of the two the bead named (bead coding-harness-5p0, "Open question for
   the maintainer").
2. **The request itself:** "a diagram of the module's code in every PR,
   following best practice, as a standard for PR reviews".

## [DECISION] 1 — the class of this change (open)

`feature` or `bounded`. Recommendation: `feature`, with the ADR proposal
"no"; decision 1 above is that answer in substance, if the maintainer says
so in one sentence. Full question: `research.md`, section 4.7.

## [DECISION] 2 — the lower bound for the map (open)

A map in every code pull request that has at least one link, or only from
three changed code files on (the research note's rule). Recommendation:
every code pull request, because that is what was asked for and the
collapsed block costs one line on the phone. Full question: `research.md`,
section 4.8.

## Decided by the agent ([DETAIL], reasons in `research.md`)

- What the script draws: path links and import edges combined, ADR 0009's
  form with a C4 level per box, three lists, caption (4.1).
- Recall rules: `/`-joined paths, tested non-code files, outward links of
  changed tests (4.2).
- Prose-only line; upper bound of 30 boxes with a split hint above 15 (4.3).
- One section "What it touches" right after "What changes", map collapsed
  inside it; the same section in the decision template (4.4).
- Script and test travel with the kit (`mechanismus`) (4.5).
