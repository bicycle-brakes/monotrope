---
title: "LikeC4, a ROADMAP.md and an arc42 skeleton — what the kit should ship"
category: research
status: proposed
created: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-05"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, architecture, c4, likec4, model-as-code, design-phase, mermaid, roadmap, arc42, templates]
---

# LikeC4, a ROADMAP.md and an arc42 skeleton

## Result first

Three questions, three answers:

1. **LikeC4: not now, and not in the form D-15 decided.** One ADR, in a
   decision pull request of its own, amends D-15 (LikeC4 in the kit) and
   O-3 (an Architectural change needs an ADR and a model diff). An
   Architectural change then carries its picture in `design.md`: a Mermaid
   flowchart, which GitHub renders in the pull request, and three short
   lists of what is added, changed and removed. LikeC4 stays the named
   upgrade path, with a revisit trigger (A7).
2. **ROADMAP.md: the file first, the template later.** Coding Harness has 23
   open or in-progress beads, no epics, and no place that says which few
   outcomes matter now and why. Write one short `ROADMAP.md` here as a
   trial: at most three Now themes, each with an appetite and its beads.
   Check it at each handover. The kit template follows once the file has
   stayed true through two handovers; if it is found stale twice, it goes
   (B7).
3. **arc42 skeleton: not now.** Both repositories already have a description
   in arc42's order, written without a template, and both aged within days
   to weeks. The skeleton stays on the not-now list until a third instance
   or the onboarding page asks for one; then the kit links arc42's own plain
   Markdown instead of copying it (C7).

**What `design.md`'s model section should say now:** the text of row (b) in
A6. It is true today. If the ADR for LikeC4 option (c) merges, only its
heading and first sentence change.

## 1 · Question and scope

The maintainer asked on 2026-10-05: "Does LikeC4 make sense?", and later the
same day widened the question to a `ROADMAP.md` template and an arc42
skeleton. All three cover Coding Harness and the repositories that run its
workflow, LakeSwitch first. On the same day the maintainer decided that the
template bundle (bead coding-harness-9qo) includes the design phase 2b, and
that D-14 stays. Phase 2b produces a `design.md` with alternatives,
interfaces, data model, an ADR draft and a model-as-code delta. The template
bundle's research had put ROADMAP and arc42 on its not-now list.

Read for this note, all on 2026-10-05:

- **This repository** at `3851f9c` (`origin/main`): D-14, D-15 and O-3 in
  [`target-architecture.md`](../architecture/target-architecture.md)
  (§5.2, §6.1, §9.1 to §9.3, §10, §12, §13); the
  [decision continuity table](../architecture/2026-09-17-omnigent-first-target.md#decision-continuity)
  and its "Direction" and planning sections; the
  [gap analysis](../architecture/2026-09-17-gap-analysis.md) (P1); the
  [implementation plan](../architecture/2026-09-17-implementation-plan.md);
  [`check_decision_continuity.py`](../../scripts/check_decision_continuity.py);
  `.github/workflows/ci.yml`; `plans/INDEX.md`; the Mermaid blocks under
  `docs/`; [`tools/claude-code/README.md`](../../tools/claude-code/README.md);
  the [review of 2026-09-16](2026-09-16-review-corpus-vs-running-workflow.md),
  the [human planning note](2026-09-18-human-planning-and-harness-gaps.md)
  and the [ADHD frame note](2026-09-30-adhd-frame.md); the two German arc42
  documents under `docs/research/`, searched for roadmap and arc42 passages.
- **The tracker**, read only: `tools/bd show coding-harness-9qo` and the
  lists of open and in-progress beads.
- **Branch `docs/template-bundle`** at `f8c39f3`:
  `plans/changes/template-bundle/research.md` (§1, §2, §3, §7 Q1 and Q4)
  and `decisions.md`.
- **Branch `feat/stage-2-codex-glm`** (PR #60) at `ef7407c`: searched for
  O-3, "model diff" and LikeC4.
- **`lakeswitch-ai`** `main` at `09c9d62`, read only: D-18, D-19, D-22,
  D-29, D-32, D-58 and D-65 in
  `plans/changes/unified-research-and-work-management/decision-interview.md`;
  the ratifications RC-003 and RC-005; contradiction 2 in
  `journal/2026-09-28-product-start-and-principles.md`; `spec/_overview.md`
  and the `implements:` headers under `spec/`; `docs/architecture.html`,
  read as extracted text (headings and searched passages).
- **`portfolio-agentic-engineering`** at `20a279c`, read only: the header of
  `docs/archive/planning-2026-04/roadmap-consolidated.md`.
- **Web sources** and GitHub, npm and VS Code Marketplace API reads, listed
  under Sources.
- **A trial:** LikeC4 1.59.4 installed into a scratch directory outside the
  repository, three small models validated (A2). Nothing was installed into
  the repository.

## Part A · LikeC4

### A1 · What LikeC4 is today

| Property | As of 2026-10-05 |
|---|---|
| What it is | A language and toolset: one architecture model in `.c4` files, many diagrams (views) generated from it. "Inspired by C4 Model and Structurizr DSL, but provides some flexibility." |
| Licence | MIT |
| Age and version | Repository since 2023-03-24. Latest v1.59.4, 2026-09-21. Still 1.x. |
| Release activity | 27 releases in the twelve months to 2026-10-05. None of the last 30 release notes mentions "breaking". |
| Who carries it | 26 human authors in the 90 days to 2026-10-05, but 92 of their 162 commits come from one maintainer. All time: 4,147 commits from him, 202 from the next person. |
| Use | npm `likec4`: 409,115 downloads in the month to 2026-10-04 (CI installs included, so an upper bound). 5,807 GitHub stars. VS Code extension: 26,576 installs (Marketplace), 41,831 downloads (Open VSX). |
| Runtime | Node.js ≥ 22.22.3 (`engines` of 1.59.4). 17 direct dependencies, among them Vite, esbuild and Playwright. |
| Command line | `validate` (syntax, references, layout drift; non-zero exit on errors), `format --check`, `build` (static site), `serve`, `export png/jpg/json/drawio`, `gen mermaid/dot/d2/plantuml/react`, `lsp`, `mcp`. |
| For agents | An MCP server with read-only tools: search elements, relationships between two elements, ancestors and descendants, upstream and downstream, render a view. Runs from `likec4 mcp`, from `@likec4/mcp`, or registered by the VS Code extension. |
| CI | The official GitHub Action (`likec4/actions`) last released on 2025-11-11. A CI step can call the pinned command line directly instead. |
| C4 strictness | Element kinds are declared freely in `specification { … }`. The specification page shows no rule for which kind may nest in which (read in the documentation source). |
| Recognition | No LikeC4 or Structurizr entry found in the Thoughtworks Technology Radar, volumes 32 (2025-04), 33 (2025-11) and 34 (2026-04). |

### A2 · Trial, measured 2026-10-05

macOS, Node.js 26.9.0, npm 11.19.1, `likec4@1.59.4` in a scratch directory:

- **Install:** 16 seconds, 118 MB of `node_modules`. npm 11 held back
  esbuild's install script; `validate` and `gen mermaid` worked without it.
- **A correct model** of four elements: "Valid", exit 0, under one second.
- **A `system` nested inside a `component`,** with a `container` inside
  that: "Valid", exit 0. The specification does not enforce the C4
  hierarchy.
- **A relationship to an element that does not exist:** two errors ("Could
  not resolve reference …"), exit 1.
- **`likec4 gen mermaid`** writes one Mermaid `graph TB` per view, in
  Mermaid's `@{ shape: … }` node syntax.

So `validate` checks the model against itself. It never compares the model
with the code.

### A3 · The alternatives

| Option | What it is | What is checked | Runtime | Renders on GitHub | State on 2026-10-05 |
|---|---|---|---|---|---|
| **Structurizr DSL** | The models-as-code tool of the C4 model's author, its reference implementation | The language enforces the hierarchy ("defines a container, within a software system"); `validate`; export to Mermaid, PlantUML and C4-PlantUML | Java 21 (WAR) or a Docker image | No; an export is needed | Apache-2.0. Consolidated in late 2025: Lite archived ("will not receive any further updates"), v2026.09.19, one listed contributor in the new repository. The server needs a licence when run from the prebuilt binaries. |
| **C4-PlantUML** | C4 shapes for PlantUML; a diagram library, not a model | PlantUML syntax only | PlantUML (Java) or a PlantUML or Kroki server | No; GitHub renders Mermaid, GeoJSON, TopoJSON and ASCII STL only | MIT, v2.14.0 (2026-08-26) |
| **Mermaid C4 syntax** | `C4Context`, `C4Container` and three more inside Mermaid | Parsing only | None in the repository | Not verified; two community sources disagree (section 2) | Part of Mermaid's core, but its documentation says: "experimental … syntax and properties can change". Layout follows statement order; no legend, no tags. |
| **Mermaid flowchart in C4 words** | An ordinary `flowchart`, each box labelled with its C4 level | Parsing only | None | Yes (GitHub documentation) | Already the house form: 10 of the 16 Mermaid blocks here are flowcharts, 11 of the 13 in LakeSwitch |
| **Markdown or arc42 views** | Text and diagrams in arc42's sections, such as the building block view | The link and frontmatter gates this repository already runs | None | Yes | See Part C |
| **No model** | ADR and prose only | That the ADR exists | None | Not applicable | Not applicable |

The C4 model's own site draws the line between the two kinds of tool.
Diagramming tools know "boxes and lines". Modelling tools keep one
definition and generate views from it, so "renaming elements/relationships
is easy". That gain grows with the number of views that share elements.
While each element appears in one or two pictures, it is close to nothing.

### A4 · What a model as code would buy here

| Question | Answerable today? | Would LikeC4 answer it? |
|---|---|---|
| Has the architecture description drifted from the code? | In part. The gates check links, frontmatter dates, the decision map and the plans registry. Nothing compares a picture with the code. | **No.** `validate` checks the model against itself. A model-to-code check is a script of its own, and that script works as well against a list in Markdown or against LakeSwitch's `implements:` headers. |
| Can a reviewer see an architectural change in the diff? | Yes, as prose and Mermaid text; GitHub renders Mermaid in the file view. | As text. A `.c4` diff reads well, but GitHub renders nothing; a picture needs `likec4 serve`, a built site or exported images. |
| Does the pull request carry the "model diff" O-3 asks for? | No, and nothing checks it (template-bundle research §1.3). | It makes "the pull request touches `model/`" checkable. Whether the delta is right still needs the reviewer. A filled section in `design.md` is checkable to the same degree by the validator already planned (bead coding-harness-jc3). |
| Can the maintainer read it on a phone? | Mermaid renders on github.com in a phone browser. In the GitHub Mobile app: not verified. | Only through a published static site or committed images, which means another deployment or a Playwright export. |
| Can an agent answer "what depends on X"? | By reading Markdown and code. At about ten elements that is one file. | Yes, through the read-only MCP server. This is the one real gain, and it grows with the size of the model. |
| Is the C4 hierarchy kept? | Not checked. | **No** (A2). Structurizr would keep it. |

**For whom.** The maintainer reads on a phone, between other things, so the
picture has to arrive inside the pull request, on its first screen about the
architecture; a Mermaid block in `design.md` does that, a `.c4` file does
not. Agents already write Mermaid (16 blocks in this repository) and read it
as text; the MCP server pays once a model outgrows a page. Coding Harness's
architecture is about ten boxes at container level (estimate: maintainer,
Claude Code with the display, Omnigent, the doctrine, the gate runner, the
tracker, the kit, GitHub, the foreign review endpoints, the instances).

**Drift needs a check on the code, not a picture.** LakeSwitch shows what
such a check could hold on to: each module specification names its code in
an `implements:` header, and 8 of the 9 code packages under `src/lakeswitch/`
are named by one (read at `09c9d62`; an observation, not a finding against
LakeSwitch). A script of a few dozen lines can compare those headers with the
packages that exist. The Thoughtworks Radar of April 2026 describes the same
answer to agent-driven drift: "deterministic analysis tools … with
LLM-powered evaluation" and "architectural fitness functions".

**The first real use** would be the **Kubernetes gate runner**
([proposal](2026-09-26-kubernetes-gate-runner.md)), which names its own
class: "Architectural: a new runtime component, so an ADR is required". Its
delta is small: one new container (the pinned verifier image, run as a Job),
one new relationship (CI or the maintainer starts the Job), and the gate list
unchanged as the one source.

| | (a) LikeC4 as D-15 says | (c) Mermaid in `design.md` |
|---|---|---|
| Before the first use | 2–4 h for the Node toolchain, the gate, a sample model and a known-bad case (template-bundle research §3, an estimate). 1–2 h to model the harness once (estimate). A custom check if the hierarchy should hold. | Nothing beyond the template, which the template bundle writes anyway. |
| Per Architectural change | Edit `model/`, run `validate`, and get the picture to a phone reader some other way: 20–40 min (estimate). | One flowchart of the touched part and three short lists: 10–20 min (estimate). |
| Keeping it current | A Node pin in a Python repository. With 27 releases a year, the pin either moves about monthly or ages. 118 MB per uncached CI install. | Nothing. |
| What is lost | Nothing. | Model queries through MCP, one definition for many views, safe renames. |

### A5 · Fit with the decisions

**D-15 (LikeC4 in the kit).** Decided on 2026-09-16, "revised after the
best-practice question". The original recommendation was the opposite: the
kit ships a placeholder and the gate, the instance chooses Structurizr or
LikeC4, because "a tool choice in doctrine ages fastest"
(target-architecture §9.2). D-15's stated basis, that the pinned
specification keeps the strictness, does not hold (A2). The continuity table
carries D-15 as Retain, and the gap analysis (P1) guards it against silent
loss. That guard is right: a change to D-15 must be an explicit amendment,
never a side effect.

**O-3 (architecture detection).** "`class: Architectural` without an ADR and
a model diff in the PR is BLOCK; a module created, deleted or renamed under
`src/` or `spec/` in a change of any other class is DRIFT". Two
observations:

- The BLOCK is not built. Nothing checks it, and PR #60, the one
  Architectural change so far, ran without a design phase or a model diff;
  its branch never names O-3 (searched at `ef7407c`). A keyword search of
  the review findings in six change folders found no defect a model delta
  would have caught.
- **Coding Harness has neither `src/` nor `spec/`,** so here the watchman
  watches nothing. Its paths would be `scripts/`, `tools/`, `prompts/`,
  `templates/` and `decisions/gates.yaml`.

**D-58 in LakeSwitch** ("No architecture model as code for now"; drafted
2026-09-24, ratified by signed commit on 2026-09-26 in RC-005). Its reason:
an Architectural change names the touched elements "as the repository's
existing diagrams and ADRs name them", the ADR records the decision, and "a
model as code is one more tool to learn, keep current and explain, which
D-65 names as a pattern to avoid, and no change so far has shown a defect
that a model delta would have caught". It is revisited when a review records
such a defect for the third time.

Does the reason apply to Coding Harness? Both halves do. The tool cost is the
same or higher, since a Python-only CI would gain Node. The defect record is
the same: none so far. One difference makes the case against even stronger.
Coding Harness is the kit, so every instance inherits what it ships, and
shipping a tool that the first instance refused by signed decision makes the
kit heavier for no adopter. LakeSwitch's journal of 2026-09-28 already
proposed the way out: "a signed Coding Harness ADR lifts the model-as-code
parts; the ADR stays required" (proposed, not approved, as far as read).

**D-14 (design phase).** D-14 stays, and the maintainer has just put phase
2b into the template bundle. D-14 names no tool; the "model-as-code delta"
comes from the phase table's row 2b and scenario Q10. Under every option
except (d), `design.md` keeps a section for it; only the content differs
(A6). LakeSwitch's own `design.md` carries "Design Impact" (its D-22), a
text section with no model. Option (c) gives both repositories the same
shape.

### A6 · Options

| | Option | Consequence | What `design.md`'s section says |
|---|---|---|---|
| **(a)** | Build LikeC4 now, as D-15 says. | 3–6 h before the first use (estimate). Node in CI. A model of about ten boxes that nobody can read on a phone. The hierarchy check still missing. The contradiction with D-58 grows: the kit ships what the instance refused. | "**Model delta.** The elements and relationships this change adds, changes or removes in `model/*.c4`, and the views that show them. The same pull request changes `model/`; `likec4 validate` is green. If nothing architectural moves: one sentence why." |
| **(b)** | Defer. D-15 stands, with the revisit trigger of A7. | 0 h now. The target keeps promising a model gate that nothing builds. No Architectural change can meet O-3's BLOCK. The two repositories keep disagreeing in writing (the template bundle's provisional answer to its Q4). | "**Model-as-code delta.** LikeC4 is deferred (D-15 stands; the revisit trigger is in `docs/research/2026-10-05-likec4-roadmap-arc42.md`). Until a model exists: name in words the elements and relationships this change adds, changes or removes, as the existing diagrams and ADRs name them. A Mermaid flowchart may show the state after the change. If nothing architectural moves: one sentence why." |
| **(c)** | Amend D-15 and O-3 by one ADR. The architecture delta lives in `design.md` as a Mermaid flowchart plus lists of what is added, changed and removed. O-3's "model diff" becomes that section. The watched paths become an instance setting. LikeC4 is named as the upgrade path, with the trigger. | One decision pull request, about 1–2 h (estimate): the ADR, the continuity rows for D-15 and O-3 set to Amend, an `AMENDMENT_ADRS` entry in `scripts/check_decision_continuity.py`, the target's wording. No new dependency. Agrees with D-58. Loses MCP queries and one definition for many views until the trigger fires. | "**Architecture delta.** A Mermaid flowchart of the part of the system this change touches, as it is after the change, each box labelled with its C4 level (person, system, container, component). Below it, three short lists: added, changed, removed (elements and relationships). If nothing architectural moves: one sentence why." |
| **(d)** | Drop architecture models entirely. | The simplest kit. But it undoes the fresh decision to keep the delta in phase 2b, and quality goal 8 ("a model as code, readable by a non-developer") and scenario Q10 lose their picture. | No section. "Interfaces" names any new or broken interface; the ADR carries the decision. |

**(b) and (c) produce nearly the same `design.md`.** That is the useful
part. The template bundle can ship the text of (b) now, without waiting for
an ADR. If the ADR for (c) merges, only the heading and the first sentence
change.

### A7 · Recommendation for LikeC4: (c), reached through (b)

1. **Now, in the template bundle:** ship `design.md`'s section with the
   text of (b). It is true today and needs no decision beyond those already
   taken.
2. **Next, as its own decision pull request** (`decide(adr): …`; ADR 0009
   unless another takes the number first): amend D-15 and O-3 to (c).
   Merging it ends the written contradiction with LakeSwitch's D-58.
3. **Revisit LikeC4 when any one of these happens.** The first trigger is
   D-58's, so both repositories move together:
   - a review records, for the third time, a defect in an Architectural
     change that a model delta would have caught, and the reviewer names it
     as such in `findings.md`;
   - the same element appears in three or more architecture pictures, and
     a rename or split had to be made by hand in more than one of them;
   - an agent's work needs dependency queries across more elements than one
     page holds (about thirty), where the MCP server pays.

   When a trigger fires, weigh Structurizr against LikeC4 again: Structurizr
   keeps the C4 hierarchy, LikeC4 does not (A2).

## Part B · A ROADMAP.md template

### B1 · What it would be

The shape the sources agree on (the toolchain document §8.1.2, the review of
2026-09-16, gap analysis P1, the target's "Direction" row): one page in
three sections, Now, Next and Later. Each item is a theme, an outcome, with
one to three sentences of why, an appetite (the time it is worth, Shape Up's
term; see the [ADHD frame note](2026-09-30-adhd-frame.md) §2.2) and, once it
is cut, a pointer to its beads. No tasks, no status. Now/Next/Later comes
from product management (ProdPad, 2012), made to replace dated timelines
whose dates turn into broken promises. The template bundle priced the
template at 30–40 lines and half an hour.

### B2 · What it would answer, and for whom

| Question | Answered today? | With a `ROADMAP.md` |
|---|---|---|
| Which few outcomes matter in the next weeks, and why? | Not in one place. The tracker holds 19 open and 4 in-progress beads (read 2026-10-05): no epics, 16 of the 23 at priority 2. The handover names the next step of one session. The M1–M4 path sits in three documents of 2026-09-17 of about 3,000–4,000 words each. | Yes, on one screen. |
| What is deliberately not now? | Scattered: not-now lists inside change folders, deferred beads, handovers. | The Later list. |
| Does this piece of work, found mid-change, belong to a current theme? | `discovered-from` and bead priority. | The Now themes give an agent a test. |
| What do I do next? | Yes: `tools/bd ready`, the handover's next step, the display's "Einstieg" line. | Nothing new. |

**For the maintainer,** two findings of the ADHD frame note pull in opposite
directions. Writing down a plan for an unfinished goal quiets it (Masicampo
and Baumeister, 2011, ADHD frame note §2.6), and a Later list does exactly
that. But help works "at the point of performance" (Barkley, §2.1), and a
roadmap is a document to look up. It helps only if the session start shows
it. The display already shows the beads in progress and the handover's next
step at session start; a line with the Now themes could join them. Three
themes read well on a phone.

**For agents,** the gain is modest. They work from the change folder and
`tools/bd ready`; a Now list helps them file found work, nothing more.

### B3 · First real use

Now. The maintainer is back from a four-day break with seven pull requests
and 23 beads to choose from. Grouping them into at most three Now themes is
the first use. An illustration only, not a proposal: stage 2 review live
(coding-harness-bc9, coding-harness-kw0); the forms of an M1 change
(coding-harness-9qo, coding-harness-jc3, coding-harness-4me); safe parallel
sessions (coding-harness-36z, coding-harness-9ca, coding-harness-1jg).

In LakeSwitch, the product start of 2026-09-28 would be the first use; its
D-18 already asks for themes (B6).

### B4 · What keeping it current costs

- **Writing it:** about an hour the first time (estimate), most of it the
  maintainer's choice of themes; an agent can draft.
- **Keeping it:** one look at each handover ("is Now still true?"), a few
  minutes (estimate). The toolchain document planned a weekly review; a
  solo maintainer who writes handovers already has the checkpoint.
- **The failure mode is staleness, and this maintainer has met it.**
  Portfolio's consolidated roadmap (state 2026-04-17, 154 lines) was marked
  superseded on 2026-06-01, because it showed overtaken phases as planned or
  in progress; the current state moved into the instruction file and the
  handovers (header read at `20a279c`).
- **A cheap check, later:** every Now theme names at least one open bead. A
  theme whose beads are all closed is stale. The review of 2026-09-16
  proposed the related check that every active change names a Now item.

### B5 · Overlap with what exists

| Artefact | What it owns | Relation to a roadmap |
|---|---|---|
| Beads | Executable work and its status | The roadmap holds no status; it points to beads. LakeSwitch's D-18 puts it as "the roadmap explains why, the Epic groups what, and child Beads track execution". |
| `plans/INDEX.md` | A generated list of change artefacts with their two status fields | What exists, not what matters. No overlap. |
| `target-architecture.md` §12 and the implementation plan | The long path M1–M4 with entry and exit criteria | The roadmap would be its current one-screen slice. It links them, never copies them. |
| Handovers | The state and next step of one session; they age by design | The handover says "next step", the roadmap "toward what". The handover is where the roadmap gets checked. |
| ADRs | Decisions and their reasons | None. |
| The German research documents | The toolchain document makes `ROADMAP.md` "the only planning source" (its ADR-0002, option C: `ROADMAP.md`, GitHub milestones and Beads epics; option D, Beads for everything, was rejected because the ready queue would become a dump). Its scenario S8: after a holiday, `bd ready` and `ROADMAP.md` answer "what now" and "why" in under five minutes. Its risk R13: roadmap and milestones drift apart. The ADW reference architecture does not mention a roadmap (searched). | The source of the shape in B1. |

### B6 · What LakeSwitch does

D-18 "Roadmap and work hierarchy" (ratified 2026-09-26 in RC-003): "The
roadmap contains outcome themes. Each theme maps to exactly one Beads Epic".
No `ROADMAP.md` exists there (searched at `09c9d62`). The view that would
show "a roadmap theme without an open Epic" (D-32) is parked under the lean
frame of 2026-09-28, and the ratification review lists "one roadmap per
repository" as an open minor item.

### B7 · Options and recommendation

| | Option | Consequence |
|---|---|---|
| **(a)** | Template now, in the template bundle. | Half an hour (template-bundle research §3). A form nobody fills yet: the case `docs/WORKFLOW.md` §8 calls "a claim without content". |
| **(b)** | Not now. The template stays on the not-now list; trigger: an instance asks for one. | 0 h. Direction stays spread over 23 flat beads, handovers and three long target documents. |
| **(c)** | The file first, the template later. A trial `ROADMAP.md` in Coding Harness. The kit template is extracted once the file stayed true through two handovers; the file is removed if a handover finds it stale twice. | About an hour now (estimate), then minutes per handover. The template comes from a file that lived. LakeSwitch's D-18 gets a worked example. |
| **(d)** | No roadmap file. Themes become Beads epics, with their why in the description. | No new file. But the Later list either enters Beads (the dump ADR-0002 rejected) or has no home, and every theme is a tracker write. |

**Recommendation: (c).** At most three Now themes, each with an appetite and
its beads by full id; Next and Later as short lists; no status. The
maintainer chooses the themes. It is a small change of its own, outside the
template bundle, which keeps the template on its not-now list until the
trial has run.

## Part C · An arc42 skeleton

### C1 · What it would be

arc42 is a template for architecture documentation in twelve sections:
introduction and goals, constraints, context, solution strategy, building
blocks, runtime, deployment, crosscutting concepts, decisions, quality
requirements, risks, glossary. Version 9.0 is of July 2025, under CC BY-SA
4.0, in 14 formats including Markdown, each "plain" or "with help". Its own
FAQ (B-1) says: "Please don't fill in everything. Document only what your
stakeholders need", because "everything you document will potentially
require maintenance effort in the future". The template bundle priced the
skeleton at twelve headings with one line each: 70–100 lines, half an hour
to an hour.

### C2 · What it would answer, and for whom

| Question | Answered today? | With an arc42 skeleton |
|---|---|---|
| What is this system, its context, its parts, how does it run? (a newcomer; scenario Q13) | In part: `README.md` (210 words), `AGENTS.md`, `docs/WORKFLOW.md`, `target-architecture.md` (10,316 words in arc42's sections 1–11, status superseded) and three documents of 2026-09-17. There is no current one-page "as built" view. | Only once someone fills it. The skeleton itself answers nothing. |
| Where does a decision, a risk, a quality goal go? | ADRs (arc42's section 9), the target's quality scenarios and risks, `design.md` per change. | An agreed order. |

**For the maintainer on a phone,** a filled arc42 is long: LakeSwitch's runs
to 23,415 words and gives a decision maker's reading path "about thirty
minutes" (C6). **For agents,** `AGENTS.md` is the entry; they read code. The
toolchain document names the risk that agents filling arc42 sections invent
architecture facts (its R18), and answers it with explicit open-point
markers.

### C3 · First real use

In neither repository: both already have one. The template-bundle research
names the first consumer: a third instance. Inside Coding Harness, the
nearest use is the onboarding page (D-17, bead coding-harness-lir), which
needs a short "what is built". That is a page, not twelve sections.

### C4 · What keeping it current costs

The skeleton is cheap; the filled document is not.

- Coding Harness's own arc42-form document, `target-architecture.md`
  (written 2026-09-16), was superseded for sequencing the next day. It stays
  as the record of the interview.
- LakeSwitch's page says "measured 15.09.2026" and "7 of 25 modules built".
  At `09c9d62`, 8 module specifications name an implementing package. The
  page dates its own numbers, which is what makes its age visible.

### C5 · Overlap with what exists

- **`target-architecture.md` is already an arc42 instance.** Its sections
  1–11 follow arc42's 1–11 (its §8 "Principles" stands for crosscutting
  concepts). It has no glossary and adds three sections of its own (the
  path, the challenge, what it does not do).
- **Per change,** `design.md` covers arc42's sections 4, 5 and 9, and the
  ADRs section 9.
- **The German research documents.** The ADW reference architecture is
  written in arc42's twelve sections (version 1.2, 2026-09-17). The
  toolchain document wanted the product's arc42 as twelve files in
  `docs/arc42/` (its ADR-0011), filled first by an agent command that marks
  everything without evidence as open. It also names its own way out "if the
  project gets smaller and arc42 too heavy" (translated): the one-page arc42
  canvas, with the ADRs and the C4 model kept.

### C6 · What LakeSwitch does

It wrote arc42 without a template, and not as twelve files:
`docs/architecture.html` is one German page in arc42's twelve sections, with
19 hand-drawn SVG pictures after C4, a register of 23 open points and reading
paths per audience after ISO/IEC/IEEE 42010. It changed five times between
2026-09-16 and 2026-09-27. Its register named "nineteen hand-drawn structure
pictures without a model behind them" (translated) and proposed a C4 model
as text; D-58 declined that on 2026-09-24 (A5).

### C7 · Options and recommendation

| | Option | Consequence |
|---|---|---|
| **(a)** | Skeleton now, in the template bundle. | Half an hour to an hour. Twelve headings no instance needs today. arc42's help texts are CC BY-SA 4.0, a share-alike licence, beside the kit's Apache-2.0 (D-17); headings alone are a smaller question. Not legal advice. |
| **(b)** | Not now. The skeleton stays on the not-now list; trigger: a third instance, or the onboarding page asks for an architecture description. | 0 h. When the trigger fires, the kit links arc42's plain Markdown and names `target-architecture.md` as a worked example. |
| **(c)** | A convention, no file: a paragraph in `docs/WORKFLOW.md` naming arc42's order for an instance's architecture description, with the link, "fill only what a reader needs", and every number with its commit. | Under an hour (estimate). A rule for a document no instance is about to write. |
| **(d)** | Drop arc42 from the kit. | The instances keep what they have; the kit says nothing. Loses the shared order a third instance would start from. |

**Recommendation: (b).** Both repositories show that the description gets
written anyway, in arc42's order, without a skeleton, and that it ages
fast. A skeleton adds nothing until an instance starts from zero.

## 2 · Not read or not verified

- **Mermaid's C4 syntax on GitHub:** two community sources disagree
  (2026-06-03: shown as raw text; 2026-09-25: renders). Not rendered here.
  A one-minute check: open `docs/research/Lake-Switch-Architektur-arc42.md`
  on github.com, which holds a `C4Context` and a `C4Deployment` block.
- **The `@{ shape: … }` node syntax** that `likec4 gen mermaid` writes:
  whether GitHub's bundled Mermaid renders it is not verified.
- **Mermaid in the GitHub Mobile app:** not verified. This is the same open
  point as in the [decision pull request note](2026-09-30-decision-pull-requests.md)
  §2.5; one test on the phone settles both.
- **`likec4 build` and `export png`** were not run, and the size of
  Playwright's browser download is not measured.
- **The default Node.js of the `ubuntu-latest` runner:** not checked. A CI
  step would pin Node.js ≥ 22.22.3 itself.
- **Structurizr** was not run; this machine has neither Java nor Docker. Its
  facts come from its documentation and repository.
- **The review findings** were searched by keyword ("diagram", "architect",
  "model delta"), not read row by row.
- **LakeSwitch's `docs/architecture.html`** was read as extracted text:
  headings and searched passages, not in full.
- **Portfolio's archived roadmap:** only its header and first table were
  read.
- **LakeSwitch's journal plan of 2026-09-28:** whether it was approved
  later was not read.
- **arc42's licence beside Apache-2.0:** a question to check, not legal
  advice. No arc42 FAQ entry other than B-1 was read.
- **The hours** in A4, A6, B4, B7 and C7 are estimates, not measurements;
  so are the template-bundle research's.
- **The Thoughtworks Radar** was searched as text extracted from the PDFs.
  An entry under another name would have been missed.

## Sources

Strength: **official** = the tool's or vendor's own documentation or
repository; **practice** = the documented experience of a named
organisation; **community** = an issue, discussion or blog;
**measured** = run or queried in this session.

- **likec4-repo:** <https://github.com/likec4/likec4> — official; GitHub API
  read 2026-10-05 (licence, releases, commits, contributors)
- **likec4-npm:** <https://registry.npmjs.org/likec4/latest> and
  <https://api.npmjs.org/downloads/point/last-month/likec4> — official,
  2026-10-05 (version, `engines`, dependencies, downloads)
- **likec4-cli:** <https://likec4.dev/tooling/cli/> — official, read
  2026-10-05
- **likec4-mcp:** <https://likec4.dev/tooling/mcp/> — official, read
  2026-10-05
- **likec4-spec:** <https://likec4.dev/dsl/specification/>, source
  `apps/docs/src/content/docs/dsl/specification.mdx` — official, read
  2026-10-05
- **likec4-vscode:** VS Code Marketplace query for `likec4.likec4-vscode`
  and <https://open-vsx.org/api/likec4/likec4-vscode> — official,
  2026-10-05
- **likec4-actions:** <https://github.com/likec4/actions> — official, API
  read 2026-10-05
- **structurizr:** <https://github.com/structurizr/structurizr> (README),
  <https://github.com/structurizr/lite> (README: no further updates),
  <https://docs.structurizr.com/>, <https://docs.structurizr.com/binaries>,
  <https://docs.structurizr.com/dsl/language> — official, read 2026-10-05
- **c4-plantuml:** <https://github.com/plantuml-stdlib/C4-PlantUML> —
  official, API read 2026-10-05
- **mermaid-c4:** <https://mermaid.js.org/syntax/c4.html> — official, read
  2026-10-05; <https://github.com/mermaid-js/mermaid> (12.1.0 of
  2026-10-02; `packages/mermaid/src/diagrams/c4`) — official
- **gh-diagrams:** <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams>
  — official, read 2026-10-05
- **gh-c4-no:** <https://github.com/orgs/community/discussions/197898> —
  community, 2026-06-03; weak: closed by a bot, no evidence shown
- **gh-c4-yes:** <https://github.com/skrymer/tucker/issues/391> — community,
  2026-09-25; weak
- **c4model-tooling:** <https://c4model.com/tooling> — official (the C4
  model's author), read 2026-10-05
- **radar-34:** <https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2026/04/tr_technology_radar_vol_34_en.pdf>
  — practice, April 2026 ("Architecture drift reduction with LLMs", Assess);
  volumes 33 (2025-11) and 32 (2025-04) under the same path pattern,
  searched for LikeC4 and Structurizr
- **arc42-download:** <https://arc42.org/download> — official, read
  2026-10-05 (version 9.0 of July 2025, CC BY-SA 4.0, formats)
- **arc42-faq-b1:** <https://faq.arc42.org/questions/B-1/> — official, read
  2026-10-05
- **prodpad-nnl:** <https://www.prodpad.com/glossary/now-next-later-roadmap/>
  — practice (the method's originator, a vendor), seen through a search
  summary on 2026-10-05; the page itself not read
- **adhd-frame:** [2026-09-30-adhd-frame.md](2026-09-30-adhd-frame.md) —
  this repository's note; Barkley (§2.1), Shape Up (§2.2) and Masicampo and
  Baumeister (§2.6) with their own sources and strengths
- **trial:** A2 — measured 2026-10-05
- **Repository and tracker reads:** section 1 — measured 2026-10-05
