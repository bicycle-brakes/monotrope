---
title: "Spec — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3, version: "2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, provenance]
class: bounded
appetite: 3
adr_files: []
neighbours: [plans/changes/archive/2026-11-16-explore-provenance/spec.md, plans/specs/implementation-verification/spec.md]
---

# Spec — runner-stamps-provenance

The goal in one sentence: the runner stamps the provenance of every artifact
it publishes, a red check holds the producer header of every artifact under
`plans/`, and every existing free-form header is migrated once (bead
`coding-harness-f9sv`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

Three failures, each read in this checkout on 2026-11-16:

1. **Hand-written producer headers fail the contract.** 50 `research.md`
   headers on main carry a free-form `produced_by`, and a lane went red on
   one (`decisions.md`, Q-1 context; `research.md`, "What exists today").
   Models and sessions write these headers by hand; only `findings.md`
   creation and research publications are stamped by the runner
   (`research.md`, "The runner already stamps provenance in these places").
2. **Nothing in verify goes red on them.** The metadata contract lives in
   `scripts/research_census.py`, but as a library no gate runs
   (`scripts/ci_gates.py` lists it as a library held by tests);
   `scripts/plans_registry.py` checks lifecycle fields only, and
   `scripts/check_docs.py` measures presence, and only under `docs/`
   (`research.md`, "What holds this today").
3. **The draft artifacts are published unstamped.** `spec.md`, `design.md`
   and `plan.md` from the `draft` verb are written by the drafting model
   session itself, so their provenance fields are exactly the hand-written
   form the census refuses (`research.md`, "The runner does not stamp
   provenance in these places").

## Terms

- **producer header** — the `produced_by` field of an artifact's frontmatter.
- **metadata contract** — the publication header form the explore-provenance
  change defined: `provenance`, `produced_by` as one record or a list of
  records (`kind: llm-session`, a program `name`, an ISO date in `version`,
  optional `model`), `review` pending, `date <= last_reviewed <= updated`
  (`plans/changes/archive/2026-11-16-explore-provenance/spec.md`;
  `scripts/research_census.py`).
- **free-form header** — a `produced_by` outside that record form: prose, a
  bare string, a record without `kind`/`name`/`version`, or an unknown
  program name.
- **per case** — one check at each header's own check, the maintainer's Q-1
  answer; the rejected alternative was one general detector of side routes.

## Acceptance criteria

1. When the `draft` verb publishes a change's `spec.md`, `design.md` or
   `plan.md`, the runner stamps the artifact's header so that `provenance`,
   `produced_by`, `review` and `updated` hold the metadata contract's form,
   whichever form the drafting session wrote.
   *Refuted by:* a draft-published artifact whose `produced_by` still carries
   a free-form value or an unknown program name after the runner's pass.
   *Basis:* `decisions.md#Q-1` (its Today: headers written by hand, only
   findings stamped); `research.md`, "What exists today".
2. When any Markdown artifact under `plans/` carries a `produced_by` that is
   not the metadata contract's record form, the `plans-registry` gate fails.
   *Refuted by:* such a header, live or archived, standing in a tree whose
   `make verify` stays green.
   *Basis:* `decisions.md#Q-1` (a red check per case at the header's own
   check).
3. When this change is done, no Markdown artifact under `plans/`, archived
   folders included, carries a `produced_by` outside the record form.
   *Refuted by:* any remaining free-form `produced_by` under `plans/`.
   *Basis:* `decisions.md#Q-2` (migrate every header once, archived ones
   included).
4. While the runner stamps a draft artifact's header, every byte outside the
   stamped header fields keeps its place: authored prose, the plan card,
   fences and unrelated frontmatter fields are untouched.
   *Refuted by:* a stamp that rewrites, reorders or drops bytes outside
   `provenance`, `produced_by`, `review` and `updated`.
   *Basis:* `research.md`, "What exists today" — `research_publication`'s
   byte-preservation contract, the helper the stamp generalizes.

## Non-goals

- No general detector of side routes: the maintainer chose a check per case
  (`decisions.md`, Q-1); other hand-written fields get their own checks in
  their own changes.
- No enforcement of the `allowed:` classes of `provenance.yaml` — the
  predecessor explore-provenance refused it; the map stays declaration-only.
- No change to the deterministic new-change skeleton: an untouched,
  unpublished skeleton stays `human-written` without `produced_by`
  (predecessor non-goal).
- The runner never writes or stamps `decisions.md` — the maintainer's
  answers file, excluded by `draft_keep()`; the check of criterion 2 reads
  its header like any other artifact's.
- No automation of approval: `review: approved` stays a human edit.
- Artifacts outside `plans/` (handovers, `docs/`) keep their presence-only
  checks; nothing here measures them.
- The stale `scripts/validate_provenance.py` reference in
  `provenance.yaml`'s header comment is separate drift housekeeping, not
  this change.

## Protected areas

- The held set (`provenance.yaml`, `decisions/gates.yaml`, `.claude/`,
  `.codex/`, `.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md`, `prompts/`,
  `templates/`, `.github/`, `.beads/`, `AGENTS.md`, `README.md`): no step of
  this change edits one — the red check lands in the existing
  `plans-registry` gate, so no gate list changes.
- `scripts/new_change.py`, the skeleton writer, stays as it is.
- `docs/adr/`: this change creates, changes or removes no file there.
- The loop record outside the git directory keeps its headerless form.

## Definition of Done

- `verify` green.
- Moved in the same pull request: the draft stamping in `scripts/stage2.py`,
  the contract reader exposed in `scripts/research_census.py`, the registry
  check in `scripts/plans_registry.py`, the one-time migration
  `scripts/migrate_producer_headers.py` with the migrated headers under
  `plans/`, and the tests named in the plan's criterion ledger.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes `coding-harness-f9sv`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-f9sv`
  (`prompts/07-commit.md`).
- Special runs: the one-time migration run, its commit named in the pull
  request body.

## Open decisions

No `[DECISION]` is open. Decided as `[DETAIL]` by the drafting session, each
with its reason:

- The red check lands in the existing `plans-registry` gate — it already
  walks every Markdown artifact under `plans/`, live and archived, so no
  held gate list changes.
- The migration is a kept, idempotent script
  (`scripts/migrate_producer_headers.py`) — repeatable and reviewable, not a
  hand edit of ~50 files, which is exactly the hand repair this change
  removes.
- A `produced_by` that is absent stays absent: the check holds the form of a
  present field, not its presence — presence under `docs/` is
  `check_docs.py`'s question, and no presence rule for `plans/` was decided.

Recorded as `[GAP]` in `research.md` ("What is unclear"): the work item's
own description (bead `coding-harness-f9sv`) names a four-part fix and could
not be read in this checkout — the tracker is an embedded Dolt database not
present in the worktree. The plan's first step reads it through the tracker
before implementation; whatever it names beyond these criteria enters this
spec as an amendment with its own criteria, and anything needing a
maintainer choice goes to `decisions.md` as a question — never a silent
decision.
