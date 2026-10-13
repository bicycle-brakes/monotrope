---
title: "Session handover — second night run, as of 2026-10-13"
category: handover
created: 2026-10-13
updated: 2026-10-13
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-13"
tags: [handover, session, night-run]
target_ref: 14f6e1a
bead: coding-harness-yuw
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Morning handover — second night run, 2026-10-13

One orchestrating Claude Code session worked the night queue of 2026-10-12/13
strictly one change after the other, from about 23:30 to 09:40. Nothing was
merged. Two of five queue items reached a pull request, a third is in its
review loop; the two explorations did not start.

## 1. The three priorities for today

1. **Decide F-13 on #133** (Codex drafts spec, design and plan; bead
   coding-harness-rhq). The last repair moved the "only this change's ADR
   answer is missing" exception into the ADR-answer gate (an environment
   variable the runner sets), because the spec's design — the runner reading
   the gate's red output — was bypassed three times by forged gate frames
   (rows F-6, F-9, F-10). The spec protects `scripts/check_adr_answers.py`, so
   code and spec diverge. Recommendation: amend spec and design to the
   gate-side exception. F-14 and F-15 (MINOR) wait behind that answer.
2. **Fix the GLM refusal** (bead coding-harness-3fc, diagnosis recorded on the
   bead). Claude Code 2.1.296 refuses `glm-5.3-flash` and `glm-5.3` as
   unrecognized models before any API call (`[claude-code:unrecognized_model]`);
   its own message names `CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1`
   as the way back. This is the "claude call failed: exit 1" of 2026-10-12. The
   refusal is intermittent: other GLM calls the same night passed. A small
   runner change may make the Pi fallback unnecessary.
3. **Merge #132** if you agree (runner formats an attempt before `make
   verify`, bead coding-harness-52r). After that, #133 needs main merged in
   (`scripts/stage2.py`).

## 2. Done — waiting for your merge

| PR | What | State |
|---|---|---|
| #132 | the runner formats an attempt before `make verify` (ruff, safe fixes only) | `make verify` green at `0355f3e`; 3 loop rounds, Codex phase 6: no BLOCKER, no MAJOR |
| #133 (draft, decision) | Codex drafts spec, design and plan; Opus 5.5 reviews the spec (ADR 0016) | `make verify` green at `3ed807d`; F-13 to F-15 open, escalated after two phase-6 repair rounds |

## 3. In progress

Change adr-owning-change (bead coding-harness-afa, ADR 0014), branch
`feat/adr-owning-change`: implemented at `ae1dbd3` (`make verify` green);
review-loop round 1 wrote three rows, all taken as text or travel rows; the
runner's repair of them was running at 09:40. Next: rounds 2 and 3, Codex phase
6, then the decision pull request.

## 4. Stuck or not as planned

- **Red first has no form for a test-strength row** (bead coding-harness-y17).
  Five rows across the two changes criticised a weak test while the code was
  right; the repair verb failed all attempts on them until they were taken as
  `not a test`.
- **Runner bookkeeping, not code, failed most repairs.** A missing line under
  `## Time used` and test-strength rows answered as fixed tests made three
  repair runs fail after a correct repair; the orchestrator or a Sonnet
  sub-agent completed them by hand, each named in its commit.
- **The kit probe misses new files** (bead coding-harness-fdz, P1). It copies
  only git-tracked files, and `make verify` runs before the runner stages
  anything, so an attempt that adds an imported script fails `leerprobe` with
  a misleading message.
- **A failed run blocks the next one** (bead coding-harness-b5w): the runner's
  own derived writes count as pre-existing changes.
- A Pi review call (`mimo-v2.6-flash`) hit the 30-minute limit once; its rerun
  passed. One Codex call failed with exit 1 (cause not read); its rerun passed.
- Not started: the exploration of bead coding-harness-3fc and the reviewer
  comparison of bead coding-harness-km1.

## 5. Which Now theme moved

"Stage 2 that can be trusted" (ROADMAP.md, Now 3): the format step is
delivered (#132), the drafting verb waits on one decision (#133), and the
GLM exit-1 failures have a measured cause.

## Beads opened tonight

coding-harness-km1 (compare OpenCode Go models as reviewers), coding-harness-b5w
(a failed run's derived writes block the next run), coding-harness-fdz (make
verify runs while new files are untracked). Changed: coding-harness-3fc
(diagnosis note). Opened the evening before: coding-harness-y17,
coding-harness-3fc.

## Parallel sessions

Session coding-harness-70 sits in the main checkout (state: waiting). This
session worked only in worktrees under `.claude/worktrees/`: stage2-format,
codex-drafts, adr-owning-change, handover-2026-10-13. Remove each after its
merge.

## Resume

Read this file, answer F-13 on #133, then continue change adr-owning-change
from its loop record
(`~/.local/state/coding-harness/stage2/adr-owning-change/loop.md`).
