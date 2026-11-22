"""The measured verification durations: clock arithmetic, history, reader, refusals.

`scripts.verify_duration` appends one JSON line per event to a local history
and reads it back without ever repairing it. Every case here builds its own
state root and never touches the real machine's verification history; each
docstring names the fault it was written against — planting it turned exactly
this test red.
"""

from __future__ import annotations

import datetime
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

    def fake_git(arguments: list[str], cwd: Path | None = None) -> str | None:  # noqa: ARG001 - the real `_git` binds a checkout
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
        "common_git_dir": str(Path(repository) / ".git"),
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
        record.update({"check_kind": kind, "change": change, "tree_id": tree, "comparison_version": 2})
    return record


def _run_end(run_id: str, *, utc: str, verdict: str = "green", seconds: float = 1.0, tree: str | None = None) -> dict:
    """A version-1 end record; `tree` is the post-execution identity of a targeted completion."""
    end = {"v": 1, "event": "run_end", "run_id": run_id, "utc": utc, "seconds": seconds, "verdict": verdict}
    if tree is not None:
        end["tree_id"] = tree
    return end


def _write_history(state: Path, events: list[dict], *, targeted_file: bool = True) -> Path:
    """The given records as the two history files, without going through any writer.

    A run whose start names the kind `targeted` and every row of it go to the
    targeted history; everything else goes to the duration history. A row may
    name its file with `_file`. Returns the duration history's path.
    """
    root = state / "coding-harness"
    root.mkdir(parents=True, exist_ok=True)
    targeted_ids = set()
    for event in events:
        if event.get("event") == "run_start" and event.get("check_kind") == "targeted":
            targeted_ids.add(event["run_id"])
    duration_rows: list[dict] = []
    targeted_rows: list[dict] = []
    for event in events:
        row = {key: value for key, value in event.items() if key != "_file"}
        destination = event.get("_file") or ("targeted" if event.get("run_id") in targeted_ids else "duration")
        (targeted_rows if destination == "targeted" else duration_rows).append(row)
    path = root / verify_duration.HISTORY_NAME
    path.write_text("".join(json.dumps(row) + "\n" for row in duration_rows), encoding="utf-8")
    targeted_path = root / verify_duration.TARGETED_HISTORY_NAME
    if targeted_file:
        targeted_path.write_text("".join(json.dumps(row) + "\n" for row in targeted_rows), encoding="utf-8")
    else:
        targeted_path.unlink(missing_ok=True)
    return path


def _check(
    run_id: str,
    kind: str,
    start: str,
    end: str,
    verdict: str,
    repository: str,
    *,
    change: str | None = "demo",
    tree: str | None = TREE,
    end_tree: str | None = None,
    config: str | None = CONFIG,
) -> list[dict]:
    """One run's start and end records; a targeted end carries its own tree reading."""
    finish = tree if end_tree is None and kind == "targeted" else end_tree
    return [
        _run_start(run_id, utc=start, repository=repository, kind=kind, change=change, tree=tree, config=config),
        _run_end(run_id, utc=end, verdict=verdict, tree=finish),
    ]


def _measured_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """A repository directory the reader runs in, so records of it are in scope by default."""
    repo = tmp_path / "repo"
    repo.mkdir()
    monkeypatch.chdir(repo)
    monkeypatch.setattr(verify_duration, "_common_git_dir", lambda _root=None: str(repo / ".git"), raising=False)
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
        _run_end(
            full_id,
            utc=(datetime.datetime.fromisoformat(full_utc) + datetime.timedelta(minutes=30)).isoformat(),
            verdict=full_verdict,
        ),
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
        # Two distinct green targeted predecessors of the same identity (equal
        # completions of interchangeable checks), then the red full run that
        # missed both — plus its start row written twice, as a retried append
        # leaves it.
        *_slip_events(repository, targeted_id="t-1", targeted_end="2026-11-13T09:05:00+00:00"),
        *_slip_events(repository, targeted_id="t-2", full_id="f-1"),
    ]
    duplicate = dict(events[2])  # f-1's start row again, dict-equal — a retried append, not a conflict
    events.append(duplicate)
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys)
    assert code == 1, out
    assert "slips: 0; incomplete/not countable runs: 3" in out, out
    assert f"repository {repository}/.git" in out and "change all" in out, out
    # Reading twice reports the same count from the same bytes.
    code_again, out_again, _ = _slips(capsys)
    assert code_again == 1 and out_again == out, out_again


def test_slips_pair_overlapping_checks_by_completion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository, targeted_end="2026-11-13T10:00:00+00:00", full_utc="2026-11-13T09:30:00+00:00")
    events[3]["utc"] = "2026-11-13T11:00:00+00:00"
    # The full start is recorded before the targeted end in real overlapping runs.
    _write_history(tmp_path / "state", [events[2], events[0], events[1], events[3]])
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out


@pytest.mark.parametrize("field", ["tree_id", "change", "config_sha256"])
@pytest.mark.parametrize("kind,verdict", [("targeted", "red"), ("full", "green")])
def test_slips_mark_all_unknown_identities_incomplete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    field: str,
    kind: str,
    verdict: str,
) -> None:
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository)
    pair = events[:2] if kind == "targeted" else events[2:]
    pair[0][field] = None
    pair[1]["verdict"] = verdict
    _write_history(tmp_path / "state", pair)
    code, out, _ = _slips(capsys)
    if kind == "full" and field == "change":
        # A full run without a change is outside the slip population, not a gap.
        assert code == 0 and "slips: 0; incomplete/not countable runs: 0" in out, out
        assert "outside the count: 1 legacy or change-less full runs" in out, out
        return
    assert code == 1 and "slips: 0; incomplete/not countable runs: 1" in out, out
    assert "evidence partial" in out, out


@pytest.mark.parametrize(
    "case",
    [
        "targeted-red",
        "full-green",
        "fallback-masquerade",
        "reversed-order",
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
    as targeted, a reversed completion order, another repository,
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
            _run_end("f-1", utc="2026-11-13T11:30:00+00:00", verdict="red", tree=TREE),
        ]
    elif case == "reversed-order":
        events = _slip_events(repository, full_utc="2026-11-13T08:00:00+00:00")
    elif case == "other-tree":
        events = _slip_events(repository, tree="t2" * 20, full_tree=TREE)
    elif case == "other-change":
        events = _slip_events(repository, change="other", full_change="demo")
    elif case == "other-config":
        events = _slip_events(repository, config="d2" * 32, full_config=CONFIG)
    elif case == "other-repository":
        # The green predecessor is another repository's; the red full run is ours.
        elsewhere = _slip_events(repository + "-elsewhere")
        events = elsewhere[:2] + _slip_events(repository)[2:]
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
    elif case == "legacy-predecessor":
        # A legacy run is outside the slip population: no gap, and no predecessor.
        assert "incomplete/not countable runs: 0" in out and code == 0, (case, out)
        assert "outside the count: 1 legacy or change-less full runs" in out, (case, out)
    else:
        assert "incomplete/not countable runs: 0" in out and code == 0, (case, out)


@pytest.mark.parametrize(
    "case",
    [
        "lost-end",
        "conflicting-ends",
        "conflicting-starts",
        "missing-comparison",
        "legacy-lost-end",
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
            # and the red full run beside it cannot be paired or called a non-slip:
            # both are incomplete.
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
            _run_end("f-1", utc="2026-11-13T11:30:00+00:00", verdict="red", tree=TREE),
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
            _run_end("f-1", utc="2026-11-13T11:30:00+00:00", verdict="red", tree=TREE),
        ]
    elif case == "missing-comparison":
        events = _slip_events(repository)[:2] + [
            _run_start(
                "f-1",
                utc="2026-11-13T11:00:00+00:00",
                repository=repository,
                kind="full",
                change="demo",
                tree=None,
                config=None,
            ),
            _run_end("f-1", utc="2026-11-13T11:30:00+00:00", verdict="red", tree=TREE),
        ]
    else:  # legacy-lost-end
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
            # A legacy full run whose end never arrived: one gap, never a pairing partner.
            _run_start("f-1", utc="2026-11-13T11:00:00+00:00", repository=repository),
        ]
    _write_history(tmp_path / "state", events)

    # A potentially matching pair with a gap on either side is incomplete on both sides, once each.
    expected = 0 if case == "legacy-lost-end" else 2
    code, out, _ = _slips(capsys)
    assert code == (0 if case == "legacy-lost-end" else 1), (case, out)
    assert f"slips: 0; incomplete/not countable runs: {expected}" in out, (case, out)
    assert ("evidence partial" in out) == (case != "legacy-lost-end"), (case, out)
    # The damaged runs keep their diagnosis, named and visible.
    if case in ("conflicting-ends", "conflicting-starts"):
        assert "history note:" in out, (case, out)


@pytest.mark.parametrize("run_index", [0, 2], ids=["targeted", "full"])
@pytest.mark.parametrize("verdict", ["green", "red"])
def test_slips_reject_completion_before_own_start(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], run_index: int, verdict: str
) -> None:
    """Plant an end before its own start: neither verdict may hide the incomplete run or pair it."""
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository)
    events[run_index + 1]["utc"] = "2026-11-13T08:00:00+00:00"
    events[run_index + 1]["verdict"] = verdict
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys)
    assert code == 1, out
    # The broken run and its potential partner are each incomplete once.
    assert "slips: 0; incomplete/not countable runs: 2" in out, out


@pytest.mark.parametrize("field", ["tree_id", "change", "config_sha256"])
@pytest.mark.parametrize("value", [None, "", "   "])
@pytest.mark.parametrize("run_indices", [(0,), (2,), (0, 2)], ids=["targeted", "full", "both"])
def test_slips_reject_unknown_comparison_identities(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    field: str,
    value: str | None,
    run_indices: tuple[int, ...],
) -> None:
    """Plant absent or blank identities: they stay visibly uncountable, even when equal.

    An unknown identity on either side leaves the pair undecidable, so the
    broken run and its potential partner are each incomplete once. The one
    exception is a full run without a change: it is outside the slip population.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository)
    for index in run_indices:
        events[index][field] = value
        if index == 0 and field == "tree_id":
            events[1][field] = value
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys)
    if field == "change" and 2 in run_indices:
        expected = 1 if 0 in run_indices else 0
        assert f"slips: 0; incomplete/not countable runs: {expected}" in out, out
        assert "outside the count: 1 legacy or change-less full runs" in out, out
        assert code == (1 if expected else 0), out
        return
    assert code == 1, out
    assert "slips: 0; incomplete/not countable runs: 2" in out, out


def test_unknown_targeted_change_is_unassignable_in_change_scope(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository, change="alpha", full_verdict="green")
    events[0]["change"] = None
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys, "--change", "alpha")
    assert code == 1, out
    assert "run t-1 cannot be assigned" in out and "change" in out, out
    assert "evidence partial" in out, out

    code, out, _ = _slips(capsys, "--change", "alpha", "--since", "2026-11-13T10:00:00+00:00")
    assert code == 0, out
    assert "run t-1 cannot be assigned" not in out, out


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
            change="gamma",
            tree=TREE,
            config=CONFIG,
        ),
    ]
    _write_history(tmp_path / "state", events)

    window = ("--since", "2026-11-13T10:00:00+00:00", "--until", "2026-11-13T14:00:00+00:00")
    code, out, _ = _slips(capsys, *window)
    assert code == 0, out
    assert "slips: 1; incomplete/not countable runs: 0" in out, out
    assert f"repository {repository}/.git" in out, out

    code, out, _ = _slips(capsys, *window, "--change", "beta")
    assert code == 0 and "slips: 0; incomplete/not countable runs: 0" in out, out

    # Without the window the late alpha run without an end is the one gap; the
    # gamma check is another change's and never a candidate.
    code, out, _ = _slips(capsys, "--change", "alpha")
    assert code == 1 and "slips: 1; incomplete/not countable runs: 1" in out, out

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
    assert "history note: line 1" in out, out

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

    # An empty selection — a misspelled change, another checkout, a window
    # with no runs — selects nothing to observe: no statement, never a bare
    # zero and never a complete success (maintainer, 2026-11-15; loop row L2-1).
    for empty in (("--change", "dmeo"), ("--since", "2026-11-14T00:00:00+00:00")):
        code, out, _ = _slips(capsys, *empty)
        assert code == 1, (empty, out)
        assert "0 runs selected, no statement possible" in out, (empty, out)
        assert "slips: 0" not in out, (empty, out)


@pytest.mark.parametrize("damaged_line", [0, 1, 2])
def test_slips_preserve_observations_beside_invalid_utf8(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], damaged_line: int
) -> None:
    """A damaged byte line must not hide valid runs before or after it."""
    repository = _measured_repo(tmp_path, monkeypatch)
    path = _write_history(tmp_path / "state", _slip_events(repository))
    lines = path.read_bytes().splitlines(keepends=True)
    lines.insert(damaged_line, b"\xff\n")
    original = b"".join(lines)
    path.write_bytes(original)

    try:
        code, out, err = _slips(capsys)
    except UnicodeDecodeError:
        pytest.fail("invalid UTF-8 must leave valid observations visible in a partial report")

    assert code == 1, (out, err)
    assert "slips: 1; incomplete/not countable runs: 0" in out, out
    assert f"history note: line {damaged_line + 1}: not valid UTF-8" in out, out
    assert "evidence partial" in out, out
    assert path.read_bytes() == original


@pytest.mark.parametrize("instant", ["0001-01-01T00:00:00+01:00", "9999-12-31T23:59:59-01:00"])
def test_slips_preserve_observations_beside_overflowing_timestamp(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], instant: str
) -> None:
    """A damaged run whose UTC conversion overflows must not abort valid observations."""
    repository = _measured_repo(tmp_path, monkeypatch)
    path = _write_history(
        tmp_path / "state",
        [*_slip_events(repository), _run_start("damaged", utc=instant, repository=repository)],
    )
    original = path.read_bytes()

    try:
        code, out, err = _slips(capsys)
    except OverflowError:
        pytest.fail("an unrepresentable UTC instant must leave valid observations visible in a partial report")

    assert code == 1, (out, err)
    assert "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "invalid run_start fields: utc for run damaged" in out, out
    assert "evidence partial" in out, out
    assert path.read_bytes() == original


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
    # The legacy run is outside the count — a complete observation, no gap.
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "outside the count: 1 legacy or change-less full runs" in out, out
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


@pytest.mark.parametrize("kind", ["nightly", "full-fallback"])
@pytest.mark.parametrize("verdict", ["green", "red"])
def test_slips_diagnose_an_unknown_check_kind(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], verdict: str, kind: str
) -> None:
    """A run naming a check kind outside the known ones is unsupported evidence, never a clean run.

    Fault this pins (loop row L1-8): an unknown kind was routed into the full
    branch, where a green verdict passed as a complete observation with exit 0.
    `full-fallback` is no kind of this change (loop row L4-2): no code writes
    it, and a distinct fallback kind is follow-up work (bead coding-harness-rodx),
    so a record naming it is read as unknown, not as a comparable full run.
    """
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository, full_kind=kind, full_verdict=verdict)
    _write_history(tmp_path / "state", events)

    code, out, _ = _slips(capsys)
    assert "slips: 0; incomplete/not countable runs: 1" in out and code == 1, out


def test_environment_cannot_mint_a_targeted_start(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An exported kind `targeted` never reaches a shell-started record as a targeted start.

    Fault this pins (loop row L1-9): the comment above `CHECK_KINDS` promised
    that only `begin_targeted_run` writes `targeted`, but the environment path
    accepted it. Since loop row L4-1 the record keeps the refused value marked
    as unrecognised instead of the null a legacy record reads as; the
    guarantee is the same: no known kind, and never `targeted`.
    """
    monkeypatch.setenv(verify_duration.KIND_ENV, "targeted")
    monkeypatch.setenv(verify_duration.CHANGE_ENV, "demo")
    monkeypatch.setenv(verify_duration.TREE_ENV, TREE)
    code, _, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    start = next(e for e in _history(verify_lock.state_root().parent) if e["event"] == "run_start")
    kind = start["check_kind"]
    assert kind is not None and kind != "targeted" and kind not in verify_duration.CHECK_KINDS, start


@pytest.mark.parametrize("kind", ["nightly", "targeted", "full-fallback"])
def test_an_unrecognised_environment_kind_is_diagnosed_by_the_reader(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], kind: str
) -> None:
    """A start launched with an unrecognised kind is read as not countable, never as a legacy clean run.

    Fault this pins (loop row L4-1): `_comparison_fields` mapped an unknown
    environment kind to null, the value a legacy record carries, so the
    reader's unknown-kind diagnosis could never fire for it and a green run
    passed as a complete observation of zero slips with exit 0.
    """
    _measured_repo(tmp_path, monkeypatch)
    monkeypatch.setenv(verify_duration.KIND_ENV, kind)
    monkeypatch.setenv(verify_duration.CHANGE_ENV, "demo")
    monkeypatch.setenv(verify_duration.TREE_ENV, TREE)
    code, run_id, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0
    code, _, _ = _run(capsys, "end", "--run", run_id.strip(), "--start", "0.0", "--end", "1.0", "--verdict", "green")
    assert code == 0
    for name in (verify_duration.KIND_ENV, verify_duration.CHANGE_ENV, verify_duration.TREE_ENV):
        monkeypatch.delenv(name)
    # The start carries the version-2 marker, so the targeted history must exist for a measurement.
    (verify_lock.state_root() / verify_duration.TARGETED_HISTORY_NAME).write_text("", encoding="utf-8")

    code, out, _ = _slips(capsys)
    assert "slips: 0; incomplete/not countable runs: 1" in out and code == 1, out


def test_slips_pair_worktrees_by_recorded_common_git_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Different worktrees of the same Git repository share a recorded identity."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    common = str((repo / ".git").resolve())
    monkeypatch.chdir(repo)
    (repo / "decisions").mkdir()
    (repo / "decisions" / "gates.yaml").write_text("gates: []\n", encoding="utf-8")
    receipt = verify_duration.begin_targeted_run(repo, "demo", TREE)
    verify_duration.finish_targeted_run(receipt, TREE, "green")
    targeted_path = tmp_path / "state" / "coding-harness" / verify_duration.TARGETED_HISTORY_NAME
    events = [json.loads(line) for line in targeted_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert events[0].get("common_git_dir") == common
    events[0]["utc"] = "2026-11-13T09:00:00+00:00"
    events[1]["utc"] = "2026-11-13T09:05:00+00:00"
    events[0]["repository"] = str(tmp_path / "removed-worktree")
    full = _slip_events(str(repo))[2:]
    full[0]["common_git_dir"] = common
    full[0]["config_sha256"] = events[0]["config_sha256"]
    events.extend(full)
    # Old records of unknown repository: legacy shape, no common Git directory.
    legacy = _slip_events(str(repo), targeted_id="old-t", full_id="old-f")
    for event in legacy:
        for name in ("common_git_dir", "check_kind", "change", "tree_id", "comparison_version"):
            event.pop(name, None)
    events.extend(legacy)
    _write_history(tmp_path / "state", events)
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "unattributed outside runs: 2" in out, out


def test_slips_reject_unstable_red_targeted_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A red targeted check with a changed tree is incomplete once, not a clean observation."""
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository, targeted_verdict="red")[:2]
    events[1]["tree_id"] = "changed"
    _write_history(tmp_path / "state", events)
    code, out, _ = _slips(capsys)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 1" in out, out


# ---------------------------------------------------------------------------
# Slips — immediate succession, potential pairs, outside runs, two histories
# ---------------------------------------------------------------------------


def _at(clock: str) -> str:
    """One UTC instant of the test day, from `HH:MM`."""
    return f"2026-11-13T{clock}:00+00:00"


def _slips_of(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    build,
    *argv: str,
) -> tuple[int, str]:
    """Write the history `build(repository)` returns and read it with `slips`."""
    repository = _measured_repo(tmp_path, monkeypatch)
    _write_history(tmp_path / "state", build(repository))
    code, out, _ = _slips(capsys, *argv)
    return code, out


def test_slips_count_only_immediate_successor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 1. Fault this pins: a repeated red full run counts as a slip again.

    Only the red full run that immediately follows the green targeted check
    counts; later red runs of the same identity answer a full check, not it.
    """

    def build(repository: str) -> list[dict]:
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            *_check("f-1", "full", _at("11:00"), _at("11:30"), "red", repository),
            *_check("f-2", "full", _at("12:00"), _at("12:30"), "red", repository),
            *_check("f-3", "full", _at("13:00"), _at("13:30"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "flaky-test signals" not in out, out


def test_slips_intervening_check_ends_pairing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 2. Fault this pins: an earlier targeted green pairs across a later same-identity check."""
    repository = _measured_repo(tmp_path, monkeypatch)
    state = tmp_path / "state"
    # A targeted red completes between the targeted green and the full red.
    _write_history(
        state,
        [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            *_check("t-2", "targeted", _at("09:10"), _at("09:15"), "red", repository),
            *_check("f-1", "full", _at("11:00"), _at("11:30"), "red", repository),
        ],
    )
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 0; incomplete/not countable runs: 0" in out, out
    # A full green completes between them: the full red answers it, not the targeted check.
    _write_history(
        state,
        [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            *_check("f-1", "full", _at("10:00"), _at("10:30"), "green", repository),
            *_check("f-2", "full", _at("11:00"), _at("11:30"), "red", repository),
        ],
    )
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 0; incomplete/not countable runs: 0" in out, out


def test_slips_report_consecutive_full_flaky_signal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 3. Fault this pins: a full green then full red of one identity lacks its separate signal,
    or an intervening same-identity check still yields one."""
    repository = _measured_repo(tmp_path, monkeypatch)
    state = tmp_path / "state"
    _write_history(
        state,
        [
            *_check("f-1", "full", _at("10:00"), _at("10:30"), "green", repository),
            *_check("f-2", "full", _at("11:00"), _at("11:30"), "red", repository),
        ],
    )
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 0; incomplete/not countable runs: 0" in out, out
    assert "flaky-test signals: 1; undecided flaky-test signals: 0" in out, out
    # A targeted green between them: the red answers it as a slip, and no signal is reported.
    _write_history(
        state,
        [
            *_check("f-1", "full", _at("10:00"), _at("10:30"), "green", repository),
            *_check("t-1", "targeted", _at("10:35"), _at("10:40"), "green", repository),
            *_check("f-2", "full", _at("11:00"), _at("11:30"), "red", repository),
        ],
    )
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "flaky-test signals" not in out, out


def test_slips_incomplete_candidate_marks_both_sides(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 7. Fault this pins: a complete red full run whose only possible targeted predecessor
    has conflicting completions is reported as a non-slip."""

    def build(repository: str) -> list[dict]:
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            _run_end("t-1", utc=_at("09:06"), verdict="red", tree=TREE),
            *_check("f-1", "full", _at("11:00"), _at("11:30"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 2" in out, out
    assert "a second end for run t-1" in out, out


def test_slips_report_legacy_and_changeless_outside_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 9. Fault this pins: an excluded run becomes incomplete or vanishes from the outside line."""
    repository = _measured_repo(tmp_path, monkeypatch)
    ghost = [
        _run_start("ghost", utc=_at("05:00"), repository=repository),
        _run_end("ghost", utc=_at("05:10"), verdict="green"),
    ]
    for event in ghost:
        event.pop("common_git_dir", None)  # a legacy run that names no repository
    _write_history(
        tmp_path / "state",
        [
            _run_start("old", utc=_at("06:00"), repository=repository),
            _run_end("old", utc=_at("06:10"), verdict="red"),
            *_check("cl", "full", _at("07:00"), _at("07:10"), "red", repository, change=None),
            *ghost,
            *_slip_events(repository),
        ],
    )
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "outside the count: 2 legacy or change-less full runs; unattributed outside runs: 1" in out, out
    # A change scope still reports excluded runs attributable to this repository.
    code, out, _ = _slips(capsys, "--change", "demo")
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert (
        "outside the count: 2 legacy or change-less full runs (not change-scoped); unattributed outside runs: 1" in out
    ), out


def test_change_scope_with_only_outside_runs_has_no_measurement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Outside runs cannot turn an unmatched change into a measured zero."""
    repository = _measured_repo(tmp_path, monkeypatch)
    _write_history(
        tmp_path / "state",
        [*_check("cl", "full", _at("07:00"), _at("07:10"), "red", repository, change=None)],
    )
    code, out, _ = _slips(capsys, "--change", "missing")
    assert code == 1, out
    assert "0 runs selected, no statement possible" in out, out
    assert "slips: 0" not in out, out


def test_empty_selection_reports_attributable_outside_runs(tmp_path, monkeypatch, capsys):
    repository = _measured_repo(tmp_path, monkeypatch)
    _write_history(
        tmp_path / "state",
        _check("cl", "full", _at("07:00"), _at("07:10"), "red", repository, change=None),
    )
    code, out, _ = _slips(capsys, "--change", "missing")
    assert code == 1 and "0 runs selected, no statement possible" in out, out
    assert "outside the count: 1 legacy or change-less full runs" in out, out


@pytest.mark.parametrize("cause", ["conflicting-ends", "unknown-tree"])
def test_uncertain_full_after_green_without_targeted_is_undecided(tmp_path, monkeypatch, capsys, cause):
    def build(repository):
        middle = _check(
            "uncertain",
            "full",
            _at("10:00"),
            _at("10:30"),
            "green",
            repository,
            tree=None if cause == "unknown-tree" else TREE,
        )
        if cause == "conflicting-ends":
            middle.append(_run_end("uncertain", utc=_at("10:31"), verdict="red"))
        return [
            *_check("green", "full", _at("09:00"), _at("09:30"), "green", repository),
            *middle,
            *_check("red", "full", _at("11:00"), _at("11:30"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 1" in out, out
    assert "flaky-test signals: 0; undecided flaky-test signals: 1" in out, out


def test_old_duration_reader_accepts_additive_version_one_fields(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 11. Fault this pins: an older reader rejects the new full-run records, or the
    duration report counts a targeted check as a full run."""
    repository = _measured_repo(tmp_path, monkeypatch)
    state = tmp_path / "state"
    _write_history(state, _slip_events(repository))
    rows = _history(state)
    assert all(row["v"] == 1 for row in rows), rows
    assert any(row.get("comparison_version") == 2 for row in rows), rows
    original = (state / "coding-harness" / verify_duration.HISTORY_NAME).read_bytes()
    code, out, _ = _run(capsys, "report")
    assert code == 0 and "run f-1" in out and "red" in out, out
    assert "run t-1" not in out and "history note" not in out, out
    assert (state / "coding-harness" / verify_duration.HISTORY_NAME).read_bytes() == original


def test_flaky_signal_undecided_after_conflicting_full(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 12. Fault this pins: the later full run becomes incomplete, or its signal is decided."""

    def build(repository: str) -> list[dict]:
        return [
            *_check("f-1", "full", _at("10:00"), _at("10:30"), "green", repository),
            _run_end("f-1", utc=_at("10:31"), verdict="red"),
            *_check("f-2", "full", _at("11:00"), _at("11:30"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 1" in out, out
    assert "flaky-test signals: 0; undecided flaky-test signals: 1" in out, out


def test_equal_completion_times_are_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 13. Fault this pins: a targeted green and a full red completing together are a complete non-slip."""

    def build(repository: str) -> list[dict]:
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            *_check("f-1", "full", _at("08:35"), _at("09:05"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 2" in out, out


def test_orphan_full_end_respects_comparison_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 14. Fault this pins: an orphan after the marker reads as legacy, one before it makes
    the report partial, or a legacy pair after the marker does."""
    repository = _measured_repo(tmp_path, monkeypatch)
    state = tmp_path / "state"
    # Before the first version-2 comparison record: legacy, outside the count.
    _write_history(
        state,
        [
            _run_end("lost-1", utc=_at("06:00"), verdict="red"),
            _run_start("old", utc=_at("07:00"), repository=repository),
            _run_end("old", utc=_at("07:10"), verdict="green"),
            *_slip_events(repository),
        ],
    )
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "outside the count: 1 legacy or change-less full runs; unattributed outside runs: 1" in out, out
    # After the marker: damaged evidence, the report is partial.
    _write_history(
        state,
        [
            *_slip_events(repository),
            _run_end("lost-2", utc=_at("12:00"), verdict="red"),
            *_check("h-1", "full", _at("13:00"), _at("13:10"), "green", repository),
        ],
    )
    code, out, _ = _slips(capsys)
    assert code == 1 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "history note: line with run_end for unknown run lost-2" in out, out
    # An end that completed before the lower bound cannot belong to this selection.
    code, out, _ = _slips(capsys, "--since", "2026-11-13T12:30:00+00:00")
    assert code == 0 and "slips: 0; incomplete/not countable runs: 0" in out, out
    assert "lost-2" not in out, out


def test_legacy_orphan_outside_count_respects_interval(tmp_path, monkeypatch, capsys):
    """A pre-marker orphan is counted only within the requested completion interval."""
    repository = _measured_repo(tmp_path, monkeypatch)
    _write_history(
        tmp_path / "state",
        [
            _run_end("lost", utc=_at("06:00")),
            *_slip_events(repository),
        ],
    )
    _, out, _ = _slips(capsys, "--since", "2026-11-13T06:00:00+00:00")
    assert "unattributed outside runs: 1" in out, out
    _, out, _ = _slips(capsys, "--since", "2026-11-13T06:01:00+00:00")
    assert "unattributed outside runs: 1" not in out, out
    _, out, _ = _slips(capsys, "--until", "2026-11-13T06:00:00+00:00")
    assert "unattributed outside runs: 1" not in out, out


def test_identical_completion_retry_collapses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 1. Fault this pins: a byte-identical duplicate completion prevents the pair counting once."""

    def build(repository: str) -> list[dict]:
        events = _slip_events(repository)
        return [*events, dict(events[1]), dict(events[2]), dict(events[3])]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "history note" not in out, out


def test_unstable_intervening_check_makes_candidates_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 7. Fault this pins: the reader pairs around an intervening check whose tree moved."""

    def build(repository: str) -> list[dict]:
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            *_check("t-2", "targeted", _at("09:10"), _at("09:20"), "red", repository, end_tree="moved"),
            *_check("f-1", "full", _at("11:00"), _at("11:30"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 3" in out, out


@pytest.mark.parametrize("moved", ["start", "end"])
def test_moved_targeted_predecessor_makes_pair_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], moved: str
) -> None:
    """Criterion 7. Fault this pins: a targeted predecessor whose tree moved leaves the full run a non-slip."""
    trees = {"tree": TREE, "end_tree": "moved"} if moved == "start" else {"tree": "a" * 40, "end_tree": TREE}

    def build(repository: str) -> list[dict]:
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository, **trees),
            *_check("f-1", "full", _at("11:00"), _at("11:30"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 2" in out, out


def test_moved_targeted_end_tree_is_possible_match(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 7. Fault this pins: a full run on the end tree of a moved targeted check is a non-slip."""

    def build(repository: str) -> list[dict]:
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository, tree="a" * 40, end_tree=TREE),
            *_check("f-1", "full", _at("11:00"), _at("11:30"), "red", repository, tree=TREE),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 2" in out, out


@pytest.mark.parametrize("target_tree", [TREE, "moved"])
def test_moved_full_tree_makes_pair_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], target_tree: str
) -> None:
    """A full run with differing recorded trees is uncertain on either tree."""

    def build(repository: str) -> list[dict]:
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository, tree=target_tree),
            *_check("f-1", "full", _at("11:00"), _at("11:30"), "red", repository, end_tree="moved"),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 2" in out, out


def test_incomplete_run_exits_partial(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 10. Fault this pins: an interrupted in-scope run exits as a complete measurement."""

    def build(repository: str) -> list[dict]:
        return [
            _run_start(
                "f-1", utc=_at("11:00"), repository=repository, kind="full", change="demo", tree=TREE, config=CONFIG
            ),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 1" in out, out
    assert "evidence partial" in out, out


def test_running_intervening_full_makes_pair_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 7. Fault this pins: a full run that is still running is bypassed by the pairing."""

    def build(repository: str) -> list[dict]:
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            _run_start(
                "f-run", utc=_at("10:00"), repository=repository, kind="full", change="demo", tree=TREE, config=CONFIG
            ),
            *_check("f-2", "full", _at("11:00"), _at("11:30"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 3" in out, out
    assert "flaky-test signals" not in out, out


def test_missing_one_history_is_unavailable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 10. Fault this pins: one missing history yields a complete zero."""
    repository = _measured_repo(tmp_path, monkeypatch)
    state = tmp_path / "state"
    unavailable = "slips: unavailable; incomplete/not countable runs: unavailable"
    # Version-2 evidence in the duration history, no targeted history.
    _write_history(state, _slip_events(repository), targeted_file=False)
    code, out, _ = _slips(capsys)
    assert code == 1 and unavailable in out and "slips: 0" not in out, out
    # A targeted history without a duration history.
    path = _write_history(state, _slip_events(repository))
    path.unlink()
    code, out, _ = _slips(capsys)
    assert code == 1 and unavailable in out, out
    # Only legacy duration records and no targeted history: nothing version 2 exists, the read completes.
    legacy = [
        _run_start("old", utc=_at("07:00"), repository=repository),
        _run_end("old", utc=_at("07:10"), verdict="green"),
    ]
    _write_history(state, legacy, targeted_file=False)
    code, out, _ = _slips(capsys)
    assert code == 0 and "slips: 0; incomplete/not countable runs: 0" in out, out


def test_orphan_end_affects_possible_selections_and_pairs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 10. Fault this pins: an orphan end between a targeted green and a full red leaves a slip
    counted, or a lower bound after it still reports the orphan."""
    repository = _measured_repo(tmp_path, monkeypatch)
    _write_history(
        tmp_path / "state",
        [*_slip_events(repository), _run_end("lost", utc=_at("10:15"), verdict="red")],
    )
    code, out, _ = _slips(capsys)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 2" in out, out
    assert "unknown run lost" in out, out
    # The lower bound after the orphan: the full run is still selected and still undecidable.
    code, out, _ = _slips(capsys, "--since", "2026-11-13T10:30:00+00:00")
    assert code == 1 and "slips: 0; incomplete/not countable runs: 1" in out, out
    assert "unknown run lost" not in out, out


def test_legacy_pair_after_marker_is_outside(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 9. Fault this pins: a well-formed legacy pair after a version-2 marker makes the report partial."""

    def build(repository: str) -> list[dict]:
        return [
            *_slip_events(repository),
            _run_start("old", utc=_at("13:00"), repository=repository),
            _run_end("old", utc=_at("13:10"), verdict="green"),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 0 and "slips: 1; incomplete/not countable runs: 0" in out, out
    assert "outside the count: 1 legacy or change-less full runs" in out, out


@pytest.mark.parametrize("cause", ["conflicting-ends", "unknown-tree"])
def test_uncertain_full_between_targeted_and_red(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], cause: str
) -> None:
    """Criterion 12. Fault this pins: an uncertain full run between a targeted green and a full red leaves
    a decided flaky signal or fewer than three incomplete runs."""

    def build(repository: str) -> list[dict]:
        middle = _check("f-u", "full", _at("10:00"), _at("10:30"), "green", repository)
        if cause == "unknown-tree":
            middle = _check("f-u", "full", _at("10:00"), _at("10:30"), "green", repository, tree=None)
        else:
            middle.append(_run_end("f-u", utc=_at("10:31"), verdict="red"))
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            *middle,
            *_check("f-2", "full", _at("11:00"), _at("11:30"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 3" in out, out
    assert "flaky-test signals" not in out, out


def test_tied_full_checks_after_targeted_are_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 13. Fault this pins: tied full checks after a targeted green leave a decided flaky line."""

    def build(repository: str) -> list[dict]:
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            *_check("f-1", "full", _at("10:00"), _at("11:00"), "green", repository),
            *_check("f-2", "full", _at("10:30"), _at("11:00"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 3" in out, out
    assert "flaky-test signals" not in out, out


@pytest.mark.parametrize("kind", ["unknown", "legacy", "changeless"])
def test_intervening_unusable_run_blocks_pair(tmp_path, monkeypatch, capsys, kind):
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository)
    middle = _check("middle", "full", "2026-11-13T09:10:00+00:00", "2026-11-13T09:30:00+00:00", "green", repository)
    if kind == "unknown":
        middle[0]["check_kind"] = "unrecognised:damaged"
    elif kind == "legacy":
        for field in ("check_kind", "change", "tree_id", "comparison_version"):
            middle[0].pop(field, None)
    else:
        middle[0]["change"] = None
    _write_history(tmp_path / "state", events + middle)
    code, out, _ = _slips(capsys)
    assert code == 1 and "slips: 0;" in out, out
    assert f"incomplete/not countable runs: {3 if kind == 'unknown' else 2}" in out, out


def test_tied_red_successors_do_not_double_count(tmp_path, monkeypatch, capsys):
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository)
    events += _check("second", "full", "2026-11-13T11:05:00+00:00", "2026-11-13T11:30:00+00:00", "red", repository)
    _write_history(tmp_path / "state", events)
    code, out, _ = _slips(capsys)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 3" in out, out


def test_incomplete_details_and_field_diagnosis(tmp_path, monkeypatch, capsys):
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository)
    events.pop()
    broken = _run_start(
        "broken", utc="2026-11-13T12:00:00+00:00", repository=repository, kind="full", change="demo", tree=TREE
    )
    broken["placement"] = None
    events.append(broken)
    _write_history(tmp_path / "state", events)
    code, out, _ = _slips(capsys)
    assert code == 1 and "placement" in out, out
    assert "f-1" in out and "demo" in out and "full" in out and "2026-11-13T11:00" in out, out


def test_orphan_tie_and_full_green_predecessor_are_incomplete(tmp_path, monkeypatch, capsys):
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _check("green", "full", "2026-11-13T09:00:00+00:00", "2026-11-13T09:05:00+00:00", "green", repository)
    events += _check("red", "full", "2026-11-13T10:00:00+00:00", "2026-11-13T10:30:00+00:00", "red", repository)
    events += [_run_end("orphan", utc="2026-11-13T09:05:00+00:00") | {"_file": "targeted"}]
    _write_history(tmp_path / "state", events)
    code, out, _ = _slips(capsys)
    assert code == 1 and "incomplete/not countable runs: 2" in out, out
    assert "flaky-test signals: 1" not in out, out


def test_uncertain_targeted_between_full_checks_marks_predecessor(tmp_path, monkeypatch, capsys):
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _check("green", "full", "2026-11-13T09:00:00+00:00", "2026-11-13T09:05:00+00:00", "green", repository)
    events += _check("red", "full", "2026-11-13T10:00:00+00:00", "2026-11-13T10:30:00+00:00", "red", repository)
    events += [_run_end("orphan", utc="2026-11-13T09:30:00+00:00") | {"_file": "targeted"}]
    _write_history(tmp_path / "state", events)
    code, out, _ = _slips(capsys)
    assert code == 1 and "incomplete/not countable runs: 2" in out, out


def test_full_writer_creates_targeted_history(monkeypatch, capsys):
    """A first version-2 full record establishes both histories without truncating either."""
    monkeypatch.setenv(verify_duration.KIND_ENV, "full")
    monkeypatch.setenv(verify_duration.CHANGE_ENV, "demo")
    monkeypatch.setenv(verify_duration.TREE_ENV, TREE)
    code, _, err = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0, err
    path = verify_duration.targeted_history_path()
    assert path.exists() and path.read_bytes() == b""
    path.write_text("existing evidence\n")
    code, _, err = _run(capsys, "start", "--job", "verify", "--placement", "local")
    assert code == 0 and path.read_text() == "existing evidence\n", err


def test_change_outside_count_is_labelled_not_scoped(tmp_path, monkeypatch, capsys):
    repository = _measured_repo(tmp_path, monkeypatch)
    _write_history(
        tmp_path / "state",
        [*_check("old", "full", _at("07:00"), _at("07:10"), "red", repository, change=None), *_slip_events(repository)],
    )
    code, out, _ = _slips(capsys, "--change", "demo")
    assert code == 0 and "not change-scoped" in out, out


def test_unattributed_legacy_obeys_interval(tmp_path, monkeypatch, capsys):
    repository = _measured_repo(tmp_path, monkeypatch)
    ghost = _run_start("ghost", utc=_at("05:00"), repository=repository)
    ghost.pop("common_git_dir")
    _write_history(tmp_path / "state", [ghost, _run_end("ghost", utc=_at("05:10")), *_slip_events(repository)])
    code, out, _ = _slips(capsys, "--since", _at("06:00"))
    assert code == 0 and "unattributed outside runs: 1" not in out, out
    code, out, _ = _slips(capsys, "--until", _at("05:00"))
    assert "unattributed outside runs: 1" not in out, out
    code, out, _ = _slips(capsys, "--since", _at("05:00"))
    assert code == 0 and "unattributed outside runs: 1" in out, out


def test_decided_red_predecessor_is_not_incomplete(tmp_path, monkeypatch, capsys):
    repository = _measured_repo(tmp_path, monkeypatch)
    for first_kind in ("full", "targeted"):
        events = _check("first", first_kind, _at("08:00"), _at("08:30"), "green", repository)
        events += _check("decided", "full", _at("09:00"), _at("10:00"), "red", repository)
        events += _check("moved", "targeted", _at("10:15"), _at("10:45"), "green", repository, end_tree="other")
        events += _check("later", "full", _at("10:50"), _at("11:00"), "red", repository)
        _write_history(tmp_path / "state", events)
        code, out, _ = _slips(capsys)
        assert code == 1 and "incomplete/not countable runs: 2" in out, out
        assert "incomplete run: decided " not in out, out
        assert ("flaky-test signals: 1" if first_kind == "full" else "slips: 1") in out, out


def test_unused_measurement_fields_are_absent():
    assert "extra_incomplete" not in verify_duration._Tally.__dataclass_fields__
    assert "tree" not in verify_duration.TargetedRun.__dataclass_fields__


def test_damaged_legacy_run_is_not_selected_or_outside(tmp_path, monkeypatch, capsys):
    repository = _measured_repo(tmp_path, monkeypatch)
    events = [
        _run_start("bad", utc=_at("09:00"), repository=repository),
        _run_end("bad", utc=_at("09:10"), verdict="invalid"),
    ]
    _write_history(tmp_path / "state", events)
    code, out, _ = _slips(capsys)
    assert code == 1 and "0 runs selected, no statement possible" in out, out
    assert "outside the count:" not in out, out


def test_unavailable_repository_scope_is_named(tmp_path, monkeypatch, capsys):
    _measured_repo(tmp_path, monkeypatch)
    monkeypatch.setattr(verify_duration, "_common_git_dir", lambda _root=None: None)
    _write_history(tmp_path / "state", [])
    code, out, _ = _slips(capsys)
    assert code == 1 and "repository unavailable" in out, out


def test_conflicting_starts_preserve_possible_intervening_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def build(repository: str) -> list[dict]:
        first = _check("t-2", "targeted", _at("09:10"), _at("09:20"), "red", repository, tree="other")
        alternate = {**first[0], "tree_id": TREE}
        return [
            *_check("t-1", "targeted", _at("09:00"), _at("09:05"), "green", repository),
            first[0],
            alternate,
            first[1],
            *_check("f-1", "full", _at("11:00"), _at("11:30"), "red", repository),
        ]

    code, out = _slips_of(tmp_path, monkeypatch, capsys, build)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 3" in out, out


@pytest.mark.parametrize("index", [0, 1, 2, 3])
def test_byte_distinct_duplicate_records_are_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], index: int
) -> None:
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    repository = _measured_repo(tmp_path, monkeypatch)
    events = _slip_events(repository)
    path = _write_history(tmp_path / "state", events)
    if index < 2:
        path = path.parent / verify_duration.TARGETED_HISTORY_NAME
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(events[index], separators=(",", ":")) + "\n")
    code, out, _ = _slips(capsys)
    assert code == 1 and "slips: 0; incomplete/not countable runs: 2" in out, out


# ---------------------------------------------------------------------------
# Criterion 8 — the completion context of a cheap-before-admission run
# ---------------------------------------------------------------------------


def test_completion_context_is_additive_and_old_history_reads(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Old records still read; a completion block speaks for the whole run or is refused wholesale.

    Planted fault: the additive completion fields rejected as an unknown
    version, an old start-only record failing to read, the reader preferring
    the stale start context over the final one, a cheap-only run shown with a
    fabricated wait, or a half-present block accepted as valid.
    """
    state = tmp_path / "state"
    monkeypatch.setenv(verify_lock.ADMISSION_ID_ENV, "start-env")
    monkeypatch.setenv(verify_lock.ADMISSION_WAIT_ENV, "7.5")

    # An old record: the completion carries no admission fields, the start's
    # context decides, and the reader shows it exactly as before.
    code, out, _ = _run(capsys, "start")
    old_id = out.strip()
    code, out, _ = _run(capsys, "end", "--run", old_id, "--start", "10.0", "--end", "13.5", "--verdict", "green")
    assert code == 0
    assert out.strip() == "execution 3.500s · admission wait 7.500s", out
    ends = [event for event in _history(state) if event["event"] == "run_end"]
    assert len(ends) == 1 and "admission_requested" not in ends[0]
    code, out, _ = _run(capsys, "report", "--run", old_id)
    assert code == 0
    assert "admission: start-env · wait: 7.5 · reused: no" in out, out
    assert "admission (final)" not in out and "final revision" not in out

    # The additive block: the final admission context wins over the stale
    # start context, and the final revision is named after a changed wait.
    code, out, _ = _run(capsys, "start")
    full_id = out.strip()
    summary = verify_duration.record_end(
        full_id,
        "green",
        segments=[(0.0, 1.0)],
        context=verify_lock.AdmissionContext("final-slot", 12.0, False),
        admission_requested=True,
        final_commit="cafe123",
        final_config="b" * 64,
    )
    assert summary == "execution 1.000s · admission wait 12.000s", summary
    code, out, _ = _run(capsys, "report", "--run", full_id)
    assert code == 0
    assert "admission (final): final-slot · wait: 12.0 · reused: no" in out, out
    assert "final revision: cafe123" in out and "b" * 64 in out
    assert "start-env" not in out, "the stale start context must not speak for the run"

    # A cheap-only completion says explicitly that no admission was requested.
    code, out, _ = _run(capsys, "start")
    cheap_id = out.strip()
    summary = verify_duration.record_end(cheap_id, "green", segments=[(0.0, 2.0)], admission_requested=False)
    assert summary == "execution 2.000s · admission wait none (no admission was requested)", summary
    code, out, _ = _run(capsys, "report", "--run", cheap_id)
    assert code == 0
    assert "admission: none (no admission was requested)" in out, out
    assert "admission (final)" not in out and "final revision" not in out
    assert "start-env" not in out

    # Half-present blocks are refused wholesale: the run keeps its start but
    # reads as incomplete, with every invalid field named.
    path = verify_duration.history_path()
    template = [event for event in _history(state) if event["event"] == "run_end"][-1]
    code, out, _ = _run(capsys, "start")
    broken_id = out.strip()
    missing = dict(template, run_id=broken_id)
    del missing["admission_reused"]
    typed = dict(template, run_id=broken_id)
    typed["admission_requested"] = "yes"
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(missing) + "\n")
        stream.write(json.dumps(typed) + "\n")
    code, out, _ = _run(capsys, "report")
    assert code == 1
    assert f"invalid run_end fields: admission_reused for run {broken_id}" in out, out
    assert f"invalid run_end fields: admission_requested for run {broken_id}" in out, out
    assert "incomplete (no completion recorded)" in out


def test_two_slot_context_does_not_mix_holder_waits(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Two concurrent admissions each record their own context; neither run reads its peer's wait.

    Planted fault: one run's completion carries the peer's admission identity or
    wait, a later holder's context overwrites an earlier holder's record, or the
    stale environment of an overlapping admission speaks for either run.
    """
    state = tmp_path / "state"

    code, out, _ = _run(capsys, "start")
    assert code == 0
    id_a = out.strip()
    code, out, _ = _run(capsys, "start")
    id_b = out.strip()

    # Both completions run inside two real, simultaneous admissions: each
    # child resolves its own context through `admission_context()` and records
    # its completion. The barrier proves both slots were held at once.
    body = """
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import verify_duration, verify_lock
name, peer = os.environ["PROBE_NAME"], os.environ["PROBE_PEER"]
root = Path(os.environ["PROBE_DIR"])
(root / ("ready-" + name)).write_text("1")
deadline = time.time() + 30
while not (root / ("ready-" + peer)).exists():
    if time.time() > deadline:
        sys.exit(3)
    time.sleep(0.05)
context = verify_lock.admission_context()
if os.environ.get("PROBE_PLANT"):
    # planted fault: context resolution hands both holders one shared record
    context = verify_lock.AdmissionContext("shared-slot", 0.0, False)
verify_duration.record_end(
    os.environ["PROBE_RUN"],
    os.environ["PROBE_VERDICT"],
    segments=[(0.0, float(os.environ["PROBE_SECONDS"]))],
    context=context,
    admission_requested=True,
)
(root / ("context-" + name)).write_text(
    json.dumps([context.admission_id, context.wait_seconds, context.reused])
)
"""

    def entry(name: str, peer: str, run_id: str, verdict: str, seconds: str) -> subprocess.Popen[bytes]:
        env = {
            "PATH": "/usr/bin:/bin",
            "HOME": str(tmp_path),
            "XDG_STATE_HOME": str(state),
            verify_lock.FLOOR_ENV: "0",
            "PROBE_NAME": name,
            "PROBE_PEER": peer,
            "PROBE_DIR": str(tmp_path),
            "PROBE_RUN": run_id,
            "PROBE_VERDICT": verdict,
            "PROBE_SECONDS": seconds,
        }
        if os.environ.get("STAGE2_PLANT_FAULT") == "1":
            env["PROBE_PLANT"] = "1"
        return subprocess.Popen(
            [sys.executable, "-m", "scripts.verify_lock", "--", sys.executable, "-c", body],
            cwd=REPO_ROOT,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    first = entry("a", "b", id_a, "green", "1.0")
    second = entry("b", "a", id_b, "red", "2.0")
    assert first.wait(timeout=90) == 0, "the first admission failed or never overlapped its peer"
    assert second.wait(timeout=90) == 0, "the second admission failed or never overlapped its peer"

    ctx_a = json.loads((tmp_path / "context-a").read_text(encoding="utf-8"))
    ctx_b = json.loads((tmp_path / "context-b").read_text(encoding="utf-8"))
    assert ctx_a[0] and ctx_b[0] and ctx_a[0] != ctx_b[0], f"the holders share one admission identity: {ctx_a} {ctx_b}"
    assert ctx_a[2] is False and ctx_b[2] is False, "a fresh admission was read as reused"

    # The history keeps both completions apart, each with its own verdict,
    # identity and wait.
    ends = [event for event in _history(state) if event["event"] == "run_end"]
    assert len(ends) == 2, ends
    by_id = {event["run_id"]: event for event in ends}
    assert by_id[id_a]["verdict"] == "green", by_id
    assert by_id[id_b]["verdict"] == "red", by_id
    assert by_id[id_a]["admission_id"] == ctx_a[0], by_id
    assert by_id[id_a]["admission_wait_seconds"] == ctx_a[1], by_id
    assert by_id[id_b]["admission_id"] == ctx_b[0], by_id
    assert by_id[id_b]["admission_wait_seconds"] == ctx_b[1], by_id

    # The reader attributes each run's own context; the peer's identity never
    # appears in the other run's report.
    code, out, _ = _run(capsys, "report", "--run", id_a)
    assert code == 0
    assert f"admission (final): {ctx_a[0]}" in out, out
    assert ctx_b[0] not in out, out
    code, out, _ = _run(capsys, "report", "--run", id_b)
    assert code == 0
    assert f"admission (final): {ctx_b[0]}" in out, out
    assert ctx_a[0] not in out, out
    assert "wait: 3.5" not in out and "wait: 99.0" not in out, out
    assert "peer-env" not in out, out
