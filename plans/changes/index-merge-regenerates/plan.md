---
title: "Plan — index-merge-regenerates"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-njtm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, merge, generated-index]
---

# Plan — index-merge-regenerates

```text
For you:     Local merges regenerate the plans index; an on-request sync updates safe pull requests and reports conflicts, protected work and old pull requests.
Done when:   Offline Git tests prove merged-tree rendering and safe branch updates, the documented local command uses the same helper, and make verify is green.
Appetite:    4 hours of phase 4, repairs included; stop at the limit.
Not now:     GitHub server-side regeneration, scheduled jobs, installed skills, ordinary conflict resolution or merging pull requests into main.
Pre-mortem:  suppose it failed: most likely because the index was rendered before all merged inputs were available.
Starts unless you say stop.
```

## Files and steps

1. Create `tests/test_pr_sync.py`: offline regression fixtures with real Git
   repositories and a bare origin, a scripted `gh` stand-in, an injected UTC
   clock and renderer failures; add the ledger's tests before production code.
2. Create `scripts/pr_sync.py`: one CLI with `merge-main` and `sync`, sharing
   merge preparation, generation and refusal handling as described below.
3. Change `Makefile`: add phony `index` with recipe
   `python3 scripts/plans_registry.py --index`; preserve gate delegation.
4. Change `docs/WORKFLOW.md`: name both commands, their exclusions and
   day/night on-request invocation; remove only `make index` from its list
   of missing bootstrap targets and retain `make change` there.
5. Change `prompts/06-review.md`: tell the orchestrator to run `merge-main`
   before starting the read-only reviewer; do not let the reviewer merge.
6. Change `templates/agents-mergeable-prs.md`: name the shared local merge
   and sync commands and the server-side limitation in the portable rule.
7. Update `plans/changes/index-merge-regenerates/plan.md`: replace pending
   ledger entries as tests land; the runner maintains this folder's
   `findings.md`, metadata and measured time, and regenerates `plans/INDEX.md`.
   No design, ADR, other new file or deletion is planned.

## Implementation contract

- Commands: `python3 scripts/pr_sync.py merge-main --root .` prepares a
  local branch for hand merges or phase 6; `python3 scripts/pr_sync.py sync
  --root .` is called explicitly by the day/night orchestrator. Neither
  merges a pull request into main. Use argument arrays, never shell text
  assembled from branch names or pull-request data.
- Fetch origin, pin its main tip and the inspected branch head. Require an
  attached, clean local branch for `merge-main`; reject main itself and
  an in-progress merge/rebase. Local merge never pushes. `sync` discovers
  all open PRs with paginated `gh` reads, including number, URL, creation
  time, base, head SHA/repository/ref, title, labels and changed files.
- Classify before preparing a merge: skip decision-labelled or `decide(`
  titled PRs, paths covered by committed `stage2.RUNNER_HELD` or committed
  human-decided provenance prefixes, forks and non-main bases. Read policy
  from the invoking committed tree, not candidate PR code. Resolve file
  renames on both sides; absent or malformed metadata means an error.
- Inspect `git worktree list --porcelain -z`. For every checkout of the
  target branch, inspect tracked, untracked and staged dirt and commits
  absent from the fetched remote head; skip if dirty or unpushed. A clean
  checkout does not block a remote update; report that it must fast-forward.
  If a listed checkout cannot be inspected, skip rather than guessing clean.
- Shared merge engine: run `git merge-tree --write-tree -z` with the pinned
  heads, decode actual unmerged paths, and accept only a clean result or
  conflicts confined to `plans/INDEX.md`. Distinguish exit 1 conflicts from
  execution failure. Other conflicts produce a path report and no target
  update. Do not resolve ordinary conflicts, including modify/delete ones.
- Materialise the merged tree in a private scratch directory and use a
  temporary Git index for its replacement index blob. Validate readable
  frontmatter for every artefact the existing renderer consumes, and reject
  unresolved conflict markers in those inputs. Handle missing parents and
  index creation/deletion without reading either parent's output as truth.
- Run the invoking committed renderer against that merged data, using the
  scratch-mirror pattern of `stage2.trusted_registry`: committed `scripts/`,
  candidate plans data, private HOME/TMPDIR, no candidate program or hook
  execution, and no symlink escape or hardlink write into a checkout.
  Use the renderer as-is; do not add tracker-dependent `--check` to this
  generation path. The registry gate still measures the committed result.
- Insert the generated blob into the merge tree, preserving all other
  merged entries; create a two-parent commit with the PR head first and
  fetched main second. When main is already included and rendering is
  unchanged, return unchanged; when only regeneration is needed, make a
  normal single-parent repair commit. Renderer failure leaves target refs
  and user worktrees unchanged; remove only helper-owned temporary files.
- For local application, recheck branch, HEAD and clean state before a
  hook-disabled fast-forward to the prepared result; do not reset user
  work. For sync, re-read PR metadata/protections and remote head immediately
  before publishing, repeat local-worktree checks, and refuse a moved head.
  Push with an exact expected-old-head lease to only the inspected branch;
  candidate ancestry must contain that head. Never use an unconditional
  force or write main. A rejected push is an error, never success.
- Report one outcome per PR (updated, unchanged, conflict, protected,
  outside scope, error), with identity and relevant paths/reason. Print an
  independent overdue list, including skipped PRs, using UTC weekdays after
  creation through today, strictly greater than five. No holidays or auto
  closure. Exit 0 for a measured pass, 1 for conflicts/errors, 2 for invalid
  invocation or refused local merge; expected protected/outside skips alone
  are not errors. A discovery failure cannot yield an empty successful pass.
- Keep `scripts/stage2.py`, `scripts/plans_registry.py`, `decisions/`,
  `provenance.yaml`, `model-endpoints.yaml`, `.github/`, tracker and installed
  skills/configuration untouched. Prompt/template edits are orchestrator
  integration work if the implementation runner refuses those held paths;
  they remain required before declaring the package complete.

## Verification

Use real Git fixtures for union-of-inputs, clean-but-stale index, index-only
and mixed conflicts, idempotence, local refusal and remote races. The GitHub
stand-in must paginate and inject metadata/fetch/push failures; assert refs,
parent order, worktree bytes, reports and exit codes, not only call strings.
The gate regression plants a wrong index in an isolated valid fixture with
an explicit tracker-render fixture and checks BLOCK plus unchanged bytes.
Make-target proof runs both actual render paths on the same small fixture.
No live GitHub update or foreign-model call is a test.

```sh
.venv/bin/python3 -m pytest -q tests/test_pr_sync.py tests/test_ci.py tests/test_merge_guard.py
python3 scripts/check_interview_minimums.py --change index-merge-regenerates
python3 scripts/check_research_handoff.py --change index-merge-regenerates
python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_pr_sync.py::test_merge_renders_all_merged_inputs — either parent's added artefact is missing, even on a textually clean merge.
- 2: not yet written tests/test_pr_sync.py::test_index_only_conflict_is_regenerated — only-index conflict stops or markers are committed.
- 3: not yet written tests/test_pr_sync.py::test_other_conflicts_preserve_target — a non-index conflict advances the target or loses its diagnostic.
- 4: not yet written tests/test_pr_sync.py::test_make_index_uses_existing_generator — the target is absent or differs from the direct generator.
- 5: not yet written tests/test_pr_sync.py::test_sync_pushes_clean_and_index_only_merges — no push, lost PR ancestry or wrong merged render.
- 6: not yet written tests/test_pr_sync.py::test_sync_reports_conflicting_paths_without_push — an ordinary conflict is hidden or pushed.
- 7: not yet written tests/test_pr_sync.py::test_sync_skips_protected_work — decision, held-path, dirty or unpushed cases are updated or unreported.
- 8: not yet written tests/test_pr_sync.py::test_uncertain_sync_state_never_pushes — discovery, fetch, metadata, policy, worktree or merge failure permits a push or false success.
- 9: not yet written tests/test_pr_sync.py::test_moved_remote_head_is_preserved — a racing writer's head is overwritten or called a successful update.
- 10: not yet written tests/test_pr_sync.py::test_overdue_report_counts_weekdays — five/six-day boundary, weekend or protected-PR reporting differs.
- 11: not yet written tests/test_pr_sync.py::test_sync_does_not_update_forks_or_other_bases — an out-of-scope branch receives a push.
- 12: not yet written tests/test_pr_sync.py::test_repeated_merge_and_sync_are_unchanged — a second invocation changes a current head or pushes again.
- 13: not yet written tests/test_pr_sync.py::test_bad_merged_inputs_or_renderer_preserve_target — invalid frontmatter, markers or generator failure is published.
- 14: not a test — phase-6 review reads docs/WORKFLOW.md, prompts/06-review.md and templates/agents-mergeable-prs.md against both CLI help texts; a missing shared command or reviewer-side merge refutes it.
- 15: not yet written tests/test_pr_sync.py::test_registry_still_blocks_without_repair — a stale index passes or checking writes it.

## Time used
