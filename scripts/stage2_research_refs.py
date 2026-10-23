"""Typed references resolved exclusively against frozen research source bytes.

A successful lookup yields the complete structural extent. Claim-level assembly
checks every reference first and shares one Unicode-character excerpt budget.
No function here opens a repository file or performs a model operation.
"""

from __future__ import annotations

import ast
import json
import math
import re
from datetime import date, datetime
from pathlib import PurePosixPath

import yaml


class UnsupportedReference(ValueError):
    """A source cannot support this exact reference."""


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise UnsupportedReference("duplicate mapping key")
        result[key] = value
    return result


class _UniqueSafeLoader(yaml.SafeLoader):
    pass


def _yaml_mapping(loader, node):
    # Reject duplicate keys, including those introduced by YAML merge keys.
    loader.flatten_mapping(node)
    return _pairs(
        [
            (loader.construct_object(key, deep=True), loader.construct_object(value, deep=True))
            for key, value in node.value
        ]
    )


_UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _yaml_mapping)


def _canonical(value):
    if isinstance(value, date | datetime):
        return value.isoformat()
    if value is None or isinstance(value, str | bool | int):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return value
    if isinstance(value, list):
        return [_canonical(item) for item in value]
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        return {key: _canonical(item) for key, item in value.items()}
    raise UnsupportedReference("value has no canonical JSON representation")


def _markdown_scan(lines):
    active = []
    headings = []
    frontmatter = bool(lines and lines[0].rstrip("\r\n") == "---")
    fence = None
    for index, line in enumerate(lines):
        text = line.rstrip("\r\n")
        if frontmatter:
            if index and text == "---":
                frontmatter = False
            continue
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}[ \t]*", text):
                fence = None
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", text)
        if opening:
            run = opening.group(1)
            fence = (run[0], len(run))
            continue
        active.append(index)
        match = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+(.*)|$)", text)
        if match:
            title = re.sub(r"(?:^|[ \t]+)#+[ \t]*$", "", match.group(2) or "").strip()
            headings.append((index, len(match.group(1)), title))
    return active, headings


def _markdown_extent(lines, reference):
    active, headings = _markdown_scan(lines)
    criterion = re.fullmatch(r"criterion ([1-9][0-9]*)", reference)
    target = "Acceptance criteria" if criterion else reference
    matches = [(line, level) for line, level, title in headings if title == target and (not criterion or level == 2)]
    if len(matches) != 1:
        raise UnsupportedReference("heading is absent or ambiguous")
    start, level = matches[0]
    end = next((line for line, other, _ in headings if line > start and other <= level), len(lines))
    if criterion:
        items = []
        for index in active:
            if start < index < end:
                item = re.match(r"^ {0,3}([1-9][0-9]*)\.[ \t]+", lines[index])
                if item:
                    items.append((index, item.group(1)))
        matches = [index for index, number in items if number == criterion.group(1)]
        if len(matches) != 1:
            raise UnsupportedReference("criterion is absent or ambiguous")
        start = matches[0]
        stops = [line for line, _ in items if line > start] + [line for line, _, _ in headings if start < line < end]
        end = min(stops, default=end)
    return start, end


def _python_extent(text, reference):
    tree = ast.parse(text)
    definitions = []

    def scan(nodes, prefix=""):
        for node in nodes:
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
                name = prefix + node.name
                if name == reference:
                    definitions.append(node)
                scan(node.body, name + ".")
                continue
            if not prefix:
                targets = (
                    node.targets
                    if isinstance(node, ast.Assign)
                    else [node.target]
                    if isinstance(node, ast.AnnAssign | ast.AugAssign)
                    else [node.name]
                    if isinstance(node, ast.TypeAlias)
                    else []
                )
                if any(
                    isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store) and child.id == reference
                    for target in targets
                    for child in ast.walk(target)
                ):
                    definitions.append(node)
            # Conditions, loops, match cases and exception handlers do not
            # introduce Python lexical scopes. Function/class bodies do.
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.stmt):
                    scan([child], prefix)
                elif isinstance(child, ast.ExceptHandler | ast.match_case):
                    scan(child.body, prefix)

    scan(tree.body)
    if len(definitions) != 1:
        raise UnsupportedReference("definition is absent or ambiguous")
    node = definitions[0]
    return node.lineno - 1, node.end_lineno


def resolve_research_reference(sources, path, reference):
    """Return a typed source extent or an explicit unsupported result."""
    base = {"path": path, "reference": reference, "supported": False}
    try:
        if (
            not isinstance(path, str)
            or not isinstance(reference, str)
            or not reference
            or any(char in reference for char in "\r\n\0")
        ):
            raise UnsupportedReference("invalid reference")
        parsed = PurePosixPath(path)
        if parsed.is_absolute() or ".." in parsed.parts or str(parsed) != path or "\\" in path or path not in sources:
            raise UnsupportedReference("path is absent from the frozen packet")
        text = sources[path].decode("utf-8")
        lines = text.splitlines(keepends=True)
        suffix = parsed.suffix.lower()
        if suffix == ".md":
            start, end = _markdown_extent(lines, reference)
        elif suffix == ".py":
            start, end = _python_extent(text, reference)
        elif suffix in (".yaml", ".yml", ".json"):
            if suffix == ".json":

                def reject_constant(_value):
                    raise UnsupportedReference("non-finite JSON value")

                value = json.loads(text, object_pairs_hook=_pairs, parse_constant=reject_constant)
            else:
                value = yaml.load(text, Loader=_UniqueSafeLoader)
            for segment in reference.split("."):
                if not segment or not isinstance(value, dict) or segment not in value:
                    raise UnsupportedReference("mapping key is absent or not citable")
                value = value[segment]
            excerpt = json.dumps(
                _canonical(value), ensure_ascii=False, sort_keys=True, indent=2, separators=(",", ": ")
            )
            excerpt.encode("utf-8")  # Lone escaped surrogates cannot enter a UTF-8 artifact.
            return {**base, "supported": True, "excerpt": excerpt, "start_line": None, "end_line": None}
        else:
            pattern = re.compile(r"(?<!\w)" + re.escape(reference) + r"(?!\w)")
            start = next((index for index, line in enumerate(lines) if pattern.search(line)), None)
            if start is None:
                raise UnsupportedReference("whole-word reference is absent")
            end = len(lines)
        return {
            **base,
            "supported": True,
            "excerpt": "".join(lines[start:end]),
            "start_line": start + 1,
            "end_line": end,
        }
    except (
        UnsupportedReference,
        SyntaxError,
        UnicodeError,
        ValueError,
        TypeError,
        yaml.YAMLError,
        RecursionError,
    ) as error:
        return {**base, "reason": str(error)}


def research_claim_evidence(sources, citations):
    """An unsupported citation invalidates the entire claim before excerpts are capped."""
    if not isinstance(citations, list) or any(
        not isinstance(item, dict) or "path" not in item or "reference" not in item for item in citations
    ):
        return {"supported": False, "references": [], "reason": "invalid citation list"}
    resolved = [resolve_research_reference(sources, item["path"], item["reference"]) for item in citations]
    if not resolved or any(not item["supported"] for item in resolved):
        return {
            "supported": False,
            "references": [{key: value for key, value in item.items() if key != "excerpt"} for item in resolved],
        }
    remaining = 4000
    for item in resolved:
        excerpt = item["excerpt"]
        item["excerpt"] = excerpt[:remaining]
        item["truncated"] = len(excerpt) > remaining
        remaining -= len(item["excerpt"])
    return {"supported": True, "references": resolved}
