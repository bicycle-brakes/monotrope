---
title: "Research — review-diff-4000"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.4
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# review diff 4000 — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1148 files, 5001 commits, 12 rules.

## Runner exploration — 2026-11-21

The exploration is complete — I have the full chain from the constant to its doctrine, tests, history and neighbours. Here is the research, ready to append to `plans/changes/review-diff-4000/research.md`.

---

## What exists today

**The bound and its choke point.** The review-loop prompt's diff is cut by `bounded_review_diff` at `REVIEW_DIFF_MAX_LINES = 2000` (`scripts/stage2.py`, constant at its `# A paid member reads the whole change, but not without end…` comment block, lines `def bounded_review_diff` through the constant; the function is `bounded_review_diff(diff: str) -> tuple[str, str | None]`). It splits on `"\n"` only — git's count, not `splitlines()` (`O191-4`, named in the function docstring) — returns the diff unchanged with a `None` note when it fits, and otherwise the first 2000 lines plus an in-prompt marker `## (the change diff was cut at … ; the rest is not carried)` and the note string `the change diff was cut at 2000 of <N> lines`. The comment block above the constant states the bound's current meaning after the pi-no-compaction change: a limit on cost and on how much one member can attend to (R-15 of the review-swarm review), **not** a guard against summaries — runner Pi settings disable compaction, so an oversized context now fails the member with `CallFailed` instead of ending in a summary it answers on.

**Where the paid diff comes from.** `change_diff(root)` (`scripts/stage2.py`, `def change_diff`) is the full `git diff` against the merge base with `origin/main`, plus untracked files via `diff --no-index /dev/null <path>`. It has no pathspec, no path ordering and no exclusion: documentation, `plans/`, and the change's own `findings.md` travel in Git's path order, `tests/` last. The paid branch of `_review_round` (`scripts/stage2.py`, `def _review_round`, else branch) calls `bounded_review_diff(change_diff(root))` and embeds the result in the prompt built from `prompts/04b-review-loop.md` with the read request before and after the diff.

**Where the free diff comes from, and the asymmetry.** The free stage reviews `free_diff(root)` (`scripts/stage2.py`, `def free_diff`), which pre-filters to source and test code only (`_free_candidate`: Python under `scripts/` and `tests/`, executable non-text files under `tools/`; documentation, plans and locks never pass) and applies its own bounds: `FREE_DIFF_MAX_LINES = 400` per file and `FREE_DIFF_MAX_TOTAL = 2000` total (`scripts/stage2.py`, constants above `REVIEW_DIFF_MAX_LINES`). The free branch of `_review_round` runs `bounded_review_diff` over that already-bounded input and merges both cut notes. Consequence: a raise of `REVIEW_DIFF_MAX_LINES` widens only the paid cut; the free stage keeps its 2000-line total and 400-line per-file bounds, and so does the availability probe (`free_probe_prompt`, `scripts/stage2.py`, which builds the real free-round prompt over the bounded free diff). No diff bound lives in `model-endpoints.yaml` — the file carries the `free_stage` rule and stage declarations only (grep for `bound`/`diff`/`lines` matches none of those as a limit).

**What a cut means in the record.** The cut note is written into the round record; a round over a cut diff never counts as clean (R-12, R-15; `docs/WORKFLOW.md` §4b, the sentence naming `REVIEW_DIFF_MAX_LINES` (2000 lines)). The record carries a `Cut rounds:` line (`CUT_ROUNDS_LINE` regex, `scripts/stage2.py`), the knowledge survives a `release-loop` (`test_a_cut_round_stays_cut_after_the_release`, `tests/test_stage2.py`), and the free diff reports its own cuts as notes, not as cut rounds (`test_free_diff_reports_its_own_cut`, `tests/test_stage2.py`). Since the merged ADR 0021 amendment (PR #422), a consumed ladder above a cut diff routes to `next: review <change>`, because phase 6 reads the complete diff in the worktree without the cut (`plans/changes/adr-0021-consumed-ladder/decisions.md`, the Option-1 answer naming `REVIEW_DIFF_MAX_LINES` and the "2,000-line cut").

**Overflow behavior today.** Every runner-written Pi settings file is `{"retry": {"enabled": false}, "compaction": {"enabled": false}}` (`PI_AGENT_SETTINGS`, `scripts/stage2.py`; criterion 1 of `plans/changes/archive/2026-11-16-pi-no-compaction/spec.md`). A context overflow therefore ends as exit 1 and `CallFailed` — a failed member, never an answer over a summary (criterion 2 of the same spec; pinned by `test_real_context_overflow_fails_without_compaction`, `tests/test_pi_contract.py`). `REVIEWER_MINUTES = 45` (`scripts/stage2.py`) is the separate round deadline, raised from 30 by the maintainer on 2026-10-24 per its comment.

**The measured effect of the cut.** `docs/research/2026-10-29-review-diff-cut.md` (bead coding-harness-ut8q): Git path order filled more than half the 2000 lines with `docs/`, `plans/` and the growing `findings.md` before any code on all three measured changes; no reviewer in any round saw a line of the test files; findings concentrated on the change's own prose, predecessors' findings were repeated, and test-strength findings were impossible. `docs/research/2026-11-03-pi-context-overflow.md` measured the token side: a diff line of this repository averages about 86 characters, so 2000 lines are about 44,000 tokens; the smallest admitted model window was 256,000 (2026-11-03, twelve reachable models, probe capped at 300,000), and it recommends keeping the bound as a cost/attention guard and deriving no per-model bound from `contextWindow` — with compaction off a wrong guess costs one failed member, not a wrong clean round. The same note records the maintainer's 2026-10-26 decision as "at most four parts of 2000 lines, each reviewed in full" — a ceiling above which even splitting would not help (`plans/changes/archive/2026-11-06-research-swarm/findings.md`, the 2026-10-26 entry naming bead coding-harness-ut8q, where a 31,720-line diff was released without a clean round as a one-time exception). That split exists only as the recorded decision: no splitting mechanism is in the runner (grep for `four parts`/`DIFF_PARTS`/`split_review` in `scripts/` finds nothing; `bounded_review_diff` cuts, it never splits).

**The trigger for this change.** The lane table of `docs/journal/handover/2026-11-20-day-run.md` shows mandatory-spec-review (bead coding-harness-ttic) with "its diff is cut at 2000 of about 4100 lines", and the end-of-day addendum parks that lane after ladder member `qwen3.7-plus` hit the 45-minute round limit twice (bead coding-harness-8kht asks why, and whether a timed-out ladder member counts as consumed). A diff of about 4100 lines is under a 4000-line bound by only ~100; whether that is the intended figure is the maintainer's to confirm, not read from any artifact here.

**Origin of the 2000 value.** The bound was introduced because Pi auto-compacted an oversized context instead of failing (handover `docs/journal/handover/2026-10-23-night-run.md`, the entry creating bead coding-harness-ut8q, which cites the pinned Pi compaction doc); R-15 is the review-swarm-review row about it (referenced in `docs/research/2026-10-20-night-run-plan.md`). The pi-no-compaction change (archived, PR per heartbeat handover) removed that reason and explicitly scoped the bound out: its spec's non-goals name "Changing `REVIEW_DIFF_MAX_LINES = 2000`, existing splitting/cut handling, or deriving limits from model context windows; the bound remains a cost and attention limit", and its Definition of Done requires the comment above the constant to explain the retained bound without claiming compaction is still enabled (`plans/changes/archive/2026-11-16-pi-no-compaction/spec.md`, Non-goals and Definition of Done).

## Where it lives

- Constant and comment: `scripts/stage2.py`, `REVIEW_DIFF_MAX_LINES = 2000` with its comment block (compaction-off statement, R-15, the pinned-Pi evidence test name, the historical research note).
- Cut function: `scripts/stage2.py`, `bounded_review_diff`; per-file and free-total bounds: `FREE_DIFF_MAX_LINES = 400`, `FREE_DIFF_MAX_TOTAL = 2000`; free filter: `_free_candidate`, `FREE_DIFF_TEXT_SUFFIXES`, `FREE_DIFF_SKIP_PARTS`.
- Call sites: `scripts/stage2.py`, `_review_round` (free branch and paid branch), `free_probe_prompt`.
- Doctrine: `docs/WORKFLOW.md` §4b, the sentence naming `REVIEW_DIFF_MAX_LINES` (2000 lines); `docs/how-it-works.md`, "Runner details" bullet "A prompt carries at most 2,000 diff lines…" including the free per-file 400 sentence.
- Tests: `tests/test_stage2.py` — `test_an_oversized_diff_reaches_the_paid_prompt_cut_and_the_record_says_so` (monkeypatches the constant), `test_a_cut_round_stays_cut_after_the_release` (same), `test_the_review_diff_is_split_on_newlines_only` (reads the constant), `test_free_diff_reports_its_own_cut` (free bounds); `tests/test_pi_contract.py` — `test_real_context_overflow_fails_without_compaction`.
- Historical records that carry the figure but are records, not doctrine: `docs/research/2026-10-29-review-diff-cut.md`, `docs/research/2026-11-03-pi-context-overflow.md`, handovers `2026-10-21-night-run-eleventh.md`, `2026-10-23-night-run.md`, `2026-10-25-cloud-runner-fixes.md`, `2026-10-29-three-lane-night.md`, `2026-11-06-heartbeat-night.md`, `2026-11-20-day-run.md`; the decision wording in `plans/changes/adr-0021-consumed-ladder/decisions.md`.
- `prompts/04b-review-loop.md` carries no line-count figure — read whole; nothing in it states 2000.

## Neighbours (for the `neighbours:` header and topic 5)

Active change folders in this worktree: `plans/changes/adr-0021-consumed-ladder/` (merged as PR #422 per the branch history; folder not yet archived), `plans/changes/review-loop-deep-a/` (bounded, `implementation_status: partial`; its spec owns the cut-round-is-never-clean record behavior). Archived: `plans/changes/archive/2026-11-16-pi-no-compaction/` (the change that kept the bound and rewrote its comment), `plans/changes/archive/2026-11-06-plan-held-paths/` (its decisions record the refusal of review-diff-order implement attempt 2 over the held prompt path), `plans/changes/archive/2026-11-06-research-swarm/` (its findings carry the 2026-10-26 four-parts decision and the 31,720-line exception). Research notes beside those folders: `docs/research/2026-10-29-review-diff-cut.md`, `docs/research/2026-11-03-pi-context-overflow.md`. The mandatory-spec-review change folder (bead coding-harness-ttic) is not found in this worktree — it lives in its own lane worktree, so its spec cannot be read from here.

## What is unclear about it

- The bead coding-harness-mwzv.4 description itself was not read: the tracker is the Dolt database under `.beads/`, which these read-only file tools cannot open; the change-folder opening commit message and `plans/INDEX.md` row are the only readable statements of intent. Whether the intended value is exactly 4000, and whether the change also wants path ordering, exclusions or a split, is not written in any artifact of this worktree.
- Whether the 2026-10-26 "at most four parts of 2000 lines" ceiling still stands as the maintainer's word, or is superseded by this change, is nowhere stated outside the two 2026-11-03 citations.
- Whether a 4000-line prompt plus tool reads still fits every currently admitted member's real window is not measured: the 256,000-token smallest window and the 86-characters-per-line average come from 2026-11-03 and 2026-10-26 measurements; the current catalog was not re-probed in this phase, and the tool reads, not the diff, decide when a member overflows (the 2026-11-03 note's own warning). With compaction off the failure mode is a failed member (`CallFailed`), never a wrong clean round.
- The interaction with the 45-minute round deadline is open: the parked lane hit that limit twice (bead coding-harness-8kht, unanswered); a doubling of diff size on that path is unmeasured.
- The fate of review-diff-order (bead coding-harness-ut8q): its change folder is not found anywhere under `plans/` (active or archive), and the 2026-11-16 guard-test findings show the tracker holding ut8q as `in_progress` with no artefact. That the tree today has no path ordering or exclusion in `change_diff` is a statement about this tree; what the tracker says about ut8q today was not read.

## Which files a change would have to touch

- `scripts/stage2.py` — the `REVIEW_DIFF_MAX_LINES` constant and its comment block; no other code site hardcodes 2000 (grep over `scripts/` shows the constant is the single source; `bounded_review_diff` and both call sites read it).
- `docs/WORKFLOW.md` — the §4b sentence naming the bound with "(2000 lines)".
- `docs/how-it-works.md` — the "Runner details" bullet stating "at most 2,000 diff lines" and the free per-file 400 sentence beside it.
- `tests/test_stage2.py` — the three bound-related tests read or monkeypatch the constant, so they move with a value change without breaking; a change adding new behavior would add its own tests there (the file is the established home).
- Nothing in `prompts/04b-review-loop.md` or `model-endpoints.yaml` carries the figure — read, not assumed.
- Historical research notes and handovers are records of their cut-off dates and are not expected to move; the decision text in `plans/changes/adr-0021-consumed-ladder/decisions.md` mentions the "2,000-line cut" as part of a merged decision record — whether that wording is updated or left as history is not decided by anything readable here.
