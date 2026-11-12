---
title: "Decisions — midnight-stamp-test"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, tests, make-verify]
---

# midnight-stamp-test — Decisions

Class: bounded (bead coding-harness-bxxt.5; one answered question or a
reasoned skip is owed — a skip below, written during the night run of
2026-11-10 and to be confirmed by the maintainer at the plan card).

## SKIP · interview

status: skipped
reason: A bounded bug fix whose intent and done-condition the bead states in full — the named test fixes the clock it compares against, and a search shows whether sibling tests take the date the same way (bead coding-harness-bxxt.5, measured failure of 2026-11-09 23:22 UTC). The exploration made that search and named the siblings. What remains is mechanics, decided below with reasons; the plan card goes to the maintainer before anything is built.

## Decided by the agent

[DETAIL] **The siblings the exploration named are fixed in the same change**,
not only the one test of the bead's title. Reason: the bead asks for the
search, and each sibling loses the same 25 minutes of the verify slot when a
full check crosses local midnight.

[DETAIL] **A test fixes the date it compares against instead of reading the
clock twice**: one date is set for the code under test and the assertion uses
the same value. Where the code under test is a subprocess stand-in, the date
reaches it explicitly rather than through a patch that cannot cross the
process. Reason: an in-process patch does not reach the planted make
stand-in, and a frozen constant would clash with its live date.

[DETAIL] **Production behaviour does not change.** Where the runner reads the
date stays as it is, except for what a test needs to set the date in one
place. Reason: the bead is a test bug; the stamps the runner writes are
correct.

[DETAIL] **The production site with the same shape is named, not repaired
here**: `review_audit_only` re-stamps at check time, so an append stamped
seconds before local midnight and checked after it would be refused. The spec
states it as a limit and the pull request proposes a follow-up bead. Reason:
no incident is recorded, the window is seconds, and repairing a production
check is scope the bead does not carry.
