---
title: "Implementation plan: reach the Omnigent-first target"
category: architecture
status: proposed
created: 2026-09-17
last_reviewed: 2026-09-17
owner: maintainer
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: codex
  version: "2026-09-17"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [plan, implementation, omnigent, workflow, gates]
---

# Implementation plan: reach the Omnigent-first target

This is a dependency and acceptance plan for the
[target state](2026-09-17-omnigent-first-target.md), grounded in the
[gap analysis](2026-09-17-gap-analysis.md) at `eddfc0b` on 2026-09-17.
**This session writes documentation only.** Beads remains the durable task
tracker; the IDs below point to existing work and are not a second backlog.
The 2026-09-17 maintainer direction places **parallel Omnigent coordination
in the first proof of concept**, changing the sequence recorded in the
[older migration research](../research/Migrationsplan_Omnigent_Referenzarchitektur.md)
and [2026-09-16 proposal](target-architecture.md). One ADR should make that
change durable before implementation of the runtime begins.

## Dependency path

```text
One gate manifest + verify ─┬─> bounded change contract ─┬─> Omnigent parallel POC
Real rule enforcers ────────┤                            │   (two workers, coordinator writes Beads)
Agent instruction import ──┤                            │
Worktree and Beads test ────┘─────────────────────────────┘
                                      │
                                      v
                         repeatable Bounded operation
                                      │
                        endpoint and disclosure barrier
                                      │
                                      v
                    Feature path + cross-vendor review
                                      │
                                      v
                    unattended and multi-writer expansion
```

The POC starts with two writing workers in separate worktrees. Its Beads
updates are serialized by the coordinator. The worktree test can run in
parallel with the first three prerequisites because simultaneous Beads writes
are **not** an entry condition for parallel coding. A failing test preserves
coordinator-only writes; it does not cancel the entire parallel POC.

## First: make the workflow executable

| Deliverable | Work and reason | Acceptance evidence | Existing Beads work |
|---|---|---|---|
| One gate list and `verify` | Build the platform-neutral gate file, runner, CI derivation and export identity gate. This is the same command Omnigent will call before integration. | CI and local runner report the same gate IDs and verdicts; every blocking gate has a known-bad case; the repository's migration test baseline improves without weakening assertions. | `coding-harness-bo0` |
| Truthful rule set | Resolve each red rule test: restore a harness enforcer, move an instance rule to its instance, or lower it with a dated valve. | No level-3-or-higher harness rule names a missing enforcer; all rule tests pass for a stated reason. | `coding-harness-2ee` |
| Single agent instruction entry | Import `AGENTS.md` from `CLAUDE.md` and remove stale placeholder instructions. | A test loads the same house rules in both adapters and confirms the instruction budget. | `coding-harness-21f` |
| Contract and minimum templates | Add spec class, acceptance criteria, exclusions and a change-specific Definition of Done; add plan marking and findings templates. The POC needs a concrete contract to split safely. | Validator rejects a missing class, unbounded or overlapping assignment and an incomplete Definition of Done; a Bounded example passes. | `coding-harness-9qo`, `coding-harness-jc3` |
| Worktree and tracker protocol | Reproduce all five checks in a throwaway repository, including the full prefix and simultaneous claims. Decide whether to retain coordinator-only writes or test server mode after a backup. | Commands and results are committed; the house rule states exactly who writes. No shared database migration happens merely to satisfy a diagram. | `coding-harness-m34` |

These deliverables unblock a meaningful pilot; they do not require every
legacy test to pass immediately if a red test is proven to be an instance
assumption and is reclassified with an enforcer or valve. The final
repository gate must be green before routine use.

## Next: run the first parallel Omnigent proof of concept

**Scope:** a throwaway repository and two small, independent code changes.
Use the chosen pinned Omnigent release and its documentation, the OSS
deployment and a dedicated host. No customer-shaped content enters this
pilot. The orchestrator receives the approved spec and plan, assigns disjoint
file scopes, starts two worker sessions in separate worktrees and observes
both. Workers cannot merge, push to the protected branch or write Beads. The
coordinator alone records claims, results and blockers; branch integration is
sequential.

| Control | Experiment and pass condition |
|---|---|
| Runtime pin and reproducibility | Record exact version, configuration hash, host, sandbox backend and adapter commands; a fresh session can repeat the run. |
| Policy and sandbox | For each promised boundary, run a harmless known-bad action and record DENY/ASK plus the audit event. A non-firing boundary stops the pilot. |
| Worktree compatibility | Run `git worktree add` through the effective policy; check `block_working_dir_changes` and global random-worktree settings on the pinned release. A denied or untraceable worktree stops the pilot until configuration is corrected. |
| Endpoint and data egress | Resolve every selected model in `model-endpoints.yaml`; prove telemetry opt-out as configured; record observed egress. Unknown endpoint or unexplained egress stops the pilot. |
| Parallel progress | Both workers are active at once in different worktrees and contexts; neither writes outside its assigned scope; the coordinator integrates one branch at a time. |
| Verification and review | `verify` runs after each integration; a fresh-context reviewer sees only the diff and spec slice; findings remain in a file. |
| Cost and stop controls | Each worker has a measured spend limit, wall-clock limit, idle or no-progress limit and cancellation path. Deliberately trip each control once in a harmless run. The spend probe must show a real stop, not only a cheaper-model fallback. |
| Recovery | Kill one worker and then the host session; restart from the repository and tracker and recover the assigned step, commit, test verdict and blocker without the old chat. |
| Fallback | Repeat the same two-worker task with ordinary harness sessions and worktrees; the git-native gate verdict is identical. |

**Exit:** all controls pass, one parallel task loop reaches a reviewable PR,
and a report records wall time, model cost, human minutes, failed attempts,
gate verdicts and a comparable serial baseline. A faster wall time alone is
insufficient if cost, review load or failures rise materially. Record the
chosen thresholds *before* the comparison. **Abort:** a broken sandbox,
missing policy verdict, unknown endpoint, lost tracker write, unrecoverable
session, or a gate result that depends on Omnigent to exist. This is the
revised scope of the existing M0 work (`coding-harness-eev`); its old text and
dependencies need updating when the ADR is accepted.

## Then: turn the pilot into routine Bounded work

Use one real repository, initially this harness, for Bounded changes. Keep
two-worker dispatch available when the plan has genuinely independent steps;
serial execution remains valid for a one-step change. Rewrite `WORKFLOW.md`
in English around phase requirements, the four classes, design phase 2b and
this runtime sequence. Add `model-routing.yaml` with a schema and endpoint
check (`coding-harness-qvl`). Add the machine-rendered verification report,
session handover, single-writer export renderer and an onboarding example.
Add a one-page `ROADMAP.md` kit template for Now/Next/Later direction; keep
tasks and dependencies in Beads. Link out-of-scope discovered work using
`discovered-from`. Preserve the current change, open decisions, invariants and
gate verdict across compaction with a tested handoff. Standardize living-spec
delta sections and search-first dependency rationale in the relevant templates.
Exercise full Beads backup and restore in a disposable checkout; test the JSONL
issue-level recovery separately.
An Omnigent policy may refuse a push before `verify`, while CI independently
enforces the same gate result.

**Exit:** ten Bounded changes pass the same contract and gate path; their
measurements include human time, cost, recovery and policy exceptions. The
research target of at most ten human minutes per Bounded change is a
calibration threshold, not a claim about current performance. No unexplained
policy non-fire is accepted. The kit probe runs in a fresh repository. Failed
measurements revise the workflow or policies before expanding scope.

## After disclosure: Feature and cross-vendor paths

Keep parallel dispatch but permit larger, dependent plans only after the
Bounded path is repeatable. Add design artefacts and ADR/model checks for
architectural changes. Add requirement IDs and acceptance-test links before
attempting a traceability matrix. Enable a foreign reviewer only after the
instance's disclosure decision, endpoint operator and residency declaration,
and a green leak check for each change. Compare its findings with fresh-context
same-lineage review rather than assuming cross-vendor review is better.

**Exit:** three complete Feature changes have reconstructable specs, plans,
verification reports, reviewer findings and integration records. At least
one reviewer finding must be independently validated as useful; otherwise
change the review configuration or input. No disclosure or leak-check failure
is allowed. This is the measured entry condition for production cross-vendor
use, not for the earlier parallel POC.

## Expand only after the measured bottleneck appears

If several workers need direct, simultaneous Beads writes, run the five-check
test with the pinned version, back up the tracker, test a Dolt server migration
in a disposable copy and prove restore. A server belongs on the host that
serves those worker sessions; remote Dolt push/pull remains the cross-machine
transport. Only then replace coordinator-only writes. Add unattended runs
after all stop conditions have known-bad tests and an overnight rehearsal
proves a clean morning review. Mutation score and attestations remain later
work unless a concrete risk requires them earlier.

## Tracker and decision reconciliation

The existing Beads graph records the older sequence: `coding-harness-eev`
depends on `coding-harness-m34`, and M0 currently describes one task loop,
not two simultaneous workers. Once the target ADR is reviewed, update that
Bead to include the parallel POC and relax only the **multi-writer**
dependency, keeping the five-check test as a condition for worker-side Beads
writes. Existing Beads `bo0`, `2ee`, `21f`, `9qo`, `jc3`, `qvl` and `m34`
already cover most prerequisites. New durable items should be created for
the runtime adapter and policy probes, the metrics and stop-control suite,
and the revised doctrine after checking that no existing item covers them.

No phase ends by declaration alone: it ends when its recorded acceptance
evidence passes and the previous topology can still resume the work.
