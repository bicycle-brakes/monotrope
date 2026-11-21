---
title: "Night-run plan — 2026-11-03 16:00 UTC to 2026-11-04 15:00 UTC"
category: research
created: 2026-11-03
updated: 2026-11-03
last_reviewed: 2026-11-03
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [night-run, plan, lanes, stage-2]
---

# Night-run plan 2026-11-03/04

The maintainer asked on 2026-11-03 at about 15:50 UTC what the five lanes do
until 15:00 UTC the next day ("was machen die fünf lanes bis morgen um 15
uhr"). The plan follows the [night plan of 2026-11-02](2026-11-02-night-run-plan.md)
and keeps its rules except where this page says otherwise. One orchestrating
Claude Code session works the lanes and is the only tracker writer.

## State at the start (2026-11-03, 15:50 UTC, `main` at b424be3a)

- Merged today: lane B (#320, bead coding-harness-wkxm). Open: the ADR 0016
  decision pull request (#323), the five-lane handover (#322), the Pi probe
  note (#321), the morning handover (#319).
- Codex was at its usage limit from about 12:10 UTC; the maintainer reset it
  at about 15:45 UTC. Meanwhile Sonnet 5.5 repaired lanes A, C and D through
  `--stage2-off` (maintainer, 2026-11-03).
- Running: phase-6 re-checks of lanes A and D and the first phase-6 review of
  the registry-block-last fix (bead coding-harness-2g7y).

## Lanes

| Lane | Until 2026-11-04 15:00 UTC |
|---|---|
| A | Self-closing beads (bead coding-harness-l1if): re-check of F6-6; clean → pull request, the maintainer merges it. Then the approved plan card of bead coding-harness-6ie. |
| B | Merged. The registry-block-last fix (bead coding-harness-2g7y): phase 6, pull request. Then the status put-back in the runner (bead coding-harness-ljmi) after lane C, because of `scripts/stage2.py`. |
| C | One Go access point (bead coding-harness-4tr4): repair of loop rows L9-1 and L9-3, further rounds until clean, phase 6; stops before the ADR 0024 decision pull request. |
| D | Time records as data (bead coding-harness-v6vk): re-check of F6-1 to F6-3; clean → pull request with auto-merge. Then the approved plan card of bead coding-harness-gxwg. |
| E | Guard test (bead coding-harness-0ho): merge `main`, phase 6, decision pull request. Beside it the second drafts of beads coding-harness-8v2c.1 and coding-harness-788 and the first of coding-harness-uxa9, each up to the plan card. |

## Backlog added (maintainer, 2026-11-03 about 16:10 UTC: "bitte erweitere den backlog für jede lane")

Each lane serves its first item, then these in order. All are `bounded`
changes: each explores through GLM 5.3 Flash and stops at the interview (an
explore writes only under `plans/changes/`), except where a line says more.

| Lane | Backlog 2 | Backlog 3 |
|---|---|---|
| A | Stopped attempts saved on a side ref by one command (bead coding-harness-c99h) | Archive the change folders of closed beads (bead coding-harness-cqun) |
| B | Repair prompt: a raising fault is caught by its test (bead coding-harness-xrzf) | Runner puts back status fields after a repair (bead coding-harness-ljmi): explore only; implementation after lane C, for `scripts/stage2.py` |
| C | Runner writes `compaction.enabled=false` into every Pi settings file (bead coding-harness-mwzv.2) | Contract tests read the pinned Pi's real data (bead coding-harness-z4oo) |
| D | Session start checks the worktree environment (bead coding-harness-cjf9) | Machine facts at night-run start (bead coding-harness-yql7) |
| E | The README states the runner's role and what the hooks do (maintainer, 2026-11-03; text pull request) | Plan card form readable at a glance (bead coding-harness-6xx) |

Lane A's first item parks at 2026-11-03 16:00 UTC: the re-check found F6-7
and F6-8, the fourth and fifth finding on reading Git's trailer output; they
go to the 15:00 block, so lane A starts its backlog.

## Rules for this run

1. **Questions park.** A lane that meets a question parks; questions collect
   with their context in the handover for the 15:00 block on 2026-11-04 and
   are asked one at a time through the interview tool.
2. **No questions at night.** A security event (a leak-check block, a full
   disk) sends a push notification that informs and asks nothing
   (maintainer, 2026-11-03).
3. **Repairs without asking:** a MAJOR finding that is a reproduced code
   fault inside the spec (maintainer, 2026-11-03); a remedy that widens the
   change or adds a guarantee parks (bead coding-harness-mwzv.1).
4. **Auto-merge** for pull requests without a decision once CI is green
   (lane D, the 2g7y fix); lane A (l1if) and lane E's decision pull request
   wait for the maintainer (maintainer, 2026-11-03).
5. **Limits:** at most three foreign-model calls and one `make verify` at a
   time; phase 6 only after the branch merged `main`; a stopped job is saved
   on a side ref under `refs/stage2/attempts/`.
6. **Agents do not write** `docs/adr/`, `AGENTS.md`, `model-endpoints.yaml`,
   `decisions/gates.yaml` or `.github/workflows/`; text for them goes to the
   maintainer as a proposal.
7. **Handover** as a pull request from its own worktree before 15:00 UTC on
   2026-11-04.
