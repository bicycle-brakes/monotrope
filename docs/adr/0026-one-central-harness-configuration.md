---
title: "ADR 0026 — One central harness configuration with staged migrations"
category: adr
status: accepted
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, configuration]
---

# ADR 0026 — One central harness configuration with staged migrations

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends no decision and supersedes no ADR.
* Review: direction chosen by the maintainer in the five interview answers
  of 2026-11-10 (`plans/changes/central-config/decisions.md`) · acceptance is
  the merge commit; no agent records an approval before it · Decider:
  maintainer · prepared by Codex.
* Date: 2026-11-10 · takes effect on merge.

## Context

Harness values are split between runner constants, `model-endpoints.yaml`,
`research-swarm-limits.yaml`, the gate list, prompts and prose. The exploration
of 2026-11-10 identifies differing reader contracts and repeated model/limit
statements (`plans/changes/central-config/research.md`, second exploration).
The existing gate-list generator and strict research-limit reader provide
local precedents for a declaration that readers and checks actually enforce.

The maintainer chose values with prompt placeholders, one directory with a
shared schema/validator, checked hand-written prose, migration of all three
existing declarations, and a staged rollout (interview answers Q-1 through
Q-5, 2026-11-10). This record proposes those contracts for merge; it does
not claim the later migrations have already happened.

## Decision Drivers

* One authoritative place for each migrated value, easy to change by pull request.
* Small topic files and pull requests under about 800 lines.
* Visible refusal on invalid settings and visible drift in prose/consumers.
* Existing data admission, leak checks and human reservations remain effective.
* Waiting consumers can adopt the shared contract without a wholesale rewrite.

## Considered Options

* **One directory, one shared schema/validator, explicit bindings:** small files
  and one contract, at the cost of inventorying readers for each migration.
* **One large file:** fewer paths, but more collisions and a longer file as
  models, rounds, lanes, limits and metrics rules accumulate.
* **Independent configuration files/readers:** cheap to retain, but differing
  contracts and repeated settings remain possible.
* **Generate all prose and store prompt text as data:** reduces hand edits but
  gives up the hand-written documentation and values-only boundary chosen
  by the maintainer.

## Decision

Chosen option: "One directory, one shared schema/validator, explicit bindings",
because it gives every migrated setting one authority while preserving small
files and readable hand-written documentation.

* `config/harness/` holds values grouped by topic. One shared schema and one
  validator reject missing, unknown, ambiguous or invalid inputs without defaults.
* Prompts remain text. The runner resolves setting placeholders before the
  existing leak check and dispatch; configuration never stores prompt prose.
* Documentation remains hand-written. Marked literal values must agree with
  the central source, and required bindings cannot disappear silently.
* The first slice establishes the mechanism using the unchanged writing-session
  limit. It does not implement session admission or change parallel-work policy.
* Migration order is skeleton, models/routes with the endpoint register,
  review seating, limits with swarm limits, then the gate list. Watchdog,
  heartbeat, size and metric/decision-rule consumers adopt it as they land.
* Each migration switches all its live readers and removes duplicate authority;
  settings not yet migrated keep their existing source until that slice lands.
* The gate list moves only through a later decision pull request that preserves
  its reservation and generated CI contract. Adding the first configuration
  gate at the current path is not that move.

## Consequences

* A setting change can require both a value edit and a marked prose edit in the
  same pull request; documentation cannot silently state another value.
* A prompt template no longer displays all literal values when read alone.
* During rollout, consumers later in the sequence retain scattered settings;
  the central-configuration parent stays open until the migrations complete.
* The drift check measures registered bindings and named declarations, not
  arbitrary semantic equivalence between unrelated literals or aliases.
* The orchestrator owns held-path wiring after accepted runner attempts;
  moving settings never widens endpoint permissions or bypasses leak checking.

## Validation

* The first slice's criterion ledger names mutation cases for malformed data,
  changed settings, missing/stale bindings, duplicate declarations and gate wiring.
* `make verify` must run the shared check locally and through generated hosted CI.
* Each later migration records its live reader inventory and regression evidence
  before removing its old source; the gate-list migration gets its own decision PR.
