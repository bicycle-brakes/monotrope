---
title: "Findings — terms-test-fixtures"
category: findings
status: draft
implementation_status: none
date: 2026-10-27
created: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-hxkw
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — terms-test-fixtures

Stage-2 call, 2026-10-27: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 705 files, 2383 commits, 12 rules.

## Draft validation — 2026-10-27

Baseline `e4f84f04`; spec and plan drafted, implementation not started.
No phase-2a rows were present to resolve. The bounded class requires neither
`design.md` nor an ADR draft. Repository gaps read during drafting are appended
to `research.md`; the maintainer's decisions and interview skip are unchanged.

- `python3 scripts/check_interview_minimums.py --change terms-test-fixtures`
  — exit 0; this change's reasoned skip satisfies the bounded minimum.
- `python3 scripts/check_criterion_ledger.py` — exit 0; existing test names
  resolve and the two new tests remain explicitly not yet written.
- `python3 scripts/check_research_handoff.py --change terms-test-fixtures`
  — exit 0; exempt because no research-swarm/v2 evidence exists.
- `git diff --check` — exit 0 on tracked edits at drafting.
- Draft structure check — exit 0; required headers, six refuting cases,
  bounded class, a single criterion ledger and empty time section checked.
- `scripts/validate_change_artefacts.py` is absent, so that check was not run.
  `templates/plan.md` is absent too; the plan follows `prompts/03-plan.md`.
- `make verify`, the contract-fault demonstration, and the three loaded runs
  are not run in this draft. The runner owns full verification, derived index
  refresh and the commit. No tracker writes, commits or mutating git commands
  were run.
- PR state is not read: `gh pr view` could not connect to GitHub.

Next: the orchestrator presents the plan card unchanged, then runs phase 4
within its two-hour appetite. Record measured implementation time in `plan.md`
and full-run evidence here; do not infer test success from this draft's checks.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/terms-test-fixtures/findings.md` +28 -0
> - `plans/changes/terms-test-fixtures/plan.md` +106 -0
> - `plans/changes/terms-test-fixtures/research.md` +37 -1
> - `plans/changes/terms-test-fixtures/spec.md` +116 -0
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 482 lines of this gate left out …]
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/findings.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/plan.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/research.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/spec.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/decisions.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/findings.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/plan.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/research.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/spec.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/decisions.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/findings.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/plan.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/research.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/spec.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - Bead 'coding-harness-2i9j' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-2i9j` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-2pj7' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-2pj7` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-6jg' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-6jg` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-vque' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-vque` -- or set the bead back to 'open' if nobody is working on it.
>
> INFO  (2):
>   - 5 running beads checked, 4 without artefact
>   - 341 artefacts checked
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=66797) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/terms-test-fixtures/tests/test_stage2.py:16292: DeprecationWarning: This process (pid=66850) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_gate_machinery.py::test_the_plans_registry_staleness_check_runs_green_here
> 1 failed, 4056 passed, 17 skipped, 5 warnings in 1445.20s (0:24:05)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [plans-registry] $ lauf_cmd
> [… 392 lines of this gate left out …]
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/test-key-runtime/research.md: bead 'coding-harness-05op' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/test-key-runtime/spec.md: bead 'coding-harness-05op' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/decisions.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/findings.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/plan.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/research.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/spec.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/decisions.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/findings.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/plan.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/research.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/spec.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/decisions.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/findings.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/plan.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/research.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/spec.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/decisions.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/findings.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/plan.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/research.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/spec.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - Bead 'coding-harness-2i9j' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-2i9j` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-2pj7' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-2pj7` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-6jg' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-6jg` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-vque' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-vque` -- or set the bead back to 'open' if nobody is working on it.
>
> INFO  (2):
>   - 5 running beads checked, 4 without artefact
>   - 341 artefacts checked
> ── [plans-registry] RED (block) — der Lauf ist rot.
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/terms-test-fixtures/decisions.md: no-frontmatter
> fix: python3 scripts/check_frontmatter_current.py --stamp
> (no-frontmatter and duplicate need a hand edit; the stamp names them and leaves them alone.)
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 20393 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-27: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 708 files, 2384 commits, 12 rules.

## Draft attempt 2 validation — 2026-10-27

Baseline remains `e4f84f04`. Added the required document header to
`decisions.md`; its body, including the interview skip and agent decisions,
is byte-for-byte unchanged. The spec's class and six acceptance criteria are
unchanged. The plan now carries the first attempt's external verification
blockers forward. No phase-2a rows were found; no design or ADR is due for
this bounded change. Implementation has not started.

Measured after the repair:

- `python3 scripts/check_interview_minimums.py --change terms-test-fixtures`
  — exit 0; the reasoned skip still satisfies the bounded minimum.
- `python3 scripts/check_criterion_ledger.py` — exit 0; test references
  resolve and the two proposed helper tests remain not yet written.
- `python3 scripts/check_research_handoff.py --change terms-test-fixtures`
  — exit 0 with the explicit legacy exemption, not a swarm handoff review.
- `python3 scripts/check_frontmatter_current.py` — exit 0; the missing
  decisions header reported by attempt 1 is repaired.
- `git diff --check` — exit 0. A structure check also confirmed required
  headers, six refuting cases, the opening plan card, one ledger, the empty
  time section and unchanged decisions body.

`make verify` is not rerun in this draft; the runner owns that check and the
commit. The previous run's tracker/artifact drift remains outside this
change's scope and has not been repaired or remeasured here. The absent
`scripts/validate_change_artefacts.py` remains unavailable. Current GitHub
PR state and external session registries were not read under the worktree-only
read boundary. No tracker writes or mutating git commands were run.

Resume: the orchestrator reruns full verification and presents the unchanged
plan card before phase 4. A red run is not completion evidence; report external
blockers without changing other packages or weakening criteria.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`
> - `plans/changes/terms-test-fixtures/decisions.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/terms-test-fixtures/decisions.md` +17 -0
> - `plans/changes/terms-test-fixtures/findings.md` +34 -0
> - `plans/changes/terms-test-fixtures/plan.md` +6 -0
>
> Diagnostics:
> ```text
> - `make verify` could not run: make was stopped by the runner's step limit after 30 minutes
> ```

Stage-2 call, 2026-10-27: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 708 files, 2384 commits, 12 rules.

## Draft attempt 3 validation — 2026-10-27

Attempt 3 (GLM 5.3) took the draft over unchanged in substance: the class and
six criteria of the spec, the card, the steps and the criterion ledger stand
as attempt 1 wrote them. Before adopting them, their claims were re-read
against the tree at `e4f84f04`:

- All six ledger test names are defined:
  `test_terms_problem_requires_an_iso_reading_date` and
  `test_paid_terms_require_a_retention_reading` in `tests/test_stage2.py`,
  `test_paid_terms_require_a_usable_expiry` and
  `test_expiry_preserves_prior_admission_guards` in
  `tests/test_stage2_terms_expiry.py`,
  `test_a_model_without_admitted_terms_or_cost_is_never_used` in
  `tests/test_stage2_research_availability.py`, and
  `test_terminal_record_survives_sigkill_after_the_outcome` in
  `tests/test_stage2_research_store.py`.
- The kill test still waits for two pipe lines through `pipe_line`
  (120-second deadline); its second child loops on the release file, its
  `audit` writes the launch record, and the three assertions (first result
  readable, `s2` absent from results, `interrupted == ["s2"]`) are as the
  plan's step 9 describes.
- `a_record` in `tests/test_stage2_terms_expiry.py` (five fields, no cost
  key, far-future expiry) and the plain cross-suite imports
  (`from test_stage2 import …`) confirm the builder shape and the import
  idiom of steps 1–8.

Changed in this attempt: the `produced_by` provenance of `spec.md` and
`plan.md` (now the GLM session), and the plan's verification-blocker
paragraph — attempt 2's sentence that the decisions header "is repaired"
was false once the runner put `decisions.md` back.

No shell is available to this drafting session, so the draft-side checks were
not re-run here; attempts 1 and 2 measured them green
(`check_interview_minimums.py`, `check_criterion_ledger.py`,
`check_research_handoff.py`, and `check_frontmatter_current.py` after the
header edit), and this attempt's edits touch none of the forms those gates
parse — verified against the gate sources, not by execution. `make verify`
remains the runner's, and its two known external blockers stand: the
plans-registry staleness drift of other changes, and this change's
`decisions.md` without a document header, which a draft may not add (the
runner reverts the edit) and which therefore needs a hand edit outside the
draft phase. A red or stopped run is not completion evidence.

Resume: the orchestrator adds the decisions header by hand, reruns full
verification, and presents the plan card unchanged before phase 4.

> Attempt 3 (glm): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 3 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/terms-test-fixtures/findings.md` +47 -0
> - `plans/changes/terms-test-fixtures/plan.md` +11 -6
> - `plans/changes/terms-test-fixtures/spec.md` +1 -1
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 482 lines of this gate left out …]
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/findings.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/plan.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/research.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/spec.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/decisions.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/findings.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/plan.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/research.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/spec.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/decisions.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/findings.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/plan.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/research.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/spec.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - Bead 'coding-harness-2i9j' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-2i9j` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-2pj7' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-2pj7` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-6jg' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-6jg` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-vque' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-vque` -- or set the bead back to 'open' if nobody is working on it.
>
> INFO  (2):
>   - 5 running beads checked, 4 without artefact
>   - 341 artefacts checked
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=89212) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/terms-test-fixtures/tests/test_stage2.py:16292: DeprecationWarning: This process (pid=89213) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_gate_machinery.py::test_the_plans_registry_staleness_check_runs_green_here
> 1 failed, 4056 passed, 17 skipped, 5 warnings in 1061.55s (0:17:41)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [plans-registry] $ lauf_cmd
> [… 392 lines of this gate left out …]
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/test-key-runtime/research.md: bead 'coding-harness-05op' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/test-key-runtime/spec.md: bead 'coding-harness-05op' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/decisions.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/findings.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/plan.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/research.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/tolerate-derived-leftovers/spec.md: bead 'coding-harness-b5w' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/decisions.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/findings.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/plan.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/research.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/venv-pycache/spec.md: bead 'coding-harness-q94b' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/decisions.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/findings.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/plan.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/research.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-absolute-python/spec.md: bead 'coding-harness-4x2c' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/decisions.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/findings.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/plan.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/research.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - plans/changes/verify-stages-new-files/spec.md: bead 'coding-harness-fdz' is closed in the export, but the artefact is not 'done' and archived
>       The tracker says finished, the artefact contradicts.
>   - Bead 'coding-harness-2i9j' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-2i9j` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-2pj7' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-2pj7` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-6jg' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-6jg` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-vque' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-vque` -- or set the bead back to 'open' if nobody is working on it.
>
> INFO  (2):
>   - 5 running beads checked, 4 without artefact
>   - 341 artefacts checked
> ── [plans-registry] RED (block) — der Lauf ist rot.
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/terms-test-fixtures/decisions.md: no-frontmatter
> fix: python3 scripts/check_frontmatter_current.py --stamp
> (no-frontmatter and duplicate need a hand edit; the stamp names them and leaves them alone.)
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 20489 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-27: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 708 files, 2390 commits, 12 rules.

## Renewed draft validation — 2026-10-27

Re-read the research, decisions, templates, prior draft diagnostics and the
named production/test seams at `454790ae`. The existing bounded class,
six acceptance criteria, two-hour appetite and plan card are unchanged.
No phase-2a rows or open ambiguities were present. No design or ADR is due.

Implemented in this draft: corrected the plan's obsolete missing-header
blocker, named the current baseline and displayed the verification command
verbatim. The decisions header is now present; its body is unchanged.
Updated spec and plan provenance to this Codex drafting session. Earlier
attempt records above remain historical evidence, not current-state claims.

Measured in this draft:

- `python3 scripts/check_interview_minimums.py --change terms-test-fixtures`
  — exit 0; the bounded interview skip satisfies the minimum.
- `python3 scripts/check_criterion_ledger.py` — exit 0; the existing test
  references resolve, and both proposed helper tests remain not yet written.
- `python3 scripts/check_research_handoff.py --change terms-test-fixtures`
  — exit 0, explicitly exempt without research-swarm/v2 evidence.
- `python3 scripts/check_frontmatter_current.py` — exit 0; current headers
  include the decisions header repaired before this draft.
- `git diff --check` and a draft structure check — exit 0; criteria,
  decisions and card match `HEAD`, the time section is empty, and changed
  paths stay inside this change folder.

The requested `scripts/validate_change_artefacts.py` and `templates/plan.md`
are absent from this tree. The plan follows `prompts/03-plan.md`; no passing
result is claimed for the absent validator. Full `make verify`, helper
contract-fault evidence and three loaded runs remain unperformed by this
draft; the runner owns full verification and the commit. Earlier tracker
drift was not remeasured. Current PR state, the shared tracker and external
session registries were not read under the worktree-only read boundary.
No tracker writes, implementation edits, commits or mutating git commands
were made. The phase-4 time section remains empty.

Resume: the orchestrator runs full verification and presents the unchanged
plan card before phase 4; report any external blocker without weakening the
criteria or repairing another change.

Stage-2 call, 2026-10-27: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 708 files, 2392 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/terms-test-fixtures/findings.md` +57 -0
> - `plans/changes/terms-test-fixtures/plan.md` +2 -2
> - `tests/terms_fixtures.py` +41 -0
> - `tests/test_pi_contract.py` +2 -10
> - `tests/test_stage2.py` +38 -45
> - `tests/test_stage2_research_availability.py` +4 -9
> - `tests/test_stage2_research_store.py` +36 -6
> - `tests/test_stage2_session.py` +5 -15
> - `tests/test_stage2_swarm.py` +10 -11
> - `tests/test_stage2_terms_expiry.py` +3 -18
> - `tests/test_terms_fixtures.py` +70 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 53 lines of this gate left out …]
> ........................................................................ [ 90%]
> ........................................................................ [ 91%]
> ........................................................................ [ 93%]
> ........................................................................ [ 95%]
> ........................................................................ [ 97%]
> ........................................................................ [ 98%]
> ............................................                             [100%]
> =================================== FAILURES ===================================
> _ test_terms_problem_requires_an_iso_reading_date[changes6-False-no dated reading of its data terms] _
> [gw7] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/terms-test-fixtures/.venv/bin/python3
>
> changes = {'gelesen': '', 'uebersprungen': None}, admitted = False
> reason = 'no dated reading of its data terms'
>
>     @pytest.mark.parametrize(
>         ("changes", "admitted", "reason"),
>         [
>             ({"gelesen": "2026-10-07", "quelle": "src"}, True, ""),
>             ({"gelesen": "2026-10-07", "quelle": "src", "uebersprungen": ""}, True, ""),
>             ({"gelesen": "soon"}, False, "gelesen is not an ISO date"),
>             ({"gelesen": True}, False, "gelesen is not an ISO date"),
>             ({"gelesen": "2026-13-45"}, False, "gelesen is not an ISO date"),
>             ({"gelesen": None, "uebersprungen": ""}, False, "no dated reading of its data terms"),
>             ({"gelesen": "", "uebersprungen": None}, False, "no dated reading of its data terms"),
>             ({"uebersprungen": "2026-10-08", "grund": "trains"}, False, "was skipped on 2026-10-08"),
>         ],
>     )
>     def test_terms_problem_requires_an_iso_reading_date(changes: dict, admitted: bool, reason: str) -> None:
>         """L1-1: `gelesen` must be an ISO date; an empty skip marker is "absent" only beside a valid one - fail closed.
>     
>         Every case starts from the shared builder and removes (`None`) or replaces
>         only the field under test, so another missing field cannot mask the refusal
>         this case is about.
>         """
>         removals = [field for field, value in changes.items() if value is None]
>         record = admissible_terms(**{field: value for field, value in changes.items() if value is not None})
>         for field in removals:
> >           del record[field]
> E           KeyError: 'uebersprungen'
>
> tests/test_stage2.py:13994: KeyError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=68393) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/terms-test-fixtures/tests/test_stage2.py:16285: DeprecationWarning: This process (pid=68403) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_terms_problem_requires_an_iso_reading_date[changes6-False-no dated reading of its data terms]
> 1 failed, 4058 passed, 17 skipped, 5 warnings in 815.69s (0:13:35)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> tests/test_stage2_research_store.py:221:9: SIM105 Use `contextlib.suppress(subprocess.TimeoutExpired)` instead of `try`-`except`-`pass`
>     |
> 219 |           if proc.poll() is None:
> 220 |               proc.kill()
> 221 | /         try:
> 222 | |             proc.wait(timeout=10)
> 223 | |         except subprocess.TimeoutExpired:
> 224 | |             pass
>     | |________________^ SIM105
> 225 |           for stream in (proc.stdout, proc.stderr):
> 226 |               if stream is not None:
>     |
>     = help: Replace with `contextlib.suppress(subprocess.TimeoutExpired)`
>
> Found 1 error.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ── [ruff-check] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 20581 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-27: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 710 files, 2393 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/terms-test-fixtures/findings.md` +31 -0
> - `plans/changes/terms-test-fixtures/plan.md` +2 -2
> - `tests/test_stage2.py` +3 -2
> - `tests/test_stage2_research_store.py` +2 -3
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - findings.md changed outside runner bookkeeping; every finding and earlier attempt's evidence must stand
> ```

Stage-2 call, 2026-10-27: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 710 files, 2393 commits, 12 rules.
