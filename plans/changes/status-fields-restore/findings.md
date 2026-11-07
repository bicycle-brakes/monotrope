---
title: "Findings — status-fields-restore"
category: findings
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-ljmi
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — status-fields-restore

Stage-2 call, 2026-11-06: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 910 files, 3352 commits, 12 rules.

Stage-2 call, 2026-11-06: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 913 files, 3356 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +11 -0
> - `plans/changes/status-fields-restore/plan.md` +8 -8
> - `scripts/stage2.py` +196 -3
> - `tests/test_stage2.py` +502 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> repair: verified and committed · route codex · attempt 1
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> ________ test_repair_lifecycle_report_describes_each_attempt[restored] _________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/status-fields-restore/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1317/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1317/popen-gw0/test_repair_lifecycle_report_d0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10792e000>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1317/popen-gw0/test_repair_lifecycle_report_d0')
> capsys = <_pytest.capture.CaptureFixture object at 0x1079336b0>
> scenario = 'accepted'
>
>     @pytest.mark.parametrize(
>         "scenario",
>         ["accepted", "rejected", "unchanged", "refused"],
>         ids=["restored", "rejected", "unchanged", "refused"],
>     )
>     def test_repair_lifecycle_report_describes_each_attempt(
>         world: World,
>         monkeypatch: pytest.MonkeyPatch,
>         tmp_path: Path,
>         capsys: pytest.CaptureFixture[str],
>         scenario: str,
>     ) -> None:
>         """Criterion 5. Planted fault: an attempt's bookkeeping stays silent, claims a restoration it did
>         not perform, or a refused restoration is reported as success."""
>         repair_world(world)
>         plant_lifecycle(world)
>         damage = {
>             "plans/changes/demo/spec.md": lifecycle_damaged(
>                 world, "plans/changes/demo/spec.md", status="superseded", implementation=None
>             ),
>             "plans/changes/demo/plan.md": lifecycle_damaged(
>                 world, "plans/changes/demo/plan.md", status=None, implementation="partial"
>             ),
>         }
>         spec_line = f"{stage2.LIFECYCLE_LABEL}: plans/changes/demo/spec.md — status"
>         unchanged = "plans/changes/demo/plan.md, plans/changes/demo/spec.md — unchanged"
>         if scenario == "accepted":
>             script_repair(
>                 world,
>                 [repair_step(plant={**damage, "src/app.py": "value = 2\n", "tests/test_fix.py": FIX_TEST})],
>                 make=[{"stdout": "green\n"}],
>             )
>             assert world.run("repair") == 0
>             line = restored_line(world)
> >           assert spec_line in line and "plans/changes/demo/plan.md — status, implementation_status" in line
> E           AssertionError: assert ('lifecycle fields: plans/changes/demo/spec.md — status' in 'Runner restoration, 2026-11-06: repair · attempt 1 · route codex — plans/changes/demo/spec.md — status; plans/changes/demo/plan.md — implementation_status, status')
>
> tests/test_stage2.py:11944: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 31 files, 4 commits, 1 rules, 1 prompt texts
> repair: the attempt's protected answer is saved at /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1317/popen-gw0/test_repair_lifecycle_report_d0/repo/.git/stage2/attempts/demo/attempt-1-20261106T023416775450Z-e9499756.md
> repair: verified and committed · route codex · attempt 1
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_repair_lifecycle_prompts_name_the_protected_fields
> FAILED tests/test_stage2.py::test_repair_lifecycle_fields_survive_failed_attempts[retry]
> FAILED tests/test_stage2.py::test_repair_lifecycle_fields_are_restored_before_verification
> FAILED tests/test_stage2.py::test_repair_lifecycle_protection_allows_no_design[created-by-the-attempt]
> FAILED tests/test_stage2.py::test_repair_lifecycle_fields_survive_failed_attempts[exhausted]
> FAILED tests/test_stage2.py::test_repair_lifecycle_restoration_preserves_other_edits
> FAILED tests/test_stage2.py::test_repair_lifecycle_report_describes_each_attempt[restored]
> 7 failed, 7 passed in 15.96s
> ```

Stage-2 call, 2026-11-06: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 913 files, 3368 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 915 files, 3459 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 915 files, 3460 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 915 files, 3460 commits, 12 rules.
