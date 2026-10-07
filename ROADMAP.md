# Roadmap

What Coding Harness works on now, next and later. Themes, not tasks: task
status stays in Beads (`tools/bd ready`). At most three themes are **Now**.

**A trial** (maintainer, 2026-10-05; research note
`docs/research/2026-10-05-likec4-roadmap-arc42.md`, part B). Every handover
checks whether Now is still true. This file becomes a kit template only
after it stays true through two handovers; if a handover finds it stale
twice, it is removed.

Last checked: 2026-10-05, `main` at `87daf91`. Appetites are first proposals,
set by the agent that drafted this file; the maintainer's merge confirms or
changes them.

## Now

1. **Forms and their checker.** Every change uses one form for its spec, its
   design and its review findings, and a checker holds class, Definition of
   Done and the design duty. Why: specs and findings are written by hand from
   memory today, and nothing checks that a change has what its class owes.
   Appetite: 3 sessions. Beads: template bundle (coding-harness-9qo),
   change-artefact validator (coding-harness-jc3), findings as checked data
   (coding-harness-4me).
2. **LakeSwitch reads Coding Harness.** LakeSwitch takes the workflow from a
   pinned Coding Harness release instead of its own copy, and drops its own
   ADR-answer pilot. Why: two copies of one rule set drift, and LakeSwitch's
   pilot expires on 2026-12-15. Appetite: 5 sessions. Beads: foundation first
   slice (coding-harness-s6i), project file and locked dependencies
   (coding-harness-ei0), release builder and pin (coding-harness-dj9), the
   ADR-answer principle (coding-harness-3ar).
3. **Hermes runs Coding Harness's recurring jobs.** Hermes Agent, already
   prepared in adhd-relief, becomes the runner for unattended jobs here,
   first the weekly re-check of research notes; it writes files only, and a
   script the maintainer owns opens the pull request. Why: research ages
   unnoticed, and the maintainer chose Hermes over the assessment's "not
   now" (2026-10-05). Appetite: 4 sessions plus one afternoon at the laptop
   for the shared spike. Beads: the Hermes runner (coding-harness-i3y),
   research currency (coding-harness-pu9).

## Next

- **The repository in English.** House rule 1 holds everywhere: the
  matched messages with their tests, the rule set, German identifiers.
  Moved from Now on 2026-10-05 to make room for Hermes. Bead: translate the
  remaining German (coding-harness-yim).
- **Stage 2 live.** Codex and GLM review Coding Harness changes before the
  merge; the first three runs are measured. Waits for the maintainer at the
  laptop (permission for `codex exec`, finding F-12, merging PR #60). Beads:
  coding-harness-bc9, coding-harness-kw0.

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
