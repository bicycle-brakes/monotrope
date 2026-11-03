"""The shared time-record writer, parser and inserter - and the cases in which they hold.

`scripts/time_records.py` is the one grammar for the fixed records below a
plan's `## Time used` heading: the runner's attempts and the interactive
session's measured spans (`route orchestrator`) format, parse and insert
through it, and the run report reads records only through it (bead
coding-harness-v6vk). Each test names the fault that turns it red; every fault
is a second grammar, a guessed duration or a lost record.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import time_records  # noqa: E402

START = dt.datetime(2026, 10, 20, 10, 0, 0, tzinfo=dt.UTC)

PLAN_HEAD = "---\ntitle: Plan\nupdated: 2000-01-01\n---\n\n# Plan\n\n## Time used\n\n"
FOLLOWING = "\n## Following\nkeep following\n"


def plan_text(time_body: str, *, following: bool = True) -> str:
    """A small plan with a frontmatter header, the time heading and a following section."""
    return PLAN_HEAD + time_body + (FOLLOWING if following else "")


def test_shared_format_preserves_runner_bytes_and_midnight() -> None:
    """Criterion 2. Planted fault: changed metadata, a different suffix, or a midnight span without its end date."""
    end = START + dt.timedelta(seconds=600)
    same_day = time_records.format_entry(START, end, 600, "implement", 1, "flash", "glm-5.3-flash", "accepted")
    assert same_day == (
        "2026-10-20 10:00:00–10:10:00 UTC, 600 s — implement · attempt 1 · route flash · "
        "model glm-5.3-flash · accepted · measured by the runner"
    )
    # The named outcome is the only difference between the two verdicts' lines.
    rejected = time_records.format_entry(START, end, 600, "implement", 1, "flash", "glm-5.3-flash", "rejected")
    assert rejected == same_day.replace("accepted", "rejected")
    # A span across midnight carries the end's date; a same-day span carries none.
    midnight_start = dt.datetime(2026, 10, 20, 23, 59, 30, tzinfo=dt.UTC)
    midnight_end = dt.datetime(2026, 10, 21, 0, 0, 16, tzinfo=dt.UTC)
    across = time_records.format_entry(
        midnight_start, midnight_end, 45, "implement", 2, "flash", "glm-5.3-flash", "rejected"
    )
    assert across == (
        "2026-10-20 23:59:30–2026-10-21 00:00:16 UTC, 45 s — implement · attempt 2 · route flash · "
        "model glm-5.3-flash · rejected · measured by the runner"
    )
    # The fixed line survives the shared parser with every field intact, and prose stays unread.
    assert time_records.parse_entry(across) == time_records.Record(
        seconds=45, verb="implement", attempt=2, route="flash", model="glm-5.3-flash", result="rejected"
    )
    assert time_records.parse_entry(same_day + " (approx)") is None
    assert time_records.parse_entry("2026-10-20 10:00–10:10 UTC, 600 s") is None


def test_explicit_seconds_are_authoritative() -> None:
    """Criterion 3. Planted fault: the writer derives the duration from the endpoints instead of taking it."""
    # Sixty named seconds over endpoints an hour apart: the record says 60, never 3600.
    line = time_records.format_entry(
        START, START + dt.timedelta(hours=1), 60, "session", 3, "orchestrator", "glm-5.3-flash", "accepted"
    )
    assert "2026-10-20 10:00:00–11:00:00 UTC, 60 s — session · attempt 3 · route orchestrator" in line
    parsed = time_records.parse_entry(line)
    assert parsed is not None and parsed.seconds == 60
    # The reverse: endpoints a second apart with a long measured span keep the explicit value.
    long_line = time_records.format_entry(
        START, START + dt.timedelta(seconds=1), 7200, "implement", 1, "flash", "m", "rejected"
    )
    assert time_records.parse_entry(long_line) == time_records.Record(
        seconds=7200, verb="implement", attempt=1, route="flash", model="m", result="rejected"
    )
    # A zero-second span is a record, not an estimate.
    zero = time_records.format_entry(START, START, 0, "implement", 1, "flash", "m", "accepted")
    assert "UTC, 0 s —" in zero
    zero_record = time_records.parse_entry(zero)
    assert zero_record is not None and zero_record.seconds == 0


def test_shared_append_preserves_section_content() -> None:
    """Criterion 5. Planted fault: old prose disappears or a following section is changed."""
    older_prose = "2026-10-06 09:00–09:05, 5 min"
    older_record = time_records.format_entry(
        START, START + dt.timedelta(minutes=10), 600, "implement", 1, "flash", "glm-5.3-flash", "accepted"
    )
    text = plan_text(f"{older_prose}\n{older_record}\n")
    entry = time_records.format_entry(
        START + dt.timedelta(hours=1),
        START + dt.timedelta(hours=2),
        3600,
        "implement",
        2,
        "orchestrator",
        "glm-5.3-flash",
        "accepted",
    )
    combined = time_records.insert_entry(text, entry)
    # Order and content: prose, then the older record, then the new record, then the untouched section.
    assert combined == PLAN_HEAD + f"{older_prose}\n{older_record}\n{entry}\n" + FOLLOWING
    # A section at the end of the file takes the record without a following heading.
    tail = time_records.insert_entry(plan_text(f"{older_record}\n", following=False), entry)
    assert tail == PLAN_HEAD + f"{older_record}\n{entry}\n"
    # An empty section gains the record directly below its heading.
    assert time_records.insert_entry("# Plan\n\n## Time used\n", entry) == f"# Plan\n\n## Time used\n\n{entry}\n"
    # The trusted pre-call section wins over a rewritten plan (the runner's recovery shape).
    recovered = time_records.insert_entry(plan_text("REWRITTEN\n"), entry, prior=text)
    assert "REWRITTEN" not in recovered
    prose_at = recovered.index(older_prose)
    record_at = recovered.index(older_record)
    entry_at = recovered.index(entry)
    section_at = recovered.index("## Following")
    assert prose_at < record_at < entry_at < section_at
    assert "keep following\n" in recovered
    # Without the heading anywhere, nothing is inserted.
    with pytest.raises(time_records.TimeSectionError):
        time_records.insert_entry("# Plan\n", entry)
    with pytest.raises(time_records.TimeSectionError):
        time_records.insert_entry(plan_text("x\n"), entry, prior="# Plan\n")


def test_validation_refuses_malformed_fields() -> None:
    """A record the fixed format cannot carry raises `ValueError` before any bytes exist."""
    end = START + dt.timedelta(seconds=60)
    ok = {
        "start": START,
        "end": end,
        "seconds": 60,
        "verb": "implement",
        "attempt": 1,
        "route": "orchestrator",
        "model": "glm-5.3-flash",
        "result": "accepted",
    }
    time_records.format_entry(**ok)  # the control
    for broken in (
        {**ok, "seconds": -1},
        {**ok, "seconds": 1.5},
        {**ok, "attempt": 0},
        {**ok, "result": "maybe"},
        {**ok, "verb": ""},
        {**ok, "model": "glm x"},  # every line break the reader splits on
        {**ok, "model": "glm x"},
        {**ok, "model": "glm\x85x"},
        {**ok, "route": "a\x0bb"},
        {**ok, "verb": "implement · extra"},
        {**ok, "route": "orchestrator\n"},
        {**ok, "model": "\tglm"},
        {**ok, "route": " orchestrator"},
    ):
        with pytest.raises(ValueError):
            time_records.format_entry(**broken)
    with pytest.raises(ValueError):
        time_records.parse_stamp("2026-10-31 10:00:00")
    with pytest.raises(ValueError):
        time_records.parse_stamp("2026-13-01T00:00:00Z")
    with pytest.raises(ValueError):
        time_records.parse_stamp("2026-10-31T10:00:00+01:00")
    assert time_records.parse_stamp("2026-10-31T10:00:00Z") == dt.datetime(2026, 10, 31, 10, 0, 0, tzinfo=dt.UTC)


def test_backward_utc_still_formats_with_explicit_seconds() -> None:
    """F6-1. Planted fault: the formatter rejects an end before the start, losing a completed attempt's entry."""
    line = time_records.format_entry(
        START, START - dt.timedelta(seconds=5), 42, "implement", 1, "flash", "m", "rejected"
    )
    record = time_records.parse_entry(line)
    assert record is not None and record.seconds == 42


def test_line_separator_in_metadata_is_refused_and_record_stays_one_line() -> None:
    """F6-2. Planted fault: U+2028 inside the model passes and splits the record for the reader."""
    with pytest.raises(ValueError):
        time_records.format_entry(START, START, 60, "implement", 1, "orchestrator", "a b", "accepted")


def test_crlf_plan_keeps_unrelated_bytes(tmp_path: Path) -> None:
    """F6-3. Planted fault: reading with newline translation rewrites every CRLF ending as LF."""
    plan = tmp_path / "plan.md"
    original = b"# Plan\r\n\r\n## Time used\r\n\r\nold prose\r\n\r\n## Following\r\nkeep\r\n"
    plan.write_bytes(original)
    time_records.write_entry("NEW", plan)
    assert plan.read_bytes() == (b"# Plan\r\n\r\n## Time used\r\n\r\nold prose\r\nNEW\r\n\r\n## Following\r\nkeep\r\n")


def test_section_reader_names_the_exact_reason(tmp_path: Path) -> None:
    """The shared section reader's two reasons are the report's contract; a wrong one hides the cause."""
    plan = tmp_path / "plan.md"
    plan.write_text(plan_text("record\n"), encoding="utf-8")
    assert time_records.section_text(plan) == "\n\nrecord\n\n"
    missing = tmp_path / "absent" / "plan.md"
    with pytest.raises(time_records.TimeSectionError) as unreadable:
        time_records.section_text(missing)
    assert str(unreadable.value) == f"{missing} cannot be read."
    other = tmp_path / "other.md"
    other.write_text("# Plan\n", encoding="utf-8")
    with pytest.raises(time_records.TimeSectionError) as without:
        time_records.section_text(other)
    assert str(without.value) == f"{other} has no `## Time used` heading."


def test_atomic_publish_leaves_the_plan_on_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A failed publication keeps the plan's bytes and leaves no temporary file behind."""
    plan = tmp_path / "plan.md"
    plan.write_bytes(b"# Plan\n\n## Time used\n\n")
    original = plan.read_bytes()

    def broken_replace(_source: Path, _destination: Path) -> None:
        raise OSError("the worktree is full")

    monkeypatch.setattr(time_records.os, "replace", broken_replace)
    with pytest.raises(OSError, match="the worktree is full"):
        time_records.publish_atomic(plan, b"next\n")
    assert plan.read_bytes() == original
    assert [left.name for left in tmp_path.iterdir() if left.name.endswith(".tmp")] == []
    # The success path replaces the bytes whole, and the write operation returns what it published.
    monkeypatch.undo()
    content = time_records.write_entry("NEW measured by the runner", plan)
    assert plan.read_bytes() == content == b"# Plan\n\n## Time used\n\nNEW measured by the runner\n"
