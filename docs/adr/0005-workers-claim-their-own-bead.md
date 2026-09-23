# ADR 0005 — Workers claim and close their own bead; the coordinator no longer writes alone

* Status: proposed · supersedes, in part, ADR 0002 (the exclusive coordinator
  writer and read-only workers)
* Review: direction chosen by the maintainer, 2026-09-23 (option "workers
  claim themselves" of three, after a check that it is feasible) ·
  Decider: maintainer · prepared by a Claude Code session
* Date: 2026-09-23

## Context

ADR 0002 lets exactly one coordinator write the tracker during parallel
runs. Workers stay read-only, and an OS-level exclusive writer lock (W1)
enforces it. Two reasons carried it. First, the embedded Dolt store was
taken to be single-writer, with concurrent writers "never proven here".
Second, responsibility: one place decides what a status means.

On 2026-09-23 the first reason fell away. Bead `coding-harness-m34`
measured the pinned bd 1.3.0 in embedded mode. Four concurrent writers made
100 creates and 100 updates, with nothing lost and no duplicates, because bd
serialises them. A contested claim has exactly one winner, and the loser gets
exit 1 ("issue already claimed")
([protocol](../research/2026-09-23-worktree-tracker-writes.md)).

The same day showed three weaknesses in ADR 0002's enforcement:

* **A CI gate cannot see a worker's tracker write.** The write lives in
  Dolt, not in the pull request.
* **An OS lock holds on one machine only.** The tracker travels through
  `refs/dolt/data`, and a coordinator is an LLM session, not one
  long-lived process.
* **Omnigent has no ticket concept and no shared-state lock**
  ([README](https://github.com/omnigent-ai/omnigent)). The lakeswitch
  architecture it was chosen for already has workers claim their own ticket
  (`docs/research/Lake-Switch-Architektur-arc42.md`, §5.2.6). ADR 0002 and
  that document contradicted each other.

## Decision Drivers

* Enforcement must happen before the act, not in a gate that cannot see it.
* Every layer must be something a pinned tool or a declared policy does,
  not something an agent is asked to do.
* One place still decides a bead's outcome. That is the bead's holder, and
  bd names the holder.

## Considered Options

* **(a) Only the coordinator writes** (ADR 0002 unchanged, its reason
  updated). Clean responsibility, fully enforceable by the sandbox. The
  coordinator becomes the bottleneck, and found work detours through it.
* **(b) Workers claim, create follow-up work and close their own bead.**
  Chosen, because it is the arc42 role protocol and it is now measured safe.
* (c) A mixed form, where workers claim and create and the coordinator
  closes. Rejected: a path-level sandbox cannot tell the two apart, so it
  would rest on a role check an agent can skip.

## Decision

A worker holds the one bead the coordinator hands it. It claims that bead
itself, records follow-up work as `discovered-from` that bead, and closes it
after the merge. It does not touch another bead. Three layers hold this,
none of them an instruction to the agent:

1. **bd itself** (measured on 2026-09-23). A claimed bead cannot be closed
   by another actor ("assignee is worker-a, actor is worker-b") or
   reassigned without `--force`. A contested claim has one winner. Every
   worker write carries `--if-assignee=<its actor>`, which refuses a write
   to a bead held by someone else.
2. **An Omnigent session policy** (documented, not yet tested). The policy
   is a custom Python policy registered through `policy_modules`
   ([policy guide](https://github.com/omnigent-ai/omnigent/blob/main/docs/POLICIES.md)).
   It keeps the session's assigned bead in its session state. It denies
   every tracker write (`bd` or `tools/bd` with a writing verb) that names
   another bead, any `--force`, any `reclaim`, and any command that sets
   `BD_ACTOR` itself. The actor comes from the session's configuration.
   The sandbox's `write_paths` include `.beads` for workers, because layers
   1 and 2 now carry the boundary.
3. **The events journal as the after-the-fact check** (measured). bd's
   events journal is turned on (`events-journal: true`). It records every
   mutation with actor and assignee. After a run, a check lists every write
   whose actor is not the bead's assignee. Each one is a finding.

The coordinator still hands out beads and never gives the same bead to two
workers. `bd ready` stays with the coordinator. The tracker export question
is gone, because since ADR 0004 no copy is committed.

## Consequences

* **ADR 0002 is superseded in part.** Its single-writer lock and read-only
  workers give way to this decision. Its rules on stale or duplicate results
  (run and attempt IDs) and on the pilot's throwaway store stay. ADR 0002
  records the supersession when this ADR is accepted.
* **The bead `coding-harness-36z` is re-scoped a second time.** It becomes
  the three layers above, proven in the M0 pilot, each with a known-bad
  case:
  * a worker's note on another worker's bead is denied by the policy,
  * a close of a foreign bead is refused by bd,
  * a forged `BD_ACTOR` is denied, and the journal check lists a planted
    foreign write.
* **House rule 4** ("while another session runs, none writes") stays for
  interactive sessions. The exception for Omnigent-run workers is added in
  the change that records the M0 protocol, as ADR 0002 already required for
  its own exception.
* **What stays open.**
  * The policy inspects command text, so an agent that calls bd through a
    script could avoid it. Layer 1 still refuses closes and reassignment
    there, and layer 3 still records the write.
  * The policy guide does not state whether an agent can alter or bypass
    its own session's policies.
  * A second machine is outside one Omnigent server's policies.

  M0 decides whether any of these needs more.

## Validation

* In M0: the three known-bad cases above fail visibly, and one two-worker
  run leaves a journal in which every write's actor is its bead's
  assignee. The protocol is committed.
