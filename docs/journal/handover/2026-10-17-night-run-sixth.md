---
title: "Session handover — sixth night run, as of 2026-10-17"
category: handover
created: 2026-10-17
updated: 2026-10-17
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-17"
tags: [handover, session, night-run, review-swarm, research-swarm]
target_ref: origin/main
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The night of 2026-10-16 to 2026-10-17 worked two large changes, one at a
time, instead of the short queue. The review swarm that loops until a round
is clean (bead coding-harness-4fk, branch `explore/loop-until-clean`) has
finished phase 4, two loop rounds and two phase-6 rounds; no BLOCKER is
open, and one MINOR repair (P6-8) was running at 10:03. The research swarm
for phase 1 (bead coding-harness-icw, branch `explore/research-swarm`) has
finished phase 2a after five spec-review rounds and stands at the start of
phase 4, stopped by its own appetite rule because earlier time cannot be
measured. No pull request for either change is open yet; both become
decision pull requests the maintainer merges (ADR 0021 and ADR 0020).

## Next step

In `.claude/worktrees/loop-until-clean`, check that the P6-8 repair (the
skip notice that names a terms problem for four wire-API skips) ended
committed and green (`git log --oneline -2`, the runner's line "repair:
verified and committed"), then run
`python3 scripts/stage2.py release-loop loop-until-clean` and start the
fresh loop run the maintainer chose (answer B below) with
`python3 scripts/stage2.py review-loop loop-until-clean`.

## Needed from the maintainer

- **Appetite of the research swarm (bead coding-harness-icw).** The card's
  12 hours include earlier phase-4 time. 78 minutes are measured; the span of
  the three implement attempts of 2026-10-15 (GLM 5.3 Flash twice, Sonnet
  5.5 once, ended 04:53:50 with commit `cf848ee`) has no start record, so the
  rule in `plan.md` ("Earlier implementation time", ruling S-30) stops phase 4
  before any work. Question: which total appetite applies? Recommendation:
  continue with a total of 13 hours 20 minutes (the measured 78 minutes plus
  12 fresh hours; the unmeasured span stays named, not counted). Consequence:
  phase 4 starts with the repair of the 46 red swarm Pi-start tests; without
  an answer nothing is built.

## Decisions and preferences

All recorded in the change folders; not to be asked again.

- **Review swarm, maintainer answers of 2026-10-17**
  (`plans/changes/loop-until-clean/decisions.md`):
  - Q-11 "B": the five ladder models whose terms were unread are admitted
    with a dated reading of the Go page's privacy table, the two that keep
    data 30 days (`gpt-6-luna`, `claude-haiku-5-5`) included; then "Passe
    minimax auf die neue Version an": `minimax-m3` replaces `minimax-m2.7`.
    The ladder id `claude-haiku-5.5` was corrected to `claude-haiku-5-5`.
  - Q-12 "Lasse a": the three Go models that train on prompts (Gemini 4
    Argon Contributor, Muse Spark 1.2 and 1.3 Contributor) stay off the
    ladder.
  - Q-13 "B": the runner orders the paid ladder by a declared cost value
    (`anfragen_5h`, the Go page's estimated requests per 5 hours, read
    2026-10-17); the Flash swarm stays a hand-kept list that should tend to
    be the three cheapest models ("Tendenziell soll der Schwarm aber aus den
    drei günstigsten Modellen bestehen"); a failed Flash member is replaced
    automatically by the cheapest admitted model not yet in the round, and
    the replacement is reported. A non-free model in the live catalog without
    a terms record is named, never admitted.
  - "B" (2026-10-17, after round 3 was refused for a spent ladder): after
    phase 6, release the rows and run a fresh loop with the current ladder
    until a round is clean, then phase 6 again on the new repairs, then the
    pull request.
- **Research swarm, maintainer answer of 2026-10-17**
  (`plans/changes/research-swarm/decisions.md`, Q-11 "D"): a free Go model
  is eligible when it is in Pi's fresh catalog, models.dev lists it with
  `tool_call: true`, and it is not `deprecated`; fallback is the 39 fixed
  slots with the reason recorded.
- **Phase 2a of the research swarm is closed.** Rounds went 30, 10, 9, 7 and
  6 rows (the last all MINOR); every row was ruled by an Opus 5.5 sub-agent
  (rulings S-1 to S-52, appended unchanged), and the round-5 ruling saw no
  reason for another round.
- **Standing rules used tonight:** GLM fails → continue on Sonnet with
  `--stage2-off` from the saved attempt (maintainer, 2026-10-16); review
  findings returned as text are committed unchanged; MINOR rows on tests,
  security or false statements are repaired without asking.

## Open work and blockers

Task status is in Beads; these are pointers.

- **Review swarm** (bead coding-harness-4fk), at `6f47f6e` plus the running
  P6-8 repair:
  - Measured 2026-10-17 by the loop itself: `step-5-preview-free` reached
    the free round because Pi's `--list-models` merges its shipped baseline
    into the live overlay (`mergeModels(baseline, dynamic)` in Pi 1.2.0
    `core/remote-catalog-provider.js`) and failed with "Model is
    unavailable"; the runner now selects free ids from Pi's
    `models-store.json` overlay only (not yet measured against the live
    network). `mimo-v2.6-flash` answered "[model_coming_soon]" again and was
    replaced by `mimo-v2.6-pro` (bead coding-harness-mkg).
  - Four ladder models (`qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5-5`,
    `minimax-m3`) sit in Pi's shipped catalog on `anthropic-messages` or
    `openai-responses`, not chat/completions; they are skipped with "wire
    API not measured" until a probe measures their address (phase-6 row
    P6-1). The live ladder is five models: `deepseek-v4.1-flash`,
    `mimo-v2.6-flash`, `longcat-2.0`, `glm-5.3-flash`, `mimo-v2.6-pro`.
    The probe belongs with the ladder check of bead coding-harness-mkg.
  - The current loop run's snapshot predates Q-11, so its ladder is spent
    (round 3 refused: "every stage of this run is consumed"); the fresh run
    after the release uses the five-model ladder.
- **Research swarm** (bead coding-harness-icw), at `e14ed63`: waiting for
  the appetite answer above. `make verify` shows the 46 known swarm tests
  that fail at the Pi start (2254 passed, 2026-10-17); their repair is the
  first phase-4 step.
- **New bead** (coding-harness-83e, P1, discovered from coding-harness-icw):
  a draft on a known-red tree fails every attempt, the runner restores the
  work, and `--stage2-off` is refused for `draft`; each spec redraft tonight
  cost about 30 minutes and had to be recovered from
  `refs/stage2/attempts/research-swarm/`.
- **GLM 5.3 failed every call tonight** ("claude call failed: exit 1"),
  likely the Z.ai budget; not measured.
- **Queue not reached tonight:** beads coding-harness-csm, 0ho, 8hr, t83,
  6ie, 6jg, ll5, fdz, b5w and k2r. The morning items from the queue (ladder
  probe for bead coding-harness-mkg; questions on beads coding-harness-a7m,
  coding-harness-juu) are still open.

## Working state and parallel-session boundary

- `explore/loop-until-clean` at `6f47f6e`, pushed; uncommitted at 10:03:
  the P6-8 repair in progress (`scripts/stage2.py`, `plan.md`,
  `findings.md`), owned by the runner's repair call of this session. The
  loop record lives outside the repository at
  `~/.local/state/coding-harness/stage2/loop-until-clean/loop.md` (rounds 1
  and 2, every row decided and marked).
- `explore/research-swarm` at `e14ed63`, pushed, clean.
- This handover: branch `docs/handover-2026-10-17-night-run-sixth`, worktree
  `.claude/worktrees/handover-2026-10-17`.
- Parallel sessions: none besides the runner's own `claude -p` calls, which
  the start hook reports as sessions in the research-swarm worktree. This
  session was the only tracker writer; tracker pushed after creating bead
  coding-harness-83e.
- Merged earlier in this session (2026-10-16): PRs #150, #152, #153, #154
  (GLM context window) and #155 (red-first install).

## Validation

- Review swarm, 2026-10-17: `make verify` green after the Q-13 work (2178
  passed, 16 skipped, reported by the Sonnet sub-agent); each runner repair
  (`42f2e4d`, `7aeb54b`) was verified and committed by the runner; the
  phase-6 round-2 re-check ran 867 tests green on `e6195de`. Not run: a live
  call through the new overlay selection; `make verify` after P6-8.
- Research swarm, 2026-10-17: the spec redrafts were recovered unverified;
  `make verify` red only on the 46 known swarm tests; quick gates (frontmatter,
  question context, decision continuity, ADR answers, criterion ledger)
  green on `e14ed63`.
- This handover: `python3 -m pytest tests/test_feedback_channel.py -q` (see
  the pull request).

## Addendum — 2026-10-17, after the release

- The P6-8 repair ended verified and committed (`b00f5b9`); the loop rows of
  rounds 1 and 2 are released into `findings.md` with the phase-6 column
  "agree" (`5856630`).
- **The fresh loop run the maintainer chose (answer B) is not possible on
  this change.** `review-loop` refused again: "every stage of this run is
  consumed and the last round was not clean". ADR 0021 decision 9, part of
  this very change, keeps the snapshot and the consumed stages across a
  release ("Neither release nor edited configuration resets … consumed
  stages"). The orchestrator had assumed a release starts a fresh snapshot;
  that was wrong. The question is back with the maintainer (see below).
- Both changes are open as draft decision pull requests at the maintainer's
  request ("Bitte Committe alle Zwischenstände in prs"): #157 (review swarm,
  origin/main merged in) and #158 (research swarm).

**Needed from the maintainer, added:** how the review-swarm change goes on
now that its loop cannot run again. Recommendation: open the pull request
for review as it stands (phase 6 has no open BLOCKER) and measure the
five-rung ladder on the next change; the alternative is a design change to
ADR 0021 decision 9 that lets the maintainer order a fresh run.

**Next step, replacing the one above:** wait for the maintainer's answer on
the review swarm; then either mark #157 ready (CI green after the merge of
origin/main) or amend decision 9.

- Maintainer, 2026-10-17: "mach a" — #157 is finished as it stands (recorded as Q-14, `45f6360`) and marked ready for review; CI was not yet reported when this line was written. The research-swarm appetite question stays open.
- Maintainer, 2026-10-17: "Ja, halt die zeitgrenze fest" — the research swarm continues with an appetite of 13 hours 20 minutes in total (`plan.md`, card and "Time used"). Next for it: phase 4, starting with the repair of the 46 red swarm Pi-start tests.

## Addendum — 2026-10-17, model reachability through Pi

**Where we are.** The maintainer asked which models Pi reaches. The
runner's probe (`stage2.py probe loop-until-clean`) stopped at the first
failed member twice, so it was repaired to name each failure and go on
(maintainer answer Q-15, "Ja"; finding P6-9, repaired by Codex through the
runner in `3a10892`, re-checked and confirmed read-only by Opus 5.5; the
stale exclusion reason it found, P6-10, fixed by the orchestrator). All on
PR #157 (review swarm, bead coding-harness-4fk), last commit `51fcc59`;
CI green on #157 when this addendum was written.

**Measured 2026-10-17 (full probe on `3a10892`):**

- Answered: `cat-jam-free`, `longcat-2.5-preview-free` (free);
  `deepseek-v4.1-flash`, `longcat-2.0`, `glm-5.3-flash`, `mimo-v2.6-pro`
  (paid). `deepseek-v4.1-flash` and `mimo-v2.6-pro` named themselves
  "Claude"; the probe measures that a call passes, not which model answers.
- Failed: `mimo-v2.6-flash` ("[model_coming_soon]"). The maintainer
  measured the same answer through OpenCode itself, so the model is not yet
  served on Go; Pi is not the cause.
- Excluded from the free stage (`model-endpoints.yaml`, `free_stage.exclude`,
  `48ba7d6`): `step-5-preview-free` ("Model is unavailable"). It and
  `cat-jam-free` appear only in Pi's pi.dev catalog, not in OpenCode's
  models.dev catalog; `cat-jam-free` once answered empty and once answered.
- Not called: `qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5-5`,
  `minimax-m3` (skipped, wire API not measured). OpenCode's own catalog
  routes them through the same Anthropic-messages and OpenAI-responses
  interfaces Pi does, so the skip is the runner's guard, not a Go failure
  (bead coding-harness-mkg).

**What the maintainer saw working in OpenCode** were the Zen free variants
(provider `opencode`, e.g. "MiMo-V2.6-Flash Free"), not the Go models.
ADR 0021 decision 2 excludes Zen. The Zen page (https://opencode.ai/docs/zen,
read 2026-10-17) lists the free models' terms: no training and no
retention for GLM-5.3-Flash Free, DeepSeek V4.1 Flash Free, LongCat 2.5
Preview Free and Space Bunny Free; no training and 30 days retention for
Beam Free; data may be used for training for Big Pickle, LL Alpha Free, Exo
Free, MiMo-V2.6-Flash Free, MiMo-V2.5 Free, the three Nemotron models and
Muse Spark 1.3 Contributor Free; no terms for Jev 1.13 Free. All are free
"for a limited time". Whether Pi can call provider `opencode` with the
existing access is not measured.

**Needed from the maintainer (two questions, one at a time):**

1. Whether `mimo-v2.6-pro` replaces `mimo-v2.6-flash` in `flash_swarm` until
   Go serves the Flash model. Recommendation: yes — today it steps in as the
   replacement on every run; one YAML line on #157, reverted by one line.
2. Whether the Zen free models with readable non-training terms join the
   free stage as a new change (hand-kept allow list with dated terms per
   model, an amendment of ADR 0021, decision pull request). Recommendation:
   yes, after #157 is merged. Its bead is not created yet: an OpenCode
   session was open on #157 and #158, and the tracker stays untouched while
   another session may write.

**Next step, replacing the one above:** ask question 1; then merge-ready
#157 waits for the maintainer.

**Validation of this addendum's work:** probe, endpoint and Pi-contract
tests green (`tests/test_stage2.py -k probe` 26 passed on `3a10892`;
`tests/test_model_endpoints.py` 43 passed after P6-10). Not run locally:
`make verify` after `3a10892`.
