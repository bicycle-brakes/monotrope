---
title: "Spec — swarm-citation-feedback"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-t2wm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-swarm, citations]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — swarm-citation-feedback

Research seats can cite Markdown headings with their opening marks and receive
specific citation failures in the existing correction request; the briefs show
how to cite Markdown and limit online fetching (bead coding-harness-t2wm —
repair citation feedback). Basis: `research.md` and the maintainer's small-repair
answer of 2026-11-14 (`decisions.md#Q-1`).

## Problem

Research of 2026-11-14 identifies three gaps in the current citation path:

- The Markdown resolver compares the citation literally to a parsed heading
  title, so opening `#` marks make an otherwise correct reference fail
  (`research.md`, “What exists today”, resolver; `decisions.md#Q-1`).
- The report validator resolves each failed citation with its reason but raises
  only “report has no runner-backed evidence claim” at the evidence floor;
  the authoring seat receives that generic line in its one correction request
  (`research.md`, “Claim evidence during report validation” and “The only
  feedback channel today”). It cannot tell which reference needs repair.
- The shared report brief gives citation rules without a Markdown example,
  and the public brief gives no fetching budget (the four-repair diagnosis
  recorded in `decisions.md`, “Decided by the agent”; confirmed in this tree
  at 3d7cc0e2 on 2026-11-14).

## Terms

- **Seat:** one frozen endpoint/model contribution to one research topic.
- **Correction:** the existing single additional answer by that same seat
  after a process-successful report is rejected, if time remains.
- **Failed citation:** an individual reference the runner cannot support;
  another good reference in the same unsupported claim is not a failed citation.

## Acceptance criteria

1. When a unique structural Markdown heading is cited with its opening ATX
   marks (`#` through `######`, followed by spaces or tabs), it resolves to
   the same frozen extent as its exact title without those opening marks.
   *Refuted by:* `a.md::## Heading` fails against `## Heading`, or returns
   different source bytes or line bounds from `a.md::Heading`.
   *Basis:* `decisions.md#Q-1` and its four-repair detail.

2. While opening heading marks are tolerated, existing structural, exact-title
   and frozen-source reference boundaries remain in force.
   *Refuted by:* an absent, duplicate, prose-only or fenced heading becomes
   supported; case or inline formatting is ignored; a literal hash in an exact
   title loses its meaning; a non-Markdown reference changes; or live files
   substitute for frozen bytes.
   *Basis:* `decisions.md#Q-1`; research.md, “The resolver”.

3. When a report with resolvable structure is rejected for having no
   runner-backed claim, its permitted correction request identifies every
   failed citation by local claim id, original citation and the runner's
   specific reason.
   *Refuted by:* two failed references with different reasons yield only the
   generic evidence-floor message, a failed reference is omitted or changed,
   or a good reference is labelled failed merely because its claim failed.
   *Basis:* `decisions.md#Q-1` and its four-repair detail.

4. While citation diagnostics travel to a correcting seat, they remain that
   seat's own rejected-attempt data within the existing correction boundaries.
   *Refuted by:* diagnostics introduce peer/private context to an online seat,
   become launcher instructions, bypass the exact-prompt leak check, disappear
   from a persisted rejected attempt needed to rebuild its correction prompt,
   or prevent reuse of a newly stored valid correction at identical inputs.
   *Basis:* `decisions.md#Q-1`; research.md, “The only feedback channel today”.

5. When a seat reads the common report contract, it sees an explicitly
   illustrative Markdown heading citation showing the source heading and the
   corresponding `path::heading` evidence string.
   *Refuted by:* the example omits either side, cannot resolve against its
   illustrated frozen source, suggests a line-number citation, or presents
   an invented example as an actual repository fact.
   *Basis:* `decisions.md#Q-1` and its four-repair detail.

6. When an online seat reads its public brief, it is told to make at most
   three `public_fetch` calls per topic attempt and then write its report
   from successful own retrievals, recording unfetched material as not read.
   *Refuted by:* the budget or reporting instruction is missing from a required
   or free online seat's prompt, or the wording permits unsupported evidence.
   *Basis:* `decisions.md#Q-1` and its four-repair detail.

7. If a report already satisfies the evidence floor, unsupported claims do not
   themselves trigger a correction.
   *Refuted by:* a partly supported valid report launches a correction, loses
   its unsupported claim, attaches partial excerpts to that claim, or changes
   its existing question links or the shared 4000-character excerpt budget.
   *Basis:* `decisions.md#Q-1`; research.md, “Claim evidence during report validation”.

## Non-goals

- Runner-issued citation ids: deferred to its own feature explore and interview
  (bead coding-harness-z3d2 — introduce runner-issued citation ids).
- Extra resolution passes, per-citation retries, corrections of valid reports,
  model substitution or replacing timed-out seats.
- Changing report fields, claim limits, the evidence floor, scoring, handoff
  derivation, invocation ceilings, scheduling or time allowances.
- Enforcing a new fetch quota in tool code: the fetch budget is brief guidance.
- Repairing or replaying historical runs; guaranteeing that a model follows
  instructions or that a public source is available.

## Protected areas

Keep judge, handoff, dispatcher, store API, snapshot, model selection and
public tool admission unchanged. Keep `docs/adr/0020-phase-1-research-swarm.md`,
`docs/WORKFLOW.md`, gate definitions and model declarations unchanged: these
repairs preserve the established evidence and correction policy. Only the
orchestrator edits the two held prompt files after the accepted attempt.

## Definition of Done

- Regression checks and `make verify` are green at the implementation commit.
- The same pull request carries `prompts/research-swarm/report.md` and
  `prompts/research-swarm/public.md`, plus this change's spec, plan and findings;
  no architecture decision or design document is due for class `bounded`.
- The pull request's file list demonstrates protected areas and non-goals.
- The pull request closes coding-harness-t2wm — repair citation feedback;
  its last commit carries `Closes-Bead: coding-harness-t2wm`.
- Special live runs: none required; deterministic fixtures establish the
  resolver, diagnostic and brief contracts without calling a foreign model.

## Open decisions

None open. The maintainer chose the small repair and accepted continuing
free-text spelling risk in `decisions.md#Q-1` (2026-11-14).

[DETAIL] Preserve exact-title lookup first; only when it finds no heading,
remove an opening ATX run followed by whitespace for a second title comparison
within the same frozen scan. This preserves literal hash titles and ambiguity
rejection while accepting copied heading prefixes; it is not another evidence
resolution pass.

[DETAIL] Set the public brief's advisory budget to three fetch calls per topic
attempt, including failed fetches, so the seat leaves time for its report;
this changes guidance only, not tool enforcement or the original time limits.

[DETAIL] Set phase-4 appetite to three hours including repairs, as a stopping
point for this bounded fix; no earlier appetite is stated in the inputs.
