---
title: "Decisions — codex-drafts"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-rhq
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, codex]
---

# Codex drafts spec and plan — Decisions

Phase 1a for bead coding-harness-rhq, on 2026-10-12, after the exploration in
`research.md`. Phases 2, 2b and 3 are drafted by Codex instead of Opus 5.5 to
save Claude tokens; so that Codex does not review what it drafted, a Claude
model reviews the spec.

## Q-1 · Which review phases move to a Claude model

asked: 2026-10-12
answer: A — the spec review (phase 2a) only; Codex stays the phase-6 code reviewer, since the code comes from GLM and Codex reviews nothing of its own there.
answered_by: maintainer
status: answered

In the context of Codex drafting spec, design and plan, facing the choice
between moving phase 2a alone or phases 2a and 6 to a Claude reviewer, we
decided on phase 2a alone to achieve that no model reviews its own draft
while Codex keeps the code review it is independent for, accepting that
Codex now appears on both sides of the change: author of the spec, reviewer
of the code. — 2026-10-12 (recorded on the bead the same day)

## Q-2 · Which Claude model reviews the spec

asked: 2026-10-12
answer: A — Opus 5.5.
answered_by: maintainer
status: answered

In the context of the spec review as the one safeguard against errors in a
Codex draft, facing the choice between Opus 5.5, Sonnet 5.5 and Haiku 4.5, we
decided on Opus 5.5 to achieve the strongest review where it matters most,
accepting that the review keeps costing Opus tokens — a fraction of what the
drafting costs today. — 2026-10-12

## Q-3 · How Codex writes its draft

asked: 2026-10-12
answer: A — a new runner verb (for example `scripts/stage2.py draft <change>`) starts Codex with write access; the runner then allows changes only inside the change folder plus an ADR draft, restores everything else, runs `make verify` and makes one commit — the guards of `implement`.
answered_by: maintainer
status: answered

In the context of a Codex that can only read when the runner calls it today,
facing the choice between a writing runner verb, the interactive session of
ADR 0012, and a read-only Codex whose text the runner writes, we decided on a
writing runner verb with `implement`'s guards to achieve drafts that also run
unattended (the night run), accepting that Codex writes without a human
watching for the first time. — 2026-10-12

## Q-4 · How a Codex draft is checked before it goes on

asked: 2026-10-12
answer: B — `make verify` with every gate, the Opus spec review, and the plan card shown unchanged to the maintainer — and in addition the orchestrating session reads the whole draft before the review.
answered_by: maintainer
status: answered

In the context of a draft whose errors only the gates, the review and the
maintainer's veto would catch, facing the choice between those three alone,
an added full read by the orchestrator, and an added Opus plan review, we
decided on the added full read by the orchestrator to achieve a Claude check
of design and plan too, accepting that it spends part of the token saving. —
2026-10-12

## Q-5 · What happens when the Codex draft fails

asked: 2026-10-12
answer: B — the fallback is GLM 5.3 instead of Opus.
answered_by: maintainer
status: answered

In the context of a Codex draft that fails (Codex unreachable, its limit
reached, or `make verify` red after the draft), facing the choice between
falling back to the Opus `spec-planner`, to GLM 5.3, or to no fallback, we
decided on GLM 5.3 to achieve that the drafting stays off Claude tokens even
when Codex fails, accepting that GLM has never drafted a spec here and its
risk is unknown. — 2026-10-12

Reading of the answer, stated to the maintainer on 2026-10-12: option B
replaces the Opus step of option A, so the sequence is one Codex attempt, one
Codex repair attempt with the diagnostics, then GLM 5.3; the fallback and its
reason are recorded as for `implement`.

## Decisions taken by the agent

[DETAIL] Class `feature` with an ADR (the reviewer roles of ADR 0007 and ADR
0011 are a maintainer decision): five answered questions meet the minimum.
The ADR number is the next free one after the open drafts (0014 for change
adr-owning-change, 0015 for change stage2-repair).

[DETAIL] The ADR answer of a drafted change is still recorded only by the
orchestrating session, from the maintainer's stated answer in
`decisions.md` (`scripts/harness.py decide adr … --stated-in …`); a drafting
model never records one.
