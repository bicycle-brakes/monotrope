---
title: "ADR 0018 — The kit installs from a pinned source commit"
category: adr
status: accepted
created: 2026-10-13
last_reviewed: 2026-10-14
updated: 2026-10-14
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, kit, install, report, ownership]
---

# ADR 0018 — The kit installs from a pinned source commit

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open is
  proposed, closed is rejected. Amends no numbered decision and supersedes
  no ADR.
* Review: direction chosen by the maintainer in the six interview answers
  of 2026-10-13 (`plans/changes/kit-install/decisions.md`, Q-1 through Q-6).
  The 2026-10-14 redraft incorporates the recorded phase-2a rulings; it does
  not supply another maintainer answer. Acceptance is the merge commit and
  is written nowhere else; the header's review remains pending. Decider:
  maintainer · prepared by Codex.
* Date: 2026-10-13 · takes effect on merge.

## Context

The kit measures portability but has no installer, comparison command or
stored source baseline. Its role manifest separates unchanged mechanism from
source inventory; the independent export manifest answers a different
migration question. Neither records which source commit an instance received
(research §§1 and 4, coding-harness `3199a28`, 2026-10-13).

An existing instance has deliberately adapted the workflow. Of the 83 source
kit paths measured at that cut-off, lakeswitch-ai `ce88eee` has none identical,
three edited and 80 missing. Its gates, lint rules and decision pull request
template belong to the instance despite sharing filenames (research §§2–3,
2026-10-13).

The maintainer chose fresh repositories first, comparison and gradual
adoption for existing instances, a source pin, target-owned starting templates
and verified changes left uncommitted. After phase 2a the maintainer split
installation, report and lock from the later update command. This PR delivers
only that first part; the durable direction for updates remains recorded
below (decisions Q-1 through Q-6, 2026-10-13; follow-up coding-harness-66q).

## Decision Drivers

* Deliver a usable first installation without displacing an existing
  instance's implementation or protected configuration.
* Identify a source commit and ownership so future updates have an honest
  baseline rather than inferred history.
* Keep instance configuration under the instance's ownership.
* Preserve target review and merge as the acceptance boundary (ADR 0008).
* Deliver install/report independently of update and release construction.

## Considered Options

* A pinned source commit with target-owned initial templates: identify
  provenance now and give future updates a baseline for preserving edits.
* A three-way merge: combine local and source changes, requiring trustworthy
  historical bases and responsibility for conflict resolution.
* A vendored kit folder: isolate source bytes, requiring another location,
  provenance policy and integration with each target's runner.
* Replacing an existing instance immediately: unify the mechanism sooner
  while displacing adaptations before their separate adoption review.

## Decision

Chosen option: "Pinned installation and target-owned initial templates",
because it makes delivery traceable while preserving instance configuration,
local work and the target's review boundary.

1. Install first into fresh repositories. An existing instance receives a
   comparison report showing missing and differing exact paths, at named
   source and target commits, and adopts through its own changes (Q-1).
2. Record the source origin URL and full kit commit in `harness.lock.yaml`,
   with installed paths, ownership and byte/mode baselines. The target has an
   explicit source pin rather than a branch name or machine-local fallback.
3. Give starting configuration a `template` role. The gates, lint rules and
   decision pull request template, plus the Makefile and dependency
   declaration required for verification, belong to the target after install.
   CI is derived from the target gate file rather than copied as a kit file.
4. Write payload and lock, run target `make verify`, and leave changes
   uncommitted for a person or session to review in the target's pull request.
   Verification failure stays a failed result with the application available
   for review; application I/O failure restores its own writes (Q-4).
5. Deliver install, comparison and lock in this change; implement `kit update`
   separately (Q-6). Q-2/Q-3 remain its direction: update obtains the selected
   source version, changes only kit-owned files, reports local edits instead
   of overwriting them, and never rewrites initial templates. Collision,
   retry, source migration and partial-pin behavior are not decided here.
6. This record takes effect only through the maintainer's decision PR merge
   (Q-5 and ADR 0008).

The freshness allowlist, starter recipes, lock encoding, command options,
transport staging and rollback implementation are the recorded phase-2a
rulings and proposed design details, not invented maintainer answers.

## Consequences

* Installed files have traceable provenance and explicit ownership before
  any automatic update capability is delivered.
* Initial template improvements reach an existing instance manually or
  through comparison; they do not acquire kit ownership because they differ.
* Existing instances keep responsibility for their adaptations, protected
  settings and gradual adoption. The first installer deliberately refuses
  populated and already pinned targets.
* A source pin describes applied provenance, not verification approval or
  merge acceptance. Red verification leaves an uncommitted result to review.
* The update follow-up must resolve its own remaining ambiguities; this PR
  does not claim update safety or partial-update bookkeeping is implemented.
* Agent, provenance, tracker, endpoint and runtime setup remain outside this
  installation, as do the independent export policy and release builder.

## Validation

* Fresh-install integration exercises actual target `make verify` with all
  four allowed root names in its initial commit, an untracked payload and a
  target environment isolated from source overrides and PATH entries; the
  fixture commits the payload and proves target verification again.
* Install regressions hold committed bytes/modes, template/derived ownership,
  freshness refusals, collisions, complete lock records and rollback on I/O
  failures.
* Report regressions hold exact Git-tree states to named commits and prove
  target files/Git state stay unchanged, including dirty working trees.
* The probe measures the same initialized payload as an empty fresh install,
  including starters, derived CI, scaffolds and lock, without growing its
  exceptions or cap. Every added/changed skip is explicitly scoped and listed;
  its source case still runs. Source `make verify` and the criterion ledger
  pass before the decision PR is ready.
* Phase 6 measures against the revised install/report spec; update validation
  belongs to the follow-up. The maintainer's merge confirms this record;
  the drafting model writes no approval or ADR answer.
