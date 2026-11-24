#!/usr/bin/env python3
"""jobs.py - start a command as a detached job that outlives the launching session (bead coding-harness-a6ns.1).

    python3 scripts/jobs.py start [--] COMMAND [ARGUMENT...]   # one window on the dedicated tmux server
    python3 scripts/jobs.py list [--all]                       # running, lost and recent (24 h) jobs
    python3 scripts/jobs.py stop JOB_ID                        # end the job's tree; the wrapper records `signal 15`

A job runs in its own window of the `tmux -L coding-harness` server (a server
that is created detached when none exists) under a small wrapper of this file.
The wrapper starts the command in a session of its own, captures standard
output and standard error in the job's log, and writes the end time and the
real exit status into the job's record. The record and the log live under
`${XDG_STATE_HOME:-~/.local/state}/coding-harness/jobs/` and are kept 14 days
(finished jobs from their end, every other kind from its start).

The job receives the caller's working directory and whole environment, supplied
per job through a private file the wrapper reads and deletes - never the tmux
server's environment - except the four verification-admission values: a
detached verification run obtains its own machine-wide admission. The record's
path travels to the command in `HARNESS_JOB_RECORD`; `scripts/stage2.py` adds
every process group it starts in a session of its own to that record, so `stop`
reaches them.

This launcher accepts any command. A runner verb (`scripts/stage2.py` followed
by a word that is not an option) is recorded as such; model starts stay routed
through the runner. It writes no lane or busy marker, schedules nothing and
restarts nothing.

Exit status: 0 success; 1 a start that failed; 2 a refusal (usage, missing tmux,
a stop on a job that is not running); 3 stop signalled but not yet recorded.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # readers of the records (run report, machine facts) write nothing

import contextlib  # noqa: E402
import fcntl  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import secrets  # noqa: E402
import shlex  # noqa: E402
import shutil  # noqa: E402
import signal  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import time  # noqa: E402
from collections.abc import Callable  # noqa: E402
from datetime import UTC, datetime  # noqa: E402
from pathlib import Path  # noqa: E402

SESSION = "jobs"
START_WAIT = 10.0  # seconds a start waits for both process ids
STOP_GRACE = 5.0  # seconds between SIGTERM and SIGKILL
FINISH_WAIT = 10.0  # seconds a stop waits for the wrapper's end record
KEEP_SECONDS = 14 * 86400
RECENT_SECONDS = 86400
STALE_START_SECONDS = 3 * START_WAIT  # a record still `starting` after this is lost
RECORD_ENV = "HARNESS_JOB_RECORD"
# The four values of a held verification admission (scripts/verify_lock.py); a job never inherits them.
EXCLUDED_ENV = (
    "HARNESS_VERIFY_LOCK_HELD",
    "HARNESS_VERIFY_LOCK_TOKEN",
    "HARNESS_VERIFY_ADMISSION_ID",
    "HARNESS_VERIFY_ADMISSION_WAIT",
)
ID_PATTERN = r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}"
ID_RE = re.compile(ID_PATTERN)
STATES = ("starting", "running", "finished", "failed to start")


class JobError(Exception):
    """A record, a tmux call or a process could not be handled; the message is bounded and plain."""


class Refused(JobError):
    """A request the launcher refuses before it does anything (exit 2)."""


# ---------------------------------------------------------------------------
# Records: JSON schema, atomic publication, locked update
# ---------------------------------------------------------------------------

_NULL_INT = {"type": ["integer", "null"]}
_NULL_STR = {"type": ["string", "null"]}
_NULL_NUM = {"type": ["number", "null"]}

SCHEMA: dict = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema",
        "id",
        "state",
        "command",
        "runner_verb",
        "cwd",
        "tmux_window",
        "started_at",
        "started_epoch",
        "log",
        "command_pid",
        "command_start",
        "wrapper_pid",
        "wrapper_start",
        "groups",
        "stop_requested",
        "ended_at",
        "ended_epoch",
        "exit",
        "error",
    ],
    "properties": {
        "schema": {"type": "integer", "enum": [1]},
        "id": {"type": "string", "pattern": ID_PATTERN},
        "state": {"enum": list(STATES)},
        "command": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "runner_verb": {"type": "boolean"},
        "cwd": {"type": "string"},
        "tmux_window": {"type": "string"},
        "started_at": {"type": "string"},
        "started_epoch": {"type": "number"},
        "log": {"type": "string"},
        "command_pid": _NULL_INT,
        "command_start": _NULL_STR,
        "wrapper_pid": _NULL_INT,
        "wrapper_start": _NULL_STR,
        "groups": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["pgid", "pid", "start"],
                "properties": {"pgid": {"type": "integer"}, "pid": {"type": "integer"}, "start": _NULL_STR},
            },
        },
        "stop_requested": _NULL_STR,
        "ended_at": _NULL_STR,
        "ended_epoch": _NULL_NUM,
        "exit": _NULL_STR,
        "error": _NULL_STR,
    },
}


def _is_type(value: object, kind: str) -> bool:
    if kind == "object":
        return isinstance(value, dict)
    if kind == "array":
        return isinstance(value, list)
    if kind == "string":
        return isinstance(value, str)
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "number":
        return isinstance(value, int | float) and not isinstance(value, bool)
    if kind == "null":
        return value is None
    return False


def _check(value: object, schema: dict, where: str) -> None:
    """Validate `value` against the small JSON-schema subset `SCHEMA` uses; raise JobError on the first fault."""
    kind = schema.get("type")
    if kind is not None:
        kinds = kind if isinstance(kind, list) else [kind]
        if not any(_is_type(value, k) for k in kinds):
            raise JobError(f"{where}: expected {'/'.join(kinds)}")
    if "enum" in schema and value not in schema["enum"]:
        raise JobError(f"{where}: value not allowed")
    if "pattern" in schema and isinstance(value, str) and not re.fullmatch(schema["pattern"], value):
        raise JobError(f"{where}: does not match the pattern")
    if isinstance(value, dict):
        for name in schema.get("required", []):
            if name not in value:
                raise JobError(f"{where}: missing {name}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise JobError(f"{where}: unknown field {extra[0]}")
        for name, sub in properties.items():
            if name in value:
                _check(value[name], sub, f"{where}.{name}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise JobError(f"{where}: too few items")
        if "items" in schema:
            for index, item in enumerate(value):
                _check(item, schema["items"], f"{where}[{index}]")


def validate(record: object) -> None:
    """Raise JobError unless `record` satisfies the record schema."""
    _check(record, SCHEMA, "record")


def state_dir() -> Path:
    """The jobs directory: `${XDG_STATE_HOME:-~/.local/state}/coding-harness/jobs`."""
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / "coding-harness" / "jobs"


def _atomic_write(path: Path, text: str) -> None:
    """Publish `text` at `path` whole or not at all (same-directory temporary file, then rename)."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        Path(temporary).replace(path)
    except BaseException:
        with contextlib.suppress(OSError):
            Path(temporary).unlink()
        raise


def write_record(path: Path, record: dict) -> None:
    """Validate, then publish atomically; an invalid record is never written."""
    validate(record)
    _atomic_write(path, json.dumps(record, indent=2, sort_keys=True) + "\n")


def read_record(path: Path) -> dict:
    """The validated record at `path`, or JobError naming the file only."""
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        raise JobError(f"{path.name}: not readable as a job record") from None
    try:
        validate(record)
    except JobError as error:
        raise JobError(f"{path.name}: {error}") from None
    return record


@contextlib.contextmanager
def _locked(path: Path):
    lock = path.with_name(path.name + ".lock")
    fd = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def update_record(path: Path, mutate: Callable[[dict], None]) -> dict:
    """Read, change and republish one record under its lock, so concurrent writers never overwrite each other."""
    with _locked(path):
        record = read_record(path)
        mutate(record)
        write_record(path, record)
        return record


# ---------------------------------------------------------------------------
# Time and process identity
# ---------------------------------------------------------------------------


def _now() -> float:
    return time.time()


def _stamp(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _norm(text: str) -> str:
    return " ".join(text.split())


def _ps(args: list[str]) -> str | None:
    env = {**os.environ, "LC_ALL": "C"}
    try:
        done = subprocess.run(["ps", *args], capture_output=True, text=True, timeout=5, env=env, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout if done.returncode == 0 else None


def process_start(pid: int | None) -> str | None:
    """The start time `ps` reports for `pid` - with the pid, the identity of a process - or None when it is gone."""
    if pid is None or pid <= 0:
        return None
    text = _norm(_ps(["-o", "lstart=", "-p", str(pid)]) or "")
    return text or None


def process_table() -> list[tuple[int, int, int, str]]:
    """(pid, parent pid, process group, start time) of every visible process."""
    rows = []
    for line in (_ps(["-axo", "pid=,ppid=,pgid=,lstart="]) or "").splitlines():
        parts = line.split(None, 3)
        if len(parts) == 4 and all(part.isdigit() for part in parts[:3]):
            rows.append((int(parts[0]), int(parts[1]), int(parts[2]), _norm(parts[3])))
    return rows


def _parse_start(text: str | None) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.strptime(text, "%a %b %d %H:%M:%S %Y")
    except ValueError:
        return None


def alive(pid: int | None, start: str | None) -> bool:
    """True when `pid` runs and began at the recorded time; a reused pid counts as gone."""
    return start is not None and process_start(pid) == start


def is_runner_verb(argv: list[str]) -> bool:
    """True when the argument vector invokes scripts/stage2.py followed by a word that is not an option."""
    verbs = {
        "explore",
        "draft",
        "implement",
        "repair",
        "triage",
        "spec-review",
        "review-loop",
        "release-loop",
        "review",
        "probe",
        "prepare-loop",
        "prepare-explore",
        "session",
    }
    if not argv or not re.fullmatch(r"python(?:\d+(?:\.\d+)*)?", Path(argv[0]).name):
        return False
    for index, token in enumerate(argv[1:], 1):
        if token == "scripts/stage2.py" or token.endswith("/scripts/stage2.py"):
            return index + 1 < len(argv) and argv[index + 1] in verbs
        if not token.startswith("-") or token in {"-c", "-m", "--"}:
            return False
    return False


def effective_state(record: dict, now: float | None = None) -> str:
    """The record's state, with `lost` derived: a running record whose wrapper is gone or replaced."""
    state = record["state"]
    if state in ("finished", "failed to start"):
        return state
    if state == "running":
        return "running" if alive(record["wrapper_pid"], record["wrapper_start"]) else "lost"
    current = _now() if now is None else now
    return "starting" if current - record["started_epoch"] <= STALE_START_SECONDS else "lost"


def new_job_id(now: float | None = None) -> str:
    moment = datetime.fromtimestamp(_now() if now is None else now, UTC)
    return f"{moment:%Y%m%dT%H%M%SZ}-{secrets.token_hex(3)}"


def new_record(job_id: str, command: list[str], cwd: str, log: str, now: float | None = None) -> dict:
    """A fresh record in state `starting`; the wrapper and the runner fill in the rest."""
    started = _now() if now is None else now
    return {
        "schema": 1,
        "id": job_id,
        "state": "starting",
        "command": list(command),
        "runner_verb": is_runner_verb(command),
        "cwd": cwd,
        "tmux_window": f"{SESSION}:job-{job_id}",
        "started_at": _stamp(started),
        "started_epoch": started,
        "log": log,
        "command_pid": None,
        "command_start": None,
        "wrapper_pid": None,
        "wrapper_start": None,
        "groups": [],
        "stop_requested": None,
        "ended_at": None,
        "ended_epoch": None,
        "exit": None,
        "error": None,
    }


def register_group(pgid: int) -> None:
    """Add a process group (its leader's pid and identity) to the job record named by `HARNESS_JOB_RECORD`.

    Called by scripts/stage2.py for every group it starts in a session of its own. Outside a job, or when the
    record cannot be updated, it does nothing: the runner never fails because of a record.
    """
    raw = os.environ.get(RECORD_ENV)
    if not raw:
        return
    entry = {"pgid": pgid, "pid": pgid, "start": process_start(pgid)}

    def add(record: dict) -> None:
        record["groups"].append(entry)

    with contextlib.suppress(JobError, OSError):
        update_record(Path(raw), add)


# ---------------------------------------------------------------------------
# tmux
# ---------------------------------------------------------------------------


def tmux_socket() -> str:
    """The dedicated server's socket name (an environment override exists for isolated tests only)."""
    return os.environ.get("HARNESS_JOBS_TMUX_SOCKET") or "coding-harness"


def tmux_path() -> str | None:
    return shutil.which("tmux")


def _tmux(tmux: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [tmux, "-L", tmux_socket(), "-f", "/dev/null", *args],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )


def launch_window(job_id: str, cwd: str, argv: list[str]) -> None:
    """Start `argv` in its own window of the dedicated server, creating the server detached when absent."""
    tmux = tmux_path()
    if tmux is None:
        raise Refused("tmux is not installed or not on PATH")
    if _tmux(tmux, "has-session", "-t", SESSION).returncode != 0:
        _tmux(tmux, "new-session", "-d", "-s", SESSION, "-n", "server", "while :; do sleep 3600; done")
        if _tmux(tmux, "has-session", "-t", SESSION).returncode != 0:
            raise JobError("tmux: the detached server could not be created")
    done = _tmux(tmux, "new-window", "-d", "-t", f"{SESSION}:", "-n", f"job-{job_id}", "-c", cwd, shlex.join(argv))
    if done.returncode != 0:
        raise JobError(f"tmux new-window failed: {done.stderr.strip()[:200]}")


def _kill_window(job_id: str) -> None:
    tmux = tmux_path()
    if tmux is not None:
        with contextlib.suppress(OSError, subprocess.SubprocessError):
            _tmux(tmux, "kill-window", "-t", f"{SESSION}:job-{job_id}")


# ---------------------------------------------------------------------------
# start
# ---------------------------------------------------------------------------


def _fail(path: Path, message: str) -> dict:
    """Move a record that has not started to its terminal `failed to start` state."""

    def mark(record: dict) -> None:
        if record["state"] == "starting":
            now = _now()
            record["state"] = "failed to start"
            record["error"] = message[:300]
            record["ended_at"] = _stamp(now)
            record["ended_epoch"] = now

    return update_record(path, mark)


def start(command: list[str], out: Callable[[str], None] = print) -> int:
    """Start `command` as a detached job; return the exit status (0, 1 failed start, 2 refusal)."""
    if tmux_path() is None:
        raise Refused("tmux is missing: install tmux; no command was run")
    cwd = str(Path.cwd())
    env = {key: value for key, value in os.environ.items() if key not in EXCLUDED_ENV and key != RECORD_ENV}
    root = state_dir()
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    prune(root)
    job_id = new_job_id()
    path = root / f"{job_id}.json"
    log = root / f"{job_id}.log"
    env_file = root / f"{job_id}.env"
    write_record(path, new_record(job_id, command, cwd, str(log)))
    wrapper = [sys.executable, str(Path(__file__).resolve()), "_wrap", str(path)]
    try:
        _atomic_write(env_file, json.dumps(env))
        os.close(os.open(log, os.O_CREAT | os.O_WRONLY, 0o600))
        launch_window(job_id, cwd, wrapper)
    except (JobError, OSError, subprocess.TimeoutExpired) as error:
        with contextlib.suppress(OSError):
            env_file.unlink()
        _kill_window(job_id)
        with contextlib.suppress(JobError, OSError):
            _fail(path, str(error))
        out(f"job {job_id} failed to start: {error}")
        return 1
    deadline = time.monotonic() + START_WAIT
    while True:
        record = read_record(path)
        if record["state"] == "failed to start":
            out(f"job {job_id} failed to start: {record['error']}")
            return 1
        if record["command_pid"] is not None and record["wrapper_pid"] is not None:
            out(f"started {job_id}")
            out(f"window: {record['tmux_window']}")
            out(f"log: {record['log']}")
            return 0
        if time.monotonic() >= deadline:
            break
        time.sleep(0.05)
    record = _fail(path, f"no command and wrapper process ids within {START_WAIT:g} seconds")
    if record["state"] != "failed to start":  # the wrapper published them at the last moment
        out(f"started {job_id}")
        return 0
    with contextlib.suppress(OSError):
        env_file.unlink()
    # Let a late wrapper observe the failed record and kill its own session.
    out(f"job {job_id} failed to start: {record['error']}")
    return 1


# ---------------------------------------------------------------------------
# The wrapper (runs inside the tmux window)
# ---------------------------------------------------------------------------


def wrap(path: Path) -> int:
    """Run the job's command, keep its log and record its real outcome; the wrapper is the record's only finisher."""
    try:
        record = read_record(path)
        env_file = path.with_suffix(".env")
        supplied = json.loads(env_file.read_text(encoding="utf-8"))
        env_file.unlink()
        env = {str(key): str(value) for key, value in supplied.items()}
        env[RECORD_ENV] = str(path)
        log = Path(record["log"]).open("ab", buffering=0)  # noqa: SIM115 - held for the child's lifetime
        child = subprocess.Popen(
            record["command"],
            cwd=record["cwd"],
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    except (OSError, ValueError, JobError, AttributeError, subprocess.SubprocessError) as error:
        with contextlib.suppress(JobError, OSError):
            _fail(path, f"{type(error).__name__}: {error}")
        return 1
    started = process_start(child.pid)
    me = os.getpid()
    my_start = process_start(me)

    def publish(rec: dict) -> None:
        rec["command_pid"] = child.pid
        rec["command_start"] = started
        rec["wrapper_pid"] = me
        rec["wrapper_start"] = my_start
        rec["groups"] = [g for g in rec["groups"] if g["pid"] != child.pid]
        rec["groups"].append({"pgid": child.pid, "pid": child.pid, "start": started})
        if rec["state"] == "starting":
            rec["state"] = "running"

    try:
        published = update_record(path, publish)
    except (JobError, OSError):
        published = None
    if published is None or published["state"] != "running":
        with contextlib.suppress(OSError):
            os.killpg(child.pid, signal.SIGKILL)
        child.wait()
        return 1
    code = child.wait()
    outcome = f"signal {-code}" if code < 0 else str(code)

    def finish(rec: dict) -> None:
        now = _now()
        rec["state"] = "finished"
        rec["exit"] = "signal 15" if rec["stop_requested"] is not None else outcome
        rec["ended_at"] = _stamp(now)
        rec["ended_epoch"] = now

    try:
        update_record(path, finish)
    except (JobError, OSError):
        return 1
    return 0


# ---------------------------------------------------------------------------
# list and prune
# ---------------------------------------------------------------------------


def read_all(root: Path | None = None) -> list[tuple[str, dict | None]]:
    """(id, record) of every file in the jobs directory; a record that cannot be read is (id, None)."""
    base = state_dir() if root is None else root
    found: list[tuple[str, dict | None]] = []
    try:
        paths = sorted(base.glob("*.json"))
    except OSError:
        return found
    for path in paths:
        try:
            found.append((path.stem, read_record(path)))
        except JobError:
            found.append((path.stem, None))
    return found


def prune(root: Path | None = None, now: float | None = None) -> None:
    """Delete records (with their log, env and lock files) 14 days past their end or, otherwise, their start."""
    base = state_dir() if root is None else root
    current = _now() if now is None else now
    for job_id, record in read_all(base):
        if record is None:
            try:
                expired = (base / f"{job_id}.json").stat().st_mtime + KEEP_SECONDS < current
            except OSError:
                continue
        elif record["state"] == "finished":
            expired = (record["ended_epoch"] or record["started_epoch"]) + KEEP_SECONDS < current
        elif record["started_epoch"] + KEEP_SECONDS < current:
            expired = record["state"] == "failed to start" or effective_state(record, current) == "lost"
        else:
            expired = False
        if expired:
            for suffix in (".json", ".log", ".env", ".json.lock"):
                with contextlib.suppress(OSError):
                    (base / f"{job_id}{suffix}").unlink()
    with contextlib.suppress(OSError):
        for log in base.glob("*.log"):  # a log whose record is gone does not outlive it
            if not (base / f"{log.stem}.json").exists() and log.stat().st_mtime + KEEP_SECONDS < current:
                log.unlink()


def visible(records: list[tuple[str, dict | None]], show_all: bool, now: float) -> list[tuple[str, dict | None, str]]:
    """The (id, record, state) rows `list` shows: running, lost and recent ones; with `show_all`, everything."""
    rows = []
    for job_id, record in records:
        if record is None:
            rows.append((job_id, None, "unreadable"))
            continue
        state = effective_state(record, now)
        if (
            show_all
            or state in ("starting", "running", "lost")
            or (record["ended_epoch"] or record["started_epoch"]) + RECENT_SECONDS >= now
        ):
            rows.append((job_id, record, state))
    return rows


def render_row(job_id: str, record: dict | None, state: str) -> str:
    if record is None:
        return f"{job_id}  unreadable record"
    detail = ""
    if state == "finished":
        detail = f"  exit {record['exit']}  ended {record['ended_at']}"
    elif state == "failed to start":
        detail = f"  {record['error']}"
    command = shlex.join(record["command"])
    if len(command) > 100:
        command = command[:99] + "…"
    return f"{job_id}  {state}  started {record['started_at']}{detail}  {command}"


def list_jobs(show_all: bool, out: Callable[[str], None] = print) -> int:
    root = state_dir()
    prune(root)
    now = _now()
    rows = visible(read_all(root), show_all, now)
    if not rows:
        out("no jobs")
        return 0
    for job_id, record, state in sorted(rows, key=lambda row: row[1]["started_epoch"] if row[1] else 0):
        out(render_row(job_id, record, state))
    return 0


def report_jobs(now: float | None = None) -> list[dict]:
    """Read-only rows for the run report and machine facts: running jobs, jobs lost in the last 24 hours and
    unreadable records. It never prunes or writes."""
    current = _now() if now is None else now
    rows = []
    for job_id, record in read_all():
        if record is None:
            try:
                if (state_dir() / f"{job_id}.json").stat().st_mtime + KEEP_SECONDS < current:
                    continue
            except OSError:
                continue
            rows.append({"id": job_id, "state": "unreadable"})
            continue
        state = effective_state(record, current)
        if state == "lost" and record["started_epoch"] + RECENT_SECONDS < current:
            continue
        if state in ("starting", "running", "lost"):
            rows.append(
                {
                    "id": job_id,
                    "state": state,
                    "command": list(record["command"]),
                    "runner_verb": record["runner_verb"],
                    "command_pid": record["command_pid"],
                    "started_at": record["started_at"],
                }
            )
    return rows


# ---------------------------------------------------------------------------
# stop
# ---------------------------------------------------------------------------


def _signal_pid(pid: int, signum: int) -> None:
    with contextlib.suppress(ProcessLookupError, PermissionError):
        os.kill(pid, signum)


def targets(record: dict) -> dict[int, str]:
    """pid -> start identity of the job's command tree and its recorded process groups, never the wrapper."""
    table = process_table()
    by_pid = {pid: (ppid, pgid, start) for pid, ppid, pgid, start in table}
    found: dict[int, str] = {}
    root = record["command_pid"]
    row = by_pid.get(root)
    if row is not None and row[2] == record["command_start"]:
        found[root] = row[2]
        children: dict[int, list[int]] = {}
        for pid, (ppid, _pgid, _start) in by_pid.items():
            children.setdefault(ppid, []).append(pid)
        pending = [root]
        while pending:
            for child in children.get(pending.pop(), []):
                if child not in found:
                    found[child] = by_pid[child][2]
                    pending.append(child)
    for group in record["groups"]:
        leader = by_pid.get(group["pid"])
        verified = leader is not None and group["start"] is not None and leader[2] == group["start"]
        if not verified:
            continue
        floor = _parse_start(group["start"])
        for pid, (_ppid, pgid, start) in by_pid.items():
            member = _parse_start(start)
            if pgid == group["pgid"] and floor is not None and member is not None and member >= floor:
                found[pid] = start
    found.pop(record["wrapper_pid"], None)
    found.pop(os.getpid(), None)
    return found


def stop(job_id: str, out: Callable[[str], None] = print) -> int:
    """End a running job's command tree: record the request, SIGTERM, then SIGKILL the survivors after the grace."""
    if not ID_RE.fullmatch(job_id):
        raise Refused(f"not a job id: {job_id[:40]}")
    path = state_dir() / f"{job_id}.json"
    try:
        record = read_record(path)
    except JobError as error:
        raise Refused(f"no readable record for job {job_id}: {error}") from None
    state = effective_state(record)
    if state != "running":
        raise Refused(f"job {job_id} is {state}, not running; nothing was signalled")
    if not alive(record["command_pid"], record["command_start"]):
        raise Refused(f"job {job_id}: its command is gone or its process id was reused; nothing was signalled")

    def request(rec: dict) -> None:
        if rec["state"] != "running":
            raise Refused(f"job {job_id} is {rec['state']}, not running; nothing was signalled")
        rec["stop_requested"] = _stamp(_now())

    record = update_record(path, request)  # the request is written before any signal
    first = targets(record)
    for pid in first:
        _signal_pid(pid, signal.SIGTERM)
    deadline = time.monotonic() + STOP_GRACE
    while time.monotonic() < deadline and any(process_start(pid) == start for pid, start in first.items()):
        time.sleep(0.1)
    survivors = {pid: start for pid, start in first.items() if process_start(pid) == start}
    survivors.update(targets(record))
    for pid in survivors:
        _signal_pid(pid, signal.SIGKILL)
    deadline = time.monotonic() + FINISH_WAIT
    while time.monotonic() < deadline:
        if read_record(path)["state"] == "finished":
            out(f"stopped {job_id}")
            return 0
        time.sleep(0.1)
    out(f"signalled {job_id}; the wrapper has not recorded its end yet")
    return 3


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

USAGE = "usage: jobs.py start [--] COMMAND [ARG...] | list [--all] | stop JOB_ID"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(USAGE, file=sys.stderr)
        return 2
    if args[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    verb, rest = args[0], args[1:]
    try:
        if verb == "start":
            command = rest[1:] if rest[:1] == ["--"] else rest
            if not command:
                raise Refused(USAGE)
            return start(command)
        if verb == "list":
            if rest not in ([], ["--all"]):
                raise Refused(USAGE)
            return list_jobs(bool(rest))
        if verb == "stop":
            if len(rest) != 1:
                raise Refused(USAGE)
            return stop(rest[0])
        if verb == "_wrap" and len(rest) == 1:
            return wrap(Path(rest[0]))
        raise Refused(USAGE)
    except Refused as error:
        print(f"jobs: {error}", file=sys.stderr)
        return 2
    except (JobError, OSError, subprocess.TimeoutExpired) as error:
        print(f"jobs: {str(error)[:300]}", file=sys.stderr)
        return 2 if verb == "stop" else 1


if __name__ == "__main__":
    raise SystemExit(main())
