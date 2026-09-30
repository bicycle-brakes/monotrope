---
title: "Research — template-bundle"
status: draft
implementation_status: none
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-9qo
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, templates, spec, design-phase]
---

# template bundle — Research

Phase 1 after [`prompts/01-explore.md`](../../../prompts/01-explore.md). Facts
as read on 2026-09-30:

- this worktree at `f985698` (`origin/main`, the merge of PR #61);
- decision PR #60, branch `origin/feat/stage-2-codex-glm`, head `8622437`,
  unmerged and staying open by the maintainer's decision (handover
  `docs/journal/handover/2026-09-30-decision-by-merge-and-stage-2.md`,
  addendum "stage 2 built with Claude, PR #60 stays open");
- `portfolio-agentic-engineering` `master` at `20a279c`, read only;
- `lakeswitch-ai` `main` at `09c9d62`, read only.

Everything here was read in this session unless it says "not read". Sections
6 (size and the smallest version) and 7 (open points) were asked for by the
caller of this phase; they are candidates for the phase 1a interview, not
decisions.

**The bead** (coding-harness-9qo, re-scoped 2026-09-17, in progress) asks for
eight parts, numbered here P1–P8 for this file only:

- P1 a spec template: the contract of `prompts/02-spec.md` plus `class` in
  the header (four values), protected areas, failure mode, size, and a
  Definition of Done holding only change-specific items and exactly one line
  "verify green" for the gates; prompt 02 references it;
- P2 design phase 2b: `prompts/02b-design.md` and a `design.md` template
  (alternatives with consequences, interfaces, data model, ADR draft,
  model-as-code delta) — mandatory for architectural, optional with a
  one-sentence reason for feature, absent for bounded and spike;
- P3 the findings template and P4 the plan-marking template, moved from
  portfolio;
- P5 a `ROADMAP.md` template, P6 an arc42 skeleton, P7 a MADR decision record;
- P8 `templates/architecture/` with a LikeC4 specification pinning the four C4
  element kinds.

Not in it: the validator rules (bead coding-harness-jc3), the per-instance
routing file (coding-harness-qvl), the machine-rendered verification report.
Its acceptance criteria: every template exists (the 2b prompt under
`prompts/`); every template link in `docs/WORKFLOW.md` resolves; the kit
manifest lists the new files with their role; the Leerprobe number does not
drop.

**The decisions it rests on**, all carried as "Retain" in the table "Decision
continuity" of `docs/architecture/2026-09-17-omnigent-first-target.md` and
worded in `docs/architecture/target-architecture.md` §9.1 and §9.3: D-2 (the
spec is the contract, with class, protected areas, failure mode, size and a
Definition of Done), D-12 (class as a validated header field), D-14 (the
design phase by class), D-15 (LikeC4 in the kit with a pinned element
specification and `likec4 build` in CI), O-1 (what the Definition of Done
carries) and O-3 (an architectural change without an ADR and a model diff is
BLOCK).

## 1 · What exists today, and where

### 1.1 The eight parts

| Part | This repository (`f985698`) | Portfolio (`20a279c`) | Elsewhere |
|---|---|---|---|
| P1 spec template | **missing**; the contract is prose in `prompts/02-spec.md` ("Required sections" and the frontmatter paragraph) | missing | lakeswitch-ai has no template file either, but a declared header schema (`src/lakeswitch/declared/change_anchor.py`, `ChangeAnchorDocument`), see 1.3 |
| P2 design phase 2b | **missing**: no `prompts/02b-design.md`, no `design.md` template; neither "2b" nor "design.md" appears in `docs/WORKFLOW.md`, `AGENTS.md` or `prompts/` (searched) | missing | only in the target: `target-architecture.md` §6.1, phase table row 2b; lakeswitch-ai carries it as a spec section, see 1.3 |
| P3 findings template | **missing**; linked from `docs/WORKFLOW.md` §2 "The findings process" and `prompts/06-review.md` ("Your answer **is** the table from `templates/findings.md`") | `templates/findings.md`, 85 lines | PR #60 defines stage-2 columns, see 1.4 |
| P4 plan-marking template | **missing**; linked from `docs/WORKFLOW.md` §4 "Mechanics" and `prompts/03-plan.md` "Model markings (stage 2 only)" | `templates/plan-marking.md`, 46 lines | PR #60 deletes both references, see 1.4 |
| P5 `ROADMAP.md` template | **missing**; no `ROADMAP.md` in the tree | missing (`docs/archive/planning-2026-04/roadmap-consolidated.md` exists, not read) | none in lakeswitch-ai (searched); the idea: `docs/research/Lake-Switch-Architektur-arc42.md` §8.1.2 and `docs/research/2026-09-18-human-planning-and-harness-gaps.md`, "Proposed setup" item 2 ("proposed paths, not files created") |
| P6 arc42 skeleton | **missing** | missing | `target-architecture.md` is itself "arc42 sections, shortened" (its "Form" paragraph); lakeswitch-ai keeps its arc42 in `docs/architecture.html` (named in its `docs/index.md`; the HTML not read) |
| P7 MADR record | **missing as a template; the practice exists**: the seven ADRs under `docs/adr/` all have Context · Decision Drivers · Considered Options · Decision · Consequences, six of them Validation | `templates/obsidian/adr-template.md`, 54 lines, German, not MADR (Kontext · Entscheidung · Konsequenzen · Considered Alternatives · Referenzen) | ADR 0007 on PR #60 departs: no Decision Drivers, options after the decision |
| P8 LikeC4 specification | **missing**: no `templates/architecture/`, no model, no `.c4` file; `likec4` is not installed on this machine (`which likec4`: not found; `node` v26.9.0 is) | missing | lakeswitch-ai declines model as code (its D-58, see 1.5) |

"Moved from portfolio" applies to P3 and P4 only. Every other part is new
work; portfolio has no spec template, design prompt, ROADMAP, arc42, MADR or
LikeC4 file.

### 1.2 The rules around `templates/` and `prompts/`

- **No header in a template.** `provenance.yaml`, prefix `templates/`:
  `allowed: [human-written]`, `frontmatter: none`.
  `tests/test_feedback_channel.py::test_the_template_carries_no_real_frontmatter`
  holds it for `templates/handover.md`, which shows its schema in a ```yaml
  block instead.
- **Kit manifest** (`scripts/kit/manifest.yaml`): `templates/gate-record.yaml`
  and `templates/handover.md` are `mechanismus`; the catch-all `templates/` is
  `bestand` ("Entity-Contract, DABs, Run-Log: Domaene"). A new template is
  `bestand` until it gets its own rule. `prompts/` is `mechanismus` by prefix,
  so a new prompt needs no entry.
- **Export manifest** (`scripts/export/manifest.yaml`): `templates/` is
  `carry` — every new template travels to lakeswitch-ai.
- **A prompt's model is checked.**
  `tests/test_model_endpoints.py::prompt_modelle` reads the `**Model:**` line
  of every `prompts/*.md`; the model must be declared in
  `model-endpoints.yaml`.
- **Every `.md` under `plans/` carries the five required fields**
  (`scripts/plans_registry.py`, `REQUIRED` and `artefacts()`), so a
  `design.md` in a change folder needs the full header, and its template has
  to show one.
- **Dead links do not block.** `scripts/check_docs.py` (gate `docs-links`,
  `enforcement: report` in `decisions/gates.yaml`) reports 49 findings at
  `f985698`, among them "toter Link ../templates/findings.md" and "toter Link
  ../templates/plan-marking.md" in `docs/WORKFLOW.md` (measured).
- `templates/handover.md` is still German (house rule 1; its translation is
  bead coding-harness-yim, not this change).

### 1.3 The shape specs actually have

| Spec | Class | Lines | Criteria | Sections |
|---|---|---|---|---|
| `archive/2026-09-21-reproducible-bead-export` | bounded | 65 | 5 | Problem · Acceptance criteria · Non-goals · Open decisions; the body repeats "Class: Bounded." |
| `archive/2026-09-29-frontmatter-current` | feature | 296 | 7 | Problem · Terms · Acceptance criteria · Non-goals · Open decisions |
| `archive/2026-09-29-omnigent-deny-layers` | feature | 322 | 8 | Problem · What this change promises · The rule and the list · Acceptance criteria · Non-goals · Open decisions |
| `harness-decide-adr` | feature | 532 | 15 | Problem · Terms · Acceptance criteria · Non-goals · Open decisions |
| `stage-2-codex-glm` (PR #60 only) | architectural | 854 | 72 | Order of work · Problem · Terms · Acceptance criteria (in `###` groups) · Non-goals · Open decisions |

- **Common to all five:** Problem; acceptance criteria as a numbered list, each
  with "*Refuted by:*" (73 of them on #60's 72 criteria); Non-goals; Open
  decisions with `[DECISION]`, `[DETAIL]` and, on #60, `[GAP]` subsections.
  Four of five open with a sentence naming the change's aim, its bead, and
  `research.md` and `decisions.md` (not `frontmatter-current`).
- **None has** a Definition of Done, protected areas, a failure mode, a size or
  appetite, a `design.md`, or a sentence why there is none. The one
  architectural change (#60) ran without phase 2b and carries its decision as
  ADR 0007 without a model diff; O-3 would call that BLOCK, and nothing checks
  it.
- **Header on `main`:** the `plans_registry` fields, `class`; a feature adds
  `change` and `adr_question` with `proposed`, `reason` and optionally
  `answered_by` (`scripts/check_adr_answers.py`, `QUESTION_KEYS`).

**LakeSwitch's specs** (five feature specs under lakeswitch-ai
`plans/changes/`; headers read, `agent-instructions-ask/spec.md` in full):
the header carries `artifact: change-spec`, `class`, `class_history`,
`appetite` (a number; "the time the outcome is worth, in session hours",
lakeswitch-ai decision-interview D-24, Feature and Architectural only),
`adr_question` and an `intent` block (`scope` paths, `outcome`, `in_scope`,
`non_goals`, `acceptance` with `id`/`criterion`/`falsifier`, `constraints`).
Its schema is "still to be settled" by its D-28 (docstring of
`change_anchor.py`). All five have a `## Design` section; four say "No
`design.md`: <reason>", one carries a short design inline. No LakeSwitch
change folder holds a `design.md`. Coding Harness's gate reads a feature's
header and leaves every other key unexamined, so a header in LakeSwitch's
shape passes here (`plans/changes/harness-decide-adr/spec.md`, criterion 2).

**Where the D-2 fields come from:**
`docs/research/Lake-Switch-Architektur-arc42.md` §8.1.1 "Ticket-Schema" —
*Protected areas*: "auth/, billing/ # Änderung erfordert menschliche Freigabe"
(areas whose change needs a person's approval); *Failure mode*: "wie sieht
falscher Output aus?" (under test expectations); *Size*: "S # Kontextbudget
< 30k Token"; its *Definition of Done* lists gates (pre-commit, gitleaks,
pytest), which O-1 later replaced by the one line "verify green".

### 1.4 What PR #60 changes that this bundle touches

Read with `git diff origin/main...origin/feat/stage-2-codex-glm` and
`git show origin/feat/stage-2-codex-glm:<path>`:

1. **Acceptance criteria** (`prompts/02-spec.md`, "Required sections"):
   "Checkable sentences, one condition each; where a trigger, a state or a
   failure applies, the sentence begins with When, While or If." 31 of #60's
   own 72 criteria start that way.
2. **Class table** (`docs/WORKFLOW.md` §4, "Which change gets what"): a
   one-sentence change or `spike` gets no stage 2; `bounded` gets Fable 5.1
   in 2a "where one is held", GLM in 4b, Fable 5.1 in 6; `feature` and
   `architectural` get Codex in 2a, GLM in 4b, the same Codex agent in 6.
   "Nothing checks a change's class."
3. **Findings format.** `prompts/02a-spec-review.md` and `06-review.md` ask a
   foreign reviewer for six-cell rows `| ID | Severity | Dimension | Origin |
   Where | Finding |`. `scripts/stage2.py`: `ROW_COLUMNS` = ID, Severity,
   Dimension, Origin, Where, Finding, Reviewer, Status, Broke a test;
   `RELEASED_COLUMNS` add Phase 6; `VERDICT_LINE` ("Phase 6 verdict:
   <reviewer> <session>, <date>"); `SESSION_LINE` ("Reviewer session: codex
   <id>"); one "Stage-2 call" line per call; `findings_header` writes the
   header itself. `docs/WORKFLOW.md` §4, "Two columns for every stage-2
   change", defines Reviewer and Broke a test "because the findings template
   is not in this repository yet". `prompts/06-review.md` on #60 no longer
   names `templates/findings.md`; `docs/WORKFLOW.md` §2 on #60 still links it.
4. **Plan markings are retired.** #60 deletes "Model markings (stage 2 only)"
   from `prompts/03-plan.md` and the plan-marking paragraph from
   `docs/WORKFLOW.md` §4; its "not here" list drops `templates/plan-marking.md`
   (keeps `templates/findings.md`, adds `docs/governance/gate-catalog.md` and
   `requirements-ci.txt`).
5. **Phase tables.** #60 adds a row 4b to `AGENTS.md` ("The workflow in one
   screen") and to `docs/WORKFLOW.md` §2 — the two tables a 2b row would go
   into.
6. **How a decided D-number changes.** #60 marks D-13 "Amend" in the
   continuity table and adds `"D-13"` to `AMENDMENT_ADRS` in
   `scripts/check_decision_continuity.py`, backed by ADR 0007. The gate
   requires each listed D- or O-number to appear in the table and each mapped
   ADR to exist and name it.

What the practised findings tables look like on `main`: all four
`findings.md` files use `| ID | Severity | Dimension | Origin | Where |
Finding | Status |` (the oldest says Disposition instead of Status); the
newest (`harness-decide-adr`) adds the line "Reviewer session: …"; below the
table they carry sections such as "Checked without a finding", "Not checked"
and "For phase 7". Portfolio's template has `| ID | Severity |
Dimension | Origin | Status | Finding | Fix commit |` — a different order,
no Where, a Fix commit column nobody here uses.

### 1.5 Other work in flight that overlaps

- **Bead coding-harness-4me** (findings as checked data; open, queued after
  coding-harness-3ar): `templates/findings.md` as Markdown with a YAML
  frontmatter list (id, phase, severity, dimension, marker, where, status,
  reason) plus a schema and a gate; prompts 02-spec, 02a and 06 point to it.
  A third findings format beside portfolio's table and #60's rows.
- **Bead coding-harness-jc3** (validator: class, Definition of Done, design
  artefact): reads what P1 and P2 define.
- **Bead coding-harness-q24** (ADHD frame; in progress in worktree
  `.claude/worktrees/adhd-frame`, clean at `f985698` when read): an appetite
  stop and a plan card in `prompts/03`, `04`, `07` — the same "appetite" a
  size field would name.
- **Bead coding-harness-kw0** (stage-2 entry measurement), blocked by this
  bead: to be re-scoped or closed once ADR 0007 merges (handover of
  2026-09-30, "Open work and blockers").
- **`plans/changes/harness-decide-adr/decisions.md`, Q3** (2026-09-30): the
  four classes become a closed header set and only a feature owes an answer;
  "No further class duties." Its spec lists "class duties beyond the answer —
  the one-way ratchet, phases per class, `appetite` …" as a non-goal.
- **lakeswitch-ai `journal/2026-09-28-product-start-and-principles.md`**
  ("proposed 2026-09-28, not yet approved"): package 1c names this bead "in
  part"; a shared Definition of Done of at most six lines for every package,
  first line "verify green" after O-1; "Do not add: a validator or gate for
  ready or done, template files of their own …"; contradiction 2 of
  "Carrying the accepted interview decisions into Coding Harness": LakeSwitch
  **D-58 "No architecture model as code for now"** (ratified in
  `decisions/ratifications/RC-005-…md`, 2026-09-26, verdict accept) against
  D-15 and O-3, proposed resolution "a signed Coding Harness ADR lifts the
  model-as-code parts; the ADR stays required". D-58's reason: "no change so
  far has shown a defect that a model delta would have caught"; revisit after
  the third such defect.

## 2 · Would anything use each part now?

| Part | Who uses it today | Verdict |
|---|---|---|
| P1 spec template | every change (five specs above), prompt 02, the validator of jc3, lakeswitch-ai's adoption of "the spec-template fields" (`target-architecture.md` §5.2) | **yes** |
| P3 findings template | every change that runs 2a or 6 (four files on `main`, one on #60), the link in prompt 06, #60's runner | **yes** — the format is contested (1.4, 1.5) |
| P7 MADR record | every new ADR; seven follow the shape informally; a "yes" to the ADR question leads to one; ADR 0007 departs from it | **yes**, small |
| P2 design phase 2b | none of the five changes; LakeSwitch keeps the reason in a spec section and has never written a `design.md` | **not yet** — `target-architecture.md` §12 names it an M1 prerequisite, but M1 is "Bounded class productive", and D-14 makes 2b absent for bounded |
| P4 plan-marking | nobody after #60; on `main` only two dead links. Its markings name models (`[FLASH]`, `[GLM5.3]`, `[SONNET]`), which D-16 keeps out of doctrine and #60's routing no longer uses (GLM reviews in 4b; Sonnet 5.5 implements) | **no** |
| P5 ROADMAP | neither repository has a `ROADMAP.md`; planning lives in beads and handovers | **no** |
| P6 arc42 | both existing descriptions are written; the first consumer would be a third instance | **no** |
| P8 LikeC4 | no model in either repository, no CLI, and the one instance declines it (D-58) | **no** |

A template no tool reads and no change uses is the case `docs/WORKFLOW.md` §8
gives for not creating `.mcp.json`: "An empty configuration would be a claim
without content."

## 3 · Cheap and heavy

Sizes are estimates from comparable files (prompts 45–97 lines, portfolio
findings 85 and plan-marking 46, the handover template 124), not measured.

| Part | What it takes | Lines | Hours |
|---|---|---|---|
| P1 spec template | template, one line in prompt 02, kit rule, a test holding the example header against `plans_registry.REQUIRED`, `check_adr_answers.CLASSES` and `QUESTION_KEYS` | 90–120 + test 40 | 1.5–2 |
| P3 findings template | adapt portfolio's text to the practised columns and #60's stage-2 columns; kit rule | 70–90 | 0.5–1 |
| P4 retire plan-marking | delete the prompt 03 section (as #60 does) and the WORKFLOW references | −15 | 0.25 |
| P7 MADR record | template in the house's section order, header in a ```yaml block; kit rule | 45–60 | 0.5 |
| Doctrine links | WORKFLOW "not here" list, prompt 02 and 06 references | ~10 | 0.25 |
| P2 design phase 2b | prompt (model line must resolve), `design.md` template with full header, rows in the two phase tables, class text in WORKFLOW §2 | 110–150 | 1.5–2.5 |
| P5 ROADMAP template | Now/Next/Later page | 30–40 | 0.5 |
| P6 arc42 skeleton | twelve section headings with one line each | 70–100 | 0.5–1 |
| P8 LikeC4 file only | a `specification { … }` block nothing parses | 20–30 | 0.5, unverified |
| P8 as D-15 means it | Node toolchain in CI, a gate entry (`action:` or command), a sample model, generated `ci.yml`, a known-bad case | — | 2–4, **heavy**; new runtime dependency |

**Heavy:** P8 in its decided form (a toolchain and a gate for a model nobody
has), and P2 by its doctrine edits, which collide with #60's table rows.
**Cheap:** P1, P3, P4, P7. **Cheap but speculative:** P5, P6, P8 as a bare
file.

## 4 · What is unclear

- **MADR 4.0.0's own text was not read** in this session, only its summary in
  `docs/research/2026-09-30-decision-pull-requests.md` §2.2 (context,
  considered options, outcome, consequences, confirmation).
- **Whether a template moves the Leerprobe number.** The probe copies
  `mechanismus` files and runs pytest; a template without a test adds no case.
  A test holding a template adds one. Not measured.
- **Provenance of agent-written templates.** `provenance.yaml` allows only
  `human-written` under `templates/`, and a template carries no header to say
  otherwise. How the two existing templates were classified when they moved:
  not read.
- **Whether LakeSwitch's plan of 2026-09-28** (package 1c, the shared
  Definition of Done, "do not add a validator … template files of their own")
  was approved later: its addendum of 2026-09-29 does not say; nothing later
  read.
- Not read: lakeswitch-ai `docs/architecture.html`, portfolio
  `docs/archive/planning-2026-04/roadmap-consolidated.md`, the HTML of MADR.

## 5 · Which files a change would touch

**For the smallest version (section 6):**

- new `templates/spec.md`, `templates/findings.md`, `templates/adr.md` (names
  are a `[DETAIL]`);
- `prompts/02-spec.md` (one reference), `prompts/06-review.md` (the reference
  stays valid), `prompts/03-plan.md` (the markings section removed);
- `docs/WORKFLOW.md`: the "not here" list, §4 "Mechanics" (the plan-marking
  paragraph);
- `scripts/kit/manifest.yaml`: one `mechanismus` rule per template;
- a test for the spec template's example header (e.g. in a new
  `tests/test_templates.py`), listed in the kit manifest;
- `plans/INDEX.md` regenerated for the change's own artefacts.

**For the full bead in addition:** `prompts/02b-design.md`,
`templates/design.md`, `templates/roadmap.md`, `templates/arc42.md`,
`templates/architecture/` (LikeC4 specification), rows in `AGENTS.md` and
`docs/WORKFLOW.md` §2, and for D-15's gate `decisions/gates.yaml` and the
generated `.github/workflows/ci.yml`.

**Touched by PR #60 as well:** `prompts/02-spec.md`, `03-plan.md`,
`06-review.md`, `docs/WORKFLOW.md` ("not here" list, §2 table, §4),
`AGENTS.md` (phase table), `scripts/kit/manifest.yaml` (other lines). Where
both delete the same section (prompt 03), git merges cleanly; where #60
rewrites a section this change edits (WORKFLOW §4 and the "not here" list),
the later branch resolves a conflict by taking #60's text.

## 6 · Size and the smallest version

| Option | Contents | Hours |
|---|---|---|
| Full bead | P1–P8 as written, P8 with its CI gate | 9–13 |
| **Contract core** | P1, P3 (practised columns plus #60's), P4 retired, P7, links, kit rules, one test | **3.5–4.5**, one session, one PR |
| Core plus 2b | the above plus P2 | 5–7 |
| Spec template only | P1 and its link | 1.5–2; leaves two dead links, so the bead's second acceptance criterion fails |

**Smallest useful version: the contract core.** It is what Omnigent step M1
(bounded changes) uses, it closes both dead links, and it writes down two
forms that four and seven files already practise (findings, ADRs). The
not-now list would carry P2, P5, P6 and P8. Either way the bead's first
acceptance criterion ("every template listed above exists") changes; the
bead is re-scoped by the one tracker writer, not by this session.

**Baseline for "the Leerprobe number does not drop"** (measured 2026-09-30 at
`f985698`, `make verify` with `commit.gpgsign=false` as the caller
prescribes): pytest 515 passed, 15 skipped; Leerprobe **356 of 387 cases
(91 %)**; verify green. Run without that override, the probe locally counted
341 of 387 and blocked on 15 red cases including `tests/test_worktree_state.py`
(cause not investigated) — the condition of the measurement belongs next to
the number.

## 7 · Open points for the phase 1a interview

Sorted by the question protocol of `docs/WORKFLOW.md`, scope first. Each
`[DECISION]` carries a recommendation.

**Q1 `[DECISION]` — Which parts are built now, and which go to the not-now
list?**
Goal: the bundle gives this repository the forms its changes use, without
templates nobody uses.

- (a) **The full bead** (P1–P8). Consequence: 9–13 h over two sessions; four
  files nothing reads yet (ROADMAP, arc42, LikeC4, `design.md` for a class
  that has not needed one); plan-marking comes back although #60 retires it.
- (b) **The contract core**: spec template, findings template, MADR record;
  plan-marking retired, not moved. Consequence: 3.5–4.5 h, one PR; both dead
  links close; M1's bounded changes get their form. The design phase,
  ROADMAP, arc42 and LikeC4 go to the not-now list, each with the trigger
  that brings it back (the first feature or architectural change that asks
  for a design; the first instance that asks for a roadmap or an arc42).
- (c) **Core plus the design phase 2b.** Consequence: 5–7 h; 2b exists
  before a change needs it, and its rows go into the two phase tables #60
  also edits.

Recommendation: **(b)** — because it builds what current changes and M1
already use, and nothing that waits for a consumer. If "ok": this change
writes the three templates, retires plan-marking, repairs the links, and the
tracker writer re-scopes bead coding-harness-9qo and opens one bead for the
not-now parts. What is lost: the design phase stays a sentence in the target
architecture until a change asks for it.

**Q2 `[DECISION]` — Which findings table does the template describe?**
Goal: one form for review results that the people, the prompts and #60's
runner agree on.

- (a) **Portfolio's template as it is.** Consequence: it contradicts all four
  findings files here and #60's runner (different columns and order).
- (b) **The practised table** (`ID | Severity | Dimension | Origin | Where |
  Finding | Status`) plus, for a stage-2 change, #60's Reviewer, Broke a test
  and Phase 6 in `stage2.py`'s order, and the session and verdict lines.
  Consequence: nothing changes for anyone today; when #60 merges, its §4
  paragraph "because the findings template is not in this repository yet"
  should point to the template instead. Bead coding-harness-4me later adds
  its machine-readable list on top.
- (c) **Leave it to bead coding-harness-4me** (frontmatter list and gate).
  Consequence: the dead link stays until 4me lands; the bead's acceptance
  criterion "every template link resolves" fails for this change.

Recommendation: **(b)** — because it writes down what four files and the
runner already do, and 4me can extend a template more easily than invent one.
If "ok": `templates/findings.md` describes that table and names the stage-2
columns as defined by `docs/WORKFLOW.md` §4 once #60 is merged. What is lost:
the frontmatter list of 4me waits for 4me.

**Q3 `[DECISION]` — How does the spec template carry "protected areas" and
"failure mode" from D-2?**
Goal: the spec template holds everything D-2 decided without a section that
repeats another.

- (a) **Two sections of their own.** Consequence: every spec gains two
  sections; "failure mode" repeats what each criterion's "*Refuted by:*"
  already says in all five specs.
- (b) **Mapped onto what specs have:** the failure mode is each criterion's
  refutation (the template says so), and protected areas are a short list of
  paths the change must not touch, which the Definition of Done's line
  "non-goals asserted untouched" (O-1) points to. Consequence: nothing is
  written twice; D-2 is met by reading, which the template states in one
  sentence.
- (c) **Drop both.** Consequence: departs from a decided contract (D-2).

Recommendation: **(b)** — because every spec already carries a failure mode
per criterion, and a second one per spec would drift from them. If "ok": the
template has a "Protected areas" list and no "Failure mode" section, and says
where the failure mode lives. What is lost: one place where a reader sees
the failure mode of the whole change at a glance.

**Q4 `[DECISION]` — If LikeC4 goes to the not-now list, does D-15 stay as
decided?**
Goal: Coding Harness and LakeSwitch do not contradict each other on
architecture models longer than necessary.

- (a) **D-15 stays; LikeC4 is deferred.** Consequence: no ADR now; the target
  architecture keeps promising a model gate that nothing builds; LakeSwitch's
  D-58 stays in open contradiction with it.
- (b) **Amend D-15 and O-3 by an ADR** to match D-58: the ADR stays required
  for an architectural change, the model diff does not. Consequence: a
  decision PR (`decide(adr): …`), the continuity row "Amend", an
  `AMENDMENT_ADRS` entry — the path #60 took for D-13.
- (c) **Build LikeC4 as D-15 says.** Consequence: 2–4 h and a Node dependency
  in CI for a model neither repository has.

Recommendation: **(a) now, (b) as its own decision PR when the maintainer
wants the two repositories to agree** — because deferring is reversible and
costs nothing, and an amendment is a decision that deserves its own PR, not a
side effect of a template change. If "ok": LikeC4 is on the not-now list with
D-58's revisit trigger. What is lost: until (b), the target document and
LakeSwitch disagree in writing.

**Q5 `[DECISION]` — only if Q1 is (a) or (c): is the design phase a duty by
class now?**
D-14 makes 2b mandatory for architectural and a reason-sentence duty for
feature. On 2026-09-30 the maintainer said "No further class duties" while
deciding the ADR question (`harness-decide-adr/decisions.md`, Q3). Two
readings: that sentence was limited to the ADR change, or it is a stance.
Options: (a) D-14 as decided, stated in doctrine and unenforced until bead
jc3; (b) 2b as a tool any class may use, no duty. Recommendation: **(a)**,
because D-14 is "Retain" in the continuity table and Q3's spec lists class
duties as a non-goal of that change, not as rejected.

### `[GAP]` — answerable by reading or measuring, not by asking

1. MADR 4.0.0's own template text — read before writing P7.
2. The Leerprobe after the change — run `make verify` and compare with 356 of
   387 (section 6, same git override).
3. How `templates/handover.md` and `gate-record.yaml` were classified against
   `provenance.yaml` (`human-written` only) when they moved.
4. Whether LakeSwitch's plan of 2026-09-28 was approved later (its shared
   Definition of Done and "do not add" list), read in lakeswitch-ai's later
   journal entries.

### `[DETAIL]` — the agent decides, with the reason in the artefact

1. **English** templates (house rule 1); the German handover template stays
   for bead coding-harness-yim.
2. **The header in a ```yaml block**, never as real frontmatter — the
   `templates/` rule in `provenance.yaml` and the handover template's
   precedent.
3. **Section names follow prompt 02** (Problem, Acceptance criteria,
   Non-goals, Open decisions) and the goal is the opening sentence, as in four
   of five specs — not a new "Goal" heading. Terms stays optional.
4. **Size is `appetite:` in session hours**, LakeSwitch's name and unit
   (its D-24), the word bead q24 and #60's decisions use; it fills D-2's
   "size". The header does not adopt LakeSwitch's `intent` block: its schema
   is unsettled there (D-28), and the gate here leaves it unexamined.
5. **The example criterion reads "When …, … *Refuted by:* …"**, compatible
   with `main` and with #60's one-condition rule; the rule itself stays in
   prompt 02 and is not restated.
6. **The Definition of Done holds O-1's list exactly**: documents, models and
   ADRs moved in the same PR; non-goals asserted untouched; the closing
   trailer (`Closes-Bead: <id>`, `prompts/07-commit.md`); special runs; and
   the one line "verify green".
7. **One `mechanismus` rule per template** in the kit manifest; the export
   manifest already carries `templates/`.
8. **The spec template is held by a test** against the readers that already
   exist (`plans_registry.REQUIRED`, `check_adr_answers.CLASSES` and
   `QUESTION_KEYS`), so it cannot drift from the gates — the handover
   template's pattern.
9. **The class of this change** is proposed in its spec; it changes what a
   spec must carry, so likely `feature`, with an ADR proposal "no": it writes
   down decisions already taken (D-2, O-1).
