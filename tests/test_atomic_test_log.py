"""The shared locked log protocol of the stand-in suites (change flaky-swarm-leak-test).

Every criterion here comes with its fault: the forced mid-append read, the
unlocked-reader control, the corrupt log, the missing directory, the held
lock, the altered scenario text and the planted guard bypasses are each shown
red on the unsafe variant and green on the shared helper of
`tests/atomic_test_log.py` (bead coding-harness-yb1l).

The guard works by declaration: `atomic_test_log.STAND_IN_LOGS` names every
stand-in log, and any read, write or open of a declared log outside the helper
is a finding - in a test module and in every Python source string it carries.
The planted samples below spell the declared name only through the `@LOG@`
placeholder, filled in at use time, so this module's own source names no log
in a raw access and the guard needs no exemption for it.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import threading
import time
from pathlib import Path, PurePath

import atomic_test_log
import pytest
from atomic_test_log import append_record, read_records, text_append
from test_stage2_swarm import SwarmWorld

HERE = Path(__file__).resolve().parent

# Larger than one buffered write, so an unlocked append is not a single write syscall.
PAYLOAD = "torn-read-payload-" + "x" * (96 * 1024)

# The calls that turn a path into another spelling of a path; any other call's result is not a path.
PATH_CALLS = frozenset(
    {"Path", "PurePath", "str", "fspath", "join", "joinpath", "get", "resolve", "absolute", "expanduser", "with_name"}
)
# The calls that read, write or open a file.
ACCESS_METHODS = frozenset({"open", "read_text", "read_bytes", "write_text", "write_bytes"})
# Modules whose presence in a stand-in would mean it can contact the outside.
CONTACT_MODULES = frozenset(
    {"socket", "ssl", "http", "urllib", "ftplib", "smtplib", "poplib", "imaplib", "asyncio", "requests", "httpx"}
)

# The planted bypass samples: recognisable test data; `@LOG@` becomes a declared log name at use time.
TOP_READ = 'from pathlib import Path\nrecords = Path("bin/@LOG@").read_text()\n'
VARIABLE_APPEND = (
    "from pathlib import Path\n"
    'target = Path("bin") / "@LOG@"\n'
    "alias = target\n"
    'with open(alias, "a") as handle:\n'
    '    handle.write("leak\\n")\n'
)
EMBEDDED_APPEND = (
    "STAND_IN = '''\nfrom pathlib import Path\nhere = Path(__file__).parent\n"
    "with (here / \"@LOG@\").open(\"a\") as handle:\n    handle.write('{}')\n'''\n"
)
ENV_ROUTED = (
    "import os\n"
    'env = {"CHILD_LOG": str(root / "@LOG@")}\n'
    "STAND_IN = '''\nimport os\n"
    "with open(os.environ[\"CHILD_LOG\"], \"a\") as handle:\n    handle.write('{}')\n'''\n"
)
# A file whose name only ends in a declared one is not a declared log: the helper refuses it, so the guard ignores it.
NEAR_MISS = 'from pathlib import Path\nrecords = Path("bin/old-@LOG@").read_text()\nother = Path("bin") / "my@LOG@"\nother.write_text("")\n'
SAFE_OPERATIONS = (
    "from pathlib import Path\n"
    "from atomic_test_log import append_record, read_records\n"
    'log = Path("bin") / "@LOG@"\n'
    "records = read_records(log)\n"
    'append_record(log, {"seq": 1})\n'
    "log.unlink(missing_ok=True)\n"
    'with open("notes.md", "a", encoding="utf-8") as handle:\n'
    '    handle.write("a document, not a stand-in log\\n")\n'
    'with Path("record.lock").open("a+") as probe:\n'
    "    pass\n"
)

# The forced-split seam, test-local: the child replays the pre-fix stand-in
# writer under the shared lock on the data file. It appends half of one large
# record and, still holding the lock, reads the file unlocked - the read every
# pre-fix observer made - and reports in `started.marker` whether that read
# was torn. Then it waits for the test's `go.marker` and completes the record.
# Its data path arrives at run time, so it names no declared log.
SPLIT_WRITER = """
import fcntl
import json
import sys
import time
from pathlib import Path
data = Path(sys.argv[1])
gap = Path(sys.argv[2])
payload = json.dumps({"seq": 1, "payload": sys.argv[3]}) + "\\n"
with data.open("a") as out:
    fcntl.flock(out, fcntl.LOCK_EX)
    try:
        out.write(payload[: len(payload) // 2])
        out.flush()
        try:
            [json.loads(line) for line in data.read_text().splitlines()]
            verdict = "whole"
        except json.JSONDecodeError:
            verdict = "torn"
        (gap / "started.marker").write_text(verdict)
        deadline = time.time() + 60
        while not (gap / "go.marker").exists() and time.time() < deadline:
            time.sleep(0.02)
        out.write(payload[len(payload) // 2 :])
        out.flush()
    finally:
        fcntl.flock(out, fcntl.LOCK_UN)
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
    return sample.replace("@LOG@", atomic_test_log.STAND_IN_LOGS[0])


def _wait_for(marker: Path, child: subprocess.Popen) -> None:
    """Wait, bounded, for a child's file handshake; never an open-ended sleep."""
    deadline = time.time() + 60
    while not marker.exists():
        if child.poll() is not None:
            pytest.fail(f"the split writer exited early with {child.returncode}")
        assert time.time() < deadline, f"no handshake at {marker}"
        time.sleep(0.02)


def _start_split_writer(tmp_path: Path, log: Path) -> tuple[subprocess.Popen, Path]:
    gap = tmp_path / "gap"
    gap.mkdir()
    script = tmp_path / "split_writer.py"
    script.write_text(SPLIT_WRITER, encoding="utf-8")
    child = subprocess.Popen(
        [sys.executable, str(script), str(log), str(gap), PAYLOAD],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    _wait_for(gap / "started.marker", child)
    return child, gap


def _finish(child: subprocess.Popen, gap: Path) -> None:
    (gap / "go.marker").write_text("go")
    try:
        child.wait(timeout=60)
    finally:
        if child.poll() is None:
            child.kill()
            child.wait(timeout=30)


# ---------------------------------------------------------------------------
# The guard: reads and appends of declared stand-in logs go through the helper
# ---------------------------------------------------------------------------


def _python_sources(text: str) -> list[tuple[int, ast.Module]]:
    """The module and every string constant in it that parses as Python, with the line it starts on.

    A stand-in template is such a string; its `@ATOMIC_LOG@` marker line is
    dropped before parsing. Prose and shell strings do not parse and carry
    no Python access.
    """
    found: list[tuple[int, ast.Module]] = [(1, ast.parse(text))]
    index = 0
    while index < len(found):
        offset, tree = found[index]
        index += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and "\n" in node.value:
                try:
                    inner = ast.parse(node.value.replace(atomic_test_log.MARKER, ""))
                except SyntaxError:
                    continue
                found.append((offset + node.lineno - 1, inner))
    return found


def _names_a_log(node: ast.AST, names: set[str], keys: set[str]) -> bool:
    """Whether this expression carries a declared log's path: its name, a variable or key bound to it.

    A string names a log when its last path part equals a declared name - the
    helper's own rule (`atomic_test_log._declared`), not a suffix match.
    """
    declared = atomic_test_log.STAND_IN_LOGS
    pending = [node]
    while pending:
        sub = pending.pop()
        if isinstance(sub, ast.Call) and getattr(sub.func, "id", getattr(sub.func, "attr", None)) not in PATH_CALLS:
            continue
        if (
            isinstance(sub, ast.Constant)
            and isinstance(sub.value, str)
            and (PurePath(sub.value).name in declared or sub.value in keys)
        ):
            return True
        if isinstance(sub, ast.Name) and sub.id in names:
            return True
        if isinstance(sub, ast.Attribute) and sub.attr == "STAND_IN_LOGS":
            return True
        pending.extend(ast.iter_child_nodes(sub))
    return False


_SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)


def _own_nodes(scope: ast.AST) -> list[ast.AST]:
    """The nodes of one scope, without the bodies of the functions nested in it."""
    nodes: list[ast.AST] = []
    pending = list(ast.iter_child_nodes(scope))
    while pending:
        node = pending.pop()
        nodes.append(node)
        if not isinstance(node, _SCOPES):
            pending.extend(ast.iter_child_nodes(node))
    return nodes


def _targets(node: ast.Assign | ast.AnnAssign) -> list[ast.expr]:
    return list(node.targets) if isinstance(node, ast.Assign) else [node.target]


def _scope_names(scope: ast.AST, inherited: set[str], keys: set[str]) -> set[str]:
    """Variables of one scope bound to a declared log's path, followed to a fixed point.

    A function sees the module's bound names unless it assigns the name itself.
    """
    nodes = [node for node in _own_nodes(scope) if isinstance(node, ast.Assign | ast.AnnAssign) and node.value]
    assigned = {target.id for node in nodes for target in _targets(node) if isinstance(target, ast.Name)}
    names = set(inherited) - assigned
    while True:
        before = len(names)
        for node in nodes:
            if _names_a_log(node.value, names, keys):
                names |= {target.id for target in _targets(node) if isinstance(target, ast.Name)}
        if len(names) == before:
            return names


def _analyse(sources: list[tuple[int, ast.Module]]) -> list[tuple[int, ast.AST, set[str], set[str]]]:
    """Every scope of every source with its log-bound variables; environment keys bound to a log are file-wide."""
    keys: set[str] = set()
    while True:
        before = len(keys)
        scoped: list[tuple[int, ast.AST, set[str], set[str]]] = []
        for offset, tree in sources:
            module_names = _scope_names(tree, set(), keys)
            scopes = [tree] + [node for node in ast.walk(tree) if isinstance(node, _SCOPES)]
            for scope in scopes:
                names = module_names if scope is tree else _scope_names(scope, module_names, keys)
                scoped.append((offset, scope, names, keys))
                for node in _own_nodes(scope):
                    if isinstance(node, ast.Assign) and _names_a_log(node.value, names, keys):
                        for target in node.targets:
                            if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant):
                                keys.add(str(target.slice.value))
                    elif isinstance(node, ast.Dict):
                        for key, value in zip(node.keys, node.values, strict=True):
                            if isinstance(key, ast.Constant) and _names_a_log(value, names, keys):
                                keys.add(str(key.value))
        if len(keys) == before:
            return scoped


def find_raw_log_access(root: Path) -> list[str]:
    """Reads, writes and opens of a declared stand-in log under root that bypass the shared helper."""
    helper = Path(atomic_test_log.__file__).resolve()
    found: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if path.resolve() == helper or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        for offset, scope, names, keys in _analyse(_python_sources(text)):
            for node in _own_nodes(scope):
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                method = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
                if method not in ACCESS_METHODS:
                    continue
                receiver = func.value if isinstance(func, ast.Attribute) else None
                first = node.args[0] if node.args else None
                if any(part is not None and _names_a_log(part, names, keys) for part in (receiver, first)):
                    number = offset + node.lineno - 1
                    source_line = lines[number - 1].strip() if number <= len(lines) else ""
                    found.append(f"{path}:{number}: raw {method} of a stand-in log: {source_line}")
    return sorted(set(found), key=lambda line: (line.split(":")[0], int(line.split(":")[1])))


def test_concurrent_log_snapshots_are_complete(tmp_path: Path) -> None:
    """Criterion 1 (flaky-swarm-leak-test). Planted fault: the fixture observer reads a forced mid-append fragment.

    The child holds the shared lock and appends half of one large record
    before the test lets it finish. Its own unlocked read at that moment is
    the red control: it observes the fragment the pre-fix reader would have
    parsed. The real `SwarmWorld.calls` observer must instead wait for the
    completed record.
    """
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    append_record(log, {"seq": 0, "payload": "seed"})
    world = SwarmWorld(root=tmp_path, bin=tmp_path, home=tmp_path)
    observed: dict = {}
    child, gap = _start_split_writer(tmp_path, log)
    try:
        assert (gap / "started.marker").read_text() == "torn", "the unlocked control read no fragment"

        def observe() -> None:
            try:
                observed["calls"] = world.calls()
            except Exception as error:  # the fault shows here: a torn read raises
                observed["error"] = error

        reader = threading.Thread(target=observe)
        reader.start()
    finally:
        _finish(child, gap)
    reader.join(timeout=120)
    assert not reader.is_alive(), "the locked observer never returned"
    assert child.returncode == 0, child.stderr.read() if child.stderr else ""
    assert "error" not in observed, observed["error"]
    assert observed["calls"] == [
        {"seq": 0, "payload": "seed"},
        {"seq": 1, "payload": PAYLOAD},
    ]


def test_a_held_lock_times_out_instead_of_hanging(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 1 (flaky-swarm-leak-test, loop rows L1-5/L1-6/L1-11). Planted fault: a reader hangs or skips the writer's lock.

    A writer that holds the lock past the deadline must make the reader fail
    loudly with `TimeoutError`, not hang the gate that observes the log. The
    reader spells the path through a symlinked directory: the lock is the
    file's own, so another spelling of one file still meets the writer's lock.
    """
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    alias = tmp_path / "alias"
    alias.symlink_to(tmp_path, target_is_directory=True)
    monkeypatch.setattr(atomic_test_log, "LOCK_TIMEOUT", 0.3)
    outcome: dict = {}
    child, gap = _start_split_writer(tmp_path, log)
    try:

        def observe() -> None:
            try:
                outcome["records"] = read_records(alias / log.name)
            except Exception as error:
                outcome["error"] = error

        reader = threading.Thread(target=observe, daemon=True)
        reader.start()
        reader.join(timeout=20)
        hung = reader.is_alive()
    finally:
        _finish(child, gap)
    assert not hung, "the reader hung on a held lock"
    assert isinstance(outcome.get("error"), TimeoutError), outcome


def test_concurrent_writers_preserve_every_record(tmp_path: Path) -> None:
    """Criterion 2 (flaky-swarm-leak-test). Planted fault: a concurrent large append is lost, duplicated or torn.

    Four independent writer processes append through the shared helper; every
    submitted record must come back exactly once with its full payload.
    """
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
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
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    append_record(log, {"seq": 1})
    text_append(log, "{ not json\n")
    append_record(log, {"seq": 2})
    with pytest.raises(json.JSONDecodeError):
        read_records(log)


def test_missing_log_is_empty(tmp_path: Path) -> None:
    """Criterion 4 (flaky-swarm-leak-test, loop rows L1-4/L1-16). Planted fault: an absent log or directory raises."""
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    assert read_records(log) == []
    append_record(log, {"name": "pi", "seq": 1})
    assert read_records(log) == [{"name": "pi", "seq": 1}]
    log.unlink()  # the suites clear the data file between runs
    assert read_records(log) == []
    assert read_records(tmp_path / "absent" / atomic_test_log.STAND_IN_LOGS[0]) == []


def test_only_declared_logs_take_records(tmp_path: Path) -> None:
    """Criterion 5 (flaky-swarm-leak-test). Planted fault: a JSON log the guard does not know about is written or read.

    The helper is the one place a stand-in log is declared: its JSON functions
    refuse an undeclared name, so every log they serve is one the guard watches.
    """
    with pytest.raises(ValueError, match="not a declared stand-in log"):
        append_record(tmp_path / "undeclared.jsonl", {"seq": 1})
    with pytest.raises(ValueError, match="not a declared stand-in log"):
        read_records(tmp_path / "undeclared.jsonl")
    assert not (tmp_path / "undeclared.jsonl").exists()


def test_text_appends_preserve_bytes(tmp_path: Path) -> None:
    """Criterion 4 (flaky-swarm-leak-test). Planted fault: the helper adds a newline or alters scenario text."""
    document = tmp_path / "text.md"
    text_append(document, "first line without a trailing newline")
    assert document.read_bytes() == b"first line without a trailing newline"
    text_append(document, "second\xa0line\n")
    expected = ("first line without a trailing newline" + "second\xa0line\n").encode("utf-8")
    assert document.read_bytes() == expected
    text_append(document, "")
    assert document.read_bytes() == expected


def test_test_logs_use_the_shared_helper() -> None:
    """Criterion 5 (flaky-swarm-leak-test). Planted fault: a raw read or append of a stand-in log remains in tests/."""
    found = find_raw_log_access(HERE)
    assert found == [], "\n".join(found)


def test_stand_ins_stay_visible_and_contact_free() -> None:
    """Criterion 5 (flaky-swarm-leak-test, loop row L1-7). Planted fault: a stand-in hides from the guard or imports a contact.

    Every template that embeds the helper must parse as Python - else the
    guard could not see its log access - and, rendered with the helper, import
    only standard-library modules, none of which can open a connection.
    """
    source = atomic_test_log.embedded_source()
    templates = 0
    helper = Path(atomic_test_log.__file__).resolve()
    for path in sorted(HERE.glob("*.py")):
        if path.resolve() == helper:
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
                continue
            if atomic_test_log.MARKER not in node.value.splitlines():
                continue
            templates += 1
            tree = ast.parse(node.value.replace(atomic_test_log.MARKER, source), filename=f"{path.name}:{node.lineno}")
            imported = {
                alias.name.split(".")[0] for sub in ast.walk(tree) if isinstance(sub, ast.Import) for alias in sub.names
            } | {sub.module.split(".")[0] for sub in ast.walk(tree) if isinstance(sub, ast.ImportFrom) and sub.module}
            where = f"{path.name}:{node.lineno}"
            assert imported <= set(sys.stdlib_module_names), f"{where} imports beyond the standard library: {imported}"
            assert not imported & CONTACT_MODULES, f"{where} imports a contact module: {imported & CONTACT_MODULES}"
    assert templates >= 7, f"only {templates} stand-in templates embed the helper"


def test_guard_detects_raw_log_access(tmp_path: Path) -> None:
    """Criterion 5 (flaky-swarm-leak-test, loop rows L1-2/L1-8). Planted fault: a raw read or append of a stand-in log passes.

    A direct read, an append through a variable, an embedded stand-in append
    and an append through an environment key that carries a log path are
    each detected with their source location; helper calls, a log's removal,
    a document append, a lock probe and a file whose name merely ends in a
    declared one (loop row L2-3) stay unflagged without any exemption.
    """
    cases = {
        "top_read": (TOP_READ, [":2: raw read_text"]),
        "variable_append": (VARIABLE_APPEND, [":4: raw open"]),
        "embedded_append": (EMBEDDED_APPEND, [":4: raw open"]),
        "env_routed": (ENV_ROUTED, [":5: raw open"]),
        "safe_operations": (SAFE_OPERATIONS, []),
        "near_miss": (NEAR_MISS, []),
    }
    for name, (sample, expected) in cases.items():
        folder = tmp_path / name
        folder.mkdir()
        (folder / f"planted_{name}.py").write_text(_render(sample), encoding="utf-8")
        found = find_raw_log_access(folder)
        assert len(found) == len(expected), (name, found)
        for line, wanted in zip(found, expected, strict=True):
            assert f"planted_{name}.py" in line and wanted in line, (name, found)
