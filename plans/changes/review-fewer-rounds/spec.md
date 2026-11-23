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
- **Model family / lineage:** the origin of model weights, independent of
  serving endpoint; model IDs have an explicit family in the policy. The
  implementer family comes from its recorded model ID, not its provider.
- **Complete shadow change:** a full, non-text-only, non-bounded change with
  every required focused and free-round seat, triage and phase-6 verdict
  recorded; early-ended or stopped changes are reported but do not count.
- **Shadow:** record per-lens signals; eligible full changes receive the free
  second round except when the configured minor-only early end applies.

## Acceptance criteria

1. When a fresh loop starts under the initial policy, it covers spec fidelity and scope, hostile input
   and failure paths, state/retry/abort, tests as evidence, and maintainability
   through sourced defect-class check questions.
   *Refuted by:* a missing initial lens, a role-only prompt, an unapproved
   initial list, or a later addition without a phase-6 finding source.
   *Basis:* decisions.md#Q-1, decisions.md#Q-9, decisions.md#Q-10, decisions.md#Q-13.

2. When round 1 runs under the initial policy, each lens receives two
   independent read-only calls, including for bounded changes: fixed
   `deepseek-v4.1-flash` and one randomly drawn reachable challenger.
   *Refuted by:* a missing seat, duplicate models, a challenger outside the
   configured reachable pool, an unrecorded draw and seed, shared answers, or
   any phase-4b call for a text-only change.
   *Basis:* decisions.md#Q-19, decisions.md#Q-24, decisions.md#Q-30.

3. When a lens is seated, at most one reviewer belongs to the implementer's
   model family, and a sole reviewer belongs to another family.
   *Refuted by:* a sole self-family reviewer, two self-family members on one
   lens, or refusal solely because a diverse group has one self-family member.
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

7. When reviewer rows are triaged, their union retains every source row,
   seat and lens, disposition, and an orchestrator-assigned defect group.
   *Refuted by:* majority voting dropping a singleton, a rejected row counted
   as a capture, a missing source row, or unrelated defects grouped merely
   because they share a location or category.
   *Basis:* decisions.md#Q-3, decisions.md#Q-11.

8. When a lens's round-1 results are complete and triaged, its observation
   states accepted-defect counts and singleton share, and applicable
   diagnostics for the actual number of independent seats.
   *Refuted by:* for two seats, S differing from f1+f2, share differing from
   f1/S, jackknife total differing from S+f1/2, Chao total differing from
   S+f1*f1/(2*f2), a fabricated ratio for S=0, or Chao for f2=0.
   *Basis:* decisions.md#Q-11, decisions.md#Q-12, decisions.md#Q-30.

9. While shadow mode is active, an eligible full change receives one free
   second round over the whole post-repair diff regardless of per-lens signals,
   except when round 1 brought at least one finding, all findings were MINOR,
   and all are repaired.
   *Refuted by:* focused lens prompts in round 2, a low singleton share alone
   skipping it, or a second round despite the configured minor-only early end.
   *Basis:* decisions.md#Q-3, decisions.md#Q-12, decisions.md#Q-19, decisions.md#Q-20, decisions.md#Q-24.

10. When ten complete shadow changes are available, a report compares the
    singleton candidate and logged estimators with additional accepted
    round-2 defects and presents the evidence for the maintainer's decision.
    *Refuted by:* counting incomplete, early-ended, bounded, text-only or
    duplicate changes; omitting zero-finding lenses or would-stop
    MAJOR/BLOCKER misses; or switching modes without the maintainer's edit.
    *Basis:* decisions.md#Q-11, decisions.md#Q-12, decisions.md#Q-19, decisions.md#Q-26, decisions.md#Q-30.

11. When an approved calibrated live policy calls for re-review on at least
    one complete lens, the runner schedules one free second round over the
    whole diff for a full change that has not met the minor-only early end.
    *Refuted by:* selective lens re-review, more than one second round, an
    incorrect comparison, treating undefined share as triggered, or a free
    second round for a bounded or text-only change.
    *Basis:* decisions.md#Q-3, decisions.md#Q-11, decisions.md#Q-19, decisions.md#Q-20, decisions.md#Q-26.

12. When round 2 finishes, its triaged findings lead to at most one last repair
    before phase 6, with no third full loop round under the initial policy.
    *Refuted by:* a MAJOR/BLOCKER in this change being deferred because it is
    outside the repair diff, a new full round being launched, or a follow-up
    task replacing a repair except for a defect in code outside this change.
    *Basis:* decisions.md#Q-6.

13. When triage finds MINOR issues, logic, state, tests, security and false
    statements require repair; maintainability and clear style go to weekly
    clean-up unless fixed in an already required repair; taste is a PR limit.
    *Refuted by:* leaving a logic MINOR unrepaired, maintainability alone
    requiring a repair, or treating a security defect as style.
    *Basis:* decisions.md#Q-6, decisions.md#Q-7, decisions.md#Q-28.

14. When Markdown lint reports an error on a line written by the change
    relative to the merge base with main, it blocks locally and in CI.
    *Refuted by:* a new-line error passing, an untouched legacy-line error
    blocking, or local and CI comparisons using different bases.
    *Basis:* decisions.md#Q-8, decisions.md#Q-29.

15. When phase 6 reaches its configured first review and one re-check, it
    stops with unresolved rows and a concrete proposal, subject to the
    documented night exception or one maintainer-authorized repair re-check.
    *Refuted by:* an ordinary third review without either authorization, a
    night exception without one evidenced repaired mechanism, replaying an
    authorization, loss or release resetting the budget, or a stopped run
    reported as clean.
    *Basis:* decisions.md#Q-5, decisions.md#Q-27.

16. When two confirmed findings in phase-6 re-checks share a recorded
    defective mechanism, the next repair instruction requires a mechanism fix.
    *Refuted by:* linked findings whose repair instruction permits only the
    latest case, or an unreviewed repair treated as reviewed.
    *Basis:* decisions.md#Q-5, decisions.md#Q-27.

17. If a required seat fails, a declared eligible substitute is attempted
    on the same complete input, and the failure and substitution are reported.
    *Refuted by:* a failed or truncated seat counted as clean, an undeclared
    or family-ineligible replacement, replaying successful seats, or completing
    a round without the required successful seats and full input.
    *Basis:* decisions.md#Q-8, decisions.md#Q-25, decisions.md#Q-30.

18. When calls and repair checks finish, the run records per-model and per-lens accepted-row share, unique accepted yield,
    call count/duration/tokens, and verification count/duration
    including lock wait, marking unavailable measurements explicitly.
    *Refuted by:* absent provenance, omitted failed calls, invented token counts, a missing challenger comparison,
    or lock wait conflated with verification execution time.
    *Basis:* decisions.md#Q-12, decisions.md#Q-30; research.md, cost section.

19. When the new loop calls a foreign reviewer, the existing admission,
    per-call leak check, credential isolation and read-only boundaries hold.
    *Refuted by:* bypassing the runner, admitting unread paid terms through
    the discovered-free exception, leaking credentials, or reviewer writes.
    *Basis:* decisions.md#Q-2, decisions.md#Q-8; research.md, current loop.

20. When this change is delivered, the workflow, prompts and one new amendment
    describe focused round 1, the configured free second round, and bounded
    phase 6 with its single-mechanism night exception.
    *Refuted by:* current instructions still requiring the old ladder/until-clean
    route for new runs, calling answered choices open, or claiming a live
    threshold was approved here.
    *Basis:* decisions.md#Q-4, decisions.md#Q-5, decisions.md#Q-7, decisions.md#Q-12, decisions.md#Q-14.

21. When a week has clear style or maintainability MINOR findings left standing,
    the orchestrator gathers them in one clean-up bead for its own pull request.
    *Refuted by:* clear findings being discarded, taste-only proposals being
    required repairs, or style alone adding a round to their source change.
    *Basis:* decisions.md#Q-7, decisions.md#Q-28.

22. When artefact formalities are removed from reviewer duties, the spec's
    formality inventory names a checking gate for each, and the orchestrator
    records a follow-up bead for every uncovered formality.
    *Refuted by:* an omitted formality, a claimed gate that does not check it,
    or an uncovered item with no follow-up record before delivery.
    *Basis:* decisions.md#Q-1.

23. When phase 6 finds a defect that no lens question covers, a derived
    question addition is shown in the pull request and applies to new runs from its merge
    after the initial list has received the maintainer's approval.
    *Refuted by:* revising the list without an uncovered phase-6 finding,
    hiding an addition, changing an already frozen run, or treating additions as permission to use
    the first list without approval.
    *Basis:* decisions.md#Q-9, decisions.md#Q-10.

24. While the central configuration skeleton has not merged, the review
    policy lives in one validated section of an existing central file and can
    later move unchanged to the central configuration.
    *Refuted by:* requiring the skeleton before implementation, creating a
    competing policy file, or duplicating authoritative settings in code.
    *Basis:* decisions.md#Q-4, decisions.md#Q-16.

25. When the free second round runs under the initial policy, three distinct
    models from several model families independently read the whole diff once,
    with at most one member of the implementer's family.
    *Refuted by:* fifteen repeated lens calls, fewer or more than three
    required calls, shared answers, one family filling the roster, or two
    implementer-family members.
    *Basis:* decisions.md#Q-14, decisions.md#Q-8.

26. When a bounded change completes its two-seat focused round and required repair,
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
  routes, or replacing phase-6 review. The maintainer makes the later
  promotion decision after seeing the calibration report (Q-26).
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

Two correlated models cannot establish review completeness. The research read
on 2026-11-09 reports approximately 27% median underestimation for
three-inspector jackknife data, not a calibrated error rate for this repo. Zero
accepted findings are weak evidence. During shadow both estimators are
diagnostics; eligible full changes get the free second round subject to the
minor-only early end. Bounded changes have two-seat overlap but do not get the free second round
(Q-19 and Q-30). A failed seat is replaced from the declared list; when no
eligible replacement succeeds, completion waits with the evidence retained. Existing legacy snapshots retain their old semantics until completed or
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
Q-9 and Q-10: an uncovered phase-6 finding is required, the addition is
disclosed in the PR, and it applies to new runs after merge. The runtime list belongs to the central configuration.

| Lens | Approved check questions | Derivation |
|---|---|---|
| Spec fidelity and scope | Does every criterion hold for its trigger, state and refuting case? Does the implementation preserve the recorded decisions and non-goals? Do current user instructions promise behavior the implementation actually provides? | Q-1; research §(a); Q-10's measured SPEC share on 2026-11-09 |
| Hostile input and failure paths | Can malformed, adversarial or missing input bypass a boundary? Do timeout, denial and dependency failure stop safely with truthful evidence? Can credentials or outside data enter output or foreign calls? | Q-1; research's cut-input failure and scenario-reading evidence §(a) |
| State, retry and abort | Does retry/resume preserve revision, ownership and completed work? Can abort/crash leave ambiguous or replayable state? Do concurrent operations, stale receipts or release/reset bypass a limit? | Q-1; research's repair-generated defects and snapshot/round rules |
| Tests as evidence | Does each criterion have evidence that reaches the production boundary? Would its stated fault turn that evidence red? Do fixtures hide failure, partial results or a missing prerequisite? | Q-1; research's distinction between measured results and missing observations |
| Maintainability | Does one place own each rule without diverging copies? Does the repair close the faulty mechanism across its callers? Can a later maintainer understand and change the behavior without hidden coupling or unrelated scope? | Q-1; Q-10's measured MAINT share on 2026-11-09; research's repeated-repair examples |

## Open decisions

None open. The following reversible details make the answered rules
observable and can be changed before implementation:

- `[DETAIL]` The appetite is 12 hours, including repairs: it is a stop, not
  a prediction; no recorded answer gives a different limit.
- `[DETAIL]` Use `model-endpoints.yaml:review_loop` as the interim central
  section (Q-16); no second authoritative policy is created.
- `[DETAIL]` The fixed seat cites its 2026-11-08 aggregate 91% accepted
  share; the validator checks the citation and date, not a claim that the
  aggregate is still the best per-lens value. The report compares observed
  per-model and per-lens shares as accepted rows divided by all triaged rows,
  with sample counts and undefined for zero rows; the maintainer changes the
  seat (Q-30). Compare only observations on the same lens and report an
  observed overtake when the challenger share exceeds the fixed seat share.
- `[DETAIL]` Model family means weight origin, declared per model ID; an
  unknown implementer or reviewer family refuses seating. This distinguishes
  OpenAI model IDs from their serving endpoint and makes Q-8 checkable.
- `[DETAIL]` The orchestrator assigns a stable defect ID and records raw row,
  reporting seat and lens, primary defect lens, disposition and mechanism in
  run evidence released into findings. A group requires the same mechanism,
  trigger and violated invariant; each seat counts once per lens. A BLOCKER
  outside its reporting lens is triaged and repaired but excluded from lens
  observations. Semantic grouping is a human judgment, not machine proof.
- `[DETAIL]` Complete review input may be split into bounded chunks, with
  coverage and revision recorded for each seat; all chunks must succeed. This
  avoids treating an oversized diff as permanently unreviewable or as clean.
- `[DETAIL]` Undefined S=0 yields no positive live trigger and is reported
  as weak evidence; an incomplete seat is not a completed observation and
  must be substituted or retried before the round can proceed.
- `[DETAIL]` Shadow records `singleton_share > 0.5` as a provisional
  candidate only. For two seats use the first-order jackknife `S + f1/2`;
  Chao is diagnostic only when `f2 > 0`. The three-seat research estimate
  is not applied to two seats. Candidate thresholds for diagnostics are
  reported as sensitivity analyses, not silently chosen live rules.
- `[DETAIL]` The orchestrator labels each accepted free-round defect with
  its primary lens and whether it existed before the round-1 repair, was
  introduced by it, or cannot be determined; only pre-existing defects are
  counted as observed misses, and unknowns remain explicit. The report gives
  candidate thresholds and misses, including zero denominators, rather than
  declaring a winner automatically. For each candidate and threshold it
  reports the number of eligible changes where it would stop and the number
  of those with at least one accepted pre-existing MAJOR/BLOCKER in round 2;
  unknown-origin cases are separately counted. The candidate threshold grid
  includes the observed distinct values for each estimator, recorded in the
  report, so no unchosen live threshold is presented as approved.
- `[DETAIL]` The maintainer's post-shadow mode edit must cite a dated,
  repository-held decision and calibration report; a reference is resolved,
  not merely checked for nonempty text. The decision sets the winning rule,
  threshold and comparison; no present record approves live mode. Prepare
  those references and settings before the maintainer switches mode with one
  central value (Q-26).
- `[DETAIL]` The orchestrator derives a question addition from an uncovered
  phase-6 finding, records its source row and discloses it in that change's
  PR. The initial list cites Q-13; additions apply to newly prepared runs
  after merge, preserving each in-progress run's frozen policy.
- `[DETAIL]` A night run is explicitly marked at run start in durable run
  evidence, rather than inferred from a clock. The orchestrator links all
  unresolved rows to one mechanism ID and its repair revision before the
  night exception; a maintainer-authorized re-check separately records the
  maintainer's actual choice and the repair revision (Q-27).
- `[DETAIL]` A weekly collection uses ISO weeks and source row IDs, with
  explicit clear-style, maintainability and taste dispositions; this makes
  omissions and duplicate collections reviewable.
- `[DETAIL]` The formality inventory's minimum reference is Q-1's headers,
  status, card against decisions and time ledger. The orchestrator records a
  follow-up for any uncovered semantic check rather than claiming proof.
- `[DETAIL]` The existing branch-local ADR draft 0027 predates Q-16–Q-30.
  This draft attempt cannot change an existing file outside the change folder;
  the orchestrator must reconcile it before a decision PR can be complete.
