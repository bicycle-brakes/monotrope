---
title: "Findings — review-diff-order"
category: findings
status: draft
implementation_status: none
date: 2026-10-29
created: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-ut8q
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — review-diff-order

Stage-2 call, 2026-10-29: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 734 files, 2638 commits, 12 rules.

Stage-2 call, 2026-10-29: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 737 files, 2645 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +9 -3
> - `plans/changes/review-diff-order/plan.md` +7 -7
> - `prompts/04b-review-loop.md` +8 -3
> - `scripts/stage2.py` +75 -1
> - `tests/test_stage2.py` +229 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `scripts/stage2.py`.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 76 lines of this gate left out …]
>         (root / "src" / "doomed.py").write_text("DOOMED = 1\n", encoding="utf-8")
>         (root / "src" / "moved_from.py").write_text("MOVED = 1\n", encoding="utf-8")
>         (root / "src" / "[bracket].py").write_text("BRACKET = 1\n", encoding="utf-8")
>         git(root, "add", "-A")
>         git(root, "commit", "-qm", "files that will change state")
>         # Every state at once: unstaged, staged, untracked, deleted, renamed, and names that stress the pathspec.
>         (root / "src" / "app.py").write_text("value = 2\n", encoding="utf-8")
>         (root / "src" / "staged.py").write_text("STAGED = 1\n", encoding="utf-8")
>         git(root, "add", "src/staged.py")
>         (root / "src" / "untracked.py").write_text("UNTRACKED = 1\n", encoding="utf-8")
>         (root / "src" / "with space.py").write_text("SPACED = 1\n", encoding="utf-8")
>         (root / "src" / "new\nline.py").write_text("NEWLINE_NAME = 1\n", encoding="utf-8")
>         (root / "src" / "[bracket].py").write_text("BRACKET = 2\n", encoding="utf-8")
>         (root / "src" / "doomed.py").unlink()
>         git(root, "mv", "src/moved_from.py", "src/moved_to.py")
>         (root / "src" / "crlf.py").write_bytes(b"FIRST = 1\r\nSECOND = 2\r\n")
>         diff = stage2.paid_review_diff(root)
>         for marker in (
>             "+COMMITTED = 2",  # committed
>             "+STAGED = 1",  # staged
>             "+value = 2",  # unstaged, with its removed side below
>             "-value = 1",
>             "+UNTRACKED = 1",  # untracked
>             "-DOOMED = 1",  # deleted
>             "-MOVED = 1",  # the rename's deletion side
>             "+MOVED = 1",  # and its addition side
>             "+BRACKET = 2",  # a tracked pathspec-metacharacter name
>             "+SPACED = 1",  # a space in the name
>             "+NEWLINE_NAME = 1",  # a newline in the name
>             "+SECOND = 2\r\n",  # the original CRLF line ends
>         ):
> >           assert diff.count(marker) == 1, marker
> E           AssertionError: -DOOMED = 1
> E           assert 0 == 1
> E            +  where 0 = <built-in method count of str object at 0x74d4d08000>('-DOOMED = 1')
> E            +    where <built-in method count of str object at 0x74d4d08000> = 'diff --git a/scripts/helper.py b/scripts/helper.py\nnew file mode 100644\nindex 0000000..c8fcecd\n--- /dev/null\n+++ ...\nnew file mode 100644\nindex 0000000..c651577\n--- /dev/null\n+++ b/src/with space.py\t\n@@ -0,0 +1 @@\n+SPACED = 1\n'.count
>
> tests/test_stage2.py:1233: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=91160) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=91167) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/review-diff-order/tests/test_stage2.py:16763: DeprecationWarning: This process (pid=91170) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_paid_review_diff_preserves_retained_file_diffs
> 1 failed, 4092 passed, 17 skipped, 5 warnings in 561.02s (0:09:21)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 21791 earlier lines left out …]
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

Stage-2 call, 2026-10-29: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 737 files, 2646 commits, 12 rules.
