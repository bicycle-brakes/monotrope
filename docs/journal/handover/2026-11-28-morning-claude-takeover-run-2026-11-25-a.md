---
title: "Session handover — 2026-11-28 morning: Claude Code took over Run 2026-11-25-a from agy, two merges, nine lanes waiting on the maintainer"
category: handover
created: 2026-11-28
updated: 2026-11-28
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-11-28"
tags: [handover, night-run, lanes, maintainer-decisions]
target_ref: 03c545f4
status: pending
session: "claude-code/9f5865da-471d-4590-a3b2-9a7dc1f4c9ac"
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

Claude Code (Opus 5.5, session `9f5865da`) took over Run `2026-11-25-a` from the Antigravity session on 2026-11-27 ~11:40 CET (Antigravity's weekly budget was spent; the maintainer stopped it and its watchdog sidecar). The maintainer extended the run to **Monday 2026-11-30 10:00 CET** and asked for at least two active lanes at all times.

Since the 2026-11-27 morning handover (`9298a50e`), five pull requests merged into `origin/main` (`03c545f4`): #471 (research-swarm limits ×1.5), #474 (`scripts/enqueue_pr.py`), #475 (morning handover), #476 (research-swarm resume, bead `coding-harness-f6qj`), #477 (worktree-setup-hook race, bead `coding-harness-1ba3`, an orchestrator hand finish approved by the maintainer).

**Most lanes now wait on the maintainer.** Two lanes are blocked by one permission (a hand correction of the `Origin`/`Where` cells in a review-loop record, which the runner asks for and the auto-mode classifier refuses); four lanes need a fourth spec-review round; four need interview or option answers.

The session stalled twice because the Claude usage limit was spent: about 01:30–04:12 and 05:35–09:11 CET on 2026-11-28 (no wakes, no runner steps).

## Next step

1. With the maintainer's permission, correct `Origin` (and for `enqueue-pr-rulesets` also `Where`) of loop row L1-1 in `~/.local/state/coding-harness/stage2/enqueue-pr-rulesets@befa018b/loop.md` and `.../bead-topic-in-research@45179c2d/loop.md`, then `triage`/`repair` → phase 6 → PR. `enqueue-pr-rulesets` (bead `coding-harness-3wtk`) repairs `enqueue_pr.py`, which today refuses every pull request; the maintainer merges it (bootstrap exception).
2. With a fourth-round authorization, re-review and implement the four lanes parked after round 3.
3. Keep two lanes running: `export-import-closure` (bead `coding-harness-5ane.7`) and `triage-where-cell` (bead `coding-harness-3ha6`) are in spec review round 2.

## Needed from the maintainer

1. **Permission for a cell correction in review-loop records** (`loop.md`, outside the repository): set `Origin` to `base` and `Where` to `scripts/enqueue_pr.py:<line>` for L1-1 of `enqueue-pr-rulesets`; set `Origin` to `base` for L1-1 of `bead-topic-in-research`. The reviewers' words stay unchanged. The runner instructs this hand step; the auto-mode classifier refused it as "Undermining Oversight". A permission rule would make it durable.
2. **Fourth spec-review round** (decisions.md `Q-<n> · Fourth spec-review round`, answer beginning `authorized`) for: `bd-trust-check` (bead `coding-harness-5ane.2`, scope narrowed by the maintainer after round 3), `stamp-day-source` (bead `coding-harness-5v6t`), `verify-lock-handle` (bead `coding-harness-42em`), `restore-keeps-runner-entries` (bead `coding-harness-7awf`). Recommendation: yes for all four; the open rows and the planned answers are in each bead's notes.
3. **Option for `read-only-agents-no-shell`** (bead `coding-harness-5ane.22`, rule RB-A2 in the maintainer-only `docs/governance/regelwerk.md`): Option 1 (recommended) marks the rule as partially enforced with a new dated valve; Option 2 waits for full enforcement. The same choice recurs for `coding-harness-5ane.20`, `.21`, `.23`, `.24`, `.25`.
4. **`model-endpoints-refresh`** (bead `coding-harness-363r.5`, 2 BLOCKER: the runner cannot re-measure skipped models): Option B (recommended) — remove only the two deprecated MiMo V2.5 models now, the re-measurement as its own bead.
5. **Interviews**: `research-seat-substitute` (bead `coding-harness-0ysc`, amends ADR 0020; five drafted questions in the bead notes) and `state-first-records` (bead `coding-harness-5ane.11`, eight drafted questions).
6. **Merge this handover pull request.**
7. **P1 cap:** 26 open non-epic P1 beads (plus 8 epics) against the cap of 10, measured 2026-11-28 09:15 CET at `03c545f4`.
8. **OpenCode Go workspace**: several Go models answer 403 "Model access is disabled" (for example `deepseek-v4-pro`, `glm-5.3`); review loops ran with a single member (`hy4-flash-free`). Enabling model access in the OpenCode console would widen them.

## Merged since the 2026-11-27 morning handover (`9298a50e` → `03c545f4`)

| PR | Merged (UTC) | Bead | Summary |
|---|---|---|---|
| #471 | 2026-11-27 11:05 | — | Research-swarm time limits ×1.5 (decision PR). |
| #474 | 2026-11-27 11:45 | `coding-harness-va1l` | `scripts/enqueue_pr.py`, the merge-queue grant enforced by code. |
| #475 | 2026-11-27 12:24 | — | 2026-11-27 morning handover. |
| #476 | 2026-11-27 17:42 | `coding-harness-f6qj` | Research-swarm resume reuses completed repository topic slots (closed by hand: the Closes-Bead trailer was split from the Co-Authored-By paragraph). |
| #477 | 2026-11-27 23:36 | `coding-harness-1ba3` | Lane-setup budget starts after the trust check (orchestrator hand edit with the maintainer's approval; two phase-6 reviews clean). |

## Lanes (as of 2026-11-28 09:15 CET)

| Lane | Bead | Branch head | State |
|---|---|---|---|
| `enqueue-pr-rulesets` | `coding-harness-3wtk` | `fix/enqueue-pr-rulesets` | Implemented (`892de08c`), verify green, loop L1-1 (MINOR, valid) — blocked on item 1. |
| `bead-topic-in-research` | `coding-harness-5vts` | `feat/bead-topic-in-research` | Implemented, verify green, loop L1-1 triaged `taken`; repair refused on `Origin` — blocked on item 1. |
| `export-import-closure` | `coding-harness-5ane.7` | `fix/export-import-closure` | Spec review round 2: 2 rows to decide. |
| `triage-where-cell` | `coding-harness-3ha6` | `fix/triage-where-cell` | Spec review round 2 by the fallback reviewer; rows to read. |
| `bd-trust-check` | `coding-harness-5ane.2` | `fix/bd-trust-check` | Parked: fourth round (item 2). |
| `stamp-day-source` | `coding-harness-5v6t` | `fix/stamp-day-source` | Parked: fourth round (item 2); implement attempt 1 rejected by the orchestrator's own too-broad S-4 detail. |
| `verify-lock-handle` | `coding-harness-42em` | `fix/verify-lock-handle` | Parked: fourth round (item 2). |
| `restore-keeps-runner-entries` | `coding-harness-7awf` | `fix/restore-keeps-runner-entries` | Parked: fourth round (item 2). |
| `read-only-agents-no-shell` | `coding-harness-5ane.22` | `test/read-only-agents-no-shell` | Parked: option (item 3). |
| `model-endpoints-refresh` | `coding-harness-363r.5` | `chore/model-endpoints-refresh` | Parked: option (item 4). |
| `research-seat-substitute` | `coding-harness-0ysc` | `fix/research-seat-substitute` | Parked: interview (item 5). |
| `state-first-records` | `coding-harness-5ane.11` | `explore/state-first-records` | Phase 1 complete (research run 6), parked: interview (item 5). |

## Decisions and lessons of the night

- Round-3 spec-review rows are no longer written into the spec by the orchestrator: a spec change after round 3 makes the review stale and implement refuses (`stamp-day-source`); such lanes park for a fourth-round authorization.
- The `Closes-Bead` trailer must sit in the same paragraph as `Co-Authored-By` (tracker memory `closes-bead-same-trailer-paragraph`).
- A research-swarm receipt is valid for 15 minutes; prepare and explore now run back to back.
- `state-first-records` runs 4 and 5 failed on finder seat 2 (`mimo-v2.6-flash` returned a tool call instead of JSON); run 6 completed with `glm-5.3-flash` on that seat (the orchestrator's choice under the night-run rules, recorded by the runner as "maintainer's choice").
- New beads: `coding-harness-cqwd` (CI: text-only PRs skip the test suite), `coding-harness-vndh` (stand-in log guard fires on pytest's tmp cleanup), `coding-harness-3wtk` (enqueue_pr.py refuses every PR).

## Findings per model

### `origin/main` — cutoff commit `03c545f4`

Measured 2026-11-28 09:15 CET with `make findings-per-model REV=origin/main` (exit 1 for the known unattributed rows in older changes).

| Model | Raised | Defects accepted | Questions settled | Rejected |
|---|---:|---:|---:|---:|
| cat-jam-free | 3 | 3 | 0 | 0 |
| deepseek-v4-pro | 19 | 18 | 0 | 1 |
| deepseek-v4.1-flash | 397 | 387 | 0 | 10 |
| glm-5.2 | 8 | 8 | 0 | 0 |
| glm-5.3 | 75 | 70 | 0 | 5 |
| glm-5.3-flash | 183 | 179 | 0 | 4 |
| gpt-6.1-sol | 384 | 364 | 0 | 7 |
| gpt-6.1-terra | 97 | 83 | 0 | 11 |
| hy3 | 81 | 70 | 0 | 11 |
| hy4-flash-free | 26 | 25 | 0 | 1 |
| hy4-preview | 86 | 81 | 0 | 5 |
| kimi-k2.7-code | 20 | 19 | 0 | 1 |
| kimi-k3 | 14 | 14 | 0 | 0 |
| longcat-2.0 | 74 | 71 | 0 | 3 |
| longcat-2.5-free | 13 | 11 | 0 | 2 |
| longcat-2.5-preview-free | 1 | 1 | 0 | 0 |
| mimo-v2.5 | 41 | 40 | 0 | 1 |
| mimo-v2.6-flash | 263 | 255 | 0 | 8 |
| mimo-v2.6-pro | 168 | 155 | 0 | 13 |
| minimax-m3 | 20 | 20 | 0 | 0 |
| minimax-m3.1-flash | 35 | 33 | 0 | 2 |
| qwen3.7-plus | 24 | 16 | 0 | 8 |
| qwen3.8-flash | 140 | 132 | 0 | 8 |
| step-5-preview | 10 | 10 | 0 | 0 |
| unattributed | 111 | 108 | 0 | 3 |

### Unmerged change branches

No unmerged branch gained released phase-4b or phase-6 rows in `findings.md` overnight: the two loop rows of the night (L1-1 of `enqueue-pr-rulesets` and of `bead-topic-in-research`) are still unreleased in their `loop.md`. Not measured per branch.

## Working state and parallel-session boundary

- Root checkout: clean on `main` at `03c545f4`.
- Single tracker writer: this Claude Code session. The Antigravity main session and its watchdog sidecar were stopped by the maintainer on 2026-11-27 (`sidecar.json` renamed to `sidecar.json.disabled`); the Antigravity IDE and its hub keep running because this session runs inside the IDE.
- Session-only schedules: 30-minute wake (`:07`/`:37`), daily handover ~09:27, final handover Monday 2026-11-30 ~09:23; `caffeinate` until Monday ~10:05. All end if this session closes.
- Run log: `~/.local/state/coding-harness/night/2026-11-25-a/lane-watch.log`.

## Validation

- `python3 scripts/check_frontmatter_current.py` and `python3 scripts/check_dangling_bead_ids.py` run in this worktree (results below the commit).
- Not run: full `make verify` (text-only Markdown handover; CI is its gate).

## Addendum — 2026-11-28 09:27 CET

- `export-import-closure` (bead `coding-harness-5ane.7`) and `triage-where-cell` (bead `coding-harness-3ha6`) finished spec review round 3 with 1 and 2 rows and are parked for a fourth-round authorization; planned answers are in each bead's notes. The fourth-round list in "Needed from the maintainer" item 2 therefore has six lanes: `bd-trust-check`, `stamp-day-source`, `verify-lock-handle`, `restore-keeps-runner-entries`, `export-import-closure`, `triage-where-cell`.
- No new lane was opened at 09:20: each of the last eight lanes parked after round 3, and the spec reviews spend the Claude budget whose limit stalled the run twice overnight. The orchestrator waits for the maintainer's answers before opening more, unless the maintainer asks otherwise.
- Running jobs at 09:27: none besides `caffeinate`.
