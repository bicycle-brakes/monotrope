---
title: "Decisions — touch-map"
status: draft
implementation_status: partial
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

## [DECISION] 1 — the class of this change (answered 2026-10-06: feature, ADR "no")

`feature` or `bounded`. Recommendation: `feature`, with the ADR proposal
"no"; decision 1 above is that answer in substance, if the maintainer says
so in one sentence. Full question: `research.md`, section 4.7.

## [DECISION] 2 — the lower bound for the map (answered 2026-10-06: every code pull request)

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

## Addendum 2026-10-06: the maintainer's answers to [DECISION] 1 and 2

Asked one at a time in the Claude Code session on 2026-10-06:

1. **Class `feature`, ADR question: no** (the recommended option: a
   pull-request convention, not an architecture decision; ADR 0009 stays
   unchanged). Recorded with `scripts/harness.py decide adr`.
2. **The map in every code pull request** that has at least one link (the
   recommended option); from 15 boxes the section says "consider
   splitting", above 30 boxes only the list is printed. Not chosen: a map
   only from three changed code files on.

## Addendum 2026-10-06 (repair round 1): the maintainer's answer to the `[AMBIGUITY]` F-3

Raised by the phase-6 review (`findings.md`, F-3) and answered by the
maintainer in the Claude Code session of 2026-10-06.

- **Question:** does a runner or shell script that names another runner make a
  link? Read as plain English, `reads` ("names any other file") covers a
  runner, so `Makefile` naming `decisions/gates.yaml` would read it; read as
  the defined term "other" (a file that is no code file, test or runner), it
  does not.
- **Answer, as stated: "Kein Pfeil"** (no arrow) — the recommended reading,
  as built in phase 4. A runner or shell script that names a runner makes no
  link. No code changes; `spec.md` gains the clause as a dated amendment
  (terms, "Link", and "Amendments" at the end).
