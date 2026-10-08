---
title: "Stage 2 in three runs — what the GLM loop and Codex's phase 6 found, 2026-10-07/08"
category: research
status: proposed
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-08"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, stage-2, measurement, review-loop, codex, glm]
---

# Stage 2 in three runs — what the GLM loop and Codex's phase 6 found

Partial evidence for bead coding-harness-kw0 (measure the first stage-2
runs). It does not close that bead: the bead asks for metrics generated
rather than typed, and for tokens and cost per vendor, which the runner does
not record. The counts below were taken by a throwaway script over each
change's `findings.md` at the named commit, on 2026-10-08.

## The three runs

| Run (pull request) | Measured at | Class | Loop rows: taken / rejected | Taken that broke a test | Phase-6 rounds | Phase-6 rows by severity | Codex disagreed with a loop decision | Stage-2 calls, leak check |
|---|---|---|---|---|---|---|---|---|
| `stage2-session` (#91) | `51acbc3` | architectural | 6 / 1 | 0 | 1 | 4 BLOCKER, 3 MAJOR (spec review) | 1 of 7 | 9, all clean |
| `runner-red-gate` (#92) | `c4d6831` | bounded | 7 / 0 | 0 | 1 | 3 BLOCKER | 1 of 7 | 4, all clean |
| `touch-map-comments` (#93) | `a8bc676` | bounded | 3 / 1 | 0 | 2 | 6 BLOCKER | 1 of 4 | 5, all clean |

The three MAJOR rows of `stage2-session` came from its phase-2a spec review
on 2026-10-07; every BLOCKER came from phase 6 and was closed with a test
that a planted regression turned red.

## What the numbers say

- **The stop rule did not fire.** No taken loop row broke a test in any of
  the three runs (bead coding-harness-kw0, notes: a taken finding that
  breaks a test sends stage 2 back to Opus 5.5).
- **Codex's phase 6 found what the loop did not.** Thirteen BLOCKERs across
  the three runs, each reproduced by Codex with a concrete input; none of
  them had been raised by the GLM loop. The loop's rows were smaller and
  mostly true (16 of 18 taken).
- **The two reviewers disagreed on three loop decisions**, each time over
  scope rather than a fault: Codex judged a rejected duplicate-parser row,
  a taken docstring row and a rejected traceability row as no correctness
  fault.
- **A hand-built parser draws a long tail.** `touch-map-comments` needed two
  phase-6 rounds; three of its six BLOCKERs (F-1, F-4, F-5) were introduced
  by an earlier repair. The run ended by naming the scanner's limits in the
  spec instead of a third round.
- **Every stage-2 call ran behind a clean leak check** (18 calls, 12 rules,
  269–276 files and 607–636 commits scanned).

## What was not measured

- Tokens and cost per vendor: the runner records neither.
- Wall time per phase: only the orchestrator's clock readings in each
  `plan.md`, partly approximate; the reviewers' wait is not separated.
- Human minutes: the maintainer was asleep for two of the three runs; the
  third (`stage2-session`) had several hand-offs between sessions that no
  file times.
- Implement through GLM Flash: none of the three was implemented by Flash
  end to end. `stage2-session`'s Flash draft stayed red after Flash, Flash
  repair and the Sonnet fallback and was repaired by hand; a separate smoke
  (`test/glm-smoke` at `0d9d5e5`, never pushed) found the causes, now beads
  coding-harness-zci (fixed in #92) and coding-harness-mfv (open).

## Model routes

GLM 5.3 (loop) and GLM 5.3 Flash (implement) ran through Claude Code with
Z.ai; Sonnet 5.5 through Claude Code with Anthropic; Codex `gpt-6.1-sol`
through the Codex CLI; the orchestrator was Claude Code with Anthropic
(Opus 5.5). All foreign calls went through `scripts/stage2.py`.
