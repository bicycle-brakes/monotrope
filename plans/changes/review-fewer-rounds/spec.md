---
title: "Spec — review-fewer-rounds"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-3rtn
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, review-loop]
class: architectural
appetite: 12
adr_files: [docs/adr/0027-focused-review-with-a-shadow-period.md]
neighbours: []
---

# Spec — review-fewer-rounds

Replace successive unfocused reviews with configurable focused lenses, a
conditional free second round, and a bounded final review (bead
`coding-harness-3rtn`). Research: `research.md`; intent: `decisions.md`.
This is a proposal until its decision pull request merges.

## Problem

- The research records typically 4–8 loop rounds across 63 changes and
  1,205 loop rows, measured 2026-11-08. Repairs create further findings;
  the 2026-10-23 run reached ten rounds without convergence. The current
  clean-round rule and spent ladder do not direct effort to missing coverage.
- Unfocused reviewers spend attention on deterministic formalities: 26% of
  296 rows in 14 loop records, measured 2026-11-07 (decision Q-1). These
  defects can be checked before a reviewer starts.
- The public research of 2026-11-09 supports investigating focused defect
  classes and model diversity, but supplies no validated three-reviewer
  stopping threshold. The maintainer therefore chose a shadow period,
  superseding the research agent's proposal to gate on jackknife estimates.

## Terms

- **Lens:** one defect class and its approved check questions.
- **Capture:** one distinct accepted defect reported by one reviewer of a
  lens on the same input revision; repeated rows by that reviewer count once.
- **Accepted:** the orchestrator has taken the defect, including a defect
  subsequently fixed; reviewer agreement is not required.
- **Round:** the scheduled reviewers reading one frozen revision, followed by
  triage; repairs happen after those calls, never between members.
- **Free second round:** reviewers read the whole diff without lens questions;
  free describes their focus, not provider pricing. Three models from several
  families review it once (Q-14).
- **Small change:** class `bounded`, or a text-only change under the repository
  rule (Markdown outside `scripts/`, `tests/`, `prompts/` and `decisions/`).
- **Shadow:** record per-lens signals; eligible full changes receive the free
  second round except when the configured minor-only early end applies.

## Acceptance criteria

1. When a fresh loop starts, it covers spec fidelity and scope, hostile input
   and failure paths, state/retry/abort, tests as evidence, and maintainability
   through maintainer-approved defect-class check questions.
   *Refuted by:* a missing lens, a role-only prompt, or an unapproved question
   list reaching a model.
   *Basis:* decisions.md#Q-1, decisions.md#Q-9, decisions.md#Q-10, decisions.md#Q-13.

2. When round 1 runs, each of the five lenses receives three independent
   read-only calls (best measured precision, cheap other lineage, and Codex
   `gpt-6.1-terra` at effort `medium`) under the initial configuration, except
   that a bounded change receives one reviewer per lens and a text-only change
   skips the loop.
   *Refuted by:* a full change scheduling other than fifteen calls, a small
   bounded change scheduling other than five, a text-only change scheduling
   any loop calls, repeated models within a trio, shared
   answers, an unmeasured precision claim, or a trio's wrong Codex effort or
   cheap seat sharing the precision seat's lineage.
   *Basis:* decisions.md#Q-2, decisions.md#Q-19, decisions.md#Q-24.

3. When a lens is seated, at most one reviewer belongs to the implementer's
   model family, and a sole reviewer belongs to another family.
   *Refuted by:* a sole self-family reviewer, two self-family members on one
   lens, or refusal solely because a diverse trio has one self-family member.
   *Basis:* decisions.md#Q-8.

4. When review policy changes, one validated central declaration supplies
   lenses, seats, round count/order, trigger/mode/threshold, finding cap,
   minor-only early end and phase-6 limit.
   *Refuted by:* a second authoritative settings file, a code edit needed to
   change those values, or a prompt/test/doc independently fixing those values.
   *Basis:* decisions.md#Q-4, decisions.md#Q-5, decisions.md#Q-12, decisions.md#Q-16, decisions.md#Q-24.

5. If the central review declaration is missing, malformed or contradictory,
   review refuses before any model call with the offending field named.
   *Refuted by:* silently using a constant, accepting unknown keys, duplicate
   keys, invalid references/ranges or an unapproved live threshold.
   *Basis:* decisions.md#Q-4, decisions.md#Q-12.

6. When an interrupted new-policy run resumes, it retains its frozen policy,
   input revisions and completed seat results without replaying those calls.
   *Refuted by:* editing configuration changing the ongoing run, losing a
   completed seat, mixing revisions within a round, or release resetting it.
   *Basis:* decisions.md#Q-4, decisions.md#Q-3.

7. When reviewer rows are triaged, their union retains every report and its
   provenance alongside an explicit accepted-defect grouping.
   *Refuted by:* majority voting dropping a singleton, counting rejected rows
   as captures, silently deleting duplicates, or combining different defects
   merely because they share a location or category.
   *Basis:* decisions.md#Q-3, decisions.md#Q-11.

8. When a lens's round-1 results are complete and decided, its observation
   states accepted-defect counts and singleton share, with three-seat
   Mh-jackknife and Chao diagnostics only where their prerequisites hold.
   *Refuted by:* for three seats, S differing from f1+f2+f3, share differing
   from f1/S, jackknife total differing from S+2*f1/3, or Chao total differing
   from S+f1*f1/(2*f2); a fabricated ratio for S=0, Chao for f2=0, or a
   three-reviewer estimate from a small change's one reviewer also refutes it.
   *Basis:* decisions.md#Q-2, decisions.md#Q-11, decisions.md#Q-12.

9. While shadow mode is active, an eligible full change receives one free
   second round over the whole post-repair diff regardless of per-lens signals,
   except when round 1 brought only MINOR findings and all are repaired.
   *Refuted by:* focused lens prompts in round 2, a low singleton share alone
   skipping it, or a second round despite the configured minor-only early end.
   *Basis:* decisions.md#Q-3, decisions.md#Q-12, decisions.md#Q-19, decisions.md#Q-20, decisions.md#Q-24.

10. When ten complete shadow changes are available, the calibration report
    presents the singleton rule and logged estimator candidates against new
    accepted round-2 defects, for an evidence-based end of shadow if clear or
    a request to the maintainer otherwise.
    *Refuted by:* waiting unconditionally for twenty changes, counting
    incomplete or duplicate runs, omitting zero-finding lenses or would-stop
    MAJOR/BLOCKER misses, or choosing a production threshold or winning
    trigger without a recorded calibration decision.
    *Basis:* decisions.md#Q-11, decisions.md#Q-12.

11. When an approved calibrated live policy calls for re-review on at least
    one lens, the runner schedules one free second round over the whole diff.
    *Refuted by:* selective lens re-review, more than one second round,
    equality interpreted differently from the configured comparison, or an
    estimator becoming authoritative before the recorded comparison of
    triggers; applying this overlap rule to small changes also refutes it.
    *Basis:* decisions.md#Q-3, decisions.md#Q-11, decisions.md#Q-12.

12. When round 2 finishes, its triaged findings lead to at most one last repair
    before phase 6, with no third full loop round under the initial policy.
    *Refuted by:* a MAJOR/BLOCKER in this change being deferred because it is
    outside the repair diff, a new full round being launched, or a follow-up
    task replacing a repair except for a defect in code outside this change.
    *Basis:* decisions.md#Q-6.

13. When triage finds MINOR issues, tests/security/false statements require
    repair and unambiguous style corrections only accompany an otherwise
    required repair; matters of taste are PR limits.
    *Refuted by:* style alone triggering a repair/round, an available clear
    style fix being omitted from a required repair without reason, or an
    unrepaired security MINOR being dismissed as style.
    *Basis:* decisions.md#Q-6, decisions.md#Q-7.

14. When new or changed Markdown or change artifacts fail their applicable
    lint/formality checks, the new checks block those paths while unchanged
    stock remains report-only under these new checks.
    *Refuted by:* an invalid changed header/status/card placement or appetite/time structure passing,
    Markdownlint failure on a changed file passing, or an unchanged legacy
    defect failing the new checks; existing blocking gates remain in force.
    *Basis:* decisions.md#Q-1, decisions.md#Q-8.

15. When phase 6 reaches its configured first review plus one re-check,
    it stops with unresolved rows and a concrete proposal unless it is a
    night run whose open findings all belong to one repaired mechanism,
    which may receive exactly one additional re-check.
    *Refuted by:* an ordinary third review, a night third review without the
    single-mechanism repair evidence, any fourth review, state release or
    loss resetting the budget, or reporting a stopped run as approved/clean.
    *Basis:* decisions.md#Q-5.

16. When a second confirmed finding exposes the same defective mechanism,
    further repair addresses that mechanism rather than another isolated case.
    *Refuted by:* another case-only repair, or repeated findings alone
    authorizing a further re-check without criterion 15's night conditions.
    *Basis:* decisions.md#Q-5.

17. If any required seat fails or receives cut/unreadable review input, its
    round remains incomplete and cannot supply completion or stopping evidence.
    *Refuted by:* timeout, exhausted quota, malformed output or truncation
    becoming a clean/zero result or a three-reviewer estimate from two results.
    *Basis:* decisions.md#Q-2, decisions.md#Q-3, decisions.md#Q-12.

18. When calls and repair checks finish, the run records per-seat unique
    accepted yield, call count/duration/tokens, and verification count/duration
    including lock wait, marking unavailable measurements explicitly.
    *Refuted by:* absent provenance, omitted failed calls, invented token
    counts, or lock wait conflated with verification execution time.
    *Basis:* decisions.md#Q-2, decisions.md#Q-12; research.md, cost section.

19. When the new loop calls a foreign reviewer, the existing admission,
    per-call leak check, credential isolation and read-only boundaries hold.
    *Refuted by:* bypassing the runner, admitting unread paid terms through
    the discovered-free exception, leaking credentials, or reviewer writes.
    *Basis:* decisions.md#Q-2, decisions.md#Q-8; research.md, current loop.

20. When this change is delivered, the workflow, prompts and one new amendment
    describe focused round 1, the three-model free second round, and bounded
    phase 6 with its single-mechanism night exception.
    *Refuted by:* current instructions still requiring the old ladder/until-clean
    route for new runs, calling answered choices open, or claiming a live
    threshold was approved here.
    *Basis:* decisions.md#Q-4, decisions.md#Q-5, decisions.md#Q-7, decisions.md#Q-12, decisions.md#Q-14.

21. When a week has clear style findings left standing, the orchestrator
    gathers them in one clean-up bead for repair in its own pull request.
    *Refuted by:* clear findings being discarded, taste-only proposals being
    required repairs, or style alone adding a round to their source change.
    *Basis:* decisions.md#Q-7.

22. When artefact formalities are removed from reviewer duties, the spec's
    formality inventory names a checking gate for each, and the orchestrator
    records a follow-up bead for every uncovered formality.
    *Refuted by:* an omitted formality, a claimed gate that does not check it,
    or an uncovered item with no follow-up record before delivery.
    *Basis:* decisions.md#Q-1.

23. When phase 6 finds a defect that no lens question covers, a derived
    question addition applies immediately and is shown in the pull request
    after the initial list has received the maintainer's approval.
    *Refuted by:* revising the list without an uncovered phase-6 finding,
    hiding an addition, or treating immediate additions as permission to use
    the first list without approval.
    *Basis:* decisions.md#Q-9, decisions.md#Q-10.

24. While the central configuration skeleton has not merged, the review
    policy lives in one validated section of an existing central file and can
    later move unchanged to the central configuration.
    *Refuted by:* requiring the skeleton before implementation, creating a
    competing policy file, or duplicating authoritative settings in code.
    *Basis:* decisions.md#Q-4, decisions.md#Q-16.

25. When the free second round runs, exactly three distinct models from
    several model families independently read the whole diff once, with at
    most one member of the implementer's family.
    *Refuted by:* fifteen repeated lens calls, fewer or more than three
    required calls, shared answers, one family filling the roster, or two
    implementer-family members.
    *Basis:* decisions.md#Q-14, decisions.md#Q-8.

26. When a bounded change completes its focused round and required repair,
    it proceeds to phase 6 without a free second round.
    *Refuted by:* scheduling a second loop round for a bounded change.
    *Basis:* decisions.md#Q-19.

27. When a reviewer reports findings, each has a file and line as evidence.
    *Refuted by:* accepting a finding without either location component.
    *Basis:* decisions.md#Q-21.

28. When a reviewer reports more than the configured finding cap, every
    finding above that cap has severity MAJOR or BLOCKER.
    *Refuted by:* accepting a sixth MINOR with the initial cap of five, or
    rejecting a sixth MAJOR solely because of the cap.
    *Basis:* decisions.md#Q-21, decisions.md#Q-24.

29. When a reviewer prepares its response, it performs one self-check against
    the code and drops findings it cannot evidence.
    *Refuted by:* a reviewer instruction omitting the check or asking it to
    retain a finding it cannot substantiate.
    *Basis:* decisions.md#Q-22.

30. When a text-only change reaches review, it skips phase 4b and goes to
    phase 6.
    *Refuted by:* any phase-4b reviewer call for a text-only change.
    *Basis:* decisions.md#Q-19.

## Non-goals

- Proving that lenses find more defects or that singleton share estimates
  completeness; collecting calibration data is included, conducting the
  subsequent ten-change evaluation is not phase 4 of this change; its report
  and decision handoff are included.
- Choosing a production stopping threshold now, changing implement/repair
  routes, or replacing phase-6 review. The promotion procedure is unresolved
  in the open spec-review findings.
- Building the separate central configuration infrastructure; this change
  uses a section of an existing central file in the meantime (Q-16).
- Majority voting, new model providers, a
  dashboard, repository-wide Markdown cleanup or automatic tracker writes by
  reviewers/repair attempts; weekly style collection belongs to the orchestrator.

## Formality inventory

The inventory below carries forward the checks documented in the draft at
`fe8a6329` on 2026-11-10; a planned extension is explicitly labelled. Existing blocking
checks keep their contracts; new lint/formality checks block changed paths only
and report unchanged stock. Reviewers hunt defects, not these formats.

| Formality | Checking gate and coverage |
|---|---|
| Required artifact headers, lifecycle values and supersession links | `plans-registry`; existing `scripts/plans_registry.py` |
| Current header date | `frontmatter-current`; existing `scripts/check_frontmatter_current.py` |
| Bead reference resolves | `dangling-beads`; existing `scripts/check_dangling_bead_ids.py` |
| Class interview minimum, ADR-file claim | `interview-minimums`; existing `scripts/check_interview_minimums.py` |
| Feature's ADR answer | `adr-answers`; existing `scripts/check_adr_answers.py` |
| Answered record's dated statement and context | `question-context`; existing `scripts/check_question_context.py` (presence, not semantic fidelity) |
| Swarm handoff, neighbours and criterion bases | `research-handoff`; existing `scripts/check_research_handoff.py` where v2 applies |
| Criterion-to-test entries and test existence | `criterion-ledger`; existing `scripts/check_criterion_ledger.py` |
| Card placement and five labels | Planned `review-formalities`, reusing `scripts/stage2.py:card_problem`; currently runner-only |
| Card scope/appetite versus spec and decisions | Planned `review-formalities` for mechanically comparable appetite and declared scope; semantic equivalence remains uncovered |
| Time-used heading and runner entry format | Planned `review-formalities`, reusing the runner's time format; entries are not invented during drafting |
| Changed Markdown syntax | Planned changed-path blocking wrapper around existing report-only `markdownlint` |

Semantic card-scope equivalence has no gate at this commit. The orchestrator
must create its follow-up bead and record the title and ID before delivery; this
attempt may not write the tracker. Any further uncovered formality identified
during implementation is handled the same way. The new gate must name unmeasured
semantic checks rather than assert that it proved them.

## Protected areas

- Existing ADR bodies, leak-check rules, endpoint data permissions, customer
  instances, and ambient user configuration: their boundaries are retained.
- Research-swarm routing and historical loop records: no reinterpretation
  as captures or silent migration to the new schedule.
- Decision answers and adoption dates: agents cannot invent approvals.

## Boundary

Three correlated models cannot establish review completeness. The research read
on 2026-11-09 reports approximately 27% median underestimation for
three-inspector jackknife data, not a calibrated error rate for this repo. Zero
accepted findings are weak evidence. During shadow both estimators are
diagnostics; eligible full changes get the free second round subject to the
minor-only early end. One-seat bounded changes cannot measure overlap and do
not get the free second round (Q-19 and Q-20). Missing required seats pause completion rather than silently changing the frozen
seating. Existing legacy snapshots retain their old semantics until completed or
explicitly restarted by the maintainer.

## Definition of Done

- Criterion-ledger evidence and `make verify` pass on the implementation head.
- The same decision PR carries `docs/adr/0027-focused-review-with-a-shadow-period.md`,
  `AGENTS.md`, `docs/WORKFLOW.md`, `docs/how-it-works.md`,
  `prompts/04b-review-loop.md`, `prompts/06-review.md`, central configuration,
  its validator, the new checks and generated `.github/workflows/ci.yml` and
  `plans/INDEX.md`, as enumerated in `plan.md`.
- The initial list and round policies follow the existing answers, including
  the later superseding answers (Q-13, Q-16, Q-19 and Q-20).
- Protected areas and non-goals remain untouched in the PR file list.
- The PR closes the focused review work item (`coding-harness-3rtn`), with
  final trailer `Closes-Bead: coding-harness-3rtn`.
- Special live runs: none required to draft or implement; report subsequent
  calibration observations with their dated commits, never as existing evidence.

## Approved lens questions

The maintainer approved this English list unchanged on 2026-11-10
(decisions.md#Q-13, referring to draft `5bda389c`). Later additions follow
Q-9 and Q-10: an uncovered phase-6 finding is required and the addition is
disclosed in the PR. The runtime list belongs to the central configuration.

| Lens | Approved check questions | Derivation |
|---|---|---|
| Spec fidelity and scope | Does every criterion hold for its trigger, state and refuting case? Does the implementation preserve the recorded decisions and non-goals? Do current user instructions promise behavior the implementation actually provides? | Q-1; research §(a); Q-10's measured SPEC share on 2026-11-09 |
| Hostile input and failure paths | Can malformed, adversarial or missing input bypass a boundary? Do timeout, denial and dependency failure stop safely with truthful evidence? Can credentials or outside data enter output or foreign calls? | Q-1; research's cut-input failure and scenario-reading evidence §(a) |
| State, retry and abort | Does retry/resume preserve revision, ownership and completed work? Can abort/crash leave ambiguous or replayable state? Do concurrent operations, stale receipts or release/reset bypass a limit? | Q-1; research's repair-generated defects and snapshot/round rules |
| Tests as evidence | Does each criterion have evidence that reaches the production boundary? Would its stated fault turn that evidence red? Do fixtures hide failure, partial results or a missing prerequisite? | Q-1; research's distinction between measured results and missing observations |
| Maintainability | Does one place own each rule without diverging copies? Does the repair close the faulty mechanism across its callers? Can a later maintainer understand and change the behavior without hidden coupling or unrelated scope? | Q-1; Q-10's measured MAINT share on 2026-11-09; research's repeated-repair examples |

## Open decisions

The spec review of 2026-11-10 contains unresolved ambiguities S-1, S-3,
S-4, S-7, S-8, S-11, S-13, S-15, S-17, S-18 and S-21 in `findings.md`.
Their meanings and alternatives are recorded there. The later answers Q-16
through Q-24 settle parts of the original scope but do not supply answers
to all of these ambiguities. The draft is not ready for implementation.

[DECISION] **End of the shadow period (S-8)**

Topic: Wann die Erprobung der zweiten Prüfrunde endet.
Intention: Der Ablauf braucht eine überprüfbare Regel für den Übergang.
Today: Die vorhandenen Aussagen lassen zwei Lesarten zu.
Repository change: Der Prüflauf dokumentiert und verwendet die gewählte Regel.
Architecture change: Der Übergang von der Erprobung zum regulären Betrieb
ändert sich; die unabhängige Abschlussprüfung bleibt bestehen.

Goal in one sentence: Klarstellen, wer den Übergang aus der Erprobung auslöst.
Options: (1) Bei klaren Daten automatisch wechseln; bei unklaren Daten fragen.
(2) Immer vor dem Wechsel die Entscheidung des Maintainers einholen.
Recommendation: Option 1 — sie entspricht der festgehaltenen Antwort Q-12.
If you say "ok": Der Lauf wechselt bei klaren Daten automatisch und fragt sonst.
What is lost: Option 2 gäbe dem Maintainer vor jedem Wechsel die letzte Kontrolle.
Downside you accept: Option 1 kann ohne erneute persönliche Prüfung wechseln;
Option 2 hält auch bei klaren Daten für eine Entscheidung an.

Welche Einbuße akzeptierst du: Option 1 oder Option 2?

I decide these reversible details and record why:

- `[DETAIL]` Twelve hours of phase 4, repairs included, is the appetite stop:
  no interview answer supplies one, and the runner, gates and doctrine must
  move together. This is not a promise to finish within twelve hours.
- `[DETAIL]` The proposed integration location is a `review_loop` section
  of existing `model-endpoints.yaml`; this existing central file is the
  interim home under Q-16. Move the section when the central configuration
  lands; do not create competing sources.
- `[DETAIL]` Initial precision seat: `deepseek-v4.1-flash` on Q-2's
  2026-11-08 aggregate 91% accepted share, explicitly not per-lens evidence.
  Cheap other-lineage seat: `mimo-v2.6-flash`, declared 30,100 requests/5h
  versus GLM Flash's 6,320 at baseline `d23f416c`. These are configuration
  proposals, subject to current admission/reachability, not fresh probes.
- `[DETAIL]` Shadow logs a provisional candidate `singleton_share > 0.5`,
  derived from research's proposed half-share signal; it has no minimum
  count override and no authority to skip a lens. S=0 is undefined. Live
  configuration requires the later recorded comparison, winning trigger and
  threshold; this shadow candidate does not prejudge that outcome.
- `[DETAIL]` A lens reviewer reports only BLOCKERs outside its own lens,
  preserving serious incidental discoveries without recreating general review.
- `[DETAIL]` The free second round initially reuses the full-change trio
  as one mixed-family team, with three calls total; Q-14 fixes the count
  and diversity, while model identities remain centrally revisable.
- `[DETAIL]` Each small-change lens initially uses the precision seat
  when it is outside the implementer family, otherwise the declared
  cheap other-family seat; refuse preparation if neither is admissible.
  This keeps its one-seat policy explicit without claiming per-lens data.
- `[DETAIL]` The checked-in branch already contains an ADR 0027 draft. Its
  current body predates Q-16 through Q-24; the present runner instruction
  permits only one new ADR file, so this draft is not silently rewritten.
