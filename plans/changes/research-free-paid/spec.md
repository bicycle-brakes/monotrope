---
title: "Spec — research-free-paid"
status: draft
implementation_status: partial
date: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-wb40
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, free-selection, research-swarm]
class: feature
appetite: 4
change: research-free-paid
adr_question: {proposed: "no", reason: "This consolidates existing free-model and destination restrictions without changing provider admission, data boundaries or the research and review protocols."}
adr_files: []
neighbours: []
---

# Spec — research-free-paid

Both swarms select free models through one rule implementation, and an offline
contract catches a pinned Pi catalog that breaks either preparation before
merge (bead `coding-harness-wb40` — shared free selection and preparation proof).
Research: `research.md`. Maintainer answers: `decisions.md`.

## Problem

- Research dated 2026-11-05 records two independent free selectors. The review
  loop drops an id admitted as paid; research does not. Pi 1.5.0 exposes
  `beam-free`, which `opencode-go.modelle` admits as paid, so research prepares
  a free candidate that its later admission cannot safely use. The maintainer
  records the blocked preparation in `decisions.md#Q-1`.
- The earlier repair covered review preparation alone despite naming both
  paths in its plan. Research's catalog and availability tests did not expose
  the collision (`research.md`, "What exists today"). Copying that guard would
  leave the next free-model rule dependent on two coordinated repairs.
- Existing real-Pi contracts do not run both preparations against the shipped
  catalog; a catalog upgrade can therefore pass while research stops in
  operation (`decisions.md#Q-3`, answered 2026-11-05).

## Terms

- **Paid admission:** membership in the `opencode-go` entry's `modelle`, even
  when the id ends in `-free` or its terms record is skipped or expired.
- **Shared free selection:** provider, fresh-catalog membership, plain id,
  suffix/include/exclude policy, paid-admission exclusion, applicable global
  exclusions and destination admission, evaluated in one component.
- **Research eligibility:** the existing additional fresh-Pi validity and
  models.dev tool-support/deprecation checks needed by a public researcher.
  Reviewers have no tools and need no such capability evidence.
- **Offline preparation contract:** production preparation logic exercised
  with the installed, exactly pinned Pi catalog as input, local source
  stand-ins and synthetic successful probe results; no hosted model request.

## Acceptance criteria

1. When review and research prepare free candidates, both use the same shared
   free-selection component.
   *Refuted by:* Either preparation retains an independent implementation of
   the common membership rules or bypasses the shared selector.
   *Basis:* decisions.md#Q-1.

2. When both preparations receive the same fresh catalog, equivalent effective
   free policies and equivalent candidate eligibility, their selected free
   membership before reachability probes is identical.
   *Refuted by:* An otherwise eligible id is selected by only one preparation,
   including an id admitted as paid whose name ends in `-free`.
   *Basis:* decisions.md#Q-1.

3. When a default-policy preparation encounters a paid-admitted id matching
   the free rule, it drops that id before free probes and continues with the
   remaining eligible free candidates.
   *Refuted by:* `beam-free` or another such id receives a free probe, enters
   a free receipt, or makes either preparation refuse solely for the collision.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3.

4. When the shared selection applies a caller's policy, it preserves that
   policy's provider, fresh-only membership, include/exclude meaning and
   applicable global exclusions.
   *Refuted by:* A wrong-provider, baseline-only, malformed or excluded id is
   selected; review loses its additive includes; research loses its explicit
   include restriction or its refusal of an ineligible explicit include.
   *Basis:* decisions.md#Q-1; research.md, "What exists today".

5. When free selection encounters a refused destination, that candidate is
   omitted with its reason while admissible peers remain selectable.
   *Refuted by:* Either preparation selects a foreign destination, suppresses
   an admitted same-host path-move notice, or duplicates destination policy
   instead of using the existing shared Go address assessment.
   *Basis:* decisions.md#Q-1.

6. When research applies its additional eligibility and reachability checks,
   it retains the existing public-research constraints and optional-free
   behavior.
   *Refuted by:* Missing tool support or deprecated metadata admits a free
   researcher; capability-source failure or failed free probes blocks the 39
   required slots; review begins requiring research capability metadata.
   *Basis:* decisions.md#Q-1; research.md, "What exists today".

7. When either preparation drops a paid-admitted free candidate, its report
   names the id and the paid-admission reason.
   *Refuted by:* The report calls the candidate free, calls its terms unread
   as though that could grant free admission, or silently omits the collision.
   *Basis:* decisions.md#Q-1; research.md, "What exists today".

8. If a saved or supplied free selection contains an id now admitted as paid,
   both call boundaries refuse it before a free model request.
   *Refuted by:* A forged or older selection containing `beam-free` authorizes
   a free review, free research probe or public-research call.
   *Basis:* decisions.md#Q-1; research.md, "Where it lives".

9. When the offline contract runs, it successfully exercises both production
   preparations against the installed pinned Pi's shipped Go catalog and the
   repository's current selection declarations without a hosted model call.
   *Refuted by:* Either preparation is omitted, a fabricated roster replaces
   the shipped input, a real credential or external request is used, a paid
   id enters a free selection, or the contract skips missing prerequisites
   instead of failing.
   *Basis:* decisions.md#Q-3.

10. If the offline contract encounters a preparation regression in either
    path, it fails before merge through the existing verification suite.
    *Refuted by:* Forcing either production preparation to refuse, bypassing
    its shared selection, or letting a paid id into a prepared free selection
    leaves the contract green; success is accepted without a valid
    preparation result.
    *Basis:* decisions.md#Q-3.

## Non-goals

- No change to the Pi/Node pin, catalog sources, provider addresses, model
  admissions, terms readings, cost order, paid seat selection or paid ladder.
- No copying review's dated `step-5-preview-free` exclusion into research's
  declaration; callers retain their declared policy values and capability
  differences. Equal catalog input alone does not erase those differences.
- No new live probe, billing measurement, research-swarm run or external
  service is needed to qualify this repair.
- No change to the 39 required research slots, optional-free budget, receipt
  lifetime, acknowledgment, resume protocol, content/tool boundaries or leak
  checks. No registry migration or general provider abstraction.
- No rewrite of the research-swarm neighbour's broad paid-terms wording;
  existing free/public exceptions remain scoped as today.

## Protected areas

- `model-endpoints.yaml`, `scripts/stage2_go.py` and the installed Pi package:
  consume the existing declarations, destination policy and pinned runtime.
- Governance, accepted ADRs, other change folders, agent configuration,
  prompts, templates and CI configuration: this work changes common internal
  selection, with tests discovered by the existing suite.
- `research.md` and `decisions.md`: evidence and maintainer answers stay intact.
  The granted one-time Flash exploration exception is not a standing bypass.

## Definition of Done

- Criteria 1–10 have the ledger's evidence; `make verify` is green at the
  implementation commit, with offline contracts run rather than skipped.
- Moved in the same pull request: the selector, its two callers and admission
  adapters, synthetic regressions, real-Pi preparation contracts, and this
  change's spec/design/plan/evidence; no doctrine, model or ADR edit.
- The pull request's file list shows the protected areas untouched and the
  non-goals unbuilt; the runner regenerates `plans/INDEX.md`.
- The pull request closes the shared-free-selection task
  (`coding-harness-wb40`); its last commit carries
  `Closes-Bead: coding-harness-wb40`.
- Special runs: none. The ADR proposal is not a maintainer answer; any required
  answer is recorded by the orchestrator only after the maintainer states it.

## Open decisions

None open about implementation scope. The feature's ADR proposal is "no";
no maintainer answer is claimed or written here.

- [DETAIL] Keep the change a feature and write a design for the shared
  component. No ADR draft is proposed: existing admission and address rules
  gain one implementation, without a new external or governance contract.
- [DETAIL] Use four hours of phase 4, repairs included, as a stop: extraction,
  migration and a real-catalog cross-preparation proof belong together.
- [DETAIL] Normalize the two existing policy shapes explicitly, preserving
  additive review includes and restrictive research includes; hard admission
  vetoes always win. Do not merge their distinct configured exclusion lists.
- [DETAIL] Compare membership, not output order: review retains catalog order
  and research retains stable sorted output to avoid unnecessary record churn.
- [DETAIL] Keep `neighbours: []`: the granted Flash exploration exception
  (`decisions.md#Q-2`) produced no complete research-swarm handoff.
