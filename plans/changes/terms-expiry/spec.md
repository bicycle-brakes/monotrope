---
title: "Spec — terms-expiry"
status: draft
implementation_status: none
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-abra
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "GLM 5.3, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, model-terms, stage-2]
class: feature
appetite: 4
change: terms-expiry
adr_question: {proposed: "yes", reason: "Mandatory expiry and advance warnings amend paid-model admission under ADR 0021 decision 5."}
adr_files: [docs/adr/0022-paid-model-terms-expire.md]
---

# Spec — terms-expiry

The goal in one sentence: paid OpenCode Go models may run only while their
recorded terms reading is valid, with advance notice of expiry
(bead `coding-harness-abra`). Research: `research.md`. Decisions:
`decisions.md`.

## Problem

- The runner checks that a terms reading has a date, source, retention text
  and permitted training, but never checks its end date. DeepSeek V4 Pro's
  October 31 expiry exists only inside retention prose (`research.md`,
  finding and source re-read of 2026-10-25; confirmed at `97980181`).
- The same source footnote covers DeepSeek V4.1 Flash, whose declaration
  lacks even that prose qualification. Both paid models would remain
  eligible after 2026-10-31 (`research.md`, source re-read of 2026-10-25).
- Other readings have no enforced review deadline, and the runner gives no
  expiry warning (`decisions.md`, answers on missing dates and warnings;
  repository inspection at `97980181`, 2026-10-26).

## Terms

- **Reading:** one paid model's sourced retention/training record under
  `modelle_terms` in the OpenCode Go endpoint declaration.
- **Expiry:** `gilt_bis`, a quoted ISO calendar date `YYYY-MM-DD`, valid
  through that UTC day; the following UTC day is expired.
- **Warning window:** zero through seven calendar days before expiry,
  inclusive; an expired reading is a skip, not an upcoming-expiry warning.

## Acceptance criteria

1. If a paid model's reading has no usable `gilt_bis`, that reading grants
   no admission.
   *Refuted by:* a missing, empty, non-string, timestamp, malformed or
   impossible calendar date admits the model, or the runtime invents a date.
2. When a reading otherwise meets admission rules, its expiry admits the
   model through the named UTC day and excludes it from the following day.
   *Refuted by:* the model is excluded on its expiry day or eligible the
   next UTC day, including when the local calendar date differs from UTC.
3. When expiry validation excludes a paid model, the diagnostic names the
   model, says whether the expiry is missing, invalid or passed, and names
   the recorded expiry date once it has passed.
   *Refuted by:* preparation or review hides the excluded id or reason, or
   a passed-expiry diagnostic omits the recorded date.
4. When preparation or a review-loop invocation evaluates terms within a
   reading's warning window, it visibly warns with the model id and expiry.
   *Refuted by:* a warning is absent at seven days, one day or the expiry
   day, appears eight days before or after expiry, or a resumed/legacy loop
   relies solely on an earlier warning instead of evaluating the current day.
5. When a paid model is about to receive a call, an expired reading prevents
   dispatch even if an earlier selection, receipt or saved run admitted it.
   *Refuted by:* a preparation retry, receipt-backed first review, resumed
   review, Flash replacement, malformed-answer retry, compatibility probe
   or interactive Go session dispatches the expired model; a refusal must
   not fabricate a completed or clean round or reset prior run history.
6. When existing non-DeepSeek readings are migrated, every record receives
   `gilt_bis` equal to its recorded `gelesen` plus 30 calendar days.
   *Refuted by:* a record, including an explicitly skipped record, is left
   undated, receives another deadline, or has its reading date advanced
   without a new source reading.
7. When the two DeepSeek readings are migrated, both record the documented
   2026-10-25 source re-read with `gilt_bis: "2026-10-31"`.
   *Refuted by:* either model receives the generic 30-day deadline, lacks
   the source and re-read date, or loses the monthly-agreement qualification
   from its retention explanation.
8. When a reading is introduced or renewed, the documented procedure
   requires an agent's dated source re-read and a decision pull request
   merged by the maintainer.
   *Refuted by:* the procedure permits renewal without that evidence or
   approval, or the runner rewrites/extends a declared expiry automatically.
9. While expiry checks apply, existing admission restrictions and the
   discovered free class's confined exception retain their force.
   *Refuted by:* a future expiry admits a skipped, unread, training-enabled
   or otherwise undeclared paid model; the free diff-only class requires a
   paid reading; a leak refusal falls through to a model call; or an empty
   eligible selection is reported as a clean review round.
10. When an expiry warning accompanies a successful preparation or written
    review round, its model and date remain in that operation's durable evidence.
    *Refuted by:* the preparation receipt omits the warning, a completed
    round has only transient console output, or releasing the round to
    `findings.md` loses the warning.

## Non-goals

- Automatic renewal, source scraping, provider monitoring or a background
  notification service; renewal remains an evidenced decision pull request.
- New model ids, cost readings, wire-API admission, provider substitution,
  free-class policy changes or a new reachability policy.
- Extending expiry enforcement to other endpoint families; the affected
  boundary is the existing paid OpenCode Go terms check.
- Rewriting historical rounds, reselection/reset of saved stages, or a new
  recovery command when a saved member becomes inadmissible. The existing
  refusal path may stop that round rather than replace the member.

## Protected areas

- `docs/adr/0021-review-swarms-until-clean.md` stays historical; the new ADR
  amends its paid-terms decision without editing its prior decision text.
- `decisions/answers/`, `decisions/gates.yaml`, `provenance.yaml`, routing
  credentials, leak-check rules and the customer-instance boundary remain
  unchanged; none is needed to implement expiry.

## Definition of Done

- `make verify` is green, with deterministic boundary tests and no real
  foreign calls in tests; the runner owns verification and the commit.
- Code, `model-endpoints.yaml`, `docs/WORKFLOW.md`,
  `docs/adr/0022-paid-model-terms-expire.md`, this change's evidence and
  generated `plans/INDEX.md` move together in the decision pull request.
- The pull request file list respects protected areas and non-goals.
- The pull request names bead coding-harness-abra (expiring model-terms
  readings) and closes it when implementation and review finish; the final
  commit then carries `Closes-Bead: coding-harness-abra`.
- No additional live source fetch or availability probe is required by
  this draft: the DeepSeek migration uses the recorded 2026-10-25 reading.

## Open decisions

None open. The five maintainer answers in `decisions.md` settle the scope;
the ADR proposal remains subject to the decision pull request's merge.

- [DETAIL] Preserve retention prose beside the binding `gilt_bis`; compare
  inclusive expiry against UTC, as already recorded in `decisions.md`.
- [DETAIL] Reject unusable dates without inference, using the existing
  reading-date string convention; this keeps malformed input fail-closed.
- [DETAIL] Warn on each terms-evaluating preparation/review invocation,
  including valid dates on otherwise skipped records; a warning never grants
  admission. Preserve warnings in the existing receipt/round evidence so
  resumed work does not depend on console scrollback.
- [DETAIL] Keep saved membership immutable and use the existing per-call
  refusal when it has expired; rebuilding a run would change historical
  selection and is outside this change.
- [DETAIL] Set a four-hour phase-4 appetite, repairs included, as a stop;
  neither input states an appetite, and the shared admission boundary needs
  coverage across preparation, review and interactive launch.
