"""The research metadata census: the contract an explore publication must leave in research.md.

A library, not an entry point: tests/test_explore_provenance.py runs it over active research.
It only reads; correcting existing research files is a separate change (bead coding-harness-2i7x).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from collections.abc import Iterable, Mapping
from datetime import date
from pathlib import Path

import venv_guard  # noqa: F401
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adoption  # noqa: E402
import plans_registry  # noqa: E402
import stage2  # noqa: E402

FRONTMATTER = plans_registry.FRONTMATTER
PROGRAMS = plans_registry.PROGRAMS
is_day = plans_registry.is_day
producer_record_problems = plans_registry.producer_record_problems
producer_records_problems = plans_registry.producer_records_problems
# Q-5 and option C (maintainer, 2026-11-12): the adoption day is read from decisions/adoption.yaml;
# a file's last change is read from git, never from a date written in the file.
GATE = "research-census"
PENDING = {"status": "pending", "approved_by": None, "approved_at": None}
SINGLE_PUBLICATION = re.compile(r"(?m)^## Runner exploration — (\d{4}-\d{2}-\d{2})[ \t]*\r?\n\s*\S")
SWARM_PUBLICATION = re.compile(
    r"(?ms)^<!-- research-swarm/v2 run [0-9a-f]+ -->\r?\n.+?^<!-- /research-swarm/v2 -->[ \t]*\r?$"
)
SWARM_DAY = re.compile(r"(?m)^## Research swarm — (\d{4}-\d{2}-\d{2})[ \t]*\r?$")


def publication_evidence(body: str) -> tuple[str | None, str | None]:
    """Return the latest visible runner publication's program and date, not quoted examples."""
    visible = stage2.research_visible_text(body)
    singles = list(SINGLE_PUBLICATION.finditer(visible))
    swarms = list(SWARM_PUBLICATION.finditer(visible))
    if swarms and (not singles or swarms[-1].start() > singles[-1].start()):
        return "stage2-research-swarm", max(SWARM_DAY.findall(swarms[-1].group()), default=None)
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

    ancestors = set()

    def duplicates(value, field):
        identity = id(value)
        if identity in ancestors:
            raise ValueError(f"{field}: recursive metadata structure")
        ancestors.add(identity)
        try:
            duplicate_children(value, field)
        finally:
            ancestors.remove(identity)

    def duplicate_children(value, field):
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
    problems.extend(producer_records_problems(producer))
    if program and not any(
        isinstance(record, Mapping)
        and record.get("name") == program
        and isinstance(record.get("version"), str)
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


def last_change_day(root: Path, relative: str) -> date | None:
    """The day of the last commit touching the file, or None when it is uncommitted,
    modified, untracked or git cannot say. None means: no stock exemption (fail closed)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, timeout=60, check=False, env=env
        )

    try:
        status = git("status", "--porcelain", "--", relative)
        if status.returncode != 0 or status.stdout.strip():
            return None
        log = git("log", "-1", "--format=%cs", "--", relative)
        if log.returncode != 0:
            return None
        return date.fromisoformat(log.stdout.strip())
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def adoption_day(root: Path) -> date | None:
    """The recorded adoption day of the census, or None when it is not recorded."""
    try:
        return adoption.adopted_on(root, GATE)
    except adoption.NotRecorded:
        return None


def text_findings(relative: str, text: str) -> list[str]:
    """Every census defect of one file's text, each line prefixed with its relative path.

    Shared with the runner's post-run check, so an active research publication a route
    prepares is judged by the same publication contract the census applies (spec,
    criterion 14). A file the census cannot read at all returns exactly one unreadable
    finding; a file without frontmatter is `unreadable header`, never silently clean.
    """
    frontmatter = FRONTMATTER.match(text)
    if frontmatter is None:
        return [f"{relative}: unreadable header (no frontmatter)"]
    try:
        header = yaml.safe_load(frontmatter.group(1))
    except (yaml.YAMLError, ValueError):
        return [f"{relative}: unreadable header (malformed YAML)"]
    if not isinstance(header, Mapping):
        return [f"{relative}: unreadable header (not a mapping)"]
    findings: list[str] = []
    body = text[frontmatter.end() :]
    try:
        program, publication_day = publication_evidence(body)
    except ValueError as error:
        findings.append(f"{relative}: {error}")
        program, publication_day = None, None
    if program or model_attribution(header.get("produced_by")) or header.get("provenance") == "ai-drafted-reviewed":
        findings.extend(
            f"{relative}: {problem}"
            for problem in metadata_problems(header, frontmatter.group(1), program, publication_day)
        )
        if stage2.research_opening_notices(text, frontmatter.end()):
            findings.append(f"{relative}: opening skeleton notice over published research")
    return findings


def _file_findings(path: Path, relative: str, collected: list[str]) -> None:
    """Read one file and append every defect it has, before any exemption."""
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        collected.append(f"{relative}: unreadable file (not UTF-8)")
        return
    except OSError as error:
        collected.append(f"{relative}: unreadable file ({error})")
        return
    collected.extend(text_findings(relative, text))


def census_findings(paths: Iterable[Path], root: Path, *, apply_adoption: bool = False) -> list[str]:
    """Report every defect of every file; one file's failure never ends the scan.

    With apply_adoption, a file with metadata findings is stock, and not reported, only when
    git shows it committed unchanged and its last commit lies before the recorded adoption
    day. Uncommitted, modified, untracked or unreadable history fails closed (EP6-13)."""
    day = adoption_day(root) if apply_adoption else None
    affected: list[str] = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        found: list[str] = []
        try:
            _file_findings(path, relative, found)
        except Exception as error:  # any YAML or read failure is this file's finding (EP6-14)
            found = [f"{relative}: unreadable metadata ({type(error).__name__}: {error})"]
        metadata_defect = bool(found) and not any(": unreadable " in line for line in found)
        if metadata_defect and day is not None:
            changed = last_change_day(root, relative)
            if changed is not None and changed < day:
                found = []
        affected.extend(found)
    return affected
