---
title: "Session handover — third night run, as of 2026-10-14"
category: handover
created: 2026-10-13
updated: 2026-10-13
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-13"
tags: [handover, session, night-run]
target_ref: 3199a28
bead: coding-harness-yuw
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Morning handover — third night run, 2026-10-14

This page is written in two steps. Tonight it holds the queue the maintainer
agreed to on 2026-10-13 at about 22:40; in the morning the four sections of
the night-run form replace the "filled in the morning" lines
(`docs/research/2026-10-12-night-run.md`, "Morning, 08:00").

## The queue (agreed 2026-10-13)

One orchestrating Claude Code session works it strictly in order, one agent or
model call at a time. No merge, no decision that belongs to the maintainer;
every item ends at a pull request or at a written stop.

| # | Bead | Change | Ends at |
|---|---|---|---|
| 1 | coding-harness-0ga | Codex repairs the taken review findings: a fifth and last phase-6 repair round for F-12 (root-cause fix: prompts built only from the snapshot, every changed snapshotted file restored), a fresh Codex re-check, then the decision pull request; a further finding of the same class becomes an accepted limit named in it | decision PR, not merged |
| 2 | coding-harness-yzk | Sol (`gpt-6.1-sol`) effort per verb instead of max: repair medium, draft high, phase-6 review high; built on the `0ga` branch because ADR 0017 is not merged; recorded as a dated amendment to ADR 0016 and 0017, the ADR answer cites the maintainer's two sentences of 2026-10-13 ("Mache Sol nur mit hoch"; "für Korrektur mit Codex Sol mit Medium, für das Entwerfen der Spec Sol mit high") | decision PR, not merged |
| 3 | coding-harness-2uk | Bring the kit into lakeswitch-ai: Codex redrafts spec, design and plan with the six interview answers and the phase-2a rulings, Opus reviews the spec; open details are decided as `[DETAIL]` within the answers | plan card for the maintainer, before implementation |
| 4 | coding-harness-l9s | Write the handover automatically when the usage limit reaches 95 %: exploration only, first of all whether Claude Code hands the five-hour window's percentage to the status line | research.md, interview questions for the maintainer |
| 5 | coding-harness-fdz | The kit probe misses new files because `make verify` runs while they are untracked | research.md |

Reserve, in order, after item 5:

| # | Bead | Change | Ends at |
|---|---|---|---|
| R1 | coding-harness-b5w | A failed run's derived writes block the next run of the same change | research.md |
| R2 | coding-harness-y17 | A test-strength finding has no red-first form in the repair | research.md |
| R3 | coding-harness-yim | Translate the remaining German in the repository, in small pull requests | pull requests |
| R4 | coding-harness-bt8 | Corpus correction: mechanical fixes and one stage vocabulary | pull request |
| R5 | coding-harness-1jg.4 | The CI job summary lists the beads a pull request changed | research.md and plan card |
| R6 | coding-harness-mvk | Review-loop round 1 looks at the structure of the code first | research.md |

In the conversation the exploration of the kit-probe bug (bead
coding-harness-fdz) stood both as item 5 and as the first reserve; it runs
once, as item 5, and the reserve is renumbered.

### Rules for this night (maintainer, 2026-10-13)

- **Z.ai is exhausted until 2026-10-14 14:34 CEST.** No GLM call; the GLM
  refusal in Claude Code (bead coding-harness-6th) waits for the reset.
  Explore and implement run under `--stage2-off` with that reason.
- **Codex has a five-hour limit.** When it is spent, the night does not wait:
  it moves on to steps that need no Codex (explorations, the Opus spec
  review, the review loop on OpenCode Go) and returns to the Codex steps after
  the reset. A phase-6 review has no fallback model; `--stage2-off` is refused
  for `review` on purpose.
- **Reviewers.** Review loop (phase 4b) on the OpenCode Go ladder through Pi;
  phase 6 on Codex `gpt-6.1-sol`; spec review (phase 2a) on Opus 5.5.
  Explorations are not reviewed.
- **Stops.** Red `make verify` after two repairs, a leak-check BLOCK, or a
  question only the maintainer can answer: written down here, the next item
  starts.

## 1. The three priorities for today

Filled in the morning.

## 2. Done — waiting for your merge

Filled in the morning.

## 3. Stuck: where, and why

Filled in the morning.

## 4. Which ROADMAP.md theme (Now) the night moved

Filled in the morning.
