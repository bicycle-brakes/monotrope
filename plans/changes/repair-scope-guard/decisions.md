---
title: "Decisions — repair-scope-guard"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-t83
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, repair, stage2-runner]
---

# repair-scope-guard — Decisions

Class: bounded (bead coding-harness-t83; orchestrator 2026-10-26: a runner or test fix inside existing behaviour, no ADR).

## SKIP · interview

status: skipped
reason: The bead description (2026-10-15, written from the night handover of that day, section 3) fixes the scope the explore could not read from the tracker: "A Codex repair on the research swarm (2026-10-15) wrote its own handover file docs/journal/handover/2026-10-15-research-swarm-loop-one-repair.md into the branch; the orchestrating session removed it (560160d). REPAIR_FORMAT in scripts/stage2.py says 'repair only the taken rows' but neither names handovers nor puts back stray paths. Needed: the repair prompt forbids handover and journal files, and the post-run check puts back or refuses new files outside the change's scope." On 2026-11-21 the maintainer chose a fresh explore for this lane (chat, ~16:30) and asked for no question windows until the block on 2026-11-23 10:00. Reading (a) of the explore — which files a repair attempt may touch — is the bead's reading. The remaining points are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Journal files are runner-held.** `docs/journal/` joins `RUNNER_HELD` in `scripts/stage2.py`, so the existing checkpoint refuses and restores any stage-2 attempt that writes a handover or journal file, for every writing verb. Reason: one choke point for the incident the bead records; handovers are the orchestrator's work (AGENTS.md, handover as a pull request from the orchestrating session), and the held-path machinery already names, stores and restores such attempts.
- **The repair prompt says it.** `REPAIR_FORMAT` and `REPAIR_FORMAT_FILE_TOOLS` add one sentence: write no handover or journal file and create no file outside the scope named below. Reason: the bead's first half; the prompt tells the model before the guard has to act.
- **New files outside the repair's scope are refused.** A repair attempt that creates a new file (untracked or added) outside its scope fails the post-run check, is stored and restored like a held-path attempt, and the diagnostic names each such file. The scope is: this change's folder `plans/changes/<change>/`, `tests/`, every path a taken row's `Where` cell names, and every path `plan.md` names. Edits to existing tracked files are not part of this guard. Reason: the bead's second half ("refuses new files outside the change's scope"); refusing keeps one attempt semantics instead of a silent put-back.
- **Hand repairs stay out of scope.** The orchestrator's own repairs keep today's doctrine. Reason: the bead names the stage-2 repair prompt and post-run check only.
- **The change-folder exemption stands.** Reason: the change's own artefacts are what a repair writes; the archived `plan-held-paths` stance is not reopened.
- **Neighbour: `repair-hand-held-rows` (bead coding-harness-0zhf).** That change hands held rows to the orchestrator before the attempt and reads `RUNNER_HELD`; adding `docs/journal/` makes rows naming journal files held there too. Whichever merges second rebases on the other. Reason: no conflict in intent, one shared held list.
