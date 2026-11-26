"""The next-step instruction: its declared schema, its validator and its atomic publisher.

Each test comes with its fault: the record that must be refused is the planted one, and the valid
control beside it shows the refusal is not blanket.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import next_step  # noqa: E402

NOW = dt.datetime(2026, 11, 25, 9, 30, 15, tzinfo=dt.UTC)


def valid(verb: str = "review") -> dict:
    rows = ["L1-1"] if verb == "hand" else []
    return next_step.build("demo", verb, "review-loop", NOW, rows)


@pytest.mark.parametrize("verb", ["review", "repair", "hand", "review-loop"])
def test_every_declared_verb_validates(verb: str) -> None:
    assert next_step.problems_of(valid(verb)) == []


def test_schema_validates_next_instruction() -> None:
    """Criterion 17: version, change, verb, row ids, producer and UTC time are required and checked."""
    schema = next_step.load_schema()
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {"schema_version", "change", "verb", "row_ids", "producer", "written_at"}
    assert schema["properties"]["verb"]["enum"] == ["review", "repair", "hand", "review-loop"]
    for field in schema["required"]:
        broken = valid()
        del broken[field]
        assert next_step.problems_of(broken), f"a record without {field} was accepted"
    plants = {
        "version 2": {"schema_version": 2},
        "boolean version": {"schema_version": True},
        "string version": {"schema_version": "1"},
        "empty change": {"change": ""},
        "unknown verb": {"verb": "advance"},
        "row ids not a list": {"row_ids": "L1-1"},
        "empty row id": {"verb": "hand", "row_ids": [""]},
        "hand without rows": {"verb": "hand", "row_ids": []},
        "review with rows": {"verb": "review", "row_ids": ["L1-1"]},
        "empty producer": {"producer": ""},
        "local time": {"written_at": "2026-11-25T09:30:15+01:00"},
        "no zone": {"written_at": "2026-11-25T09:30:15"},
        "impossible instant": {"written_at": "2026-13-45T25:61:61Z"},
        "unknown field": {"extra": 1},
    }
    for name, change in plants.items():
        assert next_step.problems_of({**valid(), **change}), f"{name} was accepted"
        with pytest.raises(next_step.InvalidNextStep):
            next_step.validate({**valid(), **change})
    assert next_step.problems_of([]), "a list was accepted as a record"
    assert next_step.problems_of({**valid("hand"), "row_ids": ["L1-1", "L1-2"]}) == []


def test_build_refuses_a_local_time() -> None:
    local = dt.datetime(2026, 11, 25, 9, 30, tzinfo=dt.timezone(dt.timedelta(hours=1)))
    with pytest.raises(next_step.InvalidNextStep):
        next_step.build("demo", "review", "review-loop", local)
    with pytest.raises(next_step.InvalidNextStep):
        next_step.build("demo", "review", "review-loop", dt.datetime(2026, 11, 25, 9, 30))
    assert next_step.build("demo", "review", "review-loop", NOW)["written_at"] == "2026-11-25T09:30:15Z"


def test_publisher_validates_and_atomically_replaces(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 19: temporary file beside the destination, validation first, replacement whole or not at all."""
    directory = tmp_path / "record"
    path = next_step.publish(directory, valid("review"))
    assert path == directory / "next.json"
    assert json.loads(path.read_text(encoding="utf-8")) == valid("review")
    # an invalid record never reaches the destination, and the old one stands
    with pytest.raises(next_step.InvalidNextStep):
        next_step.publish(directory, {**valid("repair"), "verb": "advance"})
    assert json.loads(path.read_text(encoding="utf-8")) == valid("review")
    assert [entry.name for entry in directory.iterdir()] == ["next.json"], "a temporary file stayed behind"
    # a failed replacement leaves the destination whole and removes its temporary file
    replaced = Path.replace

    def failing(self: Path, target: object) -> Path:
        if self.name.startswith(".next.json."):
            assert self.parent == directory, "the temporary file is not beside the destination"
            assert json.loads(self.read_text(encoding="utf-8"))["verb"] == "repair", "the write was partial"
            raise OSError("planted replacement failure")
        return replaced(self, target)

    monkeypatch.setattr(Path, "replace", failing)
    with pytest.raises(OSError, match="planted"):
        next_step.publish(directory, valid("repair"))
    monkeypatch.setattr(Path, "replace", replaced)
    assert json.loads(path.read_text(encoding="utf-8")) == valid("review")
    assert [entry.name for entry in directory.iterdir()] == ["next.json"]
    # the control: the same publish succeeds once replacement works
    next_step.publish(directory, valid("repair"))
    assert json.loads(path.read_text(encoding="utf-8"))["verb"] == "repair"


def test_invalidate_removes_the_file_and_tolerates_none(tmp_path: Path) -> None:
    next_step.invalidate(tmp_path / "missing")
    next_step.publish(tmp_path, valid())
    next_step.invalidate(tmp_path)
    assert not (tmp_path / "next.json").exists()
    next_step.invalidate(tmp_path)


def test_schema_timestamp_rejects_impossible_calendar_dates() -> None:
    """The schema's own pattern rejects impossible dates without Python's extra validator."""
    import re

    timestamp = next_step.load_schema()["properties"]["written_at"]
    assert timestamp.get("format") == "date-time"
    for value in ("2026-99-99T99:99:99Z", "2026-02-30T00:00:00Z", "1900-02-29T00:00:00Z"):
        assert not re.search(timestamp["pattern"], value), value
    for value in ("2026-02-28T23:59:59Z", "2000-02-29T00:00:00Z", "2024-02-29T00:00:00Z"):
        assert re.search(timestamp["pattern"], value), value
