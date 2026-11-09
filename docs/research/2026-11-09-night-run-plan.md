---
title: "Night-run plan — 2026-11-09 evening to 2026-11-10 07:00 UTC"
category: research
created: 2026-11-09
updated: 2026-11-09
last_reviewed: 2026-11-09
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [night-run, plan, lanes, stage-2]
---

# Night-run plan 2026-11-09/10

The maintainer asked on 2026-11-09 at about 19:50 UTC for a night plan
("bitte bereite schon mal einen Nachtplan vor"): every lane running now
finishes first, then the maintainer restarts Claude Code with a fresh
context, and the new session runs this plan. The plan keeps the rules of the
[night plan of 2026-11-07](2026-11-07-night-run-plan.md) except where this
page says otherwise. One orchestrating session works the lanes and is the
only tracker writer; five to six lanes run, never more (maintainer,
2026-11-06).

## Start of the fresh session

1. Read the handover of 2026-11-09 (`docs/journal/handover/`) and this page.
2. Start Claude Code through the night profile, so a permission question is
   denied at once instead of holding the session (bead coding-harness-ibde,
   maintainer 2026-11-09: use it tonight, before its pull request merges):
   `python3 .claude/worktrees/night-stall-guard/tools/claude-code/night.py`
   from the repository root. The profile was probed on 2026-11-09 with
   Claude Code 2.1.319 (plan of that change, "Runtime probe"); the
   interactive start was not measured.
3. Re-arm the heartbeat (session-only cron, minutes 13 and 43) with the run
   state folder `~/.local/state/coding-harness/night/2026-11-09-a/`, start the
   watchdog there, and keep the machine awake (`caffeinate`).
4. No phone notification at night (maintainer, 2026-11-09).

## Lanes

| Lane | Change (bead) | Until 2026-11-10 07:00 UTC |
|---|---|---|
| 1 | Explore provenance (coding-harness-g19n) | One repair round for phase-6 rows EP6-1 to EP6-4 (maintainer 2026-11-09: hold the pull request, repair them), full `make verify`, phase-6 re-check, pull request — split in two if the slicing rule (~800 lines) asks for it. EP6-5 stays a follow-up (coding-harness-4bhp). |
| 2 | Two `make verify` runs at once (coding-harness-u1ha) | Flash explore, interview record from the maintainer's two answers of 2026-11-09 (two slots; the count centrally changeable), `draft`, stop at the plan card for the morning. Not implemented tonight: it changes the lock every other lane waits on. |
| 3 | Research swarm report format (coding-harness-4q9y) | Flash explore, `draft`, stop at the plan card. Testing strategy (coding-harness-1ga5) waits for it (maintainer 2026-11-09). |
| 4 | Fewer review rounds (coding-harness-3rtn) | `draft` from decisions Q-1 to Q-12 and the research of 2026-11-09; spec and plan only, the ADR 0021 amendment as a draft; stop at the plan card. Implementation waits for coding-harness-twvx. |
| 5 | One central harness configuration (coding-harness-twvx) | Explore with `--stage2-off` and the recorded reason (research swarm report-format failures, coding-harness-4q9y), then park for the interview (architectural; the maintainer's answers are needed). |
| 6 | Follow-up bugs from today's phase-6 reviews | One at a time, Flash explore and `draft` to the plan card: origin check across phase-6 blocks (coding-harness-3h96), no-work ledger marker (coding-harness-twbl), triage-verb round-4 rows (coding-harness-3ha6), research census producer kind (coding-harness-4bhp). |

## Not tonight

- `scripts/stage2.py` refactor (coding-harness-vg9): after coding-harness-twvx,
  when few lanes touch the file (maintainer 2026-11-09).
- Testing strategy (coding-harness-1ga5): after the swarm repair.
- Implement route file (coding-harness-9ycy): blocked on coding-harness-twvx.

## Rules for this run

1. **Questions park.** A lane that meets a question parks; the question goes
   at once, with its context and a recommendation, into the bead's notes.
2. **Appetite is a stop.** A lane at its appetite parks for the morning.
3. **Repairs without asking** as before: a reproduced MAJOR code fault inside
   the spec; MINOR rows on tests, security or false statements.
4. **A repair that edits a held path** (for example a prompt or
   `model-endpoints.yaml`) is lost by the runner's restore: the orchestrator
   makes the held-path edit by hand first, then reruns the repair (seen three
   times on 2026-11-09).
5. **Sync with `main` before phase 6.** A branch behind `main` fails the
   linter on files only `main` changed (seen on 2026-11-09).
6. **No merges at night**, no edits of `docs/adr/`, `gates.yaml` or
   `.github/workflows` by agents.
7. **Handover** as a pull request from its own worktree by
   2026-11-10 07:00 UTC.

## Questions waiting for the morning

- Plan cards of lanes 2, 3, 4 and 6.
- Interview for coding-harness-twvx.
- Merges of the pull requests finished on 2026-11-09 (see the handover).
