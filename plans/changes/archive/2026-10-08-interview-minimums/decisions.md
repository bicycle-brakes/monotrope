---
title: "Decisions — interview-minimums"
status: accepted
implementation_status: done
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-6yg
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: cline, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, gates, workflow]
---

# interview-minimums — Decisions

Phase 1a, held with the maintainer in the directing conversation of
2026-10-08 (Cline session, bead coding-harness-6yg). Four questions were asked,
one at a time; their records below are the first uses of the machine-readable
question record this change introduces. Everything the maintainer set without
being asked stands under "Given by the maintainer" and is not asked again.

## Given by the maintainer

- **G-1** Features owe at least **three distinct, substantive** questions.
- **G-2** Creating or changing an ADR owes **five** questions, whatever the
  change class.
- **G-3** Questions are asked **one at a time**; the maintainer's answers are
  documented in `decisions.md`; decided matters are not asked again.
- **G-4** Only distinct, maintainer-answered questions fulfil a minimum.
  Agent answers, open questions and repeated confirmations do not. Fact gaps
  are researched (`[GAP]`); reversible details the agent decides with a
  documented reason (`[DETAIL]`).
- **G-5** A different classification must not bypass the ADR duty: the five
  attach to the fact of an ADR being created or changed.
- **G-6** The check must see staged, unstaged and uncommitted-untracked ADR
  changes (the `stage2.change_diff()` states) and needs a defined comparison
  base per context, with tests; an unmeasurable check exits 3.
- **G-7** The rules take effect through the intended decision process — a rule
  takes effect when its pull request merges (ADR 0008); no merge without the
  maintainer's explicit instruction.

## Answers

## Q-1 · The minimum when a feature also carries an ADR

asked: 2026-10-08, the directing conversation
answer: at least five in total — the ADR minimum dominates, and one question
  may serve both duties
answered_by: maintainer
status: answered

In the context of a change that is both a feature and an ADR change, facing
two minimums of three and five, we decided five in total, to achieve one
interview instead of doubled bookkeeping, accepting that such a change is
interviewed somewhat less than a strict 3+5 addition would demand. — 2026-10-08

## Q-2 · When the interview duty applies to a `bounded` change

asked: 2026-10-08, the directing conversation
answer: only when open human decisions about intent, behaviour or acceptable
  risk exist; otherwise a justified skip as one line in `decisions.md`,
  and the gate holds the justification
answered_by: maintainer
status: answered

In the context of `bounded` changes that alter an existing flow without
deciding anything new, facing the question of a blanket interview duty, we
decided the conditional duty with a gate-checked skip line, to achieve a
check that cannot be silenced by silence, accepting that a `bounded` change
without its skip reason turns red. — 2026-10-08

## Q-3 · What an interview owes on a `spike`

asked: 2026-10-08, the directing conversation
answer: a short interview on learning goal, time budget and expected outcome —
  about three questions; a skip with its reason stays permitted when all three
  follow from the assignment
answered_by: maintainer
status: answered

In the context of a class whose product is a recommendation, not a
deliverable, facing the full feature duty versus none at all, we decided the
short three-topic interview with the reasoned skip, to achieve alignment on
what the spike may cost and must return, accepting a lighter duty than a
feature's. — 2026-10-08

## Q-4 · Introduction: the cut-off and the existing stock

asked: 2026-10-08, the directing conversation
answer: the cut-off is the merge date of this change, held as a checked
  constant against the spec `date`; the existing stock, active and archived,
  is exempt
answered_by: maintainer
status: answered

In the context of fifteen active changes that predate the rule, facing a
retroactive duty nobody asked for, we decided the prospective cut-off with a
checked constant, to achieve a rule that is exact about when it begins,
accepting that until the merge the old voluntariness keeps holding. — 2026-10-08

The spec review (phase 2a, Codex session
01a11c4d-7cf9-78d3-81e5-d51fe3941095) returned four `[AMBIGUITY]` rows; the
maintainer settled each in the same conversation:

## Q-5 · Counting when a question id repeats

asked: 2026-10-08, after spec-review F-2
answer: the first occurrence counts; later records repeating an id already
  counted are ignored and do not invalidate the first
answered_by: maintainer
status: answered

In the context of a file where the same question was recorded twice, facing
two readings that accept or reject the same change, we decided first
occurrence wins, to achieve a counting rule that matches "repeated
confirmations do not fulfil the minimum" without punishing the record that
was answered. — 2026-10-08

## Q-6 · When a bounded interview is complete

asked: 2026-10-08, after spec-review F-3
answer: a bounded change owes at least one counted record or a skip record
  with its reason — no higher minimum, because bounded decides nothing new
answered_by: maintainer
status: answered

In the context of a class defined as changing an existing flow without
deciding anything new, facing a feature-sized duty versus no duty at all, we
decided the one-record-or-skip rule, to achieve a check that cannot be
silenced by an empty file, accepting that a single answered question can
suffice. — 2026-10-08

## Q-7 · What "HEAD sits on main" means for the base

asked: 2026-10-08, after spec-review F-6
answer: the branch reading — a genuine checkout of `main` uses the first
  parent (`HEAD^`) as base; every other state (feature branch, detached HEAD,
  worktree) uses the merge base with `origin/main`; unmeasurable exits 3
answered_by: maintainer
status: answered

In the context of a post-merge tree whose merge base equals HEAD, facing an
empty diff that would silence the gate, we decided the branch-based rule, to
achieve a base that is predictable in every context a gate runs in. — 2026-10-08

## Q-8 · The cut-off boundary on the merge day itself

asked: 2026-10-08, after spec-review F-7
answer: strictly greater — a change is subject when its spec `date` is later
  than the cut-off date; anything created on or before the merge day stays
  under the old voluntariness
answered_by: maintainer
status: answered

In the context of changes dated the same calendar day the rule merges, facing
a boundary that would pull same-day stock into the duty, we decided the
strict comparison, to achieve "until the cut-off the old voluntariness holds"
to the letter. — 2026-10-08

## Addendum — 2026-10-08: the base rule, refined by loop row L1-2

The review loop's first round showed Q-7's branch reading unreachable where
it matters most: hosted CI checks out a detached HEAD, so the branch name
never reads `main`, and on the post-merge push `origin/main` equals HEAD —
the merge base would be HEAD itself, the diff empty, and the ADR duty
silently unmeasured. That is the outcome AC 7 of the spec already declares
refuted. The refinement keeps the rule's intent, a base predictable in every
context a gate runs in: **the first parent when HEAD sits at `origin/main`**
— a genuine `main` checkout, or any checkout of the freshly merged tip,
detached included — **the merge base with `origin/main` otherwise**. Q-7's
answer stands; the refinement only recognises that "on main" is a position,
not a branch name. Recorded as an agent decision under the question
protocol — the maintainer reviews it in the pull request.