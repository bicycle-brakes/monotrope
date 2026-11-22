---
title: "Session handover — heartbeat night 2026-11-05/06 and morning questions, 2026-11-06"
category: handover
created: 2026-11-06
updated: 2026-11-06
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-11-06"
tags: [handover, night-run, heartbeat, lanes, review-loop, stage-2]
target_ref: a8e23d17
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

After a restart on the evening of 2026-11-05 the session resumed the six
lanes of the previous handover (PR #338) and ran the night with a heartbeat:
a 30-minute session cron, a token-free lane watchdog and keep-awake (bead
coding-harness-7x3c; maintainer: the heartbeat becomes a fixed part of every
night run). Nothing merged overnight. Eighteen change branches stand pushed;
most lanes are parked on a question for the maintainer. On the morning of
2026-11-06 the maintainer answered three questions and asked to stop all
running processes; at hand-over (about 10:45 UTC) no runner job, make verify,
watchdog, cron or keep-awake is running.

## Next step

Merge-check PR #340 (excludes `iceman-contributor-free` from the free review
swarm); once it is merged, run a fresh `prepare-loop` and `review-loop` for
the five implemented changes waiting on it — research-free-paid,
night-machine-facts, status-fields-restore, redraft-after-scope,
pi-no-compaction — and start the lane-D mechanism repair (row F6-4, answer A
below).

## Needed from the maintainer

1. **Merge PR #340** (decision: exclude `iceman-contributor-free`).
2. **Merge PR #339** (AGENTS.md: night runs stay plain) and **#338** (previous
   handover) when ready.
3. The open questions below, one at a time, each with a recommendation.

## Decisions and preferences

Recorded this session, not to be asked again:

- The heartbeat (30-minute wake, lane-watch log, watchdog, keep-awake) is a
  fixed part of every night run (2026-11-06); the agent may insert the
  AGENTS.md sentence for it when bead coding-harness-7x3c lands ("Du darfst
  das").
- Implementers change often: the implement route lives in one central,
  plainly editable file, not in an ADR (bead coding-harness-9ycy, first slice
  of coding-harness-wq1m); GLM 5.3 replaces GLM 5.3 Flash at once; the eval
  pipeline (bead coding-harness-phcy, slimmed: replay 3–5 merged changes,
  pass^k with k=3 only before a switch, one JSONL file) measures afterwards.
- Model access per use case goes into one central, easily adjusted policy
  ("nur free", "ohne contributor" …) — bead coding-harness-k0ub with
  coding-harness-wq1m. Bridge: PR #340 (Q-M9, option A).
- research-free-paid needs no ADR (Q-M2, "Nein"); recorded with
  `harness.py decide adr` (commit 0baba58f), so its PR is a decision PR.
- Lane D, F6-4: mechanism repair now (Q-M6, option A) — `review_audit_only()`
  strips every runner audit line wherever it sits and compares only verdict
  and session lines; one test per placement.
- Night runs stay plain; collecting data is allowed, a display service is not
  (PR #339). The runner audit log becomes JSONL with OpenTelemetry GenAI field
  names (bead coding-harness-oebl, linked to coding-harness-zaqf).
- Observe → measure → tune belongs to the scientific approach (bead
  coding-harness-0887).
- New beads on request: coding-harness-9ycy, coding-harness-7x3c,
  coding-harness-phcy, coding-harness-3gc6 (Namespace sandbox spike),
  coding-harness-te7q (bug, below); coding-harness-36za widened to nine models.

## Open work and blockers

Bug found tonight: **coding-harness-te7q** — the runner accepts an implement
attempt that changed only its own bookkeeping as "verified and committed"
(three times: mutation-spike on Flash, verify-worker-count on Flash and on
Sonnet). Check every accepted implement diff by hand until it is fixed.

| Change (worktree `.claude/worktrees/<name>`) | Bead | State at hand-over | Waits on |
|---|---|---|---|
| research-free-paid | wb40 | implemented, hand acceptance 1 (CI caller reason, stamps), ADR answer; pushed 0baba58f | PR #340, then prepare-loop |
| night-machine-facts | yql7 | implemented (Sonnet, 946 lines), pushed | PR #340 |
| status-fields-restore | ljmi | implemented (Flash, 836 lines), pushed | PR #340 |
| redraft-after-scope | y0qm | implemented (Sonnet, research note), pushed | PR #340 |
| pi-no-compaction | mwzv.2 | implemented (Sonnet, 382 lines), pushed | PR #340 |
| repair-targeted-check | gxwg | phase 6 F6-4 BLOCKER open; answer A given | start the repair |
| handoff-new-feature | in27 | round-8 repair committed a256a44f; diff cut at 2000 lines, so no round can end the loop | next round; bead hchx |
| research-store-home | nxdy | round 8 untriaged | Q-M12 |
| explore-provenance | g19n | round 6 untriaged | Q-M11 |
| conflict-marker-gate | i76l | Sonnet attempt 3 red only on gate registration; saved as ref `refs/stage2/attempts/conflict-marker-gate/orchestrator-saved-20261106` and uncommitted in the worktree | Q-M5, Q-M1 |
| mutation-spike | bvy | implement accepted empty (te7q); round 1: 22 rows incl. a BLOCKER | Q-M8 |
| verify-worker-count | xay1 | implement accepted empty twice (te7q) | te7q |
| implement-route-file | 9ycy | explored | Q-M3 |
| go-wire-apis | 36za | explored | Q-M4 |
| outcome-test | 3nm5 | explored | Q-M7 |
| definitive-refusal | 2ym2 | explored | Q-M10 |
| night-heartbeat | 7x3c | drafted (spec, plan) | implement |
| exclude-iceman | — | PR #340 | maintainer merge |

### Open questions (parked overnight; answered ones removed)

- **Q-M1** · New script without a CI caller fails implement (lanes G and C):
  recommendation A — the implement prompt names "every new script needs a CI
  step or an OHNE_AUFRUFER entry with its reason".
- **Q-M3** · Bead 9ycy: who may change the route file? Recommendation A — the
  agent on the maintainer's word, no decision PR. Also: the accepted spec
  implementation-verification says "no additional attempts" on the Flash
  route, and bead 6ie (in progress) was named to land before ladder changes.
- **Q-M4** · Bead 36za: measure and map each wire API (Messages, Responses,
  Google) — recommended — or go through Go's Console translation.
- **Q-M5** · Lane C: the new blocking gate lacks a ci.yml step and a leerprobe
  reason; recommendation — add both by hand (hand acceptance 1, named in the
  PR), full make verify, review loop.
- **Q-M7** · Bead 3nm5: which questions, how often, where results live;
  recommendation — eight questions, on demand before a handover or AGENTS.md
  change, one JSONL in docs/research/.
- **Q-M8** · Lane bvy: park until te7q and g19n merge, then rerun implement.
  The orchestrator's interview skip there wrongly claimed the tool choice was
  settled (rows L1-8, L1-14).
- **Q-M10** · Bead 2ym2: on 403 or 410 may a paid stage retire itself and the
  round continue (recommended), or stop with the release-loop command?
- **Q-M11** · Lane E, third finding of the provenance-backfill mechanism
  (L4-1, L5-2, L6-1/L6-4): recommendation A — the census checks the whole
  metadata contract and one script normalises every active research file.
- **Q-M12** · Lane B, third finding of the store-permission mechanism (L5-1,
  L8-1 to L8-3): recommendation A — the research store refuses to run as
  root; criterion 5 rewritten by re-running draft.

## Working state and parallel-session boundary

- Branches and last commits: the table above; all pushed. Uncommitted, not
  read in detail: one runner-written file each in research-store-home,
  explore-provenance, night-machine-facts and mutation-spike (findings.md
  audit lines of prepare-loop or review-loop, expected), and the saved lane-C
  attempt (six files).
- `.claude/worktrees/` holds about 60 worktrees, many of merged changes; a
  disk-space cleanup is due (the night of 2026-11-01/02 ran out of disk).
- The night's working files lived in the session scratchpad and are gone with
  it; the watchdog script survives as
  `plans/changes/night-heartbeat/trial-lane-watchdog.sh.txt` on branch
  feat/night-heartbeat.
- Only runner-started Claude sessions (the start hook named them
  `<change>-<n>`) shared worktrees with this one; no other session wrote the
  tracker.

## Validation

- Full make verify green: research-free-paid at 0baba58f's tree (2026-11-06,
  third run; earlier runs red on the midnight stamps and the missing ADR
  answer) and exclude-iceman at 8b938b12 (PR #340).
- Targeted tests: the handoff-new-feature prompt edit (293 passed), later
  reverted because the spec keeps prompts/ unchanged (b04c119d).
- Not run: phase 6 for any lane after its last repair; the review loops of the
  five changes waiting on PR #340.
- Lessons: an interview skip must be checked against research.md's open
  points (bvy); a row that only strengthens a test is "taken — not a test"
  (lane F round 8 failed three repair attempts on that); make verify is the
  bottleneck — one at a time, 20–35 minutes under load.
