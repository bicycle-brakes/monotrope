"""The two read-only helpers hold what the workflow promises.

`docs/WORKFLOW.md` §3 promises an explorer and a reviewer as sub-agent
definitions, read-only and with pinned models; the decisions for bead
coding-harness-9ll chose Haiku 5.5 for exploration and Opus 5.5 at high
effort for review. A promise in prose is not a configuration, so this module
parses the two definitions' YAML frontmatter and instruction bodies and
holds them against those decisions: the exact model ids, the reviewer's
effort, exactly the three repository reading tools, and role texts that
report findings instead of writing.

The orchestrator holds the two definitions until the accepted attempt, so
the file checks are red until the install lands. A missing file fails and
never skips: a green result over a missing definition would promise exactly
the helper that does not exist. Before the install this failure is the
expected pre-bootstrap state, not completion.

Counter-checks plant wrong-model, missing-effort, extra-tool,
inherited-tool and changed-role fixtures and run them through the same
assertion helpers as the real files — a helper that no longer rejects the
fixtures holds nothing.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS = REPO_ROOT / ".claude" / "agents"
READ_TOOLS = ("Read", "Grep", "Glob")

# The actions a read-only role must name as prohibited. Every sentence that
# uses one must also carry a cue — a negation, or the attribution to someone
# else (the caller, the orchestrator, a human): "you may repair what you
# find" is exactly the authorization the role must not contain.
SHARED_ACTIONS = (
    (r"repair", "repairs"),
    (r"commit", "commits"),
    (r"tracker", "tracker writes"),
    (r"accept", "accepting its own work"),
)
ACTIONS = {
    "explorer": SHARED_ACTIONS + ((r"writ", "writes"),),
    "reviewer": SHARED_ACTIONS,
}
CUE = re.compile(
    r"\b(never|not|no|without|avoid|neither|nor)\b",
    re.IGNORECASE,
)
# Naming another actor is not attribution: "when the caller asks, you commit"
# still grants permission. Accept only an explicit handoff or ownership clause.
ATTRIBUTION = re.compile(
    r"(?:leave\b.+\bto|[\w ,'-]+\b(?:belong(?:s)? to|stay(?:s)? with|remain(?:s)? with))"
    r"\s+(?:the\s+)?(?:caller|orchestrator|human|maintainer)"
    r"|(?:the\s+)?(?:caller|orchestrator|human|maintainer)"
    r"\s+(?:writes?|repairs?|commits?|accepts?)\b[^,;]*",
    re.IGNORECASE,
)
# The reporting concepts each role must state, beside its prohibitions.
CONCEPTS = {
    "explorer": (
        (r"evidence", "source-backed findings"),
        (r"unknown", "explicit unknowns"),
        (r"source", "the sources it read"),
        (r"caller", "reporting to the caller"),
    ),
    "reviewer": (
        (r"\bspec\b", "findings against the supplied spec"),
        (r"evidence", "implementation evidence"),
        (r"findings?", "actionable findings"),
    ),
}


# ---------------------------------------------------------------------------
# The readers and the assertion helpers the counter-checks share
# ---------------------------------------------------------------------------


def _definition(name: str) -> tuple[dict, str]:
    """The definition's frontmatter and body — a missing file fails, never skips."""
    path = AGENTS / f"{name}.md"
    assert path.is_file(), (
        f"{path} is missing. The change holds the two definitions until the accepted "
        "attempt and the orchestrator installs them after it; until then this failure "
        "is the expected pre-bootstrap state. A green check over a missing definition "
        "would promise a helper that does not exist."
    )
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path.name}: the file has no configuration frontmatter"
    end = text.find("\n---", 4)
    assert end != -1, f"{path.name}: the frontmatter is not closed"
    frontmatter = yaml.safe_load(text[4:end]) or {}
    assert isinstance(frontmatter, dict), f"{path.name}: the frontmatter is not a mapping"
    return frontmatter, text[end + 4 :]


def _role_text(body: str) -> str:
    """The instructions without the normative evidence paragraph.

    tests/test_regelwerk.py holds the RB-A1 paragraph byte-identical against
    the rule set; the role checks must not pass on its vocabulary alone. A
    definition without the heading fails here as it fails there.
    """
    marker = body.find("## Evidence contract (RB-A1)")
    assert marker != -1, "the definition does not carry the '## Evidence contract (RB-A1)' heading"
    return body[:marker]


def _assert_model(frontmatter: dict, model_id: str) -> None:
    assert frontmatter.get("model") == model_id, (
        f"model: {frontmatter.get('model')!r}, expected {model_id!r}. Claude Code "
        "selects the sub-agent's model from this field; anything else runs the helper "
        "on the parent's model (docs/WORKFLOW.md §3, 'Check after setup')."
    )


def _assert_effort(frontmatter: dict, effort: str) -> None:
    assert frontmatter.get("effort") == effort, (
        f"effort: {frontmatter.get('effort')!r}, expected {effort!r} — a sub-agent "
        "takes its effort from its definition's frontmatter, not from the call that "
        "starts it"
    )


def _assert_description(frontmatter: dict, name: str) -> None:
    description = frontmatter.get("description")
    assert isinstance(description, str) and description.strip(), (
        f"{name}: the description is missing or empty — Claude Code shows it to the "
        "caller that decides when to start the helper"
    )


def _assert_tools(frontmatter: dict) -> None:
    raw = frontmatter.get("tools")
    assert raw is not None, (
        "tools: the field is missing, so the helper inherits every tool it is started "
        "with — the read-only promise needs the allowlist to name exactly Read, Grep, Glob"
    )
    if isinstance(raw, str):
        tools = [tool.strip() for tool in raw.split(",") if tool.strip()]
    else:
        assert isinstance(raw, list), f"tools: {raw!r} is neither a comma-separated string nor a list"
        tools = [str(tool).strip() for tool in raw if str(tool).strip()]
    assert len(tools) == len(set(tools)), f"tools: a tool is named twice: {tools}"
    assert set(tools) == set(READ_TOOLS), (
        f"tools: {sorted(tools)}, expected exactly {sorted(READ_TOOLS)} — a shell, a "
        "writer, delegation or unrestricted inheritance breaks the read-only promise"
    )


def _role_problems(role: str, kind: str) -> list[str]:
    """What a role text misses of its read-only reporting contract, as the problems found."""
    problems: list[str] = []
    sentences = [sentence.strip() for sentence in re.split(r"[.;\n]", role) if sentence.strip()]
    for term, label in ACTIONS[kind]:
        hits = [sentence for sentence in sentences if re.search(rf"\b{term}", sentence, re.IGNORECASE)]
        if not hits:
            problems.append(f"no sentence states the prohibition on {label}")
            continue
        for sentence in hits:
            if not CUE.search(sentence) and not ATTRIBUTION.fullmatch(sentence):
                problems.append(f"the role text authorizes {label}: {sentence!r}")
    for pattern, label in CONCEPTS[kind]:
        if not re.search(pattern, role, re.IGNORECASE):
            problems.append(f"the role text never states {label}")
    return problems


def _assert_definition(kind: str, frontmatter: dict) -> None:
    """Every frontmatter claim of one helper, through the helpers above."""
    assert frontmatter.get("name") == kind, f"name: {frontmatter.get('name')!r}, expected {kind!r}"
    _assert_description(frontmatter, kind)
    _assert_model(frontmatter, "claude-haiku-5-5" if kind == "explorer" else "claude-opus-5-5")
    if kind == "reviewer":
        _assert_effort(frontmatter, "high")
    _assert_tools(frontmatter)


# ---------------------------------------------------------------------------
# The real definitions
# ---------------------------------------------------------------------------


def test_explorer_pins_haiku() -> None:
    """Criterion 1: the configuration selects Claude Haiku 5.5.

    Refuted by removing the definition or writing another model into it.
    """
    frontmatter, _ = _definition("explorer")
    assert frontmatter.get("name") == "explorer"
    _assert_description(frontmatter, "explorer")
    _assert_model(frontmatter, "claude-haiku-5-5")


def test_reviewer_pins_opus_high() -> None:
    """Criterion 2: the configuration selects Claude Opus 5.5 at high effort.

    Refuted by removing the definition, writing another model, or dropping or
    changing the effort.
    """
    frontmatter, _ = _definition("reviewer")
    assert frontmatter.get("name") == "reviewer"
    _assert_description(frontmatter, "reviewer")
    _assert_model(frontmatter, "claude-opus-5-5")
    _assert_effort(frontmatter, "high")


def test_helpers_allow_read_tools_only() -> None:
    """Criterion 3: the allowlist is exactly Read, Grep, Glob, for both helpers.

    Refuted by any shell, writer, delegation or inherited tool set.
    """
    for name in ("explorer", "reviewer"):
        frontmatter, _ = _definition(name)
        _assert_tools(frontmatter)


def test_helpers_state_read_only_reporting_roles() -> None:
    """Criterion 4: the instructions state the reporting roles and the prohibitions.

    The explorer reports source-backed findings and explicit unknowns; the
    reviewer reports findings against the supplied spec and evidence. Neither
    authorizes repairs, commits, tracker writes or accepting its own work.
    Refuted by removing the role or authorizing any of the four.
    """
    for name in ("explorer", "reviewer"):
        frontmatter, body = _definition(name)
        assert "AGENTS.md" in body, (
            f"{name}: the definition does not point at the repository instructions "
            "(AGENTS.md) whose working contract the helper follows"
        )
        problems = _role_problems(_role_text(body), name)
        assert not problems, f"{name}: the role text fails the read-only contract: {problems}"


# ---------------------------------------------------------------------------
# Frontmatter fixtures — the counter-checks through the same helpers
# ---------------------------------------------------------------------------


def _correct_frontmatter(kind: str) -> dict:
    """A minimal, otherwise correct frontmatter for one helper."""
    frontmatter: dict = {
        "name": kind,
        "description": f"Read-only {kind} helper of this repository.",
        "model": "claude-haiku-5-5" if kind == "explorer" else "claude-opus-5-5",
        "tools": "Read, Grep, Glob",
    }
    if kind == "reviewer":
        frontmatter["effort"] = "high"
    return frontmatter


MUTATIONS = [
    ("explorer", {"model": "claude-sonnet-5"}),
    ("explorer", {"model": None}),
    ("reviewer", {"model": "claude-opus-5"}),
    ("reviewer", {"effort": None}),
    ("reviewer", {"effort": "medium"}),
    ("explorer", {"tools": "Read, Grep, Glob, Bash"}),
    ("explorer", {"tools": None}),
    ("reviewer", {"tools": "Read, Grep, Glob, Task"}),
    ("reviewer", {"tools": "Read, Grep, Glob, Write"}),
    ("reviewer", {"tools": "*"}),
    ("explorer", {"name": "researcher"}),
    ("explorer", {"description": "   "}),
]


@pytest.mark.parametrize("kind", ["explorer", "reviewer"])
def test_the_correct_fixture_passes(kind: str) -> None:
    """The counter-checks measure something only if the correct fixture passes (RB-G7)."""
    _assert_definition(kind, _correct_frontmatter(kind))


@pytest.mark.parametrize(
    ("kind", "change"),
    MUTATIONS,
    ids=[
        "explorer-wrong-model",
        "explorer-model-missing",
        "reviewer-wrong-model",
        "reviewer-effort-missing",
        "reviewer-effort-low",
        "explorer-shell-tool",
        "explorer-tools-inherited",
        "reviewer-delegation-tool",
        "reviewer-writer-tool",
        "reviewer-tools-unrestricted",
        "explorer-wrong-name",
        "explorer-description-empty",
    ],
)
def test_a_mutated_frontmatter_is_caught(kind: str, change: dict) -> None:
    """Wrong models, a missing effort and extra or inherited tools fail the same helpers."""
    frontmatter = _correct_frontmatter(kind)
    for field, value in change.items():
        if value is None:
            frontmatter.pop(field, None)
        else:
            frontmatter[field] = value
    with pytest.raises(AssertionError):
        _assert_definition(kind, frontmatter)


# ---------------------------------------------------------------------------
# Role fixtures — the counter-checks through the same helper
# ---------------------------------------------------------------------------

EXPLORER_SENTENCES = (
    "You read the repository and map its sources for the caller.",
    "Report source-backed findings with their evidence, and name what you could not find as an explicit unknown.",
    "Leave research-file and tracker writes to the caller.",
    "You never repair, commit or accept your own work.",
)
REVIEWER_SENTENCES = (
    "You compare the supplied spec with the implementation evidence in your fresh "
    "context and return actionable findings.",
    "You never repair, commit or accept your own work; tracker writes stay with the orchestrator.",
)


def _role(kind: str, without: int = -1) -> str:
    source = EXPLORER_SENTENCES if kind == "explorer" else REVIEWER_SENTENCES
    sentences = [sentence for i, sentence in enumerate(source) if i != without]
    return f"# {kind}\n\n" + " ".join(sentences) + "\n"


@pytest.mark.parametrize("kind", ["explorer", "reviewer"])
def test_the_fixture_roles_pass_their_own_check(kind: str) -> None:
    """The counter-checks measure something only if the unmuted fixtures pass (RB-G7)."""
    assert _role_problems(_role(kind), kind) == []


@pytest.mark.parametrize("kind", ["explorer", "reviewer"])
def test_an_explicit_action_by_the_caller_is_not_helper_authorization(kind: str) -> None:
    assert _role_problems(_role(kind) + " The caller commits the fix.", kind) == []


@pytest.mark.parametrize(
    ("kind", "authorization"),
    [
        ("explorer", "You may repair what you find along the way."),
        ("explorer", "After mapping you commit the result."),
        ("reviewer", "Update the tracker with your verdict."),
        ("reviewer", "Accept your own findings when they hold."),
        ("explorer", "You only repair what you find."),
        ("reviewer", "When the caller asks, you commit the fix."),
        ("reviewer", "You may commit only with approval."),
        ("reviewer", "When the orchestrator asks, you commit the fix."),
        ("reviewer", "When the maintainer asks, you commit the fix."),
    ],
    ids=[
        "repair-authorized",
        "commit-authorized",
        "tracker-write-authorized",
        "self-acceptance-authorized",
        "repair-only-authorized",
        "caller-condition-authorized",
        "approval-condition-authorized",
        "orchestrator-condition-authorized",
        "maintainer-condition-authorized",
    ],
)
def test_a_role_that_authorizes_an_action_is_caught(kind: str, authorization: str) -> None:
    """A changed role that grants what it must prohibit fails the same helper."""
    problems = _role_problems(_role(kind) + " " + authorization, kind)
    assert problems, f"the inserted authorization passed: {authorization!r}"


@pytest.mark.parametrize(
    ("kind", "without"),
    [("explorer", 3), ("reviewer", 0)],
    ids=["explorer-prohibition-dropped", "reviewer-spec-comparison-dropped"],
)
def test_a_role_that_drops_a_required_statement_is_caught(kind: str, without: int) -> None:
    """A role that loses its prohibition or its reporting statement fails the same helper."""
    problems = _role_problems(_role(kind, without=without), kind)
    assert problems, f"dropping sentence {without} of {kind} passed the role check"
