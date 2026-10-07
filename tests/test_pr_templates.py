"""A decision pull request says that it decides (plans/changes/harness-decide-adr, criterion 13).

The decision block lives in one file, `.github/PULL_REQUEST_TEMPLATE/decision.md`;
every other pull request takes `.github/pull_request_template.md`, whose top says
that nothing is decided. Both texts come from
`docs/research/2026-09-30-decision-pull-requests.md`, proposals (c) and (d).
These tests read only the two templates, so they hold wherever the templates
travel. One of them also reads that `scripts/touch_map.py` exists: a template that
names a script an instance lacks sends every pull request there to a missing file,
and both travel with the kit.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DECISION = REPO / ".github" / "PULL_REQUEST_TEMPLATE" / "decision.md"
ORDINARY = REPO / ".github" / "pull_request_template.md"

# Each part criterion 13 names -> the text in the template that carries it.
DECISION_PARTS: dict[str, str] = {
    "what is decided": "**Merging this PR decides:**",
    "the merge is the maintainer's confirmation": "**Your move:** merge (or ask an agent to) = accept",
    "the consequence of the choice": "## What your merge confirms",
    "the options with their consequences": "## Options",
    "the next steps": "## After the merge",
    "how to undo it": "**Undo:**",
    "where it fits in the workflow": "## Where it fits",
}


def missing(text: str, parts: dict[str, str]) -> list[str]:
    """The parts whose carrying text is absent from `text`."""
    return [part for part, marker in parts.items() if marker not in text]


def _decision() -> str:
    return DECISION.read_text(encoding="utf-8")


def _ordinary() -> str:
    return ORDINARY.read_text(encoding="utf-8")


def test_the_decision_template_has_every_part() -> None:
    assert missing(_decision(), DECISION_PARTS) == []


def test_a_template_missing_a_part_is_caught() -> None:
    text = _decision()
    for part, marker in DECISION_PARTS.items():
        assert missing(text.replace(marker, ""), DECISION_PARTS) == [part], f"removing {marker!r} passed"


def test_the_decision_line_comes_first() -> None:
    first = _decision().splitlines()[:3]
    assert any(DECISION_PARTS["what is decided"] in line for line in first), (
        "the decision must be readable in the first lines, before anything else"
    )


def test_one_alert_and_no_table_or_checkbox() -> None:
    for path, text in ((DECISION, _decision()), (ORDINARY, _ordinary())):
        lines = text.splitlines()
        alerts = [line for line in lines if re.match(r"^> \[!\w+\]", line)]
        assert len(alerts) == (1 if path == DECISION else 0), f"{path.name}: alerts {alerts}"
        assert not [line for line in lines if line.lstrip().startswith("|")], f"{path.name} has a table"
        assert not [line for line in lines if re.match(r"^\s*[-*] \[[ xX]\]", line)], f"{path.name} has a checkbox"


def test_the_ordinary_template_says_nothing_is_decided() -> None:
    text = _ordinary()
    assert "**Your move:** nothing to decide." in text.splitlines()[2]
    assert DECISION_PARTS["what is decided"] not in text


def test_the_template_tells_an_agent_how_to_merge() -> None:
    comments = re.findall(r"<!--(.*?)-->", _decision(), re.S)
    assert len(comments) == 1, "one comment for agents, invisible on the phone"
    comment = comments[0]
    for needed in ("decide(", '"decision"', "--match-head-commit"):
        assert needed in comment, f"the agent's comment lacks {needed!r}"


TOUCH_COMMAND = "python3 scripts/touch_map.py origin/main HEAD"


def test_both_templates_carry_what_it_touches() -> None:
    """Criterion 14 of plans/changes/touch-map/spec.md: one generated section, in its place, naming a script that exists."""
    for path, text, before in (
        (ORDINARY, _ordinary(), "## What changes"),
        (DECISION, _decision(), "## What changes for you"),
    ):
        headings = [line for line in text.splitlines() if line.startswith("## ")]
        assert headings.count("## What it touches") == 1, f"{path.name}: the section must stand once"
        at = headings.index("## What it touches")
        assert headings[at - 1] == before, f"{path.name}: the section follows {before!r}"
        assert headings[at + 1] == "## Where it fits", f"{path.name}: the section precedes 'Where it fits'"
        section = [
            line for line in text.split("## What it touches\n", 1)[1].split("\n## ", 1)[0].splitlines() if line.strip()
        ]
        assert len(section) == 2, (
            f"{path.name}: nothing but the placeholder and the optional line belongs in the section"
        )
        assert TOUCH_COMMAND in section[0], f"{path.name}: the section names the command"
        assert "Architecture delta:" in section[1] and "plans/changes/<name>/design.md" in section[1], path.name
    assert (REPO / "scripts" / "touch_map.py").is_file(), "the templates name a script that is not there"
