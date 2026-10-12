---
title: "Session handover — first night-run rehearsal, as of 2026-10-12"
category: handover
created: 2026-10-12
updated: 2026-10-12
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-12"
tags: [handover, session, night-run]
target_ref: a6b7150
bead: coding-harness-yuw
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Morning handover — first night-run rehearsal, 2026-10-12

The night of 2026-10-11/12 was the first rehearsal of the night run (concept:
pull request #125, bead coding-harness-yuw). One orchestrating Claude Code
session worked a queue of three changes plus two reserves, strictly one after
the other, from about 00:15 to 04:00. Nothing was merged.

## 1. The three priorities for today

1. **Merge the decision pull request #126** — ADR 0013, every acceptance
   criterion names its proof, gate `criterion-ledger` (bead
   coding-harness-909). It unblocks coding-harness-s6i, coding-harness-jc3
   and coding-harness-yim. After the merge, close coding-harness-909 by hand:
   the last commit is a merge from `main`, not the `Closes-Bead` commit.
2. **Answer the interview of change adr-owning-change** (bead
   coding-harness-afa), which replaces the interim owner rule that #126
   carries. The exploration is done; it found two constraints to weigh:
   `owner:` in an ADR header already means a role, and the answer-file
   format (schema_version 1) is frozen "not now".
3. **Merge #127** — failed implement attempts keep their diagnostics and
   file list in `findings.md` (bead coding-harness-cit). Then the next GLM
   failure tells why it failed.

## 2. Done — waiting for your merge

| PR | What | State at 04:00 |
|---|---|---|
| #126 | `decide(criterion-ledger)`: ADR 0013 and the gate | CI clean; head `7f53552` |
| #127 | stage-2 attempt diagnostics (coding-harness-cit) | CI clean; head `6f6628e` |
| #123 | ROADMAP.md refreshed: Now 3 "Stage 2 that can be trusted", stale "Stage 2 live" replaced | CI clean; head `60d7ea7` |
| #124 | `AGENTS.md`: a text-only change skips the local `make verify` | first CI red (AGENTS.md over its 200-line budget), repaired in `3a73df2`; CI re-running |
| #125 | night-run concept, built on M3 of the implementation plan | CI clean; head `f07ec1b` |

Evidence, per change:

- **#126:** review loop rounds 1–3 (13 rows, 11 taken with a test each, 2
  rejected as disclosed limits with follow-up beads coding-harness-wpv and
  coding-harness-s9m); phase 6 Codex found three BLOCKERs (F-3 a regression
  of the round-3 repair, F-4 a CommonMark fence edge, F-5 an unsearchable
  directory), all fixed with a red-then-green test; second Codex pass: no
  findings. Replay of the original bug on `9416ffe`: 29 of 30 tests deleted →
  `exit 1`, 29 findings. `make verify` green at `9416ffe`.
- **#127:** implemented by GLM 5.3 Flash (attempt 2); review loop 3 rounds,
  8 rows (6 taken, 2 rejected); phase 6 Codex: F-1 MAJOR (the Sonnet
  fallback could store a key fragment in git's object store before the
  credential scan) and F-2 (a protected function was changed) fixed; second
  pass: no findings. `make verify` green on every repair commit.

## 3. Explorations ready (phase 1 only, branches pushed, no PR)

- `feat/adr-owning-change` — bead coding-harness-afa (priority 2 above).
- `feat/provenance-location` — bead coding-harness-3ar.1, package 1 of the
  ADR-answer pin plan: the provenance map is read at one place
  (`scripts/harness.py`, `answering_role`); `check_adr_answers.py` never
  opens it. Needs a short interview (bounded change).
- `docs/codex-takeover-research` — bead coding-harness-nsm, which workflow
  tasks Codex can take over. Researched by GLM (the runner has no Codex
  research verb). Main facts: Codex already holds 2a, 6 and the interactive
  session (ADR 0012); no token or cost figure for Codex is recorded anywhere;
  moving reviews is a maintainer decision (ADR 0011). The ranking of
  candidates (question 4) is not answered yet.

## 4. Stuck or not as planned

- A sub-agent hit the usage limit before midnight and was resumed after the reset at 00:10;
  every step was pushed, nothing was lost.
- One repair agent started about 75 polling loops for one `make verify` (the
  app showed "69 running tasks"). Every brief now forbids polling loops.
- Text-only PR #124 went red in CI because `AGENTS.md` is held at 200 lines
  — the CI caught what the skipped local run would have.
- Round 4 of the review loop was not possible: the runner stops at three
  rounds (ADR 0011; bead coding-harness-dx0 is the change to lift it).

## 5. Which Now theme moved

"Stage 2 that can be trusted" (ROADMAP.md, Now 3 in #123): coding-harness-909
and coding-harness-cit are delivered as pull requests; coding-harness-afa is
explored.

## Beads opened tonight

coding-harness-yuw (night run), coding-harness-3ar.1 (provenance location),
coding-harness-nsm (Codex takeover research), coding-harness-g2f (GLM repair
verb), coding-harness-wpv and coding-harness-s9m (criterion-ledger limits).

## Parallel sessions

Session coding-harness-70 sits in the main checkout (state: waiting). This
session worked only in worktrees under `.claude/worktrees/`: criterion-test-ledger,
attempt-diagnostics, roadmap-refresh, docs-verify-rule, night-run,
adr-owning-change, provenance-location, codex-takeover-research,
handover-night. Remove each after its merge.

## Resume

Read this file, merge #126 if you agree, then start the interview of change
adr-owning-change (`plans/changes/adr-owning-change/research.md` on branch
`feat/adr-owning-change`).
