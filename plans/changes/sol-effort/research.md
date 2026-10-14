---
title: "Research — sol-effort"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-yzk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, codex, effort]
---

# Sol runs at an effort per verb — Research

Phase 1 for bead coding-harness-yzk, read on 2026-10-13 against branch
`feat/codex-repairs` at `135cb8e`, the branch of the change codex-repairs
(bead coding-harness-0ga, pull request #138, not merged). This change builds
on it because ADR 0017, which it amends, exists only there.

## The request

The maintainer, 2026-10-13, in the conversation, in two steps:

1. "Mache Sol nur mit hoch" — run Sol (`gpt-6.1-sol`) only at effort high,
   after the Codex five-hour limit ran out with about ten max-effort calls in
   one afternoon (drafts, six repairs, reviews).
2. Later the same evening: "Bitte nutze für Korrektur mit Codex Sol mit
   Medium, für das Entwerfen der Spec Sol mit high" — repairs at medium,
   drafting the spec at high.

Read together: repair `medium`, draft (spec, design and plan in one call)
`high`, phase-6 review `high`. No verb keeps `max`.

## Where it stands

- **One constant.** `CODEX = ("openai-codex", "gpt-6.1-sol", "max")`
  (`scripts/stage2.py:154`). `run_codex` reads the effort from it
  (`scripts/stage2.py:794`) and passes `-c model_reasoning_effort="<effort>"`
  (`:805`). Every Codex call goes through `run_codex`: `draft` (`:2775–2776`,
  routes `codex` and `codex-repair`), `repair` (`:2944–2945`, the same two
  routes), `review` and its resumed loop-marks call (`:1071`, `:1099`).
  `run_codex` receives no verb today, so an effort per verb needs either a
  parameter or one endpoint tuple per verb.
- **The endpoint tuple is also an identity.** `run_attempts` compares
  `endpoint == CODEX` (`:2431`, `:2440`, `:2796`, `:2901`) to choose the Codex
  branch and the Codex repair format. Separate tuples per verb would have to
  keep those comparisons true for every Codex tuple.
- **Interactive sessions.** `stage2.py session` (`scripts/stage2_session.py`)
  starts Codex without an effort flag; the Codex CLI's own default applies.
  Not covered by the request.
- **OpenCode Go and GLM.** The review-loop ladder passes Pi `--thinking max`
  (`:892`, ADR 0011); GLM tuples carry `max` (`:149`, `:151`). Neither is Sol;
  both stay.
- **Where `max` is written for Sol** (outside change folders, journal and
  research):
  - `docs/WORKFLOW.md:439`, `:441`, `:442` (stage-1 table, the drafting
    note), `:688–690` (draft rows), `:694` (repair row), `:695` (review row);
  - `prompts/02-spec.md:3`, `prompts/02b-design.md:3`, `prompts/03-plan.md:3`,
    `prompts/06-review.md:5` (Model lines);
  - `docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md:103` (draft at
    `max`), `docs/adr/0017-codex-repairs-taken-findings.md:79` (repair at
    `max`);
  - tests: `tests/test_stage2.py:1752`, `:3701`, `:4612–4620`
    (`test_repair_uses_codex_at_max_effort`), and the WORKFLOW §4 doctrine
    check at `:6332–6365`, which requires effort `max` in every non-Flash
    row of section 4.
- **ADR mechanics.** An amendment to an existing ADR is claimed by the
  change that makes it (ADR 0014); the precedent wording is in
  `docs/adr/0014-a-change-claims-its-adr-files.md:78–80`.

## Questions this change has to answer

- [DECISION] Which effort each Sol verb gets.
- [DECISION] How the change is recorded: a new ADR, or dated amendments to
  ADR 0016 (draft) and ADR 0017 (repair, review re-check).
- [DETAIL] The resumed loop-marks call inside `review` uses the review's
  effort, `high`: it is part of the same phase-6 review.
- [DETAIL] `stage2.py session` stays without an effort flag: the request
  names the runner's verbs, and an interactive session is the maintainer's
  own choice of model in a window.
- [DETAIL] How the effort reaches `run_codex` (parameter or tuple per verb)
  is the design's choice, under the constraint above that every Codex route
  keeps its Codex branch.

## Draft preparation — 2026-10-14

Read in the dedicated worktree on `feat/sol-effort`, HEAD `9113a3d`.
The latest session handover says the maintainer merged the prerequisite
repair change on 2026-10-14; the local diff against `origin/main` now holds
only the generated plans index and this change's inputs. It contains no
ADR edit or edit to the earlier repair change's folder. The earlier
competing-claim failure is therefore not the current diff's state
(`docs/journal/handover/2026-10-14-night-run-third.md`, dated addendum;
`git diff --name-only origin/main...HEAD`). Live PR state was not read
within the worktree-only boundary.

The current runner still pins Sol to `max`. Draft's two Codex routes share
one call site; repair's two routes use `run_attempts`, which already receives
the caller's verb; review has separate verdict and loop-marks call sites.
The label `codex-repair` names a retry in both draft and repair, so the label
alone cannot select an effort (`scripts/stage2.py`, `draft`, `run_attempts`,
`repair` and `review`). The interactive session's exact-argv regression
already requires a launch without a reasoning-effort override
(`tests/test_stage2_session.py`,
`test_codex_is_dispatched_interactively_with_its_exact_safety_flags`).

Only two distinct maintainer-answered interview records stand in
`decisions.md`. The class minimum for a bounded change is one, but editing
either claimed ADR raises the duty to five regardless of class. The check
currently applies that ADR minimum only when an ADR edit is in the measured
diff; a green check on draft files alone does not discharge the planned
amendments' interview debt (`scripts/check_interview_minimums.py`,
`measure`; `docs/WORKFLOW.md`, "Change classes, the ADR question and
decision pull requests"). Completing phase 1a belongs to the orchestrator,
not this drafting call; no missing answer is inferred or invented here.

The requested change-artefact validator and a plan template are not present
in this worktree (`rg --files scripts templates`). The spec uses the spec
template; the plan uses the phase-3 prompt's prescribed form and the existing
plan conventions. The findings file contains draft-attempt audit evidence,
with no phase-2a rows to resolve. This research records no Stage-1 Explore
route to carry forward.
