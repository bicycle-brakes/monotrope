---
title: "ADR 0018 — The kit installs and updates by a pinned source commit"
category: adr
status: accepted
created: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, kit, install, update, ownership]
---

# ADR 0018 — The kit installs and updates by a pinned source commit

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open is
  proposed, closed is rejected. Amends no numbered decision and supersedes
  no ADR.
* Review: direction chosen by the maintainer in the five interview answers
  of 2026-10-13 (`plans/changes/kit-install/decisions.md`, Q-1 through Q-5).
  Acceptance is the merge commit and is written nowhere else; the header's
  review remains pending. Decider: maintainer · prepared by Codex.
* Date: 2026-10-13 · takes effect on merge.

## Context

The kit measures which workflow files can travel but has no install/update
command or stored source baseline. Its role manifest treats unchanged
mechanism and source inventory separately; its independent legacy export
manifest answers a different migration question. Neither currently records
which source commit an instance received (research §§1 and 4,
coding-harness `3199a28`, 2026-10-13).

An existing instance has deliberately reimplemented and adapted the workflow.
Of the 83 kit files measured at that source commit, lakeswitch-ai `ce88eee`
has none identical, three edited and 80 absent at the source paths. Its gate
list, lint configuration and decision pull request template belong to that
instance despite sharing source filenames (research §§2–3, 2026-10-13).

The maintainer chose fresh repositories first, incremental adoption for
existing instances, a pinned version, a separate template role, and verified
changes left uncommitted. The maintainer also requested this durable record
because the rules bind future instances and the target's planned lock
(`plans/changes/kit-install/decisions.md`, Q-1 through Q-5, 2026-10-13).

## Decision Drivers

* Deliver a usable installation without forcing an existing instance to
  discard its own implementation.
* Identify the source version and preserve local edits during updates.
* Keep instance configuration under the instance's ownership.
* Preserve the target's review and merge as the acceptance boundary
  (ADR 0008).
* Provide a distribution contract the future release builder can use.

## Considered Options

* A pinned source commit with unchanged kit files updated automatically and
  local edits reported: traceable updates with explicit manual conflict work.
* A three-way merge: combine target edits with upstream changes, requiring
  reliable historical bases and responsibility for conflict resolution.
* A vendored kit folder: isolate source bytes, requiring another location,
  target provenance policy and integration with the target's own runners.
* Replacing the existing instance immediately: unify the mechanism sooner,
  while displacing adaptations before their separate adoption review.

## Decision

Chosen option: "Pinned source commit and target-owned initial templates",
because it makes improvements traceable while preserving the instance's
configuration, local work and review boundary.

1. Install first into fresh repositories. An existing instance receives a
   comparison report showing missing and differing paths and adopts the
   workflow in changes of its own; installation is not a forced conversion
   (Q-1).
2. Record the source kit commit in `harness.lock.yaml`. Update acquires the
   selected new version, changes only kit-owned files and reports locally
   changed kit paths instead of overwriting them. The changed path waits
   for resolution by its owner (Q-2).
3. Give initial configuration a `template` role in the kit manifest. The
   gates file, lint configuration and decision pull request template are
   shipped as first-install starting content. Afterwards they belong to
   the target and update never writes them (Q-3).
4. Write the payload and lock, run the target's `make verify`, and leave
   changes uncommitted. A person or session reviews the result and brings
   it into the target through its own pull request. The tool does not
   automatically commit an install or update (Q-4).
5. Record these distribution rules in this ADR, whose decision PR becomes
   effective only through the maintainer's merge (Q-5 and ADR 0008).

Per-file baselines, partial-update bookkeeping, bootstrap recipe fields,
command options and transport staging are implementation details documented
in the change's design, not further maintainer answers.

## Consequences

* Every installed kit file has traceable provenance; update can distinguish
  an unchanged file from a target edit without inventing a historical base.
* A locally changed kit file requires deliberate resolution; safe files can
  progress only with bookkeeping that makes the remaining conflict visible.
* Improvements to an initial template reach an existing instance manually
  or through a comparison report, not through automatic updates.
* An existing instance benefits gradually and retains responsibility for its
  own adaptations, protected files and verification configuration.
* Verification failure remains a failed result with changes available for
  review; neither a lock nor the install command replaces review and merge.
* The independent export policy and runtime/tracker setup are not decided
  again by this record.

## Validation

* Installer integration tests exercise a real fresh-target `make verify`,
  resolved source bytes, file ownership and uncommitted results.
* Update regressions cover unchanged replacement, local edits and deletion,
  retired files, preserved templates and truthful partial-update baselines.
* Report regressions hold missing/identical/different states to named source
  and target commits and prove that target files and Git state do not change.
* Source `make verify` and the criterion ledger are green before the decision
  PR is ready; phase 6 checks the implementation against the revised spec.
* The maintainer's decision PR merge confirms this record; no approval or
  ADR-answer file is authored by the drafting model.
