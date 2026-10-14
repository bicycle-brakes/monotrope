---
title: "Decisions — codex-repairs"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-0ga
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, repair, codex]
---

# Codex repairs the taken review findings — Decisions

Phase 1a for bead coding-harness-0ga, on 2026-10-13, after the exploration in
`research.md`. Today `stage2.py repair` hands the taken findings to GLM 5.3
(ADR 0015); the maintainer asked that Codex (`gpt-6.1-sol`) implement the
fixes of the review findings from now on.

## Q-1 · Who re-checks a repair Codex made of its own phase-6 findings

asked: 2026-10-13
answer: A — a fresh Codex session, as `review` already starts one after a repair; no other model and no extra loop round.
answered_by: maintainer
status: answered

In the context of Codex both finding the phase-6 defects and, from now on,
repairing them, facing the choice between a fresh Codex session, another
model (Opus 5.5) or an extra round of the OpenCode Go loop as the re-check, we
decided on a fresh Codex session to achieve a re-check that never saw the
repair from the inside while the work stays on Codex's budget, accepting that
the same model judges a repair of its own kind. — 2026-10-13

## Q-2 · Which findings Codex repairs

asked: 2026-10-13
answer: A — both kinds in one call, as the verb does today: the taken loop rows of phase 4b and the taken phase-6 findings.
answered_by: maintainer
status: answered

In the context of a repair verb that today takes both kinds of findings in one
GLM 5.3 call, facing the choice between Codex taking both, only the phase-6
findings, or only the loop rows, we decided on both to achieve one repair
route and no GLM 5.3 spend on repairs, accepting that Codex also repairs rows
the OpenCode Go ladder found. — 2026-10-13

## Q-3 · The fallback when the Codex attempts fail

asked: 2026-10-13
answer: A — Sonnet 5.5 as the last attempt, as today: Codex, Codex again with the first attempt's diagnostics, then Sonnet 5.5 on stage 1.
answered_by: maintainer
status: answered

In the context of a repair that can fail its post-run checks twice on Codex,
facing the choice between a Sonnet 5.5 last attempt, a GLM 5.3 last attempt
(as `draft` does) or no fallback and a stop, we decided on Sonnet 5.5 to
achieve that a repair still lands in the rare case and no Z.ai budget goes to
GLM 5.3, accepting Claude budget for that last attempt. — 2026-10-13

## Q-4 · When Codex cannot be reached

asked: 2026-10-13
answer: A — as today: the orchestrator switches deliberately with `--stage2-off <reason>`, the repair runs on Sonnet 5.5 alone and the reason is recorded; the runner never switches by itself.
answered_by: maintainer
status: answered

In the context of Codex being out of budget or down, facing the choice
between the explicit `--stage2-off` switch, an automatic switch to Sonnet when
Codex does not answer, or no fallback at all, we decided on the explicit
switch to achieve that every move off Codex is visible and carries its reason,
accepting that a dead Codex call stops the run until the orchestrator
restarts it. — 2026-10-13

## Q-5 · What happens to ADR 0015

asked: 2026-10-13
answer: A — a new ADR "Codex repairs the taken findings" supersedes ADR 0015; 0015 stays as history, marked as superseded by the new one.
answered_by: maintainer
status: answered

In the context of ADR 0015 routing the repairs to GLM 5.3, facing the choice
between a new ADR that supersedes it and rewriting 0015 in place, we decided
on a superseding ADR to achieve that the reason for the GLM route stays
readable and the repository keeps its one way of replacing a decision,
accepting one file more. — 2026-10-13
