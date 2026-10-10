---
title: "Session handover — the Pi move decided (ADR 0012), and what can be done before the Mac test, as of 2026-10-10"
category: handover
created: 2026-10-10
updated: 2026-10-10
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-10"
tags: [handover, stage-2, pi, session, tracker]
target_ref: 7157c96
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

As of 2026-10-10, `main` is at `7157c96`. The move of `stage2.py session` from
the OpenCode CLI to the pinned Pi is built and decided:

| Pull request | Merge commit | What |
|---|---|---|
| #110 | `cc6452d` | interview answers and artefacts re-pointed to Pi |
| #111 | `f346cda` | the policy extension and its tests |
| #112 | `d6c9582` | the runner port (with discovery flags and cleanup after review) |
| #113 | `c59048e` | `docs/WORKFLOW.md` and the review handover |
| #114 | `7157c96` | decision PR: ADR 0012, Q-9, the `opencode-go` note |

ADR 0012 (`docs/adr/0012-interactive-stage-2-sessions-run-through-the-checked-runner.md`)
is the record. It amends ADR 0007 decisions 1 and 4 and ADR 0011 decisions 1
and 5, and names the accepted limits (unlisted shell commands run unasked,
`~/.pi/agent` and context files load unscanned, quoting defeats the patterns).

Before the merge of #114: an Opus review found the record misnamed what it
amended and called two later answers unrecorded. The second claim was wrong:
the maintainer chose both in a multiple-choice question on
2026-10-09T23:39Z (both the recommended option), and they are now Q-9 in
`plans/changes/stage2-session/decisions.md`, with the broader `git checkout` /
`git restore` forms the agent derived marked [DETAIL].

## Checked on 2026-10-10

- **CI runs the policy tests.** The gates job of #114 reports `1594 passed, 25
  skipped`; the roughly 200 policy cases skip only together (module-level
  `skipif` on a missing `node`), so they ran. Nothing to change.
- **Nothing has run in a live Pi.**

## Next step

1. **The Mac smoke test (package 7, maintainer).** Install Pi 1.1.0, sign in to
   OpenCode Go in `~/.pi/agent`, run `python3 scripts/stage2.py session <change>
   --model opencode-go/<id>`, and check: the window opens Pi; `rm -r x` asks; a
   read outside the worktree is blocked.
2. **Replay the tracker writes** where `tools/bd dolt push` works (it still
   fails here: on 2026-10-10 it timed out after 60 seconds, with a proxy
   rejection). The commands are in
   `docs/journal/handover/2026-10-09-remote-session-merges-tracker-and-pi-plan.md`;
   add one comment per package 3 to 6 on the Pi bead (short id 6h4) and close it
   after the Mac test.
3. **Archive finished changes — not started, needs a call.** `plans/changes/`
   holds 10 finished changes the registry reports as drift (closed bead, not
   archived), plus `stage2-mimo` and `interview-minimums`. Moving them breaks
   cited paths: ADR 0011 (human-decided, not editable here) links
   `plans/changes/stage2-mimo/`, and `tests/test_stage2.py`,
   `scripts/check_interview_minimums.py` and `scripts/kit/probe.py` name the
   folders. Proposal: one pull request for all finished changes, updating the
   tests and scripts, and leaving ADR 0011's link dead (the `docs-links` gate
   only reports) unless the maintainer prefers otherwise.

## Needed from the maintainer

- The Mac test.
- Whether to archive all finished changes in one pull request, accepting the
  dead link in ADR 0011.
- Still open from earlier: paste `tools/cloud-env/setup.sh` into the cloud
  environment's setup script field; decide D-13 criterion 4.

## Parallel sessions

None known. A commit series on 2026-10-09 23:47–23:57 UTC (the review fixes on
#111 to #113) came from this same session after a `/clear`; it is not a second
writer.

## Resumption

Read this file and ADR 0012, `git fetch`, then ask the maintainer for the Mac
test result or the archive decision.
