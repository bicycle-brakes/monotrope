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
adr_files: [docs/adr/0027-focused-review-with-a-shadow-period.md]
neighbours: []
---

# Spec — review-fewer-rounds

Replace successive unfocused reviews with five focused lenses, one free second
round during calibration, and a bounded final review (bead
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
  free describes their focus, not provider pricing. Its seating remains open.
- **Small change:** class `bounded`, or a text-only change under the repository
  rule (Markdown outside `scripts/`, `tests/`, `prompts/` and `decisions/`).
- **Shadow:** record per-lens signals, but always run the one free second round.

## Acceptance criteria

1. When a fresh loop starts, it covers spec fidelity and scope, hostile input
   and failure paths, state/retry/abort, tests as evidence, and maintainability
   through maintainer-approved defect-class check questions.
   *Refuted by:* a missing lens, a role-only prompt, or an unapproved question
   list reaching a model.
   *Basis:* decisions.md#Q-1, decisions.md#Q-9, decisions.md#Q-10.

2. When round 1 runs, each of the five lenses receives three independent
   read-only calls (best measured precision, cheap other lineage, and Codex
   `gpt-6.1-terra` at effort `medium`), except that a small change receives
   one reviewer per lens.
   *Refuted by:* a full change scheduling other than fifteen calls, a small
   change scheduling other than five, repeated models within a trio, shared
   answers, an unmeasured precision claim, or a trio's wrong Codex effort or
   cheap seat sharing the precision seat's lineage.
   *Basis:* decisions.md#Q-2.

3. When a lens is seated, at most one reviewer belongs to the implementer's
   model family, and a sole reviewer belongs to another family.
   *Refuted by:* a sole self-family reviewer, two self-family members on one
   lens, or refusal solely because a diverse trio has one self-family member.
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

8. When a lens's round-1 results are complete and decided, its observation
   states accepted-defect counts and singleton share, with three-seat
   Mh-jackknife and Chao diagnostics only where their prerequisites hold.
   *Refuted by:* for three seats, S differing from f1+f2+f3, share differing
   from f1/S, jackknife total differing from S+2*f1/3, or Chao total differing
   from S+f1*f1/(2*f2); a fabricated ratio for S=0, Chao for f2=0, or a
   three-reviewer estimate from a small change's one reviewer also refutes it.
   *Basis:* decisions.md#Q-2, decisions.md#Q-11, decisions.md#Q-12.

9. While shadow mode is active, every change receives exactly one free
   second round over the whole post-repair diff after round-1 triage and any
   required repair, regardless of its per-lens stopping signals.
   *Refuted by:* focused lens prompts in round 2, skipping it for zero or low
   singleton counts, or separate second rounds per triggered lens.
   *Basis:* decisions.md#Q-3, decisions.md#Q-12.

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
    triggers; a fabricated small-change trigger also refutes it.
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
    describe focused round 1, a free second round, and bounded phase 6 with
    its single-mechanism night exception.
    *Refuted by:* current instructions still requiring the old ladder/until-clean
    route for new runs or claiming the threshold/questions were approved here.
    *Basis:* decisions.md#Q-4, decisions.md#Q-5, decisions.md#Q-7, decisions.md#Q-12.

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

24. While the central configuration skeleton has not merged, this change's
    implementation waits without creating an interim policy file.
    *Refuted by:* starting phase 4 against a proposed local schema or
    creating a second authoritative policy source.
    *Basis:* decisions.md#Q-4.

## Non-goals

- Proving that lenses find more defects or that singleton share estimates
  completeness; collecting calibration data is included, conducting the
  subsequent ten-change evaluation is not phase 4 of this change; its report
  and decision handoff are included.
- Choosing a production stopping threshold now, automatic promotion from
  shadow, changing implement/repair routes, or replacing phase-6 review.
- Building the central configuration infrastructure owned by the central
  model/workflow configuration work item (`coding-harness-twvx`); this
  change consumes and extends it, never creates a competing policy file.
- A fourth reviewer per lens, majority voting, new model providers, a
  dashboard, repository-wide Markdown cleanup or automatic tracker writes by
  reviewers/repair attempts; weekly style collection belongs to the orchestrator.

## Formality inventory

Gate names below describe current checks read at commit `fe8a6329` on
2026-11-10; a planned extension is explicitly labelled. Existing blocking
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
diagnostics; shadow always runs the free second round. One-seat small changes
cannot measure overlap; their live trigger is explicitly undecided. Missing
required seats pause completion rather than silently changing the frozen
seating. Existing legacy snapshots retain their old semantics until completed or
explicitly restarted by the maintainer.

## Definition of Done

- Criterion-ledger evidence and `make verify` pass on the implementation head.
- The same decision PR carries `docs/adr/0027-focused-review-with-a-shadow-period.md`,
  `AGENTS.md`, `docs/WORKFLOW.md`, `docs/how-it-works.md`,
  `prompts/04b-review-loop.md`, `prompts/06-review.md`, central configuration,
  its validator, the new checks and generated `.github/workflows/ci.yml` and
  `plans/INDEX.md`, as enumerated in `plan.md`.
- The maintainer has answered the three open decisions below; the central
  configuration skeleton has merged and its integration is reconciled in the plan.
- Protected areas and non-goals remain untouched in the PR file list.
- The PR closes the focused review work item (`coding-harness-3rtn`), with
  final trailer `Closes-Bead: coding-harness-3rtn`.
- Special live runs: none required to draft or implement; report subsequent
  calibration observations with their dated commits, never as existing evidence.

## Open decisions

These unresolved intent choices prevent a final phase-2 pass. The orchestrator
presents them one at a time and records actual answers with their context in
`decisions.md` and the tracker; this draft cannot do so.

`[DECISION]` The check-question list requires maintainer approval under Q-10. It
is proposed below, not answered in this draft. The orchestrator records the
eventual answer and its context in `decisions.md` and the bead.

Topic: Die fünf Prüfschwerpunkte brauchen konkrete Prüffragen.
Intention: Die Fragen sollen die beobachteten Fehler treffen, bevor Modelle damit prüfen.
Today: Die Schwerpunkte sind beschlossen; eine Fragenliste ist noch nicht freigegeben.
Repository change: Die folgende Liste wird zur freizugebenden Grundlage der zentralen Konfiguration.
Architecture change: Keine zusätzliche Änderung; die Liste füllt die bereits beschlossenen Schwerpunkte aus.

Goal in one sentence: Jeder Schwerpunkt sucht anhand konkreter Fragen nach seiner Fehlerklasse.
Options:

- Option 1 — Die folgende Liste verwenden: Alle fünf Schwerpunkte erhalten
  konkrete Fragen; spätere Ergänzungen gelten bei einem durch Phase 6 belegten Loch sofort und stehen im Pull Request.
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

### Second-round seating — unresolved intent

`[DECISION]` Q-3 leaves the free second round's seating open (`decisions.md`,
Open — not counted). No roster is inferred from round 1.

Topic: Wer die freie zweite Prüfrunde übernimmt.
Intention: Die freie Runde ist beschlossen; für ausführbare Aufrufe fehlt ihre Besetzung.
Today: Die vorhandene Planung wiederholt die fünf Dreiergruppen; dafür gibt es keine aktuelle Antwort.
Repository change: Die zentrale Konfiguration erhält genau eine Besetzung für die freie Runde.
Architecture change: Keine weitere Runde; die vorhandene zweite Runde liest ohne Prüfschwerpunkte.

Goal in one sentence: Die freie zweite Runde erhält eine klare, bezahlbare Besetzung.
Options:

- Option 1 — Ein unabhängiges Dreierteam liest den gesamten Diff: drei Aufrufe mit mehreren Modellfamilien.
- Option 2 — Alle bisherigen Prüfer lesen erneut frei: fünfzehn Aufrufe bei großen Änderungen, mit mehr Wiederholung.

Recommendation: Option 1 — mehrere Modellfamilien bleiben vertreten, während die freie Runde drei Aufrufe benötigt.
If you say "ok": Ein Dreierteam aus den drei für große Änderungen vorgesehenen Modellen liest einmal ohne Linsen; die Familienregel gilt weiter.
What is lost: Die vielen unabhängigen Wiederholungen der zweiten Option entfallen.

Soll die freie zweite Runde ein unabhängiges Dreierteam erhalten (Option 1)?

### Small-change trigger — unresolved intent

`[DECISION]` One reviewer per lens makes every accepted defect a singleton; Q-11
therefore cannot discriminate small changes without another answer. Shadow still
always runs the free second round, including for small changes.

Topic: Wann kleine Änderungen nach der Schattenphase eine zweite Runde bekommen.
Intention: Ein Prüfer pro Schwerpunkt liefert keine Überlappung für die bisherige Auslöseregel.
Today: Bei kleinen Änderungen ist jeder bestätigte Fund ein Einzelfund; die Auslösung ist ausdrücklich offen.
Repository change: Die zentrale Konfiguration erhält eine eigene Regel für kleine Änderungen.
Architecture change: Keine zusätzlichen Prüfer oder Runden; nur die Auslösung wird vervollständigt.

Goal in one sentence: Kleine Änderungen bekommen eine verständliche Regel statt einer scheinbar gemessenen Überlappung.
Options:

- Option 1 — Kleine Änderungen immer zweimal prüfen: kein Schluss aus ungeeigneten Überlappungsdaten, aber weiterhin Kosten der freien Runde.
- Option 2 — Kleine Änderungen nur bei bestätigten Pflichtreparaturen erneut prüfen: weniger Aufrufe, aber eine leere erste Runde kann übersehene Fehler verdecken.

Recommendation: Option 1 — ohne zweite Stimme fehlt die Grundlage für eine verlässliche Auslassregel.
If you say "ok": Kleine Änderungen erhalten auch nach der Schattenphase immer genau eine freie zweite Runde.
What is lost: Die Möglichkeit, ihre zweite Runde bei leerer erster Runde zu sparen.

Sollen kleine Änderungen weiterhin immer eine freie zweite Runde bekommen
(Option 1)?

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
  configuration requires the later recorded comparison, winning trigger and
  threshold; this shadow candidate does not prejudge that outcome.
- `[DETAIL]` A lens reviewer reports only BLOCKERs outside its own lens,
  preserving serious incidental discoveries without recreating general review.
