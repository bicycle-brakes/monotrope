---
title: "Findings — swarm-test-speed"
category: findings
status: draft
implementation_status: partial
date: 2026-10-28
created: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-29
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

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 719 files, 2484 commits, 12 rules.

Stage-2 call, 2026-10-28: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 719 files, 2486 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2_declaration.py` +55 -14
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-4: tests/test_stage2_declaration.py::test_read_failure_never_returns_a_cached_declaration: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - L1-5: tests/test_stage2_declaration.py::test_returned_declarations_are_isolated_across_threads: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/swarm-test-speed/stage2/attempts/swarm-test-speed/attempt-1-20261028T180737723958Z-c2ccb98f.md
> ```

Stage-2 call, 2026-10-28: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 719 files, 2487 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-4: no fixed line
> - L1-5: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/swarm-test-speed/stage2/attempts/swarm-test-speed/attempt-2-20261028T180737723958Z-c2ccb98f.md
> ```

Stage-2 call, 2026-10-28: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 719 files, 2488 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-4: tests/test_stage2_declaration.py::test_read_failure_never_returns_a_cached_declaration: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - L1-5: tests/test_stage2_declaration.py::test_returned_declarations_are_isolated_across_threads: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/swarm-test-speed/stage2/attempts/swarm-test-speed/attempt-3-20261028T180737723958Z-c2ccb98f.md
> ```

Stage-2 call, 2026-10-28: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 719 files, 2511 commits, 12 rules.

Stage-2 call, 2026-10-28: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 732 files, 2514 commits, 12 rules.

## Phase 6 — Codex, 2026-10-28

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MAJOR | SPEC | Phase 6 | scripts/stage2_availability.py:596 | Selecting `CSafeLoader` changes the reader’s acceptance contract. Reproduced with PyYAML 6.0.2: `endpunkte: []\t# ordinary inline comment\n` returns `{'endpunkte': []}` with the new reader, while the baseline and fallback `SafeLoader` return `model-endpoints.yaml cannot be read`. The same declaration therefore succeeds or fails depending on libyaml availability; preserve the baseline refusal behavior. [Criterion 1] | Codex | fixed — tests/test_stage2_declaration.py::test_reader_preserves_safe_loader_tab_contract | — |
| F6-2 | MAJOR | SPEC | Phase 6 | plans/changes/swarm-test-speed/plan.md:130 | The recorded before/after measurements ran alongside another session’s `make verify`; the evidence explicitly states that the machine was not isolated. Alternating runs under concurrent load does not establish the required isolated comparison. Record three successful unprofiled runs per revision under matched isolated conditions before treating the speed criterion as met. [Criterion 7] | Codex | fixed — not a test — three alternating runs per revision inside one hold of the machine's verify lock, 2026-10-29 07:42–07:43 UTC, median 14.91 s before (`5c4ddcbd`) and 9.51 s after (`703869a3`); plan.md, Isolated re-measurement — 2026-10-29 | no — text and measurement only |

Phase 6 verdict: codex 01a18477-e23b-72d1-8402-5dbe905cbdaa, 2026-10-28
Reviewer session: codex 01a18477-e23b-72d1-8402-5dbe905cbdaa — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-10-28

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | spec criterion 7, plan steps 1, 5, 6 | plans/changes/swarm-test-speed/plan.md:37-42, 69-74, 95, 120-133 | The change never records the measurement its own criterion 7 and "Done when" require: the plan holds only three before runs explicitly marked as disturbed by a concurrent verify, defers the repeat to a promise, and shows no after runs, no after median, no full-suite timing and no node-ID comparison, so neither the speedup nor criterion 8's comparison is evidenced and the ledger line for criterion 7 ("recorded here") is false. | deepseek-v4.1-flash | fixed — not a test — matched before/after runs recorded in plan.md, Measurement (0f08614a); full-suite timing recorded with the post-repair make verify | no — text and measurement only | agree |
| L1-2 | MINOR | MAINT | plan.md header vs baseline section vs research.md | plans/changes/swarm-test-speed/plan.md:30, plan.md:120-128, plans/changes/swarm-test-speed/research.md baseline paragraph | The plan names one commit as its baseline in the header, the measurement section names a second and research.md a third, with nothing reconciling them; a maintainer cannot tell which tree the before numbers belong to or which tree an after number would have to match. | deepseek-v4.1-flash | fixed — not a test — plan.md Measurement names 5c4ddcbd as before and reconciles ae855930 and 7bc010f0 (0f08614a) | no — text and measurement only | agree |
| L1-3 | MINOR | MAINT | research.md template leftovers | plans/changes/swarm-test-speed/research.md:26-33 | The template blockquote is left in the filled research file: it instructs the filler to set `provenance: ai-drafted-reviewed` because "the frontmatter says `provenance: human-written`" although the frontmatter already says `ai-drafted-reviewed`, and "this file is empty until it has run" stands above a full report, so a reader is told to redo finished work and to doubt the file's state. | deepseek-v4.1-flash | fixed — not a test — template leftovers removed from research.md (0f08614a) | no — text and measurement only | agree |
| L1-4 | MINOR | MAINT | tests/test_stage2_declaration.py criterion-4 test | tests/test_stage2_declaration.py:328-331 | The repeated read of the malformed declaration and its message "the refusal was cached and stopped being attempted" cannot fail if refusals were cached — both calls return the same refusal either way — so the plan's promise that read failures are never cached is asserted rather than tested; only the later recovery check can expose a stale refusal. | deepseek-v4.1-flash | fixed — tests/test_stage2_declaration.py::test_read_failure_never_returns_a_cached_declaration — hand acceptance: red with a planted fault that caches the refusal, the round-1 version green with that fault, green at cf71a96c | no — 24 passed in tests/test_stage2_declaration.py at cf71a96c; full make verify follows | agree |
| L1-5 | MINOR | SPEC | plan step 3 ("ordinary concurrent cache misses may parse twice; they must not corrupt results") and step 4 | tests/test_stage2_declaration.py:348-382 with plans/changes/swarm-test-speed/plan.md:52-68 | The only threaded test warms the cache before the threads start, so every thread takes the cache-hit path; concurrent misses, the concurrent insert/overwrite of one key and eviction while another thread parses are untested, and a later change to the store path could break them without a red test. | deepseek-v4.1-flash | fixed — tests/test_stage2_declaration.py::test_returned_declarations_are_isolated_across_threads — hand acceptance: red with a planted fault that returns the shared object to a losing concurrent miss ("a nested mutation reached another caller's read"), the round-1 version green with that fault, green at cf71a96c | no — 24 passed in tests/test_stage2_declaration.py at cf71a96c; full make verify follows | agree |
| L1-6 | MINOR | MAINT | plan.md status sentences and artefact frontmatter | plans/changes/swarm-test-speed/plan.md:34 and the five new frontmatter blocks mirrored in plans/INDEX.md | plan.md still says "This runner draft stops before implementation" and every artefact plus its generated index row says `implementation_status: none`, while the same plan records the accepted implementation and this diff ships it; the registry publishes unbuilt work that is built. | deepseek-v4.1-flash | fixed — not a test — plan status sentence updated, implementation_status partial in all five files (25d92545, 0f08614a) | no — text and measurement only | agree |
| L1-7 | MAJOR | SPEC | spec.md criterion 7 and Definition of Done | plans/changes/swarm-test-speed/plan.md, sections "Baseline measurement" and "Time used" | The change promises three matched before/after runs whose medians prove the speedup, recorded in plan.md, but the diff contains only the before-side numbers, explicitly labelled disturbed by a concurrent verify run, and no after-side measurement, median, result counts or implementation revision anywhere; as submitted the speedup claim is unproven and criterion 7 plus the Definition of Done cannot be judged, so the change does not do what it promises. | mimo-v2.5 | fixed — not a test — same fix as L1-1 | no — text and measurement only | agree |
| L1-8 | MINOR | SPEC | plan.md step 2 | plans/changes/swarm-test-speed/plan.md, "Files and steps" step 2 | Step 2 promises to run the new reuse regression against the old reader and record its assertion failure, but no recorded run, assertion text or evidence of that check appears in the change; only the test docstring asserts the old reader would fail it. | mimo-v2.5 | fixed — not a test — run of the new tests on the old reader recorded in plan.md: 5 failed, 19 passed (0f08614a) | no — text and measurement only | agree |
| L1-9 | MINOR | MAINT | implementation detail exposed to tests | tests/test_stage2_declaration.py, test_unchanged_contents_reuse_a_bounded_parse_cache, assertions on availability._DECLARATION_CACHE and availability._DECLARATION_CACHE_SIZE | The ledger test for criterion 2 asserts directly on two private module members of the production reader, so a maintainer renaming or restructuring the private cache turns a green criterion test red even when the cache is still bounded and reusing parses; the guarantee could be stated through the public reader's parse counts alone, which the test already counts. | mimo-v2.5 | rejected — plan step 4 requires proof that the cache is bounded; no public interface exposes its size, and the private names belong to the same module, so a rename changes the test in the same commit |  | disagree — Using private cache members in tests establishes no correctness fault, missing acceptance coverage or ineffective gate; the objection concerns refactoring preferences. |
| L1-10 | BLOCKER | SPEC | free | plans/changes/swarm-test-speed/plan.md "Baseline measurement — 2026-10-28" and "Time used"; spec.md criterion 7 and Definition of Done | The change's own Done-when requires three matched before/after runs of the slowest swarm test showing a lower median, recorded in plan.md, plus full-suite elapsed time with environment and result counts. plan.md holds only the three before-runs, and it states they were disturbed because another worktree's make verify ran during all of them; there are no after-runs, no after median, no matched conditions and no full-suite timing anywhere in the change, so the promised speedup is unproven and the only recorded comparison is admittedly unmatched. | mimo-v2.6-flash | fixed — not a test — same fix as L1-1 | no — text and measurement only | agree |
| L1-11 | MINOR | SPEC | free | plans/changes/swarm-test-speed/plan.md "Files and steps" step 2 | plan.md promises to run the new reuse regression against the pre-change reader and record its assertion failure. No such run is recorded in plan.md or findings.md; the test file only asserts in comments that the old reader would fail, so the tests' ability to catch the regression they claim to guard is never demonstrated. | mimo-v2.6-flash | fixed — not a test — same fix as L1-8 | no — text and measurement only | agree |
| L1-12 | MINOR | MAINT | free | plans/changes/swarm-test-speed/research.md, opening lines and frontmatter | research.md still opens with "this file is empty until it has run" and carries a callout telling whoever fills it in that its frontmatter says `provenance: human-written`, while that same frontmatter says `ai-drafted-reviewed` and the file is full. A maintainer following the note would redo work already finished or "correct" the provenance in the wrong direction. | mimo-v2.6-flash | fixed — not a test — same fix as L1-3 | no — text and measurement only | agree |
| L1-13 | MINOR | MAINT | free | frontmatter of all five swarm-test-speed files; their rows in plans/INDEX.md | Every ledger file and index row declares `implementation_status: none`, while plan.md's "Time used" section and findings.md's attempt log record two completed implement attempts that changed scripts/stage2_availability.py and created tests/test_stage2_declaration.py. The index tells a maintainer that no implementation exists for a change that already carries one. | mimo-v2.6-flash | fixed — not a test — same fix as L1-6 | no — text and measurement only | agree |

Rounds run: 2

Record digest: sha256:5723ae384eb9cc0accbbb119ff4d8be17f6b7a298f112bf5b65f137ccc6ecec3

Record identity: sha256:ee39c57f4b961e8924304a4e87f8cff0cab68646f8b1ffc4a737b7b97a2ac338

Loop state: {"availability": {"checked_at": "2026-10-28T17:47:29+00:00", "failed": {"cat-jam-free": "pi call failed: exit 1: 400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Model is unavailable.\"}", "longcat-2.5-preview-free": "pi call failed: exit 1: 400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Model is unavailable.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 400: {\"type\":\"server_error\",\"message\":\"Upstream request failed: [400] Unsupported model mimo-v2.5-pro\"}"}, "reachable": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"], "skipped": {"gemini-4-argon-contributor": "not admitted; data terms have not been read", "gpt-5.6-luna": "not admitted; data terms have not been read", "grok-4.6": "not admitted; data terms have not been read", "grok-4.7": "not admitted; data terms have not been read", "kimi-k2.7-code": "not admitted; data terms have not been read", "kimi-k3": "not admitted; data terms have not been read", "minimax-m2.7": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read", "space-bunny": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured)", "gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured)", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured)", "minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured)", "qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured)", "qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured)"], "terms_warnings": ["the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left)", "the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left)"]}, "consumed": ["flash", "rung:longcat-2.0"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "big-pickle", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-flash", "provider": "opencode"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "exo-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "ling-3.0-flash-fin-free", "provider": "opencode"}, {"model": "ling-3.1-flash-free", "provider": "opencode"}, {"model": "longcat-2.5-preview-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-spark-1.3-contributor-free", "provider": "opencode"}, {"model": "nemotron-3-ultra-free", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "space-bunny-free", "provider": "opencode"}, {"model": "step-5-preview-free", "provider": "opencode"}, {"model": "cat-jam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-flash", "provider": "opencode-go"}, {"model": "deepseek-v4-flash-vision-exp", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon-contributor", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.6", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-preview-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m2.7", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "space-bunny", "provider": "opencode-go"}, {"model": "step-5-preview-free", "provider": "opencode-go"}], "checked_at": "2026-10-28T17:42:05+00:00", "dropped": {}, "models_store": {"opencode-go": {"checkedAt": 1793209322437, "etag": "W/\"65e1c3b71054c3b1741fe4cb46560dbf\"", "lastModified": 1792068066000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "cat-jam-free", "input": ["text"], "maxTokens": 131072, "name": "Cat Jam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"forceAdaptiveThinking": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro (New)", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/v1", "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 0, "input": 4, "output": 20}, "id": "gemini-4-argon-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.6", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.6", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 0, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "LongCat 2.5 Preview Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 204800, "cost": {"cacheRead": 0.06, "cacheWrite": 0.375, "input": 0.3, "output": 1.2}, "id": "minimax-m2.7", "input": ["text"], "maxTokens": 131072, "name": "MiniMax-M2.7", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "space-bunny", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 524288, "name": "Space Bunny", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "step-5-preview-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "overlay": ["cat-jam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon-contributor", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.6", "grok-4.7", "hy3", "hy4-preview", "kimi-k2.7-code", "kimi-k3", "longcat-2.0", "longcat-2.5-preview-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m2.7", "minimax-m3", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "space-bunny", "step-5-preview-free"], "pi_version": "1.2.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": [], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.5", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"], "rungs": ["longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "deepseek-v4-pro", "glm-5.2", "glm-5.3"]}}

Kept from the loop record:

> Notice: paid models skipped: qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured); gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured); minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured); qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured); qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured).
> Notice: in the live catalog without a terms reading: gemini-4-argon-contributor, gpt-5.6-luna, grok-4.6, grok-4.7, kimi-k2.7-code, kimi-k3, minimax-m2.7, muse-spark-1.2-contributor, muse-spark-1.3-contributor, space-bunny.
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (3 days left).
> longcat-2.0 reported no finding.
> From longcat-2.0:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> No finding.

<!-- End of released loop record -->

Stage-2 call, 2026-10-28: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 732 files, 2515 commits, 12 rules.

Stage-2 call, 2026-10-29: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 737 files, 2584 commits, 12 rules.
