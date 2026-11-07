"""One-time, evidence-based active research metadata correction for explore-provenance.

Run with --write to apply; without it, report candidates. Archives are never visited.
Only publisher-owned header fields and generated opening notices may change.
"""

from __future__ import annotations

import argparse
import re
import subprocess
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


def publication_producers(body: str) -> list[dict]:
    """Read each accepted single-model contribution, including its audited model.

    An audit without an ensuing publication is not a contribution. Fenced and
    quoted examples are not runner publications either.
    """
    visible = re.sub(r"(?ms)^(`{3,}|~{3,})[^\r\n]*\r?\n.*?^\1[ \t]*\r?$", "", body)
    records = []
    previous = 0
    for answer in re.finditer(r"(?m)^## Runner exploration — (\d{4}-\d{2}-\d{2})[ \t]*\r?\n\s*\S", visible):
        calls = list(
            re.finditer(
                r"(?m)^Stage-2 call, [^\r\n]*?explore ·[^\r\n]*?endpoint ([\w-]+)([^\r\n]*)",
                visible[previous : answer.start()],
            )
        )
        if not calls:
            raise ValueError("runner publication has no producing endpoint evidence")
        call = calls[-1]
        endpoint = call.group(1)
        if endpoint not in {"glm-coding-plan", "claude-code-plan", "openai-codex", "opencode-go"}:
            raise ValueError(f"unknown producing endpoint: {endpoint}")
        record = {"kind": "llm-session", "name": stage2.producer_for((endpoint, "", None)), "version": answer.group(1)}
        model = re.search(r" · model ([^·\r\n]+)", call.group(2))
        if model:
            record["model"] = model.group(1).strip().rstrip(".")
        if record not in records:
            records.append(record)
        previous = answer.end()
    return records


def known_producers(original: bytes, *, historical: bytes | None = None) -> list[dict]:
    """Recover original attribution plus all accepted audited contributions.

    Bare replacement headers from this branch do not erase the base's history.
    Later explicit model records remain evidence and are retained too.
    """
    text = original.decode("utf-8")
    match = FRONTMATTER.match(text)
    if match is None:
        raise ValueError("no research frontmatter")
    program, _ = publication_evidence(text[match.end() :])
    current = stage2.research_header_producers(match.group(1), program_hint=program)
    records = current if historical is None else []
    if historical is not None:
        old_text = historical.decode("utf-8")
        old = FRONTMATTER.match(old_text)
        if old is None:
            raise ValueError("historical research has no frontmatter")
        old_program, _ = publication_evidence(old_text[old.end() :])
        records = stage2.research_header_producers(old.group(1), program_hint=old_program)
        records += [record for record in current if record.get("model") and record not in records]
        for record in publication_producers(old_text[old.end() :]):
            if record not in records:
                records.append(record)
    for record in publication_producers(text[match.end() :]):
        if record not in records:
            records.append(record)
    # A model-specific record also represents a previously known bare program/day.
    return [
        record
        for record in records
        if record.get("model")
        or not any(
            other.get("model") and all(other.get(key) == value for key, value in record.items()) for other in records
        )
    ]


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
    header: Mapping,
    raw_header: str,
    program: str | None = None,
    publication_day: str | None = None,
    *,
    required_producers=(),
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
    for required in required_producers:
        if not any(
            isinstance(record, Mapping) and all(record.get(key) == value for key, value in required.items())
            for record in records
        ):
            problems.append(f"produced_by: missing known contribution {required}")
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


def normalised_research(original: bytes, *, correction_day: str, historical: bytes | None = None) -> bytes:
    text = original.decode("utf-8")
    match = FRONTMATTER.match(text)
    if match is None:
        raise ValueError("no research frontmatter")
    header = yaml.safe_load(match.group(1))
    if not isinstance(header, Mapping):
        raise ValueError("research header is not a mapping")
    program, publication_day = publication_evidence(text[match.end() :])
    producer = header.get("produced_by")
    records = known_producers(original, historical=historical)
    if (
        not program
        and not records
        and not model_attribution(producer)
        and header.get("provenance") != "ai-drafted-reviewed"
    ):
        return original
    if not records:
        raise ValueError("no historical producer/date evidence")
    if not is_day(correction_day):
        raise ValueError("no valid correction date")
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    # A compliant file is byte-identical, including its unrelated formatting and edit stamp.
    if (
        not metadata_problems(header, match.group(1), program, publication_day, required_producers=records)
        and header.get("produced_by") == (records[0] if len(records) == 1 else records)
        and not stage2.research_opening_notices(text, match.end())
    ):
        return original
    corrected = bom + stage2.research_publication(
        original[len(bom) :], producer=records[-1]["name"], day=correction_day, producers=records
    )
    final = FRONTMATTER.match(corrected.decode("utf-8"))
    problems = metadata_problems(
        yaml.safe_load(final.group(1)), final.group(1), program, publication_day, required_producers=records
    )
    if problems:
        raise ValueError("; ".join(problems))
    return corrected


BASE = "9633355e915bc64266d26b49575f63e486641471"


def historical_research(root: Path, relative: str) -> bytes | None:
    """Read pre-correction attribution; later-created files use their first Git version."""

    def git(*args):
        return subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)

    result = git("show", f"{BASE}:{relative}")
    if result.returncode == 0:
        return result.stdout
    # A missing base commit is not evidence that no historical contributor exists.
    if git("cat-file", "-e", BASE).returncode:
        raise ValueError("pre-correction Git base is unreadable")
    commits = git("log", "--reverse", "--format=%H", "HEAD", "--", relative)
    if commits.returncode:
        raise ValueError("research Git history is unreadable")
    for commit in commits.stdout.decode().splitlines():
        result = git("show", f"{commit}:{relative}")
        if result.returncode == 0:
            old = FRONTMATTER.match(result.stdout.decode("utf-8"))
            if old and model_attribution(yaml.safe_load(old.group(1)).get("produced_by")):
                return result.stdout
    return None


def base_research_paths(root: Path) -> set[str]:
    """Freeze the one-time authorisation to active research present at the base."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", BASE, "--", "plans/changes/"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError("pre-correction Git base inventory is unreadable")
    return {
        path
        for path in result.stdout.decode().splitlines()
        if re.fullmatch(r"plans/changes/(?!archive/)[^/]+/research\.md", path)
    }


def authorised_research(root: Path) -> list[Path]:
    """Check the approved base inventory; later research is outside this one-time batch."""
    plan = (root / "plans/changes/explore-provenance/plan.md").read_text()
    inventory = set(re.findall(r"^- `(plans/changes/[^/]+/research\.md)`", plan, re.M))
    base = base_research_paths(root)
    paths = []
    for path in sorted((root / "plans/changes").glob("*/research.md")):
        relative = path.relative_to(root).as_posix()
        if relative not in base:
            continue
        if relative not in inventory or path.is_symlink() or path.parent.is_symlink():
            raise ValueError(f"{relative}: outside authorised active research inventory")
        paths.append(path)
    return paths


def prepare_batch(root: Path, *, correction_day: str) -> list[tuple[Path, bytes]]:
    changes = []
    for path in authorised_research(root):
        relative = path.relative_to(root).as_posix()
        try:
            original = path.read_bytes()
            corrected = normalised_research(
                original, correction_day=correction_day, historical=historical_research(root, relative)
            )
        except (ValueError, OSError, yaml.YAMLError, stage2.Refused) as error:
            raise ValueError(f"{relative}: {error}") from error
        if corrected != original:
            changes.append((path, corrected))
    return changes


def main(root: Path | None = None, argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    root = root or Path(__file__).resolve().parents[1]
    # Prepare and validate the entire authorised batch before the first replacement.
    for path, corrected in prepare_batch(root, correction_day=date.today().isoformat()):
        print(path.relative_to(root))
        if args.write:
            stage2.write_atomic(path, corrected)


if __name__ == "__main__":
    main()
