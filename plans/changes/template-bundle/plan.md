---
title: "Plan — template-bundle"
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
tags: [plan, templates, findings, adr]
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
| 8 | `test_criterion_form_is_a_recommendation`; review | no `prompts/02-spec.md`, no "#60" in the paragraph naming When/While/If; review: a sentence making it mandatory |
| 9 | `test_protected_areas_ask_what_must_not_be_touched` | "must not touch", "reason" or "None beyond the non-goals." missing |
| 10 | `test_done_names_the_gates_in_one_line`; counter `test_done_check_catches_a_planted_gate` | "`verify` green" not exactly once; an id from `decisions/gates.yaml` on another line; the planted "- `pytest` green." not reported |
| 11 | `test_done_asks_the_change_specific_items`; review | "same pull request", "protected areas", "non-goals", "Closes-Bead" or "special runs" missing; review: an every-change item |
| 12 | `test_spec_prompt_names_the_template` | the path absent from `prompts/02-spec.md` |
| 13 | `test_findings_table_has_the_practised_columns` | the first table's header row differs cell by cell |
| 14 | `test_findings_vocabulary_is_here` | one of the terms of criterion 14 missing, or no line with both `[DIVERGENT]` and `BLOCKER` |
| 15 | `test_status_values_include_the_spec_review_ones` | `in spec` or `rejected — <reason>` missing |
| 16 | `test_lines_under_the_table` | `Reviewer session: <id>`, either heading missing |
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
§4 paragraph (§2's link becomes true), `AGENTS.md`, `docs/adr/`,
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

## Phase 7

The commit that opens the pull request sets `class: feature`, `change:
template-bundle` and `adr_question: {proposed: "no", reason: "<the spec's
option 2 reason>", answered_by: null}` in `spec.md` (spec, Open decisions,
step 2); from then `make verify` is red on exactly the one `adr-answers`
line (30). The body lists the provisional answers — `decisions.md` 1–4, the
class with the 2a verdict `feature`, the appetite's scope — the overlaps
above, the special runs (26, 31) with their commit, and says no bead closes
yet: `Closes-Bead: coding-harness-9qo` follows only after the tracker writer
cuts the bead and opens the one for the not-now parts. If `adhd-frame` has
merged, "What could break": a spec copied before #60 merges shows
When / While / If as a recommendation only.

## Time used

None yet.
