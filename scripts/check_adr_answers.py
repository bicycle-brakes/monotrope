#!/usr/bin/env python3
"""check_adr_answers.py — every feature has the maintainer's answer to the ADR question.

A change can decide something that should be recorded as an architecture
decision. The spec of each change (its anchor) states its class; a `feature`
also states its name and a proposal, and owes an answer file
`decisions/answers/<change>/adr.yaml` in the LakeSwitch pilot's format
(`schema_version: 1`). This gate holds existence and format, nothing more: it
reads the files of the tree, offline, and cannot see who wrote an answer or who
merged it. The maintainer's merge of the decision pull request that carries an
answer is what gives it effect (docs/WORKFLOW.md, "Change classes, the ADR
question and decision pull requests").

This module is also the one reader of the format: `scripts/harness.py decide
adr` imports it, so the command writes exactly what the gate accepts.

Usage:
    python3 scripts/check_adr_answers.py             # measure this repository
    python3 scripts/check_adr_answers.py --root DIR  # another tree (tests)
Exit: 0 = nothing found, 1 = findings, 3 = could not measure.

Environment: `ADR_ANSWERS_TOLERATE_CHANGE=<change>` makes the missing answer of that one change
a report line and not a finding. `scripts/stage2.py draft` sets it for its document check: only
the maintainer may create the answer, so a drafted feature never has it, and the exit code then
decides without the runner reading any output. Another change's missing answer, a refused answer
file and every anchor problem stay findings.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

CLASSES = ("spike", "bounded", "feature", "architectural")
# `fullmatch`, not `^…$`: Python's `$` also matches before a trailing newline.
NAME = re.compile(r"[a-z0-9][a-z0-9-]*")
ROLE = re.compile(r"[a-z][a-z0-9-]*")
ANSWER_KEYS = ("schema_version", "change", "question", "answer", "reason", "shown", "answered_by", "answered_at")
SHOWN_KEYS = ("proposed", "proposal_reason")
QUESTION_KEYS = ("proposed", "reason", "answered_by")
ANSWERS_DIR = "decisions/answers"
FIX = "python3 scripts/harness.py decide adr"
REFUSED_FIX = f"edit it in a decision pull request, or delete it and run {FIX}"

CHANGES_DIR = "plans/changes"
ARCHIVE = "archive"
_DATED = re.compile(r"\d{4}-\d{2}-\d{2}-")

# The header: a first line `---`, the text, the next line that is `---`. A
# leading byte-order mark and CRLF line endings are tolerated.
_BLOCK = re.compile(r"\A﻿?---\r?\n(.*?)^---[ \t]*\r?$", re.S | re.M)
# `class: feature`, `class: "feature"`, `class: 'feature'`, each optionally
# followed by whitespace and a `# comment`. A `#` without whitespace before it
# belongs to the value, as YAML reads it.
_CLASS_LINE = re.compile(
    r"""^class:[ \t]+(?:"([^"\n]*)"|'([^'\n]*)'|([^\s"'#]\S*))(?:[ \t]+\#.*)?[ \t]*\r?$""",
)


class CannotMeasure(Exception):  # noqa: N818 — a verdict, not an error class
    """The question cannot be answered here. Exit 3, nothing measured."""


# ---------------------------------------------------------------------------
# strict YAML
# ---------------------------------------------------------------------------


class _StrictLoader(yaml.SafeLoader):
    """PyYAML's safe loader, refusing a key that appears twice in one mapping.

    PyYAML keeps the last of two equal keys without a word; the pilot refuses
    them, and so does this reader, for anchor headers and answers alike.
    """

    def construct_mapping(self, node: yaml.Node, deep: bool = False) -> dict[Any, Any]:
        if isinstance(node, yaml.MappingNode):
            seen: set[Any] = set()
            for key_node, _ in node.value:
                if key_node.tag == "tag:yaml.org,2002:merge":
                    continue
                key = self.construct_object(key_node, deep=True)
                try:
                    doubled = key in seen
                except TypeError:
                    continue  # an unhashable key; the base class names it
                if doubled:
                    raise yaml.constructor.ConstructorError(
                        "while reading a mapping",
                        node.start_mark,
                        f"found the key {key!r} twice",
                        key_node.start_mark,
                    )
                seen.add(key)
        return super().construct_mapping(node, deep=deep)


def strict_load(text: str) -> Any:
    """YAML 1.1 as PyYAML reads it, with duplicate keys refused (yaml.YAMLError)."""
    return yaml.load(text, Loader=_StrictLoader)  # a SafeLoader subclass: no arbitrary objects


# ---------------------------------------------------------------------------
# the rules of one value
# ---------------------------------------------------------------------------


def reason_problem(text: Any) -> str | None:
    """None when `text` is non-blank text starting with a capital letter or a backtick."""
    if not isinstance(text, str):
        return "is not text"
    if not text.strip():
        return "is blank"
    if not (text[0].isupper() or text[0] == "`"):
        return "starts with neither a capital letter nor a backtick"
    return None


def _nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _yes_no(value: Any) -> bool:
    # A bare `no` is the boolean False in YAML 1.1; only the text passes.
    return isinstance(value, str) and value in ("yes", "no")


# ---------------------------------------------------------------------------
# the anchors
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Anchor:
    path: Path
    rel: str
    name: str  # the change folder's name, without the date of an archived one
    archived: bool


@dataclass(frozen=True)
class Feature:
    anchor: Anchor
    change: str
    title: str
    proposed: str
    proposal_reason: str
    outcome: str | None


def anchors(root: Path) -> list[Anchor]:
    """Every change anchor: `plans/changes/*/spec.md` and `plans/changes/archive/*/spec.md`."""
    base = root / CHANGES_DIR
    found: list[Anchor] = []
    for path in sorted(base.glob("*/spec.md")):
        if path.parent.name != ARCHIVE:
            found.append(Anchor(path, path.relative_to(root).as_posix(), path.parent.name, False))
    for path in sorted((base / ARCHIVE).glob("*/spec.md")):
        folder = path.parent.name
        name = folder[len(m.group(0)) :] if (m := _DATED.match(folder)) else folder
        found.append(Anchor(path, path.relative_to(root).as_posix(), name, True))
    return found


def read_header(path: Path) -> tuple[str | None, str | None]:
    """(header text, None) or (None, why there is none)."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return None, f"cannot be read ({exc.strerror or exc})"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, f"cannot be read as UTF-8 text ({exc.reason} at byte {exc.start})"
    m = _BLOCK.match(text)
    if not m:
        return None, "has no header (no `---` block at the top)"
    return m.group(1), None


def read_class(path: Path) -> tuple[str | None, str | None]:
    """Criterion 1: (class, None), or (None, the problem)."""
    header, problem = read_header(path)
    if header is None:
        return None, problem
    lines = [line for line in header.split("\n") if line.startswith("class:")]
    if not lines:
        return None, "has no `class:` line in its header"
    if len(lines) > 1:
        return None, f"has {len(lines)} `class:` lines in its header"
    m = _CLASS_LINE.match(lines[0])
    if not m:
        return None, f"has a `class:` line that cannot be read: {lines[0].rstrip()!r}"
    value = next(v for v in m.groups() if v is not None)
    if value not in CLASSES:
        return None, f"states `class: {value}`, which is not one of {', '.join(CLASSES)}"
    return value, None


def read_feature(anchor: Anchor) -> tuple[Feature | None, list[str]]:
    """Criterion 2, on the strictly loaded header of an anchor whose class is `feature`."""
    header, problem = read_header(anchor.path)
    if header is None:
        return None, [problem or "has no header"]
    try:
        data = strict_load(header)
    except yaml.YAMLError as exc:
        return None, [f"has a header that is not valid YAML ({' '.join(str(exc).split())})"]
    if not isinstance(data, dict):
        return None, ["has a header that is not a mapping"]

    problems: list[str] = []
    title = data.get("title")
    if not _nonblank(title):
        problems.append("`title` is missing or not non-blank text")
    change = data.get("change")
    if not (isinstance(change, str) and NAME.fullmatch(change)):
        problems.append(f"`change` is missing or does not match ^{NAME.pattern}$")
    elif change != anchor.name:
        problems.append(f"`change: {change}` differs from its folder's name `{anchor.name}`")

    question = data.get("adr_question")
    proposed = reason = None
    if not isinstance(question, dict):
        problems.append("`adr_question` is missing or not a mapping")
    else:
        extra = [str(k) for k in question if k not in QUESTION_KEYS]
        if extra:
            problems.append(f"`adr_question` has a key it does not admit: {', '.join(extra)}")
        proposed = question.get("proposed")
        if not _yes_no(proposed):
            problems.append(
                f"`adr_question.proposed` must be the text yes or no, is {proposed!r}"
                + (" (a bare yes or no is a YAML boolean; quote it)" if isinstance(proposed, bool) else "")
            )
        reason = question.get("reason")
        if not _nonblank(reason):
            problems.append("`adr_question.reason` is missing or not non-blank text")
        if "answered_by" in question and not (
            question["answered_by"] is None or isinstance(question["answered_by"], str)
        ):
            problems.append("`adr_question.answered_by` must be null or text")
    if problems:
        return None, problems

    intent = data.get("intent")
    outcome = intent.get("outcome") if isinstance(intent, dict) else None
    return (
        Feature(
            anchor=anchor,
            change=str(change),
            title=str(title).strip(),
            proposed=str(proposed),
            proposal_reason=str(reason).strip(),
            outcome=outcome.strip() if isinstance(outcome, str) and outcome.strip() else None,
        ),
        [],
    )


# ---------------------------------------------------------------------------
# the answers
# ---------------------------------------------------------------------------


def answer_rel(change: str) -> str:
    return f"{ANSWERS_DIR}/{change}/adr.yaml"


def answer_problems(data: Any) -> list[str]:
    """Criterion 3: why an answer file is refused. Empty = accepted."""
    if not isinstance(data, dict):
        return ["is not a YAML mapping"]
    problems: list[str] = []
    missing = [k for k in ANSWER_KEYS if k not in data]
    if missing:
        problems.append(f"lacks {', '.join(missing)}")
    extra = [str(k) for k in data if k not in ANSWER_KEYS]
    if extra:
        problems.append(f"has a key the format does not admit: {', '.join(extra)}")

    if "schema_version" in data:
        v = data["schema_version"]
        if not (type(v) is int and v == 1):
            problems.append(f"`schema_version` must be the integer 1, is {v!r}")
    if "change" in data and not (isinstance(data["change"], str) and NAME.fullmatch(data["change"])):
        problems.append(f"`change` must match ^{NAME.pattern}$, is {data['change']!r}")
    if "question" in data and data["question"] != "adr":
        problems.append(f"`question` must be the text adr, is {data['question']!r}")
    if "answer" in data and not _yes_no(data["answer"]):
        problems.append(f"`answer` must be the text yes or no, is {data['answer']!r}")
    if "reason" in data and (why := reason_problem(data["reason"])):
        problems.append(f"`reason` {why}")
    if "shown" in data:
        shown = data["shown"]
        if not isinstance(shown, dict) or sorted(map(str, shown)) != sorted(SHOWN_KEYS):
            problems.append("`shown` must be a mapping with exactly proposed and proposal_reason")
        else:
            if not _yes_no(shown["proposed"]):
                problems.append(f"`shown.proposed` must be the text yes or no, is {shown['proposed']!r}")
            if not _nonblank(shown["proposal_reason"]):
                problems.append("`shown.proposal_reason` must be non-blank text")
    if "answered_by" in data and not (isinstance(data["answered_by"], str) and ROLE.fullmatch(data["answered_by"])):
        problems.append(f"`answered_by` must match ^{ROLE.pattern}$, is {data['answered_by']!r}")
    if "answered_at" in data and type(data["answered_at"]) is not date:
        problems.append(f"`answered_at` must be a YAML date (not quoted, no time), is {data['answered_at']!r}")
    return problems


def load_answer(path: Path) -> tuple[Any, list[str]]:
    """(data, problems) for one answer file; an unreadable file or a YAML error is a problem."""
    try:
        text = path.read_bytes().decode("utf-8")
    except OSError as exc:
        return None, [f"cannot be read ({exc.strerror or exc})"]
    except UnicodeDecodeError as exc:
        return None, [f"cannot be read as UTF-8 text ({exc.reason} at byte {exc.start})"]
    return parse_answer(text)


def parse_answer(text: str) -> tuple[Any, list[str]]:
    try:
        data = strict_load(text)
    except yaml.YAMLError as exc:
        return None, [f"is not valid YAML ({' '.join(str(exc).split())})"]
    return data, answer_problems(data)


# ---------------------------------------------------------------------------
# the examination
# ---------------------------------------------------------------------------


@dataclass
class Examination:
    anchors: list[Anchor] = field(default_factory=list)
    classes: dict[str, str] = field(default_factory=dict)  # anchor rel -> class, where it reads
    features: list[Feature] = field(default_factory=list)  # held to their answer
    anchor_findings: list[tuple[Anchor, str]] = field(default_factory=list)  # (anchor, report line)
    missing: list[Feature] = field(default_factory=list)
    answer_findings: list[tuple[Feature, str]] = field(default_factory=list)  # (feature, report line)

    def lines(self) -> list[str]:
        """Every finding, one report line each, in the order anchors, missing, answers."""
        return (
            [line for _, line in self.anchor_findings]
            + [missing_line(f) for f in self.missing]
            + [line for _, line in self.answer_findings]
        )


def missing_line(f: Feature) -> str:
    return (
        f"adr-answers: {f.change}: no answer — {f.anchor.rel} is a feature and "
        f"{answer_rel(f.change)} does not exist; fix: {FIX}"
    )


def examine(root: Path) -> Examination:
    ex = Examination(anchors=anchors(root))
    read: list[Feature] = []
    for anchor in ex.anchors:
        cls, problem = read_class(anchor.path)
        if cls is None:
            ex.anchor_findings.append(
                (anchor, f"adr-answers: {anchor.rel}: {problem} — whether this change owes an ADR answer is unknown")
            )
            continue
        ex.classes[anchor.rel] = cls
        if cls != "feature":
            continue
        feature, problems = read_feature(anchor)
        if feature is None:
            ex.anchor_findings.append(
                (
                    anchor,
                    f"adr-answers: {anchor.rel}: a feature whose header breaks its shape — {'; '.join(problems)} — "
                    "whether it has the answer it owes is unknown until the header reads",
                )
            )
            continue
        read.append(feature)

    by_change: dict[str, list[Feature]] = {}
    for f in read:
        by_change.setdefault(f.change, []).append(f)
    for change, group in by_change.items():
        if len(group) > 1:
            rels = " and ".join(f.anchor.rel for f in group)
            for f in group:
                ex.anchor_findings.append(
                    (
                        f.anchor,
                        f"adr-answers: {f.anchor.rel}: two features name change `{change}` ({rels}) — "
                        "whether each has the answer it owes is unknown",
                    )
                )
    ex.features = [f for f in read if len(by_change[f.change]) == 1]

    for f in ex.features:
        path = root / answer_rel(f.change)
        if not path.exists():
            ex.missing.append(f)
            continue
        data, problems = load_answer(path)
        where = f"anchor {f.anchor.rel}; fix: {REFUSED_FIX}"
        if problems:
            ex.answer_findings.append(
                (f, f"adr-answers: {f.change}: {answer_rel(f.change)} is refused ({'; '.join(problems)}) — {where}")
            )
        elif data["change"] != f.change:
            ex.answer_findings.append(
                (f, f"adr-answers: {f.change}: {answer_rel(f.change)} names change `{data['change']}` — {where}")
            )
    return ex


# ---------------------------------------------------------------------------
# the command line
# ---------------------------------------------------------------------------


TOLERATE_ENV = "ADR_ANSWERS_TOLERATE_CHANGE"


def run(root: Path, out: Any = print, tolerate: str | None = None) -> int:
    try:
        if not root.is_dir() or not os.access(root, os.R_OK | os.X_OK):
            raise CannotMeasure(f"{root} is not a readable directory")
        ex = examine(root)
    except (CannotMeasure, OSError) as exc:
        out(f"adr-answers: cannot measure — {exc}")
        return 3
    if tolerate:
        owed = [f for f in ex.missing if f.change == tolerate]
        ex.missing = [f for f in ex.missing if f.change != tolerate]
        for f in owed:
            out(
                f"adr-answers: {f.change}: answer owed to the maintainer, tolerated for this run — {answer_rel(f.change)}"
            )
    lines = ex.lines()
    if lines:
        for line in lines:
            out(line)
        return 1
    if not ex.features:
        out(f"adr-answers: examined nothing — read {len(ex.anchors)} change anchors, none of them a feature")
        return 0
    names = ", ".join(f.change for f in ex.features)
    out(
        f"adr-answers: read {len(ex.anchors)} change anchors; held {len(ex.features)} features to their answer files: {names}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0], allow_abbrev=False)
    ap.add_argument("--root", type=Path, default=REPO_ROOT, help="tree to measure (default: this repository)")
    args = ap.parse_args(argv)
    return run(args.root.resolve(), tolerate=os.environ.get(TOLERATE_ENV) or None)


if __name__ == "__main__":
    sys.exit(main())
