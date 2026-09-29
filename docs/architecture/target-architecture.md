---
title: "Target architecture: the coding harness and its workflows — what it should be, what it should not be, and the path there"
category: architecture
status: superseded
superseded_by: 2026-09-17-omnigent-first-target.md
created: 2026-09-16
last_reviewed: 2026-09-18
updated: 2026-09-29
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-16"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [architecture, target, harness, workflow, kit, lakeswitch, portfolio, roadmap]
---

# Target architecture: the coding harness and its workflows

**Historical proposal, measured at `5a950c2`.** The maintainer's 2026-09-17
direction puts parallel Omnigent coordination in the first proof of concept.
The [current target](2026-09-17-omnigent-first-target.md),
[gap analysis](2026-09-17-gap-analysis.md) and
[implementation plan](2026-09-17-implementation-plan.md) supersede this
document for sequencing and current-state claims. The decisions below remain
a dated record until individual ADRs replace them. The current target’s
[decision continuity table](2026-09-17-omnigent-first-target.md#decision-continuity)
maps every D-1–D-17 and O-1–O-4 outcome. Earlier recommendations below do not
override those outcomes. Editorial corrections on 2026-09-18 clarify counts
and internal references; they do not change the recorded interview.

**Status: decided in interview, not yet an ADR.** The seventeen decisions in
§9 were taken with the maintainer on 2026-09-16 (outcomes in §9.1); two
went against the recommendation (D-1, D-7), one was amended (D-2), three
recommendations were revised after a best-practice check (D-5, D-10,
D-15) — all marked. The path in §12 reflects
them, with the Omnigent migration plan as the main path. The first ADRs of
this repository turn §9.1 into records. Written at coding-harness `5a950c2`,
portfolio `4ce8240`, lakeswitch-ai `458a12c`.

**Sources.** The three research documents under `docs/research/` and the
review of them (`2026-09-16-review-corpus-vs-running-workflow.md`, cited as
"the review"); the running workflow (`WORKFLOW.md`, `regelwerk.md`, prompts,
kit manifest); portfolio's ADRs 009–031 and its gate list; lakeswitch-ai's
`AGENTS.md`, `docs/workflow.md`, `decisions/` and `spec/`. Where a principle
comes from somewhere public, §8 names it. Where this document departs from
mainstream practice, §13 says so and why.

**Form.** arc42 sections, shortened. The corpus is arc42; a reader who knows
the three research documents finds the same chapters here.

## 1 · Purpose and quality goals

### 1.1 What the harness is for

A repository that owns *how software is built with coding agents* — the
phases, the artefacts between them, the gates, the rules and their enforcers,
the model routing, the tracker conventions — so that two very different
repositories (a governance framework, a Python product) run the same process
and can prove it. The harness produces no software of its own. Its product
is a kit that instances copy and a measurement of how well the copy carries.

**Intended audience, decided 2026-09-16:** a **public template**. Strangers
clone it. That decides the language (English throughout), the licence, an
onboarding page, and that no customer, employer or vendor name appears in the
harness — vendors only in an instance's configuration.

### 1.2 Quality goals, prioritised

| # | Goal | Scenario that proves it (§10) |
|---|---|---|
| 1 | **Correctness against intent** — what ships matches the spec a human owned | Q1 |
| 2 | **Reconstructability** — a stranger rebuilds any change's story from files alone | Q2 |
| 3 | **Human capacity** — a human spends minutes per change, on intent only | Q3 |
| 4 | **Enforcement that can go red** — no rule without a test or a valve; no gate over an empty set | Q4 |
| 5 | **Harness independence, measured** — the kit runs in a foreign repository and under a foreign harness; the divergence is a number | Q5 |
| 6 | **Data residency before model diversity** — nothing customer-shaped reaches an undeclared endpoint | Q6 |
| 7 | **Model independence** — the doctrine names what a phase needs, never which model; routing is configuration | Q9 |
| 8 | **Architecture is designed, recorded and visible** — a design phase with an artefact, ADRs and a model as code, readable by a non-developer | Q10 |
| 9 | **Scalable on two axes** — solo → team without changing artefacts; three → many instances without losing the measurement | Q11, Q12 |
| 10 | **Context economy** — the enforcement layer costs the agent little window | Q7 |

Goal 6 outranks goal 10 and every cost argument; it is the one goal a single
violation cannot repair.

## 2 · Constraints

| # | Constraint | Consequence |
|---|---|---|
| C1 | **One maintainer today.** All three repositories have one human; roles are named but held by one person. | Human gates are one-word vetoes on open decisions, not approval steps; approver ≠ author (RB-M2) stays a valve until a second person exists. |
| C2 | **Customer estate in scope.** portfolio and lakeswitch carry abstracted knowledge from a productive customer project; `oracle-source-inventory` is a read-only boundary. | Endpoint residency (RB-A6) and the leak-check barrier are preconditions for any foreign model, not options. |
| C3 | **Harness volatility.** Claude Code, Codex, Cline, Omnigent change monthly; Omnigent is alpha with a critical CVE in its history (research, `unverified`). | Nothing of value lives only in a harness adapter; adapters are thin and disposable (WORKFLOW §1). |
| C4 | **Tracker fragility, measured.** The Beads export broke three times in four days (WORKFLOW §3); in portfolio `bd create` produces a wrong id prefix because the repository's prefix exceeds the eight characters `bd rename-prefix` allows (wp-p0.1, open since 2026-09-02, reproduced 2026-09-16 in a worktree and in the main checkout). | One writer per tracker, one bead per change, export written by one script at one moment; a prefix chosen at `bd init` within the tool's limits. |
| C5 | **Budget.** Frontier models per phase, not per token; cross-vendor only where residency allows. | Routing table per phase; escalation rules; spend caps once a runner exists. |
| C6 | **Language.** Content artefacts are English by decision; most of portfolio is still German. | The harness is English throughout, from the first public tag; instances migrate file by file, and a translated corpse is a finding (lesson recorded in portfolio). |
| C7 | **Git is the source of truth; mirrors are push-only** (portfolio ADR-011/015/022). | No planning tool, wiki or issue mirror is ever read back as truth. |
| C8 | **Public template.** The harness will be cloned by people who know none of the three repositories. | No customer, employer or vendor reference in the harness; vendor names live only in an instance's routing configuration; a licence, an onboarding page and a public-readiness gate (a denylist scan, the mechanism lakeswitch already has) before the template switch. |

## 3 · Context

```
                      lessons, findings, ADRs (governance)
   portfolio-agentic-engineering  ◄──────────────────────────┐
     framework governance, domain content, OSI→lakeswitch     │
              ▲  copies the kit, runs the Leerprobe            │
              │                                                │
        coding-harness  ── kit (copy, measured) ──►  lakeswitch-ai
     doctrine · rules · prompts · templates ·        product, clean-room
     kit · routing · endpoints · handover             instance of the workflow
              ▲
              │ research corpus (dated sources, never normative)
   oracle-source-inventory: customer instance — read-only boundary for all three
```

**Flows.** The kit travels *outward* by copy, and the Leerprobe measures how
much of it still runs in the target. Lessons travel *inward* as files
(handover with `direction: framework->project` or the reverse), never as
chat. Rules are born in the harness; domain gates (contract acceptance,
reconciliation, cutover) are born in the instances and stay there.

## 4 · Solution strategy

Eight strategy choices, from which the historical proposal follows. S5’s
late orchestration sequence was replaced by the 2026-09-17 direction; the
current target permits early parallelism only after its explicit prerequisites.

| # | Decision | Replaces | Source |
|---|---|---|---|
| S1 | **Artefact-centred control.** Every phase leaves a versioned file; the next phase reads files, never the conversation; the session ends with a handover file. | dialogue-driven agent work | ADW S1/I1; OpenSpec; Beads "landing the plane" |
| S2 | **Intent to the human, mechanics to the model, presence to the machine.** A phase gate checks that an artefact is there and complete; a human sees only open `[DECISION]` marks; the veto is one word. | approval gates G1–G3 as human steps | WORKFLOW §2; Bezos two-way doors; Stage-Gate "kill" option; PRINCE2 management by exception |
| S3 | **Every rule enters through the ladder.** Rule sentence, enforcement level 1–5, the test or gate that holds it, or a ramp valve with a due date. Prose that cannot be levelled is a lesson, not a rule. | normative prose (the reference architecture's twenty MUSS rows and forty referenced rules, none naming its enforcer) | regelwerk §2–3; HashiCorp Sentinel's advisory / soft-mandatory / hard-mandatory as the nearest public analogue |
| S4 | **Copy and measure, never depend.** Instances copy the kit; the Leerprobe reports what carries; divergence is allowed and counted. | a versioned dependency on the harness | kit manifest; clean-room principle (lakeswitch); hermetic-build thinking |
| S5 | **Host early, orchestrate late.** Omnigent as session host with policies, sandbox and cost caps starts now, additively (Migrationsplan M0–M1); Omnigent as orchestrator with cross-vendor review (M2) starts only when the stage-2 criteria of D-13 are met — the residency rule RB-A6 is a level-4 gate, not a preference. The server never holds state the repository and the tracker do not also hold. | "process, then diversity, then orchestration" (WORKFLOW §6) as a strict sequence | decided 2026-09-16 (D-7); Migrationsplan; toolchain ADR-0007 (additive); ADW IS-5 |
| S6 | **The harness is small.** Everything an instance does with knowledge, publication, release or domain stays out. Architecture templates are the exception (S8). | the toolchain document's full stack in the kit | ADW C7 (short artefacts); regelwerk RB-S1 (instruction budget) |
| S7 | **Phase requirements, not model names.** The doctrine says what a phase needs (much input and little reasoning; highest reasoning; a reliable worker; a reviewer from another lineage). A routing file in the instance says which model meets it today. | "Stage 1: only Claude Code, only Anthropic" as doctrine | decided 2026-09-16; ADW ADR-14 (role-based routing) |
| S8 | **Architecture is a phase with an artefact.** Architectural changes pass a design phase, Feature changes by stated reason (`design.md`: alternatives, interfaces, data model, ADR draft); the kit ships arc42 and MADR templates and a LikeC4 specification and model template (D-15); an architecture change without an ADR or model update is a finding. | architecture decided inside the plan, or not at all | decided 2026-09-16; ADW P2; OpenSpec `design.md`; arc42; MADR; C4 |

## 5 · Building blocks

### 5.1 The harness — nine layers

| Layer | Holds | Today (coding-harness `5a950c2`) | Target | Gap |
|---|---|---|---|---|
| **H1 Doctrine** | `WORKFLOW.md`: phases, gates, question protocol, session handover, stages | Copied from portfolio; German; no task classes; five meanings of "Stufe" across the corpus | English; task classes with the one-way ratchet (§6.1); one stage vocabulary (review §6); session lifecycle as a section, not an afterthought | rewrite after §9 D-1, D-12 |
| **H2 Rule set** | `regelwerk.md`: six families A agents / H hooks / G gates / M human gates / P provenance / S structure, each row with level, enforcer, scope | Copied; three M rows are domain rules (M-3 contract acceptance, M-4 reconciliation, M-5 boundary before close) whose enforcers stayed in portfolio; 21 of the 60 red tests are `test_regelwerk` | Harness families A, H, G, P, S, the harness part of M (M-1 gate record, M-2 signature, M-6 ruleset, M-7 code owners, M-8 roster) and a new family **W workflow** for the adopted corpus rules; the domain rules M-3/M-4/M-5 and HG-1–4 go to portfolio; every remaining row names a test in *this* repository or a valve | split (§9 D-9); intake of review §5.9 |
| **H3 Prompts and templates** | `prompts/01–07`, `01a`, `02a`; `templates/` | Prompts present, no design prompt; `templates/` holds only `gate-record.yaml` and `handover.md` — `findings.md` and `plan-marking.md` are still in portfolio and `WORKFLOW.md` links to them into the void; there is no spec template in either repository, the spec contract lives in `prompts/02-spec.md` and already requires non-goals; no ROADMAP, arc42, MADR, C4 or verification-report template | Prompt `02b-design.md` and `design.md` template; a spec template carrying the prompt's contract plus *class, protected areas, failure mode, size* and a *Definition of Done* section (D-2); `findings.md` and `plan-marking.md` moved here; `ROADMAP.md`, arc42 skeleton, MADR record, the LikeC4 specification pinning the four C4 element kinds (D-15); machine-rendered verification report | templates PR (M1 prerequisite) |
| **H4 Kit** | `scripts/kit/manifest.yaml` (roles `mechanismus` / `geruest` / `bestand`), `probe.py`, the scripts that travelled (`plans_registry`, `ramp_valves`, `handover_schema`, `gate_record`, `new_change`, `ci_gates`, `_verdict`) | 24 mechanism entries; Leerprobe 173 of 235 green (portfolio, 2026-09-16); coding-harness has no `ci.yml`; 60 red tests at `5efe809` (27 `test_ci`, 21 `test_regelwerk`, 11 `test_feedback_channel`, 1 `test_model_endpoints`; 64 with `test_kit` included); `validate_change_artefacts.py` — the presence gate of phases 2 and 3 — stayed in portfolio as `bestand` and is not in the kit | **Decided (D-10):** the canonical one list is a platform-neutral gate file plus one `verify` command (lakeswitch's `decisions/gates.yaml` pattern); `ci.yml` is derived from it and a check reports drift; portfolio migrates its 36 steps into the gate file, the two-reader adapter is a transition only; `validate_change_artefacts.py` becomes a mechanism entry (D-11) | `bo0`, `2ee`, `9qo`; gate-file schema; portfolio migration bead |
| **H5 Routing and endpoints** | `model-endpoints.yaml`; per-phase routing; `cc-*.sh` profiles; `run_change.sh`; `make leakcheck` | Endpoints declared and tested (RB-A6); the routing table with vendor names sits inside `WORKFLOW.md`; profiles and runner are in portfolio, not yet here | The doctrine carries a **phase-requirement table** (§6.6); a `model-routing.yaml` per instance maps requirement → model → endpoint, validated against `model-endpoints.yaml` by one test; the shipped example is the Anthropic-only stage 1. Runner with stop conditions; stage-2 activation as numbers (§12 step 4) | S7; routing file + test; runner travels |
| **H6 Harness adapters** | `.claude/` (agents, commands, hooks, settings), `.codex/`, `.agents/skills/` | `SessionStart → bd prime`; nothing else here yet | Thin by test: the Leerprobe must reach the same result with the adapter directory deleted; `AGENTS.md` ≤ 200 lines is the only instruction file — no `CLAUDE.md` (maintainer decision 2026-09-22; Claude Code ≥ 2.1.277 reads `AGENTS.md` itself; supersedes the `@AGENTS.md` import of review D10) | prove before M0 that the direct read works with telemetry off; adapter-independence test |
| **H7 Tracker conventions** | `tools/bd` pin; prefix fixed at init; one bead per change; `Closes-Bead:` trailer; `discovered-from` for found work; export single writer; worktrees in the repository via the tool's own mechanism | Pin and prefix done; `export.auto true`; no `discovered-from` rule; close-by-trailer gate not here; worktrees as sibling directories by hand | The rules from C4 with enforcers: `dangling-beads`, `merged-beads`, export identity, `export.auto` off (D-4); worktrees under `.claude/worktrees/` or `bd worktree create`, base `fresh` (D-5); no `bd` writes from a worktree until the two-writer test is green | D-3, D-4, D-5 decided |
| **H8 Evidence** | provenance classes (`provenance.yaml`), generated facts blocks, handover schema, gate records for human gates, verification report for machine gates | Provenance and handover schema present; facts pipeline stayed in portfolio (`bestand`) | Machine-rendered `verification-report.md` per change; facts pipeline as a kit entry or an instance duty — decided, not assumed | §9 D-11 |
| **H9 Entry and readability** | `README.md`, an onboarding page, `docs/_INDEX.md` routed by situation, generated indices (`plans/INDEX.md`, ADR index), licence | README and bootstrap handover; no onboarding page, no licence, no situation index | A stranger's path: README → onboarding (one afternoon to a first Bounded change) → situation index; decisions written as questions with consequences (P3) so a product owner or architect can answer them without a session; licence (Apache-2.0, as lakeswitch) from foundational work, per D-17 | §12 step 1 and the template switch |

### 5.2 The instance layer — deliberately outside the harness

| Instance | Keeps as its own | Adopts from the harness | Does not adopt |
|---|---|---|---|
| **portfolio** | ADR-026 knowledge levels; domain gates HG-1–4; error catalogue, lessons, evidence pipeline; Databricks content; OSI→lakeswitch transfer; German prose during migration | The full kit; `ROADMAP.md`; task classes | — (it is the origin; the severance PR removes what moved) |
| **lakeswitch-ai** | `decisions/` roots with the floor (14 floor gates of 28), `decisions/gates.yaml` as the one list, `lakeswitch verify`, `spec/` module specifications, `plugin/` guards, CODEOWNERS, `journal/` | `plans/` roots (its `docs/workflow.md` already promises them, §8 says they are not built), prompts 01–07 next to its `implement-a-module.md`, `WORKFLOW.md` as a copy with an instance addendum, `ROADMAP.md`, the spec-template fields, handover schema | The toolchain document's Obsidian inbox, LikeC4, Argdown, static site, `openspec/`, pre-commit as a second list, Omnigent before stage 3, the ticket schema as contract |

The toolchain research document describes a Lake Switch with `brain/`,
`model/`, `ROADMAP.md`, `openspec/` and `.claude/worktrees/`. The lakeswitch-ai
repository at `458a12c` has none of these and instead has a floor, a one list
in YAML, 25 module specifications and a `verify` command. **The target for
lakeswitch is the repository that exists, extended by the kit — not the
document.** What the document contributes is listed above; the rest waits for
an instance ADR.

## 6 · Runtime views

### 6.1 A change, by class

Classes and the ratchet from ADW §8.2, mapped onto the seven phases (review
§5.5). The class is a frontmatter field of `spec.md`; the validator checks it
is present and one of four.

The phases, with the design phase added (S8):

| # | Phase | Artefact | Gate |
|---|---|---|---|
| 1 | Explore | `research.md` | — |
| 1a | Interview (optional, human-called) | `decisions.md` | every `[DECISION]` answered or skipped with a reason |
| 2 | Spec | `spec.md` (goal, acceptance criteria, non-goals — plus `class`, protected areas, failure mode, size) | validator green, no open `[DECISION]` |
| 2a | Spec review (other lineage, fresh context) | rows in `findings.md`, dimension SPEC | no open `[AMBIGUITY]` |
| **2b** | **Design** (Feature optional, Architectural mandatory) | `design.md`: alternatives with consequences, interfaces, data model, ADR draft, model-as-code delta | validator green; an ADR draft exists when the class is Architectural |
| 3 | Plan | `plan.md` (marked per segment) | validator green |
| 4 | Implement | code + tests, each test with its counterpart | `make verify` green |
| 5 | Verify | the run's output, rendered as `verification-report.md` | a red tree does not end a turn |
| 6 | Review | `findings.md` | no open BLOCKER; `[DIVERGENT]` counts as BLOCKER |
| 7 | Commit | pull request; ADR and model update in the same PR when 2b ran | CI green |

| Class | Recognition | Phases | Human touch |
|---|---|---|---|
| **Spike** | a feasibility question; output is a recommendation | 1, time-boxed; `research.md` with a recommendation and a stop reason | reads it |
| **Bounded** | change to an existing, readable flow; without such a flow it is not bounded | 4 · 5 · 7; `spec.md` of a few lines | open `[DECISION]` marks; merge |
| **Feature** | self-contained deliverable | 1 · 2 · 3 · 4 · 5 · 6 · 7; 1a, 2a, 2b by the author's stated reason | open `[DECISION]` marks; merge |
| **Architectural** | new subsystem or interface break | all; 1a, 2a, 2b mandatory; an ADR in the change | open `[DECISION]` marks; reads `design.md` and signs the ADR; merge |

**Ratchet:** up mid-change with a stop and a reason in the artefact; never
down. "Do not plan what fits in one sentence" is the lower edge of Bounded.

### 6.6 What a phase needs — the requirement table that replaces model names

| Phase | Needs | Example configuration (stage 1, Anthropic-only, lives in `model-routing.yaml`) |
|---|---|---|
| 1 Explore | much input, little output, no deep reasoning | a small fast model |
| 1a Interview · 2 Spec · 2b Design · 3 Plan | the highest reasoning available, little output; an error here is the most expensive | the strongest model |
| 2a Spec review · 6 Review | a fresh context that never saw the author's reasoning; a different lineage where residency allows, otherwise at least a different model | a second strong model; stage 2: another vendor behind the leak check |
| 4 Implement | a reliable worker given a clear plan; the token-heavy phase | a mid-class model |
| 5 Verify | deterministic — no model | — |
| 7 Commit | cheap and sufficient | a small model |
| Escalation | two failed review rounds, or security/concurrency, or a change above roughly 200k tokens → the strongest model; back down after a pass | — |

The doctrine carries the left two columns. An instance's routing file carries
the third, validated against its endpoint declaration.

### 6.2 A session

```
start   → AGENTS.md (≤ 200 lines) · bd prime · the change's files, nothing else
work    → one change · one worktree · files as handover between phases
end     → docs/journal/handover/<date>-<name>.md (schema-checked)
        → bd close what a merged PR declared · notes on open beads
        → export rendered by the one writer · git push · bd dolt push
```

The session end is the eighth movement (WORKFLOW §2) and is the same
sequence Beads calls "landing the plane" (AG-5). It is mandatory for
unattended runs too — inside the runner, not after it.

### 6.3 A lesson becoming a rule

```
lesson (journal, handover, findings)      experience — never binding
   │  someone writes the rule sentence
   ▼
rule candidate in regelwerk.md            level 1–2, valve with due date
   │  someone writes the test or gate
   ▼
rule at level 3–5                         CI reports (3), blocks (4), or a hook refuses (5)
   │  valve gate: due date passed and level not raised → red
```

No confidence scores, no automatic promotion (review §5.6). The valve is the
only clock.

### 6.4 An unattended stage-2 run

`run_change.sh` reads the marked plan, groups consecutive marks into
segments, runs each as a fresh session, runs `make verify` after each,
pauses with exit 2 on an open `[AMBIGUITY]`, BLOCKER or MAJOR. Target
additions: max segments, wall-clock limit, idle detection (no new commit in
N segments), a spend cap per run once the profile exposes cost, and the
session-end sequence inside the run. Every stop condition has a fake-session
test (`tests/test_orchestrator.py`).

### 6.5 A kit update reaching an instance

1. The harness tags a state (`kit-YYYY-MM-DD`).
2. The instance copies the mechanism entries (a script in the kit does it;
   `geruest` entries are created empty, `bestand` is untouched).
3. The instance's CI runs the Leerprobe: red cases are classified against
   `REIST_NICHT` (reasons only shrink).
4. Divergence is a number in the instance's evidence; a valve says how far it
   may drift before someone looks.

No submodule, no package, no `uses:` reference — §13 says why, and when that
should change.

## 7 · Deployment

| Repository | Holds | Travels out | Travels in |
|---|---|---|---|
| coding-harness | H1–H9; research corpus; its own ADR series (starting with §9) | the kit, by tag | lessons and findings from both instances as handover files |
| portfolio | governance, domain, evidence, lessons; a *copy* of the kit | — | kit tags |
| lakeswitch-ai | product; floor; one list in YAML; a *copy* of the kit | — | kit tags |

**Branch protection** is the security boundary in all three (portfolio
ruleset RB-M6; lakeswitch CODEOWNERS + `floor.yml`); harness policies, hooks
and sandboxes reduce blast radius and are never the boundary (ADW IS-5).

**One server component, additive from M0** (D-7): the Omnigent server as
session host and policy engine, pinned, telemetry off, OSS variant. It adds
enforcement and observability; it never replaces the git-native gates
(toolchain ADR-0007, P6), and a meta-harness that holds state the repository
and the tracker do not also hold is disqualified.

### 7.2 Scaling — two axes, equal in the target, team first on the path

**Axis T: people.** The artefacts do not change; what changes is who may
sign what, and which valves close.

| Level | Trigger | What becomes real | What the harness ships |
|---|---|---|---|
| T0 solo (today) | — | Human gates are one-word vetoes on open marks; approver = author; admin bypass on branch protection is documented debt | valves for RB-M2 (approver ≠ author) and RB-M6 (ruleset) |
| T1 second person | first collaborator | Approver ≠ author enforced; CODEOWNERS review on, bypass off; gate records carry two names; a triage duty for `discovered-from` beads | the valves close; a roster with two handles; `/decompose`-style confirmation becomes a real approval |
| T2 several | third and beyond | Roles held by different people (intent owner, architect, reviewer); per-person budgets; a board as a push-only view of beads | role-to-handle roster; budget per profile; board export script |

**Axis I: instances.** Copy and measure carries three instances; beyond that
the copy needs a version.

| Level | Trigger | Mechanism | What changes |
|---|---|---|---|
| I1 ≤ 3 instances (today: 2) | — | copy by tag, Leerprobe in each instance's CI, divergence valve | — |
| I2 > 3 instances | a fourth instance | the harness becomes a **Copier** template (the mainstream tool for templates that can be *updated* in place, with a diff); `copier update` replaces the copy script; a compatibility matrix (kit tag × instance) is generated | the kit manifest stays the source; Copier's `_answers` file is the instance's record of what it took |

Team first on the path: lakeswitch, as a product, gets a second person before
a fourth instance exists.

## 8 · Principles — what an instance applies, with the source of each

These are the principles lakeswitch and portfolio apply when they run the
workflow. Each names where it comes from; the ones marked *own* have no public
source and §13 challenges them.

| # | Principle | One line | Source |
|---|---|---|---|
| P1 | **The file is the handover** | Next phase, next session, next reviewer reads files; what is only in the chat did not happen | OpenSpec / Spec Kit artefact model; Beads "landing the plane"; ADW I1/I2 |
| P2 | **Intent is human, mechanics are the model's, presence is the machine's** | A human answers `[DECISION]`; the model decides `[DETAIL]` with a reason in the artefact; a validator checks the artefact is there | Bezos one-way vs two-way doors; Cooper Stage-Gate; PRINCE2 management by exception |
| P3 | **Ask by protocol** | `[DECISION]` → human · `[GAP]` → explore · `[DETAIL]` → decide; a mechanics question to the intent owner is a protocol violation | MADR (a question is a decision record in question form); Nielsen heuristics 2 and 6 |
| P4 | **Proportionality by class, ratchet up only** | Spike / Bounded / Feature / Architectural decide the phases; class goes up mid-change, never down | Spec Kit task sizing; ADW §8.2 I5/I6; Shape Up appetite |
| P5 | **A rule names its enforcer or its valve** | Level 1–5; without a test, at most level 2 and a due date | *own*; nearest public analogue: Sentinel enforcement levels; "policy as code" |
| P6 | **A gate must be able to go red** | Every gate has a mutation test (a known-bad case that turns it red) and asserts a non-empty subject set | Mutation testing (PIT, Stryker, mutmut); ADW §8.7 non-vacuity |
| P7 | **Independent review: fresh context, other lineage where residency allows** | The reviewer never sees the author's reasoning; findings are a table; two fix-origin rounds are an escalation | ADW I4; pass@k vs pass^k; ensemble review |
| P8 | **One list** | Exactly one artefact enumerates the gates; every runner derives from it; a second list is the cause of drift, not a symptom | DRY; RB-G1; lakeswitch G-1 |
| P9 | **Numbers are generated, provenance is declared** | Counts come from a generator with an input hash; every artefact names its class and the hand that made it | Reproducible research; SLSA provenance (analogue); RB-P1/P3 |
| P10 | **Portability is measured, not asserted** | The kit runs in an empty repository and the red cases are classified | Clean-room principle (lakeswitch); hermetic builds |
| P11 | **Residency before diversity** | Every model resolves to a declared endpoint with residency; customer-shaped content only to declared residency; leak check before any foreign call | GDPR transfer principles; RB-A6 |
| P12 | **Process, then diversity, then orchestration** | Stage 2 after a measured stage-1 signal; stage 3 additive and evaluative | Anthropic guidance on agent complexity; WORKFLOW §6; toolchain ADR-0007 |
| P13 | **One tracker, one bead per change, one export writer** | Beads only; the bead is status, the file is content; the export is rendered by one script at session end | Beads docs (sync concepts); C4 |
| P14 | **Every number carries its cut-off** | A handover, a journal, a report names commit or date next to every count | RB-P5; WORKFLOW §2 |
| P15 | **Short instructions, short artefacts** | `AGENTS.md` ≤ 200 lines; spec 1–3 pages; findings as rows | Anthropic guidance on `CLAUDE.md`; ADW C7, P1-8; RB-S1 |
| P16 | **Phase requirements, not model names** | The doctrine says what a phase needs; the instance's routing file says which model; a vendor name in the doctrine is a finding | decided 2026-09-16; ADW ADR-14 |
| P17 | **Architecture leaves a record and a picture** | Architectural changes carry `design.md`; Feature changes may omit it with a stated reason (D-14); O-3 defines the ADR/model checks | arc42; MADR; C4 (Structurizr DSL or LikeC4); OpenSpec `design.md` |
| P18 | **Written for a stranger** | Every page, question and PR text carries its meaning without the session; a stranger reaches a first Bounded change from the README in one afternoon | Nielsen heuristics 2 and 6; C8 |

## 9 · Decisions

D-1 to D-8 are the review's; D-9 to D-17 are new; D-14 to D-17 follow from
the goals decided on 2026-09-16 (model independence, architecture
accessibility, two scaling axes, public template). The table below is the
proposal as it was put to the maintainer; §9.1 records what was decided.

### 9.1 Outcomes of the interview, 2026-09-16

| # | Decided | Against the recommendation? | Consequence |
|---|---|---|---|
| D-1 | **Rename everywhere, corpus included.** One vocabulary: Stage 1–3 (model routing), Setup step S0–S7, Team level T0–T2, Omnigent adoption M0–M4, enforcement level 1–5. | yes — the recommendation kept the corpus untouched | the corpus correction PR (D-8) carries the renames; the research index carries the table until then |
| D-2 | **`spec.md` is the contract**, the bead holds status. The spec template gains `class`, protected areas, failure mode, size — and a **Definition of Done** section (which gates must be green, what "done" means beyond the acceptance criteria), presence-checked by the validator. | no (DoD added on the maintainer's request) | spec template written; validator rule; prompt 02 references the template |
| D-3 | One bead per change; task beads under an epic only once stage 2 has two workers claiming, then with `discovered-from` edges. | no | WORKFLOW §2 sentence |
| D-4 | One script writes the export, at session end, with an identity gate; `export.auto` off. | no | coding-harness config; gate into the one list (`bo0`) |
| D-5 | **Worktrees in the repository via the tool's own mechanism** (`.claude/worktrees/` through Claude Code, `bd worktree create` elsewhere), base `fresh` from the remote default branch; sibling directories retired. **No `bd` writes from a worktree until the two-concurrent-writers test is green** in a throwaway repository, with the prefix case as a fifth check. | revised after the best-practice question: both tools converge on in-repo placement | house rule now; verification bead; then the write ban lifts — **lifted 2026-09-23**: all five checks green with bd 1.3.0 (`docs/research/2026-09-23-worktree-tracker-writes.md`); the one-writer rule stays |
| D-6 | Instance gates stay in the instance; the kit keeps `ruff` and `pytest`. | no | lakeswitch adds `mypy`, `hypothesis` to its own list |
| D-7 | **The full Migrationsplan is the main path**, M0–M4 in order, starting now. The maintainer wants the Omnigent stage as early as possible. One entry condition stays because it is an enforced rule, not a preference: M2 (cross-vendor review) starts only when the foreign reviewer's endpoint is declared with residency in `model-endpoints.yaml` and lakeswitch's disclosure decision is written (D-13). | yes — the recommendation was M0–M1 now, M2+ after stage 2 | §12 rebuilt around M0–M4; harness steps become prerequisites inside the M-steps |
| D-8 | Mechanical corrections to the corpus as one PR (dates, images, ADR prefixes, language line, CVE attribution, renames per D-1); content findings stay beside the sources in the review. | no | one PR |
| D-9 | Split the rule set: A, H, G, P, S, the harness rows of M, new family W here; M-3, M-4, M-5 and HG-1–4 to portfolio; the 21 red `test_regelwerk` cases resolved row by row. | no | `2ee` |
| D-10 | **The canonical one list is a platform-neutral gate file plus one `verify` command** (lakeswitch's pattern); `ci.yml` is derived from it — one "verify" step, or generated per gate with a drift check. Portfolio migrates its 36 steps into the gate file; the two-reader adapter is a transition only. Omnigent gets a policy in M1 that requires that one command before a push. Basis: Omnigent has no gate concept and reads no CI file; "developers and CI run the same command" is the mainstream pattern. | revised after the best-practice question | kit ships the gate-file schema and the runner; portfolio migration bead; `ci_gates.py` becomes the derivation, not the source |
| D-11 | `validate_change_artefacts.py` becomes a mechanism entry; the evidence pipeline stays an instance duty with the marker convention in the kit. | no | manifest |
| D-12 | `class` as a frontmatter field with four values, validated. | no | template, validator, one test |
| D-13 | Four measured criteria open stage 2 and thereby M2: ≥ 3 full seven-phase runs with metrics in coding-harness; lakeswitch's disclosure decision written; leak check green in every run; the foreign reviewer's endpoint declared with residency. Implement-phase cost is measured, not a switch. | no | WORKFLOW §6; `uqvm` successor |
| D-14 | Design phase 2b mandatory for Architectural, optional for Feature with one sentence in `spec.md` why not; absent for Bounded and Spike. | no | prompt `02b-design.md`, `design.md` template, validator rule |
| D-15 | **LikeC4 in the kit, with a kit-shipped specification that pins the four C4 element kinds** (system, container, component, code); `likec4 build` in CI; the gate "architecture change without ADR or model update in the same PR is a finding". Basis: LikeC4 has the tooling momentum (npm, VS Code, active releases), Structurizr DSL the strictness — the pinned specification keeps the strictness. | revised after the best-practice question | `templates/architecture/` with the specification; both instances share the vocabulary |
| D-16 | `model-routing.yaml` per instance, schema in the kit, every entry resolved against `model-endpoints.yaml` (drift is BLOCK); the Anthropic-only stage 1 ships as the example; the shell profiles read the file. No vendor name in `WORKFLOW.md`. | no | file, schema, test |
| D-17 | Apache-2.0, an onboarding page, and the denylist scan as a kit gate **from now on**, not at the switch; the template switch itself when Leerprobe ≥ 95 % in both instances, the first full run is measured, and Q13 has been passed once by someone who was not there. | no | licence, `docs/onboarding.md`, gate |

### 9.3 Follow-up decisions, same day

Four points that the seventeen decisions opened; decided in the same
interview.

| # | Question | Decided | Basis |
|---|---|---|---|
| O-1 | What the Definition of Done in `spec.md` carries | **Only what is specific to the change**: documents, models and ADRs that must move in the same PR; non-goals asserted untouched; which bead closes with which trailer; special runs. For the gates exactly one line — "`verify` green" — never a list. The validator checks presence and that one line. | a DoD that lists gates is a second gate list per spec (D-10) |
| O-2 | lakeswitch's ADR-0007 ("Omnigent from setup step 5, additive") against D-7 | **ADR-0007 stays** and gains one sentence: lakeswitch enters the Omnigent topology with harness step M2, not with setup step 5. M0 runs in a throwaway repository, M1 on coding-harness; lakeswitch joins when Feature changes run there and its git-native gates stand. | the reactive layer must work alone first (toolchain P6); both documents stay true |
| O-3 | What counts mechanically as an architecture change for the ADR/model gate | **The class is the duty, the path is the watchman.** `class: Architectural` without an ADR and a model diff in the PR is BLOCK; a module created, deleted or renamed under `src/` or `spec/` in a change of any other class is DRIFT with "check the class". | the one-way ratchet (§6.1) in gate form: stepping up is asked, staying silent is not allowed |
| O-4 | Schema of the platform-neutral gate file | **lakeswitch's `gates.yaml` schema as the basis**, field names aligned with pre-commit where it costs nothing (`entry` for the command, next to the existing function resolution), enforcement as a closed vocabulary `advisory` / `report` / `block` (levels 3–4 of the ladder), `floor` kept as lakeswitch's non-negotiable set, plus `mutation_test` and `schedule`/`reason` for reporting gates (RB-G3/G4). No third format; a pre-commit file can be generated from the same list. | mainstream declarative check lists (pre-commit, Taskfile, Actions steps) share this shape; policy-as-code (Conftest, Sentinel) supplies the enforcement vocabulary; only `asserts` and the mutation-test link are ours |

### 9.2 The proposals as put to the maintainer

Historical recommendations only. Where they differ, the interview outcomes
in §9.1 and §9.3 take precedence. The current sequence is in the linked plan.

| # | Goal | Recommendation | On "ok" |
|---|---|---|---|
| D-1 | One stage vocabulary | Stage 1–3 in the harness; corpus keeps its words with a note | WORKFLOW keeps "Stage"; research index gets the table |
| D-2 | Where the contract lives | `spec.md`; take the fields the ticket schema has and the spec contract lacks | a spec template is written (none exists today) with the prompt's contract plus *class, protected areas, failure mode, size*; non-goals already exist |
| D-3 | Bead granularity | One bead per change; task beads only when stage 2 has two workers claiming | WORKFLOW §2 sentence |
| D-4 | Export writer | One script, one moment (session end), identity gate; `export.auto` off | coding-harness config; gate into `ci.yml` with `bo0` |
| D-5 | Worktree placement | No `bd` writes outside the main checkout now; run the four-point verification plus the prefix case before choosing sibling vs in-repo | house rule + one bead for the verification |
| D-6 | `mypy` and instance gates | Instance gates stay in the instance | nothing in the kit |
| D-7 | Migrationsplan | Parked until the stage-2 signal | index note |
| D-8 | Corpus corrections | Mechanical ones as one PR; the rest stays beside the review | one PR |
| **D-9** | **Split the rule set** — harness rules (families A, H, G, P, S, the harness rows of M, new W) in coding-harness; domain rules (M-3 contract, M-4 recon, M-5 boundary before close, HG-1–4) in portfolio | (a) split — the 21 `test_regelwerk` failures are resolved row by row: enforcer rebuilt here, or row moved to portfolio, or level lowered with a reason; (b) keep one file — coding-harness carries rules it cannot enforce; (c) drop the domain rules — loses decided governance. **Recommend (a).** | `regelwerk.md` here loses the three domain rows; portfolio keeps them with their enforcers; `2ee` closes by this split |
| **D-10** | **The one-list property, not the file** — the kit asserts "one artefact enumerates the gates and runners derive from it", satisfied by `ci.yml` (portfolio) or `decisions/gates.yaml` (lakeswitch) | (a) property with an adapter in `ci_gates.py` — one code path, two readers; (b) force `ci.yml` everywhere — lakeswitch's floor mechanism breaks; (c) force `gates.yaml` everywhere — portfolio's 36-gate `ci.yml` is rewritten. **Recommend (a).** | `ci_gates.py` reads either; `test_ci.py` tests the property; Leerprobe green in lakeswitch becomes possible |
| **D-11** | **Which `bestand` scripts the kit needs after all** — the evidence pipeline (`collect_inventory.py`, `render_facts.py`) and the phase presence gate (`validate_change_artefacts.py`) both stayed in portfolio | (a) evidence pipeline stays an instance duty (kit ships the marker convention and the check), the presence validator becomes a mechanism entry — without it phases 2 and 3 have no gate anywhere the kit goes; (b) both kit entries — every instance inherits a snapshot it may not need; (c) both instance duty — the kit's phase gates are prose. **Recommend (a).** | manifest gains the validator; RB-P3's enforcer named per instance |
| **D-12** | **Task classes as a spec field** | (a) frontmatter `class:` with four values, presence checked by the validator (level 4 in one test); (b) prose only (level 1). **Recommend (a).** | template, validator, one test, WORKFLOW §2 table |
| **D-13** | **Stage-2 activation as numbers** | (a) written criteria: ≥ N full seven-phase runs with metrics in coding-harness, the disclosure decision for lakeswitch recorded, leak-check green on every run, a cost figure for the implement phase; (b) "when it feels right" (today). **Recommend (a), with N = 3.** | WORKFLOW §6 gets the numbers; `uqvm`'s successor bead measures them |
| **D-14** | **The design phase** | (a) `2b` mandatory for Architectural, optional with a stated reason for Feature, absent for Bounded and Spike; (b) mandatory for Feature too — ceremony for changes that need no design; (c) fold design into the plan — architecture stays invisible. **Recommend (a).** | prompt `02b-design.md`, `design.md` template, validator rule, WORKFLOW table |
| **D-15** | **Model as code: which tool** | (a) the kit ships a placeholder and the gate, the instance chooses Structurizr DSL (the C4 author's tool, wider adoption) or LikeC4 (the toolchain document's choice, richer local viewer); (b) the kit prescribes one — a tool choice in doctrine ages fastest. **Recommend (a).** | `templates/architecture/` with both skeletons; instance ADR picks |
| **D-16** | **Routing as a file** | (a) `model-routing.yaml` per instance, schema in the kit, validated against `model-endpoints.yaml`, the Anthropic-only stage 1 as the shipped example; (b) keep the table in `WORKFLOW.md` — vendor names in doctrine. **Recommend (a).** | file, schema, one test; WORKFLOW carries §6.6 only |
| **D-17** | **Public readiness** | (a) Apache-2.0, an onboarding page, a denylist scan as a gate (no customer, employer, vendor names in the harness), all before the template switch; (b) publish as is. **Recommend (a).** | licence file; `docs/onboarding.md`; gate in `ci.yml` |

## 10 · Quality scenarios

| # | Scenario | Measure |
|---|---|---|
| Q1 | A Feature change lands | Every acceptance criterion in `spec.md` has a test; the review table has no open BLOCKER; CI green; the bead closes by trailer on the integration branch |
| Q2 | A stranger reconstructs a change from three months ago | `plans/changes/archive/<date>-<name>/` plus the PR plus the handover answer *why*, *what*, *who decided* in under ten minutes, without a chat log (ADW Q2) |
| Q3 | A Bounded change | Human time ≤ 10 minutes: the open `[DECISION]` marks and the merge (ADW Q5) |
| Q4 | Someone breaks what a gate protects | The gate's mutation test goes red; a gate over an empty set is refused (RB-G4, RB-G7) |
| Q5 | The kit is copied into an empty repository | The Leerprobe reports a number; every red case has a reason in the closed set; the reason list only shrinks |
| Q6 | A model name appears that is not in `model-endpoints.yaml` | BLOCK, before any call (RB-A6) |
| Q7 | A session starts on a Feature change | Instruction files plus the change's three artefacts fit in well under a fifth of the window; measured once by hand at stage-2 activation (KB-10 has no enforcer, review §5.2) |
| Q8 | A session dies mid-implementation | The next session finds the change folder, the plan's marks and the bead's notes and continues without asking (ADW Q9) |
| Q9 | The routing file swaps every model for another vendor's | No doctrine file changes; the endpoint test either passes or names the undeclared endpoint; the Leerprobe number is unchanged |
| Q10 | An Architectural change lands | `design.md` exists with at least two alternatives; the ADR and the model-as-code delta are in the same PR; a product owner reads `design.md` and the ADR without a session and can answer the open questions |
| Q11 | A second person joins (T1) | No artefact changes shape; two valves close; the first PR with approver ≠ author passes the gate record check |
| Q12 | A fourth instance adopts the kit (I2) | `copier update` applies a kit tag with a diff; the compatibility matrix is generated; the instance's Leerprobe number is reported in its CI |
| Q13 | A stranger clones the template | README → onboarding → first Bounded change through phases 4, 5, 7 in one afternoon, with no question that the pages do not answer |

## 11 · Risks

| Risk | Mitigation | Residual |
|---|---|---|
| **Ceremony.** Seven phases feel like paperwork and get skipped | Task classes; "one sentence" rule; presence gates are one line | medium — the classes must actually be used |
| **Rubber-stamp by absence.** A machine presence gate lets a bad spec through because no human read it | 2a spec review by another model for Feature and above; Architectural requires a human-read ADR | medium |
| **Kit drift.** Instances diverge silently | Leerprobe in instance CI; divergence valve | low with the valve, high without |
| **Tracker seam.** Export conflicts, wrong prefixes | D-3, D-4, D-5; single writer | medium until verified |
| **Residency breach** through a convenient foreign endpoint | RB-A6 BLOCK; leak check; disclosure decision recorded before stage 2 | low |
| **Meta-harness capture.** Stage 3 starts holding state | Additive-only rule; disqualification criterion (§7) | low |
| **Homegrown machinery** nobody outside understands (ladder, valves, Leerprobe) | §8 names public analogues; §13 says where mainstream is better | medium |
| **One maintainer.** Every "someone" above is one person | Written decisions instead of remembered ones; ADR series in the harness | accepted |

## 12 · The path

**Decided 2026-09-16 (D-7): the Omnigent migration plan is the main path**,
M0–M4 in order, starting now. The harness work is not a separate sequence
any more; it is the set of prerequisites inside each M-step. No durations;
exit and abort criteria per step; the Migrationsplan's own criteria are kept
where it has them (M0–M2) and added where it has none (M3, M4). Two
event-driven steps sit beside the sequence: the template switch and the
first collaborator.

Non-negotiable across every step, because each is an enforced rule or a
decided constraint, not a preference: Omnigent version pinned with a
deliberate upgrade step; telemetry opt-out as the first configuration step;
every policy proven to fire on a known-bad case before it counts; the server
holds no state that repository and tracker do not also hold; OSS variant,
no employer account; no model call to an endpoint that `model-endpoints.yaml`
does not declare (RB-A6, level 4).

| Step | What | Harness prerequisites inside the step | Exit criteria | Abort / hold criteria |
|---|---|---|---|---|
| **M0 POC** | Omnigent server on a dedicated machine, pinned, telemetry off; the approval boundaries as server policies with a known-bad test each; a Beads task loop (claim → implement → commit → close) inside a sandboxed session in a throwaway repository; observability of a blocked session from a second device; the tmux fallback rehearsed once | the severance in portfolio (PR #162's per-gate decision) and coding-harness's own gate file and `verify` command (D-10, `bo0`); the 60 red tests resolved by class (27 `test_ci`, 21 `test_regelwerk` via D-9 / `2ee`, 12 others classified); `CLAUDE.md` fixed; D-4 export writer and D-5 worktree rule in place | all basis policies fire on their known-bad case (protocol in the repository); one full task loop without manual intervention beyond approvals; telemetry opt-out shown by egress observation; the same loop repeated once in the fallback topology | sandbox not functional on the target machine; `bd` unreliable inside Omnigent terminals; alpha instability interrupting the POC more than once a day → stay on the fallback, keep the harness prerequisites |
| **M1 Bounded class productive** | Bounded changes in exactly one repository (coding-harness itself) run in the Omnigent topology: human touch over the Omnigent channel, at least one approval from a phone; a policy that requires the one `verify` command before any push; a first hard spend cap per session | doctrine intake as this repository's first ADRs (§9.1) and the rewritten `WORKFLOW.md` (English, classes, 2b, requirement table, one vocabulary, session lifecycle); the spec template with DoD; `model-routing.yaml` with schema and test; rule set split; `design.md`, arc42, MADR, LikeC4 specification, ROADMAP templates; onboarding page drafted; denylist gate live (D-17) | ≥ 10 Bounded changes completed in the topology, ≥ 1 with mobile approval; ≤ 10 minutes human time per Bounded change including approvals; no sandbox escape or policy exception without a documented reason; every adopted rule has a test here or a valve with a date | human time per Bounded change repeatedly above 10 minutes after policy tuning; more than one unexplained policy non-fire → back to M0's state |
| **M2 Feature path with cross-vendor review** | Full artefact path P1–P7 with 2b for Feature and Architectural over the Omnigent channel; G4 as cross-vendor review (implementer and reviewer from different model lineages); the machine-rendered verification report; one controlled night run with stop conditions and a hard spend cap; first drift audit after two weeks | **entry condition (D-13, enforced):** ≥ 3 full seven-phase runs with metrics in coding-harness (the successor of `uqvm`), lakeswitch's disclosure decision written, leak check green on every run, the foreign reviewer's endpoint declared with residency; plus the stage-2 runner with stop conditions and the instance adoption in lakeswitch (plans roots, prompts, WORKFLOW copy, ROADMAP, spec fields) so that Feature changes exist to run | ≥ 3 Feature changes through all gates in the topology; ≥ 1 finding by the foreign reviewer that the same-lineage review missed (otherwise the configuration is wrong: same vendor? same context?); the night run's checklist green including the spend cap; drift audit without blocking findings; Q2 passed once by a stranger; zero leak-check violations | cross-vendor review not operable (licence, setup) → G4 falls back to an in-house reviewer with stricter context separation, recorded as debt; a leak-check violation → M2 off until the cause is a rule; escalation storms at G4 → thresholds and input curation tightened before continuing |
| **M3 Night mode and parallelism as routine** | Approved plans run overnight in cloud sandboxes with spend caps and mobile approvals; morning ritual: action log → G4 results → G5; parallel beads in parallel worktrees (D-5's in-repo placement, two-writer test green) with sequential merging; optional Polly pilot only if parallelisability is real and costed | task beads under an epic (D-3's second half) with `discovered-from` edges; the two-concurrent-writers verification green; Beads store mode decided (embedded vs server) from that measurement | ≥ 1 mergeable PR per week from night runs with zero unexplained policy exceptions; parallel execution without integration conflicts; morning G5 ritual ≤ 15 minutes per run | (added, the plan has none) two consecutive weeks without a mergeable night PR, or the morning ritual above 15 minutes twice → back to M2's day operation; Polly pilot: cost × benefit < 1 → manual dispatch |
| **M4 Hardening** | Mutation-score gate in CI; evidence-bound status (attestation files, hash-chained); traceability matrix FR × test as a generated CI artefact with gaps blocking; the tmux fallback kept as the rehearsed disaster-recovery path | requirement IDs in `spec.md` and test names (from M1 on, level 2) so the matrix has something to compute; the kit tagged and, at the fourth instance, Copier (I2) | (added) each hardening gate has its mutation test and a non-empty subject set; the fallback rehearsed once after M4 | (added) a hardening gate that cannot be made to go red → not merged; fallback rehearsal fails → M4 paused until it passes |
| **Template switch** (event) | coding-harness becomes a public template: Apache-2.0, onboarding page, denylist gate green, Copier scaffold prepared | — | Leerprobe ≥ 95 % in both instances **and** the M2 entry runs measured **and** Q13 passed once by someone who was not there | a customer, employer or vendor reference found by the gate → not public until removed |
| **T1 first collaborator** (event) | On lakeswitch: valves RB-M2 and RB-M6 close, CODEOWNERS review on, roster with two handles; the `bd`-vs-`br` decision (toolchain ADR-0005) written before this | — | first PR with approver ≠ author passes the gate-record check | — |

M0's harness prerequisites are in flight (portfolio PR #162, beads `bo0`,
`2ee`, `9qo`). M0 and M1's harness prerequisites can proceed in parallel;
M2's entry condition is the one hard sequence point, because it is the first
moment content leaves for a foreign endpoint.

## 13 · Challenge: is this best practice?

Two lists. The first is where this architecture departs from mainstream
practice, with the reason and a verdict. The second is where mainstream
practice is better than what any of the three repositories does today.

### 13.1 Deliberate departures

| Departure | Mainstream | Why we depart | Verdict |
|---|---|---|---|
| **Kit by copy** (S4) | A versioned dependency: shared GitHub workflows via `uses:`, a pre-commit hooks repository, a package — or, for templates that must be updatable in place, **Copier** | Instances legitimately diverge (lakeswitch has a floor and a YAML one list); a dependency forbids that; the Leerprobe counts it instead | Defensible at two instances. **At the fourth, Copier** (§7.2): it is the mainstream answer to exactly this problem — a template that can be updated with a diff — and a copy without a version silently becomes a fork. The tag in §6.5 is the first half of that switch. |
| **A design phase** (S8) | Spec Kit folds design into `/plan`; OpenSpec has an optional `design.md`; many teams skip it | Architecture decided inside a plan is invisible to a non-developer and to the next session | Mainstream-compatible (OpenSpec's `design.md` is the same object). The ceremony risk is handled by making it mandatory only for Architectural. |
| **Model as code in the kit** (D-15) | C4 with Structurizr DSL is the C4 author's tool; LikeC4 is newer | A picture that a generator can check beats a picture in a wiki | The original recommendation left the tool to each instance. The interview selected LikeC4 plus a shared element specification (D-15); that recorded choice governs. |
| **No pre-commit** | `.pre-commit-config.yaml` is near-universal in Python repositories | It would be a second gate list (WORKFLOW §8), and a second list is how local and CI come to disagree (WORKFLOW §3) | Sound, with one concession: a generated pre-commit file *derived from* the one list is not a second list. Offer it. |
| **Beads over GitHub Issues** | Issues are the default; agents read them via `gh` | `bd ready` answers "what now" after every context reset; dependency graph; claims | Young tool, export broke three times, an open prefix defect. **Keep, but the fallback must be a written decision** — the toolchain document weighs `bd` against `br` in its ADR-0005 and leaves it open; that decision is due before T1. |
| **Enforcement ladder and ramp valves** (S3, P5) | Policy engines with warn/enforce modes (Sentinel, OPA with `deny` vs `warn`), "error budgets" as the clock | We have no policy engine; the ladder is a table and the valve a script | Homegrown but not novel: Sentinel's three levels are the same idea. **Fine as long as the valve gate exists** — a ladder without the clock is the mainstream "TODO: enforce later". |
| **Machine presence gate instead of human spec approval** (S2) | Spec-driven development expects a human to approve the spec before code | One maintainer, minutes per day; the human reads only what is open | The risk is rubber-stamping by absence (§11). **Mitigated, not removed**: 2a for Feature and above, an ADR read for Architectural. For a team this becomes a real approval again. |
| **Seven phases, routed by requirement** | Spec Kit: four commands; OpenSpec: propose / apply / archive; "use the best model everywhere" | Finer cut isolates the expensive error (the plan) and routes cost; the doctrine names requirements, the instance names models (S7) | Ceremony risk is real; task classes are the fix and must land with the phases, not after. Routing needs the `/status` check because there are reports of subagent model fields being ignored (WORKFLOW §3). |
| **German prose** | English | History; decision to migrate is taken | Not a departure any more; a migration debt. Translate on touch, and only what is still true. |
| **Meta-harness early, as host** (S5, D-7) | Mainstream in 2026 is not settled; the corpus pushes Omnigent-style runtimes now, conservative practice keeps them evaluative | The maintainer decided for the early path; the conditions that make it defensible are the additive rule (git-native gates work alone), pinning, telemetry off, policy non-vacuity, no server-held state, and the residency gate before cross-vendor review | This is the one place where the recommendation was the conservative reading and the decision was not. Recorded as such; the abort criteria in §12 are what make it a bet rather than a leap. |

### 13.2 Where mainstream is better, and we should move

| Gap | Mainstream practice | What to do | Step |
|---|---|---|---|
| **The prompts themselves are untested** | Prompt regression suites (promptfoo, DeepEval), golden runs | The Leerprobe tests scripts, not prompt quality. Build a small golden set from archived changes; run it nightly, non-blocking, trend only (the toolchain document's LLM-eval rule) | 2–3 |
| **No delivery metrics** | DORA's four (lead time, deployment frequency, change failure rate, time to restore), per change | D-13 is the start: tokens, wall time, human minutes, gate outcomes per phase. Add change failure rate (a change reopened after merge). Generated, never typed | 2 |
| **Test-first ordering** | TDD's red first | Our "test *with* the change" plus the counterpart test is stronger on non-vacuity and weaker on ordering. Add "failing test first" as a SOLL in prompt 04 | 1 |
| **Secrets and dependency scanning** | gitleaks / detect-secrets, Dependabot or Renovate, SBOM | Portfolio has a secrets guard hook; lakeswitch pins exactly. Add secret scanning to both instance CIs; dependency updates as an instance duty | 3 |
| **Mutation testing tools** | mutmut / Stryker over the whole suite | Our one-counterpart-per-test rule is cheaper and enforced. Keep it; run `mutmut` once per release in lakeswitch as a calibration, not a gate | 3 |
| **Architecture as code** | C4 / LikeC4, arc42 | lakeswitch has `spec/_overview.md`; portfolio has ADR-026. D-15 selects a shared LikeC4 specification and templates; instances own their models, and O-3 defines the applicable ADR/model gate | — |
| **Branch protection for one person** | Solo repositories usually have none | Portfolio has a ruleset gate (RB-M6); lakeswitch has CODEOWNERS and a floor workflow. Keep; the admin-bypass is the documented debt (toolchain 11.2) | — |
| **Observability of agent runs** | Traces (OpenTelemetry), cost dashboards | Nothing today. The stage-2 runner writes a per-segment record (model, tokens, verdict) as a file; a dashboard is not needed before stage 3 | 4 |

### 13.3 The corpus's own claims, challenged

- **"Harness-neutral by convention" (ADW C2, ADR-07)** is asserted; the only
  measurement in the whole corpus is the Leerprobe, which the corpus does not
  mention. Neutrality is a number or it is a hope.
- **"Omnigent is the only system that ships several building blocks
  product-ready" (ADR-17)** is a market observation from one date, not a
  decision driver that survives a quarter. Decision drivers must be ours
  (residency, additivity, state in the repo), not the vendor's feature list.
- **The confidence lifecycle (ADR-13)** puts a number on something nobody
  measures. Dropped (review §5.6).
- **Living-spec drift audits (SM-25)** are right and premature: without
  requirement IDs there is nothing to audit. IDs first (step 1), audit later.
- **The toolchain document's target Lake Switch** is not the lakeswitch that
  exists. Its valuable parts (ROADMAP, ticket-schema fields, additive
  Omnigent, `/land-the-plane`) are taken; its layout is not.

## 14 · What this document does not do

- It is not an ADR; §9.1 records the interview outcomes, the harness's first
  ADRs are the place where they become records.
- It does not size the steps in time; the exit criteria are the clock.
- It does not verify the Omnigent claims or the CVE; both stay `unverified`.
- It does not create beads; one writer per tracker, and a parallel session
  could not be excluded when it was written.
