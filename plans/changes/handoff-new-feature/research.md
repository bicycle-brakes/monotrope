---
title: "Research — handoff-new-feature"
status: draft
implementation_status: none
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-in27
owner: framework-architect
provenance: human-written
tags: [research]
---

# handoff new feature — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-04: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 888 files, 3261 commits, 12 rules.

## Runner exploration — 2026-11-04

The exploration is complete. Here is the research, ready to append to `plans/changes/handoff-new-feature/research.md`.

---

## What exists today

**Two distinct things in this repository are called "handoff":** the session handover (the eighth movement) and the `research-handoff` gate. Which one the new feature targets is not stated anywhere in the tree (see *What is unclear*).

### The session handover (the eighth movement)

- Doctrine: `docs/WORKFLOW.md`, section "The eighth movement: the session handover" — the handover runs across all seven phases and closes one session, not one change; the artefact is `docs/journal/handover/<date>-<name>.md` after `templates/handover.md`; the gate is frontmatter against `scripts/handover_schema.py` (direction, provenance and the goal's standing required). Two standing rules: the handover is the file, not the chat, and every number carries its cut-off.
- The single field list lives in `scripts/handover_schema.py` (module docstring: "the one field list that test and template read from"): `RICHTUNGEN` (`framework->framework`, `framework->project`), `GEMEINSAM`, `KANAL_EXKLUSIV` (`record_sha256`, `acknowledged_by`, `acknowledged_at`, `closed_at`), `PROJEKT_PFLICHT`, `OPTIONAL` — including the process metrics `review_rounds`, `fix_regen_rounds`, `late_findings`, `questions` (comment: added 2026-09-10) — plus `ERLAUBT`, `STATUS` and the record markers `RECORD_BEGIN`/`RECORD_END`. Identifiers are German (house rule 1 schedules their translation for a pull request of its own, bead coding-harness-yim).
- `templates/handover.md` shows that schema, it does not define it (its frontmatter is `none` per `provenance.yaml`, as its header states); Variant A is the session handover, Variant B the return channel with the immutable findings block between the record markers.
- The journal holds 62 files as of this read (2026-11-04), from `2026-09-16-coding-harness-bootstrap.md` to `2026-11-03-five-lane-night.md` (Glob over `docs/journal/handover/`). The indexes `docs/_INDEX.md` and `docs/journal/_INDEX.md` are read by `tests/test_feedback_channel.py` (constants `ROOT_INDEX`, `JOURNAL_INDEX`).
- Tests around the handover: `tests/test_feedback_channel.py` (imports `handover_schema` as the single source; its sharpest test `test_handover_records_are_immutable` recomputes the hash over the findings block) and `tests/test_handover_entry.py` (the handover-injection trust threshold, `~/.claude/handover-trust` matched against the origin URL — bead `hit`; its docstring states the German display texts of `tools/claude-code/hooks/handover.sh` stay German by rule). Six further test files mention "handover" — `tests/test_frontmatter_current.py`, `tests/test_provenance.py`, `tests/test_recap_lock.py`, `tests/test_regelwerk.py`, `tests/test_stage2_session.py`, `tests/test_stage2_runs.py` (file list only; the specific mentions are not read).
- Governance: `docs/governance/framework-witt-feedback-loop.md` is the feedback-loop contract the channel test reads (`FEEDBACK_LOOP` constant in `tests/test_feedback_channel.py`); the file itself is not read yet.

### The maintainer's Claude Code display (user-level, stays here)

- `tools/claude-code/` per its README: `statusline.sh`; `hooks/handover.sh` with the subcommands `start`, `show`, `where`, `note` (dispatch `case "$1"` at the end of the file); `hooks/recap.sh` (rolling recap plus automatic session note under `~/.claude/session-notes/`); `hooks/session-scan.sh`; `hooks/parallel-sessions.sh`; `hooks/beads-start.sh` (this repository's SessionStart hook, not part of the user-level install). The `/handover` skill is `tools/claude-code/skills/handover/SKILL.md`: it fixes the section order (`# Resume here`, `## Where we are`, `## Next step`, `## Needed from the maintainer`, …), states that the start hook reads the "Next step" section, and that a handover always opens a pull request; its check step runs `python3 -m pytest tests/test_feedback_channel.py -q`.
- Change rule: a change lands in `tools/claude-code/` and is reinstalled with `tools/claude-code/install.sh`, never only in `~/.claude` (AGENTS.md, "The maintainer's Claude Code display"). README provenance: written 2026-09-18 by Claude Code (Opus 5), "not yet reviewed".
- Travel: `scripts/kit/manifest.yaml` carries `tools/` only as a catch-all `bestand` prefix (comment: the tracker pin) — the claude-code display does not travel with the kit, and the manifest's dry-run skips the three tests whose subject is `tools/claude-code` (manifest entries naming Bead `hit`, around lines 251–257).

### Where the runner touches handovers

- `scripts/stage2.py`: the `session` verb takes `--handover <path>`, default "the change's `handover.md`", whose full text becomes the first message; `--model` and `--handover` are refused on every other verb (argparse help and the `Refused` guard near the dispatch). `scripts/stage2_session.py` implements it (named by `stage2.py`'s `session()`; not read).

### The gate of the same name

- `decisions/gates.yaml`, id `research-handoff`, runs `python3 scripts/check_research_handoff.py`; wired into CI (`.github/workflows/ci.yml`, step id `research-handoff`) and described in `prompts/01-explore.md`, `prompts/01a-interview.md`, `prompts/02-spec.md` and `templates/spec.md` (the `neighbours:` header comment). The check script itself is not read.

### Prior art: the last handover-area change

- `plans/changes/handover-at-95/research.md` (bead coding-harness-l9s, draft, last updated 2026-10-27): automatic handover when the usage window reaches 95 %. It documents that the status line receives `rate_limits.five_hour.used_percentage`, that no hook input carries a percentage, that a hook cannot invoke `/handover`, and that `tools/claude-code/statusline.sh` does not read `rate_limits` today. The folder holds only the research — no `spec.md` (Glob; `plans/INDEX.md` row: draft/none).

## What is unclear

- **The feature itself is not stated in the repository.** The bead `coding-harness-in27` lives in the Dolt tracker under `.beads/`, which this read-only phase cannot query; a search for `handoff-new-feature` and `in27` hits only `plans/INDEX.md` and the change's own files. The name fits at least two surfaces — the session handover (`tools/claude-code/` + schema + journal) and the `research-handoff` gate — and which one, or something else entirely, is an interview question, not a fact.
- Whether `handover-at-95` (l9s) is still pursued or set aside is not stated anywhere in the tree.
- Not read: `scripts/check_research_handoff.py`, `docs/governance/framework-witt-feedback-loop.md`, `scripts/stage2_session.py`, the specific "handover" mentions in the six test files listed above, and the contents of `plans/changes/archive/` (checked by folder name only — "not read", not "not there").
- The only living spec, `plans/specs/implementation-verification/spec.md`, does not cover the handover by its folder and title; its contents are not read.

## Which files a change would have to touch

Depending on the surface, from what exists today:

- Handover structure/sections: `templates/handover.md`, `tools/claude-code/skills/handover/SKILL.md` (the section order is fixed there), `docs/WORKFLOW.md` eighth movement.
- Handover fields: `scripts/handover_schema.py` first (the single field list), the schema shown in `templates/handover.md`, and `tests/test_feedback_channel.py`, which checks the two against each other.
- Display/entry behaviour: `tools/claude-code/hooks/handover.sh` (or `statusline.sh`/`recap.sh`) plus `tools/claude-code/install.sh` reinstall, with `tests/test_handover_entry.py` asserting the display texts (German allowed there by rule).
- The gate: `scripts/check_research_handoff.py` and its tests (tests not yet identified — open question).
- Any of the above also touches `plans/changes/handoff-new-feature/` itself and its row in `plans/INDEX.md`.

---

**Suggested `neighbours:` for the header:** `plans/changes/handover-at-95/research.md` (active change in the same area, research only, bead coding-harness-l9s). No living spec covers this area; `plans/specs/implementation-verification/spec.md` is unrelated by title, contents unread.

**Note for the runner:** the skeleton's frontmatter still says `provenance: human-written`; per the skeleton's own note and `provenance.yaml` (class `ai-drafted-reviewed`, `review_required: true`), filling it with this model output means setting `ai-drafted-reviewed` with `produced_by:` and `review:` blocks. The key open question for the interview: what exactly is the feature of `coding-harness-in27` — the bead description in the tracker is the only place that says.
