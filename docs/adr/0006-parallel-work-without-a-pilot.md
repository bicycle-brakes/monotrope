# ADR 0006 — Parallel work without a pilot, one worktree per session

* Status: accepted · supersedes ADR 0001 (early parallelism from M0) ·
  supersedes, in part, ADR 0005 (its Omnigent session policy, its M0
  validation, and a worker's creating and closing of beads) and ADR 0002
  (its pilot store, its W1 activation condition and its M0 validation) ·
  amends D-3 and D-7 of the
  2026-09-16 interview a second time
* Review: direction chosen by the maintainer, 2026-09-27 (option "parallel
  from now, within bounds" of two); accepted by the maintainer,
  2026-09-27, in a commit signed with the maintainer's Touch-ID key ·
  Decider: maintainer · prepared by a Claude Code session
* Date: 2026-09-27 · accepted 2026-09-27

## Context

ADR 0001 moved parallel coding forward to M0: a pilot with two coding
workers under one fenced coordinator, in a throwaway repository, with an
isolated-worktree enforcer (W0) and an exclusive-coordinator enforcer (W1)
as prerequisites. ADR 0005 then let workers claim their own bead and held
that with three layers, the second of which is a custom Omnigent session
policy; its validation is "in M0".

On 2026-09-23 the maintainer dropped the M0 pilot. Omnigent is used as its
authors intend it: `omnigent claude --use-native-config`, default settings,
no Omnigent sandbox, telemetry off (`~/.omnigent/config.yaml`,
`OMNIGENT_ANALYTICS=0`). A start on 2026-09-23 showed that it runs and
answers. The pilot material is kept outside this repository
(`~/omnigent-m0/`, protocol `PROTOCOL.md`); it is not a record here.

That leaves ADR 0001 without the thing all its contracts rest on, and ADR
0005 with a layer nobody will configure and a validation that will not run.

The lakeswitch-ai decision record answers the same question for both
repositories. D-60 ("one writer per checkout; parallel sessions only in
their own worktrees", ratified by the maintainer on 2026-09-26 in RC-003)
isolates parallel sessions by worktree rather than by a coordinator, caps
the writing sessions per repository at `writing_sessions_per_repository`
(default 2, D-59), and keeps ADR 0005's claim rule as the one exception to a
single tracker writer.

## Decision Drivers

* The maintainer wants parallel work now, not after a pilot.
* Omnigent runs unmodified; nothing here may depend on an Omnigent policy or
  sandbox the maintainer does not run.
* Every boundary is held by a tool or a declared rule, not by an instruction
  to an agent (the driver of ADR 0005).
* One place still decides a bead's outcome: its holder.

## Considered Options

* **(a) Parallel from now, within bounds.** No pilot; the adoption path
  starts at M1. Parallel sessions are allowed from the start, each in a
  worktree of its own (D-60), and a worker claims its own bead (ADR 0005).
* (b) Serial until M3. Back to D-7 as first recorded; ADR 0005's claim rule
  rests until then. Rejected by the maintainer on 2026-09-27: it gives up
  the early parallelism chosen on 2026-09-17.

## Decision

**(a)**, with these contracts:

* **No pilot.** The adoption path is M1 (routine Bounded work) → M2
  (Feature and the cross-vendor path) → M3 (qualified unattended runs) → M4
  (justified hardening). There is no M0 and no throwaway repository.
* **Isolation by worktree.** Every writing session beyond the first works
  in a worktree of its own. At most `writing_sessions_per_repository`
  writing sessions run in one repository (D-59, D-60). This takes the place
  of ADR 0001's W0 and its limit of two coding workers.
* **Tracker writes, as D-60 has them.** The first writing session writes the
  tracker: it hands out beads, runs `bd ready`, creates follow-up work as
  `discovered-from` the bead it came from, closes beads, reprioritises and
  links. A worker session claims the one bead it works on and adds its
  handover comment to that bead, nothing more. That is the part of ADR
  0005's rule D-60 keeps as its one exception. No exclusive coordinator
  process (ADR 0001's W1) is required.
* **The layers that hold it**, none of them an Omnigent setting:
  1. bd's own claim rules, as measured for ADR 0005 on 2026-09-23 (bead
     coding-harness-m34): a claimed bead cannot be closed by another actor
     or reassigned without `--force`, a contested claim has one winner, and
     a write carrying `--if-assignee=<actor>` is refused on a bead held by
     someone else;
  2. the write guard of D-60, which refuses writes from a second session in
     the same checkout and tracker writes other than a claim or a handover
     comment from a session that is not the first;
  3. bd's events journal as the after-the-fact check, as in ADR 0005.
* **D-3, amended again.** One bead per change remains the default. A task
  bead under the change epic is used when two sessions need separate
  ownership; its worker claims it itself. Plan steps keep stable IDs.
* **D-7, amended again.** Parallel sessions are available from M1, within
  the bounds above. Git-native verification stays independently usable.

## Consequences

* **ADR 0001 is superseded.** Its pilot, its throwaway repository and its
  W0/W1 prerequisites lapse. The serial path stays available; it is simply
  one writing session.
* **ADR 0005 is superseded in part.** Its layer 2 (the Omnigent session
  policy) and its validation "in M0" lapse; the write guard of D-60 takes
  layer 2's place. Of its decision, a worker's claim of its own bead stays
  in force, and a worker's creating follow-up work and closing its bead
  pass to the first session, as D-60 has it.
* **ADR 0002 is superseded in part** as well: its pilot store, its W1
  activation condition and its M0 validation lapse with the pilot. Its
  rules on stale or duplicate results stay and apply to coordinated runs,
  when there are any.
* **Until the maintainer rewrites house rule 4.** AGENTS.md house rule 4
  says that while another session runs, none writes the tracker. With no
  Omnigent workers, every session is interactive, so the rule binds them
  all. Until the maintainer rewrites it (owed item "Coding Harness 7" of
  the lakeswitch-ai decision record, the maintainer's own edit), parallel
  sessions work in worktrees of their own but make no tracker writes while
  another session runs; the worker claim above waits for that edit.
* **Owed before this holds by tool rather than by rule.** The write guard
  of D-60 — the per-checkout lock, the session cap and the tracker-write
  refusal — does not exist yet in either repository. Until it does, the
  bounds are stated and not enforced; the maintainer's display warns of a
  second session in the same checkout (`tools/claude-code/`). Building the
  guard is its own change.
* **Bead coding-harness-36z** (workers claim their own bead, proven in M0)
  loses its M0 proof. It is to be re-scoped to the D-60 guard and the
  events-journal check; this ADR does not write the tracker.
* **Worktrees are not a security boundary.** Without an Omnigent sandbox, a
  worktree keeps sessions from colliding; it does not confine what an agent
  can reach. The target document's trust contracts that assume a sandbox
  are open, not settled by this ADR.
* The target document (`docs/architecture/2026-09-17-omnigent-first-target.md`)
  still describes the M0 design. A notice at its top, in its D-3 and D-7
  rows and in its tracker section records this decision; the rest of its M0
  text is kept as the record of the earlier design, as it was for ADR 0005.

## Validation

* Once house rule 4 is rewritten: two writing sessions in two worktrees of
  one repository each claim their own bead, finish, and leave an events
  journal in which every write other than a claim or a handover comment
  comes from the first session.
* Once the D-60 guard exists, its Known-Red cases pass: a second writing
  session in one checkout is refused; a writing session beyond the cap is
  refused; a tracker write other than a claim or a handover comment from a
  session that is not the first is refused.
