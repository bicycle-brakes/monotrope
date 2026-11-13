"""The shared locked log protocol of the stand-in suites (change flaky-swarm-leak-test).

Every criterion here comes with its fault: the forced mid-append read, the
unlocked-reader control, the corrupt log, the altered scenario text and the
planted guard bypasses are each shown red on the unsafe variant and green on
the shared helper of `tests/atomic_test_log.py` (bead coding-harness-yb1l).

The planted sample strings and the exemption snippets below are assembled from
parts on purpose: this guard module's own source must stay free of
append-mode open literals, so no exemption and no skip is needed for the file
that carries the guard.
"""

from __future__ import annotations

import fcntl
import json
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

import atomic_test_log
import pytest
from atomic_test_log import append_record, read_records, text_append
from test_stage2_swarm import SwarmWorld

HERE = Path(__file__).resolve().parent

# Larger than one buffered write, so an unlocked append is not a single write syscall.
PAYLOAD = "torn-read-payload-" + "x" * (96 * 1024)
MODE = "a"

# The planted bypass samples: recognisable test data, rendered with the mode
# filled in only at use time.
TOP_APPEND = 'from pathlib import Path\nwith Path("calls.jsonl").open(@MODE@) as handle:\n    handle.write("leak\\n")\n'
KEYWORD_APPEND = (
    "import os\n"
    "from pathlib import Path\n"
    'handle = open(os.environ["NEXT_LOG"], @MODE@)\n'
    'path_handle = Path("other.jsonl").open(mode=@MODE@)\n'
)
EMBEDDED_APPEND = (
    "STAND_IN = '''\nimport json\nwith log.open(@MODE@) as handle:\n    handle.write(json.dumps({}) + '\\n')\n'''\n"
)
SAFE_OPERATIONS = (
    "from pathlib import Path\n"
    'text = Path("notes.md").read_text()\n'
    'with open("notes.md", "w", encoding="utf-8") as handle:\n'
    "    handle.write(text)\n"
)


def _q(text: str) -> str:
    """A double-quoted source spelling of `text`."""
    return '"' + text + '"'


def _method_call(mode: str, tail: str = "") -> str:
    """A source spelling of an append-mode open call with the given mode."""
    return "open(" + _q(mode) + ((", " + tail) if tail else "") + ")"


def _line(head: str, mode: str, tail: str = "") -> str:
    return head + _method_call(mode, tail) + " as handle:"


# The exact, explained non-log operations the guard lets pass. Each entry names
# one operation by file and exact line; a moved or reworded line must be
# re-declared here, it is never silently carried along.
EXEMPT_OPERATIONS = (
    (
        "tests/test_stage2.py",
        _line("with path.", "a+"),
        "holds_record_lock probes the production record lock; it appends no log",
    ),
    (
        "tests/test_stage2_availability.py",
        _line("with path.", "a+"),
        "the same production record-lock probe, for the availability record verbs",
    ),
    (
        "tests/test_verify_lock.py",
        "with open(os.environ[" + _q("PROBE_LOG") + "], " + _q(MODE) + ", encoding=" + _q("utf-8") + ") as handle:",
        "the admission-order probe of one supervised verify_lock body, not a stand-in call log",
    ),
    (
        "tests/test_stage2_research_store.py",
        _line("with (repo / RESEARCH).", "ab"),
        "publishes a stored run's marker in the fixture research document, not a stand-in log",
    ),
    (
        "tests/test_stage2.py",
        _line("with (world.root / worktree_only).", MODE, "encoding=" + _q("utf-8")),
        "mutates a tracked worktree document to dirty the tree, not a stand-in log",
    ),
    (
        "tests/test_stage2.py",
        _line("with world.plan.", MODE, "encoding=" + _q("utf-8")),
        "appends scenario text to the test world's plan.md document, not a stand-in log",
    ),
    (
        "tests/test_stage2.py",
        _line("with world.record().", MODE, "encoding=" + _q("utf-8")),
        "appends to the loop-record document, not a stand-in log",
    ),
    (
        "tests/test_stage2.py",
        _line("with world.record().", MODE),
        "appends to the loop-record document, not a stand-in log",
    ),
    (
        "tests/test_stage2.py",
        _line(
            "with (root / " + _q("plans") + " / " + _q("changes") + " / " + _q("demo") + " / " + _q("plan.md") + ").",
            MODE,
            "encoding=" + _q("utf-8"),
        ),
        "appends to a test world's plan.md document, not a stand-in log",
    ),
    (
        "tests/test_stage2.py",
        _line("with stage2.secrets_path().", MODE, "encoding=" + _q("utf-8")),
        "appends to the planted secrets document, not a stand-in log",
    ),
)

# The ordinary append-mode open forms: method and built-in opens, positional
# and keyword modes beginning with "a". A line-based static guard: multi-line
# calls and dynamic mode construction are outside its claim, as the spec's
# guard [DETAIL] states.
APPEND_OPEN_PATTERNS = (
    ("method-positional", re.compile(r"\.open\(\s*(['\"])(a[^'\"]*)\1")),
    ("builtin-positional", re.compile(r"(?<![\w.])open\(\s*[^,()]*,\s*(['\"])(a[^'\"]*)\1")),
    ("method-keyword", re.compile(r"\.open\(\s*[^()]*?mode\s*=\s*(['\"])(a[^'\"]*)\1")),
    ("builtin-keyword", re.compile(r"(?<![\w.])open\(\s*[^()]*?mode\s*=\s*(['\"])(a[^'\"]*)\1")),
)

# The forced-split seam, test-local: the child replays the pre-fix stand-in
# writer under the shared sidecar lock. It appends half of one large record,
# hands the `started.marker` to the test, waits for the test's `go.marker` and
# completes the record. The script lives only in the test's tmp_path; no
# production script is patched.
SPLIT_WRITER = """
import fcntl
import json
import sys
import time
from pathlib import Path
sys.path.insert(0, sys.argv[3])
import atomic_test_log
data = Path(sys.argv[1])
gap = Path(sys.argv[2])
side_handle = atomic_test_log.lock_path(data).open(@MODE@)
fcntl.flock(side_handle, fcntl.LOCK_EX)
try:
    payload = json.dumps({"seq": 1, "payload": sys.argv[4]}) + "\\n"
    with data.open(@MODE@) as out:
        out.write(payload[: len(payload) // 2])
    (gap / "started.marker").write_text("started")
    deadline = time.time() + 60
    while not (gap / "go.marker").exists() and time.time() < deadline:
        time.sleep(0.02)
    with data.open(@MODE@) as out:
        out.write(payload[len(payload) // 2 :])
finally:
    fcntl.flock(side_handle, fcntl.LOCK_UN)
    side_handle.close()
"""

# An independent writer process that appends only through the shared helper.
FLEET_WRITER = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import atomic_test_log
data = Path(sys.argv[2])
writer = sys.argv[3]
for seq in range(6):
    payload = writer + "-" + str(seq) + "-" + sys.argv[4]
    record = {"writer": writer, "seq": seq, "payload": payload}
    atomic_test_log.append_record(data, record)
"""


def _render(sample: str) -> str:
    return sample.replace("@MODE@", _q(MODE))


def _wait_for(marker: Path, child: subprocess.Popen) -> None:
    """Wait, bounded, for a child's file handshake; never an open-ended sleep."""
    deadline = time.time() + 60
    while not marker.exists():
        if child.poll() is not None:
            pytest.fail(f"the split writer exited early with {child.returncode}")
        assert time.time() < deadline, f"no handshake at {marker}"
        time.sleep(0.02)


def find_append_bypasses(root: Path) -> list[str]:
    """Append-mode open literals under root that neither use the shared helper nor carry an exemption."""
    helper = Path(atomic_test_log.__file__).resolve()
    found: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if path.resolve() == helper or "__pycache__" in path.parts:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            exempt = any(
                path == HERE.parent / name and stripped == snippet for name, snippet, _reason in EXEMPT_OPERATIONS
            )
            if exempt:
                continue
            for kind, pattern in APPEND_OPEN_PATTERNS:
                match = pattern.search(line)
                if match:
                    found.append(f"{path}:{number}: {kind}, mode {match.group(2)!r}: {stripped}")
                    break
    return found


def test_concurrent_log_snapshots_are_complete(tmp_path: Path) -> None:
    """Criterion 1 (flaky-swarm-leak-test). Planted fault: the fixture observer reads a forced mid-append fragment.

    The child holds the shared sidecar lock and appends half of one large
    record before the test lets it finish. An unlocked read at that moment is
    the red control: it observes the fragment the pre-fix reader would have
    parsed. The real `SwarmWorld.calls` observer must instead wait for the
    completed record.
    """
    log = tmp_path / "calls.jsonl"
    gap = tmp_path / "gap"
    gap.mkdir()
    append_record(log, {"seq": 0, "payload": "seed"})
    script = tmp_path / "split_writer.py"
    script.write_text(_render(SPLIT_WRITER), encoding="utf-8")
    child = subprocess.Popen(
        [sys.executable, str(script), str(log), str(gap), str(HERE), PAYLOAD],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    world = SwarmWorld(root=tmp_path, bin=tmp_path, home=tmp_path)
    observed: dict = {}
    try:
        _wait_for(gap / "started.marker", child)
        # The child provably holds the sidecar's exclusive lock right now.
        probe_mode = MODE
        probe = atomic_test_log.lock_path(log).open(probe_mode)
        try:
            with pytest.raises(BlockingIOError):
                fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
        finally:
            fcntl.flock(probe, fcntl.LOCK_UN)
            probe.close()
        # Red control: an unlocked reader at this moment sees the fragment.
        with pytest.raises(json.JSONDecodeError):
            [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]

        def observe() -> None:
            try:
                observed["calls"] = world.calls()
            except Exception as error:  # the fault shows here: a torn read raises
                observed["error"] = error

        reader = threading.Thread(target=observe)
        reader.start()
        (gap / "go.marker").write_text("go")
        reader.join(timeout=120)
        assert not reader.is_alive(), "the locked observer never returned"
    finally:
        if child.poll() is None:
            child.kill()
        child.wait(timeout=30)
    assert "error" not in observed, observed["error"]
    assert observed["calls"] == [
        {"seq": 0, "payload": "seed"},
        {"seq": 1, "payload": PAYLOAD},
    ]


def test_concurrent_writers_preserve_every_record(tmp_path: Path) -> None:
    """Criterion 2 (flaky-swarm-leak-test). Planted fault: a concurrent large append is lost, duplicated or torn.

    Four independent writer processes append through the shared helper; every
    submitted record must come back exactly once with its full payload.
    """
    log = tmp_path / "calls.jsonl"
    script = tmp_path / "fleet_writer.py"
    script.write_text(FLEET_WRITER, encoding="utf-8")
    writers = 4
    children = [
        subprocess.Popen(
            [sys.executable, str(script), str(HERE), str(log), f"w{index}", PAYLOAD],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        for index in range(writers)
    ]
    try:
        for child in children:
            _out, err = child.communicate(timeout=180)
            assert child.returncode == 0, err[-2000:]
    finally:
        for child in children:
            if child.poll() is None:
                child.kill()
        for child in children:
            child.wait(timeout=30)
    records = read_records(log)
    assert len(records) == writers * 6
    identities = [(record["writer"], record["seq"]) for record in records]
    assert len(set(identities)) == writers * 6, "a record was duplicated"
    for record in records:
        assert record["payload"] == f"{record['writer']}-{record['seq']}-{PAYLOAD}", "a payload was torn or truncated"


def test_corrupt_log_is_not_hidden(tmp_path: Path) -> None:
    """Criterion 3 (flaky-swarm-leak-test). Planted fault: a malformed record becomes a successful observation."""
    log = tmp_path / "calls.jsonl"
    append_record(log, {"seq": 1})
    text_append(log, "{ not json\n")
    append_record(log, {"seq": 2})
    with pytest.raises(json.JSONDecodeError):
        read_records(log)


def test_missing_log_is_empty(tmp_path: Path) -> None:
    """Criterion 4 (flaky-swarm-leak-test). Planted fault: an absent log raises instead of yielding no records."""
    log = tmp_path / "calls.jsonl"
    assert read_records(log) == []
    append_record(log, {"name": "pi", "seq": 1})
    assert read_records(log) == [{"name": "pi", "seq": 1}]
    log.unlink()  # the suites clear the data file between runs; the sidecar stays
    assert read_records(log) == []


def test_text_appends_preserve_bytes(tmp_path: Path) -> None:
    """Criterion 4 (flaky-swarm-leak-test). Planted fault: the helper adds a newline or alters scenario text."""
    log = tmp_path / "text.jsonl"
    text_append(log, "first line without a trailing newline")
    assert log.read_bytes() == b"first line without a trailing newline"
    text_append(log, "second\xa0line\n")
    expected = ("first line without a trailing newline" + "second\xa0line\n").encode("utf-8")
    assert log.read_bytes() == expected
    text_append(log, "")
    assert log.read_bytes() == expected


def test_test_logs_use_the_shared_helper() -> None:
    """Criterion 5 (flaky-swarm-leak-test). Planted fault: a bypass remains in the repository inventory."""
    found = find_append_bypasses(HERE)
    assert found == [], "\n".join(found)
    # Every exemption names a live line: a moved or reworded operation must be
    # re-declared, never carried along silently.
    for name, snippet, _reason in EXEMPT_OPERATIONS:
        lines = [line.strip() for line in (HERE.parent / name).read_text(encoding="utf-8").splitlines()]
        assert snippet in lines, f"stale exemption for {name}: {snippet}"
    # The helper's allowance does real work: its own source holds append-mode
    # opens and still yields no finding.
    helper_text = Path(atomic_test_log.__file__).read_text(encoding="utf-8")
    assert any(pattern.search(helper_text) for _kind, pattern in APPEND_OPEN_PATTERNS)


def test_guard_detects_new_unlocked_log_appends(tmp_path: Path) -> None:
    """Criterion 5 (flaky-swarm-leak-test). Planted fault: a planted bypass passes the guard, or a safe operation is flagged.

    A new top-level log append, a new embedded stand-in append, and the
    positional and keyword forms are each detected with their source location;
    the safe non-append operations stay unflagged.
    """
    one = tmp_path / "top"
    one.mkdir()
    (one / "planted_top.py").write_text(_render(TOP_APPEND), encoding="utf-8")
    found = find_append_bypasses(one)
    assert len(found) == 1 and "planted_top.py" in found[0] and ":2:" in found[0], found

    two = tmp_path / "embedded"
    two.mkdir()
    (two / "planted_embedded.py").write_text(_render(EMBEDDED_APPEND), encoding="utf-8")
    found = find_append_bypasses(two)
    assert len(found) == 1 and "planted_embedded.py" in found[0] and ":3:" in found[0], found

    three = tmp_path / "forms"
    three.mkdir()
    (three / "planted_forms.py").write_text(_render(KEYWORD_APPEND), encoding="utf-8")
    found = find_append_bypasses(three)
    assert len(found) == 2, found
    assert ":3:" in found[0] and "builtin-positional" in found[0], found
    assert ":4:" in found[1] and "method-keyword" in found[1], found

    four = tmp_path / "safe"
    four.mkdir()
    (four / "safe_operations.py").write_text(SAFE_OPERATIONS, encoding="utf-8")
    assert find_append_bypasses(four) == []
