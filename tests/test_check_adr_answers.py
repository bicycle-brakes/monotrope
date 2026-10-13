"""The gate `adr-answers`: every feature has the maintainer's answer to the ADR question.

Criteria 1-6 of plans/changes/harness-decide-adr/spec.md. Every test builds its
own tree in a temporary directory; the only files of this repository read are
the ones that travel with the kit (`decisions/gates.yaml`, the kit manifest).
Each rule stands next to the fault that turns it red.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_adr_answers.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "kit"))
import check_adr_answers as cag  # noqa: E402
import probe  # noqa: E402

FIX = "python3 scripts/harness.py decide adr"

# An answer in the shape of the pilot's five: quoted 'no', a proposal reason
# folded over two lines by PyYAML's plain style.
PILOT_ANSWER = """\
schema_version: 1
change: {change}
question: adr
answer: 'no'
reason: Only one more check.
shown:
  proposed: 'no'
  proposal_reason: one more check beside the others and one more command, reading files that already
    exist; nothing structural changes, and removing it is one revert
answered_by: architect
answered_at: 2026-09-28
"""

# The pilot's full feature anchor: every key its declaration requires, invented values.
PILOT_ANCHOR = """\
---
title: "Invented feature — specification delta"
artifact: change-spec
change: {change}
status: draft
created: 2026-01-02
provenance: ai-drafted
review: {{status: pending, approved_by: null, approved_at: null}}
class: feature
class_history:
  - {{from: null, to: feature, date: 2026-01-02, reason: "an invented reason"}}
appetite: 6
adr_question: {{proposed: "no", answered_by: null, reason: "an invented proposal reason"}}
intent:
  schema: 1
  scope:
    - plans/changes/{change}/
  outcome: >-
    An invented outcome, folded
    over two lines.
  in_scope:
    - one invented thing
  non_goals:
    - another invented thing
  acceptance:
    - id: AC-1
      criterion: an invented criterion
      falsifier: tests/test_x.py::test_y
  constraints:
    - an invented constraint
---

# Invented
"""


@pytest.fixture(autouse=True)
def _no_tolerance_from_the_caller(monkeypatch: pytest.MonkeyPatch) -> None:
    """A draft run's `make verify` sets the tolerance; the tests below measure the gate without it."""
    monkeypatch.delenv(cag.TOLERATE_ENV, raising=False)


def _tree(tmp_path: Path) -> Path:
    root = tmp_path / "tree"
    (root / "plans" / "changes" / "archive").mkdir(parents=True)
    return root


def _write(path: Path, text: str | bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8", newline="")
    return path


def _anchor(root: Path, folder: str, text: str | bytes, archived: bool = False) -> Path:
    base = root / "plans" / "changes" / ("archive" if archived else "")
    return _write(base / folder / "spec.md", text)


def _header(*lines: str) -> str:
    return "---\n" + "".join(f"{line}\n" for line in lines) + "---\n\n# Spec\n"


def _feature(change: str, *, proposed: str = '"no"', reason: str = '"a proposal reason"', extra: str = "") -> str:
    return _header(
        f'title: "Spec — {change}"',
        "class: feature",
        f"change: {change}",
        f"adr_question: {{proposed: {proposed}, reason: {reason}{extra}}}",
    )


def _answer(root: Path, change: str, text: str | None = None) -> Path:
    return _write(root / "decisions" / "answers" / change / "adr.yaml", text or PILOT_ANSWER.format(change=change))


def _run(root: Path) -> tuple[int, list[str]]:
    lines: list[str] = []
    code = cag.run(root, out=lines.append)
    return code, lines


# ---------------------------------------------------------------------------
# criterion 1 — the class
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("case", "text"),
    [
        ("no header", "# Spec\n\nclass: feature\n"),
        ("no class line", _header('title: "t"')),
        ("capitalised value", _header('title: "t"', "class: Feature")),
        ("two class lines", _header("class: bounded", "class: bounded")),
        ("not UTF-8", b"---\nclass: bounded\ntitle: \xff\xfe\n---\n"),
    ],
)
def test_an_anchor_whose_class_is_unknown_goes_red(tmp_path: Path, case: str, text: str | bytes) -> None:
    root = _tree(tmp_path)
    _anchor(root, "some-change", text)
    code, lines = _run(root)
    assert code == 1, f"{case}: exit {code}"
    assert len(lines) == 1, lines
    assert "plans/changes/some-change/spec.md" in lines[0]
    assert "whether this change owes an ADR answer is unknown" in lines[0]


@pytest.mark.parametrize(
    ("line", "value"),
    [
        ("class: bounded", "bounded"),
        ('class: "spike"', "spike"),
        ("class: 'architectural'", "architectural"),
        ("class: feature  # the pilot's full shape", "feature"),
        ('class: "bounded" # quoted and commented', "bounded"),
    ],
)
def test_the_class_line_takes_quotes_and_a_comment(tmp_path: Path, line: str, value: str) -> None:
    root = _tree(tmp_path)
    path = _anchor(root, "c", _header('title: "t"', line))
    assert cag.read_class(path) == (value, None)
    crlf = _anchor(root, "d", "﻿" + _header('title: "t"', line).replace("\n", "\r\n"))
    assert cag.read_class(crlf) == (value, None), "a byte-order mark and CRLF are tolerated"


def test_a_class_line_whose_value_runs_into_a_hash_is_not_misread(tmp_path: Path) -> None:
    """`feature#x` is one YAML scalar; reading `feature` from it would misread the class."""
    root = _tree(tmp_path)
    path = _anchor(root, "c", _header("class: feature#x"))
    cls, problem = cag.read_class(path)
    assert cls is None and "feature#x" in (problem or "")


def test_a_non_feature_is_held_to_nothing_further(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "a", _header('title: "t"', "class: bounded"))
    _anchor(root, "b", _header("class: spike"))
    _anchor(root, "2026-01-01-c", _header("class: architectural"), archived=True)
    code, lines = _run(root)
    assert code == 0, lines
    assert lines == ["adr-answers: examined nothing — read 3 change anchors, none of them a feature"]


# ---------------------------------------------------------------------------
# criterion 2 — a feature's header
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("case", "text"),
    [
        ("blank title", _feature("f").replace('title: "Spec — f"', 'title: "  "')),
        ("change differs from its folder", _feature("other")),
        ("bare no", _feature("f", proposed="no")),
        ("extra key under adr_question", _feature("f", extra=", answer: yes")),
        ("missing reason", _header('title: "t"', "class: feature", "change: f", 'adr_question: {proposed: "no"}')),
        ("duplicate key", _feature("f").replace("change: f\n", "change: f\nchange: f\n")),
        ("no adr_question", _header('title: "t"', "class: feature", "change: f")),
        ("change breaks the name rule", _feature("F_x")),
    ],
)
def test_a_feature_header_that_breaks_the_shape_goes_red(tmp_path: Path, case: str, text: str) -> None:
    root = _tree(tmp_path)
    _anchor(root, "f", text)
    _answer(root, "f")
    code, lines = _run(root)
    assert code == 1, f"{case}: accepted"
    assert len(lines) == 1, lines
    assert "plans/changes/f/spec.md" in lines[0]
    assert "a feature whose header breaks its shape" in lines[0]


def test_a_feature_in_the_pilots_full_shape_is_read(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    anchor = _anchor(root, "invented-feature", PILOT_ANCHOR.format(change="invented-feature"))
    _answer(root, "invented-feature")
    code, lines = _run(root)
    assert code == 0, lines
    feature, problems = cag.read_feature(cag.anchors(root)[0])
    assert problems == []
    assert feature is not None and feature.anchor.path == anchor
    assert feature.proposed == "no"
    assert feature.outcome == "An invented outcome, folded over two lines."


def test_an_archived_folder_loses_its_date(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "2026-01-02-old-change", _feature("old-change"), archived=True)
    [anchor] = cag.anchors(root)
    assert anchor.name == "old-change" and anchor.archived
    _answer(root, "old-change")
    assert _run(root)[0] == 0


def test_two_features_naming_one_change_go_red(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "twice", _feature("twice"))
    _anchor(root, "2026-01-02-twice", _feature("twice"), archived=True)
    _answer(root, "twice")
    code, lines = _run(root)
    assert code == 1
    assert len(lines) == 2, lines
    for line in lines:
        assert "two features name change `twice`" in line
        assert "plans/changes/twice/spec.md" in line and "plans/changes/archive/2026-01-02-twice/spec.md" in line


# ---------------------------------------------------------------------------
# criterion 3 — the answer file
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        PILOT_ANSWER.format(change="x"),
        PILOT_ANSWER.format(change="x").replace(
            "  proposal_reason: one more check beside the others and one more command, reading files that already\n"
            "    exist;",
            "  proposal_reason: >-\n    one more check beside the others and one more command, reading files that already\n    exist;",
        ),
        PILOT_ANSWER.format(change="x").replace(
            "reason: Only one more check.", "reason: '`x` is only one more check.'"
        ),
    ],
    ids=["pilot-plain-fold", "folded-block", "backtick"],
)
def test_an_answer_in_the_pilots_shape_is_accepted(text: str) -> None:
    data, problems = cag.parse_answer(text)
    assert problems == [], problems
    assert data["answer"] == "no" and data["answered_at"] == date(2026, 9, 28)


_BASE = PILOT_ANSWER.format(change="x")

DEVIATIONS = {
    "schema_version true": _BASE.replace("schema_version: 1", "schema_version: true"),
    "schema_version 1.0": _BASE.replace("schema_version: 1", "schema_version: 1.0"),
    "schema_version 2": _BASE.replace("schema_version: 1", "schema_version: 2"),
    "schema_version quoted": _BASE.replace("schema_version: 1", "schema_version: '1'"),
    "schema_version missing": _BASE.replace("schema_version: 1\n", ""),
    "extra key": _BASE + "source: a session\n",
    "change breaks the name rule": _BASE.replace("change: x", "change: X_y"),
    "question ADR": _BASE.replace("question: adr", "question: ADR"),
    "answer bare no": _BASE.replace("answer: 'no'", "answer: no"),
    "answer maybe": _BASE.replace("answer: 'no'", "answer: maybe"),
    "reason blank": _BASE.replace("reason: Only one more check.", "reason: ' '"),
    "reason lower case": _BASE.replace("reason: Only one more check.", "reason: only one more check."),
    "reason missing": _BASE.replace("reason: Only one more check.\n", ""),
    "shown missing": _BASE.split("shown:")[0] + "answered_by: architect\nanswered_at: 2026-09-28\n",
    "shown extra key": _BASE.replace("shown:\n", "shown:\n  answer: 'no'\n"),
    "shown proposed bare no": _BASE.replace("  proposed: 'no'", "  proposed: no"),
    "shown proposal_reason blank": _BASE.replace(
        "  proposal_reason: one more check beside the others and one more command, reading files that already\n"
        "    exist; nothing structural changes, and removing it is one revert\n",
        "  proposal_reason: ''\n",
    ),
    "answered_by upper case": _BASE.replace("answered_by: architect", "answered_by: Architect"),
    "answered_by a list": _BASE.replace("answered_by: architect", "answered_by: [architect]"),
    "answered_at quoted": _BASE.replace("answered_at: 2026-09-28", "answered_at: '2026-09-28'"),
    "answered_at a datetime": _BASE.replace("answered_at: 2026-09-28", "answered_at: 2026-09-28 12:00:00"),
    "duplicate key": _BASE.replace("question: adr\n", "question: adr\nquestion: adr\n"),
    "a list": "- " + _BASE.replace("\n", "\n  ").rstrip() + "\n",
    "not YAML": _BASE + "answer: [\n",
}


@pytest.mark.parametrize("case", sorted(DEVIATIONS))
def test_every_single_deviation_of_an_answer_goes_red(tmp_path: Path, case: str) -> None:
    assert cag.parse_answer(_BASE)[1] == [], "the base must be accepted, or every case below is red for it"
    _, problems = cag.parse_answer(DEVIATIONS[case])
    assert problems, f"{case}: accepted"

    root = _tree(tmp_path)
    _anchor(root, "x", _feature("x"))
    _answer(root, "x", DEVIATIONS[case])
    assert _run(root)[0] == 1, f"{case}: the gate exits 0"


# ---------------------------------------------------------------------------
# criterion 4 — each feature held to its answer
# ---------------------------------------------------------------------------


def _one_line_naming(lines: list[str], change: str, answer: str) -> str:
    assert len(lines) == 1, lines
    line = lines[0]
    assert change in line and answer in line and FIX in line, line
    return line


def test_an_active_feature_without_an_answer_goes_red(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "active", _feature("active"))
    code, lines = _run(root)
    assert code == 1
    line = _one_line_naming(lines, "active", "decisions/answers/active/adr.yaml")
    assert "plans/changes/active/spec.md" in line


def test_an_archived_feature_without_an_answer_goes_red(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "2026-01-02-done", _feature("done"), archived=True)
    code, lines = _run(root)
    assert code == 1
    line = _one_line_naming(lines, "done", "decisions/answers/done/adr.yaml")
    assert "plans/changes/archive/2026-01-02-done/spec.md" in line


def test_an_answer_naming_another_change_goes_red(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "mine", _feature("mine"))
    _answer(root, "mine", PILOT_ANSWER.format(change="theirs"))
    code, lines = _run(root)
    assert code == 1
    line = _one_line_naming(lines, "mine", "decisions/answers/mine/adr.yaml")
    assert "names change `theirs`" in line


def test_a_malformed_answer_goes_red(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "mine", _feature("mine"))
    _answer(root, "mine", PILOT_ANSWER.format(change="mine").replace("answer: 'no'", "answer: no"))
    code, lines = _run(root)
    assert code == 1
    line = _one_line_naming(lines, "mine", "decisions/answers/mine/adr.yaml")
    assert "is refused" in line and "`answer`" in line


def test_a_feature_with_a_valid_answer_is_not_reported(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "mine", _feature("mine"))
    _answer(root, "mine")
    _answer(root, "no-anchor-names-it")  # an answer without an anchor is not reported, as in the pilot
    code, lines = _run(root)
    assert code == 0, lines
    assert lines == ["adr-answers: read 1 change anchors; held 1 features to their answer files: mine"]


def test_no_report_line_calls_an_answer_confirmed(tmp_path: Path) -> None:
    """The gate cannot see who wrote or merged an answer, and no line claims it did."""
    outputs: list[str] = []
    root = _tree(tmp_path)
    outputs += _run(root)[1]  # empty
    _anchor(root, "a", _feature("a"))
    _anchor(root, "b", _feature("b"))
    _anchor(root, "c", _header("class: Feature"))
    _answer(root, "b", PILOT_ANSWER.format(change="other"))
    outputs += _run(root)[1]  # red
    (root / "plans/changes/c/spec.md").unlink()
    _answer(root, "a")
    _answer(root, "b")
    outputs += _run(root)[1]  # green
    outputs += _run(tmp_path / "absent")[1]  # cannot measure
    assert len(outputs) >= 5
    for line in outputs:
        for word in ("confirm", "approved", "signed"):
            assert word not in line.lower(), line


# ---------------------------------------------------------------------------
# criterion 5 — report and exit codes
# ---------------------------------------------------------------------------


def test_a_green_run_names_the_count_and_the_features(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "one", _feature("one"))
    _anchor(root, "2026-01-02-two", _feature("two"), archived=True)
    _anchor(root, "three", _header("class: bounded"))
    _answer(root, "one")
    _answer(root, "two")
    code, lines = _run(root)
    assert code == 0
    assert lines == ["adr-answers: read 3 change anchors; held 2 features to their answer files: one, two"]


def test_an_empty_tree_examined_nothing_and_is_not_a_pass(tmp_path: Path) -> None:
    for root in (_tree(tmp_path), tmp_path / "bare"):
        root.mkdir(exist_ok=True)
        code, lines = _run(root)
        assert code == 0
        assert lines == ["adr-answers: examined nothing — read 0 change anchors, none of them a feature"]
        for word in ("ok", "pass", "green", "every"):
            assert word not in lines[0].lower().split(), lines


def test_an_unreadable_root_is_exit_3(tmp_path: Path) -> None:
    a_file = _write(tmp_path / "a-file", "x")
    for root in (tmp_path / "absent", a_file):
        code, lines = _run(root)
        assert code == 3, (root, lines)
        assert "cannot measure" in lines[0]
    erg = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path / "absent")], capture_output=True, text=True, check=False
    )
    assert erg.returncode == 3, erg.stdout + erg.stderr


def test_the_command_line_exits_1_on_a_finding_and_0_when_green(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _anchor(root, "mine", _feature("mine"))

    def cli() -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root)], capture_output=True, text=True, check=False
        )

    red = cli()
    assert red.returncode == 1 and FIX in red.stdout
    _answer(root, "mine")
    green = cli()
    assert green.returncode == 0, green.stdout
    assert "held 1 features" in green.stdout


# ---------------------------------------------------------------------------
# criterion 6 — the one list and the kit
# ---------------------------------------------------------------------------


def test_the_gate_is_in_the_one_list() -> None:
    doc = yaml.safe_load((REPO_ROOT / "decisions" / "gates.yaml").read_text(encoding="utf-8"))
    [gate] = [g for g in doc["gates"] if g["id"] == "adr-answers"]
    assert gate["command"] == "python3 scripts/check_adr_answers.py"
    assert (gate["job"], gate["enforcement"], gate["floor"], gate["placement"]) == ("verify", "block", False, "both")
    assert "needs_tracker" not in gate and "needs_history" not in gate, "the gate reads only the files of the tree"


def test_the_kit_carries_the_mechanism_and_not_the_answers() -> None:
    for path in (
        "scripts/check_adr_answers.py",
        "scripts/harness.py",
        "tests/test_check_adr_answers.py",
        "tests/test_harness_decide_adr.py",
        ".github/PULL_REQUEST_TEMPLATE/decision.md",
        "decisions/gates.yaml",
    ):
        assert probe.rolle(path) is not None and probe.rolle(path)[0] == "mechanismus", path
    for path in ("decisions/answers/some-change/adr.yaml", "decisions/answers/"):
        assert probe.rolle(path) == ("bestand", "decisions/answers/"), path


def test_the_named_change_alone_has_its_missing_answer_tolerated(tmp_path: Path) -> None:
    # The draft verb of scripts/stage2.py asks for this through the environment (phase-6 F-9, F-10).
    # Planted fault: any change tolerated, or the tolerance also covers a refused answer file.
    root = _tree(tmp_path)
    _anchor(root, "mine", _feature("mine"))
    lines: list[str] = []
    assert cag.run(root, out=lines.append, tolerate="mine") == 0
    assert any("answer owed" in line and "mine" in line for line in lines)

    _anchor(root, "other", _feature("other"))
    lines = []
    assert cag.run(root, out=lines.append, tolerate="mine") == 1
    assert any("other: no answer" in line for line in lines)

    answers = root / "decisions" / "answers" / "mine"
    answers.mkdir(parents=True)
    (answers / "adr.yaml").write_text("not: an answer\n", encoding="utf-8")
    lines = []
    assert cag.run(root, out=lines.append, tolerate="mine") == 1
    assert any("is refused" in line for line in lines)
