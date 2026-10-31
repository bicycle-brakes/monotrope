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
  continuation with notice, and agent path maintenance in Q-1–Q-3 of
  `plans/changes/go-access-point/decisions.md` on 2026-10-31. Record placement
  remains undecided, two further counted interview answers are owed, and
  the feature's ADR answer has not been recorded. This draft settles none
  of those. Decider: maintainer · prepared by Codex. Acceptance is the merge
  commit; the review header remains pending.
* Date: 2026-10-31 · takes effect on merge.

## Context

At `2f240d90`, inspected 2026-10-31, the research selector permits only
`https://opencode.ai/zen/go/v1`, while the review overlay activates catalog
addresses without a destination check. Research reproduced the former's
refusal of `/inference/go/v1`; the real-Pi contract expects a foreign host
to survive overlay activation. The two paths therefore disagree about
where the same provider may receive content (destination finding DL-B-8;
`plans/changes/go-access-point/research.md`).

The three interview answers require one rule for review, research, probes
and interactive launch, permit a new path on the admitted host with notice,
and let an agent maintain sourced same-host paths. The current runner holds
the whole provider declaration file; the proposed storage/permission choice
must be answered before that maintenance route is implemented.

## Decision Drivers

* A catalog must not choose an undeclared host for a key or change content.
* A same-host path move must not stop every swarm.
* All Go launches must agree without duplicating destination policy.
* Address maintenance must not grant model, terms or credential authority.
* The Go address component must fit the coming provider/model registry.

## Considered Options

* **Shared registry-backed policy and explicit Pi binding** — one rule,
  with cross-caller migration and a separate storage decision.
* **Repair only the research allow-list** — unblocks that selector but
  leaves review/probes/session destination trust inconsistent.
* **Require exact known paths everywhere** — refuses foreign hosts but
  contradicts the answered permission to continue after a same-host move.

## Decision

Chosen proposal: "Shared registry-backed policy and explicit Pi binding",
because it implements the three answered intentions at one destination
boundary. The storage branch remains conditional on the spec's open decision.

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
   Under the proposed separate-record option, the held provider entry owns
   the admitted host and record reference; the writable record cannot
   override either. This storage arrangement still awaits the maintainer.
6. Address admission supplements, rather than replaces, model terms,
   data-class, free-class, measured-API and leak checks.

## Consequences

* The review loop starts refusing foreign catalog targets it accepts today;
  research accepts legitimate same-host path moves it rejects today.
* One sourced record and explicit effective definitions replace divergent
  literals; launch evidence preserves path notices and raw catalog facts.
* The storage choice must provide agent maintenance without silently
  bypassing the runner's held-path guard. No broad guard exemption is made.
* The boundary checks Pi's supplied destination. It does not confine HTTP
  redirects, DNS, arbitrary shell networking or later manual session switches.

## Validation

* The change's criterion ledger names deterministic policy, launch and
  saved-selection regressions, plus real pinned-Pi resolution contracts.
* `make verify` must pass; no live model traffic is needed in the tests.
* Before finalisation, the interview minimum is five counted answers, the
  storage decision is answered, and the authorised procedure records the
  maintainer's feature ADR answer. Merge, not this draft, accepts the ADR.
