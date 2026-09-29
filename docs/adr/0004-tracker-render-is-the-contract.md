---
title: "ADR 0004 — The tracker render is the portable contract (D-4 amended)"
category: adr
status: accepted
created: 2026-09-22
last_reviewed: 2026-09-23
updated: 2026-09-29
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr]
---

# ADR 0004 — The tracker render is the portable contract (D-4 amended)

* Status: accepted · amends D-4 of the 2026-09-16 interview
* Review: direction confirmed by the maintainer, 2026-09-22 (option A of
  three); accepted by the maintainer, 2026-09-23, after all three
  conditions of D-52 were shown (PR #34) and the record was corrected
  (PR #36), in a commit signed with the maintainer's Touch-ID key ·
  Decider: maintainer · prepared by a Claude Code session
* Date: 2026-09-22 · corrected 2026-09-23 (see "Correction" under Context)
  · accepted 2026-09-23

## Context

D-4 kept auto-export off and promised the committed export
(`.beads/issues.jsonl`) as the portable contract, guarded by an identity
gate. The parent bead `1jg` measured the price of that second truth: every
tracker change invalidates the copy, so each push needs a render commit on
main before gates go green again, and parallel branches collide on the
file. D-52 — recorded in lakeswitch-ai PR #37, not yet ratified (cluster
7) — already set the direction: the portable contract is the tracker
render; the committed copy is transitional.

PR #26 verified two of the three conditions D-52 attached to removal: the
pinned `bd` runs in the hosted runner behind a verified checksum, and the
token reads `refs/dolt/data` in the private repository (CI green on
`fbf542d`). The third condition — every reader on one access point — is
open, and it is the work of bead `1jg.3`. Stage 1 (`1jg.1`, machine-local
fields omitted from the render) is what makes renders byte-equal across
machines in the first place.

**Correction, 2026-09-23.** The paragraph above overstates what PR #26
showed. The pinned `bd` did run behind its checksum, but the token never
read `refs/dolt/data`: the hydration step left the checkout's Authorization
header set both locally and globally, git sent it twice, and `bd bootstrap`
fell back to importing the committed JSONL ("Bootstrap plan: import from
git-tracked JSONL"). The identity gate therefore compared the copy with
itself, and CI stayed green. The second condition was first shown on
2026-09-23 in PR #34, which removed the local header ("Bootstrap plan: clone
from remote" in both the verify and the drift job). The same pull request
showed the third condition in use and removed the copy. The paragraph is
kept as written, so that the record shows what was believed and when.

## Decision Drivers

* The maintainer chose full removal (option A) over a fallback copy and
  over the status quo, 2026-09-22.
* One writer per tracker must survive the change (house rule, AGENTS.md).
* A copy only a fallback would read rots silently; the status quo keeps
  the measured friction forever.

## Considered Options

* **(a) The committed copy is removed once the three conditions are
  shown; readers render fresh from Dolt.** Chosen.
* (b) The copy stays as a fallback for environments without `bd` —
  rejected: the same drift returns in a quieter form.
* (c) Status quo with the identity gate — rejected: render commits and
  branch collisions remain the price of every tracker change.

## Decision

Auto-export stays off. The render is the portable contract. The committed
copy remains **until** all three D-52 conditions are shown. (As of
2026-09-23 all three are shown and the copy is gone — PR #34; the second
condition only then, see the correction above.) When it falls:

* every reader takes the render of the one access point — hosted CI from
  the hydration of `refs/dolt/data`, locally from the writer's tracker;
* `export-identity` retires; reproducibility lives as a repeatable test
  (render twice, byte-equal), per D-54;
* `bd bootstrap` becomes the documented prerequisite of a fresh clone. It
  modifies `.beads/.gitignore` and `.beads/config.yaml` in the checkout,
  and both side effects are accounted for.

## The two conveniences and their successors

D-52's note names two conveniences of the committed copy that need a
conscious successor when it goes:

* **Tracker changes visible in the pull request diff.** Successor: the
  tracker summary of the touched beads travels in the pull request body,
  so the reviewer still sees what the tracker now says — in the place
  where review happens, not in a file diff. Decided by the maintainer on
  2026-09-23: the body rule is AGENTS.md house rule 4 now, and a CI job
  summary of the changed beads follows (bead `coding-harness-1jg.4`).
* **Readability for agents without `bd`.** Successor, as decided on
  2026-09-23: the access point `scripts/bead_render.py` refuses with both
  ways out — `tools/beads/install.sh && tools/bd bootstrap --yes`, or
  `BEAD_RENDER` pointing at a render — and a tracker-reading gate ends in
  exit 3, "not measured". The run artifact first proposed here is not
  built.

## Consequences

* The D-4 row of the
  [decision continuity table](../architecture/2026-09-17-omnigent-first-target.md#decision-continuity)
  is amended to "Amend, direction confirmed"; this ADR is the runtime
  record the row points to.
* The wording changes in lakeswitch (D-09/D-31) follow in that
  repository; they are the maintainer's act there.
* This ADR flips to accepted by the maintainer when `1jg.3` has shown
  the third condition — not before. As of 2026-09-23 (PR #34) that point
  was reached, and the maintainer accepted it the same day.
