---
title: "Findings — workflow-promises"
category: findings
status: draft
implementation_status: partial
date: 2026-10-27
created: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-i0l
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — workflow-promises

Stage-2 call, 2026-10-27: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 705 files, 2383 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/workflow-promises/plan.md` +108 -0
> - `plans/changes/workflow-promises/spec.md` +139 -0
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
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=37393) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/workflow-promises/tests/test_stage2.py:16292: DeprecationWarning: This process (pid=37465) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_gate_machinery.py::test_the_plans_registry_staleness_check_runs_green_here
> 1 failed, 4056 passed, 17 skipped, 5 warnings in 1518.91s (0:25:18)
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
> plans/changes/workflow-promises/decisions.md: no-frontmatter
> fix: python3 scripts/check_frontmatter_current.py --stamp
> (no-frontmatter and duplicate need a hand edit; the stamp names them and leaves them alone.)
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 20394 earlier lines left out …]
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

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`
> - `plans/changes/workflow-promises/decisions.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/workflow-promises/decisions.md` +17 -0
> - `plans/changes/workflow-promises/plan.md` +16 -1
> - `plans/changes/workflow-promises/spec.md` +3 -0
>
> Diagnostics:
> ```text
> - `make verify` could not run: make was stopped by the runner's step limit after 30 minutes
> ```

Stage-2 call, 2026-10-27: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 708 files, 2384 commits, 12 rules.

> Attempt 3 (glm): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 3 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/workflow-promises/plan.md` +101 -68
> - `plans/changes/workflow-promises/spec.md` +104 -63
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
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=43233) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/workflow-promises/tests/test_stage2.py:16292: DeprecationWarning: This process (pid=43237) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_gate_machinery.py::test_the_plans_registry_staleness_check_runs_green_here
> 1 failed, 4056 passed, 17 skipped, 5 warnings in 1380.74s (0:23:00)
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
> plans/changes/workflow-promises/decisions.md: no-frontmatter
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

Stage-2 call, 2026-10-27: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 708 files, 2392 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `Makefile` +26 -1
> - `docs/WORKFLOW.md` +9 -8
> - `docs/governance/gate-catalog.md` +89 -0
> - `plans/INDEX.md` +2 -2
> - `plans/changes/workflow-promises/findings.md` +32 -0
> - `plans/changes/workflow-promises/plan.md` +9 -9
> - `plans/changes/workflow-promises/spec.md` +1 -1
> - `scripts/ci_gates.py` +47 -0
> - `tests/test_gate_catalog.py` +234 -0
> - `tests/test_workflow_entry.py` +252 -3
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 631 lines of this gate left out …]
>         tree = _fixture_tree(tmp_path)
>         log = tmp_path / "aufrufe.log"
>         _controlled_python(tree, log)
>         davor = _snapshot(tree)
>     
>         ergebnis = _run_make(tree, log, "help")
>         assert ergebnis.returncode == 0, ergebnis.stderr
>         assert _snapshot(tree) == davor, "help wrote something"
> >       assert log.read_text(encoding="utf-8") == "", "help invoked a command"
>
> tests/test_workflow_entry.py:356: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1027: in read_text
>     with self.open(mode='r', encoding=encoding, errors=errors) as f:
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> self = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-847/popen-gw7/test_make_help_lists_targets_w0/aufrufe.log')
> mode = 'r', buffering = -1, encoding = 'utf-8', errors = None, newline = None
>
>     def open(self, mode='r', buffering=-1, encoding=None,
>              errors=None, newline=None):
>         """
>         Open the file pointed to by this path and return a file object, as
>         the built-in open() function does.
>         """
>         if "b" not in mode:
>             encoding = io.text_encoding(encoding)
> >       return io.open(self, mode, buffering, encoding, errors, newline)
> E       FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-847/popen-gw7/test_make_help_lists_targets_w0/aufrufe.log'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1013: FileNotFoundError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=51045) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/workflow-promises/tests/test_stage2.py:16292: DeprecationWarning: This process (pid=51017) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_gate_catalog.py::test_catalog_drift_is_rejected - KeyError:...
> FAILED tests/test_gate_catalog.py::test_catalog_matches_declared_gates - KeyE...
> FAILED tests/test_gate_catalog.py::test_catalog_renders_commands_and_actions
> FAILED tests/test_workflow_entry.py::test_make_change_delegates_to_scaffold
> FAILED tests/test_workflow_entry.py::test_make_change_rejections_preserve_tree[empty-name]
> FAILED tests/test_workflow_entry.py::test_make_change_rejections_preserve_tree[empty-bead]
> FAILED tests/test_workflow_entry.py::test_make_change_rejections_preserve_tree[unknown-bead]
> FAILED tests/test_workflow_entry.py::test_make_change_rejections_preserve_tree[closed-bead]
> FAILED tests/test_workflow_entry.py::test_make_change_rejections_preserve_tree[duplicate-name]
> FAILED tests/test_workflow_entry.py::test_make_change_rejections_preserve_tree[detached-head]
> FAILED tests/test_workflow_entry.py::test_make_help_lists_targets_without_side_effects
> 11 failed, 4058 passed, 18 skipped, 5 warnings in 1239.37s (0:20:39)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> tests/test_workflow_entry.py:204:27: ARG001 Unused function argument: `log`
>     |
> 204 | def _run_make(tree: Path, log: Path, *args: str) -> subprocess.CompletedProcess:
>     |                           ^^^ ARG001
> 205 |     """A real `make` run inside the tree, with the controlled python3 first on the path."""
> 206 |     make = shutil.which("make")
>     |
>
> Found 1 error.
> ── [ruff-check] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 20625 earlier lines left out …]
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
> - `Makefile` +1 -1
> - `plans/changes/workflow-promises/findings.md` +30 -0
> - `plans/changes/workflow-promises/plan.md` +9 -9
> - `plans/changes/workflow-promises/spec.md` +1 -1
> - `tests/test_gate_catalog.py` +6 -6
> - `tests/test_workflow_entry.py` +17 -5
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 51 lines of this gate left out …]
> ........................................................................ [ 86%]
> ........................................................................ [ 88%]
> ........................................................................ [ 89%]
> ........................................................................ [ 91%]
> ........................................................................ [ 93%]
> ........................................................................ [ 95%]
> ........................................................................ [ 96%]
> ........................................................................ [ 98%]
> .......s...............................................                  [100%]
> =================================== FAILURES ===================================
> ________________________ test_catalog_drift_is_rejected ________________________
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/workflow-promises/.venv/bin/python3
>
>     def test_catalog_drift_is_rejected() -> None:
>         """Criterion 2: a mutated inventory or a changed declaration leaves the comparison red.
>     
>         Each case plants the fault the spec refutes with, on fixture data; the
>         first assertion is the counter-check that the comparator itself is green
>         on a clean render.
>         """
>         alle = _fixture_gates()
>         rows = _rows(catalog_rows(alle))
>         assert _drift(alle, rows) == [], "the clean render must pass its own comparison"
>     
>         assert _drift(alle, rows[:2]) == ["missing row: probe-equivalent"]
>     
>         fremd = {**rows[0], "id": "probe-foreign"}
>         assert _drift(alle, [*rows, fremd]) == ["extra row: probe-foreign"]
>         assert _drift(alle, [*rows, rows[0]]) == ["duplicate row: probe-command"]
>     
>         gelogen = [{**rows[1], "enforcement": "block"}]
> >       assert _drift(alle, [gelogen[0], *rows[2:]]) == [
>             "probe-hosted: enforcement reads 'block', the gate declares 'advisory'"
>         ]
> E       assert ['missing row...s 'advisory'"] == ["probe-hoste...s 'advisory'"]
> E         
> E         At index 0 diff: 'missing row: probe-command' != "probe-hosted: enforcement reads 'block', the gate declares 'advisory'"
> E         Left contains one more item: "probe-hosted: enforcement reads 'block', the gate declares 'advisory'"
> E         Use -v to get more diff
>
> tests/test_gate_catalog.py:232: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=39115) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/workflow-promises/tests/test_stage2.py:16292: DeprecationWarning: This process (pid=39123) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_gate_catalog.py::test_catalog_drift_is_rejected - assert ['...
> 1 failed, 4068 passed, 18 skipped, 5 warnings in 1250.72s (0:20:50)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 20675 earlier lines left out …]
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

Stage-2 call, 2026-10-27: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 710 files, 2394 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: review-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: review-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 710 files, 2397 commits, 12 rules.

Stage-2 call, 2026-10-27: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 711 files, 2400 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +4 -4
> - `docs/governance/quality-gates.md` +7 -5
> - `docs/governance/regelwerk.md` +2 -2
> - `plans/INDEX.md` +4 -4
> - `plans/changes/workflow-promises/decisions.md` +1 -1
> - `plans/changes/workflow-promises/plan.md` +13 -7
> - `plans/changes/workflow-promises/research.md` +4 -11
> - `plans/changes/workflow-promises/spec.md` +1 -1
> - `scripts/kit/manifest.yaml` +3 -0
> - `scripts/kit/probe.py` +2 -0
> - `tests/test_workflow_entry.py` +76 -6
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` did not finish: make was stopped by the runner's step limit after 30 minutes
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/workflow-promises/stage2/attempts/workflow-promises/attempt-1-20261027T223630313846Z-307e8f97.md
> ```

Stage-2 call, 2026-10-28: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 711 files, 2401 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/workflow-promises/decisions.md` +1 -1
> - `plans/changes/workflow-promises/plan.md` +1 -1
> - `plans/changes/workflow-promises/spec.md` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-12: no fixed line
> - L1-13: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/workflow-promises/stage2/attempts/workflow-promises/attempt-2-20261027T223630313846Z-307e8f97.md
> ```

Stage-2 call, 2026-10-28: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 711 files, 2402 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/workflow-promises/decisions.md` +1 -1
> - `plans/changes/workflow-promises/plan.md` +1 -1
> - `plans/changes/workflow-promises/spec.md` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-2: the line is neither `<ID>: fixed — tests/<path>::<function>` nor `<ID>: fixed — not a test — <reason>`
> - L1-3: the line is neither `<ID>: fixed — tests/<path>::<function>` nor `<ID>: fixed — not a test — <reason>`
> - L1-7: `spec criterion 8: the WORKFLOW notice now lists `.claude/commands/` among the supplied pieces. The test for this is `tests/test_workflow_entry.py::test_workflow_notice_names_supplied_pieces`; I did not look inside it, only that `.claude/commands/` is among the pieces the notice must name.` is neither a test `tests/<path>::<function>` nor `not a test — <reason>`
> - L1-8: the line is neither `<ID>: fixed — tests/<path>::<function>` nor `<ID>: fixed — not a test — <reason>`
> - L1-9: the line is neither `<ID>: fixed — tests/<path>::<function>` nor `<ID>: fixed — not a test — <reason>`
> - L1-11: `spec criterion 7: `.claude/commands/workflow-start.md` exists. The skip guard on `tests/test_workflow_entry.py::test_workflow_start_delegates_to_scaffold` now skips only when `HARNESS_KIT_PROBE=1` and the file is absent. `tests/test_workflow_entry.py::test_missing_workflow_start_fails_outside_kit_probe` checks that a missing command fails outside the kit probe.` is neither a test `tests/<path>::<function>` nor `not a test — <reason>`
> - L1-12: the line is neither `<ID>: fixed — tests/<path>::<function>` nor `<ID>: fixed — not a test — <reason>`
> - L1-13: `spec criterion 4: `_snapshot` now records directories as well as files. `tests/test_workflow_entry.py::test_snapshot_detects_residual_empty_directory` shows that an empty residual change folder changes the snapshot.` is neither a test `tests/<path>::<function>` nor `not a test — <reason>`
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/workflow-promises/stage2/attempts/workflow-promises/attempt-3-20261027T223630313846Z-307e8f97.md
> ```

Stage-2 call, 2026-10-28: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 711 files, 2406 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - L1-2: no fixed line
> - L1-3: no fixed line
> - L1-7: no fixed line
> - L1-8: no fixed line
> - L1-9: no fixed line
> - L1-11: no fixed line
> - L1-12: no fixed line
> - L1-13: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/workflow-promises/stage2/attempts/workflow-promises/attempt-1-20261028T000210037922Z-9c65a354.md
> ```

Stage-2 call, 2026-10-28: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 711 files, 2406 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - L1-12: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/workflow-promises/stage2/attempts/workflow-promises/attempt-2-20261028T000210037922Z-9c65a354.md
> ```

Stage-2 call, 2026-10-28: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 711 files, 2406 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/INDEX.md` +1 -1
> - `plans/changes/workflow-promises/findings.md` +1 -1
>
> Diagnostics:
> ```text
> - findings.md changed outside runner bookkeeping; every finding and earlier attempt's evidence must stand
> - L1-7: answered `not a test`, but the row is a code row; it needs a test that was red first
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/workflow-promises/stage2/attempts/workflow-promises/attempt-3-20261028T000210037922Z-9c65a354.md
> ```

## Orchestrator acceptance of the loop-round-1 repairs — 2026-10-28

The repair verb's edits for round 1 were committed onto the branch after its
attempts failed (step limit under three-lane load, then fixed-line format), so
a rerun found the fixes already in its baseline and could not prove red first.
The orchestrator (Claude Code, Opus 5.5) accepted them by hand:

- Red first, at `e61554b0` with this branch's `tests/test_workflow_entry.py`:
  `test_workflow_notice_records_supplied_commands` and
  `test_missing_workflow_start_fails_outside_kit_probe` each failed with an
  `AssertionError`; `test_snapshot_detects_residual_empty_directory` passed,
  because the helper it pins lives in the same test file.
- At `fe85b3e1`: `tests/test_workflow_entry.py` and `tests/test_gate_catalog.py`,
  21 passed; full `make verify` alone, 00:42:29–00:54:10 UTC, VERIFY GREEN.
- The text rows (L1-2, L1-3, L1-8, L1-9, L1-12) were checked against the diff
  `e61554b0..fe85b3e1`.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 711 files, 2408 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 711 files, 2412 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 711 files, 2415 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model hy3 · leak check clean over 711 files, 2418 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 711 files, 2423 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model hy4-preview · leak check clean over 711 files, 2424 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 711 files, 2434 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 711 files, 2439 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 720 files, 2446 commits, 12 rules.
