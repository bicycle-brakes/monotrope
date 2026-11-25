---
title: "Decisions — adr-0021-consumed-ladder"
category: decisions
status: draft
implementation_status: none
date: 2026-11-20
created: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-hwll
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: antigravity, version: "2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, adr, review-loop, stage-2]
---

# adr-0021-consumed-ladder — Decisions

Class: bounded, claiming `docs/adr/0021-review-swarms-until-clean.md` under `adr_files` (bead `coding-harness-hwll`; five maintainer-answered records owed by `interview-minimums` — `Q-1` through `Q-5` below).

## Q-1 · How the runner carries the rule "an exhausted ladder goes to phase 6"

asked: 2026-11-20
answer: "Ja" — to the orchestrator's proposal, after the maintainer asked for the smartest solution: at an exhausted ladder `review-loop` ends as a normal result (exit 0), not a refusal, and prints one fixed line, `next: review <change>` when every taken row of the last round is fixed and `next: repair <change>` while a taken row is open; `review-loop` does not start phase 6 itself.
answered_by: maintainer
status: answered
context: |
  Topic: the AGENTS.md rule "An exhausted review ladder goes to phase 6" (maintainer, 2026-11-20, PR #419), carried by the runner (bead coding-harness-hwll).
  Intention: house rule 9 — a rule takes hold through code, not prose. On 2026-11-19/20 the refusal of an exhausted ladder stopped the slip-counter and findings-per-model lanes until the orchestrator applied the rule by hand.
  Today: when every stage of a run is consumed and the last round was not clean, `review-loop` refuses and says the loop stops and reports to the maintainer.
  Repository change: `scripts/stage2.py` (the exhausted-ladder branch of `review-loop`) and its tests; the doctrine sentence in `docs/WORKFLOW.md` if it names the refusal.
  Architecture change: none — no new route; the runner names the next verb, the session runs it.

In the context of review-loop runs whose ladder is consumed before a clean round, facing lanes that stopped overnight because the refusal named no next step, we decided that review-loop ends with exit 0 and one fixed `next:` line naming `review` or `repair` for the change, and does not start phase 6 itself, to achieve that any session — and the night-run wake — follows the rule mechanically, accepting that the session still starts the named verb. — 2026-11-20

## Q-2 · ADR 0021 decision 7 and the new next-step line

asked: 2026-11-20
answer: "Ergänzung zu ADR 0021 (Recommended)" — decision 7's "exhausting eligible stages with accepted findings also stops and reports to the maintainer" is amended by a decision pull request of its own: a consumed ladder whose taken rows are repaired goes to phase 6, one with open taken rows to the repair; the repair brake (two rounds of repair-caused findings) stays. This change merges after that amendment.
answered_by: maintainer
status: answered
context: |
  Topic: spec-review row S-4 of `ladder-next-step`.
  Intention: ADR 0021 decision 7 and the behaviour of this change contradict each other; an agent may not edit an ADR without a decision PR.
  Today: the ADR is unchanged; AGENTS.md (PR #419) already states the new rule.
  Repository change: a decide(...) pull request amending ADR 0021, drafted by the orchestrator, merged by the maintainer.
  Architecture change: when the review loop escalates to the maintainer.

In the context of an ADR that still escalates every consumed ladder to the maintainer, facing a runner that will name the next step instead, we decided to amend ADR 0021 decision 7 in a decision pull request of its own and merge the runner change after it, to achieve that ADR and code agree, accepting one more pull request. — 2026-11-20

## Q-3 · The AGENTS.md rule after the change

asked: 2026-11-20
answer: "Ja, im hwll-PR (Recommended)" — the AGENTS.md bullet "An exhausted review ladder goes to phase 6" is reworded in `ladder-next-step`'s pull request to: "when every stage of a `review-loop` run is consumed and the last round was not clean, the runner names the next step: `next: review <change>` once every taken row of that round is repaired, `next: repair <change>` before; phase 6 checks that last repair."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review row S-5 of `ladder-next-step`.
  Intention: the rule must name the state the runner reports, not a refusal that no longer happens.
  Today: the bullet begins "when `review-loop` refuses because every stage … is consumed".
  Repository change: one bullet of AGENTS.md, in the `ladder-next-step` pull request.
  Architecture change: none.

In the context of an AGENTS.md rule worded around a refusal, facing a runner that will end with exit 0 and a next-step line, we decided to reword the rule in the `ladder-next-step` pull request, to achieve one statement in rule and runner, accepting a held file in the change's diff. — 2026-11-20

## Q-4 · Minimum completed rounds before a consumed ladder names `next: review`

asked: 2026-11-20
answer: "Option 1" — at least one completed review round in the run is required before a consumed ladder names `next: review <change>`; when zero rounds completed (total stage outage), the loop still stops and reports to the maintainer.
answered_by: maintainer
status: answered
context: |
  Topic: minimum precondition for `next: review <change>` when review-loop stages failed or were retired with `--stage-failed`.
  Intention: define the safety floor for ADR 0021 decision 7 so single-model failures do not stall night runs while a complete OpenCode Go outage cannot silently skip phase 4b.
  Today: the draft amendment in PR #422 says only "when every eligible stage of a run is consumed" without distinguishing partial failures from a zero-round outage.
  Repository change: state the one-completed-round floor in `docs/adr/0021-review-swarms-until-clean.md` and implement it in `ladder-next-step` (bead `coding-harness-hwll`).
  Architecture change: defines when phase 4b may hand off to phase 6 without maintainer escalation.

In the context of amending ADR 0021 decision 7 for a consumed review ladder, facing both occasional per-stage failures (`--stage-failed`, timeouts) and the risk of a total provider outage, we decided to require at least one completed review round before naming `next: review <change>` and to keep stopping for the maintainer when zero rounds completed, to achieve unattended recovery from individual model failures without silently bypassing phase 4b on a total outage, accepting that a total outage still requires maintainer intervention. — 2026-11-20

## Q-5 · Consumed ladder when the review-loop diff was cut at the line bound

asked: 2026-11-20
answer: "Option 1" — `next: review <change>` also applies at a consumed ladder when the review-loop diff was cut at `REVIEW_DIFF_MAX_LINES`, because phase 6 (Codex) reads the complete diff in the worktree without a 2,000-line cut.
answered_by: maintainer
status: answered
context: |
  Topic: behaviour of a consumed review ladder in ADR 0021 when the prompt diff was cut at the 2,000-line bound.
  Intention: larger lanes (such as `finder-partial-report` and `runner-stamps-provenance`) exceed 2,000 diff lines and therefore run to the end of the ladder even after clean rounds; ADR 0021 must state whether they advance to phase 6 or stop for the maintainer.
  Today: ADR 0021 states only that a clean round over a cut diff does not end the loop early, and is silent on what happens once every stage is consumed.
  Repository change: record the cut-diff handoff rule in `docs/adr/0021-review-swarms-until-clean.md` and `decisions.md` so `ladder-next-step` applies one consistent rule until diff splitting (bead `coding-harness-hchx`) lands.
  Architecture change: clarifies that large changes with cut loop diffs advance to full-diff phase-6 review rather than stalling overnight at an exhausted ladder.

In the context of larger changes whose review-loop prompt diff is cut at `REVIEW_DIFF_MAX_LINES`, facing ladders that therefore consume every stage even on clean rounds, we decided that a consumed ladder still names `next: review <change>` once every taken row is fixed because phase-6 Codex reads the full diff in the worktree, to achieve uninterrupted handoff of large lanes until diff splitting (`coding-harness-hchx`) lands, accepting that the uncut review of lines past the bound happens in phase 6 rather than in phase 4b. — 2026-11-20
