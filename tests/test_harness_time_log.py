"""The `harness.py time-log` command - and the cases in which it refuses unwritten.

One measured span goes into an active change's plan through the shared writer
(`scripts/time_records.py`); invalid fields and unsafe destinations change
nothing (spec time-records-data, criteria 1 and 4). Every case runs the
command in process against a temporary repository that holds no provenance
map, no git history and no answers: a time record needs none of them.
"""

from __future__ import annotations

import os
import shutil
import stat
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import harness  # noqa: E402
import time_records  # noqa: E402

TODAY = date(2026, 10, 31)
START = "2026-10-31T10:00:00Z"
END = "2026-10-31T10:01:00Z"

PLAN = (
    "---\ntitle: Plan — demo\nstatus: draft\n"
    "date: 2026-10-30\nlast_reviewed: 2026-10-30\nupdated: 2026-10-30\n---\n\n"
    "# Plan — demo\n\n"
    "## Time used\n\n"
    "2026-10-30 09:00–09:05, 5 min, not measured by the orchestrator\n\n"
    "## Criterion ledger\n\n- 1: a held row\n"
)


def make_repo(tmp_path: Path) -> Path:
    """One temporary repository with the demo change's plan and nothing else."""
    folder = tmp_path / "plans" / "changes" / "demo"
    folder.mkdir(parents=True)
    (folder / "plan.md").write_text(PLAN, encoding="utf-8")
    return tmp_path


def argv_for(root: Path, change: str = "demo", **overrides: str) -> list[str]:
    """One full `time-log` invocation; an override replaces its option's value."""
    values = {
        "start": START,
        "end": END,
        "seconds": "60",
        "verb": "implement",
        "attempt": "1",
        "route": "orchestrator",
        "model": "glm-5.3-flash",
        "result": "accepted",
        **overrides,
    }
    argv = ["time-log", change]
    for option, value in values.items():
        argv.extend([f"--{option}", value])
    return [*argv, "--root", str(root)]


def run_args(argv: list[str]) -> tuple[int, list[str]]:
    """One in-process run; an argparse refusal exits, and its exit code is the verdict."""
    out: list[str] = []
    try:
        code = harness.main(argv, out=out.append, today=TODAY)
    except SystemExit as stop:
        return int(stop.code or 0), out
    return code, out


def run_log(root: Path, *extra: str) -> tuple[int, list[str]]:
    """The healthy invocation; an extra option wins over the default of its kind."""
    return run_args([*argv_for(root), *extra])


def test_time_log_appends_one_counted_record(tmp_path: Path) -> None:
    """Criterion 1. Planted fault: zero or duplicate appended records, or a line the report cannot count."""
    root = make_repo(tmp_path)
    plan = root / "plans" / "changes" / "demo" / "plan.md"
    code, out = run_log(root)
    assert code == 0
    (line,) = [row for row in out if row.endswith(time_records.MARKER)]
    text = plan.read_text(encoding="utf-8")
    records = [row for row in text.splitlines() if row.endswith(time_records.MARKER)]
    assert records == [line]
    assert "route orchestrator" in line and "attempt 1" in line and "accepted" in line and "60 s" in line
    parsed = time_records.parse_entry(line)
    assert parsed is not None and parsed.seconds == 60
    assert "updated: 2026-10-31" in text
    # The prose below the heading keeps its place, and the following section stays whole.
    assert "not measured by the orchestrator" in text
    assert text.index("not measured by the orchestrator") < text.index(line) < text.index("## Criterion ledger")
    # A second measured span appends exactly one more record, and one grammar counts both: 60 + 120 s.
    code, _ = run_log(root, "--end", "2026-10-31T10:02:00Z", "--seconds", "120", "--result", "rejected")
    assert code == 0
    text = plan.read_text(encoding="utf-8")
    section = text[text.index("## Time used") + len("## Time used") : text.index("## Criterion ledger")]
    rows = [time_records.parse_entry(row.strip()) for row in section.splitlines() if row.strip()]
    assert [row.seconds for row in rows if row is not None] == [60, 120]
    assert [row.route for row in rows if row is not None] == ["orchestrator", "orchestrator"]
    assert sum(1 for row in rows if row is None) == 1  # the prose stays unread, visible to the report


def test_invalid_input_and_unsafe_destination_leave_bytes_unchanged(tmp_path: Path) -> None:
    """Criterion 4. Planted fault: invalid fields or an unsafe destination receive a write."""
    root = make_repo(tmp_path)
    plan = root / "plans" / "changes" / "demo" / "plan.md"
    healthy = plan.read_bytes()
    outside = tmp_path / "outside-plan.md"
    outside.write_bytes(b"untouched\n")
    outside_dir = tmp_path / "outside-change"

    def reset() -> None:
        if plan.parent.is_symlink():
            plan.parent.unlink()
            plan.parent.mkdir(parents=True)
        if plan.is_symlink() or plan.exists():
            plan.unlink()
        plan.write_bytes(healthy)

    for case in (
        {"start": "2026-10-31 10:00:00"},
        {"start": "2026-13-01T00:00:00Z"},
        {"end": "2026-10-31T09:59:00Z"},
        {"seconds": "-1"},
        {"attempt": "0"},
        {"verb": ""},
        {"verb": "implement · extra"},
        {"model": "glm-5.3-flash\n"},
        {"route": " orchestrator"},
        {"result": "maybe"},
    ):
        code, _ = run_args(argv_for(root, **case))
        assert code == 2, case
        assert plan.read_bytes() == healthy, case
    code, out = run_args(argv_for(root, verb=""))
    assert any(row.startswith("refused: ") for row in out) and any(row == "Nothing was written." for row in out)
    for drop in ("--seconds", "--model", "--start", "--result"):
        argv = argv_for(root)
        position = argv.index(drop)
        del argv[position : position + 2]
        code, _ = run_args(argv)
        assert code == 2, drop
        assert plan.read_bytes() == healthy, drop
    # Names that never reach a destination: traversal, the archive, and no plain folder name.
    for change in ("../elsewhere", "archive", "..", ".hidden", "demo/plan", ""):
        code, _ = run_args(argv_for(root, change=change))
        assert code == 2, change
        assert plan.read_bytes() == healthy, change
    # An unreadable plan: bytes that are not UTF-8.
    plan.write_bytes(b"\xff\xfe not utf-8\n")
    code, _ = run_args(argv_for(root))
    assert code == 2 and plan.read_bytes() == b"\xff\xfe not utf-8\n"
    reset()
    # A plan without the heading, and one with a second heading, receive nothing.
    plan.write_text("# Plan\n\nnothing here\n", encoding="utf-8")
    code, _ = run_args(argv_for(root))
    assert code == 2 and plan.read_text(encoding="utf-8") == "# Plan\n\nnothing here\n"
    doubled = PLAN + "\n## Time used\n\nmore\n"
    plan.write_text(doubled, encoding="utf-8")
    code, _ = run_args(argv_for(root))
    assert code == 2 and plan.read_text(encoding="utf-8") == doubled
    reset()
    # A symlinked plan never receives the write; the link and its target survive untouched.
    plan.unlink()
    plan.symlink_to(outside)
    code, _ = run_args(argv_for(root))
    assert code == 2 and outside.read_bytes() == b"untouched\n" and plan.is_symlink()
    reset()
    # A hard-linked plan never receives the write through its link.
    plan.unlink()
    os.link(outside, plan)
    code, _ = run_args(argv_for(root))
    assert code == 2 and outside.read_bytes() == b"untouched\n"
    reset()
    # An aliased change folder never receives the write through the link.
    shutil.rmtree(plan.parent)
    outside_dir.mkdir()
    plan.parent.symlink_to(outside_dir, target_is_directory=True)
    (outside_dir / "plan.md").write_bytes(healthy)
    code, _ = run_args(argv_for(root))
    assert code == 2 and (outside_dir / "plan.md").read_bytes() == healthy
    # The control: with every fault repaired, the same invocation still succeeds.
    reset()
    code, out = run_args(argv_for(root))
    assert code == 0
    assert out and out[0].endswith(time_records.MARKER)


def test_publication_failure_preserves_plan(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 4. Planted fault: a failed publication truncates the plan or returns success."""
    root = make_repo(tmp_path)
    plan = root / "plans" / "changes" / "demo" / "plan.md"
    healthy = plan.read_bytes()
    real_replace = os.replace

    def failing_replace(source: object, destination: object, **_kwargs: object) -> object:
        if Path(str(destination)) == plan:
            raise OSError("the worktree is full")
        return real_replace(source, destination)  # type: ignore[arg-type]

    monkeypatch.setattr(time_records.os, "replace", failing_replace)
    code, out = run_args(argv_for(root))
    assert code == 2
    assert plan.read_bytes() == healthy
    assert [left.name for left in plan.parent.iterdir() if left.name.endswith(".tmp")] == []
    assert any("could not write the record" in row for row in out)


def test_dispatch_leaves_the_decide_adr_route_intact(tmp_path: Path) -> None:
    """The public CLI keeps its ADR behavior: time-log needs no provenance map, decide adr still refuses without one."""
    root = make_repo(tmp_path)
    code, out = run_args(argv_for(root))
    assert code == 0 and out and out[0].endswith(time_records.MARKER)
    decide_out: list[str] = []
    code = harness.main(["decide", "adr", "--root", str(root)], out=decide_out.append, today=TODAY)
    assert code == 2
    assert any("no provenance map" in row for row in decide_out)


@pytest.mark.parametrize("failure", ["open", "fsync"])
def test_directory_sync_failure_reports_published_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    """A failure after replacement warns about durability, never claims no write."""
    root = make_repo(tmp_path)
    plan = root / "plans" / "changes" / "demo" / "plan.md"
    real_open = os.open
    real_fsync = os.fsync

    def failing_open(path: object, flags: int, *args: object, **kwargs: object) -> int:
        if failure == "open" and path == plan.parent:
            raise OSError("directory open failed")
        return real_open(path, flags, *args, **kwargs)

    def failing_fsync(descriptor: int) -> None:
        if failure == "fsync" and stat.S_ISDIR(os.fstat(descriptor).st_mode):
            raise OSError("directory fsync failed")
        real_fsync(descriptor)

    monkeypatch.setattr(time_records.os, "open", failing_open)
    monkeypatch.setattr(time_records.os, "fsync", failing_fsync)
    code, out = run_log(root)
    assert code == 0
    assert "Nothing was written." not in out
    assert not any(row.startswith("refused:") for row in out)
    assert any(row.startswith("warning:") and "written" in row for row in out)
    records = [line for line in plan.read_text().splitlines() if time_records.parse_entry(line)]
    assert len(records) == 1
    assert records[0] in out


@pytest.mark.parametrize(
    "text",
    [
        "# Plan\n\n## Time used\n",
        "---\n---\n\n## Time used\n",
        "---\ntitle: Plan\n---\n\n## Time used\n",
    ],
)
def test_time_log_accepts_plan_without_updated_field(tmp_path: Path, text: str) -> None:
    """Only an existing updated date is stamped; absent frontmatter needs no repair."""
    root = make_repo(tmp_path)
    plan = root / "plans" / "changes" / "demo" / "plan.md"
    plan.write_text(text)
    code, out = run_log(root)
    assert code == 0
    (entry,) = [line for line in out if line.endswith(time_records.MARKER)]
    assert plan.read_text() == time_records.insert_entry(text, entry)
