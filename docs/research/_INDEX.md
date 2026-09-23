---
title: "Research index and reading routes"
category: research
status: proposed
created: 2026-09-16
last_reviewed: 2026-09-18
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: codex-sol
  version: "2026-09-18"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, index, workflow]
---

# Research Index

The research corpus behind the coding workflow. Every document carries
frontmatter (category: research); provenance classes follow the five-class
enum in `provenance.yaml` — the maintainer corrects a class by editing the
frontmatter, never by deleting the claim.

The [current Omnigent-first target](../architecture/2026-09-17-omnigent-first-target.md),
[gap analysis](../architecture/2026-09-17-gap-analysis.md), and
[implementation plan](../architecture/2026-09-17-implementation-plan.md)
govern proposed sequencing. The [historical target architecture](../architecture/target-architecture.md)
preserves the decision interview and its later amendments; this research corpus
is evidence and options, not a second normative workflow.

## Reading routes

- **Choose the next implementation step:** start with the current target and implementation plan, then use the gap analysis to inspect prerequisites and open evidence.
- **Plan as a human with limited attention:** read the [human planning and harness gaps note](2026-09-18-human-planning-and-harness-gaps.md) for a proposed start page, interruption defaults and remaining decisions. These proposals await review; Beads remains work-status authority.
- **Choose an external component:** read the three dated assessments below, then test a bounded claim against the target's M0/M1 gates before adoption. They are source reviews, not successful pilots.
- **Recover the original rationale:** read the four intake sources below and the [decision continuity table](../architecture/2026-09-17-omnigent-first-target.md#decision-continuity). Keep their dates and provenance attached to each claim.

Vocabulary for older sources: **Stage 1–3** means model routing; **S0–S7** means instance setup; **T0–T2** means team scale; **M0–M4** means Omnigent adoption; **levels 1–5** means rule enforcement. Older uses of *Stufe* are ambiguous; this map aids reading without rewriting the sources.

| Document | Internal stand | Focus | Tags |
|---|---|---|---|
| [`arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md`](arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md) | Version 1.2 · 17.09.2026 | arc42 reference architecture „Agentischer Delivery-Workflow“ (ADW), tool-neutral conventions, Omnigent as target runtime | arc42, adw, omnigent |
| [`Lake-Switch-Architektur-arc42.md`](Lake-Switch-Architektur-arc42.md) | 2026-09 | arc42 documentation of the toolchain/working environment Lake Switch is developed in (the product's own arc42 lives in `lakeswitch-ai`) | arc42, lakeswitch, toolchain |
| [`Migrationsplan_Omnigent_Referenzarchitektur.md`](Migrationsplan_Omnigent_Referenzarchitektur.md) | 2026-09 | stepwise instantiation of the ADW reference architecture into a productive Omnigent topology — no big bang, abort criteria per stage | migration, omnigent |
| [`2026-09-16-review-corpus-vs-running-workflow.md`](2026-09-16-review-corpus-vs-running-workflow.md) | read at `5a950c2` · 2026-09-16 | review of the three documents above against the running workflow: adopt / keep / decide per topic, contradictions between the sources, eight decisions for the maintainer, proposed corrections | review, adw, lakeswitch, omnigent |

## New assessments and planning research

| Document | Internal stand | Focus |
|---|---|---|
| [Human planning and harness gaps](2026-09-18-human-planning-and-harness-gaps.md) | proposed · 2026-09-18 | Human planning entry, attention support, unresolved harness gaps |
| [CrewAI assessment](2026-09-18-crewai-assessment.md) | proposed · 2026-09-18 | Runtime overlap with Omnigent; defer coordinator adoption pending a measured gap |
| [Open Code Review assessment](2026-09-18-open-code-review-assessment.md) | proposed · 2026-09-18 | Review tool fit, limits and smallest gated pilot |
| [Tracker writes from worktrees](2026-09-23-worktree-tracker-writes.md) | accepted · 2026-09-23 | D-5's five checks green with bd 1.3.0; the worktree write ban lifts, the one-writer rule stays |
| [Agent Skills assessment](2026-09-18-agent-skills-assessment.md) | proposed · 2026-09-18 | Selective technique adaptation and evaluation without importing a competing workflow |

Original four-source intake note: copied in by the maintainer on 2026-09-16 (Phase 2 of the
separation, bead `coding-harness-anw`). Provenance is set to
`ai-drafted-reviewed` with review pending — the maintainer corrects the class
where the hand differs.
