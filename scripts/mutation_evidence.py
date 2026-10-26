"""Mutation evidence for the gate ratchet (RB-G4): which script a gate runs, and
which mutation-named tests reach it.

Moved out of `tests/test_ci.py` (bead coding-harness-diic), so that a repair of
the analyzer can be shown red first: a test in `tests/` runs against the
analyzer in `scripts/`, not against a copy in its own file.
"""

from __future__ import annotations

import ast
import functools
import re
from pathlib import Path
from typing import NamedTuple

# These name forms count as mutation evidence. The list is deliberately bound to
# names and not to comments: a name is carried along when something is renamed,
# a comment is not.
MUTATIONS_NAMEN = re.compile(
    r"^def (test_\w*(?:goes_red|red_on|detects_tampering|refuses|is_caught|catches|"
    r"not_a_write|is_an_error|is_exit_2|never_writes|is_not_a_pass|notices)\w*)\(",
    re.M,
)


def pruefling(gate: dict) -> str:
    """The subject of this gate — the script it runs."""
    befehl = gate.get("command") or ""
    # The subfolder has to be included: until 2026-09-08 the pattern ended before
    # the second `/`, and a script under `scripts/kit/` was invisible to the
    # ratchet — it reported "no script recognisable" and demanded an exception
    # for a gate that had long had its mutation evidence.
    m = re.search(r"(?:scripts|docs/patterns)/(?:[A-Za-z_]+/)*([A-Za-z_]+\.py)", befehl)
    if m:
        return m.group(1)
    # A gate can also run a test file itself — `ruleset-drift` checks a statement
    # about the repo configuration for which there is no script and there should
    # be none: a tool that can change rulesets would be a greater risk than the
    # finding it makes. Its mutation evidence then lies in exactly that file, and
    # that is where the ratchet looks for it too.
    m = re.search(r"(tests/[A-Za-z_]+\.py)", befehl)
    return m.group(1) if m else ""


def evidence(script: str, sources: dict[Path, str]) -> list[str]:
    """The mutation evidence for the script `script`, as `<file>::<test>` names."""
    if script.startswith("tests/"):
        # If the gate runs a test file, its evidence lies IN that file. The
        # search below would instead accept every file that merely MENTIONS
        # the path — on 2026-09-08 that made `test_workflow_entry.py` the
        # evidence for `ruleset-drift`, because it names the name in a list
        # and has some mutation evidence of its own. A coverage that assumes
        # from a mention covers nothing.
        return [
            f"{p.name}::{m}"
            for p, text in sources.items()
            if p.as_posix().endswith(script)
            for m in MUTATIONS_NAMEN.findall(text)
        ]
    # A script is evidenced by a mutation-named test that REACHES it, not by a
    # file that names it (bead coding-harness-a05, maintainer 2026-10-21, option
    # B). On 2026-10-20 a call-site test named the plans-registry renderer only to
    # identify a command, and the ratchet called both plans-registry exceptions
    # stale although no test seeds a fault into the renderer.
    return [f"{p.name}::{t}" for p, text in sources.items() for t in _tests_reaching(text, script)]


class _Function(NamedTuple):
    """A module-level function of a test file, as the ratchet reads it."""

    names: set[str]  # every name used in its body
    calls: set[str]  # names invoked, rather than merely referenced
    imports: list[tuple[str, str, bool]]  # imports local to this function
    attributes: set[tuple[str, str]]  # invoked `<name>.<attr>`, dunders left out
    paths: list[str]  # every string that builds a path or a command


class _ParsedTestFile(NamedTuple):
    """A test file read once, for every script the ratchet asks about."""

    imports: list[tuple[str, str, bool]]  # (module, bound name, imported as a module?)
    constants: list[tuple[set[str], list[str]]]  # (names bound, path strings built)
    functions: dict[str, _Function]


def _path_strings(root: ast.AST, parents: dict[ast.AST, ast.AST]) -> list[str]:
    """Strings used to build paths or command arguments, excluding string predicates."""
    hits = []
    for k in ast.walk(root):
        if not (isinstance(k, ast.Constant) and isinstance(k.value, str)):
            continue
        up = parents.get(k)
        in_command = isinstance(up, ast.List | ast.Tuple) and isinstance(parents.get(up), ast.Call)
        call = up if isinstance(up, ast.Call) else parents.get(up) if isinstance(up, ast.keyword) else None
        callee = call.func if isinstance(call, ast.Call) else None
        call_name = (
            callee.id if isinstance(callee, ast.Name) else callee.attr if isinstance(callee, ast.Attribute) else None
        )
        if (
            (isinstance(up, ast.BinOp) and isinstance(up.op, ast.Div))
            or in_command
            or call_name
            in {"Path", "PurePath", "PurePosixPath", "run", "Popen", "check_call", "check_output", "system"}
        ):
            hits.append(k.value)
    return hits


def _scope_nodes(root: ast.AST):
    """Walk one lexical scope without importing bindings from nested scopes."""
    yield root
    for child in ast.iter_child_nodes(root):
        if not isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | ast.Lambda):
            yield from _scope_nodes(child)


def _imports(nodes: list[ast.AST]) -> list[tuple[str, str, bool]]:
    imports = []
    for node in nodes:
        if isinstance(node, ast.Import):
            imports.extend((a.name, a.asname or a.name, True) for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.extend((node.module, a.asname or a.name, False) for a in node.names)
    return imports


@functools.cache
def _parsed(text: str) -> _ParsedTestFile | None:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    imports = _imports(list(_scope_nodes(tree)))
    constants = []
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign | ast.AnnAssign) and stmt.value is not None:
            targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
            names = {z.id for z in targets if isinstance(z, ast.Name)}
            constants.append((names, _path_strings(stmt.value, parents)))
    functions = {}
    for stmt in tree.body:
        if not isinstance(stmt, ast.FunctionDef):
            continue
        nodes = [node for body in stmt.body for node in _scope_nodes(body)]
        calls = [node.func for node in nodes if isinstance(node, ast.Call)]
        functions[stmt.name] = _Function(
            names={node.id for node in nodes if isinstance(node, ast.Name)},
            calls={node.id for node in calls if isinstance(node, ast.Name)},
            imports=_imports(nodes),
            attributes={
                (node.value.id, node.attr)
                for node in calls
                if isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and not node.attr.startswith("__")
            },
            paths=_path_strings(stmt, parents),
        )
    return _ParsedTestFile(imports, constants, functions)


def _tests_reaching(text: str, script_file: str) -> list[str]:
    """The mutation-named tests in `text` that reach the script `script_file`.

    A test reaches the script when its body — or the body of a module-level
    helper of the same file it calls, at any depth — calls it: a non-dunder
    attribute of a module bound by `import <script>` (with or without `as`), a
    call to a name bound by `from <script> import …`, or a string naming the
    file that builds a path or a command (an operand of `/`, a path constructor
    or command execution argument, or an element of a list or tuple handed
    to a call), directly or through a module-level constant built that way. A mention in a comparison, a docstring
    or another test reaches nothing; nor does `<module>.__file__`.
    """
    stem = script_file.removesuffix(".py")
    if stem not in text:  # neither an import nor a path can name it
        return []
    parsed = _parsed(text)
    if parsed is None:
        return []
    file_re = re.compile(rf"(?:^|[/\s]){re.escape(script_file)}(?:\s|$)")

    def names_file(paths: list[str]) -> bool:
        return any(file_re.search(p) for p in paths)

    path_names = set()
    for bound, paths in parsed.constants:
        if names_file(paths):
            path_names |= bound

    reached = set()
    for name, fn in parsed.functions.items():
        imports = parsed.imports + fn.imports
        modules = {bound for module, bound, whole in imports if module == stem and whole}
        names = {bound for module, bound, whole in imports if module == stem and not whole}
        if (
            fn.calls & names
            or fn.names & path_names
            or any(base in modules for base, _ in fn.attributes)
            or names_file(fn.paths)
        ):
            reached.add(name)
    while new := {name for name, fn in parsed.functions.items() if name not in reached and fn.calls & reached}:
        reached |= new
    return [name for name in parsed.functions if name in reached and MUTATIONS_NAMEN.search(f"def {name}(")]
