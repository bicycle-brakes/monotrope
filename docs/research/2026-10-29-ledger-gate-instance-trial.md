---
title: "Criterion-ledger gate on an instance — trial run"
category: research
created: 2026-10-29
updated: 2026-10-29
last_reviewed: 2026-10-29
owner: framework-architect
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-s9m
tags: [criterion-ledger, kit, instance, adoption, spike]
---

# Criterion-ledger gate on an instance — trial run

**Result: in an instance whose live plans predate the ledger, the gate turns
`make verify` red at once.** The cause is not the instance's layout, which
matches this repository's. The cause is that the gate exempts only archived
plans dated before this repository's own cut-off (2026-10-11). An instance
has no adoption day of its own for this gate. A root without
`plans/changes/` exits 3 ("not measured"), and because the gate's
enforcement is `block`, that blocks too. This spike was asked for in bead
coding-harness-s9m (a disclosed limit of the change criterion-test-ledger,
row L3-4). The exploration of 2026-10-12 is on branch
`feat/ledger-instance-layout` and is not repeated here.

## What was run

On 2026-10-29 at about 02:00 UTC, `scripts/check_criterion_ledger.py` from
this repository's `main` at `db701a06` was run read-only against two roots.

| Root | Exit | Output |
| --- | --- | --- |
| A local `lakeswitch-ai` checkout at `09c9d62` (2026-09-30), 6 change folders, 3 uncommitted files left untouched | 1 | `5 findings in 5 plans`: each live `plan.md` "has no `## Criterion ledger` section" |
| An empty directory | 3 | `not measured — <root> has no plans/changes/ directory` |

The local checkout is behind its origin. The 2026-10-12 exploration read
origin at `ce88eee` through the GitHub API: 16 change folders, none with a
ledger. So the finding holds there too. Its counts were not re-measured
tonight, because fetching another repository's checkout was out of scope.

The five red plans are all live and dated 2026-09-26 to 2026-09-28 in their
`created:` field. That is before the ledger rule existed anywhere.

## What it means for the kit

1. **The cut-off is this repository's, not the instance's.**
   `CUTOFF = date(2026, 10, 11)` in the gate is the day of this repository's
   maintainer answers. It exempts only archived plans. A pinned instance's
   live plans from before its own adoption are measured and fail.
2. **Exit 3 blocks.** An instance that has not created `plans/changes/` yet
   (a fresh adoption) is blocked by a gate that measured nothing. Other gates
   in this repository separate "examined nothing" from "cannot measure"; this
   one already prints "examined nothing" when the directory exists but holds
   no plan.
3. **The kit carries the gate as mechanism** (ADR 0013: carried with the kit
   at once). So both effects reach an instance on its first pinned release.

## Options for the decision this spike feeds

The decision belongs with bead coding-harness-wpv (an adoption date for
instances that receive the gate later). Three options were seen:

- **An adoption day per repository.** The gate reads the repository's own
  adoption record and exempts plans created before it, live or archived.
  This repository already keeps adoption days for other gates
  (`decisions/adoption.yaml`, ADR 0014), so the mechanism exists.
- **A missing `plans/changes/` is "examined nothing", exit 0 with a notice.**
  That covers a fresh instance. It does not cover the five live plans above.
- **Migrate the instance's live plans** before pinning: add a ledger to each.
  That is work in the instance, and the gate stays strict.

**How close option one already is (read 2026-10-29 at `db701a06`):**
`scripts/adoption.py` is the one reader of a repository's adoption days
(`adopted_on(root, gate)`). It raises `NotRecorded` instead of guessing, and
its docstring already names bead coding-harness-wpv. Two gates use it today,
`interview-minimums` (2026-10-08) and `question-context` (2026-10-15).
`criterion-ledger` is not among them: its day is the constant `CUTOFF`. The
change would add `criterion-ledger: 2026-10-11` to `decisions/adoption.yaml`,
read it through `adopted_on`, and widen the exemption from archived plans to
plans created before the day. Adding or moving a day there is a decision pull
request (the file's own header).

The first two together close both effects. Which one, and whether an instance
may keep a later day, is the maintainer's decision. It is not taken here.

## Not measured

- Whether the archived plans of the instance would pass: the local checkout
  has no archived plan.
- Whether the instance's CI runs the gate today: its gate list was not read.
