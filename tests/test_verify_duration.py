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
    runs, grouping, _damaged, _unassigned = verify_duration._runs(events)
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


def test_slip_evidence_is_derived_never_persisted(capsys) -> None:
    """Q-1 and Q-2 supersede the Q-9 deferral: slips are derived, never written.

    The reader exists (`slips`), and the targeted check records ordinary run
    evidence, but the history gains no slip event of its own: the event kinds
    stay the three duration ones, no slip writer appears, and the CLI exposes
    no targeted operation — the targeted evidence is recorded by the runner
    through the module, not through a command of its own.
    """
    with pytest.raises(SystemExit) as stopped:
        verify_duration.main(["--help"])
    assert stopped.value.code == 0
    help_text = capsys.readouterr().out
    assert re.search(r"\bslips\b", help_text), "the derived reader is not exposed"
    assert not re.search(r"\btargeted\b", help_text), "a targeted CLI operation appeared"
    assert verify_duration.EVENTS == ("run_start", "gate", "run_end"), "a slip event kind appeared"
    for writer in ("append_slip", "record_slip", "record_local_slip"):
        assert not hasattr(verify_duration, writer), f"slip writer {writer} is callable"


# ---------------------------------------------------------------------------
# Slips — the derived count beside the runs that could not be counted
# ---------------------------------------------------------------------------

TREE = "t" * 40
CONFIG = "d" * 64


def _run_start(
    run_id: str,
    *,
    utc: str,
    repository: str,
    kind: str | None = None,
    change: str | None = None,
    tree: str | None = None,
    config: str | None = CONFIG,
) -> dict:
    """A version-1 start record; `kind None` gives the legacy shape without comparison fields."""
    record = {
        "v": 1,
        "event": "run_start",
        "run_id": run_id,
        "utc": utc,
        "repository": repository,
        "commit": "c" * 40,
        "dirty": False,
        "config_sha256": config,
        "job": "verify",
        "placement": "local",
        "memory_pct": None,
        "workers": None,
        "admission_id": None,
        "admission_wait_seconds": None,
        "admission_reused": None,
    }
    if kind is not None:
        record.update({"check_kind": kind, "change": change, "tree_id": tree})
    return record


def _run_end(run_id: str, *, utc: str, verdict: str = "green", seconds: float = 1.0, tree: str | None = None) -> dict:
    """A version-1 end record; `tree` is the post-execution identity of a targeted completion."""
    end = {"v": 1, "event": "run_end", "run_id": run_id, "utc": utc, "seconds": seconds, "verdict": verdict}
    if tree is not None:
        end["tree_id"] = tree
    return end


def _write_history(state: Path, events: list[dict]) -> Path:
    """The given records as the one history file, without going through any writer."""
    root = state / "coding-harness"
    root.mkdir(parents=True, exist_ok=True)
    path = root / verify_duration.HISTORY_NAME
    path.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
    return path


def _measured_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """A repository directory the reader runs in, so records of it are in scope by default."""
    repo = tmp_path / "repo"
    repo.mkdir()
    monkeypatch.chdir(repo)
    return str(repo)


def _slip_events(
    repository: str,
    *,
    change: str = "demo",
    tree: str | None = TREE,
    config: str | None = CONFIG,
    targeted_end: str = "2026-11-13T09:05:00+00:00",
    full_utc: str = "2026-11-13T11:00:00+00:00",
    targeted_id: str = "t-1",
    full_id: str = "f-1",
    targeted_kind: str | None = "targeted",
    targeted_verdict: str = "green",
    full_kind: str | None = "full",
    full_verdict: str = "red",
    full_change: str | None = None,
    full_tree: str | None = None,
    full_config: str | None = None,
) -> list[dict]:
    """One targeted check and a later full run of the same identity; the fields shape the case."""
    return [
        _run_start(
            targeted_id,
            utc="2026-11-13T09:00:00+00:00",
            repository=repository,
            kind=targeted_kind,
            change=change,
            tree=tree,
            config=config,
        ),
        _run_end(targeted_id, utc=targeted_end, verdict=targeted_verdict, tree=tree if targeted_kind else None),
        _run_start(
            full_id,
            utc=full_utc,
            repository=repository,
            kind=full_kind,
            change=change if full_change is None else full_change,
            tree=tree if full_tree is None else full_tree,
            config=config if full_config is None else full_config,
        ),
        _run_end(full_id, utc="2026-11-13T11:30:00+00:00", verdict=full_verdict),
    ]


def _slips(capsys: pytest.CaptureFixture[str], *argv: str) -> tuple[int, str, str]:
    """One slips operation in process: exit code, stdout, stderr."""
    return _run(capsys, "slips", *argv)


def test_slips_count_each_matching_red_full_run_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A qualifying red full run counts once, whatever the predecessor multiplicity.

    Fault this pins: a qualifying run counting zero, several green predecessors
    multiplying it, or repeated identical records multiplying it.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    events = [
        # Two distinct green targeted predecessors of the same identity, then the
        # red full run that missed both — plus its start row written twice, as a
        # retried append leaves it.
        *_slip_events(repository, targeted_id="t-1", targeted_end="2026-11-13T09:05:00+00:00"),
        *_slip_events(repository, targeted_id="t-2", full_id="f-1"),
        # A second, distinct red full run of the same identity counts once more.
        *_slip_events(repository, targeted_id="t-3", full_id="f-2", full_utc="2026-11-13T12:00:00+00:00"),
    ]
    duplicate = dict(events[2])  # f-1's start row again, dict-equal — a retried append, not a conflict
    events.append(duplicate)
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys)
    assert code == 0, out
    assert "slips: 2; incomplete/not countable runs: 0" in out, out
    assert f"repository {os.path.realpath(repository)}" in out and "change all" in out, out
    # Reading twice reports the same count from the same bytes.
    code_again, out_again, _ = _slips(capsys)
    assert code_again == 0 and out_again == out, out_again


@pytest.mark.parametrize(
    "case",
    [
        "targeted-red",
        "full-green",
        "fallback-masquerade",
        "reversed-order",
        "same-instant",
        "other-tree",
        "other-change",
        "other-config",
        "other-repository",
        "unknown-tree",
        "legacy-predecessor",
    ],
)
def test_slips_require_complete_matching_predecessor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], case: str
) -> None:
    """Mismatched identity, order, kind or verdict never establishes a slip.

    Fault this pins: a targeted red, a full green, a full fallback masquerading
    as targeted, a reversed or overlapping completion order, another repository,
    change, tree or configuration, or an unknown identity counting as a slip.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    if case == "targeted-red":
        events = _slip_events(repository, targeted_verdict="red")
    elif case == "full-green":
        events = _slip_events(repository, full_verdict="green")
    elif case == "fallback-masquerade":
        # The only run in the history is the red one, recorded as targeted: a
        # fallback must never masquerade as a green targeted predecessor.
        events = [
            _run_start(
                "f-1",
                utc="2026-11-13T11:00:00+00:00",
                repository=repository,
                kind="targeted",
                change="demo",
                tree=TREE,
                config=CONFIG,
            ),
            _run_end("f-1", utc="2026-11-13T11:30:00+00:00", verdict="red"),
        ]
    elif case == "reversed-order":
        events = _slip_events(repository, full_utc="2026-11-13T08:00:00+00:00")
    elif case == "same-instant":
        events = _slip_events(repository, full_utc="2026-11-13T09:05:00+00:00")
    elif case == "other-tree":
        events = _slip_events(repository, tree="t2" * 20, full_tree=TREE)
    elif case == "other-change":
        events = _slip_events(repository, change="other", full_change="demo")
    elif case == "other-config":
        events = _slip_events(repository, config="d2" * 32, full_config=CONFIG)
    elif case == "other-repository":
        events = _slip_events(repository + "-elsewhere")
    elif case == "unknown-tree":
        events = _slip_events(repository, tree=None)
    else:  # legacy-predecessor
        events = _slip_events(repository, targeted_kind=None)
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys)
    assert "slips: 0;" in out, (case, out)
    if case == "unknown-tree":
        # Both runs name their comparison tree as the explicit unknown: the green
        # predecessor counts nowhere, and the red full run cannot count against it.
        assert "incomplete/not countable runs: 2" in out and code == 1, (case, out)
    else:
        assert "incomplete/not countable runs: 0" in out and code == 0, (case, out)


@pytest.mark.parametrize(
    "case",
    [
        "lost-end",
        "conflicting-ends",
        "conflicting-starts",
        "missing-comparison",
        "legacy-red",
    ],
)
def test_slips_show_incomplete_runs_beside_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], case: str
) -> None:
    """A lost end, a conflicting duplicate or a missing comparison field appears once as not countable.

    Fault this pins: an identifiable interrupted or conflicting run vanishing,
    being counted twice, or being represented by a bare zero.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    if case == "lost-end":
        events = [
            # The green completion never arrived: the targeted run stays a start,
            # and the red full run beside it has no countable predecessor.
            _run_start(
                "t-1",
                utc="2026-11-13T09:00:00+00:00",
                repository=repository,
                kind="targeted",
                change="demo",
                tree=TREE,
                config=CONFIG,
            ),
            _run_start(
                "f-1",
                utc="2026-11-13T11:00:00+00:00",
                repository=repository,
                kind="full",
                change="demo",
                tree=TREE,
                config=CONFIG,
            ),
            _run_end("f-1", utc="2026-11-13T11:30:00+00:00", verdict="red"),
        ]
    elif case == "conflicting-ends":
        events = _slip_events(repository) + [
            _run_end("f-1", utc="2026-11-13T11:45:00+00:00", verdict="green"),
        ]
    elif case == "conflicting-starts":
        events = [
            _run_start(
                "f-1",
                utc="2026-11-13T11:00:00+00:00",
                repository=repository,
                kind="full",
                change="demo",
                tree=TREE,
                config=CONFIG,
            ),
            _run_start(
                "f-1",
                utc="2026-11-13T11:10:00+00:00",
                repository=repository,
                kind="full",
                change="demo",
                tree=TREE,
                config=CONFIG,
            ),
            *_slip_events(repository)[:2],  # the targeted green predecessor
            _run_end("f-1", utc="2026-11-13T11:30:00+00:00", verdict="red"),
        ]
    elif case == "missing-comparison":
        events = _slip_events(repository)[:2] + [
            _run_start(
                "f-1",
                utc="2026-11-13T11:00:00+00:00",
                repository=repository,
                kind="full",
                change=None,
                tree=None,
                config=None,
            ),
            _run_end("f-1", utc="2026-11-13T11:30:00+00:00", verdict="red"),
        ]
    else:  # legacy-red
        events = [
            _run_start(
                "t-1",
                utc="2026-11-13T09:00:00+00:00",
                repository=repository,
                kind="targeted",
                change="demo",
                tree=TREE,
                config=CONFIG,
            ),
            _run_end("t-1", utc="2026-11-13T09:05:00+00:00", verdict="green", tree=TREE),
            # A legacy full red run: no comparison fields, so no countable slip.
            _run_start("f-1", utc="2026-11-13T11:00:00+00:00", repository=repository),
            _run_end("f-1", utc="2026-11-13T11:30:00+00:00", verdict="red"),
        ]
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys)
    assert code == 1, (case, out)
    assert "slips: 0; incomplete/not countable runs: 1" in out, (case, out)
    assert "evidence partial" in out, (case, out)
    # The damaged runs keep their diagnosis, named and visible.
    if case in ("conflicting-ends", "conflicting-starts"):
        assert "history note:" in out, (case, out)


def test_slips_select_interval_repository_and_change(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Only selected runs enter the counts; a pre-interval predecessor still pairs.

    Fault this pins: another repository, an out-of-interval full run or an
    out-of-interval incomplete run changing either count, or a matching
    predecessor before the interval being lost for a selected full run.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    elsewhere = repository + "-elsewhere"
    events = [
        # The alpha predecessor lies before `since`; the alpha full run inside
        # the interval must still pair with it.
        *_slip_events(repository, targeted_id="t-alpha", full_id="f-alpha", change="alpha"),
        # A beta full run of another checked tree: a known nonmatch, never a slip.
        *_slip_events(
            repository,
            targeted_id="t-beta",
            full_id="f-beta",
            change="beta",
            tree="b" * 40,
            full_tree="c" * 40,
            full_utc="2026-11-13T12:30:00+00:00",
        ),
        # Another repository's identical red run never enters this reader's counts.
        *_slip_events(elsewhere, targeted_id="t-far", full_id="f-far", full_utc="2026-11-13T12:00:00+00:00"),
        # An incomplete run outside the interval, and one inside it.
        _run_start(
            "f-late",
            utc="2026-11-13T15:00:00+00:00",
            repository=repository,
            kind="full",
            change="alpha",
            tree=TREE,
            config=CONFIG,
        ),
        _run_start(
            "t-early-broken",
            utc="2026-11-13T08:00:00+00:00",
            repository=repository,
            kind="targeted",
            change="alpha",
            tree=TREE,
            config=CONFIG,
        ),
    ]
    _write_history(tmp_path / "state", events)

    window = ("--since", "2026-11-13T10:00:00+00:00", "--until", "2026-11-13T14:00:00+00:00")
    code, out, _ = _slips(capsys, *window)
    assert code == 0, out
    assert "slips: 1; incomplete/not countable runs: 0" in out, out
    assert f"repository {os.path.realpath(repository)}" in out, out

    code, out, _ = _slips(capsys, *window, "--change", "beta")
    assert code == 0 and "slips: 0; incomplete/not countable runs: 0" in out, out

    code, out, _ = _slips(capsys, "--change", "alpha")
    assert code == 1 and "slips: 1; incomplete/not countable runs: 2" in out, out

    # A reversed interval refuses with exit 2; a naive bound is not an instant.
    code, _, err = _slips(capsys, "--since", "2026-11-13T14:00:00+00:00", "--until", "2026-11-13T10:00:00+00:00")
    assert code == 2 and "reversed" in err, err
    with pytest.raises(SystemExit) as stopped:
        _slips(capsys, "--since", "2026-11-13T10:00:00")
    assert stopped.value.code == 2


def test_slips_distinguish_complete_partial_and_unavailable_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Incomplete, corrupt, unsupported or missing history never exits as a complete zero.

    Fault this pins: an incomplete run, a malformed or unassignable row,
    unsupported evidence or missing history producing a complete-success exit or
    a purported complete zero, or valid observations beside a diagnosed gap
    vanishing.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    state = tmp_path / "state"
    targeted_pair = [
        _run_start(
            "t-1",
            utc="2026-11-13T09:00:00+00:00",
            repository=repository,
            kind="targeted",
            change="demo",
            tree=TREE,
            config=CONFIG,
        ),
        _run_end("t-1", utc="2026-11-13T09:05:00+00:00", verdict="green", tree=TREE),
    ]

    # Missing history: unavailable, never a zero, and never a complete success.
    code, out, err = _slips(capsys)
    assert code == 1, (out, err)
    assert "slips: unavailable; incomplete/not countable runs: unavailable" in out, out
    assert "slips: 0" not in out and "no history" in err, (out, err)

    # A malformed unassignable row keeps the valid counts and makes them partial.
    _write_history(state, targeted_pair)
    path = state / "coding-harness" / verify_duration.HISTORY_NAME
    path.write_text(path.read_text(encoding="utf-8") + "garbage{{ not json\n", encoding="utf-8")
    code, out, _ = _slips(capsys)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 0" in out, out
    assert "history note: line 3" in out, out

    # An unsupported version is diagnosed, not read as clean evidence.
    future_end = {
        "v": 2,
        "event": "run_end",
        "run_id": "t-1",
        "utc": "2026-11-13T09:06:00+00:00",
        "seconds": 1,
        "verdict": "green",
    }
    _write_history(state, targeted_pair + [future_end])
    code, out, _ = _slips(capsys)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 0" in out, out
    assert "unsupported event version" in out, out

    # A damaged run of another repository keeps its diagnosis; the report says partial.
    far_starts = [
        _run_start("far", utc="2026-11-13T09:00:00+00:00", repository=repository + "-elsewhere"),
        _run_start("far", utc="2026-11-13T09:30:00+00:00", repository=repository + "-elsewhere"),
    ]
    _write_history(state, targeted_pair + far_starts)
    code, out, _ = _slips(capsys)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 0" in out, out
    assert "history note: a second start for run far" in out, out

    # Complete readable evidence with zero slips: the observed absence counts.
    # A red targeted check is a complete observation, so the red full run of the
    # same identity has no green predecessor — and zero is the complete finding.
    _write_history(state, _slip_events(repository, targeted_verdict="red"))
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 0; incomplete/not countable runs: 0" in out, out
    assert "evidence partial" not in out, out


def test_slips_are_read_only_and_preserve_duration_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Repeated reads never mutate the history, and legacy records stay readable as durations.

    Fault this pins: reporting writing history, repeated reporting differing on
    unchanged input, or legacy duration reporting breaking.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    events = [
        # A legacy green full run: still a duration record, never an inferred slip.
        _run_start("old", utc="2026-11-13T07:00:00+00:00", repository=repository),
        _run_end("old", utc="2026-11-13T07:30:00+00:00", verdict="green", seconds=42.0),
        # One qualifying pair.
        *_slip_events(repository),
    ]
    path = _write_history(tmp_path / "state", events)
    original = path.read_text(encoding="utf-8")

    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert path.read_text(encoding="utf-8") == original, "reporting wrote to the history"

    code_again, out_again, _ = _slips(capsys)
    assert code_again == code and out_again == out, "repeated reporting differed on unchanged input"
    assert path.read_text(encoding="utf-8") == original

    # The duration reader keeps its behavior over the same, unchanged history.
    code, listed, _ = _run(capsys, "report")
    assert code == 0, listed
    assert "run old" in listed and "42.000s" in listed and "green" in listed, listed
    assert "run f-1" in listed and "red" in listed, listed
    assert path.read_text(encoding="utf-8") == original


def test_slips_pair_one_repository_under_two_spellings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A targeted check and a full run of one repository pair even when its path is spelled twice.

    Fault this pins (loop rows L1-1, L1-11): scope resolved the recorded path
    while pairing compared the raw strings, so a symlinked spelling of the same
    worktree stayed in scope, never paired, and the report read a complete zero.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    alias = tmp_path / "alias"
    alias.symlink_to(repository)
    events = _slip_events(repository)
    events[2]["repository"] = str(alias)  # the full run recorded under the symlinked spelling
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys)
    assert "slips: 1; incomplete/not countable runs: 0" in out and code == 0, out


@pytest.mark.parametrize("verdict", ["green", "red"])
def test_slips_diagnose_an_unknown_check_kind(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], verdict: str
) -> None:
    """A run naming a check kind outside the known ones is unsupported evidence, never a clean run.

    Fault this pins (loop row L1-8): an unknown kind was routed into the full
    branch, where a green verdict passed as a complete observation with exit 0.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository, full_kind="nightly", full_verdict=verdict)
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys)
    assert "slips: 0; incomplete/not countable runs: 1" in out and code == 1, out


def test_environment_cannot_mint_a_targeted_start(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An exported kind `targeted` never reaches a shell-started record as a targeted start.

    Fault this pins (loop row L1-9): the comment above `CHECK_KINDS` promised
    that only `begin_targeted_run` writes `targeted`, but the environment path
    accepted it.
    """
    monkeypatch.setenv(verify_duration.KIND_ENV, "targeted")
    monkeypatch.setenv(verify_duration.CHANGE_ENV, "demo")
    monkeypatch.setenv(verify_duration.TREE_ENV, TREE)
    code, _, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    start = next(e for e in _history(verify_lock.state_root().parent) if e["event"] == "run_start")
    assert start["check_kind"] is None, start
