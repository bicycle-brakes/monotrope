---
title: "Session handover — before a /clear on 2026-10-10: open pull request, next steps and every bead change to replay"
category: handover
created: 2026-10-10
updated: 2026-10-10
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-10"
tags: [handover, stage-2, pi, tracker, archive]
target_ref: f9ede9f
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

As of 2026-10-10, `main` is at `f9ede9f` (the merge of #115). Merged today:
#110 to #114 (the session verb on Pi, decided as ADR 0012) and #115 (the
handover `docs/journal/handover/2026-10-10-pi-move-decided-and-next-steps.md`,
which this file continues).

**Open:** #116, branch `chore/archive-finished-changes`, archives the 13
finished changes into `plans/changes/archive/<date>-<name>/` and fixes the paths
in scripts and tests. The maintainer asked for its merge on 2026-10-10 ("Merge
Baby Mergels"); the first attempt was refused because `main` had moved (the
required check `verify` must run on the merged state), so `main` was brought
into the branch and CI is running. Merge it with the head SHA once CI is green.
It leaves ADR 0011's link to `plans/changes/stage2-mimo/` dead, which the
maintainer accepted.

## Next step

1. Merge #116 when its CI is green (already requested by the maintainer).
2. The Mac smoke test of the session verb on Pi (package 7, maintainer): see the
   2026-10-10 handover named above.
3. Replay the tracker writes below where `tools/bd dolt push` works.
4. Then: a one-page plan for bug coding-harness-909 (deleting 29 of 30
   per-criterion tests left `make verify` green), for the maintainer's approval.

## Tracker: every change that exists only in this container

`tools/bd dolt push` failed here throughout (HTTP 403 on 2026-10-09; a 60-second
timeout with a proxy rejection on 2026-10-10), so origin's `refs/dolt/data` has
none of these. Origin still shows ymx, 6yg, kw0 and 0al open and has no Pi bead;
until the replay, CI's plan registry reports drift (not a block) for the
archived `stage2-mimo`, `interview-minimums` and `stage2-runs-count`.

| Bead | Change in this container | Why |
|---|---|---|
| coding-harness-ymx | closed (`--force`, the assignee's session had ended) | #105 merged 2026-10-09 |
| coding-harness-6yg | closed (`--force`) | #104 merged 2026-10-09 |
| coding-harness-kw0 | closed | done with #106; cost tracking not needed (the maintainer works on subscriptions, 2026-10-09) |
| coding-harness-0al | one comment, then superseded by the Pi bead (closed) | the maintainer wants no OpenCode CLI |
| the Pi bead (short id 6h4) | created (P2 task, discovered-from 0al), claimed, seven comments (packages 1 to 6, Q-7/Q-8, the merges) | the session verb on Pi |

### Replay

Run from the coding-harness main checkout with no other writing session
(house rule 4). The Pi bead gets a new id when it is created again; the script
reads it from the output.

```bash
set -euo pipefail
tools/bd dolt pull

tools/bd close coding-harness-ymx --force --reason "Pull request #105 merged 2026-10-09 (7afa5b8): the review loop (4b) runs on OpenCode Go through Pi (ADR 0011). Archived as plans/changes/archive/2026-10-07-stage2-mimo by #116."
tools/bd close coding-harness-6yg --force --reason "Pull request #104 merged 2026-10-09: the phase-1a interview minimums and the gate interview-minimums. Archived as plans/changes/archive/2026-10-08-interview-minimums by #116."
tools/bd close coding-harness-kw0 --force --reason "Done with #106 (3a609ae): scripts/stage2_runs.py and the criteria in docs/WORKFLOW.md section 4. Tokens and cost per vendor stay unmeasured by the maintainer's decision of 2026-10-09 (subscriptions). Archived as plans/changes/archive/2026-10-08-stage2-runs-count by #116."

NEW="$(tools/bd create "Stage 2: run the interactive session verb on Pi, not on the OpenCode CLI" -t task -p 2 --deps discovered-from:coding-harness-0al \
  -d "Maintainer, 2026-10-09: no more OpenCode CLI. Move stage2.py session to the pinned Pi 1.1.0 with a runner-supplied policy extension. Plan: docs/research/2026-10-09-session-verb-on-pi-plan.md; change: plans/changes/stage2-session; decision: ADR 0012." \
  | sed -n 's/.*Created issue: \(coding-harness-[a-z0-9]*\).*/\1/p')"
test -n "$NEW"
tools/bd update "$NEW" --claim
tools/bd comment "$NEW" "2026-10-09/10: packages 1 to 6 done and merged: #110 cc6452d (interview Q-1 to Q-8, artefacts), #111 f346cda (policy extension, 200 cases), #112 d6c9582 (runner port), #113 c59048e (docs), #114 7157c96 (decision PR: ADR 0012, Q-9). Q-7: network programs do not ask; Q-8: git push does not ask, git reset --hard and git clean do; Q-9: --no-mcp/--no-skills/--no-prompt-templates/--no-themes with context files on, and git checkout -- . / git restore . ask. CI runs the policy tests (1594 passed, 25 skipped at #114). Open: package 7, the Mac smoke test; close after it."

tools/bd comment coding-harness-0al "2026-10-09: superseded by the move of the session verb to Pi; no opencode call remains (ADR 0012, merged 2026-10-10)."
tools/bd supersede coding-harness-0al --with "$NEW"

tools/bd dolt push
```

## Not changed in the tracker

Bead coding-harness-909 (the per-criterion test bug) and the P1 beads
(coding-harness-s6i, coding-harness-36z) are untouched. Bead coding-harness-yim
shows `in_progress` without an artefact (registry drift); nobody here worked on
it.

## Parallel sessions

None known.

## Resumption

Read this file, `git fetch`, check #116; if it is green and open, merge it with
its head SHA (the maintainer already asked). Then ask about the Mac test or the
plan for coding-harness-909.

## Addendum — #116 merged, 2026-10-10

#116 is merged (`0c71403`) after its CI went green on the branch with `main`
brought in. Step 1 of "Next step" is done; this pull request (#117) only adds
this file and waits for the maintainer's merge.
