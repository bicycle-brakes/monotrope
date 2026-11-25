---
title: "Research — frontmatter-batch-log"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.21
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-25", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
neighbours: []
---

# frontmatter batch log — Research

## Topic (bead coding-harness-bxxt.21, copied by the orchestrator 2026-11-25)

Class: bounded.

Why: scripts/check_frontmatter_current.py:180-189 runs git log -1 --no-
merges per clean held file (184); the external analysis measured the gate at
6-16 s (count of ~893 files not re-counted). What: one batched git log --
name-only pass. Related: coding-harness-y6h0, coding-harness-5v6t.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp, night run 2026-11-24-a), from an external verify-speed analysis.



PARENT
↑ ○ coding-harness-bxxt: (EPIC) Verify speed and machine load P1

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu) · leak check clean over 1202 files, 5770 commits, 12 rules.

## Runner exploration — 2026-11-25

Research for `frontmatter-batch-log`, ready to append to `research.md`. I did not edit the file: the explorer role is read-only.

## What exists today

**The per-file date lookup.** `scripts/check_frontmatter_current.py`, function `reference_dates(root, files, today)`, gives each held file the date its `updated:` must reach. It first builds a "dirty" set from two calls: `git diff --name-only --no-renames --relative -z HEAD` and `git ls-files -z --others --exclude-standard`. A dirty file gets today's date with the label `uncommitted`. Every other file gets its own `git log` call, `_git(root, "log", "-1", "--no-merges", "--format=%cs %h", "--", f)`, which returns the committer date (`%cs`) and short hash of the newest non-merge commit that touched the path. A failed or empty answer raises `CannotMeasure` and the run exits 3. The bead's citation of lines 180–189 and line 184 matches this loop.

**Where the result goes.** `findings(root, today, utc_today)` calls `held_files(root)` and then `reference_dates(...)`. It uses only the date from each `refs[f]` entry for the `STALE` comparison. The short hash is used only in the detail text of a stale finding: "its last change {ref} ({woher})". `run()` calls `held_files(root)` a second time, to count the held documents for its green message. That second call is a separate `ls-files` and map read.

**Preconditions already enforced.** `preflight(root)` refuses a non-work-tree, a repository with no commit, and a shallow clone (`git rev-parse --is-shallow-repository`). So the history that a batch log would read is always complete when the code runs.

**The gate.** `decisions/gates.yaml` (line 145) runs the script as the `frontmatter-current` gate, with `.github/workflows/ci.yml` (line 107) also running it without `--root`. `docs/governance/gate-catalog.md` (line 64) lists it as a verify-stage gate, `block`, cost "seconds". Its design came from the archived change `plans/changes/archive/2026-09-29-frontmatter-current/` (`spec.md`, `plan.md`, `findings.md`).

**Tests.** `tests/test_frontmatter_current.py` exists (confirmed by Glob). I did not open it, so I do not know which of its tests pin `reference_dates`' output format or its use of the short hash.

**Known subtleties recorded in the archive.** `plans/changes/archive/2026-09-29-frontmatter-current/plan.md` (section "Two details of `reference_dates`", item 4) says the `git diff` runs with `--no-renames --relative`, so a staged move shows as an added new path, and paths are relative to `--root`. `findings.md`, row F-6 (MINOR, fixed in 751c105), records that the `--relative` flag has no test: removing it in a scratch copy leaves every test green, because no test points `--root` at a subdirectory of a repository.

**Related beads and their traces.**
- `coding-harness-y6h0` (merging main forces `updated:` stamps on other changes' documents) appears in `docs/journal/handover/2026-11-23-morning-run-2026-11-21-a.md`, line 35, as a new bead. It is about stamp churn, not the speed of the check.
- `coding-harness-5v6t` was not found in the repository: no hit in a repository-wide search, nor in `plans/changes/ontology-relation-layer/research.md`. Its content is not in the tree.
- `coding-harness-bxxt` (the epic) and `.21` (this change) are in `plans/INDEX.md` (line 620) and in this change's own file.

## What is unclear

- **The 6–16 s figure is not measured here.** It comes from the external analysis cited in the bead topic. I ran no timing and no `git log` command, so I can say nothing about the real cost of the 893 per-file calls versus one batch call.
- **Equivalence of the batch form is unverified.** Per file, `git log -1 --no-merges -- f` follows the path with the default history simplification. A single `git log --no-merges --name-only` over all of history yields, for each path, the first commit that lists it. Whether the two agree on every held file, including renames (the batch output by default follows `diff.renames`, the per-file call sees a rename as an add of the new path) and merge-related simplification, is not established by reading.
- **Path base in the batch output.** `git log` prints paths relative to the repository top, while the per-file call takes its path relative to `-C root`. They differ when `--root` is a subdirectory of the repository. The archive records that `--relative` was needed for `git diff`, and F-6 says no test covers that case. Whether the batch form needs the same flag on `git log` is open. CI and the default run use the repository root, so the difference would only appear under `--root` in tests.
- **Stale-date reporting.** The hash in each `STALE` detail comes from `%h` of the same commit. A batch must keep that string identical, or the output changes for every stale file.
- **Error path.** Today a single file with no commit raises `CannotMeasure` for that file (`git log cannot date <file>`). Whether a batch should keep that per-file message or report one aggregate error is not settled in the sources read.

## Files a change would have to touch

- `scripts/check_frontmatter_current.py`: `reference_dates` (the per-file `git log` loop, which becomes one batched log, plus the dirty set unchanged), and possibly `run()` for the second `held_files` call.
- `tests/test_frontmatter_current.py`: the tests that pin the `(date, hash)` output and the exit-3 paths, plus a test that runs the batch against a repository where a file is renamed or a merge touches it. The `--relative` gap (F-6) lies in the same function.
- `decisions/gates.yaml`, `.github/workflows/ci.yml`, `docs/governance/gate-catalog.md`: no change expected if the command line and verdicts stay the same. Not read in full.

## Neighbours (for the runner's header)

The archived `plans/changes/archive/2026-09-29-frontmatter-current/spec.md` is the spec that defined this check. It is the one neighbour I know for certain and the runner can take it from here.
