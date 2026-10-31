---
title: "Findings — draft-gates-only"
category: findings
status: draft
implementation_status: partial
date: 2026-10-31
created: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-77qj
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — draft-gates-only

Stage-2 call, 2026-10-31: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 789 files, 2828 commits, 12 rules.

Stage-2 call, 2026-10-31: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 792 files, 2851 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +10 -7
> - `plans/changes/draft-gates-only/plan.md` +6 -6
> - `scripts/stage2.py` +19 -11
> - `tests/test_stage2.py` +306 -72
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>
> tests/test_stage2.py:3925: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 29 files, 3 commits, 1 rules, 1 prompt texts
> draft: verified and committed · route codex · attempt 1
> INFO  (1):
>   - leak check clean: 33 files, 4 commits, 1 rules, 1 prompt texts
> draft: verified and committed · route codex · attempt 1
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> __________ test_nonsecret_diagnostic_matches_still_refuse[multiline] ___________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/draft-gates-only/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-5949/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-5949/popen-gw2/test_nonsecret_diagnostic_matc0/state'))
> capsys = <_pytest.capture.CaptureFixture object at 0x108c5b650>
> multiline = True
>
>     @pytest.mark.parametrize("multiline", [False, True], ids=["single-line", "multiline"])
>     def test_nonsecret_diagnostic_matches_still_refuse(
>         world: World, capsys: pytest.CaptureFixture[str], multiline: bool
>     ) -> None:
>         """Criterion 5. Planted fault: a secret replacement over the same span hides a non-secret violation."""
>         planted = "LEAKMARK-" + "654321"
>         pattern = r"LEAKMARK-[0-9]{6}"
>         if multiline:
>             planted += "\nEND-" + "654321"
>             pattern += r"\nEND-[0-9]{6}"
>         set_denylist(f"blocked = {pattern}\nsecret:wide = {pattern}\n")
>         refusal = None
>         try:
>             stage2.protect_diagnostics(f"a\nvalue {planted}\n")
>         except stage2.Refused as error:
>             refusal = str(error)
>         assert refusal is not None, "a non-secret match must refuse before secret redaction"
>         assert "'blocked'" in refusal and "line 2" in refusal
>         assert all(line not in refusal for line in planted.splitlines())
>         draft_world(world)
>         plant = {"plans/changes/demo/plan.md": PLAN_CARD}
>         world.script(
>             codex=[codex_ok("T1", "drafted", plant=plant), codex_ok("T2", "again")],
>             claude=[{"stdout": "glm"}],
>             docs=[{"stdout": f"E {planted}\n", "exit": 1}, {"stdout": "green\n"}],
>         )
> >       assert world.run("draft") == 2
> E       AssertionError: assert 1 == 2
> E        +  where 1 = run('draft')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-5949/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-5949/popen-gw2/test_nonsecret_diagnostic_matc0/state')).run
>
> tests/test_stage2.py:3057: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 29 files, 3 commits, 2 rules (1 secret rule not applied under tests/), 1 prompt texts
> INFO  (1):
>   - leak check clean: 32 files, 3 commits, 2 rules (1 secret rule not applied under tests/), 1 prompt texts
> INFO  (1):
>   - leak check clean: 32 files, 3 commits, 2 rules (1 secret rule not applied under tests/), 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> failed: the draft failed after the allowed attempts; why each attempt failed and the files each changed: plans/changes/demo/findings.md
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_failed_first_draft_gets_one_codex_repair_with_its_diagnostics
> FAILED tests/test_stage2.py::test_a_red_verify_fails_the_draft_attempt - Asse...
> FAILED tests/test_stage2.py::test_a_failed_draft_check_leaves_its_block_and_its_tree
> FAILED tests/test_stage2.py::test_draft_docs_checks_preserve_preparation_and_artifact_guards
> FAILED tests/test_stage2.py::test_diagnostic_redaction_refuses_an_unusable_denylist
> FAILED tests/test_stage2.py::test_failed_docs_checks_fail_the_draft_attempt
> FAILED tests/test_stage2.py::test_secret_rules_outside_diagnostics_still_block_retry
> FAILED tests/test_stage2.py::test_nonsecret_diagnostic_matches_still_refuse[single-line]
> FAILED tests/test_stage2.py::test_only_the_changes_own_missing_adr_answer_is_tolerated
> FAILED tests/test_stage2.py::test_nonsecret_diagnostic_matches_still_refuse[multiline]
> 10 failed, 43 passed in 22.24s
> ```

Stage-2 call, 2026-10-31: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 792 files, 2854 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/draft-gates-only/plan.md` +6 -6
> - `tests/test_stage2.py` +14 -5
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> ..................................F..................                    [100%]
> =================================== FAILURES ===================================
> ________________ test_failed_docs_checks_fail_the_draft_attempt ________________
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/draft-gates-only/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-5951/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-5951/popen-gw4/test_failed_docs_checks_fail_t0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x109278080>
>
>     def test_failed_docs_checks_fail_the_draft_attempt(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
>         # Criterion 3 (draft-gates-only). Planted fault: a red, unstartable, timed-out or
>         # admission-refused document check is accepted, committed as a passing draft, reported as a
>         # failed `make verify` run, or slips the retry chain.
>         draft_world(world)
>         spec = "---\ntitle: Spec\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Spec\n"
>         plant = {"plans/changes/demo/spec.md": spec, "plans/changes/demo/plan.md": PLAN_CARD}
>         before = git(world.root, "rev-parse", "HEAD")
>     
>         def reset() -> None:
>             """Back to the state a fresh draft starts from: no artefacts, no call log, no derived leftovers."""
>             (world.root / "plans/changes/demo/spec.md").unlink()
>             world.plan.unlink()
>             clear_derived_leftovers(world)
>             (world.bin / "calls.jsonl").unlink()
>     
>         # a red exit: every attempt fails, the chain runs, nothing is committed
>         red = red_verify(OTHER_RED)
>         world.script(
>             codex=[codex_ok("T1", "drafted", plant=plant), codex_ok("T2", "again")],
>             claude=[{"stdout": "glm"}],
>             docs=[red, red, red],
>         )
>         assert world.run("draft") == 1
>         assert [call["argv"] for call in world.calls("bash")] == [DOCS_ARGV] * 3, "the chain did not retry"
>         assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0", "a red document check was committed"
>         block = "\n".join([b for b in quote_blocks(world.text()) if "post-run checks" in b[0]][0])
>         assert "`bash scripts/verify_all.sh --job docs` exited 1" in block and "make verify" not in block
>     
>         # a check that cannot start is as failed a post-run check as a red one
>         reset()
>         (world.bin / "bash").chmod(0o644)
>         world.script(codex=[codex_ok("T1", "drafted", plant=plant), codex_ok("T2", "again")], claude=[{"stdout": "glm"}])
>         assert world.run("draft") == 1
>         assert world.calls("bash") == [], "an unstartable document check was started"
>         assert git(world.root, "rev-list", "--count", f"{before}..HEAD") == "0"
>         block = "\n".join([b for b in quote_blocks(world.text()) if "post-run checks" in b[0]][0])
> >       assert "`bash scripts/verify_all.sh --job docs` could not run" in block and "Permission denied" in block
> E       assert ('`bash scripts/verify_all.sh --job docs` could not run' in "Attempt 1 (codex) failed its post-run checks.\n\nFiles the attempt changed (lines added, removed):\n- `plans/changes/...ers: other: no answer — other.rel needs the maintainer's answer\n── [adr-answers] RED (block) — der Lauf ist rot.\n```")
>
> tests/test_stage2.py:3789: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 29 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 33 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 33 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 33 files, 3 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 33 files, 3 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> failed: the draft failed after the allowed attempts; why each attempt failed and the files each changed: plans/changes/demo/findings.md
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> failed: the draft failed after the allowed attempts; why each attempt failed and the files each changed: plans/changes/demo/findings.md
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_failed_docs_checks_fail_the_draft_attempt
> 1 failed, 52 passed in 24.01s
> ````

Stage-2 call, 2026-10-31: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 792 files, 2854 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 792 files, 2855 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 792 files, 2856 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model hy3 · leak check clean over 792 files, 2858 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 792 files, 2861 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model hy4-preview · leak check clean over 792 files, 2864 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 792 files, 2866 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 792 files, 2867 commits, 12 rules.
