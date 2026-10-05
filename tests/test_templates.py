"""The templates and the design phase: a spec, a findings file, a decision record, a design.

Criteria 1-62 of plans/changes/template-bundle/spec.md, criterion 47 in part;
criteria 55 and 63-65 are held by review or by a command, not here (`plan.md`,
"Tests and checks per criterion"). A template is a form to copy, so the tests
hold it against what reads its copies: the gate modules
(`plans_registry`, `check_frontmatter_current`, `check_adr_answers`, read by
attribute at call time, so a constant changed in a test reaches the check),
`decisions/gates.yaml`, and the workflow texts that name a template or the
design phase. Counter-probes plant the fault a check must catch. A case that
reads a file the kit does not carry (`AGENTS.md`) skips where that file is
absent.
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

NAMES = ("spec.md", "findings.md", "adr.md", "design.md", "arc42.md")
DESIGN_PROMPT = "prompts/02b-design.md"
WORKFLOW_TEXTS = [
    "AGENTS.md",
    "docs/WORKFLOW.md",
    *sorted(p.relative_to(REPO_ROOT).as_posix() for p in (REPO_ROOT / "prompts").glob("*.md")),
]
MARKINGS = ("[FLASH]", "[GLM5.3]", "[SONNET]", "plan-marking", "Model markings")
VERIFY_LINE = "- `verify` green."
CHANGE = "filled-change"
ARC42_SECTIONS = (
    "Introduction and Goals",
    "Architecture Constraints",
    "Context and Scope",
    "Solution Strategy",
    "Building Block View",
    "Runtime View",
    "Deployment View",
    "Cross-cutting Concepts",
    "Architecture Decisions",
    "Quality Requirements",
    "Risks and Technical Debts",
    "Glossary",
)
# The regex of `tests/test_model_endpoints.py::prompt_modelle`, copied: importing that module runs its reads.
MODEL_LINE = re.compile(r"^\*\*(?:Modell|Model):\*\*\s*([^\n—]+?)\s*(?:—|\.\s*$|$)", re.M)
# What decision D-14 asks of a class, as words the prompt's line for that class must hold.
D14_WORDS = {
    "architectural": ("always",),
    "feature": ("spec.md", "one sentence"),
    "bounded": ("never",),
    "spike": ("never",),
}
# ... and the words that contradict it.
D14_NOT = {"architectural": ("never",), "bounded": ("always",), "spike": ("always",)}
C4_LEVELS = ("person", "system", "container", "component")
# A box of a Mermaid flowchart: its id, then the shape's opening and the label, quoted or bare.
NODE = re.compile(
    r'\b(?P<id>[A-Za-z_]\w*)\s*(?:\[\[|\[\(|\(\(|\{\{|\[|\(|\{|>)\s*(?:"(?P<quoted>[^"]*)"|(?P<bare>[^\]\)\}"]*))'
)
MERMAID_KEYWORDS = ("%%", "subgraph", "end", "classDef", "class ", "style", "linkStyle", "click", "direction")


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


def reference_lists(name: str) -> dict[str, dict[str, str]]:
    """The reference part below the template's `---` line: bold label -> {term in code ticks -> its definition}."""
    lines = prose(name)
    groups: dict[str, dict[str, str]] = {}
    label = term = None
    for line in lines[lines.index("---") + 1 :]:
        if bold := re.match(r"\*\*(.+?)\*\*", line):
            label, term = bold.group(1), None
            groups[label] = {}
        elif label and (entry := re.match(r"- `(.+?)` — (.*)", line)):
            term = entry.group(1)
            groups[label][term] = entry.group(2)
        elif label and term and line.startswith("  "):
            groups[label][term] += " " + line.strip()
    return groups


def flat(text: str) -> str:
    return " ".join(text.split())


def raw_section(name: str, title: str) -> str:
    """One section's text with its fenced blocks, after the template's leading comment."""
    lines = re.sub(r"<!--.*?-->", "", read(name), count=1, flags=re.S).splitlines()
    start = lines.index(f"## {title}") + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end])


def lead(name: str) -> str:
    """The text before a template's first `## `, outside its leading comment and its fences."""
    lines = prose(name)
    return "\n".join(lines[: next((i for i, line in enumerate(lines) if line.startswith("## ")), len(lines))])


def markdown_section(text: str, heading: str) -> str:
    """The text under the heading that begins with `heading`, up to the next heading of its level or a higher one."""
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if re.match(r"#+ ", line) and line.lstrip("# ").startswith(heading))
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    end = next((i for i in range(start + 1, len(lines)) if re.match(rf"#{{1,{level}}} ", lines[i])), len(lines))
    return "\n".join(lines[start + 1 : end])


def first_table(text: str) -> list[list[str]]:
    """The rows of the first table in the text, each as its cells; the header and the rule row are left out."""
    rows: list[list[str]] = []
    for line in text.splitlines():
        if line.startswith("|"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
        elif rows:
            break
    return rows[2:]


def prompt_model(text: str) -> str:
    found = MODEL_LINE.search(text)
    assert found, "the prompt has no **Model:** line"
    return found.group(1).strip()


def d14_problems(text: str, *, clauses: bool = False) -> list[str]:
    """For each class of `CLASSES`, read at call time: what the text says of it, and whether its words hold.

    The prompt says it in one list line that begins with the class; the doctrine says it in one sentence, so with
    `clauses` the unit is the part of that sentence, between `;` and the end of a sentence, that names the class.
    """
    problems = []
    for name in adr_answers.CLASSES:
        if clauses:
            units = [flat(c) for c in re.split(r";|\.(?=\s|$)", flat(text)) if f"`{name}`" in c]
        else:
            units = [flat(line) for line in text.splitlines() if line.startswith(f"- `{name}`")]
        if not units:
            problems.append(f"no line for {name}")
            continue
        problems += [f"{name}: {word!r} is missing" for word in D14_WORDS.get(name, ()) if word not in units[0]]
        problems += [f"{name}: {word!r} contradicts it" for word in D14_NOT.get(name, ()) if word in units[0]]
    return problems


def c4_problems(diagram: str) -> list[str]:
    """Every box of a Mermaid flowchart: it is defined with a label that begins `<C4 level>:`.

    A box counts where it is defined (`id["Level: text"]`, any shape) or only named in an edge (`a --> b`); the
    header line, comments and the lines of subgraphs and styles are not read. Edge labels stand between `|`.
    """
    defined: dict[str, str] = {}
    named: set[str] = set()
    for line in diagram.splitlines()[1:]:
        if not line.strip() or line.strip().startswith(MERMAID_KEYWORDS):
            continue
        for node in NODE.finditer(line):
            label = node["quoted"] if node["quoted"] is not None else node["bare"]
            defined.setdefault(node["id"], label.strip())
        rest = re.sub(r"\|[^|]*\|", " ", NODE.sub(lambda m: m["id"], line))
        named |= set(re.findall(r"[A-Za-z_]\w*", re.sub(r"[-=.]{2,}[>ox]?", " ", rest)))
    if not defined:
        return ["no box with a label"]
    problems = []
    for box in sorted(named | set(defined)):
        label = defined.get(box)
        level = re.match(r"(\w+):", label or "")
        if label is None:
            problems.append(f"{box}: no label, so no C4 level")
        elif not level or level.group(1).lower() not in C4_LEVELS:
            problems.append(f"{box}: {label!r} does not begin with one of {C4_LEVELS}")
    return problems


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


def header_problems(name: str, root: Path, *, answers: bool, placed_as: str = "findings.md") -> list[str]:
    """What the gates say about the filled-in example header, placed as a file under `plans/changes/`."""
    text = f"---\n{fill(example_header(name))}\n---\n\n# Body\n"
    path = root / "plans" / "changes" / CHANGE / ("spec.md" if answers else placed_as)
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


def d14_doctrine_paragraph() -> str:
    """The paragraph of the class section of `docs/WORKFLOW.md` that states D-14, or an empty string."""
    text = markdown_section(
        workflow_text("docs/WORKFLOW.md"), "Change classes, the ADR question and decision pull requests"
    )
    wanted = ("02b-design.md", "coding-harness-jc3", *(f"`{name}`" for name in adr_answers.CLASSES))
    return next((p for p in text.split("\n\n") if all(word in flat(p) for word in wanted)), "")


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
    # `main`'s prompt 02 has no rule of one condition per criterion: it appears only inside the recommendation
    whole = " ".join(paragraphs)
    for mention in re.finditer("one condition", whole, re.I):
        assert re.match(r"[^.]*recommended", whole[mention.start() :]), "one condition per criterion is a bare rule"


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
    """Each term is defined by its own entry in its own list of the reference part, not named somewhere in the file."""
    lists = reference_lists("findings.md")
    for label, terms in (
        ("Severity", ("BLOCKER", "MAJOR", "MINOR")),
        ("Dimension", ("SPEC", "MAINT")),
        ("Origin", ("base", "fix-r<N>")),
        ("Markers that override everything", ("[AMBIGUITY]", "[DIVERGENT]")),
    ):
        for term in terms:
            assert lists.get(label, {}).get(term, "").strip(), f"{label}: no definition of {term}"
    assert "escalation" in lists["Origin"]["fix-r<N>"]
    assert "BLOCKER" in lists["Markers that override everything"]["[DIVERGENT]"]
    lines = prose("findings.md")
    assert "new evidence" in flat("\n".join(lines[lines.index("---") :]))


def test_status_values_include_the_spec_review_ones() -> None:
    """The two values prompt 02 prescribes stand in the Status list, not merely somewhere in the template."""
    status = reference_lists("findings.md").get("Status", {})
    for value in ("in spec", "rejected — <reason>"):
        assert status.get(value, "").strip(), f"the Status list has no entry for {value}"


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


# --- the design phase (criteria 33-38) ---------------------------------------------


def test_design_prompt_names_the_template() -> None:
    assert "templates/design.md" in workflow_text(DESIGN_PROMPT)


def test_design_prompt_states_d14_for_each_class() -> None:
    assert d14_problems(workflow_text(DESIGN_PROMPT)) == []


def test_d14_check_sees_a_new_class(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(adr_answers, "CLASSES", (*adr_answers.CLASSES, "planted"))
    assert "no line for planted" in d14_problems(workflow_text(DESIGN_PROMPT))
    assert "no line for planted" in d14_problems(d14_doctrine_paragraph(), clauses=True)


def test_d14_check_sees_a_contradiction() -> None:
    sentence = (
        "an `architectural` change never runs it; a `feature` runs it or says in one sentence of `spec.md` why not"
    )
    problems = d14_problems(sentence, clauses=True)
    assert "architectural: 'always' is missing" in problems
    assert "architectural: 'never' contradicts it" in problems
    assert not [problem for problem in problems if problem.startswith("feature")]


def test_design_prompt_says_nothing_checks_the_rule_yet() -> None:
    assert "coding-harness-jc3" in workflow_text(DESIGN_PROMPT)


def test_design_prompt_says_where_the_adr_draft_goes() -> None:
    text = flat(workflow_text(DESIGN_PROMPT))
    assert "docs/adr/" in text and "decision pull request" in text


def test_design_prompt_hands_the_design_to_the_plan() -> None:
    paragraphs = [flat(p) for p in workflow_text(DESIGN_PROMPT).split("\n\n")]
    assert any(all(word in p for word in ("Phase 3", "design.md", "plan.md", "phase 4")) for p in paragraphs)


# --- the design template (criteria 39-48) -------------------------------------------


def test_design_sections_in_order() -> None:
    assert headings("design.md") == ["Alternatives", "Interfaces", "Data model", "ADR draft", "Architecture delta"]


def test_alternatives_ask_for_two_with_consequences_and_a_choice() -> None:
    text = flat(section("design.md", "Alternatives"))
    assert "at least two" in text.lower() and "consequence" in text.lower() and "Chosen" in text


@pytest.mark.parametrize("title", ["Interfaces", "Data model", "ADR draft"])
def test_empty_parts_say_why(title: str) -> None:
    assert any(line.startswith("None — ") for line in section("design.md", title).splitlines())


def test_adr_draft_takes_the_record_form() -> None:
    text = flat(section("design.md", "ADR draft"))
    assert "templates/adr.md" in text and "architectural" in text


@pytest.mark.parametrize("path", ["templates/design.md", DESIGN_PROMPT])
def test_adr_draft_is_owed_when_proposed_or_answered_yes(path: str) -> None:
    """At phase 2b the maintainer has often not answered yet, so the spec's proposal counts as well."""
    pattern = r'proposes "yes" to the ADR question or (?:the maintainer has answered|whose answer is) "yes"'
    assert re.search(pattern, flat(workflow_text(path)))


def test_delta_is_a_mermaid_flowchart_after_the_change() -> None:
    outside, blocks = split_fences(raw_section("design.md", "Architecture delta"))
    diagrams = [body for info, body in blocks if info == "mermaid"]
    assert diagrams, "no mermaid block in the Architecture delta section"
    assert diagrams[0].split()[0] == "flowchart"
    assert "after the change" in flat("\n".join(outside))


@pytest.mark.parametrize("path", ["templates/design.md", DESIGN_PROMPT])
def test_no_likec4_model_is_asked(path: str) -> None:
    text = workflow_text(path).lower()
    assert "likec4" not in text and ".c4" not in text


def test_delta_lists_below_the_diagram() -> None:
    after = raw_section("design.md", "Architecture delta").split("```mermaid", 1)[1].split("```", 1)[1]
    places = [after.find(f"**{label}**") for label in ("Added", "Changed", "Removed")]
    assert -1 not in places and places == sorted(places)


def test_delta_says_why_when_nothing_moves() -> None:
    assert "nothing architectural moves" in flat(section("design.md", "Architecture delta")).lower()


def test_delta_names_adr_0009() -> None:
    assert "ADR 0009" in flat(section("design.md", "Architecture delta"))


def test_delta_names_elements_as_the_existing_diagrams_do() -> None:
    """ADR 0009's second contract: elements are named as the existing diagrams and ADRs name them."""
    assert "as the existing diagrams and ADRs name them" in flat(section("design.md", "Architecture delta"))


def test_delta_asks_for_the_c4_level_of_each_box() -> None:
    """ADR 0009: each box of the diagram is labelled with its C4 level."""
    levels = ("person", "system", "container", "component")
    raw = raw_section("design.md", "Architecture delta")
    outside, blocks = split_fences(raw)
    text = flat("\n".join(outside)).lower()
    assert "c4 level" in text and all(level in text for level in levels)
    assert c4_problems(next(body for info, body in blocks if info == "mermaid")) == []


@pytest.mark.parametrize(
    "diagram",
    [
        'flowchart LR\n    app["what changes"]',
        'flowchart LR\n    person["Person: who"] --> app["Container: what"]\n    app --> store[("the store")]',
        'flowchart LR\n    person["Person: who"] --> app',
        'flowchart LR\n    person["Actor: who"]',
        "flowchart LR\n    person[Person who]",
        "flowchart LR",
    ],
)
def test_c4_check_sees_a_box_without_a_level(diagram: str) -> None:
    assert c4_problems(diagram) != []


@pytest.mark.parametrize(
    "diagram",
    [
        'flowchart LR\n    a["Person: who"] -->|calls| b["Container: what (Python)"]',
        'flowchart TB\n    a("System: other") -.-> b[("Component: the store")]\n    b --- c{{"Container: x"}}',
    ],
)
def test_c4_check_lets_a_labelled_diagram_pass(diagram: str) -> None:
    assert c4_problems(diagram) == []


def test_filled_design_header_passes_the_plans_gates(tmp_path: Path) -> None:
    assert header_problems("design.md", tmp_path, answers=False, placed_as="design.md") == []


# --- the design phase in the doctrine (criteria 49-53) ---------------------------------


def test_phase_table_has_2b_between_2a_and_3() -> None:
    rows = first_table(markdown_section(workflow_text("docs/WORKFLOW.md"), "2 · The phases"))
    firsts = [row[0] for row in rows]
    assert any(firsts[i : i + 3] == ["2a", "2b", "3"] for i in range(len(firsts))), firsts
    row = rows[firsts.index("2b")]
    assert "design.md" in row[2] and "prompts/02b-design.md" in row[-1]


def test_routing_gives_2b_the_prompt_model() -> None:
    rows = first_table(markdown_section(workflow_text("docs/WORKFLOW.md"), "Model routing"))
    firsts = [row[0].split()[0] for row in rows]
    assert any(firsts[i : i + 3] == ["2a", "2b", "3"] for i in range(len(firsts))), firsts
    bold = re.search(r"\*\*(.+?)\*\*", rows[firsts.index("2b")][1])
    assert bold and bold.group(1) == prompt_model(workflow_text(DESIGN_PROMPT))


def test_agents_table_has_2b_between_2a_and_3() -> None:
    rows = first_table(markdown_section(workflow_text("AGENTS.md"), "The workflow in one screen"))
    firsts = [row[0] for row in rows]
    assert any(firsts[i : i + 3] == ["2a", "2b", "3"] for i in range(len(firsts))), firsts
    assert "design.md" in rows[firsts.index("2b")][2]


def test_workflow_states_d14_by_class() -> None:
    paragraph = d14_doctrine_paragraph()
    assert paragraph, "no paragraph names 02b-design.md, coding-harness-jc3 and the four classes"
    assert d14_problems(paragraph, clauses=True) == []


def test_spec_template_says_where_a_feature_skips_design() -> None:
    text = flat(section("spec.md", "Non-goals"))
    assert "design.md" in text and "feature" in text and "one sentence" in text


# --- the arc42 skeleton (criteria 54-60) ------------------------------------------------


def credit_part(name: str) -> str:
    """What a copy keeps: the template without its leading comment and without its example header."""
    return flat(re.sub(r"<!--.*?-->", "", read(name), count=1, flags=re.S))


def test_arc42_has_the_twelve_sections_in_order() -> None:
    found = [re.fullmatch(r"(\d+)\. (.+)", title) for title in headings("arc42.md")]
    assert all(found), headings("arc42.md")
    assert [m.group(2) for m in found if m] == list(ARC42_SECTIONS)
    assert [int(m.group(1)) for m in found if m] == list(range(1, len(ARC42_SECTIONS) + 1))


def test_arc42_credits_arc42_in_the_copied_part() -> None:
    text = credit_part("arc42.md")
    for needed in (
        "arc42",
        "9.0",
        "July 2025",
        "Gernot Starke",
        "Peter Hruschka",
        "© Dr. Peter Hruschka, Dr. Gernot Starke and contributors",
        "https://arc42.org",
        "https://creativecommons.org/licenses/by-sa/4.0/",
        "changed",
    ):
        assert needed in text, needed


def test_arc42_states_its_licence() -> None:
    text = credit_part("arc42.md")
    assert "adaptation of arc42 under CC BY-SA 4.0" in text
    assert re.search(r"written into a copy[^.]*stays its author's", text)


def test_arc42_asks_only_what_a_reader_needs() -> None:
    """The three things the opening asks, each in a paragraph of its own words (a word elsewhere does not count)."""
    paragraphs = [flat(p).lower() for p in lead("arc42.md").split("\n\n")]
    items = (
        ("named reader", "one line", "nothing"),
        ("every number", "commit or date"),
        ("not known", "marked open"),
    )
    for words in items:
        assert any(all(word in p for word in words) for p in paragraphs), words


def test_arc42_decisions_point_to_the_records() -> None:
    assert "docs/adr/" in section("arc42.md", "9. Architecture Decisions")


def test_filled_arc42_header_gives_a_date() -> None:
    text = f"---\n{fill(example_header('arc42.md'))}\n---\n\n# Body\n"
    assert isinstance(frontmatter_current.read_updated(text), date)
