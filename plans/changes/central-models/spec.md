---
title: "Spec — central-models"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ylu
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, models, effort, routing, kit]
class: architectural
appetite: 8
adr_files:
  - docs/adr/0007-stage-2-reviews-by-codex-and-glm.md
  - docs/adr/0011-stage-2-reviews-through-opencode-go.md
  - docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md
  - docs/adr/0017-codex-repairs-taken-findings.md
  - docs/adr/0018-models-fill-configured-workflow-roles.md
---

# Spec — central-models

The maintainer can change the models and effort used by the workflow in one
repository setting, with its readers and documentation agreeing (bead
coding-harness-ylu). The evidence is in [research.md](research.md); the five
maintainer answers are in [decisions.md](decisions.md).

## Problem

- Permission and selection have separate authorities: the endpoint declaration
  lists permitted models, while six tuples in the runner choose models and
  effort. A disagreement is caught at call time rather than before a run
  (research, "The declaration" and "The call side", read 2026-10-14).
- Current selections are restated in two workflow tables, prompt headers and
  agent instructions. The display-name resolver guesses identifiers, effort
  has no common declaration, and the repository instructions escape that
  resolution check (research, "The prose copies" and "What is unclear",
  2026-10-14).
- Seven Claude Code agent definitions choose an older worker model, and the
  kit probe embeds that identifier in test names. Changing a selection entails
  changing unrelated assertions and probe bookkeeping (research, "The pins",
  2026-10-14).
- Permanent records bind models to roles, while the kit keeps the local
  declaration as repository inventory. There is no shared selection format for
  the four uses the maintainer requested (research, "Which files a change
  would have to touch"; decisions Q-3 to Q-5, 2026-10-14).

## Terms

**Role:** a workflow responsibility, such as drafting, repairing or reviewing;
its behavior survives a change of the model filling it.

**Selection:** an endpoint, an exact model identifier and an effort value;
an explicitly unspecified effort inherits the client's default.

**Ladder:** an ordered list of selections for a named review or research use;
endpoint permission lists do not imply execution order.

**Authoritative edit:** the maintainer's edit to the setting; generated files
may change afterward without becoming additional settings to maintain.

## Acceptance criteria

1. When a role is assigned another compatible, already permitted model in
   `model-endpoints.yaml`, its next selection uses that model without another
   authoritative edit.
   *Refuted by:* the old model is selected, or code, a prompt, an ADR or a test
   expectation needs a matching manual model edit.
2. When the supported effort of one role changes in the setting, that role's next call
   requests the changed effort.
   *Refuted by:* the call requests an old or another role's effort, or silently
   omits a configured value; the existing documented Pi clamp remains allowed.
3. When a runner attempt becomes due under the existing retry or explicit
   Stage-1 rules, its selection comes from that verb's configured binding.
   *Refuted by:* a primary, retry or fallback uses an identifier or effort
   embedded in runner code instead of the binding.
4. If a selection cannot be resolved to a permitted model on a supported
   transport for its role, the consumer refuses it before a model starts.
   *Refuted by:* an unknown endpoint or model, absent clearance or residency,
   or an incompatible client or effort launches or silently selects a default.
5. If the central setting is missing, unreadable, malformed or ambiguous, its
   consumers report why it cannot be used.
   *Refuted by:* duplicate keys, invalid references, an absent required binding
   or a bad value produce a silent default, a green gate or an uncaught error.
6. When a new Claude Code session reads regenerated agent definitions, each
   agent's model and optional effort match its central binding.
   *Refuted by:* changing that binding leaves any of the seven native
   definitions on a stale model or effort, or rewrites its tools or job text.
7. When a named configured ladder is read, its selections follow that
   ladder's configured order independently of endpoint permission-list order.
   *Refuted by:* the loop, probe or swarm selector derives order from
   `endpunkte[].modelle`, or a research and review ladder cannot differ.
8. If a future swarm ladder is explicitly unconfigured, selecting it reports
   that state without inventing members.
   *Refuted by:* the selector substitutes the existing loop, authorizes a free
   model, or starts a swarm; configuring permitted members does not resolve it.
9. When the maintainer asks for an interactive-session suggestion, it reports
   the configured default selection without launching a session.
   *Refuted by:* the suggestion is stale or starts a client; an explicit
   `session --model` is overridden or the existing explicit-model duty is lost.
10. When the routing views are generated, both workflow routing tables show
    the models, effort and alternatives resolved from the central setting.
    *Refuted by:* a valid selection change leaves a stale table, or generating
    twice changes the output or overwrites prose outside the marked tables.
11. While phase prompts and repository instructions describe current routing,
    they refer to central roles rather than repeat concrete selections.
    *Refuted by:* a live model or effort choice remains independently editable
    there, or a prompt names a role the reader cannot resolve.
12. If a generated routing view or agent selection differs from the setting,
    the routing gate makes local verification and hosted CI red.
    *Refuted by:* an edited generated value or a deleted marker passes the
    check, or the gate is absent from either verification path.
13. When the maintainer merges a later change solely to a compatible model,
    effort or ladder binding, the role contracts require no ADR amendment
    solely because that selection changed.
    *Refuted by:* an effective ADR still fixes that identifier or effort, or a
    binding-only change requires another manually maintained selection file.
14. When the kit transfers the routing capability, it includes the format,
    runnable readers, runner and table generator with an unconfigured template
    carrying role and effort defaults rather than this repository's approvals.
    *Refuted by:* the bundle has a missing dependency, uses the source
    repository's live bindings, or grants a target an endpoint/data clearance.
15. When a run report checks selections at a specified repository revision,
    it resolves that revision's central setting.
    *Refuted by:* editing the working setting changes the report for the old
    revision, importing the report requires removed runner constants, or
    historical audit lines cease to be counted.
16. While selections are migrated to the central setting, the existing
    execution and safety contracts continue to hold.
    *Refuted by:* a retry count or failure trigger changes, a leak refusal
    falls back, a repair reuses a review context, a review gains writes, or the
    three-round limit and conditional third round change.

## Non-goals

- Selecting new providers or clearing additional models or data classes;
  publication of prices, terms or residency research is separate work.
- Implementing the research or review swarms, deciding their membership, or
  changing their planned orchestration; their consumers will use this format
  when those changes land (coding-harness-icw, coding-harness-4fk).
- Changing today's model assignments or efforts, including upgrading the
  seven agent pins or adopting the separately recorded effort-per-verb change.
- Replacing CLI transports, retry policy, class routing, evidence rules,
  sandbox boundaries, session approval policy or review independence rules.
- Shared settings across repositories, a general harness extension, hot
  reloading an already running session, or installing into another repository.

## Protected areas

- Endpoint operators, billing, residency, permissions and credentials remain
  unchanged; selecting a permitted model is not permission to send new data.
- `scripts/leakcheck.py`, `scripts/stage2_session_policy.mjs` and the
  approval/sandbox settings retain their enforcement behavior.
- Historical plans, interview answers and run records retain their evidence;
  existing ledger-referenced test functions remain available.
- `tools/claude-code/`, customer repositories and user configuration are
  outside this workflow-selection change.

## Definition of Done

- `make verify` and the hosted checks are green; all criterion-ledger tests
  have been written and the routing generator's check passes.
- Moved in the same decision pull request: `model-endpoints.yaml`,
  `docs/WORKFLOW.md`, `AGENTS.md`, all twelve phase/job prompts, the seven
  agent definitions, the kit manifests and template, and the five ADR files
  claimed above; the plan names the code, tests and generated CI changes.
- Protected areas are preserved and non-goals unbuilt, shown by the PR file
  list and phase-6 review against this spec.
- The PR closes the tracking item and its final commit carries
  `Closes-Bead: coding-harness-ylu`; only the maintainer's merge accepts ADR 0018.
- Special runs: fixture-backed selection changes across two independent
  repositories and two revisions, with commands and implementation commit in
  the PR body. No live provider call is required or claimed.

## Open decisions

None open. The maintainer's Q-1 to Q-5 settle source, documentation, role
contracts, scope and repository-local values; no ADR answer is written here.

- [DETAIL] Classify this as architectural: the shared resolver replaces the
  runner's exported selection interface and serves four kinds of consumer.
- [DETAIL] Preserve the selections observed at `e048fa4`, including the older
  agent worker; centralization is not an unrequested model upgrade.
- [DETAIL] Keep a dedicated loop ladder and explicit unconfigured research
  and review swarm ladders: no approved swarm membership exists in this tree.
- [DETAIL] Generate only native agent selection fields and marked table
  blocks; the setting stays the only input and the existing agent jobs survive.
- [DETAIL] Suggest the existing final-review author profile for interactive
  sessions because its endpoint already has a supported session transport;
  the suggestion starts no call and leaves effort unspecified initially.
- [DETAIL] Set the implementation appetite to eight hours, repairs included;
  stop with a handover if it is consumed, rather than widen this change.

These reversible details are chosen by the drafting agent for the reasons
above. The missing artefact validator is a repository gap recorded in the
research addendum, not a reason to invent a maintainer decision.
