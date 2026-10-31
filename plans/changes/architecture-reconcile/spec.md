---
title: "Spec — architecture-reconcile"
category: spec
status: draft
implementation_status: none
created: 2026-10-31
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-190
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, architecture, reconciliation]
class: bounded
appetite: 2
adr_files: []
neighbours: [plans/changes/workflow-promises/spec.md, plans/changes/research-currency/spec.md]
---

# Spec — architecture-reconcile

Provide a dated, evidence-backed comparison of the architecture target,
delivery plan and original gaps with the repository, without changing their
decisions (bead `coding-harness-190` — reconcile architecture and gaps).
Research: `research.md`. Scope and interview skip: `decisions.md`.

## Problem

The exploration in `research.md` records these failures on 2026-10-31;
the draft baseline is `b58c72e75af3283f4cc9e39148ecfb02642026f9`:

- The gap analysis still measures `eddfc0b` on 2026-09-17. It calls the
  verifier, CI and several templates absent although the current tree
  contains them; its old test counts are not current evidence.
- The target and delivery plan retain earlier claims despite subsequent
  decisions: the removed M0 pilot, a separate routing file that is absent,
  and Apache-2.0 wording against the current licence. The plan also calls
  onboarding and a public scan delivered without evidence for that claim.
- Dated amendment banners and decision-continuity tests protect the original
  documents. Rewriting them would mix measurement with changing decisions.
  `decisions.md` therefore requires a separate dated table under
  `docs/research/`, with proposed remedies rather than policy edits.

## Terms

**Baseline:** the full Git commit above, frozen for this comparison; tracker
observations carry their own snapshot date because Git does not freeze Dolt.

**Disposition:** supported, partial, open, amended or not read; an amendment
explains why an earlier requirement changed and does not prove delivery.

## Acceptance criteria

1. When the reconciliation is delivered, one dated research document identifies
   its full baseline commit and measurement date.
   *Refuted by:* no report, multiple competing reports, or an unspecified or
   moving baseline such as an unqualified `origin/main`.
2. When the target is compared with that baseline, every contract section of
   `docs/architecture/2026-09-17-omnigent-first-target.md` has a traceable
   disposition in the report.
   *Refuted by:* a contract section is omitted or replaced by a general
   assertion that the target is implemented.
3. When the delivery plan is compared with that baseline, each milestone
   M0–M4 and each worktree/tracker step W0–W2 has a traceable disposition.
   *Refuted by:* a step is omitted, or the abandoned M0 pilot is presented as
   a current prerequisite without its superseding decision.
4. When the historical gap table is re-measured, each of its 26 rows at the
   baseline has a separate, identifiable disposition in the new report.
   *Refuted by:* an original gap disappears, two gaps are merged so one
   cannot be assessed independently, or an unrelated inventory substitutes
   for the original table.
5. When a row makes a current-state claim, its evidence identifies the
   inspected source or measurement at the declared baseline and date.
   *Refuted by:* file existence is treated as runtime qualification, an old
   test total is presented as re-run, a row has no checkable evidence, or
   unread evidence is reported as absent or delivered.
6. When the report names a bead cited by the original gap table, its status
   is attributed to a dated snapshot obtained through `scripts/bead_render.py`,
   or explicitly says "not read" with the access limitation.
   *Refuted by:* a status is inferred from prose, an unavailable tracker is
   treated as an empty tracker, or a bead's closure alone proves delivery.
7. When the report encounters the routing-file discrepancy, the licence
   discrepancy, the abandoned pilot, or the unsupported onboarding/public-scan
   delivery claim, it records the contradiction and a proposed remedy
   separately from the observed state.
   *Refuted by:* one of these discrepancies is omitted, or a proposed banner,
   mapping change or ADR is represented as an adopted decision.
8. While this reconciliation is delivered, the four source architecture
   documents and the mechanisms that enforce them remain unchanged.
   *Refuted by:* the diff rewrites or supersedes a source document, changes a
   gate or its tests, or activates a permission to make a report row true.

## Non-goals

- Implementing gaps, changing architecture decisions, adding ADRs, rewriting
  the four architecture documents, or declaring milestone qualification.
- Auditing live services, sibling repositories or private instances; the
  report assesses evidence available in this repository.
- Renaming the product, reconciling all workflow/governance prose, or
  duplicating the neighbouring workflow-promises change.
- Creating, claiming, closing or reprioritising tracker items; proposed
  follow-up work stays a finding for the authorized tracker writer.
- Re-running the September suite for new performance or defect statistics.
  No design phase runs for this bounded documentation change.

## Protected areas

- All four files in `docs/architecture/`: their historical text, banners,
  decision-continuity rows and supersession metadata are source evidence.
- `scripts/`, `tests/`, `prompts/`, `templates/`, `decisions/`, `docs/adr/`,
  `provenance.yaml`, `model-endpoints.yaml`, `AGENTS.md`, `README.md`,
  `LICENSE`, `COMMERCIAL.md`, `docs/WORKFLOW.md`, `.github/`, `.claude/`,
  `.codex/`, `.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md` and `.beads/`:
  no mechanism, authority, licence, configuration or tracker edit is needed.
- Other changes' artifacts and existing research records remain with their
  owners; no research index rewrite is required.

## Definition of Done

- The report passes the criterion-by-criterion evidence review; CI is green.
  The text-only exception skips local `make verify`; runner-owned verification
  remains the runner's responsibility.
- The added document is
  `docs/research/2026-10-31-architecture-reconciliation.md`; this change's
  evidence/status records and the generated `plans/INDEX.md` move with it.
  No models or ADRs change.
- The diff preserves protected areas and leaves the non-goals unbuilt.
- The orchestrator's pull request names the architecture reconciliation bead
  and its final commit carries `Closes-Bead: coding-harness-190`; this draft
  does not commit or update the tracker.
- Special runtime runs: none. An unavailable measurement remains explicitly
  unmeasured, not a green result.

## Open decisions

None open. These reversible details are chosen by the agent with their reasons:

- [DETAIL] Use the dated report filename above and separate target, delivery,
  gap and discrepancy tables so every original obligation remains findable.
- [DETAIL] Freeze the comparison at the draft baseline, rather than silently
  including later parallel work; date any tracker snapshot separately.
- [DETAIL] Allow two hours of phase 4 including repairs, then stop and report
  remaining work; neither research nor decisions states a different appetite.
- [DETAIL] No design or ADR draft is due for the recorded `bounded` class.
  The exploration used Stage 2, GLM 5.3 Flash, on 2026-10-31; no Stage-1
  fallback is recorded.
- [DETAIL] `templates/plan.md` and `scripts/validate_change_artefacts.py` are
  absent at the baseline. Follow the phase-3 prompt and existing plan headers;
  report the unavailable validator rather than introducing it in this change.
