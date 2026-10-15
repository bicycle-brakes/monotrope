"""The counterexample matrix of plans/changes/interview-context/spec.md.

Each acceptance criterion gets the test that holds it and the fault that
would refute it (plan.md, "Criterion ledger"). The fixtures are plain trees
with their own `decisions/adoption.yaml` — the gate reads files and the
adoption record, no git — so every case here holds in a kit copy too: no
fixture reads this repository's adoption days, and the instruction pins read
only files the manifest carries.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import check_interview_minimums as counting  # noqa: E402

SCRIPT = REPO / "scripts" / "check_question_context.py"
GATE_FILE = REPO / "decisions" / "gates.yaml"
CI_FILE = REPO / ".github" / "workflows" / "ci.yml"
WORKFLOW = REPO / "docs" / "WORKFLOW.md"
COMMAND = "python3 scripts/check_question_context.py"

ON = "2026-10-14"  # the fixture adoption day itself — subject (inclusive)
LATE = "2026-10-15"  # after it — subject
EARLY = "2026-10-13"  # before it — exempt
ADOPTION = "schema_version: 1\nadopted:\n  question-context: 2026-10-14\n"

CONTEXT = (
    "context: |\n"
    "  Topic: The interview records of this change.\n"
    "  Intention: Keep beside each answer the explanation it was given with.\n"
    "  Today: The counting gate holds the answers, not their context.\n"
    "  Repository change: Every subject record gains a context field.\n"
    "  Architecture change: A gate reads the records beside the counter.\n"
)


def _tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "decisions").mkdir(parents=True)
    (root / "decisions" / "adoption.yaml").write_text(ADOPTION, encoding="utf-8")
    (root / "plans" / "changes").mkdir(parents=True)
    return root


def _change(root: Path, name: str, text: str, archive: bool = False) -> Path:
    folder = root / "plans" / "changes" / "archive" / name if archive else root / "plans" / "changes" / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "decisions.md").write_text(text, encoding="utf-8")
    return folder / "decisions.md"


def record(
    qid: str,
    *,
    day: str = ON,
    asked: str | None = None,
    status: str = "answered",
    answered_by: str = "maintainer",
    context: str | None = CONTEXT,
    madr: str | None = None,
) -> str:
    """One Q-record; `context=None` omits the field, `madr=None` writes the
    ordinary one-line statement dated with the recording day. `asked` can
    precede that day when an older question receives a later answer."""
    parts = [
        f"## {qid} · the question\n\n",
        f"asked: {day if asked is None else asked}\nanswer: yes\nanswered_by: {answered_by}\nstatus: {status}\n\n",
    ]
    if context is not None:
        parts.append(context + "\n")
    if madr is None:
        madr = (
            "In the context of a rule nobody checked, facing two options, we decided one, "
            f"to achieve the goal, accepting the cost. — {day}\n"
        )
    parts.append("\n" + madr)
    return "".join(parts) + "\n"


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )


def _snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted([*(root / "plans").rglob("*.md"), *(root / "decisions").rglob("*.yaml")])
    }


# --- AC 1 · the general rule covers every question --------------------------


def test_general_rule_covers_all_questions() -> None:
    """The rule stands in the general instructions, not in the interview
    prompt alone — conversation and the review ambiguity are named."""
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "question-context" in workflow
    assert "conversation" in workflow
    assert "review ambiguities" in workflow
    agents = REPO / "AGENTS.md"
    if not agents.is_file():
        return  # AGENTS.md stays in its repository; the workflow carries the rule
    text = agents.read_text(encoding="utf-8")
    assert "every question" in text
    assert "ADHD" in text


@pytest.mark.parametrize(
    "standing_rule",
    [
        "technical terms and identifiers at first use in every message",
        "personal reasons to care stay outside the repository",
        "nothing depends on it alone",
        "with few agents and a visible queue",
    ],
    ids=["all-messages", "personal-reasons", "policy-layers", "visible-queue"],
)
def test_context_rule_preserves_existing_standing_rules(standing_rule: str) -> None:
    """Making room for question context must retain the standing rules for
    communication, research, tool permissions and coordinated work."""
    agents = REPO / "AGENTS.md"
    if not agents.is_file():
        return  # the kit carries the workflow; its AGENTS.md is local inventory
    text = " ".join(agents.read_text(encoding="utf-8").lower().split())
    assert standing_rule in text


# --- AC 2 · the form: context first, the question last ----------------------


def test_question_forms_put_context_before_options_and_question_last() -> None:
    spec = (REPO / "prompts" / "02-spec.md").read_text(encoding="utf-8")
    assert "Topic:" in spec and "Intention" in spec and "Architecture change" in spec
    assert spec.index("Topic:") < spec.index("Goal in one sentence:")
    assert "stands last" in spec
    interview = (REPO / "prompts" / "01a-interview.md").read_text(encoding="utf-8")
    assert "Topic:" in interview and "Intention" in interview and "Architecture change" in interview
    assert "Before the options" in interview
    assert "comes last" in interview


def _assert_plan_card_form(plan: str) -> str:
    before_card, card_and_tail = plan.split("```text\n", 1)
    card, tail = card_and_tail.split("\n```", 1)
    prefaces = [paragraph for paragraph in before_card.split("\n\n") if "contextual preface" in paragraph]
    assert len(prefaces) == 1, "The contextual preface must precede the card."
    preface = prefaces[0]
    instruction = " ".join(preface.split())
    assert "before the card" in instruction
    assert "then the card" in instruction
    parts = ("Topic", "Intention", "Today", "Repository change", "Architecture change")
    for part in parts:
        assert part in preface, part
    positions = [preface.index(part) for part in parts]
    assert positions == sorted(positions), "The five context parts must stay in order."
    lines = card.splitlines()
    assert len(lines) == 6
    for line, field in zip(lines[:-1], ("For you:", "Done when:", "Appetite:", "Not now:", "Pre-mortem:"), strict=True):
        assert line.startswith(field), field
    assert lines[-1] == "Starts unless you say stop."
    assert 'no "ok" is needed' in tail  # the preface asks for no extra approval
    return preface


def test_plan_card_requires_preface_and_preserves_veto() -> None:
    plan = (REPO / "prompts" / "03-plan.md").read_text(encoding="utf-8")
    preface = _assert_plan_card_form(plan)
    mutations = [
        plan.replace(preface, "", 1) + "\n\n" + preface,
        plan.replace(preface, preface.replace("before the card", "after the card"), 1),
        plan.replace("Starts unless you say stop.\n```", "Starts unless you say stop.\nMore explanation.\n```", 1),
    ]
    for part in ("Topic", "Intention", "Today", "Repository change", "Architecture change"):
        mutations.append(plan.replace(preface, preface.replace(part, "", 1), 1))
    for mutation in mutations:
        with pytest.raises(AssertionError):
            _assert_plan_card_form(mutation)


# --- AC 4 · the record keeps the context in its own field -------------------


def test_interview_record_has_a_dedicated_context_field() -> None:
    interview = (REPO / "prompts" / "01a-interview.md").read_text(encoding="utf-8")
    assert "context: |" in interview  # the record example shows the field


def test_interview_minimums_still_counts_a_record_with_a_context_field() -> None:
    text = record("Q-1")
    assert counting._counted(counting._parse_records(text)[0]) == 1
    without = record("Q-1", context=None)
    assert counting._counted(counting._parse_records(without)[0]) == 1


# --- AC 5 · a subject record without context goes red -----------------------


def test_missing_context_goes_red(tmp_path: Path) -> None:
    """Mutation evidence for scripts/check_question_context.py: deleting only
    the subject record's context turns a green run red, naming file and id."""
    root = _tree(tmp_path)
    decisions = _change(root, "one", record("Q-1"))
    assert run(root).returncode == 0
    decisions.write_text(record("Q-1", context=None), encoding="utf-8")
    done = run(root)
    assert done.returncode == 1
    assert "plans/changes/one/decisions.md" in done.stdout
    assert "Q-1" in done.stdout


@pytest.mark.parametrize(
    "value",
    [
        "context:    \n",
        "context: |\n",
        "context: null\n",
        "context: true\n",
        "context: 42\n",
        "context: [a, b]\n",
        "context: {a: b}\n",
        "context: - item\n",
        'context: ""\n',
        "context: ''\n",
    ],
    ids=[
        "whitespace",
        "empty-block",
        "null",
        "boolean",
        "number",
        "flow-list",
        "flow-map",
        "block-list",
        "quoted-blank",
        "single-quoted-blank",
    ],
)
@pytest.mark.parametrize("comment", ["", " # shown with the question"], ids=["no-comment", "comment"])
def test_empty_or_non_text_context_goes_red(tmp_path: Path, value: str, comment: str) -> None:
    root = _tree(tmp_path)
    decisions = _change(root, "thin", record("Q-1", context=f"context: kept.{comment}\n"))
    assert run(root).returncode == 0
    decisions.write_text(record("Q-1", context=value.replace("\n", f"{comment}\n", 1)), encoding="utf-8")
    done = run(root)
    assert done.returncode == 1, done.stdout
    assert "plans/changes/thin/decisions.md" in done.stdout
    assert "Q-1" in done.stdout


@pytest.mark.parametrize(
    "value",
    ["2026-10-14", "2026-10-14T12:34:56Z", "2026-10-14 12:34:56+02:00", "2026-10-14t12:34:56.789Z"],
    ids=["date", "utc-timestamp", "offset-timestamp", "fractional-timestamp"],
)
def test_date_or_timestamp_context_goes_red(tmp_path: Path, value: str) -> None:
    root = _tree(tmp_path)
    decisions = _change(root, "dated", record("Q-1", context=f'context: "{value}"\n'))
    assert run(root).returncode == 0  # a quoted date is text
    decisions.write_text(record("Q-1", context=f"context: |\n  {value}\n"), encoding="utf-8")
    assert run(root).returncode == 0  # a literal block also remains text
    decisions.write_text(record("Q-1", context=f"context: {value}\n"), encoding="utf-8")
    before = _snapshot(root)
    done = run(root)
    assert done.returncode == 1, done.stdout
    assert "plans/changes/dated/decisions.md" in done.stdout
    assert "Q-1" in done.stdout
    assert "not text" in done.stdout
    assert _snapshot(root) == before


def test_context_cannot_be_borrowed_from_another_record(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _change(root, "pair", record("Q-1") + "\n" + record("Q-2", context=None))
    done = run(root)
    assert done.returncode == 1
    assert "Q-2" in done.stdout
    assert "Q-2 —" in done.stdout and "Q-1 —" not in done.stdout
    # a context line outside every record belongs to no record
    _change(root, "pair", "context: borrowed\n\n" + record("Q-1") + "\n" + record("Q-2", context=None))
    done = run(root)
    assert done.returncode == 1
    assert "Q-2 —" in done.stdout


def test_every_answered_occurrence_needs_context(tmp_path: Path) -> None:
    """A repeated id is its own record, and an agent-attributed answer is
    answered — neither is exempt because the other block has context."""
    root = _tree(tmp_path)
    body = record("Q-1") + "\n" + record("Q-1", context=None) + "\n" + record("Q-2", answered_by="agent", context=None)
    _change(root, "repeats", body)
    done = run(root)
    assert done.returncode == 1
    assert done.stdout.count("Q-1 —") == 1
    assert "Q-2 —" in done.stdout


# --- AC 6 · presence only ----------------------------------------------------


@pytest.mark.parametrize(
    "value",
    ["kept.\n", '"kept # as text."\n', "'kept # as text.'\n", "|\n  kept.\n", ">\n  kept.\n"],
    ids=["plain", "double-quoted", "single-quoted", "literal", "folded"],
)
@pytest.mark.parametrize("comment", ["", " # shown with the question"], ids=["no-comment", "comment"])
def test_nonblank_context_passes_without_clarity_scoring(tmp_path: Path, value: str, comment: str) -> None:
    root = _tree(tmp_path)
    _change(root, "terse", record("Q-1", context="context: " + value.replace("\n", f"{comment}\n", 1)))
    _change(root, "full", record("Q-2"))
    assert run(root).returncode == 0  # wording and length are not graded


# --- AC 7 · the cut-off is each answer's own recording day ------------------


def test_adoption_day_and_later_answers_are_subject(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _change(root, "on-day", record("Q-1", day=ON, context=None))
    _change(root, "late", record("Q-2", day=LATE, context=None))
    _change(root, "early", record("Q-3", day=EARLY, context=None))
    done = run(root)
    assert done.returncode == 1
    assert "on-day" in done.stdout  # the adoption day itself is subject
    assert "late" in done.stdout
    assert "early" not in done.stdout  # the stock stays exempt


@pytest.mark.parametrize("day", [ON, LATE], ids=["adoption-day", "after-adoption"])
def test_late_answer_uses_only_the_decision_statement_suffix(tmp_path: Path, day: str) -> None:
    """An earlier asked day cannot exempt a later answer; a date embedded
    within its statement cannot supply the missing recording-day suffix."""
    root = _tree(tmp_path)
    decisions = _change(root, "old-question", record("Q-1", day=day, asked=EARLY))
    assert run(root).returncode == 0
    decisions.write_text(record("Q-1", day=day, asked=EARLY, context=None), encoding="utf-8")
    done = run(root)
    assert done.returncode == 1, done.stdout
    assert "plans/changes/old-question/decisions.md: Q-1" in done.stdout
    assert "keeps no context" in done.stdout

    statement = f"In the context of a choice, we decided A — {day} and recorded B later.\n"
    decisions.write_text(record("Q-1", day=day, asked=EARLY, context=None, madr=statement), encoding="utf-8")
    done = run(root)
    assert done.returncode == 3, done.stdout
    assert "NOT MEASURED" in done.stdout
    assert "plans/changes/old-question/decisions.md: Q-1" in done.stdout
    assert "no `— YYYY-MM-DD` date ends the decision statement" in done.stdout

    remark = f"In the context of a choice, we decided A, accepting B. — {day} (recorded on the bead the same day)\n"
    decisions.write_text(record("Q-1", day=day, asked=EARLY, context=None, madr=remark), encoding="utf-8")
    done = run(root)
    assert done.returncode == 1, done.stdout  # a closing remark after the date keeps the day readable
    assert "keeps no context" in done.stdout
    trailing = remark.replace(" (recorded", " and more (recorded")
    decisions.write_text(record("Q-1", day=day, asked=EARLY, context=None, madr=trailing), encoding="utf-8")
    assert run(root).returncode == 3  # prose after the date is not a closing remark


@pytest.mark.parametrize(
    "continuation",
    [
        pytest.param("—\n2026-10-14", id="split-date"),
        pytest.param("\n  — 2026-10-14", id="indented-suffix"),
        pytest.param("—\n  2026-10-14", id="indented-date"),
        pytest.param("\n\n— 2026-10-14", id="blank-before-suffix"),
        pytest.param("—\n\n2026-10-14", id="blank-before-date"),
        pytest.param("\n\n  —\n\n  2026-10-14", id="blank-and-indented"),
    ],
)
def test_answer_date_uses_wrapped_decision_suffix(tmp_path: Path, continuation: str) -> None:
    """Indented or blank-separated date continuations remain measurable;
    a date inside the context value never dates the answer."""
    wrapped = (
        "In the context of many existing records without a context field, facing a choice, we decided "
        f"the cut-off, to achieve a gate that holds, accepting that older answers show no context. {continuation}\n"
    )
    root = _tree(tmp_path)
    _change(root, "wrapped", record("Q-1", day=EARLY, madr=wrapped))
    assert run(root).returncode == 0
    _change(root, "other", record("Q-2", context=None), archive=True)
    _change(root, "wrapped", record("Q-1", context=None, madr=wrapped))
    done = run(root)
    assert done.returncode == 1, done.stdout
    assert "plans/changes/wrapped/decisions.md: Q-1" in done.stdout
    assert "plans/changes/archive/other/decisions.md: Q-2" in done.stdout
    assert "NOT MEASURED" not in done.stdout
    dated = CONTEXT.replace("Architecture change:", "Recorded 2026-10-13 earlier. Architecture change:")
    _change(root, "wrapped", record("Q-1", context=dated, madr=wrapped.replace("2026-10-14", "")))
    done = run(root)
    assert done.returncode == 3  # only the statement dates the answer, and its date is missing


@pytest.mark.parametrize(
    "unrelated",
    [
        "context: |\n  — 2026-10-14\n",
        "recorded: — 2026-10-14\n",
        "\nAnother paragraph. — 2026-10-14\n",
        "```text\n— 2026-10-14\n```\n",
    ],
)
def test_wrapped_date_cannot_come_from_another_field_or_example(tmp_path: Path, unrelated: str) -> None:
    root = _tree(tmp_path)
    statement = "In the context of a choice, we decided one, accepting the cost. —\n"
    _change(root, "case", record("Q-1", madr=statement + unrelated))
    done = run(root)
    assert done.returncode == 3, done.stdout
    assert "plans/changes/case/decisions.md: Q-1" in done.stdout
    assert "no `— YYYY-MM-DD` date" in done.stdout


def test_archived_and_spec_less_answers_are_subject(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _change(root, "2026-10-14-archived", record("Q-1", context=None), archive=True)
    done = run(root)
    assert done.returncode == 1
    assert "archive/2026-10-14-archived/decisions.md" in done.stdout


def test_examples_open_and_skip_records_are_not_answers(tmp_path: Path) -> None:
    example = (
        "```markdown\n"
        "## Q-9 · a documented example\n\n"
        "asked: 2026-10-14\nanswer: yes\nanswered_by: maintainer\nstatus: answered\n\n"
        "In the context of an example, facing nothing, we decided nothing. — 2026-10-14\n"
        "```\n"
    )
    open_block = record("Q-3", status="open", context=None) + "\n" + SKIP_BLOCK
    inside = record("Q-1") + "\n" + record("Q-2", status="open", context=None, madr=FENCED_STATEMENT)
    root = _tree(tmp_path)
    _change(root, "outside", example + "\n" + record("Q-1") + "\n" + open_block)
    _change(root, "inside", inside)
    assert run(root).returncode == 0


SKIP_BLOCK = "## SKIP · interview\n\nstatus: skipped\nreason: nothing is owed here.\n"
FENCED_STATEMENT = (
    "```text\n"
    "status: answered\n"
    "In the context of an example, facing nothing, we decided nothing. — 2026-10-14\n"
    "```\n"
    "\n"
    "In the context of the real answer, facing a choice, we decided one. — 2026-10-14\n"
)


# --- AC 8 · older answers stay exempt, and nothing is written ---------------


def test_older_answers_stay_exempt_in_mixed_files(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    body = record("Q-1", day=EARLY, context=None) + "\n" + record("Q-2") + "\n" + record("Q-3", context=None)
    _change(root, "mixed", body)
    done = run(root)
    assert done.returncode == 1
    assert "Q-3 —" in done.stdout  # the new answer without context is caught
    assert "Q-1 —" not in done.stdout  # the old one is exempt, not backfilled
    assert "Q-2 —" not in done.stdout


def test_gate_never_writes_records_or_adoption(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _change(root, "green", record("Q-1", day=EARLY, context=None) + "\n" + record("Q-2"))
    _change(root, "red", record("Q-3", context=None))
    before = _snapshot(root)
    assert run(root).returncode == 1
    assert _snapshot(root) == before
    assert run(root).returncode == 1
    assert _snapshot(root) == before


# --- AC 9 · unreadable evidence is not measured, and takes precedence -------


@pytest.mark.parametrize(
    ("mutation", "evidence"),
    [
        pytest.param("no-adoption", "adoption.yaml", id="no-adoption-day"),
        pytest.param("impossible", "calendar", id="impossible-date"),
        pytest.param("two-dates", "ambiguous", id="ambiguous-date"),
        pytest.param("no-statement", "In the context of", id="no-statement"),
        pytest.param("no-dash", "— YYYY-MM-DD", id="date-without-the-dash"),
        pytest.param("bytes", "cannot be read", id="unreadable-file"),
    ],
)
def test_unreadable_evidence_is_not_a_pass(tmp_path: Path, mutation: str, evidence: str) -> None:
    root = _tree(tmp_path)
    if mutation == "no-adoption":
        (root / "decisions" / "adoption.yaml").unlink()
        _change(root, "case", record("Q-1", context=None))
    elif mutation == "impossible":
        _change(
            root, "case", record("Q-1", context=None, madr="In the context of a change, we decided. — 2026-13-45\n")
        )
    elif mutation == "two-dates":
        madr = (
            "In the context of a change, we decided on the earlier note — 2026-10-14 "
            "and on the later one — 2026-10-15.\n"
        )
        _change(root, "case", record("Q-1", context=None, madr=madr))
    elif mutation == "no-statement":
        _change(root, "case", record("Q-1", context=None, madr="We decided. — 2026-10-14\n"))
    elif mutation == "no-dash":
        _change(
            root,
            "case",
            record("Q-1", context=None, madr="In the context of a change, we decided. Recorded 2026-10-14.\n"),
        )
    else:
        decisions = _change(root, "case", record("Q-1", context=None))
        # cp1252 bytes that are no valid UTF-8 (é = 0xe9, the cp1252 dash =
        # 0x97): the gate must report the file as unreadable — not measured,
        # never an exemption.
        decisions.write_bytes(b"In the context of caf\xe9. \x97 2026-10-14\n")
    done = run(root)
    assert done.returncode == 3, done.stdout
    assert "NOT MEASURED" in done.stdout
    assert evidence in done.stdout


def test_unmeasured_evidence_takes_exit_precedence(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    body = record("Q-1", context=None) + "\n" + record("Q-2", context=None, madr="We decided. — 2026-13-45\n")
    _change(root, "case", body)
    done = run(root)
    assert done.returncode == 3
    assert "Q-1" in done.stdout and "Q-2" in done.stdout  # both are named, none is passed


# --- AC 10 · the gate is blocking in both placements ------------------------


def test_gate_is_blocking_in_both_placements() -> None:
    gates = yaml.safe_load(GATE_FILE.read_text(encoding="utf-8"))
    entries = [g for g in gates["gates"] if g["id"] == "question-context"]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["command"] == COMMAND
    assert entry["job"] == "verify"
    assert entry["enforcement"] == "block"
    assert entry["placement"] == "both"
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    steps = [s for job in doc["jobs"].values() for s in job.get("steps", []) if s.get("id") == "question-context"]
    assert len(steps) == 1
    assert steps[0]["run"] == COMMAND
    assert "continue-on-error" not in steps[0]


# --- AC 11 · the kit carries principle, form, gate and tests ----------------


def test_context_gate_and_tests_travel_with_the_principle() -> None:
    manifest = yaml.safe_load((REPO / "scripts" / "kit" / "manifest.yaml").read_text(encoding="utf-8"))
    rules = {rule["prefix"]: rule["rolle"] for rule in manifest["rules"]}
    assert rules["scripts/check_question_context.py"] == "mechanismus"
    assert rules["tests/test_check_question_context.py"] == "mechanismus"
    source = SCRIPT.read_text(encoding="utf-8")
    assert "adopted_on" in source  # the day comes from the repository's record
    assert 'root / "decisions"' not in source  # and never from a path or date of its own
    assert "os.environ" not in source and "profile" not in source  # no switch to turn the rule off
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "ADHD" in workflow  # the reason travels with the principle
    adr = REPO / "docs" / "adr" / "0018-every-question-carries-its-context.md"
    if adr.is_file():
        text = adr.read_text(encoding="utf-8")
        assert "Q-1" in text and "Q-5" in text
        assert "ADHD" in text


def test_bare_context_over_indented_prose_names_the_block_fix(tmp_path: Path) -> None:
    """F-3: indented prose under a bare `context:` is not reported as blank."""
    root = _tree(tmp_path)
    _change(root, "bare", record("Q-1", context="context:\n  Topic: the cut-off.\n  Intention: a gate that holds.\n"))
    done = run(root)
    assert done.returncode == 1, done.stdout
    assert "write `context: |`" in done.stdout
    assert "is blank" not in done.stdout
