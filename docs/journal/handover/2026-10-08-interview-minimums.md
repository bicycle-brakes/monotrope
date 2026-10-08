---
title: "Session handover — interview-minimums implemented, the decision pull request is open, 2026-10-08"
category: handover
created: 2026-10-08
updated: 2026-10-08
last_reviewed: 2026-10-08
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: cline, version: "2026-10-08"}
status: pending
review: {status: pending, approved_by: null, approved_at: null}
tags: [handover, interview, gates, workflow, cline]
bead: coding-harness-6yg
---

# interview-minimums — implemented, decision pull request open

## Where we are

The mandatory feature/ADR interviews are implemented end to end on branch
`feat/interview-minimums` (worktree `.claude/worktrees/interview-minimums`,
base `cc020f5`), bead `coding-harness-6yg`, claimed as
`cline-interview-minimums`. Phases 1–7 ran in order: research, ten decisions
(four asked, six given or refined with reasons), spec with twelve acceptance
criteria, Codex spec review (nine rows, all in spec, four ambiguities settled
by the maintainer as Q-5–Q-8), the waiver of phase 2b recorded in the spec's
non-goals, plan, implementation, `make verify` green, GLM review loop round 1
(eight rows: six taken, two rejected with reasons), Codex phase-6 review
(eleven rows F-10–F-20: every one taken and repaired), and a final green
`make verify` after each repair round. The decision pull request on this
branch is the release; **no merge without the maintainer's explicit order.**

## What the change holds

- `prompts/01a-interview.md`: the duty with the minimums and the
  machine-readable question record (`## Q-n ·` fields, `## SKIP · interview`).
- `prompts/02-spec.md`: the spec gate names the interview check before the
  spec passes.
- `docs/WORKFLOW.md`, `AGENTS.md`: phase table, duty paragraph, class
  section, stage-1 table, workflow table — the optionality wording is gone.
- `scripts/check_interview_minimums.py`: the gate (exit 0/1/3) — counts
  distinct maintainer-answered records per class, sees ADR paths in every
  diff state (committed, index, unstaged, untracked), base per context
  (first parent on the main line, else the merge base; detached at
  `origin/main` exits 3), cut-off `2026-10-08` against the spec date,
  archived post-cut-off changes measured, `--change` strict.
- `tests/test_check_interview_minimums.py`: 36 cases — the spec's
  counterexample matrix plus the loop and phase-6 rows, Git-isolated
  fixtures (F-19).
- `decisions/gates.yaml` + regenerated `.github/workflows/ci.yml`: the gate,
  verify, block, both.

## Evidence

- Final `make verify`: **VERIFY GREEN — every local gate of the 'verify' job
  passed** (pytest 1300+ passed, ruff, plans-registry, adr-answers,
  interview-minimums, ci-drift, gate-schema and the rest), 2026-10-08, after
  the phase-6 repairs.
- Review evidence stands unchanged in
  `plans/changes/interview-minimums/findings.md`: phase 2a nine rows `in
  spec`; phase 4b eight rows decided (L1-5 and L1-8 rejected with reasons,
  named as accepted limits in the pull request); phase 6 eleven rows, all
  `taken`, each with the test that holds it.

## Decisions and preferences

- The maintainer's ten decisions and the Q-7 base refinement are recorded in
  `plans/changes/interview-minimums/decisions.md`; nothing was asked twice.
- The ADR question of this change was answered "no" as stated by the
  maintainer and is recorded in
  `decisions/answers/interview-minimums/adr.yaml`; this pull request is
  therefore a **decision pull request** (title `decide(workflow): …`, label
  `decision`, body from `.github/PULL_REQUEST_TEMPLATE/decision.md`).
- Accepted limits, stated in the pull request: a multi-commit direct push to
  `main` shows only its last commit to the gate (RB-M6 makes that path a
  pull request anyway), and the `goes_red` mutation test deliberately
  resembles its neighbour — the ratchet's price.

## Parallel sessions and ownership

- Only this session wrote bead `coding-harness-6yg` and the files of
  `plans/changes/interview-minimums`. `.claude/worktrees/stage2-mimo`
  (OpenCode) and `mimo-watch-audit` were not touched; no other bead was
  claimed, closed or reprioritised.

## Resume

The maintainer reads the decision pull request and merges it — or comments.
After the merge: archive `plans/changes/interview-minimums/` per
`plans/_README.md`, close the bead (`tools/bd close coding-harness-6yg
--reason=…`), `tools/bd dolt push`, then delete the worktree. Nothing else is
open on this change.

## Addendum — 2026-10-08, Codex repairs the interrupted PR review

### Objective and takeover

The maintainer asked Codex to repair the interrupted Cline task here and to
prepare a night session. Codex takes over the existing worktree; Cline must
remain stopped while Codex writes. The two attempted UI messages to Cline
were rejected after the app state changed; neither was confirmed sent.

The previous statement that nothing remained open describes the earlier
checkpoint, not the PR-review state. The decision pull request is open at
`a6dde6b9a476177526c1917a03a6c988f1df7976` (PR #104, read 2026-10-08).
Its hosted tests failed on the unsupported `owner` field in this handover
on both Python 3.11 and 3.12. No merge is authorized.

### Repairs and evidence

Cline added two regression tests and corrected the staged-only fixture,
then reverted the entire checker with `git checkout --` after a temporary
mutation. This also deleted the uncommitted rename and date-comment fixes.
The background verifier had already finished red when the repeated
`kill -0` polls triggered Cline's identical-call guard. Its log records
three failures, 1308 passes and 16 skips on 2026-10-08
(`/tmp/make_verify_p2.log`); the log is local evidence, not a durable artifact.

Codex restored rename detection suppression for both Git diffs, restored
date metadata with trailing comments, and removed the unsupported handover
field without expanding the schema. The maintainer-review tests and the
fixture repair are preserved. All 38 interview tests plus the unknown-field
test passed on 2026-10-08. Three temporary regressions each made their
intended test fail; the repaired source was restored from an exact byte
snapshot in `finally`, preserving every uncommitted repair.

Full verification is pending at the time this addendum is first written.
These repairs are local and uncommitted. No tracker write, commit, push or
merge is claimed; the bead remains assigned to `cline-interview-minimums`
and in progress (read 2026-10-08). Repository session scanning returned no
rows; that scan does not establish the absence of non-Claude sessions.

The first full Codex verification on 2026-10-08 exited 2: 1296 tests passed,
16 skipped and 15 fixture setups errored because unrelated Git fixtures
inherited an unavailable SSH signing key. The live ruleset check also could
not reach GitHub from the sandbox. This is not a green verification claim.
The retry supplies `commit.gpgsign=false` only through the test process's
`GIT_CONFIG_COUNT` environment and permits the existing live GitHub check;
it changes no repository/global signing configuration and skips no gate.

### Night-session start brief

Prepare only; do not launch another writer automatically. The default scope
is to finish the repaired PR first, then at most one bounded item. Task
status stays in Beads; this is a resumption instruction, not another tracker.

1. Start inside `.claude/worktrees/interview-minimums`. Read this addendum,
   the three maintainer-review rows in the findings, and `AGENTS.md`. Inspect
   the current diff, PR head and checks before writing. Confirm that Cline
   remains stopped and respect the repository session cap and tracker owner.
2. Use the recorded verification result below. If the tree has changed,
   verify that new state. Capture the real command exit status and inspect
   the log; do not infer completion from a background PID or repeat an
   identical polling command. Preserve current source exactly around any
   temporary mutation. Leave the decision and gate policy unchanged.
   Where unrelated fixtures inherit unavailable signing, set
   `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=commit.gpgsign` and
   `GIT_CONFIG_VALUE_0=false` only for the `make verify` process, with network
   access for the live GitHub ruleset gate. Do not persist this override in
   Git configuration or use it for real project commits.
3. If publication is authorized, publish the repaired checkpoint to the
   existing decision PR and wait for hosted CI on that exact head. State
   explicitly which beads changed; push authorized tracker changes before
   Git. Do not close the bead or archive the change before its merge.
   A green PR still requires the maintainer's merge request.

Only after that checkpoint is green, the next bounded candidate is the
missing reproducible count of findings from the first three Stage-2 runs
(coding-harness-kw0). Re-read its current description and the merged research
note before claiming it. Follow the seven phases in a fresh worktree from
freshly fetched `origin/main`, and run `make venv` once. Derive findings,
verdicts and leak-check counts from recorded evidence with commit cut-offs;
report unavailable token and cost data as unmeasured. Do not invent values
or close the item while its evidence is incomplete. If a human decision is
needed, record it and stop that item rather than inventing an answer.

The other open decision PR concerns the reviewer ladder (PR #105,
`feat/stage2-mimo`, read 2026-10-08). It retains its existing session's
ownership and is outside this night brief. The customer instance and other
workers' files remain outside scope. Do not start sub-agents, change model
routing, run live model probes or merge PRs under this brief.

Resume: inspect the repaired local diff and its final verification evidence
below, then finish the publication step within the authority of the active
session.

### Final local verification — 2026-10-08

The retry exited 0 with `VERIFY GREEN`: 1311 passed, 16 skipped; the live
ruleset gate also passed (90 tests). Every blocking gate passed. Existing
report-only link and Markdown findings remain reports. The evidence was
measured on `a6dde6b` plus the five modified paths reported by `git status`,
including the restored checker, the preserved tests and review rows, the
spec clarification, and this handover. The authorized run is recorded locally
(`/tmp/codex_interview_repairs_verify_authorized.log`).

The repairs are still uncommitted and unpublished. No bead was changed or
closed, and no merge was performed. The conservative publication policy from
the session's Beads context remains in force. The night brief is prepared,
not launched. Resume with the existing repaired worktree; do not replay the
failed background polling or discard its uncommitted files.


## Addendum — 2026-10-08, authorized night-session publication

### Objective and authority

The maintainer launched the prepared night brief with “und go” on
2026-10-08. This authorizes publication of the reviewed repairs to the
existing decision PR #104; it does not authorize a merge. The five inherited
modified paths match the repair checkpoint above. The three maintainer
review rows are preserved unchanged in this publication.

### Parallel sessions and boundaries

Before writing, Codex read the local Cline session metadata: session
`1791472146419_oo8ja` has status `failed`; the extension log ends its agent
turn with `idle` at 2026-10-08T21:21:49Z. The repaired worktree remained
unchanged throughout inspection. The UI tool declined access to Code, so
this evidence comes from session metadata and the extension log.

The authorized process/session inspection found an existing repository
session in the main checkout and a running review process in
`.claude/worktrees/stage2-runs-count`. The follow-up measurement bead was
already in progress when read on 2026-10-08, with a recent heartbeat.
Consequently this night session takes no second item, launches no agents,
and does not write the tracker. The earlier session retains tracker
ownership; the measurement worktree and PR #105 remain outside this scope.
No bead is opened, changed or closed by this publication. The interview
bead stays in progress until the maintainer merges PR #104.

### Verification and resumption

The inherited repair checkpoint has the green evidence recorded above.
The night addendum is included in a fresh verification before publication;
its result and the exact hosted head will be recorded in a later addendum.
No real commit uses the process-local test signing override.

Resume: read PR #104 at its current exact head and its hosted checks.
If green, await the maintainer's explicit merge request; after an authorized
merge, the tracker owner archives the change and closes the interview bead.


### Night checkpoint — 2026-10-08, verification and publication complete

Fresh local `make verify` exited 0 with `VERIFY GREEN`: 1311 passed,
16 skipped, and the live ruleset gate passed its 90 tests. Only the temporary
Git fixtures used the process-local signing override; the real commit used
the repository's configured signing. Local evidence is retained in
`/tmp/codex_night_interview_verify.log`.

The five-path repair checkpoint was committed and pushed as
`88102d7a044b57bbdc8a3ff1b637685ecfa0a8d9` on
`feat/interview-minimums`, PR #104. Both hosted workflows passed their
Python 3.11 and 3.12 gates and their final `verify` jobs on that exact head;
the non-applicable drift jobs were skipped. Durable hosted evidence:

- [Push workflow](https://github.com/MPAdesso/coding-harness/actions/runs/37849937311).
- [Pull-request workflow](https://github.com/MPAdesso/coding-harness/actions/runs/37849943904).

The PR description now explains the repairs and uses the generated touch
map. The three maintainer-review rows were committed unchanged. This dated
checkpoint is a documentation-only successor to the verified repair;
its own hosted CI must also be green before any merge.

No tracker write or merge occurred. The interview bead remains in progress
under its existing assignee, and the parallel session retains the measurement
item. No new worktree or agent was started. At the repair checkpoint the
worktree was clean; this successor records the final evidence in the file.

Resume: inspect the latest head and checks of
[PR #104](https://github.com/MPAdesso/coding-harness/pull/104), then await the
maintainer's explicit merge request. After that authorized merge, coordinate
archival and closure with the existing tracker owner and push tracker data
before any resulting Git publication. The bounded follow-up measurement
remains with the other session; do not take it over from this handover.
