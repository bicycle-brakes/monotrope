---
title: "Night-run plan — 2026-11-02 21:00 UTC to 2026-11-03 11:00 UTC"
category: research
created: 2026-11-02
updated: 2026-11-02
last_reviewed: 2026-11-02
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-4emv
tags: [night-run, plan, lanes, stage-2]
---

# Night-run plan 2026-11-02/03

The maintainer asked on 2026-11-02 at about 20:40 UTC for a night run of all
five lanes ("Bitte plane einen nachtlauf für alle 5 lanes"). The plan follows
the [night plan of 2026-11-01](2026-11-01-night-run-plan.md) and keeps its
rules except where this page says otherwise. One orchestrating Claude Code
session works the lanes and is the only tracker writer.

## State at the start (2026-11-02, 20:42 UTC, `main` at da48284f)

- Merged today: the five-lane night handover (#310), two research notes
  (#311, #313), the afternoon handover (#314), and the `--job docs` report
  header (#315, bead coding-harness-ooj5). Open: the README (#312, in the merge
  queue) and the documentation currency pass (#316).
- Lane B (bead coding-harness-wkxm) is in phase 6: the loop ended after round 6
  on the maintainer's word (rounds 5 and 6 were cut at 2000 lines, bead
  coding-harness-ut8q); re-checks found F-1 to F-5, F-1 to F-4 are repaired,
  the F-5 repair is running.
- The machine: 45 GB free, load low, the SSH signing key reloads at login
  (a launch agent since 2026-11-02).

## Lanes

Each lane runs its first item, then its backlog in order. An item marked
**needs** waits for that answer; without it the lane goes straight to its
backlog.

| Lane | First tonight | Backlog 1 | Backlog 2 |
|---|---|---|---|
| A | Self-closing beads (bead coding-harness-l1if): repair F6-4 and F6-5 with the two structural remedies, phase-6 re-check, pull request — **needs** question 1; the maintainer merges | Sonnet continues Flash's edits (bead coding-harness-6ie): implement — **needs** question 2 (its plan card) | Repair scope guard (bead coding-harness-t83): stays at its interview |
| B | Red-first proofs in a private clone (bead coding-harness-wkxm): F-5 repair, phase-6 re-check, full `make verify`, pull request with auto-merge | Runner stops at the appetite (bead coding-harness-uxa9): explore with GLM Flash, draft up to the plan card | Stop hook (bead coding-harness-788): explore up to the interview |
| C | One Go access point (bead coding-harness-4tr4): only after wkxm merges — merge `main`, round-8 repair from `refs/stage2/attempts/go-access-point/enospc-20261102`, loop, phase 6; stops before the ADR 0024 decision pull request | A clean free round ends the loop (bead coding-harness-1gzo): draft up to the plan card | ADR 0016 names the draft's document check (bead coding-harness-v9xx): the amended text as a proposal |
| D | Time records as data (bead coding-harness-v6vk): implement — **needs** question 2 (its plan card) | Repair line skeleton (bead coding-harness-k93f): implement — **needs** question 2 | Targeted check per repair (bead coding-harness-gxwg): implement — **needs** question 2 |
| E | Guard test (bead coding-harness-0ho): plan step 5 — **needs** question 3 | Review diff order (bead coding-harness-ut8q, worktree `review-diff-order`): decide R6-2 and R6-3 — **needs** question 4 | The Pi context probe for ut8q: one tool-free call per admitted Go model with a prompt just over its catalog window and `compaction.enabled: false` — **needs** question 4 |

## Needed from the maintainer before the start

One at a time, in this order; each unlocks the lane named.

1. **Lane A:** accept the two structural remedies for the self-closing beads
   (F6-4: read Git's output as raw bytes and accept only a full bead-id match;
   F6-5: fail closed, a peer is unrelated only outside every Git repository).
   Recommendation: accept both.
2. **Lanes A and D:** the four plan cards shown since 2026-10-31 and 2026-11-02
   (6ie, v6vk, k93f, gxwg) — each shown unchanged, one answer each. Without
   them, A and D run only their explore and draft items.
3. **Lane E:** the `guard-test-environment` entry in `decisions/gates.yaml`
   (agents may not write it).
4. **Lane E:** for ut8q, whether the night may (a) decide R6-2 and R6-3 of
   `review-diff-order` with a structural remedy — R6-1 to R6-3 are one
   mechanism, the temporary index seeded from the merge base, the same one lane
   B closed with "entries only, no flags" — and (b) run the Pi context probe.

## Rules for this run

1. **Night until 07:00 UTC, day from 07:00 to 11:00 UTC.** A pull request
   without a decision gets auto-merge when it leaves draft, as on 2026-11-01;
   decision pull requests and l1if wait for the maintainer.
2. **Implementation starts only on an approved plan card.** Backlog drafts stop
   at the plan card; explores stop at the interview.
3. **Hot file:** at most three changes to `scripts/stage2.py` are open at once:
   B, then C after B merges, plus one implementation (A's 6ie or D's first
   approved card). Drafts and explores write only under `plans/changes/`.
4. **Agents do not write `docs/adr/`, `AGENTS.md`, `model-endpoints.yaml`,
   `decisions/gates.yaml` or `.github/workflows/`.** Text for them goes to the
   maintainer as a proposal.
5. **Checks:** one `make verify` at a time on the machine. A full run before
   phase 6 and before a pull request leaves draft. Phase 6 runs only after the
   branch has merged `main` (on 2026-11-02 lane D's review ran before that
   merge; not again).
6. **A stopped job** is saved on a side ref under `refs/stage2/attempts/`,
   never as a WIP commit (bead coding-harness-c99h).
7. **Remote calls run beside the local check**, at most three foreign-model
   calls at once.
8. **Questions** collect in the handover for the 15:00 block on 2026-11-03;
   one goes to the chat only when a lane is blocked without it. Night answers
   are cut, park or drop, never continue.
9. **Status** in the chat at 07:00 UTC; the handover goes as a pull request
   from its own worktree by 10:45 UTC.

## Not tonight, and why

- The leak check's `tests/` exemption in a prompt (bead coding-harness-juu) and
  the fast pre-check before `make verify` (bead coding-harness-csm) are
  `feature` changes: their explore is the research swarm, whose availability
  report must be shown to the maintainer before it runs.
- An unreadable member replaced for one round (bead coding-harness-mfth)
  amends ADR 0021 and owes five interview answers.
- Pi sending no local paths (bead coding-harness-xul8, worktree
  `pi-neutral-paths`) touches the same Pi paths as 4tr4; it follows it.
