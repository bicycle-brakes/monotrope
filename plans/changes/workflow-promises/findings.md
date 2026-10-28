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

## Review loop ended without a clean round, 2026-10-28

The review loop (phase 4b) ran nine rounds; every row was fixed or rejected
with its reason, and a full `make verify` was green after each repair
(last at `dcb9af49`). Round 10 was refused: every stage of the run was
consumed and the last round was not clean. The last rounds saw the change
diff cut at 2000 of 2470 lines. The maintainer answered on 2026-10-28 (the
directing conversation): run phase 6 now rather than restart the loop. The
pull request is merged by the maintainer, because no round was clean.

Stage-2 call, 2026-10-28: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 720 files, 2448 commits, 12 rules.

## Phase 6 — Codex, 2026-10-28

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MINOR | MAINT | phase-6 | tests/test_gate_catalog.py:103; scripts/ci_gates.py:400 | A schema-valid gate reason containing `first line\nsecond line` fails the catalog check even after regeneration: the renderer replaces the newline with a space, but the comparator expects the original newline. Reproduced by passing that gate through `_drift([g], _rows(catalog_rows([g])))`, which reports drift on freshly generated output. Valid multiline metadata must remain verifiable after regeneration. [Plan step 2: newline handling] | Codex | fixed — tests/test_gate_catalog.py::test_catalog_renders_commands_and_actions — the comparator shows a declared value as a cell does (a line break reads as a space); the new regeneration check fails with the previous comparator | pending — full make verify queued behind the running implement of another lane |

Phase 6 verdict: codex 01a182df-833f-7023-9247-6bcdcf6f5198, 2026-10-28
Reviewer session: codex 01a182df-833f-7023-9247-6bcdcf6f5198 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-10-28

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | BLOCKER | SPEC | diff | `.claude/commands/workflow-start.md` (absent), `tests/test_workflow_entry.py` (`COMMAND_SKIP`), `plans/changes/workflow-promises/spec.md` criterion 7 | The package promises `/workflow-start` but no command file exists: criterion 7, the Definition of Done and plan step 6 all name `.claude/commands/workflow-start.md`, and the plan's summary says `/workflow-start` works. The only test for it is skipped whenever the file is missing, so `make verify` stays green while criterion 7 is unimplemented and the test can never go red for the reason it exists. | deepseek-v4.1-flash | rejected — duplicate of L1-11 |  | agree |
| L1-2 | MAJOR | MAINT | diff | `docs/governance/gate-catalog.md`, `docs/governance/regelwerk.md` §8, `docs/governance/quality-gates.md` | The new page takes the filename two existing pages already describe as the catalog of twelve gate families and their operating rules, but the new page is the machine-gate list from the gate file. Those pages now send a reader to a page that is not the catalog they describe, and the change neither updates nor reconciles them. | deepseek-v4.1-flash | fixed — not a test — regelwerk.md section 8 and quality-gates.md now describe gate-catalog.md as the generated machine-gate view (orchestrator acceptance at fe85b3e1) | no — the full make verify after the repair stayed green | agree |
| L1-3 | MAJOR | MAINT | diff | `scripts/kit/manifest.yaml` role rules, `docs/WORKFLOW.md` §2 | The new catalog falls under the `docs/` catch-all and therefore stays home, while `docs/WORKFLOW.md`, `regelwerk.md` and `quality-gates.md` are declared as travelling mechanism and now link to it. Every kit copy carries three documents pointing at a file that does not travel, which is exactly what the manifest roles exist to prevent; the plan asserted no manifest change was needed. | deepseek-v4.1-flash | fixed — not a test — docs/governance/gate-catalog.md declared in scripts/kit/manifest.yaml (orchestrator acceptance at fe85b3e1) | no — the full make verify after the repair stayed green | agree |
| L1-4 | MINOR | MAINT | diff | `docs/governance/gate-catalog.md`, rows `docs-links` and `ramp-valves` | Two reason cells are German although the new page is otherwise English and the repository's artefacts are English by its own language note. A reader without German cannot understand why those two gates exist. The text is copied from the gate list, so a repair belongs in the reason there, not in the generated block. | deepseek-v4.1-flash | rejected — house rule 1: German in the tree is translated in a pull request of its own (bead coding-harness-yim), never in passing |  | disagree — The catalog must preserve source metadata; translating existing German gate definitions belongs in a separate change. |
| L1-5 | MINOR | SPEC | diff | `plans/changes/workflow-promises/spec.md` and `plan.md` frontmatter, `plans/INDEX.md` | Plan step 7 requires the implementation status of spec and plan to be updated, but both still read `implementation_status: none` after an accepted implementation, so the regenerated index lists the change as not implemented. | deepseek-v4.1-flash | rejected — duplicate of L1-12 |  | agree |
| L1-6 | BLOCKER | SPEC | spec criterion 7, plan step 6 | plans/changes/workflow-promises/spec.md; tests/test_workflow_entry.py (COMMAND_SKIP) | The promised Claude Code command `.claude/commands/workflow-start.md` is not in the change — `.claude/` holds only `agents/` and `settings.json` — so criterion 7 is refuted by its own clause ("the command is absent"); its ledger test `test_workflow_start_delegates_to_scaffold` is guarded by `COMMAND_SKIP` and skips when the file is missing, so `make verify` stays green over an unmet criterion. | mimo-v2.5 | rejected — duplicate of L1-11 |  | agree |
| L1-7 | MAJOR | SPEC | spec criterion 8 | docs/WORKFLOW.md header notice, lines 38–41 | Criterion 8 requires the missing-pieces notice to name `.claude/commands/` as supplied; the notice still lists `.claude/commands/` among the pieces **not** in this repository and its "Supplied since the last check" sentence names only the catalog and the two make targets, so criterion 8 fails as written. | mimo-v2.5 | fixed — tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands | no — the full make verify after the repair stayed green | agree |
| L1-8 | MINOR | MAINT | maintainer-trip | docs/WORKFLOW.md, lines 38–39 | The parenthetical "(the entry is `python3 scripts/new_change.py <name> --bead <id>`)" was left dangling when the `make change`/`make index` targets were deleted from the absent list; it now modifies `.claude/commands/`, and a maintainer cannot tell which absent piece it qualifies or whether `/workflow-start` (line 25) is expected to work. | mimo-v2.5 | fixed — not a test — the parenthetical now qualifies the make targets it belongs to (orchestrator acceptance at fe85b3e1) | no — the full make verify after the repair stayed green | agree |
| L1-9 | MAJOR | MAINT | provenance.yaml, class `human-written` | plans/changes/workflow-promises/research.md frontmatter | The body records a Stage-2 model run (explore, glm-5.3-flash, 2026-10-27) and still carries the skeleton note "Whoever fills it with a language model sets ai-drafted-reviewed and adds produced_by: and review:", yet the frontmatter still says `provenance: human-written` with no produced_by or review — the class tells every reader a person wrote the audit. | mimo-v2.5 | fixed — not a test — research.md provenance ai-drafted-reviewed with produced_by and review, skeleton text removed (orchestrator acceptance at fe85b3e1) | no — the full make verify after the repair stayed green | agree |
| L1-10 | MINOR | MAINT | plan step 7 | plans/changes/workflow-promises/spec.md, plan.md, decisions.md frontmatter; plans/INDEX.md rows | Every artefact of the change still declares `implementation_status: none` and the regenerated INDEX repeats `none` for all five files, although the diff ships the implementation; plan step 7 promised to update the implementation status, so the index reads as a change not started. | mimo-v2.5 | rejected — duplicate of L1-12 |  | agree |
| L1-11 | BLOCKER | SPEC | spec criterion 7 and 8, plan step 6 | `.claude/commands/workflow-start.md` (absent); `tests/test_workflow_entry.py:163,377`; `docs/WORKFLOW.md` header | The change promises the `/workflow-start` repository command — its spec refutes criterion 7 with "the command is absent", its Definition of Done lists `.claude/commands/workflow-start.md` as a document that moves with the behaviour, and criterion 8 requires the WORKFLOW notice to name `.claude/commands/` as supplied. No `.claude/commands/` file exists anywhere in the tree, the WORKFLOW missing-pieces notice still lists `.claude/commands/` among the absent pieces, and no recorded decision defers it (only the stop hook was split out). The acceptance test `test_workflow_start_delegates_to_scaffold` guards this with `skipif` on the file's absence, so `make verify` is green over an unmet criterion; a maintainer following the documented entry finds it does not exist. | mimo-v2.6-flash | fixed — tests/test_workflow_entry.py::test_missing_workflow_start_fails_outside_kit_probe | no — the full make verify after the repair stayed green | agree |
| L1-12 | MAJOR | SPEC | plan step 7 ("Files and steps") | `plans/changes/workflow-promises/{spec,plan,findings,decisions,research}.md` frontmatter; `plans/INDEX.md` rows | The plan promises, as an implementation step, to update `spec.md` and `plan.md` "for implementation status, ledger markers and time used" and to append implementation evidence. The time section moved, but all five artefacts still read `implementation_status: none`, and the regenerated `plans/INDEX.md` renders `none` for every row of this change, while the same diff ships the implemented Makefile targets, the gate catalog, the renderer and the new tests (a sibling in-flight change reads `partial`). Anyone reading the index concludes this change has built nothing, and the promised ledger markers were never written. | mimo-v2.6-flash | fixed — not a test — implementation_status partial on every artefact of the change, plans/INDEX.md regenerated (orchestrator acceptance at fe85b3e1) | no — the full make verify after the repair stayed green | agree |
| L1-13 | MINOR | MAINT | spec criterion 4's counter-check | `tests/test_workflow_entry.py` `_snapshot` (~line 240), `test_make_change_rejections_preserve_tree` | The tree-preservation counter-check records file bytes only — `_snapshot` keeps `p.is_file()` entries — so a residual empty `plans/changes/<name>/` directory left by a rejected `make change` passes the assertion, although criterion 4 refutes exactly "a residual folder" after a rejection. `scripts/new_change.py` creates the target directory before writing into it, so a failure between the two is precisely the case this check cannot see. | mimo-v2.6-flash | fixed — not a test — the snapshot helper lives in the test file itself, so no baseline red exists; tests/test_workflow_entry.py::test_snapshot_detects_residual_empty_directory pins it (orchestrator acceptance at fe85b3e1) | no — the full make verify after the repair stayed green | agree |
| L2-1 | MAJOR | SPEC | workflow-start.md | `.claude/commands/workflow-start.md` | The command runs `python3 scripts/new_change.py $ARGUMENTS` without quoting. The spec promises "arguments are data, not extra shell instructions" (detail in `plans/changes/workflow-promises/spec.md`). The Makefile's `change` target correctly quotes its arguments (`"$$NAME"`, `"$$BEAD"`), but the slash command does not. An argument containing shell metacharacters (`;`, `\|`, `&&`, etc.) would be interpreted by the shell rather than passed as data to the entry script. | longcat-2.0 | fixed — not a test — the command now checks the name and bead id against fixed patterns and runs the script with the two checked values single-quoted; it never hands raw arguments to the shell | no — tests/test_workflow_entry.py passed after the change | agree |
| L2-2 | MINOR | MAINT | plan-implementation mismatch | `plans/changes/workflow-promises/plan.md` | The plan's "Boundaries and route" section states "Neither `scripts/kit/manifest.yaml` nor `scripts/kit/probe.py` changes", but both files were modified during implementation (a kit-manifest rule for the new gate catalog, and `HARNESS_KIT_PROBE` in the probe). A maintainer reading the plan would not expect these files to carry changes from this pull request. | longcat-2.0 | fixed — not a test — plan.md now names the two kit-file changes and why | no — text only; no code or test changed | agree |
| L3-1 | MINOR | MAINT | reviewer | .claude/commands/workflow-start.md (name check) vs scripts/new_change.py NAME_PATTERN | The command's own name rule `^[a-z0-9][a-z0-9-]*$` is looser than the entry script's `^[a-z0-9]+(-[a-z0-9]+)*$`: a name like `abc-` or `a--b` passes the command's documented pre-check ("kebab-case, nothing else" — if it does not match, answer with usage and stop) but is rejected by the delegated `scripts/new_change.py` with a different BLOCK message, so the usage-vs-script-block boundary the command promises does not match the boundary that actually runs; a test comparing the command's pattern with `new_change.NAME_PATTERN` (e.g. over `abc-`, `a--b`, `ab`) shows the disagreement. | glm-5.3-flash | fixed — tests/test_workflow_entry.py::test_workflow_start_name_rule_matches_the_entry_script | no — tests/test_workflow_entry.py 19 passed | agree |
| L4-1 | MINOR | MAINT | plan.md step 6 / spec.md DETAIL vs the command file | .claude/commands/workflow-start.md | The command file carries YAML frontmatter (`description`, `argument-hint`), yet plan.md and spec.md state "No frontmatter belongs there" — a maintainer reading the plan could strip the frontmatter and break command registration, since Claude Code commands require it. | hy3 | fixed — not a test — plan.md now says no provenance frontmatter; the command keeps only Claude Code's own description and argument-hint keys | no — text only; no code or test changed | agree |
| L4-2 | MINOR | MAINT | .claude/commands/workflow-start.md vs scripts/new_change.py | .claude/commands/workflow-start.md | The command's bead pre-check `^coding-harness-[a-z0-9.]+$` is stricter than the entry script, which only checks the bead against the tracker export; a tracker-valid bead whose id contains a hyphen in the suffix (e.g. `coding-harness-abc-def`) would be refused by the command yet accepted by the script, so the two entry points disagree on a valid bead. | hy3 | rejected — every bead id in the tracker (252 on 2026-10-28) matches ^coding-harness-[a-z0-9.]+$; the prefix is fixed at init and suffixes carry no hyphen, so the command refuses no valid bead |  | disagree — No existing or pinned-tracker-generated bead ID rejected by this pattern is demonstrated. |
| L4-3 | MINOR | MAINT | decisions/gates.yaml → docs/governance/gate-catalog.md | docs/governance/gate-catalog.md | The catalog renders the `reason` column verbatim from the gate list, so German `reason` cells (`docs-links`, `ramp-valves`, …) sit inside an otherwise-English "readable view" with no note that the text is inherited from the gate list — a maintainer skimming the catalog cold meets untranslated prose. | hy3 | rejected — duplicate of L1-4: German reason cells are translated at their source, decisions/gates.yaml, in a pull request of its own (house rule 1, bead coding-harness-yim) |  | disagree — Verbatim source metadata is required; an explanatory language note is not an acceptance requirement. |
| L4-4 | MINOR | MAINT | scripts/kit/probe.py (_faelle) | scripts/kit/probe.py | `_faelle` unconditionally sets `HARNESS_KIT_PROBE=1` for the isolated probe's whole pytest run, so the exemption "only the kit probe may skip the repository command" is granted by the harness to every test in the probe rather than by the test's own marker — a coupling a maintainer editing the test would miss. | hy3 | rejected — intended: the probe runs the kit copy, where .claude/commands/ does not travel, so the whole probe run is the kit context; plan.md names the variable and why |  | disagree — Exporting the switch does not itself exempt tests; no unintended reader or skipped test is identified. |
| L5-1 | MINOR | MAINT | diff vs. plan.md "Boundaries and route" | plan.md · Boundaries and route; spec.md · Definition of Done | The plan states "No other production files are added, changed or deleted" and step 7 says to update "only" the missing-pieces notice and the §2 anchor in `docs/WORKFLOW.md`, and the DoD lists the moved documents as gate-catalog.md, WORKFLOW.md, workflow-start.md and INDEX.md — but the change also edits `docs/governance/quality-gates.md` and `docs/governance/regelwerk.md`. The boundary paragraph was amended for the two kit files ("added by the review-loop repair") but never for these two documents, so the plan's file accounting contradicts the diff it accompanies. | mimo-v2.6-pro | fixed — not a test — plan.md Boundaries names the two governance pages and why | no — full make verify green at fa9bfdf3 | agree |
| L5-2 | MINOR | MAINT | spec.md · Open decisions vs. plan.md · card and Time used | plans/changes/workflow-promises/spec.md (frontmatter `appetite: 2`, Open decisions "[DETAIL] Allow two hours of phase 4 … no smaller appetite is stated in the inputs") | The spec still records a two-hour appetite and claims the inputs state no other one, while plan.md records the maintainer's revised appetite of four hours (2026-10-27) and the measured use of about 3.9 h against it; the spec's stop rule and appetite field were never amended, so a reviewer comparing the two artefacts sees a run that appears to have over-run its declared appetite. | mimo-v2.6-pro | fixed — not a test — spec.md appetite 4 and the DETAIL names the maintainer's new appetite | no — full make verify green at fa9bfdf3 | agree |
| L5-3 | MINOR | MAINT | quality-gates.md rewrite in this change | docs/governance/quality-gates.md §4 ("Das Verdikt wird aus den Findings gerechnet (Gate-Katalog GK-8)") | The change rewrote this document's two other gate-catalog references (§3, §7) to describe the new catalog, but left §4's citation "(Gate-Katalog GK-8)" — an identifier no gate in `docs/governance/gate-catalog.md` or `decisions/gates.yaml` carries (ids are `pytest`, `ruff-check`, …). The reference now resolves to the newly created page, where "GK-8" does not exist, so a maintainer following it finds nothing. | mimo-v2.6-pro | fixed — not a test — the dead (Gate-Katalog GK-8) reference in quality-gates.md section 4 is dropped | no — full make verify green at fa9bfdf3 | agree |
| L5-4 | MINOR | MAINT | generated inventory rendered by this change | docs/governance/gate-catalog.md · rows `docs-links` and `ramp-valves` (reason column) | The new English page renders two `reason` cells in German ("Scharf geschaltet wird er, sobald bt8 …", "Ein Ventil ist ein datiertes Versprechen …"), against the repository's English-artefact rule that WORKFLOW.md's own language note states. `tests/test_gate_catalog.py` pins these cells verbatim to `decisions/gates.yaml`, so the strings cannot be translated in the catalog alone — the fix belongs in the protected gate list and needs a maintainer decision rather than a silent edit. | mimo-v2.6-pro | rejected — duplicate of L1-4 and L4-3: German reason cells are translated at their source, decisions/gates.yaml, in a pull request of its own (house rule 1, bead coding-harness-yim) |  | disagree — Translating the protected gate list would exceed this change’s scope and the repository requires separate translation changes. |
| L5-5 | MINOR | MAINT | manifest roles vs. the catalog's own promise | scripts/kit/manifest.yaml (rules for `docs/governance/gate-catalog.md`, `tests/test_gate_catalog.py`, catch-all `tests/`) | `docs/governance/gate-catalog.md`, `decisions/gates.yaml` and `scripts/ci_gates.py` all travel as `mechanismus`, and the catalog page promises that `tests/test_gate_catalog.py` fails the suite on any drifting row — but that test file gets no manifest entry of its own and falls under the `tests/` catch-all (`bestand`, stays behind), unlike every other holder of travelling mechanism (e.g. `tests/test_ci.py`, `tests/test_workflow_entry.py`). A kit consumer receives the drift-guard promise without the guard. | mimo-v2.6-pro | fixed — not a test — tests/test_gate_catalog.py travels as mechanismus in scripts/kit/manifest.yaml | no — full make verify green at fa9bfdf3 | agree |
| L6-1 | MINOR | SPEC | hy4-preview | `README.md` §"Not built yet", lines 303–306 (untouched by this change) | The front page still lists "slash commands, a `make change` shortcut (the script `scripts/new_change.py` exists; the target does not), and a catalogue of every gate: described in the doctrine, not built" — all three are supplied by this change, so the README now contradicts the re-dated notice in `docs/WORKFLOW.md`. The plan declares the broader README reconciliation a non-goal, but the change leaves the contradiction standing with no pointer to the new state. | hy4-preview | fixed — not a test — README.md "Not built yet" no longer lists the slash command, the make change shortcut or the gate catalog | no — full make verify at 64dad47a green except the ruleset gate, which could not reach GitHub (no network); the ruleset gate rerun green at 64dad47a | agree |
| L6-2 | MAJOR | MAINT | hy4-preview | `scripts/kit/probe.py`, `_faelle` (new line `umgebung["HARNESS_KIT_PROBE"] = "1"`) | The probe exports one unconditional environment switch into every test process of the throwaway repository, and nothing bounds which tests may honour it: any future test can read `HARNESS_KIT_PROBE` and vanish from the probe, raising the green quote without anything travelling — precisely the failure the comment directly above the line warns about. A scoped name, or a list of exemptions the probe asserts, would keep the exemption to the one test it was invented for. | hy4-preview | fixed — tests/test_workflow_entry.py::test_only_the_workflow_entry_test_reads_the_kit_probe_switch — a planted reader of HARNESS_KIT_PROBE in another file turned it red | no — full make verify at 64dad47a green except the ruleset gate, which could not reach GitHub (no network); the ruleset gate rerun green at 64dad47a | disagree — This describes a hypothetical future reader, without identifying a current unintended exemption or failing contract. |
| L6-3 | MINOR | SPEC | hy4-preview | `docs/governance/gate-catalog.md`, generated inventory, rows `docs-links` and `ramp-valves` | The page the workflow introduces in English carries two German `reason` cells ("Scharf geschaltet wird er, sobald bt8 …", "Ein Ventil ist ein datiertes Versprechen …"), and neither the page nor the drift test says the inventory is mixed-language; the fix belongs to `decisions/gates.yaml`, which is a protected area, so the reader is not told that the inconsistency is inherited. | hy4-preview | fixed — not a test — the catalog prose says the reason column is copied verbatim from decisions/gates.yaml and a German reason is translated there (bead coding-harness-yim) | no — full make verify at 64dad47a green except the ruleset gate, which could not reach GitHub (no network); the ruleset gate rerun green at 64dad47a | disagree — The inventory must reproduce source metadata; a mixed-language disclaimer is not an acceptance requirement. |
| L6-4 | MINOR | MAINT | hy4-preview | `docs/governance/quality-gates.md`, "Was diese Seite nicht sagt" (new English paragraph) and the HG-2 sentence ~7 lines below | Two edits a maintainer trips over: the German section now ends with an English paragraph and English "Verwandtes" labels, mixing languages inside one page; and the removed "Das Verdikt wird aus den Findings gerechnet (Gate-Katalog GK-8)" left the sentence without any source for how the verdict is computed, while the reflow into a single ~110-character line adds a new finding to the report-only markdownlint gate. | hy4-preview | fixed — not a test — the dead (Gate-Katalog GK-8) reference is gone and the HG-2 sentence rewrapped; the language mix is rejected: German in governance pages is translated in a pull request of its own (house rule 1, bead coding-harness-yim) | no — full make verify at 64dad47a green except the ruleset gate, which could not reach GitHub (no network); the ruleset gate rerun green at 64dad47a | disagree — Language mixing and line length are style concerns; removing the nonexistent GK-8 citation does not remove a usable source. |
| L6-5 | MINOR | MAINT | hy4-preview | `.claude/commands/workflow-start.md`, argument checking (lines 8–20) | The command requires a name and `--bead <id>` and answers surplus or malformed input only for those two: nothing says what happens to extra tokens (for example `/workflow-start foo --bead coding-harness-x --force`), so the model silently drops them instead of answering with the usage line, and no test covers that case. | hy4-preview | fixed — not a test — .claude/commands/workflow-start.md answers any extra token with the usage line | no — full make verify at 64dad47a green except the ruleset gate, which could not reach GitHub (no network); the ruleset gate rerun green at 64dad47a | agree |
| L7-1 | MAJOR | SPEC | spec | README.md | The spec's Protected areas places `README.md` "outside this bounded package" and its Non-goals says broader README reconciliation remains separate, yet the diff rewrites README.md's "Not built yet" list — work the spec explicitly excludes. | deepseek-v4-pro | fixed — not a test — spec Non-goals and Protected areas name the README "Not built yet" list as the one README edit (row L6-1) | no — text-only edit of spec.md and plan.md; full make verify at 64dad47a green, its ruleset gate rerun green after the network came back | agree |
| L7-2 | MINOR | MAINT | plan | plans/changes/workflow-promises/plan.md · plans/changes/workflow-promises/spec.md | The plan's "Boundaries and route" claims "No other production files are added, changed or deleted" and the Definition of Done lists only four moved documents, but the diff also changes README.md, docs/governance/quality-gates.md and docs/governance/regelwerk.md; README.md appears in no file list, so a maintainer reconstructing scope cannot see it was touched. | deepseek-v4-pro | fixed — not a test — plan Boundaries and route names the README edit; the Definition of Done points to that list | no — text-only edit of spec.md and plan.md; full make verify at 64dad47a green, its ruleset gate rerun green after the network came back | agree |
| L7-3 | MINOR | MAINT | diff | docs/governance/quality-gates.md · docs/governance/regelwerk.md | English prose replaces the German "Gate-Katalog" references inside otherwise German documents (quality-gates.md §3 and §7 "Verwandtes", regelwerk.md §8), leaving mixed-language governance pages. | deepseek-v4-pro | rejected — duplicate of L1-4, L4-3 and L6-4: German governance prose is translated in a pull request of its own, and new text is English (house rule 1, bead coding-harness-yim) |  | disagree — English replacement text follows repository policy; translating the surrounding legacy document is outside scope. |
| L8-1 | MINOR | MAINT | readability | docs/governance/quality-gates.md §3 and §7; docs/governance/regelwerk.md §8 | The review-loop edits rewrote German prose and German link descriptions into English — a full English paragraph in quality-gates.md §3 ("The gate catalog lists the declared machine gates...") and the §7/§8 "Gate catalog" link labels — leaving English sentences inside otherwise wholly German governance documents. | glm-5.2 | rejected — duplicate of L1-4, L4-3, L6-4 and L7-3: German governance prose is translated in a pull request of its own, and new text is English (house rule 1, bead coding-harness-yim) |  | disagree — Repeats the language-style objection without new correctness evidence; repository policy requires English additions. |
| L8-2 | MINOR | MAINT | code | tests/test_workflow_entry.py::_fixture_tree | The `name` parameter is rebound by the `for name in ENTRY_SCRIPTS` loop, shadowing the argument; any later reference to `name` in that function would silently read the loop's last value instead of the passed tree name. | glm-5.2 | fixed — not a test — the fix lives in the test helper: tests/test_workflow_entry.py::_fixture_tree loops over `script`, no longer rebinding its `name` argument | no — full make verify green at 4db90ba3 | disagree — The parameter is consumed before the loop and never read afterward; no input produces an incorrect result. |
| L9-1 | MINOR | MAINT | base | `.claude/commands/workflow-start.md` (the bead-id pre-check) | The command pre-checks the bead id against `^coding-harness-[a-z0-9.]+$`, a shape that exists nowhere else in the repository: the delegated entry script `scripts/new_change.py` deliberately imposes no bead-id pattern (it accepts any id present in the export), and while the name rule is pinned to the script's own `NAME_PATTERN` by `tests/test_workflow_entry.py::test_workflow_start_name_rule_matches_the_entry_script`, no test and no source holds the bead pattern. A bead id outside it — for instance the hyphenated slug form a tracker can issue — is refused with usage by this one entry while `make change` and the direct script accept it, and the wrapper can drift from the entry silently because nothing compares the two. | glm-5.3 | rejected — the pattern is the tracker's fixed prefix (house rule 3: set at init, cannot change) plus the id alphabet bd issues, hierarchical ids included; it is the Markdown command's quoting guard, and make change and the entry script still refuse an id the export does not hold |  | disagree — Repeats L4-2 without demonstrating a tracker-valid ID that this repository’s command rejects. |
| L9-2 | MINOR | MAINT | base | `Makefile`, target `change` (the `$(if $(NAME),...)` guard) | The presence guard reads `NAME` and `BEAD` from the process environment as well as from the command line: a stray exported `NAME` or `BEAD` in the shell passes the guard and starts folder creation with an unintended value, and nothing distinguishes an argument from an ambient variable — unlike the wrapper, whose text pre-check at least names what it received. | glm-5.3 | fixed — tests/test_workflow_entry.py::test_make_change_rejections_preserve_tree — new cases ambient-name and ambient-bead: an exported NAME or BEAD no longer passes the guard; both cases fail against the previous Makefile | no — full make verify green at dcb9af49 | disagree — Make conventionally accepts environment variables; the specification required nonempty inputs, not command-line-only origins. |
| L9-3 | MINOR | SPEC | base | `plans/changes/workflow-promises/spec.md` (frontmatter `appetite: 4` and Open decisions) and `plans/changes/workflow-promises/plan.md` (card "Appetite: 4 hours" vs "Time used") | The change's own artefacts disagree on the operative limit: the spec frontmatter and the plan card still declare four hours (raised 2026-10-27), while `plan.md` "Time used" records the maintainer's later decision of five hours in total (2026-10-28) that governs the change — a reader of either document alone gets the wrong appetite. | glm-5.3 | fixed — not a test — spec appetite 5 with the DETAIL naming both answers; the plan card states 5 hours | no — full make verify green at dcb9af49 | agree |
| L9-4 | MINOR | MAINT | base | `docs/governance/gate-catalog.md`, generated inventory between the markers | Every generated row is a single line of roughly 200 to 500 characters, so the report-level markdownlint gate (whose globs cover `docs/governance/`) gains about two dozen MD013 line-length findings that the do-not-edit markers make permanently unclearable — the new catalog grows the very report stock that gate's report level exists to hold down, and a maintainer trying to clear the stock will find these rows unfixable without abandoning the generated design. | glm-5.3 | fixed — not a test — the generated block is wrapped in markdownlint-disable MD013 MD060; the catalog's markdownlint findings went from 41 to 1 (MD025, shared by the repository's frontmatter pages) | no — full make verify green at dcb9af49 | disagree — Generated table line lengths are style findings in a report-only linter; no acceptance criterion or blocking gate fails. |

Rounds run: 9

Record digest: sha256:88731e464e6c75481334ea36034e99e7f3e572283065e4a48d714e78c4a14b4b

Record identity: sha256:f34bb924b06eb9f972a2bfaf0d8a68f4d94fdd7978e6179aa7503746c7f1b05c

Cut rounds: 1, 2, 3, 4, 5, 6, 7, 8, 9

Loop state: {"availability": {"checked_at": "2026-10-27T22:24:18+00:00", "failed": {"cat-jam-free": "pi call failed: exit 1: 400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Model is unavailable.\"}", "longcat-2.5-preview-free": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model longcat-2.5-preview-free has been deprecated.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: [400] Unsupported model mimo-v2.5-pro\"}"}, "reachable": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"], "skipped": {"gemini-4-argon-contributor": "not admitted; data terms have not been read", "gpt-5.6-luna": "not admitted; data terms have not been read", "grok-4.6": "not admitted; data terms have not been read", "grok-4.7": "not admitted; data terms have not been read", "kimi-k2.7-code": "not admitted; data terms have not been read", "kimi-k3": "not admitted; data terms have not been read", "minimax-m2.7": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read", "space-bunny": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured)", "gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured)", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured)", "minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured)", "qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured)", "qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured)"], "terms_warnings": ["the data terms of deepseek-v4.1-flash expire on 2026-10-31 (4 days left)", "the data terms of deepseek-v4-pro expire on 2026-10-31 (4 days left)"]}, "consumed": ["flash", "rung:longcat-2.0", "rung:glm-5.3-flash", "rung:hy3", "rung:mimo-v2.6-pro", "rung:hy4-preview", "rung:deepseek-v4-pro", "rung:glm-5.2", "rung:glm-5.3"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "big-pickle", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-flash", "provider": "opencode"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "exo-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "ling-3.0-flash-fin-free", "provider": "opencode"}, {"model": "ling-3.1-flash-free", "provider": "opencode"}, {"model": "longcat-2.5-preview-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-spark-1.3-contributor-free", "provider": "opencode"}, {"model": "nemotron-3-ultra-free", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "space-bunny-free", "provider": "opencode"}, {"model": "step-5-preview-free", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-flash", "provider": "opencode-go"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon-contributor", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.6", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-preview-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m2.7", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "space-bunny", "provider": "opencode-go"}, {"model": "step-5-preview-free", "provider": "opencode-go"}], "checked_at": "2026-10-27T22:22:09+00:00", "dropped": {}, "models_store": {"opencode-go": {"checkedAt": 1793139728376, "etag": "W/\"65e1c3b71054c3b1741fe4cb46560dbf\"", "lastModified": 1792068066000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "cat-jam-free", "input": ["text"], "maxTokens": 131072, "name": "Cat Jam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"forceAdaptiveThinking": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro (New)", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/v1", "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 0, "input": 4, "output": 20}, "id": "gemini-4-argon-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.6", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.6", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 0, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "LongCat 2.5 Preview Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 204800, "cost": {"cacheRead": 0.06, "cacheWrite": 0.375, "input": 0.3, "output": 1.2}, "id": "minimax-m2.7", "input": ["text"], "maxTokens": 131072, "name": "MiniMax-M2.7", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "space-bunny", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 524288, "name": "Space Bunny", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "step-5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "overlay": ["cat-jam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon-contributor", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.6", "grok-4.7", "hy3", "hy4-preview", "kimi-k2.7-code", "kimi-k3", "longcat-2.0", "longcat-2.5-preview-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m2.7", "minimax-m3", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "space-bunny", "step-5-preview-free"], "pi_version": "1.2.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": [], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"], "rungs": ["longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"]}}

Kept from the loop record:

> Notice: paid models skipped: qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured); gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured); minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured); qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured); qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured).
> Notice: in the live catalog without a terms reading: gemini-4-argon-contributor, gpt-5.6-luna, grok-4.6, grok-4.7, kimi-k2.7-code, kimi-k3, minimax-m2.7, muse-spark-1.2-contributor, muse-spark-1.3-contributor, space-bunny.
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (4 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (4 days left).
> mimo-v2.5 was asked again with the format reminder: the first answer was malformed
> The diff was cut: the change diff was cut at 2000 of 2005 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From mimo-v2.5:
> mimo-v2.5's first answer, which was not in the required format:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> | ID | Severity | Dimension | Origin | Where |
> |---|---|---|---|---|
> | R1-1 | BLOCKER | SPEC | code | Makefile, `change` target — the recipe runs `python3 scripts/new_change.py "$$NAME"` and passes BEAD only as an exported environment variable; the `--bead` flag is never handed to the entry script, while the spec, plan and tests all describe and assert the documented invocation `scripts/new_change.py <name> --bead <id>` (`test_make_change_delegates_to_scaffold` asserts `--bead` and the bead id in the invocation log). The delegation is asymmetric and undocumented: success silently depends on `new_change.py` reading BEAD from the environment — an interface no document names — and breaks the moment the script's documented contract (positional name plus `--bead` flag) is what it enforces. |
> | R1-2 | MAJOR | SPEC | spec-vs-code | plans/changes/workflow-promises/spec.md, criterion 6 — the criterion promises `make help` lists "`change`, `index` and `help` alongside the existing public targets", but `tests/test_workflow_entry.py::test_make_help_lists_targets_without_side_effects` additionally demands `verify`, `test`, `staleness`, `gates`, `leakcheck`, `venv` and `lock` by name. As written, a Makefile listing only the three named targets plus `change`/`index` would satisfy the spec while failing the test; the spec's enumeration is not what the change enforces. |
> | R1-3 | MINOR | MAINT | code | tests/test_gate_catalog.py, `_drift` — for a duplicate row, `_drift` records only `duplicate row: <id>` and never compares the duplicate against the declared gate, so a table with the same id rendered twice with conflicting cells reports one finding, not two, and the second copy's field drift stays unmeasured. |
> 
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> longcat-2.0 was asked again with the format reminder: the first answer was malformed
> The diff was cut: the change diff was cut at 2000 of 2349 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From longcat-2.0:
> longcat-2.0's first answer, which was not in the required format:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> Based on my thorough review of the implementation against the spec, I've analyzed all 9 acceptance criteria and the supporting code.
> 
> Key findings from my analysis:
> 
> 1. **All 9 acceptance criteria are satisfied**: The gate catalog renders correctly from `decisions/gates.yaml`, `make change`/`make index`/`make help` delegate properly, rejections preserve the tree, `/workflow-start` delegates to the entry script, the WORKFLOW.md notice names supplied pieces at a dated baseline (`e61554b0`), and the §2 anchor now resolves to the English `Before enabling a gate` heading.
> 
> 2. **The `_drift` comparator in `test_gate_catalog.py` is correctly implemented**: It adds row IDs to track duplicates, reports extras, detects missing declared gates, and compares every displayed field using an independently authored formatter (`_expected_cells`), satisfying criterion 2's requirement that a renderer compared only with itself cannot hold the tests green.
> 
> 3. **The Makefile `change` target passes arguments safely**: NAME and BEAD are passed through exported environment variables (`"$$NAME"`, `"$$BEAD"`), never interpolated into the shell line — arguments stay data, not code.
> 
> 4. **The `/workflow-start` command** correctly requires both name and `--bead`, delegates to `scripts/new_change.py`, and surfaces the script's output unchanged.
> 
> 5. **The kit probe skip guard** is correctly implemented: `HARNESS_KIT_PROBE=1` is set by the probe, and the `@COMMAND_SKIP` marker skips the command test only when that env var is set and the command file is absent — the traveling copy stays green without a new `REIST_NICHT` entry.
> 
> 6. **The `catalog_rows` renderer** handles all field types distinctly (command vs. hosted-only action vs. action with local equivalent), escapes pipes/newlines, and keeps the existing CLI modes byte-unchanged.
> 
> No finding.
> 
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> The diff was cut: the change diff was cut at 2000 of 2362 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> The diff was cut: the change diff was cut at 2000 of 2377 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From hy3:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> Based on a thorough read of the worktree (the on-disk `test_gate_catalog.py` already differs from the truncated diff — the drift assertion was fixed to `[rows[0], gelogen, rows[2]]`), and verification of `new_change.py`, `catalog_rows()`, `gates()`, the Makefile targets, and the `workflow-start` command, the change is well-covered by tests. The genuine issues are latent/consistency ones a maintainer would trip over:
> 
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> The diff was cut: the change diff was cut at 2000 of 2381 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> The diff was cut: the change diff was cut at 2000 of 2409 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> The diff was cut: the change diff was cut at 2000 of 2459 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> The diff was cut: the change diff was cut at 2000 of 2468 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> The diff was cut: the change diff was cut at 2000 of 2470 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.

<!-- End of released loop record -->

Stage-2 call, 2026-10-28: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 720 files, 2449 commits, 12 rules.

Stage-2 call, 2026-10-28: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 720 files, 2453 commits, 12 rules.

## Phase 6 — Codex, 2026-10-28

Codex reported no finding.

The answer was not only six-cell rows; what is not one is kept below as it came.

> No finding.

Phase 6 verdict: codex 01a182fd-4309-7ec3-aeac-b303c96f1d88, 2026-10-28
Reviewer session: codex 01a182fd-4309-7ec3-aeac-b303c96f1d88 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check
