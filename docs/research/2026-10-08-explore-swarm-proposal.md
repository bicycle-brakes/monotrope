---
title: "A bounded research swarm for workflow phase 1"
category: research
status: proposed
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-11
owner: framework-architect
provenance: ai-generated
produced_by:
  kind: llm-session
  name: codex
  version: "2026-10-08"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, explore, swarm, judge, model-routing]
---

# Phase 1 as a bounded research swarm

## Intent and status

The maintainer wants phase 1 to use non-Claude models to preserve Claude's
allowance, with a small team that researches current internet practices,
discusses how a requested feature fits adjacent specifications and the whole
system, and ends with a judge. This document makes that proposal concrete;
no runner, model routing, phase contract or decision has been changed.

Working assumption, not a maintainer answer: enable the swarm for features
and architectural changes; retain the single explorer for smaller changes.
The maintainer was asked whether the swarm should instead run for every
change. No answer was available when this proposal was written.

## What exists today

Read against freshly fetched Coding Harness `origin/main` at `0e231c1`,
2026-10-08:

- `prompts/01-explore.md` selects GLM 5.3 Flash and an explicit Haiku fallback.
  It currently says to collect facts without recommendations or judgement.
- `scripts/stage2.py:explore` makes one non-interactive model call, then
  appends its result to `research.md`. `run_work_model` launches Claude Code;
  `glm_env` routes GLM calls to Z.ai. The client is not the inference vendor.
- `WORK_READ_TOOLS` and the workflow allow repository file tools, not an
  internet researcher. Parallel role calls, a debate and a judge are absent.
- Every foreign-model call must use the checked stage-2 entry point. Model
  declarations, the leak check, restricted reads and audit records remain
  applicable to each swarm participant and each discussion turn.
- The accepted endpoint declaration contains GLM and Codex. DeepSeek and
  MiMo through OpenCode Go exist in the separate, unmerged reviewer change;
  that is not phase-1 support on main.

## Team and one bounded discussion

The runner schedules the work with a fixed sequence. It does not require an
additional model merely to decide who speaks next.

| Role | Question and evidence | Proposed first-pilot model |
| --- | --- | --- |
| Existing-system researcher | What exists in code, tests and the feature's own spec? What can be reused? Cite paths and symbols. | GLM 5.3 Flash |
| External-practice researcher | What do current official docs, standards and research say? Under which assumptions does each approach apply here? Open the original sources. | GLM 5.3 Flash, with a separately qualified web tool path |
| Integration researcher | How does the request fit adjacent specs, interfaces, ADRs and system boundaries? What would conflict, duplicate responsibility or reopen a decision? | GLM 5.3 Flash |
| Judge | Are the claims supported, contradictions resolved or explicitly open, and all requested contexts covered? | Codex using the currently declared model |

Model choices are a starting proposal, not a measured ranking. Separate
research contexts and an independently prompted judge matter more for this
first experiment than adding three provider integrations at once. A later
comparison may substitute DeepSeek or MiMo once their routes are accepted.

The execution has seven phase-level agent invocations:

1. Three independent research calls run against the same commit and intent
   brief. They do not see each other's first reports.
2. Freeze those reports. Each researcher receives the other reports and
   responds once: a concrete objection, its evidence, and a correction or
   explicit unresolved disagreement. These are three more calls, not a
   free-running group conversation.
3. A fresh judge receives the reports, responses and their evidence. It
   checks decisive citations against the source material and produces the
   final synthesis in one call.

The judge does not decide truth by counting votes. Unsupported agreement is
still unsupported. Important dissent stays visible with its evidence. All
roles must distinguish source facts, local facts, applicability inferences
and proposed options. There is no requirement to manufacture agreement.

Each agent invocation can make several model requests while using tools.
Measure those requests, search-service inference and charges, tool calls,
tokens and retries in the run budget. If a provider or tool path hides them,
report them as unknown rather than claiming a complete cost figure.

## Research output and the judge's boundary

The final artifact stays `plans/changes/<name>/research.md`. It contains:

- The current behavior and evidence from code, tests and specifications.
- A dated external-practice comparison, its assumptions and applicability.
- The fit with adjacent specifications, system responsibilities and ADRs.
- Contradictions, rejected claims and disagreements that remain unresolved.
- Which files/specs a change would touch, without editing them in phase 1.
- `[GAP]` items to research and `[DECISION]` items reserved for the maintainer.
- A judge conclusion: evidence sufficient for the next phase, more research
  needed, or a human decision needed; each with a concrete reason.

This conclusion is proposed research triage, not an accepted new gate. It
does not approve a feature, write a binding spec, accept an ADR, release an
implementation or replace phase 2a/6 review. Recommendations must be labelled
as options for later phases. Expanding phase 1 beyond its current no-judgement
rule requires an explicit workflow change.

The smallest pilot uses proposed caps: three workers, one discussion round,
one judge, no recursive delegation, and no automatic extra round. Target
first reports at at most 600 words, discussion responses at 250 words and
the synthesis at 1,000 words. These prompt targets are not hard token limits.
The implementation must distinguish enforceable deadlines/call limits from
requested output length and must not invent provider usage measurements.

On a failed worker, missing source access, exhausted budget or unresolved
conflict, preserve the partial evidence and report the missing contribution.
No clean verdict follows from an incomplete run. A retry is explicit and
uses the remaining run budget; it does not restart the budget or switch to
Claude. Checkpoints bind to the input commit and intent; changed inputs
invalidate reuse of earlier reports.

## Handoff into phase 2

The current `prompts/02-spec.md` synthesizes `research.md` and `decisions.md`.
Keep that entry contract. The swarm's judge supplies a compact final research
section with links to supporting evidence and the discussion's unresolved
points. Phase 2 reads that section, the maintainer's intent and decision
answers first, then retrieves original evidence when a material claim needs
checking. It does not need every worker's full conversation.

| Phase-1 result | Phase-2 use |
| --- | --- |
| Observed gap and current behavior | Problem statement with evidence |
| Applicable external practice | Proposed requirements, with assumptions and source provenance preserved |
| Constraints from accepted ADRs and adjacent specs | Explicit constraints, boundaries and interfaces |
| Impact map of affected specs | Identify proposed specification deltas and consequences; coordinate changes rather than silently rewriting an adjacent contract |
| Failure cases and counterexamples | Testable acceptance criteria, each with a refuting case |
| Options and unresolved dissent | Non-goals, alternatives and classified open questions |

Material requirements must remain traceable to a source fact, an accepted
constraint, a stated human decision or a labelled derivation. The judge's
preferred option alone is not evidence of a maintainer decision.

If the judge reports missing evidence, route a bounded `[GAP]` back to the
relevant researcher. If intent or a binding architecture choice is open,
retain `[DECISION]` and obtain the maintainer's answer. The current accepted
workflow makes phase 1a optional and human-called. The maintainer requests
the mandatory interview policy below; it is proposed here, not yet installed
as a workflow rule. Phase 2 may prepare
a draft while decisions are open, but its existing gate cannot pass with an
open `[DECISION]`. Findings first noticed in phase 2 follow the same routing.

The spec states what must hold. Implementation choices belong to later design
and planning where appropriate. Phase 2a independently reviews the resulting
spec; it is not replaced by the phase-1 judge. The inspected phase-2 prompt
still assigns Opus 5.5, so introducing the swarm alone does not change that
model assignment.

## Interview policy requested by the maintainer

On 2026-10-08 the maintainer explicitly requested mandatory interviews for
features and ADR work to ensure engagement, with at least three questions for
a feature and at least five for an ADR. These are minimum counts, not maximums.
If a feature also requires an ADR, the five-question minimum applies; the
minimums are not added together. This overlap treatment is a proposal.

| Change scope | Interview policy | Status |
| --- | --- | --- |
| `feature` | Mandatory, at least three substantive questions | Maintainer-requested |
| Creating or changing an ADR, including `architectural` work | Mandatory, at least five substantive questions | Maintainer-requested |
| `spike` | Recommend a short interview about the learning question, time budget and useful result; no fixed minimum proposed | Recommendation, not a stated decision |
| `bounded` | Recommend an interview only when human intent, expected behavior or acceptable risk remains open | Recommendation, not a stated decision |

ADR is an artifact rather than a separate change class. Classifying work as
`bounded` or `spike` must not bypass the ADR interview when it creates or
changes an architecture decision.

Ask one question at a time and adapt subsequent questions to the answers.
For a feature, start with the desired user outcome, scope and non-goals, and
observable acceptance criteria. For an ADR, cover the decision goal,
constraints, alternatives and their tradeoffs, acceptable risks, and adoption
or reversal conditions. These are coverage guides, not a fixed questionnaire.
Offer an evidence-based recommendation with consequences where appropriate.
The judge prepares questions and options; one interviewer holds the human
conversation rather than making the maintainer answer several agents.

Only distinct substantive questions answered by the maintainer count toward
the minimum. Agent-authored answers, unanswered questions and repeated
confirmations do not count. Reuse settled decisions as context rather than
asking them again; ask relevant consequences or boundaries instead. An
answered question need not force a new decision merely to increase the count.
Resolve factual `[GAP]` items through research and reversible `[DETAIL]` items
through a reasoned agent choice, without padding the interview with them.

Record the questions, human answers and resulting decisions in `decisions.md`.
Under the proposed policy, phase 2 may draft but cannot pass its gate for a
feature or ADR change until the applicable minimum is answered and no
`[DECISION]` remains open. The agent cannot skip these mandatory interviews
by giving its own reason. This policy requires a deliberate workflow decision
and corresponding prompt and gate changes before it becomes effective.

## Internet access and ownership

Qualifying the web tool path is part of the pilot. Simply adding roles to the
existing file-only explorer cannot deliver internet research. Require actual
page retrieval, source URL/date/title and an evidence excerpt or locator;
search snippets alone are insufficient. Treat fetched pages as evidence, not
instructions. Restrict queries to framework requirements and keep customer
material and personal vault data outside the run.

All model roles are read-only. The existing runner alone writes the final
artifact and run evidence; no participant commits, publishes, writes the
tracker or edits surrounding specs. Do not increase writing-session counts
merely because several read-only researchers run concurrently.

Share compact reports and selected evidence rather than full transcripts.
Deduplicate identical web fetches and record the request/topic, commit,
roles, model versions, sources, call outcomes, measured usage and total time.
Keep resume records outside the personal vault and use Git for the final
artifact. An incomplete record is a visible limit, not a successful run.

## Best-practice evidence, and what it does not prove

[Anthropic's research-system account](https://www.anthropic.com/engineering/multi-agent-research-system)
supports decomposing research into bounded roles with separate contexts,
explicit task boundaries and source-based evaluation. It also reports
substantial token overhead. Its performance figures are specific to its own
system and evaluation; they do not establish savings or quality here.

[AutoGen's group-chat documentation](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/selector-group-chat.html)
shows explicit termination conditions and programmatic speaker selection.
This proposal adopts bounded turns and deterministic sequencing as ideas;
it does not propose installing AutoGen. The existing
[CrewAI assessment](2026-09-18-crewai-assessment.md) likewise argues against
adding another coordinator without a measured missing function.

These sources were read on 2026-10-08. No multi-model swarm, browsing adapter,
discussion, judge or cost comparison was executed in this assessment.

## Reviewable first implementation slice

After the maintainer settles the activation scope and architecture answer,
and the first tracker-writing session assigns a bead:

1. Write the architectural change package for one phase-1 entry point,
   roles, evidence format, bounded sequence and qualified web path.
2. Implement it through `scripts/stage2.py`, with prompts, endpoint/tool
   declarations, audit records and tests. Update phase-1 wording and the
   workflow deliberately; retain the normal decision-PR process where a
   protected policy changes.
3. Compare the swarm against the current explorer on three representative
   requests: a local feature, a change touching neighboring specs, and a
   request requiring current web documentation. Use the same input SHAs.

Seed a stale source, a conflict with an accepted ADR and a failed participant.
Done means the judge exposes those cases, provides traceable evidence for
normal runs, and does not conceal missing contributions or take human
decisions. Measure missed facts, source correctness, human correction effort,
Claude consumption, total provider consumption/cost and wall time. Saving
Claude's allowance is a separate outcome from reducing total tokens.

No recurring service, Kubernetes cluster, new agent framework or modification
to another project's specs belongs to this first slice.
