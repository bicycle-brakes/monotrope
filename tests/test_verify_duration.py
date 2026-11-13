"""The measured verification durations: clock arithmetic, history, reader, refusals.

`scripts.verify_duration` appends one JSON line per event to a local history
and reads it back without ever repairing it. Every case here builds its own
state root and never touches the real machine's verification history; each
docstring names the fault it was written against — planting it turned exactly
this test red.
"""

from __future__ import annotations

import errno
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
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


def _valid_records(run_id: str) -> list[dict]:
    """Complete version-1 records, including explicit unknown machine context."""
    common = {"v": 1, "run_id": run_id, "utc": "2026-11-04T10:00:00+00:00"}
    return [
        {
            **common,
            "event": "run_start",
            "repository": "/repo",
            "commit": None,
            "dirty": None,
            "config_sha256": None,
            "job": "verify",
            "placement": "local",
            "memory_pct": None,
            "workers": None,
            "admission_id": None,
            "admission_wait_seconds": None,
            "admission_reused": None,
        },
        {**common, "event": "gate", "gate": "pytest", "seconds": 0, "exit": 0, "enforcement": "block"},
        {**common, "event": "run_end", "seconds": 1.5, "verdict": "green"},
    ]


@pytest.mark.parametrize("kind", ["run_start", "gate", "run_end"])
def test_reader_validates_all_record_types(capsys, kind):
    """Every required field and range is checked; later green ends cannot erase a bad record."""
    records = _valid_records("validated")
    index = [record["event"] for record in records].index(kind)
    valid = records[index]
    mutations = [
        {key: value for key, value in valid.items() if key != field}
        for field in valid
        if field not in ("event", "run_id", "v")
    ]
    mutations += [{**valid, "utc": value} for value in (None, "yesterday", "2026-11-04", 1)]
    if kind in ("gate", "run_end"):
        mutations += [
            {**valid, "seconds": value} for value in (-1, float("nan"), float("inf"), float("-inf"), True, "1", None)
        ]
    if kind == "gate":
        mutations += [{**valid, "exit": value} for value in (True, 0.5, "0", None)]
        mutations += [{**valid, "enforcement": "unknown"}, {**valid, "gate": ""}]
    if kind == "run_end":
        mutations += [{**valid, "verdict": "unknown"}]
    if kind == "run_start":
        for field, values in {
            "memory_pct": (-1, 101, float("nan"), True, "50"),
            "admission_wait_seconds": (-1, float("inf"), True, "1"),
            "dirty": (0, "false"),
            "admission_reused": (0, "false"),
            "repository": (None, ""),
            "job": (None, ""),
            "placement": (None, ""),
            "commit": (1, ""),
            "config_sha256": (1, ""),
            "workers": (1, ""),
            "admission_id": (1, ""),
        }.items():
            mutations += [{**valid, field: value} for value in values]
    path = verify_duration.history_path()
    path.parent.mkdir(parents=True)
    # A valid control proves explicit nulls and zero seconds/exits remain accepted.
    path.write_text("\n".join(map(json.dumps, records)) + "\n")
    assert _run(capsys, "report")[0] == 0
    for malformed in mutations:
        changed = [dict(record) for record in records]
        changed[index] = malformed
        # Even a later valid record of the same type must not repair persisted history.
        changed.append(valid)
        original = "\n".join(map(json.dumps, changed)) + "\n"
        path.write_text(original)
        for selection in ((), ("--run", "validated")):
            code, out, _ = _run(capsys, "report", *selection)
            assert code != 0, malformed
            assert "incomplete" in out and "history note:" in out, malformed
            assert "verdict green" not in out and "verdict: green" not in out, malformed
        assert path.read_text() == original


@pytest.mark.parametrize(
    "completion",
    [
        {"verdict": "green"},
        {"verdict": "green", "seconds": -1},
        {"verdict": "green", "seconds": float("nan")},
        {"verdict": "green", "seconds": float("inf")},
        {"verdict": "green", "seconds": float("-inf")},
        {"verdict": "green", "seconds": None},
        {"verdict": "green", "seconds": True},
        {"verdict": "green", "seconds": "1"},
        {"seconds": 1},
        {"verdict": "unknown", "seconds": 1},
    ],
)
def test_reader_rejects_malformed_completion(
    completion: dict, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Invalid completion fields cannot turn an interrupted run into a green run."""
    root = tmp_path / "state" / "coding-harness"
    root.mkdir(parents=True)
    start = _valid_records("broken-end")[0]
    end = {key: value for key, value in _valid_records("broken-end")[2].items() if key not in ("seconds", "verdict")}
    end.update(completion)
    path = root / verify_duration.HISTORY_NAME
    original = "\n".join(json.dumps(event) for event in (start, end)) + "\n"
    path.write_text(original, encoding="utf-8")

    events, parsing = verify_duration._read_events()
    runs, grouping = verify_duration._runs(events)
    assert runs["broken-end"]["end"] is None
    assert parsing or grouping
    for selection in ((), ("--run", "broken-end")):
        code, out, _ = _run(capsys, "report", *selection)
        assert code != 0
        assert "incomplete" in out and "history note:" in out
        assert "verdict green" not in out and "verdict: green" not in out
    assert path.read_text(encoding="utf-8") == original


@pytest.mark.parametrize("verdict", ["green", "red"])
@pytest.mark.parametrize("seconds", [0, 1.5])
def test_reader_accepts_valid_completion(
    verdict: str, seconds: float, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Zero and positive durations remain valid for both completion outcomes."""
    root = tmp_path / "state" / "coding-harness"
    root.mkdir(parents=True)
    events = [
        _valid_records("valid-end")[0],
        {**_valid_records("valid-end")[2], "seconds": seconds, "verdict": verdict},
    ]
    (root / verify_duration.HISTORY_NAME).write_text("\n".join(map(json.dumps, events)) + "\n", encoding="utf-8")
    for selection in ((), ("--run", "valid-end")):
        code, out, _ = _run(capsys, "report", *selection)
        assert code == 0
        assert verdict in out and f"{seconds:.3f}s" in out
        assert "incomplete" not in out and "history note:" not in out


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
                "utc": "2026-11-04T10:01:00+00:00",
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


@pytest.mark.parametrize("porcelain,returncode,dirty", [("", 0, False), (" M x", 0, True), ("", 1, None)])
def test_real_git_helper_preserves_clean_answer(tmp_path, monkeypatch, capsys, porcelain, returncode, dirty):
    """Exercise the real helper: a successful empty status is a clean tree."""

    def answer(arguments, **_kwargs):
        return subprocess.CompletedProcess(arguments, returncode, porcelain if "status" in arguments else "a" * 40, "")

    monkeypatch.setattr(verify_duration.subprocess, "run", answer)
    assert _run(capsys, "start")[0] == 0
    assert _history(tmp_path / "state")[-1]["dirty"] is dirty


@pytest.mark.parametrize("kind", ["symlink", "fifo"])
def test_reader_refuses_substituted_history(tmp_path, kind):
    """A reader neither follows a symlink nor blocks waiting for a FIFO writer."""
    path = verify_duration.history_path()
    path.parent.mkdir(parents=True)
    if kind == "symlink":
        victim = tmp_path / "foreign"
        victim.write_text('{"v":1,"event":"run_start","run_id":"foreign"}\n')
        path.symlink_to(victim)
    else:
        os.mkfifo(path)
    try:
        done = subprocess.run(
            [sys.executable, "-m", "scripts.verify_duration", "report"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("the history reader blocked on a substituted destination")
    assert done.returncode == 2, done
    assert "refusing" in done.stderr and "foreign" not in done.stdout


@pytest.mark.parametrize("version", [None, 0, 2, "1", True])
def test_reader_refuses_unsupported_event_version(capsys, version):
    """An incompatible end cannot turn a valid start into a completed run."""
    path = verify_duration.history_path()
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(_valid_records("one")[0])
        + "\n"
        + json.dumps({"v": version, "event": "run_end", "run_id": "one", "verdict": "green"})
        + "\n"
    )
    code, out, _ = _run(capsys, "report")
    assert code == 0 and "incomplete" in out and "green" not in out
    assert "line 2" in out and "version" in out and repr(version) in out


@pytest.mark.parametrize("fault", ["lock", "write", "short-write"])
def test_append_io_failure_is_named_refusal(monkeypatch, capsys, fault):
    """Lock, disk-full and incomplete writes use the CLI refusal, never a traceback."""

    def fail(*_args):
        raise OSError(errno.ENOSPC, "injected storage failure")

    if fault == "lock":
        monkeypatch.setattr(verify_duration.fcntl, "flock", fail)
    elif fault == "write":
        monkeypatch.setattr(verify_duration.os, "write", fail)
    else:
        monkeypatch.setattr(verify_duration.os, "write", lambda _fd, data: len(data) - 1)
    try:
        code, _, err = _run(capsys, "start")
    except OSError as error:
        pytest.fail(f"storage failure escaped the CLI refusal handler: {error}")
    assert code == 2 and "refusing" in err and "Traceback" not in err


def test_writer_refuses_hard_linked_history(tmp_path, capsys):
    """An existing history with another name is an alias, never an append target."""
    path = verify_duration.history_path()
    path.parent.mkdir(parents=True)
    victim = tmp_path / "victim"
    victim.write_text("unchanged\n")
    os.link(victim, path)
    code, _, err = _run(capsys, "start")
    assert code == 2 and "refusing" in err
    assert victim.read_text() == "unchanged\n"


# ---------------------------------------------------------------------------
# Criterion 11 — targeted and slip records keep the history safe and compatible
# ---------------------------------------------------------------------------


def test_targeted_history_preserves_safety_and_legacy_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 11. Faults this pins: a new event kind breaking the version-1 reader or its
    verdicts, raw output or a credential landing in a record, concurrent slip writers mixing or
    doubling a row, a storage failure changing a verdict instead of being named, or a substituted
    destination being written through by one of the new writers.
    """
    state = tmp_path / "state"
    root = state / "coding-harness"
    root.mkdir(parents=True)
    path = root / verify_duration.HISTORY_NAME

    # The version-1 records read exactly as before, beside targeted and slip rows: the new
    # kinds never join a run, so the old run keeps its green verdict and its detail view.
    legacy = _valid_records("legacy-run")
    targeted_row = {
        "v": 1,
        "event": "targeted",
        "check_id": "check-one",
        "utc": "2026-11-04T10:02:00+00:00",
        "repository": str(REPO_ROOT),
        "worktree": str(tmp_path),
        "change": "demo",
        "verb": "implement",
        "tests": ["tests/test_demo.py"],
        "gates": ["criterion-ledger"],
        "outcome": "green",
        "config_sha256": "e" * 64,
        "tree": "f" * 40,
        "commit": None,
    }
    slip_row = {
        "v": 1,
        "event": "slip",
        "check_id": "check-one",
        "run_id": "legacy-run",
        "utc": "2026-11-04T10:03:00+00:00",
        "repository": str(REPO_ROOT),
        "failed_gates": ["pytest"],
        "failed_tests": None,
        "config_sha256": "e" * 64,
        "tree": "f" * 40,
    }
    path.write_text("\n".join(json.dumps(row) for row in [*legacy, targeted_row, slip_row]) + "\n", encoding="utf-8")
    code, out, _ = _run(capsys, "report")
    assert code == 0, out
    assert "run legacy-run" in out and "green" in out and "1.500s" in out, out
    assert "history note:" not in out, "a targeted or slip row was mistaken for a version-1 record"
    code, out, _ = _run(capsys, "report", "--run", "legacy-run")
    assert code == 0 and "pytest" in out and "verdict: green" in out, out

    # The runner's writer stores identifiers only: the field set leaves no room for command
    # output, environment dumps or credentials.
    verify_duration.append_targeted(
        repository=str(tmp_path),
        worktree=str(tmp_path / "wt"),
        change="demo",
        verb="implement",
        check_id="check-two",
        tests=["tests/test_demo.py"],
        gates=["criterion-ledger"],
        config_sha256="e" * 64,
        tree="f" * 40,
        commit=None,
        outcome="green",
    )
    stored = _history(state)[-1]
    assert stored["event"] == "targeted" and stored["check_id"] == "check-two"
    assert set(stored) == {
        "v",
        "event",
        "check_id",
        "utc",
        "repository",
        "worktree",
        "change",
        "verb",
        "tests",
        "gates",
        "outcome",
        "config_sha256",
        "tree",
        "commit",
    }, "the targeted record carries a field that is not a bounded identifier"

    # Concurrent slip writers never mix lines and never count one full run twice: the
    # deduplication shares the append's lock, so four racing writers leave one row.
    def slip_event(run_id: str) -> dict:
        return {
            "v": 1,
            "event": "slip",
            "check_id": "check-two",
            "run_id": run_id,
            "utc": "2026-11-04T10:04:00+00:00",
            "repository": str(REPO_ROOT),
            "failed_gates": [],
            "failed_tests": None,
            "config_sha256": None,
            "tree": "f" * 40,
        }

    results: list[bool] = []
    writers = [
        threading.Thread(target=lambda: results.append(verify_duration.append_slip(slip_event("race-run"))))
        for _ in range(4)
    ]
    for worker in writers:
        worker.start()
    for worker in writers:
        worker.join()
    assert sum(results) == 1, f"one full run was counted {sum(results)} times under a race"
    races = [row for row in _history(state) if row["event"] == "slip" and row["run_id"] == "race-run"]
    assert len(races) == 1, "the racing writers left more than one slip row"

    # Different full runs append independently under the same lock: two more rows, none mixed.
    results = []
    writers = [
        threading.Thread(target=lambda rid=rid: results.append(verify_duration.append_slip(slip_event(rid))))
        for rid in ("race-a", "race-b")
    ]
    for worker in writers:
        worker.start()
    for worker in writers:
        worker.join()
    assert sum(results) == 2, "a distinct full run was refused as a duplicate"
    slips = [row for row in _history(state) if row["event"] == "slip"]
    assert sorted(row["run_id"] for row in slips) == ["legacy-run", "race-a", "race-b", "race-run"]
    assert sum(1 for row in slips if row["run_id"] == "race-run") == 1
    for line in path.read_text(encoding="utf-8").splitlines():
        json.loads(line)  # a mixed or partial write would raise here

    # A storage failure is named and leaves the standing records untouched — the caller keeps
    # its verdict and reports that measurement is unavailable, never a silent pass.
    before = path.read_text(encoding="utf-8")

    def fail(*_args):
        raise OSError(errno.ENOSPC, "injected storage failure")

    with monkeypatch.context() as failure:
        failure.setattr(verify_duration.os, "write", fail)
        with pytest.raises(verify_duration.StorageUnusable):
            verify_duration.append_slip(slip_event("run-lost"))
        with pytest.raises(verify_duration.StorageUnusable):
            verify_duration.append_targeted(
                repository=str(tmp_path),
                worktree=str(tmp_path),
                change="demo",
                verb="implement",
                check_id="check-lost",
                tests=[],
                gates=[],
                config_sha256=None,
                tree="f" * 40,
                commit=None,
                outcome="green",
            )
    assert path.read_text(encoding="utf-8") == before, "a failed write changed the standing history"

    # A substituted destination is refused by the new writers exactly as by the old ones:
    # nothing is written through the link.
    victim = tmp_path / "victim.jsonl"
    victim.write_text("do not write through me\n", encoding="utf-8")
    path.unlink()
    path.symlink_to(victim)
    with pytest.raises(verify_duration.StorageUnusable):
        verify_duration.append_slip(slip_event("run-sub"))
    with pytest.raises(verify_duration.StorageUnusable):
        verify_duration.append_slip(slip_event("run-sub"))
    with pytest.raises(verify_duration.StorageUnusable):
        verify_duration.append_targeted(
            repository=str(tmp_path),
            worktree=str(tmp_path),
            change="demo",
            verb="implement",
            check_id="check-sub",
            tests=[],
            gates=[],
            config_sha256=None,
            tree="f" * 40,
            commit=None,
            outcome="green",
        )
    assert victim.read_text(encoding="utf-8") == "do not write through me\n"


# ---------------------------------------------------------------------------
# Criterion 12 — the slip report counts one repository's distinct slipped runs
# ---------------------------------------------------------------------------


def test_slip_report_counts_interval_and_reports_gaps(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 12. Faults this pins: a duplicated full run counted twice, another repository
    or interval counted, or missing, corrupt or incomplete evidence reported as a trustworthy
    zero instead of an unavailable measurement.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    since = "2026-01-01T00:00:00+00:00"
    until = "2027-01-01T00:00:00+00:00"

    # No history at all: the measurement is unavailable, never zero.
    fresh = tmp_path / "fresh-state"
    monkeypatch.setenv("XDG_STATE_HOME", str(fresh))
    code, out, _ = _run(capsys, "slips", "--repository", str(repo), "--since", since, "--until", until)
    assert code == 1 and "unavailable" in out, (code, out)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))

    # The runner's own flow: one accepted targeted green, then one correlated completed red
    # full run on the same tree and gate configuration. The green carries the digest the run
    # start recorded, exactly as the runner reads both from the same gate file.
    tree = "d" * 40
    check_id = "check-targeted"
    correlation = "corr-" + "a" * 12
    monkeypatch.setenv(verify_duration.CORRELATION_ENV, correlation)
    code, run_id, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    run_id = run_id.strip()
    monkeypatch.delenv(verify_duration.CORRELATION_ENV)
    started = _history(tmp_path / "state")[-1]
    assert started["event"] == "run_start" and started["correlation"] == correlation
    verify_duration.append_targeted(
        repository=str(repo),
        worktree=str(tmp_path / "wt"),
        change="demo",
        verb="implement",
        check_id=check_id,
        tests=["tests/test_demo.py"],
        gates=["pytest"],
        config_sha256=started["config_sha256"],
        tree=tree,
        commit=None,
        outcome="green",
    )
    code, _, _ = _run(
        capsys,
        "gate",
        "--run",
        run_id,
        "--gate",
        "pytest",
        "--start",
        "0.0",
        "--end",
        "1.0",
        "--status",
        "1",
        "--enforcement",
        "block",
    )
    assert code == 0
    code, _, _ = _run(capsys, "end", "--run", run_id, "--start", "0.0", "--end", "9.0", "--verdict", "red")
    assert code == 0
    note = verify_duration.record_local_slip(str(repo), correlation, tree, ["tests/test_demo.py::test_demo"])
    assert "recorded one local slip" in note, note

    # The count CLI names the count and its interval and repository; the half-open window
    # holds the slip once.
    done = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.verify_duration",
            "slips",
            "--repository",
            str(repo),
            "--since",
            since,
            "--until",
            until,
        ],
        cwd=REPO_ROOT,
        env=dict(os.environ, XDG_STATE_HOME=str(tmp_path / "state")),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert done.returncode == 0, done
    assert "slips: 1 distinct slipped full runs" in done.stdout, done.stdout
    assert f"repository {repo}" in done.stdout, done.stdout

    # Reprocessing the same completed red run adds nothing: one slip per full-run identity.
    note = verify_duration.record_local_slip(str(repo), correlation, tree, ["tests/test_demo.py::test_demo"])
    assert "stands already" in note, note
    code, out, _ = _run(capsys, "slips", "--repository", str(repo), "--since", since, "--until", until)
    assert code == 0 and "slips: 1" in out, out

    # A second completed red run on the same green is a distinct slipped run: the count grows.
    second_corr = "corr-" + "b" * 12
    monkeypatch.setenv(verify_duration.CORRELATION_ENV, second_corr)
    code, second_run, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    second_run = second_run.strip()
    monkeypatch.delenv(verify_duration.CORRELATION_ENV)
    code, _, _ = _run(
        capsys,
        "gate",
        "--run",
        second_run,
        "--gate",
        "pytest",
        "--start",
        "0.0",
        "--end",
        "1.0",
        "--status",
        "1",
        "--enforcement",
        "block",
    )
    assert code == 0
    code, _, _ = _run(capsys, "end", "--run", second_run, "--start", "0.0", "--end", "8.0", "--verdict", "red")
    assert code == 0
    note = verify_duration.record_local_slip(str(repo), second_corr, tree, None)
    assert "recorded one local slip" in note, note
    code, out, _ = _run(capsys, "slips", "--repository", str(repo), "--since", since, "--until", until)
    assert code == 0 and "slips: 2" in out, out

    # A duplicated slip row for an already-counted run (an old writer's race, replayed here by
    # appending directly) is not counted again: distinct run identities decide.
    duplicate = dict(slip_event_like(check_id, second_run, str(repo), tree))
    duplicate["check_id"] = "check-replay"
    verify_duration.append_event(duplicate)
    code, out, _ = _run(capsys, "slips", "--repository", str(repo), "--since", since, "--until", until)
    assert code == 0 and "slips: 2" in out, out

    # Another repository's slip stays out of this count.
    other = tmp_path / "other"
    other.mkdir()
    verify_duration.append_event(slip_event_like("check-other", "run-other", str(other), tree))
    code, out, _ = _run(capsys, "slips", "--repository", str(repo), "--since", since, "--until", until)
    assert code == 0 and "slips: 2" in out, out
    code, out, _ = _run(capsys, "slips", "--repository", str(other), "--since", since, "--until", until)
    assert code == 0 and "slips: 1" in out, out

    # The interval is half-open on UTC instants: a 2020 slip sits outside the 2026 window,
    # inside its own window at the inclusive start, and outside at the exclusive end.
    old = slip_event_like("check-old", "run-old", str(repo), tree)
    old["utc"] = "2020-06-01T12:00:00+00:00"
    verify_duration.append_event(old)
    code, out, _ = _run(capsys, "slips", "--repository", str(repo), "--since", since, "--until", until)
    assert code == 0 and "slips: 2" in out, out
    code, out, _ = _run(
        capsys,
        "slips",
        "--repository",
        str(repo),
        "--since",
        "2020-06-01T12:00:00+00:00",
        "--until",
        "2020-06-01T12:00:01+00:00",
    )
    assert code == 0 and "slips: 1" in out and "inclusive" in out and "exclusive" in out, out
    code, out, _ = _run(
        capsys,
        "slips",
        "--repository",
        str(repo),
        "--since",
        "2020-06-01T11:59:59+00:00",
        "--until",
        "2020-06-01T12:00:00+00:00",
    )
    assert code == 0 and "slips: 0" in out, out

    # Corrupt rows and an invalid slip record make the count explicitly untrustworthy —
    # it is never presented as a clean zero or a clean total.
    path = tmp_path / "state" / "coding-harness" / verify_duration.HISTORY_NAME
    broken_slip = slip_event_like("check-broken", "run-broken", str(repo), tree)
    del broken_slip["tree"]
    original = path.read_text(encoding="utf-8")
    path.write_text(original + "not json at all{{\n" + json.dumps(broken_slip) + "\n", encoding="utf-8")
    code, out, _ = _run(capsys, "slips", "--repository", str(repo), "--since", since, "--until", until)
    assert code == 1 and "not trustworthy" in out and "incomplete" in out, (code, out)


def slip_event_like(check_id: str, run_id: str, repository: str, tree: str) -> dict:
    """One valid slip record, used to seed reader cases directly."""
    return {
        "v": 1,
        "event": "slip",
        "check_id": check_id,
        "run_id": run_id,
        "utc": "2026-06-01T12:00:00+00:00",
        "repository": repository,
        "failed_gates": ["pytest"],
        "failed_tests": None,
        "config_sha256": None,
        "tree": tree,
    }


def seed_correlated_red(
    repo: Path, monkeypatch: pytest.MonkeyPatch, capsys, config: str | None, target_config: str | None
) -> str:
    """An isolated accepted green and completed blocking red with runner correlation."""
    monkeypatch.setattr(verify_duration, "_gate_file_digest", lambda: config)
    monkeypatch.setattr(verify_duration, "_git", lambda argv: "commit" if argv[0] == "rev-parse" else "")
    monkeypatch.chdir(repo)
    monkeypatch.setenv(verify_duration.CORRELATION_ENV, "correlation")
    _, run, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    run = run.strip()
    verify_duration.append_targeted(
        repository=str(repo),
        worktree=str(repo),
        change="demo",
        verb="implement",
        check_id="green",
        tests=["tests/test_demo.py"],
        gates=["pytest"],
        config_sha256=target_config,
        tree="d" * 40,
        commit="commit",
        outcome="green",
    )
    _run(
        capsys,
        "gate",
        "--run",
        run,
        "--gate",
        "pytest",
        "--start",
        "0",
        "--end",
        "1",
        "--status",
        "1",
        "--enforcement",
        "block",
    )
    _run(capsys, "end", "--run", run, "--start", "0", "--end", "2", "--verdict", "red")
    return run


def test_slips_detects_failed_correlated_append(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    """A lost slip append leaves a visible measurement gap rather than a trustworthy zero."""
    repo = tmp_path / "repo"
    repo.mkdir()
    seed_correlated_red(repo, monkeypatch, capsys, "a" * 64, "a" * 64)

    def fail_append(_event):
        raise verify_duration.StorageUnusable("planted storage failure")

    append_slip = verify_duration.append_slip
    monkeypatch.setattr(verify_duration, "append_slip", fail_append)
    with pytest.raises(verify_duration.StorageUnusable):
        verify_duration.record_local_slip(str(repo), "correlation", "d" * 40, None)
    code, out, _ = _run(
        capsys, "slips", "--repository", str(repo), "--since", "2020-01-01T00:00:00Z", "--until", "2100-01-01T00:00:00Z"
    )
    assert code == 1 and "not measured" in out and "slips: 0" not in out, out
    # Reprocessing after storage recovers fills the gap; the reader then trusts the one count.
    monkeypatch.setattr(verify_duration, "append_slip", append_slip)
    assert "recorded one local slip" in verify_duration.record_local_slip(str(repo), "correlation", "d" * 40, None)
    code, out, _ = _run(
        capsys, "slips", "--repository", str(repo), "--since", "2020-01-01T00:00:00Z", "--until", "2100-01-01T00:00:00Z"
    )
    assert code == 0 and "slips: 1" in out, out


@pytest.mark.parametrize("config,target_config", [(None, None), (None, "a" * 64), ("a" * 64, None)])
def test_unknown_gate_digests_never_correlate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys, config: str | None, target_config: str | None
) -> None:
    """Two unreadable gate digests are unknown identities, never a matching configuration."""
    repo = tmp_path / "repo"
    repo.mkdir()
    seed_correlated_red(repo, monkeypatch, capsys, config, target_config)
    note = verify_duration.record_local_slip(str(repo), "correlation", "d" * 40, None)
    assert "unmeasured" in note, note
    events, _ = verify_duration._read_events()
    assert not [event for event in events if event["event"] == verify_duration.SLIP]
