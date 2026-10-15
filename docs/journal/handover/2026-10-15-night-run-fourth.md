---
title: "Session handover — fourth night run, as of 2026-10-15"
category: handover
created: 2026-10-14
updated: 2026-10-15
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-14"
tags: [handover, session, night-run]
target_ref: origin/main
bead: coding-harness-yuw
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Morning handover — fourth night run, 2026-10-15

This page is written in two steps. Tonight it holds the queue the maintainer
agreed to on 2026-10-14 at about 19:55 ("passt, starte die nacht"); in the
morning the four sections of the night-run form replace the "filled in the
morning" lines (`docs/research/2026-10-12-night-run.md`, "Morning, 08:00").

## The queue (agreed 2026-10-14)

One orchestrating Claude Code session works it strictly in order, one model
call or sub-agent at a time. No merge, no decision that belongs to the
maintainer; every item ends at a pull request or at a written stop. Every
plan card below was shown to the maintainer unchanged before the start.

| # | Bead | Change | Branch | Ends at |
|---|---|---|---|---|
| 1 | coding-harness-yzk | Sol effort per verb (repair medium, draft high, review high), one central setting in `scripts/stage2.py`; appetite 1 hour | `feat/sol-effort-r2` (draft PR #143) | implement, loop (4b), phase-6 review, repairs, decision PR |
| 2 | coding-harness-eao | Haiku 5.5 instead of Haiku 4.5 wherever a Haiku version is pinned; appetite 1 hour | `feat/haiku-5-5` | pull request |
| 3 | coding-harness-zs7 | Every question to the maintainer starts with a fixed context form, checked by a gate for answers recorded from adoption; appetite 4 hours | `docs/interview-context` | decision PR |
| 4 | coding-harness-icw | Phase 1 as a research swarm for feature and architectural changes, free models first on public research with one Opus-written topic sentence (Q-6), Opus 5.5 reconciles; appetite 12 hours | `explore/research-swarm` | decision PR; no live free-model call before the merge |
| 5 | coding-harness-s9r | Each writing attempt runs in its own container (Podman by default); appetite 24 hours, so it runs until the morning and stops there | `explore/isolated-attempts` | partial implementation, pushed, with a written stop |

Drafts only, already queued before the start, plan cards for the morning:

| Bead | Change | Branch |
|---|---|---|
| coding-harness-ni8 | The handover checks the architecture docs, the front page and the vault | `explore/handover-currency` |
| coding-harness-ylu | One central model and effort setting | `explore/central-models` |
| coding-harness-4fk | The review loop runs until clean, on a model ladder | `explore/loop-until-clean` |

### Rules for this night (maintainer, 2026-10-13 and 2026-10-14)

- **Codex still runs at effort max** for drafts, reviews and repairs until
  item 1 merges. When its five-hour limit is spent, the night moves to steps
  that need no Codex and comes back after the reset.
- **Two changes claim ADR 0018** (research swarm, isolated attempts).
  Whichever merges second renumbers; the gate that refuses a double claim
  sees them in separate branches tonight.
- **Most changes touch `scripts/stage2.py`.** Each branch starts from main;
  conflicts surface at merge and are resolved then, not tonight.
- **Stops.** Red `make verify` after two repairs, a leak-check BLOCK, or a
  question only the maintainer can answer: written down here, the next item
  starts.
- **No tracker write while a draft check or `make verify` runs** in any
  worktree: the render byte-equality test reads the live tracker.

### Lessons of 2026-10-14 the night applies

- The macOS keychain hung every HTTPS git call (tracker push included) from
  about 18:55 to 19:15 and recovered by itself. A hanging push is waited for
  once, not retried in a loop.
- Each worktree needs `make venv` once; the runner is called with
  `.venv/bin/python3`.
- Never two drafts at once in one worktree.
- Notes on a bead are appended (`--append-notes`), never replaced.
- macOS has no `timeout` command.

## 1. The three priorities for today

1. **Merge the three finished changes** (CI green on all, 2026-10-15
   ~06:20): #143 Sol effort per verb, #147 Haiku 5.5, and the decision PR
   #148 every question carries its context. Before merging #148, move its
   adoption day (`decisions/adoption.yaml`, now 2026-10-15) to the real
   merge day.
2. **Research swarm** (coding-harness-icw, branch `explore/research-swarm`
   at `83a4f31`): phase 6 (Opus 5.5) left one open BLOCKER, F-1 — the
   offline capture with the pinned Pi and synthetic canaries (spec build
   step 2) never ran, and it is the only real evidence for criteria 8 and 9
   (nothing private reaches a free model; free models get no tool that reads
   the repository). It was deliberately not run unattended. Rows F-2 to
   F-10 are taken (among them: the free path cannot run on the real Pi
   1.1.0 at all — wrong tool signature, `--list-models` prints a table, not
   JSON; a report with no retrieved page counts as success; the topic
   filter lets hyphenated identifiers through; search returns redirect
   wrappers, not page URLs), but the runner refuses to repair while F-1
   waits for a decision. Decide how F-1 is run (or deferred), then
   `stage2.py repair research-swarm`.
3. **Decide whether the runner's red-first check needs an exception** for
   fixes that live only in test code (see section 3); it stopped three
   repairs tonight.

## 2. Done — waiting for your merge

| PR | Bead | What changes | Review record |
|---|---|---|---|
| #143 | coding-harness-yzk | Codex runs each verb at its own effort — draft high, repair medium, review high — from one central `CODEX_EFFORTS` in `scripts/stage2.py`; docs and prompts link to it | loop 3 rounds; L1-1 and L3-1 (test helpers) fixed by the orchestrating session or an Opus sub-agent; phase 6 Opus 5.5: no finding, all loop rows agreed |
| #147 | coding-harness-eao | Every operative Haiku pin names Haiku 5.5; both Anthropic endpoints list 5.5, not 4.5 | phase 6 Opus 5.5: F-1, F-2 (missing guard tests) fixed by the orchestrating session; re-check confirmed |
| #148 (decision) | coding-harness-zs7 | Every question to the maintainer carries its context; gate `question-context` from the adoption day; ADR 0018 | phase 6 Opus 5.5: F-1 MAJOR (standing rules dropped from `AGENTS.md`, restored), F-4/F-5 BLOCKER [DIVERGENT] (recording-day date ends the statement; one closing parenthetical allowed as a [DETAIL]) — all fixed, re-checked twice |

Also still open from before the night: #144, #145 (handovers) and this
page's #146. A follow-up bead was opened: coding-harness-k2r (the
interview-minimums gate counts fenced examples as records).

## 3. Stuck: where, and why

- **Red-first cannot pass a fix that lives only in test code.** The repair
  runner demands a new test that is red on the old production code. Three
  times tonight the right fix was a test or a test helper over code that
  was already right (yzk L1-1, eao F-1/F-2, yzk L3-1); every runner attempt
  failed, one by moving checker logic into `scripts/stage2.py` to satisfy
  the check. The orchestrating session completed these by hand or through
  an Opus sub-agent. Proposed bead: the runner accepts a "guard test" mark
  whose test plants the fault itself.
- **The runner misreads repaired loop rows.** For eao it reported "L1-1: no
  fixed line" for a row already repaired by hand, and read words such as
  `expected:` and `Resume:` from the answer as finding ids. Proposed bead.
- **The loop silently dropped a round's findings.** Round 2 on the research
  swarm (mimo-v2.6-flash) numbered its rows `R2-1`… instead of `L2-1`…; the
  runner kept them as raw text in `findings.md` and reported "0 rows", so
  round 3 never ran. The phase-6 review found it; one of the seven rows was
  real and new (raised as F-10). Proposed bead: refuse or renumber
  non-conforming row ids instead of reporting a clean round.
- **The "Broke a test" cell accepts only `yes` or `no`.** A mark with an
  explanation made the next loop round refuse; the explanation now lives
  in the commit message.
- **A Codex repair wrote its own handover file** into the research-swarm
  branch; removed (`560160d`). The repair prompt should forbid it.
- **zs7 implement and phase-6 repair failed three attempts each**; the
  second failure was real: anchoring the date to the statement's end left
  a live record (`plans/changes/codex-drafts/decisions.md` Q-1) unmeasured.
  Completed by hand; the allowance is documented in spec, design and plan.
- **Research swarm implement** failed three runner attempts (three
  doctrine tests red); an Opus sub-agent completed it. The leak check then
  blocked the loop on two synthetic test keys in new test files; they are
  built from parts now. Not done: the offline Pi capture (spec build
  step 2). An earlier gap between collected and run tests (2081 against
  2054) did not recur at phase 6 (2100 collected, 2084 passed + 16 skipped);
  its cause was not measured.
- **ADR 0018 is claimed by four open changes** (interview-context, research
  swarm, isolated attempts, loop-until-clean); each later merge renumbers.
- **Isolated attempts** (coding-harness-s9r) started late: implement
  (GLM 5.3 Flash) began at about 06:35 in `.claude/worktrees/isolated-attempts`;
  its result is recorded in that branch's `findings.md`.
- **Codex usage limit** was hit at about 20:50 the evening before ("try
  again at 10:48 PM"); the runner printed only "codex call failed: exit 1",
  the reason stood only in `~/.codex/sessions/…/rollout-*.jsonl`.

## 4. Resume

Say which of #143, #147, #148 to merge; for #148 first confirm the
adoption day. Then the research swarm: phase-6 result (section 1, item 2)
and the offline Pi capture.

Plan cards waiting for you, drafted before the night (unchanged, in each
branch's `plan.md`): coding-harness-ni8 (`explore/handover-currency`),
coding-harness-ylu (`explore/central-models`), coding-harness-4fk
(`explore/loop-until-clean`).
