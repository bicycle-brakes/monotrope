---
title: "ADR 0021 — The review loop runs until a clean round: a free swarm first, then the ladder"
category: adr
status: accepted
created: 2026-10-14
last_reviewed: 2026-10-16
updated: 2026-10-16
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, review-loop, opencode-go, swarm]
---

# ADR 0021 — The review loop runs until a clean round: a free swarm first, then the ladder

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends ADR 0011 decisions 3 and 8 and
  ADR 0017 decision 6; supersedes no ADR. Amends no D- or O-number.
* Review: the maintainer chose the direction in Q-1 through Q-8 on
  2026-10-14 and corrected free admission and the Flash round in Q-9/Q-10
  on 2026-10-16 (`plans/changes/loop-until-clean/decisions.md`). Acceptance
  is the merge commit, recorded nowhere else; the header's review remains
  pending · Decider: maintainer · prepared by Codex through stage 2.
* Date: 2026-10-16 · takes effect on merge.

## Context

The loop currently stops at three rounds (ADR 0011 decision 3; ADR 0017
decision 6). It refused a needed fourth round in the first night run
(`docs/journal/handover/2026-10-12-night-run-first-rehearsal.md`, section 4).
A clean first round still admits round 2, and each round calls one model
(`plans/changes/loop-until-clean/research.md`, exploration at `e0cea42`,
2026-10-14). This does not meet the request to review until clean or the
implementation-review swarm decision.

On 2026-10-16 the maintainer clarified that all free Go models found by the
run's check enter automatically, and that the three named Flash models
review together after the free swarm. These answers replace the earlier
draft's undeclared-free-model exclusion and sequential Flash interpretation.
The existing ADR answer names this amendment as 0021.

The repository-pinned Pi and its isolation remain ADR 0019's launch path.
Source inspection of the installed Pi on 2026-10-16 shows a static Go model
catalog behind `--list-models`: the Go provider imports catalog data and
supplies no `fetchModels` callback (`pi-ai/dist/providers/opencode-go.js`;
`pi-ai/dist/models.js`; `pi-coding-agent/dist/cli/list-models.js`). Therefore
checking the installed list per run does not measure the vendor's live
availability or whether a call is billed free.

## Decision Drivers

- End on a review with no accepted findings rather than a fixed round count.
- Honor the free-first and parallel-three-Flash order the maintainer stated.
- Bound paid review by declared models without repeating the final rung.
- Admit unread terms only for the diff-confined discovered free class.
- Escalate when repairs keep generating findings, and retain the existing
  declaration, leak, row-decision, verification and release guards.

## Considered Options

- **Free swarm, paid Flash swarm, then single paid rungs until clean:** the
  chosen order provides cheap parallel views before successive paid views;
  merging members and retaining stage history add runner state.
- **The three Flash models alongside the free swarm:** would guarantee paid
  Flash review even on a clean free result; Q-10 chose separate rounds.
- **Only manually declared free models:** would require a repository edit
  for each new offer; Q-9 instead chose automatic discovered membership.
- **Higher fixed cap or repeating the last model:** simpler scheduling, but
  either recreates the arbitrary stop or removes the chosen ladder bound.

## Decision

Chosen option: "Free swarm, paid Flash swarm, then single paid rungs until
clean", because it implements the maintainer's recorded answers, including
the corrected order and automatic free admission.

1. **Clean ends the loop at every round number.** A completed round is clean
   once every row is decided and none has Status beginning `taken` or
   `fixed`; no rows or all rejected rows count. A clean free round ends the
   loop before any paid review. This amends ADR 0011 decision 3's compulsory
   second round, three-round cap and special round-3 admission rule.
2. **Round 1 is the discovered free Go swarm.** Before each fresh loop run,
   the runner checks the pinned Pi's `--list-models` table, selecting exact
   provider `opencode-go` and ids ending in `-free`, never provider `opencode`
   (Zen). All distinct matches enter automatically without individual YAML
   entries. Record check date/time, source, Pi version and exact list in the
   run record. A failed, unreadable or empty check refuses the run. State
   the pin-limited freshness and unmeasured free billing explicitly.
3. **The free class is declared and confined.** The endpoint entry declares
   this class and the accepted unread retention/training terms (Q-8/Q-9).
   Admission requires membership in this run's discovery plus the free-only
   purpose; it does not relax generic paid or interactive model declarations.
   Only implementation source/test diff hunks reach these calls, with no
   repository-reading instructions, tools, context loaders or whole-worktree
   prompt. Existing per-call declaration and leak checks remain mandatory.
4. **Round 2 is the parallel paid Flash swarm.** Its eligible members are
   DeepSeek V4.1 Flash, MiMo-V2.6-Flash and LongCat-2.0. Later rounds take
   one eligible model at a time in Q-1 order: GLM-5.3-Flash, Qwen3.8 Flash,
   GPT 6 Luna, Claude Haiku 5.5, MiniMax M2.7, MiMo-V2.6-Pro. The configuration
   holds ids/order; all paid calls retain the existing read tools. Q-10
   replaces Q-5's round number without changing parallel Flash review.
5. **Paid terms are read before admission.** Record dated retention/training
   readings for paid models; skip and name in the handover any whose terms
   retain/train or cannot be read (Q-7). No address/model substitution follows
   a refused id. An empty eligible Flash stage is named and skipped without
   completing an empty review round.
6. **Each swarm produces one decided round and one repair batch.** Calls
   run concurrently in separate scratch environments; one parent merges
   rows into unique ids with their actual reviewers and names failures.
   A partially successful swarm stands with that limitation visible; an
   all-failed swarm completes no round. Explicitly rejected duplicates remain
   visible. The orchestrator decides and repairs before another review,
   requiring `make verify` green after repair as today.
7. **The repair brake and ladder bound are distinct escalations.** Two
   consecutive rounds each having accepted findings all caused by repairs
   (Origin `fix-r`) stop and go to the maintainer (Q-3). Exhausting eligible
   stages with accepted findings also stops and reports to the maintainer
   (Q-6); no final-model repeat follows. A fixed row still counts as taken:
   ADR 0017 decision 6 keeps that rule and loses only its three-round limit.
8. **The call bound replaces ADR 0011 decision 8's three-call assumption.**
   Per completed loop run there is at most one review call per discovered
   free member and one per eligible paid model: with all nine paid models,
   at most eight completed rounds and F + 9 member calls, F being the run's
   free count. Skipped paid members shorten this bound. Failed attempts and
   separate compatibility probes are audited additional calls, not included
   in that completed-run bound; no new money cap is claimed. Prices and
   subscription limits remain sourced in the endpoint entry.
9. **Release preserves admission history.** Snapshot membership/stages and
   completed-round state survive transfer to findings and deletion of the
   external record. Neither release nor edited configuration resets the
   clean stop, repair brake or consumed stages. The phase-6 verdict still
   precedes release; the reviewer's own session never repairs.

## Consequences

- A clean free result may end review without any paid reviewer; this is
  explicitly accepted in Q-10. A partial swarm result can also be clean,
  with failed members named rather than presented as successful coverage.
- New free Go models can receive implementation diffs under unread terms
  immediately. This exception does not authorize broader repository input,
  Zen models or paid models on unread terms.
- The loop can cost more than three single calls. Its finite paid membership
  bounds a completed pass, while the changing free catalog determines F;
  failed attempts, probes and subscription consumption remain visible.
- The runner owns free discovery and history; the orchestrator owes paid
  terms readings, row decisions, green repair checks and skipped-model
  handover notes. The installed catalog cannot promise the live free offer.
- Live doctrine and tests move together. Older ADR bodies remain historical;
  their round-budget text is read with this amendment.

## Validation

- The change's `plan.md` criterion ledger maps all 16 criteria to tests,
  including concurrency, dynamic Go admission, real pinned-Pi loopback
  confinement, terms exclusion, both swarms, stops and release continuity.
- The verification commands in that plan and `make verify` must pass.
- Phase 4 records terms readings/skips, compatibility-probe evidence and the
  change's own new review-loop result with their commits in the decision PR.
- Merge, not this draft or its pending review header, makes the amendment
  effective; no maintainer answer is written by the drafting agent.
