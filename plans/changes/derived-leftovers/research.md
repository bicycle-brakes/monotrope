---
title: "Research — derived-leftovers"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-b5w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, runner, derived-files, retry]
---

# A failed run's derived writes block the next run — Research

Phase 1 for bead coding-harness-b5w, read on 2026-10-14 against `origin/main`
at `3199a28` and the unmerged branch `origin/feat/codex-repairs` (pull
request #138) at `135cb8e`. Exploration only, during the night run; the
questions below wait for the maintainer.

## Result first

- After a run that fails its post-run checks, the worktree holds three kinds
  of change: the model's edits (kept on purpose), the runner's own writes to
  `findings.md` (allowed), and the runner's other writes — the rendered
  `plans/INDEX.md`, `updated:` stamps, ruff's formatting and, on the stage-1
  route, a "Runner route" block in `plan.md`. Only `findings.md` is exempt
  from the next run's pre-existing-change refusal.
- The attempt block in `findings.md` lists only the files the **model**
  changed (both snapshots stand around the model call alone), so an
  orchestrator who discards exactly those files still meets a refusal on
  files nobody listed.
- Same on `main` and on PR #138: all three verbs keep the identical refusal,
  and #138 only restores inputs between attempts, not after the last one.
- Whether the refusal after a failed run is a bug at all is contested: the
  review loop of change codex-drafts answered "disagree — … a fresh invocation
  refusing those changes conforms to criterion 5". That is the first
  question for the maintainer.

## What exists today

### The refusal (three copies)

`scripts/stage2.py` on `main`, the same text in `implement`, `draft` and
`repair`: `outside = changed_paths(root) - allowed`, `allowed =
{findings.md}`, then `Refused("the worktree has pre-existing changes outside
this change's findings.md: …")`. PR #138 keeps all three (`implement`,
`draft`, `repair`).

### What the runner itself writes, and when

| Write | Where in `scripts/stage2.py` (`main`) | Path | Exempt next run? |
|---|---|---|---|
| audit line, attempt block | `begin_work_call`, `append` → `stamp_updated` | `findings.md` | yes |
| route block on stage-1 | `run_attempts`, `insert_before_time(ctx.plan, …)` before the call | `plan.md` | **no** |
| `updated:` stamp of every changed held document | `prepare_derived`, `check_frontmatter_current.stamp` | `findings.md`, `plan.md`, any held file the model changed | only `findings.md` |
| rendered index | `prepare_derived`, `scripts/plans_registry.py --index` | `plans/INDEX.md` (tracked) | **no** |
| ruff safe fixes and format | `format_step` | Python files the model changed | no (mixed with the model's edits) |

- `plans/INDEX.md` is tracked (`git ls-files` on 2026-10-14) and is
  re-rendered on every attempt; it differs from `HEAD` whenever a held
  document's frontmatter changed — including the runner's own stamp on
  `findings.md` (inferred from the renderer's purpose, not measured).
- `__pycache__/` is ignored in this repository (`.gitignore`), so it does not
  count here; in the test world of `tests/test_stage2.py` there is no
  `.gitignore`, which is why `clear_derived_leftovers` also removes it.

### What happens to the tree on failure

- **The model call itself fails** (`CallFailed` from the call):
  `restore_baseline` puts back every path but `findings.md`, derived writes of
  earlier attempts included. No leftover; the next run starts clean.
- **A post-run check fails on the last attempt:** `run_attempts` ends with
  `raise CallFailed(closing)`; nothing is put back. `docs/WORKFLOW.md` (runner
  section) says so: "a failed post-run check leaves its tree and its quoted
  block". `plans/changes/codex-drafts/spec.md`, criterion 21, says the next
  **attempt** starts on the tree the failed one left; it says nothing about the
  next **run**.
- Draft (`draft`) additionally calls `put_back` after each attempt for paths a
  draft may not change — `plans/INDEX.md` among them — but `verify_draft` then
  calls `prepare_derived` again, which re-renders the index after the
  put-back.
- PR #138, `run_attempts`: between attempts it restores every snapshotted
  prompt input (the plan included) to its pre-call bytes; after the last
  attempt it restores nothing. `INDEX.md` is not an input.

### Why the leftover tree matters to the orchestrator

The kept tree is used: change adr-owning-change, `plan.md`, "Phase 4,
2026-10-13" — the orchestrator's sub-agent completed the failed Sonnet
attempt's tree; PR #138's commit `1ea2f0d` reads "Sonnet attempt, completed
by the orchestrator". A fix that puts the whole tree back after a failed run
would remove that path.

### Evidence of the bug

- `plans/changes/codex-drafts/findings.md`, loop row L3-3 (mimo-v2.6-pro,
  2026-10-13): rejected as out of that change's scope; implementer's verdict
  "disagree — The prescribed second draft follows a successful, committed
  first draft. Failed post-run checks intentionally retain their tree under
  criterion 21; a fresh invocation refusing those changes conforms to
  criterion 5."
- `tests/test_stage2.py`, `clear_derived_leftovers` ("Remove what a failed
  run's `prepare_derived` left untracked; the next run would refuse it"), used
  by two draft tests before their second run. PR #138 keeps it.
- `docs/journal/handover/2026-10-13-night-run-second.md`: "A failed run
  blocks the next one … the runner's own derived writes count as pre-existing
  changes."

## Candidate fixes

1. **Tolerate exactly the derived writes at the next run's check.** Exempt
   `plans/INDEX.md`, and any held document whose diff against `HEAD` is the
   `updated:` line alone.
   - For: the kept tree stays as the orchestrator uses it; small, one helper
     shared by the three verbs; the next run re-renders and re-stamps anyway.
   - Against: does not cover the `plan.md` route block or ruff's formatting;
     an `updated:`-only diff a human made is accepted silently (harmless — the
     runner would stamp it again).
2. **The runner puts back its own derived writes when a run fails** (index to
   `HEAD`, stamps undone where the stamp is the file's only change, route
   block removed), and lists them in the closing message.
   - For: the leftover tree is the model's work alone, which is what the
     attempt block lists.
   - Against: a stamp on a model-changed file cannot be undone without
     remembering the pre-stamp bytes; on PR #138 the plan input is restored
     between attempts but not after the last, so a second mechanism.
3. **Name every runner write in the attempt block** (a "The runner also
   wrote" list), keep the refusal as it is.
   - For: no behaviour change; criterion 5 of codex-drafts stays literal; the
     orchestrator's manual restore becomes exact instead of guessed.
   - Against: the retry still needs a manual step; the tests keep
     `clear_derived_leftovers`.
4. **Put the whole tree back after the last failed attempt**, as a failed
   call already does.
   - Against: removes the "orchestrator completes the attempt" path the night
     runs rely on; contradicts `docs/WORKFLOW.md` ("leaves its tree").

## Which files a change would touch

- `scripts/stage2.py`: the three refusals (`implement`, `draft`, `repair`)
  through one helper; `run_attempts` and `draft` for candidates 2 and 3.
- `tests/test_stage2.py`: a failed run followed by a second run of the same
  verb, without `clear_derived_leftovers`; that helper removed or narrowed.
- `docs/WORKFLOW.md`, runner section: what a failed run leaves and what the
  next run accepts.
- With PR #138 unmerged: its `run_attempts` and `repair` are rewritten; the
  refusal lines themselves are unchanged there, so a helper extracted after
  #138 merges conflicts little.

## Questions this change has to answer

- [DECISION] Is a second run on a failed run's tree meant to start at all?
  (a) yes, the runner tolerates its own derived writes (candidate 1,
  recommended — it removes the manual restore and keeps the leftover tree for
  completion by hand); (b) no, the refusal stands and the runner names its
  writes so the restore is exact (candidate 3).
- [DECISION] Whether this change waits for pull request #138 (recommended:
  yes — #138 rewrites `run_attempts` and `repair`, and the helper is small).
- [GAP] What exactly `plans/INDEX.md` changes after a failed run in this
  repository — whether the runner's own stamp on `findings.md` alone already
  changes it (decides whether the leftover appears on every failed run or only
  when the model touched a held document). One rendered diff settles it.
- [GAP] Whether the `plan.md` route block on the stage-1 route and ruff's
  formatting belong to this change, or only `INDEX.md` and stamps as the bead
  names them.
- [DETAIL] Tolerance compares against `HEAD`, not the baseline of the
  failed run: the runner does not keep a record of a past run, and `HEAD` is
  what the refusal compares against today.
- [DETAIL] The test drives one failed `implement` run, discards the files its
  attempt block lists, and starts a second run that must reach its model call.
