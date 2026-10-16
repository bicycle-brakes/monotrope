---
title: "ADR 0020 — Phase 1 uses a research swarm with a checked handoff"
category: adr
status: accepted
created: 2026-10-15
last_reviewed: 2026-10-16
updated: 2026-10-16
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, research, swarm, stage-2]
---

# ADR 0020 — Phase 1 uses a research swarm with a checked handoff

* Status: accepted by the merge of the pull request that carries this file.
  Until then, open is proposed and closed is rejected. Amends the phase-1
  routing of ADR 0007 and research purpose of ADR 0011; supersedes neither
  whole ADR and amends no numbered D/O decision.
* Review: maintainer chose the amended direction in the research-swarm
  interview on 2026-10-14–16, Q-1–Q-10; acceptance is the future merge, with
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
change (Q-3, Q-6, Q-8). Q-10 adds free models offered by Go itself, selected
from a fresh Pi catalog each run, only to online topics alongside the Flash
trio; Zen stays excluded. The source was read at `6146fde` on 2026-10-16;
this draft neither probes the catalog nor claims live availability. The
repository runtime pin is now Pi 1.2.0 (ADR 0019).

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
   In addition, every eligible Go chat model ending `-free`, selected from a
   live-fetched Pi Go overlay with declared include/exclude lists, works each
   online topic on the same brief. No Zen provider, OpenCode CLI, fixed free
   roster or substitution for the mandatory Flash trio. Dynamic free
   permission applies to public-only research, never private roles. Select only
   text-input chat entries with explicit catalog tool-call support; record
   absent/negative support, non-chat and baseline-only exclusions. These free
   seats are best-effort: failure is named, never hidden or substituted, and
   does not alone invalidate the 39 required fixed contributions.
5. Reports hold at most seven identified claims with evidence, kind,
   confidence/basis, counter-evidence, unread sources, neighbour relation
   and typed questions with report-local ids and claim links. The runner
   namespaces identities by run/topic/endpoint-model seat. Topic 3 carries a
   class assessment; topic 6 marks volatile facts and their central/runtime/
   dated governance proposal. Opus reconciles all topics and records per-model
   supported/refuted/unique/off-brief scores grounded in claim ids, plus
   unresolved and unsupported. Valid claims have one disposition, off-brief
   first; unique is an extra mark only for supported claims. Bad references
   remain unsupported; a report needs at least one evidence-backed claim. Every
   model starts with the same perspectives; differing angles need a later
   maintainer decision.
6. Independent topic reports stay buffered until their stage ends. Each role
   is fresh/read-only, declaration-checked and exact-prompt leak-checked.
   Online Pi has scratch-only discovery-disabled context and public tools
   that refuse private/local sources and retain successful retrieval receipts.
   The accepted repository-Pi read risk is not called public-context isolation.
7. Research carries every accepted raw-report decision (even refuted or
   off-brief) and unresolved judge disagreement into an interview inventory
   with global claim/question links, grouping duplicates without source loss.
   Class mismatches and neighbour
   contradictions are human decisions. Phase 1a may exceed class minima;
   only actual maintainer answers settle obligations. Phase 2 carries confirmed
   and given neighbours in `neighbours:` and names claims/answers behind
   criteria. Only a linked maintainer answer can drop a given neighbour;
   proposed removal creates an obligation. Runtime instruction auto-loading
   is disabled; finders/topic author share the frozen research/decisions/spec
   brief and repository seats receive identical embedded AGENTS.md.
8. A blocking `research-handoff` gate checks v2 inventory coverage, answered
   human links, neighbours and criterion bases in live/archive changes.
   Only complete runs support interview/spec and carry obligations; prior
   complete runs remain binding across reruns. Before a spec exists, valid
   pending items are listed with exit 0; with a spec, missing answers or no
   complete v2 run exit 1. Incomplete-run claims cannot support criteria.
   Older unstructured evidence is exempt; unread/ambiguous inputs are not
   success. The gate and tests travel with the kit. Review still checks
   semantic fidelity and source applicability.
9. Queues permit at most four calls per provider across roles, and a security
   refusal cancels queued work and stops/reaps active children, retaining
   available partial evidence as cancelled; exit 2 takes precedence. Freeze `N`
   selected Go free
   models before model calls; the budget is at most `39 + 3N` invocations. A
   bounded
   Go-only catalog refresh must succeed each run; failures never fall back to
   cached/shipped rosters or Zen, while valid zero availability keeps the
   fixed 39 slots. Defaults select all eligible models; explicit include
   narrows and exclude wins. Record dated source, freshness, policy and roster;
   missing explicit includes exit 1 before models; no silent truncation of
   models/reports to fit the deadline or judge context.
   Finite per-role and 150-minute total deadlines include catalog preflight;
   no retry, recursive delegation or debate. Required topic slots precede free
   slots, by topic and declared seat order (free ids sorted); reserve the
   judge's 15 minutes. Every unlaunched slot has a deadline outcome. Failed
   finder/merge/topic-author stages prevent later stages; filter rejection
   exits 1. Topic siblings finish after ordinary failures, but the judge
   requires all required reports. Failed/incomplete runs retain evidence
   and exit nonzero; only the runner appends research and writes audit records.
10. Endpoint role lists are separate from the review ladder. Qwen is declared
    for research without changing that ladder. Every output is scrubbed of
    used credentials; HEAD plus retained copies/digest of all tracked files
    and untracked non-ignored change-folder inputs bind local evidence.
    Changed inputs invalidate publication with named paths and exit 1; only
    runner research appends/restamping are ignored. Invalid given neighbours
    refuse preflight (exit 2); later unread evidence stays a named gap.

## Consequences

* More calls and subscription/Claude quota buy independently comparable
  evidence; concurrency reduces waiting but no duration/cost saving is measured.
* Finder, live catalog qualification, queue cancellation, templates, gate
  and kit integration add maintenance. Large free rosters may leave named
  best-effort slots unfinished at the deadline; that alone does not invalidate
  completion. Missing required slots still do. No seat silently disappears.
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
  They explicitly inject the pinned-wrapper stand-in and trap bare-Pi launches;
  actual-runtime qualification continues to use the real repository pin.
* Handoff mutations delete decisions/answers/bases/neighbours, including class
  mismatches and neighbour contradictions; local and hosted checks must fail.
* `make verify`, generated CI and kit probe hold the same blocking contract.
* Phase-6 review checks prose scope, comparison meaning, faithful dissent,
  volatile-fact classification and the relevance of resolved criterion bases.
* Before merge, the maintainer attends an offline real-pinned-Pi capture with
  synthetic canaries and a local mock model server; record version, source
  hashes, payload/tool-schema capture, attempted escapes and outcomes.
* Offline real-Pi catalog tests prove forced refresh despite fresh caches,
  Go-only selection and removal of obsolete shipped ids; malformed/timeouts
  never become zero availability or a fixed-roster fallback.
* After merge, public-only live qualification records the refreshed catalog,
  actual Go Flash/free models and search/fetch outcomes. Until success no
  complete live swarm is claimed.
