---
title: "Research — bead-topic-in-research"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5vts
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# bead topic in research — Research

## Topic (bead coding-harness-5vts)

Class: bounded.

Why: a stage-1 explore (--stage2-off, Haiku or Sonnet) cannot read the tracker; on 2026-11-25 the first explore of test-ci-shared-tree guessed its topic from the change name and had to be rerun. For every later lane the orchestrator copied the bead description into research.md by hand. Recorded as tracker memory stage1-explore-needs-topic.

What: scripts/new_change.py already reads the bead's status from the tracker export; it also writes the bead's description under a '## Topic (bead <id>)' heading below the research title, so every harness's explorer sees it. A missing or empty description is named, never invented.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1325 files, 6161 commits, 12 rules.

## Runner exploration — 2026-11-28

The research is ready to append to `plans/changes/bead-topic-in-research/research.md`. I did not edit any file: this phase is read-only, and the runner writes the artefact.

## What exists today

- **The change's own research skeleton already has a topic section.** `plans/changes/bead-topic-in-research/research.md` carries `## Topic (bead coding-harness-5vts)` with the class (`bounded`), the reason and the claimed behaviour. That section was written by hand, not by a script. The body below it is still the generated skeleton.
- **`scripts/new_change.py::main` reads only the bead's `status` from the export.** It calls `reg._bead_export_path()` and `reg._bead_statuses()`, refuses a missing bead, a missing export and a closed bead, and writes the folder. `_bead_statuses` in `scripts/plans_registry.py` keeps only `id` and `status` from each JSON Lines row.
- **`scripts/new_change.py::BODY_TEMPLATE` has no topic section.** It holds the title, the phase-1 pointer and the provenance notice. `_frontmatter_template` and `_known_field_values` do not touch the bead description either. So the sentence in this change's research.md, "scripts/new_change.py already reads the bead's status … it also writes the bead's description under a '## Topic (bead <id>)' heading", is not borne out by the code in this tree.
- **Other changes carry the same topic section, copied by hand.** `plans/changes/*/research.md` at line 22 holds `## Topic (bead …)` in `agent-policy-list`, `availability-scrub-import`, `cheap-checks-admission`, `enqueue-pr`, `frontmatter-batch-log`, `slow-test-fixes`, `standin-call-counter`, `test-ci-shared-tree` and `worktree-setup-hook`. Most say "copied by the orchestrator 2026-11-25"; `enqueue-pr` and `worktree-setup-hook` do not carry that note.
- **Stage 2 depends on the skeleton text.** `scripts/stage2.py::skeleton_notices` reads `new_change.BODY_TEMPLATE` at call time. It splits the template on blank lines and treats every part after the title as a generated notice, which `research_opening_notices` then strips. Any section added to `BODY_TEMPLATE` would become one of those notices.
- **Tests pin the template.** `tests/test_stage2.py` (helper near the research skeleton fixture, and `test_new_change_creates_the_folder_and_a_current_index`) and `tests/test_stage2_swarm.py` (the swarm skeleton helper) both build their fixtures from `new_change._frontmatter_template` and `BODY_TEMPLATE`.
- **The entry points.** `Makefile` line 65 runs `python3 scripts/new_change.py "$$NAME" --bead "$$BEAD"` (the `change` target). `.claude/commands/workflow-start.md` invokes the same script. `docs/WORKFLOW.md` (line 530) states that the call "requires an existing bead, creates none".
- **Guard and kit.** `scripts/new_change.py` calls `scripts/check_worktree_state.sh` before writing. `scripts/ci_gates.py` (entry `"new_change.py"`, around line 307) and `scripts/kit/manifest.yaml` (around line 196) list the script as a kit file with a reason.
- **Neighbour records.** Handover `docs/journal/handover/2026-11-25-night-run-seven-prs.md` (around line 145) names `coding-harness-5vts` as the bead for "new_change.py writes the bead text as …". `docs/research/2026-11-02-firstmate-video.md` (around line 90) notes that `new_change.py` requires an existing bead.
- **Decision record.** `plans/changes/bead-topic-in-research/decisions.md` marks the phase-1a interview as skipped under the bounded standing grant, on the premise that the bead "fully specifies" the behaviour.

## Where it lives

- The bead export is read through `scripts/bead_render.py::render_pfad()`, which returns a fresh render, or the path in `BEAD_RENDER` in CI. `render_beads_export.py` is the one-writer renderer it imports. No committed `.beads/issues.jsonl` exists in this worktree (a glob for it returned nothing).

## What is unclear

- **Whether the bead export carries a description field.** `_bead_statuses` reads only `id` and `status`. `render_beads_export.py` was not read, so I cannot say whether a row includes `description`, or what its key is called. Until that is read, the source of the topic text is unverified.
- **Where the topic text should come from.** The bead description is the premise. Whether `bd` exports it under a field the renderer keeps is open.
- **How "missing or empty" is treated.** The change says a missing or empty description is "named, never invented". No existing code path names that case for a topic; the closest is the existing `Bead '<id>' is not in the export` refusal.
- **Whether the other nine changes' hand-copied topics are the same text as the bead.** I did not compare them against the export, so I cannot say whether they drifted.
- **Whether the BODY_TEMPLATE change alters skeleton stripping.** `skeleton_notices` treats every blank-line-separated part after the title as a notice. How a topic section that is filled per bead would interact with that is not settled by reading the code.

## Which files a change would have to touch

- `scripts/new_change.py`: read the description from the export (the `_bead_statuses` path or a sibling helper in `plans_registry.py`), and write the `## Topic (bead <id>)` section in `BODY_TEMPLATE` or after it. Empty or missing is named.
- `scripts/plans_registry.py`: `_bead_statuses` or a new reader for the description.
- `scripts/stage2.py::skeleton_notices` and `research_opening_notices`: check that they still strip only the two generated notices once a topic section exists.
- `tests/test_stage2.py` and `tests/test_stage2_swarm.py`: the skeleton fixtures that build `BODY_TEMPLATE`.
- `tests/` for `new_change` itself: the test named `test_new_change_creates_the_folder_and_a_current_index` lives in `tests/test_stage2.py`. No dedicated `new_change` test file was found in this read.
- `plans/changes/bead-topic-in-research/research.md`: the hand-written topic section and the claim it makes about `new_change.py`.
- `docs/WORKFLOW.md` (line 530) only if the phase-1 description of the call changes.
