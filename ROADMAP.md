# Roadmap

What Coding Harness works on now, next and later. Themes, not tasks: task
status stays in Beads (`tools/bd ready`). At most three themes are **Now**.

**A trial** (maintainer, 2026-10-05; research note
`docs/research/2026-10-05-likec4-roadmap-arc42.md`, part B). Every handover
checks whether Now is still true. This file becomes a kit template only
after it stays true through two handovers; if a handover finds it stale
twice, it is removed.

Last checked: 2026-10-11, `main` at `a6b7150`. Appetites are first proposals,
set by the agent that drafted this file; the maintainer's merge confirms or
changes them.

## Now

1. **Forms and their checker.** Every change uses one form for its spec, its
   design and its review findings, and a checker holds class, Definition of
   Done and the design duty. Why: specs and findings are written by hand from
   memory today, and nothing checks that a change has what its class owes.
   Appetite: 3 sessions. The template bundle is done (coding-harness-9qo,
   closed). Beads: change-artefact validator (coding-harness-jc3), findings
   as checked data (coding-harness-4me; stays a table, a gate is open).
2. **LakeSwitch reads Coding Harness.** LakeSwitch takes the workflow from a
   pinned Coding Harness release instead of its own copy, and drops its own
   ADR-answer pilot. Why: two copies of one rule set drift, and LakeSwitch's
   pilot expires on 2026-12-15. Appetite: 5 sessions. Locked dependencies are
   done (coding-harness-ei0, closed). Order, decided 2026-10-11: foundation
   first slice (coding-harness-s6i), then release builder and pin
   (coding-harness-dj9), then the ADR-answer principle with the full pin
   (coding-harness-3ar; plan in
   `docs/research/2026-10-11-adr-answer-pin-plan.md`).
3. **Stage 2 that can be trusted.** The foreign-model runner stays live, and
   its checks cannot be bypassed or lost. Why: on 2026-10-11 a model repaired
   a red run by deleting tests and two failed attempts left no trace. Appetite:
   3 sessions. Beads: every criterion names its proof (coding-harness-909,
   ADR 0013 awaits the maintainer's merge), diagnostics of failed attempts
   (coding-harness-cit), an ADR names its owning change (coding-harness-afa),
   review rounds until one finds nothing (coding-harness-dx0), live view of a
   round (coding-harness-uco).

## Next

- **The repository in English.** House rule 1 holds everywhere: the
  matched messages with their tests, the rule set, German identifiers.
  Moved from Now on 2026-10-05 to make room for Hermes. Bead: translate the
  remaining German (coding-harness-yim).
- **Stage 2 on Pi.** The interactive session and GLM runs go through Pi
  instead of Claude Code. Waits for the maintainer's Mac smoke test planned
  for 2026-10-14. Beads: session verb on Pi (coding-harness-351), GLM
  through Pi (coding-harness-rwa). Stage 2 itself is live (coding-harness-bc9
  and coding-harness-kw0, closed).

## Later

- **Safe parallel sessions:** the write guard and session start after D-60
  (coding-harness-36z, coding-harness-9ca), the tracker export
  (coding-harness-1jg, coding-harness-1jg.4).
- **Public readiness:** licence, onboarding page, denylist gate
  (coding-harness-lir).
- **Doctrine upkeep:** corpus correction (coding-harness-bt8), per-instance
  model routing (coding-harness-qvl), LakeSwitch decisions promoted into
  specifications (coding-harness-mr2), workflow-entry tests
  (coding-harness-kkh).
- **Omnigent:** the default policy, layer 2 (coding-harness-671).
- **Hermes runs the recurring jobs — parked** (maintainer, 2026-10-11; was
  Now 3 since 2026-10-05). Why parked: the first job, the weekly re-check of
  research notes, finds no note due before about 2026-12-15 (0 of 26 due on
  2026-10-11); ADR 0010's revisit trigger 5 fired when PR #60 merged
  (2026-10-07), so running Hermes without the leak check goes back to the
  maintainer; and slice 2's endpoint entry conflicts with the stage-2
  `opencode-go` entry on `main`. What is built stays: the job prompt
  `prompts/research-recheck.md` on `main`, slices 2 and 5 on the branch
  `feat/hermes-runner-2` at `faffe99`. Re-entry: when notes fall due, the
  re-check runs once by hand and is measured first. Beads: the Hermes runner
  (coding-harness-i3y), research currency (coding-harness-pu9).
