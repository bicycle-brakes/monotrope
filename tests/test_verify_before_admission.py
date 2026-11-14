"""The cheap-before-admission proofs: cheap red never waits, protected work keeps its one lock.

Every case here builds its own checkout, gate list and state root (bead
coding-harness-bxxt.6): a git-initialized tree with a synthetic schema-3 gate
file, marker gates whose commands live outside the checkout (so the proofs
measure real input edits, never their own logs), and a holder admission in a
separate process for real isolated contention. No network, no models, no
shared machine lock.
"""

from __future__ import annotations

import contextlib
import fcntl
import io
import json
import os
import selectors
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import ci_gates  # noqa: E402
import verify_duration  # noqa: E402
import verify_lock  # noqa: E402
import verify_run  # noqa: E402
import yaml  # noqa: E402

# The mechanism files the kit transfers; the recipient proof copies exactly these.
KIT_MECHANISM = (
    "scripts/ci_gates.py",
    "scripts/verify_run.py",
    "scripts/verify_lock.py",
    "scripts/verify_duration.py",
    "scripts/verify_all.sh",
)

# The marker gate's body: it records the queue it saw, the admission marker it
# carried and whether the holder had already let go, then exits with the code
# its argv names — or with the control file's code, so one gate list can be
# driven red and green between runs. The queue reading is the proof's heart: a
# gate that runs while another admission holds must see an empty queue, or
# somebody took admission before the cheap work was done.
GATE_BODY = """
import json, os, sys, time
from pathlib import Path
name = sys.argv[1]
wanted = int(sys.argv[2])
sleep = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
queue = Path(os.environ["XDG_STATE_HOME"]) / "coding-harness" / "verify.queue"
names = sorted(p.name for p in queue.iterdir()) if queue.is_dir() else []
entry = {
    "gate": name,
    "queue": names,
    "held": os.environ.get("HARNESS_VERIFY_LOCK_HELD", ""),
    "released": Path(os.environ["RELEASED_MARKER"]).exists(),
}
if len(sys.argv) > 4:
    Path(sys.argv[4]).write_text("written by the gate itself", encoding="utf-8")
with open(os.environ["GATE_LOG"], "a", encoding="utf-8") as handle:
    handle.write(json.dumps(entry) + chr(10))
time.sleep(sleep)
exit_code = wanted
control = os.environ.get("GATE_EXIT_FILE", "")
if control and Path(control).exists():
    exit_code = int(Path(control).read_text().strip() or wanted)
sys.exit(exit_code)
"""

# The holder body: one real admission in a separate process, released only
# when the release marker appears (or after a minute, so a broken proof fails
# instead of hanging the suite).
HOLDER_BODY = """
import os, sys, time
from pathlib import Path
sys.path.insert(0, os.environ["SCRIPTS_DIR"])
import verify_lock
with verify_lock.hold_admission(["holder"]) as owned:
    Path(os.environ["HELD_MARKER"]).write_text("held")
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline and not Path(os.environ["RELEASE_MARKER"]).exists():
        time.sleep(0.02)
    Path(os.environ["RELEASED_MARKER"]).write_text("released")
"""

# One protected gate that leaves a grandchild behind: the spawner exits, its
# own python keeps sleeping in the gate's process group — the scheduler must
# end it before the admission is released.
SPAWNER_BODY = """
import os, subprocess, sys
from pathlib import Path
child = subprocess.Popen(
    [sys.executable, "-c", "import time; time.sleep(30)"],
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
Path(os.environ["GRANDCHILD_MARKER"]).write_text(str(child.pid), encoding="utf-8")
"""


def _git(root: Path, *args: str) -> None:
    env = dict(os.environ)
    env.update(
        {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "commit.gpgsign",
            "GIT_CONFIG_VALUE_0": "false",
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@example.com",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@example.com",
        }
    )
    subprocess.run(["git", *args], cwd=root, env=env, check=True, capture_output=True, text=True)


def _git_init_commit(root: Path) -> None:
    _git(root, "init", "--quiet")
    (root / "README.md").write_text("a fixture checkout\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "--quiet", "--allow-empty", "-m", "base")


def write_gates(root: Path, gates: list[dict]) -> None:
    """One synthetic gate file for the checkout, schema 3."""
    doc = {"schema_version": 3, "tools": {"python": ["3.12"]}, "gates": gates}
    folder = root / "decisions"
    folder.mkdir(exist_ok=True)
    (folder / "gates.yaml").write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _gate(gid: str, command: str, *, cost: str = "seconds", enforcement: str = "block", **extra: object) -> dict:
    return {
        "id": gid,
        "title": gid,
        "command": command,
        "job": "verify",
        "enforcement": enforcement,
        "cost": cost,
        "floor": False,
        "placement": "both",
        "reason": "a marker gate of the proof",
        **extra,
    }


@pytest.fixture
def checkout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    """An isolated git checkout with its own state root, marker log and holder markers."""
    root = tmp_path / "checkout"
    root.mkdir()
    markers = tmp_path / "markers"
    markers.mkdir()
    (tmp_path / "home").mkdir()
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("HARNESS_VERIFY_MEMORY_FLOOR", "0")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("GATE_LOG", str(markers / "gates.log"))
    monkeypatch.setenv("RELEASED_MARKER", str(markers / "released"))
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.TOKEN_ENV, raising=False)
    monkeypatch.delenv(verify_lock.ADMISSION_ID_ENV, raising=False)
    monkeypatch.delenv(verify_lock.ADMISSION_WAIT_ENV, raising=False)
    _git_init_commit(root)
    return SimpleNamespace(root=root, markers=markers, tmp_path=tmp_path, monkeypatch=monkeypatch)


@pytest.fixture
def gate_script(tmp_path: Path) -> Path:
    """The marker gate script, outside every checkout it measures."""
    path = tmp_path / "bin" / "gate.py"
    path.parent.mkdir()
    path.write_text(GATE_BODY, encoding="utf-8")
    return path


def _read_log() -> list[dict]:
    log = Path(os.environ["GATE_LOG"])
    if not log.exists():
        return []
    text = log.read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _wait_log_gate(name: str, timeout: float = 60.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if any(entry["gate"] == name for entry in _read_log()):
            return
        time.sleep(0.02)
    raise AssertionError(f"the gate {name} never ran")


def _wait_marker(path: Path, timeout: float = 30.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists():
            return
        time.sleep(0.02)
    raise AssertionError(f"the marker never appeared: {path}")


def _wait_queued(timeout: float = 30.0) -> None:
    """Wait until the scheduler has registered in the admission queue — the wait has begun."""
    queue = Path(os.environ["XDG_STATE_HOME"]) / "coding-harness" / "verify.queue"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if queue.is_dir() and any(queue.iterdir()):
            return
        time.sleep(0.02)
    raise AssertionError("the scheduler never queued for admission")


def _release(checkout: SimpleNamespace) -> None:
    (checkout.markers / "release").write_text("release", encoding="utf-8")


def start_holder(checkout: SimpleNamespace) -> subprocess.Popen[bytes]:
    """One real admission in a separate process, against the checkout's state root."""
    env = dict(os.environ)
    env["SCRIPTS_DIR"] = str(REPO_ROOT / "scripts")
    env["HELD_MARKER"] = str(checkout.markers / "held")
    env["RELEASE_MARKER"] = str(checkout.markers / "release")
    proc = subprocess.Popen(
        [sys.executable, "-c", HOLDER_BODY],
        cwd=REPO_ROOT,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _wait_marker(checkout.markers / "held")
    return proc


@contextlib.contextmanager
def scheduler_run(root: Path, **kwargs: object):
    """One scheduler run in a thread, joined with a bound: a blocked run fails the proof."""
    outcome: dict[str, object] = {}

    def body() -> None:
        out, err = io.StringIO(), io.StringIO()
        try:
            result = verify_run.run_verification(
                root,
                out=out,
                err=err,
                python=sys.executable,
                **kwargs,  # type: ignore[arg-type]
            )
            outcome["value"] = (result, out.getvalue(), err.getvalue())
        except Exception as error:  # the thread's failure is the proof's failure
            outcome["error"] = error

    thread = threading.Thread(target=body, daemon=True)
    thread.start()
    try:
        yield outcome
    finally:
        thread.join(timeout=60)
        assert not thread.is_alive(), "the scheduler blocked where it must not wait"
        if "error" in outcome:
            raise outcome["error"]  # type: ignore[misc]


def run_scheduler(root: Path, **kwargs: object):
    """One straight scheduler run in the calling thread."""
    out, err = io.StringIO(), io.StringIO()
    result = verify_run.run_verification(root, out=out, err=err, python=sys.executable, **kwargs)  # type: ignore[arg-type]
    return result, out.getvalue(), err.getvalue()


def _history(state: Path) -> list[dict]:
    path = Path(state) / "coding-harness" / verify_duration.HISTORY_NAME
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _admission_spy(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    """Count the admissions the scheduler requests, around the real one."""
    calls: list[list[str]] = []
    real = verify_lock.hold_admission

    def spy(command: list[str]):
        calls.append([str(word) for word in command])
        return real(command)

    monkeypatch.setattr(verify_lock, "hold_admission", spy)
    return calls


def test_admission_metadata_is_validated_and_cost_derived(checkout: SimpleNamespace) -> None:
    """An invalid `needs_admission` is a schema error, and effective protection derives from cost.

    Planted fault: a non-boolean mark is accepted, `needs_admission: false` exempts a minutes gate, or
    an unmarked seconds gate is classified as protected.
    """
    base = {
        "id": "g",
        "title": "g",
        "command": "echo g",
        "job": "verify",
        "enforcement": "block",
        "cost": "seconds",
        "floor": False,
        "placement": "both",
        "reason": "a metadata probe",
    }
    for bad in ("yes", "true", 1, None):
        doc = dict(base, needs_admission=bad)
        errors = ci_gates.validate_schema({"schema_version": 3, "tools": {"python": ["3.12"]}, "gates": [doc]})
        assert errors, f"needs_admission={bad!r} must be refused by the schema"
        assert any("needs_admission" in error for error in errors), errors
    assert ci_gates.validate_schema({"schema_version": 3, "tools": {"python": ["3.12"]}, "gates": [dict(base)]}) == []

    write_gates(
        checkout.root,
        [
            dict(base, id="quick"),
            dict(base, id="marked", needs_admission=True),
            dict(base, id="heavy", cost="minutes", needs_admission=False),
            dict(base, id="plain", cost="minutes"),
        ],
    )
    records = {str(g["id"]): g for g in ci_gates.gates_at(checkout.root)}
    assert records["quick"]["needs_admission"] is False and records["quick"]["admission"] is False
    assert records["marked"]["needs_admission"] is True and records["marked"]["admission"] is True
    # False cannot exempt a minutes gate: the cost decides, the flag only adds.
    assert records["heavy"]["needs_admission"] is False and records["heavy"]["admission"] is True
    assert records["plain"]["admission"] is True
    selection = [str(g["id"]) for g in ci_gates.selection_at(checkout.root, "verify")]
    assert selection == ["quick", "marked", "heavy", "plain"]


def test_all_cheap_failures_finish_without_queueing(checkout: SimpleNamespace, gate_script: Path) -> None:
    """Both cheap gates run to their diagnostics while a holder keeps the slot; the heavy gate waits.

    Planted fault: the run stops at the first cheap red, registers in the admission queue before the
    last cheap gate, or runs the protected gate after a cheap blocking failure.
    """
    write_gates(
        checkout.root,
        [
            _gate("cheap-one", f"python3 {gate_script} cheap-one 1"),
            _gate("cheap-two", f"python3 {gate_script} cheap-two 1"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    holder = start_holder(checkout)
    try:
        result, out, err = run_scheduler(checkout.root)
        assert result.exit_code == 1, (result, out, err)
        entries = _read_log()
        assert [entry["gate"] for entry in entries] == ["cheap-one", "cheap-two"], entries
        # The heart of the proof: while the holder held, no cheap gate saw a queue entry.
        assert all(entry["queue"] == [] for entry in entries), entries
        assert "──   [heavy] not run" in out, out
        assert "VERIFY RED" in out, out
        assert holder.poll() is None, "the holder must stay alive through the cheap pass"
    finally:
        _release(checkout)
        holder.wait(timeout=30)
    # And the failure named every protected gate it did not execute — only that one.
    assert "──   [cheap-one] not run" not in out, out
    assert "──   [cheap-two] not run" not in out, out


def test_only_protected_work_enters_one_admission(checkout: SimpleNamespace, gate_script: Path, monkeypatch) -> None:
    """One admission covers the whole protected set; the cheap gate runs before it, unlocked.

    Planted fault: one admission per protected gate, a protected gate outside the holder, or the cheap
    gate run under the lock.
    """
    write_gates(
        checkout.root,
        [
            _gate("cheap", f"python3 {gate_script} cheap 0"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
            _gate("heavy-two", f"python3 {gate_script} heavy-two 0", cost="minutes"),
        ],
    )
    calls = _admission_spy(monkeypatch)
    holder = start_holder(checkout)
    try:
        with scheduler_run(checkout.root) as outcome:
            _wait_log_gate("cheap")
            _wait_queued()
            _release(checkout)
        result, out, err = outcome["value"]
        assert result.exit_code == 0, (result, out, err)
        # One admission, requested once, for the whole protected set.
        assert calls == [["verify-run", "verify"]], calls
        entries = _read_log()
        assert [entry["gate"] for entry in entries] == ["cheap", "heavy", "heavy-two"], entries
        assert entries[0]["released"] is False, entries
        assert entries[1]["released"] is True and entries[2]["released"] is True, entries
        # The protected gates carry the admission marker; the cheap one carries none.
        assert entries[0]["held"] == "", entries
        assert entries[1]["held"].isdigit() and entries[2]["held"].isdigit(), entries
        assert entries[0]["queue"] == [], entries
        assert "VERIFY GREEN" in out, out
    finally:
        _release(checkout)
        holder.wait(timeout=30)


def test_seconds_only_jobs_never_request_admission(checkout: SimpleNamespace, monkeypatch) -> None:
    """A docs-only run executes its gates and states, in history and output, that no admission was asked.

    Planted fault: an empty protected set still requests admission, or the completion record omits
    that none was requested.
    """
    write_gates(
        checkout.root,
        [
            _gate("docs-a", "echo docs-a", subsets=["docs"]),
            _gate("docs-b", "echo docs-b", subsets=["docs"]),
            _gate("heavy", "echo heavy", cost="minutes"),
        ],
    )
    calls = _admission_spy(monkeypatch)
    result, out, err = run_scheduler(checkout.root, job="docs")
    assert result.exit_code == 0, (result, out, err)
    assert calls == [], calls
    assert "── [docs-a] gruen" in out and "── [docs-b] gruen" in out, out
    assert "no admission was requested" in out, out
    end = [event for event in _history(checkout.tmp_path / "state") if event["event"] == "run_end"][-1]
    assert end["admission_requested"] is False, end
    assert end["admission_id"] is None and end["admission_wait_seconds"] is None, end


def test_unchanged_tree_reuses_cheap_results(checkout: SimpleNamespace, gate_script: Path) -> None:
    """A stable tree across the wait reuses the cheap pass: the cheap gate runs once, not twice.

    Planted fault: the cheap gates rerun inside the admission although the tree is unchanged.
    """
    write_gates(
        checkout.root,
        [
            _gate("cheap", f"python3 {gate_script} cheap 0"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    holder = start_holder(checkout)
    try:
        with scheduler_run(checkout.root) as outcome:
            _wait_log_gate("cheap")
            _wait_queued()
            _release(checkout)
        result, out, err = outcome["value"]
        assert result.exit_code == 0, (result, out, err)
        entries = _read_log()
        assert [entry["gate"] for entry in entries] == ["cheap", "heavy"], entries
        assert entries[0]["released"] is False and entries[1]["released"] is True, entries
        assert "VERIFY GREEN" in out, out
    finally:
        _release(checkout)
        holder.wait(timeout=30)


def test_changed_tree_refreshes_selection_and_rechecks(checkout: SimpleNamespace, gate_script: Path) -> None:
    """A tree that moved while queued reruns the complete cheap set from the reloaded list, inside the lock.

    Planted fault: an edit to an already dirty file during the wait is missed, or the stale gate list
    is reused after a reclassification.
    """
    tracked = checkout.root / "tracked.txt"
    tracked.write_text("first\n", encoding="utf-8")
    write_gates(
        checkout.root,
        [
            _gate("cheap-a", f"python3 {gate_script} cheap-a 0"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    _git(checkout.root, "add", ".")
    _git(checkout.root, "commit", "--quiet", "-m", "gates")
    # The file is already dirty; the later edit changes its content without changing porcelain status.
    tracked.write_text("first\nsecond\n", encoding="utf-8")

    holder = start_holder(checkout)
    try:
        with scheduler_run(checkout.root) as outcome:
            _wait_log_gate("cheap-a")
            _wait_queued()
            tracked.write_text("first\nsecond\nthird\n", encoding="utf-8")
            write_gates(
                checkout.root,
                [
                    _gate("cheap-a", f"python3 {gate_script} cheap-a 0"),
                    _gate("cheap-b", f"python3 {gate_script} cheap-b 0"),
                    _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
                ],
            )
            _release(checkout)
        result, out, err = outcome["value"]
        assert result.exit_code == 0, (result, out, err)
        entries = _read_log()
        # cheap-a ran twice — once before the wait, once inside the held admission;
        # cheap-b exists only in the refreshed list, so its frame proves the reselection.
        assert [entry["gate"] for entry in entries] == ["cheap-a", "cheap-a", "cheap-b", "heavy"], entries
        assert entries[0]["released"] is False, entries
        assert all(entry["released"] for entry in entries[1:]), entries
        assert "── [cheap-b] gruen" in out, out
        assert "── [heavy] gruen" in out, out
        assert "VERIFY GREEN" in out, out
    finally:
        _release(checkout)
        holder.wait(timeout=30)


def test_two_phases_share_history_and_exclude_wait(checkout: SimpleNamespace, gate_script: Path) -> None:
    """One identity spans both phases: every execution is recorded, the queue wait stays out of the seconds.

    Planted fault: a second run identity at admission, a repeated cheap execution left unrecorded, or the
    queue wait counted as execution time.
    """
    tracked = checkout.root / "tracked.txt"
    tracked.write_text("first\n", encoding="utf-8")
    write_gates(
        checkout.root,
        [
            _gate("cheap-a", f"python3 {gate_script} cheap-a 0"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    _git(checkout.root, "add", ".")
    _git(checkout.root, "commit", "--quiet", "-m", "gates")
    tracked.write_text("first\nsecond\n", encoding="utf-8")

    # One clock step per reading: every gate segment consumes exactly two readings and measures
    # one second, so the recorded run seconds are the segments' sum and nothing else — a wait
    # charged to execution would push the sum past four seconds on this very holder.
    readings = {"now": 0.0}

    def fake_clock() -> float:
        readings["now"] += 1.0
        return readings["now"]

    holder = start_holder(checkout)
    try:
        with scheduler_run(checkout.root, clock=fake_clock) as outcome:
            _wait_log_gate("cheap-a")
            _wait_queued()
            # The tree moves while queued: the complete cheap set reruns inside the held admission,
            # so the history must carry the repeated cheap gate under the same run identity.
            tracked.write_text("first\nsecond\nthird\n", encoding="utf-8")
            write_gates(
                checkout.root,
                [
                    _gate("cheap-a", f"python3 {gate_script} cheap-a 0"),
                    _gate("cheap-b", f"python3 {gate_script} cheap-b 0"),
                    _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
                ],
            )
            time.sleep(0.25)  # a real, measurable wait — never a claimed one
            _release(checkout)
        result, out, err = outcome["value"]
        assert result.exit_code == 0, (result, out, err)

        events = _history(checkout.tmp_path / "state")
        starts = [event for event in events if event["event"] == "run_start"]
        assert len(starts) == 1, events  # admission must not start a second run identity
        run_id = starts[0]["run_id"]
        gates = [event for event in events if event["event"] == "gate" and event["run_id"] == run_id]
        assert [event["gate"] for event in gates] == ["cheap-a", "cheap-a", "cheap-b", "heavy"], gates
        ends = [event for event in events if event["event"] == "run_end" and event["run_id"] == run_id]
        assert len(ends) == 1, events
        end = ends[0]
        # Four segments of one clock step each: the holder's real wait (well past the 0.25 s sleep)
        # is recorded beside them, never inside them.
        assert end["seconds"] == pytest.approx(4.0), (end, gates)
        assert end["admission_requested"] is True, end
        assert end["admission_wait_seconds"] is not None and end["admission_wait_seconds"] > 0, end
        assert "execution 4.000s" in out, out
    finally:
        _release(checkout)
        holder.wait(timeout=30)


def test_unmeasurable_inputs_refuse_reuse(checkout: SimpleNamespace, gate_script: Path) -> None:
    """A failed selection, an unreadable tree and an unstable cheap pass all refuse before any green.

    Planted fault: an empty or failed selection reports green, or an unmeasurable or changing tree is
    accepted as a stable baseline.
    """
    # An empty gate list is a configuration error, not a green run.
    write_gates(checkout.root, [])
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 2, (result, out, err)
    assert "liess sich nicht erzeugen" in err, err
    # A selection that selects nothing is the same refusal.
    write_gates(checkout.root, [_gate("far", "echo far", placement="hosted")])
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 2, (result, out, err)
    assert "ist leer" in err, err

    # An unreadable tree entry refuses the measurement before any gate runs.
    write_gates(
        checkout.root,
        [
            _gate("cheap", f"python3 {gate_script} cheap 0"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    victim = checkout.root / "tracked.txt"
    victim.write_text("readable\n", encoding="utf-8")
    _git(checkout.root, "add", ".")
    _git(checkout.root, "commit", "--quiet", "-m", "tracked")
    victim.unlink()
    os.mkfifo(victim)
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 2, (result, out, err)
    assert "cannot be measured" in err, err
    assert _read_log() == [], "no gate may run on an unmeasurable tree"
    victim.unlink()
    victim.write_text("readable\n", encoding="utf-8")

    # A cheap gate that writes into the checkout makes its own baseline unstable: refuse, never accept.
    writer = f"python3 {gate_script} cheap 0 0 {checkout.root}/side-file"
    write_gates(
        checkout.root, [_gate("cheap", writer), _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes")]
    )
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 2, (result, out, err)
    assert "changed while the cheap gates ran" in err, err
    # The refusal names what moved and ends with the run's account (review rows L2-1, L2-2).
    assert "changed: side-file (untracked)" in err, err
    assert "── not run — the run was refused before these gates:" in out, out
    assert "──   [heavy] not run" in out, out
    assert verify_run.BANNER_REFUSED in out and "VERIFY GREEN" not in out, out
    assert result.not_run == ["heavy"] and result.exit_code == 2, result


def test_enforcement_and_ci_exhaustiveness_survive_partitioning(checkout: SimpleNamespace, gate_script: Path) -> None:
    """Only `block` stops; the local protected phase stops at its first blocking failure; `--ci` exhausts.

    Planted fault: a report-level red suppresses the protected work, a later protected gate runs after a
    local blocking red, or `--ci` omits a gate after an earlier failure.
    """
    # A report gate that fails speaks up without blocking the protected phase.
    write_gates(
        checkout.root,
        [
            _gate("loud", f"python3 {gate_script} loud 1", enforcement="report"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 0, (result, out, err)
    assert "rot, aber nur report" in out, out
    assert "── [heavy] gruen" in out, out
    assert "VERIFY GREEN" in out, out

    # Locally, a cheap blocking failure keeps the heavy gate from running and names it.
    write_gates(
        checkout.root,
        [
            _gate("cheap-red", f"python3 {gate_script} cheap-red 1"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 1, (result, out, err)
    assert "──   [heavy] not run" in out, out
    assert "VERIFY RED" in out, out

    # The same shape under --ci stays exhaustive: every selected gate of both phases ran.
    result, out, err = run_scheduler(checkout.root, ci=True)
    assert result.exit_code == 1, (result, out, err)
    ran = [entry["gate"] for entry in _read_log()]
    assert ran[-2:] == ["cheap-red", "heavy"], ran
    assert "not run" not in out, out
    assert "VERIFY RED" in out, out

    # Inside the protected phase, the first blocking failure stops the rest of it.
    write_gates(
        checkout.root,
        [
            _gate("cheap", f"python3 {gate_script} cheap 0"),
            _gate("heavy-one", f"python3 {gate_script} heavy-one 1", cost="minutes"),
            _gate("heavy-two", f"python3 {gate_script} heavy-two 0", cost="minutes"),
        ],
    )
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 1, (result, out, err)
    ran = [entry["gate"] for entry in _read_log()]
    assert "heavy-two" not in ran, ran
    assert "──   [heavy-two] not run" in out, out


def test_nested_refused_and_interrupted_protected_work(
    checkout: SimpleNamespace, gate_script: Path, monkeypatch
) -> None:
    """A forged marker queues like anyone; a valid one nests; a lingering grandchild is ended first.

    Planted fault: a forged marker skips the queue, a valid marker queues behind its own ancestor, or
    the admission is released while a protected grandchild still runs.
    """
    calls = _admission_spy(monkeypatch)
    # A forged marker (a pid nobody published with this token) is refused back to ordinary admission.
    monkeypatch.setenv(verify_lock.LOCK_ENV, "999999")
    monkeypatch.setenv(verify_lock.TOKEN_ENV, "forged-token")
    write_gates(
        checkout.root,
        [
            _gate("cheap", f"python3 {gate_script} cheap 0"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    holder = start_holder(checkout)
    try:
        with scheduler_run(checkout.root) as outcome:
            _wait_log_gate("cheap")
            _wait_queued()
            _release(checkout)
        result, out, err = outcome["value"]
        assert result.exit_code == 0, (result, out, err)
        assert calls == [["verify-run", "verify"]], calls
        entries = _read_log()
        assert entries[-1]["released"] is True, entries  # it waited for the holder like any fresh entry
        assert entries[-1]["held"].isdigit(), entries
    finally:
        _release(checkout)
        holder.wait(timeout=30)

    # A valid marker nests: no queue, no wait, the protected work runs while the holder still holds.
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.TOKEN_ENV, raising=False)
    token = "nested-proof-token"
    lock_root = Path(os.environ["XDG_STATE_HOME"]) / "coding-harness"
    lock_root.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(lock_root / verify_lock.LOCK_NAME, os.O_RDWR | os.O_CREAT | os.O_NONBLOCK, 0o600)
    (lock_root / verify_lock.HOLDER_NAME).write_text(
        json.dumps({"pid": os.getpid(), "token": token, "command": ["proof"], "start": "2026-11-13T00:00:00"}),
        encoding="utf-8",
    )
    calls.clear()
    # The first holder's "released" marker would otherwise read as released for this held phase.
    (checkout.markers / "released").unlink(missing_ok=True)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
        monkeypatch.setenv(verify_lock.TOKEN_ENV, token)
        result, out, err = run_scheduler(checkout.root)
        assert result.exit_code == 0, (result, out, err)
        assert calls == [["verify-run", "verify"]], calls
        entries = _read_log()
        assert entries[-1]["gate"] == "heavy" and entries[-1]["released"] is False, entries
        assert "VERIFY GREEN" in out, out
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)
        with contextlib.suppress(OSError):
            (lock_root / verify_lock.HOLDER_NAME).unlink()
    monkeypatch.delenv(verify_lock.LOCK_ENV, raising=False)
    monkeypatch.delenv(verify_lock.TOKEN_ENV, raising=False)

    # A protected gate that leaves a grandchild: the scheduler ends it before the admission exits.
    spawner = checkout.tmp_path / "bin" / "spawner.py"
    spawner.parent.mkdir(exist_ok=True)
    spawner.write_text(SPAWNER_BODY, encoding="utf-8")
    monkeypatch.setenv("GRANDCHILD_MARKER", str(checkout.markers / "grandchild"))
    write_gates(
        checkout.root,
        [
            _gate("cheap", f"python3 {gate_script} cheap 0"),
            _gate("heavy", f"python3 {spawner} heavy 0", cost="minutes"),
        ],
    )
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 0, (result, out, err)
    grandchild = int((checkout.markers / "grandchild").read_text().strip())
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            os.kill(grandchild, 0)
        except ProcessLookupError:
            break
        time.sleep(0.05)
    else:
        raise AssertionError("the grandchild outlived the admission")


def test_transferred_kit_keeps_before_admission_behavior(checkout: SimpleNamespace, tmp_path: Path) -> None:
    """A recipient checkout with renamed gates runs two-phase, with no source-tree import and no opt-out.

    Planted fault: the transferred scheduler classifies by gate id or needs a file the kit does not carry.
    """
    recipient = tmp_path / "recipient"
    (recipient / "scripts").mkdir(parents=True)
    for relative in KIT_MECHANISM:
        shutil.copy(REPO_ROOT / relative, recipient / relative)
    control = tmp_path / "gate_exit"
    control.write_text("1", encoding="utf-8")
    gate = tmp_path / "bin" / "gate.py"
    gate.parent.mkdir(exist_ok=True)
    gate.write_text(GATE_BODY, encoding="utf-8")
    write_gates(
        recipient,
        [
            _gate("lint-quick", f"python3 {gate} lint-quick 0"),
            _gate("suite-full", f"python3 {gate} suite-full 0", cost="minutes"),
        ],
    )
    _git_init_commit(recipient)

    def child_env() -> dict[str, str]:
        env = {
            key: value
            for key, value in os.environ.items()
            if key not in ("PYTHONPATH", verify_lock.LOCK_ENV, verify_lock.TOKEN_ENV)
        }
        env["HARNESS_VERIFY_MEMORY_FLOOR"] = "0"
        # A plausible opt-out switch: the behavior must not change, because none exists.
        env["HARNESS_VERIFY_WHOLE_RUN"] = "1"
        env["GATE_EXIT_FILE"] = str(control)
        return env

    def run_once() -> tuple[int, str, str]:
        proc = subprocess.Popen(
            [sys.executable, "scripts/verify_run.py", "--job", "verify"],
            cwd=recipient,
            env=child_env(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        out, err = proc.communicate(timeout=120)
        return proc.returncode, out, err

    holder = start_holder(checkout)
    try:
        code, out, err = run_once()
        assert code == 1, (code, out, err)
        assert "── [lint-quick] RED (block)" in out, out
        assert "──   [suite-full] not run" in out, out
        assert "VERIFY RED" in out, out
        entries = [json.loads(line) for line in Path(os.environ["GATE_LOG"]).read_text().splitlines() if line.strip()]
        assert [entry["gate"] for entry in entries] == ["lint-quick"], entries
        assert entries[0]["queue"] == [], entries
        assert holder.poll() is None, "the holder stayed alive through the recipient's cheap pass"
    finally:
        _release(checkout)
        holder.wait(timeout=30)

    control.write_text("0", encoding="utf-8")
    code, out, err = run_once()
    assert code == 0, (code, out, err)
    assert "── [lint-quick] gruen" in out and "── [suite-full] gruen" in out, out
    assert "VERIFY GREEN" in out, out


@pytest.mark.parametrize("interrupted", [False, True])
def test_gate_leader_exit_closes_inherited_streams(tmp_path: Path, interrupted: bool) -> None:
    """A child retaining the gate's pipes must be killed before waiting for EOF."""
    group_file = tmp_path / "gate-group"
    body = (
        "import os, subprocess, sys, time; from pathlib import Path; "
        f"Path({str(group_file)!r}).write_text(str(os.getpgrp())); "
        "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)']); "
        "print('before-child', flush=True); " + ("time.sleep(30)" if interrupted else "sys.exit(0)")
    )
    command = f"python3 -c {shlex.quote(body)}"
    script = f"""
import sys
from pathlib import Path
sys.path.insert(0, {str(REPO_ROOT / "scripts")!r})
import verify_run
verify_run._install_run_handlers()
try:
    verify_run.gate_process(Path({str(tmp_path)!r}), sys.executable, {{'fd': None}}, {{}},
        {command!r}, dict(__import__('os').environ))
except verify_run.GateInterrupted as error:
    sys.exit(128 + error.signum)
"""
    proc = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        prefix = b""
        if interrupted:
            # Output must arrive while the leader is still running; a later
            # interruption must not discard what the gate already printed.
            with selectors.DefaultSelector() as selector:
                selector.register(proc.stdout, selectors.EVENT_READ)
                assert selector.select(timeout=5), "gate output must stream before its leader exits"
                prefix = proc.stdout.readline()
            assert prefix == b"before-child\n" and proc.poll() is None
            proc.send_signal(signal.SIGTERM)
        stdout, stderr = proc.communicate(timeout=18)
    except subprocess.TimeoutExpired:
        pytest.fail("the gate leader exited but its child's inherited pipes prevented cleanup")
    finally:
        if proc.poll() is None:
            proc.kill()
        if group_file.exists():
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(int(group_file.read_text()), signal.SIGKILL)
        proc.communicate(timeout=8)
    assert proc.returncode == (128 + signal.SIGTERM if interrupted else 0), stderr
    assert b"before-child" in prefix + stdout


def test_history_records_effective_worker_default(checkout: SimpleNamespace, monkeypatch: pytest.MonkeyPatch) -> None:
    """The start record and gate receive the same derived setting, without mutating the caller."""
    monkeypatch.delenv("PYTEST_XDIST_AUTO_NUM_WORKERS", raising=False)
    monkeypatch.setattr(verify_run, "worker_default", lambda: 3)
    write_gates(checkout.root, [_gate("cheap", "true")])
    seen = []
    real_append = verify_duration.append_event

    def append(event, **kwargs):
        seen.append(event)
        return real_append(event, **kwargs)

    def execute(_gate, _command, env):
        assert env["PYTEST_XDIST_AUTO_NUM_WORKERS"] == "3"
        return verify_run.GateProcess(0, "", "")

    monkeypatch.setattr(verify_duration, "append_event", append)
    result, out, err = run_scheduler(checkout.root, executor=execute)
    assert result.exit_code == 0, (out, err)
    assert next(event for event in seen if event["event"] == "run_start")["workers"] == "3"
    assert "PYTEST_XDIST_AUTO_NUM_WORKERS" not in os.environ


def test_gate_descendant_outside_its_group_cannot_hold_the_run(tmp_path: Path) -> None:
    """A descendant in a session of its own keeps the gate's pipes; the gate still ends (row L1-1).

    Planted fault: the run waits for end-of-file on the gate's pipes, so a child that left the
    gate's process group — and so survives the group's cleanup — blocks the run for as long as it
    lives, and its late output lands after the gate's verdict.
    """
    child_file = tmp_path / "escaped-child"
    child = "import time; print('late', flush=True); time.sleep(30); print('later', flush=True)"
    body = (
        "import subprocess, sys; from pathlib import Path; "
        f"escaped = subprocess.Popen([sys.executable, '-c', {child!r}], start_new_session=True); "
        f"Path({str(child_file)!r}).write_text(str(escaped.pid)); "
        "print('gate-done', flush=True)"
    )
    command = f"python3 -c {shlex.quote(body)}"
    script = f"""
import sys
from pathlib import Path
sys.path.insert(0, {str(REPO_ROOT / "scripts")!r})
import verify_run
verify_run.OUTPUT_DRAIN_SECONDS = 1.0
done = verify_run.gate_process(Path({str(tmp_path)!r}), sys.executable, {{'fd': None}}, {{}},
    {command!r}, dict(__import__('os').environ))
print('returned', done.returncode, flush=True)
"""
    proc = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = proc.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate(timeout=8)
        pytest.fail("a descendant outside the gate's group held the run on the gate's pipes")
    finally:
        if child_file.exists():
            with contextlib.suppress(ProcessLookupError, PermissionError, ValueError):
                os.kill(int(child_file.read_text()), signal.SIGKILL)
    assert proc.returncode == 0, stderr
    assert b"gate-done" in stdout and b"returned 0" in stdout, stdout
    assert b"later" not in stdout, "output after the gate's frame closed was written"
    assert b"left the gate's group" in stderr, stderr


@pytest.mark.parametrize(
    "gates",
    [["not a mapping"], {"not": "a list"}],
)
def test_malformed_gate_list_is_a_red_run_with_a_diagnostic(checkout: SimpleNamespace, gates: object) -> None:
    """Whatever the reader raises on a malformed list, the run is red with a diagnostic (row L1-12).

    Planted fault: a gate-list shape the reader does not name as its own error (a non-mapping entry)
    escapes the scheduler as an exception instead of the red run the shell's reader process gave.
    """
    folder = checkout.root / "decisions"
    folder.mkdir(exist_ok=True)
    doc = {"schema_version": 3, "tools": {"python": ["3.12"]}, "gates": gates}
    (folder / "gates.yaml").write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 2 and not result.executed, (result, out, err)
    assert "liess sich nicht erzeugen" in err, err
    assert "VERIFY GREEN" not in out, out


def test_cheap_red_on_a_moving_tree_ends_red_with_its_account(checkout: SimpleNamespace, gate_script: Path) -> None:
    """A cheap blocking red that also moved the tree is an ordinary red run (rows L2-2, L2-7).

    Planted fault: the tree comparison runs after a cheap blocking red and refuses, so the run
    exits 2 with no banner, no not-run summary and no completion record; or the cheap phase's
    summary says the run "stopped at" the first red gate although every cheap gate ran.
    """
    writer = f"python3 {gate_script} first 1 0 {checkout.root}/side-file"
    write_gates(
        checkout.root,
        [
            _gate("first", writer),
            _gate("second", f"python3 {gate_script} second 1"),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 1, (result, out, err)
    assert "changed while the cheap gates ran" not in err, err
    assert "── not run — every seconds gate ran; blocking red in [first], [second], so no protected" in out, out
    assert "stopped at the blocking failure" not in out, out
    assert "──   [heavy] not run" in out and verify_run.BANNER_RED in out, out
    end = [event for event in _history(checkout.tmp_path / "state") if event["event"] == "run_end"][-1]
    assert end["verdict"] == "red", end


def test_refused_admission_ends_with_the_runs_account(
    checkout: SimpleNamespace, gate_script: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A refused admission still names the gates it did not run and closes the record (row L2-2).

    Planted fault: the refusal propagates past the scheduler's ending, so the executed cheap gates
    sit in the history as an incomplete run and the not-run list and banner are missing.
    """
    write_gates(
        checkout.root,
        [_gate("cheap", f"python3 {gate_script} cheap 0"), _gate("heavy", "echo heavy", cost="minutes")],
    )

    @contextlib.contextmanager
    def refusing(_command: list[str]):
        raise verify_lock.MemoryFloorRefused("planted: too little free memory")
        yield None  # pragma: no cover - never reached

    monkeypatch.setattr(verify_lock, "hold_admission", refusing)
    out, err = io.StringIO(), io.StringIO()
    with pytest.raises(verify_lock.MemoryFloorRefused):
        verify_run.run_verification(checkout.root, out=out, err=err, python=sys.executable)
    text = out.getvalue()
    assert "── [cheap] gruen" in text, text
    assert "── not run — the run was refused before these gates:" in text and "──   [heavy] not run" in text, text
    assert verify_run.BANNER_REFUSED in text, text
    end = [event for event in _history(checkout.tmp_path / "state") if event["event"] == "run_end"][-1]
    assert end["verdict"] == "red" and end["admission_requested"] is True, end


def test_seconds_only_job_runs_on_an_unmeasurable_tree(checkout: SimpleNamespace, gate_script: Path) -> None:
    """A seconds-only job reuses nothing, so it measures no tree and never refuses over one (row L2-3).

    Planted fault: the baseline is measured for every job, so a docs run on a tree the comparison
    cannot read (here a tracked FIFO) refuses with zero gates executed.
    """
    write_gates(
        checkout.root,
        [
            _gate("docs-a", f"python3 {gate_script} docs-a 0", subsets=["docs"]),
            _gate("heavy", f"python3 {gate_script} heavy 0", cost="minutes"),
        ],
    )
    victim = checkout.root / "tracked.txt"
    victim.write_text("readable\n", encoding="utf-8")
    _git(checkout.root, "add", ".")
    _git(checkout.root, "commit", "--quiet", "-m", "tracked")
    victim.unlink()
    os.mkfifo(victim)
    result, out, err = run_scheduler(checkout.root, job="docs")
    assert result.exit_code == 0, (result, out, err)
    assert result.executed == ["docs-a"], result
    assert "cannot be measured" not in err, err
    # The full job still refuses that tree before its protected work.
    result, out, err = run_scheduler(checkout.root)
    assert result.exit_code == 2 and "cannot be measured" in err, (result, out, err)


def test_interpreter_default_comes_from_the_env_argument(checkout: SimpleNamespace, tmp_path: Path) -> None:
    """The run's `env` argument names the gates' interpreter, not the process environment (row L2-9).

    Planted fault: the default interpreter is read from `os.environ["PYTHON"]`, so an in-process
    caller's own environment is ignored for it.
    """
    marker = tmp_path / "wrapper-used"
    wrapper = tmp_path / "bin-wrapper" / "python-wrapper"
    wrapper.parent.mkdir()
    wrapper.write_text(f'#!/bin/sh\necho used > {shlex.quote(str(marker))}\nexec {shlex.quote(sys.executable)} "$@"\n')
    wrapper.chmod(0o755)
    write_gates(checkout.root, [_gate("cheap", "python3 -c 'pass'", subsets=["docs"])])
    env = dict(os.environ)
    env["PYTHON"] = str(wrapper)
    checkout.monkeypatch.delenv("PYTHON", raising=False)
    out, err = io.StringIO(), io.StringIO()
    result = verify_run.run_verification(checkout.root, job="docs", env=env, out=out, err=err)
    assert result.exit_code == 0, (result, out.getvalue(), err.getvalue())
    assert marker.exists(), "the gate ran under the process's interpreter, not the one `env` names"


def test_real_tool_caches_keep_the_baseline_stable(checkout: SimpleNamespace) -> None:
    """Real ruff and pytest gates inside the checkout leave the tree unchanged (row L2-1, rejected).

    Both tools write a `.gitignore` of `*` into their cache directories, so the comparison sees no
    new path even without a user-level ignore file; `__pycache__/` is ignored by the checkout's own
    `.gitignore`, as in this repository. Planted fault: the comparison counts the caches.
    """
    root = checkout.root
    (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests" / "test_one.py").write_text("def test_one():\n    assert True\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "--quiet", "-m", "a test")
    empty = checkout.tmp_path / "no-excludes"
    empty.write_text("", encoding="utf-8")
    checkout.monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(empty))
    checkout.monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    write_gates(
        root,
        [
            _gate("lint", "python3 -m ruff check tests/"),
            _gate("suite", "python3 -m pytest -q tests/"),
            _gate("heavy", "echo heavy", cost="minutes"),
        ],
    )
    result, out, err = run_scheduler(root)
    assert result.exit_code == 0, (result, out, err)
    assert (root / ".ruff_cache").is_dir() and (root / ".pytest_cache").is_dir(), "the caches were not written"
    assert result.executed == ["lint", "suite", "heavy"], result
