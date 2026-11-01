---
title: "Spec — go-access-point"
status: draft
implementation_status: partial
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-4tr4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, opencode-go]
class: feature
appetite: 6
change: go-access-point
adr_question: {proposed: "yes", reason: "The shared Go destination policy is a data-flow boundary beside ADR 0020, as the maintainer answered in Q-4."}
adr_files: [docs/adr/0024-one-access-policy-for-opencode-go.md]
neighbours:
  - plans/changes/review-loop-deep-b/spec.md
  - plans/changes/pi-catalog-redirect/spec.md
  - plans/changes/research-swarm/spec.md
  - plans/changes/pi-pin/spec.md
  - plans/changes/kimi-admission/spec.md
  - plans/changes/terms-expiry/spec.md
---

# Spec — go-access-point

Every runner-controlled OpenCode Go launch — review loop, research swarm,
availability probes and the interactive session — reads its admitted address
from one record and follows one policy: a different path on the admitted host
runs on with a notice, any other destination is refused before a model
request (bead `coding-harness-4tr4` — the central Go access point).
Research: `research.md`. Intent: `decisions.md`, answers Q-1–Q-5.

This is a proposed, unimplemented specification at `b126fce7`, inspected
2026-10-31. The maintainer chose an architecture decision record (ADR) in
Q-4 and the provider-entry storage with orchestrator maintenance in Q-5.
The existing draft `docs/adr/0024-one-access-policy-for-opencode-go.md`
belongs to this change; its acceptance still requires the maintainer's
merge. The recorded feature ADR answer is already "yes"; this draft does
not change that answer.

## Problem

- The research selector recognises only `/zen/go/v1`, while the refreshed
  catalog carries `/inference/go/v1`; the offline reproduction rejects
  otherwise identical models on that path alone, so the research swarm
  cannot run (`research.md`, Haiku report §§1–2, 2026-10-31).
- The review overlay copies a catalog's `baseUrl` unchecked. The pinned Pi
  contract even expects a foreign host to survive activation: the catalog
  can choose where a change's diff and its key go — the destination finding
  DL-B-8 (`research.md`, "What exists today" and Haiku report §3,
  2026-10-31).
- Research launch defaults and interactive launch resolution carry their own
  literals or none; three Go paths hold two opinions about the same fact,
  and no machine-readable Go address record exists (`research.md`,
  inventories, 2026-10-31).
- The maintainer has authorised agent maintenance of documented same-host
  paths, but `model-endpoints.yaml` is held from stage-2 attempt commits, so
  the change must name the route by which the agent maintains the record
  (`decisions.md#Q-3`; `decisions.md#Q-5` settles the orchestrator route).

## Terms

- **Address record:** the address part of the `opencode-go` entry in
  `model-endpoints.yaml` — the admitted host and, per wire API, the known
  base with its source and source-reading date; it holds no credentials and
  no model permissions.
- **Effective base:** the concrete `baseUrl` and wire API Pi will use for
  the selected model after permitted defaults and overrides resolve.
- **Known path:** a base recorded for that wire API; matching tolerates one
  trailing slash and an explicit default HTTPS port.
- **Go launch:** a review member, a probe, a research seat or the initial
  model of an interactive session started through `scripts/stage2.py`.

## Acceptance criteria

1. When any Go launch assesses its destination, it uses the same address
   record and the same admission policy.
   *Refuted by:* changing the record affects one swarm but not the other, a
   probe or an interactive launch, or a caller keeps its own Go origin rule
   or missing-address default.
   *Basis:* decisions.md#Q-1; decisions.md#Q-5.
2. If an effective base is not an unambiguous HTTPS URL on the admitted
   host `opencode.ai`, with the default port and without credentials, query
   or fragment, that destination is refused before a model request.
   *Refuted by:* a foreign host, subdomain, host-suffix trick, userinfo,
   plain HTTP, non-default port, query, fragment, malformed authority,
   control character or backslash reaches a model request.
   *Basis:* decisions.md#Q-2.
3. When an otherwise eligible model names another path on the admitted
   host, its effective base is preserved and a visible notice names the
   model, the recorded path and the observed path.
   *Refuted by:* `/inference/go/v1` is refused solely for differing from
   `/zen/go/v1`, silently replaced, or used without that notice.
   *Basis:* decisions.md#Q-2.
4. If a selected definition omits its base, the effective base is explicit
   and comes from the record for its resolved wire API.
   *Refuted by:* Pi supplies a shipped or ambient default after validation,
   an explicit invalid base is treated as absent, or a missing API mapping
   permits a guessed default.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.
5. When a catalog row has a refused destination, it cannot become a
   dispatchable selection through filtering or fallback.
   *Refuted by:* dropping the row lets the same id's shipped definition
   run, one bad row needlessly excludes unrelated valid candidates, or an
   empty admitted set is reported as a clean review round.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.
6. When a Go model request is about to start, its effective base is checked
   against current policy regardless of earlier selection evidence.
   *Refuted by:* an old receipt, saved overlay, resumed round, replacement,
   probe retry or malformed-answer retry dispatches a currently refused
   destination; refusing it rewrites earlier completed-round history.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.
7. When an interactive Go session starts, its selected model uses the
   checked effective base despite ambient model configuration.
   *Refuted by:* the terminal receives a launch whose selected model can
   resolve to another base, or enforcing the check reads, copies or writes
   the user's saved credentials in runner-owned files.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.
8. If the address record is missing, unreadable or ambiguous, Go admission
   fails with a diagnostic identifying the unusable record.
   *Refuted by:* duplicate keys, an invalid host, an invalid dated source
   or a malformed API mapping silently activate a literal or cached policy.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3; decisions.md#Q-5.
9. When an agent records a documented same-host path change, the record
   gains the new path with its source and actual source-reading date,
   without a new maintainer approval step for that path move.
   *Refuted by:* the documented maintenance route needs a new human answer
   for each move, a catalog observation alone counts as a source reading,
   or path maintenance changes the admitted host, credentials, model
   permissions or terms.
   *Basis:* decisions.md#Q-3; decisions.md#Q-5.
10. While address admission applies, all existing independent model, terms,
    data-class, measured-wire-API and leak restrictions still apply.
    *Refuted by:* an admitted address admits an unread paid model or an
    unmeasured research wire API, broadens the free class's input or tools,
    or turns a leak refusal into a fallback call.
    *Basis:* decisions.md#Q-1; decisions.md#Q-2.
11. When address admission reports a path move or a refusal, its diagnostic
    stays available in the operation's existing audit evidence without
    exposing a credential-bearing URL.
    *Refuted by:* only transient console output explains a launched path
    move, a refused model is unnamed, raw userinfo or query secrets enter a
    diagnostic, or admission rewrites raw catalog evidence as if it had
    always contained the admitted default.
    *Basis:* decisions.md#Q-1; decisions.md#Q-2.

## Non-goals

- The general model registry, phase and model routing, the catalog sources
  (`pi.dev`, `models.dev`) and their redirect handling: this change is the
  Go address part of that future registry, not another model list
  (`decisions.md`, details).
- New models, terms renewal, price changes, new measured wire APIs, Pi
  upgrades, credentials management, background scraping, or the record
  rewriting itself from a catalog refresh.
- No earlier ADR is rewritten: ADR 0011's recorded history, including its
  zen address readings, stays as history; ADR 0024 alone records the new
  boundary and the maintenance route chosen in Q-4 and Q-5.
- No lifting of the runner's held-path guard: the address record is
  maintained through the orchestrator route the workflow already defines,
  not by exempting `model-endpoints.yaml` from the hold.

### Boundary

The boundary is the effective destination handed to the pinned Pi for a
runner-controlled launch, including each headless retry. It is not network
confinement: HTTP redirects after dispatch, DNS or provider compromise,
shell network programs and later manual model switches inside an
interactive session stay outside it. No claim is made that all traffic can
reach only this host. Interactive authentication remains Pi-owned; the
runner binds the initial model without inspecting the user's credentials.

## Protected areas

- `scripts/stage2_research_catalog.mjs` and its source and redirect policy:
  catalog acquisition is the merged neighbour `pi-catalog-redirect`.
- Files under `docs/adr/` other than this change's ADR 0024 draft,
  `decisions/answers/`,
  `decisions/gates.yaml`, `provenance.yaml`, endpoint secrets and the
  model and terms declarations: no historical rewrite, no invented answer,
  no permission widening.
- `model-endpoints.yaml`: the stage-2 attempt never edits it; its edits are
  orchestrator steps in this change's plan, the workflow's route for held
  paths.
- The customer-instance boundary and the Pi manifest and lock stay
  unchanged.

## Definition of Done

- `make verify` green; the runner owns the check and the commit.
- Moved in the same pull request: the address record on the `opencode-go`
  entry of `model-endpoints.yaml` and the refreshed address prose in its
  `bemerkung` (orchestrator edits), one paragraph in `docs/WORKFLOW.md`,
  `docs/adr/0024-one-access-policy-for-opencode-go.md`, and this change's
  artifacts. The ADR makes this a decision pull request; it takes effect
  only on the maintainer's merge.
- The protected areas untouched and the non-goals unbuilt, shown by the
  pull request's file list.
- The pull request closes bead `coding-harness-4tr4`; its final commit
  carries the trailer `Closes-Bead: coding-harness-4tr4`.
- Special runs: none — no live model call belongs in the tests; the initial
  record values need one fresh reading of the Go page, part of the
  orchestrator step.

## Open decisions

None open. The details below were decided while drafting; each carries its
reason.

**Settled by the maintainer:** Q-4 requires ADR 0024; Q-5 places the
record on the `opencode-go` entry of `model-endpoints.yaml` and every edit
of that held file with the orchestrator. These answers supersede the
earlier draft's "no ADR" and separate-record alternatives; neither is an
open decision or an agent-chosen detail.

[DETAIL] **The phase-4 appetite is six hours, repairs included**, chosen as
a visible stop for the cross-caller migration; neither research nor the
interview supplies a different limit.

[DETAIL] **Strict URL parsing keeps the swarm's existing safeguards**
— default HTTPS port, no userinfo, query or fragment, no parser-confusing
characters — and relaxes only its path equality, exactly as Q-2 requires.

[DETAIL] **The record's field names follow `model-endpoints.yaml`** —
German keys beside English technical terms, dated sources per value, as
`modelle_terms` already does. The names are freely revisable in phase 4.

No phase-2a rows existed in `findings.md` on 2026-10-31; nothing was open
to work in.
