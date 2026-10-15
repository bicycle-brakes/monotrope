---
title: "Session handover — third night run, as of 2026-10-14"
category: handover
created: 2026-10-13
updated: 2026-10-14
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-14"
tags: [handover, session, night-run]
target_ref: e0cea42
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

## What happened

One orchestrating Claude Code session worked the queue from 22:36 to about
03:00, one model call or sub-agent at a time. Nothing was merged. Five pull
requests wait for the merge, all with green CI (read 2026-10-14 02:47); one
change stopped; seven explorations and one plan card wait for the
maintainer. Main stayed at `3199a28`.

## 1. The three priorities for today

1. **Decide #138** (Codex repairs the taken review findings; ADR 0017
   supersedes ADR 0015; bead coding-harness-0ga). Six repair rounds fixed
   F-1 to F-14; F-15 to F-17 stay open as accepted limits by the
   maintainer's rule of 2026-10-13. Two of them can make the runner's
   restoration write outside the worktree through a symlink the model
   attempt planted; the class is closed structurally by the new bead
   coding-harness-s9r (isolate each writing attempt). Recommendation in the
   PR: merge with the limits. Its merge also unblocks item 2 and the three
   runner explorations.
2. **Veto or start the plan card of the kit install** (bead coding-harness-2uk,
   branch `feat/kit-install` at `bd6c55d`). Three phase-2a rounds took the
   spec from nine rows to three; all were ruled as `[DETAIL]` within Q-1 to
   Q-6 (`decisions.md`, three rulings sections). The card, unchanged:

   ```text
   For you:     Install a pinned workflow in a fresh repository and compare an existing instance at named commits without writing to it.
   Done when:   A fresh target passes actual make verify before and after its fixture commits the payload, comparison and refusal tests hold, and this worktree's make verify is green.
   Appetite:    12 hours of phase 4, including repairs; stop at the limit.
   Not now:     Updating a pin, switching existing instances, building releases, or configuring agents, trackers and model endpoints.
   Pre-mortem:  suppose it failed: most likely because source inventory assumptions survived in the target's verification.
   Starts unless you say stop.
   ```

3. **Sol's effort per verb** (bead coding-harness-yzk: repair medium, draft
   high, review high). Stopped tonight (section 3); after #138 merges it
   rebases on main and Codex drafts it again (about 25 minutes).

## 2. Done — waiting for your merge

| PR | What | State |
|---|---|---|
| #138 (decision) | Codex repairs the taken review findings, ADR 0017 supersedes ADR 0015 (coding-harness-0ga) | `make verify` green at `1ea2f0d`; F-15 to F-17 accepted limits; CI green |
| #139 | `plans/_README.md` in English (coding-harness-yim, step 1); the two governance documents are `human-decided` and left for a decision PR | `make verify` green at `2efc38b`; CI green |
| #140 | comments, docstrings and messages of two scripts and five tests in English (coding-harness-yim, step 2, first slice); display texts the maintainer sees stay German | `make verify` green at `9bcab68`; CI green |
| #141 | research corpus: mechanical fixes and one stage vocabulary (coding-harness-bt8); content findings left in the review | `make verify` green at `ae5ad6c`; CI green |
| #137 | this page | — |

## 3. Stuck: where, and why

- **Sol's effort per verb** (coding-harness-yzk, branch `feat/sol-effort` at
  `cace591`). Both Codex drafts were red on one gate: ADR 0017 was claimed by
  two changes in one diff, because the branch stacks on the unmerged #138.
  The gate is right; the queue was not. The runner put the drafts back, so
  they are lost. Lesson for the preparation: a change that amends an ADR of
  another open change does not go into the same night.
- **The fix-by-case pattern of #138.** Each phase-6 re-check found the next
  case of one class (F-8, F-10 to F-17), and F-13 was created by the F-12
  fix. Bead coding-harness-s9r (P1) holds the structural answer.
- **Runner bookkeeping again.** The Sonnet repair of F-13 and F-14 was
  correct but failed the `## Time used` check, because a file-tools session
  cannot read the clock; the orchestrator completed it by hand (`1ea2f0d`).
  The GLM 5.3 last attempt of every failed draft is a wasted call while Z.ai
  is exhausted (until 2026-10-14 14:34 CEST).
- **One wasted sub-agent run:** a translation slice was picked without
  measuring; the scripts were already English. The next slice was measured
  first.

### Explorations waiting for their interview (phase 1a)

Each branch holds a `research.md` with its `[DECISION]` questions and a
recommendation per question; no pull request yet.

| Bead | Branch, commit | Core finding |
|---|---|---|
| coding-harness-l9s, handover at 95 % | `explore/handover-at-95`, `6b27f87` | the status line receives `rate_limits.five_hour.used_percentage` (documented, and present in the installed 2.1.296); a Stop hook that blocks once is the only documented way to make the session write its handover |
| coding-harness-fdz, kit probe misses new files | `explore/probe-untracked-files`, `e63b859` | `make verify` runs before the runner stages new files; intent-to-add before verify is the recommended fix; after #138 |
| coding-harness-b5w, derived leftovers block the next run | `explore/derived-leftovers`, `c8b009b` | the runner's own writes (INDEX, stamps, format, a route block in `plan.md`) stay after a failed run; after #138 |
| coding-harness-y17, test-strength rows | `explore/test-strength-rows`, `2831404` | a stronger test for correct code is green on the baseline; recommended: red against a planted fault named when the row is taken; after #138 |
| coding-harness-1jg.4, CI lists changed beads | `explore/ci-bead-summary`, `e5d3ee8` | the tracker has no base and head, only a shared time window; recommended: list the beads the PR names, the window's others as a hint, never blocking |
| coding-harness-mvk, loop round 1 on structure | `explore/loop-structure-first`, `a42f8a1` | the evidence rule, not the prompt, rejects structure rows; recommended: structure first, anchored in design.md or a duplicated helper |

## 4. Which ROADMAP.md theme (Now) the night moved

- **Stage 2 that can be trusted** (Now 3): moved most — #138 ready for the
  merge, s9r opened for the class behind it, three runner bugs explored.
- **LakeSwitch reads Coding Harness** (Now 2): the kit install reached its
  plan card (coding-harness-2uk).
- **Forms and their checker** (Now 1): not moved.

Outside Now, by the maintainer's queue: the corpus correction, the
translation steps and the handover-at-95 exploration.

## Decisions and preferences recorded tonight (maintainer, 2026-10-13/14)

- Sol's effort per verb: repair medium, draft high, review high (bead
  coding-harness-yzk; memory until it merges).
- Research in phase 1 runs as a swarm of OpenCode Go models; each topic is
  worked by one free and one Flash model, and the first stage uses all free
  models automatically; six topics agreed (bead coding-harness-icw notes).
- The review of the implementation runs as a swarm of OpenCode Go models too,
  first stage all free models (new bead coding-harness-4fk).
- The sixth repair round of #138 ran on Sonnet 5.5 by the maintainer's choice.

## Resume

Merge #138 if you agree; then the session rebases `feat/sol-effort` on main
and runs `python3 scripts/stage2.py draft sol-effort`.

## Addendum 2026-10-14, 11:31 — the merges are in

Written by the same orchestrating Claude Code session, against `origin/main`
at `e0cea42`.

### What happened since 08:00

- The maintainer merged #138 at 10:24 (Codex repairs the taken review
  findings; ADR 0017 supersedes ADR 0015; bead coding-harness-0ga). Main
  went to `c52bf14`.
- On the maintainer's instruction ("Bitte merge die offen prs"), a Haiku
  sub-agent merged the four others with merge commits, through `gh` only:
  #137 (this page) at `3100055`, #141 (corpus correction, bead
  coding-harness-bt8) at `cb79dda`, #139 (`plans/_README.md` in English, bead
  coding-harness-yim step 1) at `059e6f0`, #140 (script and test texts in
  English, bead coding-harness-yim step 2) at `e0cea42`.
- #139, #140 and #141 were first refused: GitHub requires a branch to be up
  to date with main, and each merge put the next branch behind. The agent
  updated each branch on the server (`gh pr update-branch`), waited for CI
  and merged. Lesson for the next merge round: expect one CI run per pull
  request after the previous merge, about 15 to 20 minutes each.
- No pull request is open (read 2026-10-14 11:31). No bead was opened,
  changed or closed in this addendum.

### What is next, in order

1. **Sol's effort per verb** (bead coding-harness-yzk: repair medium, draft
   high, review high). The blocker is gone with #138: rebase
   `feat/sol-effort` (`cace591`) on main, then
   `python3 scripts/stage2.py draft sol-effort` (about 25 minutes of Codex).
   While Z.ai is exhausted (until 2026-10-14 14:34 CEST), the GLM 5.3 last
   attempt of a failed draft is a wasted call.
2. **The kit install's plan card** (bead coding-harness-2uk, branch
   `feat/kit-install` at `bd6c55d`) still waits for the maintainer's veto
   or go; the card is in section 1 above.
3. **Six interviews** (phase 1a) for the explorations in section 3. The
   three runner explorations (coding-harness-fdz, coding-harness-b5w,
   coding-harness-y17) were waiting for #138 and can start now.
4. After 14:34 CEST: the live GLM probe of bead coding-harness-6th (the GLM
   refusal in Claude Code).

### Open question for the maintainer

The six explorations of the night ran on Opus 5.5 sub-agents, not through
`python3 scripts/stage2.py explore` and not under `--stage2-off`, and their
`research.md` files name neither the model nor the reason. Recommendation:
add one line with model and reason to each before its interview.

### Recorded rules still waiting for their change

- Research in phase 1 as a swarm of OpenCode Go models — one free and one
  Flash model per topic, first stage all free models, six topics (bead
  coding-harness-icw). Open: whether the free models may see repository
  content (their data terms are not read).
- Review of the implementation as an OpenCode Go swarm (bead
  coding-harness-4fk).

### Resume (addendum)

Create a worktree for bead coding-harness-yzk from `feat/sol-effort`,
rebase it on `origin/main` (`e0cea42` or later), and run
`python3 scripts/stage2.py draft sol-effort`.

## Addendum 2026-10-14, 14:49 — draft of sol-effort done, review by the remote session

Written by the maintainer's Mac session (`019EPak4XgNE5A3cvTW7eZ4G`), against
`origin/main` at `659fb35`.

### What happened since the first addendum

- **Sol's effort per verb** (bead coding-harness-yzk): `feat/sol-effort` was
  rebased on main. Two drafts failed on the gate `frontmatter-current`: the
  rebase set the commit date to 2026-10-14 while `decisions.md` said
  `updated: 2026-10-13`. After the date was corrected (`9113a3d`), Codex Sol
  drafted spec and plan in the first attempt (`5440262`, route codex, verified
  and committed by the runner).
- **A mistake of the orchestrator:** an uncommitted `findings.md` was
  discarded with `git checkout --`. The first run's attempt records are in git;
  the three attempt blocks of the second run are restored from session
  excerpts and marked "reconstructed" (`440c749`). Original output not read.
- **Branch:** `origin/feat/sol-effort` still holds the pre-rebase commits and a
  push was refused (no force push). The rebased stand is on
  **`feat/sol-effort-r2`**, draft pull request **#143**.
- **Phase 2a review:** a remote session reviewed the spec with an Opus 5.5
  sub-agent and found four rows (`bd0cec5` on `feat/sol-effort-r2`; its own
  handover is #144, not merged at 14:49):
  - S-1 MAJOR: criterion 4 covers tables and Model lines, while the prose of
    `docs/WORKFLOW.md` also says Sol at `max`.
  - S-2 MAJOR: editing ADR 0016 and 0017 needs five interview records;
    `decisions.md` holds two.
  - S-3, S-4 MINOR: two ambiguities in criteria 3 and 4.
- A remote session was also told to work on bead coding-harness-fdz (the kit
  probe misses untracked new files); no result read by 14:49.
- No tracker write was made by this session in this addendum.

### Waiting for the maintainer

1. **S-2:** proposal made, no answer yet: take the ADR edits out of #143 and
   resume them after the three missing interview answers.
2. S-1 to S-4 must be settled before the phase 2a gate (no open `[AMBIGUITY]`).
3. The plan card of the kit install (bead coding-harness-2uk), still no veto
   or go.
4. Six interviews (phase 1a) for the explorations in section 3.
5. Whether to add a model and reason line to the six `research.md` files.

### Next, in order

1. After the maintainer's answer on S-1 to S-4: repair the spec on
   `feat/sol-effort-r2`, then plan, implement and phase 6 for coding-harness-yzk.
2. Live GLM probe of coding-harness-6th (Z.ai reset passed at 14:34 CEST, not
   yet probed).
3. Start of bead coding-harness-icw (research swarm) and coding-harness-4fk
   (review swarm) only after the open data question: may the free models see
   repository content?

### Resume (second addendum)

Ask the maintainer for the answer on S-2, then settle S-1 to S-4 on #143 and
repair `spec.md` on `feat/sol-effort-r2`.
