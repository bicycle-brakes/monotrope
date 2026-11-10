#!/usr/bin/env python3
"""The drift check of the central harness configuration (gate `harness-config`).

It measures three things against `scripts/harness_config.py`, the one shared
contract: the configuration validates, every registered binding (the marked
literal in `AGENTS.md`, the placeholder in the implement prompt) is present
and states the configured value, and no live Python under `scripts/` or
`tools/` redeclares an owned setting as a numeric assignment.

Exit vocabulary: 0 is measured agreement, 1 is drift, 3 is unreadable
evidence. Without `--check` the same findings are only reported.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness_config  # noqa: E402

EXIT_OK = 0
EXIT_DRIFT = 1
EXIT_UNREADABLE = 3

# A finding is ("drift" | "unreadable", one diagnostic line naming path and binding).
Findings = list[tuple[str, str]]


def _reserved_findings(path: Path, text: str, snapshot: harness_config.HarnessSnapshot) -> Findings:
    """Every reserved token in one registered text that is malformed or names an unknown key."""
    findings: Findings = []
    for match in harness_config.CANDIDATE.finditer(text):
        candidate = (match.group(1) or "").strip()
        if not harness_config.KEY.fullmatch(candidate):
            findings.append(("drift", f"{path}: malformed reserved token {match.group(0)!r}"))
            continue
        try:
            harness_config.lookup(snapshot, candidate)
        except harness_config.HarnessConfigError as error:
            findings.append(("drift", f"{path}: {error.reason}"))
    # What remains after every well-formed token is removed must hold no
    # reserved prefix: an unclosed `{{ harness.` survives the candidate scan.
    leftover = harness_config.RESERVED_PREFIX.search(harness_config.CANDIDATE.sub("", text))
    if leftover:
        fragment = text[leftover.start() : leftover.start() + 40]
        findings.append(("drift", f"{path}: malformed reserved token {fragment!r}"))
    return findings


def _placeholder_findings(path: Path, text: str, dotted: str, snapshot: harness_config.HarnessSnapshot) -> Findings:
    """The registered placeholder must be present; a literal at its site is drift."""
    findings: Findings = []
    registered = re.compile(r"\{\{\s*harness\." + re.escape(dotted) + r"\s*\}\}")
    if not registered.search(text):
        findings.append(("drift", f"{path}: the registered placeholder for {dotted} is missing"))
    findings.extend(_reserved_findings(path, text, snapshot))
    return findings


def _marker_findings(path: Path, text: str, dotted: str, snapshot: harness_config.HarnessSnapshot) -> Findings:
    """Every well-formed marker must state the configured value; the required one must exist."""
    findings: Findings = []
    marked = 0
    matches = list(harness_config.MARKER.finditer(text))
    for match in matches:
        key, literal = match.group(1), match.group(2).strip()
        try:
            value = harness_config.lookup(snapshot, key)
        except harness_config.HarnessConfigError as error:
            findings.append(("drift", f"{path}: {error.reason}"))
            continue
        if str(value) != literal:
            findings.append(
                (
                    "drift",
                    f"{path}: the marker for {key} states {literal!r}; the configuration states {value!r}",
                )
            )
        if key == dotted:
            marked += 1
    if not marked:
        findings.append(("drift", f"{path}: the required marker for {dotted} is missing"))
    malformed = len(harness_config.MARKER_OPEN.findall(text)) - len(matches)
    if malformed:
        findings.append(("drift", f"{path}: {malformed} harness-config marker(s) are malformed"))
    return findings


def _binding_findings(root: Path, snapshot: harness_config.HarnessSnapshot) -> Findings:
    """The registered bindings of every owned setting, measured against the snapshot."""
    findings: Findings = []
    for relative, dotted, kind in harness_config.REQUIRED_BINDINGS:
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            findings.append(("unreadable", f"{path}: the registered binding cannot be read ({error})"))
            continue
        if kind == "placeholder":
            findings.extend(_placeholder_findings(path, text, dotted, snapshot))
        else:
            findings.extend(_marker_findings(path, text, dotted, snapshot))
    return findings


def _target_name(target: ast.expr) -> str | None:
    """The plain name an assignment binds, or None for everything else."""
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return None


def _numeric_constant(node: ast.expr | None) -> bool:
    """Whether the expression is a numeric literal; a Boolean is not a count."""
    return isinstance(node, ast.Constant) and isinstance(node.value, int | float) and not isinstance(node.value, bool)


def _named_declarations(path: Path, node: ast.AST, owned: set[str]) -> Findings:
    """The numeric declarations of an owned name in one syntax node."""
    findings: Findings = []
    line = getattr(node, "lineno", 0)
    if isinstance(node, ast.Assign) and _numeric_constant(node.value):
        names = {name for name in (_target_name(target) for target in node.targets) if name}
        for name in sorted(names & owned):
            findings.append(
                (
                    "drift",
                    f"{path}:{line}: numeric declaration of {name}; the central configuration owns this setting",
                )
            )
    elif isinstance(node, ast.AnnAssign) and _numeric_constant(node.value):
        name = _target_name(node.target)
        if name in owned:
            findings.append(
                (
                    "drift",
                    f"{path}:{line}: numeric declaration of {name}; the central configuration owns this setting",
                )
            )
    elif isinstance(node, ast.Dict):
        for key in node.keys:
            if isinstance(key, ast.Constant) and key.value in owned:
                findings.append(
                    (
                        "drift",
                        f"{path}:{line}: a dict key names the owned setting {key.value}; the central configuration owns it",
                    )
                )
    return findings


def _live_python(root: Path) -> list[Path]:
    """The Python files whose declarations count as live authority.

    Tests and history are not duplicate-authority inputs: fixtures plant
    faults on purpose, so `test_` files and tests directories stay outside
    the scan.
    """
    found: list[Path] = []
    for top in ("scripts", "tools"):
        base = root / top
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.py")):
            relative = path.relative_to(root)
            if path.name.startswith("test_") or "__pycache__" in relative.parts:
                continue
            if "tests" in relative.parts[:-1]:
                continue
            found.append(path)
    return found


def _declaration_findings(root: Path) -> Findings:
    """Every live numeric redeclaration of an owned setting, with its location."""
    findings: Findings = []
    owned = set(harness_config.OWNED_NAMES)
    for path in _live_python(root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError) as error:
            findings.append(("unreadable", f"{path}: live Python cannot be scanned ({error})"))
            continue
        for node in ast.walk(tree):
            findings.extend(_named_declarations(path, node, owned))
    return findings


def measure(root: Path) -> Findings:
    """Every drift and unreadable finding of one root, as (kind, diagnostic)."""
    try:
        snapshot = harness_config.load(root)
    except harness_config.HarnessConfigError as error:
        return [("unreadable", str(error))]
    findings = _binding_findings(root, snapshot)
    findings.extend(_declaration_findings(root))
    return findings


def main(argv: list[str] | None = None) -> int:
    """Report the findings; with `--check`, turn them into the exit code."""
    parser = argparse.ArgumentParser(description="The drift check of the central harness configuration.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="the repository root to measure (default: this checkout)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="enforce: exit 1 on drift and 3 on unreadable evidence instead of only reporting",
    )
    args = parser.parse_args(argv)
    findings = measure(args.root)
    for _, line in findings:
        print(line, file=sys.stderr)
    if not findings:
        print("the central harness configuration holds")
    if not args.check:
        return EXIT_OK
    if any(kind == "unreadable" for kind, _ in findings):
        return EXIT_UNREADABLE
    return EXIT_DRIFT if findings else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
