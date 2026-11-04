"""The checked-in limits file and its strict loader (bead coding-harness-ht1b).

`research-swarm-limits.yaml` at a worktree root carries the research swarm's whole-run and
per-role allowances in minutes. These tests cover the loader contract and the checked-in
starting values; the wiring into a live research invocation is covered in test_stage2_swarm.py.
No test here starts a model call.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2_research_limits  # noqa: E402

BASE = (
    "run_minutes: 160.0\n"
    "role_minutes:\n"
    "  finders: 20.0\n"
    "  merge: 10.0\n"
    "  sentence: 5.0\n"
    "  topics: 10.0\n"
    "  judge: 15.0\n"
)

PATH = None  # a missing file: nothing is written for that case


def write(root: Path, text: str | bytes) -> Path:
    """Plant one limits document in `root`; bytes plant a file no reader can decode."""
    path = root / stage2_research_limits.FILE_NAME
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8")
    return path


def expect_refusal(root: Path, fault: str) -> None:
    """The loader refuses `root`'s document, naming the exact path and the fault."""
    with pytest.raises(stage2_research_limits.LimitsError) as caught:
        stage2_research_limits.load(root)
    message = str(caught.value)
    assert str(root / stage2_research_limits.FILE_NAME) in message, message
    assert fault in message, message


def test_checked_in_limits_have_decided_values() -> None:
    # Criterion 1. Planted fault: the checked-in file disagrees with the interview's decision
    # (finders 20, run 160), misses one of the six limits or states one in another unit.
    limits = stage2_research_limits.load(REPO_ROOT)
    assert limits.run_minutes == 160.0
    assert limits.role_minutes == {"finders": 20.0, "merge": 10.0, "sentence": 5.0, "topics": 10.0, "judge": 15.0}
    assert limits.run_seconds == 160.0 * 60.0, "the run limit is minutes, converted to seconds"
    assert limits.role_seconds("finders") == 20.0 * 60.0


def test_each_root_reads_its_current_limits(tmp_path: Path) -> None:
    # Criterion 2. Planted fault: another root's file leaks in, a cached first read survives a
    # valid edit, or a root without its own file silently falls back to the checked-in values.
    one = tmp_path / "one"
    two = tmp_path / "two"
    bare = tmp_path / "bare"
    for folder in (one, two, bare):
        folder.mkdir()
    write(one, BASE)
    assert stage2_research_limits.load(one).role_seconds("finders") == 1200.0
    write(one, BASE.replace("finders: 20.0", "finders: 25.5"))
    assert stage2_research_limits.load(one).role_minutes["finders"] == 25.5, "a valid edit changes the next read"
    write(two, BASE.replace("run_minutes: 160.0", "run_minutes: 90.0"))
    assert stage2_research_limits.load(two).run_minutes == 90.0
    assert stage2_research_limits.load(one).run_minutes == 160.0, "another root's file does not leak in"
    expect_refusal(bare, "cannot be read")


@pytest.mark.parametrize(
    ("text", "fault"),
    [
        pytest.param(PATH, "cannot be read", id="missing-file"),
        pytest.param(b"\xff\xfe not utf-8\n", "not valid UTF-8", id="bad-utf-8"),
        pytest.param("run_minutes: [160\n", "not valid YAML", id="bad-yaml"),
        pytest.param("", "must be a mapping", id="empty-document"),
        pytest.param("- 160\n- 20\n", "must be a mapping", id="sequence-document"),
        pytest.param(
            "role_minutes:\n  finders: 20\n  merge: 10\n  sentence: 5\n  topics: 10\n  judge: 15\n",
            "is missing run_minutes",
            id="no-run-key",
        ),
        pytest.param("run_minutes: 160\n", "is missing role_minutes", id="no-role-key"),
        pytest.param(BASE + "extra: 1\n", "unknown key(s) extra", id="unknown-top-key"),
        pytest.param("run_minutes: 160\nrole_minutes: 5\n", "must be a mapping of finders", id="roles-not-a-mapping"),
        pytest.param(BASE.replace("  judge: 15.0\n", ""), "role_minutes is missing judge", id="role-missing"),
        pytest.param(
            BASE.replace("  judge: 15.0\n", "  judge: 15.0\n  researcher: 10\n"),
            "unknown role(s) researcher",
            id="role-unknown",
        ),
        pytest.param(
            "run_minutes: 160\n"
            "role_minutes:\n  finders: 20\n  merge: 10\n  sentence: 5\n  topics: 10\n  judge: 15\n"
            "run_minutes: 170\n",
            "'run_minutes' appears more than once",
            id="duplicate-top-key",
        ),
        pytest.param(
            BASE.replace("  finders: 20.0\n", "  finders: 20.0\n  finders: 21.0\n"),
            "'finders' appears more than once",
            id="duplicate-role-key",
        ),
        pytest.param(BASE.replace("finders: 20.0", "160: 20.0"), "is not a name", id="non-name-key"),
    ],
)
def test_limits_reject_unusable_documents(tmp_path: Path, text: str | bytes | None, fault: str) -> None:
    # Criterion 3. Planted fault: a missing, unreadable, malformed, ambiguous or incomplete
    # document yields usable settings instead of a refusal.
    root = tmp_path / "repo"
    root.mkdir()
    if text is not None:
        write(root, text)
    expect_refusal(root, fault)


@pytest.mark.parametrize(
    ("text", "fault"),
    [
        pytest.param(BASE.replace("run_minutes: 160.0", "run_minutes: true"), "must be a number", id="bool"),
        pytest.param(BASE.replace("finders: 20.0", "finders: '20'"), "must be a number", id="numeric-string"),
        pytest.param(BASE.replace("topics: 10.0", "topics: null"), "must be a number", id="null"),
        pytest.param(BASE.replace("merge: 10.0", "merge: [10]"), "must be a number", id="container"),
        pytest.param(BASE.replace("sentence: 5.0", "sentence: 0"), "positive finite", id="zero"),
        pytest.param(BASE.replace("sentence: 5.0", "sentence: -5.0"), "positive finite", id="negative"),
        pytest.param(BASE.replace("run_minutes: 160.0", "run_minutes: .nan"), "positive finite", id="nan"),
        pytest.param(BASE.replace("run_minutes: 160.0", "run_minutes: .inf"), "positive finite", id="infinity"),
        pytest.param(
            "run_minutes: " + "9" * 400 + "\nrole_minutes:\n  finders: 20\n  merge: 10\n  sentence: 5\n"
            "  topics: 10\n  judge: 15\n",
            "too large",
            id="unconvertible-integer",
        ),
        pytest.param(
            BASE.replace("run_minutes: 160.0", "run_minutes: 1.0e+308"),
            "representable range",
            id="seconds-overflow",
        ),
        pytest.param(BASE.replace("finders: 20.0", "finders: 200.0"), "must not exceed", id="role-above-run"),
        pytest.param(BASE.replace("judge: 15.0", "judge: 170.0"), "must not exceed", id="judge-above-run"),
        pytest.param(BASE.replace("judge: 15.0", "judge: 160.0"), "strictly below", id="judge-equals-run"),
    ],
)
def test_limits_reject_implausible_values(tmp_path: Path, text: str, fault: str) -> None:
    # Criterion 3. Planted fault: a non-numeric, non-positive, non-finite, overflowing or
    # impossible budget is accepted.
    root = tmp_path / "repo"
    root.mkdir()
    write(root, text)
    expect_refusal(root, fault)


def test_valid_limits_accept_fractional_minutes(tmp_path: Path) -> None:
    # Criterion 4. Planted fault: valid fractional minutes are refused or converted wrongly.
    root = tmp_path / "repo"
    root.mkdir()
    write(root, BASE.replace("run_minutes: 160.0", "run_minutes: 160.5").replace("finders: 20.0", "finders: 0.5"))
    limits = stage2_research_limits.load(root)
    assert limits.run_minutes == 160.5
    assert limits.run_seconds == pytest.approx(9630.0)
    assert limits.role_seconds("finders") == pytest.approx(30.0)
    assert limits.role_minutes == {"finders": 0.5, "merge": 10.0, "sentence": 5.0, "topics": 10.0, "judge": 15.0}


@pytest.mark.parametrize("value", ["1.0e+308", "1.0e+999"])
@pytest.mark.parametrize("field", ["run_minutes: 160.0", "finders: 20.0"])
def test_scientific_overflow_reports_range(tmp_path: Path, value: str, field: str) -> None:
    # Plant numeric YAML floats whose value or seconds conversion overflows.
    write(tmp_path, BASE.replace(field, f"{field.split(':')[0]}: {value}"))
    expect_refusal(tmp_path, "representable range")


@pytest.mark.parametrize(
    "value",
    [
        "'16e1'",
        '"16e1"',
        "!!str 16e1",
        "16e1",
        '"1.0e308"',
        "'1.0e+999'",
        "!!str 1.0e+308",
        "1e308",
        "1e+308",
        "1e999",
        "1.0e999",
    ],
)
def test_quoted_scientific_numbers_remain_strings(tmp_path: Path, value: str) -> None:
    write(tmp_path, BASE.replace("run_minutes: 160.0", f"run_minutes: {value}"))
    expect_refusal(tmp_path, "must be a number")


def test_captured_role_limits_are_immutable(tmp_path: Path) -> None:
    # Planted fault: a caller mutates the captured judge reserve after loading.
    write(tmp_path, BASE)
    limits = stage2_research_limits.load(tmp_path)
    with pytest.raises(TypeError):
        limits.role_minutes["judge"] = 1.0
    assert limits.role_seconds("judge") == 900.0
    supplied = {"judge": 15.0}
    direct = stage2_research_limits.Limits(160.0, supplied)
    supplied["judge"] = 1.0
    assert direct.role_seconds("judge") == 900.0


@pytest.mark.parametrize("failure", [RecursionError, MemoryError])
@pytest.mark.parametrize("phase", ["read", "decode", "parse"])
def test_resource_errors_are_named_refusals(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure, phase: str
) -> None:
    # Planted fault: resource exhaustion escapes the loader instead of naming its input.
    write(tmp_path, BASE)

    def fail(*_args, **_kwargs):
        raise failure("planted resource exhaustion")

    if phase == "read":
        monkeypatch.setattr(Path, "read_bytes", fail)
    elif phase == "decode":

        class Undecodable(bytes):
            decode = fail

        monkeypatch.setattr(Path, "read_bytes", lambda _self: Undecodable())
    else:
        monkeypatch.setattr(stage2_research_limits.yaml, "load", fail)
    expect_refusal(tmp_path, "resource exhaustion")
