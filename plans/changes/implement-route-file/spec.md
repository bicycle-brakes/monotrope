---
title: "Spec — implement-route-file"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-9ycy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, implement, routing]
class: bounded
appetite: 3
adr_files: [docs/adr/0007-stage-2-reviews-by-codex-and-glm.md]
neighbours: [plans/specs/implementation-verification/spec.md, plans/changes/research-swarm/spec.md, plans/changes/codex-repairs/spec.md, plans/changes/kimi-admission/spec.md]
---

# Spec — `implement-route-file`

Implementation uses one central, auditable route file, initially selecting
GLM 5.3 instead of Flash, editable on the maintainer's stated instruction
(bead `coding-harness-9ycy` — central implementation routing).
Research: [research.md](research.md). Authority: [decisions.md](decisions.md#q-1--who-may-change-the-route-file).

## Problem

- At `ff012eba` (2026-11-06), `implement()` hard-codes the implementing model
  twice in its three-attempt ladder; changing it requires Python edits
  (research, "What exists today").
- Current instructions in `AGENTS.md`, `docs/WORKFLOW.md`,
  `prompts/04-implement.md`, `model-endpoints.yaml` and ADR 0007 independently
  name Flash as the implementer, so changing only the runner leaves competing
  instructions (same research section; ADR re-read during drafting).
- The interview requires one central artifact with the current route and
  each change's date, stated words and reason, and ordinary pull requests
  for subsequent route edits (decisions Q-1, answered 2026-11-06).

## Terms

**Primary** means the configured model used for the initial implementation
and its one post-check retry; this is separate from the `repair` verb.
**Fallback** means the final Stage-1 implementation attempt, also used alone
with explicit `--stage2-off`.

## Acceptance criteria

1. When a normal implement run starts, its primary comes from the single
   repository-root route file, whose initial primary is GLM 5.3 at effort `max`
   on the already admitted `glm-coding-plan` endpoint.
   *Refuted by:* Flash runs first, or Python rather than the file supplies the selection.
   *Basis:* decisions.md#Q-1 (answer and context).
2. When the maintainer instructs a switch between models on the existing
   supported implementation transports, changing that route file alone changes
   subsequent implement runs without a runner, ADR or workflow edit.
   *Refuted by:* an admitted alternative on a supported transport still needs a second selection edited elsewhere.
   *Basis:* decisions.md#Q-1.
3. When a route change is proposed, the central file retains the preceding
   entries and records its date, the maintainer's stated words, reason and
   resulting primary and fallback; its latest entry identifies the current route.
   *Refuted by:* the proposal erases history, invents a quotation or leaves the active selection ambiguous.
   *Basis:* decisions.md#Q-1.
4. If the route file is missing, unreadable, malformed, internally invalid or
   selects an unsupported transport, implement refuses with a diagnostic
   naming the route file before reading credentials or calling a model.
   *Refuted by:* an invalid file starts a call, silently uses a constant or produces an unhandled parser error.
5. When post-run checks fail on the normal route, the existing ceiling remains
   primary, one fresh primary retry, then one fallback, with no further attempt.
   *Refuted by:* a fourth attempt, a different retry model or fallback after a call failure rather than the existing post-check transition.
6. When explicit `--stage2-off [REASON]` is used, only the configured fallback
   runs and the supplied reason is recorded without reading the GLM credential.
   *Refuted by:* a primary call, a second attempt, a GLM secret read or a missing reason.
7. When any implementation attempt is about to call a model, the existing
   endpoint/model/data-class/residency admission and clean leak check still
   hold, and a refusal stops without another model call.
   *Refuted by:* a route entry bypasses admission, or a planted leak or refused endpoint reaches a call or fallback.
8. When a run records an attempt, its audit and measured-time entries name the
   actual endpoint, model and route without labelling a non-Flash primary as
   Flash, and existing reports still count both historical and new entries.
   *Refuted by:* a GLM 5.3 attempt is recorded as Flash or either record generation stops counting.
9. While an implementation run is in progress, all attempts use its initial
   route snapshot and an implementing or repairing model cannot commit a
   change to the central route file.
   *Refuted by:* an in-run edit redirects a retry or a worker's route edit is accepted into its checkpoint.
10. When this change is complete, current implementation instructions in
    `AGENTS.md`, `docs/WORKFLOW.md`, `prompts/04-implement.md`,
    `model-endpoints.yaml` and ADR 0007 point to the route file as the selection
    authority, including its instruction-backed ordinary-PR update rule.
    *Refuted by:* one of those current instructions still independently selects the primary model or requires an ADR edit for a later route-only switch.
11. When another runner verb executes, its model selection remains unchanged.
    *Refuted by:* editing the implementation route changes explore, draft, repair, a review or a research seat.
12. When implementation attempts pass or fail, their existing preparation,
    verification, time measurement, held-path protection and checkpoint
    conditions remain in force.
    *Refuted by:* a red check checkpoints, measured evidence disappears or a previously held edit is accepted.

## Non-goals

- New endpoint admissions, transports, executable commands in configuration,
  per-change overrides or a general routing engine; support is limited to the
  existing Claude Code GLM and native Claude Code work transports.
- Changes to retry counts, retry/call-failure transitions, failed-edit
  continuation, the review ladder, other verbs or endpoint data permissions.
- Automatically authenticating a maintainer quotation; the conversation and
  pull-request review establish authority, not a self-asserted YAML field.
- Rewriting historical findings, research, time records or previous decisions.
  ADR 0007 receives only the explicitly authorised current-routing wording
  amendment, with a dated note preserving the previous decision's history.

Phase 2b does not run because this change is `bounded`.

## Protected areas

Endpoint admission, leak rules, gates, provenance rules, permission settings,
other ADRs and the tracker remain unchanged: moving selection does not admit
an endpoint or change the workflow's governance. Held files are edited only
by the orchestrator, as the plan assigns them.

## Definition of Done

- `make verify` is green after code and orchestrator bootstrap edits.
- The route file, runner, tests and the five instruction surfaces named in
  criterion 10 move together; the living implementation-verification spec
  replaces only obsolete model-specific wording, preserving its attempt limits.
- The PR file list respects the protected areas and non-goals.
- The PR closes the central-route work item (`coding-harness-9ycy`) and its
  final commit carries `Closes-Bead: coding-harness-9ycy`.
- No live model experiment is required; offline stand-ins verify dispatch.
- Before the ADR edit, phase 1a meets the five-answer ADR-edit minimum; the
  one recorded answer is not duplicated or supplemented by agent answers.

## Open decisions

None open about intent; Q-1 supplies the authority and initial model choice.

- [DETAIL] Use `implement-route.yaml` and generic primary/retry route labels:
  a root YAML file fits existing declarations and labels must survive a model swap.
- [DETAIL] Keep the three-attempt policy in code and store model selections
  and their history in the file: configuration need not become executable policy.
- [DETAIL] Three hours of phase 4, including repairs, is the stop; no earlier
  appetite is stated in the supplied research or interview.
- [GAP] The interview gate requires five maintainer-answered records once
  this change edits its claimed ADR; `decisions.md` currently has one.
  Return this prerequisite to phase 1a before that bootstrap edit. This draft
  neither invents four answers nor treats ordinary-PR authority as a gate exemption.
