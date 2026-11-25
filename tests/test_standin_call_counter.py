"""The swarm stand-in's per-key call counter (change standin-call-counter, bead coding-harness-bxxt.14).

The swarm stand-in (`tests/test_stage2_swarm.py`, `STAND_IN`) selects its
scripted step by the number of earlier calls with the selected key. It now
takes that number from the counter beside the call log
(`atomic_test_log.append_counted`) instead of parsing every earlier record.
Each test names its criterion and the fault it plants or catches.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import atomic_test_log
import pytest
from atomic_test_log import append_counted, append_record, counter_path, read_counter, read_records
from test_stage2_swarm import STAND_IN, SwarmWorld

LOG = atomic_test_log.STAND_IN_LOGS[0]

FINDER_3 = "# Finder task\nTopic 3 of 11\n"
FINDER_5 = "# Finder task\nTopic 5 of 11\n"
WORK = "plain work\n"

# The scripted calls: the prompt, the model and the keys the stand-in tries, first present wins.
CALLS = [
    (FINDER_3, "go/m1", ["finder:3:m1", "finder:3", "finder"]),
    (FINDER_3, "go/m2", ["finder:3:m2", "finder:3", "finder"]),
    (FINDER_3, "go/m1", ["finder:3:m1", "finder:3", "finder"]),
    (FINDER_5, "go/m1", ["finder:5:m1", "finder:5", "finder"]),
    (FINDER_3, "go/m1", ["finder:3:m1", "finder:3", "finder"]),
    (FINDER_3, "go/m2", ["finder:3:m2", "finder:3", "finder"]),
    (FINDER_5, "go/m1", ["finder:5:m1", "finder:5", "finder"]),
    (FINDER_5, "go/m3", ["finder:5:m3", "finder:5", "finder"]),
    (WORK, "go/m1", ["work:None:m1", "work:None", "work"]),
    (WORK, "go/m1", ["work:None:m1", "work:None", "work"]),
    (FINDER_3, "go/m1", ["finder:3:m1", "finder:3", "finder"]),
]

SCENARIO = {
    "finder:3:m1": [{"stdout": "m1-first"}, {"stdout": "m1-second", "exit": 3, "stderr": "planted"}],
    "finder:3": [{"stdout": "topic-3-only", "sleep": 0}],
    "finder": [{"stdout": "generic-first"}, {"stdout": "generic-second", "exit": 4}],
    "other": [{"stdout": "never selected"}],
}


def _former_index(previous: list, used: str) -> int:
    """Frozen verbatim from the swarm stand-in at commit 12c773c5: the log-based count."""
    return sum(1 for call in previous if call.get("key") == used)


def _counted(key: str):
    return lambda index: {"key": key, "index": index}


def _stand_in(folder: Path, scenario: dict) -> None:
    """Render the real swarm stand-in as `claude` into folder with its scenario."""
    folder.mkdir(parents=True, exist_ok=True)
    rendered = STAND_IN.replace("@PYTHON@", sys.executable).replace("@PI@", "0.0.0")
    rendered = rendered.replace(atomic_test_log.MARKER, atomic_test_log.embedded_source())
    program = folder / "claude"
    program.write_text(rendered, encoding="utf-8")
    program.chmod(0o755)
    (folder / "scenario.json").write_text(json.dumps(scenario), encoding="utf-8")


def _call(folder: Path, prompt: str, model: str) -> tuple[int, str]:
    run = subprocess.run(
        [str(folder / "claude"), "--model", model],
        input=prompt,
        capture_output=True,
        text=True,
        cwd=folder,
        env={"PATH": os.environ.get("PATH", ""), "HOME": str(folder)},
        timeout=60,
    )
    return run.returncode, run.stdout


def test_count_uses_counter_without_reading_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 1. Planted fault: the matching fast path reads prior records, or counts another key.

    With the counter current, the log's records are never parsed: the only
    reader of them is replaced by a refusal. The control appends a record
    past the counter, so the counter no longer matches and that refusal must
    fire, which shows the probe would catch a log read.
    """
    log = tmp_path / LOG
    assert [append_counted(log, key, _counted(key)) for key in ("a", "a", "b")] == [0, 1, 0]

    def refuse(_handle) -> dict:
        raise AssertionError("the matching fast path read the log's records")

    monkeypatch.setattr(atomic_test_log, "_rebuild_counts", refuse)
    assert [append_counted(log, key, _counted(key)) for key in ("a", "b", "c", "a")] == [2, 1, 0, 3]
    append_record(log, {"key": "a", "index": "past the counter"})
    with pytest.raises(AssertionError, match="fast path read"):
        append_counted(log, "a", _counted("a"))


@pytest.mark.parametrize("repeat_last", [False, True])
def test_scripted_answers_match_log_count(tmp_path: Path, repeat_last: bool) -> None:
    """Criterion 3. Planted fault: the counter changes an answer, exit status or selected key.

    Each sequential call of the real stand-in is compared with the answer the
    frozen former count expression selects over the log as it stood before
    that call: key fallback, steps, exhaustion with and without `repeat_last`.
    """
    scenario = {**SCENARIO, "repeat_last": True} if repeat_last else dict(SCENARIO)
    folder = tmp_path / "bin"
    _stand_in(folder, scenario)
    for number, (prompt, model, candidates) in enumerate(CALLS):
        previous = read_records(folder / LOG)
        used = next((key for key in candidates if key in scenario), candidates[-1])
        steps = scenario.get(used, [])
        index = _former_index(previous, used)
        step = steps[index] if index < len(steps) else (steps[-1] if steps and scenario.get("repeat_last") else {})
        answer = _call(folder, prompt, model)
        assert answer == (step.get("exit", 0), step.get("stdout", "")), (number, used, index)
        record = read_records(folder / LOG)[-1]
        assert (record["key"], record["sleep"]) == (used, step.get("sleep", 0)), number
    assert len(read_records(folder / LOG)) == len(CALLS)


def test_removal_and_rewind_clear_history(tmp_path: Path) -> None:
    """Criterion 4. Planted fault: a stale record or a later step survives a removal or a rewind.

    The counter stays beside a removed log; the next call must still start
    its key at the first step on a log holding only its own record.
    """
    folder = tmp_path / "bin"
    _stand_in(folder, {"work": [{"stdout": "first"}, {"stdout": "second"}, {"stdout": "third"}]})
    log = folder / LOG
    assert [_call(folder, WORK, "go/m1") for _ in range(2)] == [(0, "first"), (0, "second")]
    log.unlink()  # the suites' direct clear
    assert _call(folder, WORK, "go/m1") == (0, "first")
    assert [record["key"] for record in read_records(log)] == ["work"]
    assert _call(folder, WORK, "go/m1") == (0, "second")
    root = tmp_path / "repo"
    (root / "plans" / "changes" / "demo").mkdir(parents=True)
    SwarmWorld(root=root, bin=folder, home=tmp_path).rewind()
    assert _call(folder, WORK, "go/m1") == (0, "first")
    assert [record["key"] for record in read_records(log)] == ["work"]
    assert read_counter(log)["counts"] == {"work": 1}


def _tag(log: Path) -> dict:
    status = log.stat()
    return {"device": status.st_dev, "inode": status.st_ino, "size": status.st_size, "mtime_ns": status.st_mtime_ns}


def _write(log: Path, value) -> None:
    counter_path(log).write_text(json.dumps(value), encoding="utf-8")


def _stale(log: Path, **shift: int) -> dict:
    """A counter with a false count whose tag differs from this log's by the shifted fields."""
    tag = _tag(log)
    for field, delta in shift.items():
        tag[field] += delta
    return {**tag, "counts": {"a": 9}}


PLANTS = {
    "missing": lambda log: counter_path(log).unlink(),
    "unreadable_bytes": lambda log: counter_path(log).write_bytes(b"\xff\xfe\x00{"),
    "truncated": lambda log: counter_path(log).write_text(json.dumps({**_tag(log), "counts": {"a": 9}})[:25]),
    "empty": lambda log: counter_path(log).write_text(""),
    "list": lambda log: _write(log, []),
    "no_counts": lambda log: _write(log, _tag(log)),
    "extra_field": lambda log: _write(log, {**_tag(log), "counts": {"a": 9}, "extra": 1}),
    "text_size": lambda log: _write(log, {**_tag(log), "size": str(_tag(log)["size"]), "counts": {"a": 9}}),
    "bool_count": lambda log: _write(log, {**_tag(log), "counts": {"a": True}}),
    "negative_count": lambda log: _write(log, {**_tag(log), "counts": {"a": -1}}),
    "counts_list": lambda log: _write(log, {**_tag(log), "counts": [["a", 9]]}),
    "other_inode": lambda log: _write(log, _stale(log, inode=1)),
    "other_device": lambda log: _write(log, _stale(log, device=1)),
    "reused_inode_larger_size": lambda log: _write(log, _stale(log, size=7)),
    "reused_inode_smaller_size": lambda log: _write(log, _stale(log, size=-1)),
}


@pytest.mark.raw_stand_in_log_access(reason="plants invalid and stale counters beside a log")
def test_missing_or_mismatched_counter_rebuilds(tmp_path: Path) -> None:
    """Criterion 5. Planted fault: an invalid or mismatched counter raises or yields a stale count.

    Every planted counter beside a log of records a, a, b must be rebuilt:
    the next calls count 2 for a, 1 for b and 0 for c, and the published
    counter then matches the log. A reused inode is planted as a counter with
    this log's device and inode but another size. The control plants a
    current tag with a false count: it is trusted, which shows each other
    plant is what forces the rebuild.
    """
    plants = dict(PLANTS)
    if os.geteuid() != 0:
        plants["unreadable_mode"] = lambda log: counter_path(log).chmod(0)
    for name, plant in plants.items():
        log = tmp_path / name / LOG
        log.parent.mkdir()
        for key in ("a", "a", "b"):
            append_counted(log, key, _counted(key))
        plant(log)
        assert [append_counted(log, key, _counted(key)) for key in ("a", "b", "c")] == [2, 1, 0], name
        stored = read_counter(log)
        assert stored == {**_tag(log), "counts": {"a": 3, "b": 2, "c": 1}}, name
    control = tmp_path / "control" / LOG
    control.parent.mkdir()
    append_counted(control, "a", _counted("a"))
    _write(control, {**_tag(control), "counts": {"a": 9}})
    assert append_counted(control, "a", _counted("a")) == 9, "a current counter was not used"


def test_counter_write_failure_propagates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 9. Planted fault: a failed counter write or replacement is suppressed.

    A directory at the counter path fails its read, which only means rebuild,
    and then fails the replacement, which must reach the caller. A failed
    temporary write and a failed replacement propagate too and leave no
    temporary file behind.
    """
    real_replace = Path.replace
    replaced: list[str] = []

    def spy(self: Path, target) -> Path:
        replaced.append(Path(target).name)
        return real_replace(self, target)

    directory = tmp_path / "directory"
    directory.mkdir()
    log = directory / LOG
    counter_path(log).mkdir()
    with monkeypatch.context() as patch:
        patch.setattr(Path, "replace", spy)
        with pytest.raises(OSError):
            append_counted(log, "a", _counted("a"))
    assert replaced == [counter_path(log).name], "the call stopped before the replacement was attempted"
    assert not list(directory.glob("*.tmp")), "a failed replacement left its temporary file"

    def refuse_write(*_args, **_kwargs):
        raise PermissionError("planted counter write failure")

    written = tmp_path / "written"
    written.mkdir()
    with monkeypatch.context() as patch:
        patch.setattr(atomic_test_log.tempfile, "mkstemp", refuse_write)
        with pytest.raises(PermissionError, match="planted counter write failure"):
            append_counted(written / LOG, "a", _counted("a"))

    def refuse_replace(_self: Path, _target) -> Path:
        raise OSError("planted counter replacement failure")

    moved = tmp_path / "moved"
    moved.mkdir()
    append_counted(moved / LOG, "a", _counted("a"))
    before = read_counter(moved / LOG)
    with monkeypatch.context() as patch:
        patch.setattr(Path, "replace", refuse_replace)
        with pytest.raises(OSError, match="planted counter replacement failure"):
            append_counted(moved / LOG, "a", _counted("a"))
    assert not list(moved.glob("*.tmp")), "a failed replacement left its temporary file"
    assert read_counter(moved / LOG) == before, "a failed replacement changed the counter"
