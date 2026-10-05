---
title: "Session handover — work done while the maintainer was away, seven PRs waiting, 2026-10-05"
category: handover
created: 2026-10-05
updated: 2026-10-05
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-05"
tags: [handover, adhd-frame, template-bundle, translation, stage-2]
target_ref: "f985698"
bead: coding-harness-9qo
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

The maintainer was away from 2026-09-30 evening to 2026-10-04 and asked the
session to work off the plan meanwhile. Seven pull requests wait for them
(#60, #62 to #67), all with green CI and mergeable as of 2026-10-05. A third
change, the template bundle, is in its first repair round and has no pull
request yet. Answers the session had to choose without the maintainer are
marked provisional in each change's `decisions.md` and listed in its pull
request.

## Where we are

As of 2026-10-05, `origin/main` at `f985698`:

- **#67 — ADHD frame** (bead coding-harness-q24): a plan card in
  `prompts/03-plan.md`, an appetite stop and a timed `done:` line in
  `prompts/04-implement.md`, "What could break" in the PR templates, the
  handover skill renamed to `handover` with "always a pull request". Four
  provisional answers to confirm; one minor finding (F-10) escalated; after
  the merge the maintainer reinstalls the Claude Code display.
- **#60 — stage 2** (bead coding-harness-bc9): stays open by the
  maintainer's decision. Repair round 2 fixed F-10 and F-11; one minor
  finding (F-12) is escalated to the maintainer.
- **#62 to #66 — translations** (bead coding-harness-yim): templates,
  `plans_registry.py` and `new_change.py`, `tests/test_ci.py`, five test
  files, five scripts. No code change in any (AST compared). Strings a test
  matches stay German until the next slice.
- **Template bundle** (bead coding-harness-9qo, branch
  `docs/template-bundle`): spec, findings and ADR templates plus
  `tests/test_templates.py`, built and green (568 passed, 15 skipped at
  `e3f997e`). The phase-6 review (`7e11f82`) found one blocker (the spec
  template states "one condition per criterion" as a rule, which only PR #60
  introduces) and five minor findings, among them two tests that search the
  whole file for a word and so miss a deleted definition. Repair round 1 was
  started on 2026-10-05.

## Next step

When the template-bundle repair round reports back: have its fixes
re-reviewed on Opus 5.5, then ask the maintainer the ADR question for the
template bundle (proposed "no"), switch its class to `feature` with the
answer recorded, and open it as a decision PR.

## Needed from the maintainer

**Go through the seven pull requests.** Recommended order, least effort
first:

1. #62 to #66, translations: nothing to decide.
2. #67, ADHD frame: confirm the four provisional answers at its top, decide
   finding F-10, then reinstall the display at the laptop
   (`tools/claude-code/install.sh --check`, then `install.sh`).
3. #60, stage 2: stays open; decide finding F-12 when you decide the PR.

## Decisions and preferences

From the maintainer, not to be asked again:

- 2026-09-30: work off the plan while away; nothing is merged without the
  maintainer; Claude only (no Codex, no GLM); PR #60 stays open.
- Earlier decisions of 2026-09-30 stand (decision by merge, ADR 0008; review
  on Opus 5.5 and implement on Sonnet until stage 2 is live; see the
  hand-over `2026-09-30-decision-by-merge-and-stage-2.md`).

Chosen provisionally by the session, awaiting confirmation:

- ADHD frame (`plans/changes/adhd-frame/decisions.md`): the skill rename
  travels in #67; the acceptance card lives in the PR templates; the plan
  card starts phase 4 unless the maintainer says stop; only the maintainer
  may answer "continue" at an appetite stop.
- Template bundle (`plans/changes/template-bundle/decisions.md`): the
  contract core only (design phase, ROADMAP, arc42 and LikeC4 not now); the
  practised findings table; protected areas and failure mode mapped onto
  existing spec parts; LikeC4 deferred with D-15 unchanged; the appetite
  bounds phase 4 only; class `feature` with the ADR answer proposed "no",
  set in phase 7.

## Open work and blockers

Task status is in Beads (`tools/bd show <id>`):

- Template bundle for M1 (coding-harness-9qo): in progress, repair round 1.
- ADHD frame in the phase prompts (coding-harness-q24): in progress, closes
  with #67 (`Closes-Bead` trailer).
- Stage 2: Codex and GLM review Coding Harness changes (coding-harness-bc9):
  in progress, #60 open.
- Translate the remaining German (coding-harness-yim): in progress. Next
  slices need #63 and #65 merged first (matched strings move with their
  test patterns); the rule set is a decision PR; identifier renames need a
  plan of their own.
- The ADR-answer principle (coding-harness-3ar): in progress, open until
  LakeSwitch switches.
- Closed on 2026-09-30: `harness decide` with signing tools
  (coding-harness-xv3, superseded) and the signed-decision key-list bug
  (coding-harness-in1, moved to lakeswitch-ai).

## Working state and parallel-session boundary

- `main` checkout clean at `f985698`.
- Worktrees, one per open branch: `stage-2-codex-glm` (#60),
  `adhd-frame` (#67), `template-bundle` (no PR yet), `translate-templates`
  (#62), `translate-plans-tooling` (#63), `translate-test-ci` (#64),
  `translate-tests-batch` (#65), `translate-scripts-batch` (#66),
  `handover-2026-10-05` (this hand-over). Remove each after its merge.
- Other sessions (read 2026-10-05): `lakeswitch-ai-bd` in lakeswitch-ai
  (writes nothing here) and one in `/private/tmp`. This session is the
  tracker writer for coding-harness.

## Validation

- CI green on #60 and #62 to #67, all mergeable (read 2026-10-05).
- `make verify` (commit signing off by environment) green on each branch at
  its last code commit; counts are in each pull request's evidence block.
- Not run: any Codex or GLM call; `tools/claude-code/install.sh` (the
  maintainer's step); a merge of all branches together (pairwise trial
  merges only).
