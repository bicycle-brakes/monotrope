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
    UTC_START,
    FakeClock,
    ScriptedPrograms,
    World,
    _beside_docs_gate,
    formatted_attempt,  # noqa: E402
    git,  # noqa: E402
    prompt_entry,  # noqa: E402
    red_verify,  # noqa: E402
    repair_step,  # noqa: E402
    runner_entries,  # noqa: E402
    script_repair,  # noqa: E402
    seed_tests,  # noqa: E402
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
CHEAP = "Runner cheap checks before post-run verification"


def overstaying_cheap_pytest(monkeypatch: pytest.MonkeyPatch) -> ScriptedPrograms:
    """The cheap pytest doubled at the `Popen` boundary to outlast `TOOL_SECONDS` on the fake clock.

    Spec criterion 4 of the runner clock: a budget expires through the clock seam, never by a real
    child sleeping past it, so the timeout costs no wall time.
    """
    clock = FakeClock(monkeypatch, UTC_START)

    def cheap_pytest(command: list[str]) -> bool:
        return command[:3] == [".venv/bin/python3", "-m", "pytest"] or (
            command[0].endswith("/.venv/bin/python3") and command[1:3] == ["-m", "pytest"]
        )

    return ScriptedPrograms(monkeypatch, clock, [(cheap_pytest, {"duration": stage2.TOOL_SECONDS + 1.0})])


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
    the runner names as missing and never passes to pytest - the attempt stays red because implement
    owes it), and on a retry exactly the ids the attempt before reported as failed
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
        "tests/test_new.py",
    ]
    assert calls[0]["argv"] == first
    # The retry adds exactly the surviving failed id; the deleted file's id is dropped.
    expected = sorted([*first[len(head) :], "tests/test_existing.py::test_keep"])
    assert calls[1]["argv"] == [*head, *expected]
    # The attempt before reported no id, so the third run holds the changed and ledger sources only.
    # The unwritten ledger id is named by the runner itself, never passed to pytest (bead
    # coding-harness-bxxt.9); the attempt stays red because implement owes it, not because pytest
    # saw the id.
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
    # A text-only attempt: it changes `src/app.py` alone, outside `scripts/` and `tests/`. The shared
    # helper `successful_implementation` also plants a covering test file, which rightly starts ruff
    # and pytest, so this guarantee states its own attempt.
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
            }
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0
    assert world.calls("ruff") == [] and world.calls("python3") == []
    assert len(world.calls("make")) == 1
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    assert stage2.cheap_checks(world.root, env, world.plan, None, None) == []


def test_cheap_green_still_requires_full_verification(world: World) -> None:
    """Ledger 5. Planted fault: an uncovered attempt checkpointed without `make verify`, or despite its red result.

    A targeted green checkpoints when the coverage is safe (no `make verify`); when it is not, the
    admitted full check runs and its red result still blocks the checkpoint (`decisions.md#Q-6`).
    """
    red = red_verify(("pytest", ["FAILED tests/test_b.py::test_b - assert 1 == 2"]))
    baseline = git(world.root, "rev-parse", "HEAD")
    # `src/app.py` is tracked code with no linked test: the coverage is not safe, so the full check runs.
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
            },
            {"stdout": "must not run"},
            {"stdout": "must not run"},
        ],
        make=[red] * 3,
    )
    assert world.run("implement") == 1
    # Since bead coding-harness-bxxt.6 the full check runs the gates of the one list itself, the world's
    # document gate (a seconds member of the verify job) before the protected `make verify`; it is counted
    # apart, so the full check's launch order stays exactly as pinned.
    names = [call["name"] for call in _beside_docs_gate(world.calls())]
    assert names[:2] == ["claude", "make"], names[:2]
    assert "make" in names, "the full check did not run for an uncovered attempt"
    assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "0", "a red full check checkpointed"


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
    # The fixture's seeded spec review carries one audit line of its own.
    assert world.text().count("Stage-2 call,") == 2
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
    assert world.text().count("Stage-2 call,") == 5, "an earlier attempt's audit line was erased"
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
    programs = overstaying_cheap_pytest(monkeypatch) if case == "timeout" else None
    baseline = git(world.root, "rev-parse", "HEAD")
    world.script(
        claude=[one_test_step(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        python3=[{}] * 3,
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    if programs is not None:
        assert [row["outcome"] for row in programs.waits()] == ["timeout"] * 3, "the overstay was not simulated"
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
    targets, fault, missing, faults = stage2.selected_tests(world.root, env, plan, previous)
    assert fault is None
    assert not missing and not faults, "a ledger-less plan names no missing test"
    # A failed parameter id is selected by its function (review row F6-2).
    assert targets == ["tests/test_r.py::test_keep", "tests/test_r.py::test_new"]


def test_a_timed_out_cheap_pytest_names_its_selected_tests(world: World, monkeypatch) -> None:
    """Row L1-10. Planted fault: the timeout diagnostic named only the command, not what it ran."""
    venv_ruff(world)
    venv_pytest(world)
    programs = overstaying_cheap_pytest(monkeypatch)
    world.script(
        claude=[one_test_step(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        python3=[{}] * 3,
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    assert [row["outcome"] for row in programs.waits()] == ["timeout"] * 3, "the overstay was not simulated"
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


def test_missing_ledger_test_in_new_file_is_excluded(world: World) -> None:
    """Row L3-1. Planted fault: a new test file selected whole hid the ledger test it lacks.

    Since bead coding-harness-bxxt.9 the whole file is still covered, but the ledger entry the
    attempt left unwritten is no longer a pytest target - the runner names it as missing instead
    (spec, criterion 3 and 5): the file id covers the standing tests, the missing id never reaches
    pytest.
    """
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_fresh.py").write_text("def test_other():\n    assert 1\n\n\ndef test_named():\n    assert 1\n")
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    plan = (
        "---\ntitle: Plan\n---\n\n# Plan\n\n## Criterion ledger\n\n"
        "- 1: tests/test_fresh.py::test_named — written in the new file\n"
        "- 2: not yet written tests/test_fresh.py::test_required — the attempt left it out\n"
    ).encode()
    targets, fault, missing, faults = stage2.selected_tests(world.root, env, plan)
    assert fault is None
    assert targets == ["tests/test_fresh.py"], "the whole new file is still covered, without the missing id"
    assert missing == {"tests/test_fresh.py::test_required": "not yet written"}
    assert faults == []


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
    targets, fault, missing, faults = stage2.selected_tests(
        world.root, env, b"---\ntitle: Plan\n---\n\n# Plan\n", previous
    )
    assert fault is None
    assert not missing and not faults, "a ledger-less plan names no missing test"
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
    targets, fault, missing, faults = stage2.selected_tests(world.root, env, b"---\ntitle: Plan\n---\n\n# Plan\n")
    assert targets is None
    assert not missing and not faults, "a selection fault preempts the ledger classification"
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


@pytest.mark.usefixtures("world")
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
    targets, fault, missing, faults = stage2.selected_tests(
        world.root, env, b"---\ntitle: Plan\n---\n\n# Plan\n", previous
    )
    assert fault is None
    assert not missing and not faults, "a ledger-less plan names no missing test"
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
    targets, fault, missing, faults = stage2.selected_tests(
        world.root, env, b"---\ntitle: Plan\n---\n\n# Plan\n", previous
    )
    assert fault is None
    assert not missing and not faults, "a ledger-less plan names no missing test"
    assert targets == ["tests/test_i.py::TestDerived::test_case"]


# ---------------------------------------------------------------------------
# The ledger classification before pytest (bead coding-harness-bxxt.9): the runner names every
# missing ledger test itself, before pytest starts, and a missing id is never one of pytest's
# arguments. Ledger rows 1-9 and 12-17 stand here; rows 10 and 11 stand in test_stage2.py beside
# the answer check they pin.
# ---------------------------------------------------------------------------

PYTEST_HEAD = ["-m", "pytest", "-q", "-n", "auto"]


def plan_with_ledger(entries: list[str]) -> str:
    """The accepted plan's text with the given criterion-ledger lines and a time section."""
    body = "".join(f"{entry}\n" for entry in entries)
    return (
        "---\ntitle: Plan\nupdated: 2026-09-30\nbead: demo-1\n---\n\n# Plan\n\n"
        f"## Criterion ledger\n\n{body}\n## Time used\n"
    )


def commit_tree(world: World, message: str) -> None:
    """Commit the tree as it stands, so the attempt's snapshot holds the plan's ledger."""
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", message)


def test_ledger_ids_are_checked_before_pytest(world: World) -> None:
    """Ledger 1. Planted fault: a missing ledger id reached pytest as a target id.

    The plan names four ledger tests: one standing, one defined only inside a string, one whose
    file is gone, one still unwritten. pytest runs the standing targets only - none of the three
    missing ids appears in its arguments - and the implement attempt fails naming all three.
    """
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_standing.py").write_text(
        "def test_standing():\n    assert 1\n\n\n_DECOY = '''\ndef test_in_string():\n    pass\n'''\n",
        encoding="utf-8",
    )
    venv_ruff(world)
    venv_pytest(world)
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: tests/test_standing.py::test_standing — written on an earlier change",
                "- 2: tests/test_standing.py::test_in_string — defined only inside a string",
                "- 3: tests/test_gone.py::test_gone — written once, its file is gone",
                "- 4: not yet written tests/test_later.py::test_later — nobody writes it",
            ]
        ),
        encoding="utf-8",
    )
    commit_tree(world, "a standing test and a plan with three missing ledger tests")
    world.script(
        claude=[one_test_step(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        python3=[{}, {}, {}],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    calls = world.calls("python3")
    assert calls[0]["argv"] == [*PYTEST_HEAD, "tests/test_new.py", "tests/test_standing.py::test_standing"]
    assert world.calls("make") == [], "a red cheap check still started `make verify`"
    text = world.text()
    assert "the criterion ledger names tests that do not stand, and this attempt owes them:" in text
    for ref in (
        "`tests/test_gone.py::test_gone` (written)",
        "`tests/test_later.py::test_later` (not yet written)",
        "`tests/test_standing.py::test_in_string` (written)",
    ):
        assert ref in text


def test_missing_ledger_ids_persist_in_attempt_record(world: World) -> None:
    """Ledger 2. Planted fault: a missing ledger id vanished from the attempt's own record.

    The repair is otherwise green - the unwritten-only missing test does not fail it - and its
    accepted attempt's measured time line still names the id (spec, criterion 2).
    """
    seed_tests(world)
    world.plan.write_text(
        plan_with_ledger(["- 1: not yet written tests/test_later.py::test_later — parked for a later change"]),
        encoding="utf-8",
    )
    commit_tree(world, "a plan whose ledger names an unwritten test")
    world.write_record([("L1-1", "taken — test_a", "no")])
    script_repair(world, [repair_step()], make=[{"stdout": "green\n"}])
    assert world.run("repair") == 0
    entry = runner_entries(world.plan)[-1]
    assert "tests/test_later.py::test_later" in entry, entry
    assert "named but not owed" in entry, entry


def test_standing_targets_run_when_ledger_ids_are_missing(world: World) -> None:
    """Ledger 3. Planted fault: a missing id replaced or blocked the standing targets."""
    venv_ruff(world)
    venv_pytest(world)
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: tests/test_new.py::test_new — written by this attempt",
                "- 2: not yet written tests/test_new.py::test_required — the attempt left it out",
            ]
        ),
        encoding="utf-8",
    )
    commit_tree(world, "a plan with a standing and an unwritten ledger test")
    world.script(
        claude=[one_test_step(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        python3=[{}, {}, {}],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    calls = world.calls("python3")
    assert calls[0]["argv"] == [*PYTEST_HEAD, "tests/test_new.py"], "the standing target did not run"
    assert "tests/test_new.py::test_required" not in calls[0]["argv"], "the missing id reached pytest"
    assert "tests/test_new.py::test_required" in world.text()


def test_only_missing_ledger_ids_skip_pytest(world: World) -> None:
    """Ledger 4. Planted fault: pytest started although no selected target stands."""
    venv_pytest(world)
    world.plan.write_text(
        plan_with_ledger(["- 1: not yet written tests/test_later.py::test_later — parked for a later change"]),
        encoding="utf-8",
    )
    commit_tree(world, "a plan whose only ledger test is unwritten and missing")
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {"plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n"},
            },
            {"stdout": "must not run"},
            {"stdout": "must not run"},
        ],
        make=[{"stdout": "green\n"}] * 3,
    )
    assert world.run("implement") == 1
    assert world.calls("python3") == [], "pytest started without a standing target"
    assert world.calls("make") == []
    text = world.text()
    assert "tests/test_later.py::test_later" in text
    assert "owes them" in text


def test_implement_fails_after_running_standing_tests_with_missing_ledger_ids(world: World) -> None:
    """Ledger 5. Planted fault: an implement attempt with a missing ledger test was accepted.

    The standing ledger test runs green; the attempt still fails, because implement owes the
    unwritten one too.
    """
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_standing.py").write_text("def test_standing():\n    assert 1\n", encoding="utf-8")
    venv_ruff(world)
    venv_pytest(world)
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: tests/test_standing.py::test_standing — written on an earlier change",
                "- 2: not yet written tests/test_later.py::test_later — parked for a later change",
            ]
        ),
        encoding="utf-8",
    )
    commit_tree(world, "a standing ledger test and an unwritten one")
    world.script(
        claude=[one_test_step(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        python3=[{}, {}, {}],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    calls = world.calls("python3")
    assert calls, "the standing ledger test never ran"
    assert calls[0]["argv"] == [*PYTEST_HEAD, "tests/test_new.py", "tests/test_standing.py::test_standing"]
    assert world.calls("make") == []
    assert "tests/test_later.py::test_later" in world.text()


def test_repair_accepts_unclaimed_unwritten_ledger_ids(world: World) -> None:
    """Ledger 6. Planted fault: a repair was rejected solely for an unwritten missing ledger test.

    The repair is green - its cheap pytest runs the standing targets without the missing id - and
    the run ends accepted with the row marked fixed (spec, criterion 6).
    """
    seed_tests(world)
    world.plan.write_text(
        plan_with_ledger(["- 1: not yet written tests/test_later.py::test_later — parked for a later change"]),
        encoding="utf-8",
    )
    commit_tree(world, "a plan whose ledger names an unwritten test")
    world.write_record([("L1-1", "taken — test_a", "no")])
    script_repair(world, [repair_step()], make=[{"stdout": "green\n"}])
    assert world.run("repair") == 0
    cheap = world.calls("python3")[0]["argv"]
    assert cheap == [*PYTEST_HEAD, "tests/test_fix.py"], "the unwritten missing id reached pytest"
    record = {row[0]: row[7] for row in stage2.record_rows(world.record().read_text(encoding="utf-8"))}
    assert record["L1-1"] == "fixed — tests/test_fix.py::test_fix"


@pytest.mark.parametrize(
    "entries",
    [
        ["- 1: tests/test_gone.py::test_gone — written once, its file is gone"],
        [
            "- 1: tests/test_gone.py::test_gone — written once, its file is gone",
            "- 2: not yet written tests/test_gone.py::test_gone — parked beside it",
        ],
    ],
    ids=["written-only", "written-and-unwritten"],
)
def test_repair_fails_for_missing_written_ledger_test(world: World, entries: list[str]) -> None:
    """Ledger 7. Planted fault: a missing written ledger test was excused by an unwritten duplicate.

    Written takes precedence: both parametrize cases owe the same missing written test, and every
    repair attempt fails at the cheap check before anything derived runs (spec, criterion 7).
    """
    seed_tests(world)
    world.plan.write_text(plan_with_ledger(entries), encoding="utf-8")
    commit_tree(world, "a plan whose ledger names a missing written test")
    world.write_record([("L1-1", "taken — test_a", "no")])
    script_repair(world, [repair_step()] * 3, make=[{"stdout": "green\n"}] * 3)
    assert world.run("repair") == 1
    assert world.calls("make") == []
    assert (
        "the criterion ledger names tests that do not stand, and this attempt owes them: "
        "`tests/test_gone.py::test_gone` (written)"
    ) in world.text()


def test_standing_test_failure_is_not_hidden_by_missing_ledger_ids(world: World) -> None:
    """Ledger 8. Planted fault: a red standing test was excused, or hid the missing ids.

    The findings hold the pytest failure and every missing ledger id beside it, and the attempt
    fails (spec, criterion 8).
    """
    venv_ruff(world)
    venv_pytest(world)
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: tests/test_new.py::test_new — written by this attempt",
                "- 2: not yet written tests/test_later.py::test_later — parked for a later change",
                "- 3: tests/test_gone.py::test_gone — written once, its file is gone",
            ]
        ),
        encoding="utf-8",
    )
    commit_tree(world, "a plan with a standing test and two missing ones")
    red = {"stdout": "FAILED tests/test_new.py::test_new - assert 1 == 2\n", "exit": 1}
    world.script(
        claude=[one_test_step(), {"stdout": "must not run"}, {"stdout": "must not run"}],
        python3=[red] * 3,
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 1
    text = world.text()
    assert "FAILED tests/test_new.py::test_new" in text, "the red standing test was hidden"
    assert "`tests/test_later.py::test_later` (not yet written)" in text
    assert "`tests/test_gone.py::test_gone` (written)" in text
    assert world.calls("make") == []


@pytest.mark.parametrize("case", ["unparseable", "invalid-bytes"])
def test_unreadable_or_invalid_ledger_test_is_not_missing(world: World, case: str) -> None:
    """Ledger 9. Planted fault: a read or parse error became a missing id, or the check stayed green.

    The fault names the input that cannot be read or parsed; the classification reports no missing
    id for it, and the cheap check fails on the fault (spec, criterion 9).
    """
    tests = world.root / "tests"
    tests.mkdir()
    target = tests / "test_broken.py"
    if case == "unparseable":
        target.write_text("def test_broken(:\n    pass\n", encoding="utf-8")
    else:
        target.write_bytes(b"\xff\xfe this file is not utf-8\n")
    commit_tree(world, "a ledger test file that cannot be read or parsed")
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    plan = (
        "---\ntitle: Plan\n---\n\n# Plan\n\n## Criterion ledger\n\n"
        "- 1: tests/test_broken.py::test_broken — written on an earlier change\n"
    ).encode()
    targets, fault, missing, faults = stage2.selected_tests(world.root, env, plan)
    assert fault is None
    assert missing == {}, "a read or parse error was diagnosed as a missing id"
    assert targets == [], "the check stayed green on an uninspectable ledger test"
    assert len(faults) == 1
    assert "tests/test_broken.py" in faults[0] and "cannot be read or parsed" in faults[0]
    problem = stage2.cheap_checks(world.root, env, world.plan, None, plan)
    assert problem, "the cheap check stayed green on an uninspectable ledger test"
    assert "cannot be read or parsed" in problem[0] and "tests/test_broken.py" in problem[0]


def test_implement_prompt_requires_all_ledger_tests(world: World) -> None:
    """Ledger 12. Planted fault: the implement prompt let an unwritten ledger test stay unwritten."""
    snapshot = plan_with_ledger(
        [
            "- 1: tests/test_fix.py::test_fix — written on an earlier change",
            "- 2: not yet written tests/test_new.py::test_new — the attempt writes it",
        ]
    )
    world.plan.write_text(snapshot, encoding="utf-8")
    ctx = stage2.Context(world.root, "demo", world.plan.parent, "demo-1")
    prompt = stage2.implementation_prompt(ctx, "baseline-sha", [])
    assert ("Write every test the ledger names, including the rows still marked `not yet written`") in prompt, (
        "the implement prompt permitted a missing unwritten ledger test"
    )
    for ref in ("tests/test_fix.py::test_fix", "tests/test_new.py::test_new"):
        assert ref in prompt, ref


def test_repair_prompt_distinguishes_finding_proof_from_unwritten_tests(world: World) -> None:
    """Ledger 13. Planted fault: the repair prompt owed every unwritten test, or omitted an obligation.

    Both prompt variants owe the findings' proofs and the written entries, name the missing
    unwritten tests without owing them, and never carry the implement prompt's all-tests sentence.
    """
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_standing.py").write_text("def test_standing():\n    assert 1\n", encoding="utf-8")
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: tests/test_standing.py::test_standing — written and standing",
                "- 2: tests/test_owed.py::test_owed — written once, its file is gone",
                "- 3: not yet written tests/test_later.py::test_later — parked for a later change",
            ]
        ),
        encoding="utf-8",
    )
    commit_tree(world, "a plan with a standing, a missing written and an unwritten ledger test")
    ctx = stage2.Context(world.root, "demo", world.plan.parent, "demo-1")
    for endpoint in (stage2.CODEX, stage2.GLM_FLASH):
        prompt = stage2.repair_prompt(ctx, "baseline-sha", [], [], endpoint=endpoint)
        assert "the proof of every finding it addresses" in prompt, endpoint
        assert "every written entry of the plan's criterion ledger, standing or missing" in prompt, endpoint
        assert "named but not owed" in prompt, endpoint
        assert "Write every test the ledger names" not in prompt, f"{endpoint} owes unwritten tests"
        refs = (
            "tests/test_standing.py::test_standing",
            "tests/test_owed.py::test_owed",
            "tests/test_later.py::test_later",
        )
        for ref in refs:
            assert f"- {ref}" in prompt, (endpoint, ref)


def test_repair_prompt_pytest_list_excludes_missing_ledger_ids(world: World) -> None:
    """Ledger 14. Planted fault: a missing id stood in the repair's pytest command list.

    The pytest line names the standing ledger tests as its targets; the sections after it hold the
    missing written and unwritten ids, and none of them stands in the pytest list (spec, criterion 14).
    """
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_standing.py").write_text("def test_standing():\n    assert 1\n", encoding="utf-8")
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: tests/test_standing.py::test_standing — written and standing",
                "- 2: tests/test_owed.py::test_owed — written once, its file is gone",
                "- 3: not yet written tests/test_later.py::test_later — parked for a later change",
            ]
        ),
        encoding="utf-8",
    )
    commit_tree(world, "a plan with a standing, a missing written and an unwritten ledger test")
    ctx = stage2.Context(world.root, "demo", world.plan.parent, "demo-1")
    prompt = stage2.repair_prompt(ctx, "baseline-sha", [], [], endpoint=stage2.CODEX)
    assert "`.venv/bin/python3 -m pytest -q -n auto` over the standing ledger tests below" in prompt
    assert (
        "Standing ledger tests, the pytest targets - run them and leave them green:\n"
        "- tests/test_standing.py::test_standing"
    ) in prompt
    assert (
        "Written ledger entries whose test is missing - owed: write them:\n- tests/test_owed.py::test_owed"
    ) in prompt
    assert (
        "Missing unwritten ledger tests - named but not owed, never passed to pytest:\n"
        "- tests/test_later.py::test_later"
    ) in prompt


def test_missing_ledger_file_is_reported_as_missing(world: World) -> None:
    """Ledger 15. Planted fault: an absent file was diagnosed as an unreadable existing file.

    Both ids of files that do not exist are missing, each with its entry's state; no fault is named
    (spec, criterion 15).
    """
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    plan = plan_with_ledger(
        [
            "- 1: tests/test_gone.py::test_gone — written once, its file is gone",
            "- 2: not yet written tests/test_absent.py::test_absent — parked for a later change",
        ]
    ).encode()
    targets, fault, missing, faults = stage2.selected_tests(world.root, env, plan)
    assert fault is None and faults == []
    assert missing == {
        "tests/test_gone.py::test_gone": "written",
        "tests/test_absent.py::test_absent": "not yet written",
    }
    assert targets == []


def test_repair_prompt_reports_uninspectable_ledger_test(world: World) -> None:
    """Ledger 16. Planted fault: prompt construction refused, or named the uninspectable test standing.

    The prompt still builds: the standing section holds the standing ref alone, the uninspectable
    file is named as unreadable in its own section, and no ledger ref of it is listed (spec, criterion 16).
    """
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_standing.py").write_text("def test_standing():\n    assert 1\n", encoding="utf-8")
    (tests / "test_broken.py").write_text("def test_broken(:\n    pass\n", encoding="utf-8")
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: tests/test_standing.py::test_standing — written and standing",
                "- 2: tests/test_broken.py::test_broken — written on an earlier change",
            ]
        ),
        encoding="utf-8",
    )
    commit_tree(world, "a standing and an unparseable ledger test file")
    ctx = stage2.Context(world.root, "demo", world.plan.parent, "demo-1")
    prompt = stage2.repair_prompt(ctx, "baseline-sha", [], [], endpoint=stage2.CODEX)
    assert (
        "Standing ledger tests, the pytest targets - run them and leave them green:\n"
        "- tests/test_standing.py::test_standing"
    ) in prompt
    assert "Ledger tests the runner cannot inspect" in prompt
    listed = [line for line in prompt.splitlines() if line.startswith("- ")]
    assert any("test_broken.py" in line and "cannot be read or parsed" in line for line in listed)
    assert not any(line.startswith("- tests/test_broken.py") for line in listed), "named as standing"


def test_malformed_ledger_entry_is_not_selected(world: World) -> None:
    """Ledger 17. Planted fault: a malformed entry was selected or named as a missing ledger test.

    The line in no recognized entry form is left to the criterion-ledger gate: the cheap selection
    neither sends it to pytest nor reports it as missing (spec, criterion 17).
    """
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_real.py").write_text("def test_real():\n    assert 1\n", encoding="utf-8")
    commit_tree(world, "a standing test file")
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    plan = plan_with_ledger(
        [
            "- 1: tests/test_real.py::test_real — written and standing",
            "- 2: someday tests/test_malformed.py::test_someday — no recognized entry form",
        ]
    ).encode()
    targets, fault, missing, faults = stage2.selected_tests(world.root, env, plan)
    assert fault is None and missing == {} and faults == []
    assert targets == ["tests/test_real.py::test_real"]


def test_implement_prompt_separates_standing_and_missing_ledger_tests(world: World) -> None:
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_standing.py").write_text("def test_standing():\n    pass\n", encoding="utf-8")
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: tests/test_standing.py::test_standing — standing",
                "- 2: not yet written tests/test_later.py::test_later — owed",
            ]
        ),
        encoding="utf-8",
    )
    ctx = stage2.Context(world.root, "demo", world.plan.parent, "demo-1")
    prompt = stage2.implementation_prompt(ctx, "baseline-sha", [])
    assert (
        "Standing ledger tests, the runner will run these pytest targets:\n- tests/test_standing.py::test_standing"
        in prompt
    )
    assert (
        "Missing ledger tests - owed: write them for the runner to check:\n- tests/test_later.py::test_later" in prompt
    )


def test_owed_ledger_diagnostic_is_protected_and_bounded(world: World, monkeypatch) -> None:
    monkeypatch.setattr(stage2, "format_targets", lambda *_args: [])
    missing = {f"tests/test_{i}.py::test_secretvalue_{i}": "written" for i in range(100)}
    monkeypatch.setattr(stage2, "selected_tests", lambda *_args: ([], None, missing, []))
    problems = stage2.cheap_checks(world.root, {}, world.plan, "secretvalue", b"plan")
    assert len(problems) == 1
    assert "secretvalue" not in problems[0]
    assert len(problems[0].splitlines()) <= stage2.TAIL_LINES
    assert "left out" in problems[0]


def test_repair_uninspectable_prompt_does_not_invent_obligation(world: World) -> None:
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_bad.py").write_text("def test_bad(:\n", encoding="utf-8")
    plan = plan_with_ledger(["- 1: not yet written tests/test_bad.py::test_bad — pending"])
    text = stage2.repair_must_run_refs(world.root, plan.encode())
    assert "cannot inspect" in text and "test_bad.py" in text
    assert "owed as written entries" not in text
    assert "cheap check fails" in text


def test_retired_ledger_reference_helper_is_removed() -> None:
    assert not hasattr(stage2, "_ledger_test_refs"), "retired selection helper still exists"


def test_implement_prompt_delegates_ledger_checks(world: World) -> None:
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_standing.py").write_text("def test_standing():\n    pass\n", encoding="utf-8")
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: tests/test_standing.py::test_standing — standing",
                "- 2: not yet written tests/test_missing.py::test_missing — missing",
            ]
        ),
        encoding="utf-8",
    )
    ctx = stage2.Context(world.root, "demo", world.plan.parent, "demo-1")
    prompt = stage2.implementation_prompt(ctx, "baseline", [])
    assert "You cannot run commands" in prompt
    assert "runner will run these pytest targets" in prompt
    assert "write them for the runner to check" in prompt
    assert "standing accepted plan ledger tests" in prompt
    assert "run them and leave them green" not in prompt


def test_repair_prompts_do_not_claim_implement_file_guard(world: World) -> None:
    ctx = stage2.Context(world.root, "demo", world.plan.parent, "demo-1")
    for endpoint in (stage2.CODEX, stage2.GLM_FLASH):
        prompt = stage2.repair_prompt(ctx, "baseline", [], [], endpoint=endpoint)
        assert "Implement refuses new production code" not in prompt


def test_workflow_repair_describes_standing_pytest_targets() -> None:
    text = (Path(stage2.__file__).resolve().parent.parent / "docs/WORKFLOW.md").read_text(encoding="utf-8")
    section = text.split("**Red first:**", 1)[1].split("Post-run verification", 1)[0]
    assert "standing ledger tests as pytest targets" in section
    assert "missing unwritten" in section and "not owed" in section
    assert "ruff and them itself" not in section


@pytest.mark.parametrize("selection_fault", [False, True])
def test_ledger_fault_preserves_classified_missing_ids(world: World, monkeypatch, selection_fault: bool) -> None:
    monkeypatch.setattr(stage2, "format_targets", lambda *_: [])
    missing = {"tests/test_missing.py::test_missing": "written", "tests/test_later.py::test_later": "not yet written"}
    monkeypatch.setattr(
        stage2,
        "selected_tests",
        lambda *_: (
            None if selection_fault else [],
            "selection failed" if selection_fault else None,
            missing,
            ["tests/test_bad.py cannot be read or parsed"],
        ),
    )
    evidence: list[str] = []
    problems = stage2.cheap_checks(world.root, {}, world.plan, None, b"plan", verb="repair", evidence=evidence)
    assert problems and "test_missing.py::test_missing" in "\n".join(problems)
    assert "test_later.py::test_later" in "\n".join(evidence)
    assert "selection failed" in problems[0] if selection_fault else "test_bad.py" in problems[0]


def test_unowed_ledger_evidence_is_bounded(world: World, monkeypatch) -> None:
    monkeypatch.setattr(stage2, "format_targets", lambda *_: [])
    missing = {f"tests/test_{i}.py::test_{i}": "not yet written" for i in range(200)}
    monkeypatch.setattr(stage2, "selected_tests", lambda *_: ([], None, missing, []))
    evidence: list[str] = []
    assert stage2.cheap_checks(world.root, {}, world.plan, None, b"plan", verb="repair", evidence=evidence) == []
    assert len(evidence) <= stage2.TAIL_LINES
    assert any("left out" in line for line in evidence)


def test_ledger_classification_recognizes_async_test(world: World) -> None:
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_async.py").write_text("async def test_async():\n    pass\n", encoding="utf-8")
    standing, missing, faults = stage2.ledger_standings(
        world.root,
        plan_with_ledger(
            [
                "- 1: tests/test_async.py::test_async — async test",
            ]
        ).encode(),
    )
    assert "tests/test_async.py::test_async" in standing
    assert not missing and not faults


def test_lint_failure_precedes_missing_ledger_classification(world: World, monkeypatch) -> None:
    monkeypatch.setattr(stage2, "format_targets", lambda *_: ["scripts/example.py"])
    monkeypatch.setattr(stage2, "_cheap_ruff", lambda *_: "ruff found an error")

    def forbidden(*_):
        pytest.fail("ledger selection ran after red lint")

    monkeypatch.setattr(stage2, "selected_tests", forbidden)
    evidence: list[str] = []
    problems = stage2.cheap_checks(world.root, {}, world.plan, None, b"plan", evidence=evidence)
    assert problems == ["ruff found an error"] and not evidence


def test_claimed_unwritten_missing_ledger_proof_is_rejected_later(world: World) -> None:
    seed_tests(world)
    world.plan.write_text(
        plan_with_ledger(
            [
                "- 1: not yet written tests/test_later.py::test_later — pending",
            ]
        ),
        encoding="utf-8",
    )
    commit_tree(world, "ledger with missing unwritten proof")
    world.write_record([("L1-1", "taken — test_a", "no")])
    script_repair(
        world,
        [repair_step(stdout="L1-1: fixed — tests/test_later.py::test_later"), repair_step()],
        make=[{"stdout": "green\n"}] * 2,
    )
    assert world.run("repair") == 0
    prompt = world.calls("codex")[1]["argv"][-1]
    assert "tests/test_later.py::test_later defines no function" in prompt


def test_unparseable_ledger_file_keeps_other_missing_ids(world: World) -> None:
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_bad.py").write_text("def test_bad(:\n", encoding="utf-8")
    plan = plan_with_ledger(
        [
            "- 1: tests/test_bad.py::test_bad — broken",
            "- 2: tests/test_gone.py::test_gone — written",
            "- 3: not yet written tests/test_later.py::test_later — pending",
        ]
    ).encode()
    commit_tree(world, "broken ledger input")
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    evidence: list[str] = []
    problems = stage2.cheap_checks(world.root, env, world.plan, None, plan, verb="repair", evidence=evidence)
    assert "test_bad.py" in "\n".join(problems)
    assert "test_gone.py::test_gone" in "\n".join(problems)
    assert "test_later.py::test_later" in "\n".join(evidence)


def test_whole_file_filter_drops_nonstanding_explicit_target(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """A future target source cannot pass an absent name alongside a whole file to pytest."""
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_fresh.py").write_text("def test_present():\n    pass\n", encoding="utf-8")
    monkeypatch.setattr(stage2, "ledger_standings", lambda *_: (["tests/test_fresh.py::test_absent"], {}, []))
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    targets, fault, _, _ = stage2.selected_tests(world.root, env, b"")
    assert fault is None
    assert targets == ["tests/test_fresh.py"]


def test_late_credential_refusal_keeps_missing_ledger_record(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """A credential discovered after diagnostics were decided still leaves the missing test in the record."""
    verified = False

    def verify(*_args, **kwargs):
        nonlocal verified
        verified = True
        kwargs["evidence"].append("missing ledger test, named but not owed: `tests/test_later.py::test_later`")
        return []

    def scan(*_args, **kwargs):
        return [Path("src/app.py")] if verified and "findings" in kwargs else []

    monkeypatch.setattr(stage2, "verify_attempt", verify)
    monkeypatch.setattr(stage2, "remove_changed_credential", scan)
    world.script(claude=[{"stdout": "done", "plant": {"src/app.py": "value = 2\n"}}])
    assert world.run("implement") == 2
    assert "tests/test_later.py::test_later" not in runner_entries(world.plan)[-1]
    assert "tests/test_later.py::test_later" in world.text()


@pytest.mark.parametrize("verb", ["implement", "repair"])
def test_missing_ledger_truncation_names_diagnostic_lines(world: World, verb: str) -> None:
    """A bounded list of missing tests must not describe its omitted lines as a gate."""
    plan = plan_with_ledger(
        [f"- {n}: not yet written tests/test_missing.py::test_missing_{n} — later" for n in range(100)]
    ).encode()
    evidence: list[str] = []
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    problems = stage2.cheap_checks(world.root, env, world.plan, None, plan, verb=verb, evidence=evidence)
    record = "\n".join([*problems, *evidence])
    assert "lines of this gate left out" not in record
    assert "lines left out" in record


def test_ledger_parse_fault_survives_many_missing_tests(world: World, monkeypatch) -> None:
    tests = world.root / "tests"
    tests.mkdir()
    (tests / "test_broken.py").write_text("def test_bad(:\n", encoding="utf-8")
    commit_tree(world, "an unparseable test file")
    plan = plan_with_ledger(
        ["- 1: tests/test_broken.py::test_bad — broken"]
        + [f"- {i + 2}: tests/test_absent.py::test_missing_{i} — written" for i in range(100)]
    ).encode()
    monkeypatch.setattr(stage2, "format_targets", lambda *_: [])
    env = stage2.runner_env(stage2.foreign_env({}), world.root)
    problems = stage2.cheap_checks(world.root, env, world.plan, None, plan)
    diagnostic = "\n".join(problems)
    assert "tests/test_broken.py" in diagnostic and "cannot be read or parsed" in diagnostic
    assert "left out" in diagnostic


def test_repair_prompt_names_file_when_stat_is_denied(world: World, monkeypatch) -> None:
    target = world.root / "tests" / "test_denied.py"
    original_is_file = Path.is_file

    def denied(path: Path) -> bool:
        if path == target:
            raise PermissionError("parent directory is not searchable")
        return original_is_file(path)

    monkeypatch.setattr(Path, "is_file", denied)
    plan = plan_with_ledger(["- 1: tests/test_denied.py::test_denied — written"]).encode()
    prompt = stage2.repair_must_run_refs(world.root, plan)
    assert "tests/test_denied.py" in prompt and "cannot be read or parsed" in prompt
    assert "plan's criterion ledger could not be read" not in prompt
