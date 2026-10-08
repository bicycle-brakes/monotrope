---
title: "Session handover — RB-G7 merged, Codex takes over the MiMo watch, 2026-10-08"
category: handover
created: 2026-10-08
updated: 2026-10-08
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-08"
tags: [handover, codex-takeover, rb-g7, stage2-mimo]
target_ref: "902c0f7"
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

Written for Codex, which takes over because the maintainer's Claude budget
runs out (bead coding-harness-amp — Codex takes over when the Claude budget is
spent).

## Where we are

On 2026-10-08 the maintainer merged every open pull request of the night
(#91–#97) and the RB-G7 decision (#99, merge `902c0f7`): rule RB-G7 ("the
merge state is checked, not the branch head") is now held by tests instead of
a valve that would have turned every run red on 2026-10-31, and the live
branch ruleset of `main` requires branches to be up to date before merging.
In parallel an OpenCode session (model MiMo-V2.6-Pro) works the change
`stage2-mimo` (bead coding-harness-ymx — stage-2 reviews through OpenCode Go)
on `feat/stage2-mimo`; this session tracked and checked every step of it. At
11:48 that session was applying a decision the maintainer changed today (see
Decisions), with 8 uncommitted paths in its worktree.

## Next step

Keep watching the MiMo session: when `origin/feat/stage2-mimo` moves past
`dedecf5`, check out the new commit in a throwaway worktree, run `make venv`
and `make verify`, and confirm that `run_codex` and `thread_id` in
`scripts/stage2.py` are back and byte-identical to `origin/main`, that
`spec-review` and `review` start Codex as on `main`, and that only
`review-loop` uses the OpenCode Go ladder. Report the verdict to the
maintainer in German, short, result first.

## Needed from the maintainer

Nothing right now. Later: whether MiMo may run the probe (step 4, three live
OpenCode Go calls that spend subscription credit, approved on 2026-10-07)
once its decision repair is green — recommended yes, only the 4b rungs.

## Decisions and preferences

- **Review routes (maintainer, 2026-10-08, supersedes 2026-10-07):** the
  OpenCode Go ladder (DeepSeek V4.1 Flash → MiMo-V2.6-Flash → MiMo-V2.6-Pro)
  runs only the 4b review loop. Phases 2a and 6 stay with Codex; phase 6
  resumes the 2a session. Reason: Codex's phase 6 found two real BLOCKERs in
  rb-g7-merge-freshness after the GLM loop had passed it, as on every change
  of the night run. Recorded as a comment on bead coding-harness-ymx; the
  MiMo session was told to add a dated addendum to
  `plans/changes/stage2-mimo/decisions.md`.
- **RB-G7 (merged in #99):** option 2 — merge ref checked by
  `tests/test_ci.py`, up-to-date branches by `tests/test_repo_settings.py`;
  no ADR (the maintainer said "nein" to the shown proposal); rule set 5.0.0.
- **Merging now needs an up-to-date branch.** Before any merge:
  `gh pr update-branch <n>`, wait for green CI, then merge
  (`prompts/07-commit.md`, merge step 7). Merge only when the maintainer asks
  in the conversation; for a decision PR restate the decision block first,
  as a PR comment too, and merge with `--match-head-commit <full sha>`.
- The MiMo session writes no tracker (maintainer, 2026-10-08). After this
  session ends, the Codex session is the tracker writer.

## What the MiMo watch found (2026-10-08, times local)

The MiMo session got a seven-step instruction at about 09:25 (checkpoint,
repair two red tests, merge `main`, probe, 4b, 6, decision PR; stop after
step 3 and step 7). Verdict so far: good diagnoses, keeps spec, plan and code
consistent and records every deviation as a `[DETAIL]`; it did not notice on
its own that its merge broke the session verb's tests.

1. 09:32 — checkpoint `77f78aa`, all 14 uncommitted paths of the failed
   implement run, pushed. Commit unsigned (the maintainer's Claude Code
   commits are signed; GitHub does not require it).
2. 10:08 — `1f7c298`, the two red review-loop tests repaired on the test side
   (a stale read; a regex that never matched), reasons in `plan.md`. It also
   raised the kit exemption cap (`scripts/kit/probe.py`, 33 → 36) for new
   repo-only tests, with reasons. Re-run by this session: 272 passed.
3. 10:23 — merge of `origin/main` (`52a8f5a`), then `dedecf5` at 11:08.
   The merge was red at first: 7 failures in `tests/test_stage2_session.py`,
   because the implement run had moved the `failed:` line to standard output
   (main prints it to standard error) and one case assumed `opencode-go` is
   undeclared. Repaired after this session's hint. Audited by this session
   in a throwaway worktree at `dedecf5`: `main` fully contained,
   `make verify` green (1252 passed, 16 skipped), the #92 repair code
   byte-identical, the session verb wired. `run_codex` and `thread_id` were
   removed by design — they must come back under the new route decision.
4. Since about 11:40 — the route-decision repair (uncommitted at 11:48:
   `AGENTS.md`, `docs/WORKFLOW.md`, `model-endpoints.yaml`, `decisions.md`,
   `spec.md`, `prompts/02a-spec-review.md`, `prompts/06-review.md`,
   `scripts/stage2.py`).

`main` moved to `902c0f7` after `dedecf5`; the MiMo branch must merge `main`
again (RB-G7 touched `tests/test_ci.py`, `tests/test_repo_settings.py`,
`docs/governance/`, `prompts/07-commit.md`) and, under the new ruleset, be
up to date before its pull request merges.

## Open work and blockers

Task status is in Beads. Queue, one at a time:

1. MiMo change (coding-harness-ymx): route repair → merge `main` → probe →
   4b → 6 (Codex) → decision PR. Watched, not done, by the takeover session.
2. Runner regenerates derived files (coding-harness-mfv, P1): seen again
   today — `stage2.py review-loop` created `findings.md` for
   rb-g7-merge-freshness and left `plans/INDEX.md` stale, so `make verify`
   was red until the index was regenerated by hand.
3. Test-holding gap (coding-harness-909): options merged in #96, waits for
   the maintainer's choice. Stage-2 measurements (coding-harness-kw0):
   partial evidence in #95.

## Working state and parallel-session boundary

- `main` at `902c0f7` (2026-10-08). Open pull requests: #98 (Kubernetes
  research, not from this session, not read).
- `.claude/worktrees/stage2-mimo` (branch `feat/stage2-mimo`, pushed head
  `dedecf5`) belongs to the OpenCode MiMo session — do not edit it; check its
  commits from a separate throwaway worktree.
- `.claude/worktrees/rb-g7-merge-freshness` is merged and can be removed.
- Tracker this session: closed coding-harness-zci (#92), coding-harness-cff
  (#93), coding-harness-34z (#99); comments on coding-harness-amp, -909,
  -kw0, -ymx; pushed with `tools/bd dolt push`.
- The watch log of this session lived in its scratchpad; its points are
  copied above, nothing else is in it.

## Validation

- `make verify` green on rb-g7-merge-freshness at `6d0857b` (1248 passed,
  16 skipped, writer gate `ruleset` 90 passed, 2026-10-08); hosted CI green on
  #99 before the merge.
- `make verify` green on `feat/stage2-mimo` at `dedecf5` (1252 passed,
  16 skipped), run by this session in a throwaway worktree, 2026-10-08.
- The live ruleset: `gh api repos/MPAdesso/coding-harness/rules/branches/main`
  showed `strict_required_status_checks_policy: true` (2026-10-08 09:48).
- Not run: the MiMo session's uncommitted route repair; the `stage2.py
  session` Terminal smoke from #91.
