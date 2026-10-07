<!--
Template for an architecture decision record (ADR). Copy it to
`docs/adr/<NNNN>-<slug>.md` and fill it in. This comment is not copied.

1. The yaml block below is the header of the copy: put its lines between two
   `---` lines at the top and replace every `<...>`. It carries no header of
   its own here (`provenance.yaml`, prefix `templates/`). In the body a
   placeholder stands in backticks, so that GitHub shows it: replace it,
   backticks included.
2. The form is MADR 4.0.0 (Markdown Architectural Decision Records,
   `https://github.com/adr/madr`, tag `4.0.0`), with the house's section names.
   Where a name differs, the MADR 4.0.0 element it stands for:
   - Context — Context and Problem Statement
   - Decision — Decision Outcome
   - Validation — Confirmation
   MADR's two optional sections, Pros and Cons of the Options and More
   Information, may be added; the house writes Consequences and Validation as
   sections of their own.
3. A pull request that adds a file under `docs/adr/` is a decision pull
   request: title `decide(<scope>): ...`, label `decision`, body from
   `.github/PULL_REQUEST_TEMPLATE/decision.md`.
4. A record that amends a decided D- or O-number moves two more places in the
   same pull request: an "Amend" row in the table "Decision continuity" of
   `docs/architecture/2026-09-17-omnigent-first-target.md`, and the entry in
   `AMENDMENT_ADRS` of `scripts/check_decision_continuity.py`, which the gate
   `decision-continuity` holds.
-->

```yaml
title: "ADR <NNNN> — <the decision as a statement>"
category: adr
status: accepted
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <role>
provenance: human-decided
produced_by: {kind: llm-session, name: <agent>, version: "<YYYY-MM-DD>"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, <topic>]
```

# ADR `<NNNN>` — `<the decision as a statement>`

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. `<Amends which D- or O-number and supersedes
  which ADR — or: Amends no decision and supersedes no ADR.>`
* Review: `<who chose the direction, and when>` · the acceptance is the merge
  commit and is written nowhere else, so the header's `review` stays empty: no
  agent writes an approval for a merge that has not happened · Decider:
  maintainer · prepared by `<agent>`
* Date: `<YYYY-MM-DD>` · takes effect on merge

## Context

The problem and what forces it, with the facts it stands on, each with where
it was read and when.

## Decision Drivers

* `<A force the decision has to satisfy.>`

## Considered Options

* `<Option a — what it does and what follows from it.>`
* `<Option b.>`

## Decision

Chosen option: "`<title>`", because `<justification>`.

What is decided, stated so that a later reader can tell whether it was kept.

## Consequences

* `<What changes, what becomes harder, what is owed and by whom.>`

## Validation

* `<How the decision is confirmed: a test, a gate, or a review, and when.>`
