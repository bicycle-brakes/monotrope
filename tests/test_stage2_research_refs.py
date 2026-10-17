"""Structural frozen-source lookup, independent of model dispatch and live files."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


def resolve(path, text, reference):
    import stage2_research_refs as refs

    return refs.resolve_research_reference({path: text.encode()}, path, reference)


@pytest.mark.parametrize(
    "text",
    [
        "The heading appears in prose.\n",
        "```md\n## Heading\n```\n",
        "---\n# Heading\n---\n",
        "    ## Heading\n",
        "Heading\n=======\n",
        "## Heading\n\n## Heading\n",
    ],
)
def test_reference_markdown_rejects_nonstructural_or_ambiguous_heading(text):
    assert not resolve("a.md", text, "Heading")["supported"]


def test_reference_markdown_extent_ignores_frontmatter_fences_and_lower_headings():
    text = "---\n# Target\n---\n# Intro\n## Target ##\nbody\n```\n## Target\n```\n### Child\nchild\n## Next\nend\n"
    result = resolve("a.md", text, "Target")
    assert result["supported"]
    assert result["start_line"] == 5 and result["end_line"] == 11
    assert result["excerpt"] == "## Target ##\nbody\n```\n## Target\n```\n### Child\nchild\n"


@pytest.mark.parametrize("opening,closing", [("~~~", "~~~~"), ("````", "```"), (" ```", "  ```")])
def test_reference_markdown_fence_length_and_indentation(opening, closing):
    text = f"{opening}\n## Heading\n{closing}\n## Real\nbody\n"
    assert not resolve("a.md", text, "Heading")["supported"]
    assert resolve("a.md", text, "Real")["supported"] == (len(closing.strip()) >= len(opening.strip()))


def test_reference_criterion_selects_one_item_and_ignores_fenced_items():
    text = "## Acceptance criteria\n1. first\n   evidence\n```\n2. fake\n```\n2. second\n## Notes\n"
    result = resolve("a.md", text, "criterion 1")
    assert result["supported"]
    assert result["excerpt"] == "1. first\n   evidence\n```\n2. fake\n```\n"
    assert resolve("a.md", text, "criterion 2")["excerpt"] == "2. second\n"
    assert not resolve("a.md", text.replace("2. second", "1. duplicate"), "criterion 1")["supported"]
    assert not resolve("a.md", "```\n## Acceptance criteria\n1. fake\n```\n", "criterion 1")["supported"]


def test_reference_heading_keeps_inline_formatting_and_case():
    text = "## The `criterion` ledger ###\nbody\n"
    assert resolve("a.md", text, "The `criterion` ledger")["supported"]
    assert not resolve("a.md", text, "The criterion ledger")["supported"]
    assert not resolve("a.md", text, "the `criterion` ledger")["supported"]


@pytest.mark.parametrize(
    "reference,excerpt",
    [
        (
            "Outer",
            "class Outer:\n    async def run(self):\n        def inner():\n            return 1\n        return inner()\n",
        ),
        ("Outer.run", "    async def run(self):\n        def inner():\n            return 1\n        return inner()\n"),
        ("Outer.run.inner", "        def inner():\n            return 1\n"),
        ("VALUE", "VALUE: int = 2\n"),
    ],
)
def test_reference_python_uses_ast_definition_extent(reference, excerpt):
    text = "VALUE: int = 2\nclass Outer:\n    async def run(self):\n        def inner():\n            return 1\n        return inner()\n"
    result = resolve("a.py", text, reference)
    assert result["supported"] and result["excerpt"] == excerpt


@pytest.mark.parametrize(
    "text",
    [
        "# def target():\n",
        'message = "target"\n',
        "def target():\n    pass\ndef target():\n    pass\n",
        "def broken(\n",
    ],
)
def test_reference_python_never_falls_back_to_word_search(text):
    assert not resolve("a.py", text, "target")["supported"]


@pytest.mark.parametrize(
    "path,text,reference,expected",
    [
        ("a.yaml", "adopted:\n  day: 2026-10-08\n", "adopted.day", '"2026-10-08"'),
        ("a.yml", 'a:\n  b: [true, null, "ü"]\n', "a.b", '[\n  true,\n  null,\n  "ü"\n]'),
        ("a.json", '{"a":{"z":2,"ä":"ü","a":1}}', "a", '{\n  "a": 1,\n  "z": 2,\n  "ä": "ü"\n}'),
        (
            "a.yaml",
            "free_focuses:\n  longcat-2.5-preview-free: 9\n",
            "free_focuses",
            '{\n  "longcat-2.5-preview-free": 9\n}',
        ),
    ],
)
def test_reference_mapping_has_exact_canonical_json(path, text, reference, expected):
    result = resolve(path, text, reference)
    assert result["supported"] and result["excerpt"] == expected


@pytest.mark.parametrize(
    "path,text,reference",
    [
        ("a.yaml", "a: [x]\n", "a.0"),
        ("a.yaml", "a:\n  literal.key: 1\n", "a.literal.key"),
        ("a.yaml", "a: 1\na: 2\n", "a"),
        ("a.yaml", "a:\n  1: x\n", "a"),
        ("a.yaml", "a: !!set {x: null}\n", "a"),
        ("a.yaml", "a: !!binary SGVsbG8=\n", "a"),
        ("a.yaml", "a: .nan\n", "a"),
        ("a.json", '{"a":1,"a":2}', "a"),
        ("a.json", '{"a":NaN}', "a"),
        ("a.json", '{"a":Infinity}', "a"),
        ("a.json", "{broken a}", "a"),
    ],
)
def test_reference_mapping_rejects_ambiguous_or_uncitable_values(path, text, reference):
    assert not resolve(path, text, reference)["supported"]


@pytest.mark.parametrize("path", ["Makefile", "script.sh", "config.toml", "script.js"])
def test_reference_other_files_start_at_first_whole_word(path):
    result = resolve(path, "prefixtarget\nfirst target value\nlast target\n", "target")
    assert result["supported"]
    assert result["start_line"] == 2
    assert result["excerpt"] == "first target value\nlast target\n"


def test_reference_claim_has_one_shared_unicode_budget_and_no_partial_support():
    import stage2_research_refs as refs

    sources = {"a.md": ("# A\n" + "ü" * 5000).encode(), "b.py": b"VALUE = 1\n"}
    citations = [{"path": "a.md", "reference": "A"}, {"path": "b.py", "reference": "VALUE"}]
    result = refs.research_claim_evidence(sources, citations)
    assert result["supported"]
    assert sum(len(item["excerpt"]) for item in result["references"]) == 4000
    assert all(item["truncated"] for item in result["references"])
    citations[1]["reference"] = "absent"
    failed = refs.research_claim_evidence(sources, citations)
    assert not failed["supported"]
    assert all("excerpt" not in item for item in failed["references"])


def test_reference_reads_only_frozen_bytes_and_refuses_escape(tmp_path):
    import stage2_research_refs as refs

    (tmp_path / "a.py").write_text("LIVE = 1\n")
    sources = {"a.py": b"FROZEN = 2\n", "../a.py": b"FROZEN = 3\n"}
    assert refs.resolve_research_reference(sources, "a.py", "FROZEN")["supported"]
    assert not refs.resolve_research_reference(sources, "a.py", "LIVE")["supported"]
    assert not refs.resolve_research_reference(sources, "../a.py", "FROZEN")["supported"]


@pytest.mark.parametrize(
    "reference,expected",
    [
        ("LEFT", "LEFT, RIGHT = (1, 2)\n"),
        ("RIGHT", "LEFT, RIGHT = (1, 2)\n"),
        ("FLAG", "    FLAG = True\n"),
        ("conditional", "        def conditional():\n            pass\n"),
    ],
)
def test_reference_python_lexical_scope_includes_conditional_definitions_and_assignments(reference, expected):
    text = "LEFT, RIGHT = (1, 2)\nif True:\n    FLAG = True\nmatch FLAG:\n    case True:\n        def conditional():\n            pass\n"
    result = resolve("a.py", text, reference)
    assert result["supported"] and result["excerpt"] == expected


@pytest.mark.parametrize("citations", [None, {}, [None], [{}], [{"path": "a.py"}]])
def test_reference_malformed_claim_citations_fail_without_exception(citations):
    import stage2_research_refs as refs

    assert not refs.research_claim_evidence({"a.py": b"VALUE = 1\n"}, citations)["supported"]


def test_reference_single_line_identity_is_required():
    assert not resolve("a.sh", "target\n", "target\n")["supported"]


def test_reference_recorded_plan_prompt_extent_uses_exact_structural_title():
    # Verbatim repository blob d862bc2:prompts/03-plan.md; no Git history
    # or live prompt is required to preserve the S-47 counterexample.
    text = (Path(__file__).parent / "fixtures/research_refs/plan-prompt-d862bc2.md").read_text()
    result = resolve("prompts/03-plan.md", text, "The criterion ledger")
    assert result["supported"]
    assert (result["start_line"], result["end_line"]) == (65, 94)
    assert result["excerpt"] == "".join(text.splitlines(keepends=True)[64:94])
    assert not resolve("prompts/03-plan.md", text, "Criterion ledger")["supported"]


def test_reference_json_requires_a_utf8_representable_canonical_excerpt():
    # JSON escape syntax can encode a lone surrogate, which cannot be written
    # into the UTF-8 research artifact or judge packet as unescaped Unicode.
    assert not resolve("a.json", '{"a":"\\ud800"}', "a")["supported"]


@pytest.mark.parametrize(
    "text,reference",
    [
        ("obj.value = 1\n", "obj"),
        ("obj.value: int = 1\n", "obj"),
        ("items[0] = 1\n", "items"),
        ("mapping[key] = 1\n", "key"),
    ],
)
def test_reference_assignment_reads_do_not_define_module_variables(text, reference):
    assert not resolve("a.py", text, reference)["supported"]


def test_reference_augmented_assignment_counts_as_an_ambiguous_rebinding():
    assert not resolve("a.py", "VALUE = 1\nVALUE += 1\n", "VALUE")["supported"]
    result = resolve("a.py", "VALUE += 1\n", "VALUE")
    assert result["supported"] and result["excerpt"] == "VALUE += 1\n"


def test_reference_python_type_alias_has_its_module_assignment_extent():
    result = resolve("a.py", "type Alias = tuple[int, str]\n", "Alias")
    assert result["supported"] and result["excerpt"] == "type Alias = tuple[int, str]\n"
    assert not resolve("a.py", "type Alias = int\ntype Alias = str\n", "Alias")["supported"]
