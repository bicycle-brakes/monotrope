---
title: "ADR 0020 — Phase 1 uses a research swarm with a checked handoff"
category: adr
status: accepted
created: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, research, swarm, stage-2]
---

# ADR 0020 — Phase 1 uses a research swarm with a checked handoff

* Status: accepted by the merge of the pull request that carries this file.
  Until then, open is proposed and closed is rejected. Amends the phase-1
  routing of ADR 0007 and research purpose of ADR 0011; supersedes neither
  whole ADR and amends no numbered D/O decision.
* Review: maintainer chose the amended direction in the research-swarm
  interview on 2026-10-14/15, Q-1–Q-9; acceptance is the future merge, with
  no agent-written approval. Decider: maintainer; prepared by Codex.
* Date: 2026-10-15 · takes effect on merge.

## Context

The original single explorer lacked independent evidence and reconciliation
(research-swarm research, 2026-10-14, baseline `1e29f6e`). The first unmerged
slice used six broad topic pairs and free public researchers. The maintainer
amended that on 2026-10-15: finder first, smaller topics, three same-brief
models per repository topic and a fixed report/scoring contract (Q-7).
Pi's free-model path was observed to return 403 FreeTierError by the
maintainer; Q-8 replaces it with OpenCode Go through Pi, Q-9 selects DeepSeek,
MiMo and Qwen Flash for online topics. This draft relies on that recorded
observation, not a new live probe. Public-only context survives the provider
change (Q-3, Q-6, Q-8). The current six-topic source and missing handoff links
were read at `6e80ded` on 2026-10-15.

## Decision Drivers

* Comparable independent reports with the same input and perspectives.
* Mapped repository evidence, explicit neighbouring specs and public practice.
* No private context in online research, regardless of subscription billing.
* Human decisions and sourced disagreements survive research into the spec.
* Finite concurrent work with auditable refusals and partial results.

## Considered Options

* One runner with stage barriers and provider queues: one owner for state,
  context isolation, cancellation, provenance and append-only output.
* Separate finder/research/judge commands: inspectable steps, but more operator
  coordination and persisted state to prevent mixing baselines and budgets.
* Sequential execution of the same roles: simpler scheduling, but contradicts
  the maintainer's choice of concurrency in Q-7.

## Decision

Chosen option: "One runner with stage barriers and provider queues", because
it keeps the established entry point while making boundaries and handoff
checkable.

1. `stage2.py explore` dispatches features and architectural changes to the
   swarm, bounded/spike to GLM Flash; explicit Stage-1 fallback remains Haiku
   5.5 with its reason. Early research/spec/argument classes must agree.
2. Finder step 0 uses independent DeepSeek Flash, MiMo Flash and Haiku 5.5
   locators; Opus 5.5 merges code, rules/ADRs, tests/gates and neighbour lists.
   Finder suggestions remain marked rather than silently accepted.
3. Topics 1–8 cover code/reuse, callers/interfaces, rules/class, architecture,
   neighbours, history/volatility, tests/gates and risks; each uses the same
   repository trio on identical briefs, perspectives and report template.
4. Topics 9–11 cover best practice, existing tools/standards and public failure
   reports. Each uses DeepSeek Flash, MiMo Flash and Qwen 3.8 Flash through Pi
   with only the filtered Opus sentence, fixed questions and public sources.
   No free model or OpenCode CLI runs; that path is deferred by Q-8.
5. Reports hold at most seven identified claims with evidence, kind,
   confidence/basis, counter-evidence, unread sources, neighbour relation
   and typed questions. Opus reconciles all topics and records per-model
   supported/refuted/unique/off-brief scores grounded in claim ids. Every
   model starts with the same perspectives; differing angles need a later
   maintainer decision.
6. Independent topic reports stay buffered until their stage ends. Each role
   is fresh/read-only, declaration-checked and exact-prompt leak-checked.
   Online Pi has scratch-only discovery-disabled context and public tools
   that refuse private/local sources and retain successful retrieval receipts.
   The accepted repository-Pi read risk is not called public-context isolation.
7. Research carries all decisions and unresolved disagreements into an
   interview inventory with claim links. Class mismatches and neighbour
   contradictions are human decisions. Phase 1a may exceed class minima;
   only actual maintainer answers settle obligations. Phase 2 carries confirmed
   neighbours in `neighbours:` and names claims/answers behind criteria.
8. A blocking `research-handoff` gate checks v2 inventory coverage, answered
   human links, neighbours and criterion bases in live/archive changes.
   Older unstructured evidence is exempt; unread/ambiguous inputs are not
   success. The gate and tests travel with the kit. Review still checks
   semantic fidelity and source applicability.
9. Queues permit at most four calls per provider across roles, and a security
   refusal stops further dispatch with exit 2. The current graph has 39
   invocations; finite per-role and 150-minute total deadlines, no retry,
   recursive delegation or debate. Failed/incomplete runs retain evidence
   and exit nonzero; only the runner appends research and writes audit records.
10. Endpoint role lists are separate from the review ladder. Qwen is declared
    for research without changing that ladder. Every output is scrubbed of
    used credentials; frozen-state changes invalidate complete publication.

## Consequences

* More calls and subscription/Claude quota buy independently comparable
  evidence; concurrency reduces waiting but no duration/cost saving is measured.
* Finder, queue cancellation, templates, gate and kit integration add maintenance.
* Questions may exceed minimum counts; the gate cannot invent answers or
  establish that a recorded answer faithfully reflects a human conversation.
* Same-brief scoring is evidence for later evaluation, not automatic model
  selection or architecture/class changes. Volatile-fact governance remains
  a maintainer-approved proposal, not a global policy installed by research.
* Isolation must be demonstrated with the actual pinned runtime. An earlier
  phase-6 blocker for the offline capture remains until measured evidence
  exists; changing the online provider does not waive it.

## Validation

* Runner tests plant wrong roles, early dispatch, unequal briefs, missing
  claims/receipts, frozen-state drift, expired budgets and queued leak refusals.
* Handoff mutations delete decisions/answers/bases/neighbours, including class
  mismatches and neighbour contradictions; local and hosted checks must fail.
* `make verify`, generated CI and kit probe hold the same blocking contract.
* Before merge, the maintainer attends an offline real-pinned-Pi capture with
  synthetic canaries and a local mock model server; record version, source
  hashes, payload/tool-schema capture, attempted escapes and outcomes.
* After merge, public-only live qualification records actual Go models and
  search/fetch outcomes. Until success no complete live swarm is claimed.
