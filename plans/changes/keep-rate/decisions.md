---
title: "Decisions — keep-rate"
category: decisions
status: draft
implementation_status: none
date: 2026-11-03
created: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-363r.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, spike, measurement]
---

# keep-rate — Decisions

Class: spike (three topics owed: learning goal, time budget, expected
outcome). Interview held on 2026-11-03 through the interview tool, one
question per call. The phase-1 explore (GLM 5.3 Flash) read "keep rate" as the
share of taken review findings per reviewer; the bead means the share of lines
a runner route wrote that still stand on main. Q-1 keeps both.

## Q-1 · Learning goal

asked: 2026-11-03
answer: "Beides" — measure both: the share of lines each runner route (Flash implement, Codex repair, Sonnet fallback, hand repair) added that still stands on main, per route and model; and the share of review-loop findings taken per reviewer and stage.
answered_by: maintainer
status: answered
context: |
  Topic: what the keep-rate spike measures.
  Intention: the explore read the term differently from the bead.
  Today: the bead asks for surviving lines per route (git blame against attempt commits) and whether the ranking differs from the acceptance ranking (route-success note, bead coding-harness-hleu); the explore read it as taken findings per reviewer, whose data already stands in findings.md.
  Repository change: a note under docs/research/ in every option. Options: code lines as in the bead; both; review findings only.
  Architecture change: none.

In the context of a spike whose term the explore read differently from its bead, facing code lines, review findings or both, we decided to measure both, to achieve the value of the writing routes and of the reviewing ones side by side, accepting twice the work. — 2026-11-03

## Q-2 · Time budget

asked: 2026-11-03
answer: "4 Stunden" — four hours, a stop; at the limit the note says what was not measured.
answered_by: maintainer
status: answered
context: |
  Topic: the spike's time budget.
  Intention: a spike needs a fixed limit; with both measurements there are two parts.
  Today: the route-success spike took about two hours (scratchpad script, one note); counting findings is quick, git blame over every merged change since 2026-10-22 is the larger part.
  Repository change: one note under docs/research/; the script stays in the scratchpad. Options: 3, 2 or 4 hours.
  Architecture change: none.

In the context of a two-part measurement, facing a tight or a roomy limit, we decided on four hours, to achieve room for a clean method where refactors move lines, accepting a longer spike than its sibling. — 2026-11-03

## Q-3 · Expected outcome

asked: 2026-11-03
answer: "Jetzt + Messpunkt später" — now: the method and the values measurable today (no change merged since 2026-10-22 is 30 days old, and none is 14 days old before 2026-11-05); a follow-up bead (coding-harness-jf00, deferred to 2026-11-21) takes the 30-day point; the note recommends whether it becomes a recurring measurement.
answered_by: maintainer
status: answered
context: |
  Topic: what the spike delivers now, given that the 30-day point cannot be reached today.
  Intention: the bead wants 14- and 30-day values for changes merged since 2026-10-22; on 2026-11-03 no such change has its 30-day value.
  Today: nothing measured; acceptance per route stands in docs/research/2026-11-02-route-success.md.
  Repository change: a note under docs/research/ with method, numbers with their cut-off commit and a recommendation; a follow-up bead for the later point. Options: now plus a later point; move the window to 2026-10-01; wait until 2026-11-21.
  Architecture change: none.

In the context of a measurement whose windows are not yet reachable, facing waiting, an older window or a split, we decided to measure what is measurable now and take the 30-day point in a follow-up on 2026-11-21, to achieve a method and first numbers today, accepting that today's numbers rest on few changes. — 2026-11-03
