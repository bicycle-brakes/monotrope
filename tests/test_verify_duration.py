"""The measured verification durations: clock arithmetic, history, reader, refusals.

`scripts.verify_duration` appends one JSON line per event to a local history
and reads it back without ever repairing it. Every case here builds its own
state root and never touches the real machine's verification history; each
docstring names the fault it was written against — planting it turned exactly
this test red.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import verify_duration  # noqa: E402
import verify_lock  # noqa: E402


@pytest.fixture(autouse=True)
def _isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """One test, one state root — and none of an outer run's admission context.

    Under `make verify` the pytest gate itself runs inside an admission, so the
    environment carries the outer run's context variables; a record written
    with them would measure the outer run, not the case. Unavailable readings
    come from patched probes, never from the machine that happens to run this.
    """
    for name in (
        verify_lock.ADMISSION_ID_ENV,
        verify_lock.ADMISSION_WAIT_ENV,
        verify_lock.LOCK_ENV,
        verify_lock.TOKEN_ENV,
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: None)
    return tmp_path / "state"


def _history(state: Path) -> list[dict]:
    """The history as it stands, one dict per JSON line, without creating anything."""
    path = state / "coding-harness" / verify_duration.HISTORY_NAME
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _run(capsys: pytest.CaptureFixture[str], *argv: str) -> tuple[int, str, str]:
    """One helper operation in process: exit code, stdout, stderr."""
    code = verify_duration.main(list(argv))
    seen = capsys.readouterr()
    return code, seen.out, seen.err


# ---------------------------------------------------------------------------
# Criterion 2 — monotonic arithmetic; the admission wait stays outside
# ---------------------------------------------------------------------------


def test_monotonic_execution_excludes_admission_wait(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Execution seconds are the difference of the runner's own readings, never plus the wait.

    Fault this pins: an injected admission delay counted into execution
    seconds, a wall-clock adjustment producing a negative window, or a
    non-numeric reading accepted as time.
    """
    state = tmp_path / "state"
    monkeypatch.setenv(verify_lock.ADMISSION_ID_ENV, "outer-admission")
    monkeypatch.setenv(verify_lock.ADMISSION_WAIT_ENV, "50.0")

    code, out, _ = _run(capsys, "clock")
    assert code == 0
    assert re.fullmatch(r"\d+\.\d{6}", out.strip()), out

    code, run_id, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    run_id = run_id.strip()

    # The recorded window is 10 s of execution; the 50 s admission wait beside it is
    # context, never an addend (criterion 2).
    code, out, _ = _run(capsys, "end", "--run", run_id, "--start", "100.0", "--end", "110.0", "--verdict", "green")
    assert code == 0
    assert out.strip() == "execution 10.000s · admission wait 50.000s", out
    ends = [event for event in _history(state) if event["event"] == "run_end"]
    assert len(ends) == 1
    assert ends[0]["seconds"] == 10.0 and ends[0]["verdict"] == "green"

    # The same shape for one gate: 9.5 s measured, the raw exit beside it.
    code, out, _ = _run(
        capsys,
        "gate",
        "--run",
        run_id,
        "--gate",
        "probe",
        "--start",
        "7.0",
        "--end",
        "16.5",
        "--status",
        "0",
        "--enforcement",
        "block",
    )
    assert code == 0 and out.strip() == "9.500"
    gates = [event for event in _history(state) if event["event"] == "gate"]
    assert len(gates) == 1 and gates[0]["seconds"] == 9.5 and gates[0]["exit"] == 0

    # A window that runs backwards refuses and records nothing: a clock that
    # jumped must not leave negative seconds in history.
    code, _, err = _run(capsys, "end", "--run", run_id, "--start", "110.0", "--end", "100.0", "--verdict", "green")
    assert code == 2 and "negative" in err, err
    assert len([event for event in _history(state) if event["event"] == "run_end"]) == 1


# ---------------------------------------------------------------------------
# Criterion 3 — history appends; a start without an end stays incomplete
# ---------------------------------------------------------------------------


def test_history_appends_distinct_runs_and_marks_incomplete(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """A later run appends its own identity and an interrupted run never reads as complete.

    Fault this pins: a second run overwriting the first's records, concurrent
    or nested runs mixing identities, or a run whose end never arrived being
    presented with a verdict.
    """
    state = tmp_path / "state"
    code, first, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    first = first.strip()
    code, second, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    second = second.strip()
    assert first != second, "two starts handed out one run identity"

    # The two runs interleave in the real order: a's gate, then b's gate, then
    # only b's completion. History must hold all five lines, in that order.
    for run_id, gate_id in ((first, "alpha"), (second, "beta")):
        code, _, _ = _run(
            capsys,
            "gate",
            "--run",
            run_id,
            "--gate",
            gate_id,
            "--start",
            "0.0",
            "--end",
            "1.0",
            "--status",
            "0",
            "--enforcement",
            "block",
        )
        assert code == 0
    code, _, _ = _run(capsys, "end", "--run", second, "--start", "0.0", "--end", "9.0", "--verdict", "green")
    assert code == 0

    events = _history(state)
    assert len(events) == 5, f"expected 2 starts + 2 gates + 1 end, got {len(events)}"
    assert [event["run_id"] for event in events if event["event"] == "gate"] == [first, second], (
        "a later run replaced an earlier run's records"
    )
    assert {event["run_id"] for event in events} == {first, second}

    # The reader keeps the two apart and labels the interrupted one incomplete.
    code, out, _ = _run(capsys, "report")
    assert code == 0
    assert f"run {first}" in out and f"run {second}" in out
    incomplete = [line for line in out.splitlines() if line.startswith(f"run {first}")]
    complete = [line for line in out.splitlines() if line.startswith(f"run {second}")]
    assert incomplete and "incomplete" in incomplete[0] and "unknown" in incomplete[0], out
    assert complete and "green" in complete[0] and "9.000s" in complete[0], out

    code, out, _ = _run(capsys, "report", "--run", first)
    assert code == 0
    assert "no completion recorded" in out and "alpha" in out, out


# ---------------------------------------------------------------------------
# Criterion 4 — every record binds to revision and configuration
# ---------------------------------------------------------------------------


def test_records_bind_results_to_revision_and_configuration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A record names its commit, dirty state, gate configuration, job and the command's raw exit.

    Fault this pins: runs of different jobs or dirty trees becoming
    indistinguishable, or a failed command losing its exit status in history.
    """
    state = tmp_path / "state"
    repo = tmp_path / "repo"
    (repo / "decisions").mkdir(parents=True)
    gate_file = repo / "decisions" / "gates.yaml"
    gate_file.write_text("gates: []\n", encoding="utf-8")
    monkeypatch.chdir(repo)

    commits = iter(["a" * 40, "b" * 40])
    porcelains = iter(["", " M scripts/x.py"])

    def fake_git(arguments: list[str]) -> str | None:
        if arguments == ["rev-parse", "HEAD"]:
            return next(commits, None)
        if arguments == ["status", "--porcelain"]:
            return next(porcelains, None)
        return None

    monkeypatch.setattr(verify_duration, "_git", fake_git)

    code, first, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    started = _history(state)[-1]
    assert started["run_id"] == first.strip()
    assert started["commit"] == "a" * 40 and started["dirty"] is False
    assert started["config_sha256"] == hashlib.sha256(gate_file.read_bytes()).hexdigest()
    assert started["repository"] == str(repo)
    assert started["utc"].endswith("+00:00"), started["utc"]

    code, second, _ = _run(capsys, "start", "--job", "docs", "--placement", "ci")
    assert code == 0
    started = _history(state)[-1]
    assert started["commit"] == "b" * 40 and started["dirty"] is True, (
        "a dirty tree must be distinguishable from a clean one"
    )

    # A failed gate keeps its raw exit status — an advisory failure is not a pass.
    code, _, _ = _run(
        capsys,
        "gate",
        "--run",
        first.strip(),
        "--gate",
        "probe",
        "--start",
        "0.0",
        "--end",
        "2.0",
        "--status",
        "3",
        "--enforcement",
        "advisory",
    )
    assert code == 0
    gates = [event for event in _history(state) if event["event"] == "gate"]
    assert len(gates) == 1
    assert gates[0]["exit"] == 3 and gates[0]["enforcement"] == "advisory" and gates[0]["seconds"] == 2.0

    # The two runs stay distinguishable in the listing.
    code, out, _ = _run(capsys, "report")
    assert code == 0
    lines = [line for line in out.splitlines() if line.startswith("run ")]
    assert len(lines) == 2
    assert any("job verify" in line for line in lines) and any("job docs" in line for line in lines)
    assert any("placement ci" in line for line in lines)


# ---------------------------------------------------------------------------
# Criterion 5 — unknowns stay unknown; the worker override is verbatim
# ---------------------------------------------------------------------------


def test_machine_context_preserves_unknowns_and_worker_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An unavailable reading is null, never zero, and a worker override is never guessed away.

    Fault this pins: unavailable memory becoming zero, a worker override
    replaced by a derived count, or a missing admission context fabricated.
    """
    state = tmp_path / "state"
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.chdir(empty)
    monkeypatch.delenv("PYTEST_XDIST_AUTO_NUM_WORKERS", raising=False)

    code, run_id, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    started = _history(state)[-1]
    assert started["memory_pct"] is None, "unavailable memory became a number"
    assert started["workers"] is None, "an unset worker setting became a count"
    assert started["commit"] is None and started["dirty"] is None
    assert started["config_sha256"] is None
    assert started["admission_id"] is None
    assert started["admission_wait_seconds"] is None
    assert started["admission_reused"] is None

    code, out, _ = _run(capsys, "report", "--run", run_id.strip())
    assert code == 0
    assert "free memory at start: unknown" in out
    assert "workers: unset (xdist decides)" in out
    assert "admission: unknown · wait: unknown · reused: unknown" in out

    # An explicit override is recorded verbatim — the runner forwards it, and
    # the record must not replace it with a machine-derived guess.
    monkeypatch.setenv("PYTEST_XDIST_AUTO_NUM_WORKERS", "7")
    code, _, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    assert _history(state)[-1]["workers"] == "7"


# ---------------------------------------------------------------------------
# Criterion 6 — the reader selects and diagnoses; it never repairs
# ---------------------------------------------------------------------------


def test_reader_selects_runs_and_diagnoses_truncated_history(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Malformed lines are named gaps, valid records survive them, and an unfinished run stays one.

    Fault this pins: a truncated final row crashing the reader, a malformed
    line hiding the runs around it, or an unfinished run presented as a
    successful complete one.
    """
    state = tmp_path / "state"
    root = state / "coding-harness"
    root.mkdir(parents=True)

    def start(run_id: str, job: str) -> dict:
        return {
            "v": 1,
            "event": "run_start",
            "run_id": run_id,
            "utc": "2026-11-04T10:00:00+00:00",
            "repository": "/repo",
            "commit": "c" * 40,
            "dirty": False,
            "config_sha256": "d" * 64,
            "job": job,
            "placement": "local",
            "memory_pct": 61.0,
            "workers": None,
            "admission_id": None,
            "admission_wait_seconds": None,
            "admission_reused": None,
        }

    good_end = {
        "v": 1,
        "event": "run_end",
        "run_id": "run-one",
        "utc": "2026-11-04T10:05:00+00:00",
        "seconds": 5.0,
        "verdict": "green",
    }
    lines = [
        json.dumps(start("run-one", "verify")),
        json.dumps(
            {
                "v": 1,
                "event": "gate",
                "run_id": "run-one",
                "utc": "x",
                "gate": "probe",
                "seconds": 1.5,
                "exit": 0,
                "enforcement": "block",
            }
        ),
        "garbage{{ not json",
        json.dumps(good_end),
        json.dumps(start("run-two", "docs")),
        '{"v": 1, "event": "gate", "run_id": "run-two", "gat',  # truncated final row
    ]
    (root / verify_duration.HISTORY_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8")

    code, out, _ = _run(capsys, "report")
    assert code == 0, out
    assert "run run-one" in out and "run run-two" in out, out
    one = [line for line in out.splitlines() if line.startswith("run run-one")]
    two = [line for line in out.splitlines() if line.startswith("run run-two")]
    assert one and "green" in one[0] and "5.000s" in one[0]
    assert two and "incomplete" in two[0], "a run without a completion became eligible as complete"
    notes = [line for line in out.splitlines() if line.startswith("history note:")]
    assert any("line 3" in note for note in notes), notes
    assert any("line 6" in note for note in notes), "the truncated final row was not diagnosed"

    code, out, _ = _run(capsys, "report", "--run", "run-one")
    assert code == 0
    assert "probe" in out and "1.500s" in out and "exit 0" in out, out

    # An id the history does not hold exits non-zero instead of inventing a run.
    code, _, err = _run(capsys, "report", "--run", "missing")
    assert code == 1 and "missing" in err, err


# ---------------------------------------------------------------------------
# Criterion 7 — substituted destinations refuse before anything is written
# ---------------------------------------------------------------------------


def test_history_rejects_substituted_destinations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A symlink or FIFO standing where the history belongs refuses; nothing is written through it.

    Fault this pins: an append following a substituted file to its target, a
    FIFO in the file's place hanging the runner, or an aliased state root
    being written into at all.
    """
    root = tmp_path / "state" / "coding-harness"
    root.mkdir(parents=True)

    # A symlink in the file's place: the victim keeps its bytes, the op refuses.
    victim = tmp_path / "victim.jsonl"
    victim.write_text("do not write through me\n", encoding="utf-8")
    (root / verify_duration.HISTORY_NAME).symlink_to(victim)
    code, _, err = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 2 and "substituted" in err, err
    assert victim.read_text(encoding="utf-8") == "do not write through me\n"

    # A FIFO in the file's place: refused without waiting on a writer that never comes.
    (root / verify_duration.HISTORY_NAME).unlink()
    os.mkfifo(root / verify_duration.HISTORY_NAME)
    code, _, err = _run(
        capsys,
        "gate",
        "--run",
        "some-run",
        "--gate",
        "probe",
        "--start",
        "0.0",
        "--end",
        "1.0",
        "--status",
        "0",
        "--enforcement",
        "block",
    )
    assert code == 2 and "substituted" in err, err

    # The whole state root as a symlink: the aliased target is never touched.
    target = tmp_path / "elsewhere"
    target.mkdir()
    (target / "sentinel.txt").write_text("do not touch", encoding="utf-8")
    aliased = tmp_path / "aliased-state"
    aliased.mkdir()
    (aliased / "coding-harness").symlink_to(target)
    monkeypatch.setenv("XDG_STATE_HOME", str(aliased))
    code, _, err = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 2 and "not a usable directory" in err, err
    assert (target / "sentinel.txt").read_text(encoding="utf-8") == "do not touch"
    assert not (target / verify_duration.HISTORY_NAME).exists(), "the aliased state root was written through"
