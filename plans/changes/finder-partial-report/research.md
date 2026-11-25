---
title: "Research — finder-partial-report"
status: draft
implementation_status: none
date: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-yd8w
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-19", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# finder partial report — Research

Stage-2 call, 2026-11-19: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM via Z.ai fails with claude-code:unrecognized_model since 2026-11-18 (bead coding-harness-b5pu) · leak check clean over 1114 files, 4748 commits, 12 rules.

## Runner exploration — 2026-11-19

## Research: finder-partial-report

The change folder holds only the skeleton. Its `research.md` says the file is empty until phase 1 has run, and `decisions.md`, `spec.md` and `plan.md` do not exist yet. The change's intent is not written anywhere I could read. Bead `coding-harness-yd8w` is named in the frontmatter, but I have no tracker access in this phase, so its description is unread. The reading of "partial report" below is inferred from the code, not from a stated goal.

### What exists today

- **Finder stage.** `scripts/stage2_research_run.py`, `Run.stage_finders` runs the finder trio (`finder_agents`). Each answer is checked by `valid()` against `stage2_research_map.validate_locator_report`, which requires exactly the four locator lists. Answers that fail are passed to `self.invalidate(...)`, which I did not read. Then `Run.require_ok` raises `Stop("a finder failed: <slot> (<outcome>); no later stage starts.")` if any finder is not `ok`. So one failed finder stops the whole run before the map merge.
- **Map merge.** `Run.stage_merge` and `Run.map_merge` (same file) require the merged map to be the exact union of the finder lists. A mismatch raises `Stop` with "no topic starts."
- **Run outcome.** `scripts/stage2_research_run.py`, module function `run(root, change, runner, klass, selection)` catches `Stop` from `current.stages()`. It sets `status = "incomplete - <stop>"` and still calls `current.publish(status, clear=...)`. Only a `Stop` with code 2 (a refusal) is raised to the runner as `Refused`. Any other incomplete status raises `CallFailed`.
- **Partial record in the published block.** `Run.compose` (the function that builds the appended block ending in `<!-- /research-swarm/v2 (quoted) -->`) adds a `research-swarm/v2 partial` fence for every seat whose record is not `ok`. It holds `slot_id`, `outcome`, `error`, `stdout`, `stderr` and `receipts`. Finder records that failed therefore appear in the appended block, and so do the status line `run <id> status: incomplete - …` and any audit lines.
- **Publication.** `Run.publish` (same file) binds the text with `set_append` in the state store before the atomic write of `research.md`. The `clear` flag is set only when the status starts with `complete`.
- **Handoff gate.** `scripts/check_research_handoff.py` has a `KINDS` tuple that includes `"partial"` (line 54 in that file). I did not read how the gate uses it.

### What is unclear

- Whether a `research-swarm/v2 partial` block in `research.md` counts as a complete run for the `research-handoff` gate. I did not read the gate's logic.
- What `Run.invalidate` sets the record's `outcome` to, and whether that differs from an ordinary failure. I did not read `invalidate`.
- Whether `publish` writes the block when the run ends in `Stop` before any finder record exists. I read the path that binds and publishes, but not the store's `set_append` or `publication_bytes`.
- Whether existing tests (`tests/`) cover the case of a failed finder seat with a published partial block. I did not search the tests.
- What the change is supposed to change. Possible readings are: partial finder output kept as usable evidence instead of stopping the run, or a clearer report of which finder seat failed. The folder does not say which, and only the maintainer or the bead can settle it.

### Files a change would likely touch

Based on the symbols above, only files already read or named here: `scripts/stage2_research_run.py` (`stage_finders`, `require_ok`, `run`, `compose`, `publish`), `scripts/stage2_research_map.py` (`validate_locator_report`, `merge_research_map`), and `scripts/check_research_handoff.py` (`KINDS` and its gate logic, not yet read). The tests for these modules were not searched, so they are not listed.
