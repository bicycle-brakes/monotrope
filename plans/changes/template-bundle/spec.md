---
title: "Spec — template-bundle"
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
tags: [spec, templates, findings, adr, definition-of-done]
class: bounded
appetite: 4
---

# Spec — template-bundle

After this change a spec, a findings table and an architecture decision
record each have one written form under `templates/`, prompt 02 points to the
spec form, and no workflow text points to a template that does not exist
(bead coding-harness-9qo, cut to its contract core). Research: `research.md`
— its section 8, "Corrections after verification, and gaps closed in phase
2", holds where it disagrees with the text above it. Decisions:
`decisions.md`.

> **Provisional — awaiting the maintainer's confirmation at the merge.** The
> answers in `decisions.md` were chosen on 2026-09-30 by the orchestrating
> session from the recommendations of `research.md`, because the maintainer
> is away until 2026-10-04 and the phase 1a interview could not be held. This
> spec honours them exactly: (1) the contract core only, the design phase,
> ROADMAP, arc42 and LikeC4 on the not-now list; (2) the practised findings
> table, with the stage-2 columns named as coming with pull request #60;
> (3) the failure mode carried by each criterion's refutation, and a
> protected-areas list; (4) decision D-15 (LikeC4) stays as decided. This
> spec adds one provisional answer of its own: the class (Open decisions).
> Nothing here takes effect before the maintainer merges the pull request
> (`AGENTS.md`, house rule 8); an answer the maintainer changes is reworked
> before the merge.

## Problem

What does not work today (`research.md` sections 1–2 and 8; read on
2026-09-30 at `f985698` and `eee26ae`):

- **The spec contract is prose only, and part of it is missing.** The form of
  a spec lives in the "Required sections" of `prompts/02-spec.md`. The five
  specs research compared (four on `main`, one on pull request #60) share
  Problem, acceptance criteria each with "*Refuted by:*", Non-goals and Open
  decisions — and none carries a Definition of Done, protected areas, a
  failure mode or a size, although decisions D-2 and O-1 of the 2026-09-16
  interview asked for exactly these and the current target document retains
  them.
- **Two workflow links point at nothing.** `docs/WORKFLOW.md` links
  `templates/findings.md` (§2, "The findings process") and
  `templates/plan-marking.md` (§4); `scripts/check_docs.py` reports both as
  dead. Prompt 06 tells the reviewer to write "the table from
  `templates/findings.md` — columns exactly as they stand there", and prompt
  03 sends the planner to `templates/plan-marking.md`.
- **The findings form exists only as practice.** All four findings files
  here use `ID | Severity | Dimension | Origin | Where | Finding | Status`
  (the oldest says Disposition). Portfolio's template has another order, no
  Where and a Fix commit column nobody here uses. Pull request #60 (stage 2,
  open, not merged) adds three columns and defines two of them in
  `docs/WORKFLOW.md` "because the findings template is not in this
  repository yet".
- **The decision-record form exists only as practice.** The seven ADRs on
  `main` share Context · Decision Drivers · Considered Options · Decision ·
  Consequences, six add Validation; no template says so, portfolio's is
  German and not MADR, and ADR 0007 on pull request #60 already departs from
  the shape.
- **Plan markings describe a mechanism that is not here.** They route plan
  steps to named models through `scripts/run_change.sh`, which this tree
  does not have; decision D-16 keeps model names out of doctrine, and pull
  request #60 retires the markings.

## Terms

- **Template** — a file under `templates/` that is copied to start an
  artefact. It carries no header of its own (`provenance.yaml`, prefix
  `templates/`: `frontmatter: none`) and shows the header its copy needs in a
  fenced `yaml` block, as `templates/handover.md` does.
- **The spec template, the findings template, the decision-record
  template** — `templates/spec.md`, `templates/findings.md`,
  `templates/adr.md`.
- **Example header** — the fenced `yaml` block in a template that shows the
  header of its copy.
- **Filled in** — an example header whose placeholders are replaced by
  values as the template's own instructions say.
- **Practised table** — the seven columns `ID | Severity | Dimension |
  Origin | Where | Finding | Status`, in this order.
- **Stage-2 columns and lines** — `Reviewer`, `Broke a test`, `Phase 6`, and
  the lines `Reviewer session: codex <id>`, `Phase 6 verdict: <reviewer>
  <session>, <date>` and `Stage-2 call, …`, as pull request #60 defines them
  (its runner `scripts/stage2.py` at `bd39160`: `ROW_COLUMNS`,
  `RELEASED_COLUMNS`, `SESSION_LINE`, `VERDICT_LINE`).
- **MADR 4.0.0** — the Markdown Architectural Decision Records template at
  tag `4.0.0` of `github.com/adr/madr` (`research.md` section 8, gap 1).
- **Workflow texts** — `AGENTS.md`, `docs/WORKFLOW.md` and every
  `prompts/*.md`.

## Acceptance criteria

Each criterion states one condition; its *Refuted by* line is what a wrong
result looks like. Where a test is named, the plan names the file.

### The spec template

1. **The spec template has the sections of a spec, in order.** The
   second-level headings of `templates/spec.md` are, in this order: Problem,
   Terms (marked optional), Acceptance criteria, Non-goals, Protected areas,
   Definition of Done, Open decisions.
   *Refuted by:* a test that reads the template's second-level headings and
   finds one missing, renamed, added or out of this order.

2. **The template opens with the goal.** The first paragraph under the
   template's title asks for the change's goal in one sentence — what holds
   after the change — followed by its bead and its inputs `research.md` and
   `decisions.md`.
   *Refuted by:* a first body paragraph that does not ask for the goal (a
   test on the word "goal" in it).

3. **When the example header is filled in and placed as a change's spec, the
   gates accept it.** The example header is a feature's, the form with the
   most keys. Filled in and written as `plans/changes/<change>/spec.md` in a
   temporary tree, it has every field `plans_registry.REQUIRED` names, none
   of them empty; its `status` and `implementation_status` are in
   `plans_registry.STATUS` and `plans_registry.IMPLEMENTATION`; and
   `scripts/check_adr_answers.py` raises no finding about the header — only
   the one about the answer file the temporary tree lacks.
   *Refuted by:* a test that takes those names from the two modules at run
   time, not from a copy, and reports a missing or empty field, a refused
   value or a header finding; the same test staying green when a field the
   template lacks is added to `REQUIRED`.

4. **The template offers exactly the four classes.** The template's `class:`
   line names each entry of `check_adr_answers.CLASSES` and no other value.
   *Refuted by:* a test that finds a value in that line outside `CLASSES`, or
   an entry of `CLASSES` missing from it.

5. **The size is the appetite.** The example header carries `appetite:`, a
   positive number: the session hours the outcome is worth — a budget, not
   an estimate — for a change of any class.
   *Refuted by:* an example header without `appetite`, or with a value YAML
   does not read as a number greater than zero (test).

6. **The failure mode is carried only by the refutations.** Decision D-2's
   failure mode is each criterion's *Refuted by:* line — what a wrong result
   looks like — and the template says so in one sentence of its Acceptance
   criteria section instead of giving the failure mode a section.
   *Refuted by:* a heading in the template containing "failure mode", or the
   sentence missing (test).

7. **When the template shows a criterion, it shows one with its
   refutation.** The template's example criterion is one sentence beginning
   with "When", "While" or "If", followed by a line beginning "*Refuted
   by:*".
   *Refuted by:* an example criterion beginning with another word, or
   without the refutation line (test).

8. **The template asks of a criterion no more than `main`'s prompt 02 does.**
   It requires a checkable sentence and its refutation, points to
   `prompts/02-spec.md` for the rule, and offers one condition per criterion
   with When / While / If as a recommendation, saying that it becomes the
   rule with pull request #60.
   *Refuted by:* a sentence in the template that makes the When / While / If
   form mandatory (review).

9. **Protected areas are what the change must not touch.** The Protected
   areas section asks for the paths or areas the change must not touch, each
   with its reason, or the single line "None beyond the non-goals."
   *Refuted by:* the section's instruction without "must not touch" or
   without that single line (test).

10. **The Definition of Done names the gates only in one line.** The
    Definition of Done section of the template has exactly one line about
    the gates, reading "`verify` green", and no other of its lines names a
    gate of `decisions/gates.yaml`.
    *Refuted by:* a test that reads the gate ids from `decisions/gates.yaml`
    at run time and finds one in the section outside that line, or finds the
    line missing or twice; the test staying green on a planted line
    "`pytest` green".

11. **Everything else in the Definition of Done is specific to the change.**
    Besides that line, the section asks for what decision O-1 lists and
    nothing that holds for every change: the documents, models and ADRs that
    move in the same pull request; that the protected areas stay untouched
    and the non-goals unbuilt; the bead the pull request closes, with its
    `Closes-Bead: <id>` trailer (`prompts/07-commit.md`); and special runs.
    *Refuted by:* one of the four missing (test on their key words); an item
    that holds for every change, such as "tests pass" or "English commit
    message" (review).

12. **Prompt 02 names the template.** `prompts/02-spec.md` names
    `templates/spec.md` as the form `spec.md` is written in.
    *Refuted by:* the prompt without that path (test).

### The findings template

13. **The findings table has the practised columns.** The first table of
    `templates/findings.md` has the header `ID | Severity | Dimension |
    Origin | Where | Finding | Status`, in this order.
    *Refuted by:* a test comparing that header row cell by cell.

14. **The template holds the vocabulary the doctrine hands it.**
    `docs/WORKFLOW.md` §2 says the form and vocabulary of a review result
    "live in `templates/findings.md` and are not kept twice here". The
    template defines the severities `BLOCKER`, `MAJOR`, `MINOR`; the
    dimensions `SPEC` and `MAINT`; the origins `base` and `fix-r<N>`, two
    consecutive rounds of `fix-r` origin being an escalation rather than a
    third round; the markers `[AMBIGUITY]` and `[DIVERGENT]`, a
    `[DIVERGENT]` counting as a `BLOCKER`; and that a finding rejected before
    returns only with new evidence.
    *Refuted by:* a test that finds one of these terms missing from the
    template.

15. **The status values include the two prompt 02 prescribes.** Among the
    Status values the template lists are `in spec` and `rejected —
    <reason>`, which `prompts/02-spec.md` ("After the spec review") requires
    for each spec-review row.
    *Refuted by:* either value missing (test).

16. **Under the table stand the practised lines.** Below the table the
    template shows the line `Reviewer session: <id>`
    (`prompts/02a-spec-review.md`) and the sections "Checked without a
    finding" and "Not checked" (prompt 06: "name what you checked").
    *Refuted by:* one of the three missing (test).

17. **The stage-2 columns are named as coming with pull request #60.** The
    template names what a change that runs stage 2 adds once pull request
    #60 (ADR 0007) is merged: the header `ID | Severity | Dimension | Origin
    | Where | Finding | Reviewer | Status | Broke a test`, with `Phase 6`
    appended for the released loop rows, and the lines `Reviewer session:
    codex <id>`, `Phase 6 verdict: <reviewer> <session>, <date>` and one
    `Stage-2 call, …` line per call. It says, with its date, that
    `docs/WORKFLOW.md` §4 defines them once that pull request is merged and
    that until then no change carries them.
    *Refuted by:* a column name or order, or a line form, that differs from
    `ROW_COLUMNS`, `RELEASED_COLUMNS`, `SESSION_LINE` or `VERDICT_LINE` in
    `scripts/stage2.py` at pull request #60's head `bd39160` (review — the
    runner is not in this tree); a sentence saying stage 2 is active or that
    the columns are required today.

18. **When the findings template's example header is filled in, it has what
    a file under `plans/` needs.** It has every field `plans_registry.REQUIRED`
    names, none of them empty, with `status` and `implementation_status` in
    the accepted sets.
    *Refuted by:* the test of criterion 3 run over this header reporting a
    missing, empty or refused field.

### The decision-record template

19. **The record has the house's six sections, options before the
    decision.** The second-level headings of `templates/adr.md` are, in this
    order: Context, Decision Drivers, Considered Options, Decision,
    Consequences, Validation — the six sections six of the seven ADRs under
    `docs/adr/` carry.
    *Refuted by:* a test that reads the headings and finds one missing,
    renamed, added or out of this order.

20. **The template names its source and maps the names that differ.** It
    names MADR 4.0.0 with its address, and for each house section whose name
    differs it names the MADR 4.0.0 element it stands for: Context — Context
    and Problem Statement; Decision — Decision Outcome; Validation —
    Confirmation.
    *Refuted by:* "MADR 4.0.0" or one of the three pairs missing (test).

21. **The record takes effect by the merge.** The template's status lines
    say, as ADR 0008 does, that the decision takes effect when the maintainer
    merges the pull request carrying it — while that pull request is open the
    decision is proposed, and closed unmerged it is rejected.
    *Refuted by:* the merge sentence missing (test); a signature, a signed
    commit or a filled approval field named as the acceptance (review).

22. **The template says that its pull request is a decision pull request.**
    It says that a pull request adding a file under `docs/adr/` is a decision
    pull request: title `decide(<scope>): …`, label `decision`, body from
    `.github/PULL_REQUEST_TEMPLATE/decision.md`.
    *Refuted by:* the title form, the label or the template path missing
    (test).

23. **When a record amends a decided D- or O-number, the template says what
    moves with it.** It names the row "Amend" in the table "Decision
    continuity" of `docs/architecture/2026-09-17-omnigent-first-target.md`
    and the entry in `AMENDMENT_ADRS` of
    `scripts/check_decision_continuity.py`, which the gate
    `decision-continuity` holds.
    *Refuted by:* either name missing from the template (test).

24. **When the decision-record template's example header is filled in, it
    has the fields the ADRs carry.** It has `title`, `category: adr`,
    `status`, `created`, `last_reviewed`, `updated`, `owner`,
    `provenance: human-decided`, `produced_by`, `review` and `tags`, as ADR
    0008 has them.
    *Refuted by:* one of them missing, or `provenance` or `category` with
    another value (test).

### Plan markings retired, links whole

25. **No workflow text names a template that does not exist.** Every path
    `templates/<file>` named in the workflow texts names an existing file.
    *Refuted by:* a test that reads the workflow texts and finds such a path
    without its file; the same test staying green on a planted mention of
    `templates/missing.md`.

26. **When `scripts/check_docs.py` runs, it reports no dead link into
    `templates/`.** At `f985698` it reports two, `../templates/findings.md`
    and `../templates/plan-marking.md`.
    *Refuted by:* its output naming a link into `templates/` as dead.

27. **No workflow text asks for a plan marking.** None of the workflow texts
    contains `[FLASH]`, `[GLM5.3]`, `[SONNET]`, `plan-marking` or `Model
    markings`, and `templates/plan-marking.md` does not exist: the markings
    are retired, not moved. The section "Model markings (stage 2 only)" of
    `prompts/03-plan.md` goes exactly as pull request #60 removes it.
    *Refuted by:* one of the five strings in a workflow text, or the file
    present (test).

28. **The note "Not all of it is here yet" no longer names the two
    templates.** The opening note of `docs/WORKFLOW.md` names neither
    `templates/findings.md` nor `templates/plan-marking.md`.
    *Refuted by:* either path in that note (test or search).

### The kit and the tree

29. **The three templates and their test travel with the kit.**
    `scripts/kit/manifest.yaml` has a `mechanismus` rule with a reason for
    each of the three templates and for the test that holds them.
    *Refuted by:* `python3 scripts/kit/probe.py --list` without one of them;
    `tests/test_kit.py` red.

30. **When `make verify` runs on the pull request's last commit, it is
    green**, run with `commit.gpgsign=false` as this repository's
    measurements are.
    *Refuted by:* `VERIFY RED` on that commit.

31. **The Leerprobe does not lose a case.** On the pull request's last commit
    the Leerprobe carries at least 356 cases (the baseline at `eee26ae`,
    2026-09-30: 356 of 387), and the new test is among the cases that carry.
    *Refuted by:* a count below 356, or a case of the new test among the red
    ones, in the probe's report.

32. **The new texts are English.** The three templates and every line this
    change writes into the workflow texts are English (`AGENTS.md`, house
    rule 1).
    *Refuted by:* a German sentence among them (review).

## Non-goals

### Not now, and what brings each back

- **The design phase 2b** — `prompts/02b-design.md`, a `design.md` template,
  and its rows in the phase tables. Decision D-14 stays as decided. Back
  when the first `architectural` change after this one reaches phase 2, or a
  `feature` spec says it needs a design it cannot hold in a section.
- **A `ROADMAP.md` template.** Planning lives in beads and handovers; neither
  repository has a roadmap file. Back when an instance asks for one.
- **An arc42 skeleton.** Both existing architecture descriptions are written
  already. Back when a third instance starts without one.
- **The LikeC4 specification and its model gate.** Decision D-15 stays as
  decided, unbuilt (`decisions.md`, answer 4); LakeSwitch declines model as
  code for now (its D-58). Back when an instance keeps an architecture model,
  when LakeSwitch's D-58 revisit trigger fires (a third defect a model delta
  would have caught), or when the maintainer takes up amending D-15 and O-3
  in a decision pull request of its own.
- The tracker writer — not this change — cuts bead coding-harness-9qo to
  this contract core and opens one bead for these four parts
  (`decisions.md`, answer 1).

### Not in this change

- **A check that a spec follows the template** — presence of class,
  Definition of Done, protected areas or appetite. The template is a form,
  not a gate; the validator rules are bead coding-harness-jc3.
- **Findings as checked data** — a machine-readable list and its gate (bead
  coding-harness-4me), which may extend this template later.
- **Reshaping existing artefacts** to the templates: no spec, findings file
  or ADR, active or archived, is changed; ADR 0007 on pull request #60 keeps
  its order.
- **Building anything of stage 2** or editing pull request #60's branch; the
  stage-2 columns are named, not implemented.
- **Amending D-15 or O-3** — its own decision pull request with an ADR
  (`decisions.md`, answer 4).
- **Updating the target and gap documents** under `docs/architecture/`.
  Their rows from 2026-09-17 still name `plan-marking.md` as moving here;
  they record the design of that date, and the re-scoped bead and this spec
  record the change of plan.
- **Class duties** — the one-way ratchet, phases per class, a `design.md`
  duty (as in `plans/changes/harness-decide-adr/spec.md`, Non-goals). The
  appetite applies to every class and is no class duty.
- **LakeSwitch's anchor shape**: its `intent` block, `class_history` and
  `artifact` keys (its schema is still open there, its D-28).
- **The appetite stop, the plan card and the acceptance card** in prompts
  03, 04 and 07 and in the pull request templates — the parallel change
  `adhd-frame` (bead coding-harness-q24). This change uses the same word,
  appetite.
- **Translating `templates/handover.md`** (bead coding-harness-yim).
- **Anything in lakeswitch-ai.** It receives the templates through the
  export manifest's `carry` of `templates/` when it next takes them.

## Protected areas

This change must not touch:

- **The "Required sections" list of `prompts/02-spec.md`.** Pull request #60
  rewrites its acceptance-criteria bullet, and a test on that branch holds
  the new text; the reference to the template goes elsewhere in the prompt.
- **`prompts/06-review.md`.** Pull request #60 rewrites the paragraph that
  names the findings template; on this branch the name becomes true without
  an edit.
- **`docs/WORKFLOW.md` beyond the opening note and the plan-marking
  paragraph of §4**, in particular the phase table of §2 and the routing of
  §3, which pull request #60 edits; and **`AGENTS.md`**, whose phase table
  pull request #60 edits. One exception, only if pull request #60 merges
  first: the sentence of its §4 that the `[DETAIL]` "Overlaps with pull
  request #60" names.
- **Every path `provenance.yaml` reserves for `human-decided`** — `docs/adr/`,
  `decisions/answers/`, the rule set — so that this pull request is no
  decision pull request.
- **`docs/architecture/`** — the target, its decision-continuity table, the
  gap analysis and the implementation plan.
- **`templates/handover.md` and `templates/gate-record.yaml`.**
- **Every other change folder** under `plans/changes/`, active or archived.
- **`.github/`, `prompts/04-implement.md` and `prompts/07-commit.md`** — the
  parallel change `adhd-frame` edits them; `prompts/03-plan.md` loses only
  its markings section.
- **The gate scripts, `decisions/gates.yaml` and
  `scripts/export/manifest.yaml`** — no gate is added or changed, and the
  export manifest already carries `templates/`.

## Definition of Done

- `verify` green.
- Moved in the same pull request: the three templates and their test;
  `prompts/02-spec.md` (the reference); `prompts/03-plan.md` (the markings
  section removed); `docs/WORKFLOW.md` (the opening note, the plan-marking
  paragraph of §4); `scripts/kit/manifest.yaml`; `plans/INDEX.md`
  regenerated. No ADR and no model moves.
- The protected areas above untouched and nothing of the not-now list built,
  shown by the pull request's file list.
- Bead: the last commit carries `Closes-Bead: coding-harness-9qo` only once
  the tracker writer has cut the bead to this contract core and opened the
  bead for the not-now parts; until then no closing trailer, and the pull
  request body says so.
- Special runs, with their commit in the pull request body:
  `python3 scripts/check_docs.py` without a dead link into `templates/`, and
  the Leerprobe's count against 356 of 387.
- The pull request body lists every provisional answer — `decisions.md`
  answers 1–4 and this spec's class — for the maintainer's confirmation,
  and names the overlaps with pull request #60 and how the later merge
  resolves each (the `[DETAIL]` "Overlaps with pull request #60" below).

## Open decisions

None open. One provisional answer awaits the maintainer.

### [DECISION] — The class of this change (provisional answer: `bounded`)

The class decides whether the maintainer is asked the ADR question for this
change. Research recommended `feature` as "likely" (`research.md` section 7,
`[DETAIL]` 9); on reading the class definitions against this scope, two
readings are plausible, so it is asked here, answered provisionally, and
flagged for the merge.

```text
Goal in one sentence:  Say what kind of change this is, which decides
                       whether the maintainer answers the ADR question
                       for it before it merges.
Options:
  1. bounded — "changes an existing, readable flow without deciding
     anything new": the flows exist (prompt 02's contract, four findings
     files, seven ADRs), the new spec sections were decided on 2026-09-16
     (D-2, O-1), and nothing new is enforced. Consequence: no ADR question;
     `make verify` stays green, so phases 3 to 7 can run while the
     maintainer is away; the maintainer can still reclassify at the merge.
  2. feature — "a self-contained deliverable that changes what the system
     must do": three new templates, and every later spec carries three more
     sections. Consequence: the header adds `change: template-bundle` and
     `adr_question`; the gate `adr-answers` is red on this branch until the
     maintainer answers, so no phase 4 or 5 gate can go green before
     2026-10-04.
Recommendation:        1 (bounded) — because the change writes down what was
                       decided and practised and decides nothing an ADR
                       would record, and the review before the merge holds
                       the class ("Nothing checks that the class is right",
                       docs/WORKFLOW.md).
If you say "ok":       the header keeps `class: bounded`, and the build
                       goes on as specified.
What is lost:          the ADR question is not put to the maintainer; its
                       answer would be "no" on this reading. This departs
                       from the precedent of classing upward when unsure
                       (plans/changes/harness-decide-adr/spec.md). If the
                       maintainer says "option 2", the header gains
                       `class: feature`, `change: template-bundle` and
                       adr_question: {proposed: "no", reason: "it writes
                       down the spec, findings and decision-record forms
                       that decisions D-2 and O-1 and the practised files
                       already set, and decides no architecture"}, and the
                       maintainer's answer is recorded with
                       `python3 scripts/harness.py decide adr --stated-in …`.
```

**Provisional answer, 2026-09-30:** option 1, `bounded`, chosen by this
phase under the orchestrator's instruction that no open `[DECISION]` may
remain while the maintainer is away. It awaits the maintainer's
confirmation at the merge, with the answers of `decisions.md`.

### [GAP] — closed by reading

All four `[GAP]`s of `research.md` section 7 are closed there, section 8:
MADR 4.0.0's own text; the Leerprobe baseline (356 of 387 at `eee26ae`);
the provenance class of a template written by an agent (declared, enforced
by nothing, held by review); and LakeSwitch's plan of 2026-09-28 (no
approval found).

### `[DETAIL]` — decided here, with the reason

Each of these is reversible and binds nothing beyond this change.

- **The phase gate is `plans_registry.py --check`.** Prompt 02 names
  `scripts/validate_change_artefacts.py`, which does not exist in this tree
  (`research.md` section 8, correction 2).
- **File names `templates/spec.md`, `templates/findings.md`,
  `templates/adr.md`.** The first two are the names of the files they start;
  the house calls its records ADRs, and the directory already says
  "template".
- **English, and every example header in a fenced `yaml` block** — house rule
  1, the `templates/` rule of `provenance.yaml`, and the handover template's
  precedent.
- **The goal is the opening sentence, not a heading.** Four of the five
  specs open that way, and the required sections of prompt 02 stay as they
  are.
- **The order of the spec template's sections.** The sections every spec
  already has keep their order; Protected areas stands after Non-goals
  because both bound the scope; the Definition of Done follows because it
  points to both; Open decisions stays last, as in every spec.
- **The example header is a feature's.** It shows every key a spec can
  need; a comment says that only a `feature` carries `change` and
  `adr_question` (with `proposed` quoted, as `prompts/02-spec.md` asks), and
  the class meanings are pointed to in `docs/WORKFLOW.md`, not restated —
  a second list would drift from the first.
- **`appetite:` in the header, a number of session hours, for every class.**
  LakeSwitch's key and unit (its D-24), and the word the parallel change
  `adhd-frame` uses; in the header so that a later validator (bead
  coding-harness-jc3) and the plan card read one place. No default number
  (as `adhd-frame` decides for its prompts). **This change's appetite is 4
  session hours:** research gave the chosen option 3.5–4.5 hours, and
  `decisions.md` answer 1 took that option with that consequence.
- **The criterion form is recommended, not required** (`decisions.md`,
  "Details the orchestrator adds"): When / While / If arrives with pull
  request #60, and the template must not state a rule `main` does not have.
- **Protected areas mean "must not touch".** `decisions.md` answer 3 reads
  them so; the ticket schema's other sense, areas whose change needs a
  person's approval, is what `provenance.yaml`'s `human-decided` paths
  already hold.
- **The Status values** the findings template lists: `open`, `fixed in
  <commit>`, `in spec`, `rejected — <reason>`, each optionally followed by a
  dash and a note. They are what the four findings files and prompt 02 use;
  portfolio's `fix`, `accepted` and `bead` are used by none of them.
- **The house's ADR section names, mapped to MADR 4.0.0.** Six of the
  seven ADRs on `main` carry all six, the seventh five of them; a template
  that differs from every record it serves makes the next ADR the odd one,
  and the mapping keeps the tie to MADR visible. MADR's
  optional *Pros and Cons of the Options* and *More Information* are named
  in one line as optional; the house writes *Consequences* and *Validation*
  as sections of their own, as it does today.
- **The ADR template's header and status lines follow ADR 0008**: `status:
  accepted`, `provenance: human-decided`, an empty `review` block, and the
  first bullet that the merge gives the decision effect.
- **One test file holds the three templates** against the modules and files
  that read their copies — the pattern of `tests/test_feedback_channel.py`
  for the handover template. The plan names it.
- **One `mechanismus` rule per template and one for the test** in the kit
  manifest; the export manifest already carries `templates/`.
- **The opening note of `docs/WORKFLOW.md` keeps its date and commit.** The
  two entries go; the others were measured absent at that commit, and
  re-measuring the whole list is not this change.
- **Overlaps with pull request #60**, for whichever of the two merges
  second: `prompts/03-plan.md` — both remove the same section, which git
  merges; the opening note of `docs/WORKFLOW.md` — keep #60's text without
  `templates/findings.md`; §4 of `docs/WORKFLOW.md` — keep #60's section,
  which has no plan-marking paragraph, and replace its words "because the
  findings template is not in this repository yet" with a pointer to
  `templates/findings.md` (the one §4 edit this change then makes);
  `prompts/06-review.md` — #60's text; `scripts/kit/manifest.yaml` — keep
  both sets of lines.
