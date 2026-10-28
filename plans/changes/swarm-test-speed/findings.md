---
title: "Findings — swarm-test-speed"
category: findings
status: draft
implementation_status: none
date: 2026-10-28
created: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-dca4
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — swarm-test-speed

Stage-2 call, 2026-10-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 715 files, 2468 commits, 12 rules.

Stage-2 call, 2026-10-28: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 718 files, 2472 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/swarm-test-speed/plan.md` +7 -7
> - `scripts/stage2_availability.py` +47 -4
> - `tests/test_stage2_declaration.py` +450 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 56 lines of this gate left out …]
> ........................................................................ [ 94%]
> ........................................................................ [ 96%]
> ........................................................................ [ 98%]
> .......................................................................  [100%]
> =================================== FAILURES ===================================
> ________________ test_reader_selects_safe_loader_with_fallback _________________
> [gw5] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/swarm-test-speed/.venv/bin/python3
>
> root = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1069/popen-gw5/test_reader_selects_safe_loade0/repo')
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10821a9c0>
>
>     def test_reader_selects_safe_loader_with_fallback(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
>         """Criterion 1: a safe loader parses, the unsafe tag is refused, and a missing C loader loses no read."""
>         # Distinct contents: this test counts its own parses in the shared process-local cache.
>         text = NESTED + "loader-test: unique\n"
>         path = write(root, text)
>         calls = patch_load_counter(monkeypatch)
>         data = availability.read_declaration(root)
>         assert isinstance(data, dict) and data["loader-test"] == "unique"
>         assert len(calls) == 1
>         if getattr(yaml, "__with_libyaml__", False):
>             assert calls[0][1] is yaml.CSafeLoader, "the C safe loader was not chosen although it is available"
>         else:
>             assert calls[0][1] is yaml.SafeLoader
>     
>         # An unsafe tag is refused, not executed - planted fault: a full loader would return a mapping.
>         path.write_text('!!python/object/apply:os.system ["echo no"]\n', encoding="utf-8")
>         assert availability.read_declaration(root) == REFUSAL
>     
>         if hasattr(yaml, "CSafeLoader"):
>             # Without the C loader the pure-Python safe loader serves the same read: a different
>             # loader is a different cache key, so this parse happens again under SafeLoader.
>             monkeypatch.delattr(yaml, "CSafeLoader")
>             path.write_text(text, encoding="utf-8")
>             data = availability.read_declaration(root)
> >           assert len(calls) == 2, "the fallback loader reused the C loader's cache entry"
> E           AssertionError: the fallback loader reused the C loader's cache entry
> E           assert 3 == 2
> E            +  where 3 = len([('endpunkte:\n  - name: opencode-go\n    residenz: "München — EU-Rechenzentrum ✓"\n    darf_sehen: [framework, public... &anchor\n  key: value\n  keep: [1, 2]\nalias_user: *anchor\nloader-test: unique\n', <class 'yaml.loader.SafeLoader'>)])
>
> tests/test_stage2_declaration.py:203: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=9300) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/swarm-test-speed/tests/test_stage2.py:16286: DeprecationWarning: This process (pid=9296) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2_declaration.py::test_reader_selects_safe_loader_with_fallback
> 1 failed, 4085 passed, 17 skipped, 5 warnings in 688.29s (0:11:28)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> tests/test_stage2_declaration.py:222:5: F841 Local variable `path` is assigned to but never used
>     |
> 220 |     """
> 221 |     text = "reuse: yes\nmarker: bounded-cache-test\n"
> 222 |     path = write(root, text)
>     |     ^^^^ F841
> 223 |     calls = patch_load_counter(monkeypatch)
> 224 |     first = availability.read_declaration(root)
>     |
>     = help: Remove assignment to unused variable `path`
>
> tests/test_stage2_declaration.py:283:5: PTH105 `os.replace()` should be replaced by `Path.replace()`
>     |
> 281 |     temporary.write_text(replaced_text, encoding="utf-8")
> 282 |     before = path.stat()
> 283 |     os.replace(temporary, path)
>     |     ^^^^^^^^^^ PTH105
> 284 |     os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
> 285 |     after = path.stat()
>     |
>
> Found 2 errors.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ── [ruff-check] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 20801 earlier lines left out …]
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

Stage-2 call, 2026-10-28: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 719 files, 2480 commits, 12 rules.
