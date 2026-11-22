---
title: "Research — draft-known-red"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-83e
owner: Data Architect
provenance: ai-drafted-reviewed
neighbours: []
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-22", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# draft known red — Research

Stage-2 call, 2026-11-22: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason research swarm refuses: its state store must lie outside the home directory (XDG_STATE_HOME), not set up for this night run · leak check clean over 1167 files, 5376 commits, 12 rules.

## Runner exploration — 2026-11-22

## Research: draft-known-red (phase 1, read-only)

I read the repository through Read, Grep and Glob only and changed no file. The runner writes `research.md`. Line numbers below are for orientation; the symbol names are the stable references.

### What exists today

- **The bead's problem is recorded in the handover.** `docs/journal/handover/2026-10-17-night-run-sixth.md` (section on the new bead, around lines 127–131) says a draft on a known-red tree fails every attempt, the runner restores the work, and `--stage2-off` is refused for `draft`. It adds that each spec redraft that night cost about 30 minutes and had to be recovered from `refs/stage2/attempts/research-swarm/`. The bead is coding-harness-83e, P1, discovered from coding-harness-icw.
- **The queue order is recorded in `docs/research/2026-10-31-run-plan.md`** (around line 305). It lists 83e ("draft on a known-red tree") among the research-swarm changes that start after 4tr4 merges.
- **The `--stage2-off` refusal is in code.** `scripts/stage2.py`, in the argument handling near line 12422, refuses `--stage2-off` for every verb except `explore`, `implement` and `repair`. So `draft` cannot be run with the Haiku route.
- **The draft verb is `draft(root, change)` in `scripts/stage2.py` (around line 11361).** Its order is: `preflight` (which reads the bead from the header of `research.md`), `refuse_preexisting`, `refuse_unreadable_statements`, a baseline `HEAD` read, then up to three attempts: Codex, Codex repair, and GLM 5.3 (`routes` list, around line 11381). Each attempt calls `run_codex(..., verb="draft")` or `run_work_model(...)`, and after a call it runs the leak-check path and the moved-`HEAD` guard.
- **The draft prompt is `draft_prompt(ctx, diagnostics)` (around line 11104)** and receives the diagnostics of earlier failed attempts. `draft_keep` (around line 11136) decides which paths a draft may keep.
- **The restore mechanism is `restore_baseline` (around line 6066).** It puts every path except `keep` back to the baseline after a failed model call, and `plan_baseline_restore` (around line 5990) plans the restore first. This is the "runner restores the work" step in the handover.
- **The draft's gate is the document subset.** `docs/WORKFLOW.md`, section "The draft (phases 2, 2b and 3)" (around lines 1536–1575), says the draft runs only the locally runnable gates that the gate registry assigns to the document subset (`document_gates` in `scripts/stage2.py`). No pytest and no code or kit gate runs there. A red check fails the attempt, except that the runner sets `ADR_ANSWERS_TOLERATE_CHANGE=<change>` for `adr-answers` only.
- **A red-first mechanism exists for `implement`, not for `draft`.** `red_first(root, baseline, test, key, tools)` (around line 8988) runs one named test on the baseline's code in a private repository. `RED_FIRST_MINUTES = 10` (around line 545) bounds it. The draft path does not call it.
- **Related text on Known-Red.** `docs/adr/0006-parallel-work-without-a-pilot.md` (around lines 153–156) uses "Known-Red" for the D-60 writing-session guard's validation cases. That is a different topic; the name only overlaps. `docs/journal/handover/2026-09-17-tracker-pin-and-session-end-interview.md` (around line 214) mentions "4 known red" in the kit tests, also unrelated to the draft path.
- **Earlier specs and changes.** `plans/changes/` has no other change with a `draft-known-red` name. `plans/INDEX.md` (line 600) lists only this change, as `draft`, bead coding-harness-83e, dated 2026-11-22.

### Where it lives

- Draft verb and routes: `scripts/stage2.py`, `draft` (around line 11361), `draft_prompt` (around 11104), `draft_keep` (around 11136).
- Preflight and refusals: `scripts/stage2.py`, `preflight` (line 1830), the verb argument check (around line 12422).
- Restore: `scripts/stage2.py`, `restore_baseline` (around line 6066), `plan_baseline_restore` (around 5990), `save_attempt` (around 5935, which writes the `refs/stage2/attempts/...` snapshots).
- Document gate: `scripts/stage2.py`, `document_gates` (named in `docs/WORKFLOW.md`, lines 1555–1561).
- Red-first probe: `scripts/stage2.py`, `red_first` (around 8988) and `RED_PROBE_SOURCE` (around 551).
- Documented doctrine: `docs/WORKFLOW.md` §4, "The draft (phases 2, 2b and 3)".

### What is unclear

- **Why a known-red tree fails the draft.** The draft runs only the document subset, and `WORKFLOW.md` says no pytest runs there. So a red test should not reach the draft gate by that path. The handover says the draft fails every attempt on a known-red tree, which points to another check, maybe the `preflight` or the leak check, or a document gate that reads the tree's state. Not found in the code I read. Open question: which check fails the attempt, and with what message. A night-run log or the attempt's diagnostics in `refs/stage2/attempts/` would settle it; I have not read those.
- **The current red state of the tree.** The handover reports 46 failing swarm tests on 2026-10-17 at `make verify` (2254 passed). I cannot run tests and did not read a current run. Open question: whether that red set still exists on `feat/draft-known-red` today, and which tests are red.
- **Whether `draft` should be red-aware.** The code has a red-first probe, but it is wired only into `implement`'s path. Whether a draft should check the baseline's red set or only its own document gate is a design question, not something this research settles.
- **The bead's own description.** I did not find the text of coding-harness-83e beyond the handover and run plan. Its class is not confirmed in the bead; the change's `research.md` header says `feature` only in the research swarm plan. Not read: `tools/bd show coding-harness-83e`, which I cannot run.

### Which files a change would have to touch

Read-only facts about where the mechanism lives, not a design: `scripts/stage2.py` (draft verb, preflight, route list, restore, document gate wiring, `red_first`); `docs/WORKFLOW.md` §4 "The draft (phases 2, 2b and 3)" (the doctrine the code must match); `tests/` files that cover `stage2.py`'s draft verb (not enumerated here; not searched in this pass); and, if the `--stage2-off` refusal changes, the argument check near `scripts/stage2.py` line 12422.
