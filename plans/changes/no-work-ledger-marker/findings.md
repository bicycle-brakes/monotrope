---
title: "Findings — no-work-ledger-marker"
category: findings
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-twbl
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — no-work-ledger-marker

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1008 files, 3895 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/no-work-ledger-marker/plan.md` +127 -0
> - `plans/changes/no-work-ledger-marker/research.md` +19 -0
> - `plans/changes/no-work-ledger-marker/spec.md` +124 -0
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/no-work-ledger-marker/findings.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> plans/changes/no-work-ledger-marker/plan.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> plans/changes/no-work-ledger-marker/research.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> plans/changes/no-work-ledger-marker/spec.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 36933 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-11: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 1011 files, 3902 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-12: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1011 files, 3974 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +8 -1
> - `plans/changes/no-work-ledger-marker/plan.md` +5 -5
> - `scripts/stage2.py` +184 -10
> - `tests/test_stage2.py` +229 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/stage2.py`, `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> scripts/stage2.py:1954:9: F402 Import `field` from line 174 shadowed by loop variable
>      |
> 1952 |     if not isinstance(record, dict):
> 1953 |         return f"an entry of the free rule's {kind} list must be a record with id, date and reason"
> 1954 |     for field in ("id", "date", "reason"):
>      |         ^^^^^ F402
> 1955 |         value = record.get(field)
> 1956 |         if not isinstance(value, str) or not value.strip():
>      |
>
> tests/test_stage2.py:10981:66: ARG005 Unused lambda argument: `args`
>       |
> 10979 |     seeded_ledger_plan(world)
> 10980 |     if fault == "capture":
> 10981 |         monkeypatch.setattr(stage2, "_clearing_records", lambda *args, **kwargs: None)
>       |                                                                  ^^^^ ARG005
> 10982 |     else:
> 10983 |         real_prepare = stage2.prepare_derived
>       |
>
> tests/test_stage2.py:10981:74: ARG005 Unused lambda argument: `kwargs`
>       |
> 10979 |     seeded_ledger_plan(world)
> 10980 |     if fault == "capture":
> 10981 |         monkeypatch.setattr(stage2, "_clearing_records", lambda *args, **kwargs: None)
>       |                                                                          ^^^^^^ ARG005
> 10982 |     else:
> 10983 |         real_prepare = stage2.prepare_derived
>       |
>
> Found 3 errors.
> ```

Stage-2 call, 2026-11-12: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1011 files, 3975 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/no-work-ledger-marker/plan.md` +5 -5
> - `scripts/stage2.py` +3 -3
> - `tests/test_stage2.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> failed: repair post-run checks failed after the allowed attempts; why each attempt failed and the files it changed: plans/changes/demo/findings.md
> _____ test_runner_ledger_clearing_cannot_qualify_a_retry[repair-targeted] ______
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/no-work-ledger-marker/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-124/popen-gw2...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-124/popen-gw2/test_runner_ledger_clearing_ca0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x108d185c0>
> capsys = <_pytest.capture.CaptureFixture object at 0x108a8b2f0>, verb = 'repair'
> forced_full = False
>
>     @pytest.mark.parametrize(
>         ("verb", "forced_full"),
>         [("implement", False), ("repair", True), ("repair", False)],
>         ids=["implement-full", "repair-full-fallback", "repair-targeted"],
>     )
>     def test_runner_ledger_clearing_cannot_qualify_a_retry(
>         world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], verb: str, forced_full: bool
>     ) -> None:
>         """Criteria 1 and 4. Planted fault: a time-body-only retry is accepted because verification
>         cleared the retained test's runner-owned marker; or a marker-only retry loses its diagnostic,
>         its rejected records or its taken rows, or checkpoints or reports success on exhaustion."""
>         seeded_ledger_plan(world)
>         clearings: list[int] = []
>         counting_capture(monkeypatch, clearings)
>         targeted = None
>         if verb == "repair" and not forced_full:
>             # The actual targeted path, not the fallback: attempt 1's targeted pytest is the one red run.
>             targeted = targeted_mode(monkeypatch)
>             targeted.outcomes["pytest"] = lambda _command: RED_PYTEST if len(targeted.of("pytest")) == 2 else None
>         first = work_step(verb)
>         if verb == "implement":
>             first = {**first, "plant": {**first["plant"], "tests/test_fix.py": FIX_TEST}}
>         if verb == "repair" and forced_full:
>             # The idle-retry fixture's forcing: an input kind the targeted selector does not cover.
>             first = {**first, "plant": {**first["plant"], "verification-scope.txt": "requires full verification\n"}}
>         baseline = script_work(
>             world,
>             verb,
>             [first, idle_step("time-body-only"), idle_step("time-body-only")],
>             [{"stdout": "red\n", "exit": 1}, GREEN, GREEN],
>         )
>         held = world.record().read_text(encoding="utf-8") if verb == "repair" else None
>         assert world.run(verb) == 1, "a retry whose model spent only the time body was accepted"
>         assert git(world.root, "rev-parse", "HEAD") == baseline
>         assert clearings == [1, 1, 1], clearings
>         entries = runner_entries(world.plan)
>         assert len(entries) == 3
>         assert all("rejected" in line and "accepted" not in line for line in entries)
>         assert world.text().count("Stage-2 call,") == 3
>         text = world.text()
>         assert text.count(stage2.NO_WORK) == 2, text
>         # The marker came back with the restored plan while the retained test stayed: the retry stands.
> >       assert "- 1: not yet written tests/test_fix.py::test_fix" in world.plan.read_text(encoding="utf-8")
> E       AssertionError: assert '- 1: not yet written tests/test_fix.py::test_fix' in '---\ntitle: Plan\nupdated: 2026-11-12\nbead: demo-1\n---\n\n# Plan\n\n## Criterion ledger\n\n- 1: tests/test_fix.py::...03:14:53 UTC, 1 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner\n'
> E        +  where '---\ntitle: Plan\nupdated: 2026-11-12\nbead: demo-1\n---\n\n# Plan\n\n## Criterion ledger\n\n- 1: tests/test_fix.py::...03:14:53 UTC, 1 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner\n' = read_text(encoding='utf-8')
> E        +    where read_text = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-124/popen-gw2/test_runner_ledger_clearing_ca0/repo/plans/changes/demo/plan.md').read_text
> E        +      where PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-124/popen-gw2/test_runner_ledger_clearing_ca0/repo/plans/changes/demo/plan.md') = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-124/popen-gw2...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-124/popen-gw2/test_runner_ledger_clearing_ca0/state')).plan
>
> tests/test_stage2.py:10963: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 30 files, 4 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 33 files, 4 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 33 files, 4 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: repair post-run checks failed after the allowed attempts; why each attempt failed and the files it changed: plans/changes/demo/findings.md
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_ledger_discount_keeps_clearing_in_both_verify_modes[targeted]
> FAILED tests/test_stage2.py::test_ledger_discount_keeps_clearing_in_both_verify_modes[full]
> FAILED tests/test_stage2.py::test_runner_ledger_clearing_cannot_qualify_a_retry[implement-full]
> FAILED tests/test_stage2.py::test_runner_ledger_clearing_cannot_qualify_a_retry[repair-full-fallback]
> FAILED tests/test_stage2.py::test_runner_ledger_clearing_cannot_qualify_a_retry[repair-targeted]
> 5 failed, 32 passed in 17.58s
> ```

Stage-2 call, 2026-11-12: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1011 files, 3975 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1011 files, 3976 commits, 12 rules.

Stage-2 call, 2026-11-12: review-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1011 files, 3976 commits, 12 rules.

Loop attempt: 2026-11-12 — no round was written; the review-loop calls above consumed no stage; audit calls: 1

Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).

Notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base.

Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).

Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor.

Notice: the data terms of longcat-2.0 expire on 2026-11-16 (4 days left).

Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (4 days left).

Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (4 days left).

Notice: the data terms of gpt-6-luna expire on 2026-11-16 (4 days left).

Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (4 days left).

Notice: the data terms of minimax-m3 expire on 2026-11-16 (4 days left).

Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
