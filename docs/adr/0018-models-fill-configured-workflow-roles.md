---
title: "ADR 0018 — Models fill configured workflow roles"
category: adr
status: accepted
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, models, effort, routing, kit]
---

# ADR 0018 — Models fill configured workflow roles

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends the concrete model/effort assignments
  of ADRs 0007, 0011, 0016 and 0017; supersedes no complete ADR and changes no
  D- or O-number's contract. Their non-selection rules remain effective.
* Review: the maintainer chose the direction in Q-1 to Q-5 of
  `plans/changes/central-models/decisions.md`, 2026-10-14. These are interview
  answers, not a recorded ADR answer. Acceptance is the merge commit and is
  written nowhere else; the header's review stays pending · Decider:
  maintainer · prepared by Codex.
* Date: 2026-10-14 · takes effect on merge.

## Context

The endpoint declaration lists permissions, but runner constants select models
and effort. Workflow tables, prompts, repository instructions and seven agent
definitions restate choices. Existing resolution tests guess display names;
neither effort nor all live instructions are held to a common setting
(`plans/changes/central-models/research.md`, read 2026-10-14 at `e048fa4`).

Earlier routing ADRs named concrete models and, in some cases, effort. Changing
one choice can therefore require an architecture amendment even though the
responsibilities and data boundaries remain unchanged. The maintainer asks for
one repository-local setting, generated tables, role-based ADRs and portable
format without inherited clearances (decisions Q-1 to Q-5, 2026-10-14).

## Decision Drivers

* A compatible model or effort change has one authoritative edit.
* A selection never grants data clearance or changes an execution contract.
* Human-readable routing and native agent settings agree with actual calls.
* Each repository owns its selections and endpoint/data permissions.

## Considered Options

* **Resolve workflow roles from the central declaration.** Runtime consumers
  read validated selections; generate the views clients and humans need.
  Requires a shared reader and a drift check.
* **Generate runnable constants from the declaration.** Fewer consumer
  changes, but stale executable copies can diverge at call time.
* **Keep model assignments in ADRs and maintain their copies.** Retains today's
  process, but each substitution repeats architecture paperwork and edits.

## Decision

Chosen option: "Resolve workflow roles from the central declaration", because
the authority of a selection stays with its repository while role contracts
continue to explain the workflow.

1. `model-endpoints.yaml` contains endpoint permissions and a distinct routes
   section for model, effort, fallback and manual/Stage-1 bindings. Shared
   profiles identify exact permitted models; role bindings choose them.
   The shared reader validates these relationships before clients start.
2. Permanent ADRs decide workflow responsibilities and their contracts.
   Current models and effort filling those roles are set only in the central
   declaration. A compatible binding-only substitution needs no ADR amendment
   solely for its model, effort or ladder order; the maintainer still merges
   its pull request. New endpoint approvals, changed role contracts and risks
   remain decisions under the existing protocol.
3. The runner's verbs, Claude Code agent selections, named research/review
   ladders and interactive-session suggestion consume that authority.
   An unconfigured swarm is reported as such; this decision neither authorizes
   new members nor implements swarm execution. An interactive suggestion
   does not launch a client or replace the explicit-model session contract.
4. The workflow's two routing tables and native agent selection fields are
   generated; phase prompts and repository instructions name roles. A block
   gate rejects disagreement with the setting. Historical evidence retains
   its original model identifiers and counts.
5. The kit transfers the format, resolver, runner, generator and a template
   with role/effort defaults. Template model bindings and endpoint clearances
   are unset; a target supplies its own values before any selection can run.
6. ADR 0007's checked-runner and data boundaries, ADR 0011's bounded ordered
   review rounds, ADR 0016's combined draft and spec-review responsibilities,
   and ADR 0017's taken-finding repair and fresh re-check remain effective.
   Their concrete assignments become historical upon this amendment; retries,
   failure triggers, read-only reviews, leak refusals and sandbox rules do not
   move into configurable model policy.

## Consequences

* Compatible substitutions become setting changes plus deterministic generated
  output, without editing code, prompts, tests or ADR bodies for identifiers.
* A resolver and generator become shared dependencies; invalid or absent
  settings must refuse, including in a freshly configured target repository.
* Native agent changes require regeneration and a new Claude Code session;
  existing sessions are not hot reloaded.
* This decision does not approve a model, vendor, capability or privacy claim.
  Stand-in tests prove selection propagation and refusals, not provider quality
  or a client's actual runtime enforcement.
* Implementation adds dated amendment notices to the four earlier ADRs,
  preserving their historical text. No D- or O-number changes, so neither the
  continuity map nor its validator changes.

## Validation

* The central-models criterion ledger names selection-mutation, malformed
  setting, no-launch refusal, generation/drift, revision and target-local tests.
* `python3 scripts/render_model_routes.py --check` and `make verify` pass after
  implementation; hosted CI runs the same routing check.
* Phase 6 checks the four amendment notices against the preserved contracts
  and Q-3; the decision PR's file list shows no new permissions or swarm work.
* The maintainer's merge accepts this proposal under ADR 0008. No agent records
  acceptance or an ADR answer before that merge.
