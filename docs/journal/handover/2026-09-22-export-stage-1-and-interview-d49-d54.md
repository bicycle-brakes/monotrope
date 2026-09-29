---
title: "Session handover — export stage 1 merged, interview D-49 to D-54, 2026-09-22"
category: handover
created: 2026-09-22
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-22"
tags: [handover, beads, export, lakeswitch, interview, ratification]
target_ref: "7f480f6"
bead: coding-harness-bl2
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
updated: 2026-09-29
---

# Resume here

This continues the handover of 2026-09-21
(`docs/journal/handover/2026-09-21-stack-merged-and-foundation-decisions.md`),
which stays as it is. Same session, second half.

## Where we are

`main` is green and carries everything this session built in Coding Harness:
the gate stack, the first stage of the tracker-export work (the renderer now
produces the same bytes on every machine) and two archived change packages.
In the sibling repository lakeswitch-ai, the decision interview in draft pull
request #37 grew from 48 to 54 entries: four entries settle where the record
disagreed with the running practice here, two answer a review on attestation
and evidence, and one false evidence claim was corrected. None of the 54
entries is binding yet — each is an assistant's record, and the maintainer
ratifies them in seven clusters before anything is promoted. Three Coding
Harness pull requests stay open and unchanged: the ADRs (#12), the
Omnigent-first target (#8, draft, now conflicting with `main`) and the session
display (#10).

## Next step

Claim the bead "CI runs every gate even after a red block gate"
(`coding-harness-bl2`) and make the generated workflow run every gate step
after a failure. Unchanged from the previous handover: it is small, and two
latent gate bugs were hidden by exactly this behaviour.

## Needed from the maintainer

In lakeswitch-ai, in this order:

1. **Set up Git commit signing with an SSH key** (hardware-backed if
   possible). Commits there are unsigned and `gpg` is not installed. Without
   it no ratification can be made.
2. **Admit `plans/` and the class `ai-drafted` in `decisions/provenance.yaml`.**
   Only you can change that file; until then the provenance-coverage gate
   (M-5) keeps pull request #37 red.
3. **Ratify cluster 7 first** (foundation and tracker: D-45, D-46, D-47, D-48,
   D-52), because the next build work in this repository rests on it. Ask a
   session to prepare the file with the digests; you write `accept`, `reject`
   or `amend` per entry, commit and sign it yourself.

In this repository: accept or amend the three ADRs of pull request #12
yourself, then merge #12 into `docs/omnigent-first-target` before #8 reaches
`main`. Unchanged from the previous handover.

## Decisions and preferences

Recorded in lakeswitch-ai pull request #37, head `fb4fd35`
(`plans/changes/unified-research-and-work-management/decision-interview.md`).
They are not asked again; they still await ratification.

- **Two handover levels (D-49).** A structured comment on the Bead carries the
  resume context of one change; the dated file here carries the session. The
  file never states task status — it points to Beads.
- **Review required in both routes (D-50).** `review/findings.md` in the
  standard route, a fixed `Review` section in `change.md` in the lightweight
  one; the reviewer is never the producing actor; an open BLOCKER blocks
  closure.
- **Standard-route triggers (D-51).** A path on the protected control-surface
  list always takes the standard route, however small; everything else only
  when an obligation changes. No size threshold. The standard route is to be
  cheap rather than rare.
- **Tracker export (D-52).** The portable contract is the render, not the
  committed file. The file stays until three things are shown (see the bead
  for stage 3, `coding-harness-1jg.3`).
- **Ratification (D-53).** Seven clusters, each by a maintainer-written,
  signed file below `decisions/`. An assistant prepares, never writes or signs.
- **Evidence (D-54).** A verification claim lives as a repeatable test beside
  the code; change packages cite the test and restate no numbers. A throwaway
  measurement is a dated observation.
- **lakeswitch-ai pull request #36** is raised to Pydantic 2.13.5 with
  `pydantic-core` 2.46.5 while it is reworked onto `main`, so its three
  governed pin locations change once.

How the maintainer wants questions put: one at a time, as an interview with
two or three alternatives and a recommendation, preceded by enough plain
context to decide — no jargon, short sentences. Twice in this session a
question had to be asked again because it was too dense.

## Open work and blockers

Task status lives in Beads; this list only points.

- Tracker export without double bookkeeping (`coding-harness-1jg`): stage 1 is
  closed and merged; stage 2, the gate file declares where a gate can measure
  (`coding-harness-1jg.2`), is ready; stage 3 (`coding-harness-1jg.3`) waits
  for two measurements in the hosted runner.
- Filed this half: the scaffold command cannot run here because its guard
  script did not travel (`coding-harness-cke`, blocks the workflow-entry tests
  `coding-harness-kkh`); eleven beads carry a placeholder owner
  (`coding-harness-xcy`).
- Dated notes were added to the foundation chain (`coding-harness-ei0`,
  `coding-harness-s6i`) and to the promotion bead (`coding-harness-mr2`).
- The plans registry reports one drift: the ADR bead (`coding-harness-nkr`) is
  in progress without a change package. Its lease expired on 2026-09-19; do not
  run `bd reclaim` unless you want it set back to open.

## Working state and parallel-session boundary

- Branch `docs/handover-2026-09-22-session-end`, cut from `main` at `7f480f6`.
  It carries this file and the re-rendered `.beads/issues.jsonl`.
- Coding Harness pull requests merged this half: #17 (renderer, `b694911`),
  #18 (closing chores and archive, `1135e50`), #19 (two beads, `7f480f6`).
  Tracker data was pushed to the Dolt remote after each write.
- lakeswitch-ai pull request #37: this session pushed eight commits
  (`db8f03b` … `fb4fd35`), always from a throwaway worktree, never force. A
  Codex session pushed its own handover in between and preserved this
  session's commits. A lakeswitch-ai session was registered as waiting when
  this handover was written; it must pull before it writes to that branch.
- Worktree `/Users/mikypiky/coding-harness-wt-claude-code` belongs to pull
  request #10 and was not touched. No parallel session in this checkout at the
  end (session scan, 2026-09-22).
- Mistakes of this session, repaired: a false evidence claim ("780 tests")
  was carried into D-47 unverified and corrected once measured; one bead note
  was written twice and reduced to one copy.

## Validation

- 2026-09-21, `main` at `7f480f6`: CI green; `render_beads_export.py --check`
  reports identity.
- 2026-09-21, stage 1 at `c65a548` and its review fix: `verify_all.sh` VERIFY
  GREEN, 275 passed, 15 skipped; the wiring test was proved by mutation; an
  independent review in a fresh context found no BLOCKER and two MINOR
  findings, both fixed.
- 2026-09-21, observation, not proof: lakeswitch-ai declared-document branch
  `fc4d55f` passed 563 of 563 tests and every gate under Pydantic 2.10.6 and
  2.13.5 with identical schema digests — Python 3.12.4, disposable
  environment, not the required 3.11.
- 2026-09-21: a fresh-clone bootstrap of the tracker from `refs/dolt/data`
  took 4.4 s.
- lakeswitch-ai: `lakeswitch verify` after every commit showed only the two
  known provenance-coverage findings on the change package.
- Not run: anything under Python 3.11; the two hosted-runner prerequisites of
  stage 3. Not read: the full research document of pull request #37, the
  content of `plans/specs/`, the upstream beads documentation (unreachable).

## Addendum — 2026-09-22, state after the session closed

The sections above were written before their own pull request merged. What a
session starting tomorrow finds:

- **Checkout.** `main`, clean, level with the remote. The handover branch
  named under "Working state" was merged through pull request #20
  (`e96dee0`) and deleted; this addendum arrives through its own pull request
  and carries nothing else. No temporary worktree of this session remains in
  either repository.
- **Tracker.** Pushed to the Dolt remote after the last write;
  `render_beads_export.py --check` reported identity on `main` at `e96dee0`.
  No tracker write is pending.
- **lakeswitch-ai pull request #37.** Head `3cf4d22`. After this file was
  written it gained forward pointers on the amended entries (D-24, D-27, D-29,
  D-31, D-45), a note closing the open end of the foundation research, and a
  journal handover of its own:
  `journal/2026-09-22-decision-interview-d45-d54-and-ratification.md`. That
  journal supersedes the next step of the Codex journal beside it — the
  implementation plan comes after the maintainer's ratification, not before.
- **Where to start tomorrow.** Work in this repository: the bead under "Next
  step" above. Work in lakeswitch-ai: the journal named in the previous point;
  its first step is to prepare the ratification file for cluster 7 as a
  proposal.
- **Unchanged and still waiting on the maintainer:** commit signing and the
  provenance map in lakeswitch-ai, the first ratification, and the three ADRs
  of pull request #12 here.
