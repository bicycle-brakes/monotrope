"""Resumable state store of the research swarm (Q-13): finished slots survive an aborted run.

The store is runner-owned and lives outside the repository, beside the review loop record:
``record_dir(change)/research/``. One directory per run (its random 128-bit id) holds
``run.json`` and, per slot, ``<slot>.launch.json`` and ``<slot>.result.json``. Every record is
scrubbed, written to a temporary name, flushed, renamed into place and its directory flushed,
so a crash leaves the whole record or none; a reader ignores temporary names and refuses a
record that does not parse or whose own SHA-256 field does not match.

The module knows nothing about models or the dispatcher: callers hand it plain dictionaries.
A slot is reused only when the latest stored run's resume binding, stage, topic, seat,
endpoint, model and exact prompt hash equal the planned slot's, its outcome is ``ok`` and its
report passes the new run's own validation. Nothing is retried, merged or half-reused.
"""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from stage2_research_snapshot import ResearchSnapshotError, changed_against_stored

RUN_ID = re.compile(r"[0-9a-f]{32}")
SLOT_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,119}")
LOCK_NAME = ".lock"
TEMP_PREFIX = ".tmp-"
DISCARD_PREFIX = ".discarded-"
STATES = ("running", "incomplete", "complete")
# The identity a stored result must share with the planned slot, in the order mismatches are named.
SLOT_KEY_FIELDS = ("stage", "topic", "seat", "endpoint", "model", "prompt_sha256")
REUSABLE_OUTCOME = "ok"
STOP_REASON = "state-store-unwritable"


class StoreWriteError(OSError):
    """The store could not be written, read safely or placed safely; the stage stops with exit 1."""

    stage_stop_reason = STOP_REASON
    exit_code = 1


class StoreLocked(RuntimeError):
    """Another run of the same change holds the store lock; explore refuses with exit 2."""

    exit_code = 2


def research_dir(change):
    """``record_dir(change)/research`` without importing the runner (same XDG rule, read at call time)."""
    state = os.environ.get("XDG_STATE_HOME")
    base = Path(state) if state else Path.home() / ".local" / "state"
    return base / "coding-harness" / "stage2" / change / "research"


def _now():
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _canonical(body):
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _seal(body):
    return {**body, "sha256": hashlib.sha256(_canonical(body)).hexdigest()}


def _read_sealed(path):
    """The record, or None for anything missing, truncated, unparseable or unsealed (fail closed)."""
    try:
        data = json.loads(Path(path).read_bytes())
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get("sha256"), str):
        return None
    body = {name: value for name, value in data.items() if name != "sha256"}
    if hashlib.sha256(_canonical(body)).hexdigest() != data["sha256"]:
        return None
    return body


def _fsync_directory(directory):
    fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _scrubbed(value, scrub):
    if isinstance(value, str):
        return scrub(value)
    if isinstance(value, dict):
        return {name: _scrubbed(item, scrub) for name, item in value.items()}
    if isinstance(value, list | tuple):
        return [_scrubbed(item, scrub) for item in value]
    return value


def _slot_id(slot_id):
    if not isinstance(slot_id, str) or not SLOT_ID.fullmatch(slot_id):
        raise StoreWriteError("unsafe slot id for the state store")
    return slot_id


@dataclass(frozen=True)
class Source:
    """The latest stored run as a resume source; ``usable`` False reuses nothing and says why."""

    usable: bool
    run_id: str | None = None
    reasons: list = field(default_factory=list)
    results: dict = field(default_factory=dict)
    interrupted: list = field(default_factory=list)
    run: dict | None = None


@dataclass(frozen=True)
class ReusePlan:
    reused: dict
    not_reused: list  # (slot id or stored label, reason)
    to_launch: list  # the planned slot keys that still need a call, in planned order


class Store:
    """One change's research state directory."""

    def __init__(self, directory, *, scrub: Callable[[str], str] | None = None):
        self.directory = Path(directory)
        self._scrub = scrub
        self._lock_fd = None

    # -- placement --------------------------------------------------------------------------

    def assert_outside(self, *forbidden, home=None):
        """Refuse a store inside (or equal to) any directory a model, the worktree or git may see.

        ``home`` is the real home directory Claude research processes inherit; a store beneath it is refused
        with the way out (Q-15): ``XDG_STATE_HOME`` must point outside it.
        """
        # Resolve ``..`` and parent links before comparing (F-19): a lexical spelling must not slip past.
        mine = Path(os.path.realpath(self.directory))
        if home is not None:
            base = Path(os.path.realpath(home))
            if mine == base or mine.is_relative_to(base) or base.is_relative_to(mine):
                raise StoreWriteError(
                    f"the state store would lie inside the home directory {base}, which Claude research "
                    "processes inherit; set XDG_STATE_HOME to a directory outside it"
                )
        for other in forbidden:
            other = Path(os.path.realpath(other))
            if mine == other or mine.is_relative_to(other) or other.is_relative_to(mine):
                raise StoreWriteError(f"the state store must stay outside {other}")

    def _ensure(self):
        """Create the owner-only directory, or refuse a link, a foreign owner or loose modes."""
        try:
            self.directory.parent.mkdir(parents=True, exist_ok=True)
            with contextlib.suppress(FileExistsError):
                self.directory.mkdir(mode=0o700)
            info = self.directory.lstat()
        except OSError as error:
            raise StoreWriteError(f"cannot create the state store: {error}") from error
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise StoreWriteError("the state store is a link, not ours or not owner-only")

    # -- the lock ---------------------------------------------------------------------------

    def acquire_lock(self):
        """One run per change; the operating system drops the lock when the holder dies."""
        self._ensure()
        try:
            fd = os.open(self.directory / LOCK_NAME, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        except OSError as error:
            raise StoreWriteError(f"cannot open the state store lock: {error}") from error
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            os.close(fd)
            raise StoreLocked("another run of this change holds the research state lock") from error
        self._lock_fd = fd

    def release_lock(self):
        if self._lock_fd is not None:
            os.close(self._lock_fd)
            self._lock_fd = None

    @contextlib.contextmanager
    def locked(self):
        self.acquire_lock()
        try:
            yield self
        finally:
            self.release_lock()

    # -- writing ----------------------------------------------------------------------------

    def _write(self, directory, name, body):
        """Scrub, seal, write to a temporary name, flush, rename, flush the directory."""
        try:
            if self._scrub is not None:
                body = _scrubbed(body, self._scrub)
            data = _canonical(_seal(body))
        except Exception as error:  # an unscrubbable record is never written
            raise StoreWriteError(f"cannot prepare a state store record: {error}") from error
        temporary = directory / f"{TEMP_PREFIX}{secrets.token_hex(8)}-{name}"
        try:
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
            except BaseException:
                with contextlib.suppress(OSError):
                    temporary.unlink()
                raise
            temporary.replace(directory / name)
            _fsync_directory(directory)
        except OSError as error:
            with contextlib.suppress(OSError):
                temporary.unlink()
            raise StoreWriteError(f"cannot write the state store: {error}") from error

    def _run_directory(self, run_id):
        if not isinstance(run_id, str) or not RUN_ID.fullmatch(run_id):
            raise StoreWriteError("invalid run id")
        return self.directory / run_id

    def start_run(self, change, receipt_id, binding, *, run_id=None):
        """Create the run directory and its ``run.json``; returns the new run id."""
        self._ensure()
        run_id = run_id or secrets.token_hex(16)
        directory = self._run_directory(run_id)
        try:
            directory.mkdir(mode=0o700)
        except OSError as error:
            raise StoreWriteError(f"cannot create a run directory: {error}") from error
        self._write(
            directory,
            "run.json",
            {
                "kind": "run",
                "run_id": run_id,
                "change": change,
                "started": _now(),
                "receipt_id": receipt_id,
                "binding": binding,
                "state": "running",
                "refusal": None,
            },
        )
        return run_id

    def _update_run(self, run_id, **changes):
        directory = self._run_directory(run_id)
        run = _read_sealed(directory / "run.json")
        if run is None:
            raise StoreWriteError("the run record is unreadable")
        self._write(directory, "run.json", {**run, **changes})

    def set_append(self, run_id, binding):
        """Record the binding that carries the exact bytes about to be appended to research.md."""
        self._update_run(run_id, binding=binding)

    def finish_run(self, run_id, state, *, refusal=None):
        if state not in STATES:
            raise StoreWriteError("invalid run state")
        self._update_run(run_id, state=state, ended=_now(), refusal=refusal)

    def write_launch(self, run_id, slot_id, record):
        self._write(self._run_directory(run_id), f"{_slot_id(slot_id)}.launch.json", {"kind": "launch", **record})

    def write_result(self, run_id, slot_id, record):
        self._write(self._run_directory(run_id), f"{_slot_id(slot_id)}.result.json", {"kind": "result", **record})

    def adopt(self, run_id, source, record):
        """Copy a reused result into the new run, keeping its original times and leak-check record."""
        body = {name: value for name, value in record.items() if name != "kind"}
        self.write_result(run_id, body["slot_id"], {**body, "reused_from": {"run_id": source.run_id}})

    def clear(self):
        """Remove every stored run (after a complete publication); the lock file stays."""
        try:
            for entry in self.directory.iterdir():
                if entry.name != LOCK_NAME and not entry.is_symlink():
                    shutil.rmtree(entry)
        except FileNotFoundError:
            return
        except OSError as error:
            raise StoreWriteError(f"cannot clear the state store: {error}") from error

    def stage_clear(self):
        """Move every stored run aside; ``commit_clear`` deletes them, ``restore_clear`` brings them back.

        The staging step is the part of clearing that can fail for a reason the run must report, and it
        runs before the record is published (F-28, F-30): a failure here leaves every run in place and
        raises ``StoreWriteError``, and a failed publication restores the runs, so the results stay
        reusable. Returns the staging directory, or None when there is nothing to clear.
        """
        try:
            entries = [e for e in self.directory.iterdir() if e.name != LOCK_NAME and not e.is_symlink()]
        except FileNotFoundError:
            return None
        except OSError as error:
            raise StoreWriteError(f"cannot clear the state store: {error}") from error
        if not entries:
            return None
        staging = self.directory / f"{DISCARD_PREFIX}{secrets.token_hex(8)}"
        moved = []
        try:
            staging.mkdir(mode=0o700)
            for entry in entries:
                entry.rename(staging / entry.name)
                moved.append(entry.name)
        except OSError as error:
            for name in moved:
                with contextlib.suppress(OSError):
                    (staging / name).rename(self.directory / name)
            with contextlib.suppress(OSError):
                staging.rmdir()
            raise StoreWriteError(f"cannot clear the state store: {error}") from error
        return staging

    def restore_clear(self, staging):
        """Undo ``stage_clear``; best effort, a failure leaves the runs unreachable but never wrongly reused."""
        if staging is None:
            return
        with contextlib.suppress(OSError):
            for entry in staging.iterdir():
                entry.rename(self.directory / entry.name)
            staging.rmdir()

    def commit_clear(self, staging):
        """Delete what ``stage_clear`` moved aside, and any staging left by an earlier crash; best effort."""
        with contextlib.suppress(OSError):
            for entry in self.directory.iterdir():
                if entry.name.startswith(DISCARD_PREFIX) and not entry.is_symlink() and entry.is_dir():
                    shutil.rmtree(entry, ignore_errors=True)

    # -- reading ----------------------------------------------------------------------------

    def _run_directories(self):
        try:
            entries = sorted(self.directory.iterdir())
        except OSError:
            return []
        return [
            entry for entry in entries if RUN_ID.fullmatch(entry.name) and entry.is_dir() and not entry.is_symlink()
        ]

    def runs(self):
        """Readable runs, oldest first by start time; unreadable ones are not listed here."""
        runs = []
        for entry in self._run_directories():
            run = _read_sealed(entry / "run.json")
            if run is not None and run.get("run_id") == entry.name:
                runs.append(run)
        return sorted(runs, key=lambda run: (run["started"], run["run_id"]))

    def slot_records(self, run_id):
        """(results by slot id, slot ids with a launch record and no readable result), sorted."""
        directory = self._run_directory(run_id)
        results, launches = {}, set()
        try:
            names = sorted(path.name for path in directory.iterdir())
        except OSError:
            return {}, []
        for name in names:
            if name.startswith(TEMP_PREFIX):
                continue
            slot_id, _, kind = name.rpartition(".")[0].rpartition(".")  # "<slot>.<kind>" from "<slot>.<kind>.json"
            if not name.endswith(".json") or kind not in ("launch", "result") or not SLOT_ID.fullmatch(slot_id):
                continue
            record = _read_sealed(directory / name)
            if kind == "launch":
                launches.add(slot_id)  # even a torn launch record proves the slot was about to start
            elif record is not None and record.get("kind") == "result" and record.get("slot_id") == slot_id:
                results[slot_id] = record
        return results, sorted(launches - set(results))

    def resume_source(self, manifest, research_path, research_bytes):
        """The latest stored run as a source for a new run with this frozen state; nothing older."""
        directories = self._run_directories()
        runs = self.runs()
        unreadable = [
            entry.name
            for entry in directories
            if (entry / "run.json").exists() and entry.name not in {run["run_id"] for run in runs}
        ]
        if unreadable:
            return Source(False, reasons=["unreadable run record " + ", ".join(unreadable) + ": nothing is reused"])
        if not runs:
            return Source(False, reasons=["no stored run"])
        latest = runs[-1]
        run_id = latest["run_id"]
        results, interrupted = self.slot_records(run_id)
        base = {"run_id": run_id, "results": results, "interrupted": interrupted, "run": latest}
        reasons = []
        refused = [slot for slot, record in sorted(results.items()) if record.get("outcome") == "refused"]
        if latest.get("refusal"):
            refusal = latest["refusal"]
            reasons.append(
                f"run {run_id} recorded a refused slot (security refusal) at {refusal.get('slot')}: {refusal.get('reason')}"
            )
        for slot in refused:
            reason = (
                (results[slot].get("leak_check") or {}) if isinstance(results[slot].get("leak_check"), dict) else {}
            )
            reasons.append(
                f"run {run_id} recorded a refused slot (security refusal) at {slot}" + (f": {reason}" if reason else "")
            )
        if latest.get("state") == "complete":
            reasons.append(f"run {run_id} was published complete")
        if reasons:
            return Source(False, reasons=reasons, **base)
        try:
            changed = changed_against_stored(manifest, research_path, research_bytes, latest["binding"])
        except (ResearchSnapshotError, KeyError, TypeError):
            return Source(False, reasons=[f"run {run_id} has an unreadable binding"], **base)
        if changed:
            return Source(False, reasons=["binding changed: " + ", ".join(changed)], **base)
        return Source(True, **base)


def plan_reuse(source, planned, validate):
    """Split the planned slots (dicts with ``slot_id`` and the key fields) into reused and to-launch.

    ``validate(record)`` is the new run's own report validation. Every stored result that is not
    reused is named with its reason, so a silent discard cannot happen.
    """
    planned = list(planned)
    if not source.usable:
        return ReusePlan({}, [], planned)
    reused, named = {}, []
    ids = {slot["slot_id"] for slot in planned}
    for slot in planned:
        record = source.results.get(slot["slot_id"])
        if record is None:
            if slot["slot_id"] in source.interrupted:
                named.append((slot["slot_id"], "interrupted"))
            continue
        mismatch = next((name for name in SLOT_KEY_FIELDS if record.get(name) != slot.get(name)), None)
        if mismatch is not None:
            named.append((slot["slot_id"], mismatch.replace("_sha256", "")))
        elif record.get("outcome") != REUSABLE_OUTCOME:
            named.append((slot["slot_id"], "outcome"))
        elif not _valid(validate, record):
            named.append((slot["slot_id"], "validation"))
        else:
            reused[slot["slot_id"]] = record
    for slot_id in sorted(set(source.results) - ids):
        named.append((slot_id, "not planned"))
    return ReusePlan(reused, named, [slot for slot in planned if slot["slot_id"] not in reused])


def _valid(validate, record):
    try:
        return bool(validate(record))
    except Exception:
        return False
