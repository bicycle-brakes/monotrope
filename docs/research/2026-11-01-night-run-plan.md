---
title: "Night-run plan — 2026-11-01 19:05 UTC to 2026-11-02 11:00 UTC"
category: research
created: 2026-11-01
updated: 2026-11-01
last_reviewed: 2026-11-01
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-4emv
tags: [night-run, plan, lanes, stage-2]
---

# Night-run plan 2026-11-01/02

The maintainer asked on 2026-11-01 at about 19:00 UTC to continue all five
lanes and to give every lane two backlog beads ("ich möchte zwei beads im
backlog für jede spur"). The plan follows the
[run plan of 2026-10-31](2026-10-31-run-plan.md) and keeps its rules except
where this page says otherwise. One orchestrating Claude Code session works
the lanes and is the only tracker writer.

## State at the start (2026-11-01, 19:05 UTC, `main` at 37b78b0a)

- Merged today: #301, #303, #304 and #305 (the verify worker cap, bead
  coding-harness-l7sc).
- Open: #306, the README's "What works today" as of ac11da5d, auto-merge on.
- Running: every lane has a runner job (table below). Three jobs stopped by
  the previous session's end at 18:23 UTC were saved as WIP commits and
  restarted.

## Lanes

Each lane first finishes its current change, then takes its two backlog beads
in order.

| Lane | Current change, and where it stops | Backlog 1 | Backlog 2 |
|---|---|---|---|
| A | Self-closing beads (bead coding-harness-l1if): repair of F6-2/F6-3, phase-6 re-check, pull request — **the maintainer merges** | Sonnet continues Flash's edits (bead coding-harness-6ie): draft up to the plan card | The repair prompt forbids handover files and edits outside the taken rows (bead coding-harness-t83): draft up to the plan card |
| B | Red-first proofs in a private clone (bead coding-harness-wkxm): repair of round 2, rounds until clean, phase 6, pull request with auto-merge | An unreadable member is replaced for one round (bead coding-harness-mfth): draft up to the plan card | The stop hook blocks a session end on a red tree (bead coding-harness-788): draft up to the plan card |
| C | One Go access point (bead coding-harness-4tr4): repair of round 7, round 8, phase 6; stops before the decision pull request for ADR 0024 | A clean free round ends the loop (bead coding-harness-1gzo): draft up to the plan card | ADR 0016 names the draft's document check (bead coding-harness-v9xx): the amended text as a proposal for a decision pull request |
| D | Explorer and reviewer helpers (bead coding-harness-9ll): phase 6 (round 2 clean), pull request with auto-merge | The `--job docs` report header (bead coding-harness-ooj5): implement — free since #305 merged | Fast pre-check before `make verify` (bead coding-harness-csm): draft up to the plan card |
| E | Guard test (bead coding-harness-0ho): implement up to plan step 5, which needs the maintainer's `guard-test-environment` entry in `decisions/gates.yaml` | The leak check's `tests/` exemption inside a prompt (bead coding-harness-juu): draft up to the plan card | The runner stops at the appetite (bead coding-harness-uxa9): draft up to the plan card |

## Rules for this run

1. **Night until 07:00 UTC, day from 07:00 to 11:00 UTC.** A pull request
   without a decision gets auto-merge when it leaves draft; decision pull
   requests and l1if wait for the maintainer.
2. **Backlog beads stop at the plan card**, except ooj5, which was planned for
   implementation in the run plan of 2026-10-31. Implementation of the others
   starts on the maintainer's word.
3. **Hot file:** `scripts/stage2.py` is changed tonight by lanes B and C only.
   The first of the two to reach its pull request merges first; the other
   merges `main` in afterwards. Backlog drafts write only under
   `plans/changes/`.
4. **Agents do not write `docs/adr/`, `AGENTS.md`, `model-endpoints.yaml` or
   `.github/workflows/`.** Text for them goes to the maintainer as a proposal
   (v9xx, the ADR 0024 decision for 4tr4).
5. **Checks:** one `make verify` at a time on the machine (the admission of
   bead coding-harness-p6mu). A hand repair gets a targeted check; a full
   `make verify` runs before phase 6 and before a pull request leaves draft.
6. **A stopped job** is saved unchanged as a WIP commit and restarted, never
   committed as finished runner output.
7. **Questions** collect in the handover for the 15:00 block on 2026-11-02;
   one goes to the chat only when a lane is blocked without it.
8. **Status** in the chat at 07:00 UTC; the handover goes as a pull request
   from its own worktree by 10:45 UTC.

## Not tonight, and why

- The lanes and check-in skills (beads coding-harness-0sfe and
  coding-harness-dmwz) and the lane watch with lane orchestration (beads
  coding-harness-5q2p and coding-harness-4emv) are `feature` changes; their
  research swarm waits for the Go access point (coding-harness-4tr4).
- Pi's real data in contract tests (bead coding-harness-z4oo) and Pi sending
  no local paths (bead coding-harness-xul8) touch the same Pi paths as 4tr4;
  they follow it.
- A free "red against" commit (bead coding-harness-qvf7) extends guard-test;
  it follows that merge.
