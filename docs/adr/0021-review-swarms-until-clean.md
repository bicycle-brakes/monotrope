---
title: "ADR 0021 — The review loop runs until a clean round: a free swarm first, then the ladder"
category: adr
status: accepted
created: 2026-10-14
last_reviewed: 2026-10-16
updated: 2026-10-17
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
  2026-10-14 and corrected free admission, the Flash round, live refresh and
  configurable selection in Q-9/Q-10 and the addenda of 2026-10-16
  (`plans/changes/loop-until-clean/decisions.md`). Acceptance
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
The final decisions addendum of 2026-10-16 (after `a0d5bc8`) records a
corrected Pi 1.2.0 source reading: `core/remote-catalog-provider.js` obtains
models from `pi.dev` and caches them for four hours;
`package-manager-cli.js` forces refresh through `pi update --models` (the
flag spelling the pinned CLI measures in phase 4).
The maintainer requested live retrieval and retained Pi's catalog after
its distinction from Go's own endpoint was explained. They also requested
easy later changes to the free-model rule. Catalog membership still does
not measure whether a model call is actually billed free.

## Decision Drivers

- End on a review with no accepted findings rather than a fixed round count.
- Honor the free-first and parallel-three-Flash order the maintainer stated.
- Bound paid review by declared models without repeating the final rung.
- Admit unread terms only for the diff-confined discovered free class.
- Refresh the catalog live before each fresh run and keep selection editable
  through an ordinary configuration PR.
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
   the runner forces `tools/pi/pi update --models` in its scratch agent
   directory, then reads `tools/pi/pi --list-models` there. Failed/timed-out
   refresh refuses before listing or model calls; no stale-cache fallback.
   The YAML rule holds provider (initially `opencode-go`), id suffix
   (initially `-free`), and include/exclude lists with date and reason per
   entry. Include only ids present under the configured Go provider in that
   catalog; exclusions win. Never admit provider `opencode` (Zen). All
   selected ids enter without individual declarations; no free id/suffix
   literal belongs in runner code. Invalid rules, unreadable/empty selection
   or failed listing refuse the run. Record UTC check time, source `pi.dev`,
   Pi version, rule, catalog and selected ids. Changes apply to fresh runs
   through an ordinary YAML PR. State the live intermediary and unmeasured
   free billing explicitly.
3. **The free class is declared and confined.** The endpoint entry declares
   this class and the accepted unread retention/training terms (Q-8/Q-9).
   Admission requires membership in this run's discovery plus the free-only
   purpose; it does not relax generic paid or interactive model declarations.
   Only implementation source/test diff hunks reach these calls, with no
   repository-reading instructions, tools, context loaders or whole-worktree
   prompt. Existing per-call declaration and leak checks remain mandatory.
4. **Round 2 is the parallel paid Flash swarm; later rounds go cheapest first.**
   The Flash swarm is a hand-kept list (`flash_swarm`) of eligible paid
   models; the runner never changes it, and prints a notice (and writes one
   record line) when it is not the three admitted models with the highest
   `anfragen_5h`. The paid ladder is a set (`modelle`): the runner orders it by
   a declared cost value, `anfragen_5h` in each model's `modelle_terms` record
   (the Go page's "Estimated requests", Go column, requests per 5 hours, with
   its reading date and source), descending, ties by id; a model without the
   value goes last and is named on stderr and in the record (maintainer,
   2026-10-17, Q-13, replacing the hand-ordered list). Later rounds take one
   eligible model at a time in that order, Flash members excluded while they
   are in the swarm. When a Flash member fails (nonzero exit, timeout, empty
   answer), the runner calls the cheapest admitted ladder model that is not in
   the round and not consumed, on the same paid prompt; if that one fails,
   the next, each model at most once, until one answers or the ladder is
   spent. A replacement is consumed: it is no later rung. Each swap is written
   `<model> failed: <reason>; replaced by <model>` in the loop record and
   printed on stderr; the reason carries the last line of Pi's standard
   error. The configuration holds ids and cost values; all paid calls retain
   the existing read tools. Q-10 replaces Q-5's round number without changing
   parallel Flash review. The free stage selects only ids in the freshly
   fetched `opencode-go` overlay of the forced refresh, not ids only Pi's
   shipped list carries.
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
  handover notes. The live Pi catalog is an intermediary rather than Go's
  own endpoint, and cannot promise actual free billing. Rule changes remain
  configuration edits; in-flight runs retain their original snapshot.
- Live doctrine and tests move together. Older ADR bodies remain historical;
  their round-budget text is read with this amendment.

## Validation

- The change's `plan.md` criterion ledger maps all 16 criteria to tests,
  including concurrency, forced live refresh, configurable Go admission, real pinned-Pi loopback
  confinement, terms exclusion, both swarms, stops and release continuity.
- The verification commands in that plan and `make verify` must pass.
- Phase 4 records terms readings/skips, compatibility-probe evidence and the
  change's own new review-loop result with their commits in the decision PR.
- Merge, not this draft or its pending review header, makes the amendment
  effective; no maintainer answer is written by the drafting agent.
