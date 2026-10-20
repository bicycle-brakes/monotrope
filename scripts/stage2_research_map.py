"""Exact finder-map union and neighbour derivation from supplied frozen sources.

This module performs no file, tracker, network or model operation. Trusted
finder-seat identifiers come from the caller, not from a model report.
"""

from __future__ import annotations

import hashlib
import json
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


def _entries(report, *, merged=False):
    if isinstance(report, str):
        try:
            report = json.loads(report, object_pairs_hook=_json_object, parse_constant=_bad_json_constant)
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


def validate_locator_report(report):
    """A finder answer that is exactly the four locator lists; raises ResearchMapError otherwise."""
    _entries(report)


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
