---
title: "Decisions — central-config"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-twvx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, configuration, central-config]
---

# central-config — Decisions

Class: architectural (bead coding-harness-twvx).

The answers are the maintainer's, given in the conversation on 2026-11-10 by
choosing among options; the quoted words are the label of the chosen option.
The decision statements below each answer are worded by the orchestrator; the
"accepting that" clause restates the consequence shown with the option.

## Q-1 · What belongs in the central configuration

asked: 2026-11-10
answer: "Werte, Prompts lesen sie" — values only (numbers, model names, lists, thresholds); prompts stay text and get placeholders the runner fills from the configuration; no value is stated twice.
answered_by: maintainer
status: answered
context: |
  Topic: the scope of the central harness configuration.
  Intention: decide what goes in before a spec is written.
  Today: values sit in constants of scripts/stage2.py, in model-endpoints.yaml, in tables of the documentation and in sentences of the prompts.
  Repository change: a new validated configuration; prompts become templates with placeholders.
  Architecture change: an ADR; the configuration becomes the one source of these values.

In the context of the scope of the central harness configuration, facing
values that today sit in runner constants, YAML files, documentation tables
and prompt sentences, we decided that the configuration holds values only and
that prompts read them through placeholders the runner fills, to achieve one
source for every value without turning prompts into configuration, accepting
that prompts become templates and a prompt can no longer be read alone with
its numbers in it — 2026-11-10

## Q-2 · One file or one directory

asked: 2026-11-10
answer: "Ein Ordner, ein Schema" — one directory with a few files by topic (models, review, lanes, verify, limits), one shared schema, one validator.
answered_by: maintainer
status: answered
context: |
  Topic: the form of the central configuration.
  Intention: quick to read and a one-line change, also when it grows.
  Today: several single files in the repository root, each with its own validator.
  Repository change: one directory of YAML files, one schema, one validator.
  Architecture change: part of the same ADR.

In the context of the form of the central configuration, facing a set of
values that will grow and several pull requests that change them at the same
time, we decided that one directory with a few files by topic under one shared
schema and one validator, to achieve files that fit one screen and fewer
colliding pull requests, accepting that a reader looks in more than one file —
2026-11-10

## Q-3 · How prose stays in step

asked: 2026-11-10
answer: "Prüfer findet Abweichungen" — documentation stays hand-written; a gate compares marked numbers with the configuration and fails on a difference.
answered_by: maintainer
status: answered
context: |
  Topic: how docs/WORKFLOW.md and AGENTS.md agree with the configured values.
  Intention: a changed value must not leave the documentation stating another.
  Today: numbers are written by hand in prose; a difference is found by chance.
  Repository change: a gate over marked numbers in prose.
  Architecture change: part of the same ADR.

In the context of prose that states configured values, facing documentation
and instruction files that repeat numbers by hand, we decided that the prose
stays hand-written and a gate compares its marked numbers with the
configuration and fails on a difference, to achieve readable documentation
that cannot silently disagree, accepting that a change of a value takes a
second line in the same pull request — 2026-11-10

## Q-4 · The existing configuration files

asked: 2026-11-10
answer: "Alle drei umziehen" — model-endpoints.yaml, research-swarm-limits.yaml and gates.yaml all move into the central configuration.
answered_by: maintainer
status: answered
context: |
  Topic: the relation of the new configuration to three existing files.
  Intention: one place per value.
  Today: model-endpoints.yaml (models, endpoints, data terms), research-swarm-limits.yaml (swarm limits), gates.yaml (gates; reserved, agents do not edit it).
  Repository change: the three files move under the shared schema.
  Architecture change: part of the same ADR; the move of gates.yaml also touches the reservation rules and the CI wiring and is a decision pull request of its own.

In the context of three existing configuration files beside the new central
configuration, facing values that would otherwise stay in four places, we
decided that all three files — model-endpoints.yaml, research-swarm-
limits.yaml and gates.yaml — move into the central configuration, to achieve
one place for every value, accepting that the move of gates.yaml needs a
decision of its own on the reservation rules and touches the CI wiring —
2026-11-10

## Q-5 · The order of the work

asked: 2026-11-10
answer: "Gerüst, Modelle, Review, Rest" — (1) ADR, directory, schema, validator and a first small value (lane count, verify slots); (2) models and routes with the move of model-endpoints.yaml; (3) review seating; (4) limits and swarm limits; (5) gates.yaml last, as a decision of its own.
answered_by: maintainer
status: answered
context: |
  Topic: the steps in which the central configuration is built.
  Intention: pull requests under about 800 lines; six beads wait for the configuration.
  Today: waiting consumers are review seating (bead coding-harness-3rtn), the implement route (bead coding-harness-9ycy), the size gate (bead coding-harness-g8g7), lane watch and heartbeat (beads coding-harness-5q2p, coding-harness-6pn3) and metrics (bead coding-harness-nqaf).
  Repository change: several pull requests in sequence.
  Architecture change: one ADR in the first step; the move of gates.yaml is its own decision pull request.

In the context of the order in which the central configuration is built,
facing six waiting consumers and a size limit of about 800 lines per pull
request, we decided that the order is skeleton with a first small value, then
models and routes, then review seating, then limits, and gates.yaml last, to
achieve small pull requests and an early proof that the mechanism carries,
accepting that the consumers that come later keep their scattered values for a
while — 2026-11-10
