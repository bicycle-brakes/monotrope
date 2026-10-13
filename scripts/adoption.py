#!/usr/bin/env python3
"""adoption.py — the day a repository adopted a gate that exempts older changes.

A gate that holds only the changes begun after it came (the class minimums of
`interview-minimums`) needs that day per repository, and the day is not the
kit's to give: `decisions/adoption.yaml` stays in its repository and maps a
gate id of `decisions/gates.yaml` to the day, an unquoted YAML date:

    schema_version: 1
    adopted:
      interview-minimums: 2026-10-08

`adopted_on(root, gate)` is the one reader. It neither writes nor guesses a
day: a record it cannot read, or a gate with no day in it, raises
`NotRecorded`, and the caller says "not measured" (ADR 0014, ADR 0013 for the
second reader, bead coding-harness-wpv).
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_adr_answers  # noqa: E402 — the one strict YAML reader of the decisions files

RECORD = "decisions/adoption.yaml"


class NotRecorded(Exception):  # noqa: N818 — a verdict, not an error class
    """The day cannot be read from the record. The message names the record and the line to add."""


def _remedy(gate: str) -> str:
    return f"{RECORD} needs `schema_version: 1` and, under `adopted:`, the line `  {gate}: YYYY-MM-DD` (unquoted)"


def adopted_on(root: Path, gate: str) -> date:
    """The day `root` adopted `gate`, or NotRecorded."""
    path = root / RECORD
    try:
        text = path.read_bytes().decode("utf-8")
    except FileNotFoundError:
        raise NotRecorded(f"{RECORD} does not exist — {_remedy(gate)}") from None
    except (OSError, UnicodeDecodeError) as exc:
        raise NotRecorded(f"{RECORD} cannot be read ({exc}) — {_remedy(gate)}") from None
    try:
        data = check_adr_answers.strict_load(text)
    except (yaml.YAMLError, ValueError) as exc:  # ValueError: an impossible date such as 2026-02-30
        raise NotRecorded(f"{RECORD} is not valid YAML ({' '.join(str(exc).split())}) — {_remedy(gate)}") from None
    if not isinstance(data, dict):
        raise NotRecorded(f"{RECORD} is not a YAML mapping — {_remedy(gate)}")
    version = data.get("schema_version")
    if not (type(version) is int and version == 1):
        raise NotRecorded(f"{RECORD} lacks `schema_version: 1` (it holds {version!r}) — {_remedy(gate)}")
    adopted = data.get("adopted")
    if not isinstance(adopted, dict):
        raise NotRecorded(f"{RECORD} has no `adopted:` mapping — {_remedy(gate)}")
    if gate not in adopted:
        raise NotRecorded(f"{RECORD} holds no day for {gate} — {_remedy(gate)}")
    day = adopted[gate]
    if type(day) is not date:
        raise NotRecorded(f"{RECORD} holds {day!r} for {gate}, which is no unquoted date — {_remedy(gate)}")
    return day
