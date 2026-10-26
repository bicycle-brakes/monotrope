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


RUN_CALLS = {"run", "Popen", "check_call", "check_output"}


class _Function(NamedTuple):
    """A module-level function of a test file, as the ratchet reads it."""

    calls: set[str]  # names invoked, rather than merely referenced; shadowed ones left out
    imports: list[tuple[str, str, bool]]  # imports local to this function
    attributes: set[tuple[str, str]]  # invoked `<name>.<attr>`, dunders and shadowed bases left out
    params: set[str]  # parameter names (fixtures shadow module-level names)
    locals: dict[str, list[str]]  # names assigned in the body, with the strings of their values
    runs: list[tuple[list[str], set[str]]]  # per run call: strings and names in its arguments


class _ParsedTestFile(NamedTuple):
    """A test file read once, for every script the ratchet asks about."""

    imports: list[tuple[str, str, bool]]  # (module, bound name, imported as a module?)
    constants: list[tuple[set[str], list[str]]]  # (names bound, strings in the value)
    functions: dict[str, _Function]


def _strings(root: ast.AST) -> list[str]:
    return [k.value for k in ast.walk(root) if isinstance(k, ast.Constant) and isinstance(k.value, str)]


def _is_run_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    callee = node.func
    name = callee.id if isinstance(callee, ast.Name) else callee.attr if isinstance(callee, ast.Attribute) else None
    return name in RUN_CALLS


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
    imports = _imports(list(_scope_nodes(tree)))
    constants = []
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign | ast.AnnAssign) and stmt.value is not None:
            targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
            names = {z.id for z in targets if isinstance(z, ast.Name)}
            constants.append((names, _strings(stmt.value)))
    functions = {}
    for stmt in tree.body:
        if not isinstance(stmt, ast.FunctionDef):
            continue
        nodes = [node for body in stmt.body for node in _scope_nodes(body)]
        spec = stmt.args
        params = {a.arg for a in [*spec.posonlyargs, *spec.args, *spec.kwonlyargs, spec.vararg, spec.kwarg] if a}
        assigned: dict[str, list[str]] = {}
        for node in nodes:
            if isinstance(node, ast.Assign | ast.AnnAssign) and node.value is not None:
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for z in targets:
                    if isinstance(z, ast.Name):
                        assigned.setdefault(z.id, []).extend(_strings(node.value))
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                assigned.setdefault(node.id, [])
        shadowed = params | set(assigned)
        calls = [node.func for node in nodes if isinstance(node, ast.Call)]
        runs = []
        for node in nodes:
            if _is_run_call(node):
                parts = [*node.args, *(k.value for k in node.keywords)]
                runs.append(
                    (
                        [s for p in parts for s in _strings(p)],
                        {k.id for p in parts for k in ast.walk(p) if isinstance(k, ast.Name)},
                    )
                )
        functions[stmt.name] = _Function(
            calls={node.id for node in calls if isinstance(node, ast.Name)} - shadowed,
            imports=_imports(nodes),
            attributes={
                (node.value.id, node.attr)
                for node in calls
                if isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id not in shadowed
                and not node.attr.startswith("__")
            },
            params=params,
            locals=assigned,
            runs=runs,
        )
    return _ParsedTestFile(imports, constants, functions)


def _tests_reaching(text: str, script_file: str) -> list[str]:
    """The mutation-named tests in `text` that reach the script `script_file`.

    A test reaches the script when its body — or the body of a module-level
    helper of the same file it calls, at any depth — calls it: a non-dunder
    attribute of a module bound by `import <script>` (with or without `as`), a
    call to a name bound by `from <script> import …`, or a string naming the
    file handed to a run call (`run`, `Popen`, `check_call`, `check_output`) —
    in its arguments, through a local bound to the command, or through a
    module-level constant. A name that a parameter or an assignment of the
    function rebinds is no longer the module's. A mention in a comparison, a
    docstring or another test reaches nothing; nor does `<module>.__file__`.
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

    def runs_script(fn: _Function) -> bool:
        for strings, used in fn.runs:
            if names_file(strings):
                return True
            for used_name in used:
                if used_name in fn.locals:
                    if names_file(fn.locals[used_name]):
                        return True
                elif used_name in path_names and used_name not in fn.params:
                    return True
        return False

    reached = set()
    for name, fn in parsed.functions.items():
        imports = parsed.imports + fn.imports
        modules = {bound for module, bound, whole in imports if module == stem and whole}
        names = {bound for module, bound, whole in imports if module == stem and not whole}
        if fn.calls & names or any(base in modules for base, _ in fn.attributes) or runs_script(fn):
            reached.add(name)
    while new := {name for name, fn in parsed.functions.items() if name not in reached and fn.calls & reached}:
        reached |= new
    return [name for name in parsed.functions if name in reached and MUTATIONS_NAMEN.search(f"def {name}(")]
