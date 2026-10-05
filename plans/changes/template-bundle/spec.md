---
title: "Spec — template-bundle"
status: draft
implementation_status: none
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-9qo
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, templates, findings, adr, definition-of-done, design-phase, arc42]
class: bounded
appetite: 4
---

# Spec — template-bundle

After this change a spec, a findings table, an architecture decision record,
a design and an architecture description each have one written form under
`templates/`; the design phase 2b has its prompt and its rows in the workflow
tables; prompt 02 points to the spec form; and no workflow text points to a
template that does not exist (bead coding-harness-9qo). Research:
`research.md` — its sections 8 and 9 hold where they disagree with the text
above them. Decisions: `decisions.md`.

> **Answers, and what is still open — amended 2026-10-05.** Criteria 1–32
> were written on 2026-09-30 under provisional answers, while the maintainer
> was away. On 2026-10-05 the maintainer confirmed or changed each of them
> (`decisions.md`, both addenda of that day): the scope is the three
> templates plus the design phase 2b and an arc42 skeleton (answers 1 and
> 8); the practised findings table (2); the failure mode in the refutations
> and a protected-areas list (3); D-14 as decided (5); D-15 and O-3 amended
> by ADR 0009 toward a Mermaid architecture delta, in a decision pull request
> of its own that merges first (6); ROADMAP as a change of its own (7).
> Criteria 33–65 build the widened scope. Still provisional, for the
> maintainer at the merge: the class, which the spec review holds to be
> `feature` (`findings.md`, row 2a-1), and the scope of the appetite (row
> 2a-2). Answered later the same day: the licence of the arc42 skeleton is
> option 1, CC BY-SA 4.0 (Open decisions, `decisions.md` answer 9). Nothing
> here takes effect before the maintainer merges the pull request
> (`AGENTS.md`, house rule 8).

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

Read on 2026-10-05 at `3851f9c` (`research.md` section 9):

- **The design phase exists only in the target.** Decision D-14 (2026-09-16)
  gives a change a design phase 2b with a `design.md` — alternatives with
  consequences, interfaces, data model, an ADR draft and a model-as-code
  delta — mandatory for an `architectural` change and a stated choice for a
  `feature`. `main` has no `prompts/02b-design.md`, no design template and
  no 2b row in any phase table, and the one architectural change so far,
  pull request #60, ran without it. The delta's form was LikeC4 (D-15) until
  the maintainer chose to amend D-15 and O-3 by ADR 0009 toward a Mermaid
  diagram and three lists (`decisions.md`, answer 6).
- **An architecture description has no form.** Both existing descriptions
  follow arc42's order without a template (`docs/architecture/target-architecture.md`,
  LakeSwitch's architecture page); a new instance starts from nothing.
  arc42 is licensed CC BY-SA 4.0, and its licensors count its structure and
  headings as part of the licensed template (`research.md` section 9,
  item 1).

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
  <session>, <date>` and `Stage-2 call, …`, and the section of released loop
  rows criterion 17 names, as pull request #60 defines them (its runner
  `scripts/stage2.py` at `bd39160`, unchanged at `ef7407c`: `ROW_COLUMNS`,
  `RELEASED_COLUMNS`, `SESSION_LINE`, `VERDICT_LINE`, `RELEASE_HEADING`,
  `ROUNDS_LINE`, `NO_LOOP_LINE`).
- **MADR 4.0.0** — the Markdown Architectural Decision Records template at
  tag `4.0.0` of `github.com/adr/madr` (`research.md` section 8, gap 1).
- **Workflow texts** — `AGENTS.md`, `docs/WORKFLOW.md` and every
  `prompts/*.md`.
- **Appetite** — the hours the maintainer is willing to spend on phase 4 of
  a change, repair rounds included; a stop, not an estimate. The meaning the
  parallel change `adhd-frame` gives the word; provisional (Open decisions,
  "The scope of the appetite").
- **The design prompt, the design template, the arc42 skeleton** —
  `prompts/02b-design.md`, `templates/design.md`, `templates/arc42.md`.
- **D-14** — the decision of 2026-09-16 on the design phase: always for an
  `architectural` change; for a `feature` either the phase or one sentence in
  its `spec.md` saying why not; never for `bounded` or `spike`
  (`docs/architecture/target-architecture.md`, D-14; `decisions.md`,
  answer 5).
- **ADR 0009** — the decision record that amends D-15 and O-3: a change's
  architecture delta lives in its `design.md` as a Mermaid diagram plus lists
  of what is added, changed and removed, and LikeC4 stays the upgrade path
  (`decisions.md`, answer 6). It is written in a decision pull request of its
  own (branch `decide/adr-0009-mermaid-delta`) that merges before this
  change; on 2026-10-05 it was not written yet (`research.md` section 9,
  item 5).
- **Architecture delta** — the section of a `design.md` whose form ADR 0009
  sets.
- **arc42's twelve sections** — the section titles of arc42 9.0 in English
  (July 2025), in this order: Introduction and Goals, Architecture
  Constraints, Context and Scope, Solution Strategy, Building Block View,
  Runtime View, Deployment View, Cross-cutting Concepts, Architecture
  Decisions, Quality Requirements, Risks and Technical Debts, Glossary
  (`github.com/arc42/arc42-template`, `EN/adoc/`, read 2026-10-05).

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
   `plans_registry.STATUS` and `plans_registry.IMPLEMENTATION`;
   `check_frontmatter_current.read_updated` reads a date from it (the gate
   `frontmatter-current` holds every header under `plans/`); and
   `scripts/check_adr_answers.py` raises no finding about the header — only
   the one about the answer file the temporary tree lacks.
   *Refuted by:* a test that takes those names from the three modules at run
   time, not from a copy, and reports a missing or empty field, a refused
   value, no date from `read_updated` or a header finding; the same test
   staying green when a field the template lacks is added to `REQUIRED`.

4. **The template offers exactly the four classes.** The template's `class:`
   line names each entry of `check_adr_answers.CLASSES` and no other value.
   *Refuted by:* a test that finds a value in that line outside `CLASSES`, or
   an entry of `CLASSES` missing from it.

5. **When the example header is filled in, its size is the appetite.** The
   template's own `appetite:` value is a placeholder, not a number (no
   default appetite); filled in, it is a number greater than zero — the
   appetite as Terms defines it, for a change of any class — and the
   template's note on the key says "phase 4".
   *Refuted by:* a number as the template's own `appetite:` value; a
   filled-in header without `appetite`, or with a value YAML does not read
   as a number greater than zero; the note without "phase 4" (test).

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
   form mandatory (review); the template without the path
   `prompts/02-spec.md`, or without "#60" beside the recommendation (test).

9. **Protected areas are what the change must not touch.** The Protected
   areas section asks for the paths or areas the change must not touch, each
   with its reason, or the single line "None beyond the non-goals."
   *Refuted by:* the section's instruction without "must not touch",
   without "reason", or without that single line (test).

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
    appended for the released loop rows; the Status value `taken — <test or
    criterion>` of a loop row; the lines `Reviewer session: codex <id>`,
    `Phase 6 verdict: <reviewer> <session>, <date>` and one `Stage-2 call,
    <date>: <verb> · endpoint … · model … · leak check clean over …` line
    per call; and the section `## Phase 4b — GLM loop rows, released <date>`
    with the line `Rounds run: <n>`, or in its place the line `Loop rows:
    none — the GLM loop did not run for this change.` It says, with its
    date, that `docs/WORKFLOW.md` §4 defines them once that pull request is
    merged and that until then no change carries them.
    *Refuted by:* a column name or order, a line form or a heading that
    differs from `ROW_COLUMNS`, `RELEASED_COLUMNS`, `SESSION_LINE`,
    `VERDICT_LINE`, `RELEASE_HEADING`, `ROUNDS_LINE`, `NO_LOOP_LINE` or the
    `Stage-2 call` line in `scripts/stage2.py` at pull request #60's head
    (`ef7407c` on 2026-09-30; `stage2.py` unchanged since `bd39160`) (review
    — the runner is not in this tree); a sentence saying stage 2 is active
    or that the columns are required today.

18. **When the findings template's example header is filled in, it has what
    a file under `plans/` needs.** It has every field `plans_registry.REQUIRED`
    names, none of them empty, with `status` and `implementation_status` in
    the accepted sets, and `check_frontmatter_current.read_updated` reads a
    date from it.
    *Refuted by:* the test of criterion 3 run over this header reporting a
    missing, empty or refused field, or no date.

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
    present (test); `git diff origin/main -- prompts/03-plan.md` showing
    anything but the eight lines pull request #60 removes there — the
    heading, its five-line paragraph and the blank line after each
    (command).

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

30. **When `make verify` runs on the commit the maintainer merges, it is
    green**, run with `commit.gpgsign=false` as this repository's
    measurements are. Between the commit that sets `class: feature` and the
    maintainer's answer to the ADR question, the one expected red is the
    line of the gate `adr-answers` naming this change's missing answer (Open
    decisions, the class).
    *Refuted by:* `VERIFY RED` on the merged commit; before the answer, any
    red besides that one line.

31. **The Leerprobe does not lose a case.** On the pull request's last commit
    the Leerprobe carries at least as many cases as on its merge base with
    `origin/main`, measured the same way (356 of 387 at `eee26ae`,
    2026-09-30), and the new test is among the cases that carry. A case of
    the new test that reads a file the kit does not carry — `AGENTS.md`,
    which criteria 25 and 27 read, is `bestand` in
    `scripts/kit/manifest.yaml` — skips where that file is absent; the probe
    counts a skipped case neither way.
    *Refuted by:* a count below the merge base's, or a case of the new test
    among the red ones, in the probe's report.

32. **The new texts are English.** The three templates and every line this
    change writes into the workflow texts are English (`AGENTS.md`, house
    rule 1).
    *Refuted by:* a German sentence among them (review).

Criteria 33–65 were added on 2026-10-05 for the widened scope; 1–32 keep
their wording and their numbers.

### The design prompt

33. **The design prompt names a model that resolves.** The `**Model:**` line
    of `prompts/02b-design.md` names a model that `model-endpoints.yaml`
    declares.
    *Refuted by:* no case `[02b-design.md-…]` among the cases of
    `tests/test_model_endpoints.py::test_every_model_in_a_phase_prompt_resolves`,
    or that case red.

34. **The design prompt names the design template.** `prompts/02b-design.md`
    names `templates/design.md` as the form `design.md` is written in.
    *Refuted by:* the prompt without that path (test).

35. **The design prompt states D-14 for each class.** Its list of when the
    phase runs has one line for each class of `check_adr_answers.CLASSES`:
    `architectural` always; `feature` either the phase or one sentence in
    `spec.md` saying why not; `bounded` and `spike` never.
    *Refuted by:* a test that reads the classes from
    `check_adr_answers.CLASSES` at run time and finds a class without its
    line, the `architectural` line without "always", the `feature` line
    without `spec.md` or "one sentence", or a `bounded` or `spike` line
    without "never"; the same test staying green when a planted class is
    added to `CLASSES`.

36. **While no gate checks the class rule, the design prompt says so.** It
    says that nothing checks the rule until the validator of bead
    coding-harness-jc3 lands, and that the review before the merge holds it.
    *Refuted by:* the prompt without `coding-harness-jc3` (test); a sentence
    in it saying a gate checks the rule today (review).

37. **When a design holds an ADR draft, the design prompt says where the
    draft goes.** It becomes a record under `docs/adr/` in the change's own
    pull request, which makes that pull request a decision pull request.
    *Refuted by:* the prompt without `docs/adr/` or without "decision pull
    request" (test).

38. **The plan carries the design.** The design prompt says that phase 3
    plans from `spec.md` and `design.md` and writes into `plan.md` what
    phase 4 needs from the design, so that phase 4 still reads `plan.md` and
    `spec.md` only.
    *Refuted by:* no paragraph of the prompt naming phase 3, `design.md`,
    `plan.md` and phase 4 together (test); `prompts/03-plan.md` or
    `prompts/04-implement.md` edited for the design (the pull request's
    file list).

### The design template

39. **The design template has D-14's five parts, in order.** The
    second-level headings of `templates/design.md` are, in this order:
    Alternatives, Interfaces, Data model, ADR draft, Architecture delta.
    *Refuted by:* a test that reads the headings and finds one missing,
    renamed, added or out of this order.

40. **The alternatives come with their consequences and a choice.** The
    Alternatives section asks for at least two alternatives, each with its
    consequences, and for the chosen one with its reason.
    *Refuted by:* the section without "at least two", "consequence" or
    "chosen" (test).

41. **If a part has nothing to say, it says why in one sentence.** The
    sections Interfaces, Data model and ADR draft each offer `None — <one
    sentence why>` in place of their content.
    *Refuted by:* one of the three sections without that line (test).

42. **The ADR draft takes the form of the decision-record template.** The
    ADR draft section names `templates/adr.md` as its form and says that an
    `architectural` change always has one.
    *Refuted by:* the section without `templates/adr.md` or without
    `architectural` (test).

43. **The architecture delta is a Mermaid diagram of the state after the
    change.** The Architecture delta section holds a fenced `mermaid` block
    with a `flowchart` and asks for the part of the system the change
    touches, as it is after the change.
    *Refuted by:* no `mermaid` block in the section, a block that is no
    `flowchart`, or no "after the change" in the section (test); the
    section, the design template or the design prompt asking for a LikeC4
    model, a `.c4` file or `likec4` (test).

44. **Below the diagram stand three lists.** The Architecture delta section
    asks, below the diagram, for the elements and relationships the change
    adds, changes and removes, in three lists labelled Added, Changed and
    Removed.
    *Refuted by:* one of the three labels missing below the `mermaid` block
    (test).

45. **If nothing architectural moves, one sentence says why.** The
    Architecture delta section offers one sentence saying why in place of
    the diagram and the lists.
    *Refuted by:* the section without "nothing architectural moves" (test).

46. **The architecture delta names its source.** The Architecture delta
    section names ADR 0009 as the decision that sets its form.
    *Refuted by:* "ADR 0009" missing from the section (test).

47. **The architecture delta asks for what ADR 0009 decides, no more and no
    less.** Measured against ADR 0009 as merged on `origin/main`.
    *Refuted by:* an element ADR 0009 requires of the delta that the section
    lacks, or one the section requires that ADR 0009 does not (review,
    against `docs/adr/0009-*.md` on `origin/main` when the pull request
    opens).

48. **When the design template's example header is filled in, it has what a
    file under `plans/` needs.** It has every field `plans_registry.REQUIRED`
    names, none of them empty, with `status` and `implementation_status` in
    the accepted sets, and `check_frontmatter_current.read_updated` reads a
    date from it.
    *Refuted by:* the test of criterion 18, run over this header placed as
    `plans/changes/<change>/design.md`, reporting a missing, empty or refused
    field, or no date.

### The design phase in the doctrine

49. **The phase table of `docs/WORKFLOW.md` has a 2b row between 2a and 3.**
    In the table of §2, "The phases", the 2b row follows the 2a row, precedes
    the 3 row, names `design.md` and links `prompts/02b-design.md`.
    *Refuted by:* a test that reads the table's first cells and finds 2b
    missing or elsewhere, or the row without `design.md` or the link.

50. **The routing table gives 2b the design prompt's model.** In the table
    of §3, "Model routing", a 2b row stands between the 2a and the 3 row and
    names the model of the `**Model:**` line of `prompts/02b-design.md`.
    *Refuted by:* the row missing or elsewhere, or a model that differs from
    the prompt's (test).

51. **The phase table of `AGENTS.md` has a 2b row between 2a and 3.** In
    "The workflow in one screen", the 2b row follows the 2a row, precedes
    the 3 row and names `design.md`.
    *Refuted by:* the row missing, elsewhere or without `design.md` (test,
    which skips where `AGENTS.md` is absent).

52. **The doctrine states D-14 where the classes are defined.** The section
    "Change classes, the ADR question and decision pull requests" of
    `docs/WORKFLOW.md` has a paragraph that states D-14's rule for the four
    classes, names `prompts/02b-design.md` and says that nothing checks the
    rule until bead coding-harness-jc3.
    *Refuted by:* no paragraph of that section naming `02b-design.md`, each
    of the four classes and `coding-harness-jc3` (test).

53. **When a `feature` does without the design phase, the spec template
    says where its sentence goes.** The Non-goals section of
    `templates/spec.md` says that a `feature` without a `design.md` says
    there, in one sentence, why it does without the design phase.
    *Refuted by:* the Non-goals section without `design.md`, `feature` or
    "one sentence" (test); a new heading in the spec template (the test of
    criterion 1).

### The arc42 skeleton

54. **The skeleton has arc42's twelve sections in arc42's order.** The
    second-level headings of `templates/arc42.md` are arc42's twelve
    sections (Terms), in that order, each with its arc42 number.
    *Refuted by:* a test that strips the numbers and finds a title missing,
    renamed, added or out of order, or a number that is not the heading's
    position.

55. **The skeleton's texts are this repository's own.** No sentence of
    arc42's explanatory text is copied into `templates/arc42.md`; of arc42's
    words it holds only the section titles and the names in its credit.
    *Refuted by:* a run of eight or more words that the skeleton shares with
    arc42 9.0's English sources (`EN/adoc/*.adoc` of
    `github.com/arc42/arc42-template`, fetched into a scratch directory and
    never committed), outside the titles and the credit (command); review.

56. **The skeleton credits arc42 in the part a copy keeps.** Outside its
    leading comment it names arc42 with its version 9.0 of July 2025 and its
    creators Gernot Starke and Peter Hruschka, links `https://arc42.org` and
    the licence `https://creativecommons.org/licenses/by-sa/4.0/`, and says
    what the skeleton changed.
    *Refuted by:* one of these missing outside the leading comment (test).

57. **The skeleton states its licence as the maintainer answered.** Written
    for option 1 of the `[DECISION]` "The licence of the arc42 skeleton",
    which the maintainer chose on 2026-10-05: outside its leading comment it
    says that its structure and headings are an adaptation of arc42 under
    CC BY-SA 4.0 and that what is written into a copy stays its author's.
    *Refuted by:* either statement missing outside the leading comment
    (test).

58. **The skeleton asks for no more than a reader needs.** Its opening asks
    to fill only what a named reader needs and to say so in one line where a
    section has nothing; to give every number its commit or date; and to
    mark what is not known as open instead of filling it in.
    *Refuted by:* one of the three missing from the paragraphs before the
    first section (test).

59. **The decisions section points to the decision records.** The section
    Architecture Decisions points to the records under `docs/adr/` instead
    of asking for decisions of its own.
    *Refuted by:* the section without `docs/adr/` (test).

60. **When the skeleton's example header is filled in, `frontmatter-current`
    reads its date.** Filled in as the template's instructions say,
    `check_frontmatter_current.read_updated` reads a date from it.
    *Refuted by:* no date (test).

### The kit, the language and the merges

61. **The two new templates travel with the kit.** `scripts/kit/manifest.yaml`
    has a `mechanismus` rule with a reason for `templates/design.md` and for
    `templates/arc42.md`; the design prompt travels by the rule for
    `prompts/`.
    *Refuted by:* `python3 scripts/kit/probe.py --list` without one of the
    two; `tests/test_kit.py` red.

62. **The design prompt's model case is the one new exemption.**
    `REIST_NICHT` in `scripts/kit/probe.py` gains exactly the case of
    criterion 33, as `bestand-dieses-repos`, and `DECKEL` rises by one with
    a comment that says why, as it did for `01a` and `02a`.
    *Refuted by:* `python3 scripts/kit/probe.py --strict` red; more than one
    new entry, or the cap without its comment (diff).

63. **The new texts of the widened scope are English.** The design prompt,
    the design template, the arc42 skeleton and every line criteria 33–62
    write into other files are English (`AGENTS.md`, house rule 1).
    *Refuted by:* a German sentence among them (review).

64. **When the branch is merged in trial with pull request #60, it adds
    conflicts only where predicted.** The files `git merge-tree --write-tree
    --name-only` reports as conflicting for this pull request's head and
    #60's head, less those it reports for `origin/main` and #60's head, are
    only `docs/WORKFLOW.md` (the opening note, the routing table of §3, §4),
    `scripts/kit/probe.py` (the prompt entries, the cap) and
    `plans/INDEX.md`; resolved as `plan.md` says, `tests/test_templates.py`
    passes on the merged tree.
    *Refuted by:* another file in that difference (command); a red case of
    `tests/test_templates.py` on the resolved tree.
    *Amended 2026-10-05 ([DETAIL], orchestrating session):* the first
    wording counted every conflict with #60. Once ADR 0009 merged (criterion
    65), `origin/main` itself conflicts with #60 in the two architecture
    documents of 2026-09-17, so criteria 64 and 65 could not both hold as
    written. The intent, that this change adds no unforeseen conflict, is
    kept; measured on 2026-10-05 at `4e99ec5`, the difference is exactly
    the three predicted files.

65. **ADR 0009 merges before this change.** When this pull request is
    merged, the merge commit of ADR 0009's pull request is an ancestor of
    its head.
    *Refuted by:* `git merge-base --is-ancestor <ADR 0009's merge commit>
    HEAD` failing on the pull request's head (command); this pull request
    merged while ADR 0009's is open.

## Non-goals

### Not now, and what brings each back

Amended 2026-10-05: the design phase 2b and the arc42 skeleton left this
list for the scope (`decisions.md`, answers 1 and 8).

- **A `ROADMAP.md` template.** The maintainer chose to try the file first: a
  `ROADMAP.md` in Coding Harness with at most three "Now" themes, checked at
  every hand-over, and a kit template only once that file has stayed true
  through two hand-overs — a change of its own, not this one (`decisions.md`,
  answer 7).
- **The LikeC4 specification and its model gate.** ADR 0009 amends D-15 and
  O-3 toward the Mermaid delta of `design.md`; LikeC4 stays the upgrade
  path, back when one of the revisit triggers of
  `docs/research/2026-10-05-likec4-roadmap-arc42.md` (section A7) fires
  (`decisions.md`, answer 6).
- The tracker writer — not this change — cuts bead coding-harness-9qo to
  this scope; the ROADMAP trial and the LikeC4 triggers have homes of their
  own.

### Not in this change

- **No `design.md` for this change** — D-14's sentence for a `feature`: it
  adds forms and doctrine text, no component, interface or data model of a
  system, and the one architecture question it touches, the form of the
  delta, is ADR 0009's.
- **A check that a spec follows the template** — presence of class,
  Definition of Done, protected areas or appetite — or that a change ran the
  design phase as D-14 says, that a `feature`'s spec carries its sentence,
  or that a `design.md` holds an ADR draft. The templates are forms, not
  gates; the validator rules are bead coding-harness-jc3.
- **Findings as checked data** — a machine-readable list and its gate (bead
  coding-harness-4me), which may extend this template later.
- **Reshaping existing artefacts** to the templates: no spec, findings file
  or ADR, active or archived, is changed, and no change gets a `design.md`;
  ADR 0007 on pull request #60 keeps its order.
- **Building anything of stage 2** or editing pull request #60's branch; the
  stage-2 columns are named, not implemented.
- **ADR 0009 itself** — the record, the continuity rows of D-15 and O-3, its
  `AMENDMENT_ADRS` entry and the target's wording: a decision pull request
  of its own, which merges first (`decisions.md`, answer 6).
- **Updating the target and gap documents** under `docs/architecture/`.
  Their rows from 2026-09-17 still name `plan-marking.md` as moving here;
  they record the design of that date, and the re-scoped bead and this spec
  record the change of plan.
- **Writing an architecture description** with the skeleton: no arc42
  description of Coding Harness or LakeSwitch is written or converted, and
  `docs/architecture/target-architecture.md` stays as it is.
- **The kit's licence file** (bead coding-harness-lir). This change states
  only the arc42 skeleton's own licence, in the skeleton (Open decisions).
- **Prompts 03, 04 and 07 for the design.** The plan takes the design in by
  the design prompt's sentence (criterion 38), and the ADR draft's move to
  `docs/adr/` is stated there too (criterion 37).
- **The README's one-line cycle.** Pull request #60 did not add its 4b
  there either; the phase tables are the doctrine.
- **Class duties beyond D-14** — the one-way ratchet, phases per class (as in
  `plans/changes/harness-decide-adr/spec.md`, Non-goals). D-14's rule is
  stated, not checked. The appetite applies to every class and is no class
  duty.
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
- **`docs/WORKFLOW.md` beyond** the opening note, the plan-marking
  paragraph of §4 and the first sentence of the paragraph after it (repair
  round 1, finding 6-7), the 2b row of §2's phase table, the 2b row of §3's
  routing table and one paragraph in "Change classes, the ADR question and
  decision pull requests" — in particular every other row of those two
  tables and the rest of §3, which pull request #60 edits; and **`AGENTS.md`
  beyond the 2b row of its phase table**, whose other rows pull request #60
  edits. One exception, only if pull request #60 merges first: the sentence
  of its §4 that the `[DETAIL]` "Overlaps with pull request #60" names.
- **Every path `provenance.yaml` reserves for `human-decided`** — `docs/adr/`,
  `decisions/answers/`, the rule set — so that this pull request is no
  decision pull request. One exception, only once the maintainer answers
  the ADR question of this change as a `feature`: its own answer file
  `decisions/answers/template-bundle/adr.yaml`, which makes the pull request
  a decision pull request (Open decisions, the class).
- **`docs/architecture/`** — the target, its decision-continuity table, the
  gap analysis and the implementation plan.
- **`templates/handover.md` and `templates/gate-record.yaml`.**
- **Every other change folder** under `plans/changes/`, active or archived.
- **`.github/`, `prompts/04-implement.md` and `prompts/07-commit.md`** — the
  parallel change `adhd-frame` edits them; `prompts/03-plan.md` loses only
  its markings section.
- **The gate scripts, `decisions/gates.yaml` and
  `scripts/export/manifest.yaml`** — no gate is added or changed, and the
  export manifest already carries `templates/`; and **`scripts/kit/probe.py`
  beyond one `REIST_NICHT` entry and its cap** (criterion 62).
- **`README.md` and `model-endpoints.yaml`** — the design prompt names a
  model that is declared already.

## Definition of Done

- `verify` green.
- Moved in the same pull request: the five templates (`templates/spec.md`
  with the Non-goals sentence of criterion 53) and their test;
  `prompts/02b-design.md`; `prompts/02-spec.md` (the reference);
  `prompts/03-plan.md` (the markings section removed); `docs/WORKFLOW.md`
  (the opening note, the plan-marking paragraph of §4, the 2b rows, the
  D-14 paragraph); `AGENTS.md` (the 2b row); `scripts/kit/manifest.yaml`;
  `scripts/kit/probe.py` (one entry, the cap); `plans/INDEX.md` regenerated.
  No ADR and no model moves: ADR 0009 is its own pull request.
- The protected areas above untouched and nothing of the not-now list built,
  shown by the pull request's file list.
- Bead: the last commit carries `Closes-Bead: coding-harness-9qo` only once
  the tracker writer has cut the bead to this scope; until then no closing
  trailer, and the pull request body says so.
- Special runs, with their commit in the pull request body:
  `python3 scripts/check_docs.py` without a dead link into `templates/`; the
  Leerprobe's count against its merge base's (356 of 387 at `eee26ae`, and
  at `3851f9c`); the arc42 copy check (criterion 55); the trial merge with
  pull request #60 (criterion 64); ADR 0009's merge commit as an ancestor
  (criterion 65).
- The pull request body lists the maintainer's answers of `decisions.md`
  and what is still provisional — the class with the spec review's verdict
  `feature`, and the scope of the appetite — together with the answer on the
  arc42 skeleton's licence, naming the skeleton's licence for the kit's
  licence work (bead coding-harness-lir); and it names the overlaps with
  pull request #60 and how the later merge resolves each (the `[DETAIL]`s
  "Overlaps with pull request #60" below).

## Open decisions

None open: the one question of the amendment of 2026-10-05, the licence of
the arc42 skeleton, was answered by the maintainer the same day. Two
provisional answers await the maintainer at the merge: the class, and the
scope of the appetite.

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
     must do or how it is checked": three new templates, and every later
     spec carries three more sections, a Definition of Done among them.
     Consequence: the header adds `change: template-bundle` and
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

**Spec review (phase 2a), 2026-09-30: the class is `feature`** (`findings.md`,
row 2a-1). The definition on `main` reads in full "changes what the system
must do or how it is checked"; the template sets how every later change is
checked — a Definition of Done, Protected areas, the appetite — and prompt
02 makes it the form of every spec. The change also decides, provisionally,
the four answers of `decisions.md`, the readings of D-2's failure mode and
protected areas, and the retirement of plan markings on `main`. That it
decides no architecture argues for the ADR answer "no", a feature's answer,
not for a lower class; a class chosen because it keeps a gate green is the
misclassification the one-way ratchet stands against. Once pull request #60
merges, the class also picks the reviewer of phases 2a and 6. The maintainer
decides at the merge.

**How the pull request proceeds without the maintainer** — the spec
review's path, which needs the maintainer only at the end:

1. Phases 3 to 6 run under the provisional `class: bounded`, so `make
   verify` measures every gate green and the build's evidence stays clean.
2. The commit that opens the pull request (phase 7) sets `class: feature`,
   `change: template-bundle` and the `adr_question` of option 2 with
   `answered_by: null`. From then on the gate `adr-answers` reports exactly
   one line, this change's missing answer, and the pull request is red on
   that gate alone — as the spec of pull request #54 prescribed for its own
   missing answers (`plans/changes/harness-decide-adr/spec.md`, "The pull
   request waits for the maintainer's answers; no ramp").
3. The maintainer answers after 2026-10-04 with `python3 scripts/harness.py
   decide adr` on this branch — typed, or stated and recorded with
   `--stated-in`. The answer file `decisions/answers/template-bundle/adr.yaml`
   lands in this pull request, which then becomes a decision pull request
   (title `decide(<scope>): …`, label `decision`, the block of
   `.github/PULL_REQUEST_TEMPLATE/decision.md`), as pull request #54 was;
   `make verify` goes green (criterion 30).
4. If the maintainer confirms `bounded` instead, one commit removes the
   three keys, and the gate is green without an answer.

**Amendment, 2026-10-05.** The widened scope leaves the reading as it was:
the design phase and the skeleton set how later changes are designed and
described, which is still "how it is checked", and the change decides no
architecture of its own — D-14 was decided on 2026-09-16, and the delta's
form is ADR 0009's. The proposal the class commit writes becomes
`adr_question: {proposed: "no", reason: "it writes down the forms of a spec,
a findings file, a decision record, a design and an architecture
description, and the design phase that decision D-14 set, and decides no
architecture"}`.

### [DECISION] — The scope of the appetite (provisional answer: phase 4)

Raised by the spec review as `[AMBIGUITY]` (`findings.md`, row 2a-2): this
spec and the parallel change `adhd-frame` (its `spec.md` at `ac30a69`,
Terms) gave the one word two scopes.

```text
Goal in one sentence:  Say what the number on a spec's `appetite:` line
                       covers, so the plan card and the stop of the
                       parallel change read it as the spec meant it.
Options:
  1. The whole change — "the session hours the outcome is worth", as
     LakeSwitch's D-24 words it. Consequence: `adhd-frame` changes its
     term, or its plan card compares a phase-4 figure with a whole-change
     one, and a card that gives phase 4 the whole appetite widens nothing.
  2. Phase 4 — "the time the maintainer is willing to spend on phase 4 of
     a change; a stop, not an estimate", as `adhd-frame` defines it.
     Consequence: only this spec changes; the key keeps LakeSwitch's name
     and unit but not its scope, and a template carried to LakeSwitch says
     phase 4.
Recommendation:        2 — because the stop of `adhd-frame` is the one text
                       that acts on the number, and `decisions.md` chose the
                       word so that the two name one concept.
If you say "ok":       the template's note on `appetite:` says phase 4,
                       repair rounds included; criterion 5 holds it.
What is lost:          one number for the budget of the whole change;
                       nothing records it.
```

**Provisional answer, 2026-09-30:** option 2, taken by phase 2a so that no
`[AMBIGUITY]` stays open while the maintainer is away; the maintainer
settles it at the merge. This change's own `appetite: 4` stands: research's
3.5–4.5 hours size the building of the contract core.

**Amendment, 2026-10-05.** The widened scope keeps `appetite: 4` for phase 4
of the whole change; the reason is the `[DETAIL]` "The appetite stays at 4
hours" below.

### [DECISION] — The licence of the arc42 skeleton (answered 2026-10-05: option 1)

The maintainer asked that the licence point be checked, not assumed
(`decisions.md`, answer 8). The check (`research.md` section 9, item 1)
finds that arc42's licensors count the template's structure and headings,
not only its explanatory text, as what CC BY-SA 4.0 covers, and that an
adapted template made public carries CC BY-SA 4.0; Apache-2.0, the kit's
licence by decision D-17, cannot take such an adaptation. Writing in this
repository's own words therefore does not by itself keep the skeleton under
the kit's licence. Today nothing is shared: both repositories are private,
and the kit's licence file does not exist yet.

```text
Goal in one sentence:  Say under which licence the arc42 skeleton travels,
                       now that arc42's licensors count its structure and
                       headings as part of their licensed template.
Options:
  1. Mark the skeleton as an adaptation of arc42 under CC BY-SA 4.0 — the
     one file of the kit under that licence, beside the kit's Apache-2.0.
     Consequence: it follows the licensors' own reading; a copy keeps the
     notice, and what an instance writes into its copy stays its own, as
     arc42 says; when the kit goes public, its licence file names this one
     exception (bead coding-harness-lir).
  2. Credit and links only; the licence is left to the kit's licence work
     (bead coding-harness-lir). Consequence: nothing changes while both
     repositories stay private; the file sits in a kit meant for
     Apache-2.0 with a status that the licence work has to find and settle
     before publication.
  3. No arc42 headings: the skeleton links arc42's twelve sections and uses
     titles and an order of its own. Consequence: the kit keeps one
     licence; the shared order answer 8 chose is lost, and with it most of
     what makes the file a skeleton.
Recommendation:        1 — because it keeps answer 8 whole, costs one
                       sentence, and puts the exception where the licence
                       work will see it instead of leaving it to be found
                       at publication.
If you say "ok":       the skeleton ends, in the part a copy keeps, with the
                       credit of criterion 56 and the statement of
                       criterion 57; the pull request body names the
                       exception for bead coding-harness-lir.
What is lost:          a kit under a single licence; an instance that
                       publishes its adapted skeleton publishes that
                       skeleton, not its content, under CC BY-SA 4.0.
```

**Answer, 2026-10-05:** option 1, by the maintainer in the Claude Code
session (`decisions.md`, answer 9). The skeleton carries CC BY-SA 4.0, stated
visibly and with arc42's credit; it is the one exception in a kit meant to be
Apache-2.0 (bead coding-harness-lir). It is an assessment, not legal advice,
and both repositories are private, so nothing is shared today. Options 2 and
3 are not taken: criteria 54 and 57 stand as written, and phase 4 builds the
skeleton last, as the plan says.

### [GAP] — closed by reading in the amendment of 2026-10-05

`research.md` section 9: the arc42 licence (item 1); the probe's exemption
for a prompt with a model line, and the phase words of the kit files (2);
the Leerprobe at the new merge base, 356 of 387 at `3851f9c` (3); the trial
merges of the planned rows with pull request #60 (4); ADR 0009, not written
yet — not read (5); what reads a `design.md` and an arc42 copy (6); where
2b's model is checked (7); the README's line (8).

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
- **`appetite:` in the header, a number of hours, for every class.**
  LakeSwitch's key and unit (its D-24), with the scope the parallel change
  `adhd-frame` gives the word, phase 4 (Open decisions, "The scope of the
  appetite"); in the header so that a later validator (bead
  coding-harness-jc3) and the plan card read one place. No default number
  (as `adhd-frame` decides for its prompts): the template shows a
  placeholder. **This change's appetite is 4 hours:** research gave the
  chosen option 3.5–4.5 hours of building, and `decisions.md` answer 1 took
  that option with that consequence.
- **The criterion form is recommended, not required** (`decisions.md`,
  "Details the orchestrator adds"): When / While / If arrives with pull
  request #60, and the template must not state a rule `main` does not have.
- **Protected areas mean "must not touch".** `decisions.md` answer 3 reads
  them so; the ticket schema's other sense, areas whose change needs a
  person's approval, is what `provenance.yaml`'s `human-decided` paths
  already hold.
- **The Status values** the findings template lists: `open`, `fixed in
  <commit>`, `resolved <date> by <source>`, `answered` (a phase-2a question
  answered in phase 6), `in spec` and `rejected — <reason>`, each optionally
  followed by a dash and a note — the values the four findings files and
  prompt 02 use (`research.md` section 8), named as the values in use, not
  as a closed set; a checked set is bead coding-harness-4me's. Portfolio's
  `fix`, `accepted` and `bead` are used by none of them. Stage 2's `taken —
  <test or criterion>` stands with the stage-2 columns (criterion 17).
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

### `[DETAIL]` — decided in the amendment of 2026-10-05, with the reason

Each of these is reversible and binds nothing beyond this change.

- **File names `prompts/02b-design.md`, `templates/design.md`,
  `templates/arc42.md`.** D-14 and the target name the prompt; the design
  template is named after the file it starts; the skeleton is one file
  because both existing descriptions are one document each.
- **The design template's sections follow D-14's list**, with the
  architecture delta in the place of the model-as-code delta, which ADR
  0009 replaces.
- **The design template's header** carries the keys of a findings file's
  header and no `class` or `adr_question`, which only `spec.md` carries
  (`research.md` section 9, item 6).
- **2b runs on Opus 5.5 at effort `xhigh`**, as spec and plan do: the
  target's requirement table groups the three (`research.md` section 9,
  item 7), and the maintainer set that routing for spec and plan on
  2026-09-29. One line in the prompt and one row in §3 change it.
- **The 2b row goes into `AGENTS.md` as well.** "The workflow in one screen"
  is the table every harness reads first; a phase that §2 lists and it does
  not would be two answers to one question. The trial merge with pull
  request #60 is clean there (`research.md` section 9, item 4).
- **D-14 is stated in "Change classes, the ADR question and decision pull
  requests"**, right after the four classes: it is a rule by class, and
  pull request #60 does not edit that section.
- **A `feature`'s sentence goes into Non-goals** of its spec: it says what
  the change does not do and why, which is what Non-goals hold, and
  LakeSwitch's specs write it as "No `design.md`: <reason>". A section of
  its own would change criterion 1's seven headings.
- **The design prompt names the gate that runs**, `python3
  scripts/plans_registry.py --check`; prompts 02 and 03 name
  `scripts/validate_change_artefacts.py`, which is not in this tree
  (`research.md` section 8, correction 2).
- **The plan takes the design in by the design prompt** (criterion 38), so
  prompts 03, 04 and 07 stay as they are: 04 and 07 are protected, and 03
  changes only by the markings section.
- **One test file.** The new cases join `tests/test_templates.py`, which the
  kit carries already.
- **arc42's titles in English, numbered 1 to 12**, as arc42 9.0 numbers
  them, so that a reader maps each section to arc42 at a glance.
- **The appetite stays at 4 hours** for phase 4 of the whole change. The
  first slice used 21 minutes of it (`plan.md`, "Time used"); research's
  5–7 hours for the core plus 2b and 0.5–1 hour for the skeleton are
  estimates that the first slice undercut by an order of magnitude (9
  minutes against 3.5–4.5 hours). An appetite is a stop: when it is reached
  the maintainer is asked (prompt 04), so a smaller one asks earlier rather
  than builds more.
- **Overlaps with pull request #60 for the rows of the widened scope**, for
  whichever of the two merges second (`research.md` section 9, item 4): the
  routing table of §3 — keep #60's rows and add the 2b row after its 2a
  row; `scripts/kit/probe.py` — keep #60's prompt entries and add the 2b
  entry, and set the cap to the length of the merged list (33) with both
  comments; `AGENTS.md`, §2's table, the "Change classes" paragraph and the
  kit manifest merge without a conflict.
