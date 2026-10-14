---
title: "plans/ — the artifacts handed over between the phases"
category: engine
status: current
created: 2026-09-05
last_reviewed: 2026-09-05
updated: 2026-10-14
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-05"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [workflow, artifacts, spec, plan, lifecycle]
---

# plans/

This is where what one phase of the workflow hands to the next lives. **The
handover is the file, not the chat history.** The whole point: between plan and
implementation the context is wiped, and everything must still be there
afterwards.

The workflow itself is in [`docs/WORKFLOW.md`](../docs/WORKFLOW.md).

## Three states, three places

| Place | What lives there | Lifetime |
|---|---|---|
| `specs/<capability>/spec.md` | **living** — what a capability is meant to deliver today | stays, is kept up to date |
| `changes/<name>/` | **active** — a change in progress: `research.md`, `spec.md`, `plan.md` | until completion |
| `changes/archive/YYYY-MM-DD-<name>/` | **historical** — completed | stays as evidence, is never cited |

After a change is completed: merge the delta into the living capability spec,
lift lasting architecture decisions into an ADR under `docs/adr/`, archive the
rest. **An implemented feature spec does not stay behind as a living
document** — code and Git history are there for that, and two truths about the
same subject are one too many.

## Frontmatter

Two separate status fields, and the separation is the point:

```yaml
status: draft | accepted | superseded      # moves when the project decides
implementation_status: none | partial | done   # moves when the code moves
date: 2026-09-05
last_reviewed: 2026-09-05
supersedes: null
superseded_by: null
bead: portfolio-agentic-engineering-<id>
```

A field that carries both cannot say whether an accepted spec is still unbuilt
or whether built code rests on a withdrawn spec. Exactly these two cases are the
interesting ones.

`bead:` connects the artifact to the tracker. Work is tracked in Beads, not in
Markdown lists (AGENTS.md) — the artifacts here describe *what* is being built,
the tracker says *where it stands*.

`status`, `implementation_status`, `date`, `last_reviewed` and `bead` are
**mandatory**; `plans_registry.py --check` blocks if one is missing — **or
present but empty or `null`**. "Present" and "filled" are not the same thing: a
`last_reviewed:` without a value is the same blind spot for every downstream
check as a missing field. `supersedes` and `superseded_by` are the only two
fields allowed to be `null`. Until 06 September `bead` was only a convention —
all artifacts carried it, nobody checked it. A rule that everyone follows and no
gate knows is a habit.

`bead:` is more than a pointer: `plans_registry.py` holds `implementation_status`
against the state of the same item in the tracker render — through the single
access point `scripts/bead_render.py` (in CI the preset `BEAD_RENDER`, otherwise
a fresh render). If the bead is closed, the artifact must be `done` **and** lie
under `changes/archive/`; if it is `done`, the bead must be closed. Both
directions report DRIFT and only become sharp in the nightly `--strict` run, not
at the pull request — between `bd close` and the later archiving there is
deliberately a window of hours, no reason to block.

If `implementation_status` moves away from `none`, the folder must carry a
`plan.md` — DRIFT in the same `--strict` run.

`last_reviewed` ages: if it lies more than `STALE_AFTER_DAYS` days back (today
90; the number is in `scripts/plans_registry.py`, not here), that is DRIFT.
Archived artifacts are exempt — an archive ages by definition. And a `date` or
`last_reviewed` that **cannot be read as a date** is itself a DRIFT finding: an
unreadable value is no reason to skip the check, but the occasion to report it.

**All DRIFT rules together** — built and not archived, one-sided supersession,
age threshold, unreadable date, the coupling to the item, the missing
`plan.md` — become sharp at night in the `drift` job
(`plans_registry.py --check --strict`), not at the pull request. What blocks at
the pull request is BLOCK: a missing or empty mandatory field, a status outside
the allowed set, a supersession pointer into nothing, a stale `INDEX.md`, a
missing tracker export.

## The rule against duplicate creation

> Before creating a spec or plan artifact: **always first** search `plans/specs/`
> and `plans/changes/` for the topic with `rg`. If a matching artifact exists,
> it is **updated** — not created anew.

It appears verbatim in `AGENTS.md` too, because an agent does not necessarily
read this file. What `make staleness` checks is the consequence: artifacts
without frontmatter, without a bead, with a contradictory status, or finished
and never archived.
