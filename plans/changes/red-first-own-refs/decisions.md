---
title: "Decisions — red-first-own-refs"
category: decisions
status: draft
implementation_status: partial
date: 2026-11-01
created: 2026-11-01
last_reviewed: 2026-11-01
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-wkxm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# red-first-own-refs — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).

## SKIP · interview

status: skipped
reason: the second finding of one mechanism (AGENTS.md, the mechanism rule) — on 2026-10-31 and 2026-11-01 the red-first and fixed-code proofs of four changes (verify-worker-cap, beads-close-themselves, pi-neutral-paths and go-access-point, the last in its round 1) were voided by refs that other lanes moved — obliges a structural remedy, and the remedy chosen here keeps the protection of red-first-install criterion 8 whole instead of narrowing it, so no decision of the maintainer's is changed; narrowing the watched refs would weaken that criterion and is kept out of scope for the maintainer.

## Details for the draft

[DETAIL] **Isolate, do not narrow.** Reason: the ref comparison exists so that
no named test changes the shared store's refs (red-first-install criterion 8).
The proofs run in a store of their own — a scratch clone of the baseline (and,
for the fixed-code proof, of the fixed tree) whose refs no other worktree
writes — and compare that store's refs before and after. A test that changes
refs is still caught; another lane's commit, push, fetch or tracker push no
longer voids the proof. Whether the shared store's refs may also be
watched is left to the design, as long as a foreign move cannot void a proof.

[DETAIL] **Every existing ref-protection test keeps its meaning or moves to
the scratch store's refs explicitly**, and one new test moves an unrelated
branch of the shared store during the named test and expects the proof to
stand. Reason: the research found no test for the fixed-code proof's ref
branch (open point 4) and one test pinning today's any-difference rule.

[DETAIL] **The refusal names the refs that moved in both proofs.** Reason:
the fixed-code proof's message names none today (research, open point 3).
