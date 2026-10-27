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


RUN_CALLS = {"run", "Popen", "call", "check_call", "check_output"}


class _Imported(NamedTuple):
    """A name resolved through an import, rather than a similarly named call."""

    path: str


def _scope_nodes(root: ast.AST):
    """Walk one lexical scope without importing bindings from nested scopes."""
    yield root
    if isinstance(root, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | ast.Lambda):
        return
    for child in ast.iter_child_nodes(root):
        yield from _scope_nodes(child)


@functools.cache
def _parsed(text: str) -> ast.Module | None:
    """Read each source file once, without importing or executing it."""
    try:
        return ast.parse(text)
    except SyntaxError:
        return None


def _tests_reaching(text: str, script_file: str) -> list[str]:
    """Follow same-file calls and ordered command bindings from mutation tests.

    Only resolved subprocess calls run commands. The script must occupy argv[0]
    or argv[1] after a Python interpreter; other arguments are mere mentions.
    Values are deliberately limited to imports, functions, paths and lists.
    Fixtures and cross-file helpers are not evaluated.
    """
    stem = script_file.removesuffix(".py")
    if stem not in text:
        return []
    tree = _parsed(text)
    if tree is None:
        return []
    hit = False
    module: dict = {}

    def is_script(value):
        return isinstance(value, str) and value.rsplit("/", 1)[-1] == script_file

    def runs_script(command):
        if isinstance(command, str):
            return is_script(command)
        if not isinstance(command, list) or not command:
            return False
        if is_script(command[0]):
            return True
        program = command[0]
        interpreter = program == _Imported("sys.executable") or (
            isinstance(program, str) and re.fullmatch(r"python(?:[0-9]+(?:\.[0-9]+)*)?", program.rsplit("/", 1)[-1])
        )
        return bool(interpreter and len(command) > 1 and is_script(command[1]))

    def imported_gate(path):
        return path in {stem, "scripts." + stem}

    def value(node, env, active):
        nonlocal hit
        if isinstance(node, ast.Name):
            return env.get(node.id)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Attribute):
            base = value(node.value, env, active)
            if isinstance(base, _Imported):
                return _Imported(base.path + "." + node.attr)
        elif isinstance(node, ast.List | ast.Tuple):
            return [value(item, env, active) for item in node.elts]
        elif isinstance(node, ast.JoinedStr):
            return "".join(str(value(part, env, active) or "") for part in node.values)
        elif isinstance(node, ast.FormattedValue):
            return value(node.value, env, active)
        elif isinstance(node, ast.BinOp):
            left = value(node.left, env, active)
            right = value(node.right, env, active)
            if isinstance(node.op, ast.Div) and isinstance(right, str):
                return (left.rstrip("/") + "/" if isinstance(left, str) else "") + right
            if isinstance(node.op, ast.Add) and isinstance(left, str) and isinstance(right, str):
                return left + right
        elif isinstance(node, ast.Call):
            callee = value(node.func, env, active)
            args = [value(arg, env, active) for arg in node.args]
            kwargs = {kw.arg: value(kw.value, env, active) for kw in node.keywords}
            if isinstance(callee, _Imported):
                base, _, name = callee.path.rpartition(".")
                if base == "subprocess" and name in RUN_CALLS:
                    hit |= runs_script(args[0] if args else kwargs.get("args"))
                elif imported_gate(base) and not name.startswith("__"):
                    hit = True
            if isinstance(callee, ast.FunctionDef | ast.AsyncFunctionDef):
                invoke(callee, args, kwargs, active)
            # Preserve path constructors without treating their strings as runs.
            if isinstance(node.func, ast.Name) and node.func.id in {"str", "Path"} and args:
                return args[0]
            if callee == _Imported("pathlib.Path") and args:
                return args[0]
        else:
            # Calls in assertions, comparisons, subscripts and comprehensions
            # still execute; nested function and lambda bodies do not.
            if not isinstance(node, ast.Lambda):
                for child in ast.iter_child_nodes(node):
                    value(child, env, active)
        return None

    def statements(body, env, active):
        for stmt in body:
            if isinstance(stmt, ast.Import):
                for alias in stmt.names:
                    env[alias.asname or alias.name.split(".")[0]] = _Imported(
                        alias.name if alias.asname else alias.name.split(".")[0]
                    )
            elif isinstance(stmt, ast.ImportFrom):
                for alias in stmt.names:
                    env[alias.asname or alias.name] = _Imported(f"{stmt.module}.{alias.name}")
            elif isinstance(stmt, ast.FunctionDef | ast.AsyncFunctionDef):
                env[stmt.name] = stmt
            elif isinstance(stmt, ast.ClassDef):
                env[stmt.name] = None
            elif isinstance(stmt, ast.Assign | ast.AnnAssign):
                assigned = value(stmt.value, env, active) if stmt.value is not None else None
                targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
                for target in targets:
                    if isinstance(target, ast.Name):
                        env[target.id] = assigned
            elif isinstance(stmt, ast.With | ast.AsyncWith):
                for item in stmt.items:
                    value(item.context_expr, env, active)
                statements(stmt.body, env, active)
            elif isinstance(stmt, ast.If | ast.For | ast.AsyncFor | ast.While):
                # Syntax evidence reads both branches, not runtime conditions.
                value(stmt.test if isinstance(stmt, ast.If | ast.While) else stmt.iter, env, active)
                statements(stmt.body, env.copy(), active)
                statements(stmt.orelse, env.copy(), active)
            elif isinstance(stmt, ast.Try):
                statements(stmt.body, env.copy(), active)
                for handler in stmt.handlers:
                    statements(handler.body, env.copy(), active)
                statements(stmt.orelse, env.copy(), active)
                statements(stmt.finalbody, env, active)
            else:
                value(stmt, env, active)

    def invoke(fn, args, kwargs, active):
        if id(fn) in active:
            return
        env = module.copy()
        # Python treats assigned names as local even before the assignment.
        for stmt in fn.body:
            for node in _scope_nodes(stmt):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    env[node.id] = None
        positional = [*fn.args.posonlyargs, *fn.args.args]
        for param in [*positional, *fn.args.kwonlyargs, fn.args.vararg, fn.args.kwarg]:
            if param:
                env[param.arg] = None
        for param, default in zip(positional[-len(fn.args.defaults) :], fn.args.defaults, strict=False):
            env[param.arg] = value(default, module, active)
        for param, arg in zip(positional, args, strict=False):
            env[param.arg] = arg
        for param in [*positional, *fn.args.kwonlyargs]:
            if param.arg in kwargs:
                env[param.arg] = kwargs[param.arg]
        statements(fn.body, env, active | {id(fn)})

    statements(tree.body, module, set())
    tests = []
    for stmt in tree.body:
        if isinstance(stmt, ast.FunctionDef | ast.AsyncFunctionDef):
            tests.append((stmt.name, stmt))
        elif isinstance(stmt, ast.ClassDef):
            tests.extend(
                (f"{stmt.name}::{fn.name}", fn)
                for fn in stmt.body
                if isinstance(fn, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    reached = []
    for name, fn in tests:
        if MUTATIONS_NAMEN.search(f"def {fn.name}("):
            hit = False
            invoke(fn, [], {}, set())
            if hit:
                reached.append(name)
    return reached
