---
title: "ADR 0018 — Isolate writing attempts and publish validated results"
category: adr
status: accepted
created: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, isolation, containers]
---

# ADR 0018 — Isolate writing attempts and publish validated results

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, open is proposed and closed is rejected. Amends the
  writing-call boundary and failed-tree carry-over of ADR 0016/0017 and the
  interactive boundary of ADR 0012. Supersedes no entire ADR and amends no
  D- or O-number; their model routes and other proof contracts remain.
* Review: the maintainer chose a fresh container, limited inputs and API-only
  network with measured confinement, four writing verbs, confined reads,
  absorbed failed-run cleanup and Podman behind a configurable program in
  Q-1 to Q-5 of `plans/changes/isolated-attempts/decisions.md`, 2026-10-14.
  The architecture below is a proposal implementing those answers. Acceptance
  is the merge commit; no agent records approval in the pending header.
  Decider: maintainer · prepared by Codex.
* Date: 2026-10-14 · takes effect on merge.

## Context

Writing attempts currently edit the same worktree on which recovery and
verification operate. The preceding repair change accepts three limitations:
linked input parents or findings paths can redirect recovery outside the
worktree, and a directory in place of findings can prevent recovery and
diagnostics (phase-6 F-15 to F-17, collected in this change's research on
2026-10-14). CLI settings are configured rather than measured confinement.

The failed-run exploration additionally records that index rendering,
document stamps, formatting and route blocks survive failed post-checks and
block the next invocation (`c8b009b`, read from Git on 2026-10-14). Current
source at `36e4349` has a shared implementation/repair loop and a separate
draft loop, both requiring the same boundary. Running candidate-controlled
`make verify` on the host would leave an execution path outside that boundary.

The maintainer's five interview answers settle container isolation of all
four writing verbs and their reads, include failed-run cleanup in this change
and choose Podman as default with Docker/Apple substitution by configuration.

## Decision Drivers

* A model sees only its passed repository material and selected login.
* Reads, writes and API-only networking have live negative probes.
* A failed attempt cannot contaminate the next attempt or the host baseline.
* Host evidence remains durable without trusting model-controlled paths.
* The interactive return path preserves the lack of automatic session commits.
* Official clients, existing subscriptions, routes and proof rules remain.

## Considered Options

* **Private runtime volumes with validated publication** — removes host
  directory mounts and discards failed candidates; requires supervised export,
  verification, publication and interrupted-run recovery.
* **A container with a writable host copy** — easier inspection, but recovery
  still handles a host-visible namespace shaped by the model.
* **Disposable copies without a container** — isolates retry files, but does
  not provide the measured read/network boundary chosen in Q-1 and Q-3.
* **Further restoration-path patches** — smaller fixes, but preserve the
  fix-by-case class and cannot meet the chosen operating-system boundary.

## Decision

Chosen option: "Private runtime volumes with validated publication", because
it removes host paths from the writing process and recovery rather than
repairing each possible alias after the model has changed it.

1. Each `draft`, `implement`, `repair` attempt and interactive `session` has
   a fresh non-root container, private candidate and temporary home. The host
   Git directory, ignored state, sign-in homes and live tracker are absent;
   necessary Git history and tracker render are independent, checked inputs.
2. Podman is the default configurable container program. Docker and Apple
   `container` adapters owe the same capabilities and live qualification;
   missing prerequisites refuse the call, including Stage-1 fallbacks.
3. The official client receives only its endpoint's login. A private network
   and trusted proxy restrict external traffic to its declared API hosts;
   proxy variables alone are insufficient. Unqualified authentication or
   network requirements stop rather than silently widen the boundary.
4. Candidate preparation, formatting, gates and repair proofs run in a
   separate credential-free, network-disabled verifier. The host supervisor
   checks exported paths and bytes and never executes candidate code.
5. Retries start from the invocation baseline with accumulated diagnostics.
   Failed candidates and derived writes are discarded; only runner-owned
   failure evidence remains in the host change folder. This replaces the
   earlier failed-tree carry-over explicitly, including the absorbed cleanup.
6. After all verb-specific checks, validated files are published without
   following aliases and with baseline comparison and owned-write rollback.
   Automatic verbs make their one checkpoint; a normally completed interactive
   session publishes verified edits without making a host commit. Resource
   ownership records support cleanup after interruption without global pruning.
7. Live Podman boundary probes on macOS and Linux are required completion
   evidence. A changed backend/image/policy needs qualification before a real
   call. Model-call stand-ins do not prove runtime confinement.

## Consequences

* Setup now needs a container runtime, pinned client/verifier images and
  qualified login/API profiles. Startup and verification cost more time;
  no performance figure has been measured for this change.
* Interactive edits become visible in the host worktree after verified exit,
  and failed candidate trees are discarded rather than completed in place.
* Podman attempts share a machine VM where that backend uses one, as accepted
  in Q-5; this is not a per-attempt kernel-escape guarantee.
* The selected API can still receive readable call inputs and its login.
  No claim is made that allowed-provider exfiltration is prevented.
* Read-only Explore/review calls retain their documented limits; review roles,
  model efforts, client pins, loop budgets and billing authorizations do not
  change. The new boundary changes no subscription into an own integration.
* Host loss may leave private resources until recovery. Evidence distinguishes
  pending cleanup from completed cleanup and records no copied login value.

## Validation

* `plans/changes/isolated-attempts/plan.md` maps every criterion to a test or
  review and names the commands for stand-ins, live probes and `make verify`.
* A hosted blocking gate runs the production Podman launch probes with local
  test programs and synthetic login data, without a paid model call. The
  maintainer's Mac runs the same probes; reports identify commit, platform,
  runtime version and immutable image.
* Tests inject linked parents, findings-as-link/directory, unsafe exports,
  failed gates/format/preparation, retry contamination, concurrent edits,
  partial publication, interruption and checkpoint failure.
* Phase 6 reads this proposal against Q-1 to Q-5 and checks the file list and
  live evidence. Existing ADR bodies and the continuity map are unchanged.
