---
title: "Spec — redraft-after-scope"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-y0qm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, spike, scope]
class: spike
appetite: 2
adr_files: []
neighbours:
  - plans/changes/guard-test/spec.md
  - plans/changes/research-swarm/spec.md
  - plans/changes/loop-until-clean/spec.md
  - plans/changes/sol-effort/spec.md
  - plans/changes/interview-context/spec.md
---

# Spec — redraft-after-scope

Determine which intervention best prevents implementation from following a
changed scope while its governing artifacts still describe the old scope,
and give the maintainer an evidence-based recommendation (bead
`coding-harness-y0qm` — investigate redrafting after scope changes).
Sources: `research.md` and the reasoned interview skip in `decisions.md`.

## Problem

- The exploration dated 2026-11-06 records redrafts in guard-test,
  research-swarm, sol-effort and loop-until-clean, but finds no common rule
  for a scope change after drafting. Existing checks measure artifact form
  and recorded answers, rather than semantic agreement between them
  (`research.md`, “The precedents” and “Adjacent mechanisms”).
- The interview skip identifies a concrete protected-area conflict: the
  orchestrator of handoff-new-feature edited `prompts/`, which its spec
  kept unchanged (loop row L6-1); the edit was reverted in `b04c119d` on
  2026-11-06. A redraft after a late answer and a check on protected-area conflicts address different possible
  causes; the investigation must distinguish them before recommending either
  (`decisions.md`, “SKIP · interview”).

## Terms

- **Scope change:** a proposed or maintainer-answered change to intended
  behavior, acceptance criteria, exclusions or permitted edit areas; it is
  not automatically authorized by being proposed.
- **Redraft:** revision of the existing spec and dependent plan (and design
  where its class requires one), retaining decision and evidence history.
- **Investigation result:** a repository research report proposing a remedy;
  it neither adopts that remedy nor answers for the maintainer.

## Acceptance criteria

1. When the investigation presents its evidence, its report reconstructs the
   protected-prompt incident and the four redraft precedents from dated,
   repository-verifiable sources.
   *Refuted by:* a case is missing, a claim lacks a source path and revision
   or date, a historical observation is presented as current, or an unread
   input is described as absent.

2. When the report compares remedies, it evaluates mandatory redrafting after
   a scope-changing answer, a check on protected-area conflicts and the
   current review-led practice against the same documented cases.
   *Refuted by:* an alternative is omitted, the comparison lacks trigger,
   detection boundary, responsible actor, operational cost or residual risk,
   or a remedy is credited with preventing a case without showing how.

3. When the report describes a proposed redraft procedure, it distinguishes
   scope changes from ordinary drafting details, phase-2a incorporation,
   stale-base refreshes and resuming an interrupted exploration.
   *Refuted by:* the proposal treats every edit as a new interview or a new
   exploration, silently replaces an answer, changes class or criterion
   meaning without maintainer authority, erases history, or assumes swarm
   Basis/neighbour obligations disappear on redraft.

4. When the report recommends a next step, it traces that recommendation to
   the comparison and gives a concrete counterexample or limit that the
   preferred remedy does not cover.
   *Refuted by:* it merely lists options, recommends without evidence, claims
   complete prevention, or omits the proposed follow-up's affected paths,
   change class, ADR implications or remaining maintainer choice.

5. While the spike is delivered, its result remains a proposal without
   introducing a redraft requirement or a protected-area enforcement mechanism.
   *Refuted by:* the change modifies workflow instructions, runner behavior,
   gates, templates, ADRs or another change's artifacts, or records an
   unprovided maintainer answer as settled.

## Non-goals

- Implementing or adopting any remedy, including a new gate, runner verb,
  semantic scope detector or mandatory redraft rule.
- Redrafting other changes, reopening their interviews, changing class
  definitions, adding stale-base thresholds or changing review routing.
- Live model trials, external research or claims of measured prevention rates
  from this small set of historical cases.
- A design document or ADR: phase 2b never runs for a spike; architectural
  choices for a possible remedy belong to a subsequent authorized change.

## Protected areas

All executable code, tests, `docs/WORKFLOW.md`, `AGENTS.md`, `prompts/`,
`templates/`, `decisions/`, `docs/adr/`, `provenance.yaml`,
`model-endpoints.yaml`, configuration directories and other change folders
remain unchanged. The only deliverable outside this change folder is
`docs/research/2026-11-06-redraft-after-scope.md`; `plans/INDEX.md` is derived
by the orchestrator or runner, never edited by an implementation attempt.

## Definition of Done

- The report satisfies criteria 1–4 on source review; the pull request file
  list demonstrates criterion 5.
- Updated together: the report and this change's research/spec/plan/findings
  as needed for evidence and review; no doctrine or ADR moves with them.
- CI is green; this Markdown-only spike skips local `make verify` under the
  repository's text-only rule. The runner owns its draft checks and commit.
- The pull request closes the scope-investigation bead `coding-harness-y0qm`;
  its final commit carries `Closes-Bead: coding-harness-y0qm`.
- Special runs: none are needed for historical source review. Note (orchestrator, 2026-11-07): the stage-2 review loop ran two rounds on this spike by an orchestrator routing error — `docs/WORKFLOW.md`, "Which change gets what", gives a spike no stage 2; its round-1 text repairs are kept, no further round runs, and the review is Opus 5.5 as §3 asks.

## Open decisions

None open for performing the investigation. The maintainer chooses a remedy
after its result, as the interview skip states; no implementation is implied.

- [DETAIL] Use a two-hour phase-4 appetite, repairs included, to bound a
  repository-only comparison; stop with named unread evidence if it runs out.
- [DETAIL] Write the result under `docs/research/` because repository research
  belongs there; a recommendation in it is explicitly a proposal.
- [DETAIL] Use source review rather than new tests for the report's historical
  and semantic claims, because text-presence tests cannot establish them.
