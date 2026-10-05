"""The three templates: a spec, a findings file, an architecture decision record.

Criteria 1-29 of plans/changes/template-bundle/spec.md. A template is a form to
copy, so the tests hold it against what reads its copies: the gate modules
(`plans_registry`, `check_frontmatter_current`, `check_adr_answers`, read by
attribute at call time, so a constant changed in a test reaches the check),
`decisions/gates.yaml`, and the workflow texts that name a template. Three
counter-probes plant the fault a check must catch. A case that reads a file the
kit does not carry (`AGENTS.md`) skips where that file is absent.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = REPO_ROOT / "templates"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import check_adr_answers as adr_answers  # noqa: E402
import check_frontmatter_current as frontmatter_current  # noqa: E402
import plans_registry  # noqa: E402

NAMES = ("spec.md", "findings.md", "adr.md")
WORKFLOW_TEXTS = [
    "AGENTS.md",
    "docs/WORKFLOW.md",
    *sorted(p.relative_to(REPO_ROOT).as_posix() for p in (REPO_ROOT / "prompts").glob("*.md")),
]
MARKINGS = ("[FLASH]", "[GLM5.3]", "[SONNET]", "plan-marking", "Model markings")
VERIFY_LINE = "- `verify` green."
CHANGE = "filled-change"


# --- reading a template -------------------------------------------------------


def read(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


def split_fences(text: str) -> tuple[list[str], list[tuple[str, str]]]:
    """The lines outside fenced blocks, and the blocks as (info string, body)."""
    outside: list[str] = []
    blocks: list[tuple[str, str]] = []
    info: str | None = None
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith("```"):
            if info is None:
                info, body = line[3:].strip(), []
            else:
                blocks.append((info, "\n".join(body)))
                info = None
        elif info is None:
            outside.append(line)
        else:
            body.append(line)
    return outside, blocks


def prose(name: str) -> list[str]:
    """The template's lines outside its leading comment and outside fences."""
    return split_fences(re.sub(r"<!--.*?-->", "", read(name), count=1, flags=re.S))[0]


def headings(name: str, prefix: str = "## ") -> list[str]:
    return [line[len(prefix) :] for line in prose(name) if line.startswith(prefix)]


def section(name: str, title: str) -> str:
    lines = prose(name)
    start = lines.index(f"## {title}") + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end])


def flat(text: str) -> str:
    return " ".join(text.split())


def example_header(name: str) -> str:
    return next(body for info, body in split_fences(read(name))[1] if info == "yaml")


def fill(header: str, change: str = CHANGE) -> str:
    """The example header with its placeholders replaced as the plan says."""
    for placeholder, value in (
        ("<YYYY-MM-DD>", "2026-09-30"),
        ("<hours>", "3"),
        ("<yes|no>", "no"),
        ("<change>", change),
    ):
        header = header.replace(placeholder, value)
    return re.sub(r"<[^<>\n]+>", "Filled", header)


def header_problems(name: str, root: Path, *, answers: bool) -> list[str]:
    """What the gates say about the filled-in example header, placed as a file under `plans/changes/`."""
    text = f"---\n{fill(example_header(name))}\n---\n\n# Body\n"
    path = root / "plans" / "changes" / CHANGE / ("spec.md" if answers else "findings.md")
    path.parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")
    meta = plans_registry._frontmatter(path)
    if meta is None:
        return ["no readable header"]
    problems = []
    for key in plans_registry.REQUIRED:
        if key not in meta:
            problems.append(f"{key} is missing")
        elif meta[key] in (None, ""):
            problems.append(f"{key} is empty")
    if meta.get("status") not in plans_registry.STATUS:
        problems.append(f"status {meta.get('status')!r} is refused")
    if meta.get("implementation_status") not in plans_registry.IMPLEMENTATION:
        problems.append(f"implementation_status {meta.get('implementation_status')!r} is refused")
    if not isinstance(frontmatter_current.read_updated(text), date):
        problems.append("no date from read_updated")
    if answers:
        wanted = f"adr-answers: {CHANGE}: no answer"
        lines = adr_answers.examine(root).lines()
        problems += [line for line in lines if not line.startswith(wanted)]
        if not any(line.startswith(wanted) for line in lines):
            problems.append("the header is not read as a feature that owes its answer")
    return problems


def done_problems(done: str) -> list[str]:
    """The Definition of Done's faults: the gate line not exactly once, a gate id on any other line."""
    gates = yaml.safe_load((REPO_ROOT / "decisions" / "gates.yaml").read_text(encoding="utf-8"))["gates"]
    lines = done.splitlines()
    problems = [] if lines.count(VERIFY_LINE) == 1 else [f"{VERIFY_LINE!r} is not there exactly once"]
    for line in lines:
        for gate in (g["id"] for g in gates):
            if line != VERIFY_LINE and re.search(rf"(?<![\w-]){re.escape(gate)}(?![\w-])", line):
                problems.append(f"gate {gate} named in {line!r}")
    return problems


def missing_template_paths(text: str, root: Path = REPO_ROOT) -> list[str]:
    return sorted({p for p in re.findall(r"templates/[\w./-]*\w", text) if not (root / p).is_file()})


def workflow_text(path: str) -> str:
    if not (REPO_ROOT / path).is_file():
        pytest.skip(f"{path} does not travel with the kit")
    return (REPO_ROOT / path).read_text(encoding="utf-8")


# --- all three -----------------------------------------------------------------


@pytest.mark.parametrize("name", NAMES)
def test_templates_carry_no_real_header(name: str) -> None:
    assert not read(name).lstrip().startswith("---"), "provenance.yaml: templates/ has frontmatter: none"


# --- the spec template (criteria 1-12) ------------------------------------------


def test_spec_sections_in_order() -> None:
    expected = [
        "Problem",
        "Terms",
        "Acceptance criteria",
        "Non-goals",
        "Protected areas",
        "Definition of Done",
        "Open decisions",
    ]
    assert headings("spec.md") == expected
    assert "optional" in section("spec.md", "Terms").lower()


def test_spec_opens_with_the_goal() -> None:
    lines = prose("spec.md")
    body = "\n".join(lines[next(i for i, line in enumerate(lines) if line.startswith("# ")) + 1 :])
    first = flat(body.strip().split("\n\n", 1)[0])
    assert "goal" in first and "research.md" in first and "decisions.md" in first


def test_filled_spec_header_passes_the_gates(tmp_path: Path) -> None:
    assert header_problems("spec.md", tmp_path, answers=True) == []


def test_header_check_sees_a_new_required_field(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(plans_registry, "REQUIRED", (*plans_registry.REQUIRED, "planted_field"))
    assert "planted_field is missing" in header_problems("spec.md", tmp_path, answers=True)


def test_class_line_offers_the_four_classes() -> None:
    line = next(line for line in example_header("spec.md").splitlines() if line.startswith("class:"))
    value, comment = line[len("class:") :].split("#", 1)
    assert value.strip() in adr_answers.CLASSES
    assert {name.strip() for name in comment.split("|")} == set(adr_answers.CLASSES)


def test_appetite_is_a_placeholder_for_phase_4_hours() -> None:
    line = next(line for line in example_header("spec.md").splitlines() if line.startswith("appetite:"))
    raw = line[len("appetite:") :].split("#", 1)[0].strip()
    assert not isinstance(yaml.safe_load(raw), int | float), "the template sets a default appetite"
    assert "phase 4" in line
    filled = yaml.safe_load(fill(example_header("spec.md")))["appetite"]
    assert isinstance(filled, int | float) and not isinstance(filled, bool) and filled > 0


def test_failure_mode_lives_in_the_refutations() -> None:
    assert not [h for h in headings("spec.md", "#") if "failure mode" in h.lower()]
    criteria = section("spec.md", "Acceptance criteria").lower()
    assert "failure mode" in criteria and "refuted by" in criteria


def test_example_criterion_has_condition_and_refutation() -> None:
    lines = section("spec.md", "Acceptance criteria").splitlines()
    i = next(i for i, line in enumerate(lines) if line.startswith("1. "))
    assert re.match(r"1\. (When|While|If) ", lines[i]) and re.match(r"\s+\*Refuted by:\*", lines[i + 1])


def test_criterion_form_is_a_recommendation() -> None:
    paragraphs = [flat(p) for p in section("spec.md", "Acceptance criteria").split("\n\n")]
    paragraph = next(p for p in paragraphs if "When, While or If" in p)
    assert "`prompts/02-spec.md`" in paragraph and "#60" in paragraph


def test_protected_areas_ask_what_must_not_be_touched() -> None:
    text = flat(section("spec.md", "Protected areas"))
    assert "must not touch" in text and "reason" in text and "None beyond the non-goals." in text


def test_done_names_the_gates_in_one_line() -> None:
    assert done_problems(section("spec.md", "Definition of Done")) == []


def test_done_check_catches_a_planted_gate() -> None:
    planted = section("spec.md", "Definition of Done") + "\n- `pytest` green.\n"
    assert any("gate pytest" in problem for problem in done_problems(planted))


def test_done_asks_the_change_specific_items() -> None:
    text = flat(section("spec.md", "Definition of Done")).lower()
    for key in ("same pull request", "protected areas", "non-goals", "closes-bead", "special runs"):
        assert key in text, key


def test_spec_prompt_names_the_template() -> None:
    assert "templates/spec.md" in workflow_text("prompts/02-spec.md")


# --- the findings template (criteria 13-18) --------------------------------------


def test_findings_table_has_the_practised_columns() -> None:
    first = next(line for line in prose("findings.md") if line.startswith("|"))
    assert [cell.strip() for cell in first.strip("|").split("|")] == [
        "ID",
        "Severity",
        "Dimension",
        "Origin",
        "Where",
        "Finding",
        "Status",
    ]


def test_findings_vocabulary_is_here() -> None:
    text = flat(read("findings.md"))
    for term in (
        "BLOCKER",
        "MAJOR",
        "MINOR",
        "SPEC",
        "MAINT",
        "base",
        "fix-r<N>",
        "escalation",
        "[AMBIGUITY]",
        "[DIVERGENT]",
    ):
        assert term in text, term
    assert "new evidence" in text
    assert any("[DIVERGENT]" in line and "BLOCKER" in line for line in read("findings.md").splitlines())


def test_status_values_include_the_spec_review_ones() -> None:
    text = read("findings.md")
    assert "`in spec`" in text and "`rejected — <reason>`" in text


def test_lines_under_the_table() -> None:
    text = read("findings.md")
    assert text.index("Reviewer session: `<id>`") > text.index("| ID |")
    assert {"Checked without a finding", "Not checked"} <= set(headings("findings.md"))


def test_filled_findings_header_passes_the_plans_gates(tmp_path: Path) -> None:
    assert header_problems("findings.md", tmp_path, answers=False) == []


# --- the decision-record template (criteria 19-24) -------------------------------


def test_adr_sections_in_order() -> None:
    assert headings("adr.md") == [
        "Context",
        "Decision Drivers",
        "Considered Options",
        "Decision",
        "Consequences",
        "Validation",
    ]


def test_adr_names_madr_and_maps_the_names() -> None:
    text = flat(read("adr.md"))
    for needed in (
        "MADR 4.0.0",
        "https://github.com/adr/madr",
        "Context — Context and Problem Statement",
        "Decision — Decision Outcome",
        "Validation — Confirmation",
    ):
        assert needed in text, needed


def test_adr_takes_effect_by_the_merge() -> None:
    text = flat(read("adr.md"))
    for needed in (
        "accepted by the merge of the pull request that carries this file",
        "open is proposed",
        "closed is rejected.",
    ):
        assert needed in text, needed


def test_adr_names_the_decision_pull_request() -> None:
    text = flat(read("adr.md"))
    assert (
        "decide(<scope>)" in text and "label `decision`" in text and ".github/PULL_REQUEST_TEMPLATE/decision.md" in text
    )


def test_adr_names_what_moves_with_an_amendment() -> None:
    text = flat(read("adr.md"))
    assert '"Amend" row' in text and "Decision continuity" in text and "AMENDMENT_ADRS" in text


def test_adr_header_has_the_fields_of_the_adrs() -> None:
    meta = yaml.safe_load(fill(example_header("adr.md")))
    fields = "title category status created last_reviewed updated owner provenance produced_by review tags".split()
    assert [f for f in fields if f not in meta] == []
    assert meta["category"] == "adr" and meta["provenance"] == "human-decided"


# --- plan markings retired, links whole (criteria 25-28) --------------------------


@pytest.mark.parametrize("path", WORKFLOW_TEXTS)
def test_no_workflow_text_names_a_missing_template(path: str) -> None:
    assert missing_template_paths(workflow_text(path)) == []


def test_path_check_catches_a_planted_path() -> None:
    assert missing_template_paths("named here: `templates/missing.md`.") == ["templates/missing.md"]


@pytest.mark.parametrize("path", WORKFLOW_TEXTS)
def test_no_workflow_text_asks_for_a_marking(path: str) -> None:
    text = workflow_text(path)
    assert [m for m in MARKINGS if m in text] == []


def test_the_marking_template_is_gone() -> None:
    assert not (TEMPLATES / "plan-marking.md").exists()


def test_workflow_note_names_neither_template() -> None:
    text = workflow_text("docs/WORKFLOW.md")
    note = text.split("Not all of it is here yet", 1)[1].split("One thing is missing", 1)[0]
    assert "templates/findings.md" not in note and "templates/plan-marking.md" not in note
