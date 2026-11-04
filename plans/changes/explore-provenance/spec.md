---
title: "Spec — explore-provenance"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, explore, provenance]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — `explore-provenance`

After the runner publishes model-written research, its provenance and opening
text describe a filled research artifact; existing affected active research is
corrected once (bead coding-harness-g19n — truthful Explore provenance).
Research: [research.md](research.md). Scope: [decisions.md, Q-1](decisions.md#q-1--how-far-the-change-goes).

## Problem

- On 2026-11-04, the research records that single-model Explore and the research
  swarm append model output while leaving the skeleton's `human-written`
  declaration and empty-file notice intact; the explorer itself is read-only
  and cannot repair the runner's output (`research.md`, “What exists today”).
- The same research records that the runner stamps only `updated:` and that
  existing gates do not reject this false provenance under `plans/`; subsequent
  review and repair therefore repeat the correction instead of preventing it.
- The maintainer chose the runner fix plus correction of affected open research,
  including removal of the skeleton note (`decisions.md`, Q-1, 2026-11-04).
  At `a2b00438` on that date, the affected active files are this change's research
  and `plans/changes/loop-until-clean/research.md`; archived examples are history.

## Terms

- **Publication** — an accepted single-model research answer or a runner-written
  swarm record, including a published incomplete swarm run; an audit line alone
  is not publication of model research.
- **Skeleton text** — the generated opening “Phase 1 per … file is empty until
  it has run” paragraph and “Bring the provenance up to date” blockquote from
  `scripts/new_change.py`, before the runner's research; the research title stays.
- **Affected active research** — a `research.md` directly under an active
  `plans/changes/<name>/` folder, outside `archive/`, whose header still declares
  `human-written` although its body contains runner-published model research.

## Acceptance criteria

1. When Explore publishes model research through Flash, the explicit Stage-1
   fallback or the research swarm, the resulting research header declares
   `provenance: ai-drafted-reviewed`.
   *Refuted by:* any route publishes model research with `human-written`, a
   missing provenance declaration or conflicting provenance declarations.
   *Basis:* decisions.md#Q-1.

2. When Explore publishes model research, `produced_by` identifies the producing
   program or the swarm orchestration and the publication date.
   *Refuted by:* missing or duplicate producer metadata, an unrelated producer,
   a stale publication date, or attribution of the entire swarm to one model.
   *Basis:* decisions.md#Q-1.

3. When Explore publishes model research, the research header records the
   resulting document's review as pending, with no claimed human approval.
   *Refuted by:* missing or duplicate review metadata, retained approval for the
   newly extended document, or an invented approver or approval date.
   *Basis:* decisions.md#Q-1.

4. When Explore publishes into a generated research skeleton, its opening
   skeleton text is absent from the resulting document.
   *Refuted by:* either generated notice remains, or a second publication
   reintroduces it.
   *Basis:* decisions.md#Q-1.

5. While provenance and skeleton text are corrected, all unrelated existing
   header fields and research body bytes are preserved, apart from the existing
   `updated:` stamp.
   *Refuted by:* altered class, bead, owner, lifecycle fields, authored prose,
   audit lines, prior swarm envelopes or line endings outside the corrected spans.
   *Basis:* decisions.md#Q-1; research.md, “What exists today”.

6. If replacement of an existing research file fails during publication, its
   previous bytes remain intact.
   *Refuted by:* truncated research, a header corrected without its publication,
   or a published body without the corresponding header and skeleton correction.
   *Basis:* decisions.md#Q-1; research.md, “What exists today”.

7. When this change is completed, every affected active research file has the
   corrected provenance, evidence-backed producer metadata, pending review and
   no opening skeleton text.
   *Refuted by:* an affected active file remains, or the correction invents
   historical authorship, discards research, or edits an archived research file.
   *Basis:* decisions.md#Q-1.

8. When an incomplete swarm publication is corrected and the run is resumed,
   the runner's own correction does not invalidate otherwise reusable results.
   *Refuted by:* unchanged inputs force research seats to repeat because of the
   correction, or changed research outside the permitted correction and exact
   runner publication is accepted as the same input.
   *Basis:* decisions.md#Q-1; research.md, “What exists today” and “Where it lives”.

## Non-goals

- No new provenance class, repository-wide provenance validator or enforcement
  of `allowed:` in the provenance map.
- No archive cleanup, changes to the living implementation-verification spec,
  or correction of research without evidence of model publication.
- No change to model selection, prompts, leak checks, admission, swarm record
  format, interview rules, research findings or the meaning of human approval.
- No alteration of the deterministic new-change skeleton's initial provenance:
  it may remain `human-written` until model research is actually published.
- No design phase or ADR: the agreed `bounded` correction preserves the existing
  publication and state-store responsibilities.

## Protected areas

- `plans/changes/archive/` and `plans/specs/` — historical evidence and unrelated
  capability contracts are outside the maintainer's active-research correction.
- `provenance.yaml`, `decisions/`, `docs/adr/`, `AGENTS.md`, `prompts/`,
  `templates/`, agent settings and model declarations — no policy or routing change.
- Other active change folders except the named research backfill — their
  specifications, decisions, plans and research findings belong to other work.

## Definition of Done

- Targeted regression checks and `make verify` are green at the implementation
  commit; each ledger test rejects its stated fault.
- The same pull request includes the runner correction, regression tests and
  corrected active research, including this change's research and
  `plans/changes/loop-until-clean/research.md`; no model or ADR changes are due.
- The pull request's file list respects the protected areas and non-goals.
- The pull request closes the truthful-Explore-provenance task, and its last
  commit carries `Closes-Bead: coding-harness-g19n`.
- Special runs: none requiring live model calls; tests use local stand-ins.

## Open decisions

None open. The maintainer's answer in Q-1 is unchanged.

- [DETAIL] Use the existing `producer_for(endpoint)` program names for
  single-model publication and `stage2-research-swarm` for the mixed swarm;
  use the publication date as `produced_by.version`, matching findings headers
  without pretending one swarm participant authored the whole document.
- [DETAIL] Replace prior review approval with pending on publication because
  the extended document has not yet been approved; do not change lifecycle status.
- [DETAIL] Backfill producer identity and version from the existing Explore audit
  evidence, stamp `updated:` on the correction date and keep review pending;
  this records what is known without inventing historical approval.
- [DETAIL] Set a two-hour implementation appetite, repairs included, because
  this bounded correction must include swarm-resume regression coverage; stop
  and report remaining work if that budget is exhausted.
