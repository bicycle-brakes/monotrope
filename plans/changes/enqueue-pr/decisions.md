---
title: "Decisions — enqueue-pr"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-va1l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, merge-queue, grant, harness-neutral]
---

# enqueue-pr — Decisions

## SKIP · interview

status: skipped
reason: The maintainer decided the direction in the conversation of 2026-11-25 (session 9200c6b1): the merge-queue grant of AGENTS.md (PR #459) is enforced by one script that checks phase 6, required checks and the Closes-Bead trailer and only admits to the merge queue; asked 'Ok, leg los'. The bead (coding-harness-va1l) states every condition; no open human intent question remains.

## Q-1 · Ambiguity S-1 (what a clean phase 6 is)

asked: 2026-11-25
answer: "Clean means the newest phase-6 table reports no finding or every row is fixed or rejected; any row open or taken refuses, at any severity."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-1 of enqueue-pr.
  Intention: fix the admission condition for phase 6.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/enqueue-pr/spec.md in the final draft.
  Architecture change: none.

In the context of admitting pull requests to the merge queue unattended, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that an open MINOR also holds a pull request back. — 2026-11-25

## Q-2 · Ambiguity S-3 (which commit phase 6 reviewed)

asked: 2026-11-25
answer: "The runner records the reviewed commit in the phase-6 block; after that commit only record commits inside the change folder, empty commits and merges of main may follow; anything else refuses."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-3 of enqueue-pr.
  Intention: tie the phase-6 evidence to the admitted head.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/enqueue-pr/spec.md in the final draft.
  Architecture change: none.

In the context of phase-6 evidence that records no commit, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting a small runner change that writes the reviewed commit. — 2026-11-25

## Q-3 · Ambiguity S-4 (which checks must pass)

asked: 2026-11-25
answer: "The required set comes from the main ruleset; a required check missing on the head refuses; SKIPPED and NEUTRAL pass as GitHub counts them."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-4 of enqueue-pr.
  Intention: fix the required-check condition.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/enqueue-pr/spec.md in the final draft.
  Architecture change: none.

In the context of required checks on the head, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting GitHub's own semantics for skipped checks. — 2026-11-25

## Q-4 · Ambiguity S-5 (an admission that cannot merge directly)

asked: 2026-11-25
answer: "Admission uses the GraphQL enqueuePullRequest mutation with the expected head commit; it can only enqueue and fails when there is no queue."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-5 of enqueue-pr.
  Intention: make a direct merge impossible.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/enqueue-pr/spec.md in the final draft.
  Architecture change: none.

In the context of the admission call, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting a GraphQL call instead of gh pr merge. — 2026-11-25

## Q-5 · Decision in the draft (decision pull requests)

asked: 2026-11-25
answer: "Option 1: the script refuses decision pull requests and names the reason; the maintainer admits them."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-10 of enqueue-pr.
  Intention: keep decisions effective only by the maintainer's merge.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/enqueue-pr/spec.md in the final draft.
  Architecture change: none.

In the context of decision pull requests, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that decision PRs wait for the maintainer. — 2026-11-25

## Q-6 · Ambiguity S-11 (one admission path)

asked: 2026-11-25
answer: "The script becomes the one admission path for everyone (one-path principle, PR #402); prompts/07-commit.md step 5, docs/WORKFLOW.md and the decision-PR template switch to it; a direct gh pr merge stays behind approval. Asked back what is more sustainable; the orchestrator recommended one path; confirmed."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-11 of enqueue-pr.
  Intention: one path into the merge queue.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/enqueue-pr/spec.md in the final draft.
  Architecture change: none.

In the context of how pull requests enter the merge queue, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting a wider documentation change in this lane. — 2026-11-25

## Q-7 · Ambiguity S-14 (admission without the maintainer asking)

asked: 2026-11-25
answer: "Yes, as granted in PR #459: the orchestrator admits by itself once the script passes; the commit procedure and house rule 8 are amended."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-14 of enqueue-pr.
  Intention: unattended admission backed by code.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/enqueue-pr/spec.md in the final draft.
  Architecture change: none.

In the context of who may trigger admission, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting an amended house rule 8. — 2026-11-25

## Q-8 · Ambiguities S-15 and S-16 (requests the default refuses)

asked: 2026-11-25
answer: "A maintainer mode (--maintainer) keeps one path: it skips the phase-6, change-folder and trailer conditions but keeps checks, pinned head and enqueue-only; the agent policy list asks for it when attended and denies it unattended."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-15, S-16 of enqueue-pr.
  Intention: one path that still admits handovers, decision PRs and similar requests.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/enqueue-pr/spec.md in the final draft.
  Architecture change: none.

In the context of requests the default conditions refuse, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting a maintainer option guarded by the agent policy list. — 2026-11-25

## Q-9 · Ambiguity S-18 (phase-6 marks and released rows)

asked: 2026-11-25
answer: "They count: a disagree mark or a released row neither fixed nor rejected refuses."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-18 of enqueue-pr.
  Intention: a strict reading of a clean phase 6.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/enqueue-pr/spec.md in the final draft.
  Architecture change: none.

In the context of the phase-6 verdict, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting more refusals on disputed loop rows. — 2026-11-25
