---
title: "Findings — research-store-home"
category: findings
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-nxdy
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — research-store-home

Stage-2 call, 2026-11-04: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 889 files, 3290 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-store-home/plan.md` +131 -0
> - `plans/changes/research-store-home/spec.md` +150 -0
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/research-store-home/findings.md: stale — updated 2026-11-04 is older than its last change 2026-11-05 (uncommitted)
> plans/changes/research-store-home/plan.md: stale — updated 2026-11-04 is older than its last change 2026-11-05 (uncommitted)
> plans/changes/research-store-home/spec.md: stale — updated 2026-11-04 is older than its last change 2026-11-05 (uncommitted)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 30934 earlier lines left out …]
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
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-05: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 892 files, 3291 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-05: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 892 files, 3294 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +21 -0
> - `plans/changes/research-store-home/plan.md` +7 -7
> - `scripts/research_capture.py` +22 -19
> - `scripts/stage2_research_run.py` +15 -3
> - `scripts/stage2_research_store.py` +49 -12
> - `tests/test_research_capture.py` +23 -2
> - `tests/test_stage2_research_deep_review.py` +12 -8
> - `tests/test_stage2_research_store.py` +111 -15
> - `tests/test_stage2_swarm.py` +69 -5
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_stage2_swarm.py`.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ......F..............                                                    [100%]
> =================================== FAILURES ===================================
> _________ test_research_store_keeps_change_and_resolved_worktree_keys __________
> [gw5] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-store-home/.venv/bin/python3
>
> self = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-912/popen-gw5/test_research_store_keeps_chan0/deeper/..')
> mode = 511, parents = True, exist_ok = False
>
>     def mkdir(self, mode=0o777, parents=False, exist_ok=False):
>         """
>         Create a new directory at this given path.
>         """
>         try:
> >           os.mkdir(self, mode)
> E           FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-912/popen-gw5/test_research_store_keeps_chan0/deeper/..'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1311: FileNotFoundError
>
> During handling of the above exception, another exception occurred:
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-912/popen-gw5/test_research_store_keeps_chan0')
> state_home = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-912/popen-gw5/test_research_store_keeps_chan0/research-state')
>
>     def test_research_store_keeps_change_and_resolved_worktree_keys(tmp_path, state_home):
>         # Criterion 4. Planted fault: two changes or two spellings of one resolved worktree share a store,
>         # or aliases of one resolved root split it.
>         m = module()
>         root = tmp_path / "worktree"
>         root.mkdir()
>         alias = tmp_path / "link-to-worktree"
>         alias.symlink_to(root)
>         through = tmp_path / "deeper" / ".." / "worktree"
> >       through.parent.mkdir(parents=True)
>
> tests/test_stage2_research_store.py:386: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1316: in mkdir
>     self.mkdir(mode, parents=False, exist_ok=exist_ok)
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> self = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-912/popen-gw5/test_research_store_keeps_chan0/deeper/..')
> mode = 511, parents = False, exist_ok = False
>
>     def mkdir(self, mode=0o777, parents=False, exist_ok=False):
>         """
>         Create a new directory at this given path.
>         """
>         try:
> >           os.mkdir(self, mode)
> E           FileExistsError: [Errno 17] File exists: '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-912/popen-gw5/test_research_store_keeps_chan0/deeper/..'
>
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1311: FileExistsError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_store.py::test_research_store_keeps_change_and_resolved_worktree_keys
> 1 failed, 20 passed in 17.06s
> ```

Stage-2 call, 2026-11-05: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 892 files, 3297 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 892 files, 3301 commits, 12 rules.

Stage-2 call, 2026-11-05: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 892 files, 3305 commits, 12 rules.
