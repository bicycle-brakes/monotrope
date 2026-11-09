"""The research metadata census: the contract an explore publication must leave in research.md.

A library, not an entry point: tests/test_explore_provenance.py runs it over active research.
It only reads; correcting existing research files is a separate change (bead coding-harness-2i7x).
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from datetime import date
from pathlib import Path

import stage2
import yaml

FRONTMATTER = re.compile(r"\A\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)
PROGRAMS = {"claude-code", "codex", "pi", "stage2-research-swarm"}
PENDING = {"status": "pending", "approved_by": None, "approved_at": None}


def publication_evidence(body: str) -> tuple[str | None, str | None]:
    """Return the latest visible runner publication's program and date, not quoted examples."""
    visible = stage2.research_visible_text(body)
    singles = list(re.finditer(r"(?m)^## Runner exploration — (\d{4}-\d{2}-\d{2})[ \t]*\r?\n\s*\S", visible))
    swarms = list(
        re.finditer(
            r"(?ms)^<!-- research-swarm/v2 run [0-9a-f]+ -->\r?\n.+?^<!-- /research-swarm/v2 -->[ \t]*\r?$",
            visible,
        )
    )
    if swarms and (not singles or swarms[-1].start() > singles[-1].start()):
        # The exact swarm publication date is already retained in its producer header.
        return "stage2-research-swarm", None
    if not singles:
        return None, None
    answer = singles[-1]
    calls = list(
        re.finditer(r"(?m)^Stage-2 call, [^\r\n]*?explore ·[^\r\n]*?endpoint ([\w-]+)", visible[: answer.start()])
    )
    if not calls:
        raise ValueError("runner publication has no producing endpoint evidence")
    endpoint = calls[-1].group(1)
    return stage2.producer_for((endpoint, "", None)), answer.group(1)


def is_day(value: object) -> bool:
    if isinstance(value, date):
        return type(value) is date
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def metadata_problems(
    header: Mapping, raw_header: str, program: str | None = None, publication_day: str | None = None
) -> list[str]:
    """Check the whole publication metadata contract, including duplicate owned fields."""
    problems = []
    node = yaml.compose(raw_header)
    keys = [key.value for key, _ in node.value]
    for key in ("provenance", "produced_by", "review", "date", "last_reviewed", "updated"):
        if keys.count(key) != 1:
            problems.append(f"{key}: expected exactly one field")

    def duplicates(value, field):
        if isinstance(value, yaml.MappingNode):
            nested_keys = [child.value for child, _ in value.value]
            if len(nested_keys) != len(set(nested_keys)):
                problems.append(f"{field}: duplicate metadata keys")
            for _, child in value.value:
                duplicates(child, field)
        elif isinstance(value, yaml.SequenceNode):
            for child in value.value:
                duplicates(child, field)

    for key, value in node.value:
        if key.value in {"produced_by", "review"}:
            duplicates(value, key.value)
    if header.get("provenance") != "ai-drafted-reviewed":
        problems.append("provenance: expected ai-drafted-reviewed")
    producer = header.get("produced_by")
    records = producer if isinstance(producer, list) else [producer]
    if not records:
        problems.append("produced_by: expected nonempty producer list")
    for record in records:
        if not isinstance(record, Mapping):
            problems.append("produced_by: expected program and publication date")
            continue
        if record.get("kind") != "llm-session":
            problems.append("produced_by.kind: expected llm-session")
        if not isinstance(record.get("name"), str) or record.get("name") not in PROGRAMS:
            problems.append("produced_by.name: expected producing program")
        if not isinstance(record.get("version"), str) or not is_day(record.get("version")):
            problems.append("produced_by.version: expected one publication date")
        if "model" in record and (not isinstance(record["model"], str) or not record["model"].strip()):
            problems.append("produced_by.model: expected known model identity")
    if program and not any(
        isinstance(record, Mapping)
        and record.get("name") == program
        and is_day(record.get("version"))
        and (not publication_day or record["version"] >= publication_day)
        for record in records
    ):
        problems.append("produced_by: missing publication program/date")
    if header.get("review") != PENDING:
        problems.append("review: expected pending without approval")
    for field in ("date", "last_reviewed", "updated"):
        if not is_day(header.get(field)):
            problems.append(f"{field}: expected calendar date")
    if all(is_day(header.get(field)) for field in ("date", "last_reviewed", "updated")):
        created, reviewed, updated = (str(header[field]) for field in ("date", "last_reviewed", "updated"))
        if not created <= reviewed <= updated:
            problems.append("dates: expected date <= last_reviewed <= updated")
        for record in records:
            version = record.get("version") if isinstance(record, Mapping) else None
            if is_day(version) and not created <= str(version) <= updated:
                problems.append("dates: publication outside date..updated")
    return problems


def model_attribution(producer) -> bool:
    records = producer if isinstance(producer, list) else [producer]
    return any(isinstance(record, Mapping) and record.get("kind") == "llm-session" for record in records)


def census_findings(paths: Iterable[Path], root: Path) -> list[str]:
    """Read current research and report every path-specific defect before exemptions."""
    affected = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            affected.append(f"{relative}: unreadable file (not UTF-8)")
            continue
        except OSError as error:
            affected.append(f"{relative}: unreadable file ({error})")
            continue
        frontmatter = FRONTMATTER.match(text)
        if frontmatter is None:
            affected.append(f"{relative}: unreadable header (no frontmatter)")
            continue
        try:
            header = yaml.safe_load(frontmatter.group(1))
        except (yaml.YAMLError, ValueError):
            affected.append(f"{relative}: unreadable header (malformed YAML)")
            continue
        if not isinstance(header, Mapping):
            affected.append(f"{relative}: unreadable header (not a mapping)")
            continue
        body = text[frontmatter.end() :]
        try:
            program, publication_day = publication_evidence(body)
        except ValueError as error:
            affected.append(f"{relative}: {error}")
            program, publication_day = None, None
        producer = header.get("produced_by")
        model_written = model_attribution(producer)
        if program or model_written or header.get("provenance") == "ai-drafted-reviewed":
            affected.extend(
                f"{relative}: {problem}"
                for problem in metadata_problems(header, frontmatter.group(1), program, publication_day)
            )
            notices = stage2.research_opening_notices(text, frontmatter.end())
            if notices:
                affected.append(f"{relative}: opening skeleton notice over published research")
    return affected
