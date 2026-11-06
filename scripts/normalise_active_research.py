"""One-time, evidence-based active research metadata correction for explore-provenance.

Run with --write to apply; without it, report candidates. Archives are never visited.
Only publisher-owned header fields and generated opening notices may change.
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Mapping
from datetime import date
from pathlib import Path

import stage2
import yaml

FRONTMATTER = re.compile(r"\A\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)
PROGRAMS = {"claude-code", "codex", "pi", "stage2-research-swarm"}
PENDING = {"status": "pending", "approved_by": None, "approved_at": None}


def publication_evidence(body: str) -> tuple[str | None, str | None]:
    """Return the latest visible runner publication's program and date, not quoted examples."""
    visible = re.sub(r"(?ms)^(`{3,}|~{3,})[^\r\n]*\r?\n.*?^\1[ \t]*\r?$", "", body)
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
    if endpoint not in {"glm-coding-plan", "claude-code-plan", "openai-codex", "opencode-go"}:
        raise ValueError(f"unknown producing endpoint: {endpoint}")
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
    for key, value in node.value:
        if key.value in {"produced_by", "review"} and isinstance(value, yaml.MappingNode):
            nested_keys = [child.value for child, _ in value.value]
            if len(nested_keys) != len(set(nested_keys)):
                problems.append(f"{key.value}: duplicate metadata keys")
    if header.get("provenance") != "ai-drafted-reviewed":
        problems.append("provenance: expected ai-drafted-reviewed")
    producer = header.get("produced_by")
    version = None
    if not isinstance(producer, Mapping):
        problems.append("produced_by: expected program and publication date")
    else:
        version = producer.get("version")
        if producer.get("kind") != "llm-session":
            problems.append("produced_by.kind: expected llm-session")
        if producer.get("name") not in PROGRAMS or (program and producer.get("name") != program):
            problems.append("produced_by.name: expected producing program")
        if not isinstance(version, str) or not is_day(version):
            problems.append("produced_by.version: expected one publication date")
        elif publication_day and version < publication_day:
            problems.append("produced_by.version: predates published research")
    if header.get("review") != PENDING:
        problems.append("review: expected pending without approval")
    for field in ("date", "last_reviewed", "updated"):
        if not is_day(header.get(field)):
            problems.append(f"{field}: expected calendar date")
    if all(is_day(header.get(field)) for field in ("date", "last_reviewed", "updated")):
        created, reviewed, updated = (str(header[field]) for field in ("date", "last_reviewed", "updated"))
        if not created <= reviewed <= updated:
            problems.append("dates: expected date <= last_reviewed <= updated")
        if is_day(version) and not created <= str(version) <= updated:
            problems.append("dates: publication outside date..updated")
    return problems


def normalised_research(original: bytes, *, correction_day: str) -> bytes:
    text = original.decode("utf-8")
    match = FRONTMATTER.match(text)
    if match is None:
        raise ValueError("no research frontmatter")
    header = yaml.safe_load(match.group(1))
    program, publication_day = publication_evidence(text[match.end() :])
    producer = header.get("produced_by", {})
    model_written = isinstance(producer, Mapping) and producer.get("kind") == "llm-session"
    if not program and not model_written and header.get("provenance") != "ai-drafted-reviewed":
        return original  # An unpublished skeleton is still human-written.
    if not metadata_problems(header, match.group(1), program, publication_day) and not stage2.research_opening_notices(
        text, match.end()
    ):
        return original
    producer = producer if isinstance(producer, Mapping) else {}
    if not program:
        name = producer.get("name")
        program = "claude-code" if name == "Claude Code" else name
        if program not in PROGRAMS:
            raise ValueError("no program evidence")
    days = re.findall(r"\d{4}-\d{2}-\d{2}", str(producer.get("version", "")))
    if len(days) == 1 and is_day(days[0]):
        publication_day = max(filter(None, (publication_day, days[0])))
    if not is_day(publication_day) or not is_day(correction_day):
        raise ValueError("no valid publication or correction date")
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    corrected = bom + stage2.research_publication(original[len(bom) :], producer=program, day=publication_day)
    # Publication date remains historical; only the edit stamp is today's date.
    corrected = re.sub(rb"(?m)^updated: [^\r\n]+", b"updated: " + correction_day.encode(), corrected, count=1)
    final = FRONTMATTER.match(corrected.decode("utf-8"))
    problems = metadata_problems(yaml.safe_load(final.group(1)), final.group(1), program, publication_day)
    if problems:
        raise ValueError("; ".join(problems))
    return corrected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    # Prepare every correction before writing any: unknown evidence stops the backfill.
    changes = []
    for path in sorted((root / "plans/changes").glob("*/research.md")):
        original = path.read_bytes()
        corrected = normalised_research(original, correction_day=date.today().isoformat())
        if corrected != original:
            changes.append((path, corrected))
    for path, corrected in changes:
        print(path.relative_to(root))
        if args.write:
            stage2.write_atomic(path, corrected)


if __name__ == "__main__":
    main()
