---
title: "ADR 0019 — Phase 1 separates public research from repository comparisons and reconciles six topics"
category: adr
status: accepted
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, research, swarm, public-boundary]
---

# ADR 0019 — Phase 1 separates public research from repository comparisons and reconciles six topics

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, open is proposed and closed is rejected. Amends only
  ADR 0007's universal phase-1 route and ADR 0011's OpenCode Go research
  purpose; supersedes no whole ADR and changes no numbered D/O decision.
* Review: direction chosen by the maintainer in Q-1 to Q-6 on 2026-10-13/14
  (`plans/changes/research-swarm/decisions.md`); subsystem shape and runtime
  details proposed by Codex, not answered for the maintainer. Acceptance is
  the merge commit, written nowhere else, so approval fields stay empty
  (ADR 0008) · Decider: maintainer · prepared by Codex.
* Date: 2026-10-14 · takes effect on merge.
* Number: drafted as 0018 and renumbered to 0019 on 2026-10-15, after
  ADR 0018 (every question carries its context) merged first.

## Context

Exploration currently calls one GLM 5.3 Flash model with repository file
tools and appends its facts to research; it has no paired views, public-web
tools or judge (`scripts/stage2.py`, `explore`, read at `1e29f6e` on 2026-10-14).
The existing paid Pi reviewer has unconfined file reads, a residual risk
accepted for that route, and cannot be reused for free public-only research
(`scripts/stage2.py`, "Reads"; ADR 0011).

The maintainer chose a research swarm, all free models in its first stage,
six fixed topics, free models receiving no repository content beyond one
Opus-written topic sentence without file or code names (Q-6), activation
for feature/architectural changes, and Opus 5.5 reconciling each pair. Q-3
explicitly leaves replacement of repository-bound free seats to the spec.
The earlier three-researcher/Codex-judge proposal is not the chosen team
(`plans/changes/research-swarm/research.md` and `decisions.md`, read 2026-10-14).

Free model availability, Pi provider mapping and the public-web tool path
are not qualified by this draft. Their data terms and residency remain
unread; the existing paid models' privacy statement is not applied to them.

## Decision Drivers

* Independent research on code, rules, history, tests, risks and neighbours.
* Public practice, architecture and nearby-spec comparisons are explicit.
* No repository content goes to a free model, including indirect context,
  except the filtered one-sentence public topic.
* Opus reconciles evidence without taking the maintainer's decisions.
* Every call has a declared role, an individual leak check and visible outcome.

## Considered Options

* **One runner-controlled swarm with separate public and private packets.**
  One phase-1 entry point enforces ordering, boundaries and failure records.
* **An interactive orchestrator dispatching the same separated roles.**
  Lower initial runner work, but each operator reproduces the guarantees.
* **Separate researcher and judge commands with an input manifest.**
  Easier individual reruns, but more state and a risk of mixed input revisions.

## Decision

Chosen option: "one runner-controlled swarm with separate public and private
packets", because public-only disclosure must hold in the launcher and tool
surface rather than depend on a model obeying an instruction.

1. Feature and architectural exploration uses the swarm; bounded work and
   spikes retain the single explorer. Explore accepts an explicit early
   class without requiring a spec and refuses contradictory class inputs.
2. All declared free models run first on fixed generic public questions.
   Initially these are LongCat, Space Bunny Free and Big Pickle (Q-1, as
   amended 2026-10-15).
   Their contexts expose only qualified public search and page retrieval,
   no local tools or repository-derived prompts. The public declaration
   records unknown terms/residency; it grants no framework permission.
3. Each repository-bound topic (1–5) gets independent DeepSeek Flash and
   MiMo Flash contributions on OpenCode Go. Topic 6 pairs Big Pickle's public
   research with DeepSeek Flash's local applicability comparison. Public
   reports can inform private researchers; private reports never flow back.
4. One fresh Opus 5.5 context through official Claude Code reconciles all
   six pairs, preserving evidence, dissent, gaps and human questions. This
   is research reconciliation, not a design verdict or a new workflow gate.
5. The runner checks each endpoint/model/data class and leak-checks every
   exact prompt before calling. It alone appends research, including
   original contributions, source receipts, input state and partial failures.
   Declaration or leak refusal stops; other incomplete runs exit nonzero.
6. Calls are finite and sequential: one per free model, eleven Flash calls
   and one judge, with no automatic retries or debate. Initial deadlines
   are 10 minutes per researcher, 15 for Opus and 150 for the whole run.
7. Explicit Stage-1 exploration keeps Haiku 5.5 and its recorded reason.
   No unrequested fallback follows a failed swarm or a leak BLOCK.
8. The public boundary is qualified offline on the pinned Pi with synthetic
   canaries before live calls. New free endpoints are contacted only after
   the decision merge, and actual public transport/web support is then
   recorded before any complete live swarm is claimed.

## Consequences

* The initial run has sixteen role invocations, rather than one; Opus uses
  Claude quota, as Q-5 accepts. This draft makes no cost-saving claim.
* Public questions are generic apart from the one-sentence topic, so free
  providers learn what a change is about (accepted in Q-6); Flash and Opus own the
  applicability comparison that cannot be delegated to free models.
* Paid Pi retains its already documented residual read risk; that is not an
  exemption from the stronger public-only boundary for free models.
* The review ladder and other phases stay unchanged. The six-topic result
  still hands off through `research.md` plus the maintainer's `decisions.md`.
* Doctrine, endpoint declarations, prompts and this ADR move in one decision
  pull request. Existing ADRs, numbered decisions and their continuity map
  are not rewritten; no agent writes an ADR answer or merge approval.

## Validation

* The change's criterion ledger names fault-bearing routing, boundary,
  evidence, judge, failure and deadline tests; `make verify` must be green.
* Offline pinned-Pi request captures must exclude synthetic private canaries
  and show local tools unavailable; argv mocks alone do not prove that.
* A post-merge public-only qualification records actual free-model and web
  support; unavailable components are failures, not successful research.
* Phase-6 review confirms six-topic evidence and the decision pull request
  adds only this ADR; its maintainer merge is the acceptance.
