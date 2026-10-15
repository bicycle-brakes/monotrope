---
title: "Spec — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, research, swarm]
class: architectural
appetite: 12
adr_files: [docs/adr/0018-phase-1-research-swarm.md]
---

# Spec — research-swarm

Phase 1 gives larger changes six reconciled research topics, using all declared
free models for public research, Flash models for repository comparisons and
Opus 5.5 for reconciliation (bead coding-harness-icw). Sources:
[`research.md`](research.md) and [`decisions.md`](decisions.md), Q-1 to Q-6.

## Problem

Evidence was collected on 2026-10-14; the drafting baseline is `1e29f6e`.

- Exploration obtains one model's repository facts, with no independent
  second view or reconciliation; broad architecture and adjacent-spec
  comparisons are not assigned to anyone (`research.md`, "Phase 1 as it
  runs today"; `scripts/stage2.py`, `explore`).
- The existing explorer has file tools, with no qualified public-web research
  path; adding researchers alone cannot deliver current outside evidence
  (`research.md`, "The earlier proposal this bead was created for").
- The free models named by the interview have unread data terms, and the
  existing Pi review calls can read outside the worktree; reusing those calls
  would contradict the maintainer's exclusion of repository content from
  free research (`research.md`, "The OpenCode Go infrastructure";
  `decisions.md`, Q-1 and Q-3).
- Exploration precedes the spec that currently carries the class; the
  maintainer's class-dependent routing needs an earlier explicit input
  (`scripts/stage2.py`, `explore`; `docs/WORKFLOW.md`, "Which change gets
  what"; supplementary repository evidence in `research.md`).

## Terms

- **Free roster:** every model declared for public-only OpenCode research;
  initially `longcat-2.5-preview-free`, `space-bunny`, `hy4-preview` (Q-1).
- **Flash pair:** `deepseek-v4.1-flash` and `mimo-v2.6-flash` on OpenCode Go.
- **Topics:** (1) code today, (2) rules and decisions, (3) history,
  (4) tests and gates, (5) risks and edge cases,
  (6) outside world and neighbours (Q-2).
- **Public topic:** one sentence, written by a fresh Opus 5.5 call, that
  names what the change is about in plain words, without file, path, code,
  identifier, change or bead names (Q-6). Example: "container isolation for
  AI agent runs".
- **Public brief:** fixed generic engineering questions, the public topic and
  public sources; no other change-specific text or repository-derived content.
- **Research stage:** one part of this phase-1 run; it is not Stage 1 or 2
  of the workflow's model routing.
- **Role invocation:** one isolated CLI process; its tool use can entail
  several provider requests. Invocation counts are not token or cost figures.
- **Complete run:** every required contribution and the judge's six-topic
  reconciliation succeeded; completeness does not settle an open question.

## Acceptance criteria

1. When Stage 2 exploration selects `feature` or `architectural`, phase 1
   uses the research swarm.
   *Refuted by:* either class producing only the former single GLM report.
2. When Stage 2 exploration selects `bounded` or `spike`, phase 1 keeps the
   existing single GLM 5.3 Flash exploration.
   *Refuted by:* either class starting a free researcher or a swarm judge.
3. When Stage 2 exploration runs before `spec.md` exists, its routing class
   is explicitly available from the research header or an explore-only
   `--class` argument.
   *Refuted by:* requiring a spec or plan to explore with an explicit class.
4. If the routing class is absent, invalid or disagrees between supplied
   sources, Stage 2 exploration refuses before a model call.
   *Refuted by:* guessing `bounded`, overriding a contrary spec, or calling
   a model after the conflict.
5. When a swarm starts, its first research stage attempts every model in the
   declared free roster before any Flash researcher starts.
   *Refuted by:* omitting `space-bunny` or starting Flash before the free
   roster's attempted contributions are recorded.
6. When the six topic pairs are assembled, topics 1–5 each have separate
   contributions from both Flash models and topic 6 has a free public
   contribution paired with a Flash repository comparison.
   *Refuted by:* a free model assigned repository inspection, a missing
   topic, or two seats backed by one Flash report or one shared session.
7. When the reconciled research is published, it explicitly compares public
   practice, the overall architecture and nearby specifications with the
   change, identifying missing evidence where a comparison could not be made.
   *Refuted by:* six code summaries with none of those comparisons or an
   assertion that unread adjacent specs are absent.
8. While a free researcher runs, its model requests and web requests contain
   no repository-derived content other than the public topic, in particular
   no change name, identifiers, paths, history, instructions, private briefs
   or paid-model reports.
   *Refuted by:* a repository canary in a captured public request, including
   one introduced through ambient context, the public topic or a web query.
9. While a free researcher runs, it has no tool or automatic context path
   through which it can obtain repository files, git data or other private
   local content.
   *Refuted by:* an available file or shell tool, discovered repository
   context, or a web fetch reaching a local file or private network address.
10. When public evidence supports a claim in the research, the evidence
    records an actually retrieved source page's URL, title, retrieval date
    and excerpt or locator, with applicability distinguished from fact.
    *Refuted by:* a search snippet or an invented URL standing as the only
    evidence, or a generic best practice presented as a local observation.
11. If a role's endpoint, model or permitted data class is undeclared or
    incompatible with that role, the runner refuses that call.
    *Refuted by:* a free endpoint permitted to read framework content, an
    unlisted model called, or unread free-model residency presented as known.
12. If the leak check immediately before any participant or judge call is
    not clean, the run stops with exit 2 and starts no subsequent model call.
    *Refuted by:* one scan covering all calls or any fallback after a BLOCK.
13. When a participant or judge call is attempted, its durable research
    record identifies the run, input state, role, topic, endpoint, model,
    individual leak-check result and eventual outcome.
    *Refuted by:* an anonymous contribution, a failed slot recorded as
    successful, or a judge without its own audit entry.
14. When the pairs are reconciled, a fresh Opus 5.5 context produces the
    reconciliation for all six topics.
    *Refuted by:* MiMo or Codex judging, a researcher judging its own report,
    or an Opus answer omitting a topic.
15. When the judge cannot resolve a disagreement from cited evidence, the
    research retains the disagreement and its evidence as unresolved.
    *Refuted by:* majority agreement erasing a sourced objection, or a
    judge's preference being recorded as a maintainer answer or accepted ADR.
16. When a run's synthesis is appended to `research.md`, its local claims
    remain traceable to source paths and symbols at the recorded input state.
    *Refuted by:* only line numbers, a nonexistent source, a source from
    another input state, or loss of the supporting contribution.
17. While swarm exploration runs, only the runner writes the research
    artifact and all pre-existing repository content outside that artifact
    remains unchanged.
    *Refuted by:* a participant editing a file, a changed interview answer,
    replacement of earlier research, a git mutation or a tracker write.
18. If a required participant, source retrieval or judge fails, the run
    preserves its partial evidence and names the missing contribution with
    an incomplete result and nonzero exit status.
    *Refuted by:* exit 0 and a complete result after an empty report, timeout,
    malformed judge answer or unavailable public-web path.
19. When a swarm executes, the number and duration of its calls stay within
    its recorded finite budget without automatic retries or extra debate.
    *Refuted by:* a second invocation of a failed role, recursive delegation,
    a call after the total deadline, or an unbounded participant.
20. When exploration uses `--stage2-off [REASON]`, it retains the single
    Haiku 4.5 route and records the reason for the later plan.
    *Refuted by:* a swarm, an Opus judge, a foreign credential read, or a
    missing route/model/reason on that explicitly selected path.
21. When a call exposes its credential in output, the durable record and
    diagnostics redact the credential and every fragment of eight or more
    characters.
    *Refuted by:* a planted credential fragment in research, source receipts
    or an error message.
22. When the change is delivered, the phase-1 routing documentation and
    endpoint declaration agree with this spec and claim exactly the new
    research-swarm ADR.
    *Refuted by:* documentation still routing every class to one explorer,
    free ids added to the review ladder, or an existing ADR rewritten.
23. Before the free research stage, a fresh Opus 5.5 call writes the public
    topic, and the runner accepts it only if it is a single sentence of at
    most 20 words with no path, file name, identifier-shaped token (a
    hyphenated token counts as one), change name or bead id, and its leak
    check is clean; otherwise the run stops
    before any free call. The accepted sentence is recorded in the research.
    *Refuted by:* a free call after a rejected or missing topic, a topic
    written by a researcher or the runner itself, or an unrecorded topic.

## Non-goals

- The implementation-review swarm is separate work (bead coding-harness-4fk).
- Changing phase 1a, the draft, implementation, repairs, reviews or interactive
  sessions, or replacing the phase-2 input contract of research plus decisions.
- Sharing repository content beyond the one-sentence public topic with free
  models, reading their terms as a substitute for Q-3 and Q-6, or using a
  repository summary as a public brief.
- The old proposal's three-role team, cross-critique round, Codex judge,
  activation for every class or automatic research-completeness gate.
- A new agent framework, service, persistent web cache, benchmark project,
  cost-saving claim, live model discovery that automatically grants access,
  or a new paid search subscription.
- Opening sibling checkouts; comparisons use this worktree's architecture,
  adjacent specs and public sources, with unread neighbours named as gaps.

## Protected areas

- `decisions/`, `provenance.yaml` and existing `docs/adr/` files: human-owned
  answers and accepted records are not rewritten.
- `scripts/stage2_session.py`, `scripts/stage2_session_policy.mjs` and the
  OpenCode Go `modelle` ladder: the existing session and review routes stay.
- Tracker storage, user configuration and sibling repositories: this change
  introduces no writer or installation there.

## Definition of Done

- `make verify` is green; interview minimums and the criterion ledger hold.
- Routing moves together in `AGENTS.md`, `docs/WORKFLOW.md`,
  `prompts/01-explore.md`, `model-endpoints.yaml` and the new
  `docs/adr/0018-phase-1-research-swarm.md`.
- An offline capture on pinned Pi proves the public boundary with synthetic
  private canaries before the first live free-model call; mock launch tests
  alone are not evidence of runtime isolation.
- The decision pull request names the bead, keeps approval pending until the
  maintainer merges, and its final commit carries `Closes-Bead: coding-harness-icw`.
- A live public-only qualification after the merge records the actual free
  transport and public-web outcomes; until that succeeds, no complete live
  swarm is claimed. No new free endpoint is contacted before the merge.

## Open decisions

None open. Q-1 to Q-6 settle the human choices; no ADR answer is recorded here.
I choose the following reversible details and record their reasons explicitly.

- [DETAIL] The class is `architectural`: the swarm scheduler and separate
  public-data boundary form a new subsystem, so design and an ADR are owed;
  this is the first class declaration, not a reclassification to pass a gate.
- [DETAIL] Before a spec, callers provide `--class` or `research.md`'s class;
  all available declarations must agree, because silently assuming a small
  change would bypass Q-4. Explicit Stage-1 exploration needs no new class.
- [DETAIL] A spike retains the single explorer: Q-4 activates only feature
  and architectural work and does not request a swarm for spikes.
- [DETAIL] Q-3 supersedes the repository access implied by Q-1's original
  pairing. Two different Flash models fill topics 1–5; topic 6 pairs public
  free research with Flash's local comparison. All free reports also supply
  public analogues to the other topics, without becoming local evidence.
- [DETAIL] The initial free roster is exactly the three ids recorded in Q-1;
  every declared member is used automatically, and new ids need an explicit
  declaration. Availability and their Pi provider mapping are not presumed.
- [DETAIL] The public topic comes from its own headless Opus 5.5 call at effort
  `high`, given the private brief and the instruction of criterion 23, because
  Q-6 names Opus as its author and a runner call is auditable like every
  other role. A mechanical filter, not the model's promise, enforces the
  shape; a rejected topic stops the run rather than falling back to generic
  questions, so the maintainer sees the failure. The topic is the same for
  all free researchers.
- [DETAIL] One fresh headless Opus 5.5 call, at effort `xhigh` through official
  Claude Code, reconciles all six pairs: Q-5 chooses the judge, not six
  separate Claude calls, and the runner applies the leak check to this call.
- [DETAIL] Research remains evidence collection: the judge assesses support
  and exposes gaps, dissent and human questions, without selecting a design
  or adding a workflow gate. This meets Q-5 without adopting the old proposal.
- [DETAIL] The stages run sequentially, with one topic call, one invocation
  per free model, eleven Flash contributions and one judge; the initial
  roster means sixteen invocations. The topic call's deadline is 5 minutes. Researcher deadlines are 10 minutes, the judge's 15 minutes,
  and the whole run's 150 minutes, measured monotonically. Partial results
  fail visibly rather than spending unbounded quota.
- [DETAIL] Phase 4 has an appetite of 12 hours including repairs, stopping at
  the limit: no prior answer sets an appetite, and runtime qualification is
  part of this boundary change. No token or price ceiling is invented.
- [DETAIL] Free-model data is declared separately as public-only; unread
  residency and data terms stay explicitly unknown. Existing framework
  permissions and their residency check are not relaxed.
