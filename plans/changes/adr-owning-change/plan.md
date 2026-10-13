---
title: "Plan — adr-owning-change"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-afa
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, gates, interview-minimums, adr, kit]
---

# Plan — adr-owning-change

```text
For you:     an ADR edit counts for the change that lists the file under `adr_files` in its spec header, never for the other plans the same pull request touches; a "yes" without a claimed ADR file, or a "no" with one, turns verify red; the interview gate travels with the kit, and each repository records once the day it adopted it
Done when:   criteria 1–24 hold — the gate finds nothing over this repository at the head with ADR 0014 and ADR 0013 claimed, the empty-repository probe is green without a new exemption — and `make verify` ends VERIFY GREEN
Appetite:    6 h of phase 4, one repair round included; a stop, not an estimate
Not now:     claims for ADRs 0001–0012, a check that a claimed file exists, the criterion-ledger gate reading the record (bead coding-harness-wpv), any change to the ADR or answer format
Pre-mortem:  suppose it failed: most likely because one of the sixteen ADR fixtures moved to claims goes red for "unclaimed" instead of the five-record finding it was written for, and the suite stays green while that criterion is unheld
Starts unless you say stop.
```

Implements `spec.md` (criteria 1–24) with `design.md` (the adoption record and
the ADR 0014 draft). Facts read on 2026-10-12 at `d3b086f` of this branch and
at `7f53552` of pull request #126. Explore ran through the runner (route
flash, `glm-5.3-flash`; `research.md`), so no Stage-1 route is carried forward.

## Landing

1. **Pull request #126 merges first.** Phase 4 does not start before it is
   merged; if it closes unmerged, phase 4 stops and asks, because ADR 0014's
   number and criteria 23 and 24 depend on it.
2. Phase 4 opens with `git fetch origin && git merge origin/main` — a merge
   commit, never a rebase or a force push. The branch then holds #126's
   interim rule, its four tests, ADR 0013 and the gate `criterion-ledger`,
   which from then on holds this plan's ledger.
3. This change then removes the interim rule (step 2) and opens its own
   decision pull request; nothing of it lands before #126.

## Decided in phase 3

No `[DECISION]` is open. `[GAP]`s closed by reading, recorded in `research.md`,
"Corrections after verification":

- **The ledger of criterion-test-ledger names the four interim tests** under
  its criterion 24, so the commit that removes them edits those four lines
  (spec criterion 24): they become one entry naming the test that now holds
  the same case.
- **Sixteen existing tests stage an ADR**; without a claim each would go red
  for "unclaimed", and two of them (`test_unstaged_adr_path_is_seen`,
  `test_committed_adr_path_is_seen`) assert only the exit code — they would
  pass vacuously. Each gets a claim, and each that expects the five-record
  finding asserts `of 5`.
- **`test_unmeasurable_tree_exits_three`** builds its own repository; without
  an adoption record it would exit 3 for the record, not for the base. It
  writes the record and asserts the base's message.
- **One case reads a file that stays home** (`AGENTS.md`, in
  `test_workflow_and_agents_state_the_duty`): its `AGENTS.md` half skips when
  the file is absent, as `tests/test_templates.py` does.
- **The role of a path** comes from `scripts/kit/probe.py`, `rolle(pfad)`.

`[DETAIL]`s decided here: all findings of one run are collected, none returns
early; a header is parsed as YAML only when it has a line beginning
`adr_files:`, so stock headers are never parsed; the reader loads the record
with `check_adr_answers.strict_load`, which refuses a doubled key; test and
helper names as below.

## Files

- `scripts/check_interview_minimums.py` — changed: reads claims, attributes
  each ADR edit by claim, checks answer and claim, takes the day from the
  reader; `CUTOFF`, `_folders_named_by_adrs` and `plan_only` go; docstring and
  messages say "adoption day".
- `scripts/adoption.py` — new: the reader.
- `decisions/adoption.yaml` — new: this repository's record, as
  `design.md`, "Data model", shows it.
- `tests/test_check_interview_minimums.py` — changed: fixtures claim, four
  interim tests go, new tests as in the ledger.
- `tests/test_adoption.py` — new: the reader, the record's place in the kit
  and in `provenance.yaml`.
- `scripts/ci_gates.py` — one `OHNE_AUFRUFER` entry for `adoption.py`:
  "Library — reads the day a repository adopted a gate for the gates that
  exempt older changes; tests/test_adoption.py runs it".
- `scripts/kit/manifest.yaml` — five rules: `mechanismus` for
  `scripts/check_interview_minimums.py`, `scripts/adoption.py`,
  `tests/test_check_interview_minimums.py`, `tests/test_adoption.py`;
  `bestand` for `decisions/adoption.yaml` ("this repository's adoption days;
  another repository records its own (ADR 0014)").
- `provenance.yaml` — one `paths:` entry: prefix `decisions/adoption.yaml`,
  `allowed: [human-decided]`, `frontmatter: none`.
- `templates/spec.md` — after `adr_question`, the line
  `adr_files: []  # every class: the files under docs/adr/ this change creates, changes or removes`;
  comment item 2 says `adr_files` belongs to every class.
- `prompts/02-spec.md` — after the `adr_question` paragraph, one paragraph:
  every class lists under `adr_files` each file under `docs/adr/` it creates,
  changes or removes; the gate `interview-minimums` attributes an ADR edit to
  that claim alone and holds a feature's answer to it (ADR 0014).
- `docs/WORKFLOW.md` — §2, paragraph after the phase table: the cut-off
  sentence names the adoption record (this repository: 2026-10-08) and adds
  the claim; the "Interview" row of the tools table says the same; the
  classes section adds the agreement, and its last bullet becomes "Nothing
  checks that the class is right, that a claimed ADR file exists, or that a
  decision pull request carries its label and block."
- `docs/adr/0014-a-change-claims-its-adr-files.md` — new, the draft of
  `design.md`, dates set to the day it is written.
- `plans/changes/criterion-test-ledger/spec.md` — one header line,
  `adr_files: [docs/adr/0013-every-criterion-names-its-proof.md]`.
- `plans/changes/criterion-test-ledger/plan.md` — its four criterion-24 lines
  naming the interim tests become one (step 2).
- `plans/INDEX.md` — regenerated, `python3 scripts/plans_registry.py --index`.
- this `plan.md` — each `not yet written` dropped in the commit that writes
  its test (ADR 0013).

## The gate

`measure(root, only)` in this order:

1. `day = adoption.adopted_on(root, "interview-minimums")`; `NotRecorded`
   becomes `CannotMeasure` with the reader's message (exit 3).
2. `claims`: for every change folder with a spec, active and archived,
   `_claim(spec)` → `(paths, problem)`. No line beginning `adr_files:` → no
   claim. Otherwise the header block is matched with the gate's own copy of
   `check_adr_answers`' block regex and loaded with `check_adr_answers.strict_load`
   (not `read_header`: a spec without a `---` header block claims nothing, like
   one without `adr_files`, instead of being a problem here), and the value must be a list of distinct texts, each
   matching `docs/adr/` plus segments that are neither empty, `.` nor `..`.
   A problem is a finding: `<spec path>: adr_files cannot be read — <why>; the
   form is adr_files: [docs/adr/<file>, …]`.
3. `touched`: today's owner set — active folder names of the diff — renamed.
4. Per ADR path, sorted: `claimants = touched` folders whose claim lists it.
   None: `<path> changed, but no change in this diff claims it — list it under
   adr_files in the spec header of the change it belongs to, whose
   decisions.md carries five answers`. Two or more: `<path> is claimed by <a>,
   <b> in one diff — one change claims an edit; drop the other claims or
   split the pull request`. One: it joins `owners`.
5. Each owner owes five, as today (`(ADR change): N of 5`); the class loop
   skips owners, as today, and exempts `spec_date <= day`.
6. Agreement, over subject features (class `feature`, date unreadable or
   later than `day`, active or archived, the named one alone under
   `--change`), owners included: the answer is read with
   `check_adr_answers.answer_rel(name)` and `load_answer`; a missing file or
   one with problems is skipped. `answer == "yes"` and no claim: `<name>:
   answers yes to the ADR question but claims no ADR file — list it under
   adr_files, or correct the answer in a decision pull request`; `"no"` with
   claims: `<name>: answers no to the ADR question but claims <paths> —
   remove the claim, or correct the answer in a decision pull request`.

The ok line and the exempt line name `adoption day <day>` instead of
`cut-off`. `scripts/adoption.py`: `RECORD = "decisions/adoption.yaml"`,
`class NotRecorded(Exception)`, `adopted_on(root: Path, gate: str) -> date`;
it refuses a missing or unreadable file, invalid YAML or a doubled key, a
`schema_version` that is not the integer 1, an `adopted` that is not a
mapping, and a value for `gate` whose `type` is not `date`; each message
names the record's path and the line `  <gate>: YYYY-MM-DD` under `adopted:`.

## Steps

Each step ends with `make verify` green, then a commit and a push.

1. **The day.** `decisions/adoption.yaml`, `scripts/adoption.py`,
   `tests/test_adoption.py`, the `ci_gates.py` and `provenance.yaml` entries;
   the gate reads its day through the reader and `CUTOFF` goes. The `repo`
   fixture commits the record on `main` with its seed; the `lonely` tree of
   `test_unmeasurable_tree_exits_three` writes it too.
2. **The claim.** Steps 2 to 6 of "The gate"; `write_change(…, adr_files=…)`
   and an answer-file helper in the test file; the sixteen fixtures claim;
   the four interim tests go, and in the same commit the four criterion-24
   lines of `plans/changes/criterion-test-ledger/plan.md` become
   `- 24: tests/test_check_interview_minimums.py::test_a_claimant_beside_unclaiming_folders_is_decided_by_its_own_records`;
   the claim line in criterion-test-ledger's spec.
3. **Travel.** The five manifest rules; the `AGENTS.md` half skips when the
   file is absent; `python3 scripts/kit/probe.py --strict` green with
   `REIST_NICHT` and `DECKEL` unchanged.
4. **Texts and the ADR.** `templates/spec.md`, `prompts/02-spec.md`,
   `docs/WORKFLOW.md`, `docs/adr/0014-a-change-claims-its-adr-files.md`,
   `plans/INDEX.md`; the gate now sees ADR 0014, claimed by this change.

## Verification

```bash
.venv/bin/python -m pytest tests/test_check_interview_minimums.py tests/test_adoption.py -q
.venv/bin/python scripts/check_interview_minimums.py
.venv/bin/python scripts/check_interview_minimums.py --change adr-owning-change
.venv/bin/python scripts/check_criterion_ledger.py
.venv/bin/python scripts/kit/probe.py --strict
make verify
```

The second line's output at the head goes into the pull request body
(criterion 23).

## Not touched

`scripts/check_adr_answers.py`, `scripts/harness.py` and their tests (Q-1);
`scripts/check_criterion_ledger.py` (bead coding-harness-wpv);
`decisions/gates.yaml` and `.github/workflows/ci.yml` — the entry's command
does not change; `scripts/check_decision_continuity.py` — ADR 0014 amends no
D- or O-number (`research.md`, "Corrections after verification");
`scripts/kit/probe.py`; `AGENTS.md`; `prompts/01a-interview.md`;
`docs/adr/0001` to `0013`.

## Criterion ledger

- 1: tests/test_check_interview_minimums.py::test_a_claim_in_flow_or_block_form_names_the_owner
  — a block-style list read as no claim; a path under another key taken as one
- 2: tests/test_check_interview_minimums.py::test_an_unreadable_claim_is_reported
  — any of the five bad forms, or one in an archived stock spec, exits 0
- 3: tests/test_check_interview_minimums.py::test_adr_change_demands_five_regardless_of_class
  — a bounded claimant with four records exits 0
- 3: tests/test_check_interview_minimums.py::test_adr_edit_in_a_stock_folder_still_owes_five
  — the adoption day exempting a claimant dated before it
- 4: tests/test_check_interview_minimums.py::test_the_gate_goes_red_when_an_adr_edit_is_unclaimed
  — one touched folder that does not claim the edit taken as its owner again; a message without `adr_files`
- 4: tests/test_check_interview_minimums.py::test_a_claim_outside_the_diff_does_not_own_the_edit
  — an active change outside the diff, or an archived one, taken as the claimant
- 4: tests/test_check_interview_minimums.py::test_adr_outside_any_change_is_a_finding
  — a diff touching no change folder exits 0, or its finding lacks the path
- 5: tests/test_check_interview_minimums.py::test_adr_with_two_owning_changes_is_a_finding
  — two claimants with five records each exit 0
- 6: tests/test_check_interview_minimums.py::test_a_claimant_beside_unclaiming_folders_is_decided_by_its_own_records
  — a finding naming one of four plan-only folders beside a claimant with five; green with four
- 6: tests/test_check_interview_minimums.py::test_a_claimant_touched_through_plan_md_alone_owns_its_edit
  — a claimant touched only through plan.md reported unclaimed
- 7: tests/test_check_interview_minimums.py::test_each_claimant_owes_its_own_five
  — one claimant with five and another with four exits 0
- 8: tests/test_check_interview_minimums.py::test_the_adr_text_does_not_decide_the_owner
  — an ADR naming an unclaiming touched folder changes the verdict
- 9: tests/test_check_interview_minimums.py::test_a_yes_answer_without_a_claim_is_reported
  — a subject yes-feature without `adr_files`, or with `[]`, exits 0
- 10: tests/test_check_interview_minimums.py::test_a_no_answer_with_a_claim_is_reported
  — a subject no-feature claiming a path exits 0
- 11: tests/test_check_interview_minimums.py::test_the_agreement_holds_subject_features_alone
  — a feature dated on the day, a bounded claimant or another change under `--change` reported; an archived subject feature exempted
- 12: tests/test_check_interview_minimums.py::test_a_missing_or_refused_answer_is_left_to_adr_answers
  — a finding of this gate for a missing answer file or an unquoted `answer: yes`
- 13: tests/test_check_interview_minimums.py::test_the_adoption_day_comes_from_the_record
  — with the day moved to 2026-10-10, a feature dated 2026-10-09 still reported
- 14: tests/test_check_interview_minimums.py::test_a_missing_adoption_record_is_not_measured
  — exit 0 or 1 without the record; a message without its path
- 14: tests/test_adoption.py::test_the_reader_refuses_a_record_it_cannot_read
  — a missing file, invalid YAML, `schema_version: 2`, a quoted day, a missing key or a doubled key accepted
- 15: tests/test_adoption.py::test_the_reader_returns_each_gates_own_day
  — another gate's id answered with the interview day, or a record with two gates refused
- 16: tests/test_this_repository_adoption.py::test_this_repository_adopted_the_gate_on_2026_10_08
  — another day in this repository's record; the case stays home, in a file no manifest rule lets travel
- 16: not a test — the gate's run over this repository at the head, under "Verification": no stock change reported
- 17: tests/test_adoption.py::test_the_gate_and_its_reader_travel_and_the_record_stays
  — one of the four files left to a catch-all `bestand`, or the record `mechanismus`
- 18: not a test — the gate `leerprobe` in `make verify`, with `REIST_NICHT` and `DECKEL` unchanged in the diff
- 19: tests/test_adoption.py::test_the_adoption_record_is_human_decided
  — no `paths:` entry for the record, or one allowing another class
- 20: tests/test_check_interview_minimums.py::test_the_spec_template_and_prompt_name_the_claim
  — the template line missing or reported by the claim reader; the prompt without `adr_files`
- 21: tests/test_check_interview_minimums.py::test_the_workflow_states_the_claim_and_the_adoption_record
  — `adr_files`, `decisions/adoption.yaml` or ADR 0014 missing; the old "yes is followed by an ADR" sentence still there
- 22: not a test — the phase-6 review reads `docs/adr/0014-a-change-claims-its-adr-files.md` against the draft in `design.md`; the gate `decision-continuity` stays green
- 23: not a test — the gate's run over this repository at the head, under "Verification"; its output in the pull request body
- 24: not a test — the gate `criterion-ledger` in `make verify` reports a ledger line that names a removed test

## Runner route — 2026-10-13

Stage-1 route: implement · model claude-sonnet-5-5 · reason: Claude Code 2.1.296 refused glm-5.3-flash as an unrecognized model twice on 2026-10-13 (bead coding-harness-3fc).

## Runner route — 2026-10-13

Stage-1 route: repair · model claude-sonnet-5-5 · reason: Claude Code 2.1.296 refused glm-5.3 as an unrecognized model on 2026-10-13 (bead coding-harness-3fc).

## Runner route — 2026-10-13

Stage-1 route: repair · model claude-sonnet-5-5 · reason: Claude Code 2.1.296 refused glm-5.3(-flash) as an unrecognized model before any call (bead coding-harness-6th).

## Time used

2026-10-13 — review-loop round 2 repair (L2-1 to L2-4) under the Stage-2
runner; no command tool, so no wall-clock reading.

2026-10-13 span not measured — this session had file tools and no command tool, so `date` could not be read at start or end; the runner's own timestamps for this call are the record. Appetite not reached as far as the session could tell (6 h; no reading exists).


Phase 4, 2026-10-13: the Stage-2 route (GLM 5.3 Flash) was refused twice by Claude Code 2.1.296 as an unrecognized model, so Sonnet 5.5 implemented under `--stage2-off`; the orchestrator's sub-agent completed the `leerprobe` fix (the kit probe copies only git-tracked files, so the untracked `scripts/adoption.py` was missing in the foreign repository and collection of the interview-minimums tests aborted). No wall-clock reading exists.

2026-10-13 — review-loop round 1 repair (L1-1 to L1-3) under the Stage-2
runner, Sonnet 5.5 under `--stage2-off` (Claude Code 2.1.296 refused glm-5.3 as
an unrecognized model); no command tool, so no wall-clock reading. The case
asserting this repository's adoption day moved to a test file the kit does not
carry, the gate's docstring and the criterion-test-ledger plan prose were
corrected. The attempt failed only for this missing line; the orchestrator
added it and ran `make verify`.
