---
title: "Target state: an Omnigent-first, evidence-driven coding harness"
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
tags: [architecture, target, workflow, omnigent, parallelism]
---

# Target state: an Omnigent-first coding harness

**Direction confirmed by the maintainer on 2026-09-17:** Omnigent should
coordinate parallel agents from the beginning. This changes the sequencing in
the [2026-09-16 target proposal](target-architecture.md): parallel orchestration
starts in the first proof of concept, while production use still depends on
measured exit criteria. The mechanics in this document are a proposal pending
review and an ADR. The [gap analysis](2026-09-17-gap-analysis.md) states what is
present at `eddfc0b`; the [implementation plan](2026-09-17-implementation-plan.md)
states how to reach this target. Research remains evidence, not a second rule
set.

## Outcome and boundaries

A developer can start a change from one Beads item, let Omnigent coordinate
independent workers in isolated worktrees, inspect their progress and costs,
and reach a reviewable pull request. A later session can resume from repository
artefacts and the tracker without the previous chat. The same verification
command runs locally, in CI and when Omnigent requests it. A failed gate stops
integration. The human owns intent, exceptions and merge; agents own mechanics.

The harness owns reusable process and its kit. Each instance owns domain
requirements, secrets, endpoint permissions and additional gates. The customer
instance is a read-only boundary; its expressions never enter harness files.
Content artefacts, commit messages and pull request bodies are English.
Omnigent is the named reference runtime; the workflow contract and gate
manifest remain portable. A public-readiness scan must allow this tool name
while still excluding customer and employer identifiers and instance secrets.

## Source of truth and topology

| Concern | Authoritative state | Runtime responsibility |
|---|---|---|
| Change contract | `spec.md`, with acceptance criteria, exclusions, class and change-specific Definition of Done | Agents read the spec; a validator checks its structure |
| Direction and appetite | A one-page `ROADMAP.md` with Now, Next and Later themes; Beads holds the executable tasks | The coordinator links a change to its theme without turning the roadmap into a second task list |
| Design and execution | `design.md` when required; `plan.md` with bounded, assignable steps | Omnigent dispatches independent steps and records assignments |
| Work status and dependencies | Beads Dolt database, transported by `refs/dolt/data` | A single coordinator writes first; workers report results. Multiple writers are enabled only after the concurrency test |
| Code and review evidence | Git branches, pull requests, tests, findings and a machine-rendered verification report | One worktree per writing worker; fresh-context review of diff and contract |
| Gates | One platform-neutral gate manifest and its `verify` command | Local, CI and Omnigent call the same command; CI and branch protection remain authoritative for merge |
| Agent execution | Pinned Omnigent configuration and disposable sessions | Omnigent starts, observes, limits and cancels work; it never becomes the sole holder of a change's state |
| Long-term memory | Dated handovers, living specs, ADRs and Beads | A session ends by recording enough to resume and syncing the tracker |

Parallel work is a property of **execution**, not permission for uncontrolled
tracker writes. In the first topology, the coordinator creates and claims the
Beads work in the main checkout and assigns independent tasks. Workers write
only their own worktree and report a commit, test result and blocker to the
coordinator. The coordinator serializes tracker updates and integrates
branches one at a time. A worker receives a tracker snapshot from the
coordinator until worktree visibility has been verified; direct tracker reads
can then be enabled. This permits parallel coding
from the first Omnigent experiment without assuming embedded Dolt supports
simultaneous writers. The existing one-writer house rule remains in force until
the five-check worktree test passes. A later switch to Dolt server mode is a
measured response to a need for simultaneous tracker writes, not a prerequisite
for parallel code execution. [Beads describes embedded as single-writer and
server mode as multi-writer.](https://github.com/gastownhall/beads/blob/main/docs/architecture/dolt.md)

## A change through the system

1. **Intake and class.** A Bead names the goal and status. The change folder
   contains the contract. Work discovered outside the contract becomes a
   separate Bead linked with `discovered-from`. Spike, Bounded, Feature and Architectural classes
   determine the proportionate artefacts and gates; class may rise mid-change.
2. **Explore, spec, design, plan.** The seven-phase workflow remains the
   backbone. Architectural work requires `design.md`, an ADR and an architecture
   model update. A Feature can omit design with a recorded reason. A small
   Bounded change avoids unnecessary ceremony. The question protocol is
   `[DECISION]` for human intent, `[GAP]` for exploration, `[DETAIL]` for agent
   judgement recorded in the artefact.
3. **Dispatch.** Omnigent checks that steps are independent, the worktree and
   model endpoint are permitted, and each worker has a bounded file scope,
   time limit, tool-call or iteration limit, and spend cap. Dependent steps
   wait. The coordinator owns the integration order.
4. **Implement and verify.** A worker changes only its branch, runs relevant
   tests and reports evidence. The canonical `verify` command runs after
   integration. A generated report records the gate verdict and a reference to
   full output; agent context receives the verdict, not raw logs.
5. **Review and merge.** A reviewer in fresh context reads the diff and spec,
   records BLOCKER, MAJOR or MINOR findings and may disagree explicitly.
   Cross-vendor review runs only when the endpoint and disclosure decision
   permit it. CI and branch protection gate the human merge; Beads close after
   the declaring change reaches the integration branch.
6. **Handover.** The session records open decisions, exact commits, gate state,
   costs and next action in a dated handover. The coordinator renders the JSONL
   export once, checks identity, and pushes Dolt state. Every number names its
   measurement commit or date.

The session context loads the current change, open decisions, invariants and
gate state first. A compaction check preserves those items; verification emits
short verdicts with links to evidence instead of raw logs. Living-spec updates
use explicit ADDED, MODIFIED, REMOVED and RENAMED sections; a MODIFIED section
contains the complete replacement text.

## Enforcement and runtime controls

Every binding harness rule names its enforcing test or gate. A rule awaiting
enforcement stays advisory with an owner and due date. Every gate has a
known-bad case that makes it fail and refuses an empty subject set. The gate
manifest is the sole list; hooks and Omnigent policies are adapters or early
stops, not replacement sources of gate truth.

Omnigent policies cover repository write scope, secrets, network egress,
unsandboxed shell, workflow dispatch, pushes and costs. Each policy is proven
on a harmless known-bad probe before use. Policy and sandbox behavior are
version-specific and belong in a pinned compatibility record. An explicit
endpoint registry and leak check precede any foreign model call. The runtime
must fail closed when a required endpoint or policy cannot be verified.
The worktree probe also checks whether the chosen policies allow `git worktree
add`. A spend cap is treated as a stop control only after the pinned runtime
has demonstrably stopped the worker at its limit; model downgrading alone does
not meet that condition. A full Beads backup and restore rehearsal protects
state beyond the issue-level JSONL export before any storage-mode change.
Omnigent's official [agent specification](https://github.com/omnigent-ai/omnigent/blob/main/docs/AGENT_YAML_SPEC.md)
and [policy documentation](https://github.com/omnigent-ai/omnigent/blob/main/docs/POLICIES.md)
support the intended configuration model; neither proves this repo's policies
or sandbox work until exercised locally.

## Acceptance scenarios

| Scenario | Evidence required |
|---|---|
| Two workers run from the first Omnigent proof of concept | Separate worktrees and contexts; disjoint assigned scopes; concurrent progress visible; coordinator integrates sequentially; no worker writes the shared tracker |
| A worker or Omnigent session dies | A fresh session recovers the spec, assigned step, commit, test verdict and blocker from files and Beads without chat history |
| A worker attempts a forbidden action | The pinned policy returns DENY or ASK in a recorded probe, and CI still rejects a bad merge independently |
| Two workers need Beads writes | The five-check worktree test passes first; if embedded mode cannot sustain concurrent writes, a backed-up migration to server mode is tested before lifting the write ban |
| The tracker store must be recovered | Restore a full backup in a disposable checkout and check issue, dependency and non-issue state; the JSONL export is tested separately as an issue-level recovery view |
| A change is ready for merge | The same `verify` command passes locally and in CI, findings have no open BLOCKER, a human reviews the PR, and the declared Bead closes on integration |
| A foreign reviewer is selected | Endpoint, operator and residency resolve in configuration; disclosure decision and leak check are recorded before any content leaves |
| A public user adopts the kit | A fresh repository runs the kit probe and a first Bounded change from the onboarding page, with no instance secret or domain rule copied |

## Decisions to record

The maintainer's 2026-09-17 direction supersedes the earlier sequencing of
parallelism at M3 and optional Polly use in the [migration research](../research/Migrationsplan_Omnigent_Referenzarchitektur.md)
and the [2026-09-16 proposal](target-architecture.md). An ADR should record
this change, the coordinator-only Beads write topology, the decision rule for
server mode, and the evidence that ends the first parallel pilot. The research
documents remain dated sources; their older sequence must not silently regain
authority. No Omnigent deployment or version choice is approved by this
document alone.
