---
title: "Spec — adr-owning-change"
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
tags: [spec, gates, interview-minimums, adr, kit]
class: feature
appetite: 6
change: adr-owning-change
adr_question: {proposed: "yes", reason: "The rule binds every repository the kit reaches: a change claims the ADR files it creates or changes in its spec header, the interview gate attributes an ADR edit by that claim alone and holds the recorded answer to it, and the gate travels with a per-repository adoption day."}
adr_files: [docs/adr/0014-a-change-claims-its-adr-files.md]
---

# Spec — `adr-owning-change`

The goal in one sentence: after this change, an edit under `docs/adr/` belongs
to the change that claims that file in its spec header — not to whichever
change folders the same diff touches — the recorded answer to the ADR question
and those claims cannot drift apart, and the interview gate travels with the
kit and measures each repository from the day it adopted the gate (bead
`coding-harness-afa`). Research: `research.md`, its section "Corrections after
verification" included. Decisions: `decisions.md` Q-1 to Q-5. Design:
`design.md`. This spec assumes that pull request #126 (change
criterion-test-ledger) merges first; `plan.md` says how this change lands
after it.

## Problem

- **The gate infers an ADR's owner from the diff.** Every active change folder
  with a file in the measured diff is an owner, and exactly one is required
  (`research.md`, Q1, read at `2d6a1c6`). A change that adds an ADR and touches
  another change folder for any reason goes red: criterion-test-ledger adds
  ADR 0013 beside four migrated plans (bead `coding-harness-afa`).
- **The repair of pull request #126 guesses.** It treats a folder touched
  through `plan.md` alone as no owner and, beside another owner, lets the ADR
  text decide; its own docstring calls the rule interim, and any other
  cross-folder edit breaks it again (`research.md`, "Corrections after
  verification", read at `7f53552`).
- **Nothing states an ADR's owner.** An answer file binds a change to its
  answer, never an ADR to a change; `owner:` in an ADR header names a role, and
  no ADR carries a change name (`research.md`, Q2).
- **A "yes" is not held to an ADR.** `docs/WORKFLOW.md` §2 says it itself:
  "Nothing checks … that a 'yes' is followed by an ADR" (`research.md`, Q3).
- **The gate stays home, and its cut-off is this repository's.** The kit
  manifest has no entry for `scripts/check_interview_minimums.py`, while the
  gate list that runs it travels; the cut-off is a constant in the script,
  2026-10-08, the day this repository adopted the gate; the criterion-ledger
  gate of #126 has the same shape (bead `coding-harness-wpv`; `research.md`,
  Q4 and "Corrections after verification").

## Terms

- **ADR edit** — a path under `docs/adr/` in the measured diff. Which states
  the diff holds and which base it is taken against stay as the gate has them
  today: committed, staged, unstaged and untracked paths, a rename seen as a
  removal and an addition.
- **Claim** — the list `adr_files` in the header of a change's `spec.md`: the
  paths under `docs/adr/` the change creates, changes or removes. A
  **claimable path** begins `docs/adr/`, names a file below that folder, and
  holds no empty, `.` or `..` segment. A header without the field claims
  nothing, and so does `adr_files: []` (amended 2026-10-13 after phase-6 row
  F-6: the field is recognised by the parsed key in any YAML spelling, and a
  header that does not parse as YAML is reported, since it cannot be decided
  whether it claims).
- **Changes of the diff** — the active change folders, directly under
  `plans/changes/` and not `archive/`, that hold at least one path of the
  measured diff, whichever file it is.
- **Claimant** — of an ADR edit: a change of the diff whose claim lists the
  edit's path.
- **Adoption record** — `decisions/adoption.yaml`: per repository, the day it
  adopted each gate that exempts the changes begun before it, keyed by the
  gate's id in `decisions/gates.yaml`. It stays in its repository and does not
  travel with the kit (`design.md`).
- **Adoption day** — the day the adoption record holds for
  `interview-minimums`.
- **Subject** — a change whose spec `date` is later than the adoption day,
  active or archived: the rule the cut-off holds today, with the adoption day
  in place of the constant. A change whose date cannot be read stays subject.
- **The gate** — `scripts/check_interview_minimums.py`, gate id
  `interview-minimums`. **The reader** — `scripts/adoption.py`, the one module
  that reads the adoption record.

## Acceptance criteria

Criteria 1 and 2 say what a claim is, 3 to 8 how an ADR edit is attributed,
9 to 12 how answer and claim agree, 13 to 16 where the adoption day comes from,
17 to 19 what travels and what stays, 20 to 22 the texts and the ADR, and
23 and 24 what this repository must show at the pull request's head.

1. When a spec header lists paths under `adr_files`, the gate takes exactly
   those paths as the change's claim, in YAML's flow form and in its block
   form alike.
   *Refuted by:* a change listing `docs/adr/0099-x.md` in either form not
   taken as the claimant of an edit of that path; a path named under another
   header key taken as a claim.
2. If a spec header has an `adr_files` line whose claim cannot be read — the
   header is not valid YAML, the value is not a list, an item is not text or
   not a claimable path, or an item stands twice — the gate reports the spec
   and the expected form, for every change folder that carries a spec, active
   or archived, whatever its class and date, with and without `--change`.
   *Refuted by:* exit 0 for `adr_files: docs/adr/0099-x.md`,
   `adr_files: [plans/x.md]`, `adr_files: [docs/adr/../x.md]`,
   `adr_files: [docs/adr/]` or one path listed twice; exit 0 for such a line
   in an archived spec dated before the adoption day.
3. When an ADR edit has exactly one claimant, that claimant owes five counted
   interview records, whatever its class and its spec date.
   *Refuted by:* a claimant with four counted records exits 0; a `bounded`
   claimant, or one dated before the adoption day, with four records exits 0.
4. If an ADR edit has no claimant, the gate reports the path and names the
   remedy — list the path under `adr_files` in the spec header of the change it
   belongs to — also when the diff touches no change folder, when the folders
   it touches do not claim it, and when only a change outside the diff or an
   archived change claims it.
   *Refuted by:* exit 0 for an ADR edit beside one touched change folder that
   does not claim it, the inference of today; exit 0 for an edit only an active
   change outside the diff claims; a finding that does not name `adr_files`.
5. If two or more changes of the diff claim the same ADR edit, the gate reports
   the path and every claimant.
   *Refuted by:* exit 0 when two claimants each carry five counted records.
6. When a change of the diff does not claim an ADR edit, it is no owner of that
   edit, whichever of its files the diff touches: an edit with one claimant is
   decided by the claimant's records alone, beside any number of other touched
   folders.
   *Refuted by:* a finding naming an unclaiming folder beside a claimant with
   five records — the shape of criterion-test-ledger, one claimant changing its
   spec, decisions and plan beside four folders touched through `plan.md`
   alone; a claimant touched through `plan.md` alone not taken as the owner.
7. When the diff holds ADR edits with different claimants, each claimant owes
   its five records on its own.
   *Refuted by:* one claimant with five records and another with four exits 0.
8. When the gate attributes an ADR edit, it reads no ADR text: the interim rule
   of pull request #126 is gone.
   *Refuted by:* an ADR whose text names an unclaiming touched folder changes
   the verdict; `_folders_named_by_adrs` or a `plan_only` set still in the
   gate.
9. When a subject feature's answer file holds `answer: 'yes'` and its claim
   lists no path, the gate reports the change and names both remedies: claim
   the ADR file, or correct the answer in a decision pull request.
   *Refuted by:* exit 0 for a subject "yes" feature without `adr_files`, or
   with `adr_files: []`.
10. When a subject feature's answer file holds `answer: 'no'` and its claim
    lists a path, the gate reports the change and the claimed paths.
    *Refuted by:* exit 0 for a subject "no" feature claiming
    `docs/adr/0099-x.md`.
11. While a change is not a subject feature, the gate does not compare its
    answer and its claim; under `--change`, it compares the named change
    alone.
    *Refuted by:* a "yes" feature dated on the adoption day without a claim
    reported; an archived subject "yes" feature without a claim exits 0; a
    `bounded` change that claims an ADR file reported for its answer;
    `--change other` reporting a disagreement of this feature.
12. If a feature has no answer file, or one the gate `adr-answers` refuses, the
    gate reports nothing about its agreement.
    *Refuted by:* a finding of this gate naming a feature whose answer file is
    missing, or holds `answer: yes` unquoted.
13. When the gate decides whether a change is subject, it compares the spec
    date with the adoption day read through the reader, and holds no cut-off
    date of its own.
    *Refuted by:* with the record's day moved to 2026-10-10, a feature dated
    2026-10-09 without records still reported; a date constant in the gate
    still deciding.
14. If the adoption record is missing, is not valid YAML, lacks
    `schema_version: 1`, or holds no unquoted YAML date for
    `interview-minimums`, the gate exits 3, names the record and the line to
    add, and reports no finding.
    *Refuted by:* exit 0 or 1 without the record; `"2026-10-08"` in quotes
    accepted; an exit-3 message without the record's path.
15. When the reader is asked for a gate id, it returns that gate's day from the
    same record, so a second gate reads its own day by its own id (bead
    `coding-harness-wpv`).
    *Refuted by:* the reader returning the `interview-minimums` day for another
    id; a record with days for two gates refused.
16. This repository's adoption record holds `interview-minimums: 2026-10-08`,
    so no change of this repository moves between stock and subject.
    *Refuted by:* another day in the record; a change of the stock reported, or
    a subject change exempted, at the pull request's head.
17. The kit manifest gives the gate, its test file, the reader and the reader's
    test the role `mechanismus`, and the adoption record the role `bestand`.
    *Refuted by:* any of the four left to the `scripts/` or `tests/` catch-all;
    the record left to the `decisions/` rule.
18. When the empty-repository probe runs, no case of the gate's test file or of
    the reader's test is red, and `REIST_NICHT` and its cap stay as they are.
    *Refuted by:* a red case of either file in the probe; an entry added to
    `REIST_NICHT` or the cap raised.
19. The adoption record is declared `human-decided` in `provenance.yaml`, so a
    pull request that moves an adoption day is a decision pull request.
    *Refuted by:* no `paths:` entry for the record, or one that allows another
    class.
20. The spec template carries an `adr_files` line saying that it belongs to
    every class, and the line as the template has it passes the gate's claim
    reading; `prompts/02-spec.md` says that the header lists every ADR file the
    change creates, changes or removes.
    *Refuted by:* the line missing from `templates/spec.md`; the template's
    line reported by the gate; the prompt without `adr_files`.
21. `docs/WORKFLOW.md` states the claim, the finding for an unclaimed ADR edit,
    the agreement of answer and claim, and the adoption record with this
    repository's day, and no longer says that nothing checks that a "yes" is
    followed by an ADR.
    *Refuted by:* any of the four missing; the old sentence still there.
22. `docs/adr/0014-a-change-claims-its-adr-files.md` records the decisions of
    Q-1 to Q-5 in the form of `templates/adr.md`, as `design.md` drafts it, and
    amends no D- or O-number.
    *Refuted by:* the file missing; its Decision section differing in substance
    from the draft; a D- or O-number named as amended.
23. When the gate runs over this repository at the pull request's head, it
    finds nothing: this change's spec claims ADR 0014, and the spec of
    criterion-test-ledger claims
    `docs/adr/0013-every-criterion-names-its-proof.md`.
    *Refuted by:* any finding; either claim missing.
24. When a test of the interim rule is removed or renamed, the criterion ledger
    of `plans/changes/criterion-test-ledger/plan.md` changes with it in the
    same commit, so it names no test that is gone.
    *Refuted by:* a ledger line of that plan naming a removed test.

## Non-goals

- **The ADR format and the answer format stay as they are** (Q-1): no field in
  an ADR header, no key in `decisions/answers/<change>/adr.yaml`.
  `scripts/check_adr_answers.py` and `scripts/harness.py` are not changed.
- **No check that a claimed file exists.** A change claims its ADR in phase 2
  and writes the file in phase 4. What brings it back: the change-artefact
  validator (bead `coding-harness-jc3`), or a check of archived changes.
- **No claims for ADRs 0001 to 0012 or for the archived changes.** An ADR edit
  is measured per diff, so the stock needs a claim only when a change edits one
  of them.
- **An archived change is no claimant**, also when the same diff archives it:
  such an ADR edit is reported unclaimed, as today it is reported for the
  missing `decisions.md`. What brings it back: a change that archives itself
  in the pull request that edits its ADR.
- **The criterion-ledger gate keeps its own cut-off.** Reading the adoption
  record from `scripts/check_criterion_ledger.py` is bead `coding-harness-wpv`;
  this change builds the record and the reader that gate can call.
- **No check that an `architectural` change claims its ADR**, that a class is
  right, or that a decision pull request carries its label and block.
- **Unchanged:** `AGENTS.md` (its row states the counts, which stay true),
  `decisions/gates.yaml` and so `.github/workflows/ci.yml`, the base rule and
  the diff states, `prompts/01a-interview.md`.
- **No instance runs the gate through this change.** LakeSwitch receives it
  with its next pinned Coding Harness release (bead `coding-harness-dj9`) and
  records its adoption day then.

## Protected areas

- `docs/adr/0001` to `0013`: unchanged; this change adds ADR 0014 only.
- `decisions/answers/`: only this change's own answer file, written by
  `scripts/harness.py decide adr`.
- `scripts/check_adr_answers.py`, `scripts/harness.py`,
  `scripts/check_criterion_ledger.py` and their tests: Q-1 freezes the answer
  format, and the criterion-ledger gate belongs to bead `coding-harness-wpv`.
- Other change folders, except two edits in criterion-test-ledger: the
  `adr_files` line of its spec header (criterion 23) and the criterion-24
  lines of its plan's ledger (criterion 24). (Amended 2026-10-13 after phase-6
  row F-4: a third edit is permitted — the "Phase 4 amendments" narrative of
  that plan, rewritten because the old text described as current the interim
  owner rule this change deletes and named tests that no longer exist, a false
  statement (loop row L1-3).)
  (Amended 2026-10-13 after the merge of codex-drafts: that change's spec
  header gains `adr_files: [docs/adr/0016-…]`. It answered "yes" and added
  ADR 0016 on main before this gate's claim rule existed, so the agreement of
  answer and claim turned red on the updated branch; the claim records the
  edit it made.)

## Definition of Done

- `verify` green.
- Moved in the same pull request: `docs/WORKFLOW.md`, `prompts/02-spec.md`,
  `templates/spec.md`, `scripts/kit/manifest.yaml`, `provenance.yaml`,
  `scripts/ci_gates.py` (the reader's declared reason) and the ADR
  `docs/adr/0014-a-change-claims-its-adr-files.md`; the pull request is a
  decision pull request.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes `coding-harness-afa`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-afa`
  (`prompts/07-commit.md`).
- Special runs: none; the gate's output over this repository at the head
  stands in the pull request body.

## Open decisions

None open. Each point below is a `[DETAIL]` this spec decides, with its
reason; the maintainer's answers Q-1 to Q-5 are not reopened.

- `[DETAIL]` **Field name `adr_files`**, a list of paths: the working name of
  `decisions.md`, plural because a change may edit several files, and distinct
  from `owner`, which names a role.
- `[DETAIL]` **Every path under `docs/adr/` is claimable**, not only `*.md`:
  the gate counts every path there as an ADR edit, so every edit must be
  claimable.
- `[DETAIL]` **A claimant is a change of the diff.** The claim decides who owns
  an edit; the diff only says which changes the measured work comprises. A
  claim anywhere in the tree would attribute a typo fix of an ADR to the
  change that once created it, and pass without a change folder — the
  opposite of the attribution per edit of Q-1 and of the consequence Q-2
  accepts ("even a typo fix in an ADR needs a change folder with a spec").
- `[DETAIL]` **Each ADR edit is attributed on its own** (criterion 7): Q-1 asks
  for an attribution per edit, and "exactly one change folder per diff" was a
  consequence of the inference Q-2 removes.
- `[DETAIL]` **The adoption day exempts the class minimums and the agreement,
  never an ADR edit** (criterion 3): this keeps the rule of loop row L1-3 of
  change interview-minimums, which no answer reopened; Q-4 moves the cut-off
  into a per-repository record without widening what it exempts. For an
  instance this means: a change begun before its adoption day that edits an
  ADR after it claims the file and owes five records.
- `[DETAIL]` **The agreement lives in this gate** (Q-5: "the gate also
  checks"), and reads the answer file through `check_adr_answers.py`, the one
  reader of that format, so the two gates cannot disagree about it. A missing
  or refused answer is the gate `adr-answers`' finding, not a second one here
  (criterion 12).
- `[DETAIL]` **The adoption record, its reader and exit 3 when it is missing**
  (criteria 13 to 15): weighed in `design.md`, "Alternatives". An unmeasured
  block gate is red (bead `coding-harness-4t8`'s rule), which makes an
  instance record its day, the cost Q-4 accepts.
- `[DETAIL]` **This repository's adoption day stays 2026-10-08** (criterion
  16): the day the gate has held since it was adopted here, and Q-5 counts
  criterion-test-ledger, dated 2026-10-11, among the changes the agreement
  holds, which a later day would exempt.
- `[DETAIL]` **The claim is read in every spec, in both modes** (criterion 2):
  a claim that cannot be read makes the attribution of any later ADR edit
  unknowable; only specs written after this change carry the field, so the
  stock cannot trip it, and the ADR attribution is not filtered by `--change`
  today either.
- `[DETAIL]` **Class `feature`, appetite 6 hours** of phase 4, one repair round
  included: the change tightens an existing gate and adds one small module;
  the interview of Q-1 to Q-5 meets the minimum of five.
- `[DETAIL]` **ADR number and name**: 0014 — 0013 is taken by pull request
  #126 — and the slug `a-change-claims-its-adr-files`.
