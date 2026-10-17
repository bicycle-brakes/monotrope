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


## Addendum — 2026-10-17, Codex takeover, first repair and Leantime

### Where we are

Codex read the full instructions and every earlier addendum, fetched origin
and checked the three requested pull requests and worktrees. At entry all
three worktrees were clean at the supplied commits. The first research-swarm
wrapper/fixture repair is now verified and pushed; the full amended research
graph is still unfinished. The maintainer also requested a Leantime subagent
assessment and then its follow-up task.

Remote state checked on 2026-10-17:

| PR | State and head | Meaning |
|---|---|---|
| #156 | Merged, `3f6d467`; main merge `6477d04` | The original handover merged outside this session. |
| #157 | Open, not draft, `51fcc59`, CI green | Review swarm; first model question below still awaits an answer. |
| #158 | Draft, `e9ec953`, hosted CI running | Initial wrapper repair locally green; amended subsystem incomplete. |
| #159 | Open, `3e03dca`, CI green | Confirmed temporary GLM availability instruction. |
| #160 | Open, `dcae6d5` | Leantime feasibility research; no integration adopted. |

The descriptions of #157 and #158 were refreshed: the spent-loop decision
and research-swarm appetite are already settled, not pending stops.

### Next step

Obtain the maintainer's answer to the first MiMo question already sent in
this resumption. Do not interpret the later "ja" about the outage date as
an answer to this separate question.

### Needed from the maintainer

First question's context, for the next session to present in German:

- Topic: temporary membership of the paid Flash swarm on PR #157.
- Intention: avoid the known unavailable member on every new run.
- Today: the 2026-10-17 probe found MiMo Flash returning model_coming_soon,
  while MiMo Pro answered and already steps in as its automatic replacement.
- Repository change: replace only the Flash-swarm MiMo entry in
  model-endpoints.yaml; retain a one-line reversal when Go serves Flash.
- Architecture change: none. Recommendation: yes.

Should mimo-v2.6-pro temporarily replace mimo-v2.6-flash in flash_swarm?

Only after that answer, ask whether Zen free models with dated non-training
terms should join the review free stage through a new change amending
ADR 0021, after #157 merges. Recommendation remains yes; no task for that
specific change was created. The existing deferred research-swarm Zen task
is a different OpenCode-CLI path (coding-harness-fkt); inspect its scope before
creating related work. No new reachability or terms probe ran here.

### Decisions and preferences

- Maintainer: "ich habe kein claude budget mehr, bitte übernehme alle claude
  aufgaben". Codex takes over the previous Claude duties; no further Claude
  model call was made. Permanent role assignments were not silently changed.
- The maintainer confirmed the GLM outage cutoff as **2026-10-21 20:34
  Asia/Singapore**, equal to **12:34 UTC** and **14:34 Europe/Berlin**.
  Before that cutoff use Sol 6.1 or Sonnet for implementation; use Sol while
  Claude budget remains exhausted. The "ja" confirmed this date/time only.
- The rule is saved and reread in both personal instruction files
  (`~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`). The English repository rule
  is proposed in #159. Future GLM reachability is not measured by that rule.
- The earlier 13-hour-20-minute appetite and decision to finish the review
  swarm as it stands remain settled. No pull request was merged by Codex.

### Open work and blockers

- Research swarm (coding-harness-icw): inventory, public and repository Pi
  launches now use PI_WRAPPER. The fixture injects a named pin double and
  traps bare Pi; its path regression covers infrastructure and model calls.
  Timeout/environment interceptors follow the pin, and the append-only test
  allows only the required updated-date stamp. The amended 39 + 3N graph,
  catalog/handoff checks and attended F-1 isolation capture remain unfinished.
  Next code action: write the plan's red-first catalog/graph fixtures.
- The measured phase-4 span is 2026-10-17 **10:33:55–11:12:32 UTC,
  38 minutes 37 seconds**, with breaks counted, recorded in plan.md. Add it
  to historical measured time; the total appetite stays 13 hours 20 minutes.
- Review swarm (coding-harness-4fk): configuration answer pending; wire-API
  qualification remains with the existing model-reachability follow-up
  (coding-harness-mkg).
- Leantime qualification (coding-harness-al8), requested by the maintainer:
  open task, priority 2. The read-only subagent recommends only a small
  additional human planning view, with Beads/Dolt and repository artifacts
  authoritative. A synthetic pilot is proposed, not started. API mapping,
  permissions, usability, operation and full plugin terms remain untested or
  not read. Sources and limits are in
  docs/research/2026-10-17-leantime-fit.md at dcae6d5 (#160).

### Working state and parallel-session boundary

All work was done in worktrees; the main checkout remains at `6029bbf` with
its pre-existing untracked `.codex/agents/` untouched. Fetched origin/main is
`6477d04`. The original handover worktree remains at `3f6d467`; the review
swarm remains at `51fcc59`; the research swarm is clean and pushed at
`e9ec953`. New instruction and research branches are clean and pushed:
`docs/glm-availability-2026-10-21` at `3e03dca` and
`docs/leantime-assessment-2026-10-17` at `dcae6d5`.

This addendum uses worktree `.claude/worktrees/resume-2026-10-17-models`,
branch `docs/resume-2026-10-17-models`. It initially fast-forwarded the
original handover, then fast-forwarded to origin/main after #156 merged;
its pull request targets main. All earlier records are preserved byte for
byte.

The startup hook reported coding-harness-b7 as waiting. Initial tracker
writes were held. At the maintainer's explicit request for a Leantime task,
the configured session scan was rerun with process access and returned no
other interactive session; a Leantime search found no existing task.
The read-only subagent /root/leantime_fit had finished without writes.
The parent then created the Leantime task, appended its research commit and
the research-swarm checkpoint to their task notes, and successfully pushed
Dolt before the subsequent research git push. No task was closed.

### Validation

- Source checkpoint e9ec953: full make verify GREEN on 2026-10-17;
  **2301 passed, 16 skipped** (pytest 828.98 seconds), all blocking local
  gates green. Markdownlint is report-only and still reports warnings.
- Final verification command used process-local GIT_CONFIG_COUNT=1,
  GIT_CONFIG_KEY_0=commit.gpgsign, GIT_CONFIG_VALUE_0=false and permission for
  local test servers. Earlier runs hit sandbox socket denial and inherited
  SSH-signing setup errors (2286 passed, 16 skipped, 15 setup errors);
  affected Git-fixture groups then passed separately (13 and 5 tests).
  Those already-invalid runs were stopped. No global Git setting changed.
- Pin repair red-first: original fixture failed; injecting the pin exposed
  the bare inventory launch before production was fixed. Nine affected
  cases passed; all 70 swarm cases passed in the complete pytest sweep.
  After the time-log append, criterion-ledger, frontmatter and whitespace
  checks passed; the generated plans index had no diff.
- Instruction #159: three entry-point tests passed, AGENTS.md is within its
  200-line budget at 198 lines, timezone conversion checked with zoneinfo,
  hosted CI green at 3e03dca. SSH signing was bypassed per-command under the
  repository's explicit no-signing convention, not by unlocking a key.
- Research #160: primary-source read-only assessment, current frontmatter and
  clean whitespace. No installation, live API test, deployment or adoption.
- Handover: feedback-channel checks passed (49 passed, 13 skipped) using the
  existing locked Python 3.12 environment. Building a new handover venv was
  attempted but its package index could not supply a locked dependency;
  existing environment used explicitly. Text-only PRs skip local make verify
  under the repository rule; hosted CI is their gate.
- Credential contents were not inspected or printed. No customer repository
  was read, and no real foreign-model call was made. Pi contract tests used local model
  doubles. The earlier live reachability evidence remains dated 2026-10-17.

## Addendum — 2026-10-17, reachable review ladder checkpoint (12:59 UTC)

### Where we are

The maintainer approved general availability preparation for the review
ladder on PR #157 (Q-16), replacing the need for a temporary individual
MiMo substitution. The implementation is committed and pushed at `8ad049d`;
full local verification is green. PR #157 is deliberately a draft again:
the historical phase-6 verdict covers the old scope only, and a fresh
independent read-only Sol 6.1 review is running. This addendum is an interim
checkpoint during continued work, not a claim that the session is complete.

### Next step

Inspect the fresh phase-6 result for the reachable-reviewer implementation
on PR #157 and triage its findings before starting another code change.
The runner was started through the loop-until-clean worktree's
`.venv/bin/python scripts/stage2.py review loop-until-clean`; its output is
in `/tmp/coding-harness-pr157-q16-phase6.log`. At this checkpoint no verdict
has returned. Do not reset or replay the spent phase-4b run.

### Needed from the maintainer

Nothing right now. The previous addendum's first MiMo question is superseded
by the approved general preparation. The separate proposal to admit Zen free
models with dated non-training terms remains a later decision, after #157
merges; no bead for that specific proposal has been created. The existing
deferred Zen-through-OpenCode-CLI task is a different scope.

### Decisions and preferences

- The maintainer requested actual availability checks before review, a report
  in the main Claude Code or Codex conversation, and selection from available
  models. They answered "ja" to implementing that general mechanism on
  PR #157 (recorded as Q-16); the one-off MiMo replacement is deferred.
- The maintainer requested the structural runner refactor to be recorded.
  It is separate work, not silently bundled with availability behavior.
- The maintainer requested autonomous continuation until only five percent
  of the five-hour Codex allowance remains, followed by a handover PR.
  They subsequently said "mach weiter". A safe local usage-event reading
  measured 40 percent used in the 300-minute window at
  2026-10-17 12:59:12 UTC; this is a dated observation, not a fixed budget.
  It reads usage fields only, never credentials. Continue useful work and
  reserve enough allowance to write and push the final handover.
- Claude budget remains exhausted; implementation and the fresh independent
  review use Sol 6.1. No GLM call is allowed before the exact cutoff already
  recorded above: 2026-10-21 20:34 Asia/Singapore. No merge was requested.

### Open work and blockers

The tracker owns task status. The implementation-review swarm remains in
progress pending fresh independent review and the maintainer's decision
merge (coding-harness-4fk). Runner modularization is a newly recorded open
follow-up, priority 2 (coding-harness-vg9, Refactor stage2.py into cohesive
runner modules). Its scope preserves routing, admission, leak checks,
snapshots and evidence behavior while reducing runner responsibilities.
Measured before this implementation, stage2.py had 3570 lines at main
`6477d04`, and 4622 lines at the review branch's `51fcc59`; these are
historical counts, not the current file size.

The approved research-swarm graph remains unfinished at its earlier green
checkpoint (coding-harness-icw, PR #158, `e9ec953`). It is the next code
change after PR #157's review is handled. Leantime qualification remains
an open, unstarted pilot (coding-harness-al8, research PR #160, `dcae6d5`).
No task was closed. Tracker comments and Q-16/refactor notes were pushed
before the subsequent Git push.

### Working state and parallel-session boundary

At this checkpoint the review worktree is
`.claude/worktrees/loop-until-clean`, branch `explore/loop-until-clean`,
pushed at `8ad049d`. The running stage2 review has appended its call audit
to `plans/changes/loop-until-clean/findings.md`; that file is intentionally
uncommitted until the result is triaged. No source change is pending.
PR #157 remains a decision draft. The handover stays on its own branch
`docs/resume-2026-10-17-models`, PR #161, with the earlier handover preserved.
The main checkout and other worktrees were not changed by this implementation.

The configured session scan returned no other interactive writing session
at 12:59 UTC. This measures that hook's scope, not every possible process.
The external read-only Sol review is this session's child, not another
tracker writer. The earlier Leantime subagent has finished without writes.

### Validation

- At `8ad049d`, final full make verify GREEN on 2026-10-17:
  **2259 passed, 16 skipped** (pytest 885.03 seconds), every blocking local
  gate green, including the kit probe. Documentation-link and Markdown-format
  checks report findings but do not block under the declared gate policy.
- All 24 new synthetic availability cases passed. The initial preparation
  test failed before the verb existed; the namespaced exclusion regression
  failed before the matching fix. The first full verification found two
  integration faults, helper registration and an overbroad client-attribution
  assertion; both were repaired before the final full green run.
- After the plan's evidence/time append, frontmatter-current, the criterion
  ledger and whitespace checks passed; plans index regeneration had no diff.
  Measured phase-4 span: 11:35:25–12:57:23 UTC, 01:21:58 including waits.
- Availability tests use local stand-ins, not live providers. Preparation
  probes contain no repository content and expose no tools. No actual GLM
  or Claude call was made. The fresh Sol review is still pending here.
- Preparation expires after 900 seconds and binds the worktree, endpoint
  declaration and diff. The caller acknowledges reporting in the main
  conversation; the runner cannot verify what a user interface displayed.
  Existing snapshots remain frozen, and all-failed preparation is no clean
  result. Future catalog entries still require their existing admission.
- This interim handover's feedback and session-entry checks passed on
  2026-10-17 (55 passed, 13 skipped), using the existing locked research-swarm
  Python environment explicitly. Frontmatter-current and whitespace checks
  passed, and an exact byte-prefix check preserved the earlier handover.

## Addendum — 2026-10-17, quota reserve and native feedback research

### Where we are

The fresh independent review returned three major findings. A fresh Sol
repair passed full verification and committed them at `20f976e`. The
orchestrator then reproduced a remaining Pi restoration fault without a
network/model call: a copied model store with a missing server modification
date is ignored. Evidence and taken follow-up P6-14 are pushed at `bb8b5e1`
on PR #157, still draft. No further repair was started as quota approached
the requested reserve.

### Next step

After observing the actual allowance reset, repair P6-14 through stage2.py
in the review worktree, then obtain a fresh independent read-only verdict.

### Needed from the maintainer

Nothing right now. A reset was announced for about half an hour after
13:29 UTC, but has not been observed at this checkpoint. Preserve the
five-percent reserve until it actually occurs.

### Decisions and preferences

The maintainer requested an eighteen-hour night-run plan, then two native
Sol research subagents: recurring PR/chat/review feedback, and keeping
research current. They prefer a harness-native approach over Hermes.
These are research proposals, not authorization for silent runner/skill,
ADR, scheduling or model-admission changes. Claude remains exhausted and
the exact GLM cutoff above remains binding. No merge was requested.

### Open work and blockers

The proposed night plan is pushed at `045210f`, PR #162; preparation is
tracked as coding-harness-yuw.1. It preserves existing appetites and scopes.
The first research created coding-harness-0kw, Native feedback evidence loop:
correlate PR feedback, repairs and later verdicts. The second updates the
existing deferred research-currency task, coding-harness-pu9, preserving
its status. All research subagents have finished read-only; none owns tracker
writes. The tracker contains sourced scope, acceptance criteria and limits.

### Working state and parallel-session boundary

Review branch `explore/loop-until-clean` is pushed at `bb8b5e1`; its two
latest commits include the green source repair and documented residual.
Night plan branch `docs/night-run-plan-2026-10-17` is pushed at `045210f`.
Two own research worktrees hold the English source notes:
`review-feedback-research-2026-10-17` and `research-currency-2026-10-17`,
with matching docs branches. Check their Git status/upstream before resuming:
publication is being completed during this handover reserve. Main remains
untouched, origin/main is `6477d04`. Last configured scan found no other
interactive writer; this parent alone wrote the tracker.

### Validation

The repair runner reported full verification green, first Codex attempt,
and committed `20f976e`; its successful output did not retain a new pytest
count. Its plan records six baseline-red regressions, successful affected
reruns and 12 real-Pi contracts. Do not reuse the older 2259 count as the
new repair count. The offline residual reproducer, hashes and controls are
in docs/research/2026-10-17-pi-overlay-resolution.md on PR #157.
The night plan passed frontmatter/whitespace checks; CI was pending when
published. The earlier handover checkpoint `6c17cc8` has hosted CI green.
Research-current measurement: 29 notes, zero age-due on 2026-10-17; this
does not prove semantic freshness. A partial recheck can renew a whole note,
which motivates per-claim evidence. Online sources and limitations are in
the new research notes and Beads. No research implementation, credentials,
customer access, GLM/Claude model call or merge occurred.

Resume: verify the quota reset and finish any research-document publication,
then return to P6-14; the research-swarm implementation remains next in queue.

Publication completion, 2026-10-17: the feedback research is clean/pushed at
`b41fefd`, PR #163; research currency is clean/pushed at `7b83f3f`, PR #164.
Both source notes passed frontmatter-current and staged whitespace checks;
hosted CI is pending. The tracker, including the research-currency wording
clarification, was pushed before Git. The night plan is PR #162. No code
repair or new model call was started during the quota reserve. At 13:43 UTC
the meter showed 96 percent used; the remaining allowance was used for this
requested handover and publication, not another implementation attempt.

## Addendum — 2026-10-17, continuation after observed allowance reset

### Where we are

The maintainer said "mach weiter" and asked for status. At 14:06:10 UTC the
local usage event reported zero percent used in the new 300-minute window;
the announced reset was actually observed. The targeted P6-14 repair is now
running through stage2.py with a fresh Sol context in the review worktree.
The earlier reserve checkpoint remains historical, not a current stop.

### Next step

Inspect the existing running repair's result in
`/tmp/coding-harness-pr157-p614-repair.log` before starting another model
call; after a green checkpoint, push tracker/Git and run a fresh independent
read-only phase-6 verdict. Do not launch a duplicate repair or reset the
spent phase-4b run.

### Needed from the maintainer

Nothing right now.

### Decisions and preferences

Continue the approved queue after the observed reset. The five-percent
reserve applies to the new allowance window; the existing per-change
appetites and human merge boundary remain binding. The night plan proposes
an operational envelope, not a new architecture or routine unattended runtime.
Claude budget remains exhausted; the temporary local Claude-command guard
is still active around the Sol repair, and no GLM call is permitted before
the previously recorded cutoff.

### Open work and blockers

The remaining protocol-activation fault is still taken pending the runner
result (coding-harness-4fk). The amended research swarm remains next
(coding-harness-icw). Both new research reports remain proposals; feedback
collection is open under coding-harness-0kw and research currency keeps its
existing deferred status under coding-harness-pu9. Task state stays in Beads.

### Working state and parallel-session boundary

At resumption, the review branch was clean and pushed at `bb8b5e1`, PR #157
open/draft. The running repair now owns changes to stage2.py, its tests and
the change's plan/findings; it makes its own checkpoint only after checks.
Its outer tool session is 78620 in this conversation; the log above is the
filesystem resumption reference. The parent owns this separate handover
worktree, and no other interactive writer was detected by the configured scan.
All three requested native research subagents are finished and read-only.
Main remains at `6029bbf`; fetched origin/main remains `6477d04`.

### Validation

At the post-reset remote check, PR #157 at `bb8b5e1`, handover #161 at
`14f5e86`, night plan #162 at `045210f`, feedback research #163 at `b41fefd`
and research currency #164 at `7b83f3f` all had hosted verification green.
The new P6-14 repair is not yet reported green here. Its current diff adds
real-pinned-Pi resolution tests and explicit model configuration while
retaining source retrieval dates. No live provider qualification, GLM/Claude
model call or merge ran. Read-only preparation of the research-swarm spec,
design and plan continued; no phase-4 work on that change started after reset.

## Addendum — 2026-10-17, visible agent activity and editor interface idea

### Where we are

The maintainer asked whether active Codex, Pi and Claude jobs could open
visible terminals in VS Code, whether the harness could become an extension,
and whether TypeScript or Rust would justify rewriting it. They then asked
for a bead and for alternatives to an extension. The requested idea is now
recorded as an open child of the existing cross-harness extension vision:
qualify a VS Code interface with live agent terminals and compare
editor-independent alternatives (coding-harness-25h.1; parent
coding-harness-25h). The tracker push completed on 2026-10-17.

### Next step

Inspect the existing second Sol repair attempt for the Pi activation fault
before starting another model call; the active outer process is still 78620
and its log remains /tmp/coding-harness-pr157-p614-repair.log.

### Needed from the maintainer

Nothing right now. No interface or language choice was accepted.

### Decisions and preferences

The interface bead captures exploration, not implementation authority. The
proposed sequence is to expose shared, versioned runner progress first, then
compare a thin TypeScript VS Code extension, a local web dashboard and a
terminal interface. Keeping the existing Python core and splitting its
responsibilities is a recommendation, not a language decision or a measured
performance result. Named per-job terminals should expose actual emitted
activity, waiting and checking states without inventing progress from silence.
Official VS Code extension/task documentation was checked; it does not prove
an integration exists in this repository.

### Open work and blockers

The interface exploration is open under coding-harness-25h.1; task status
stays in Beads. The review runner's first P6-14 repair attempt failed its
red-first evidence gate because the regression's setup failed against the
baseline. Its diagnostic block is preserved in findings.md. The runner has
started its allowed fresh Sol repair attempt with that diagnostic; no Claude
fallback or GLM call has been made. Do not report the overall repair green
until its postconditions and checkpoint succeed.

### Working state and parallel-session boundary

PR #157 remains draft at pushed bb8b5e1, with repair-owned uncommitted
changes in the review worktree. This separate handover worktree alone owns
this addendum. The configured session scan returned no other interactive
writing session immediately before creating the interface bead; this parent
remains the sole tracker writer. Earlier read-only research agents are done.

### Validation

The existing extension vision was read before creating its more specific
child. The new bead was read from the create result and pushed; no UI code,
prototype, language migration or UI test was produced. The source proposal
and five acceptance criteria are in the tracker. The current repair's last
measured phase transition is a failed first post-run check followed by a
fresh Sol attempt; full success is pending. No merge was requested or run.

## Addendum — 2026-10-17, Pi activation repair green and fresh review running

### Where we are

The second fresh Sol repair passed the outer runner's complete make verify
and every repair postcondition. Source checkpoint 79a73a8 fixes P6-14;
orchestrator evidence commit 80be40f is clean and pushed on PR #157.
The runner returned "repair: verified and committed · route codex-repair ·
attempt 2". A new independent read-only Sol phase-6 review is now running
against 80be40f through stage2.py. The PR remains draft until its renewed
verdict and hosted checks are assessed.

### Next step

Inspect the existing review at
/tmp/coding-harness-pr157-after-p614-review.log and tool session 19575;
collect its verdict before starting another model call or changing the
review source. Triage new findings under the evidence rule, or checkpoint
and publish a clean verdict before moving to the research swarm.

### Needed from the maintainer

Nothing right now. No merge was requested.

### Decisions and preferences

The maintainer additionally wants more of Pi's provider APIs/models usable
in both swarms, with interactive choice of participating models. This
requirement is appended to the existing central model/effort configuration
task (coding-harness-ylu) and linked from the new interface exploration
(coding-harness-25h.1). Pi 1.2.0's installed usage/RPC/SDK documentation and
ModelRuntime declarations were read statically: it has a model selector,
language-independent command/event transport and TypeScript session APIs.
This was no credential inspection or live availability measurement. The
proposed selector distinguishes catalog presence, role eligibility, data
admission, cost information and actual reachability, then freezes a roster.
No policy, provider admission, implementation or language migration was
accepted through this idea capture.

The existing night-run epic's two-week restraint on dashboards is named in
the interface bead for evaluation; the future wish does not silently waive
it. The bounded night-plan preparation task is now closed as delivered
(coding-harness-yuw.1); its open PR #162 and hosted verification are green
at 045210f. The night-run epic itself stays open. Both tracker updates were
pushed, and PR #162 names the closed preparation task.

### Open work and blockers

The renewed phase-6 verdict is pending (coding-harness-4fk). The research
swarm remains next (coding-harness-icw), with its existing attended offline
capture still required and real Claude qualification unavailable while the
maintainer's budget is exhausted. Read-only preparation found stale active
12-hour appetite wording in spec/plan beside the already approved 13-hour
20-minute total in the card and Time used. Align active wording to that
recorded answer before the next implementation; preserve historical text
and the named unmeasured old span. No phase-4 work on research-swarm began
after the allowance reset. New catalog/helper/handoff work is still pending.

### Working state and parallel-session boundary

Review worktree: .claude/worktrees/loop-until-clean, branch
explore/loop-until-clean, pushed 80be40f. The sole active foreign-model child
is the fresh read-only Sol reviewer; this parent alone writes the tracker
and this separate handover branch. The last configured session scan found
no other interactive writer. Main remains untouched at 6029bbf; a new fetch
did not change origin/main from 6477d04. GLM's exact cutoff and the local
Claude-command guard remain in force. The previous repair process 78620 has
finished successfully; do not resume or duplicate it.

### Validation

The source repair passed complete make verify and the baseline assertion
proof on its second Sol attempt, leaving a clean worktree at 79a73a8.
The first attempt's setup failure remains in findings.md; it was not
accepted as red-first evidence. The strengthened dependency-free launch
regression gives six baseline assertion failures with passing setup and
teardown. Four additional actual pinned-Pi resolver cases check new and
existing model API, endpoint, context and limits at missing/invalid-date
representation zero and older server dates. The repair plan records 720
affected-suite passes and 16 real-Pi contracts. The successful outer runner
does not retain a new full-suite pytest count; 2259 remains older evidence.

Models-store keeps retrieval/server-date evidence unchanged. Scratch
models.json activates the fetched definitions before listing and offline
launch, independently of Pi's cache-age filter. The orchestrator recorded
the measured repair interval 14:07:38–14:53:57 UTC, 0:46:19, including both
attempts and outer verification, without double counting. It marked the
changed existing test explicitly. Frontmatter-current (295 held documents),
criterion ledger and whitespace passed after that evidence-only update;
source code did not change after its complete green verification.

The earlier handover at e36154e has hosted verification green. Newest PR
#157 CI and the independent verdict are pending here. No live model
qualification, credential-file read, customer access, GLM/Claude call or
merge occurred in this continuation.

## Addendum — 2026-10-17, new independent verdict and fresh safety repair

### Where we are

The fresh independent Sol review of 80be40f finished with two new findings:
P6-15 BLOCKER, catalog model headers copied into models.json can invoke Pi's
command/environment-template configuration resolver; P6-16 MAJOR, arbitrary
inability/error prose with no table rows can certify a false clean round.
The orchestrator confirmed both by static source inspection and took them
at pushed 8986d9e on draft PR #157. The earlier green repair at 79a73a8
remains valid test evidence, not a clean final verdict.

A separate fresh Sol repair is now active through stage2.py, started around
15:01 UTC with the Claude-command guard still in force. The read-only
reviewer did not repair its own findings. The exact latest reviewer session
is 01a14a5c-e94b-7650-8c28-d0c7843dcb27; its verdict is in findings.md.

### Next step

Inspect the existing repair at /tmp/coding-harness-pr157-p61516-repair.log
and tool session 80267 before starting any other model call. On success,
check its clean checkpoint and regression evidence, push tracker before
Git, and obtain a new independent read-only phase-6 re-check. On failure,
read its preserved diagnostics; do not call Claude or waive a failed proof.
Do not resume the completed review process 19575 or prior repair 78620.

### Needed from the maintainer

Nothing right now. No merge was requested.

### Decisions and preferences

These are repairs under existing accepted criteria: preserve catalog
headers as literal values, including command-shaped and environment-shaped
strings, while keeping raw retrieval evidence; validate explicit no-finding
answers and treat failed review prose as a member failure. No new model,
provider, interface or language policy is being decided. The interactive
Pi selection and interface wishes remain captured in coding-harness-ylu
and coding-harness-25h.1 respectively, with implementation still future.

### Open work and working state

The implementation-review task remains in progress (coding-harness-4fk).
The repair owns the review worktree, branch explore/loop-until-clean,
baseline 8986d9e; do not edit its files while it works. This parent owns the
separate handover worktree and is the sole tracker writer. The latest
configured scan found no other interactive writer. Research-swarm remains
next with no new phase-4 work after reset; its old capture blocker remains.
The night-plan preparation is closed as delivered, with the epic open.

### Validation

The new findings' disposition passed frontmatter-current (295 documents)
and whitespace checks before commit. The source check read pinned Pi's
provider-composer.js and resolve-config-value.js, plus run_swarm; it ran no
catalog-controlled command and read no credential file. The new repair has
not yet reported green. PR #157's body names both taken findings and the
running repair. No live provider qualification, customer access, GLM/Claude
call or merge occurred.

## Addendum — 2026-10-17, safety repair verified and quota handover

### Where we are

P6-15 and P6-16 are repaired at 142384902074a196f66944112e520ca35ec144b4.
The runner returned "repair: verified and committed · route codex · attempt
1", with complete make verify and all repair postconditions green, leaving
a clean checkpoint. Orchestrator evidence is committed at ab5e688 and
published on draft PR #157. All taken findings through P6-16 are repaired;
a fresh independent phase-6 re-check of this latest source remains pending.
No clean final verdict or merge is claimed.

### Next step

In .claude/worktrees/loop-until-clean, check Git/PR state, then run a fresh
`.venv/bin/python scripts/stage2.py review loop-until-clean` through Sol.
Retain the local Claude-command guard while its budget remains exhausted.
Inspect the new verdict, then commit and push its evidence; do not resume
an earlier reviewer or reset the spent phase-4b run. Only after this review
is safely checkpointed should research-swarm resume.

### Needed from the maintainer

Nothing to answer now. Continuation needs sufficient session allowance.
At 15:27:03 UTC the local meter recorded 94 percent used in the current
five-hour window; this final publication uses the remaining handover reserve
before the requested five-percent stop. No further model call was started.

### Decisions and preferences

The VS Code/live-terminal interface versus browser/terminal alternatives is
recorded as coding-harness-25h.1. Interactive use of more Pi providers/models
in both swarms is recorded under coding-harness-ylu and linked to that child.
These are future requirements, not implemented UI, language migration or
new provider admission. Night-plan preparation coding-harness-yuw.1 is
closed as delivered; its epic stays open. The exact GLM cutoff and exhausted
Claude-budget rule remain binding. No merge was requested.

### Open work and working state

Review worktree branch explore/loop-until-clean is clean at pushed ab5e688;
PR #157 remains draft awaiting independent re-check and current hosted CI.
Research-swarm remains at e9ec953 on PR #158, with no new phase-4 work after
reset, its approved 13-hour 20-minute total and attended capture requirement
preserved. Align its stale active 12-hour wording before implementation.
The latest repair process 80267 has finished successfully; its log is
/tmp/coding-harness-pr157-p61516-repair.log. All earlier repair/review
processes have ended. This parent alone wrote the tracker; the last
configured scan found no other interactive writer, and the three requested
research subagents are finished read-only. Main was not edited.

### Validation

The repair plan records eight baseline assertion failures, 18 focused
passes, a broad run with 726 passes followed by passing corrected cases,
and all 17 actual pinned-Pi contracts passing. Successful outer verification
retains no new full-suite pytest count. Catalog headers stay literal through
Pi's actual composer without changing retrieval evidence; arbitrary failure
prose cannot certify a clean review member. The measured interval is
15:01:41–15:25:31 UTC, 0:23:50, including model and outer checks without
overlap. P6-15's existing-test mark is no; P6-16's is yes. The final
source-evidence update passed frontmatter-current (295 documents), criterion
ledger (661 entries) and whitespace. Tracker was pushed before Git.

Earlier handover 97f3bf9 has hosted CI green. Newest repair/evidence and this
text-only addendum have hosted CI pending at publication; local full verify
is skipped for this handover under the text-only rule. No live provider
qualification, credential-file read, customer access, GLM/Claude call or
merge occurred. All earlier handover bytes remain unchanged.

## Addendum — 2026-10-17, night continuation and clean independent re-check

### Where we are

The maintainer requested "mach weiter bis morgen im 10". Continuation
started after the full handover and instructions were reread, worktrees
and PRs checked, and a new fetch completed. The local usage event at
21:00:42 UTC measured zero percent used in the new five-hour window.
At entry PR #157 (ab5e688), #158 (e9ec953) and this handover (2818e2d)
had hosted verification green. Original handover PR #156 remains merged.

A fresh independent read-only Sol review of ab5e688 finished with exactly
"No finding.", session 01a14bab-758c-7092-bd54-81d6bdeeb919. The runner's
verdict was committed unchanged at 0c03ec0, with no source change after the
fully verified safety repair. It is pushed to PR #157, still draft while
the latest verdict commit's hosted checks run. No model process is active.

### Next step

Check hosted CI for PR #157 at 0c03ec0. When green, mark it ready for the
maintainer's review without merging, then resume research-swarm under its
existing plan and measured remaining appetite. Keep the implementation
bead open until its intended merge boundary.

### Needed from the maintainer

Nothing right now. The reported interpretation of the requested deadline
is 2026-10-18 10:00 Asia/Singapore, equivalent to 02:00 UTC and 04:00
Europe/Berlin. This active session continues until that boundary or its
actual allowance/other hard stop, whichever comes first; uninterrupted
runtime was not promised. No scheduled or unattended service is created.

### Decisions and preferences

Preserve the earlier five-percent allowance reserve and individual change
appetites. The eighteen-hour plan remains a proposal; this continuation's
operational endpoint is the deadline above, not a fresh eighteen hours.
One code change and one foreign call at a time; the exhausted Claude budget
and exact GLM cutoff remain in force. The local Claude-command guard is
present and was used for the re-check. No merge, new provider admission,
interface implementation or language rewrite was authorized here.

### Open work and working state

Review worktree branch explore/loop-until-clean is clean at 0c03ec0.
Research-swarm stays at e9ec953 and requires the amended graph/catalog/
handoff implementation and the attended isolation capture. The stale active
12-hour wording must follow the already approved 13-hour 20-minute total
before new phase-4 work; historical records remain unchanged. The finished
re-check log is /tmp/coding-harness-pr157-night-recheck.log. Do not resume
the earlier review/repair sessions. The configured scan found no other
interactive writer; this parent remains the sole tracker writer, and all
three earlier native research subagents are finished read-only. Main was
not edited and remains at 6029bbf; existing worktree ancestry is retained.

### Validation

All previous handover bytes remain unchanged. Fresh review completed through
the worktree's locked Python and stage2.py with a clean pre-call leak check.
The verdict-only change passed frontmatter-current (295 documents) and
whitespace checks; source full verification stays at 1423849 and hosted CI
was green at ab5e688. Tracker comment was pushed before Git. No live provider
qualification, credential-file read, customer access, GLM/Claude call or
merge occurred in this resumption. Latest verdict and new handover CI are
pending at publication.


## Addendum — 2026-10-17, research catalog foundation and typed references

### Where we are

At 21:14 UTC PR #157's final independent-verdict commit 0c03ec0 had hosted
verification green and was marked ready for the maintainer. Its fresh
read-only Sol re-check returned exactly "No finding." No merge occurred.
The implementation-review task remains open until its intended merge
boundary (coding-harness-4fk).

Research-swarm PR #158 remains a draft. Its next green source checkpoint is
379ed2838fd3c2d66286a59e11436957e1197e45, pushed after the tracker. It adds
a standalone pinned-Pi public-catalog bridge, duplicate-aware two-source
selection and an immutable planned 39 + 3N seat description. This does not
activate the amended dispatcher. Updated the existing Phase-1 research-swarm
task (coding-harness-icw); no task opened or closed. Its status stays
in progress. Spec/design/plan now explicitly say implementation partial.

### Completed work and evidence

The catalog tests exercise the real pinned Pi against local HTTP servers.
An in-memory catalog-only sentinel enables Pi's configured refresh branch;
no credential file or authentication header is used, and no model is called.
The bridge forces a fresh Go-only read alongside credential-free models.dev
with one deadline. Python retains raw duplicate identity evidence, source
UTC/digests, fixed-model checks, per-candidate reasons, mandatory explicit
includes and distinct measured-empty/capability-unavailable outcomes.

At 379ed28 the new catalog set passed 56 tests; full make verify GREEN
included 2357 passed and 16 skipped in 756.26 seconds, then every blocking
gate green. Process-local commit.gpgsign=false and local test servers were
enabled. A standalone kit command omitted that signing override and failed
17 Git fixtures; the complete correctly configured run passed its kit gate.
Documentation/Markdown findings remain report-only. Later accounting/status/
index changes passed frontmatter, criterion ledger and whitespace checks.
Measured phase-4 span 21:15:16–21:40:12 UTC, 24m56s, is appended in plan.md;
add it to retained history and the earlier 38m37s under the approved total
of 13h20m. Historical unmeasured time is still named and excluded by the
recorded maintainer continuation, never treated as zero.

### Current work and next step

A second phase-4 interval began at 21:41:24 UTC. Four red-first catalog
counterexamples found overbroad duplicate checks, an unrelated Pi-entry
failure and missing raw evidence. Two further red-first cases establish
that repeated keys inside Go models make the entire free capability result
ambiguous. Those fixes are implemented, not yet fully verified. Foreign
provider/property duplicates are ignored; raw keys inside Go models are
checked recursively. The follow-up catalog set passed 62 cases.

The new pure stage2_research_refs.py resolves frozen-byte structural
Markdown sections/criteria, Python AST definitions/module assignments and
canonical safe YAML/JSON key paths; other files use first whole-word matches.
One 4000-Unicode-character budget is shared per claim; any unresolved
citation removes every excerpt from that claim. The historical S-47 prompt
blob is a committed test fixture, requiring no live prompt or Git history.
This helper is not wired to the legacy substring citation path yet; amended
map/report integration remains pending. Initial missing-module tests failed
41 cases; the implemented helper passed 41, followed by 9 failures and one
passing added edge case, then 51 green. The baseline fixture made 52; a
red-first lone-surrogate case now makes 53 green. A combined boundary run
before that final Unicode case passed 114 tests in 20.98 seconds.

Full verification of these current staged changes is running at publication:
exec session 25323, log /tmp/coding-harness-research-refs-verify.log. Do not
change those source bytes until it ends. Then inspect the actual result,
repair if needed, append the measured second span, commit, push the tracker
before Git and update PR #158. The previous full log is
/tmp/coding-harness-research-catalog-verify.log. Planned integration ledger
entries remain pending; standalone tests do not prove actual 39 + 3N calls,
barriers, isolation or research-to-interview-to-spec handoff.

### Decisions, ownership and remaining limits

Continue to the reported deadline 2026-10-18 10:00 Asia/Singapore / 02:00 UTC,
or the actual allowance/hard stop first; retain the five-percent reserve.
At 21:35 UTC the local allowance event measured 47 percent primary and
7 percent weekly use. Re-measure before a long call or stopping decision.
Claude budget remains exhausted, and GLM remains forbidden until
2026-10-21 20:34 Asia/Singapore. No GLM/Claude call, provider admission,
customer access, credential-file read, language rewrite or merge occurred.
The attended F-1 isolation capture remains open and cannot be replaced by
offline unit tests or waived during this night continuation.

Parent is the only tracker writer; the configured scan was empty before the
checkpoint comment. The three earlier requested native research agents are
finished read-only. Main is unchanged at 6029bbf. Research worktree branch
explore/research-swarm has HEAD 379ed28 plus the staged second slice; do not
reset or discard it. Handover branch docs/resume-2026-10-17-models stays in
its own worktree and PR #161. Nothing is required from the maintainer now.

### Validation of this addendum

Preserve all prior handover bytes. The prior handover checkpoint 487a500 has
hosted gates/verify green. This text-only addendum skips local make verify
under the repository rule; its frontmatter/whitespace checks and hosted CI
are the applicable gate. The next session starts by reading the final log
above and the current PR heads, rather than restarting any old runner.
