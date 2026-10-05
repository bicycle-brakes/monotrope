---
title: "Findings — template-bundle"
category: findings
created: 2026-09-30
updated: 2026-10-05
status: draft
implementation_status: none
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
| 6-6 | MINOR | SPEC | base | `plan.md`, "Phase 7" (lines 228–240) | The commit that sets `class: feature` changes the header of `spec.md` on 2026-10-05 or later, while its `updated:` says 2026-09-30. The gate `frontmatter-current` compares `updated:` with the committer date of the file's newest commit (`scripts/check_frontmatter_current.py`, module docstring) and reports the file stale — a second red line beside the expected `adr-answers` line. The plan names `python3 scripts/check_frontmatter_current.py --stamp` only for phase 4 (step 6). What should hold: before the maintainer's answer, `make verify` is red on the one `adr-answers` line and nothing else. (criterion 30) | open — not repaired in this round, on purpose: the class commit is phase 7's. `plan.md`, "Phase 7", now says that the class commit also stamps `updated:` in `spec.md` and that the pull request becomes a decision pull request (title `decide(template-bundle): …`, label `decision`, the block of `.github/PULL_REQUEST_TEMPLATE/decision.md`) once the answer file lands. Round 2: unchanged and still owed to the class commit |
| 6-7 | MINOR | SPEC | fix-r1 | `spec.md`, "Protected areas", third bullet, and "Definition of Done", third item; `docs/WORKFLOW.md`, lines 535–536 | The spec still forbids what the repair of 6-5 did, and the departure is recorded only in `plan.md` and this file. The spec says the change must not touch `docs/WORKFLOW.md` "beyond the opening note and the plan-marking paragraph of §4", and lists its exceptions in that same bullet; repair round 1 rewrote the first sentence of the next paragraph and recorded it as a `[DETAIL]` in `plan.md` ("Not touched", "Repair round 1") without adding it there. Case: in phase 7 the pull request body reports the Definition of Done item "The protected areas untouched … shown by the pull request's file list"; against the spec as written that item is false, and the file list cannot show it either way, because `docs/WORKFLOW.md` is in it for the allowed edits. In substance the departure is harmless, measured: the trial merge with #60 conflicts in the same two hunks of `docs/WORKFLOW.md` as before the round (the opening note; §4, where this side's part grows from four lines to five), and the spec's `[DETAIL]` "Overlaps with pull request #60" (keep #60's §4) resolves both unchanged. Not `[DIVERGENT]`: `plan.md` records a departure from the rule, not a competing rule. What should hold: the spec's bullet names this sentence as an exception, as it names its others, or the pull request body names the departure where it reports the Definition of Done. (Protected areas; Definition of Done, item 3) | open |
| 6-8 | MINOR | MAINT | base | `spec.md`, `plan.md`, `research.md`, `decisions.md`, `findings.md`, header line `implementation_status: none` each; `plans/INDEX.md` | All five artefacts of the change say `implementation_status: none`, and the regenerated index lists the change as unbuilt, while the branch has carried the built templates, their test and the edited prompts since phase 4 (`e3f997e`). `plans/_README.md` says the field moves when the code moves; `harness-decide-adr` moved its spec and plan to `partial` after its phase 4 (`1964244`), and `adhd-frame`'s review held it to the same (its F-6, on `main`). Case: a reader of `plans/INDEX.md` on this branch, or after the merge, sees nothing of this change built. The row existed before repair round 1; the first phase-6 review missed it. What should hold: at least `spec.md` and `plan.md` say `partial`. (no criterion; the plans convention) | open |

Reviewer session: none — phase 2a ran as a sub-agent (Opus 5.5,
`claude-opus-5-5`) of the orchestrating session, without an id a later
session can resume; phase 6 starts a fresh session and says so here.
Phase 6 did so: a fresh sub-agent (Opus 5.5, `claude-opus-5-5`) of the
orchestrating session, again without an id a later round could resume.
Phase 6, round 2: the same, a fresh sub-agent (Opus 5.5, `claude-opus-5-5`)
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

## For phase 7

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
