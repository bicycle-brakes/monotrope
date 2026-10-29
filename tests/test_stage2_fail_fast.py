"""The cheap checks before full verification, and the findings the runner owns.

Bead coding-harness-5tyh: a work attempt stops at the first red, unstartable or over-bound cheap
command instead of spending a full verification on it, the prompts carry the accepted plan's
ledger tests as must-runs, and an attempt's edit of `findings.md` is restored before any check
reads model-written state — so the edit alone never spends the attempt. Every case here runs the
runner in-process against a temporary repository and stand-ins, as `test_stage2.py` does; no test
starts a real model, a real ruff or a real pytest.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import stage2  # noqa: E402
from test_stage2 import (  # noqa: E402
    KEY,
    World,
    formatted_attempt,  # noqa: E402
    git,  # noqa: E402
    prompt_entry,  # noqa: E402
    red_verify,  # noqa: E402
    successful_implementation,  # noqa: E402
    venv_pytest,  # noqa: E402
    venv_ruff,  # noqa: E402
)
from test_stage2 import world as stage2_world  # noqa: E402

world = stage2_world

RESTORED = (
    "the attempt's edits to findings.md were restored before the checks; the file stands as it stood "
    "before the call, and the attempt failed for the reasons below"
)
NOTICE = "The attempt edited findings.md; the runner restored it before the post-run checks"
CHEAP = "Runner cheap checks before `make verify`"


def one_test_step(**more: object) -> dict:
    """One Flash attempt whose only change is a new test file and its measured plan line."""
    return {
        "stdout": "implemented",
        "plant": {"tests/test_new.py": "def test_new():\n    assert 1\n"},
        "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
        **more,
    }


@pytest.mark.parametrize("half", ["lint", "format"])
def test_red_ruff_skips_full_verification(world: World, half: str) -> None:
    """Ledger 1. Planted fault: a red cheap ruff still starts `make verify`, or the attempt is accepted."""
    red_check = {"stdout": "scripts/a.py:1:1: F401 `a` imported but unused\n", "exit": 1}
    red_format = {"stdout": "would reformat scripts/a.py\n", "exit": 1}
    # One attempt consumes four ruff steps: the format step's check and format, then the cheap
    # lint and format check. The red stands at the cheap position, never at the format step's.
    steps = [{}, {}, red_check, {}] if half == "lint" else [{}, {}, {}, red_format]
    venv_ruff(world)
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(
        claude=[formatted_attempt(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        ruff=steps * 3,
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    assert world.calls("make") == [], "a red cheap ruff still started `make verify`"
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "0"
    assert CHEAP in world.text()


@pytest.mark.parametrize("case", ["failing", "uncollectable"])
def test_red_selected_pytest_skips_full_verification(world: World, case: str) -> None:
    """Ledger 2. Planted fault: a failing or uncollectable selected test still starts `make verify`."""
    red = {
        "failing": {"stdout": "FAILED tests/test_new.py::test_new - assert 1 == 2\n", "exit": 1},
        "uncollectable": {"stderr": "ERROR tests/test_new.py - ImportError: no module named need\n", "exit": 2},
    }[case]
    venv_ruff(world)
    venv_pytest(world)
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(
        claude=[one_test_step(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        python3=[red] * 3,
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    assert len(world.calls("python3")) == 3
    assert world.calls("make") == [], "a red selected pytest still started `make verify`"
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "0"
    text = world.text()
    assert "`.venv/bin/python3 -m pytest -q -n auto` exited" in text
    assert ("FAILED tests/test_new.py::test_new" if case == "failing" else "ImportError") in text


def test_cheap_test_selection_matches_changed_functions_and_ledger(world: World) -> None:
    """Ledger 3. Planted fault: selection omits or duplicates a source, or replaces it by broad discovery.

    Importers are not selected (`decisions.md#Q-3`). The changed set spans every source at once — in a modified tracked test file only the new and the
    edited function, a new test file whole, the plan's ledger ids in both forms (one inside the new
    file, so it must not run twice; one in an untouched file; one still unwritten and absent, which
    keeps the attempt red), and on a retry exactly the ids the attempt before reported as failed
    whose file still stands. A modified script, a deleted script's committed importer and a deleted
    test file are not selected. The explicit argv of each attempt's pytest run is the assertion.
    """
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_existing.py").write_text(
        "def test_keep():\n    assert 1\n\n\ndef test_edit():\n    assert 1\n", encoding="utf-8"
    )
    (tests / "test_ledger_old.py").write_text("def test_old():\n    assert 1\n", encoding="utf-8")
    (tests / "test_imports_verdict.py").write_text("import scripts._verdict  # noqa: F401\n", encoding="utf-8")
    (tests / "test_gone.py").write_text("def test_gone():\n    assert 1\n", encoding="utf-8")
    venv_ruff(world)
    venv_pytest(world)
    world.plan.write_text(
        "---\ntitle: Plan\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Plan\n\n## Criterion ledger\n\n"
        "- 1: tests/test_new.py::test_new — the attempt writes it\n"
        "- 2: tests/test_ledger_old.py::test_old — written on an earlier change\n"
        "- 3: not yet written tests/test_missing.py::test_later — nobody writes it\n\n## Time used\n",
        encoding="utf-8",
    )
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "committed tests, an importer and a plan with ledger tests")
    attempt = {
        "stdout": "implemented",
        "plant": {
            "scripts/helper.py": "VALUE = 3\n",
            "tests/test_existing.py": (
                "def test_keep():\n    assert 1\n\n\n"
                "def test_edit():\n    assert 2\n\n\n"
                "def test_added():\n    assert 1\n"
            ),
            "tests/test_new.py": "def test_new():\n    assert 1\n",
        },
        "delete": ["scripts/_verdict.py", "tests/test_gone.py"],
        "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
    }
    second = {"stdout": "second", "append": {"plans/changes/demo/plan.md": "2026-10-07 10:05–10:10, 5 min\n"}}
    # `test_keep` is unchanged and `test_gone` no longer stands: only the first is selected next.
    first_red = {
        "stdout": "FAILED tests/test_existing.py::test_keep - boom\nFAILED tests/test_gone.py::test_gone - boom\n",
        "exit": 1,
    }
    second_red = {"stdout": "nothing that names a test\n", "exit": 1}
    world.script(
        claude=[attempt, second, {"stdout": "third"}],
        python3=[first_red, second_red, second_red],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    calls = world.calls("python3")
    assert len(calls) == 3 and world.calls("make") == []
    head = ["-m", "pytest", "-q", "-n", "auto"]
    first = [
        *head,
        "tests/test_existing.py::test_added",
        "tests/test_existing.py::test_edit",
        "tests/test_ledger_old.py::test_old",
        "tests/test_missing.py::test_later",
        "tests/test_new.py",
    ]
    assert calls[0]["argv"] == first
    # The retry adds exactly the surviving failed id; the deleted file's id is dropped.
    expected = sorted([*first[len(head) :], "tests/test_existing.py::test_keep"])
    assert calls[1]["argv"] == [*head, *expected]
    # The attempt before reported no id, so the third run holds the changed and ledger sources only.
    # The unwritten ledger test stays a target (`first` holds it): the real pytest then fails the
    # attempt naming the missing id; the stand-in's own output is not the runner's to rewrite.
    assert calls[2]["argv"] == first


def test_failed_test_ids_are_read_from_the_pytest_summary() -> None:
    """Ledger 3, retry source. Planted fault: a width-cut line, a repeat or a non-test line is taken as an id."""
    output = (
        "`.venv/bin/python3 -m pytest -q -n auto` exited 1\n"
        "FAILED tests/test_a.py::test_a[x y] - assert 1 == 2\n"
        "FAILED tests/test_a.py::test_a[x y] - assert 1 == 2\n"
        "FAILED tests/test_b.py::TestB::test_b\n"
        "FAILED tests/test_c.py::test_a_very_long_name_that_the_summary_cut - File...\n"
        "FAILED tests/test_d.py::test_d...\n"
        "ERROR tests/test_e.py - ImportError\n"
    )
    assert stage2.failed_test_ids([output]) == [
        "tests/test_a.py::test_a[x y]",
        "tests/test_b.py::TestB::test_b",
        "tests/test_c.py::test_a_very_long_name_that_the_summary_cut",
    ]


def test_empty_targets_skip_their_command(world: World) -> None:
    """Ledger 4. Planted fault: a zero-target check started ruff or pytest, or rejected a text-only attempt."""
    successful_implementation(world)  # plants `src/app.py` only: outside `scripts/` and `tests/`
    assert world.run("implement") == 0
    assert world.calls("ruff") == [] and world.calls("python3") == []
    assert len(world.calls("make")) == 1
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    assert stage2.cheap_checks(world.root, env, world.plan, None, None) == []


def test_cheap_green_still_requires_full_verification(world: World) -> None:
    """Ledger 5. Planted fault: cheap green checkpointed without `make verify`, or despite its red result."""
    red = red_verify(("pytest", ["FAILED tests/test_b.py::test_b - assert 1 == 2"]))
    venv_ruff(world)
    venv_pytest(world)
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(
        claude=[
            formatted_attempt(plant={"scripts/a.py": "a=1\n", "tests/test_b.py": "def test_b():\n    assert 1\n"}),
            {"stdout": "must not run"},
            {"stdout": "must not run"},
        ],
        ruff=[{}] * 8,
        python3=[{}] * 3,
        make=[red] * 3,
    )
    assert world.run("implement") == 1
    names = [call["name"] for call in world.calls()]
    assert names[:7] == ["claude", "ruff", "ruff", "ruff", "ruff", "python3", "make"], names[:7]
    assert len(names) == 21 and names.count("make") == 3, "a checkpoint or a skipped verification appeared"
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "0"


def test_cheap_failures_reach_findings_and_next_route_safely(world: World) -> None:
    """Ledger 6. Planted fault: the evidence is lost, a credential escapes, the span or the ladder changes."""
    red = {"stdout": f"scripts/a.py:1:1: F401 `a` imported but unused\nsecret {KEY} in the finding\n", "exit": 1}
    venv_ruff(world)
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(
        claude=[formatted_attempt(), {"stdout": "second"}, {"stdout": "third"}],
        ruff=[{}, {}, red] * 4,
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    text = world.text()
    assert "`.venv/bin/ruff check` exited 1" in text, "the identified command and exit were lost"
    assert "F401" in text, "the actual failure output was lost"
    assert "[credential]" in text and KEY not in text, "a credential escaped into the findings"
    later = world.calls("claude")[1]["prompt_file"]
    assert "F401" in later and KEY not in later, "the next attempt's prompt lost the evidence or gained the key"
    models = [call["argv"][call["argv"].index("--model") + 1] for call in world.calls("claude")]
    # The ladder is the runner's own: two Flash attempts, then the Stage-1 Sonnet fallback.
    assert models == ["glm-5.3-flash", "glm-5.3-flash", "claude-sonnet-5-5"], "the ladder changed"
    plan = world.plan.read_text(encoding="utf-8")
    assert plan.count("measured by the runner") == 3 and plan.count("· rejected ·") == 3, "a span disappeared"
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "0"


def test_prompts_require_ledger_tests_with_file_only_delegation(world: World) -> None:
    """Ledger 7. Planted fault: a reference or the must-run is missing, or a file-only model got commands.

    The lists come from the accepted plan's snapshot: a retry is built from the cached bytes while
    the plan file may hold the rejected attempt's own edits, so a name the attempt planted must not
    enter its next prompt.
    """
    snapshot = (
        "---\ntitle: Plan\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Plan\n\n## Criterion ledger\n\n"
        "- 1: not yet written tests/test_new.py::test_new — the attempt writes it\n"
        "- 2: tests/test_fix.py::test_fix — written on an earlier change\n\n## Time used\n"
    )
    world.plan.write_text(snapshot, encoding="utf-8")
    ctx = stage2.Context(world.root, "demo", world.plan.parent, "demo-1")
    prompt = stage2.implementation_prompt(ctx, "baseline-sha", [])
    assert "## Must-run checks before handback" in prompt
    for ref in ("tests/test_new.py::test_new", "tests/test_fix.py::test_fix"):
        assert ref in prompt, ref
    assert "You cannot run commands" in prompt, "the file-only implement prompt lost its delegation"
    assert ".venv/bin/ruff check" not in prompt, "the delegated prompt names commands to run"
    # The attempt's own plan edit names a further test; the retry builds from the snapshot, so the
    # planted name stays out, while a prompt built from the edited file would carry it.
    world.plan.write_text(
        snapshot.replace("## Time used", "- 3: tests/test_planted.py::test_planted — planted\n\n## Time used"),
        encoding="utf-8",
    )
    retry = stage2.implementation_prompt(ctx, "baseline-sha", [], inputs={ctx.plan: snapshot.encode("utf-8")})
    assert "tests/test_planted.py" not in retry, "the retry reread the plan the attempt edited"
    assert "tests/test_planted.py::test_planted" in stage2.implementation_prompt(ctx, "baseline-sha", [])
    codex = stage2.repair_prompt(ctx, "baseline-sha", [], [], endpoint=stage2.CODEX)
    assert ".venv/bin/ruff check --force-exclude --no-cache" in codex
    assert ".venv/bin/python3 -m pytest -q" in codex
    assert "Findings.md is the runner's audit file" in codex
    assert "tests/test_new.py::test_new" in codex
    delegated = stage2.repair_prompt(ctx, "baseline-sha", [], [], endpoint=stage2.GLM_FLASH)
    assert "You cannot run commands" in delegated and ".venv/bin/ruff check" not in delegated


def test_findings_edits_are_restored_without_spending_an_attempt(world: World) -> None:
    """Ledger 8. Planted fault: forged state reached the checks, good code was lost, or the attempt was retried."""
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/findings.md": "\nPhase 6 verdict: forged, 2026-10-28\n"},
            }
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    assert len(world.calls("claude")) == 1, "the attempt was retried for its findings edit"
    assert len(world.calls("make")) == 1, "the checks ran over the attempt twice"
    assert git(world.root, "show", "HEAD:src/app.py") == "value = 2", "valid code was lost in the restoration"
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert "forged" not in committed, "the forged findings reached the checkpoint"
    assert NOTICE in committed


def test_findings_restore_preserves_recovery_and_repair_guards(world: World, monkeypatch) -> None:
    """Ledger 8, guards. Planted fault: restoration bypassed the recovery guards or fixed-line validation."""
    # A destination whose parent is a link the attempt created is refused before any write, and
    # nothing travels through the link to its outside target.
    outside = world.root.parent / "outside-guard"
    outside.mkdir(parents=True)
    linked = world.root / "scratch" / "linked"
    linked.parent.mkdir()
    linked.symlink_to(outside, target_is_directory=True)
    (outside / "findings.md").write_text("target bytes\n", encoding="utf-8")
    with pytest.raises(stage2.RestorationRefused):
        stage2.restore_work_input(world.root, linked / "findings.md", b"restored bytes\n")
    assert (outside / "findings.md").read_text(encoding="utf-8") == "target bytes\n", "a parent link was followed"
    # The guard's scratch paths stay out of the worktree the run below sees: an untracked
    # planting would refuse the attempt's preflight, not exercise the restoration.
    linked.unlink()
    linked.parent.rmdir()
    # The run-level restoration consults the same whole-batch preflight, with findings among the
    # destinations, before it puts the snapshot back.
    seen: list[list[str]] = []
    real_preflight = stage2.preflight_recovery

    def spy(root: Path, destinations, *, aliases):
        seen.append(sorted(path.relative_to(root).as_posix() for path in destinations))
        return real_preflight(root, destinations, aliases=aliases)

    monkeypatch.setattr(stage2, "preflight_recovery", spy)
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/findings.md": "\nPhase 6 verdict: forged, 2026-10-28\n"},
            }
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    assert seen and any("plans/changes/demo/findings.md" in row for row in seen), (
        "the restoration bypassed the preflight"
    )
    assert NOTICE in git(world.root, "show", "HEAD:plans/changes/demo/findings.md")


def test_findings_restore_notice_matches_the_verdict(world: World) -> None:
    """Ledger 9. Planted fault: restore evidence disappeared, overwrote history, or called a pass a failure."""
    # An accepted attempt whose findings edit was restored: the notice is quoted under the audit
    # line, and no failed block stands for it.
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/findings.md": "\nLoop restarted: 2026-10-28 after round 9\n"},
            }
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    assert world.text().count("Stage-2 call,") == 1
    assert "failed its post-run checks" not in world.text(), "a passing restored attempt was labelled failed"
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert NOTICE in committed and "Loop restarted" not in committed
    assert git(world.root, "show", "HEAD:src/app.py") == "value = 2"
    # A rejected attempt whose findings edit was restored: the note stands first in the next
    # prompt's entry, beside the real failure, and no earlier evidence is gone. The red make
    # steps spend attempts 1 and 2; attempt 3's stand-in step is missing, so its empty answer
    # stops the run with every audit line kept.
    red = red_verify(("pytest", ["FAILED tests/test_x.py::test_x - assert"]))
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 4\n"},
                "append": {"plans/changes/demo/findings.md": "\nPhase 6 verdict: forged, 2026-10-28\n"},
            },
            {"stdout": "implemented without touching findings"},
        ],
        make=[red, red, {"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    # Attempt 3 (the Stage-1 route) still makes its call - the empty answer is a failed call that
    # stops the run - so both counts cover it: four calls, four audit lines, no checkpoint.
    assert len(world.calls("claude")) == 4
    assert world.text().count("Stage-2 call,") == 4, "an earlier attempt's audit line was erased"
    prompt = world.calls("claude")[2]["prompt_file"]
    entry = prompt_entry(prompt, 1, "flash")
    assert entry[0] == f"- {RESTORED}", "the rejected attempt's restore note does not stand first"
    assert any("`make verify` exited 1" in line for line in entry), "the real failure was lost beside the note"
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert "forged" not in committed
    assert git(world.root, "show", "HEAD:src/app.py") == "value = 2", "a rejected attempt left a checkpoint"


@pytest.mark.parametrize("case", ["missing", "not-executable", "timeout"])
def test_unstartable_or_timed_out_cheap_checks_never_pass(world: World, case: str, monkeypatch) -> None:
    """Ledger 10. Planted fault: a command that cannot start or runs over its bound reached verify as green."""
    # The planted test file is the format step's target and pytest's sole selected test, so both
    # worktree tools stand here; the fault then breaks exactly one of them.
    venv_ruff(world)
    if case == "not-executable":
        venv_pytest(world, executable=False)
    else:
        venv_pytest(world)
    if case == "missing":
        (world.root / ".venv" / "bin" / "python3").unlink()
    if case == "timeout":
        monkeypatch.setattr(stage2, "TOOL_SECONDS", 0.5)
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(
        claude=[one_test_step(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        python3=[{"sleep": 2}] * 3 if case == "timeout" else [{}] * 3,
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    assert world.calls("make") == [], "an unstartable or over-bound cheap check still reached `make verify`"
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "0"
    expected = {
        "missing": "no pytest interpreter at `.venv/bin/python3`",
        "not-executable": "could not be run",
        "timeout": "did not finish",
    }[case]
    assert expected in world.text()


# Review loop round 1 (2026-10-28), rows the orchestrator repaired by hand; each test was red on
# the code before its fix.


def test_a_failed_id_with_a_dash_in_its_parameter_is_read_whole() -> None:
    """Rows L1-3, L1-20. Planted fault: a parameter id holding ` - ` was cut at the separator."""
    output = "FAILED tests/test_a.py::test_p[x - y] - assert 0\nFAILED tests/test_a.py::test_q[a - b]\n"
    assert stage2.failed_test_ids([output]) == ["tests/test_a.py::test_p[x - y]", "tests/test_a.py::test_q[a - b]"]


def test_a_retry_drops_a_failed_test_the_attempt_removed(world: World) -> None:
    """Row L1-12. Planted fault: a failed id whose function no longer stands was handed to pytest."""
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_r.py").write_text("def test_keep():\n    assert 1\n\n\ndef test_old():\n    assert 1\n")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "a test file")
    (tests / "test_r.py").write_text("def test_keep():\n    assert 1\n\n\ndef test_new():\n    assert 1\n")
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    plan = b"---\ntitle: Plan\n---\n\n# Plan\n"
    previous = ["tests/test_r.py::test_old", "tests/test_r.py::test_keep", "tests/test_r.py::test_keep[1]"]
    targets, fault = stage2.selected_tests(world.root, env, plan, previous)
    assert fault is None
    # A failed parameter id is selected by its function (review row F6-2).
    assert targets == ["tests/test_r.py::test_keep", "tests/test_r.py::test_new"]


def test_a_timed_out_cheap_pytest_names_its_selected_tests(world: World, monkeypatch) -> None:
    """Row L1-10. Planted fault: the timeout diagnostic named only the command, not what it ran."""
    venv_ruff(world)
    venv_pytest(world)
    monkeypatch.setattr(stage2, "TOOL_SECONDS", 0.5)
    world.script(
        claude=[one_test_step(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        python3=[{"sleep": 2}] * 3,
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    assert "did not finish" in world.text()
    assert "selected tests: tests/test_new.py" in world.text()


def test_the_runners_scan_record_is_not_an_attempt_edit(world: World, monkeypatch) -> None:
    """Row L1-2. Planted fault: the runner's own scan record was restored away and credited to the attempt."""
    original = stage2.remove_changed_credential
    record = "credential scan skipped scratch/x: its parent is planted; contents were not inspected"

    def planted(root, key, *args, **kwargs):
        stage2.record_credential_scan_skips(root, kwargs.get("findings"), [record], key)
        return original(root, key, *args, **kwargs)

    monkeypatch.setattr(stage2, "remove_changed_credential", planted)
    successful_implementation(world)
    assert world.run("implement") == 0
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert record in committed, "the runner's own record was deleted by the restoration"
    assert NOTICE not in committed, "the runner's own record was credited to the attempt as an edit"


def test_a_ledger_test_missing_from_a_new_file_is_still_selected(world: World) -> None:
    """Row L3-1. Planted fault: a new test file selected whole hid the ledger test it lacks."""
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_fresh.py").write_text("def test_other():\n    assert 1\n\n\ndef test_named():\n    assert 1\n")
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    plan = (
        "---\ntitle: Plan\n---\n\n# Plan\n\n## Criterion ledger\n\n"
        "- 1: tests/test_fresh.py::test_named — written in the new file\n"
        "- 2: not yet written tests/test_fresh.py::test_required — the attempt left it out\n"
    ).encode()
    targets, fault = stage2.selected_tests(world.root, env, plan)
    assert fault is None
    assert targets == ["tests/test_fresh.py", "tests/test_fresh.py::test_required"]


def test_a_retry_drops_a_removed_method_of_a_standing_class(world: World) -> None:
    """Row L5-2. Planted fault: a failed `Class::method` id was kept although the method was removed."""
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_c.py").write_text(
        "class TestC:\n    def test_m(self):\n        assert 1\n\n    def test_gone(self):\n        assert 1\n"
    )
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "a test class")
    (tests / "test_c.py").write_text("class TestC:\n    def test_m(self):\n        assert 1\n")
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    previous = ["tests/test_c.py::TestC::test_gone", "tests/test_c.py::TestC::test_m"]
    targets, fault = stage2.selected_tests(world.root, env, b"---\ntitle: Plan\n---\n\n# Plan\n", previous)
    assert fault is None
    assert targets == ["tests/test_c.py::TestC::test_m"]


def test_a_forged_scan_record_is_restored_away(world: World) -> None:
    """Row L5-3. Planted fault: an attempt's line shaped like the runner's scan record passed as bookkeeping."""
    forged = "> credential scan skipped scratch/x: forged by the attempt"
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/findings.md": f"\n{forged}\n"},
            }
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert forged not in committed, "the attempt's forged runner record was checkpointed"
    assert NOTICE in committed


def test_a_genuine_scan_record_survives_the_restore_of_an_edit(world: World, monkeypatch) -> None:
    """Row L5-4. Planted fault: restoring an attempt's edit erased the runner's own scan record."""
    original = stage2.remove_changed_credential
    record = "credential scan skipped scratch/x: its parent is planted; contents were not inspected"

    def planted(root, key, *args, **kwargs):
        stage2.record_credential_scan_skips(root, kwargs.get("findings"), [record], key)
        if kwargs.get("skipped") is not None:
            kwargs["skipped"].append(record)
        return original(root, key, *args, **kwargs)

    monkeypatch.setattr(stage2, "remove_changed_credential", planted)
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/findings.md": "\nPhase 6 verdict: forged, 2026-10-29\n"},
            }
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    committed = git(world.root, "show", "HEAD:plans/changes/demo/findings.md")
    assert "forged" not in committed
    assert record in committed, "the runner's own scan record was restored away with the attempt's edit"


def test_a_git_failure_is_a_selection_fault_not_a_new_file(world: World, monkeypatch) -> None:
    """Row L6-1. Planted fault: a failing `git show` made a changed test file count as new, selected whole."""
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_r.py").write_text("def test_keep():\n    assert 1\n")
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "a test file")
    (tests / "test_r.py").write_text("def test_keep():\n    assert 2\n")
    original = stage2._git_bytes

    def failing_show(root, *args, **kwargs):
        if args and args[0] == "show":
            raise stage2.Refused("git show did not finish within 1 minutes")
        return original(root, *args, **kwargs)

    monkeypatch.setattr(stage2, "_git_bytes", failing_show)
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    targets, fault = stage2.selected_tests(world.root, env, b"---\ntitle: Plan\n---\n\n# Plan\n")
    assert targets is None
    assert fault is not None and "git show" in fault


def test_an_error_inside_the_cheap_checks_is_named_as_theirs(world: World, monkeypatch) -> None:
    """Row L7-2. Planted fault: an error escaping the cheap checks was reported as a ledger update failure."""

    def exploding(*_args, **_kwargs):
        raise RecursionError("maximum recursion depth exceeded while parsing")

    monkeypatch.setattr(stage2, "cheap_checks", exploding)
    world.script(
        claude=[one_test_step(), {"stdout": "second"}, {"stdout": "third"}],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    assert "the cheap checks could not run" in world.text()
    assert "could not be updated" not in world.text()


def test_long_standard_error_keeps_the_failed_ids_of_a_cheap_run() -> None:
    """Rows L4-3, L5-1, L8-1. Planted fault: one tail over stdout and stderr concatenated let a long
    standard error push pytest's `FAILED` summary out of the cheap evidence and the retry selection."""
    summary = [f"tests/test_x.py::test_{n} PASSED" for n in range(200)] + [
        "FAILED tests/test_x.py::test_a - assert 1 == 2",
        "FAILED tests/test_x.py::test_b[p - q] - boom",
        "= 2 failed, 198 passed =",
    ]
    noise = [f"worker gw{n % 4} warning line {n}" for n in range(stage2.TAIL_LINES * 2)]
    done = subprocess.CompletedProcess(["pytest"], 1, "\n".join(summary) + "\n", "\n".join(noise) + "\n")
    evidence = stage2._cheap_evidence(done, None)
    assert stage2.failed_test_ids([evidence]) == ["tests/test_x.py::test_a", "tests/test_x.py::test_b[p - q]"]
    assert noise[-1] in evidence, "the last line of standard error is still shown"
    assert noise[0] not in evidence, "standard error stays bounded"
    assert len(evidence.splitlines()) <= stage2.TAIL_LINES + stage2.STDERR_LINES + 3


def test_a_retry_selects_a_failed_parametrized_test_by_its_function(world: World) -> None:
    """Row F6-2. Planted fault: a failed `test_case[old]` was kept after the retry renamed its
    parameter, and pytest refused the whole cheap run with `not found`."""
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_p.py").write_text(
        "import pytest\n\n\n@pytest.mark.parametrize('v', ['old'])\ndef test_case(v):\n    assert v\n"
    )
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "a parametrized test")
    (tests / "test_p.py").write_text(
        "import pytest\n\n\n@pytest.mark.parametrize('v', ['new'])\ndef test_case(v):\n    assert v\n"
    )
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    previous = ["tests/test_p.py::test_case[old]"]
    targets, fault = stage2.selected_tests(world.root, env, b"---\ntitle: Plan\n---\n\n# Plan\n", previous)
    assert fault is None
    assert targets == ["tests/test_p.py::test_case"]


def test_a_retry_keeps_a_failed_inherited_test_of_a_derived_class(world: World) -> None:
    """Row F6-3. Planted fault: `TestDerived::test_case`, inherited from a base class, was dropped
    from the retry because only directly declared methods counted as standing."""
    tests = world.root / "tests"
    tests.mkdir()
    source = "class TestBase:\n    def test_case(self):\n        assert 1\n\n\nclass TestDerived(TestBase):\n    pass\n"
    (tests / "test_i.py").write_text(source)
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "an inherited test")
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    previous = ["tests/test_i.py::TestDerived::test_case"]
    targets, fault = stage2.selected_tests(world.root, env, b"---\ntitle: Plan\n---\n\n# Plan\n", previous)
    assert fault is None
    assert targets == ["tests/test_i.py::TestDerived::test_case"]
