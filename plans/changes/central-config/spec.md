---
title: "Spec — central-config"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-twvx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, configuration]
class: architectural
appetite: 3
adr_files: [docs/adr/0026-one-central-harness-configuration.md]
neighbours: [plans/changes/review-loop-deep-a/spec.md]
---

# Spec — central-config

Establish one validated source for harness settings, beginning with the
existing writing-session limit and the machinery its later consumers need
(bead coding-harness-twvx — central harness configuration). Research:
`research.md`; maintainer answers: `decisions.md`, Q-1 through Q-5.

## Problem

- Model choices, timeouts and limits live in Python constants, separate YAML
  files and prose; a setting change can leave these readers disagreeing
  (`research.md`, second exploration, 2026-11-10).
- There are working local precedents, but no common configuration contract:
  the gate list drives CI generation, while research limits have their own
  strict reader (`research.md`, “Declarations that already exist”, 2026-11-10).
- The maintainer requires small, ordered migrations rather than one large
  replacement. The first useful step must work while the existing model,
  review and gate declarations retain their present authority
  (`decisions.md#Q-5`, answered 2026-11-10).

## Terms

- **Owned setting:** a value explicitly migrated into the central directory;
  in this first slice, only `lanes.writing_sessions_per_repository`.
- **Marked literal:** a readable value in hand-written prose linked to an
  owned setting so a check can compare them; it is not a second authority.
- **Prompt placeholder:** a reference to an owned setting, resolved by the
  runner as text before its existing leak check and model dispatch.

## Acceptance criteria

1. When the first slice is merged, its central directory declares the current
   maximum of two writing sessions per repository exactly once as a value.
   *Refuted by:* no owned setting, a changed initial policy, or another
   authoritative declaration of this setting remains in live inputs.
   *Basis:* decisions.md#Q-1, decisions.md#Q-2, decisions.md#Q-5.
2. When central settings are read, one shared schema and validator determine
   which topic files, keys and value types are accepted.
   *Refuted by:* a topic has a separate schema, an unknown file or key is
   silently accepted, or a Boolean/string/non-positive number is a valid
   writing-session count.
   *Basis:* decisions.md#Q-2.
3. If an owned configuration file is missing, unreadable, invalid UTF-8,
   malformed YAML, ambiguous through duplicate or merge keys, or invalid
   against the schema, its consumer refuses with the file and reason.
   *Refuted by:* a consumer supplies a fallback value, dispatches using that
   file, or presents an unhandled traceback instead of the diagnostic.
   *Basis:* decisions.md#Q-1, decisions.md#Q-2.
4. When a migrated phase prompt is composed, its setting placeholders become
   literal values from a single captured configuration for that composition.
   *Refuted by:* an unresolved/unknown/malformed reserved placeholder reaches
   dispatch, a configuration edit mixes values in that composition, or the
   next composition still uses a previous configuration.
   *Basis:* decisions.md#Q-1.
5. When the implement prompt is prepared, it states the configured
   writing-session limit through a placeholder resolved before leak checking.
   *Refuted by:* the prompt hard-codes the count, ignores a valid changed
   count, or the exact outgoing resolved text bypasses the existing leak check.
   *Basis:* decisions.md#Q-1, decisions.md#Q-5.
6. When marked prose is checked, every declared occurrence of an owned value
   agrees with the configuration.
   *Refuted by:* changing or deleting the marker around the session count in
   `AGENTS.md`, naming an unknown setting, or changing its displayed number
   leaves the check green.
   *Basis:* decisions.md#Q-3.
7. If a live consumer redeclares the owned setting as a numeric constant or
   replaces its registered prompt placeholder with a literal, the drift
   check fails and names the location.
   *Refuted by:* a planted assignment to the owned setting's canonical name,
   its uppercase spelling, or a planted literal at the migrated prompt site
   passes the check.
   *Basis:* decisions.md#Q-1, decisions.md#Q-3.
8. When the normal verification job runs, invalid configuration or drift in
   an owned binding makes it fail through the existing single gate list.
   *Refuted by:* the standalone checker fails but local verification or the
   generated hosted workflow omits its blocking gate.
   *Basis:* decisions.md#Q-2, decisions.md#Q-3, decisions.md#Q-5.
9. While only the first slice is implemented, the documented migration order
   preserves existing authorities until each later slice replaces its readers.
   *Refuted by:* the first slice moves any of the three existing declarations,
   changes model routing/review policy, or claims the full migration complete.
   *Basis:* decisions.md#Q-4, decisions.md#Q-5.

## Non-goals

- This slice does not move `model-endpoints.yaml`,
  `research-swarm-limits.yaml` or `decisions/gates.yaml`. Subsequent pull
  requests migrate models/routes, review seating, limits, then the gate list;
  moving the gate list needs its own decision on reservations and CI wiring.
- No scheduler, session admission enforcement, verify-slot implementation,
  retry change, model selection change, dashboard, metrics collector or
  automatic tuning. Future settings for these areas enter with their consumers.
- No configuration defaults for unimplemented consumers, environment overlays,
  secrets, executable expressions, prompt prose stored as configuration or
  live reload of an already composed prompt.
- No rewriting historical decisions, research, handovers or archived changes
  to reflect current settings; no changes to customer instances.

## Protected areas

- Existing endpoint admissions, leak policy and routing: this is a source
  migration mechanism, not permission to change what a model may receive.
- The gate list's current path and reservation: adding the first checker
  does not move the list or relax who can change it.
- Existing ADRs, decision answers and tracker state: no answer is inferred
  or recorded, and the central-configuration parent is not closed after
  the skeleton alone.

## Definition of Done

- `make verify` is green after orchestrator bootstrap edits; targeted tests
  demonstrate the refusal and drift cases without a live model call.
- The same decision pull request carries the new ADR, the configuration,
  shared reader/checker, migrated prompt binding, marked session-limit prose
  and gate/CI/kit/provenance wiring named in `plan.md`.
- The pull request's file list shows the protected areas preserved and the
  non-goals unbuilt. The ADR and design retain the ordered follow-on slices.
- The skeleton contributes to the central-configuration parent (bead
  coding-harness-twvx); it does not close it. Its eventual closing pull
  request carries `Closes-Bead: coding-harness-twvx` after all migrations.
- Special runs: isolated mutation checks named in the criterion ledger,
  reported with their commit in the implementation pull request; no paid calls.

## Open decisions

None open. The five maintainer answers stand unchanged.

- `[DETAIL]` — The first small value is the existing writing-session count,
  not a new scheduler setting: it is already stated in `AGENTS.md`, whereas
  the verify-slot consumer is not present in this worktree. The current count
  stays two. This selects the lane-count proof permitted by Q-5.
- `[DETAIL]` — Use `config/harness/` and a three-hour phase-4 stop for this
  skeleton, repairs included; names and the stop are reversible and no prior
  appetite is stated. The design fixes the schema and binding syntax.
- `[DETAIL]` — The gate covers registered bindings and canonical named
  declarations of migrated settings. It cannot prove that an unrelated number
  or an arbitrarily renamed variable has the same meaning. Each later migration
  must inventory and register its actual readers before claiming ownership;
  the remaining scattered settings are deliberately outside this slice.
