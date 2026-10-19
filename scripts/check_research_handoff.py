#!/usr/bin/env python3
"""check_research_handoff.py - what a research run hands to the interview and the spec stays measured.

The research runner (`stage2_research_run.py`) appends fenced `research-swarm/v2` records to a
change's `research.md`. This gate reads them - no tracker, model or network - and holds the
handoff of every *complete* run to the maintainer's answers:

- obligations: it derives the inventory itself from the raw reports and the judge's structured
  disagreements (`research_handoff.derive_inventory`), never from the judge's inventory prose, and
  adds the cross-run neighbour items (a path confirmed in one complete run and rejected in
  another, a given path a later run omits). A persisted inventory that lost a derived item is a
  finding;
- answers: an item `<run>/H-<n>` (cross-run items `<run>/X-<n>`) is closed by a maintainer-answered
  Q-record in the change's `decisions.md` whose `research_items` links it, with an actual answer and
  its context. A neighbour item also needs its path in that record's `research_neighbours` keep
  or drop list; no agent waiver and no prose reading counts;
- neighbours: once `spec.md` exists its `neighbours:` header must equal the paths given or confirmed
  in any complete run, plus the keep and add paths of maintainer-answered records, minus their drop
  paths. A split path is not required until a structured keep;
- bases: every acceptance criterion's `*Basis:*` names supported claims of complete runs and/or
  answered Q-records of the change (`decisions.md#Q-<id>`).

Before `spec.md` exists, valid pending items are listed and the gate exits 0. Evidence that cannot
be read or is ambiguous (malformed records, duplicate global ids, links to nothing, one field
twice, a path in two directive lists or incompatible answered records) is not measured: exit 3,
which takes precedence over findings. A change without any v2 run is a reported legacy exemption.

Usage:
    python3 scripts/check_research_handoff.py                  # this repository, live and archive
    python3 scripts/check_research_handoff.py --root DIR       # another tree (tests)
    python3 scripts/check_research_handoff.py --change NAME    # one change
Exit: 0 = nothing found, 1 = findings, 3 = could not measure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import research_handoff  # noqa: E402 - the one derivation the runner shares

REPO_ROOT = Path(__file__).resolve().parent.parent

CHANGES_DIR = "plans/changes"
ARCHIVE = "archive"

KINDS = ("manifest", "map", "history", "report", "partial", "reconciliation", "inventory")
_OPEN = re.compile(r"^<!-- research-swarm/v2 run ([0-9a-f]+) -->$")
_CLOSE = "<!-- /research-swarm/v2 -->"
_FENCE_V2 = re.compile(r"^(`{3,})research-swarm/v2 (\S+)$")
_FENCE_ANY = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_RECORD = re.compile(r"^(Q-[^\s·]+)[ \t]*·[ \t]*(.*)$")
_FIELD = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$")
_QREF = re.compile(r"^decisions\.md#(Q-\S+)$")
_CLAIM = re.compile(r"^([0-9a-f]+)/([0-9]+)/([^/\s]+)/(C[1-7])$")
_ITEM = re.compile(r"^([0-9a-f]+)/([HX]-[1-9][0-9]*)$")
_ARCHIVED = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-(.+)$")


class CannotMeasure(Exception):  # noqa: N818 - a verdict, not an error class
    """The question cannot be answered here. Exit 3, nothing measured."""


# ---------------------------------------------------------------------------
# reading the v2 records
# ---------------------------------------------------------------------------


@dataclass
class ParsedRun:
    run_id: str
    label: str
    manifest: dict
    map: dict | None = None
    reports: list[dict] = field(default_factory=list)
    reconciliation: dict | None = None
    inventory: dict | None = None
    blocks: dict[str, list] = field(default_factory=dict)
    derived: dict | None = None

    @property
    def complete(self) -> bool:
        return str(self.manifest.get("status", "")).startswith("complete")

    @property
    def given(self) -> list[str]:
        return list(self.manifest.get("given_neighbours", ()))

    def supported(self) -> set[str]:
        scores = (self.reconciliation or {}).get("scores", ())
        return {claim for entry in scores for claim in entry["supported"]["claims"]}


def _no_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict:
    keys = [key for key, _ in pairs]
    repeated = sorted({key for key in keys if keys.count(key) > 1})
    if repeated:
        raise ValueError(f"the key {repeated[0]!r} stands twice in one object")
    return dict(pairs)


class _UniqueKeyLoader(yaml.SafeLoader):
    """A safe YAML loader that refuses a mapping naming one key twice (the last would win silently)."""


def _construct_unique_mapping(loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    seen: set[object] = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=True)
        if key in seen:
            raise yaml.YAMLError(f"the key {key!r} stands twice in one mapping")
        seen.add(key)
    return loader.construct_mapping(node, deep=deep)


_UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping)


def _yaml_load(text: str) -> object:
    return yaml.load(text, Loader=_UniqueKeyLoader)  # noqa: S506 - SafeLoader subclass


def _json(body: str, where: str) -> object:
    try:
        return json.loads(body, object_pairs_hook=_no_duplicate_pairs)
    except ValueError as error:
        raise CannotMeasure(f"{where}: a record is not valid JSON ({error})") from error


def _is_list_of(value: object, kind: type) -> bool:
    return isinstance(value, list) and all(isinstance(item, kind) for item in value)


def _check_report(report: object, run_id: str, where: str) -> dict:
    if not isinstance(report, dict):
        raise CannotMeasure(f"{where}: a report is not an object")
    topic, seat = report.get("topic"), report.get("seat")
    if type(topic) is not int or not isinstance(seat, str) or report.get("run_id") != run_id:
        raise CannotMeasure(f"{where}: a report lacks its run, topic or seat identity")
    prefix = f"{run_id}/{topic}/{seat}/"
    claims, questions = report.get("claims"), report.get("questions")
    if not _is_list_of(claims, dict) or not _is_list_of(questions, dict):
        raise CannotMeasure(f"{where}: report {topic}/{seat} has no claim and question lists")
    for claim in claims:
        if not isinstance(claim.get("id"), str) or not claim["id"].startswith(prefix):
            raise CannotMeasure(f"{where}: a claim id does not carry its run, topic and seat")
        if claim.get("evidence_status") not in ("valid", "unsupported"):
            raise CannotMeasure(f"{where}: claim {claim['id']} has no evidence status")
    for question in questions:
        ok = (
            isinstance(question.get("id"), str)
            and question["id"].startswith(prefix)
            and isinstance(question.get("question"), str)
            and question.get("classification") in ("[DECISION]", "[GAP]", "[DETAIL]")
            and _is_list_of(question.get("claims"), str)
        )
        if not ok:
            raise CannotMeasure(f"{where}: a question of report {topic}/{seat} is malformed")
    assessment = report.get("class_assessment")
    if assessment is not None and not (
        isinstance(assessment, dict)
        and isinstance(assessment.get("class"), str)
        and _is_list_of(assessment.get("claims"), str)
    ):
        raise CannotMeasure(f"{where}: a class assessment is malformed")
    relations = report.get("neighbour_relations", [])
    if not isinstance(relations, list) or any(
        not (
            isinstance(item, dict)
            and isinstance(item.get("path"), str)
            and item.get("relation") in ("related", "unrelated", "contradicts")
            and _is_list_of(item.get("claims"), str)
        )
        for item in relations
    ):
        raise CannotMeasure(f"{where}: neighbour relations are malformed")
    return report


def parse_text(text: str, label: str) -> list[ParsedRun]:
    """Every v2 run envelope of one research.md, validated; raises CannotMeasure on anything ambiguous."""
    runs: list[ParsedRun] = []
    lines = text.splitlines()
    envelope: str | None = None
    blocks: dict[str, list[tuple[str, str]]] = {}
    index = 0
    other: tuple[str, int] | None = None
    while index < len(lines):
        line = lines[index]
        index += 1
        if other is not None:
            closed = _FENCE_ANY.match(line)
            if (
                closed
                and closed.group(1)[0] == other[0]
                and len(closed.group(1)) >= other[1]
                and line.strip() == closed.group(1)
            ):
                other = None
            continue
        v2 = _FENCE_V2.match(line)
        if v2:
            if envelope is None:
                raise CannotMeasure(f"{label}: a research-swarm/v2 record stands outside a run envelope")
            ticks, kind = v2.group(1), v2.group(2)
            if kind not in KINDS:
                raise CannotMeasure(f"{label}: unknown record kind {kind!r}")
            body = []
            while index < len(lines) and lines[index] != ticks:
                body.append(lines[index])
                index += 1
            if index >= len(lines):
                raise CannotMeasure(f"{label}: a {kind} record is never closed")
            index += 1
            blocks.setdefault(kind, []).append(("\n".join(body), f"{label} run {envelope} {kind}"))
            continue
        fence = _FENCE_ANY.match(line)
        if fence:
            other = (fence.group(1)[0], len(fence.group(1)))
            continue
        opened = _OPEN.match(line)
        if opened:
            if envelope is not None:
                raise CannotMeasure(f"{label}: run {opened.group(1)} opens inside run {envelope}")
            envelope, blocks = opened.group(1), {}
        elif line == _CLOSE:
            if envelope is None:
                raise CannotMeasure(f"{label}: a run envelope closes that never opened")
            runs.append(_build(envelope, blocks, label))
            envelope = None
    if envelope is not None:
        raise CannotMeasure(f"{label}: run {envelope} is never closed")
    return runs


def _build(run_id: str, blocks: dict[str, list[tuple[str, str]]], label: str) -> ParsedRun:
    where = f"{label} run {run_id}"
    for kind in ("manifest", "map", "reconciliation", "inventory"):
        if len(blocks.get(kind, ())) > 1:
            raise CannotMeasure(f"{where}: more than one {kind} record")
    decoded = {kind: [_json(body, source) for body, source in items] for kind, items in blocks.items()}
    if "manifest" not in decoded:
        raise CannotMeasure(f"{where}: no manifest record")
    manifest = decoded["manifest"][0]
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema") != "research-swarm/v2"
        or manifest.get("run_id") != run_id
        or not isinstance(manifest.get("status"), str)
        or not isinstance(manifest.get("class"), str)
        or not _is_list_of(manifest.get("given_neighbours", []), str)
    ):
        raise CannotMeasure(f"{where}: the manifest is malformed or names another run")
    parsed = ParsedRun(run_id, where, manifest, blocks=decoded)
    for kind, attribute in (("map", "map"), ("reconciliation", "reconciliation"), ("inventory", "inventory")):
        if kind in decoded:
            if not isinstance(decoded[kind][0], dict):
                raise CannotMeasure(f"{where}: the {kind} record is not an object")
            setattr(parsed, attribute, decoded[kind][0])
    for item in decoded.get("report", ()):
        parsed.reports.append(_check_report(item, run_id, where))
    seen = set()
    for report in parsed.reports:
        key = (report["topic"], report["seat"])
        if key in seen:
            raise CannotMeasure(f"{where}: two reports for topic {key[0]} and seat {key[1]}")
        seen.add(key)
    if parsed.complete:
        _complete_shape(parsed, where)
    return parsed


def _complete_shape(parsed: ParsedRun, where: str) -> None:
    packet = (parsed.map or {}).get("neighbours")
    if not parsed.reports or not (
        isinstance(packet, list)
        and all(
            isinstance(item, dict)
            and isinstance(item.get("path"), str)
            and item.get("status") in ("given", "suggested")
            for item in packet
        )
    ):
        raise CannotMeasure(f"{where}: a complete run lacks its reports or neighbour packet")
    reconciliation = parsed.reconciliation or {}
    judge, scores = reconciliation.get("reconciliation"), reconciliation.get("scores")
    if not (
        isinstance(judge, dict)
        and isinstance(judge.get("disagreements"), list)
        and all(
            isinstance(d, dict) and _is_list_of(d.get("claims"), str) and isinstance(d.get("summary"), str)
            for d in judge["disagreements"]
        )
        and isinstance(scores, list)
        and all(
            isinstance(s, dict)
            and isinstance(s.get("supported"), dict)
            and _is_list_of(s["supported"].get("claims"), str)
            for s in scores
        )
    ):
        raise CannotMeasure(f"{where}: a complete run lacks a well-formed reconciliation")
    # The judge's supported list must agree with each claim's own evidence status (F-23): a claim its report
    # marks unsupported, or one no report holds, cannot be supported - the records contradict each other.
    valid = {c["id"] for report in parsed.reports for c in report["claims"] if c["evidence_status"] == "valid"}
    contradicted = sorted(parsed.supported() - valid)
    if contradicted:
        raise CannotMeasure(
            f"{where}: the reconciliation lists {contradicted[0]} as supported, "
            "which its report does not hold with valid evidence"
        )
    parsed.derived = research_handoff.derive_inventory(
        run_id=parsed.run_id,
        declared_class=parsed.manifest["class"],
        packet=packet,
        reports=parsed.reports,
        disagreements=judge["disagreements"],
    )


# ---------------------------------------------------------------------------
# the maintainer's records
# ---------------------------------------------------------------------------


@dataclass
class QRecord:
    ident: str
    answered: bool
    context: bool
    items: list[str] = field(default_factory=list)
    claims: list[str] = field(default_factory=list)
    keep: list[str] = field(default_factory=list)
    drop: list[str] = field(default_factory=list)
    add: list[str] = field(default_factory=list)

    def directive_paths(self) -> set[str]:
        return {*self.keep, *self.drop, *self.add}


def _fenced_flags(lines: list[str]) -> list[bool]:
    inside, marker = [], None
    for line in lines:
        fence = _FENCE_ANY.match(line)
        if marker is None:
            inside.append(False)
            if fence:
                marker = (fence.group(1)[0], len(fence.group(1)))
                inside[-1] = True
        else:
            inside.append(True)
            if (
                fence
                and fence.group(1)[0] == marker[0]
                and len(fence.group(1)) >= marker[1]
                and line.strip() == fence.group(1)
            ):
                marker = None
    return inside


def _snippet(body: list[str], index: int) -> str:
    lines = [body[index]]
    for line in body[index + 1 :]:
        if line.startswith((" ", "\t", "- ")) or not line.strip():
            lines.append(line)
        else:
            break
    return "\n".join(lines)


def _string_list(value: object, where: str) -> list[str]:
    if value is None:
        return []
    if not _is_list_of(value, str):
        raise CannotMeasure(f"{where} is not a list of text values")
    if len(set(value)) != len(value):
        raise CannotMeasure(f"{where} repeats a value")
    return list(value)


def parse_decisions(text: str, label: str) -> dict[str, QRecord]:
    """The first record of each Q id, with its structured research links; later repeats are ignored."""
    lines = text.splitlines()
    fenced = _fenced_flags(lines)
    heads = [
        (number, _RECORD.match(line[3:].rstrip()))
        for number, line in enumerate(lines)
        if not fenced[number] and line.startswith("## ")
    ]
    ends = [number for number, line in enumerate(lines) if not fenced[number] and line.startswith("## ")]
    records: dict[str, QRecord] = {}
    for start, matched in heads:
        if matched is None:
            continue
        ident = matched.group(1)
        stop = next((n for n in ends if n > start), len(lines))
        body = lines[start + 1 : stop]
        if ident in records:
            if any(line.startswith("research_") for line in body):
                raise CannotMeasure(f"{label} {ident}: the record stands twice and carries research links")
            continue
        found: dict[str, int] = {}
        flags = _fenced_flags(body)
        for number, line in enumerate(body):
            field_match = _FIELD.match(line)
            if field_match and not flags[number]:
                name = field_match.group(1)
                if name in found and name.startswith(("research_", "answer", "status", "answered_by", "context")):
                    raise CannotMeasure(f"{label} {ident}: the field {name} stands twice")
                found.setdefault(name, number)

        def value(name: str, body: list[str] = body, found: dict[str, int] = found) -> str:
            if name not in found:
                return ""
            first = _FIELD.match(body[found[name]])
            assert first is not None
            rest = first.group(2).strip().strip("\"'").strip()
            if rest and rest not in ("|", ">", "|-", ">-"):
                return rest
            tail = []
            for line in body[found[name] + 1 :]:
                if line.startswith((" ", "\t")):
                    tail.append(line.strip())
                else:
                    break
            return " ".join(tail).strip()

        answered = value("status") == "answered" and value("answered_by") == "maintainer" and bool(value("answer"))
        record = QRecord(ident, answered, bool(value("context")))
        for name in ("research_items", "research_claims", "research_neighbours"):
            if name not in found:
                continue
            try:
                loaded = _yaml_load(_snippet(body, found[name]))
            except yaml.YAMLError as error:
                raise CannotMeasure(f"{label} {ident}: {name} is not readable ({error})") from error
            content = loaded.get(name) if isinstance(loaded, dict) else None
            where = f"{label} {ident}: {name}"
            if name == "research_items":
                record.items = _string_list(content, where)
            elif name == "research_claims":
                record.claims = _string_list(content, where)
            else:
                if not isinstance(content, dict) or not set(content) <= {"keep", "drop", "add"}:
                    raise CannotMeasure(f"{where} must be a mapping of keep, drop and add lists")
                record.keep = _string_list(content.get("keep"), where + ".keep")
                record.drop = _string_list(content.get("drop"), where + ".drop")
                record.add = _string_list(content.get("add"), where + ".add")
        records[ident] = record
    return records


def neighbour_form(path: str) -> bool:
    """The three permitted spec forms: an active change, an archived change or a living spec. No I/O."""
    if not path or "\\" in path:
        return False
    parsed = PurePosixPath(path)
    parts = parsed.parts
    if parsed.is_absolute() or ".." in parts or str(parsed) != path or len(parts) < 4 or parts[0] != "plans":
        return False
    if parts[-1] != "spec.md":
        return False
    if parts[1] == "specs":
        return len(parts) == 4
    if parts[1] != "changes":
        return False
    if parts[2] != ARCHIVE:
        return len(parts) == 4
    return len(parts) == 5 and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-.+", parts[3]) is not None


# ---------------------------------------------------------------------------
# one change
# ---------------------------------------------------------------------------


@dataclass
class Item:
    ident: str
    reason: str
    summary: str
    path: str | None = None
    kind: str | None = None
    claims: list[str] = field(default_factory=list)

    @property
    def needs_path(self) -> bool:
        return self.path is not None


def _items_of(runs: list[ParsedRun]) -> dict[str, Item]:
    items: dict[str, Item] = {}
    for run in runs:
        assert run.derived is not None
        for entry in run.derived["items"]:
            items[f"{run.run_id}/{entry['id']}"] = Item(
                f"{run.run_id}/{entry['id']}",
                entry["reason"],
                entry["summary"],
                entry.get("path"),
                entry.get("kind"),
                list(entry.get("claims", ())),
            )
    statuses = [{n["path"]: n["status"] for n in (run.derived or {})["neighbours"]} for run in runs]
    claims = [
        {
            n["path"]: sorted({c for row in n["relations"] for c in row["claims"]})
            for n in (run.derived or {})["neighbours"]
        }
        for run in runs
    ]
    for later, run in enumerate(runs):
        pending: list[Item] = []
        for path in sorted({p for status in statuses[:later] for p in status} | set(statuses[later])):
            now = statuses[later].get(path)
            for earlier in range(later):
                before = statuses[earlier].get(path)
                if {before, now} == {"confirmed", "rejected"}:
                    pending.append(
                        Item(
                            "",
                            "neighbour",
                            f"run {runs[earlier].run_id} {before} and run {run.run_id} {now} {path}",
                            path,
                            "conflict",
                            claims[earlier].get(path, []) + claims[later].get(path, []),
                        )
                    )
        for path in sorted({p for previous in runs[:later] for p in previous.given} - set(run.given)):
            source = next(previous for previous in runs[:later] if path in previous.given)
            pending.append(
                Item(
                    "",
                    "neighbour",
                    f"run {run.run_id} omits {path}, given by run {source.run_id} (source manifest)",
                    path,
                    "given-omitted",
                )
            )
        for number, item in enumerate(pending, 1):
            item.ident = f"{run.run_id}/X-{number}"
            items[item.ident] = item
    return items


def _header(spec_text: str) -> dict:
    matched = re.match(r"\A﻿?---\r?\n(.*?)^---[ \t]*\r?$", spec_text, re.S | re.M)
    if not matched:
        return {}
    try:
        loaded = _yaml_load(matched.group(1))
    except yaml.YAMLError as error:
        raise CannotMeasure(f"spec.md: the header is not readable ({error})") from error
    return loaded if isinstance(loaded, dict) else {}


def _basis_lines(spec_text: str) -> dict[int, list[str]]:
    """Per criterion number the text of its `*Basis:*` lines; a criterion without one maps to []."""
    lines = spec_text.splitlines()
    fenced = _fenced_flags(lines)
    result: dict[int, list[str]] = {}
    inside = False
    current: int | None = None
    collecting = False
    for number, line in enumerate(lines):
        if fenced[number]:
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            if len(heading.group(1)) <= 2:  # a level-three heading is a subsection, not the end (F-25)
                inside = heading.group(2).strip().lower().startswith("acceptance criteria")
            current, collecting = None, False
            continue
        if not inside:
            continue
        numbered = re.match(r"^([1-9][0-9]*)\. ", line)
        if numbered:
            current = int(numbered.group(1))
            result[current] = []
            collecting = False
            continue
        basis = re.match(r"^\s+\*Basis:\*(.*)$", line)
        if current is not None and basis:
            result[current].append(basis.group(1))
            collecting = True
        elif current is not None and collecting and line.startswith(("  ", "\t")) and not line.strip().startswith("*"):
            result[current][-1] += " " + line.strip()
        else:
            collecting = False
    return result


@dataclass
class Outcome:
    findings: list[str] = field(default_factory=list)
    pending: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def check_change(folder: Path, label: str) -> Outcome:
    out = Outcome()
    research = folder / "research.md"
    if not research.is_file():
        out.notes.append(f"{label}: exempt - no research.md, so no v2 evidence")
        return out
    try:
        runs = parse_text(research.read_text(encoding="utf-8"), label)
    except (OSError, UnicodeDecodeError) as error:
        raise CannotMeasure(f"{label}: research.md cannot be read ({error})") from error
    if not runs:
        out.notes.append(f"{label}: exempt - legacy, no research-swarm/v2 evidence")
        return out
    ids = [run.run_id for run in runs]
    if len(set(ids)) != len(ids):
        raise CannotMeasure(f"{label}: a run id appears twice")
    seen_claims: set[str] = set()
    seen_questions: set[str] = set()
    for run in runs:
        for report in run.reports:
            for identifier in (c["id"] for c in report["claims"]):
                if identifier in seen_claims:
                    raise CannotMeasure(f"{label}: the global claim id {identifier} appears twice")
                seen_claims.add(identifier)
            for identifier in (q["id"] for q in report["questions"]):
                if identifier in seen_questions:
                    raise CannotMeasure(f"{label}: the global question id {identifier} appears twice")
                seen_questions.add(identifier)
    complete = [run for run in runs if run.complete]
    out.notes.append(f"{label}: {len(runs)} v2 run(s), {len(complete)} complete")

    decisions = folder / "decisions.md"
    try:
        records = parse_decisions(decisions.read_text(encoding="utf-8"), label) if decisions.is_file() else {}
    except (OSError, UnicodeDecodeError) as error:
        raise CannotMeasure(f"{label}: decisions.md cannot be read ({error})") from error
    items = _items_of(complete)
    all_claims = {c["id"] for run in runs for report in run.reports for c in report["claims"]}
    for record in records.values():
        for link in record.items:
            if link not in items:
                raise CannotMeasure(f"{label} {record.ident}: research_items names {link}, which no complete run holds")
        for link in record.claims:
            if link not in all_claims:
                raise CannotMeasure(f"{label} {record.ident}: research_claims names {link}, which no run holds")
    # directives of maintainer-answered records
    directive_records = [r for r in records.values() if r.answered and r.context]
    for record in directive_records:
        lists = {"keep": record.keep, "drop": record.drop, "add": record.add}
        for first in lists:
            for second in lists:
                if first < second and set(lists[first]) & set(lists[second]):
                    raise CannotMeasure(f"{label} {record.ident}: a path stands in both {first} and {second}")
    for index, record in enumerate(directive_records):
        for other in directive_records[index + 1 :]:
            clash = {*record.keep, *record.add} & set(other.drop) | {*other.keep, *other.add} & set(record.drop)
            if clash:
                raise CannotMeasure(
                    f"{label}: {record.ident} and {other.ident} give incompatible directives for {sorted(clash)[0]}"
                )
    for record in directive_records:
        for path in sorted(record.directive_paths()):
            if not neighbour_form(path):
                out.findings.append(f"{label} {record.ident}: {path!r} has none of the three permitted spec forms")

    spec = folder / "spec.md"
    spec_exists = spec.is_file()
    # coverage: the persisted inventory against the independent derivation
    for run in complete:
        assert run.derived is not None
        if run.inventory is None:
            out.findings.append(f"{label}: run {run.run_id} has no inventory record")
        elif {"neighbours": run.inventory.get("neighbours"), "items": run.inventory.get("items")} != {
            "neighbours": run.derived["neighbours"],
            "items": run.derived["items"],
        }:
            lost = [
                f"{run.run_id}/{entry['id']}"
                for entry in run.derived["items"]
                if entry not in (run.inventory.get("items") or [])
            ]
            out.findings.append(
                f"{label}: the persisted inventory of run {run.run_id} differs from the independent derivation"
                + (f" (missing or changed: {', '.join(lost)})" if lost else "")
            )
    # obligations
    open_items = []
    for ident, item in items.items():
        closing = [
            r
            for r in directive_records
            if ident in r.items and (not item.needs_path or item.path in (*r.keep, *r.drop))
        ]
        if not closing:
            open_items.append(item)
    for item in open_items:
        text = f"{item.ident} ({item.reason}{' ' + item.kind if item.kind else ''}): {item.summary}"
        if item.claims:
            text += f" [claims: {', '.join(item.claims)}]"
        if spec_exists:
            hint = " - link it in a maintainer-answered Q-record's research_items" + (
                " and name its path in research_neighbours keep or drop" if item.needs_path else ""
            )
            out.findings.append(f"{label}: open research item {text}{hint}")
        else:
            out.pending.append(f"{label}: pending: {text}")
    if not spec_exists:
        return out
    if not complete:
        out.findings.append(f"{label}: the spec exists but no complete v2 run exists")
        return out
    spec_text = spec.read_text(encoding="utf-8")
    _parity(out, label, spec_text, complete, directive_records)
    _bases(out, label, spec_text, complete, records)
    return out


def _parity(out: Outcome, label: str, spec_text: str, complete: list[ParsedRun], records: list[QRecord]) -> None:
    header = _header(spec_text).get("neighbours")
    if not _is_list_of(header, str):
        out.findings.append(f"{label}: spec.md needs a neighbours: list of spec paths")
        return
    problems = False
    if len(set(header)) != len(header):
        out.findings.append(f"{label}: the neighbours header repeats a path")
        problems = True
    for path in header:
        if not neighbour_form(path):
            out.findings.append(
                f"{label}: the neighbours header path {path!r} has none of the three permitted spec forms"
            )
            problems = True
    required = {
        n["path"]
        for run in complete
        for n in (run.derived or {})["neighbours"]
        if n["status"] in ("given", "confirmed")
    }
    required |= {p for r in records for p in (*r.keep, *r.add)}
    required -= {p for r in records for p in r.drop}
    if problems:
        return
    for path in sorted(required - set(header)):
        out.findings.append(f"{label}: the neighbours header lacks the required path {path}")
    for path in sorted(set(header) - required):
        out.findings.append(
            f"{label}: the neighbours header holds {path}, which no complete run confirmed or gave and no maintainer record keeps or adds"
        )


def _bases(out: Outcome, label: str, spec_text: str, complete: list[ParsedRun], records: dict[str, QRecord]) -> None:
    by_run = {run.run_id: run for run in complete}
    supported = {claim for run in complete for claim in run.supported()}
    known = {c["id"] for run in complete for report in run.reports for c in report["claims"]}
    for number, bases in sorted(_basis_lines(spec_text).items()):
        origins = 0
        for token in re.findall(r"`([^`]+)`", " ".join(bases)):
            qref, claim = _QREF.match(token), _CLAIM.match(token)
            if qref:
                origins += 1
                record = records.get(qref.group(1))
                if record is None or not record.answered:
                    out.findings.append(
                        f"{label}: criterion {number} names {token}, which is not a maintainer-answered record"
                    )
            elif claim:
                origins += 1
                if token not in known:
                    reason = "an incomplete run" if claim.group(1) not in by_run else "no report"
                    out.findings.append(f"{label}: criterion {number} names the claim {token} of {reason}")
                elif token not in supported:
                    out.findings.append(
                        f"{label}: criterion {number} names the claim {token}, which the judge did not mark supported"
                    )
        if not origins:
            out.findings.append(
                f"{label}: criterion {number} names no supported claim and no answered Q-record as its basis"
            )


# ---------------------------------------------------------------------------
# the tree
# ---------------------------------------------------------------------------


def changes(root: Path, only: str | None) -> list[tuple[str, Path]]:
    base = root / CHANGES_DIR
    if not base.is_dir():
        raise CannotMeasure(f"{CHANGES_DIR} does not exist under {root}")
    folders = [(p.name, p) for p in sorted(base.iterdir()) if p.is_dir() and p.name != ARCHIVE]
    archive = base / ARCHIVE
    if archive.is_dir():
        folders += [(f"{ARCHIVE}/{p.name}", p) for p in sorted(archive.iterdir()) if p.is_dir()]
    if only is None:
        return folders
    chosen = [
        (label, path)
        for label, path in folders
        if label == only
        or (label.startswith(ARCHIVE + "/") and (m := _ARCHIVED.match(path.name)) and m.group(1) == only)
    ]
    if not chosen:
        raise CannotMeasure(f"no change named {only} under {CHANGES_DIR}")
    return chosen


def run(root: Path, only: str | None, out=print) -> int:
    findings: list[str] = []
    pending: list[str] = []
    unmeasured: list[str] = []
    try:
        folders = changes(root, only)
    except CannotMeasure as error:
        out(f"research-handoff: not measured - {error}")
        return 3
    for label, folder in folders:
        try:
            outcome = check_change(folder, label)
        except CannotMeasure as error:
            unmeasured.append(str(error))
            continue
        findings += outcome.findings
        pending += outcome.pending
        for note in outcome.notes:
            out(note)
    for line in pending:
        out(line)
    if unmeasured:
        for line in unmeasured:
            out(f"research-handoff: not measured - {line}")
        return 3
    for line in findings:
        out(f"research-handoff: {line}")
    if findings:
        out(f"research-handoff: {len(findings)} finding(s)")
        return 1
    out(f"research-handoff: measured {len(folders)} change(s), nothing found")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--change", default=None)
    args = parser.parse_args(argv)
    return run(args.root, args.change)


if __name__ == "__main__":
    raise SystemExit(main())
