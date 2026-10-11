---
title: "Session handover — phase-1 research swarm proposal, 2026-10-08"
category: handover
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-11
direction: framework->framework
provenance: ai-generated
produced_by:
  kind: llm-session
  name: codex
  version: "2026-10-08"
tags: [handover, explore, swarm, proposal]
target_ref: "0e231c1"
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Objective and concrete proposal

After asking to preserve Claude's token allowance in phase 1, the maintainer
asked for a small swarm that discusses a feature, researches current internet
practices, checks adjacent specs and overall context, and ends with a judge.
The read-only assessment makes that concrete as three independent researchers,
one bounded cross-critique round and one fresh judge, producing `research.md`
([proposal](../../research/2026-10-08-explore-swarm-proposal.md)).

The proposed first models are GLM 5.3 Flash for the three roles and the
currently declared Codex model for the judge. There is no Claude-model
fallback in the proposal. Judge conclusions assess research completeness and
evidence; intent, binding specifications and accepted ADRs remain human-owned.
The existing file-only explorer needs a qualified web tool path.

## Decisions and open input

The swarm intent is the maintainer's request. The maintainer was asked whether
to activate it for every change or only features/architectural changes; no
answer was available at drafting time. The latter is explicitly a working
assumption. No architecture answer, activation policy, cost ceiling or
implementation plan was approved or recorded as a decision.

## Completed work and evidence

Read Coding Harness's current phase-1 prompt, workflow, runner and endpoint
declaration at freshly fetched `origin/main` `0e231c1`, 2026-10-08. Read the
existing CrewAI and Agent SDK research. Read primary Anthropic and AutoGen
documentation on 2026-10-08. The attempted LangChain reference retrieval
failed and is not treated as read evidence.

No swarm call, internet-tool qualification, model benchmark, installation or
runner change was performed. No full verifier is claimed for these uncommitted
proposal documents; metadata, local links and whitespace are checked locally.
The Kubernetes assessment PR #98 is a separate completed publication and
is not changed by this proposal.

## Working state, ownership and resumption

Branch `docs/explore-swarm-proposal`, worktree
`.claude/worktrees/explore-swarm-proposal`, based on `0e231c1`. The proposal
and this handover are uncommitted; no PR or implementation change was made.

The live scanner reports session `coding-harness-82` in the main checkout.
That session owns tracker writes under the one-writer rule. No matching swarm
task was found by the read-only tracker search; this session creates, claims
and closes no bead. Before implementation, the owning session must allocate
the new task and its worker must claim it. Other worktrees are untouched.

Resume by reading the proposal and the maintainer's activation-scope answer.
Then the tracker-writing session allocates the change and the owning session
prepares its architectural spec/design/plan, including the maintainer's ADR
answer, before modifying the runner.

## Addendum — 2026-10-08, the handoff into phase 2

The maintainer asked how the swarm result enters phase 2. Read the current
phase-2 spec and phase-1a interview prompts at `0e231c1` and added a handoff
section to the proposal. Phase 2 keeps its `research.md` plus `decisions.md`
input contract, using the judge's compact synthesis and selectively checked
original evidence. It translates observations into problem/criteria, accepted
constraints into boundaries and adjacent-spec impacts into explicit proposed
deltas. Missing facts return as `[GAP]`; human intent remains `[DECISION]`.
The phase-2 decision gate and independent phase-2a review remain in place.
No model assignment, runtime or tracker state was changed.

## Addendum — 2026-10-08, mandatory interviews and minimum questions

The maintainer explicitly requested mandatory interviews for features and ADR
work to ensure engagement, then specified at least three questions for a
feature and five for an ADR. Added this stated intent to the research proposal.
The current accepted workflow remains optional; no workflow prompt, runner or
gate was changed. Inspected the four change-class definitions at `origin/main`
`902c0f7`: `spike`, `bounded`, `feature` and `architectural`; ADR is an artifact.

Recommended, without recording a maintainer decision: a short interview for
spikes, a conditional interview for bounded changes, and the five-question
minimum when a feature also requires an ADR rather than adding both minimums.
The proposal counts substantive human-answered questions, asks them one at a
time, preserves settled answers and records interview evidence in
`decisions.md`. These details remain proposed implementation semantics.

Next action: incorporate the stated feature/ADR minimums into the change's
spec and decision proposal once the tracker-owning session allocates the work;
resolve the remaining class and overlap policies with the maintainer. This
session still has no allocated bead and performs no tracker writes. The two
proposal documents remain uncommitted on `docs/explore-swarm-proposal`.

## Addendum — 2026-10-08, implementation priorities overview

The maintainer asked for the most important current implementations. Read
the local Beads ready and in-progress lists and details for the runner,
decision/interview, foundation, write-guard and validator work. A read-only
GitHub query returned Kubernetes assessment PR #98 as the only open pull
request at query time. This is a local tracker snapshot, not a fresh Dolt
remote synchronization; priorities discussed in the conversation are
recommendations and do not change tracker priorities or ownership.

No swarm task was found by the tracker search. The requested mandatory
feature/ADR interviews and their question minimums remain in this proposal;
they have not been implemented or allocated as a new tracker task. No code,
tracker state, commits or PRs were changed by this overview.

## Addendum — 2026-10-08, Codex takes over the MiMo watch

At the maintainer's explicit request, read
`docs/journal/handover/2026-10-08-codex-takes-over-mimo-watch.md` from
`origin/main` and started its Next step. Fetched origin repeatedly during the
watch; as of 12:14 Europe/Berlin, the published MiMo head is still
`dedecf5c577f1407b953df4c1905b65890f7d031`. Current `origin/main` is
`8f097a3f5c2f27e5b19cf23310bc9465b34ebedc`, which merges that takeover
handover in PR #100. The worker has 14 modified paths; do not edit or commit
them. Its changes progressed during the watch but are not published.

Prepared a separate detached audit worktree at
`.claude/worktrees/mimo-watch-audit`, initially at `dedecf5`, and successfully
ran `make venv` with the hash-locked requirements. The sandbox's first
dependency download failed on network access; the approved network-enabled
retry succeeded. No full verifier was run against the already-audited old
commit. No live model or subscription-credit probe was started.

A preliminary read-only function-source comparison of the mutable worker
file found `thread_id`, `run_codex`, `spec_review` and `review` byte-identical
to current `origin/main`. This is not a verdict on a published commit. Spec
and reviewer prompts also describe Codex for 2a/6 and the ladder for 4b.
The watch cannot produce its requested commit verdict until the worker
publishes the route repair. No tracker writes were performed.

Resume by fetching origin. If `origin/feat/stage2-mimo` has advanced past
`dedecf5`, check out that exact SHA detached in `mimo-watch-audit`, rerun
`make venv` if the locked requirements changed, and run `make verify` there.
Compare the four Codex functions with `origin/main`, verify that only 4b
uses the ladder, and report the exact tested SHA and results in German.
For fixture commits, the prior independent audit used process-local
`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`
to avoid interactive signing; do not change persistent git configuration.

## Addendum — 2026-10-08, runner-derived-file defect assessment

The maintainer asked about the size of the derived-file repair
(coding-harness-mfv). Read the current runner's implementation and verification
boundary, the existing registry renderer and frontmatter stamp command. Both
repair mechanisms already exist; the missing piece is runner orchestration
before verification, with bounded writes and regression evidence. The defect
can waste repair/fallback calls or stop an otherwise correct implementation;
it was also observed in a review-loop audit-file creation. Recommended a small
implementation slice, estimated a few hours for code and focused tests and
roughly a working day including workflow artifacts and review. These are
unmeasured estimates, not a commitment. No implementation was performed.

## Addendum — 2026-10-08, Codex session closed; review handed to Cline

The maintainer explicitly ended this Codex session and confirmed that the
latest review was sent to Cline. Further repair and publication belong to
Cline; this session takes no implementation action.

Checked at 21:18 UTC on 2026-10-08: decision PR #104 is open at
`a6dde6b9a476177526c1917a03a6c988f1df7976`, branch
`feat/interview-minimums`, worktree `.claude/worktrees/interview-minimums`.
The interview bead remains in progress, assigned to cline-interview-minimums
(coding-harness-6yg). The worker has an uncommitted change in
`scripts/check_interview_minimums.py`; this session did not modify it.

The latest review of `a6dde6b` reports three P2 findings: an ADR renamed out
of its directory escapes detection; a valid inline YAML comment prevents
reading an old spec date; the staged-only regression fixture creates its
baseline ADR on the wrong branch. Reviewer-reported evidence at that commit:
171 relevant tests passed, 2 skipped. That evidence is not a green verdict
on Cline's subsequent uncommitted repair. No repair, fresh full verification
or merge is claimed by this session.

PR: https://github.com/MPAdesso/coding-harness/pull/104. Cline's earlier
handover is `docs/journal/handover/2026-10-08-interview-minimums.md` in its
worktree; its statement that nothing remains open predates these findings.
No bead is closed here, and no tracker, commit or push action was performed.
This addendum stays local and uncommitted with the earlier proposal notes on
`docs/explore-swarm-proposal` (HEAD `0e231c1`); other worktrees stay worker-owned.

Resume only on a new maintainer request: inspect Cline's repair commit and
validation for all three review findings before considering PR #104 ready.
The phase-1 swarm remains separate proposed work.

## Addendum — 2026-10-11, published from the local worktree

The two documents had stayed uncommitted in this worktree since 2026-10-08;
a review of the older handovers on 2026-10-11 found them there, and the
maintainer asked to secure them. They are committed unchanged except for this
addendum, on `docs/explore-swarm-proposal` rebased onto `origin/main`
`0c71403`. The tracker-writing session created bead coding-harness-icw (Phase 1
as a bounded research swarm) for the proposal.

What changed since this file was written: the interview minimums are merged
(#104, bead coding-harness-6yg closed), so the proposal's interview section is
history, not open work; the stage-2 reviewers now run on OpenCode Go through
Pi (ADR 0011, ADR 0012), which changes the "unmerged reviewer change" remark
in the proposal. Still open: the maintainer's answer on the activation scope
(every change, or only feature and architectural changes).
