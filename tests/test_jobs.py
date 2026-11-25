"""Tests for scripts/jobs.py - the detached job launcher (bead coding-harness-a6ns.1).

Most cases run the launcher's real wrapper, records, stop and prune against an isolated state root; only the
call that opens a tmux window is replaced by a start of the same wrapper in a session of its own (the
`detached` fixture). Two cases use a real tmux server on a socket of their own and skip when tmux is absent.
"""

from __future__ import annotations

import contextlib
import fcntl
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import textwrap
import threading
import time
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import jobs  # noqa: E402

try:
    import job_containment  # noqa: E402
except ImportError:  # a baseline before the containment module: the regression tests then fail by assertion
    job_containment = None
import verify_lock  # noqa: E402

JOBS_PY = REPO_ROOT / "scripts" / "jobs.py"
DAY = 86400
SLEEPER = [sys.executable, "-c", "import time; time.sleep(120)"]
OLD_START = "Mon Jan 1 00:00:00 2001"


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An isolated state root; the caller holds no admission and runs no job."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    for name in (*jobs.EXCLUDED_ENV, jobs.RECORD_ENV):
        monkeypatch.delenv(name, raising=False)
    return tmp_path / "xdg" / "coding-harness" / "jobs"


@pytest.fixture
def detached(state: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Replace only the tmux window by a wrapper start in its own session, under a polluted server environment.

    Jobs start in a working directory of this test alone, so a stop's directory rule never meets the
    processes of another test running in parallel."""
    job_cwd = tmp_path / "job-cwd"
    job_cwd.mkdir()
    monkeypatch.chdir(job_cwd)
    processes: list[subprocess.Popen] = []

    def fake_launch(_job_id: str, cwd: str, argv: list[str]) -> None:
        server_env = {"PATH": os.environ.get("PATH", ""), "SERVER_ONLY": "from-server", "CALLER_VALUE": "from-server"}
        processes.append(
            subprocess.Popen(
                argv,
                cwd=cwd,
                env=server_env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        )

    monkeypatch.setattr(jobs, "launch_window", fake_launch)
    monkeypatch.setattr(jobs, "tmux_path", lambda: "/fake/tmux")
    yield processes
    for process in processes:
        with contextlib.suppress(OSError):
            os.killpg(process.pid, signal.SIGKILL)
    for _job_id, record in jobs.read_all(state):
        if record is None:
            continue
        for group in record["groups"]:
            with contextlib.suppress(OSError):
                os.killpg(group["pgid"], signal.SIGKILL)
    for process in processes:
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.wait(timeout=10)


def wait_for(predicate, timeout: float = 30.0, step: float = 0.05) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(step)
    pytest.fail("condition not reached in time")


def running(pid: int) -> bool:
    """True when the process exists and is not a zombie."""
    done = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True, check=False)
    status = done.stdout.strip()
    return bool(status) and not status.startswith("Z")


def record_path(job_id: str) -> Path:
    return jobs.state_dir() / f"{job_id}.json"


def start_job(capsys: pytest.CaptureFixture[str], *command: str) -> tuple[int, str]:
    code = jobs.main(["start", "--", *command])
    return code, capsys.readouterr().out


def started_id(out: str) -> str:
    assert out.startswith("started "), out
    return out.split()[1]


def wait_finished(job_id: str) -> dict:
    wait_for(lambda: jobs.read_record(record_path(job_id))["state"] == "finished")
    return jobs.read_record(record_path(job_id))


def synthetic(state_name: str = "running", *, started_ago: float = 0.0, **changes) -> str:
    """Write a record by hand into the state root; returns its id. The wrapper is this test process by default."""
    now = time.time()
    job_id = jobs.new_job_id(now - started_ago)
    record = jobs.new_record(
        job_id, ["echo", "hi"], "/work", str(jobs.state_dir() / f"{job_id}.log"), now - started_ago
    )
    me = os.getpid()
    record.update(state=state_name, wrapper_pid=me, wrapper_start=jobs.process_start(me))
    record.update(changes)
    jobs.write_record(record_path(job_id), record)
    return job_id


# ---------------------------------------------------------------------------
# Criteria 1, 2, 18 - tmux
# ---------------------------------------------------------------------------


@pytest.fixture
def real_tmux(tmp_path: Path):
    tmux = shutil.which("tmux")
    if tmux is None:
        pytest.skip("tmux is not installed")
    socket = f"chtest-{os.getpid()}-{uuid.uuid4().hex[:8]}"
    env = {k: v for k, v in os.environ.items() if k not in {"TMUX", *jobs.EXCLUDED_ENV, jobs.RECORD_ENV}}
    env.update(XDG_STATE_HOME=str(tmp_path / "xdg"), HARNESS_JOBS_TMUX_SOCKET=socket)
    yield SimpleNamespace(
        tmux=tmux, socket=socket, env=env, state=tmp_path / "xdg" / "coding-harness" / "jobs", cwd=tmp_path
    )
    subprocess.run([tmux, "-L", socket, "kill-server"], capture_output=True, check=False)  # only this test's server


def launch_from_short_lived_parent(real, *command: str) -> tuple[int, str, str]:
    launcher = subprocess.Popen(
        [sys.executable, str(JOBS_PY), "start", "--", *command],
        cwd=real.cwd,
        env=real.env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    out, err = launcher.communicate(timeout=60)
    with contextlib.suppress(OSError):
        os.killpg(launcher.pid, signal.SIGKILL)  # the caller's whole process tree ends
    return launcher.returncode, out, err


def test_job_survives_launcher_exit(real_tmux) -> None:
    """Fault: the command stops with the launcher's process tree, or two jobs share a window (criterion 1)."""
    script = "import sys, time; print('out'); print('err', file=sys.stderr); time.sleep(3); sys.exit(3)"
    code, out, err = launch_from_short_lived_parent(real_tmux, sys.executable, "-c", script)
    assert code == 0, out + err
    job_id = out.split()[1]
    path = real_tmux.state / f"{job_id}.json"
    record = jobs.read_record(path)
    assert record["state"] == "running"
    assert jobs.alive(record["command_pid"], record["command_start"]), "the command died with its launcher"
    windows = subprocess.run(
        [real_tmux.tmux, "-L", real_tmux.socket, "list-windows", "-t", jobs.SESSION, "-F", "#{window_name}"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.split()
    assert f"job-{job_id}" in windows and windows.count(f"job-{job_id}") == 1
    wait_for(lambda: jobs.read_record(path)["state"] == "finished", timeout=40)
    done = jobs.read_record(path)
    assert done["exit"] == "3"
    log = Path(done["log"]).read_text(encoding="utf-8")
    assert "out" in log and "err" in log


def test_start_creates_detached_server(real_tmux) -> None:
    """Fault: a caller outside tmux cannot start a job although the tmux binary exists (criterion 18)."""
    probe = [real_tmux.tmux, "-L", real_tmux.socket, "has-session", "-t", jobs.SESSION]
    assert subprocess.run(probe, capture_output=True, check=False).returncode != 0  # no server yet
    assert "TMUX" not in real_tmux.env
    code, out, err = launch_from_short_lived_parent(real_tmux, sys.executable, "-c", "import time; time.sleep(2)")
    assert code == 0, out + err
    assert subprocess.run(probe, capture_output=True, check=False).returncode == 0  # the server was created detached


def test_missing_tmux_refuses_start(state: Path, tmp_path: Path, monkeypatch, capsys) -> None:
    """Fault: the command runs without tmux, or the diagnostic does not name tmux (criterion 2)."""
    empty = tmp_path / "empty-bin"
    empty.mkdir()
    monkeypatch.setenv("PATH", str(empty))
    marker = tmp_path / "ran"
    code = jobs.main(["start", "--", sys.executable, "-c", f"open({str(marker)!r}, 'w').close()"])
    assert code == 2
    assert "tmux" in capsys.readouterr().err
    assert not marker.exists()
    assert not state.exists(), "a refused start left state behind"


# ---------------------------------------------------------------------------
# Criteria 3, 21, 22 - stop
# ---------------------------------------------------------------------------

PARENT = """
import subprocess, sys, time
subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2], sys.argv[3]], start_new_session=True)
time.sleep(120)
"""
CHILD = """
import fcntl, os, sys, time
fd = os.open(sys.argv[1], os.O_CREAT | os.O_RDWR)
fcntl.flock(fd, fcntl.LOCK_EX)
with open(sys.argv[2], "w") as handle:
    handle.write(str(os.getpid()))
time.sleep(120)
"""


@pytest.mark.usefixtures("detached")
def test_stop_targets_only_selected_job(capsys, tmp_path: Path) -> None:
    """Fault: a separately sessioned descendant or the lock it holds survives, the wrapper cannot record
    `signal 15`, or another job stops (criterion 3)."""
    parent, child = tmp_path / "parent.py", tmp_path / "child.py"
    parent.write_text(textwrap.dedent(PARENT), encoding="utf-8")
    child.write_text(textwrap.dedent(CHILD), encoding="utf-8")
    lock, pidfile = tmp_path / "admission.lock", tmp_path / "grandchild.pid"
    code, out = start_job(capsys, sys.executable, str(parent), str(child), str(lock), str(pidfile))
    assert code == 0, out
    target = started_id(out)
    code, out = start_job(capsys, *SLEEPER)
    assert code == 0, out
    other = started_id(out)
    wait_for(lambda: pidfile.exists() and pidfile.read_text(encoding="utf-8").strip().isdigit())
    grandchild = int(pidfile.read_text(encoding="utf-8"))
    assert os.getpgid(grandchild) != jobs.read_record(record_path(target))["command_pid"], "not a separate session"

    assert jobs.main(["stop", target]) == 0

    done = wait_finished(target)
    assert done["exit"] == "signal 15"
    assert done["stop_requested"] is not None
    wait_for(lambda: not running(grandchild), timeout=10)
    fd = os.open(lock, os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)  # the admission-like lock is released
    finally:
        os.close(fd)
    survivor = jobs.read_record(record_path(other))
    assert jobs.effective_state(survivor) == "running"
    assert running(survivor["command_pid"]), "stop ended another job"
    assert jobs.main(["stop", other]) == 0


@pytest.mark.usefixtures("detached")
def test_stop_request_precedes_signal(capsys, monkeypatch) -> None:
    """Fault: a signal is sent before the stop request is recorded (criterion 22)."""
    code, out = start_job(capsys, *SLEEPER)
    assert code == 0, out
    job_id = started_id(out)
    real = jobs._signal_pid
    observed: list[str | None] = []

    def spy(pid: int, signum: int) -> None:
        observed.append(jobs.read_record(record_path(job_id))["stop_requested"])
        real(pid, signum)

    monkeypatch.setattr(jobs, "_signal_pid", spy)
    assert jobs.main(["stop", job_id]) == 0
    assert observed, "nothing was signalled"
    assert all(value is not None for value in observed)


@pytest.mark.usefixtures("state")
def test_stop_refuses_finished_lost_and_reused_pids(monkeypatch, capsys) -> None:
    """Fault: stop signals an unrelated process (a reused pid) or exits with another status (criterion 21)."""
    victim = subprocess.Popen(["sleep", "60"])
    signalled: list[int] = []
    monkeypatch.setattr(jobs, "_signal_pid", lambda pid, _signum: signalled.append(pid))
    try:
        finished = synthetic("finished", exit="0", ended_at="2026-01-01T00:00:00Z", ended_epoch=time.time())
        lost = synthetic("running", wrapper_pid=victim.pid, wrapper_start=OLD_START, command_pid=victim.pid)
        reused = synthetic("running", command_pid=victim.pid, command_start=OLD_START)
        for job_id in (finished, lost, reused, "20260101T000000Z-abcdef", "../escape"):
            assert jobs.main(["stop", job_id]) == 2, job_id
        capsys.readouterr()
        assert signalled == []
        assert victim.poll() is None, "an unrelated process was signalled"
        for job_id in (finished, lost, reused):
            assert jobs.read_record(record_path(job_id))["stop_requested"] is None
    finally:
        victim.kill()
        victim.wait()


# ---------------------------------------------------------------------------
# Criteria 4, 5, 6, 17 - the record's life
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("detached")
def test_start_record_contains_command_window_time_and_log(state: Path, tmp_path, monkeypatch, capsys) -> None:
    """Fault: a required field, a PID's start time, a process group or the location is wrong (criterion 4)."""
    monkeypatch.chdir(tmp_path)
    code, out = start_job(capsys, *SLEEPER)
    assert code == 0, out
    job_id = started_id(out)
    path = record_path(job_id)
    assert path.parent == state and state == tmp_path / "xdg" / "coding-harness" / "jobs"
    record = jobs.read_record(path)
    assert record["command"] == SLEEPER
    assert record["runner_verb"] is False
    assert record["cwd"] == str(Path.cwd())
    assert record["tmux_window"] == f"jobs:job-{job_id}"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", record["started_at"])
    assert record["log"] == str(state / f"{job_id}.log")
    assert isinstance(record["command_pid"], int) and isinstance(record["wrapper_pid"], int)
    assert record["command_start"] == jobs.process_start(record["command_pid"])
    assert record["wrapper_start"] == jobs.process_start(record["wrapper_pid"])
    assert record["groups"] == [
        {"pgid": record["command_pid"], "pid": record["command_pid"], "start": record["command_start"]}
    ]
    assert record["stop_requested"] is None
    assert jobs.is_runner_verb(["python3", "scripts/stage2.py", "implement", "x"]) is True
    assert jobs.is_runner_verb(["python3", "/r/scripts/stage2.py", "--spec-review-inventory"]) is False
    assert jobs.is_runner_verb(["echo", "hi"]) is False
    assert not jobs.is_runner_verb(["grep", "-n", "scripts/stage2.py", "draft"])
    assert jobs.is_runner_verb(["python3", "scripts/stage2.py", "unknown"])


@pytest.mark.usefixtures("detached")
def test_completion_retains_real_exit_status(state: Path, monkeypatch, capsys) -> None:
    """Fault: an exit code, a signal death or the end time is wrong, or a record is pruned before 14 days
    from its end (criterion 5)."""
    cases = {
        "7": [sys.executable, "-c", "import sys; sys.exit(7)"],
        "0": [sys.executable, "-c", "pass"],
        "signal 9": [sys.executable, "-c", "import os, signal; os.kill(os.getpid(), signal.SIGKILL)"],
    }
    ids = {}
    for expected, command in cases.items():
        code, out = start_job(capsys, *command)
        assert code == 0, out
        ids[expected] = started_id(out)
    for expected, job_id in ids.items():
        done = wait_finished(job_id)
        assert done["exit"] == expected
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", done["ended_at"])
        assert done["ended_epoch"] >= done["started_epoch"]
    done = jobs.read_record(record_path(ids["7"]))
    monkeypatch.setattr(jobs, "_now", lambda: done["ended_epoch"] + 14 * DAY - 60)
    jobs.prune(state)
    assert record_path(ids["7"]).exists() and Path(done["log"]).exists(), "pruned before 14 days from its end"
    monkeypatch.setattr(jobs, "_now", lambda: done["ended_epoch"] + 14 * DAY + 60)
    jobs.prune(state)
    assert not record_path(ids["7"]).exists() and not Path(done["log"]).exists()


@pytest.mark.usefixtures("detached", "state")
def test_list_reports_running_job(capsys) -> None:
    """Fault: a running, lost or recently finished job is missing, or an older finished job shows without
    `--all` (criterion 6)."""
    code, out = start_job(capsys, *SLEEPER)
    assert code == 0, out
    live = started_id(out)
    now = time.time()
    recent = synthetic("finished", started_ago=3 * 3600, exit="0", ended_at="x", ended_epoch=now - 2 * 3600)
    old = synthetic("finished", started_ago=4 * DAY, exit="1", ended_at="x", ended_epoch=now - 3 * DAY)
    lost = synthetic("running", started_ago=5 * DAY, wrapper_pid=2**22 + 17, wrapper_start=OLD_START)
    assert jobs.main(["list"]) == 0
    shown = capsys.readouterr().out
    assert f"{live}  running" in shown
    assert f"{recent}  finished" in shown
    assert f"{lost}  lost" in shown
    assert old not in shown
    assert jobs.main(["list", "--all"]) == 0
    assert old in capsys.readouterr().out


def test_missing_process_is_lost(state: Path, monkeypatch, capsys) -> None:
    """Fault: a vanished or replaced wrapper shows as running or as a success, or lost retention is wrong
    (criterion 17)."""
    me = os.getpid()
    vanished = synthetic("running", wrapper_pid=2**22 + 17, wrapper_start=OLD_START)
    replaced = synthetic("running", wrapper_pid=me, wrapper_start=OLD_START)  # a live pid with another identity
    healthy = synthetic("running")
    assert jobs.effective_state(jobs.read_record(record_path(vanished))) == "lost"
    assert jobs.effective_state(jobs.read_record(record_path(replaced))) == "lost"
    assert jobs.effective_state(jobs.read_record(record_path(healthy))) == "running"
    assert jobs.main(["list"]) == 0
    shown = capsys.readouterr().out
    assert f"{vanished}  lost" in shown and "exit" not in shown.split(vanished)[1].splitlines()[0]
    start = time.time()
    young = synthetic("running", started_ago=13 * DAY, wrapper_pid=2**22 + 17, wrapper_start=OLD_START)
    stale = synthetic("running", started_ago=15 * DAY, wrapper_pid=2**22 + 17, wrapper_start=OLD_START)
    monkeypatch.setattr(jobs, "_now", lambda: start)
    jobs.prune(state)
    assert record_path(young).exists(), "a lost record was pruned before 14 days from its start"
    assert not record_path(stale).exists()


# ---------------------------------------------------------------------------
# Criteria 8, 16 - environment and admission
# ---------------------------------------------------------------------------


def dump_environment(capsys, tmp_path: Path) -> tuple[str, dict]:
    out_file = tmp_path / "environment.json"
    script = "import json, os, sys; json.dump({**os.environ, '_CWD': os.getcwd()}, open(sys.argv[1], 'w'))"
    code, out = start_job(capsys, sys.executable, "-c", script, str(out_file))
    assert code == 0, out
    job_id = started_id(out)
    wait_finished(job_id)
    return job_id, json.loads(out_file.read_text(encoding="utf-8"))


@pytest.mark.usefixtures("detached")
def test_caller_environment_and_admission_are_passed_safely(state: Path, tmp_path, monkeypatch, capsys) -> None:
    """Fault: the server's values replace the caller's, or any of the four admission values is inherited
    (criterion 16)."""
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    monkeypatch.setenv("CALLER_VALUE", "from-caller")
    monkeypatch.setenv("VIRTUAL_ENV", "/x/venv")
    monkeypatch.setenv("HARNESS_VERIFY_LOCK_HELD", "123")
    monkeypatch.setenv("HARNESS_VERIFY_LOCK_TOKEN", "token")
    monkeypatch.setenv("HARNESS_VERIFY_ADMISSION_ID", "admission")
    monkeypatch.setenv("HARNESS_VERIFY_ADMISSION_WAIT", "1.5")
    job_id, seen = dump_environment(capsys, tmp_path)
    assert seen["CALLER_VALUE"] == "from-caller"
    assert "SERVER_ONLY" not in seen
    assert seen["PATH"] == os.environ["PATH"] and seen["VIRTUAL_ENV"] == "/x/venv"
    assert seen["_CWD"] == str(Path.cwd())
    assert seen[jobs.RECORD_ENV] == str(record_path(job_id))
    for name in jobs.EXCLUDED_ENV:
        assert name not in seen, name
    assert not (state / f"{job_id}.env").exists(), "the private environment file outlived the start"


@pytest.mark.usefixtures("detached", "state")
def test_detached_verify_obeys_shared_admission(tmp_path, monkeypatch, capsys) -> None:
    """Fault: a job inherits its caller's held admission or leaves the shared state root, so it could
    bypass the machine-wide limit and floor (criterion 8)."""
    assert jobs.EXCLUDED_ENV == (
        verify_lock.LOCK_ENV,
        verify_lock.TOKEN_ENV,
        verify_lock.ADMISSION_ID_ENV,
        verify_lock.ADMISSION_WAIT_ENV,
    )
    monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
    monkeypatch.setenv(verify_lock.TOKEN_ENV, "held-token")
    monkeypatch.setenv(verify_lock.ADMISSION_ID_ENV, "held-admission")
    monkeypatch.setenv(verify_lock.ADMISSION_WAIT_ENV, "2.0")
    _job_id, seen = dump_environment(capsys, tmp_path)
    for name in jobs.EXCLUDED_ENV:
        assert name not in seen, f"{name} reached the job"
    assert seen["XDG_STATE_HOME"] == str(tmp_path / "xdg"), "the job left the shared state root"
    source = JOBS_PY.read_text(encoding="utf-8")
    assert "import verify_lock" not in source, "the launcher must hold no admission and make no second quota"


# ---------------------------------------------------------------------------
# Criteria 12, 19, 24, 25, 26
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("detached")
def test_launcher_does_not_write_lane_markers(state: Path, tmp_path, monkeypatch, capsys) -> None:
    """Fault: starting, listing or stopping a job writes anything beside the job's own files (criterion 12)."""
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    code, out = start_job(capsys, *SLEEPER)
    assert code == 0, out
    job_id = started_id(out)
    assert jobs.main(["list"]) == 0
    assert jobs.main(["stop", job_id]) == 0
    capsys.readouterr()
    assert list(work.iterdir()) == [], "the launcher wrote into the caller's directory"
    written = [p for p in tmp_path.rglob("*") if p.is_file() and not p.is_relative_to(state)]
    assert written == [], f"files outside the jobs directory: {written}"
    assert all(re.search(r"\.(json|log|env|lock|tmp)$", p.name) for p in state.iterdir())
    assert not any("lane" in p.name or "busy" in p.name for p in tmp_path.rglob("*"))


def test_records_are_schema_validated_and_atomic(state: Path, monkeypatch) -> None:
    """Fault: an invalid or partial record becomes visible, or concurrent updates overwrite each other
    (criterion 19)."""
    job_id = jobs.new_job_id()
    path = record_path(job_id)
    good = jobs.new_record(job_id, ["echo", "hi"], "/work", str(state / f"{job_id}.log"))
    for broken in (
        {**good, "schema": True},
        {**good, "schema": 1.0},
        {**good, "state": "sleeping"},
        {**good, "command": []},
        {**good, "groups": [{"pgid": "x", "pid": 1, "start": None}]},
        {k: v for k, v in good.items() if k != "log"},
        {**good, "extra": 1},
    ):
        with pytest.raises(jobs.JobError):
            jobs.write_record(path, broken)
        assert not path.exists(), "an invalid record was published"
    jobs.write_record(path, good)
    before = path.read_text(encoding="utf-8")
    real_fsync = os.fsync

    def failing_fsync(_fd: int) -> None:
        raise OSError("disk")

    monkeypatch.setattr(os, "fsync", failing_fsync)
    with pytest.raises(OSError, match="disk"):
        jobs.write_record(path, {**good, "state": "running"})
    monkeypatch.setattr(os, "fsync", real_fsync)
    assert path.read_text(encoding="utf-8") == before, "a failed write left a partial record"
    assert sorted(p.name for p in state.iterdir()) == [path.name]  # no temporary file remains
    path.write_text(before[: len(before) // 2], encoding="utf-8")  # a truncated record is refused, never repaired
    with pytest.raises(jobs.JobError):
        jobs.read_record(path)
    path.write_text(before, encoding="utf-8")

    def add(n: int):
        return lambda record: record["groups"].append({"pgid": n, "pid": n, "start": None})

    threads = [threading.Thread(target=jobs.update_record, args=(path, add(n))) for n in range(1, 9)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sorted(g["pgid"] for g in jobs.read_record(path)["groups"]) == list(range(1, 9))


@pytest.mark.usefixtures("detached", "state")
def test_start_waits_for_both_pids(monkeypatch, capsys) -> None:
    """Fault: start reports success before both process ids are published, or waits over 10 seconds
    (criterion 24)."""
    assert jobs.START_WAIT == 10.0
    real_launch = jobs.launch_window

    def delayed(job_id: str, cwd: str, argv: list[str]) -> None:
        threading.Timer(0.6, real_launch, args=(job_id, cwd, argv)).start()

    monkeypatch.setattr(jobs, "launch_window", delayed)
    began = time.monotonic()
    code, out = start_job(capsys, *SLEEPER)
    elapsed = time.monotonic() - began
    assert code == 0, out
    assert 0.5 <= elapsed <= 10.0, "start must wait for both ids, at most ten seconds"
    record = jobs.read_record(record_path(started_id(out)))
    assert record["command_pid"] is not None and record["wrapper_pid"] is not None


@pytest.mark.usefixtures("detached")
def test_failed_start_has_terminal_state(state: Path, monkeypatch, capsys) -> None:
    """Fault: missing process ids do not give exit 1 and the `failed to start` state (criterion 25)."""
    monkeypatch.setattr(jobs, "START_WAIT", 0.5)
    monkeypatch.setattr(jobs, "launch_window", lambda *_args: None)  # the wrapper never runs
    code, out = start_job(capsys, *SLEEPER)
    assert code == 1
    (record_file,) = state.glob("*.json")
    record = jobs.read_record(record_file)
    assert record["state"] == "failed to start" and record["command_pid"] is None
    assert "process ids" in record["error"] and record["ended_at"] is not None
    assert not list(state.glob("*.env")), "the private environment file stayed behind"

    def refuse(*_args: object) -> None:
        raise jobs.JobError("tmux new-window failed: no space")

    monkeypatch.setattr(jobs, "launch_window", refuse)
    code, out = start_job(capsys, *SLEEPER)
    assert code == 1 and "failed to start" in out
    assert sorted(jobs.read_record(p)["state"] for p in state.glob("*.json")) == ["failed to start"] * 2


@pytest.mark.usefixtures("detached")
def test_command_that_cannot_run_fails_to_start(state: Path, capsys) -> None:
    """A command the wrapper cannot execute ends the start with exit 1, not a hang."""
    code, out = start_job(capsys, str(state / "no-such-program"))
    assert code == 1 and "failed to start" in out
    (record_file,) = state.glob("*.json")
    assert jobs.read_record(record_file)["state"] == "failed to start"


@pytest.mark.usefixtures("detached")
def test_log_captures_streams_and_is_pruned(state: Path, monkeypatch, capsys) -> None:
    """Fault: a stream is missing from the log, or the log outlives its pruned record (criterion 26)."""
    script = "import sys; print('to-stdout'); print('to-stderr', file=sys.stderr)"
    code, out = start_job(capsys, sys.executable, "-c", script)
    assert code == 0, out
    job_id = started_id(out)
    done = wait_finished(job_id)
    log = Path(done["log"])
    text = log.read_text(encoding="utf-8")
    assert "to-stdout" in text and "to-stderr" in text
    orphan = state / "20200101T000000Z-aaaaaa.log"
    orphan.write_text("left behind\n", encoding="utf-8")
    old = time.time() - 15 * DAY
    os.utime(orphan, (old, old))
    monkeypatch.setattr(jobs, "_now", lambda: done["ended_epoch"] + 14 * DAY + 60)
    jobs.prune(state)
    assert not log.exists() and not record_path(job_id).exists(), "the log outlived its record"
    assert not orphan.exists(), "a log without a record was kept"


def test_reused_recorded_group_is_never_targeted() -> None:
    """A reused group leader and its members are not the recorded job."""
    assert job_containment is not None, "scripts/job_containment.py is missing"

    class TableBackend(job_containment.PsBackend):
        """A stand-in process table: no sessions, no tokens, no files."""

        def __init__(self, table: list) -> None:
            self.table = table

        def processes(self) -> list:
            return self.table

        def session(self, _pid: int) -> int | None:
            return None

        def token_holders(self, _token: str) -> set[int]:
            return set()

        def paths(self, _pids) -> dict[int, list[str]]:
            return {}

    old = "Mon Jan 1 00:00:00 2024"
    new = "Tue Jan 2 00:00:00 2024"

    def proc(pid: int, ppid: int, pgid: int, start: str) -> job_containment.Proc:
        return job_containment.Proc(pid, ppid, pgid, os.getuid(), "??", "S", start, "x")

    record = {
        "id": "20240101T000000Z-abcdef",
        "cwd": "/work",
        "started_epoch": 0,
        "command_pid": 100,
        "command_start": old,
        "wrapper_pid": 101,
        "groups": [{"pid": 200, "pgid": 200, "start": old}],
    }
    backend = TableBackend([proc(100, 1, 100, old), proc(200, 1, 200, new), proc(201, 200, 200, new)])
    assert set(job_containment.members(record, [], backend)) == {100}


def test_stop_spares_unrelated_process_in_job_directory() -> None:
    """A process with files in the job directory is not a member or a signal target."""
    assert job_containment is not None
    started = "Mon Jan 1 00:00:00 2024"
    root = job_containment.Proc(100, 1, 100, os.getuid(), "??", "S", started, "job")
    unrelated = job_containment.Proc(200, 1, 200, os.getuid(), "??", "S", started, "editor")

    class Backend:
        def __init__(self):
            self.signals = []

        def processes(self):
            return [root, unrelated]

        def token_holders(self, _token):
            return set()

        def session(self, _pid):
            return None

        def paths(self, _pids):
            return {200: ["/work/project", "/work/project/open-file"]}

        def alive(self, pid, _start):
            return pid not in {sent for sent, _ in self.signals}

        def send(self, pid, signum):
            self.signals.append((pid, signum))

    record = {
        "id": "job",
        "cwd": "/work/project",
        "started_epoch": 0,
        "command_pid": 100,
        "command_start": started,
        "groups": [],
    }
    backend = Backend()
    job_containment.end(record, backend=backend)
    assert [pid for pid, _ in backend.signals] == [100], "an unrelated process was signalled"


@pytest.mark.usefixtures("state")
def test_stop_writes_survivors_into_the_record(monkeypatch, capsys) -> None:
    """Finding F-1: a member still alive after SIGKILL and a last scan is written into the record and shown by
    `list` - never left silent."""
    assert job_containment is not None, "scripts/job_containment.py is missing"
    survivor = subprocess.Popen(["sleep", "60"])
    try:
        wait_for(lambda: jobs.process_start(survivor.pid) is not None)
        started = jobs.process_start(survivor.pid)
        job_id = synthetic("running", command_pid=survivor.pid, command_start=started, cwd="/")
        monkeypatch.setattr(jobs, "_signal_pid", lambda _pid, _signum: None)  # the signals do not land
        monkeypatch.setattr(job_containment, "STOP_GRACE", 0.2)
        monkeypatch.setattr(job_containment, "KILL_WAIT", 0.2)
        monkeypatch.setattr(jobs, "FINISH_WAIT", 0.2)
        assert jobs.main(["stop", job_id]) == 3
        assert f"survivor: pid {survivor.pid}" in capsys.readouterr().out
        record = jobs.read_record(record_path(job_id))
        assert [s["pid"] for s in record["survivors"]] == [survivor.pid]
        assert record["survivors"][0]["start"] == jobs.process_start(survivor.pid)
        assert "sleep" in record["survivors"][0]["command"]
        assert jobs.main(["list"]) == 0
        assert f"survivors after stop: pid {survivor.pid}" in capsys.readouterr().out
    finally:
        survivor.kill()
        survivor.wait()


def test_future_runner_verb_is_recognized() -> None:
    assert jobs.is_runner_verb([sys.executable, "scripts/stage2.py", "future-verb", "change"])
    assert not jobs.is_runner_verb(["grep", "scripts/stage2.py", "future-verb"])
    assert not jobs.is_runner_verb([sys.executable, "scripts/stage2.py", "--help"])


def test_start_deadline_includes_hung_tmux(state, tmp_path, monkeypatch, capsys) -> None:
    fake = tmp_path / "tmux"
    fake.write_text("#!/bin/sh\nsleep 5\n")
    fake.chmod(0o755)
    monkeypatch.setattr(jobs, "tmux_path", lambda: str(fake))
    monkeypatch.setattr(jobs, "START_WAIT", 0.5)
    started = time.monotonic()
    assert jobs.main(["start", "--", *SLEEPER]) == 1
    assert time.monotonic() - started < 2
    assert jobs.read_record(next(state.glob("*.json")))["state"] == "failed to start"
    capsys.readouterr()


@pytest.mark.usefixtures("detached")
def test_stop_reparented_session_descendant(tmp_path, capsys) -> None:
    marker = tmp_path / "pid"
    grandchild = "import os,time; open(os.environ['PID_FILE'],'w').write(str(os.getpid())); time.sleep(120)"
    middle = f"import subprocess,sys; subprocess.Popen([sys.executable,'-c',{grandchild!r}],start_new_session=True)"
    parent = f"import subprocess,sys,time; subprocess.run([sys.executable,'-c',{middle!r}],start_new_session=True); time.sleep(120)"
    os.environ["PID_FILE"] = str(marker)
    try:
        code, out = start_job(capsys, sys.executable, "-c", parent)
        assert code == 0
        job_id = started_id(out)
        wait_for(marker.exists)
        pid = int(marker.read_text())
        assert running(pid)
        assert jobs.main(["stop", job_id]) == 0
        wait_for(lambda: not running(pid))
    finally:
        os.environ.pop("PID_FILE", None)
        if marker.exists():
            with contextlib.suppress(ProcessLookupError):
                os.kill(int(marker.read_text()), signal.SIGKILL)


@pytest.mark.usefixtures("detached")
def test_detached_verify_waits_for_slots_and_memory(tmp_path, monkeypatch, capsys) -> None:
    """Fault: a detached verification run while both admissions are held - one of them by its own caller -
    or while memory is below the floor runs at once instead of waiting or refusing (criterion 8).

    Under `STAGE2_PLANT_FAULT` the launcher passes the caller's held admission on to the job (the real
    fault this test guards), so the job nests in that admission and runs at once."""
    monkeypatch.chdir(REPO_ROOT)
    monkeypatch.setenv(verify_lock.FLOOR_ENV, "0")
    holders = []
    held = tmp_path / "held.json"
    try:
        for i in range(2):
            marker = tmp_path / f"holder-{i}"
            body = (
                "import json, os, time; from pathlib import Path; "
                f"json.dump({{k: os.environ.get(k) for k in {[verify_lock.LOCK_ENV, verify_lock.TOKEN_ENV]!r}}}, "
                f"open({str(held)!r}, 'w')) if {i} == 0 else None; "
                f"Path({str(marker)!r}).touch(); time.sleep(120)"
            )
            holders.append(
                subprocess.Popen(
                    [sys.executable, "-m", "scripts.verify_lock", "--", sys.executable, "-c", body],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            )
            wait_for(marker.exists)
        # The caller holds the first admission, as a session inside a verification run would.
        caller = json.loads(held.read_text(encoding="utf-8"))
        assert caller[verify_lock.LOCK_ENV] and caller[verify_lock.TOKEN_ENV], "the holder published no admission"
        for name, value in caller.items():
            monkeypatch.setenv(name, value)
        if os.environ.get("STAGE2_PLANT_FAULT"):
            monkeypatch.setattr(jobs, "EXCLUDED_ENV", ())  # planted: the job inherits the caller's admission
        result = tmp_path / "admitted"
        body = f"from pathlib import Path; Path({str(result)!r}).touch()"
        code, out = start_job(capsys, sys.executable, "-m", "scripts.verify_lock", "--", sys.executable, "-c", body)
        assert code == 0
        job_id = started_id(out)
        time.sleep(1)
        assert not result.exists(), "detached verification bypassed occupied admissions"
        for name in caller:
            monkeypatch.delenv(name)
        holders[0].terminate()
        holders[0].wait(timeout=10)
        wait_for(result.exists)
        wait_finished(job_id)
    finally:
        for holder in holders:
            if holder.poll() is None:
                holder.terminate()
                holder.wait(timeout=10)
    result.unlink()
    script = f"import sys; sys.path.insert(0, {str(REPO_ROOT / 'scripts')!r}); import verify_lock as v; v.read_available_memory=lambda: 0; v.MEMORY_POLL_SECONDS=0.05; v.MEMORY_DEADLINE_SECONDS=0.2; sys.exit(v.main(['--',sys.executable,'-c',{body!r}]))"
    monkeypatch.setenv(verify_lock.FLOOR_ENV, "50")
    code, out = start_job(capsys, sys.executable, "-c", script)
    assert code == 0
    record = wait_finished(started_id(out))
    assert not result.exists(), "detached verification bypassed the memory floor"
    assert record["exit"] != "0"


def test_env_launched_runner_verb_is_classified() -> None:
    """Finding F-2 (Terms; criterion 4): a runner verb behind `env`, with or without its options and
    NAME=value words, behind a versioned interpreter or `uv run`, is a runner verb; `-c` and `-m` are not."""
    assert jobs.is_runner_verb(["env", "python3", "scripts/stage2.py", "review", "change"])
    with_options = ["/usr/bin/env", "-u", "X", "A=1", "python3.12", "-X", "dev", "scripts/stage2.py", "y"]
    assert jobs.is_runner_verb(with_options)
    assert jobs.is_runner_verb(["python3", "--", "scripts/stage2.py", "review"])
    assert jobs.is_runner_verb(["uv", "run", "--python", "3.12", "python", "/r/scripts/stage2.py", "draft"])
    assert not jobs.is_runner_verb(["env", "python3", "-m", "scripts.stage2", "review"])
    assert not jobs.is_runner_verb(["env", "python3", "scripts/stage2.py", "--help"])
    assert not jobs.is_runner_verb(["env", "grep", "scripts/stage2.py", "review"])


def test_runner_classifier_skips_launchers() -> None:
    assert jobs.is_runner_verb(["env", "-i", "FOO=bar", "python3", "-u", "scripts/stage2.py", "review"])
    assert jobs.is_runner_verb(["uv", "run", "--no-project", "python3.12", "scripts/stage2.py", "review"])
    assert not jobs.is_runner_verb(["env", "python3", "-c", "scripts/stage2.py", "review"])
