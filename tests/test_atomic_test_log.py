"""The shared locked log protocol of the stand-in suites (change flaky-swarm-leak-test).

Every criterion here comes with its fault: the forced mid-append read, the
unlocked-reader control, the corrupt log, the missing directory, the held
lock, the altered scenario text and the planted guard bypasses are each shown
red on the unsafe variant and green on the shared helper of
`tests/atomic_test_log.py` (bead coding-harness-yb1l).

Both checks work by declaration: `atomic_test_log.STAND_IN_LOGS` names every
stand-in log. At run time any read, write or open of a declared log outside
the helper fails its test (`tests/stand_in_log_guard.py`, decisions.md#Q-5);
the static guard is a cheap advisory that also reads every Python source
string a test module carries, so it reaches the stand-in templates.
The planted samples below spell the declared name only through the `@LOG@`
placeholder, filled in at use time, so this module's own source names no log
in a raw access and the guard needs no exemption for it.
"""

from __future__ import annotations

import ast
import io
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path, PurePath
from types import SimpleNamespace

import atomic_test_log
import pytest
import stand_in_log_guard
from atomic_test_log import append_counted, append_record, counter_path, read_counter, read_records, text_append
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
# A nested reader inherits its enclosing function's log binding (finding F6-4).
CLOSURE_READ = (
    "from pathlib import Path\n"
    "def outer():\n"
    '    log = Path("@LOG@")\n'
    "    def reader():\n"
    "        return (\n"
    "            log.read_text())\n"
    "    return reader\n"
)
# A parameter shadows a module-level log binding of the same name (finding F6-5).
PARAMETER_SHADOW = (
    "from pathlib import Path\n"
    'log = Path("@LOG@")\n'
    "def read_doc(log):\n"
    "    return log.read_text()\n"
    'read_doc(Path("notes.md"))\n'
    "shadow = lambda log: log.read_text()\n"
)
# Every way a name gets bound carries a log's identity, element-wise where unpacking pairs (finding F6-6).
BINDING_FORMS = (
    "from pathlib import Path\n"
    'log, document = Path("@LOG@"), Path("notes.md")\n'
    "log.read_text()\n"
    "document.read_text()\n"
    '[head, *tail] = [Path("notes.md"), Path("@LOG@")]\n'
    "head.read_text()\n"
    "tail[0].read_text()\n"
    'base = Path("bin")\n'
    'annotated: Path = base / "@LOG@"\n'
    "annotated.read_bytes()\n"
    "grown = base\n"
    'grown /= "@LOG@"\n'
    'grown.write_bytes(b"")\n'
    'if (caught := base / "@LOG@").exists():\n'
    "    caught.read_text()\n"
    'for looped in [Path("notes.md"), base / "@LOG@"]:\n'
    "    looped.read_text()\n"
    'with Path("@LOG@") as held:\n'
    "    held.read_text()\n"
    '[item.read_text() for item in (base / "@LOG@",)]\n'
    'def reader(path=base / "@LOG@"):\n'
    "    return path.read_text()\n"
    'outer, (inner, other) = Path("notes.md"), (Path("@LOG@"), Path("other.md"))\n'
    "inner.read_text()\n"
    "other.read_text()\n"
    'first = second = Path("@LOG@")\n'
    "second.read_text()\n"
)
# A module-level log binding is shadowed by every local binding form, not only assignment and parameters.
BINDING_SHADOWS = (
    "from pathlib import Path\n"
    'log = Path("@LOG@")\n'
    "def unpacked():\n"
    '    log, doc = Path("notes.md"), Path("other.md")\n'
    "    return log.read_text()\n"
    "def looped(docs):\n"
    "    for log in docs:\n"
    "        log.read_text()\n"
    "def held():\n"
    '    with open("notes.md") as log:\n'
    "        return log.read()\n"
    "def imported():\n"
    "    from notes import doc as log\n"
    "    return log.read_text()\n"
    "def caught():\n"
    "    try:\n"
    "        pass\n"
    "    except OSError as log:\n"
    "        return log.filename.read_text()\n"
    'docs = [path.read_text() for path in [Path("notes.md")]]\n'
    'logs = [path for path in [Path("@LOG@")]]\n'
)
# The destination of a pathlib read or write is its receiver; write_text's argument is content (finding F6-7).
RECEIVER_DESTINATION = (
    "from pathlib import Path\n"
    'Path("notes.md").write_text("@LOG@")\n'
    'Path("notes.md").write_bytes(b"@LOG@")\n'
    'Path.read_text(Path("@LOG@"))\n'
)
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
with data.open("a", encoding="utf-8") as out:
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


_FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
_COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
_SCOPES = _FUNCTIONS + _COMPREHENSIONS
# A pathlib method called on the class itself takes its path as the first argument.
_PATH_CLASSES = frozenset({"Path", "PurePath", "PosixPath", "PurePosixPath"})
# A binding: the bound name and the expression it receives, None when nothing the guard can follow.
Binding = tuple[str, ast.expr | None]


def _own_nodes(scope: ast.AST) -> list[ast.AST]:
    """The nodes of one scope, without the bodies of the functions and comprehensions nested in it."""
    nodes: list[ast.AST] = []
    pending = list(ast.iter_child_nodes(scope))
    while pending:
        node = pending.pop()
        nodes.append(node)
        if not isinstance(node, _SCOPES):
            pending.extend(ast.iter_child_nodes(node))
    return nodes


def _unstarred(elements: list[ast.expr]) -> bool:
    return not any(isinstance(element, ast.Starred) for element in elements)


def _pair(target: ast.expr, value: ast.expr | None) -> list[Binding]:
    """Each name a binding target binds, with the expression it receives.

    Unpacking pairs element-wise when the value is a literal tuple or list of
    matching shape; a starred target receives the leftover elements as a list.
    Any other value - a variable, a call, a mismatched shape - goes whole to
    every name of the target, so a log anywhere in it marks them all.
    """
    if isinstance(target, ast.Name):
        return [(target.id, value)]
    if isinstance(target, ast.Starred):
        return _pair(target.value, value)
    if not isinstance(target, ast.Tuple | ast.List):
        return []  # an attribute or subscript target binds no name
    targets = target.elts
    if isinstance(value, ast.Tuple | ast.List) and _unstarred(value.elts):
        values = list(value.elts)
        stars = [index for index, element in enumerate(targets) if isinstance(element, ast.Starred)]
        if not stars and len(values) == len(targets):
            return [binding for sub, element in zip(targets, values, strict=True) for binding in _pair(sub, element)]
        if len(stars) == 1 and len(values) >= len(targets) - 1:
            star, after = stars[0], len(targets) - stars[0] - 1
            middle = ast.List(elts=values[star : len(values) - after], ctx=ast.Load())
            paired = [*values[:star], middle, *values[len(values) - after :]]
            return [binding for sub, element in zip(targets, paired, strict=True) for binding in _pair(sub, element)]
    return [binding for sub in targets for binding in _pair(sub, value)]


def _iterated(target: ast.expr, iterable: ast.expr) -> list[Binding]:
    """A loop target receives one element at a time: each element of a literal, else the whole iterable."""
    if isinstance(iterable, ast.Tuple | ast.List | ast.Set) and _unstarred(iterable.elts):
        return [binding for element in iterable.elts for binding in _pair(target, element)]
    return _pair(target, iterable)


def _binding_nodes(scope: ast.AST) -> list[ast.AST]:
    """The nodes that can bind a name in this scope.

    A walrus binds in the nearest enclosing function or module, through any
    comprehensions around it, never in the comprehension itself.
    """
    own = _own_nodes(scope)
    if isinstance(scope, _COMPREHENSIONS):
        return [node for node in own if not isinstance(node, ast.NamedExpr)]
    nodes = list(own)
    pending = [node for node in own if isinstance(node, _COMPREHENSIONS)]
    while pending:
        for node in _own_nodes(pending.pop()):
            if isinstance(node, ast.NamedExpr):
                nodes.append(node)
            elif isinstance(node, _COMPREHENSIONS):
                pending.append(node)
    return nodes


def _bindings(scope: ast.AST) -> list[Binding]:
    """Every name this scope binds, by every binding form Python has, with what each receives."""
    found: list[Binding] = []
    if isinstance(scope, _FUNCTIONS):
        arguments = scope.args
        positional = arguments.posonlyargs + arguments.args
        defaults: list[ast.expr | None] = [None] * (len(positional) - len(arguments.defaults))
        defaults += arguments.defaults
        found += [(parameter.arg, default) for parameter, default in zip(positional, defaults, strict=True)]
        found += [
            (parameter.arg, default)
            for parameter, default in zip(arguments.kwonlyargs, arguments.kw_defaults, strict=True)
        ]
        found += [(extra.arg, None) for extra in (arguments.vararg, arguments.kwarg) if extra is not None]
    if isinstance(scope, _COMPREHENSIONS):
        for generator in scope.generators:
            found += _iterated(generator.target, generator.iter)
    for node in _binding_nodes(scope):
        if isinstance(node, ast.Assign):
            found += [binding for target in node.targets for binding in _pair(target, node.value)]
        elif isinstance(node, ast.AnnAssign):
            found += _pair(node.target, node.value)
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            # `log /= name` binds log to the old value combined with the new part.
            combined = ast.BinOp(left=ast.Name(id=node.target.id, ctx=ast.Load()), op=node.op, right=node.value)
            found.append((node.target.id, combined))
        elif isinstance(node, ast.NamedExpr):
            found += _pair(node.target, node.value)
        elif isinstance(node, ast.For | ast.AsyncFor):
            found += _iterated(node.target, node.iter)
        elif isinstance(node, ast.With | ast.AsyncWith):
            found += [
                binding
                for item in node.items
                if item.optional_vars is not None
                for binding in _pair(item.optional_vars, item.context_expr)
            ]
        elif isinstance(node, ast.Import | ast.ImportFrom):
            found += [((alias.asname or alias.name).split(".")[0], None) for alias in node.names if alias.name != "*"]
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | ast.ExceptHandler):
            # A definition or an except-as binds a name to no path; so does a match capture below.
            found += [(node.name, None)] if node.name else []
        elif isinstance(node, ast.MatchAs | ast.MatchStar) and node.name:
            found.append((node.name, None))
        elif isinstance(node, ast.MatchMapping) and node.rest:
            found.append((node.rest, None))
        elif isinstance(node, ast.Delete):
            found += [binding for target in node.targets for binding in _pair(target, None)]
    return found


def _scope_names(scope: ast.AST, inherited: set[str], keys: set[str]) -> set[str]:
    """Variables of one scope bound to a declared log's path, followed to a fixed point.

    Lexical scoping: a function or comprehension sees the bound names of every
    enclosing scope unless it binds the name itself, by any binding form
    (`_bindings`); a `global` or `nonlocal` name stays the enclosing one. A
    name is a log for the whole scope once any of its bindings receives one.
    """
    bindings = _bindings(scope)
    outer = {name for node in _own_nodes(scope) if isinstance(node, ast.Global | ast.Nonlocal) for name in node.names}
    names = set(inherited) - ({name for name, _value in bindings} - outer)
    while True:
        before = len(names)
        for name, value in bindings:
            if value is not None and name not in names and _names_a_log(value, names, keys):
                names.add(name)
        if len(names) == before:
            return names


def _analyse(sources: list[tuple[int, ast.Module]]) -> list[tuple[int, ast.AST, set[str], set[str]]]:
    """Every scope of every source with its log-bound variables; environment keys bound to a log are file-wide."""
    keys: set[str] = set()
    while True:
        before = len(keys)
        scoped: list[tuple[int, ast.AST, set[str], set[str]]] = []
        for offset, tree in sources:
            # Each scope inherits from its lexically enclosing scope, not only the module.
            pending: list[tuple[ast.AST, set[str]]] = [(tree, set())]
            while pending:
                scope, enclosing = pending.pop()
                names = _scope_names(scope, enclosing, keys)
                scoped.append((offset, scope, names, keys))
                for node in _own_nodes(scope):
                    if isinstance(node, _SCOPES):
                        pending.append((node, names))
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
                if method == "open":
                    # open()'s file comes positionally or as file=, Path.open's is
                    # its receiver; every open of a declared log is access whatever
                    # its mode (positional, mode=, or the implicit read default).
                    file_arg = next((keyword.value for keyword in node.keywords if keyword.arg == "file"), None)
                    destinations = (receiver, first, file_arg)
                elif receiver is None or getattr(receiver, "id", getattr(receiver, "attr", None)) in _PATH_CLASSES:
                    # A bare function or `Path.read_text(path)`: the path is the first argument.
                    destinations = (first,)
                else:
                    # A pathlib read or write acts on its receiver; write_text's argument is content.
                    destinations = (receiver,)
                if any(part is not None and _names_a_log(part, names, keys) for part in destinations):
                    number = offset + node.lineno - 1
                    source_line = lines[number - 1].strip() if number <= len(lines) else ""
                    found.append(f"{path}:{number}: raw {method} of a stand-in log: {source_line}")
    return sorted(set(found), key=lambda line: (line.split(":")[0], int(line.split(":")[1])))


def test_concurrent_log_snapshots_are_complete(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
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
    attempted = threading.Event()
    flock = atomic_test_log.fcntl.flock

    def observed_flock(handle, operation: int) -> None:
        try:
            flock(handle, operation)
        except BlockingIOError:
            # The reader has actually met the split writer's lock. Merely
            # starting its thread does not establish this ordering.
            if operation & atomic_test_log.fcntl.LOCK_SH:
                attempted.set()
            raise

    monkeypatch.setattr(atomic_test_log.fcntl, "flock", observed_flock)
    child, gap = _start_split_writer(tmp_path, log)
    try:
        assert (gap / "started.marker").read_text() == "torn", "the unlocked control read no fragment"

        def observe() -> None:
            try:
                observed["calls"] = world.calls()
            except Exception as error:  # the fault shows here: a torn read raises
                observed["error"] = error
            finally:
                # An unlocked observer completes (or parses the fragment)
                # before the writer is released as well.
                attempted.set()

        reader = threading.Thread(target=observe)
        reader.start()
        assert attempted.wait(timeout=30), "the observer never attempted its read"
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


@pytest.mark.raw_stand_in_log_access(reason="plants the unlocked observer the race test must reject")
def test_race_rejects_a_delayed_unlocked_observer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The race must expose an unlocked observer even when its thread starts late.

    Without the read-attempt handshake this schedule runs the observer only
    after the writer finishes, so the old race test silently passes.
    """
    permit_read = threading.Event()
    real_thread = threading.Thread
    real_event = threading.Event
    finish = _finish

    class AttemptEvent:
        def __init__(self) -> None:
            self.event = real_event()

        def set(self) -> None:
            self.event.set()

        def wait(self, timeout: float) -> bool:
            permit_read.set()
            return self.event.wait(timeout)

    def delayed_thread(*, target):
        def delayed() -> None:
            assert permit_read.wait(timeout=30), "the observer was never released"
            target()

        return real_thread(target=delayed)

    def finish_then_read(child, gap) -> None:
        try:
            finish(child, gap)
        finally:
            permit_read.set()

    def unlocked_calls(world):
        # Render the planted access like the guard's other unsafe samples.
        log = world.bin / _render("@LOG@")
        return [json.loads(line) for line in log.read_text().splitlines()]

    module = sys.modules[__name__]
    monkeypatch.setattr(module, "threading", SimpleNamespace(Thread=delayed_thread, Event=AttemptEvent))
    monkeypatch.setattr(module, "_finish", finish_then_read)
    monkeypatch.setattr(SwarmWorld, "calls", unlocked_calls)
    with pytest.raises(AssertionError, match="JSONDecodeError"):
        test_concurrent_log_snapshots_are_complete(tmp_path, monkeypatch)


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


def test_corrupt_log_is_not_hidden(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 3 (flaky-swarm-leak-test). Planted fault: a malformed record becomes a successful observation."""
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    append_record(log, {"seq": 1})
    with monkeypatch.context() as patch:
        patch.setattr(atomic_test_log.json, "dumps", lambda _record: "{ not json")
        append_record(log, {"seq": "corrupt"})
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


def test_a_cleared_log_starts_fresh_under_a_late_writer(tmp_path: Path) -> None:
    """Criterion 2 (flaky-swarm-leak-test, loop row L2-2). Planted fault: a clear lets a writer of the cleared run reach the next run's log.

    The suites clear a declared log by removing the file. A writer of the
    cleared run that still holds the old file's lock completes its record on
    the removed file: the next run's log is neither blocked by that lock nor
    given the late record. A clear that empties the file in place instead
    would wait on the old writer and then hand its record to the next run.
    """
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    child, gap = _start_split_writer(tmp_path, log)
    try:
        log.unlink()  # the suites' clear between runs
        append_record(log, {"seq": 2}, timeout=2)
        assert read_records(log, timeout=2) == [{"seq": 2}]
    finally:
        _finish(child, gap)
    assert child.returncode == 0, child.stderr.read() if child.stderr else ""
    assert read_records(log) == [{"seq": 2}], "the cleared run's late record reached the next run's log"


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


def test_text_append_refuses_declared_logs(tmp_path: Path) -> None:
    """A text append cannot bypass the declared logs' JSON-record API."""
    for name in atomic_test_log.STAND_IN_LOGS:
        log = tmp_path / name
        with pytest.raises(ValueError, match="use append_record"):
            text_append(log, json.dumps({"seq": 1}) + "\n")
        assert not log.exists(), "a refused text append created the log"
        append_record(log, {"seq": 1})
        with pytest.raises(ValueError, match="use append_record"):
            text_append(log, "malformed\n")
        assert read_records(log) == [{"seq": 1}], "a refused text append altered the log"


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

    A direct read, an append through a variable, a nested reader closing over
    its enclosing function's log (finding F6-4), an embedded stand-in append
    and an append through an environment key that carries a log path are
    each detected with their source location; helper calls, a log's removal,
    a document append, a lock probe and a file whose name merely ends in a
    declared one (loop row L2-3) and a parameter that shadows a module-level log
    binding (finding F6-5) stay unflagged without any exemption. Every binding
    form carries a log's identity, unpacking element-wise (finding F6-6), and
    shadows an enclosing log binding; a pathlib read or write is judged by its
    receiver, never by the content it writes (finding F6-7).
    """
    cases = {
        "top_read": (TOP_READ, [":2: raw read_text"]),
        "variable_append": (VARIABLE_APPEND, [":4: raw open"]),
        "embedded_append": (EMBEDDED_APPEND, [":4: raw open"]),
        "env_routed": (ENV_ROUTED, [":5: raw open"]),
        "safe_operations": (SAFE_OPERATIONS, []),
        "near_miss": (NEAR_MISS, []),
        "positional_append": ('open("@LOG@", "a")\n', [":1: raw open"]),
        "keyword_append": ('open(file="@LOG@", mode="a")\n', [":1: raw open"]),
        "positional_read": ('open("@LOG@")\n', [":1: raw open"]),
        "keyword_read": ('open(file="@LOG@")\n', [":1: raw open"]),
        "mixed_append": ('open("@LOG@", mode="a")\n', [":1: raw open"]),
        "keyword_document": ('open(file="notes.md", mode="a")\n', []),
        "closure_read": (CLOSURE_READ, [":6: raw read_text"]),
        "parameter_shadow": (PARAMETER_SHADOW, []),
        "binding_forms": (
            BINDING_FORMS,
            [
                ":3: raw read_text",
                ":7: raw read_text",
                ":10: raw read_bytes",
                ":13: raw write_bytes",
                ":15: raw read_text",
                ":17: raw read_text",
                ":19: raw read_text",
                ":20: raw read_text",
                ":22: raw read_text",
                ":24: raw read_text",
                ":27: raw read_text",
            ],
        ),
        "binding_shadows": (BINDING_SHADOWS, []),
        "receiver_destination": (RECEIVER_DESTINATION, [":4: raw read_text"]),
    }
    for name, (sample, expected) in cases.items():
        folder = tmp_path / name
        folder.mkdir()
        (folder / f"planted_{name}.py").write_text(_render(sample), encoding="utf-8")
        found = find_raw_log_access(folder)
        assert len(found) == len(expected), (name, found)
        for line, wanted in zip(found, expected, strict=True):
            assert f"planted_{name}.py" in line and wanted in line, (name, found)


# ---------------------------------------------------------------------------
# The runtime check: the choke point behind the static guard (decisions.md#Q-5)
# ---------------------------------------------------------------------------

# A test the runtime check must fail although its own code swallows the refusal,
# directly and in a thread; `@LOG@` becomes a declared log name at use time.
SWALLOWED = """
import threading

import pytest
import stand_in_log_guard
from atomic_test_log import append_record


def test_swallowed_in_the_test(tmp_path):
    log = tmp_path / "@LOG@"
    append_record(log, {"seq": 1})
    try:
        log.read_text()
    except Exception:
        pass


def test_swallowed_in_a_thread(tmp_path):
    log = tmp_path / "@LOG@"
    append_record(log, {"seq": 1})

    def observe():
        try:
            open(log).read()
        except Exception:
            pass

    reader = threading.Thread(target=observe)
    reader.start()
    reader.join()


@pytest.fixture(params=["yield", "addfinalizer"])
def swallowed_finalizer(request, tmp_path):
    def get_log():
        return tmp_path / "@LOG@"

    append_record(get_log(), {"seq": 1})

    def finalize():
        try:
            get_log().read_text()
        except stand_in_log_guard.RawStandInLogAccess:
            pass

    if request.param == "addfinalizer":
        request.addfinalizer(finalize)
    yield
    if request.param == "yield":
        finalize()


def test_swallowed_in_a_finalizer(swallowed_finalizer):
    pass


def test_after_finalizers():
    assert stand_in_log_guard.take_violations() == []


def test_helper_only(tmp_path, request):
    log = tmp_path / "@LOG@"
    append_record(log, {"seq": 1})
    assert [record["seq"] for record in __import__("atomic_test_log").read_records(log)] == [1]
    request.addfinalizer(lambda: __import__("atomic_test_log").read_records(log))
"""


def _declared_log(folder: Path) -> Path:
    """A declared log's path, returned from a call so the static advisory does not follow it (its stated boundary)."""
    return folder / atomic_test_log.STAND_IN_LOGS[0]


def test_runtime_check_refuses_raw_access_to_declared_logs(tmp_path: Path) -> None:
    """Probe intentional refusals outside pytest's session audit in an isolated process."""
    run = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; from pathlib import Path; import test_atomic_test_log as tests; "
            "tests.stand_in_log_guard.install(); tests._check_raw_access_forms(Path(sys.argv[1]))",
            str(tmp_path),
        ],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert run.returncode == 0, run.stdout + run.stderr


def _check_raw_access_forms(tmp_path: Path) -> None:
    """Criterion 5 (flaky-swarm-leak-test, decisions.md#Q-5, finding F6-8). Planted fault: a raw access of a declared log runs.

    Each raw spelling, including both forms of phase-6 row F6-8 that the
    static advisory cannot follow (a comprehension's first iterable and a
    parameter default), must fail at run time before touching the file.
    """
    log = _declared_log(tmp_path)
    append_record(log, {"seq": 1})
    stand_in_log_guard.take_violations()

    def reader(log=log):
        return log.read_text()

    forms = {
        "open_read": lambda: open(log).read(),  # noqa: SIM115, PTH123 - the planted raw access
        "open_append": lambda: open(str(log), "a").write("leak\n"),  # noqa: SIM115, PTH123 - the planted raw access
        "open_keyword": lambda: open(file=log, mode="a"),  # noqa: SIM115, PTH123 - the planted raw access
        "io_open": lambda: io.open(log, "rb"),  # noqa: SIM115, UP020 - the planted raw access
        "os_open": lambda: os.open(log, os.O_RDONLY),
        "path_open": lambda: log.open("a"),
        "read_text": lambda: log.read_text(),
        "read_bytes": lambda: log.read_bytes(),
        "write_text": lambda: log.write_text("leak\n"),
        "write_bytes": lambda: log.write_bytes(b"leak\n"),
        "class_read_text": lambda: Path.read_text(log),
        "f6_8_comprehension": lambda: [log.read_text() for log in [log]],
        "f6_8_default": reader,
    }
    for name, form in forms.items():
        with pytest.raises(stand_in_log_guard.RawStandInLogAccess, match="read_records / append_record"):
            form()
        recorded = stand_in_log_guard.take_violations()
        assert len(recorded) == 1 and log.name in recorded[0], (name, recorded)
        assert "test_atomic_test_log.py" in recorded[0], (name, recorded)
    assert read_records(log) == [{"seq": 1}], "a refused raw access changed the log"


def test_runtime_check_lets_the_helper_through(tmp_path: Path) -> None:
    """Criterion 5 (flaky-swarm-leak-test, decisions.md#Q-5). Planted fault: the runtime check refuses a locked helper access or an unrelated file.

    The helper's append and read pass on the main thread and in the observer
    threads the suites use; a document, a name that merely ends in a declared
    one, removal and existence checks stay untouched.
    """
    stand_in_log_guard.take_violations()
    log = _declared_log(tmp_path)
    append_record(log, {"seq": 1})
    outcome: dict = {}

    def observe() -> None:
        try:
            append_record(log, {"seq": 2})
            outcome["records"] = read_records(log)
        except Exception as error:
            outcome["error"] = error

    reader = threading.Thread(target=observe)
    reader.start()
    reader.join(timeout=60)
    assert "error" not in outcome, outcome
    assert outcome["records"] == [{"seq": 1}, {"seq": 2}]
    document = tmp_path / "notes.md"
    text_append(document, "first\n")
    assert document.read_text(encoding="utf-8") == "first\n"
    near_miss = tmp_path / ("old-" + log.name)
    near_miss.write_text("{}\n", encoding="utf-8")
    with near_miss.open(encoding="utf-8") as handle:
        assert handle.read() == "{}\n"
    assert log.exists()
    log.unlink()
    assert read_records(log) == []
    assert stand_in_log_guard.take_violations() == []


def test_runtime_check_fails_a_test_that_swallows_the_refusal(tmp_path: Path) -> None:
    """Criterion 5 (flaky-swarm-leak-test, decisions.md#Q-5). Planted fault: code under test swallows the refusal and the test passes.

    The swarm gates turn an exception into a refusal by design, so a raised
    error alone can vanish. A separate pytest run over the repository's own
    conftest, guard and helper must fail both swallowing tests - in the test
    body, in a thread and in yield/addfinalizer fixture teardown - and pass
    the following clean test and helper-only access, including its finalizer.
    """
    project = tmp_path / "project"
    project.mkdir()
    for name in ("conftest.py", "stand_in_log_guard.py", "runner_clock_guard.py", "atomic_test_log.py"):
        (project / name).write_text((HERE / name).read_text(encoding="utf-8"), encoding="utf-8")
    (project / "test_swallowed.py").write_text(_render(SWALLOWED), encoding="utf-8")
    (project / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "no:xdist", str(project)],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=180,
    )
    output = run.stdout + run.stderr
    assert run.returncode == 1, output
    assert "2 failed, 4 passed, 2 errors" in output, output
    audit = output.split("stand-in log access violations", 1)[1]
    for name in (
        "test_swallowed_in_the_test",
        "test_swallowed_in_a_thread",
        "test_swallowed_in_a_finalizer[yield]",
        "test_swallowed_in_a_finalizer[addfinalizer]",
    ):
        assert f"test_swallowed.py::{name}: raw" in audit, output
    for style in ("yield", "addfinalizer"):
        assert f"ERROR test_swallowed.py::test_swallowed_in_a_finalizer[{style}]" in output, output
    assert output.count("raw read_text of the declared stand-in log") >= 1, output
    assert output.count("raw open of the declared stand-in log") >= 1, output


@pytest.mark.parametrize("drain", [False, True])
@pytest.mark.parametrize("workers", [0, 2])
@pytest.mark.parametrize("outcome", ["pass", "skip", "xfail", "error", "finalizer", "setup"])
def test_runtime_check_keeps_every_access_until_session_finish(
    tmp_path: Path, workers: int, outcome: str, drain: bool
) -> None:
    """F6-10: even skip/xfail and draining the phase buffer cannot erase an access."""
    project = tmp_path / "project"
    project.mkdir()
    for name in ("conftest.py", "stand_in_log_guard.py", "runner_clock_guard.py", "atomic_test_log.py"):
        (project / name).write_text((HERE / name).read_text(encoding="utf-8"), encoding="utf-8")
    source = """
import pytest
import stand_in_log_guard
from pathlib import Path


def access():
    try:
        Path("@LOG@").read_text()
    except stand_in_log_guard.RawStandInLogAccess:
        pass
    if DRAIN:
        stand_in_log_guard.take_violations()


@pytest.fixture
def setup_access():
    access()
    pytest.skip("after setup access")


@pytest.fixture
def finalizer_access(request):
    def finalize():
        access()
        pytest.skip("after finalizer access")
    request.addfinalizer(finalize)


def test_recorded(request):
    if OUTCOME == "setup":
        request.getfixturevalue("setup_access")
    elif OUTCOME == "finalizer":
        request.getfixturevalue("finalizer_access")
    else:
        access()
        if OUTCOME == "skip":
            pytest.skip("after access")
        elif OUTCOME == "xfail":
            pytest.xfail("after access")
        elif OUTCOME == "error":
            raise ValueError("after access")


def test_clean():
    pass
"""
    (project / "test_recorded.py").write_text(
        f"OUTCOME = {outcome!r}\nDRAIN = {drain!r}\n" + _render(source), encoding="utf-8"
    )
    (project / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-n", str(workers), str(project)],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=180,
    )
    output = run.stdout + run.stderr
    assert run.returncode == 1, output
    assert "stand-in log access violations" in output, output
    assert "test_recorded.py::test_recorded" in output, output
    assert "raw read_text" in output, output
    assert "1 passed" in output or "2 passed" in output, output


# ---------------------------------------------------------------------------
# The per-key call counter beside a log (change standin-call-counter)
# ---------------------------------------------------------------------------

# Independent counted writers: each signals it is ready, waits for one shared
# start signal, then appends counted records alternating a shared key and its own.
COUNTED_WRITER = """
import sys
import time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import atomic_test_log
data = Path(sys.argv[2])
writer = sys.argv[3]
go = Path(sys.argv[4])
Path(sys.argv[5]).write_text("ready")
deadline = time.time() + 60
while not go.exists() and time.time() < deadline:
    time.sleep(0.005)
for seq in range(8):
    key = "shared" if seq % 2 == 0 else writer
    def build(index, key=key, seq=seq):
        return {"key": key, "writer": writer, "seq": seq, "index": index, "payload": sys.argv[6]}
    atomic_test_log.append_counted(data, key, build)
"""

# A counted writer of the old log generation that pauses, holding the old
# log's lock, either inside its record builder (after its count was taken)
# or inside its counter publication (the temporary file written, not yet
# replaced) until the test's `go.marker`. It prints the index it received.
PAUSED_WRITER = """
import sys
import time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import atomic_test_log
data = Path(sys.argv[2])
gap = Path(sys.argv[3])
pause = sys.argv[4]


def wait():
    (gap / "started.marker").write_text("paused")
    deadline = time.time() + 60
    while not (gap / "go.marker").exists() and time.time() < deadline:
        time.sleep(0.02)


if pause == "publish":
    replace = Path.replace

    def paused_replace(self, target):
        wait()
        return replace(self, target)

    Path.replace = paused_replace


def build(index):
    if pause == "build":
        wait()
    return {"key": "a", "writer": "old", "index": index}


print(atomic_test_log.append_counted(data, "a", build))
"""

COUNTER_FIELDS = {"device", "inode", "size", "counts"}


def _counted(key: str, writer: str = "test"):
    """A record builder for `append_counted` that keeps the index it received."""
    return lambda index: {"key": key, "writer": writer, "index": index}


def _start_paused_writer(tmp_path: Path, log: Path, pause: str) -> tuple[subprocess.Popen, Path]:
    gap = tmp_path / f"gap-{pause}"
    gap.mkdir()
    script = tmp_path / "paused_writer.py"
    script.write_text(PAUSED_WRITER, encoding="utf-8")
    child = subprocess.Popen(
        [sys.executable, str(script), str(HERE), str(log), str(gap), pause],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    _wait_for(gap / "started.marker", child)
    return child, gap


def _child_output(child: subprocess.Popen) -> str:
    out = child.stdout.read() if child.stdout else ""
    err = child.stderr.read() if child.stderr else ""
    assert child.returncode == 0, err[-2000:]
    return out


def _check_counter_access(tmp_path: Path) -> None:
    """Criterion 7 (standin-call-counter), run under the installed guard in an isolated process.

    The helper's counted append and counter read pass; every raw access to
    the counter, and a raw access a record builder makes while
    `append_counted` runs it, is refused before touching either file.
    """
    tmp_path.mkdir(parents=True, exist_ok=True)
    log = _declared_log(tmp_path)
    counter = counter_path(log)
    assert counter.name in atomic_test_log.STAND_IN_COUNTERS
    assert counter.name in atomic_test_log.STAND_IN_FILES
    stand_in_log_guard.take_violations()
    assert append_counted(log, "a", _counted("a")) == 0
    assert read_counter(log)["counts"] == {"a": 1}
    assert stand_in_log_guard.take_violations() == [], "the helper's locked access was refused"
    forms = {
        "open_read": lambda: open(counter).read(),  # noqa: SIM115, PTH123 - the planted raw access
        "open_write": lambda: open(counter, "w"),  # noqa: SIM115, PTH123 - the planted raw access
        "os_open": lambda: os.open(counter, os.O_RDONLY),
        "read_text": lambda: counter.read_text(),
        "write_text": lambda: counter.write_text("{}"),
        "builder_reads_log": lambda: append_counted(
            log, "a", lambda index: {"key": "a", "index": index, "raw": log.read_text()}
        ),
        "builder_reads_counter": lambda: append_counted(
            log, "a", lambda index: {"key": "a", "index": index, "raw": counter.read_bytes()}
        ),
    }
    for name, form in forms.items():
        with pytest.raises(stand_in_log_guard.RawStandInLogAccess, match="read_records / append_record"):
            form()
        recorded = stand_in_log_guard.take_violations()
        assert len(recorded) == 1, (name, recorded)
        assert "test_atomic_test_log.py" in recorded[0], (name, recorded)
    with pytest.raises(ValueError, match="use append_counted"):
        text_append(counter, "{}")
    assert read_records(log) == [{"key": "a", "writer": "test", "index": 0}], "a refused access changed the log"
    assert read_counter(log)["counts"] == {"a": 1}, "a refused access changed the counter"


def test_counter_guard_and_locked_access(tmp_path: Path) -> None:
    """Criterion 7 (standin-call-counter). Planted fault: raw counter access passes, or a builder escapes the guard.

    The refusals run in an isolated process, outside this session's audit.
    Here, a writer holding the log's lock mid-record makes the counted
    append wait and time out instead of reading the partial record or
    publishing a counter beside it; once released, the count is rebuilt from
    the completed log.
    """
    run = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; from pathlib import Path; import test_atomic_test_log as tests; "
            "tests.stand_in_log_guard.install(); tests._check_counter_access(Path(sys.argv[1]))",
            str(tmp_path / "isolated"),
        ],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    assert append_counted(log, "a", _counted("a")) == 0
    published = read_counter(log)
    child, gap = _start_split_writer(tmp_path, log)
    try:
        with pytest.raises(TimeoutError):
            append_counted(log, "a", _counted("a"), timeout=0.3)
        assert read_counter(log) == published, "a counter was published while another writer held the log"
    finally:
        _finish(child, gap)
    assert child.returncode == 0, child.stderr.read() if child.stderr else ""
    assert append_counted(log, "a", _counted("a")) == 1
    assert [record.get("key") for record in read_records(log)] == ["a", None, "a"]


def test_counter_serializes_parallel_calls_with_log(tmp_path: Path) -> None:
    """Criterion 2 (standin-call-counter). Planted fault: parallel calls receive duplicate or out-of-order indices.

    Four writer processes released by one start signal append counted
    records with a shared key and their own; each record's index must equal
    the number of earlier records with its key in the serialized log.
    """
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    script = tmp_path / "counted_writer.py"
    script.write_text(COUNTED_WRITER, encoding="utf-8")
    go = tmp_path / "go.marker"
    writers = 4
    ready = [tmp_path / f"ready-{index}.marker" for index in range(writers)]
    children = [
        subprocess.Popen(
            [sys.executable, str(script), str(HERE), str(log), f"w{index}", str(go), str(ready[index]), PAYLOAD],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        for index in range(writers)
    ]
    try:
        for marker, child in zip(ready, children, strict=True):
            _wait_for(marker, child)
        go.write_text("go")
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
    assert len(records) == writers * 8
    seen: dict[str, int] = {}
    for position, record in enumerate(records):
        assert record["payload"] == PAYLOAD, f"record {position} was torn"
        assert record["index"] == seen.get(record["key"], 0), f"record {position} got a count out of log order"
        seen[record["key"]] = seen.get(record["key"], 0) + 1
    stored = read_counter(log)
    status = log.stat()
    assert [stored["device"], stored["inode"], stored["size"]] == [status.st_dev, status.st_ino, status.st_size]
    assert stored["counts"] == seen


def test_late_old_writer_does_not_affect_new_log(tmp_path: Path) -> None:
    """Criterion 6 (standin-call-counter). Planted fault: a late writer of a removed log changes the new run's count.

    The old writer holds the removed log's lock with its count taken; the new
    run starts on a fresh log; then the old writer completes and publishes a
    counter for the removed inode. The new run's next call must still count
    only the new log, and the late record must stay out of it.
    """
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    for expected in range(2):
        assert append_counted(log, "a", _counted("a", "seed")) == expected
    old_inode = log.stat().st_ino
    child, gap = _start_paused_writer(tmp_path, log, "build")
    try:
        log.unlink()  # the suites' clear between runs
        assert append_counted(log, "a", _counted("a", "new"), timeout=2) == 0
    finally:
        _finish(child, gap)
    assert _child_output(child).strip() == "2", "the old writer did not count its own history"
    assert read_counter(log)["inode"] == old_inode, "the late writer's counter publication did not land"
    assert append_counted(log, "a", _counted("a", "new")) == 1
    assert read_records(log) == [
        {"key": "a", "writer": "new", "index": 0},
        {"key": "a", "writer": "new", "index": 1},
    ], "the late writer's record reached the new log"


def _complete_counter(snapshot) -> bool:
    return (
        isinstance(snapshot, dict)
        and set(snapshot) == COUNTER_FIELDS
        and all(type(snapshot[field]) is int for field in ("device", "inode", "size"))
        and isinstance(snapshot["counts"], dict)
    )


def test_counter_publication_is_atomic_across_log_generations(tmp_path: Path) -> None:
    """Criterion 8 (standin-call-counter). Planted fault: a reader sees a partial counter while two generations publish.

    The old-generation writer pauses with its counter staged but not
    replaced; the new generation publishes meanwhile; then the old one
    replaces. A reader thread reads the counter throughout and at each
    synchronized step: every snapshot is complete, and the staged one is not
    visible before its replacement.
    """
    log = tmp_path / atomic_test_log.STAND_IN_LOGS[0]
    for expected in range(2):
        assert append_counted(log, "a", _counted("a", "seed")) == expected
    old_inode = log.stat().st_ino
    snapshots: list = []
    errors: list = []
    stop = threading.Event()

    def observe() -> None:
        while not stop.is_set():
            try:
                snapshots.append(read_counter(log))
            except Exception as error:  # a partial counter shows here
                errors.append(error)

    reader = threading.Thread(target=observe)
    reader.start()
    try:
        child, gap = _start_paused_writer(tmp_path, log, "publish")
        try:
            staged = read_counter(log)
            assert staged["inode"] == old_inode and staged["counts"] == {"a": 2}, "a staged counter became visible"
            log.unlink()
            for expected in range(2):
                assert append_counted(log, "a", _counted("a", "new"), timeout=2) == expected
            fresh = read_counter(log)
            assert fresh["inode"] == log.stat().st_ino and fresh["counts"] == {"a": 2}
        finally:
            _finish(child, gap)
        assert _child_output(child).strip() == "2"
        late = read_counter(log)
        assert late["inode"] == old_inode and late["counts"] == {"a": 3}, "the old generation's counter did not land"
        assert append_counted(log, "a", _counted("a", "new")) == 2
    finally:
        stop.set()
        reader.join(timeout=60)
    assert not reader.is_alive()
    assert errors == [], errors[:3]
    assert snapshots, "the reader read no counter"
    incomplete = [snapshot for snapshot in snapshots if not _complete_counter(snapshot)]
    assert incomplete == [], incomplete[:3]


def test_guard_reports_dynamic_callback(tmp_path: Path) -> None:
    """A dynamic callback is the caller, even while a locked helper invokes it."""
    script = r"""
import os
import sys
from pathlib import Path
import atomic_test_log as helper
import stand_in_log_guard as guard

if os.environ.get("STAGE2_PLANT_FAULT") == "1":
    def skip_dynamic(frame):
        while frame is not None:
            code = frame.f_code
            where = guard._real_file(code.co_filename)
            if code.co_filename.startswith("<") or where == guard._THIS_FILE or where.startswith(guard._STDLIB):
                frame = frame.f_back
                continue
            return code.co_name in guard._HELPER_FUNCTIONS and where == guard._HELPER_FILE
        return False
    guard._from_helper = skip_dynamic

guard.install()
log = Path(sys.argv[1]) / "calls.jsonl"
for target in (log, helper.counter_path(log)):
    namespace = {"target": target}
    exec(compile("def builder(index):\n    return {'key': 'a', 'raw': target.read_text()}\n", "<dynamic callback>", "exec"), namespace)
    try:
        helper.append_counted(log, "a", namespace["builder"])
    except guard.RawStandInLogAccess:
        pass
    else:
        raise AssertionError("dynamic callback raw access was not refused")
    violations = guard.take_violations()
    assert len(violations) == 1 and "<dynamic callback>" in violations[0], violations
"""
    run = subprocess.run(
        [sys.executable, "-c", script, str(tmp_path)],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert run.returncode == 0, run.stdout + run.stderr
