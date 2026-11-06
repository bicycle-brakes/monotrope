---
title: "Findings — archive-closed-changes"
category: findings
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-cqun
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — archive-closed-changes

Stage-2 call, 2026-11-06: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 910 files, 3405 commits, 12 rules.

Stage-2 call, 2026-11-06: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 913 files, 3418 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `Makefile` +32 -1
> - `plans/changes/archive-closed-changes/plan.md` +10 -10
> - `scripts/archive_closed_changes.py` +614 -0
> - `scripts/ci_gates.py` +5 -0
> - `tests/test_archive_closed_changes.py` +634 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_archive_closed_changes.py`.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>     
>         def _flaky(src: Path, dst: Path, artefacts: dict[Path, archive.Artefact], day: dt.date) -> None:
>             if src.name == "beta":
>                 raise OSError("disk full during the move")
>             original(src, dst, artefacts, day)
>     
>         monkeypatch.setattr(archive, "_relocate", _flaky)
> >       assert archive.main(["--write"]) == 1
> E       AssertionError: assert 0 == 1
> E        +  where 0 = <function main at 0x10b50aca0>(['--write'])
> E        +    where <function main at 0x10b50aca0> = archive.main
>
> tests/test_archive_closed_changes.py:564: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> archive: nothing to archive — no eligible closed folder is left active
> _____ test_preflight_failure_leaves_entire_batch_unchanged[symlink-member] _____
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/archive-closed-changes/.venv/bin/python3
>
> plans_repo = <test_archive_closed_changes.Fixture object at 0x106536270>
> capsys = <_pytest.capture.CaptureFixture object at 0x106534470>
> case = 'symlink-member'
>
>     @pytest.mark.parametrize(
>         "case",
>         ["broken-render", "empty-render", "duplicate-ids", "malformed-header", "existing-destination", "symlink-member"],
>     )
>     def test_preflight_failure_leaves_entire_batch_unchanged(
>         plans_repo: Fixture, capsys: pytest.CaptureFixture[str], case: str
>     ) -> None:
>         fx = plans_repo
>         fx.add("good-one", files=_closed_files("b-good"))
>         fx.add("also-good", files=_closed_files("b-also"))
>         rows = {"b-good": "closed", "b-also": "closed"}
>         if case == "malformed-header":
>             fx.add("bad-one", files={"spec.md": _artefact("Spec — bad", "b-bad"), "plan.md": "no front matter at all\n"})
>             rows["b-bad"] = "closed"
>         elif case == "existing-destination":
>             occupied = fx.archive / "2026-03-04-good-one"
>             occupied.mkdir()
>             (occupied / "sentinel.txt").write_bytes(b"evidence")
>         elif case == "symlink-member":
>             fx.add("linked-one", files=_closed_files("b-link"), companions={"note.txt": b"n"})
>             (fx.changes / "linked-one" / "link.txt").symlink_to(fx.changes / "linked-one" / "note.txt")
>             rows["b-link"] = "closed"
>         fx.set_render(rows)
>         if case == "broken-render":
>             fx.render_path.write_text("not json at all\n", encoding="utf-8")
>         elif case == "empty-render":
>             fx.render_path.write_text("", encoding="utf-8")
>         elif case == "duplicate-ids":
>             fx.render_path.write_text(
>                 json.dumps({"id": "b-good", "status": "closed"})
>                 + "\n"
>                 + json.dumps({"id": "b-good", "status": "open"})
>                 + "\n",
>                 encoding="utf-8",
>             )
>     
>         before = _snapshot(fx.root)
> >       assert archive.main(["--write"]) == 1
> E       AssertionError: assert 0 == 1
> E        +  where 0 = <function main at 0x1067faca0>(['--write'])
> E        +    where <function main at 0x1067faca0> = archive.main
>
> tests/test_archive_closed_changes.py:519: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> archive: nothing to archive — no eligible closed folder is left active
> =========================== short test summary info ============================
> FAILED tests/test_archive_closed_changes.py::test_default_cli_and_make_are_read_only
> FAILED tests/test_archive_closed_changes.py::test_archiving_does_not_exempt_criterion_ledger
> FAILED tests/test_archive_closed_changes.py::test_write_moves_complete_folder_on_captured_day
> FAILED tests/test_archive_closed_changes.py::test_successful_repeat_is_byte_identical
> FAILED tests/test_archive_closed_changes.py::test_preflight_failure_leaves_entire_batch_unchanged[malformed-header]
> FAILED tests/test_archive_closed_changes.py::test_only_lifecycle_header_fields_change
> FAILED tests/test_archive_closed_changes.py::test_index_matches_registry_after_archive
> FAILED tests/test_archive_closed_changes.py::test_only_closed_single_bead_folders_are_selected
> FAILED tests/test_archive_closed_changes.py::test_preflight_failure_leaves_entire_batch_unchanged[existing-destination]
> FAILED tests/test_archive_closed_changes.py::test_write_failure_reports_partial_work
> FAILED tests/test_archive_closed_changes.py::test_preflight_failure_leaves_entire_batch_unchanged[symlink-member]
> 11 failed, 3 passed, 1 skipped in 0.65s
> ```

Stage-2 call, 2026-11-06: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 915 files, 3425 commits, 12 rules.
