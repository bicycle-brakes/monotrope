---
title: "Plan — template-bundle"
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
tags: [plan, templates, findings, adr, design-phase, arc42]
---

# Plan — template-bundle

```text
For you:     one form each for a spec, a findings table and an ADR; prompt 02 names the spec form; no dead template link; plan markings retired
Done when:   the checks below hold criteria 1–32, `make verify` green, the Leerprobe not below 356 cases (merge base f985698)
Appetite:    4 h of phase 4, repair rounds included
Not now:     design phase 2b, ROADMAP, arc42, LikeC4; a check that specs follow the form; findings as checked data
Pre-mortem:  suppose it failed: most likely because the one test file, holding about 30 criteria, eats the appetite before the templates read well
Starts unless you say stop.
```

Implements `spec.md` (criteria 1–32), provisional like it: phases 3 to 6 run
under `class: bounded`, phase 7 sets `class: feature` (spec, Open decisions),
and the appetite covers phase 4 only. No model markings: this change retires
them. Phase 2a ran; phase 6 appends its rows to the same `findings.md`. Facts
read on 2026-09-30: `origin/main` `f985698`, pull request #60 at `ef7407c`,
#62 `b8667ed`, #63 `abe5508`, #64 `9048837`, `adhd-frame` `306b5ac`.
Slice 2 — the design phase and the arc42 skeleton, criteria 33–65, added on
2026-10-05 — stands below, before "Phase 7", with its own card.

## Decided in phase 3

No `[DECISION]` is open.

- `[GAP]`, closed — #63 translates `scripts/plans_registry.py` but keeps
  `REQUIRED`, `STATUS`, `IMPLEMENTATION` and `_frontmatter`; #62 touches only
  `templates/handover.md` and `templates/gate-record.yaml`; #64 only
  `tests/test_ci.py`; none of #60's workflow texts contains a marking string
  or a `templates/` path besides `findings.md` and `handover.md`.
- `[GAP]`, closed — `tests/test_kit.py::test_the_kit_does_not_describe_the_phases`
  goes red when a kit file names five of the seven phase words; the kit
  manifest names four already (spec, plan, verify, commit), so no new reason
  may contain "explore", "implement" or "review" (also not "reviewer").
- `[DETAIL]` — **each template reads like its copy:** a leading `<!-- … -->`
  with the instructions that are not copied, the example header in a fenced
  `yaml` block, then the title and the body. The findings template's
  reference part follows its copy part after a line `---`, as lists, so the
  first table is the practised one (criterion 13).
- `[DETAIL]` — **placeholders are `<…>`.** The test fills `<YYYY-MM-DD>` with
  a date, `<hours>` with `3`, `<yes|no>` with `no`, `<change>` with the
  temporary folder's name, and every other `<…>` with `Filled` — one rule for
  all three headers, and no default number in the template.
- `[DETAIL]` — **the class line** is `class: feature  # spike | bounded |
  feature | architectural`: `_CLASS_LINE` of the gate accepts the comment, and
  the test reads the four names off one line.
- `[DETAIL]` — **`## Terms`**, with "Optional" in its body, not its heading, so
  copies keep the heading existing specs use.
- `[DETAIL]` — **paths in templates are code spans, never Markdown links:** a
  copy lands at another depth, where a relative link breaks.
- `[DETAIL]` — **the test reads with the gates' own readers**
  (`plans_registry._frontmatter`, `check_frontmatter_current.read_updated`,
  `check_adr_answers.examine`) and reads their constants at call time, so a
  monkeypatched constant reaches it.
- `[DETAIL]` — **the kit rules** stand after `templates/handover.md` and after
  `tests/test_feedback_channel.py`, away from #60's two insertions (after base
  lines 90 and 149), so neither merge conflicts there.
- `[DETAIL]` — **a clock for the appetite:** phase 4 reads `date` at its start
  and end and appends `<date> <start>–<end>, <span>` under "Time used" below,
  as `adhd-frame`'s prompt 04 will ask; without it the appetite stops nothing.

## Steps

1. `templates/spec.md` (40 min) — top to bottom: the comment (copy to
   `plans/changes/<change>/spec.md`; the block becomes the header between two
   `---` lines; the rules are `prompts/02-spec.md`; the class meanings are
   `docs/WORKFLOW.md`, "Change classes, the ADR question and decision pull
   requests"); the block with a feature's header — the keys of this change's
   spec header with `<…>` for its values, the class line above, `appetite:
   <hours>  # hours of phase 4, repair rounds included — a stop, not an
   estimate`, and `change: <change>` and `adr_question: {proposed: "<yes|no>",
   reason: "<one sentence>"}`, each commented "a feature only", the quotes
   kept; no comment line of its own in the block, only comments after a
   value; `# Spec — <change>`; the goal paragraph (2); then
   the seven sections of criterion 1 — Terms "Optional"; Acceptance criteria
   with the rule sentence (6, 8) and the example `1. When <trigger>, <what
   holds>.` over `   *Refuted by:* <…>.` (7); Protected areas (9, verbatim
   "None beyond the non-goals."); Definition of Done as five lines, the first
   "- `verify` green." (10, 11); Open decisions pointing to prompt 02's form.
2. `templates/findings.md` (30 min) — the comment; the block (the keys of this
   change's `findings.md`); `# Findings — <change>`; a paragraph for phase,
   commit, date and reader; the table of criterion 13 with one example row;
   `Reviewer session: <id>`; `## Checked without a finding`; `## Not
   checked`; `---`; the reference: severities, dimensions, origins with the
   escalation, the two markers (`[DIVERGENT]` counts as a `BLOCKER`), "only
   with new evidence" (14); the Status values of the spec's `[DETAIL]`, as
   values in use (15); stage 2 (17), dated 2026-09-30, in a `text` block:
   `| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status |
   Broke a test |`, the same row with `Phase 6 |` appended for released rows,
   `taken — <test or criterion>`, `Reviewer session: codex <id>`,
   `Phase 6 verdict: <reviewer> <session>, <date>`, `Stage-2 call, <date>:
   <verb> · endpoint <endpoint> · model <model> · leak check clean over <n>
   files, <n> commits, <n> rules.`, `## Phase 4b — GLM loop rows, released
   <date>` with `Rounds run: <n>`, or `Loop rows: none — the GLM loop did not
   run for this change.` Portfolio's text may lend wording, never columns.
3. `templates/adr.md` (20 min) — the comment: MADR 4.0.0
   (`https://github.com/adr/madr`, tag `4.0.0`) with one line per pair
   (Context — Context and Problem Statement; Decision — Decision Outcome;
   Validation — Confirmation) and its two optional sections (20); the
   decision pull request (22); an amendment's "Amend" row in "Decision
   continuity" and `AMENDMENT_ADRS` (23). The block: ADR 0008's eleven fields
   (24). `# ADR <NNNN> — <the decision as a statement>`; ADR 0008's three
   bullets, the first verbatim up to "closed is rejected." (21); the six
   sections of criterion 19, Decision opening `Chosen option: "<title>",
   because <justification>.` Commit steps 1–3.
4. `tests/test_templates.py` (70 min) — English; helpers for the fenced block,
   the fill, headings outside fences, one section's text, header
   problems, Definition-of-Done problems and missing `templates/` paths
   (`templates/[\w./-]*\w`, resolved from the root). The cases are the table
   below; the workflow-text cases are parametrized over `AGENTS.md`,
   `docs/WORKFLOW.md` and `sorted(prompts/*.md)` and skip a file that is
   absent (31). Commit.
5. The texts (15 min) — `prompts/02-spec.md`: after line 8 a paragraph of its
   own, "Write `spec.md` in the form of `templates/spec.md`: copy it into the
   change folder and fill it in." `prompts/03-plan.md`: delete lines 22–29
   ("Model markings" heading through the blank line after its paragraph).
   `docs/WORKFLOW.md`: from the opening note drop `templates/findings.md` and
   `templates/plan-marking.md` and reflow the two lines, date and commit kept;
   in §4 delete the paragraph "**The assignment stands in the plan.** …" and
   the blank line after it. `scripts/kit/manifest.yaml`: four `mechanismus`
   rules with English reasons — the three templates ("the form of …; …
   names it") and the test ("holds the three templates against the gate
   modules; skips a case whose file does not travel"). Commit.
6. Checks (25 min) — the block below; on a day after 2026-09-30 first
   `python3 scripts/check_frontmatter_current.py --stamp`; `python3 -m ruff
   format scripts/ tests/`; `python3 scripts/plans_registry.py --index`; the
   verification; push. The last line is the `done:` line of `adhd-frame`'s
   form, `done: <evidence> · <time used> of 4 h`.

Verification, verbatim (the prefix only where commit signing is unavailable):
`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify`,
ending `VERIFY GREEN`.

## Tests and checks per criterion

| # | Held by (`tests/test_templates.py` unless named) | Red when |
|---|---|---|
| — | `test_templates_carry_no_real_header[3]` | a template starts with `---` |
| 1 | `test_spec_sections_in_order` | a `##` heading missing, renamed, added or moved; Terms without "Optional" |
| 2 | `test_spec_opens_with_the_goal` | first paragraph after `# ` lacks "goal", `research.md` or `decisions.md` |
| 3 | `test_filled_spec_header_passes_the_gates`; counter `test_header_check_sees_a_new_required_field` | a `REQUIRED` field missing or empty, a status outside the sets, no date from `read_updated`, `examine()` lines other than the one missing answer; the counter: `REQUIRED` plus a field reported nothing |
| 4 | `test_class_line_offers_the_four_classes` | the names on the `class:` line differ from `CLASSES` |
| 5 | `test_appetite_is_a_placeholder_for_phase_4_hours` | the raw value is a number; the filled one is no number above 0; the line lacks "phase 4" |
| 6 | `test_failure_mode_lives_in_the_refutations` | a heading holds "failure mode"; Acceptance criteria lacks it beside "Refuted by" |
| 7 | `test_example_criterion_has_condition_and_refutation` | item `1.` begins otherwise than When/While/If, or its next line not `*Refuted by:*` |
| 8 | `test_criterion_form_is_a_recommendation`; review | no `prompts/02-spec.md`, no "#60" in the paragraph naming When/While/If; "one condition" outside a sentence that says "recommended" (repair round 1); review: a sentence making When/While/If mandatory |
| 9 | `test_protected_areas_ask_what_must_not_be_touched` | "must not touch", "reason" or "None beyond the non-goals." missing |
| 10 | `test_done_names_the_gates_in_one_line`; counter `test_done_check_catches_a_planted_gate` | "`verify` green" not exactly once; an id from `decisions/gates.yaml` on another line; the planted "- `pytest` green." not reported |
| 11 | `test_done_asks_the_change_specific_items`; review | "same pull request", "protected areas", "non-goals", "Closes-Bead" or "special runs" missing; review: an every-change item |
| 12 | `test_spec_prompt_names_the_template` | the path absent from `prompts/02-spec.md` |
| 13 | `test_findings_table_has_the_practised_columns` | the first table's header row differs cell by cell |
| 14 | `test_findings_vocabulary_is_here` | a term of criterion 14 without its own entry in its own list of the reference part; no "escalation" in the `fix-r<N>` entry, no `BLOCKER` in the `[DIVERGENT]` entry, no "new evidence" below the `---` line (repair round 1) |
| 15 | `test_status_values_include_the_spec_review_ones` | `in spec` or `rejected — <reason>` without an entry in the Status list (repair round 1) |
| 16 | `test_lines_under_the_table` | the line `Reviewer session: ` with `<id>` in backticks, or either heading, missing (repair round 1) |
| 17 | check below; review against `stage2.py` | a string of the check missing; a sentence saying stage 2 is active |
| 18 | `test_filled_findings_header_passes_the_plans_gates` | as 3, without `examine()` |
| 19 | `test_adr_sections_in_order` | the six headings differ |
| 20 | `test_adr_names_madr_and_maps_the_names` | "MADR 4.0.0", the address or a pair's line missing |
| 21 | `test_adr_takes_effect_by_the_merge`; review | the merge sentence, "open is proposed" or "closed is rejected" missing; review: a signature as acceptance |
| 22 | `test_adr_names_the_decision_pull_request` | `decide(<scope>)`, `decision` or the template path missing |
| 23 | `test_adr_names_what_moves_with_an_amendment` | "Amend", "Decision continuity" or `AMENDMENT_ADRS` missing |
| 24 | `test_adr_header_has_the_fields_of_the_adrs` | one of the eleven fields missing; `category` not `adr`, `provenance` not `human-decided` |
| 25 | `test_no_workflow_text_names_a_missing_template[file]`; counter `test_path_check_catches_a_planted_path` | a named `templates/` file absent; the planted `templates/missing.md` not reported |
| 26 | check below | a dead link into `templates/` |
| 27 | `test_no_workflow_text_asks_for_a_marking[file]`, `test_the_marking_template_is_gone`; check below | one of the five strings, or the file present; the diff not #60's |
| 28 | `test_workflow_note_names_neither_template` | a path between "Not all of it is here yet" and "One thing is missing" |
| 29 | check below; `tests/test_kit.py` | fewer than four lines; a kit test red |
| 30, 31 | the verification | `VERIFY RED`; the Leerprobe below 356 or a red case of the new test |
| 32 | review; check below | German in the new lines |

```bash
python3 -m pytest tests/test_templates.py tests/test_kit.py -q  # 1–16, 18–25, 27–29: passed
for s in '| Reviewer | Status | Broke a test |' 'Broke a test | Phase 6 |' 'taken — <test or criterion>' 'Reviewer session: codex <id>' 'Phase 6 verdict: <reviewer> <session>, <date>' 'leak check clean over <n> files, <n> commits, <n> rules.' '## Phase 4b — GLM loop rows, released' 'Rounds run: <n>' 'Loop rows: none — the GLM loop did not run for this change.'; do grep -qF -- "$s" templates/findings.md || echo "missing: $s"; done  # 17: nothing
git show origin/feat/stage-2-codex-glm:scripts/stage2.py | grep -nE '^(ROW_COLUMNS|RELEASED_COLUMNS|RELEASE_HEADING|NO_LOOP_LINE) ='  # 17: as quoted in step 2 (lines 118–134 at ef7407c)
python3 scripts/check_docs.py | grep 'templates/'  # 26: nothing
diff <(git diff origin/main -- prompts/03-plan.md | tail -n +5) <(git diff origin/main...origin/feat/stage-2-codex-glm -- prompts/03-plan.md | tail -n +5)  # 27: nothing
python3 scripts/kit/probe.py --list | grep -cE 'templates/(spec|findings|adr)\.md|tests/test_templates\.py'  # 29: 4
git merge-base HEAD origin/main | cut -c1-7  # 31: f985698, else measure the probe at that commit first
grep -nE '[äöüßÄÖÜ]' templates/spec.md templates/findings.md templates/adr.md tests/test_templates.py  # 32: nothing
git diff --name-only origin/main...HEAD  # the Definition of Done's files and this change folder, nothing else
```

The verification's Leerprobe line reads 356 plus the new test's cases that do
not skip, of 387 plus all of its cases (the two `AGENTS.md` cases skip).

## Not touched

The spec's protected areas: prompt 02's "Required sections", prompt 06 (its
reference becomes true), `docs/WORKFLOW.md` beyond the opening note and the
§4 paragraph (§2's link becomes true; repair round 1 touched one sentence of the
paragraph after it, row 6-5), `AGENTS.md`, `docs/adr/`,
`decisions/`, `docs/architecture/`, `templates/handover.md` and
`gate-record.yaml`, other change folders, `.github/`, prompts 04 and 07, the
gate scripts and the export manifest. Also `scripts/kit/probe.py` — no entry
in `REIST_NICHT`: every new case carries or skips.

## Overlaps with open work

| File | Also changed by | When the second one merges |
|---|---|---|
| `plans/INDEX.md` | #60, #63 (translates its header), `adhd-frame` | take either side, then `python3 scripts/plans_registry.py --index` on the merged tree |
| `prompts/03-plan.md` | #60 (the same deletion), `adhd-frame` (card above `Required:`) | no conflict: identical hunk, and another hunk |
| `prompts/02-spec.md` | #60 (the criteria bullet, from line 15) | no conflict: this sentence stands after line 8 |
| `docs/WORKFLOW.md`, opening note | #60 | conflict: keep #60's text without `templates/findings.md` |
| `docs/WORKFLOW.md` §4 | #60 rewrites §4 | conflict: keep #60's §4, and replace "defined here because the findings template is not in this repository yet" with a pointer to `templates/findings.md` |
| `scripts/kit/manifest.yaml` | #60 (two rules elsewhere) | no conflict expected; if one comes, keep both |
| `templates/` | #62 (`handover.md`, `gate-record.yaml`) | no shared file |
| `scripts/plans_registry.py`, read by the test | #63 | none; names unchanged at `abe5508` |
| `tests/test_ci.py` | #64 | not touched here; no shared file |
| `AGENTS.md`, read by the test | #60, `adhd-frame` | not edited here; neither adds a `templates/` path or a marking string |

After #60 merges, the test's workflow-text cases include
`prompts/04b-review-loop.md` by the glob; it holds neither.

## Slice 2 — the design phase and the arc42 skeleton

```text
For you:     a design phase 2b — its prompt, its form with the Mermaid delta of ADR 0009, its rows in the workflow tables — and an arc42 skeleton in our own words
Done when:   the checks below hold criteria 33–65, `make verify` green, the Leerprobe not below 356 cases (merge base 3851f9c)
Appetite:    3 h 39 min of phase 4 for this slice — the change's 4 h less the 21 min slice 1 used; repair rounds included, a stop
Not now:     ROADMAP (its own change), LikeC4 (ADR 0009's upgrade path), a check that 2b ran (bead coding-harness-jc3), the kit's licence file
Pre-mortem:  suppose it failed: most likely because ADR 0009 merges with a delta form the design template did not foresee
Starts unless you say stop.
```

Implements criteria 33–65 of `spec.md` (amended 2026-10-05); criteria 30 and
31 hold over the whole pull request. Phase 4's spans go under "Time used" at
the end, after slice 1's. Facts read on 2026-10-05: this branch at `9945697`
(the merge of `origin/main` `3851f9c`), pull request #60 at `ef7407c`, ADR
0009's branch at `3851f9c` with no record yet, the research note of pull
request #69 at `3ed4c3b`.

### Decided in phase 3

No `[DECISION]` beyond the spec's open one, the arc42 skeleton's licence.

- `[DETAIL]` — **the skeleton comes last** (step 13), written for the
  recommendation of that `[DECISION]`. If no answer stands in `spec.md` when
  phase 4 reaches step 13, phase 4 stops there with its resumption line
  (prompt 04); everything else is built first.
- `[DETAIL]` — **the design prompt reads like prompt 02a**: the title, the
  bold lines Model, Input, Result and Gate, then four short parts — when the
  phase runs, what `design.md` holds (pointing to the template, not
  restating it), the ADR draft, from design to plan — and prompt 03's
  classify block. About 45 lines.
- `[DETAIL]` — **one list line per class, beginning with the class in
  backticks** (`` - `architectural` — always …``), so that the test of
  criterion 35 reads one line per class.
- `[DETAIL]` — **the Mermaid example has plain words in its labels**, no
  `<…>`: Mermaid labels take HTML, so an angle-bracket placeholder would
  vanish where GitHub renders it (finding 6-4). `flowchart LR` with
  `person["Person: who uses it"] --> app["Container: what changes"]`.
- `[DETAIL]` — **Added, Changed and Removed are bold labels** below the
  `mermaid` block, each with one `- ` item, like the findings template's
  reference lists.
- `[DETAIL]` — **the skeleton's header is a `docs/architecture/` file's**:
  the eleven keys of `docs/architecture/target-architecture.md` (`title`,
  `category: architecture`, `status`, `created`, `last_reviewed`, `updated`,
  `owner`, `provenance: ai-drafted-reviewed`, `produced_by`, `review`,
  `tags`); the copy goes where the instance keeps its architecture
  description, for example `docs/architecture/<system>.md`.
- `[DETAIL]` — **the credit's URLs stand bare**, not in angle brackets:
  GitHub links them, and an angle bracket in a template body reads as a
  placeholder (6-4).
- `[DETAIL]` — **the kit files stay below five phase words**: no
  "explore", "implement" or "review" in a new reason of
  `scripts/kit/manifest.yaml`, no "explore", "implement" or "verify" in the
  cap's comment in `scripts/kit/probe.py` (`research.md` §9, item 2).
- `[DETAIL]` — **the test reads a prompt's model with the regex of
  `tests/test_model_endpoints.py::prompt_modelle`**, copied rather than
  imported: importing a test module runs its collection-time reads.

### Steps

7. **Start** (5 min) — `git fetch origin`; if `origin/main` moved,
   `git merge origin/main` (no rebase; on a conflict in `plans/INDEX.md`,
   `python3 scripts/plans_registry.py --index`). If `docs/adr/0009-*.md` is
   on `origin/main`, read it: its words for the delta go into step 9, and
   where they contradict criteria 43–46, stop with prompt 04's four lines.
8. **`prompts/02b-design.md`** (20 min) — `# Phase 2b · Design`; Model:
   "Opus 5.5 — at effort `xhigh` (`claude --model claude-opus-5-5 --effort
   xhigh`); the same demand as spec and plan."; Input: `spec.md` as revised
   after 2a, `research.md`, `decisions.md`; Result:
   `plans/changes/<name>/design.md`; Gate: `python3
   scripts/plans_registry.py --check` green, and for an `architectural`
   change an ADR draft in `design.md`. Then a paragraph on what the phase
   decides (how the system is shaped, between what the spec says and how the
   plan builds it); "When this phase runs" — the D-14 lines of criterion 35
   and the sentence of 36; "Write `design.md` in the form of
   `templates/design.md`: copy it into the change folder and fill it in."
   (34); the ADR draft — the form of `templates/adr.md`, always for
   `architectural`, for a `feature` whose ADR answer is "yes"; it becomes
   `docs/adr/<NNNN>-<slug>.md` in the change's own pull request, which makes
   that pull request a decision pull request (37); the chosen alternative is
   a proposal, and the merge decides it (ADR 0008); "Phase 3 plans from
   `spec.md` and `design.md` and writes into `plan.md` what phase 4 needs
   from the design: phase 4 still reads `plan.md` and `spec.md` and nothing
   else." (38); prompt 03's classify block, a `[DECISION]` going back to
   `decisions.md`.
9. **`templates/design.md`** (25 min) — the leading comment (copy to
   `plans/changes/<change>/design.md`; the block becomes the header;
   placeholders in backticks, replaced with them; when a design is written:
   `prompts/02b-design.md`); the block — the keys of `templates/findings.md`'s
   block, with `title: "Design — <change>"` and `tags: [design, <topic>]`;
   `# Design — <change>` (the placeholder in backticks); a goal paragraph
   naming `spec.md`, `research.md` and `decisions.md`; the five sections of
   criterion 39. Alternatives: "at least two", each with its consequences
   for users, operations or risk, then "Chosen: …, because …" (40).
   Interfaces and Data model: what crosses a boundary or is stored, or the
   line `None — <one sentence why>` (41). ADR draft: the form of
   `templates/adr.md`, always for an `architectural` change, for a `feature`
   whose ADR answer is "yes", otherwise the None line (41, 42). Architecture
   delta: "the part of the system this change touches, as it is after the
   change", the `mermaid` block, the three labels, "If nothing architectural
   moves: one sentence why, in place of the diagram and the lists.", and
   "The form is ADR 0009's." (43–46), in ADR 0009's words where step 7 found
   it merged.
10. **The doctrine** (15 min) — the five insertions below, then the stamp of
    `docs/WORKFLOW.md`. Commit steps 8–10.
11. **The kit** (10 min) — `scripts/kit/manifest.yaml`, after the rule for
    `templates/adr.md`: `templates/design.md` ("the form of a design;
    prompts/02b-design.md names it") and `templates/arc42.md` ("a skeleton
    in arc42's sections, in this repository's words, with arc42's credit
    and licence"), both `mechanismus`; the reason of `tests/test_templates.py`
    becomes "holds the templates and the design phase's texts against the
    gate modules; skips a case whose file does not travel".
    `scripts/kit/probe.py`: after the `02a-spec-review.md` entry, the entry
    `[02b-design.md-Opus 5.5]` as `bestand-dieses-repos`; above `DECKEL` the
    comment "31 -> 32 on <date>: `prompts/02b-design.md` came along
    (plans/changes/template-bundle). A prompt with a model line is one case
    more, red in the throwaway repo for the reason the other prompt cases
    are: `model-endpoints.yaml` stays home."; `DECKEL = 32`, its trailing
    comment naming the earlier moves. Commit.
12. **Tests** (60 min) — in `tests/test_templates.py`: `NAMES` gains
    `design.md` and `arc42.md`; `header_problems` takes the file name the
    header is placed as (a keyword, `findings.md` by default), so that 48
    places it as `design.md`; helpers for a prompt's model, a table's first
    cells under a heading, and the text before a template's first `## `. The
    cases are the table below; the module docstring names criteria 1–65.
    Commit.
13. **`templates/arc42.md`** (30 min, after the licence answer) — the
    leading comment (where the copy goes; the block becomes the header;
    placeholders in backticks; the closing credit stays in every copy); the
    block of the `[DETAIL]` above; `# Architecture — <system>` (in
    backticks); the opening of criterion 58 — fill only what a named reader
    needs and say so in one line where a section has nothing, every number
    with its commit or date, what is not known marked open; the twelve
    sections of criterion 54 as `## 1. Introduction and Goals` to `## 12.
    Glossary`, each one to three sentences in this repository's words on
    what goes there and, where this repository has a place for it, a
    pointer: 5 to the form of ADR 0009's delta, 9 to `docs/adr/` (59); last,
    a paragraph "**Credit.**" with criterion 56's items and criterion 57's
    statement. Then the copy check of 55 below. Commit.
14. **Checks and close** (25 min) — the block below; `python3
    scripts/check_frontmatter_current.py --stamp`; `python3 -m ruff format
    scripts/ tests/`; `python3 scripts/plans_registry.py --index`; the
    verification; the trial merges; push. The last line is the `done:` line.

The five insertions of step 10, each a line or paragraph of its own:

```text
docs/WORKFLOW.md §2, after the 2a row:
| 2b | Design *(by class)* | `plans/changes/<name>/design.md` | validator green; for an `architectural` change, an ADR draft in it | [`02b-design.md`](../prompts/02b-design.md) |

docs/WORKFLOW.md §3, after the 2a row:
| 2b Design | **Opus 5.5** | effort `xhigh`; the same demand as spec and plan |

docs/WORKFLOW.md, "Change classes …", after the list of four classes:
**The design phase 2b goes by class** (decision D-14, `prompts/02b-design.md`): an `architectural` change always runs it; a `feature` runs it or says in one sentence of its `spec.md` why not; a `bounded` change and a `spike` never run it. Nothing checks this until the validator of bead coding-harness-jc3 lands; the review before the merge holds it.

AGENTS.md, "The workflow in one screen", after the 2a row:
| 2b | Design *(by class)* | `design.md` | validator green; an ADR draft when `architectural` |

templates/spec.md, appended to the Non-goals paragraph:
A `feature` without a `design.md` says here, in one sentence, why it does without the design phase 2b (`prompts/02b-design.md`).
```

Verification as in slice 1, verbatim:
`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify`,
ending `VERIFY GREEN`.

### Tests and checks per criterion (slice 2)

| # | Held by (`tests/test_templates.py` unless named) | Red when |
|---|---|---|
| — | `test_templates_carry_no_real_header[design.md]`, `[arc42.md]` | either starts with `---` |
| 33 | `tests/test_model_endpoints.py::test_every_model_in_a_phase_prompt_resolves[02b-design.md-Opus 5.5]`, by its glob | the model is not declared; no such case |
| 34 | `test_design_prompt_names_the_template` | `templates/design.md` absent from the prompt |
| 35 | `test_design_prompt_states_d14_for_each_class`; counter `test_d14_check_sees_a_new_class` | a class of `CLASSES` (read at call time) without its line, a line without its words; the counter: a planted class not reported |
| 36 | `test_design_prompt_says_nothing_checks_the_rule_yet`; review | no `coding-harness-jc3`; review: a gate named as checking it |
| 37 | `test_design_prompt_says_where_the_adr_draft_goes` | no `docs/adr/` or "decision pull request" |
| 38 | `test_design_prompt_hands_the_design_to_the_plan`; the file list | no paragraph with "Phase 3", `design.md`, `plan.md` and "phase 4"; prompt 03 or 04 changed for it |
| 39 | `test_design_sections_in_order` | a heading missing, renamed, added or moved |
| 40 | `test_alternatives_ask_for_two_with_consequences_and_a_choice` | "at least two", "consequence" or "Chosen" missing |
| 41 | `test_empty_parts_say_why[Interfaces]`, `[Data model]`, `[ADR draft]` | the section without a line beginning `None — ` |
| 42 | `test_adr_draft_takes_the_record_form` | `templates/adr.md` or `architectural` missing |
| 43 | `test_delta_is_a_mermaid_flowchart_after_the_change`; `test_no_likec4_model_is_asked` | no `mermaid` fence in the section, its first line not `flowchart …`, no "after the change"; "likec4" or ".c4" in the template or the prompt |
| 44 | `test_delta_lists_below_the_diagram` | **Added**, **Changed** or **Removed** missing after the fence |
| 45 | `test_delta_says_why_when_nothing_moves` | "nothing architectural moves" missing |
| 46 | `test_delta_names_adr_0009` | "ADR 0009" missing in the section |
| 47 | review; check below | the merged ADR asks for an element the section lacks, or the reverse |
| 48 | `test_filled_design_header_passes_the_plans_gates` | as 18, placed as `design.md` |
| 49 | `test_phase_table_has_2b_between_2a_and_3` | the first cells not …, 2a, 2b, 3, …; the row without `design.md` or `02b-design.md` |
| 50 | `test_routing_gives_2b_the_prompt_model` | no 2b row between 2a and 3; its bold model not the prompt's |
| 51 | `test_agents_table_has_2b_between_2a_and_3` | as 49 in `AGENTS.md`; skips without the file |
| 52 | `test_workflow_states_d14_by_class` | no paragraph of the section with `02b-design.md`, the four classes and `coding-harness-jc3` |
| 53 | `test_spec_template_says_where_a_feature_skips_design`; `test_spec_sections_in_order` | Non-goals without `design.md`, `feature` or "one sentence"; a new heading |
| 54 | `test_arc42_has_the_twelve_sections_in_order` | a title missing, renamed, added or moved, or a number not its position |
| 55 | check below; review | a run of eight words shared with arc42 outside the titles and the credit |
| 56 | `test_arc42_credits_arc42_in_the_copied_part` | "arc42", "9.0", "July 2025", "Gernot Starke", "Peter Hruschka", `https://arc42.org`, the licence URL or "changed" missing outside the leading comment |
| 57 | `test_arc42_states_its_licence` | "CC BY-SA 4.0" for the skeleton, or the sentence that a copy's content stays its author's, missing |
| 58 | `test_arc42_asks_only_what_a_reader_needs` | "reader", "commit or date" or "open" missing before the first `## ` |
| 59 | `test_arc42_decisions_point_to_the_records` | `docs/adr/` missing in section 9 |
| 60 | `test_filled_arc42_header_gives_a_date` | `read_updated` reads no date |
| 61 | check below; `tests/test_kit.py` | fewer than two; a kit test red |
| 62 | the verification (`probe.py --strict`); `tests/test_kit.py`; check below | the Leerprobe red; the cap not the list's length; more than one new entry |
| 63 | review; check below | German in the new lines |
| 64 | check below | a conflict in another file or hunk; a red template case on the resolved tree |
| 65 | check below | ADR 0009's merge commit not an ancestor of `HEAD` |

```bash
python3 -m pytest tests/test_templates.py tests/test_kit.py tests/test_model_endpoints.py -q  # 33–46, 48–54, 56–62: passed
python3 scripts/kit/probe.py --list | grep -cE 'templates/(design|arc42)\.md'  # 61: 2
git diff origin/main...HEAD -- scripts/kit/probe.py | grep -c '^+    "tests\.'  # 62: 1
git ls-tree --name-only origin/main docs/adr/ | grep '/0009-'  # 47: the record, read against 43-46
git merge-base --is-ancestor "$(git log origin/main --first-parent --format=%H -1 -- 'docs/adr/0009-*')" HEAD && echo ancestor  # 65: ancestor
git merge-tree --write-tree --name-only HEAD origin/feat/stage-2-codex-glm  # 64: conflicts in docs/WORKFLOW.md, plans/INDEX.md, scripts/kit/probe.py only
grep -nE '[äöüßÄÖÜ]' prompts/02b-design.md templates/design.md templates/arc42.md  # 63: nothing
git diff --name-only origin/main...HEAD  # the Definition of Done's files and this change folder, nothing else
```

For 55, a throwaway script, not kept: fetch the twelve section files of
arc42 9.0 with `gh api repos/arc42/arc42-template/contents/EN/adoc/<file>`
into the scratch directory, and compare every run of eight words of the
skeleton outside its headings and its credit with them; expected: none
shared. For 64, resolve the merged tree in a scratch copy as the overlap
table says and run `python3 -m pytest tests/test_templates.py` there. If the
head of #60 has moved from `ef7407c`, measure again and update the table
below before phase 6.

### Overlaps with open work (slice 2)

Measured with `git merge-file` on 2026-10-05 against #60's head `ef7407c`,
merge base `1e4cccf` (`research.md` §9, item 4).

| File | Also changed by | When the second one merges |
|---|---|---|
| `docs/WORKFLOW.md`, §3 routing table | #60 (rows 2a, 4, 6) | conflict: keep #60's rows, add the 2b row after its 2a row |
| `docs/WORKFLOW.md`, §2 table, "Change classes …" | #60 (the 4b row) | no conflict |
| `AGENTS.md` | #60 (the 4b row, a paragraph after the table) | no conflict |
| `scripts/kit/probe.py` | #60 (prompt entries renamed, 04b added, the cap) | two conflicts: keep #60's entries and add the 02b one; `DECKEL = 33`, with both comments |
| `scripts/kit/manifest.yaml` | #60 (two rules elsewhere) | no conflict |
| `plans/INDEX.md` | #60; ADR 0009 if it adds a change folder | regenerate on the merged tree |
| ADR 0009's branch | expected: `docs/adr/0009-*.md`, the continuity rows of D-15 and O-3, `AMENDMENT_ADRS`, the target's wording | no file of this change (expected, not measured: nothing was written on 2026-10-05); it merges first, and step 7 or 14 merges `origin/main` here; should it touch a file of this change, keep both sides and the ADR's words for the delta |

After #60 merges, its `prompts/04b-review-loop.md` joins the workflow-text
cases by the glob, its entries are the base of this change's one, and §3
routes 2a to Fable 5.1 while 2b stays on Opus 5.5.

### Not touched (slice 2)

Beyond slice 1's list: `README.md` (its one-line cycle; #60 did not add 4b
there either), `model-endpoints.yaml` (Opus 5.5 is declared), prompts 02
beyond slice 1's sentence, 03, 04 and 07 (criterion 38), `docs/architecture/`
and `docs/adr/` (ADR 0009's own pull request), `.claude/agents/` (no design
sub-agent), `scripts/export/manifest.yaml` (it carries `templates/`, so the
two new templates reach LakeSwitch — private, among the maintainer's own
repositories). Slice 1 left `scripts/kit/probe.py` alone; slice 2 adds the
one entry and the cap (criterion 62).

## Phase 7

The commit that opens the pull request sets `class: feature`, `change:
template-bundle` and `adr_question: {proposed: "no", reason: "<the spec's
option 2 reason>", answered_by: null}` in `spec.md` (spec, Open decisions,
step 2). The same commit stamps `updated:` in `spec.md`
(`python3 scripts/check_frontmatter_current.py --stamp`): it changes the header
on a day after 2026-09-30, and `frontmatter-current` compares `updated:` with
the committer date of the file's newest commit, so without the stamp a second
line is red beside `adr-answers` (finding 6-6). From then `make verify` is red
on exactly the one `adr-answers` line (30) and on no other; that is checked
before the push. The maintainer is back
and answers the ADR question in this phase; once the answer file
`decisions/answers/template-bundle/adr.yaml` lands in the pull request, the
pull request becomes a decision pull request (spec, Open decisions, step 3):
title `decide(template-bundle): …` instead of the title it opened with, label
`decision`, and the body from `.github/PULL_REQUEST_TEMPLATE/decision.md`.
The body lists the provisional answers — `decisions.md` 1–4, the
class with the 2a verdict `feature`, the appetite's scope — the overlaps
above, the special runs (26, 31) with their commit, and says no bead closes
yet: `Closes-Bead: coding-harness-9qo` follows only after the tracker writer
cuts the bead and opens the one for the not-now parts. If `adhd-frame` has
merged, "What could break": a spec copied before #60 merges shows
When / While / If as a recommendation only.

**Amended 2026-10-05 for the widened scope.** The class commit writes the
`adr_question` reason of the spec's amendment under "The class of this
change", not the earlier one. The same commit, under the one stamp, takes
finding 6-7 (the spec's protected-areas bullet names the sentence since the
amendment, so its Status moves to `fixed in <commit>`) and 6-8
(`implementation_status: partial` in `spec.md` and `plan.md`). Before the
pull request opens, ADR 0009 is merged and `origin/main` merged here
(criterion 65), and the trial merge with #60 is measured again (64). The
body gives the maintainer's answers of 2026-10-05 as answers, no longer as
provisional ones; the answer on the arc42 skeleton's licence and, under its
option 1, the exception for the kit's licence work (bead
coding-harness-lir); and the special runs of criteria 55, 64 and 65. The
closing trailer waits until the tracker writer has cut the bead to this
scope.

## Repair round 1

Origin `fix-r1`, 2026-10-05, on the six rows 6-1 to 6-6 of the phase-6 review
(`findings.md`, read at `e3f997e`; this round starts at `7e11f82`, with the
head of pull request #60 at `ef7407c`, of `adhd-frame` at `b4bb2cb` and of
`origin/main` at `f985698`, all fetched at the start). Five rows are fixed, in
`a3ede4a` (the wording of 6-1, 6-2, 6-4, 6-5) and `23eeff8` (the tests of
6-3 and a guard for 6-1). Row 6-6 is not repaired here, on purpose: its repair
is part of the class commit of phase 7, which this round must not make (the
class stays `bounded` until then); phase 7 above now carries it. The
decisions below are the coordinating session's `[DETAIL]`s. No reviewer has
read this round, and no row is marked reviewed.

- **6-1, the BLOCKER.** Line 59 of `templates/spec.md` reads "One condition
  per criterion, beginning the sentence with When, While or If, is
  recommended, not required: it becomes the rule once pull request #60 merges,
  and until then the rule is `prompts/02-spec.md`." — the reviewer's planted
  wording, which kept all 53 cases green, so the old test was no guard. The
  round adds one: `test_criterion_form_is_a_recommendation` also refuses
  "one condition" anywhere in the Acceptance criteria section unless the same
  sentence says "recommended" (the first fault of the table below planted the
  old wording back and turns it red). Criterion 8's refutation still marks the
  rest of the mandatory-form check as review.
- **6-2.** The stage-2 part of `templates/findings.md` shows the heading and
  `Rounds run: <n>` as the section of released rows, and the line `Loop rows:
  none — …` apart from it, "in place of the section, at the end of the file,
  without a heading", as the runner's `release` writes it (lines 740–750 of
  `scripts/stage2.py` at `ef7407c`, re-read). All strings the check of
  criterion 17 greps for are still in the file.
- **6-4.** Every placeholder of the body that stood bare in angle brackets
  now stands in backticks: 22 of them over the three templates (the headings,
  the example criterion, the findings opening, the ADR Status bullet, Review
  and Date lines, Decision Drivers, Considered Options, the Decision opening,
  Consequences, Validation). That includes `Reviewer session: ` with `<id>` in
  backticks, so the line of criterion 16 differs from the spec's wording by the
  backticks only (the test follows). Each copy instruction (item 1 of the
  leading comment) says to replace a placeholder, backticks included.
  Measured: `gh api markdown` (GFM) over the three files at `a3ede4a` shows
  every one of them; `markdownlint-cli2` v0.23.2 reports MD033 17 times on
  the three files at `7e11f82` and none at `a3ede4a`. Not changed: the leading
  comment, which GitHub does not show at all — it is an HTML comment on
  purpose, so that the copy instructions stay out of the copy; whoever copies
  the file opens the raw text — and the placeholders in the yaml blocks and
  `text` fences, which render as they stand.
- **6-5.** The paragraph after the removed one reads "The orchestrator —
  `scripts/run_change.sh`, not in this tree yet (see the note at the top) —
  holds **no second rule set**." A departure from the spec's protected areas,
  which allowed the §4 paragraph only: one sentence of the next paragraph, the
  only way to give the referent back (the departure is the coordinating
  session's `[DETAIL]`). Pull request #60 rewrites §4 anyway; the conflict of
  the trial merge stays where it was predicted. A header of its own was owed:
  `docs/WORKFLOW.md` is held by `frontmatter-current`, so `a3ede4a` alone leaves
  its `updated:` at 2026-09-30 and that one gate red on that commit (measured
  with `check_frontmatter_current.py`, which named the file); the commit with
  these records stamps it, and the tip is green.
- **6-3, tests that read the places.** `reference_lists` in
  `tests/test_templates.py` reads the reference part below the `---` line into
  its bold-labelled lists. `test_findings_vocabulary_is_here` needs each
  severity, dimension, origin and marker as an entry of its own list, the word
  "escalation" in the `fix-r<N>` entry, `BLOCKER` in the `[DIVERGENT]` entry
  and "new evidence" below the line;
  `test_status_values_include_the_spec_review_ones` needs `in spec` and
  `rejected — <reason>` as entries of the Status list. The case count is the
  same (53).

**Planted faults.** One fault at a time into the committed template, then
`python3 -m pytest tests/test_templates.py`, then the file restored (a
throwaway script, not kept; `git status` was clean afterwards). "Before" is
the test file of `a3ede4a` (the assertions of `e3f997e`), "after" the one of
`23eeff8`, both over the templates of `23eeff8`; every row of the table was
run, 2026-10-05 14:39–14:40. The clean tree passes 53 of 53 both times. The
first four are the reviewer's four survivors; the other rows are more of the
same kind, planted so that the tests are not only as tight as the four.

| # | Fault planted | Before | After: test that went red |
|---|---|---|---|
| 1 | delete the `MINOR` line of the Severity list | green | `test_findings_vocabulary_is_here` |
| 2 | delete the `SPEC` line of the Dimension list | green | `test_findings_vocabulary_is_here` |
| 3 | delete the `base` line of the Origin list | green | `test_findings_vocabulary_is_here` |
| 4 | delete `rejected — <reason>` from the Status list | green | `test_status_values_include_the_spec_review_ones` |
| 5 | delete `in spec` from the Status list | red | `test_status_values_include_the_spec_review_ones` |
| 6 | delete the `MAJOR` entry | red | `test_findings_vocabulary_is_here` |
| 7 | delete the `MAINT` entry | red | `test_findings_vocabulary_is_here` |
| 8 | delete the `BLOCKER` entry | green | `test_findings_vocabulary_is_here` |
| 9 | delete the `fix-r<N>` entry | red | `test_findings_vocabulary_is_here` |
| 10 | delete the `[AMBIGUITY]` entry | green | `test_findings_vocabulary_is_here` |
| 11 | delete the `[DIVERGENT]` entry | red | `test_findings_vocabulary_is_here` |
| 12 | take "escalation" out of the `fix-r<N>` entry | red | `test_findings_vocabulary_is_here` |
| 13 | take `BLOCKER` out of the `[DIVERGENT]` entry | red | `test_findings_vocabulary_is_here` |
| 14 | delete the "new evidence" paragraph | red | `test_findings_vocabulary_is_here` |
| 15 | move the `MINOR` line from Severity into Origin | green | `test_findings_vocabulary_is_here` |
| 16 | move `rejected — <reason>` from Status into Origin | green | `test_status_values_include_the_spec_review_ones` |
| 17 | spec form line 59 back to "One condition per criterion. Beginning the sentence …" (6-1) | green | `test_criterion_form_is_a_recommendation` |

Seventeen faults: nine were green before, all seventeen are red after, each
in the test that is meant for it and in no other. The earlier build's "31 of
31" is still not recorded anywhere; this table is the first record.

**Verification** (2026-10-05, `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign
GIT_CONFIG_VALUE_0=false make verify`, on the tree of the commit that carries
this section, `a3ede4a` and `23eeff8` under it): `VERIFY GREEN`, 568 passed,
15 skipped, 42 s; the Leerprobe carries 407 of 438 cases, the same as before
the round, because the round adds no case (53 in `tests/test_templates.py`,
the two `AGENTS.md` cases skip there). On `a3ede4a` alone the one gate
`frontmatter-current` was red (see 6-5 above), not measured with `make
verify`. `git merge-tree --write-tree`, run on `23eeff8`: with
`origin/feat/stage-2-codex-glm` (`ef7407c`) conflicts only in `docs/WORKFLOW.md`
and `plans/INDEX.md`, as before (`prompts/02-spec.md` and
`scripts/kit/manifest.yaml` merge automatically); resolved as the overlap table
says (#60's two files, `templates/findings.md` struck from its opening note),
the merged tree passes 55 of 55 cases of `tests/test_templates.py`. With
`origin/docs/adhd-frame` (`b4bb2cb`): no conflict, 53 of 53 pass. The tests of
`tests/test_kit.py` were not run on those trees (an archive has no git).

## Time used

Phase 4 and its repair rounds, read with `date` (CEST); appetite 4 h.

- 2026-09-30 23:34–23:38, 4 min — steps 1–3, the three templates (reading the inputs included).
- 2026-09-30 23:38–23:40, 2 min — step 4, `tests/test_templates.py`.
- 2026-09-30 23:40–23:41, 1 min — step 5, the texts.
- 2026-09-30 23:41–23:44, 3 min — step 6, the checks and the verification, run twice (`VERIFY GREEN`: 568 passed, 15 skipped; Leerprobe 407 of 438).
- Total 2026-09-30 23:34:44–23:43:31, 9 min of 4 h (the commit and push follow within the minute); no repair round.
- Repair round 1, 2026-10-05 14:34–14:35, 1 min — reading `findings.md`, `plan.md` and how earlier rounds are recorded; fetching the heads (unchanged).
- 14:35–14:38, 3 min — the reviewer's survivors reproduced on `7e11f82`'s tests, 6-1 and 6-4 in the templates, `gh api markdown`.
- 14:38–14:39, 1 min — 6-2 and 6-5, the tests of 6-3, commits `a3ede4a` (14:39:11) and `23eeff8` (14:39:19).
- 14:39–14:40, 1 min — the seventeen planted faults, after and before.
- 14:40–14:46, 6 min — phase 7 text, the section above, the rows' Status, the stamp, `make verify` three times (14:43, 14:45, 14:46: the same counts each time), the trial merges, the 55 and 53 cases on the merged trees.
- Total 2026-10-05 14:34:40–14:47, 12 min of 4 h for the round (the commit and push follow within the minute); with the 9 min of the build, 21 min of 4 h.
