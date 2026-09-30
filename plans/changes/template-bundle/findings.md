---
title: "Findings — template-bundle"
category: findings
created: 2026-09-30
updated: 2026-09-30
status: draft
implementation_status: none
date: 2026-09-30
last_reviewed: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-9qo
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, spec-review, templates, change-class, appetite]
---

# Findings — template-bundle

Phase 2a, on commit `5d4aab2` (branch `docs/template-bundle`, three commits
over `origin/main` at `f985698`), 2026-09-30. The reviewer ran on Opus 5.5 in
a fresh context that never saw the author's reasoning, and read `spec.md`,
`research.md` (section 8 included) and `decisions.md`. Facts were re-read on
`main` at `f985698`, on pull request #60 (`origin/feat/stage-2-codex-glm`,
head `ef7407c`) and on the parallel change `adhd-frame`
(`origin/docs/adhd-frame`, head `ac30a69`, which now carries a spec). The
answers of `decisions.md` are provisional (the maintainer is away until
2026-10-04) and bind the spec as provisional; they were checked for how the
spec carries them, not reopened.

**Verdict: no BLOCKER, one `[AMBIGUITY]`, no `[DIVERGENT]`.** Two MAJOR, six
MINOR. The first MAJOR is the class: measured against the definitions on
`main`, this change is a `feature`, not `bounded` (2a-1). The second is the
`[AMBIGUITY]`: "appetite" means the whole change here and phase 4 in
`adhd-frame` (2a-2).

The orchestrating session asked this reviewer to work the rows into
`spec.md` as well, in place of the spec's author (`prompts/02-spec.md`,
"After the spec review"). Every row is taken; each Status says how. The
class stays the maintainer's decision at the merge; the `[AMBIGUITY]` has a
provisional answer in the spec so that none stays open while the maintainer
is away, and the maintainer settles it at the merge.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| 2a-1 | MAJOR | SPEC | base | `spec.md`, header `class: bounded`; "Open decisions", `[DECISION]` "The class of this change" | The class is `feature`, measured against `docs/WORKFLOW.md` §2 on `main`, "Change classes". (1) Option 2 quotes `feature` as "changes what the system must do" and drops the rest of the definition, "or how it is checked". This change sets how every later change is checked: prompt 02 will name the template as the form of every spec (criterion 12), and the template adds a Definition of Done, Protected areas and `appetite`, which no spec carries today (`research.md` §1.3). (2) `bounded` is "without deciding anything new", and the change decides, provisionally: the four answers of `decisions.md`, D-2's failure mode read as the refutations, protected areas read as "must not touch" rather than the ticket schema's "needs a person's approval", an `appetite` for every class, and the retirement of plan markings on `main`. That all of it writes down decisions of 2026-09-16 and practice argues for the ADR answer "no" — a feature's answer, as `frontmatter-current` and `omnigent-deny-layers` got — not for a lower class. (3) The recommendation rests partly on the gate: with `bounded`, "`make verify` stays green, so phases 3 to 7 can run while the maintainer is away". A class chosen by what it costs is the misclassification the one-way ratchet exists against (`docs/research/arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md` §8.2 and ADR-06, "too simple to need approval"), and classing down settles the ADR answer without the maintainer (`plans/changes/harness-decide-adr/spec.md`, "classes upward where the text is silent"). (4) The goal line says the class decides the ADR question only; on pull request #60 it also picks the reviewer of phases 2a and 6 (Fable 5.1 for `bounded`, Codex for `feature`). Verdict: `feature`, with `adr_question.proposed: "no"`. The maintainer decides at the merge. | in spec — the `[DECISION]` quotes the definition in full and records this verdict and a path that needs the maintainer only at the end: phases 3 to 6 run under the provisional `bounded`; the commit that opens the pull request sets `class: feature`, `change` and `adr_question`, and the pull request is then red on exactly one line of `adr-answers` until the maintainer answers, as the spec of pull request #54 prescribed; the answer file then lands in this pull request, which becomes a decision pull request (the one exception to the protected area `decisions/answers/`); criterion 30 and the Definition of Done measure `verify` on the commit the maintainer merges |
| 2a-2 | MAJOR | SPEC | base | criterion 5; `[DETAIL]` "`appetite:` in the header"; `adhd-frame` `spec.md` at `ac30a69`, Terms "Appetite" and "Widens", `[DETAIL]` "The appetite bounds phase 4" | `[AMBIGUITY]` — "appetite" names two scopes. This spec: "the session hours the outcome is worth", for the whole change, after LakeSwitch's D-24. `adhd-frame`'s spec, written after `research.md` read that branch at `5bb3d58`: "the time the maintainer is willing to spend on phase 4 of a change; a stop, not an estimate", phase 4 and its repair rounds, not phases 5 to 7; and its plan card "widens the appetite when its `Appetite:` is larger than an appetite `decisions.md` or `spec.md` states". Reading (a), the whole change: a spec's `appetite: 4` covers plan, build, review and commit, and a card that gives phase 4 all four hours widens nothing. Reading (b), phase 4: the same line lets phase 4 alone run four hours before the stop. `decisions.md` chose the word "so the two do not name one concept twice"; as written they name two. | in spec — a new `[DECISION]` "The scope of the appetite" with both readings; provisional answer (b), phase 4, taken by phase 2a so that no `[AMBIGUITY]` stays open while the maintainer is away, because the stop of `adhd-frame` is the one text that acts on the number and (b) changes only this spec. Terms, criterion 5 and the `[DETAIL]` follow it. The maintainer settles it at the merge. |
| 2a-3 | MINOR | SPEC | base | criterion 5 against the `[DETAIL]` "`appetite:` in the header" ("No default number") | Criterion 5 asks the template's example header itself to carry a number greater than zero; the `[DETAIL]` says the template sets no default number. One template cannot do both: a literal `appetite: 4` is the default the `[DETAIL]` rules out, and a placeholder fails criterion 5's test. | in spec — criterion 5 holds the filled-in header, as criteria 3 and 18 do, and refutes a number as the template's own value |
| 2a-4 | MINOR | SPEC | base | criteria 3 and 18 | "The gates accept it" is tested against `plans_registry` and `check_adr_answers` only. A third blocking gate reads every header under `plans/`: `frontmatter-current` (`scripts/check_frontmatter_current.py`, `read_updated`; `provenance.yaml` gives `plans/` `frontmatter: required`) reports a spec or findings file without a readable `updated:` date. A template without `updated:` passes both criteria, and its first copy turns `make verify` red. | in spec — both criteria add that `check_frontmatter_current.read_updated` reads a date from the filled-in header, and their refutations name it |
| 2a-5 | MINOR | SPEC | base | criterion 15; `[DETAIL]` "The Status values" | The `[DETAIL]` says `open`, `fixed in <commit>`, `in spec` and `rejected — <reason>` "are what the four findings files and prompt 02 use". The files use two more (`research.md` §8, re-read): `answered` (the three 2a rows of `harness-decide-adr`) and `resolved <date> by <source>` (F-1 of `omnigent-deny-layers`); pull request #60 adds `taken — <test or criterion>` for loop rows (its `docs/WORKFLOW.md` §4, "The review loop"). Whether the template's list is closed is not said, so the builder decides it: closed, it calls two practised files wrong; open, the word "among" in criterion 15 is all a test can hold. | in spec — the `[DETAIL]` lists the six practised values as the values in use, not a closed set (a checked set is bead coding-harness-4me's), and criterion 17 names `taken — …` with the stage-2 columns |
| 2a-6 | MINOR | SPEC | base | criterion 17; Terms, "Stage-2 columns and lines" | The list of what stage 2 adds to `findings.md` is shorter than what the runner writes. `scripts/stage2.py` on pull request #60 also writes the section `## Phase 4b — GLM loop rows, released <date>` with the line `Rounds run: <n>` (`RELEASE_HEADING`, `ROUNDS_LINE`), or the line `Loop rows: none — the GLM loop did not run for this change.` (`NO_LOOP_LINE`); and the `Stage-2 call, …` line the criterion names has no form its refutation holds (the f-string in `stage2.py`, line 446). A template that names "what a change that runs stage 2 adds" without them is contradicted by the first stage-2 findings file. Pull request #60's head moved to `ef7407c` (a findings commit); `stage2.py` is unchanged since `bd39160`. | in spec — criterion 17 and Terms name the section, the two lines and the call line's form, and the refutation holds them against `stage2.py` at `ef7407c` |
| 2a-7 | MINOR | SPEC | base | criteria 8, 9, 27, 31 | Parts of four criteria cannot go red with the refutation given. 8: "points to `prompts/02-spec.md`" and "saying that it becomes the rule with pull request #60" — the refutation catches only a mandatory When / While / If. 9: "each with its reason" — the test looks for "must not touch" and the single line. 27: "goes exactly as pull request #60 removes it" — the five-string test stays green on a removal that takes a line more or leaves one. 31: the floor is 356 at `eee26ae`; if `main` moves first (pull request #60 adds its own tests and raises the probe's cap), a case this change loses hides under the new ones. | in spec — each refutation names the missing case: the path and "#60" (8), "reason" (9), the diff of `prompts/03-plan.md` against `origin/main` being exactly the eight lines #60 removes (27), and the count on the merge base with `origin/main` as the floor (31) |
| 2a-8 | MINOR | SPEC | base | criterion 31 with criteria 25 and 27; `scripts/kit/manifest.yaml`; `scripts/kit/probe.py`, `_faelle` | The new test must carry in the Leerprobe with no red case, but criteria 25 and 27 read `AGENTS.md`, which the kit manifest classes `bestand`, so the probe's throwaway repository lacks it. A case that reads it is red there, and the spec is silent on how it carries. The probe counts a skipped case neither way. | in spec — criterion 31 says that a case reading a file the kit does not carry skips where that file is absent |

Reviewer session: none — phase 2a ran as a sub-agent (Opus 5.5,
`claude-opus-5-5`) of the orchestrating session, without an id a later
session can resume; phase 6 starts a fresh session and says so here.

## Checked without a finding

- **The answers of `decisions.md` in the spec.** Answer 1 (contract core):
  criteria 1–29 build the three templates, retire plan markings and repair
  the links; the design phase, ROADMAP, arc42 and LikeC4 stand on the
  not-now list, each with its trigger, and the re-scoping is left to the
  tracker writer. Answer 2 (the practised table): criteria 13 and 17.
  Answer 3 (failure mode and protected areas): criteria 6, 9 and 11, and no
  failure-mode section. Answer 4 (D-15 stays): Non-goals, twice. Q5 not
  asked. The orchestrator's details: criteria 7 and 8 keep When / While / If
  a recommendation; the word "appetite" is kept (its meaning: 2a-2).
- **The criteria that name code on `main`** (`f985698`): `REQUIRED`,
  `STATUS` and `IMPLEMENTATION` in `scripts/plans_registry.py`; `CLASSES`
  and `QUESTION_KEYS` in `scripts/check_adr_answers.py`, whose `examine()`
  returns a filled-in feature header in a tree without its answer file as
  exactly one missing answer, so criterion 3 can go red both ways; `pytest`
  is a gate id in `decisions/gates.yaml` and `verify` is none, so criterion
  10's planted line is caught and its one line is not; `AMENDMENT_ADRS`,
  `.github/PULL_REQUEST_TEMPLATE/decision.md`, `probe.py --list` and the
  `Closes-Bead` trailer of prompt 07 exist.
- **Criteria 19, 21 and 24 against `docs/adr/`.** Six of the seven ADRs
  carry Context, Decision Drivers, Considered Options, Decision,
  Consequences and Validation in that order; ADR 0004 has the first five
  and a section of its own. ADR 0008's header has the eleven fields
  criterion 24 lists, and its first bullet is the merge sentence.
- **Criteria 26 and 27 against the protected areas.** `check_docs.py` on
  `5d4aab2` reports exactly two dead links into `templates/`, both in
  `docs/WORKFLOW.md`, so criterion 26 is reachable without touching
  `docs/architecture/`. The five plan-marking strings stand on `main` only
  in the WORKFLOW opening note, the plan-marking paragraph of §4 and the
  section of prompt 03 — all inside what this change may edit.
- **Pull request #60** (`ef7407c`): its hunk in `prompts/03-plan.md` is the
  section this change removes; in `prompts/02-spec.md` it edits only the
  acceptance-criteria bullet, which is protected here; in
  `prompts/06-review.md` it rewrites the paragraph naming the findings
  template, also protected; its kit-manifest lines stand elsewhere in the
  file. Nothing else collides beyond 2a-6.
- **`adhd-frame`** (`ac30a69`): it edits prompts 03 (a card above
  `Required:`), 04 and 07, the two pull-request templates, the handover
  skill and a hook; of this change's edit set it shares only prompt 03, in
  another hunk. The one collision is the meaning of "appetite" (2a-2).
- **Scope against the 3.5–4.5-hour core.** The spec builds the core's parts
  and nothing from the not-now list. Its test surface — about 25
  test-held criteria in one file — is larger than research's "test 40
  lines" for the spec template alone; that is a risk for the plan's card
  and the appetite of 4 hours, not a widening of scope.

## Not checked

- MADR 4.0.0's own text: `research.md` §8, gap 1, is taken as read.
- lakeswitch-ai: not read in this phase; its D-24 and D-58 are cited from
  `research.md`.
- `make verify` of the future build: phase 4.
