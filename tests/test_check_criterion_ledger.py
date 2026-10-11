"""The gate `criterion-ledger`: every test a plan names for a criterion still exists.

Criteria 1-23 of plans/changes/criterion-test-ledger/spec.md. Every tree
a test runs over is built in `tmp_path`; the only files of this repository
read are the ones that travel with the kit (`decisions/gates.yaml`, the kit
manifest through `probe`, two phase prompts, `docs/WORKFLOW.md`). Each test
stands next to the fault that turns it red.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_criterion_ledger.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "kit"))
import check_criterion_ledger as gate  # noqa: E402
import probe  # noqa: E402

# --- helpers: every test builds its own tree -------------------------------


def _tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "plans" / "changes").mkdir(parents=True, exist_ok=True)
    return root


def _put(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _put_bytes(root: Path, rel: str, raw: bytes) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def _spec(count: int, body: str = "") -> str:
    numbers = "\n".join(f"{n}. Criterion {n} holds." for n in range(1, count + 1))
    return f"# Spec\n\n## Acceptance criteria\n\n{numbers}\n{body}"


def _ledger(*lines: str) -> str:
    return "## Criterion ledger\n\n" + "\n".join(lines) + "\n"


def _plan_text(ledger: str, date_line: str | None = "date: 2026-10-11") -> str:
    header = "---\ntitle: plan\n"
    if date_line is not None:
        header += f"{date_line}\n"
    return f"{header}---\n\n# Plan\n\n{ledger}"


def _test_file(*names: str) -> str:
    return "".join(f"def {name}() -> None:\n    pass\n\n" for name in names)


def _run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )


# --- criterion 1: live plans are held, whatever their date and class --------


def test_every_live_plan_is_held_whatever_its_date_and_class(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/old/spec.md", _spec(1))
    old = "---\ntitle: plan\ndate: 2026-09-01\nclass: bounded\n---\n\n# Plan\n"
    _put(root, "plans/changes/old/plan.md", old)
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "plans/changes/old/plan.md" in done.stdout


def test_a_live_change_without_a_plan_is_not_examined(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/only-research/research.md", "# Research\n")
    done = _run(root)
    assert done.returncode == 0, done.stdout
    assert "only-research" not in done.stdout
    assert "examined nothing" in done.stdout


# --- criterion 2: no ledger section, or more than one -----------------------


def test_a_plan_without_exactly_one_ledger_section_is_reported(tmp_path: Path) -> None:
    plain = "---\ntitle: plan\ndate: 2026-10-11\n---\n\n# Plan\n"
    for plan, marker in (
        (plain, 'no "## Criterion ledger" section'),
        (_plan_text(_ledger("- 1: not a test — review") + "\n" + _ledger("- 1: not a test — review")), "sections"),
        (
            plain.replace("# Plan\n", "# Plan\n\n```\n## Criterion ledger\n```\n"),
            'no "## Criterion ledger" section',
        ),
    ):
        root = _tree(tmp_path)
        _put(root, "plans/changes/x/spec.md", _spec(1))
        _put(root, "plans/changes/x/plan.md", plan)
        done = _run(root)
        assert done.returncode == 1, (marker, done.stdout)
        assert marker in done.stdout, done.stdout


# --- criteria 3 and 4: archived plans, held or exempt -----------------------


def test_an_archived_ledger_is_held_whatever_its_date(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/archive/old/spec.md", _spec(1))
    _put(
        root,
        "plans/changes/archive/old/plan.md",
        _plan_text(_ledger("- 1: tests/test_gone.py::test_deleted"), "date: 2026-10-01"),
    )
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "test_deleted" in done.stdout


def test_an_archived_plan_without_a_ledger_is_exempt_only_by_an_earlier_plain_date(tmp_path: Path) -> None:
    cases = [
        ("date: 2026-10-10", 0),
        ("date: 2026-10-11", 1),
        ('date: "2026-10-01"', 1),
        ("date: 2026-10-01 # old", 1),
        ("created: 2026-10-01", 1),
        ("date: 2026-02-30", 1),
        ("date: 2026-10-01\ndate: 2026-10-02", 1),
    ]
    for date_line, expected in cases:
        root = _tree(tmp_path)
        _put(
            root,
            "plans/changes/archive/old/plan.md",
            f"---\ntitle: plan\n{date_line}\n---\n\n# Plan\n",
        )
        done = _run(root)
        assert done.returncode == expected, (date_line, done.stdout, done.returncode)
        if expected == 0:
            assert "1 archived plan dated before 2026-10-11 exempt" in done.stdout, date_line


# --- criterion 5: the entry forms -------------------------------------------


def test_a_line_in_no_entry_form_is_reported_with_the_three_forms(tmp_path: Path) -> None:
    bad_lines = [
        "* 3: tests/test_a.py::test_b",
        "3: tests/test_a.py::test_b",
        "- 3: `tests/test_a.py::test_b`",
        "- 03: tests/test_a.py::test_b",
        "- 3: tests/test_a.py::TestA::test_b",
        "- 3: tests/test_a.py::test_b[case]",
        "- 3: tests/helpers.py::test_b",
        "- 3: tests/test_a.py::test_b - a hyphen for the dash",
        "- 3: not a test",
        "A sentence of prose instead of an entry.",
        "  - 3: tests/test_a.py::test_b",
    ]
    for line in bad_lines:
        root = _tree(tmp_path)
        _put(root, "plans/changes/x/spec.md", _spec(1))
        _put(root, "plans/changes/x/plan.md", _plan_text(_ledger(line)))
        done = _run(root)
        assert done.returncode == 1, (line, done.stdout)
        findings = [ln for ln in done.stdout.splitlines() if "none of the three entry forms" in ln]
        assert findings, (line, done.stdout)
        finding = findings[0]
        assert finding.startswith("plans/changes/x/plan.md:"), (line, finding)
        assert "- <n>: tests/<file>::<function>" in finding
        assert "not yet written tests/<file>::<function>" in finding
        assert "not a test — <what holds it>" in finding


def test_the_three_entry_forms_and_continuation_lines_are_read(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    ledger = _ledger(
        "- 1: tests/test_example.py::test_a",
        "- 2: tests/test_example.py::test_b — the fault that turns it red",
        "- 3: not yet written tests/test_example.py::test_c",
        "- 4: not a test — review holds this one",
        "- 4: not a test — a command holds this one",
        "- 5: not yet written tests/test_example.py::test_d",
        "  — the fault stands on the line below its entry",
    )
    _put(root, "plans/changes/x/spec.md", _spec(5))
    _put(root, "plans/changes/x/plan.md", _plan_text(ledger))
    _put(root, "tests/test_example.py", _test_file("test_a", "test_b"))
    done = _run(root)
    assert done.returncode == 0, (done.stdout, done.stderr)
    assert "held 1 plan (1 live, 0 archived)" in done.stdout
    assert "read 6 entries (2 test, 2 not yet written, 2 not a test)" in done.stdout


# --- criteria 6 and 7: a defined function, found by text --------------------


def test_the_gate_goes_red_when_a_named_test_is_deleted(tmp_path: Path) -> None:
    ledger = _ledger("- 1: tests/test_example.py::test_a")
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(1))
    _put(root, "plans/changes/x/plan.md", _plan_text(ledger))
    _put(root, "tests/test_example.py", _test_file("test_a"))
    assert _run(root).returncode == 0
    (root / "tests" / "test_example.py").unlink()
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "test_example.py" in done.stdout
    _put(root, "tests/test_example.py", _test_file("test_other"))
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert '"test_a" is not defined in tests/test_example.py' in done.stdout


def test_a_prefix_or_an_indented_def_is_not_defined(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(1))
    _put(root, "plans/changes/x/plan.md", _plan_text(_ledger("- 1: tests/test_example.py::test_b")))
    body = (
        "def test_b_more() -> None:\n    pass\n\n\n"
        "class Wrapper:\n    def test_b(self) -> None:\n        pass\n\n\n"
        "def outer() -> None:\n    def test_b() -> None:\n        pass\n"
    )
    _put(root, "tests/test_example.py", body)
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert '"test_b" is not defined' in done.stdout


def test_the_gate_never_imports_a_named_test_file(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(1))
    _put(root, "plans/changes/x/plan.md", _plan_text(_ledger("- 1: tests/test_example.py::test_a")))
    module = (
        "from pathlib import Path\n"
        '(Path(__file__).resolve().parent / "imported_marker").write_text("imported", encoding="utf-8")\n\n\n'
        "def test_a() -> None:\n    pass\n"
    )
    _put(root, "tests/test_example.py", module)
    done = _run(root)
    assert done.returncode == 0, done.stdout
    assert not (root / "tests" / "imported_marker").exists()


# --- criteria 8 to 11: the not-yet-written and not-a-test kinds -------------


def test_a_live_not_yet_written_entry_is_accepted(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(1))
    promised = _plan_text(_ledger("- 1: not yet written tests/test_example.py::test_a"))
    _put(root, "plans/changes/x/plan.md", promised)
    done = _run(root)
    assert done.returncode == 0, done.stdout


def test_a_not_yet_written_entry_whose_test_exists_is_reported(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(1))
    promised = _plan_text(_ledger("- 1: not yet written tests/test_example.py::test_a"))
    _put(root, "plans/changes/x/plan.md", promised)
    _put(root, "tests/test_example.py", _test_file("test_a"))
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "remove `not yet written`" in done.stdout


def test_an_archived_not_yet_written_entry_is_reported(tmp_path: Path) -> None:
    ledger = _ledger("- 1: not yet written tests/test_example.py::test_a")
    for test_file in (None, _test_file("test_a")):
        root = _tree(tmp_path)
        _put(root, "plans/changes/archive/x/spec.md", _spec(1))
        _put(root, "plans/changes/archive/x/plan.md", _plan_text(ledger, "date: 2026-10-01"))
        if test_file is not None:
            _put(root, "tests/test_example.py", test_file)
        done = _run(root)
        assert done.returncode == 1, done.stdout
        assert "not-yet-written entry" in done.stdout


def test_a_not_a_test_entry_is_accepted_on_its_form(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    ledger = _ledger(
        "- 1: not a test — the phase-6 review reads the help text against the spec",
        "- 2: not a test — tests/test_missing.py::test_gone would hold it, but nothing checks that",
    )
    _put(root, "plans/changes/x/spec.md", _spec(2))
    _put(root, "plans/changes/x/plan.md", _plan_text(ledger))
    done = _run(root)
    assert done.returncode == 0, done.stdout


# --- criteria 12 to 14: coverage, both ways ---------------------------------


def test_a_criterion_without_an_entry_is_reported(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(2))
    _put(root, "plans/changes/x/plan.md", _plan_text(_ledger("- 1: not a test — review holds it")))
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "criterion 2 has no entry" in done.stdout


def test_an_entry_for_an_unknown_criterion_is_reported(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(16))
    ledger = _ledger(
        "- 1: tests/test_example.py::test_a",
        "- 99: tests/test_example.py::test_a",
    )
    _put(root, "plans/changes/x/plan.md", _plan_text(ledger))
    _put(root, "tests/test_example.py", _test_file("test_a"))
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "criterion 99" in done.stdout


def test_a_plan_without_a_spec_or_its_criteria_is_reported(tmp_path: Path) -> None:
    ledger = _ledger("- 1: not a test — review holds it")
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/plan.md", _plan_text(ledger))
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "spec.md" in done.stdout and "cannot be read" in done.stdout
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", "# Spec\n\nNothing numbered here.\n")
    _put(root, "plans/changes/x/plan.md", _plan_text(ledger))
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "no criterion number" in done.stdout


def test_criterion_numbers_are_read_across_level_3_headings_and_outside_fences(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    body = (
        "\n### A level-3 heading does not end the section\n\n"
        "2. Criterion two holds.\n\n"
        "```text\n9. A numbered line inside a fence is no criterion.\n```\n\n## Later\n"
    )
    _put(root, "plans/changes/x/spec.md", _spec(1, body))
    ledger = _ledger("- 1: not a test — review holds it", "- 2: not a test — review holds it")
    _put(root, "plans/changes/x/plan.md", _plan_text(ledger))
    done = _run(root)
    assert done.returncode == 0, done.stdout


# --- criteria 15 to 18: what a run says -------------------------------------


def test_a_clean_run_names_its_counts(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(3))
    ledger = _ledger(
        "- 1: tests/test_example.py::test_a",
        "- 2: tests/test_example.py::test_b — the fault",
        "- 3: not a test — review holds it",
    )
    _put(root, "plans/changes/x/plan.md", _plan_text(ledger))
    _put(root, "tests/test_example.py", _test_file("test_a", "test_b"))
    _put(root, "plans/changes/archive/old/plan.md", "---\ntitle: plan\ndate: 2026-10-10\n---\n\n# Plan\n")
    done = _run(root)
    assert done.returncode == 0, (done.stdout, done.stderr)
    assert "held 1 plan (1 live, 0 archived)" in done.stdout
    assert "read 3 entries (2 test, 0 not yet written, 1 not a test)" in done.stdout
    assert "1 archived plan dated before 2026-10-11 exempt" in done.stdout


def test_an_empty_tree_says_it_examined_nothing(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    done = _run(root)
    assert done.returncode == 0, done.stdout
    assert "examined nothing" in done.stdout
    assert "OK" not in done.stdout
    assert "pass" not in done.stdout
    assert "green" not in done.stdout


def test_each_finding_is_one_line_with_path_line_and_remedy(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(1))
    _put(root, "plans/changes/x/plan.md", _plan_text(_ledger("3: tests/test_a.py::test_b")))
    done = _run(root)
    assert done.returncode == 1, done.stdout
    lines = done.stdout.splitlines()
    assert lines
    for line in lines:
        assert line.startswith("plans/changes/"), line
        assert " — " in line, line
    numbered = [line for line in lines if line.split(":")[1].isdigit()]
    assert numbered, lines
    summary = done.stderr.splitlines()
    assert any("findings in" in line for line in summary)


def test_an_unreadable_or_non_utf8_file_is_a_finding(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put_bytes(root, "plans/changes/x/plan.md", b"\xff\xfe bad bytes")
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "not valid UTF-8" in done.stdout
    assert "Traceback" not in done.stderr
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/plan.md", _plan_text(_ledger("- 1: not a test — review holds it")))
    _put_bytes(root, "plans/changes/x/spec.md", b"\xff\xfe bad bytes")
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "not valid UTF-8" in done.stdout
    assert "Traceback" not in done.stderr
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(1))
    _put(root, "plans/changes/x/plan.md", _plan_text(_ledger("- 1: tests/test_example.py::test_a")))
    (root / "tests" / "test_example.py").mkdir(parents=True)
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "cannot be read" in done.stdout
    assert "Traceback" not in done.stderr


def test_an_empty_plan_or_spec_is_reported_without_a_traceback(tmp_path: Path) -> None:
    """Review-loop row L1-1: `ord("")` raised on an empty file. Fault: test the
    byte-order mark with `ord(text[:1])` again and this run tracebacks."""
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(1))
    _put(root, "plans/changes/x/plan.md", "")
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert 'no "## Criterion ledger" section' in done.stdout
    assert "Traceback" not in done.stderr
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", "")
    _put(root, "plans/changes/x/plan.md", _plan_text(_ledger("- 1: not a test — review holds it")))
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "Traceback" not in done.stderr


def test_a_doubled_ledger_heading_on_the_last_line_is_reported(tmp_path: Path) -> None:
    """Review-loop row L1-2: an empty second section raised IndexError. Fault:
    read the line as `sections[1][0][0]` again and this run tracebacks."""
    root = _tree(tmp_path)
    _put(root, "plans/changes/x/spec.md", _spec(1))
    plan = _plan_text(_ledger("- 1: not a test — review holds it")) + "\n## Criterion ledger"
    _put(root, "plans/changes/x/plan.md", plan)
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert "sections — keep exactly one" in done.stdout
    last = len(plan.split("\n"))
    assert f"plans/changes/x/plan.md:{last}:" in done.stdout, done.stdout
    assert "Traceback" not in done.stderr


def test_a_not_yet_written_entry_whose_file_cannot_be_read_is_reported(tmp_path: Path) -> None:
    """Review-loop row L1-3: only a missing file may stand as not yet written.
    Fault: discard the read reason again and both runs go green."""
    promised = _plan_text(_ledger("- 1: not yet written tests/test_example.py::test_a"))
    for case, make in (
        ("directory", lambda root: (root / "tests" / "test_example.py").mkdir(parents=True)),
        ("bytes", lambda root: _put_bytes(root, "tests/test_example.py", b"\xff\xfe bad bytes")),
    ):
        root = _tree(tmp_path / case)
        _put(root, "plans/changes/x/spec.md", _spec(1))
        _put(root, "plans/changes/x/plan.md", promised)
        make(root)
        done = _run(root)
        assert done.returncode == 1, done.stdout
        assert "make the file readable UTF-8" in done.stdout


def test_the_summary_counts_a_change_with_plan_and_spec_findings_once(tmp_path: Path) -> None:
    """Review-loop row L1-5: findings on plan.md and spec.md of one change are
    one plan. Fault: count distinct finding paths and the summary says 2 plans."""
    root = _tree(tmp_path)
    _put_bytes(root, "plans/changes/x/spec.md", b"\xff\xfe bad bytes")
    _put(root, "plans/changes/x/plan.md", _plan_text(_ledger("- 1: tests/test_gone.py::test_a")))
    done = _run(root)
    assert done.returncode == 1, done.stdout
    assert {"plans/changes/x/plan.md", "plans/changes/x/spec.md"} <= {
        line.split(":")[0] for line in done.stdout.splitlines()
    }, done.stdout
    assert "in 1 plan" in done.stderr, done.stderr


def test_a_root_it_cannot_measure_exits_3(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    done = _run(empty)
    assert done.returncode == 3, (done.returncode, done.stdout)
    assert "not measured" in done.stdout
    done = _run(tmp_path / "missing")
    assert done.returncode == 3
    assert "not measured" in done.stdout
    a_file = tmp_path / "a_file"
    a_file.write_text("not a directory\n", encoding="utf-8")
    done = _run(a_file)
    assert done.returncode == 3
    assert "not measured" in done.stdout


# --- criteria 19 to 23: the wiring and the texts ----------------------------


def test_gates_yaml_declares_criterion_ledger() -> None:
    doc = yaml.safe_load((REPO_ROOT / "decisions" / "gates.yaml").read_text(encoding="utf-8"))
    [entry] = [g for g in doc["gates"] if g["id"] == "criterion-ledger"]
    assert entry["command"] == "python3 scripts/check_criterion_ledger.py"
    shape = (entry["job"], entry["enforcement"], entry["floor"], entry["placement"])
    assert shape == ("verify", "block", False, "both")
    assert "Deleting 29 of 30" in entry["reason"]


def test_the_kit_carries_the_script_and_its_test() -> None:
    for path in ("scripts/check_criterion_ledger.py", "tests/test_check_criterion_ledger.py"):
        assert probe.rolle(path) is not None and probe.rolle(path)[0] == "mechanismus", path


def test_the_plan_prompt_requires_the_ledger() -> None:
    text = (REPO_ROOT / "prompts" / "03-plan.md").read_text(encoding="utf-8")
    assert "## The criterion ledger" in text
    assert "as entries of the criterion ledger below" in text
    assert "The gate `criterion-ledger` holds the ledger" in text
    for form in (
        "a test entry, `- <n>: tests/<path>::<function>`",
        "a not-yet-written entry, `- <n>: not yet written tests/<path>::<function>`",
        "a not-a-test entry, `- <n>: not a test — <what holds it>`",
    ):
        assert form in text, form
    block = text.split("## The criterion ledger", 1)[1].split("```markdown", 1)[1].split("```", 1)[0]
    examples = [line.strip() for line in block.splitlines() if line.strip().startswith("- ")]
    assert len(examples) == 3, examples
    for line in examples:
        assert gate.parse_entry(line) is not None, line


def test_the_implement_prompt_moves_the_ledger_with_the_tests() -> None:
    raw = (REPO_ROOT / "prompts" / "04-implement.md").read_text(encoding="utf-8")
    text = " ".join(raw.split())  # the prompt wraps its lines; the rules read on one line
    assert "The ledger moves with the tests." in text
    assert "removes `not yet written` from its line" in text
    assert "changes that ledger line in the same commit" in text


def test_the_workflow_names_the_gate_and_its_exemption() -> None:
    text = (REPO_ROOT / "docs" / "WORKFLOW.md").read_text(encoding="utf-8")
    rows = [line for line in text.splitlines() if line.startswith("| Criterion tests |")]
    assert len(rows) == 1, rows
    row = rows[0]
    assert "check_criterion_ledger.py" in row
    assert "criterion-ledger" in row
    assert "archived" in row
    assert "2026-10-11" in row
