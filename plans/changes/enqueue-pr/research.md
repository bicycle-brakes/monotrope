---
title: "Research — enqueue-pr"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-va1l
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-25", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
neighbours: []
---

# enqueue pr — Research

## Topic (bead coding-harness-va1l)

Class: bounded. Maintainer grant 2026-11-25 (AGENTS.md, PR #459): the orchestrator admits a pull request to the merge queue itself once phase 6 is clean, make verify is green on its head and its last commit carries Closes-Bead. Today the grant is prose and gh pr merge stays 'ask' in .claude/settings.json and in Antigravity, so an unattended run cannot use it. Build scripts/enqueue_pr.py <number>: refuse unless (1) the PR targets main and is open, (2) the change's newest phase-6 table in plans/changes/<change>/findings.md has no open row (or reports no finding), (3) every required check on the PR head is SUCCESS, (4) the head commit carries a Closes-Bead trailer naming an existing bead; then run gh pr merge <number> --merge (admission to the merge queue only, never --admin, never a direct merge). Every refusal names the failing condition. Harness-neutral: Claude Code, Codex and Antigravity allow only this script; a direct gh pr merge stays ask (deny at night). Needed before the 72-hour Antigravity run.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29; bounded change · leak check clean over 1234 files, 5894 commits, 12 rules.

## Runner exploration — 2026-11-25

## Research for enqueue-pr (bead coding-harness-va1l, class bounded)

Source of this text: read-only search of the worktree at `/Users/mikypiky/coding-harness/.claude/worktrees/enqueue-pr`, with Grep, Glob and Read. Nothing was run and nothing was written. The bead text itself was not read (no tracker access in this phase). The topic is taken as the topic section of `plans/changes/enqueue-pr/research.md` states it.

### What exists today

**The merge path, as written down.**
- `prompts/07-commit.md`, section "The merge": steps 1 to 8. The maintainer asks in their own message (step 1). The agent restates the decision and posts it as a PR comment (step 3). It never uses `--admin` (step 4). It runs `gh pr merge <n> --merge --match-head-commit <sha>` (step 5). Step 7 says that with the merge queue active the same command admits the PR to the queue at its exact head, and that "queued is not merged". The PR counts as merged only once `gh pr view <n> --json state,mergeCommit` shows `MERGED`.
- `docs/WORKFLOW.md`, section "Merging a series, one at a time": admission is reported as queued until the PR shows `MERGED`. The maintainer's request, the restatement, the exact head and the ban on `--admin` are stated to hold as before.
- `AGENTS.md`, house rule 8 and the "Pull requests stay mergeable" bullet: merge through the merge queue at the exact head. Merge only when the maintainer asks, after the restatement.
- `docs/journal/handover/2026-10-31-night-and-day-run.md` reports that the merge queue has been on for `main` since 2026-10-31 07:00 UTC, and that a plain `gh pr merge --auto --merge` returned "The merge strategy for main is set by the merge queue".

**Ask rules that stop an agent before a merge.**
- `.claude/settings.json`, `permissions.ask`: `Bash(gh pr merge *)`, `Bash(gh -* pr merge*)`, `Bash(gh pr -* merge *)`, the REST and GraphQL merge and enqueue spellings, `Bash(gh alias set *)`, `Bash(git push *main*)`, `mcp__*__merge_pull_request`. No `allow` rule for any enqueue script exists.
- `scripts/merge_guard.py`, `MERGE_ASK_RULES`, `covers()` and `problems()`: lists the ask rules and their sample calls. `problems()` reports any `allow` or `deny` rule that covers a merge sample. `tests/test_merge_guard.py` compares the settings file with this list.
- `templates/repo-settings.md` and `tests/test_repo_settings.py`: the required check is named `verify` (`REQUIRED_CHECK`). The test checks `required_status_checks` rules and `merge_queue` rules.

**Declaring a closure.**
- `prompts/07-commit.md`: a commit that finishes a work item carries `Closes-Bead: <id>`.
- `scripts/close_merged_beads.py`, `collect_declarations()` and `raw_trailers()`: reads the trailer with `git interpret-trailers --parse` under isolated config. It walks every commit reachable from a pinned sha. `load_state()` reads the tracker through `bead_render.render_pfad()` and validates it. Bead status is the field `status`. Its `close` call goes through the pinned `tools/bd`. The Makefile target is `close-merged`.
- This reader works on merged history from `origin/main`. Nothing in the repository reads a trailer from a PR head.

**Phase-6 findings.**
- `plans/changes/<name>/findings.md` holds the phase-6 record in two shapes. Shape A is a heading `## Phase 6 — <reviewer>, <date>` followed by a line `Phase 6 verdict: …`, with prose such as "Codex reported no finding." Several files carry several such headings, one per round (for example `plans/changes/archive/2026-10-08-stage2-runs-count/findings.md`).
- Shape B is a loop table headed `## Phase 4b — loop rows`, with columns `ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6`. The `Phase 6` column holds `agree` or `disagree` text. Status values seen: `fixed — …` and `rejected — an accepted limit: …`.
- The AGENTS.md phase-6 table gate says: no open BLOCKER, and `[DIVERGENT]` counts as BLOCKER.

**Checks on a PR.**
- `scripts/pr_sync.py`: `run_gh()` calls `gh` through an injectable `--gh` argument with `GH_SECONDS = 120`. `VIEW_FIELDS` is `state,number,url,title,createdAt,baseRefName,headRefName,headRefOid,isCrossRepository,labels,files,changedFiles`. It does not include `statusCheckRollup`, `mergeable` or `mergeStateStatus`.
- No script in `scripts/` reads `statusCheckRollup` or `gh pr checks` today.
- `docs/WORKFLOW.md` (section 3) says a pending check has no conclusion yet, and an empty or pending rollup is not green.

**Existing name.** Nothing called `enqueue_pr` exists. `Glob` on `scripts/*merge*` returns `scripts/close_merged_beads.py` and `scripts/merge_guard.py` only.

### Where it lives

| Concern | Path |
|---|---|
| Merge procedure, steps 1–8 | `prompts/07-commit.md` (section "The merge") |
| Queue admission, pending-check rule | `docs/WORKFLOW.md` §3 "Merging a series, one at a time" |
| Governing rules | `AGENTS.md` house rules 4, 8, 9; "Pull requests stay mergeable" |
| Ask rules and their test | `.claude/settings.json`, `scripts/merge_guard.py`, `tests/test_merge_guard.py` |
| Closure from trailer | `scripts/close_merged_beads.py`, Makefile target `close-merged` |
| Phase-6 records | `plans/changes/<name>/findings.md` (shapes A and B above) |
| Required check `verify` | `templates/repo-settings.md`, `tests/test_repo_settings.py`, `scripts/ci_gates.py` |
| `gh` wrapper pattern | `scripts/pr_sync.py` (`run_gh`, `VIEW_FIELDS`) |
| Merge-queue history | `plans/changes/archive/2026-11-06-merge-queue/spec.md` (criteria 7 and 9); its findings |
| Decision-PR merge command | `.github/PULL_REQUEST_TEMPLATE/decision.md` (merge command with `--match-head-commit`) |

### What is unclear

1. **The grant is not in this checkout.** The topic cites a maintainer grant of 2026-11-25 in `AGENTS.md` (PR #459). A search of this worktree's `AGENTS.md` for `2026-11-25`, `#459` and `grant` finds nothing. The line that matched `grant` is the stage-2 paragraph, not a grant. The grant is therefore either on another branch or not yet merged. Its wording was not read.
2. **Conflict with the written merge rule.** `prompts/07-commit.md` step 1 and `AGENTS.md` house rule 8 say the agent merges only when the maintainer asks in their own message. The topic makes admission by the orchestrator, without that message, a standing grant. The text that authorises it is not in this checkout (see 1).
3. **Command shape.** The topic gives `gh pr merge <number> --merge`. Every written merge command in the repository (`prompts/07-commit.md` step 5, `docs/WORKFLOW.md`, the decision PR template) carries `--match-head-commit <sha>`. Whether the script must carry it is not stated in the topic.
4. **Phase-6 "newest table".** Files have shape A (prose verdict, possibly several rounds) and shape B (a `Phase 6` column in a loop table). No file carries a separate phase-6 table. "Newest" is not defined in terms of heading order or date. An "open row" is not defined either: the status vocabulary seen is `fixed` and `rejected`, with no `open` value found.
5. **Required checks.** The topic says "every required check on the PR head is SUCCESS". The required check that the repository declares is `verify`. No reader of the ruleset's full list of required checks exists in the scripts. Whether to read the ruleset or the PR's rollup is not decided in the sources.
6. **Decision PRs.** House rule 8 says a decision PR takes effect when the maintainer merges it. The topic's conditions do not say whether a PR with the `decision` label is refused. Not stated in the sources.
7. **Antigravity.** The topic says `gh pr merge` stays `ask` "in Antigravity". No Antigravity configuration was found in the repository. Files that mention Antigravity: `tools/omnigent/README.md`, `plans/changes/archive/2026-09-29-omnigent-deny-layers/spec.md` and `decisions.md`, `plans/changes/adr-0021-consumed-ladder/spec.md` and `decisions.md`, and three handovers from 2026-11-21. These were not read. The Antigravity configuration is therefore not located here.
8. **Possibly related, not read.** `plans/changes/archive/2026-11-16-night-stall-guard/` matched the word "enqueue" in the repository-wide search. Its context was not read.

### Which files a change would have to touch

- `scripts/enqueue_pr.py`: new. No file of that name exists.
- A test file for it (for example `tests/test_enqueue_pr.py`): new.
- `.claude/settings.json`: an `allow` entry for the script, if the topic's "allow only this script" is to hold in Claude Code. Any such entry is checked by `scripts/merge_guard.py` `problems()`; by `covers()` as written, an allow pattern for `python3 scripts/enqueue_pr.py …` covers none of the merge samples.
- `tests/test_merge_guard.py`: runs against the settings file, so it is affected by any change to `.claude/settings.json`.
- `prompts/07-commit.md` (section "The merge") and `docs/WORKFLOW.md` (section 3, "Merging a series"): the procedure for an orchestrator-admitted PR is described there, and both currently describe a maintainer request as step 1.
- `AGENTS.md`: house rule 8 and the "Pull requests stay mergeable" bullet name the merge procedure.
- `Makefile`: if a make target is added. The `close-merged` target is the precedent, and its help text lives in the Makefile.
- `plans/INDEX.md`: regenerated by `scripts/plans_registry.py --index` after a header edit.

### Not read

- `tests/test_close_merged_beads.py` (it contains 61 matches for the terms searched; its stubs for `gh` and `bd` were not read)
- `scripts/bead_render.py` beyond the function `render_pfad`
- the `Closes-Bead` trailer rules in `tests/test_beads_start.py`
- the Antigravity configuration (not located in the repository)
- `plans/changes/archive/2026-11-16-night-stall-guard/`
- the bead `coding-harness-va1l` and the AGENTS.md grant of PR #459 (not in this checkout)

### Neighbours (candidates found, for the runner's header)

- `plans/changes/archive/2026-11-06-merge-queue/spec.md` — the merge procedure and queue admission
- `plans/changes/archive/2026-10-08-rb-g7-merge-freshness/spec.md` — the freshness requirement the queue replaces
- `plans/changes/harness-decide-adr/` — decision PRs and `merge_guard.py` (its `plan.md` and `findings.md` match "merge")
