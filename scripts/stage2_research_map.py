"""Exact finder-map union and neighbour derivation from supplied frozen sources.

This module performs no file, tracker, network or model operation. Trusted
finder-seat identifiers come from the caller, not from a model report.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import date
from pathlib import PurePosixPath

from stage2_research_refs import resolve_research_reference

CATEGORIES = ("code", "rules", "tests", "neighbours")


class ResearchMapError(ValueError):
    """Preparation failure (1) or invalid given-neighbour declaration (2)."""

    def __init__(self, message, exit_code=1):
        super().__init__(message)
        self.exit_code = exit_code


def _parts(path):
    if not isinstance(path, str) or not path or "\\" in path:
        return None
    parsed = PurePosixPath(path)
    if parsed.is_absolute() or ".." in parsed.parts or str(parsed) != path:
        return None
    return parsed.parts


def _spec_folder(path):
    parts = _parts(path)
    if not parts or len(parts) < 4 or parts[0] != "plans":
        return None
    if parts[1] == "specs":
        return PurePosixPath(*parts[:3])
    if parts[1] != "changes":
        return None
    if parts[2] != "archive":
        return PurePosixPath(*parts[:3])
    if len(parts) < 5 or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-.+", parts[3]):
        return None
    try:
        date.fromisoformat(parts[3][:10])
    except ValueError:
        return None
    return PurePosixPath(*parts[:4])


def neighbour_spec_form(path):
    """The exact active, archived or living specification form; no I/O."""
    folder = _spec_folder(path)
    return folder is not None and str(folder / "spec.md") == path


def validate_given_neighbours(header, frozen_sources, own_spec):
    """Missing and explicit empty headers have different meanings before dispatch."""
    message = "add neighbours: [] or a unique list of existing frozen neighbour specs"
    if not neighbour_spec_form(own_spec):
        raise ResearchMapError("invalid own-spec context; " + message, 2)
    values = header.get("neighbours") if isinstance(header, dict) else None
    if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
        raise ResearchMapError(message, 2)
    if len(set(values)) != len(values):
        raise ResearchMapError(message + "; duplicate neighbour", 2)
    for path in values:
        if not neighbour_spec_form(path) or path == own_spec or path not in frozen_sources:
            raise ResearchMapError(message + f"; invalid neighbour: {path}", 2)
    return list(values)


def _json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ResearchMapError("duplicate finder/merge JSON key")
        result[key] = value
    return result


def _bad_json_constant(_value):
    raise ResearchMapError("non-finite finder/merge JSON value")


def _finite_json_float(value):
    number = float(value)
    if not math.isfinite(number):
        _bad_json_constant(value)
    return number


def _entries(report, *, merged=False):
    if isinstance(report, str):
        try:
            report = json.loads(
                report,
                object_pairs_hook=_json_object,
                parse_constant=_bad_json_constant,
                parse_float=_finite_json_float,
            )
        except (ValueError, RecursionError) as error:
            raise ResearchMapError("invalid finder/merge JSON") from error
    if not isinstance(report, dict) or set(report) != set(CATEGORIES):
        raise ResearchMapError("finder/merge must return exactly the four locator categories")
    result = []
    for category in CATEGORIES:
        values = report[category]
        if not isinstance(values, list) or not values:
            raise ResearchMapError("locator category needs entries or an explicit not_read marker")
        for entry in values:
            if isinstance(entry, dict) and set(entry) == {"not_read"}:
                if not merged and (not isinstance(entry["not_read"], str) or not entry["not_read"].strip()):
                    raise ResearchMapError("finder unread marker needs a text reason")
                normalized = {"origins" if merged else "reason": entry["not_read"]}
                result.append(((category, None, None), normalized))
                continue
            expected_fields = {"path", "reference", "origins" if merged else "reason"}
            if (
                not isinstance(entry, dict)
                or set(entry) != expected_fields
                or any(not isinstance(entry.get(key), str) or not entry[key] for key in ("path", "reference"))
            ):
                raise ResearchMapError("locator needs a path and exact symbol/section")
            if not merged and (not isinstance(entry["reason"], str) or not entry["reason"].strip()):
                raise ResearchMapError("finder locator needs a text reason")
            result.append(((category, entry["path"], entry["reference"]), entry))
    return result


def validate_locator_report(report, schema):
    """A finder answer that matches the shared locator schema; raises ResearchMapError otherwise (Q-3).

    Every rule comes from the interpreted schema the finder calls receive, never from a
    second copy of it: an outer-shape fault raises, an entry fault is reported as such.
    """
    _retained, rows = filter_locator_report(report, schema)
    if rows:
        row = rows[0]
        raise ResearchMapError(
            f"invalid entry at index {row['index']} of '{row['category']}': {'; '.join(row['errors'])}"
        )


FILTERED_MARKER = "every entry of this category was dropped by locator validation (finder-partial-report)"

# The keywords the small interpreter below supports (decisions.md S-13, S-18): anything
# else in the schema file is refused, so an edit cannot be silently ignored.
_SCHEMA_ANNOTATIONS = frozenset({"description", "title", "$schema"})
_SCHEMA_OBJECT_KEYWORDS = frozenset({"type", "properties", "required", "additionalProperties"}) | _SCHEMA_ANNOTATIONS
_SCHEMA_ARRAY_KEYWORDS = frozenset({"type", "items", "minItems"}) | _SCHEMA_ANNOTATIONS
_SCHEMA_ANYOF_KEYWORDS = frozenset({"anyOf"}) | _SCHEMA_ANNOTATIONS
_SCHEMA_STRING_KEYWORDS = frozenset({"type", "pattern"}) | _SCHEMA_ANNOTATIONS


def _check_schema_keywords(schema, allowed, where):
    unknown = sorted(set(schema) - allowed)
    if unknown:
        raise ResearchMapError(f"{where} uses the unsupported schema keyword: {unknown[0]}")


def interpret_locator_schema(value):
    """Compile the one locator schema for finder validation and filtering (Q-3, S-13).

    ``value`` is the schema text or its parsed object; the compiled form carries the
    categories, their non-empty list rule and every entry form. A missing, malformed
    or unsupported schema raises ``ResearchMapError`` (S-17), never a silent default.
    """
    if isinstance(value, str | bytes):
        try:
            value = json.loads(value)
        except ValueError as error:
            raise ResearchMapError(f"the locator schema is not valid JSON: {error}") from error
    if not isinstance(value, dict):
        raise ResearchMapError("the locator schema must be a JSON object")
    _check_schema_keywords(value, _SCHEMA_OBJECT_KEYWORDS, "the locator schema")
    if value.get("type") != "object":
        raise ResearchMapError("the locator schema must hold an object")
    if value.get("additionalProperties") is not False:
        raise ResearchMapError("the locator schema must close its properties")
    properties, required = value.get("properties"), value.get("required")
    if not isinstance(properties, dict) or not properties:
        raise ResearchMapError("the locator schema needs its category properties")
    if (
        not isinstance(required, list)
        or not all(isinstance(name, str) for name in required)
        or set(required) != set(properties)
    ):
        raise ResearchMapError("the locator schema must require every category")
    if set(properties) != set(CATEGORIES):
        raise ResearchMapError("the locator schema categories must match the merge categories")
    categories = {name: _category_schema(name, item) for name, item in properties.items()}
    return {"categories": categories}


def _category_schema(name, schema):
    where = f"the locator schema category '{name}'"
    if not isinstance(schema, dict):
        raise ResearchMapError(f"{where} must be a JSON object")
    _check_schema_keywords(schema, _SCHEMA_ARRAY_KEYWORDS, where)
    if schema.get("type") != "array":
        raise ResearchMapError(f"{where} must hold an array")
    minimum = schema.get("minItems")
    if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 1:
        raise ResearchMapError(f"{where} must require at least one entry")
    items = schema.get("items")
    if not isinstance(items, dict):
        raise ResearchMapError(f"{where} must describe its items")
    _check_schema_keywords(items, _SCHEMA_ANYOF_KEYWORDS, where)
    forms = items.get("anyOf")
    if not isinstance(forms, list) or not forms:
        raise ResearchMapError(f"{where} needs at least one entry form")
    branches = [_entry_form(f"{where} entry form {number}", form) for number, form in enumerate(forms, 1)]
    return {"min_items": minimum, "branches": branches}


def _entry_form(where, schema):
    if not isinstance(schema, dict):
        raise ResearchMapError(f"{where} must be a JSON object")
    _check_schema_keywords(schema, _SCHEMA_OBJECT_KEYWORDS, where)
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        raise ResearchMapError(f"{where} must be a closed object")
    properties, required = schema.get("properties"), schema.get("required")
    if not isinstance(properties, dict) or not properties:
        raise ResearchMapError(f"{where} needs its fields")
    if (
        not isinstance(required, list)
        or not all(isinstance(name, str) for name in required)
        or not set(required) <= set(properties)
    ):
        raise ResearchMapError(f"{where} must require known fields")
    fields = {name: _field_schema(f"{where} field '{name}'", item) for name, item in properties.items()}
    return {"required": set(required), "fields": fields}


def _field_schema(where, schema):
    if not isinstance(schema, dict):
        raise ResearchMapError(f"{where} must be a JSON object")
    _check_schema_keywords(schema, _SCHEMA_STRING_KEYWORDS, where)
    if schema.get("type") != "string":
        raise ResearchMapError(f"{where} must hold a string")
    pattern = schema.get("pattern")
    if pattern is None:
        return None
    if not isinstance(pattern, str):
        raise ResearchMapError(f"{where} needs its pattern as text")
    try:
        return re.compile(pattern)
    except re.error as error:
        raise ResearchMapError(f"{where} has an unusable pattern: {error}") from error


def _entry_faults(entry, branches):
    """The faults of one entry against the schema's entry forms; empty when one form matches.

    Keys that identify one form select that form. Otherwise use the closest form
    (fewest faults, schema order on a tie).
    """
    if not isinstance(entry, dict):
        return ["the entry must be a JSON object"]
    closest = None
    aimed = [branch for branch in branches if set(entry) & set(branch["fields"])]
    preferred = branches[0] if not entry else aimed[0] if len(aimed) == 1 else None
    preferred_faults = None
    for branch in branches:
        foreign = sorted(set(entry) - set(branch["fields"]))
        faults = [f"the field '{name}' is not part of the entry form" for name in foreign]
        faults += [f"the required field '{name}' is missing" for name in sorted(branch["required"] - set(entry))]
        for name, value in sorted(entry.items()):
            if name not in branch["fields"]:  # already faulted as foreign to this form
                continue
            pattern = branch["fields"][name]
            if not isinstance(value, str):
                faults.append(f"the field '{name}' must be a string")
            elif pattern is not None and pattern.search(value) is None:
                faults.append(f"the field '{name}' does not match the schema pattern")
        if not faults:
            return []
        if branch is preferred:
            preferred_faults = faults
        if closest is None or len(faults) < len(closest):
            closest = faults
    return preferred_faults or closest or ["the entry matches no entry form of the schema"]


def filter_locator_report(report, schema):
    """Split a finder answer into the entries that survive locator validation and the dropped rows (Q-2).

    An outer-shape fault raises ``ResearchMapError`` and stops the run as today (S-2,
    S-6); a fault inside one entry drops that entry and records its exact errors. A
    category whose entries are all dropped keeps the fixed unread marker, so the merge
    reproduces the retained report exactly (S-7). Path and reference form stay with the
    existing merge resolution (S-19).
    """
    shape = schema.get("categories") if isinstance(schema, dict) else None
    if not shape:
        raise ResearchMapError("finder filtering needs the interpreted locator schema")
    if isinstance(report, str):
        try:
            report = json.loads(
                report,
                object_pairs_hook=_json_object,
                parse_constant=_bad_json_constant,
                parse_float=_finite_json_float,
            )
        except (ValueError, RecursionError) as error:
            raise ResearchMapError("invalid finder JSON") from error
    if not isinstance(report, dict) or set(report) != set(shape):
        raise ResearchMapError("the finder answer must hold exactly the schema's locator categories")
    retained, rows = {}, []
    kept_count = 0
    for category, compiled in shape.items():
        values = report[category]
        if not isinstance(values, list) or len(values) < compiled["min_items"]:
            raise ResearchMapError("locator category needs entries or an explicit not_read marker")
        kept = []
        for index, entry in enumerate(values):
            faults = _entry_faults(entry, compiled["branches"])
            if faults:
                rows.append({"category": category, "index": index, "entry": entry, "errors": faults})
            else:
                kept.append(entry)
        kept_count += len(kept)
        retained[category] = kept or [{"not_read": FILTERED_MARKER}]
    if not kept_count:
        raise ResearchMapError("finder report has no valid entries after locator validation")
    return retained, rows


def _origin(entry):
    if (
        not isinstance(entry, dict)
        or set(entry) != {"finder", "reason"}
        or any(not isinstance(entry[key], str) or not entry[key].strip() for key in ("finder", "reason"))
    ):
        raise ResearchMapError("invalid finder origin")
    return entry["finder"], entry["reason"]


def merge_research_map(finder_reports, merged_report, frozen_sources, given, own_spec):
    """Validate Opus's exact union, then independently resolve and insert given specs.

    Returned audit entries contain extents and hashes, never whole frozen-file
    snapshots. Unresolved locators remain visible but grant no mapped scope.
    """
    given = validate_given_neighbours({"neighbours": given}, frozen_sources, own_spec)
    if (
        not isinstance(finder_reports, dict)
        or len(finder_reports) != 3
        or any(not isinstance(key, str) or not key for key in finder_reports)
    ):
        raise ResearchMapError("exactly three trusted finder seats are required")
    union = {}
    for finder, report in finder_reports.items():
        for key, entry in _entries(report):
            reason = entry.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                raise ResearchMapError("finder locator needs a reason")
            union.setdefault(key, set()).add((finder, reason))
    received = {}
    for key, entry in _entries(merged_report, merged=True):
        if key in received:
            raise ResearchMapError("duplicate merged locator")
        origins = entry.get("origins")
        if not isinstance(origins, list):
            raise ResearchMapError("merged locator needs every finder origin")
        pairs = [_origin(item) for item in origins]
        if len(set(pairs)) != len(pairs):
            raise ResearchMapError("duplicate merged finder origin")
        received[key] = set(pairs)
    if received != union:
        raise ResearchMapError("merged map adds/drops a locator or changes finder reasons")
    neighbours = {path: {"path": path, "status": "given", "map_keys": []} for path in given}
    entries = []
    scope = []
    gaps = []
    not_read = []
    own_folder = _spec_folder(own_spec)
    for key in sorted(union, key=lambda item: (CATEGORIES.index(item[0]), item[1] or "", item[2] or "")):
        category, path, reference = key
        if path is None:
            not_read.append(
                {
                    "category": category,
                    "origins": [{"finder": finder, "reason": reason} for finder, reason in sorted(union[key])],
                }
            )
            continue
        resolution = resolve_research_reference(frozen_sources, path, reference)
        entry = {
            "key": list(key),
            "category": category,
            "path": path,
            "reference": reference,
            "origins": [{"finder": finder, "reason": reason} for finder, reason in sorted(union[key])],
            "status": "resolved" if resolution["supported"] else "unresolved",
        }
        if not resolution["supported"]:
            entry["reason"] = resolution["reason"]
            entries.append(entry)
            continue
        entry["extent"] = {key: resolution[key] for key in ("start_line", "end_line")}
        entry["excerpt_sha256"] = hashlib.sha256(resolution["excerpt"].encode()).hexdigest()
        scope.append(list(key))
        if category == "neighbours":
            folder = _spec_folder(path)
            spec = str(folder / "spec.md") if folder else None
            if folder is not None and folder == own_folder:
                entry["neighbour_status"] = "self"
            elif spec is not None and spec in frozen_sources:
                neighbour = neighbours.setdefault(spec, {"path": spec, "status": "suggested", "map_keys": []})
                neighbour["map_keys"].append(list(key))
                entry["neighbour_status"] = neighbour["status"]
                entry["neighbour_spec"] = spec
            else:
                entry["neighbour_status"] = "no-spec"
                gaps.append({"key": list(key), "reason": "no frozen specification for the resolved neighbour artifact"})
        entries.append(entry)
    return {
        "entries": entries,
        "scope": scope,
        "neighbours": [neighbours[path] for path in sorted(neighbours)],
        "gaps": gaps,
        "not_read": not_read,
    }
