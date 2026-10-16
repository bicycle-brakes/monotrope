---
title: "Research — repair-scope"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-t83
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair]
---

# What a repair attempt may write — Research

Phase 1 for bead coding-harness-t83, seeded by the orchestrating session on
2026-10-16 against `origin/main` at `135f029`.

## The question

A Codex repair on the research swarm (2026-10-15) wrote its own handover file
`docs/journal/handover/2026-10-15-research-swarm-loop-one-repair.md` into the
branch; the orchestrating session removed it by hand (commit `560160d` on
`explore/research-swarm`). The `repair` verb of `scripts/stage2.py` tells the
model "Repair only the taken rows below" (`REPAIR_FORMAT`, around line 228)
but names no file it must not write, and its post-run checks neither put
back nor refuse a stray path. Needed (bead text): the repair prompt forbids
handover and journal files, and the post-run check puts back or refuses new
files outside the change's scope.

## Known so far (read, not run)

- `DRAFT_RULES` (around line 238) already says what a draft may write and
  that "the runner puts back every changed path outside the change folder";
  the draft verb has that put-back mechanism — find it and say whether the
  repair can reuse it.
- A repair legitimately changes code, tests, doctrine and the change's own
  `plan.md` (its `## Time used` entry); it must not edit `findings.md` beyond
  the runner's own Status writes (`REPAIR_ANSWER`).
- The embedded `prompts/04-implement.md` asks for a report and a `Resume:`
  line; whether it or another embedded prompt invites a handover file is not
  read yet.

## To explore

1. Where the draft's put-back lives, what it compares against (the baseline
   commit, the ignored-file snapshot), and what it reports.
2. What "outside the change's scope" can mean for a repair, which may touch
   any code or test file: a deny list (`docs/journal/**`, handover files,
   `.beads/**`, other change folders, `AGENTS.md`, settings) versus an allow
   list, and which the existing checks already cover (the implement verb's
   pre-existing-change refusal, `ignored_snapshot`).
3. Which prompts embedded in the repair prompt mention handovers, journals or
   session notes, and how the session-handover rules of `AGENTS.md` reach a
   Codex repair at all.
4. The same question for `implement`: does an implement attempt have the
   same gap?
5. Which tests cover the draft's put-back, so the repair's can follow them.

Stage-2 call, 2026-10-16: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 458 files, 1301 commits, 12 rules.

## Runner exploration — 2026-10-16

The exploration is complete — I have every fact the seed's five questions asked for, each with its source. Here is the prose, ready to append to `plans/changes/repair-scope/research.md`.

---

## What exists today

**The draft has a per-attempt write scope; the repair has none.** After every `draft` attempt that did not fail as a call, `draft_keep` (`scripts/stage2.py`, `draft_keep`) computes what the attempt may keep changed — every path under `plans/changes/<change>/` except `decisions.md`, plus new-ADR paths matching `NEW_ADR` (`docs/adr/\d{4}-[a-z0-9][a-z0-9-]*\.md`, the `NEW_ADR` constant) that the merge base of the baseline and `origin/main` does not hold — and `put_back` (`scripts/stage2.py`, `put_back`) restores everything else to the baseline commit with `git restore --staged --worktree` and `git clean -fdq` over `:(exclude)` pathspecs, returning the sorted list of what moved; a non-empty result is quoted into `findings.md` as "the runner put back what a draft may not change:" through `put_back_lines` (every path in backticks, unbounded — `put_back_lines`). The model is told this contract in `DRAFT_RULES` (`scripts/stage2.py`, `DRAFT_RULES`: "Change nothing else: the runner puts back every changed path outside the change folder except the one new ADR draft, and the change's `decisions.md`"), and the doctrine states it in `docs/WORKFLOW.md` §4, "The draft" ("every path outside the change folder is put back at the baseline before verification, a new ADR file under `docs/adr/` excepted, and the change's `decisions.md` is put back with them").

**A repair attempt's writes are only bounded by when they are measured, not where they land.** `repair` (`scripts/stage2.py`, `repair`) runs on the shared attempt loop `run_attempts` with `allowed = {findings.md}`, and three guards touch scope: the pre-existing-change refusal before the first call (`changed_paths` — tracked diff plus untracked, `changed_paths` — minus `findings.md`; the same refusal stands in `implement`); the full put-back `restore_baseline` (`scripts/stage2.py`, `restore_baseline`) when the model *process* fails, which restores every path but `findings.md` to the baseline and removes gitignored paths created since the pre-call `ignored_snapshot`; and the moved-HEAD stop for Codex calls. After *failed post-run checks* no put-back runs — the code comment says "Failed edits stay in the attempt's evidence" (`run_attempts`), and only `findings.md` (from the pre-call snapshot) and the snapshotted inputs `decisions.md`, `design.md`, `plan.md` are byte-restored before the next attempt. A *passing* attempt is committed whole: `checkpoint` runs `git add -A` (`scripts/stage2.py`, `checkpoint`), so every path the attempt wrote anywhere in the worktree lands in the one commit, once `make verify` (`verify_attempt`), the time-log check, the ruff format step and the answer checks pass. None of those checks (`check_repair_answer`: fixed-line form, findings body byte-equal outside frontmatter, audit line present, released/phase-6 rows unchanged, named test exists, red-first proof) looks for a file unrelated to the taken rows. The doctrine states today's contract positively, `docs/WORKFLOW.md` §4, "The runner is the only way": "What a repair's Codex call writes is checked and committed by the runner, including changes outside the change folder; a checkpoint requires all checks to pass."

**The repair prompt names no path it must not write, and the embedded rules actively teach handover files.** `REPAIR_FORMAT` says only "Repair only the taken rows below. You may run tests and `make verify`; write a measured entry under `## Time used` in `plan.md`. Do not commit…" and `REPAIR_ANSWER` adds "Do not edit `findings.md`." (`scripts/stage2.py`, `REPAIR_FORMAT`, `REPAIR_ANSWER`; `REPAIR_FORMAT_FILE_TOOLS` likewise). `work_prompt` embeds the whole of `AGENTS.md` into every work prompt as "## Repository agent rules" (`scripts/stage2.py`, `work_prompt`), and `repair_prompt` builds the repair call on it with `prompts/04-implement.md`. `AGENTS.md` carries house rule 5 ("The handover is the file, not the chat. Session end → a file under `docs/journal/handover/`") and the session-continuity bullet ("Before ending or handing over a session, maintain a dated file under `docs/journal/handover/`"); `prompts/04-implement.md` mentions handovers twice — the *drop* stop ("the reason goes into the handover") and "If the session writes a handover, that line is the handover's 'Next step'." Nothing in the embedded set forbids writing one. The seed's incident (a Codex repair writing `docs/journal/handover/2026-10-15-research-swarm-loop-one-repair.md`, removed by hand in commit `560160d` on `explore/research-swarm`) is thereby explained by reachable text: the model is instructed to keep a handover file at session end and no sentence stops it.

**`implement` has the same gap.** `implement` (`scripts/stage2.py`, `implement`) uses the same `run_attempts`, the same `allowed = {findings.md}`, the same no-put-back-after-failed-checks and the same `git add -A` checkpoint. Its model is Claude Code with file tools only (`WORK_WRITE_TOOLS = "Read,Grep,Glob,Edit,Write"`, `run_work_model` — "One non-interactive Claude Code work call with file tools only"); the repair's Codex attempts additionally run tests and `make verify` in the CLI's configured `workspace-write` sandbox (`run_codex`). The exposure differs in degree, not in guard structure.

**The runner itself legitimately writes outside the change folder during implement and repair**, which any scope rule would have to leave alone: `prepare_derived` stamps `updated:` in changed held documents and renders `plans/INDEX.md` through `scripts/plans_registry.py --index`; `format_step`/`format_targets` ruff-rewrite changed `.py` under `FORMAT_DIRS = ("scripts/", "tests/")`; `run_attempts` inserts the stage-1 route block and routing evidence into `plan.md`; `mark_repaired_findings` writes taken rows' Status cells and stamps `findings.md`; `mark_repaired_record` marks the loop record, which lives outside the repository entirely (`record_dir` — `$XDG_STATE_HOME` else `~/.local/state`, then `coding-harness/stage2/<change>/loop.md`), beyond the file tools' reach; and `restore_baseline` performs the failed-call restore.

## Where it lives

- `scripts/stage2.py` — `REPAIR_ANSWER`, `REPAIR_FORMAT`, `REPAIR_FORMAT_FILE_TOOLS`, `DRAFT_RULES` (prompt constants, adjacent block); `NEW_ADR`; `changed_paths`, `ignored_snapshot`; `restore_baseline`, `put_back`, `draft_keep`, `put_back_lines`; `work_prompt`, `repair_prompt`, `implementation_prompt`; `run_attempts` (the shared loop, with the failed-call, failed-check and passing branches); `checkpoint`; `verify_attempt`, `prepare_derived`, `format_step`, `format_targets`; `check_repair_answer`, `mark_repaired_findings`, `mark_repaired_record`, `record_dir`; `implement`, `draft`, `repair`.
- `prompts/04-implement.md` — the embedded implement/repair contract, handover mentions in the drop stop and the last-line paragraph.
- `AGENTS.md` — house rule 5 and the session-continuity bullet, embedded into every work prompt.
- `docs/WORKFLOW.md` §4 — the "runner is the only way" sentence stating today's repair contract; "The draft" with the draft's put-back wording; "Repairing taken findings (repair)" carries no scope sentence today.
- `plans/changes/stage2-repair/spec.md` — criterion 20 (restore on a failed model process), criteria 21–22 (statuses and the one checkpoint commit) as the existing criteria nearest the topic.
- `tests/test_stage2.py` — the draft put-back tests and the repair restore tests (below).

## What tests cover today

The draft's put-back: `test_paths_outside_the_change_folder_are_put_back_and_named` (spec criterion 8), `test_the_put_back_names_every_path_beyond_the_bound` (2a's F-8), `test_an_edited_decisions_file_is_put_back` (criterion 9), `test_put_back_paths_are_named_in_full_however_long`, `test_a_put_back_path_with_a_newline_is_never_cut`, `test_a_failed_draft_call_is_put_back_and_recorded` — all in `tests/test_stage2.py`. The repair-side analogues that exist: `test_a_failed_repair_process_restores_the_baseline_without_a_further_attempt`, `test_a_failed_repair_process_removes_the_ignored_paths_it_created`, the moved-HEAD tests `test_codex_repair_that_moves_head_stops_without_rewriting` and `test_a_failed_codex_repair_call_that_moves_head_stops_without_rewriting`, and `test_a_passing_repair_ends_in_one_checkpoint_commit_with_its_statuses`. The only test plants named "stray" stand in the draft tests; no repair or implement test plants a file outside the change folder to assert what becomes of it.

## What is unclear

- The exact wording of bead coding-harness-t83 beyond the seed's quotation (the tracker was not read in this phase).
- Commit `560160d` on `explore/research-swarm` is recorded in the seed, not re-verified here (no shell in this phase's toolset).
- Which gates a stray handover file would trip, and whether one satisfying `templates/handover.md`'s schema would pass `make verify`, is not measured: `tests/test_feedback_channel.py` enumerates `docs/journal/handover/` through `project_handovers` and parametrizes several checks over it, while `tests/test_regelwerk.py` skips `docs/journal/` paths for one of its rules; the outcome for a concrete stray path is an open question, not a fact.
- Whether the Codex CLI additionally auto-reads an `AGENTS.md` at the repository root is not measurable from repository files; the explicit embedding through `work_prompt` is what the repository shows.

## Which files a change would have to touch

`scripts/stage2.py` (the guard path in `repair`/`implement`/`run_attempts`, a prompt constant beside `REPAIR_FORMAT`/`DRAFT_RULES`, and `checkpoint` if the refusal stands before the commit); `prompts/04-implement.md` (the embedded contract); `docs/WORKFLOW.md` §4 (the two passages named above); `tests/test_stage2.py` (new tests beside the draft put-back and repair restore tests, using the file's existing `World` harness); possibly `AGENTS.md`, since its embedded rules are how the handover instruction reaches the model.
