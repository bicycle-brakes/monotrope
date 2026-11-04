---
title: "Spec — research-store-home"
status: draft
implementation_status: none
date: 2026-11-04
last_reviewed: 2026-11-05
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-nxdy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-swarm, state-store]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — research-store-home

The research swarm can use a store outside the inherited home directory without
moving the machine-wide verification queue (bead coding-harness-nxdy).
Research: `research.md`. Maintainer's answer: `decisions.md#Q-1`.

## Problem

At commit `a06da805` (2026-11-04), the research store, review-loop records and
verification admission all derive their location from `XDG_STATE_HOME`.
Without it, the store defaults beneath HOME and the existing placement guard
refuses the run. Moving that shared variable outside HOME makes research work,
but also moves the verification queue: differently configured lanes can then
hold different verification locks. These facts and the three path-computing
functions are recorded in `research.md`, “What exists today”.

The maintainer chose a separate research-store variable with a documented
default outside HOME, leaving verification admission where it is
(`decisions.md#Q-1`). This changes the setup needed by the earlier home guard,
while retaining its exclusion of stores beneath the inherited HOME.

## Terms

**Store:** the runner-owned resumable research records and their `.lock`, not
the research availability receipt or probe audit in the review-record directory.

## Acceptance criteria

1. When `STAGE2_RESEARCH_STATE` contains a non-empty absolute directory, the
   research store uses that base as read at call time.
   *Refuted by:* a subsequent call keeps a previous value or uses `XDG_STATE_HOME` instead.
   *Basis:* `decisions.md#Q-1`.

2. When `STAGE2_RESEARCH_STATE` is unset or empty, the selected default base is
   stable for the current user and independent of HOME, `XDG_STATE_HOME` and the working directory.
   *Refuted by:* ordinary startup selects `~/.local/state`, or changing one of those inputs changes the default base.
   *Basis:* `decisions.md#Q-1`.

3. While HOME and `XDG_STATE_HOME` stay fixed, changing the research-store setting
   leaves the verification queue and review-loop record and lock locations identical.
   *Refuted by:* any of those paths changes between two research-store settings.
   *Basis:* `decisions.md#Q-1`.

4. When the store base is selected, the existing change-and-resolved-worktree
   key continues to isolate each change's research records.
   *Refuted by:* distinct worktrees or changes share a directory, or two spellings of one resolved worktree select different directories.
   *Basis:* `decisions.md#Q-1`; `research.md`, the existing `research_dir` contract.

5. When a selected store is opened, the existing owner-only directory, file
   and lock permissions continue to hold.
   *Refuted by:* a store directory allows group access, a record or lock allows other users access, or an existing unsafe store is accepted.
   *Basis:* `decisions.md#Q-1`; `research.md`, “Placement hard rules in code”.

6. If the selected location is unsafe or unusable, the research run stops
   before launching a research model, with exit 1 and guidance naming the dedicated setting rather than silently choosing another store.
   *Refuted by:* a relative override, a store overlapping a forbidden directory or inherited HOME (including resolved aliases), or an unwritable store permits a model launch or silently falls back.
   *Basis:* `decisions.md#Q-1`; `research.md`, the placement guard and existing failure contract.

7. When a model process is launched, its prompt, arguments and environment
   receive neither the dedicated store setting nor the selected store path.
   *Refuted by:* a unique store-path canary appears in any of those launch inputs.
   *Basis:* `decisions.md#Q-1`; `research.md`, the neighbour spec's store exposure contract.

8. When an interrupted run is resumed from the same selected store, its sealed
   results retain the existing exact-binding reuse behavior.
   *Refuted by:* a matching durable result is lost because of the relocation, or a mismatched result becomes reusable.
   *Basis:* `decisions.md#Q-1`; `research.md`, the existing resumable-store contract.

9. When a review-loop record is released, research records and their held
   store lock remain effective at the independently selected location.
   *Refuted by:* release deletes research state or lets a second store holder acquire the same lock.
   *Basis:* `decisions.md#Q-1`; `research.md`, “Release interplay”.

10. When an operator reads the workflow's research-resume instructions, they
    find the dedicated setting, exact defaults, placement requirements and the effect on pre-existing stores.
    *Refuted by:* the instructions still require moving `XDG_STATE_HOME` for research, omit a default, or imply automatic migration or a changed verification location.
    *Basis:* `decisions.md#Q-1`.

## Non-goals

- Moving or redesigning verification admission, review-loop state, research
  availability receipts or probe audits; callers must still agree on HOME and
  `XDG_STATE_HOME` for shared verification admission.
- Automatically migrating, searching, merging or deleting stores at old locations.
- Changing record schemas, seals, reuse eligibility, publication, lock semantics
  or model selection; weakening the existing home and repository boundaries.
- A design document or ADR: phase 2b does not run for this `bounded` change.

## Protected areas

- `scripts/verify_lock.py` and its admission protocol: research configuration
  must not split the machine-wide queue.
- `scripts/stage2.py` and `scripts/stage2_availability.py`: their existing path
  consumers and launch allow-list already provide the required separation.
- Existing neighbour artifacts, especially `plans/changes/research-swarm/`:
  historical decisions remain intact; current setup guidance belongs in the workflow.
- Held governance and configuration paths, including `AGENTS.md`, `prompts/`,
  `templates/`, `decisions/`, `.claude/`, `.codex/` and `.beads/`: no policy or tracker edit is needed.

## Definition of Done

- `make verify` is green after implementation, including the criterion ledger.
- `docs/WORKFLOW.md` documents the new setting and defaults in the same pull request.
- The pull request's file list shows the protected areas untouched and non-goals unbuilt.
- The pull request closes the research-store location work item
  (`coding-harness-nxdy`), with `Closes-Bead: coding-harness-nxdy` on its last commit.
- Special runs: none; tests use synthetic homes and stores, without live models.

## Open decisions

None open. The maintainer's answer is unchanged. The following reversible
details are chosen here and carried into the plan:

- `[DETAIL]` Name the variable `STAGE2_RESEARCH_STATE`, the interview's example,
  because it distinguishes research state from the shared XDG state root.
- `[DETAIL]` Use `/Users/Shared/coding-harness-research-<uid>` on macOS and
  `/var/tmp/coding-harness-research-<uid>` on other supported POSIX systems;
  `<uid>` is `os.getuid()`, so the default is per user without trusting a name
  supplied by the environment. The unchanged placement guard also applies to
  unusual homes overlapping these paths; unusable defaults require an override.
- `[DETAIL]` Retain the suffix `coding-harness/stage2/<change>@<digest>/research`,
  where `<digest>` is the first eight SHA-256 characters of the resolved root,
  so an explicit safe old base can still address existing records.
- `[DETAIL]` Treat an empty override as unset and refuse a relative override,
  because a store must not move with the caller's working directory.
- `[DETAIL]` Leave old stores untouched; an operator may explicitly select the
  previous safe base to resume them. No automatic fallback can choose stale records.
- `[DETAIL]` Limit phase 4, including repairs, to two hours; this is a stop,
  chosen for a bounded resolver, test and documentation change.
