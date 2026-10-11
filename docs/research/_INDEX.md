---
title: "Research index and reading routes"
category: research
status: proposed
created: 2026-09-16
last_reviewed: 2026-09-18
updated: 2026-10-11
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

A note's `last_reviewed:` is the day its content was last checked against its
sources. An edit moves `updated:`, not this date; whoever re-checks a note sets
it. The nightly `drift` job lists the notes whose review is more than 90 days
old (`scripts/check_research_currency.py`, report-only).

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
| [Obsidian as a reader](2026-09-23-obsidian-as-reader.md) | proposed · 2026-09-23, re-checked 2026-09-27 | Seven recommendations for reading this repository in Obsidian, each with its status at `4e7ea5c` |
| [Kubernetes gate runner](2026-09-26-kubernetes-gate-runner.md) | proposed · 2026-09-26 | The verifier in a pinned container, run as a Kubernetes Job in five stages; bead proposal and ADR draft |
| [Tracker writes from worktrees](2026-09-23-worktree-tracker-writes.md) | accepted · 2026-09-23 | D-5's five checks green with bd 1.3.0; the worktree write ban lifts, the one-writer rule stays |
| [Agent Skills assessment](2026-09-18-agent-skills-assessment.md) | proposed · 2026-09-18 | Selective technique adaptation and evaluation without importing a competing workflow |
| [Agent SDK and formal models](2026-09-26-agent-sdk-and-formal-models.md) | proposed · 2026-09-26 | TLA+ for four protocol seams alongside M0 (three models run, one new finding in the recap lock, reproduced), property tests before Lean for pure logic (Lean run and checked against the code; four alternatives measured on the same targets), the Agent SDK as one adapter of a runner-neutral qualification runner |
| [Work framing for ADHD](2026-09-30-adhd-frame.md) | proposed · 2026-09-30 | Evidence for the plan card with a pre-mortem line, the appetite stop, the clock in "done:", the resumption line and the acceptance card; each source dated, with its strength, and what was not read |
| [LikeC4, a ROADMAP.md and an arc42 skeleton](2026-10-05-likec4-roadmap-arc42.md) | proposed · 2026-10-05 | Three kit questions: LikeC4 not now, amend D-15 and O-3 toward a Mermaid architecture delta in `design.md` (LikeC4 measured: no C4 hierarchy check, Node ≥ 22); a trial `ROADMAP.md` before any template; the arc42 skeleton stays on the not-now list |
| [Hermes Agent as a job runner](2026-10-05-hermes-agent-runner.md) | proposed · 2026-10-05 | Not Hermes now: the weekly research re-check runs by hand first, then as a scheduled GitHub Actions job whose agent holds no write token; Hermes, a Claude Code routine, Actions, the Kubernetes gate runner and "by hand" compared on first run, weekly cost, burden, exposure and reversal; the runner-neutral prompt and what any runner must guarantee |
| [The i-have-adhd skill](2026-10-06-i-have-adhd-skill.md) | proposed · 2026-10-06 | An MIT skill with ten rules for ADHD-friendly agent output, compared item by item: 10 of 17 covered here, 6 partly, time estimates different by design; do not install the plugin (its always-on hook injects unreviewed upstream text into every session); fold five gaps into `AGENTS.md` and the global `CLAUDE.md` (debug-spiral stop, pre-send check, honest error causes, list caps, "step n of m"); its blind A/B evaluation and what this repository could measure |
| [Diagrams in pull requests](2026-10-06-diagrams-in-pull-requests.md) | proposed · 2026-10-06 | A generated touch list (what runs and tests the changed code) in every code pull request, a Mermaid map only at three or more changed code files and collapsed, the `design.md` architecture delta linked, never an agent-drawn diagram; review bots, deterministic generators and the GitHub Mobile app (Mermaid shows as code) checked; a prototype run read-only on `feat/project-lock` (14 of 14 links right, the map needs zooming on a phone) |
| [mattpocock/skills against Coding Harness](2026-10-06-mattpocock-skills.md) | proposed · 2026-10-06 | Do not install the plugin; 22 skills mapped (9 rows covered or better here, 5 partly, 2 missing, 3 left out); adopt a debugging prompt, sharper interview, test and ADR-question lines, and a root `GLOSSARY.md` with a report-only check; an architecture survey as a second recurring job after the research re-check; where a process-owning framework takes control away, honestly |
| [Ponytail, the least-code skill](2026-10-06-ponytail-skill.md) | proposed · 2026-10-06 | Take the ladder, not the plugin: fold it into prompts 03 and 04 and a "built and not promised" finding into 06, never thinner on tests and planted faults; the ladder run by hand over five changes finds about 5 % to cut, mostly grown in the review loop; deleting 29 of 30 tests of one script leaves `make verify` green, so only prompts and the reviewer hold per-criterion tests |
| [Kubernetes across the three projects](2026-10-08-kubernetes-across-projects.md) | proposed · 2026-10-08 | A bounded read-only verifier pilot in Coding Harness, later CLI batch execution for LakeSwitch, and retaining ADHD Relief's macOS core; updates the older gate-runner assumptions against the dependency lock and accepted Hermes architecture |
| [GLM through Pi](2026-10-11-glm-through-pi.md) | proposed · 2026-10-11 | Z.ai lists Pi as a supported GLM Coding Plan tool (read 2026-10-11); implement needs no shell today, so Pi with the ADR 0012 policy extension and no `bash` matches the Claude Code shape, `sandbox-exec` (measured, deprecated) as the step if a shell is granted; the decision PR is a new ADR amending ADR 0007 decision 2 and ADR 0011's runner shape |

Original four-source intake note: copied in by the maintainer on 2026-09-16 (Phase 2 of the
separation, bead `coding-harness-anw`). Provenance is set to
`ai-drafted-reviewed` with review pending — the maintainer corrects the class
where the hand differs.
