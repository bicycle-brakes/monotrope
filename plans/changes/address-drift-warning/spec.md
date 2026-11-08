---
title: "Spec — address-drift-warning"
status: draft
implementation_status: partial
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-x2g9
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, opencode-go, address]
class: bounded
appetite: 2
adr_files: []
neighbours: [plans/changes/go-access-point/spec.md, plans/changes/research-swarm/spec.md]
---

# Spec — address-drift-warning

Catalog differences from the declared OpenCode Go address are visible without
changing which definitions may run (bead `coding-harness-x2g9` — warn on a
differing Go address). Research: `research.md`. Intent: `decisions.md#Q-1`.
This is a proposed change, not an implementation report.

## Problem

- The approved interview skip describes silent address differences, but the
  predecessor already implements same-host path warnings across Go launches;
  its released records demonstrate them. Rebuilding that mechanism would
  duplicate existing policy (`research.md`, "The warning machinery is
  implemented and wired" and "The drift warning fires today", read
  2026-11-07).
- A remaining silent case is an explicit, valid same-host base with a wire
  API absent from the address record: the shared assessment admits it with
  no notice. Research selection also collects notices only after eligibility
  filtering, hiding the address difference of an unmeasured API
  (`research.md`, "Draft gap check", reproduced offline at `a40f22e5` on
  2026-11-07).
- The original warn-only intention does not authorise bypassing the accepted
  destination policy. Foreign hosts and missing defaults already have refusal
  rules; this change must preserve them (ADR 0024, "Decision", and
  `research.md`, "The declared address record", read 2026-11-07).

## Terms

- **Address record:** the existing `adresse` mapping on the `opencode-go`
  entry of `model-endpoints.yaml`, with its host and bases keyed by wire API.
- **Wire API:** the model definition's `api`, identifying its request format;
  an API differs here when its name is absent from the record's API keys.
  Any API present in that record is compared with its own recorded base.
- **Address-admissible row:** a definition accepted by the existing address
  policy; this alone grants neither model eligibility nor permission to send.

## Acceptance criteria

1. When an address-admissible row uses a recorded API with a different
   same-host path, its warning identifies the provider/model, recorded path
   and observed path.
   *Refuted by:* either path or the model is missing, or the existing path
   warning disappears.
   *Basis:* `decisions.md#Q-1`; `research.md`, existing path-warning machinery.

2. When an address-admissible row explicitly supplies a base and a non-empty
   wire API absent from the address record, its warning identifies the
   provider/model, observed API and declared API names without inventing a
   recorded path for that API.
   *Refuted by:* the difference stays silent, a declared API is presented as
   unrecorded, or the warning borrows another API's path as its expected base.
   *Basis:* `decisions.md#Q-1`; `research.md`, "Draft gap check".

3. When review catalog handling or research catalog selection encounters an
   address-admissible row with either difference, the warning reaches its
   existing catalog diagnostic evidence even if a later eligibility filter
   excludes the row.
   *Refuted by:* review preparation loses the notice or research's address
   notices omit an unmeasured-API row that still has its exclusion reason.
   *Basis:* `decisions.md#Q-1`; `research.md`, "Draft gap check".

4. When an otherwise permitted Go launch uses a row with an unrecorded API,
   its warning reaches the same launch evidence as an existing path warning.
   *Refuted by:* a review round, availability probe, research launch or
   initial interactive session loses the notice from its existing audit
   record; console-only output does not satisfy durable evidence.
   *Basis:* `decisions.md#Q-1`; `research.md`, launch-site inventory.

5. When the effective address matches the record for its API under existing
   equivalence rules, no address-difference warning is emitted.
   *Refuted by:* a recorded path, one trailing slash, an explicit HTTPS port
   443, or a missing base filled from that API's record produces a warning;
   a second recorded API is treated as different merely for being second.
   *Basis:* `decisions.md#Q-1`; `research.md`, existing default/path policy.

6. When a warning is added, address admission, effective definition and all
   independent eligibility decisions remain those of the existing policy.
   *Refuted by:* the warning drops or rewrites an otherwise admitted overlay
   row, admits a foreign/malformed destination, guesses a default for an
   unmapped API, or bypasses terms or measured-API checks.
   *Basis:* `decisions.md#Q-1`; `research.md`, accepted predecessor policy.

7. When a diagnostic includes an address difference, it preserves the existing
   sanitisation boundary for untrusted catalog values.
   *Refuted by:* a notice echoes credential-bearing URLs or an unreadable API
   value with control characters instead of a safe description.
   *Basis:* `research.md`, sanitised shared assessment and evidence tests.

## Non-goals

- Updating the recorded Go address, reading live documentation, refreshing a
  live catalog, or measuring/admitting additional wire APIs.
- Changing refusal rules, defaults, terms, model selection, saved-state
  formats, or the scope of initial interactive-session destination checks.
- Consolidating repeated notices across models, launches or review rounds.
- Reopening or completing the predecessor's tracker work or rewriting its
  historical artifacts. No design phase runs for this bounded change.

## Protected areas

- `model-endpoints.yaml` and `docs/adr/`: the accepted address policy and
  orchestrator-owned record are inputs, not edits in this change.
- `provenance.yaml`, `decisions/`, `AGENTS.md`, `README.md`, `prompts/`,
  `templates/`, `.github/`, `.claude/`, `.codex/`, `.agents/`, `.pi/`,
  `.mcp.json`, `CLAUDE.md` and `.beads/`: no governance, permissions or
  installation change is needed.

## Definition of Done

- Targeted offline regressions and `make verify` are green at the PR head.
- New API-warning tests fail on the pre-change implementation and pass with
  the fix; the existing path-warning and refusal tests remain green.
- Moved with the code: this change's `spec.md`, `plan.md`, `research.md` and
  `findings.md`; `plans/INDEX.md` is regenerated by the orchestrator/runner.
  No endpoint declaration, workflow document or ADR changes.
- The PR file list shows protected areas untouched and non-goals unbuilt.
- The PR closes the differing-address warning work item, and the closing
  commit carries `Closes-Bead: coding-harness-x2g9`.
- Special runs: none; synthetic catalog rows and transport stand-ins suffice.

## Open decisions

None open.

- [DETAIL] Preserve the approved `bounded` class and the predecessor's
  admission rules: the interview authorises warnings, not new permissions.
- [DETAIL] An unrecorded API is compared with the set of declared API names,
  not one arbitrarily chosen API; this remains meaningful with several maps.
- [DETAIL] Reuse existing notice fields and audit channels; the wording is
  revisable, and API names unsafe to display get a safe description.
- [DETAIL] Set a two-hour implementation appetite including repairs because
  the change extends one shared assessment and one selector's evidence flow.

These reversible details are agent choices with their reasons recorded here.
