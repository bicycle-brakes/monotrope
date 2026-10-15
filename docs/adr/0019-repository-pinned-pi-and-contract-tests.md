---
title: "ADR 0019 — The runner owns its pinned Pi and measures it with offline contracts"
category: adr
status: accepted
created: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage2, pi, toolchain]
---

# ADR 0019 — The runner owns its pinned Pi and measures it with offline contracts

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open is
  proposed, closed is rejected. Amends ADR 0011 decision 6 and ADR 0012's Pi
  version and launcher assumptions; supersedes no ADR and amends no D-/O-number.
* Review: direction stated by the maintainer on 2026-10-15, recorded in the six
  interview answers for the runner's own pinned Pi (bead coding-harness-agx,
  `plans/changes/pi-pin/decisions.md`). The acceptance is the merge commit and
  is written nowhere else; no agent records that merge as already approved.
  Decider: maintainer · prepared by Codex.
* Date: 2026-10-15 · takes effect on merge

## Context

ADR 0011 decision 6 ties reviewer isolation to the manual Pi 1.1.0 measurement
of 2026-10-08. The runner checks that version but finds Pi through PATH. A global
update to 1.2.0 stopped calls on 2026-10-15; the interactive path also resolves
global Pi. Existing tests simulate the CLI or the extension API and cannot show
whether the installed Pi honours the flags and tool contracts
(`plans/changes/pi-pin/research.md`, read 2026-10-15).

The maintainer chose a repository-local npm install, real offline contracts
locally and in CI, the same wrapper for sessions, and a measured Node major
(Q-1, Q-2, Q-4 and Q-5). After Zen's free-tier refusal, Q-3 narrows live use to
Go with offline coverage of Zen's provider; Q-6 requests this amendment.

## Decision Drivers

* Global updates must not select the runner's executable.
* Dependency integrity and relied-on Pi behaviour must be reproducible.
* A version move must measure the real program, not only expected arguments.
* Existing credential, declaration and residual-risk boundaries must hold.

## Considered Options

* Repository-local npm install with lock, wrapper and real contracts locally
  and in CI: repeatable measurements, with Node and package provisioning owed.
* A versioned global binary: isolates one version but leaves transitive
  dependencies and machine setup outside the repository lock.
* Global Pi and renewed manual measurements: little setup, but the failure
  caused by an unrelated global update remains possible.
* Local-only contracts: avoids CI setup but cannot gate a version move in CI.

## Decision

Chosen option: "Repository-local npm install with real offline contracts",
because it separates the runner from global updates and makes the original
isolation measurement repeatable on every proposed version change.

1. `tools/pi/package.json` holds the exact Pi dependency; its npm lock records
   the dependency graph and integrity values. `tools/pi/install.sh` uses
   `npm ci --ignore-scripts`. No installed dependencies are committed.
2. Every runner Pi path, including loop/probe and interactive-session preflight,
   extension confirmation and dispatch, uses `tools/pi/pi`. The wrapper refuses
   a missing or mismatched local install and never installs or falls back globally.
3. `tools/pi/.node-version` holds the exact CI Node version. The wrapper refuses
   another major locally; minor/patch moves within that major remain eligible
   for the same contracts. Pi and Node changes are proposed in pull requests.
4. The suite starts real pinned Pi with synthetic credentials and a loopback
   model stand-in, locally and in CI. It holds reviewer tool declarations and
   refusal, suppression of discovered extension/MCP startup and skill/prompt/theme
   reads, context-file exclusion and scratch-agent separation from ambient auth
   and command-valued model configuration, extension input/results, the production session
   policy's foreign-read blocking, model-list table and Go/Zen provider address
   and key mapping. Missing prerequisites fail rather than skip these contracts.
5. This replaces the requirement to repeat a manual measurement alone when the
   pin moves; the manual Pi 1.1.0 findings remain historical evidence. The normal
   verification gates and real contracts must pass before a version move ships.
6. Authentication boundaries stay as decided: scratch reviewer configuration
   and Go key only in `OPENCODE_API_KEY`; interactive sessions sign in from the
   maintainer's own Pi agent directory. No paid Zen endpoint is enabled here.

## Consequences

* Fresh clones and CI provision Node and install locked npm packages before
  verification; installation needs registry access, contract execution does not.
* Reviewers still have unconfined read/search tools. Discovery isolation is not
  a filesystem sandbox; the accepted residual read risk of ADR 0011 remains.
* Session file tools retain their policy boundary; shell/network residual risks
  and user-agent configuration caveats of ADR 0012 remain unchanged.
* Offline Zen coverage proves a client contract, not paid service access or an
  exception to the free-tier refusal. Later live use needs its own declaration.
* There is no scheduled updater; a version move is a reviewed manifest/lock
  change, plus a Node declaration change when needed.

## Validation

* The criterion ledger in `plans/changes/pi-pin/plan.md` names real-Pi contracts,
  wrapper/installer faults and runner/session launch regressions.
* CI installs the exact Node declaration and the same locked Pi as local setup;
  `make verify` includes contracts through pytest and must fail on missing Pi.
* Phase 6 checks current guidance and unchanged historical ADRs/permissions.
  Implementation and test execution are outstanding at draft time, 2026-10-15;
  neither compatibility nor adoption is asserted by this proposal.
