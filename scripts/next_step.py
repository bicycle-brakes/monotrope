"""The next-step instruction: its schema validator and its atomic publisher.

A verb that names the caller's next action leaves a machine-readable `next.json` beside the loop
record (spec of ladder-next-step, criteria 16-24). The shape is declared in `next_step_schema.json`;
this module is the one validator against that declaration and the one writer of the file. No
third-party schema library is a dependency of the runner, so the validator reads the keyword subset
the declaration uses (`type`, `const`, `enum`, `minLength`, `pattern`, `items`, `minItems`,
`maxItems`, `required`, `properties`, `additionalProperties`, `allOf`, `if`/`then`/`else`) and
refuses a declaration that uses another one instead of ignoring it.

The module never reads a clock: the caller passes the UTC instant it wants written.
"""

from __future__ import annotations

import contextlib
import datetime as dt
import json
import os
import re
import tempfile
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent / "next_step_schema.json"
FILE_NAME = "next.json"
SCHEMA_VERSION = 1
VERBS = ("review", "repair", "hand", "review-loop")

_ANNOTATIONS = {"$schema", "title", "description"}
_KEYWORDS = {
    "type",
    "const",
    "enum",
    "minLength",
    "pattern",
    "items",
    "minItems",
    "maxItems",
    "required",
    "properties",
    "additionalProperties",
    "allOf",
    "if",
    "then",
    "else",
}


class InvalidNextStep(ValueError):
    """The record does not satisfy the declared schema, or cannot be published."""


def load_schema() -> dict:
    """The declared schema, read fresh from its file."""
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _type_ok(value: object, name: str) -> bool:
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "string":
        return isinstance(value, str)
    if name == "array":
        return isinstance(value, list)
    if name == "object":
        return isinstance(value, dict)
    raise InvalidNextStep(f"the schema declares an unsupported type `{name}`")


def _check(value: object, schema: dict, path: str) -> list[str]:
    """Every violation of `schema` by `value`, each naming its place."""
    unknown = set(schema) - _KEYWORDS - _ANNOTATIONS
    if unknown:
        raise InvalidNextStep(f"the schema uses unsupported keywords at {path}: {', '.join(sorted(unknown))}")
    problems: list[str] = []
    if "type" in schema and not _type_ok(value, schema["type"]):
        return [f"{path}: expected {schema['type']}"]
    if "const" in schema and (value != schema["const"] or isinstance(value, bool)):
        problems.append(f"{path}: must be {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        problems.append(f"{path}: must be one of {', '.join(map(str, schema['enum']))}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            problems.append(f"{path}: must not be empty")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            problems.append(f"{path}: does not match {schema['pattern']}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            problems.append(f"{path}: needs at least {schema['minItems']} item(s)")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            problems.append(f"{path}: allows at most {schema['maxItems']} item(s)")
        if "items" in schema:
            for index, item in enumerate(value):
                problems.extend(_check(item, schema["items"], f"{path}[{index}]"))
    if isinstance(value, dict):
        for name in schema.get("required", []):
            if name not in value:
                problems.append(f"{path}: `{name}` is missing")
        properties = schema.get("properties", {})
        for name, item in value.items():
            if name in properties:
                problems.extend(_check(item, properties[name], f"{path}.{name}"))
            elif schema.get("additionalProperties") is False:
                problems.append(f"{path}: `{name}` is not a known field")
    for part in schema.get("allOf", []):
        problems.extend(_check(value, part, path))
    if "if" in schema:
        branch = "then" if not _check(value, schema["if"], path) else "else"
        if branch in schema:
            problems.extend(_check(value, schema[branch], path))
    return problems


def problems_of(record: object) -> list[str]:
    """Why `record` is no valid next-step instruction, or an empty list."""
    problems = _check(record, load_schema(), "$")
    written = record.get("written_at") if isinstance(record, dict) else None
    if isinstance(written, str) and not problems:
        try:
            dt.datetime.strptime(written, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            problems.append("$.written_at: is not a real UTC instant")
    return problems


def validate(record: object) -> None:
    """Raise `InvalidNextStep` naming every violation, or return."""
    problems = problems_of(record)
    if problems:
        raise InvalidNextStep("; ".join(problems))


def build(change: str, verb: str, producer: str, now: dt.datetime, row_ids: list[str] | None = None) -> dict:
    """The version-1 record for `verb`, written at the UTC instant `now` (a timezone-aware datetime)."""
    if now.tzinfo is None or now.utcoffset() != dt.timedelta(0):
        raise InvalidNextStep("written_at must be a UTC instant")
    return {
        "schema_version": SCHEMA_VERSION,
        "change": change,
        "verb": verb,
        "row_ids": list(row_ids or []),
        "producer": producer,
        "written_at": now.astimezone(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def publish(directory: Path, record: dict) -> Path:
    """Validate `record`, write it to a temporary file beside the destination and replace `next.json`.

    The destination is replaced whole or not at all: an invalid record is never written, and a write or
    replacement that fails leaves the destination as it was and the temporary file removed.
    """
    validate(record)
    destination = directory / FILE_NAME
    directory.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{FILE_NAME}.", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(json.dumps(record, indent=2, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        Path(temporary).replace(destination)
    except BaseException:
        with contextlib.suppress(OSError):
            Path(temporary).unlink()
        raise
    return destination


def invalidate(directory: Path) -> None:
    """Delete the directory's `next.json`; an absent file is already invalid. A failed deletion raises."""
    try:
        (directory / FILE_NAME).unlink()
    except FileNotFoundError:
        return
