---
title: "Spec — review-fewer-rounds"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
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
adr_files: [docs/adr/0026-focused-review-with-a-shadow-period.md]
neighbours: []
---

# Spec — review-fewer-rounds

Replace successive unfocused reviews with five focused reviewer trios, two
rounds during calibration, and a bounded final review (bead
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
- **Round:** all scheduled lens trios reviewing one frozen revision, followed
  by triage; repairs happen after those calls, never between members.
- **Shadow:** compute a proposed stopping signal, but review every lens again.

## Acceptance criteria

1. When a fresh loop starts, it covers spec fidelity and scope, hostile input
   and failure paths, state/retry/abort, tests as evidence, and maintainability
   through maintainer-approved defect-class check questions.
   *Refuted by:* a missing lens, a role-only prompt, or an unapproved question
   list reaching a model.
   *Basis:* decisions.md#Q-1, decisions.md#Q-9, decisions.md#Q-10.

2. When round 1 runs, each lens receives three independent read-only calls:
   the best measured-precision model, a cheap model of another lineage, and
   Codex `gpt-6.1-terra` at effort `medium`.
   *Refuted by:* fewer than fifteen scheduled calls, duplicate models within
   a trio, shared reviewer answers, an unmeasured precision claim, a cheap
   seat from the precision seat's lineage, or a different Codex model/effort.
   *Basis:* decisions.md#Q-2.

3. If an implementer's model family would be the sole reviewer of a revision,
   that seating is refused.
   *Refuted by:* a sole self-family reviewer being called, or a diverse
   parallel trio being rejected solely because one member shares the family.
   *Basis:* decisions.md#Q-8.

4. When review policy changes, one validated central declaration supplies
   lenses, seats, round count/order, trigger/mode/threshold and phase-6 limit.
   *Refuted by:* a second authoritative settings file, a code edit needed to
   change those values, or a prompt/test/doc independently fixing those values.
   *Basis:* decisions.md#Q-4, decisions.md#Q-5, decisions.md#Q-12.

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

8. When a lens's three round-1 results are complete and decided, its record
   contains S, f1, f2, f3, singleton share, Mh-jackknife and Chao diagnostics.
   *Refuted by:* S differing from f1+f2+f3, share differing from f1/S,
   jackknife total differing from S+2*f1/3, Chao total differing from
   S+f1*f1/(2*f2), or S=0/f2=0 producing a fabricated numeric ratio/Chao.
   *Basis:* decisions.md#Q-11, decisions.md#Q-12.

9. While shadow mode is active, round 2 reviews all five lenses after round-1
   triage and any required repair, regardless of the recorded stopping signal.
   *Refuted by:* a zero-finding or low-singleton lens skipping round 2, or
   a jackknife/Chao value deciding which lenses run.
   *Basis:* decisions.md#Q-11, decisions.md#Q-12.

10. When calibration evidence is requested after 10–20 completed shadow
    changes, it shows per-lens round-2 accepted yield against round-1 singleton
    shares without automatically activating a threshold.
    *Refuted by:* missing zero-finding lenses, counting incomplete changes,
    hiding MAJOR/BLOCKER misses where a candidate would stop, or enabling
    selective review without a later maintainer-stated threshold.
    *Basis:* decisions.md#Q-12, decisions.md#Q-11.

11. When an approved live policy is eventually used, only lenses whose
    singleton-share rule calls for re-review enter round 2.
    *Refuted by:* either diagnostic estimator controlling selection, equality
    being interpreted differently from the declared comparison, or undefined
    overlap evidence being treated as evidence to skip review.
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
    *Refuted by:* an invalid changed header/status/card/time ledger passing,
    Markdownlint failure on a changed file passing, or an unchanged legacy
    defect failing the new checks; existing blocking gates remain in force.
    *Basis:* decisions.md#Q-1, decisions.md#Q-8.

15. When phase 6 has exhausted the configured initial review plus one re-check,
    another substantive phase-6 reviewer call is refused with an unresolved-row
    report and a concrete proposal for a named PR limit, mechanism repair or stop.
    *Refuted by:* a third review starting, missing/renamed/released state
    resetting the budget, or a stop being presented as an approval or clean verdict.
    *Basis:* decisions.md#Q-5.

16. When a second confirmed finding exposes the same defective mechanism,
    further repair addresses that mechanism rather than another isolated case.
    *Refuted by:* another case-only repair or treating the rule as permission
    for a second re-check beyond criterion 15's budget.
    *Basis:* decisions.md#Q-5.

17. If any required seat fails or receives cut/unreadable review input, its
    lens remains incomplete and cannot supply completion or stopping evidence.
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
    describe the configured two-round shadow policy and bounded phase 6.
    *Refuted by:* current instructions still requiring the old ladder/until-clean
    route for new runs or claiming the threshold/questions were approved here.
    *Basis:* decisions.md#Q-4, decisions.md#Q-5, decisions.md#Q-7, decisions.md#Q-12.

## Non-goals

- Proving that lenses find more defects or that singleton share estimates
  completeness; collecting calibration data is included, conducting the
  subsequent 10–20-change evaluation is not phase 4 of this change.
- Choosing a production stopping threshold now, automatic promotion from
  shadow, changing implement/repair routes, or replacing phase-6 review.
- Building the central configuration infrastructure owned by the central
  model/workflow configuration work item (`coding-harness-twvx`); this
  change consumes and extends it, never creates a competing policy file.
- A fourth reviewer, majority voting, new model providers, a dashboard,
  repository-wide Markdown cleanup or automatic follow-up tracker writes.

## Protected areas

- Existing ADR bodies, leak-check rules, endpoint data permissions, customer
  instances, and ambient user configuration: their boundaries are retained.
- Research-swarm routing and historical loop records: no reinterpretation
  as captures or silent migration to the new schedule.
- Decision answers and adoption dates: agents cannot invent approvals.

## Boundary

Three correlated models cannot establish review completeness. The research
read on 2026-11-09 reports approximately 27% median underestimation for
three-inspector jackknife data, not a calibrated error rate for this repo.
Zero accepted findings are weak evidence. Both estimators are diagnostics;
shadow always runs round 2, and later live mode must re-review undefined
evidence. Missing seats stop completion rather than silently changing the
agreed three-seat experiment. Existing legacy snapshots retain their old
semantics until completed or explicitly restarted by the maintainer.

## Definition of Done

- Criterion-ledger evidence and `make verify` pass on the implementation head.
- The same decision PR carries `docs/adr/0026-focused-review-with-a-shadow-period.md`,
  `AGENTS.md`, `docs/WORKFLOW.md`, `docs/how-it-works.md`,
  `prompts/04b-review-loop.md`, `prompts/06-review.md`, central configuration,
  its validator, the new checks and generated `.github/workflows/ci.yml` and
  `plans/INDEX.md`, as enumerated in `plan.md`.
- The maintainer has approved the question list below; the configuration
  dependency has landed and its exact integration is reconciled in the plan.
- Protected areas and non-goals remain untouched in the PR file list.
- The PR closes the focused review work item (`coding-harness-3rtn`), with
  final trailer `Closes-Bead: coding-harness-3rtn`.
- Special live runs: none required to draft or implement; report subsequent
  calibration observations with their dated commits, never as existing evidence.

## Open decisions

`[DECISION]` The check-question list requires maintainer approval under Q-10.
It is proposed below, not answered in this draft. The orchestrator records
the eventual answer and its context in `decisions.md` and the bead.

Topic: Die fünf Prüfschwerpunkte brauchen konkrete Prüffragen.
Intention: Die Fragen sollen die beobachteten Fehler treffen, bevor Modelle damit prüfen.
Today: Die Schwerpunkte sind beschlossen; eine Fragenliste ist noch nicht freigegeben.
Repository change: Die folgende Liste wird zur freizugebenden Grundlage der zentralen Konfiguration.
Architecture change: Keine zusätzliche Änderung; die Liste füllt die bereits beschlossenen Schwerpunkte aus.

Goal in one sentence: Jeder Schwerpunkt sucht anhand konkreter Fragen nach seiner Fehlerklasse.
Options:

- Option 1 — Die folgende Liste verwenden: Alle fünf Schwerpunkte erhalten
  konkrete Fragen; spätere Änderungen bleiben sichtbar freizugeben.
- Option 2 — Einzelne Fragen ändern: Die Umsetzung wartet auf die korrigierte Liste.

Recommendation: Option 1 — sie verbindet die beobachteten Spezifikations- und Wartungsfehler mit den Fehlerszenarien aus der Recherche.
If you say "ok": Genau die folgende Liste wird als freigegebener Fragenkatalog umgesetzt.
What is lost: Ein längerer Fragenkatalog könnte weitere Spezialfälle einzeln nennen, erhöht aber den Prüfaufwand.

| Lens | Proposed check questions | Derivation |
|---|---|---|
| Spec fidelity and scope | Does every criterion hold for its trigger, state and refuting case? Does the implementation preserve the recorded decisions and non-goals? Do current user instructions promise behavior the implementation actually provides? | Q-1; research §(a); Q-10's measured SPEC share on 2026-11-09 |
| Hostile input and failure paths | Can malformed, adversarial or missing input bypass a boundary? Do timeout, denial and dependency failure stop safely with truthful evidence? Can credentials or outside data enter output or foreign calls? | Q-1; research's cut-input failure and scenario-reading evidence §(a) |
| State, retry and abort | Does retry/resume preserve revision, ownership and completed work? Can abort/crash leave ambiguous or replayable state? Do concurrent operations, stale receipts or release/reset bypass a limit? | Q-1; research's repair-generated defects and snapshot/round rules |
| Tests as evidence | Does each criterion have evidence that reaches the production boundary? Would its stated fault turn that evidence red? Do fixtures hide failure, partial results or a missing prerequisite? | Q-1; research's distinction between measured results and missing observations |
| Maintainability | Does one place own each rule without diverging copies? Does the repair close the faulty mechanism across its callers? Can a later maintainer understand and change the behavior without hidden coupling or unrelated scope? | Q-1; Q-10's measured MAINT share on 2026-11-09; research's repeated-repair examples |

Soll diese Fragenliste unverändert umgesetzt werden (Option 1)?

I decide these reversible details and record why:

- `[DETAIL]` Twelve hours of phase 4, repairs included, is the appetite stop:
  no interview answer supplies one, and the runner, gates and doctrine must
  move together. This is not a promise to finish within twelve hours.
- `[DETAIL]` The proposed integration location is a `review_loop` section
  of existing `model-endpoints.yaml`; the configuration prerequisite must
  confirm it before phase 4. Reconcile the path here if that work chose
  another canonical file; do not create both.
- `[DETAIL]` Initial precision seat: `deepseek-v4.1-flash` on Q-2's
  2026-11-08 aggregate 91% accepted share, explicitly not per-lens evidence.
  Cheap other-lineage seat: `mimo-v2.6-flash`, declared 30,100 requests/5h
  versus GLM Flash's 6,320 at baseline `d23f416c`. These are configuration
  proposals, subject to current admission/reachability, not fresh probes.
- `[DETAIL]` Shadow logs a provisional candidate `singleton_share > 0.5`,
  derived from research's proposed half-share signal; it has no minimum
  count override and no authority to skip a lens. S=0 is undefined. Live
  configuration requires a later maintainer-approved threshold and comparison.
- `[DETAIL]` A lens reviewer reports only BLOCKERs outside its own lens,
  preserving serious incidental discoveries without recreating general review.
