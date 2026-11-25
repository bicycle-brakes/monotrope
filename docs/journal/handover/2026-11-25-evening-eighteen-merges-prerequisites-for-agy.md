---
title: "Session handover — 2026-11-25 day and evening: eighteen merges, the prerequisites for the 72-hour Antigravity run"
category: handover
created: 2026-11-25
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-11-25"
tags: [handover, lanes, merge-queue, antigravity, autonomy, tracker]
target_ref: a679f0f0
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
updated: 2026-11-25
---

# Resume here

## Where we are

Session 9200c6b1 (profile `~/.claude-mp`, Claude Code, orchestrator and the
only tracker writer) took over from the night run 2026-11-24-a (handover PR
#456) at about 12:30 CET and worked until 21:30 CET. Everything listed under
"Running" below was **still running** when this handover was written; the
session goes on and keeps its 30-minute wake (`7,37 * * * *`, session-only).

Eighteen pull requests merged today (#445–#463 except #449, which was
closed). The goal set by the maintainer: a **72-hour autonomous run with
Antigravity (`agy`) and Gemini 4 Neon High as orchestrator, always two lanes
in parallel**, starting once three prerequisite lanes are merged
(enqueue-pr, agent-policy-list, worktree-setup-hook).

## Next step

1. Finish the three prerequisite lanes (table below) to clean phase 6 and
   admit them; then write the rule PR for the 72-hour run (answers below),
   install `~/.gemini/config/GEMINI.md` and the start hook, write the run's
   agy settings file, hand over to agy.
2. ladder-next-step: three hand steps were in progress (see table).
3. pi-work-route: the spec draft was running after the interview.

## Needed from the maintainer

- **The rule PR for the 72-hour run** (not written yet) — the maintainer
  merges it.
- **Codex Desktop automation** (bead coding-harness-xrcd): check on the
  laptop whether a Codex Desktop automation runs in this repository; it is the
  likely writer of the stray `.codex/agents/` copies (evidence below).
- Optional: `tmux -L coding-harness kill-server` ends an idle tmux server left
  by the job-launcher smoke test (auto mode refused that kill).

## Merged today

| PR | What |
|---|---|
| #450 | review-loop rounds carry up to 4,000 diff lines |
| #451 | a repair cannot keep files outside its rows' scope |
| #452–#455, #457 | test and verify speed-ups, scrub import, cheap-checks worker cap |
| #456, #448 | night and afternoon handovers |
| #458 | swarm stand-in counts earlier calls from a locked counter (conflict with main resolved by hand) |
| #459 | **standing grants**: structural remedies at a further case of one mechanism; the orchestrator admits pull requests to the merge queue itself (phase 6 clean, verify green, `Closes-Bead`) |
| #460 | red-first proof reports what pytest truly reported (a CI-only denylist test fixed) |
| #461 | findings per model; legacy duplicate grammar **frozen** (re-measured twice after syncs with main) |
| #462 | **ADR 0026**, `scripts/jobs.py` detached job launcher (tmux smoke test recorded on the PR) |
| #463 | twelve ramp valves re-dated 2026-11-30 → 2026-12-31 (bead coding-harness-5ane.1) |
| #445, #446, #447 | audit synthesis, house rule 11, visitor docs |

Closed: #449 (one-line pointer from ADR 0021 to ADR 0025; the pointer travels
with advance-verb, noted on coding-harness-z40g).

## Running at 21:30 and open work

| Lane | Bead | State |
|---|---|---|
| worktree-setup-hook | coding-harness-wg4z | phase-6 re-check running; trust now **only a commit on origin/main** (maintainer, security P6-1); 47 hook tests green |
| enqueue-pr | coding-harness-va1l | review-loop round 3 running (availability id b25ff24a…); round 2's 21 rows fixed by repair + hand finish 5c673baf |
| agent-policy-list | coding-harness-r7zc | round 5 wrote 6 rows (catalog not re-rendered, mutation evidence, kit classification, exact-match registration, Antigravity protocol wording, host check not recorded) — **not yet triaged** |
| ladder-next-step | coding-harness-hwll | implement attempt failed post-run; hand finish in progress in the worktree (uncommitted): prompts 04b/02a/06 and AGENTS.md now name `next: repair/review <change>`; **one test still red**: `test_spent_ladder_next_step_does_not_start_or_mutate` (a findings.md is created) |
| pi-work-route | coding-harness-363r.3 | interview done (Q-1..Q-5 in decisions.md); spec draft running |
| isolated-writing-attempts | coding-harness-s9r | waits: large Claude implement, held back while the Claude window is scarce |
| advance-verb | coding-harness-z40g | after ladder-next-step |

## Decisions and preferences (maintainer, 2026-11-25)

- Standing grants (#459); the orchestrator may decide spec-review questions
  of **bounded** changes itself except BLOCKERs, recorded as details; it asks
  for security and architectural questions.
- **72-hour run with agy**: model Neon High; one long agy conversation with
  timers plus a 2-hour watchdog automation; `--mode auto` with a run settings
  file (ask → deny), merges first `gh pr merge <n> --merge`, after enqueue-pr
  only the script; install `~/.gemini/config/GEMINI.md` (draft in the session
  scratchpad `agy-prep/`) and the start hook as a PR; beads by priority, two
  lanes, bounded/spike to PR, feature/architectural to explore plus interview
  questions; appetite: park only after +50 % buffer; other sessions allowed in
  own worktrees without tracker writes; DeepSeek stays in the swarm until
  2026-11-30; no cost cap but a report; notify only stop events (agy Remote
  Control); handovers daily 09:00 and at the end.
- enqueue-pr: one admission path (`scripts/enqueue_pr.py`, maintainer mode
  `--maintainer` for decision PRs, handovers etc.); GraphQL enqueue pinned to
  the head; clean phase 6 means every row fixed or rejected.
- agent-policy-list: one harness-neutral check command plus thin hooks;
  compound lines split as the shell reads them, `bash -c` behind wrappers
  checked; Codex not supported (no pre-tool hook; bead coding-harness-1tn1).
- pi-work-route: all three parts; order Go → Codex → Claude; DeepSeek V4.1
  Flash default with GLM 5.3 Flash fallback; new ADR; own path-checked write
  tools first, containers later (coding-harness-363r.6); Herdr checked — no
  isolation of its own.
- Opus as a second phase-6 reader for architectural and security changes
  (coding-harness-mwzv.5), evaluated with findings-per-model.
- Research swarm: optimise in order coding-harness-0ysc (substitute seat),
  0yui (readable synthesis), jghc (draft Q-records, claim bases), then the
  measurement spike m9ms. Measured: 2 of 10 runs complete; research.md
  ~65,000 lines, 80 % JSON.

## Tracker work (this session is the writer)

New beads: a6ns.3 (containment backends), a6ns.4 (launcher edge cases), jdsr
and 9yjt (flaky tests), va1l, r7zc, wg4z, 5ane.20–25 (rule enforcers for the
72-hour run), mwzv.5, mwzv.6 (phase-6 answers with guard-evidence lines
refused), 1tn1 (Codex pre-tool hook), 363r.5 (model list clean-up), 363r.6
(containers), 0ysc, 0yui, jghc. Closed: hw7w (DeepSeek terms re-read).

## Working state

- **Claude default profile** (runner's Claude calls): hit its 5-hour limit
  twice today (reset 18:10, then 23:10; the maintainer re-enabled access
  about 21:05). Probe with `env -i HOME=$HOME USER=$USER LOGNAME=$LOGNAME
  PATH=/usr/bin:/bin:$HOME/.local/bin claude -p OK` — without USER/LOGNAME
  the probe falsely says "OAuth session expired" (tracker memory updated).
- **`.codex/agents/` copies** (coding-harness-xrcd): the 20:23:09 copies in
  agent-policy-list and ladder-next-step coincide to the second with Codex
  Desktop sessions (originator "Codex Desktop", source "vscode"); the
  runner's codex_exec calls created none. Copies were byte-identical and moved
  to the session scratchpad.
- OpenCode Go (measured ~17:50): 10 admitted models reachable; 7 disabled
  in the workspace (403), mimo-v2.5 and -pro deprecated (410); bead 363r.5.
- GitHub returned intermittent 500/502 errors all evening; `gh api` REST
  worked where GraphQL failed.

## Orchestrator mistakes

- Two test-file rows triaged as criterion rows again (worktree-setup-hook
  L1-1) → three refused repair attempts; finished by hand.
- A helper split loop rows on `|` and broke escaped pipes (L2-1), and labelled
  every detail section "round 1"; both corrected, memories recorded.
- One review started with `&` inside a command; stopped within seconds, no
  model call, nothing left behind.
- The first spec probe of the default profile misread a keychain failure as
  an expired login and sent the maintainer to log in again needlessly.

## Validation

- Every merged PR: phase 6 clean and `make verify` green on its head or by
  CI in the merge queue.
- Not run: a full `make verify` on the uncommitted ladder-next-step state.

## Addendum — 21:40 CET

- **#461 merged** (findings per model) after a second sync with main: three
  more legacy duplicate statuses arrived and were added to the frozen
  inventory; a CI-only failure (the inner `make` printed "Entering
  directory") was fixed with `--no-print-directory`.
- **worktree-setup-hook (wg4z):** the phase-6 re-check found one more no-perl
  edge case (a child ignoring TERM); fixed by hand (the group gets KILL when
  the limit is reached), 48 tests green; the next phase-6 re-check is running.
  Trust is now only a commit on origin/main (maintainer, P6-1 security).
- **enqueue-pr (va1l):** round 3 (11 rows) repaired by codex-repair; still to
  do by hand on runner-held files: L3-1 bootstrap note (the PR that adds
  the script is merged by the maintainer), L3-2 transition note (lanes whose
  phase 6 predates `Reviewed commit:` get a re-check), L3-3/L3-4 restore the
  no-queue alternative as steps 5-8 in `prompts/07-commit.md`, L3-11 the
  ask-over-allow precedence in docs/WORKFLOW.md. L3-1/L3-2 were marked
  "fixed" by the model although they are hand steps — reopen them.
- **agent-policy-list (r7zc):** round 5 (6 rows) fixed by repair and hand
  (gate catalog re-rendered, kit rules, mutation-named drift test, host
  table "pending the recorded host check", adapter docstring cites the agy
  hooks documentation); review-loop round 6 running.
- **pi-work-route (363r.3):** interview done (Q-1..Q-5). The draft failed:
  the `research-handoff` gate needs a complete v2 run for an architectural
  change. Maintainer: run 3 with the per-topic limit doubled to 20 minutes
  (committed in the lane, a4cc09d1); the earlier partial results stay in
  research.md. **Run 3 needs Claude** (Haiku finders, Opus merge and judge)
  and waits for the reset at 23:10. Seat recommendation (prepare-explore
  21:36): repository and online trios deepseek-v4.1-flash, mimo-v2.6-flash,
  glm-5.3-flash — **to confirm with the maintainer** (Q-18). The draft also
  named its ADR 0026, already taken by #462: the next draft must use 0027.
- **Maintainer requirement:** the runner must continue a started research
  run instead of recomputing it — bead coding-harness-f6qj raised to P1.
- **Codex Desktop (xrcd):** the maintainer confirmed an automated process in
  the Codex Desktop app; option A (shared `.git/info/exclude`) or stopping
  the automation remains to decide.
- **Claude default profile:** the 5-hour limit was hit again at about 21:35
  (reset 23:10). Runner steps that need Claude wait until then; Codex and Go
  steps continue.
- ladder-next-step: unchanged since the main entry (hand finish in progress,
  one test red).
