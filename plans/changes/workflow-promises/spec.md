---
title: "Spec — workflow-promises"
status: draft
implementation_status: partial
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-i0l
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, workflow]
class: bounded
appetite: 5
adr_files: []
neighbours: []
---

# Spec — workflow-promises

Make the promised gate catalog and workflow entry shortcuts usable without
changing the checks or scaffold they expose (bead coding-harness-i0l —
workflow reconciliation). Research: `research.md`. Decisions:
`decisions.md`, which bundles the catalog, the slash command and the Make
targets into one pull request.

## Problem

- The exploration dated 2026-10-27 finds no gate catalog, although the
  workflow names `docs/governance/gate-catalog.md` the one home of its gate
  checklist; the §2 link to it is dead and ends in the German anchor
  fragment `#bevor-ein-gate-scharfgestellt-wird` of a file that does not
  exist (`research.md`, promised and absent, item 6). Gate definitions
  already live in `decisions/gates.yaml`; what is missing is the readable
  view of them.
- The documented entry commands do not exist: the workflow's header block
  and its §3 entry-commands row promise `make change`, `make index` and
  `/workflow-start`, but the Makefile defines neither target and
  `.claude/commands/` does not exist (`research.md`, promised and absent,
  items 4–5). The entry script `scripts/new_change.py` already exists;
  users must call it directly.
- The workflow's missing-pieces notice still describes its 2026-09-30
  baseline at `41abf42` (`research.md`, stale statements, item 5). Once
  this package supplies three of the listed pieces, the notice must say
  which remain absent, at a dated baseline.

## Terms

**Gate catalog:** a readable view of the existing machine-gate list, plus
an explanation of the existing rule for enabling a gate; it creates no
policy.

**Missing-pieces notice:** the "Not all of it is here yet" block in the
`docs/WORKFLOW.md` header, which names the pieces the doctrine describes
but the tree lacks, with its check date and commit.

## Acceptance criteria

1. When a reader opens `docs/governance/gate-catalog.md`, its inventory
   contains every declared gate exactly once with its identifier, title,
   command or hosted action, job, enforcement, floor, placement and reason
   matching `decisions/gates.yaml`.
   *Refuted by:* a missing, extra or duplicate gate, a changed field, or a
   hosted-only action incorrectly presented as a locally runnable command.
2. If the catalog inventory and declared gates disagree, the existing test
   suite fails.
   *Refuted by:* deleting or adding a catalog row, or changing a declared
   gate's displayed metadata, leaves the catalog contract tests green.
3. When `make change NAME=<name> BEAD=<id>` receives valid inputs in a
   usable worktree for an existing bead that is not closed, it creates the
   same research scaffold, bead link, current index and next-phase guidance
   as the existing entry script `scripts/new_change.py`.
   *Refuted by:* a successful call omits an artifact or bead link, leaves a
   stale index, or starts another workflow phase instead of reporting
   phase 1.
4. If either required Make input is empty, or the delegated entry script
   rejects the request, `make change` exits nonzero without leaving a new
   change folder or changing the index.
   *Refuted by:* success, a residual folder or index edit after an empty
   input, unknown or closed bead, duplicate name, or unusable-worktree
   refusal.
5. When `make index` runs, it regenerates `plans/INDEX.md` using the
   existing registry's current rendering.
   *Refuted by:* a stale index remains, differs from the registry
   rendering, or the recipe masks a failing registry command.
6. When `make help` runs, it lists `change`, `index` and `help` alongside
   the existing public targets, including the required change inputs,
   without creating artifacts or running verification.
   *Refuted by:* a missing target or required input, a file mutation, or a
   scaffold, verification or installation command invoked by help.
7. When `/workflow-start <name> --bead <id>` is invoked in Claude Code, its
   repository command delegates change creation to `scripts/new_change.py`
   with the supplied name and bead, and surfaces that script's result.
   *Refuted by:* the command is absent, invents a bead, writes its own
   scaffold, substitutes another entry point, hides a failure, or starts
   phase 1 itself.
8. The `docs/WORKFLOW.md` missing-pieces notice names the gate catalog, the
   `make change` and `make index` targets and `.claude/commands/` as
   supplied, at a re-check dated to this change's baseline commit, and
   keeps every piece that remains absent (the artefact validator, the two
   sub-agents, the stop hook) listed as absent.
   *Refuted by:* a supplied piece is still listed as absent, a remaining
   absence disappears from the list, or the re-check carries no date or no
   commit.
9. The §2 gate-checklist link in `docs/WORKFLOW.md` resolves to an English
   heading in `docs/governance/gate-catalog.md` whose section explains the
   existing gate-enabling rule (a gate is sensible, proportionate and more
   than an end in itself).
   *Refuted by:* the link is dead, its anchor fragment is still the German
   `bevor-ein-gate-scharfgestellt-wird`, or the heading it resolves to
   holds no such rule.

## Non-goals

- Implementing the stop hook, change-artefact validator, missing agents,
  container fence, orchestration or any other mechanism found by the audit;
  the stop hook is split out to the daily decision block (`decisions.md`).
- A second audit report: the exploration is the comparison, as
  `decisions.md` records. Broader README and how-it-works reconciliation
  remains separate; only the README's "Not built yet" list drops the three
  pieces this change supplies, so the front page does not contradict the
  workflow (review loop row L6-1).
- Changing gate definitions, enforcement, workflow phases, tracker policy,
  scaffold validation or the registry's rendering and lifecycle semantics.
- Repairing the plans-registry drift findings in other changes' folders or
  the tracker states behind them; the plan's Verification names them and
  leaves them to their owners.
- Installing user-level commands, querying live services, or creating or
  closing tracker items during drafting.

## Protected areas

- `decisions/`, `docs/adr/`, `provenance.yaml`, `AGENTS.md` and
  `.claude/settings.json`: no policy, architecture or hook change is
  required.
- `scripts/new_change.py` and `scripts/plans_registry.py`: reuse their
  behavior.
- `README.md`, `docs/how-it-works.md` and existing agent definitions:
  outside this bounded package, except the README's "Not built yet" list
  named in the Non-goals (review loop rows L6-1, L7-1).

## Definition of Done

- `make verify` green at the implementation commit. Pre-existing failures
  named in `plan.md`, Verification, remain blockers to report to the
  maintainer; they do not waive this gate or authorize unrelated repairs.
  Targeted tests demonstrate the catalog and entry failures above before
  their corresponding repairs.
- Documents moved with the behavior: `docs/governance/gate-catalog.md`,
  `docs/WORKFLOW.md`, `.claude/commands/workflow-start.md`, the generated
  `plans/INDEX.md`, and the review-loop edits `plan.md` names under
  Boundaries and route (README "Not built yet", two governance pages, two
  kit lines); no ADR.
- Protected areas untouched and non-goals unbuilt, shown by the file list.
- The pull request names all bundled tracker items from `decisions.md`;
  tracker ownership determines who updates them. The final commit carries
  `Closes-Bead: coding-harness-i0l` for the workflow reconciliation.
- Special runs: none beyond the targeted tests and repository verification.

## Open decisions

None open. The following reversible details are chosen by the agent and
recorded here so implementation does not silently supply defaults.

- [DETAIL] No design or ADR draft: the recorded class is `bounded`; the
  package exposes existing behavior and supplies documentation, without an
  architecture change.
- [DETAIL] Reuse the existing gate reader for catalog rows and compare the
  committed inventory to its rendering in tests; this avoids a second gate
  list. Keep document prose and frontmatter outside the generated
  inventory.
- [DETAIL] The slash command accepts the entry script's name and `--bead`
  syntax; arguments are data, not extra shell instructions. Missing inputs
  surface usage, never inferred identifiers.
- [DETAIL] Allow two hours of phase 4 including repairs, then stop and
  report remaining work. At the stop on 2026-10-27 the maintainer named a
  new appetite of four hours in total, and on 2026-10-28 five hours in total
  (`plan.md`, Time used; review loop row L9-3).
- [DETAIL] There is no plan template in `templates/` at baseline
  `78970dfd` (2026-10-27); use the phase-3 prompt's card, file list,
  verification, ledger and empty time section, following existing plan
  headers.
- [DETAIL] The lifecycle and provenance header of `decisions.md` is already
  present at `6f350742` (2026-10-27); preserve it and the recorded decisions.
  Earlier draft diagnostics describe its absence at their older baseline,
  not an outstanding implementation task.
