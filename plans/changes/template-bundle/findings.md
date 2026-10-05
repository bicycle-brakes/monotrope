---
title: "Findings — template-bundle"
category: findings
created: 2026-09-30
updated: 2026-10-05
status: draft
implementation_status: partial
date: 2026-09-30
last_reviewed: 2026-10-05
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

Phase 6, on commit `e3f997e` (branch `docs/template-bundle`, nine commits
over `origin/main` at `f985698`), read on 2026-10-05 by a fresh session
(Opus 5.5, see under the table) that never saw the author's reasoning and
wrote nothing but this file and the regenerated `plans/INDEX.md`. Measured
against the revised `spec.md` — criteria 1–32, the non-goals, the protected
areas and the Definition of Done — after checking that each 2a row arrived
in it as its Status says (all eight did). Facts were re-read on pull request
#60 (`origin/feat/stage-2-codex-glm`, `ef7407c`) and on `adhd-frame`
(`origin/docs/adhd-frame`, which moved from `1fc0038` to `b4bb2cb` during
this review); both were merged with this head in trial (`git merge-tree`).
Rows 6-1 to 6-6.

**Verdict (phase 6): one BLOCKER, no MAJOR, five MINOR; no `[AMBIGUITY]`,
no `[DIVERGENT]`.** The BLOCKER (6-1) is one sentence of the spec form that
states a rule `main`'s prompt 02 does not have; its repair is one sentence
and needs no test change (measured). The MINORs do not stop the change.

Repair round 1 (origin `fix-r1`, 2026-10-05, on `7e11f82`): 6-1 to 6-5 are
fixed, in `a3ede4a` (wording) and `23eeff8` (tests); 6-6 stays open until the
class commit of phase 7, and `plan.md`, "Phase 7", carries it. The reasons,
the planted faults with their results and the trial merges are in `plan.md`,
"Repair round 1". No reviewer has read the repair yet, and no row is marked
reviewed; a finding that a review of it opens is the second round in a row
of `fix-r` findings, which `docs/WORKFLOW.md` §2 makes an escalation to the
maintainer, not a third round.

Phase 6, round 2 — the repair read, on commit `4c1bf24`, 2026-10-05, by a
reviewer on Opus 5.5 in a fresh context that never saw the repairer's
reasoning and wrote nothing but this file. It read the repair diff
`7e11f82..4c1bf24` against rows 6-1 to 6-6 and the spec, replayed the first
review's four survivors and four of the seventeen recorded faults, ran `make
verify` on the head and on a trial merge with `origin/main` (`3851f9c`, which
has taken pull requests #62 to #68 since the merge base `f985698`, `adhd-frame`
among them), and merged the head in trial with pull request #60 (`ef7407c`).
**Verdict: 6-1 to 6-5 are closed; 6-6 stays open until phase 7; two new rows,
both MINOR — 6-7 of origin `fix-r1` (the departure from the protected areas
that 6-5's repair made is recorded in `plan.md` but not in the spec) and 6-8
of origin `base` (the five artefacts still say `implementation_status:
none`). No BLOCKER, no MAJOR, no `[AMBIGUITY]`, no `[DIVERGENT]`: nothing here
stops phase 7.** One correction to the paragraph above: a row this review
opens is the first round with rows of `fix-r` origin, not the second, because
every row before it is `base`. A second repair round that again produces rows
(`fix-r2`) is the escalation `docs/WORKFLOW.md` §2 names, not a third round —
as `adhd-frame` counted it (its `findings.md` on `main` at `3851f9c`).

Phase 6, slice 2 — the design phase 2b and the arc42 skeleton, on commit
`7ac9fc5` (range `b02b1be..7ac9fc5`, which holds a merge of `origin/main`
`87daf91` at `4b0b6f3`; main's own content was not reviewed), 2026-10-05, by
a reviewer on Opus 5.5 in a fresh context that never saw the builder's
reasoning and wrote nothing but this file. Measured against criteria 33–65
of `spec.md` (criterion 64 as amended in `7ac9fc5`), answers 1–9 of
`decisions.md`, ADR 0009 as merged on `origin/main` (`a847516`) and
`plan.md`'s slice 2 with its 74 recorded faults, of which nine were replayed
and six variants planted that a weak test could pass. arc42's English
sources (version 9.0-EN, July 2025) were read with `gh api` into the scratch
directory, not committed; pull request #60 was merged with this head in
trial (`ef7407c`, unchanged). Rows 6-9 to 6-15, origin `base` (built in
slice 2, no repair since; the vocabulary has no `build`).
**Verdict (slice 2): one BLOCKER, one MAJOR, five MINOR; no `[AMBIGUITY]`, no
`[DIVERGENT]`.** The BLOCKER (6-9) is one sentence of ADR 0009 that the
delta section does not ask for (criterion 47); the MAJOR (6-10) is that no
later phase's prompt reads `design.md`.

Phase 6, slice 2, round 2 — the repair read, on commit `a1fb864` (range
`33a8442..a1fb864`, seven commits), 2026-10-05, by a reviewer on Opus 5.5 in a
fresh context that never saw the repairer's reasoning and wrote nothing but
this file. It read the diff against rows 6-9 to 6-15, against `spec.md`
(criteria 33–65, criterion 64 as amended twice) and against ADR 0009 on
`origin/main` (`87daf91`, unchanged since the slice-2 review, as is #60 at
`ef7407c`); replayed fourteen of the sixteen faults that `plan.md` records for
the round and planted five variants of its own, each on a throwaway copy of the
head with the test file of `33a8442` beside the new one; and ran `make verify`
and the criterion-64 check of `plan.md` on the head. **Verdict: 6-9 and 6-11 to
6-15 are closed; 6-10 stays with the maintainer; one new row, MINOR, of origin
`fix-r2` — 6-16: the new box check of 6-12 reads no line whose first box id
begins with a Mermaid keyword, so a fault the file caught before the round
passes after it. No BLOCKER, no `[AMBIGUITY]`, no `[DIVERGENT]`. 6-16 follows
6-7 (`fix-r1`): two repair rounds in a row with rows of `fix-r` origin, which
`docs/WORKFLOW.md` §2 makes an escalation to the maintainer, not a third
round.**

Phase 6, round 3 — the read of repair round 3 and of the phase-7
preparation, on commit `6af6a07` (range `855eeb6..6af6a07`; `7afa516` merges
`origin/main` at `d5813ec`, whose own content was not reviewed), 2026-10-05,
by a reviewer on Opus 5.5 in a fresh context that never saw the repairer's
reasoning and wrote nothing but this file. The round is the maintainer's
(`decisions.md` answers 10–12): repair 6-16, fix 6-10 now, and the ADR answer
"no" with the class `feature`; with it came the class commit that 6-6 to 6-8
waited for. The review read the diff against those five rows, against
criteria 27, 38 and 64 as amended and against the Definition of Done;
replayed seven of the twenty faults that `plan.md` records and planted five
variants of its own on a `git archive` copy of the head, with the test file of
`855eeb6` beside the new one; ran `make verify` on the head and the plan's
checks for criteria 27, 64 and 65; and resolved the trial merge with pull
request #60 (`ef7407c`) as `plan.md` says and ran `tests/test_templates.py`
on it. **Verdict: 6-6, 6-7, 6-8, 6-10 and 6-16 are closed; two new rows, both
MINOR, of origin `fix-r3` — 6-17: the whole-word pattern no longer skips
`end;`, a valid way to close a Mermaid subgraph, so the box check goes red on
it (a false red, on a form the template does not use); 6-18: criteria 27, 38
and 64 were amended in the spec but not in `plan.md`'s rows and check lines,
and criterion 64 still names a file that its own note says has left the
difference. No BLOCKER, no open MAJOR, no `[AMBIGUITY]`, no `[DIVERGENT]`.
This is the third round in a row that produced rows of `fix-r` origin, so
both rows go to the maintainer, who may accept them as recorded.**

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
| 6-1 | BLOCKER | SPEC | base | `templates/spec.md`, line 59 | The spec form makes "one condition per criterion" a rule that `main` does not have. Line 59 opens the paragraph on the criterion form with the bare sentence "One condition per criterion."; only the sentence after it — beginning with When, While or If — is marked "recommended, not required". `main`'s `prompts/02-spec.md` asks for checkable sentences, each with what refutes it, and says nothing of one condition; "one condition each" is the text pull request #60 adds to that prompt (`git diff origin/main...origin/feat/stage-2-codex-glm -- prompts/02-spec.md`, at `ef7407c`), and `decisions.md` ("Details the orchestrator adds") names one condition and When / While / If together as the form that stays a recommendation until #60 merges. Case: a spec written on `main` today with the criterion "the gate refuses the header and names the field" meets prompt 02 and breaks the template's rule. `test_criterion_form_is_a_recommendation` reads only the path and "#60" in that paragraph, so it stays green. Planted on a copy of `e3f997e`, the wording "One condition per criterion, beginning the sentence with When, While or If, is recommended, not required: …" keeps all 53 cases of `tests/test_templates.py` green, so the repair is this one sentence. What should hold: one condition per criterion appears only as part of the recommendation. (criterion 8; spec `[DETAIL]` "The criterion form is recommended, not required") | fixed in a3ede4a and 23eeff8, reviewed at `4c1bf24`, closed — `templates/spec.md` line 59 now reads "One condition per criterion, beginning the sentence with When, While or If, is recommended, not required: …" (a3ede4a); `test_criterion_form_is_a_recommendation` also refuses "one condition" outside a sentence that says "recommended" (23eeff8), and planting the old wording back turns it red, where it was green before (`plan.md`, "Repair round 1", fault 17). Round 2: lines 61–63 at `4c1bf24` carry one condition only inside the recommendation, as `decisions.md` ("Details the orchestrator adds") has it; `main`'s `prompts/02-spec.md` at `3851f9c` still names no number of conditions; the old spec form under the tip's tests is red in this one test only. The guard reads the word, not its sense — "is required, not recommended" and an added "Each criterion holds a single condition." stay green — which criterion 8 leaves to review |
| 6-2 | MINOR | SPEC | base | `templates/findings.md`, lines 121–128 | The stage-2 part says the released loop rows "stand in a section of their own, and the section holds one of two lines", and shows the heading `## Phase 4b — GLM loop rows, released <date>` above both `Rounds run: <n>` and `Loop rows: none — the GLM loop did not run for this change.` The runner it quotes writes the no-loop line alone, without that heading: `scripts/stage2.py` on pull request #60 (`ef7407c`), function `release`, appends `NO_LOOP_LINE` only when neither that line nor the heading is in the file (lines 740–741), and writes the heading only together with released rows and `Rounds run:` (lines 747–750). Case: a person writing a stage-2 findings file from the template puts the heading over `Loop rows: none …`, a form the runner never writes, although the template says it shows the forms "as that pull request's runner `scripts/stage2.py` writes them". What should hold: the no-loop line stands in place of the section, not inside it. (criterion 17, "or in its place the line") | fixed in a3ede4a, reviewed at `4c1bf24`, closed — the stage-2 part shows the heading with `Rounds run: <n>` as the section of released rows, and the no-loop line apart from it, in place of the section, at the end of the file and without a heading, as `release` writes it; the strings of criterion 17's check are all still in the file. Round 2: re-read against `scripts/stage2.py` at `ef7407c` — `release` appends `NO_LOOP_LINE` alone through `append`, which adds at the end (lines 740–741, 291–297), and writes the heading only with the rows and `Rounds run:` (lines 747–754); the plan's criterion-17 `grep` finds every string |
| 6-3 | MINOR | SPEC | base | `tests/test_templates.py`, lines 271–292 | Two tests search the whole template for a word, so a definition or a listed value can go while the test stays green. Planted on a copy of `e3f997e` and run: deleting the definition line of `MINOR`, of `SPEC` or of `base` from the reference part keeps 53 of 53 cases green, because the example row `\| F-1 \| MINOR \| SPEC \| base \| …` still carries each word; deleting `rejected — <reason>` from the Status list keeps them green, because the stage-2 part still names it as the status of a loop row. Five other plants went red as they should (unquoted `adr_question.proposed`, a `leerprobe` line in the Definition of Done, `[SONNET]` in prompt 04, `Reviewer session: <id>` above the table, "Optional" removed from Terms). What should hold: removing a definition the template owes, or one of the two Status values, turns a test red. (criterion 14, "defines"; criterion 15, "Among the Status values the template lists") | fixed in 23eeff8, reviewed at `4c1bf24`, closed — the two tests read the reference part's lists (`reference_lists`): each term needs its own entry in its own list, and `in spec` and `rejected — <reason>` stand in the Status list. The reviewer's four survivors (the `MINOR`, `SPEC` and `base` lines; `rejected — <reason>` from the Status list) were green before and are red after, with thirteen more faults planted, each in the test meant for it (`plan.md`, "Repair round 1", faults 1–17). Round 2, replayed on copies of `7e11f82` and `4c1bf24` (2026-10-05 15:02): the four survivors and recorded faults 8 (`BLOCKER` entry deleted), 15 (`MINOR` moved into Origin) and 16 (`rejected — <reason>` moved into Origin) are green on `7e11f82`'s tree and red on the tip's, each in its one test (1 failed, 52 passed); fault 17 under 6-1; every copy restored and green afterwards |
| 6-4 | MINOR | MAINT | base | `templates/spec.md`, lines 63–64; `templates/findings.md`, lines 37–38; `templates/adr.md`, lines 45–46, 60, 64–65, 69 | Where a person reads a template on GitHub, part of the form disappears. GitHub's renderer (`gh api markdown`, GFM, run on 2026-10-05 over the three files at `e3f997e`) takes a prose placeholder in angle brackets for an HTML tag and drops it: the example criterion renders as "When , ." over "Refuted by: .", the findings opening as "Phase , on commit `<commit>`, …, read by .", and in the ADR template the amendment placeholder of the Status bullet, the bullets of Decision Drivers and Considered Options and `<justification>` render empty. The leading comment that says how to copy and fill each template is not shown there at all. The report-only markdownlint run inside `make verify` flags the same placeholders as inline HTML (MD033). Case: an ADR copied from the template whose author left the amendment placeholder unfilled shows a complete-looking Status bullet in the pull request's rendered view, and the reviewer does not see the gap. Placeholders in code spans and in the yaml blocks are unaffected, and so is an agent reading the raw file. What should hold: an unfilled placeholder stays visible where a person reads the file. (no criterion; the spec is silent on how a template renders) | fixed in a3ede4a, reviewed at `4c1bf24`, closed — 22 placeholders of the body stand in backticks, `Reviewer session: ` with `<id>` in backticks among them, and each copy instruction says to replace them, backticks included. `gh api markdown` shows every one; MD033 reports 17 on the three files at `7e11f82` and none at `a3ede4a`. Not changed: the leading comment, an HTML comment by design, which GitHub does not show (`plan.md`, "Repair round 1"). Round 2: counted 22; `markdownlint-cli2` v0.23.2, run locally, reports MD033 17 times on the three files at `7e11f82` and none at `4c1bf24` (the templates are the same blobs as at `a3ede4a`); not re-rendered through GitHub. Criterion 16 and the template do not disagree: the spec names the line's form, the template marks its placeholder by the convention its item 1 states, and the filled copy reads `Reviewer session: <uuid>` as `prompts/02a-spec-review.md` asks |
| 6-5 | MINOR | MAINT | base | `docs/WORKFLOW.md`, line 535 | With the plan-marking paragraph of §4 removed, the next paragraph's subject has no referent: "The orchestrator holds **no second rule set**" followed the paragraph that introduced `scripts/run_change.sh` as the program that runs plan segments, and nothing else in §4 says what "the orchestrator" is; the opening note names `scripts/run_change.sh` only as absent. A reader of §4 on `main` cannot tell which program the sentence binds. Pull request #60 replaces §4, so this lasts while this change is merged and #60 is not. (house rule 7 of `AGENTS.md`; the spec's protected areas allowed only the paragraph itself) | fixed in a3ede4a, reviewed at `4c1bf24`, closed — "The orchestrator — `scripts/run_change.sh`, not in this tree yet (see the note at the top) — holds **no second rule set**." One sentence beyond the spec's protected-area allowance (the §4 paragraph only), the coordinating session's `[DETAIL]`; #60 rewrites §4 anyway; the file's `updated:` stamp follows in the commit with these records. Round 2: the claim is true — `scripts/run_change.sh` is in no tree (`4c1bf24`, `origin/main` at `3851f9c`, #60 at `ef7407c`); the opening note lists it as absent (line 39); `main`'s removed paragraph named it as the program that runs the segments, and `docs/research/2026-09-16-review-corpus-vs-running-workflow.md` (line 124) gives it the same exit-2 pause the sentence states. The departure itself is 6-7 |
| 6-6 | MINOR | SPEC | base | `plan.md`, "Phase 7" (lines 228–240) | The commit that sets `class: feature` changes the header of `spec.md` on 2026-10-05 or later, while its `updated:` says 2026-09-30. The gate `frontmatter-current` compares `updated:` with the committer date of the file's newest commit (`scripts/check_frontmatter_current.py`, module docstring) and reports the file stale — a second red line beside the expected `adr-answers` line. The plan names `python3 scripts/check_frontmatter_current.py --stamp` only for phase 4 (step 6). What should hold: before the maintainer's answer, `make verify` is red on the one `adr-answers` line and nothing else. (criterion 30) | fixed in `6da39ee`, reviewed at `6af6a07`, closed — the class commit carries the stamp: `updated:` of `spec.md` already read 2026-10-05 (the amendments of that day set it), so `check_frontmatter_current.py --stamp` changed nothing and `check_frontmatter_current.py` reports every `updated:` current. The second red line the row feared does not occur: the answer file `decisions/answers/template-bundle/adr.yaml` (`95b1cf9`) is in the tree, and `make verify` is green (`plan.md`, "Repair round 3"). Review of the repair: at `6af6a07`, `frontmatter-current` holds 84 documents, every `updated:` current; `adr-answers` holds four features to their answer files, `template-bundle` among them, exit 0; `make verify` green. The answer commit precedes the class commit (both 23:11:30), so the branch never had the state the row was about — red on `adr-answers` alone — and it does not need it now |
| 6-7 | MINOR | SPEC | fix-r1 | `spec.md`, "Protected areas", third bullet, and "Definition of Done", third item; `docs/WORKFLOW.md`, lines 535–536 | The spec still forbids what the repair of 6-5 did, and the departure is recorded only in `plan.md` and this file. The spec says the change must not touch `docs/WORKFLOW.md` "beyond the opening note and the plan-marking paragraph of §4", and lists its exceptions in that same bullet; repair round 1 rewrote the first sentence of the next paragraph and recorded it as a `[DETAIL]` in `plan.md` ("Not touched", "Repair round 1") without adding it there. Case: in phase 7 the pull request body reports the Definition of Done item "The protected areas untouched … shown by the pull request's file list"; against the spec as written that item is false, and the file list cannot show it either way, because `docs/WORKFLOW.md` is in it for the allowed edits. In substance the departure is harmless, measured: the trial merge with #60 conflicts in the same two hunks of `docs/WORKFLOW.md` as before the round (the opening note; §4, where this side's part grows from four lines to five), and the spec's `[DETAIL]` "Overlaps with pull request #60" (keep #60's §4) resolves both unchanged. Not `[DIVERGENT]`: `plan.md` records a departure from the rule, not a competing rule. What should hold: the spec's bullet names this sentence as an exception, as it names its others, or the pull request body names the departure where it reports the Definition of Done. (Protected areas; Definition of Done, item 3) | fixed in `6da39ee`, reviewed at `6af6a07`, closed — the spec's third protected-areas bullet has named the sentence since `d68dd26`; Definition of Done item 3 now reads "apart from the departures they name themselves" and lists them (this sentence of §4, finding 6-7; the Input line of prompt 06 and one sentence of prompt 03, finding 6-10), shown by the file list and the pull request body. Review of the repair: each departure stands in its own protected-area bullet — §4's sentence in the `docs/WORKFLOW.md` bullet, the Input line in the `prompts/06-review.md` bullet, prompt 03's sentence in the `.github/` bullet — and the round's files (`git diff --name-only 7afa516..6af6a07`) are the five artefacts, `plans/INDEX.md`, prompts 03 and 06, `tests/test_templates.py` and the answer file, nothing beyond the allowances. The parenthesis of item 3 lists the departures of the repair rounds; the answer file is the exception planned from the start, which the `human-decided` bullet names |
| 6-8 | MINOR | MAINT | base | `spec.md`, `plan.md`, `research.md`, `decisions.md`, `findings.md`, header line `implementation_status: none` each; `plans/INDEX.md` | All five artefacts of the change say `implementation_status: none`, and the regenerated index lists the change as unbuilt, while the branch has carried the built templates, their test and the edited prompts since phase 4 (`e3f997e`). `plans/_README.md` says the field moves when the code moves; `harness-decide-adr` moved its spec and plan to `partial` after its phase 4 (`1964244`), and `adhd-frame`'s review held it to the same (its F-6, on `main`). Case: a reader of `plans/INDEX.md` on this branch, or after the merge, sees nothing of this change built. The row existed before repair round 1; the first phase-6 review missed it. What should hold: at least `spec.md` and `plan.md` say `partial`. (no criterion; the plans convention) | fixed in `6da39ee`, reviewed at `6af6a07`, closed — `implementation_status: partial` in all five artefacts of the change, as `adhd-frame`'s five are; `plans/INDEX.md` regenerated. `done` waits for the merge and the closed bead. Review of the repair: the five headers say `partial`, `plans/INDEX.md` lists all five as `partial`, and `plans-registry` is green |
| 6-9 | BLOCKER | SPEC | base | `templates/design.md`, lines 76–105 ("Architecture delta"); ADR 0009 on `origin/main` (`a847516`), lines 124–127 | The delta section lacks one thing ADR 0009 decides for it. The decision's second contract says: "Elements are named as the existing diagrams and ADRs name them, as in LakeSwitch's D-58" (lines 126–127). It is what the ADR puts in place of the single definition per element that a model as code would have given; its revisit trigger 2 (the same element in three or more pictures, renamed or split by hand, lines 145–146) and its agreement with D-58 ("names the touched elements as the existing diagrams and ADRs name them", lines 69–70) rest on it. Neither the section nor `prompts/02b-design.md` nor section 5 of `templates/arc42.md` asks for it (`grep -n "named as\|existing diagram"` over the three: nothing). Phase 4's review counterpart of criterion 47 (`plan.md`, "Verification (slice 2)") counted "three contracts" and did not see this one. Case: the first `architectural` change draws a box "Gate runner" for what the existing diagrams call the verify job; the template asked for nothing else, and the phase-6 reviewer has no line of the form to hold it against. The other reading — the sentence belongs to the contract "No model as code in the kit now" and binds no section — is rejected here: its subject is the elements, and the delta's lists are lists of elements and relationships. What should hold: the section asks that elements and relationships be named as the existing diagrams and ADRs name them; one sentence, which a test can hold by its words. (criterion 47, "an element ADR 0009 requires of the delta that the section lacks") | fixed in `c551836`, reviewed at `a1fb864`, closed — the Architecture delta section of `templates/design.md` says "Elements and relationships are named as the existing diagrams and ADRs name them, in the diagram and in the lists." between the diagram and the three lists; it leaves out "as in LakeSwitch's D-58", a decision of another repository that a copy of the template cannot look up. `test_delta_names_elements_as_the_existing_diagrams_do` holds the words; deleting the sentence, or naming another rule, was green before and is red after (`plan.md`, "Repair round 2", faults 11 and 12). Review of the repair: both faults replayed — green under the test file of `33a8442`, red in this one test under the new one. The omission is sound: in ADR 0009 "as in LakeSwitch's D-58" names the precedent, not something the section must ask, and the template names ADR 0009, which carries it — although the stated reason (a copy cannot look up another repository) would hold for "ADR 0009" too, which criterion 46 requires. "and relationships" asks nothing ADR 0009 does not: its lists are lists of elements and relationships, and this row asked for both |
| 6-10 | MAJOR | MAINT | base | `prompts/02b-design.md`, lines 40–44; `prompts/03-plan.md`, lines 7–8; `prompts/06-review.md`, line 6; ADR 0009, lines 165–168 | No prompt of a later phase reads `design.md`. The handover to the plan is stated only in the design prompt ("Phase 3 plans from `spec.md` and `design.md` …"), which a phase-3 session does not read: prompt 03 says the next session needs `plan.md` and `spec.md` and names no input. Prompt 06's input is "the diff and `spec.md`", while ADR 0009 leaves the truth of the delta "the reviewer's question in phase 6". Case: the first `architectural` change runs 2b; a fresh phase-3 session started with prompt 03 plans from `spec.md`; phase 6 reviews the diff against `spec.md`; the chosen alternative and the delta are read by nobody after 2b, and no gate notices. The spec chose the route for phase 3 (criterion 38 and its `[DETAIL]` "The plan takes the design in by the design prompt") and is silent on phase 6; both prompts are protected here, and pull request #60 rewrites 06. Not a violation of the spec; a person decides — for example one input line each in prompts 03 and 06 once #60 has merged, as a bead of its own. (criterion 38; ADR 0009, Consequences) | fixed in `59ff6fe` and `6da39ee`, reviewed at `6af6a07`, closed — the maintainer decided on 2026-10-05 (`decisions.md`, answer 11): `prompts/03-plan.md` says in one sentence that the plan is made from `design.md` as well when the change has one; `prompts/06-review.md` names `design.md` on its Input line, with ADR 0009's question about the delta. The spec departs from its protected areas as it says (criteria 27, 38 and 64 amended, the two bullets, the Definition of Done). Two tests hold the sentences, seven faults planted (`plan.md`, "Repair round 3", faults 14–20). The trial merge with #60 gains one hunk in `prompts/06-review.md`, #60's Model lines against this Input line. Review of the repair: the prompt edits are minimal — in each prompt one line becomes three, nothing else (`git diff 7afa516..6af6a07 -- prompts/`). Prompt 03's sentence agrees with "From design to plan" of the design prompt and leaves phase 4 on `plan.md` and `spec.md`; prompt 06's question is ADR 0009's ("whether the delta is right stays the reviewer's question in phase 6", lines 165–168), read for the diff under review. Criteria 27 and 38 as amended hold: `git diff origin/main -- prompts/03-plan.md` shows the sentence and the eight lines #60 removes, nothing else. Faults 14, 17 and 19 replayed: green under the test file of `855eeb6`, red under the new one in the test the record names. On the resolved trial merge with #60, the Input line stands under #60's Model line and both tests pass. The plan's rows and check lines for 27, 38 and 64 were not amended with the criteria: 6-18 |
| 6-11 | MINOR | SPEC | base | `spec.md`, criterion 64 and its amendment (`7ac9fc5`); `plan.md`, "Stop — criterion 64 does not hold as written", the slice-2 check block (line 443) and "Verification (slice 2)" | The amendment is sound and, in substance, no goal-post move. Measured at `7ac9fc5` against #60 at `ef7407c`: `git merge-tree --write-tree --name-only` reports five files for this head and two for `origin/main` `87daf91` (the two architecture documents of 2026-09-17, which ADR 0009 and #60 both edit); the difference is exactly the three predicted files. The conflict hunks are those the criterion names (the opening note, the routing table of §3 and §4 of `docs/WORKFLOW.md`; the prompt entries and the cap of `scripts/kit/probe.py`; `plans/INDEX.md`), and the tree resolved as the spec's `[DETAIL]`s say passes 144 of 144 cases of `tests/test_templates.py`, `tests/test_kit.py` and `tests/test_model_endpoints.py`. Two loose ends: (1) the refutation went from "a conflict in another file or hunk" to "another file in that difference" — the hunk half was not part of the contradiction with criterion 65 and fell without a reason; (2) `plan.md` still records the stop as open ("Slice 2 stays open at this one criterion"; "criterion 64 is the stop above"), and its check line for 64 (`git merge-tree --write-tree --name-only HEAD origin/feat/stage-2-codex-glm  # 64: … only`) now prints five files. What should hold: the refutation keeps "or hunk"; `plan.md` records the amendment and the check as it now runs. (criterion 64) | fixed in `14ca394`, reviewed at `a1fb864`, closed — criterion 64's refutation keeps "or hunk" (a conflict hunk beyond the named ones in the three files, counted as conflict markers of the merged tree: 3, 2 and 1 at `8822677`); `plan.md` marks the stop as resolved by the amendment `7ac9fc5`, and its check line prints the difference (three files) and the hunks per file. The resolved tree with #60 passes 156 cases of the three test files (`plan.md`, "Repair round 2"). Review of the repair: the check block of `plan.md` run at `a1fb864` (`origin/main` `87daf91` and #60 `ef7407c`, both unchanged): the difference is `docs/WORKFLOW.md`, `plans/INDEX.md` and `scripts/kit/probe.py`, with 3, 2 and 1 conflict hunks — those of `docs/WORKFLOW.md` at the opening note, the 2b row of §3's routing table and §4; ADR 0009's merge commit is an ancestor. The resolved tree's 156 cases are taken from `plan.md`, not re-run |
| 6-12 | MINOR | SPEC | base | `tests/test_templates.py`: `test_delta_asks_for_the_c4_level_of_each_box`, `test_arc42_asks_only_what_a_reader_needs`, `test_workflow_states_d14_by_class` | Planted on `7ac9fc5`, one at a time, each file restored: four faults keep all 88 cases of the file green. (a) A box without a level, `app["what changes"]`, and (b) a third box `store[("the store")]` without one: the test reads only labels of the form `["Word:`, so a box without that shape is not seen — the half of criterion 47 that phase 4 put under a test. (c) The skeleton's opening loses its whole first paragraph (fill only what a named reader needs; one line where a section has nothing): green, because "reader" survives in the second paragraph's "a later reader". Recorded fault A15 is red only when all four "reader" go; with three of four removed it stays green. Criterion 58's refutation ("one of the three missing") is met, and the test does not see it. (d) The D-14 paragraph of `docs/WORKFLOW.md` says an `architectural` change "never" runs 2b: green, because the test holds the class names, not the rule; the prompt's lines are held word by word (`d14_problems`), the doctrine's are not. (d) stays within criterion 52's refutation as written; (a) to (c) do not. What should hold: every node of the mermaid block carries one of the four levels; the opening's first item is held by its own words; the doctrine's D-14 words held as the prompt's are. (criteria 47, 52, 58) | fixed in `631ce30`, reviewed at `a1fb864`, closed — `c4_problems` reads every box of the diagram, the arc42 opening is held item by item in a paragraph of its own words, and the D-14 paragraph of `docs/WORKFLOW.md` is held clause by clause, with a contradicting word failing it. The row's four faults, the variant of fault A15 and eleven more were planted: fourteen of sixteen were green before, all sixteen are red after, each in its own test (`plan.md`, "Repair round 2", faults 1–16). Review of the repair: faults 1–7 and 10 replayed on a copy of `a1fb864` — each green under the test file of `33a8442` and red under the new one, in the test the record names. Closed for its four faults and the variant; two variants of this review's stay green within criteria 52 and 58 as written ("Checked without a finding"), and a third is a regression of the new box check: 6-16 |
| 6-13 | MINOR | MAINT | base | `prompts/02b-design.md`, line 34; `templates/design.md`, lines 70–72 | "a `feature` whose ADR answer is 'yes'" names something that is usually missing at 2b. The answer is the maintainer's (`docs/WORKFLOW.md`, "Change classes …": "The proposal only proposes. The maintainer answers"), recorded in `decisions/answers/<change>/adr.yaml` and in practice given at the merge — this change carries a provisional class until then, as `harness-decide-adr` did. Case: a `feature` proposes `adr_question.proposed: "yes"`; at 2b no answer exists, so its design writes `None — …` under ADR draft; the maintainer answers "yes" at the merge, and the ADR is then written without the design that should have drafted it. What should hold: the draft is owed when the ADR question is proposed or answered "yes". (no criterion; criterion 42 asks only for `architectural`) | fixed in `4e5ee14`, reviewed at `a1fb864`, closed — the design template and the design prompt say the ADR draft is owed when the spec proposes "yes" to the ADR question or the maintainer has answered "yes"; `test_adr_draft_is_owed_when_proposed_or_answered_yes` holds both files (`plan.md`, "Repair round 2", faults 13 and 14; the reason is there). Review of the repair: faults 13 and 14 replayed, green before, red after. The reading agrees with the doctrine: D-14 sets when 2b runs and says nothing of a `feature`'s draft, and criterion 42's floor (`architectural` always) stands; a draft written on the proposal decides nothing, since the record takes effect by the merge (ADR 0008) and the answer stays the maintainer's (`harness.py decide adr`, the `answer:` of `decisions/answers/<change>/adr.yaml`), while "proposes" is the header's `adr_question.proposed`. The gate lines (the prompt's, §2's phase table, `AGENTS.md`) still name only `architectural`, as before the round — a floor, not a contradiction |
| 6-14 | MINOR | MAINT | base | `templates/arc42.md`, lines 106–114; arc42 `EN/adoc/about-arc42.adoc` (9.0-EN) | The credit leaves out the copyright notice and the "and contributors" that arc42 supplies with its template: "Created, maintained and (C) by Dr. Peter Hruschka, Dr. Gernot Starke and contributors." (`about-arc42.adoc`, read with `gh api` on 2026-10-05). CC BY-SA 4.0, section 3(a)(1)(A)(i) and (ii), asks a reuser to retain the creators' identification and a copyright notice where the licensor supplies them. Everything else is there: the creators, version and date, both links, what was changed, the non-endorsement and the licence of the adaptation; and the sentence that a copy's content stays its author's matches the licensors' own `LICENSE.txt` ("Publishing an architecture document in arc42 structure does not place your own content under CC BY-SA"). That `LICENSE.txt` asks only for credit, a licence link and the changes "in any reasonable manner", which the credit gives — so a suspicion, not a defect; an assessment, not legal advice. What should hold: the credit carries "© Peter Hruschka, Gernot Starke and contributors". (criterion 56 does not ask for it) | fixed in `397b188`, reviewed at `a1fb864`, closed — the credit of `templates/arc42.md` reads "© Dr. Peter Hruschka, Dr. Gernot Starke and contributors", the notice's own names; `about-arc42.adoc` and `LICENSE.txt` of arc42 read with `gh api` on 2026-10-05; the test holds the notice (faults 15 and 16). Criterion 56 is not amended. Review of the repair: `about-arc42.adoc` and `LICENSE.txt` re-read with `gh api` on 2026-10-05 — the notice reads "Created, maintained and (C) by Dr. Peter Hruschka, Dr. Gernot Starke and contributors."; faults 15 and 16 replayed, green before, red after. Criterion 56 left as it is is no drift: it is a floor the credit still meets, the test's extra string is recorded in `plan.md`'s table as "row 6-14, beyond the criterion", and no sentence of `spec.md` says otherwise |
| 6-15 | MINOR | MAINT | base | `docs/WORKFLOW.md`, line 258; `templates/spec.md`, line 74; `prompts/02b-design.md`, line 22; `templates/design.md`, lines 47–48 and 92–100; `tests/test_templates.py`, lines 3 and 41 | Form. (1) Two inserted paragraphs stand as single lines in prose wrapped at 80 columns: the D-14 paragraph of `docs/WORKFLOW.md` (350 characters) and the Non-goals sentence of `templates/spec.md` (128); the report-only markdownlint run of `make verify` flags both (MD013). The plan's insertion block showed them unwrapped, and they were copied so. (2) A bead id carries a sentence, twice (`AGENTS.md`, house rule 7): "until the validator of bead coding-harness-jc3 lands" in the prompt and in `docs/WORKFLOW.md`; a reader without the session does not learn which validator. "Until the change-artefact validator lands (bead coding-harness-jc3)" keeps the string criteria 36 and 52 test. (3) `templates/design.md` mixes `*` bullets (Alternatives) with `-` bullets (the three lists; MD004). (4) The comment "The regex of `tests/test_model_endpoints.py::prompt_modelle`, copied" stands above `ARC42_SECTIONS`, not above `MODEL_LINE`; the module docstring says "Criteria 1-65", while 47, 55 and 63–65 are held by review or command. Not counted: the design prompt's model line (124 characters) and its fence without a language, which follow prompts 02 and 03. (house rules 1 and 7; no criterion) | fixed in `c551836`, `631ce30` and `8822677`, reviewed at `a1fb864`, closed — the D-14 paragraph and the Non-goals sentence are wrapped at 80 columns; the bead id stands as a suffix in the prompt and in the workflow ("until the change-artefact validator lands (bead coding-harness-jc3)"); one bullet style in the design template; the test comment stands above `MODEL_LINE`, and the docstring names what a test does not hold. `markdownlint-cli2` on the five touched files, `33a8442` against `8822677`: MD004 3 → 0, MD013 33 → 31. Review of the repair: in the five touched texts no prose line is over 80 columns (left: the yaml header lines of `templates/spec.md` and the design prompt's model line, not counted); `make verify`'s markdownlint report on them at `a1fb864`: MD013 31, MD004 none. Residues, cosmetic, no row: the docstring still reads as if criteria 26, 29–33, 61 and 62 were held in this file (commands, `tests/test_kit.py` and `tests/test_model_endpoints.py` hold them); the round's own section of `plan.md` has three prose lines of 81, 83 and 93 characters; the Alternatives placeholder now reads "for users, operations, risk", its code span split across a line, which CommonMark joins with a space |
| 6-16 | MINOR | SPEC | fix-r2 | `tests/test_templates.py`, line 73 (`MERMAID_KEYWORDS`) and line 209 (`c4_problems`) | The box check that repair round 2 built for 6-12 skips every line of the diagram whose text begins with a Mermaid keyword, and it compares by prefix, not by word: a line whose first box id begins with "end", "style", "click" or "direction" (`endUser`, `endpoint`, `styleguide`, `clickstream`) is not read at all, and so neither is any box on it. Case, planted one at a time on a copy of `a1fb864` with the template's example diagram given one more line: `endUser["User: who calls it"] --> app` — a level that is none of the four — turns `test_delta_asks_for_the_c4_level_of_each_box` red under the test file of `33a8442` (its label regex reads every quoted label) and keeps all 100 cases green under the new one; `endpoint["the API endpoint"] --> app` and `styleguide["the style guide"] --> app`, boxes without a level, stay green under both. A fault the file caught before the round passes after it, and the row's "every node of the mermaid block carries one of the four levels" does not hold for such a line. None of the six counter-probe diagrams has such an id. What should hold: a keyword is recognised only as a whole word (`end` alone, `style` followed by a space), so that every line naming a box is read, and a counter-probe whose box id begins with a keyword goes red. (criterion 47, the part under a test; row 6-12) | fixed in `ba46f58`, reviewed at `6af6a07`, closed — escalated and decided by the maintainer on 2026-10-05 (`decisions.md`, answer 10): `MERMAID_KEYWORDS` is a compiled pattern that takes a keyword as a whole word (`style` or `click` then white space, `end` alone), so a box id such as `endUser` or `styleguide` is read; counter-tests hold both directions. Thirteen faults planted, five of them green under the old file and all thirteen red under the new (`plan.md`, "Repair round 3", faults 1–13). Review of the repair: faults 1 and 3 replayed — green under the test file of `855eeb6`, red under the new one in `test_delta_asks_for_the_c4_level_of_each_box`; faults 6 and 10, of the new pattern, red in the test the record names (6 in all seven cases). Two variants of this review's — `linkStyleguide["a guide"] --> app`, and `endUser --> app`, a box only named in an edge — green before, red after. The row's own case and its two siblings (`endUser`, `endpoint`, `styleguide`) are read. Closed for its faults; one real keyword line is no longer skipped, `end;`: 6-17 |
| 6-17 | MINOR | MAINT | fix-r3 | `tests/test_templates.py`, lines 75–77 (`MERMAID_KEYWORDS`) and line 213 (`c4_problems`) | The whole-word pattern that repair round 3 built for 6-16 takes `end` only when nothing but white space or a `%%` comment follows it, so a subgraph closed with `end;` is read as a box named `end` that has no label. Mermaid's flowchart grammar admits the form: its lexer takes `"end"\b\s*` as the token, a subgraph statement ends at `end`, and a lone `;` is a line of the document (`packages/mermaid/src/diagrams/flowchart/parser/flow.jison` of `mermaid-js/mermaid`, branch `develop`, last changed in `8d56560df5`, read with `gh api` on 2026-10-05: lines 121, 318–321 and 380–386; Mermaid itself was not run). Case, planted on a copy of `6af6a07`: the template's diagram wrapped in `subgraph sys["System: the harness"]` … `end;` keeps all 100 cases of the test file of `855eeb6` green, because the prefix match skipped the line, and turns `test_delta_asks_for_the_c4_level_of_each_box` red under the new file with "end: no label, so no C4 level"; the same diagram closed with `end` is green under both. The check fails closed: no fault passes, and the template's example has no subgraph. Round 2 recorded a false red of this kind (`A -- text --> B`) without a row; this one is a row because this round made it — the line was skipped before. What should hold: `end` followed by `;` is skipped as `end` alone is, and the skip test carries such a line. (criterion 47, the part under a test; rows 6-12 and 6-16) | open — for the maintainer: the third round in a row with rows of `fix-r` origin |
| 6-18 | MINOR | SPEC | fix-r3 | `spec.md`, criterion 64; `plan.md`, the verification table's rows 27, 38 and 64 (lines 181, 408, 434) and the check blocks (lines 192, 444, 446) | Repair round 3 amended criteria 27, 38 and 64 in the spec but not their rows and check lines in `plan.md`, and criterion 64 now disagrees with itself. (1) Criterion 64 names four files — `prompts/06-review.md` added — among them still `plans/INDEX.md`, which its own third amendment note says has left the difference; its refutation still speaks of "one of those three files". (2) `plan.md`'s table still refutes 38 by "prompt 03 or 04 changed for it" and 27 by "the diff not #60's", both of which the amended criteria now allow, and 64 by "its three files". (3) The check lines, run at `6af6a07` (#60 at `ef7407c`, `origin/main` at `d5813ec`): line 192, commented `# 27: nothing`, prints prompt 03's new hunk; line 444, commented `# 64: the difference, only docs/WORKFLOW.md, plans/INDEX.md, scripts/kit/probe.py`, prints `docs/WORKFLOW.md`, `prompts/06-review.md` and `scripts/kit/probe.py`; line 446 counts the hunks of `plans/INDEX.md` (1, now shared with `origin/main`) and never those of `prompts/06-review.md`. The measured state is the one the amendments describe (this review: three files in the difference with 3, 1 and 2 hunks; criterion 27's diff is the sentence and #60's eight lines). What is wrong is the record phase 7 runs: the Definition of Done asks for criterion 64's special run in the pull request body, and the plan's check prints, against its own comments, a mismatch for a criterion that holds, while it does not count the one hunk this round added. Row 6-11 (2) was the same loose end for round 2. What should hold: criterion 64 names the three files of the difference and its refutation counts them; `plan.md`'s rows and check lines for 27, 38 and 64 say what the amended criteria say. (criteria 27, 38 and 64; row 6-11) | open — for the maintainer: the third round in a row with rows of `fix-r` origin |

Reviewer session: none — phase 2a ran as a sub-agent (Opus 5.5,
`claude-opus-5-5`) of the orchestrating session, without an id a later
session can resume; phase 6 starts a fresh session and says so here.
Phase 6 did so: a fresh sub-agent (Opus 5.5, `claude-opus-5-5`) of the
orchestrating session, again without an id a later round could resume.
Phase 6, round 2: the same, a fresh sub-agent (Opus 5.5, `claude-opus-5-5`)
without an id.
Phase 6, slice 2: the same, a fresh sub-agent (Opus 5.5, `claude-opus-5-5`)
without an id.
Phase 6, slice 2, round 2: the same, a fresh sub-agent (Opus 5.5,
`claude-opus-5-5`) without an id.
Phase 6, round 3: the same, a fresh sub-agent (Opus 5.5, `claude-opus-5-5`)
without an id.

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

Phase 6, on `e3f997e`, 2026-10-05:

- **The 2a rows in the revised spec.** 2a-1: the `[DECISION]` on the class
  quotes the definition in full, records the verdict `feature` and the path
  that needs the maintainer only at the end; criterion 30 and the Definition
  of Done carry it. 2a-2: the `[DECISION]` on the appetite's scope, Terms
  and criterion 5 say phase 4. 2a-3: criterion 5 holds the filled-in header.
  2a-4: criteria 3 and 18 name `read_updated`. 2a-5: the `[DETAIL]` lists six
  values in use, not a closed set. 2a-6: criterion 17 and Terms name the
  section, both lines and the call line. 2a-7 and 2a-8: the refutations of
  criteria 8, 9, 27 and 31 name the missing cases.
- **The tests against their criteria** (`tests/test_templates.py`, 53
  cases). The criteria 1–7, 9–13, 16, 18–25, 27 and 28 are held by tests that
  read what the criterion names: headings outside the leading comment and
  the fences, the filled-in header through the gates' own readers with the
  constants read at call time, the gate ids from `decisions/gates.yaml` at
  run time. The three counter-probes (a new `REQUIRED` field, a planted
  `pytest` line, a planted `templates/missing.md`) each go red. The gaps
  are 6-1 (criterion 8's review part) and 6-3 (criteria 14 and 15).
- **Criterion 17 against the runner.** `ROW_COLUMNS`, `RELEASED_COLUMNS`,
  `SESSION_LINE`, `VERDICT_LINE`, `RELEASE_HEADING`, `ROUNDS_LINE`,
  `NO_LOOP_LINE` and the `Stage-2 call` f-string (lines 118–134 and 446–447
  of `scripts/stage2.py` at `ef7407c`) match the template's forms character
  for character; nothing says stage 2 is active or the columns required
  today. The placement of the no-loop line is 6-2.
- **The decision-record template against ADR 0008 and MADR 4.0.0.** The
  eleven header fields, `status: accepted`, `provenance: human-decided`,
  the empty `review` block and the three bullets match ADR 0008 word for
  word where the template keeps its text; the three name pairs are MADR
  4.0.0's (Consequences and Confirmation are parts of Decision Outcome
  there). `AMENDMENT_ADRS` (`scripts/check_decision_continuity.py`, line
  39), the table "Decision continuity" with its "Amend" entries and the gate
  `decision-continuity` exist.
- **Criteria 26, 27, 29 and 32 by command.** `check_docs.py` reports no
  link into `templates/`; `prompts/03-plan.md` is the same blob (`5ef4015`)
  on this branch and on #60's head, so its diff against `origin/main` is
  #60's eight lines; `probe.py --list` lists the three templates and the
  test; no German in the new lines.
- **No fifth phase word in the kit.** The kit manifest names spec, plan,
  verify and commit — on `origin/main`, on `e3f997e` and on both trial
  merges; `tests/test_kit.py` goes red at five.
- **Criteria 30 and 31.** `make verify` on `e3f997e` with
  `commit.gpgsign=false`, 2026-10-05: `VERIFY GREEN`, 568 passed, 15
  skipped, 44 s; the Leerprobe carries 407 of 438 cases, the merge base's
  356 of 387 plus 51 of the new test's 53 (the two `AGENTS.md` cases skip).
- **Trial merges** (`git merge-tree --write-tree`, 2026-10-05). With #60
  (`ef7407c`): conflicts in `docs/WORKFLOW.md` (the opening note, §4) and
  `plans/INDEX.md`, as `plan.md`'s overlap table says; `prompts/03-plan.md`
  merges without a conflict (identical blob), `prompts/02-spec.md` and
  `scripts/kit/manifest.yaml` merge automatically. Resolved as the spec's
  `[DETAIL]` "Overlaps with pull request #60" says, the merged tree passes
  55 of 55 template cases (#60's `prompts/04b-review-loop.md` adds two).
  With `adhd-frame` (`b4bb2cb`): no conflict, 53 of 53 pass, and its card
  line `Appetite: <time for phase 4; a stop, not an estimate>` agrees with
  the template's note on `appetite:`.
- **Protected areas and non-goals.** The pull request's file list is the
  Definition of Done's files and this change folder; nothing of the
  not-now list is built.
- **Usability.** The three templates have 92, 128 (about half of it
  reference) and 79 lines, are English, set no default appetite
  (`<hours>`), and each shows the header its copy needs — apart from 6-1
  and 6-4. That `prompts/02-spec.md` lists four "Required sections" while
  the form it now names has seven is not a contradiction: the prompt names
  the template as the form, and the spec protects that list for #60.

Phase 6, round 2, on `4c1bf24`, 2026-10-05:

- **The head.** `make verify` with `commit.gpgsign=false`: `VERIFY GREEN`,
  568 passed, 15 skipped; the Leerprobe carries 407 of 438 cases, as before
  the round. `tests/test_templates.py` still has 53 cases. MD033 reports
  nothing on the three templates.
- **The two commits under the head.** `check_frontmatter_current.py`, run on
  a worktree of each, reports `docs/WORKFLOW.md` stale on `a3ede4a` and on
  `23eeff8` — the record names `a3ede4a` alone — and nothing on `4c1bf24`.
  Acceptable: neither `docs/WORKFLOW.md` nor prompts 04 and 07 ask for a
  green intermediate commit, the phase-4 gate and CI measure the head, and the
  stamp is in the round's last commit.
- **The planted faults** (2026-10-05 15:02, throwaway copies, not kept): see
  6-1 and 6-3. The tip's tests, run over `7e11f82`'s spec form, are red in
  `test_criterion_form_is_a_recommendation` only.
- **The copy instruction of 6-4** ("replace it, backticks included") also
  covers four placeholders that stood in code spans before the round:
  `<commit>` in the findings opening, `<bead id>` twice in the spec form, once
  inside `Closes-Bead: <bead id>`. Read literally it drops a code format
  there. Cosmetic, read by no gate; no finding.
- **Trial merge with `origin/main`** (`3851f9c`; `git merge-tree
  --write-tree`, merge base `f985698`). No conflict: the two files both sides
  changed, `plans/INDEX.md` (#63's English header) and `prompts/03-plan.md`
  (`adhd-frame`'s card), merge automatically. On a worktree of the merged
  tree: `make verify` `VERIFY GREEN`, 569 passed, 15 skipped, Leerprobe 407 of
  438; `plans_registry.py --index` rewrites `plans/INDEX.md` to exactly the
  merged file; the diff of `prompts/03-plan.md` against `origin/main` is #60's
  eight lines (only the hunk's offset differs, by the card). On the branch
  itself the plan's criterion-27 command now also shows the card, because
  `main` moved; on the merge it holds.
- **Trial merge with pull request #60** (`ef7407c`, merge base `1e4cccf`).
  Conflicts in `docs/WORKFLOW.md` (the opening note, §4) and `plans/INDEX.md`,
  as before the round; `prompts/02-spec.md` and `scripts/kit/manifest.yaml`
  merge automatically. Resolved as the spec's `[DETAIL]` "Overlaps with pull
  request #60" says (#60's file, `templates/findings.md` struck from the note,
  #60's "defined here because the findings template is not in this repository
  yet" replaced by a pointer; the index regenerated): 55 of 55 cases of
  `tests/test_templates.py` pass.

Phase 6, slice 2, on `7ac9fc5`, 2026-10-05:

- **The head.** `make verify` with `commit.gpgsign=false`: `VERIFY GREEN`,
  605 passed, 15 skipped; the Leerprobe carries 441 of 473 cases.
- **D-14 per class.** The prompt's four lines (`prompts/02b-design.md`, lines
  17–20), the paragraph of `docs/WORKFLOW.md` (line 258) and the Non-goals
  sentence of `templates/spec.md` agree with D-14 as recorded
  (`docs/architecture/target-architecture.md`, line 365: mandatory for
  `architectural`, optional for a `feature` with one sentence in `spec.md`,
  absent for `bounded` and `spike`) and with the rule text of bead
  coding-harness-jc3 (read with `tools/bd show`, nothing written). Both places
  say that nothing checks the rule until that validator lands and that the
  review holds it; no sentence claims a gate. Their form is 6-15.
- **The delta against ADR 0009**, apart from 6-9: a fenced `mermaid`
  `flowchart` of the part the change touches, as it is after the change,
  each box labelled with its C4 level (person, system, container, component),
  the example labelled so; below it the three lists Added, Changed and
  Removed; one sentence in their place when nothing architectural moves; ADR
  0009 named; no LikeC4, `.c4` or model asked for (ADR 0009's own validation
  `grep` finds nothing in `templates/`, `scripts/kit/` and
  `decisions/gates.yaml`). Nothing is asked that the ADR does not decide.
- **The arc42 copy check (criterion 55).** The 14 files of `EN/adoc/` of
  `github.com/arc42/arc42-template` (`version.properties`: 9.0-EN, July
  2025), fetched with `gh api` into the scratch directory and not committed,
  against the skeleton's 458 words outside its header block, headings and
  credit: no shared run of eight words, nor of five or four; the whole
  skeleton, credit included, shares none of eight. The script sees a copy:
  one sentence of `02_architecture_constraints.adoc` appended gives 13 runs.
  The twelve titles are the `==` titles of the twelve section files, in
  order. arc42's text is in the skeleton as titles and as names in the
  credit, nothing more.
- **The licence statement** stands in the body after section 12, outside the
  leading comment, so GitHub shows it and a copy keeps it: an adaptation of
  arc42 under CC BY-SA 4.0 with the licence's URL, creators, version, date,
  `https://arc42.org`, what was changed, the non-endorsement, and that a
  copy's content stays its author's — as answer 9 and option 1 say.
  Attribution: 6-14.
- **2b beside #60's 4b** (trial merge, resolved in a scratch worktree, then
  removed): the 2b and 4b rows stand together in §2 of `docs/WORKFLOW.md`
  and in `AGENTS.md`, with the same columns and the same italic qualifier
  (*(by class)*, *(stage 2)*); §3's routing table takes the 2b row after
  #60's 2a row (Fable 5.1); #60's stage-2 routing table in §4 routes
  reviewers and needs no 2b row.
- **The model line and the gate.** 02b follows prompts 02 and 03 (Opus 5.5
  at effort `xhigh`, the same command line) rather than 02a and 06 (Opus 5.5
  until stage 2, a fresh context), which fits a phase that writes rather than
  reviews; its gate names `scripts/plans_registry.py --check`, the gate that
  exists (the spec's `[DETAIL]`), and its question block is prompt 03's, with
  "design" for "plan". `tests/test_model_endpoints.py` has the case
  `[02b-design.md-Opus 5.5]`.
- **Filled copies under the gates.** A filled `design.md` placed as
  `plans/changes/template-bundle/design.md` and a filled skeleton placed as
  `docs/architecture/coding-harness.md`, committed in a scratch worktree
  (removed afterwards): `make verify` `VERIFY GREEN` once `plans/INDEX.md` is
  regenerated, which any new artefact needs.
- **The kit and the file list.** `probe.py --list` carries
  `prompts/02b-design.md`, `templates/design.md` and `templates/arc42.md`;
  the diff of `scripts/kit/probe.py` is one `REIST_NICHT` entry and the cap
  with its comment. Against `origin/main` the branch does not touch prompts
  04, 06 or 07, `README.md`, `model-endpoints.yaml`, `docs/adr/`,
  `docs/architecture/` or `.github/`; prompt 03 loses only its markings
  section (slice 1). Criterion 65: `a847516` is an ancestor of the head. No
  German word among the added lines.
- **The replayed faults** (one at a time in the worktree, each restored,
  `git status` clean afterwards): D22, D18, A15, A11, W8, P10, T1 and P4 are
  red in the tests the record names; K2 leaves `tests/test_kit.py` green (19
  passed) and turns `probe.py --strict` to exit 2, naming the 02b case, as
  recorded. Of six variants, four are 6-12; the other two — the delta's list
  items removed under their labels, and the D-14 paragraph claiming a gate
  checks the rule — stay green within criteria 44 and 36/52, which hold
  labels by test and the claim by review.
- **Rows 6-6 to 6-8** stand as round 2 left them. 6-7's "what should hold"
  is met since `d68dd26`: the spec's Protected areas name the first sentence
  of the paragraph after §4's plan-marking paragraph as an exception.

Phase 6, slice 2, round 2, on `a1fb864`, 2026-10-05:

- **The head.** `make verify` with `commit.gpgsign=false`: `VERIFY GREEN`,
  617 passed, 15 skipped; the Leerprobe carries 453 of 485 cases — slice 2's
  441 of 473 plus the twelve new cases, all of which carry.
  `tests/test_templates.py` has 100 cases.
- **The replayed faults** (19:13, a copy of `a1fb864` made with `git archive`
  in the scratch directory, not kept; the worktree was not touched). Faults
  1–7 and 10–16 of `plan.md`'s round-2 table: each green under the test file
  of `33a8442` (88 passed) and red under the new one in the one test the
  record names (1 failed, 99 passed); the restored copy passes 100 and 88.
  Faults 8 and 9, the controls, not replayed.
- **Five variants of this review's.** One is 6-16 (`endUser` with the level
  "User"). Two more show its other half, boxes without a level on a line the
  check skips (`endpoint`, `styleguide`): green before and after. The D-14
  paragraph saying "a `bounded` change may run it and a `spike` never does"
  stays green: the two classes share one clause, and the clause holds
  "never" for both — within criterion 52's refutation, which tests the names
  and leaves the rule to review. The arc42 opening saying "What is not known
  is not marked open: it is filled in with a best guess." stays green: the
  words are there, the sense is not, as with the guard of 6-1 — within
  criterion 58's refutation ("one of the three missing").
- **The new counter-probes** hold the checks themselves and pass: a planted
  class is reported missing from the doctrine paragraph too, a D-14 sentence
  with "never" for `architectural` gives both problems and none for
  `feature`, six diagrams are rejected by `c4_problems` and two pass. The
  check fails closed on Mermaid's `A -- text --> B` edges (the text is read
  as a box) — a false red, which the template's example does not use.
- **Protected areas.** The round's nine files are the three of the change
  folder, the three templates, the design prompt, the test file and
  `docs/WORKFLOW.md` in its D-14 paragraph only — each within the spec's
  allowances; prompts 03, 04, 06 and 07, `AGENTS.md`, `docs/adr/`,
  `docs/architecture/`, `scripts/` and `.github/` untouched; nothing of the
  not-now list built.
- **The round's records.** The commits and their times in `plan.md`,
  "Repair round 2", and in its time log match git (`c551836` 18:58:41 to
  `14ca394` 19:00:50, the records `a1fb864` 19:05:01); the stop on criterion
  64 is marked resolved by `7ac9fc5`, committed 18:26:42 as stated.

Phase 6, round 3, on `6af6a07`, 2026-10-05:

- **The head.** `make verify` with `commit.gpgsign=false`: `VERIFY GREEN`,
  711 passed, 15 skipped; the Leerprobe carries 547 of 579 cases;
  `adr-answers` holds four features to their answer files, `template-bundle`
  among them; `frontmatter-current` finds 84 documents current.
  `tests/test_templates.py` has 110 cases; the file of `855eeb6` passes its
  100 on the head's tree.
- **The class commit and the answer.** `spec.md` carries `class: feature`,
  `change: template-bundle` and `adr_question` with `proposed: "no"`,
  `answered_by: null` and the reason that the answer file repeats as
  `proposal_reason` — the form of `harness-decide-adr`'s spec.
  `decisions/answers/template-bundle/adr.yaml` records `answer: 'no'` with a
  reason, `answered_by: framework-architect` and `answered_at: 2026-10-05`,
  like the three earlier answer files. `stated_in` is not a field of the
  file: `harness.py` writes it into the commit message, and `95b1cf9` reads
  "Stated by the maintainer in: Claude Code session 2026-10-05, maintainer's
  answer to: Does this change need an ADR? — Nein". The reason (the
  decisions are already made: D-14, ADR 0009, the answers of 2026-10-05) is
  not part of that recorded statement; whether the maintainer gave it cannot
  be read from the repository, and house rule 8 records an answer only as
  the maintainer stated it. The decision block restated before the merge is
  where he confirms or corrects it. Criterion 65: ADR 0009's merge commit
  `a847516` is an ancestor of the head.
- **`decisions.md`, answers 10–12**, say what the maintainer chose, as the
  orchestrating session reports it: repair 6-16; fix 6-10 now, with one
  sentence each in prompts 03 and 06; "no" to the ADR question, with the
  class `feature`. What they add is the row's own "what should hold" (10),
  6-10's reason and the expected conflict with #60 (11), and the reason for
  "no" (12, above); nothing that decides more.
- **The amendments.** Criterion 27 gains a dated note and keeps its text.
  Criteria 38 and 64 are edited in place — 38's refutation now allows prompt
  03 "beyond the one sentence below", 64 names `prompts/06-review.md` — and
  each carries a dated note naming the round, the finding and the reason;
  not silent. Their echo in `plan.md` is 6-18.
- **The trial merge with #60** (`git merge-tree --write-tree --name-only`,
  #60 at `ef7407c`, `origin/main` at `d5813ec`): the head conflicts in six
  files, `origin/main` in three (the two architecture documents and
  `plans/INDEX.md`); the difference is `docs/WORKFLOW.md`,
  `prompts/06-review.md` and `scripts/kit/probe.py`, with 3, 1 and 2
  conflict hunks — the ones `plan.md` predicts. `prompts/03-plan.md` merges
  without a conflict. Resolved in a scratch worktree as `plan.md` and the
  spec's `[DETAIL]`s say (the opening note from #60 without
  `templates/findings.md`; §3 from #60 with the 2b row after its 2a row; §4
  from #60; #60's 02a entry with this change's 02b entry and `DECKEL = 33`;
  #60's Model lines with this change's Input line; the architecture
  documents from the head's side; `plans/INDEX.md` regenerated):
  `tests/test_templates.py` passes 112 cases, so criterion 64's second
  clause holds; with `tests/test_kit.py` and `tests/test_model_endpoints.py`,
  166 pass (round 2's 156 and this round's ten). The worktree is removed.
- **The replayed faults** (a `git archive` copy of `6af6a07` in the scratch
  directory, not kept; the worktree was not touched, the copy clean
  afterwards): faults 1, 3, 14, 17 and 19 are green under the test file of
  `855eeb6` and red under the new one, each in the one test the record
  names; faults 6 and 10, of the new pattern, are red in the test named.
- **Five variants of this review's.** `linkStyleguide["a guide"] --> app`,
  and `endUser --> app` (a box only named in an edge): green before, red
  after. The Input line's words moved below the Result field: red. Prompt
  03's sentence inverted with its words kept ("A `design.md` is not read
  here; phase 4 needs nothing from it."): green — the test holds words and
  leaves the sense to review, as 6-1's guard does; within criterion 38's
  refutation. A subgraph closed with `end;`: 6-17.
- **Keyword lines still skipped**, probed against the pattern: `%%` comments
  and `%%{init: …}%%`, `subgraph` with and without a title, `end` and `end
  %% …`, and the `style`, `classDef`, `class`, `linkStyle`, `click` and
  `direction` lines, also with a trailing `;`. `End["…"]` and `class_a["…"]`
  are read as boxes. Older than this round, and failing closed on forms the
  template does not use: `a:::warm` reads `warm` as a box, and `accTitle:`
  and `accDescr:` lines are read.
- **The round's records.** The commits of `plan.md`, "Repair round 3", and
  of its time log match git (`7afa516` 23:04:25 to `6da39ee` 23:11:30, the
  records `6af6a07` 23:15:32); the merge `7afa516` changed nothing of this
  change but `plans/INDEX.md`. Residue, cosmetic, no row: the "Not touched"
  paragraph of `plan.md` gained one prose line of 163 characters (line
  485).

## Not checked

- MADR 4.0.0's own text: `research.md` §8, gap 1, is taken as read.
- lakeswitch-ai: not read in this phase; its D-24 and D-58 are cited from
  `research.md`.
- `make verify` of the future build: phase 4.
- Phase 6: a count of 31 mutations said to have been planted during the
  build — no such record is in the repository or the commit messages; not
  read. This review planted ten (6-1, 6-3).
- Phase 6: the hosted CI — no pull request exists yet.
- Phase 6: whether phase 4 began in a cleared context (`/clear` between
  phases 3 and 4) — git does not show it.
- Round 2: GitHub's rendering of the tip (`gh api markdown`) — not re-run;
  MD033 was measured locally instead.
- Round 2: `make verify` and `tests/test_kit.py` on the #60 trial merge (an
  archive without git), and a three-way merge of this branch, `main` and #60.
- Round 2: the remaining ten of the seventeen recorded faults — not replayed.
- Slice 2: the remaining 65 of the 74 recorded faults — not replayed.
- Slice 2: GitHub's rendering of the Mermaid example — Mermaid renders in
  the browser, and no pull request exists to look at.
- Slice 2: `probe.py --strict` and `make verify` on the trial merge with #60
  (phase 4 recorded 473 of 506 for the probe there).
- Slice 2: LakeSwitch's D-58 itself — cited from ADR 0009.
- Slice 2: the hosted CI — no pull request exists yet.
- Slice 2, round 2: the resolved trial merge with #60 and its 156 cases —
  taken from `plan.md`; the conflicting files and hunk counts were re-run.
- Slice 2, round 2: faults 8 and 9 (controls) — not replayed.
- Slice 2, round 2: GitHub's rendering of the split code span in the
  Alternatives bullets — CommonMark's rule read, not rendered; markdownlint
  not run directly, its counts read from `make verify`'s report.
- Round 3: thirteen of the twenty recorded faults (2, 4, 5, 7–9, 11–13, 15,
  16, 18 and 20) — not replayed.
- Round 3: `make verify` and `probe.py --strict` on the resolved trial merge
  with #60 — only the three test files were run there.
- Round 3: the maintainer's own words in the session of 2026-10-05 — not
  read; answers 10–12 were measured against the orchestrating session's
  report of them and against `95b1cf9`.
- Round 3: Mermaid itself on a diagram ending in `end;` — its grammar was
  read, not run.
- Round 3: the hosted CI — no pull request exists yet.

## For phase 7

Round 3, on `6af6a07`, 2026-10-05:

- **Verdict: the gate of phase 6 is open; the next step is the
  maintainer's.** No BLOCKER, no open MAJOR, no `[AMBIGUITY]`, no
  `[DIVERGENT]`; 6-6, 6-7, 6-8, 6-10 and 6-16 are closed. 6-17 and 6-18
  (MINOR, `fix-r3`) make the third round in a row with rows of `fix-r`
  origin, so they go to the maintainer: he accepts them as recorded or asks
  for a repair — for 6-17 one alternative of the pattern and one line of the
  skip test, for 6-18 text in `spec.md` and `plan.md`. By the gate, neither
  row stops the pull request.
- **Owed by phase 7:** the decision pull request (title
  `decide(template-bundle): …`, label `decision`, the block of
  `.github/PULL_REQUEST_TEMPLATE/decision.md`), restating the ADR answer
  "no" and its reason for the maintainer to confirm; the Definition of
  Done's items, the third with its departures; criterion 64's special run
  reported as measured — the difference `docs/WORKFLOW.md`,
  `prompts/06-review.md` and `scripts/kit/probe.py` with 3, 1 and 2 hunks,
  112 cases of `tests/test_templates.py` on the resolved tree — and not as
  the comments of `plan.md`'s check lines state it, unless 6-18 is repaired
  first; 6-17 and 6-18 named as the maintainer's; and no closing trailer
  until the bead is cut to this scope.

Slice 2, round 2, on `a1fb864`, 2026-10-05:

- **Verdict: the gate of phase 6 is open, and the next step is the
  maintainer's, not a third repair round.** No BLOCKER, no `[AMBIGUITY]`, no
  `[DIVERGENT]`; 6-9, the BLOCKER, is closed. Two rows go to the
  maintainer: 6-10 (MAJOR, whether prompts 03 and 06 name `design.md` as an
  input, after #60) and 6-16 (MINOR, `fix-r2`), the escalation that
  `docs/WORKFLOW.md` §2 names after 6-7 (`fix-r1`). For 6-16 the maintainer
  decides between a repair (keywords matched as whole words, one more
  counter-probe) and accepting it as recorded; by the gate, neither row stops
  the pull request.
- **Owed by phase 7 as before:** 6-6, 6-7, 6-8 and the Definition of Done's
  items in the pull request body, with criterion 64 as amended twice; the
  body also names 6-10 and 6-16 as open with the maintainer.

Slice 2, on `7ac9fc5`, 2026-10-05:

- **Verdict: not yet.** 6-9 is a BLOCKER until the Architecture delta
  section asks that elements be named as the existing diagrams and ADRs name
  them — one sentence, and one assertion if a test is to hold it. 6-10, the
  MAJOR, is for the maintainer: whether prompts 03 and 06 name `design.md` as
  input, in a change of their own after #60. The MINORs do not stop the pull
  request; 6-11 and 6-15 are text-only and fit the same repair commit.
- **A repair of 6-9 is repair round 2 of this change.** Round 1 produced a
  row of origin `fix-r1` (6-7); a row that round 2 produces would be
  `fix-r2`, and two consecutive rounds of `fix-r` origin are the escalation
  to the maintainer that `docs/WORKFLOW.md` §2 names, not a third round.
- **Owed by phase 7 as before:** 6-6 (the stamp with the class commit), 6-7
  (its Status — the spec carries the exception since `d68dd26`), 6-8
  (`implementation_status`), and the pull request body's items of the
  Definition of Done, now with the arc42 licence exception for bead
  coding-harness-lir and criterion 64 as amended.

Round 2, on `4c1bf24`, 2026-10-05:

- **Verdict: go.** No BLOCKER, no MAJOR, no `[AMBIGUITY]`, no `[DIVERGENT]`.
  Three MINORs stay open and do not stop the pull request: 6-6 (the stamp,
  owed by the class commit), 6-7 (the protected-area departure, one clause in
  the spec or one line in the body) and 6-8 (`implementation_status`). All
  three touch only the headers or text of `spec.md` and `plan.md`, so the
  class commit can take them together under one stamp.
- **`main` moved** from `f985698` to `3851f9c`; the branch merges into it
  without a conflict and green (above). CI runs on `push` and on
  `pull_request` (`.github/workflows/ci.yml`, checkout without a `ref`), so
  the pull request is measured on the head and on GitHub's merge with `main`.

Phase 6, on `e3f997e`:

- **Verdict: not yet.** 6-1 is a BLOCKER until line 59 of
  `templates/spec.md` carries one condition per criterion only as part of
  the recommendation; the planted repair keeps every case green. The MINORs
  do not stop the pull request; 6-6 is cheapest to take in the same commit
  as the class.
- **The provisional class plan is sound.** It moves the class upward, never
  down; it keeps the build's evidence measured under green gates; it
  follows the precedent of pull request #54 (`harness-decide-adr`); and the
  red `adr-answers` line exists only on this branch. Two things it needs:
  stamping `updated:` in the same commit (6-6), and, once the maintainer's
  answer file lands, the decision pull request's title, label and body
  (spec, Open decisions, step 3) — `plan.md`, "Phase 7", names neither. The
  maintainer's absence ended on 2026-10-04, so the answer can be asked at
  once.
- **The recorded time is consistent with git and measures phase 4 only.**
  `plan.md` logs 2026-09-30 23:34:44–23:43:31; the build commits stand at
  23:38:11, 23:40:16 and 23:40:58, the log commit at 23:43:38; `make verify`
  takes 44 s here, so two runs fit in the logged last span; the spans add
  to 10 minutes against a total of 9 because each is rounded to whole
  minutes. The 4 hours rest on research's 3.5–4.5 hours of building; the
  design work sat in phase 3, whose plan names every test case. Measured
  between commits, phase 2 took at most 16 minutes, phase 2a at most 18 and
  phase 3 at most 13, each more than phase 4's 9 — a data point for the
  maintainer's open decision on the appetite's scope (spec, "The scope of
  the appetite"), not a finding against the build.
