---
title: "Session handover — five-lane night 2026-11-02/03, 2026-11-03"
category: handover
created: 2026-11-03
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-11-03"
tags: [handover, night-run, lanes, stage-2]
target_ref: 019853f1
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The night run of 2026-11-02/03 (plan: `docs/research/2026-11-02-night-run-plan.md`)
ran all five lanes until each reached a point that needs the maintainer; as of
2026-11-03 03:55 UTC no lane job is running. Three pull requests wait for review
(#319, #320, #321); lane B's (#320) blocks lane C. Lanes A, D and E each stand
before a maintainer decision, and four explores stand before their interviews.
Every state below was read on 2026-11-03 between 01:00 and 03:55 UTC; `main`
is at 019853f1.

## Next step

Review and merge #320 (red-first proofs in a private clone, bead
coding-harness-wkxm) after reading its named limits, then start lane C (one Go
access point, bead coding-harness-4tr4): merge `main` into worktree
`go-access-point` and run the round-8 repair from
`refs/stage2/attempts/go-access-point/enospc-20261102`.

## Needed from the maintainer

One at a time, in this order (each through the interview form with context):

1. **#320, lane B (red-first proofs in a private clone):** merge with its named
   limits, or keep repairing F-10 (root references such as ORIG_HEAD are not
   measured; remedy proposed in its `findings.md`). Recommendation: merge; F-10
   as a follow-up bead. Consequence: lane C can start.
2. **Lane D (time records as data, bead coding-harness-v6vk):** every loop round
   saw the diff cut at 2000 of 2035–2194 lines (bead coding-harness-ut8q), so the
   loop cannot end clean. End it with a named stop and start phase 6, as for lane
   B on 2026-11-02? Recommendation: yes. Also review the orchestrator's hand
   acceptance (two lines, recorded in its `plan.md`).
3. **Lane E (guard test, bead coding-harness-0ho), two loop rows parked:**
   L1-2 `[AMBIGUITY]` — does the guard proof mark go only into the private record
   (today's code and test, the reading spec criterion 7's "existing location"
   suggests) or into every row location? L1-9 — should the runner enforce that a
   guard repair changes test code only? That is a new guarantee (bead
   coding-harness-mwzv.1 says such remedies are the maintainer's).
   Recommendation: L1-2 private record only; L1-9 a follow-up bead, not this change.
4. **Lane A (self-closing beads, bead coding-harness-l1if):** F6-6 parked — with
   `trailer.separators` configured, Git prints `Closes-Bead=` and the collector
   drops every declaration. Proposed remedy: the collector runs Git with a neutral
   configuration. Accept? Third finding of one mechanism (F6-1, F6-4, F6-6).
5. **Night choices to confirm:** lane B's remedies for F-7 (raw bytes, which
   caused F-8 and F-9) and for F-8/F-9 (logical reference map) were chosen by
   the orchestrator under "repair on".
6. **ADR 0016 text (bead coding-harness-v9xx):** the exact amendment is below
   under "Proposal: ADR 0016"; open the decision pull request from it?
7. **Interviews for four explores** (stopped before phase 1a): keep rate (bead
   coding-harness-363r.1, `spike/keep-rate`), runner stops at the appetite
   (bead coding-harness-uxa9, `feat/appetite-stop`), stop hook (bead
   coding-harness-788, `feat/stop-hook`), questions through the interview tool
   (bead coding-harness-8v2c.1, `docs/questions-interview-tool`).

## Decisions and preferences

- The night plan's twelve answers stand (`docs/research/2026-11-02-night-run-plan.md`).
- Lane B used its three allowed re-checks (F-7, F-8/F-9, F-10); its pull request
  opened without auto-merge, as answer 10 says.
- Night answers were cut, park or drop; no lane continued past a question.
- 2026-11-02: every question to the maintainer goes through the interview tool
  with ADR 0018's context (bead coding-harness-8v2c.1 makes it doctrine).

## Open work and blockers

Task status lives in Beads; this lists only where each lane stopped.

| Lane | Bead | Where it stopped (2026-11-03) |
|---|---|---|
| A | self-closing beads (coding-harness-l1if) | F6-4, F6-5 repaired (a2140674); re-check found F6-6, parked (66100f2b). Backlog 6ie and k93f wait for a `scripts/stage2.py` slot (night rule 3). |
| B | red-first proofs (coding-harness-wkxm) | PR #320 open, `make verify` green at 0f7e2783. Backlog uxa9 and 788 explored (see 7 above). |
| C | one Go access point (coding-harness-4tr4) | Blocked until #320 merges. 1gzo not drafted (may amend ADR 0021: architectural). v9xx proposal below. |
| D | time records (coding-harness-v6vk) | Implemented, hand-accepted (63ac2f74); loop rounds 1–3 repaired or decided; loop cannot end (cut diff). Backlog gxwg waits; 8v2c.1 explored. |
| E | guard test (coding-harness-0ho) | Doctrine written (WORKFLOW, prompts 04/04b/06, findings template); verify green; loop round 1 decided, L1-2 and L1-9 parked; it is a decision PR (gate in branch). Pi probe done (#321); keep rate explored. |

Created tonight: bead coding-harness-mwzv.2 (the runner writes
`compaction.enabled=false` into every Pi settings file, P1, bounded). Noted on
bead coding-harness-xul8: every review-loop call also sends Pi's system prompt
with the absolute install path (home directory, worktree name); the leak check
does not see that text.

Not done tonight: bead coding-harness-ut8q's R6-2/R6-3 repair (worktree
`review-diff-order`) — not reached; the fix-r and ADR 0018 follow-ups.

### Proposal: ADR 0016 (bead coding-harness-v9xx)

Read on `origin/main` 2026-11-03: the draft runner's check is
`DOCS_VERIFY = ["bash", "scripts/verify_all.sh", "--job", "docs"]`
(`scripts/stage2.py`, `verify_draft`); `docs/WORKFLOW.md` already says so.
Amend in place, title `decide(adr-0016): the draft's document check replaces
make verify in decisions 2, 3 and 7`, label `decision`:

- Decision 2: "then the derived files, `make verify`, and the checks" →
  "then the derived files, the document check `bash scripts/verify_all.sh
  --job docs`, and the checks".
- Decision 3: "for its `make verify`," → "for its document check
  (`bash scripts/verify_all.sh --job docs`),".
- Decision 7: "(Q-4): `make verify`, the" → "(Q-4): the document check
  `bash scripts/verify_all.sh --job docs`, the".
- Note after the Decision section: "Amended 2026-11-01 (bead
  coding-harness-77qj, no behavior change): the draft runner's post-run check
  is the verify job's document subset, `bash scripts/verify_all.sh --job docs`,
  not `make verify`; decisions 2, 3 and 7 name it. Implement and repair keep
  the full `make verify`."

## Working state and parallel-session boundary

- One orchestrating session (this one) wrote the tracker; no other session ran.
- Worktrees with pushed branches (all clean as of 03:55 UTC):
  `red-first-own-refs` (fix/red-first-own-refs, 0f7e2783, PR #320),
  `beads-close-themselves` (66100f2b), `time-records-data` (feat/time-records-data,
  last commit the round-4 audit lines), `guard-test` (feat/guard-test, c878b9c3),
  `keep-rate`, `appetite-stop`, `stop-hook`, `questions-interview-tool`,
  `go-access-point`, `review-diff-order`, this handover's `handover-1103`.
- Saved attempts: `refs/stage2/attempts/time-records-data/orchestrator-saved-20261103`
  (bc486f94), `refs/stage2/attempts/guard-test/orchestrator-saved-20261102`.
- Loop records outside the repository: `~/.local/state/coding-harness/stage2/`
  `guard-test@8d312694`, `time-records-data@9a72ead9`.
- `caffeinate` runs until about 11:00 UTC.

## Validation

- `make verify` green: lane B at 0f7e2783, lane E after 3755e313's follow-ups
  (cap raise commit), lane D at 63ac2f74 — all 2026-11-03.
- Each runner repair ran its own `make verify` (A a2140674, B 71754269 and
  732058b1, D 0a01ad38 and fc986a52).
- Pi context probe: 3 calls, about 0.001 USD by catalog prices (#321).
- Not run: phase 6 for lanes D and E; the hosted CI of the open branches was not
  read.
