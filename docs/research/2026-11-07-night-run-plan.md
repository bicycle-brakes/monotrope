---
title: "Night-run plan — 2026-11-07 16:00 UTC to 2026-11-08 07:00 UTC"
category: research
created: 2026-11-07
updated: 2026-11-07
last_reviewed: 2026-11-07
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [night-run, plan, lanes, stage-2]
---

# Night-run plan 2026-11-07/08

The maintainer asked on 2026-11-07 at about 15:05 UTC for a night plan
("Bitte erstelle einen Nachtplan"). The plan keeps the rules of the
[night plan of 2026-11-03](2026-11-03-night-run-plan.md) except where this
page says otherwise. One orchestrating Claude Code session works the lanes and
is the only tracker writer. It keeps five to six lanes running, never more
(maintainer, 2026-11-06).

## State at the start (2026-11-07, 15:07 UTC, `main` at eb0aa134)

- Merged today: #339 (night runs stay plain), #342 (open questions into bead
  notes), #344 (redraft-after-scope research), #345 (AGENTS.md shortened to
  189 lines), #346 (Pi agents never compact), #347 (beam-free dropped).
- Open: #348 (night heartbeat, CI green, waits for the maintainer) and #343
  (targeted check per repair, CI red; its mechanism repair is lane backlog).
- The machine-wide `make verify` lock is the bottleneck: one run takes about
  22 minutes, and every repair needs one. Recorded lane times of 6–11 hours
  against 2–4 hour appetites are mostly this wait (bead coding-harness-po0a).
- Four lanes run on an extra hour the maintainer granted today (wb40, yql7,
  ljmi, cqun). That hour is their last; see rule 2.

## Lanes

| Lane | Change (bead) | Until 2026-11-08 07:00 UTC |
|---|---|---|
| 1 | One central free-model selection (coding-harness-wb40) | Repair of loop round 4, loop until clean, phase 6, pull request. **First priority:** the testing-strategy spike (coding-harness-1ga5) and the central model state (coding-harness-atxy) wait for it, because today's research-swarm preparation proposed a paid id and an excluded, training model as free seats. |
| 2 | Go wire APIs, two of three (coding-harness-36za) | Repair of loop row L2-3, loop until clean, phase 6, pull request. |
| 3 | Machine facts at night-run start (coding-harness-yql7) | Repair of phase-6 rows F6-1 and F6-2, phase-6 re-check, pull request. |
| 4 | Status fields put back after repairs (coding-harness-ljmi) | Mechanism repair (YAML-parsed frontmatter, created documents protected), loop until clean, phase 6, pull request. |
| 5 | Archive closed change folders (coding-harness-cqun) | Repair of loop rows L4-1, L4-3, L4-5, loop until clean, phase 6, pull request. |
| 6 | Outcome test (coding-harness-3nm5) | Full `make verify` of the hand-completed attempt 3, `prepare-loop` (its selection reported in the conversation), review loop, phase 6, pull request. |

## Backlog, in this order, for the first lane that frees

1. Targeted check per repair (coding-harness-gxwg, #343): the mechanism
   repair of F6-7 the maintainer chose, then phase-6 re-check.
2. Explore provenance (coding-harness-g19n): redraft without the
   normalisation (decision Q-4), revert the normaliser edits to other
   changes' files, resolve the `main` merge conflict, repair, review.
3. Research store home (coding-harness-nxdy): redraft criterion 5
   ("check, never change"), repair the taken L8 rows.
4. Implement route file (coding-harness-9ycy): redraft without `docs/adr/`
   edits (the ADR edit is bead coding-harness-07d8), implement.
5. CI-caller rule (coding-harness-8sxb): new lane — change folder, Flash
   explore, reasoned interview skip, draft, implement.
6. Conflict-marker gate (coding-harness-i76l): hand-complete the CI step and
   the empty-probe reason, `make verify`, review loop.

## Backlog added (maintainer, 2026-11-07 about 15:20 UTC: "Kannst du mehr beads in den backlog legen")

All are `bounded` and unblocked. Each explores through GLM 5.3 Flash and
stops at the interview: an explore writes only under `plans/changes/`, and the
interview questions park for the morning. Most touch `scripts/stage2.py`, so
none goes past the interview tonight beside lanes 1 and 4.

7. Codex capacity retry (coding-harness-m98e) as the package the maintainer
   set on 2026-10-27, with the `cut_rounds` crash (coding-harness-jmtl) and
   coding-harness-y125 in one pull request.
8. A runner verb to triage loop rows (coding-harness-o2s1): replaces the
   orchestrator's hand edits of the loop record, which caused several failed
   repairs this week.
9. An implement attempt that changes only runner bookkeeping is accepted as
   verified (coding-harness-te7q): read the saved attempt record first, as
   its notes say.
10. Repair brake: the orchestrator sets the Origin cell (coding-harness-ywbh).
11. Warn when a catalog base URL or API differs from the declared Go address
    (coding-harness-x2g9).
12. `stage2.py session` launch command truncated by the terminal
    (coding-harness-rm8).
13. Plan card readable at a glance (coding-harness-6xx), a prompt-text change.
14. The Flash route's `unrecognized_model` failure (coding-harness-ygsw):
    first check whether the night's Flash explores hit it; explore only if
    they do.

Not started tonight: the speed beads coding-harness-w2ay, -wnka, -0swp and
the other test-strategy beads now linked to coding-harness-1ga5 wait for the
spike's report (maintainer-approved grooming, 2026-11-07).

## Rules for this run

1. **Questions park.** A lane that meets a question parks; the question goes
   at once, with context and a recommendation, into the bead's notes, and the
   handover gathers them under "Needed from the maintainer".
2. **The granted hour is the last.** Lanes 1, 3, 4 and 5 used their appetite
   and got one extra hour today. A further round with a new MAJOR, or a second
   finding of one mechanism at a phase-6 re-check, parks the lane for the
   morning instead of another repair.
3. **Repairs without asking** stay as before: a reproduced MAJOR code fault
   inside the spec; MINOR rows on tests, security or false statements. Style
   rows are named limits in the pull request.
4. **Codex at capacity:** wait four minutes, retry once, then Sonnet 5.5 for
   that one step (`docs/WORKFLOW.md`, "Night runs").
5. **No research-swarm explore tonight.** Its seat choice needs the
   maintainer's answer to the preparation report, which a night run cannot
   get; lanes for coding-harness-1ga5 and coding-harness-atxy start in the
   morning after lane 1 merges.
6. **No merges at night.** Pull requests wait for the maintainer.
7. **Supervision:** the lane watchdog and one log line per wake in the
   session's lane-watch log; `caffeinate` keeps the machine awake for the run.
8. **Handover** as a pull request from its own worktree by 2026-11-08
   07:00 UTC.

## Questions waiting for the morning

- Seat choice for the research swarm of coding-harness-1ga5 and
  coding-harness-atxy, once lane 1 is merged (prepare-explore runs then).
- Merge of #348 (night heartbeat), CI green.
