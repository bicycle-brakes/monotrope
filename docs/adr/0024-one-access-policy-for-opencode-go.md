---
title: "ADR 0024 — One access policy for OpenCode Go"
category: adr
status: accepted
created: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, opencode-go, destination-admission]
---

# ADR 0024 — One access policy for OpenCode Go

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, open is proposed and closed is rejected. Supplements
  ADR 0011's Go transport and ADR 0020's research-origin rule; amends no
  D- or O-number and supersedes no ADR.
* Review: the maintainer chose all-path central control, same-host path
  continuation with notice, agent path maintenance, an ADR of its own,
  and storage on the provider entry with orchestrator maintenance in
  Q-1–Q-5 of `plans/changes/go-access-point/decisions.md` on 2026-10-31.
  The feature's ADR answer is recorded as "yes" in
  `decisions/answers/go-access-point/adr.yaml`. Decider: maintainer ·
  prepared by Codex. Acceptance is the merge commit; the review header
  remains pending.
* Date: 2026-10-31 · takes effect on merge.

## Context

At `b126fce7`, inspected 2026-10-31, the research selector permits only
`https://opencode.ai/zen/go/v1`, while the review overlay activates catalog
addresses without a destination check. Research reproduced the former's
refusal of `/inference/go/v1`; the real-Pi contract expects a foreign host
to survive overlay activation. The two paths therefore disagree about
where the same provider may receive content (destination finding DL-B-8;
`plans/changes/go-access-point/research.md`).

The five interview answers require one rule for review, research, probes
and interactive launch, permit a new path on the admitted host with notice,
and let an agent maintain sourced same-host paths. The address record lives
on the `opencode-go` entry of `model-endpoints.yaml`. The runner holds that
whole file from foreign model attempts; the orchestrating session maintains
it, with no new maintainer approval for each documented same-host path
move. These directions are answered; this draft takes effect on merge.

## Decision Drivers

* A catalog must not choose an undeclared host for a key or change content.
* A same-host path move must not stop every swarm.
* All Go launches must agree without duplicating destination policy.
* Address maintenance must not grant model, terms or credential authority.
* The Go address component must fit the coming provider/model registry.

## Considered Options

* **Shared provider-entry policy and explicit Pi binding** — one rule,
  with cross-caller migration and orchestrator-owned record maintenance.
* **Separate writable address record** — attempts could update paths,
  but a second record splits provider governance; Q-5 chose the entry.
* **Repair only the research allow-list** — unblocks that selector but
  leaves review/probes/session destination trust inconsistent.
* **Require exact known paths everywhere** — refuses foreign hosts but
  contradicts the answered permission to continue after a same-host move.

## Decision

Chosen proposal: "Shared provider-entry policy and explicit Pi binding",
because it implements the five answered intentions at one destination
boundary and fits the future central registry without another model list.

1. Every runner-controlled Go launch uses one current provider address
   policy, including probes, retries and calls using saved selections.
2. Bases require HTTPS, the exact admitted host `opencode.ai` and the default
   port, with no credentials, query, fragment or ambiguous URL form.
3. A different path on that origin is preserved and visibly reported with
   the model and old/new paths. It does not update the known path by itself.
4. Missing bases use a recorded default for the resolved API; invalid bases
   and absent mappings never fall through to unchecked Pi defaults.
5. Agent maintenance of documented paths records source and reading date;
   changing the host, model permissions or terms is outside that delegation.
   The one record is the address part of the `opencode-go` entry in
   `model-endpoints.yaml`; the orchestrating session owns its edits.
   Foreign model attempts never edit it, and no held-path exemption is
   added. A catalog observation alone never updates the record.
6. Address admission supplements, rather than replaces, model terms,
   data-class, free-class, measured-API and leak checks.

## Consequences

* The review loop starts refusing foreign catalog targets it accepts today;
  research accepts legitimate same-host path moves it rejects today.
* One sourced record and explicit effective definitions replace divergent
  literals; launch evidence preserves path notices and raw catalog facts.
* A path update requires an orchestrator edit and a documentation reading;
  an implementation attempt cannot repair the held entry itself. The
  initial bootstrap must finish before Go launches can use the new policy.
* The boundary checks Pi's supplied destination. It does not confine HTTP
  redirects, DNS, arbitrary shell networking or later manual session switches.

## Validation

* The change's criterion ledger names deterministic policy, launch and
  saved-selection regressions, plus real pinned-Pi resolution contracts.
* `make verify` must pass; no live model traffic is needed in the tests.
* The interview and ADR-answer gates hold the five counted answers, the
  claimed ADR file and the already recorded "yes" answer; phase 6 checks
  the maintenance route against Q-3 and Q-5. Merge, not this draft,
  accepts the ADR.
