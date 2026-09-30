"""The command `python3 scripts/harness.py decide adr`.

Criteria 7-10 of plans/changes/harness-decide-adr/spec.md. Every test builds its
own git repository in a temporary directory; the terminal dialogue is scripted
through an injected `ask`, and the terminal guard is run through the real
command line with stdin from /dev/null. The one file of this repository read
is `provenance.yaml`, which travels with the kit.
"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "harness.py"
GATE = REPO_ROOT / "scripts" / "check_adr_answers.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import check_adr_answers as cag  # noqa: E402
import harness  # noqa: E402

TODAY = date(2026, 9, 30)

MAP = """\
schema_version: 1
roles:
  decider:
    handle: "@someone"
paths:
  - prefix: "docs/"
    frontmatter: required
  - prefix: "decisions/answers/"
    allowed: [human-decided]
    frontmatter: none
    owner_role: decider
"""


@pytest.fixture(autouse=True)
def _no_outer_git(monkeypatch: pytest.MonkeyPatch) -> None:
    """A git variable of the caller (a hook, make verify) must not point the command elsewhere."""
    for name in list(os.environ):
        if name.startswith("GIT_"):
            monkeypatch.delenv(name)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def _git(repo: Path, *args: str) -> str:
    erg = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return erg.stdout.strip()


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _feature(change: str, *, proposed: str = "no", outcome: str | None = None) -> str:
    lines = [
        "---",
        f'title: "Spec — {change}"',
        "class: feature",
        f"change: {change}",
        f'adr_question: {{proposed: "{proposed}", answered_by: null, reason: "the proposal for {change}"}}',
    ]
    if outcome:
        lines += ["intent:", f"  outcome: {outcome}"]
    return "\n".join([*lines, "---", "", "# Spec", ""])


def _repo(tmp_path: Path, *features: str, map_text: str | None = MAP) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    if map_text is not None:
        _write(repo / "provenance.yaml", map_text)
    for change in features:
        _write(repo / "plans" / "changes" / change / "spec.md", _feature(change))
    _write(repo / "README.md", "r\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "init")
    return repo.resolve()


def _msg(repo: Path) -> Path:
    where = Path(_git(repo, "rev-parse", "--git-path", "ADR_ANSWER_MSG"))
    return where if where.is_absolute() else repo / where


def _answer_path(repo: Path, change: str) -> Path:
    return repo / "decisions" / "answers" / change / "adr.yaml"


class Script:
    """An `ask` that returns scripted lines and records each prompt."""

    def __init__(self, *replies: str | type[BaseException]) -> None:
        self.replies = list(replies)
        self.prompts: list[str] = []

    def __call__(self, prompt: str) -> str:
        self.prompts.append(prompt)
        reply = self.replies.pop(0)
        if isinstance(reply, type):
            raise reply
        return reply


def _never(prompt: str) -> str:
    raise AssertionError(f"asked although it must not: {prompt!r}")


def _decide(repo: Path, ask: harness.Ask, role: str = "decider") -> tuple[int, list[str]]:
    out: list[str] = []
    code = harness.decide_adr(repo, ask=ask, out=out.append, today=TODAY, role=role, message_path=_msg(repo))
    return code, out


def _main(repo: Path, *args: str, ask: harness.Ask = _never) -> tuple[int, list[str]]:
    out: list[str] = []
    code = harness.main(["decide", "adr", *args, "--root", str(repo)], ask=ask, out=out.append, today=TODAY)
    return code, out


def _record(change: str = "one", answer: str = "no", reason: str = "Nothing structural changes.") -> list[str]:
    return ["--change", change, "--answer", answer, "--reason", reason, "--stated-in", "session s-1, 2026-09-30"]


def _cli(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=repo,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=False,
    )


def _written(repo: Path) -> list[str]:
    answers = sorted(p.relative_to(repo).as_posix() for p in (repo / "decisions").rglob("*") if p.is_file())
    return answers + (["message"] if _msg(repo).exists() else [])


FULL = ("y", "It fixes a format.", "I said yes.", "An ADR follows.", "It is drafted later.")


# ---------------------------------------------------------------------------
# criterion 7 — the terminal dialogue
# ---------------------------------------------------------------------------


def test_without_a_terminal_the_dialogue_refuses_and_never_writes(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one")
    erg = _cli(repo, "decide", "adr", "--root", str(repo))
    assert erg.returncode == 2, erg.stdout + erg.stderr
    assert "run this yourself in a terminal" in erg.stdout
    assert _written(repo) == []


def test_each_question_shows_its_context(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "alpha")
    _write(repo / "plans/changes/beta/spec.md", _feature("beta", proposed="yes", outcome="Beta does a thing."))
    ask = Script("n", "Alpha decides nothing.", "y", "Beta decides a boundary.", "One.", "Two.", "Three.")
    code, out = _decide(repo, ask)
    assert code == 0, out

    first = out.index("ADR question 1 of 2 — change alpha")
    second = out.index("ADR question 2 of 2 — change beta")
    alpha, beta = out[first:second], out[second:]
    assert "  Title:    Spec — alpha" in alpha
    assert "  Anchor:   plans/changes/alpha/spec.md" in alpha
    assert "  Proposal: no — the proposal for alpha" in alpha
    assert not any(line.startswith("  Outcome:") for line in alpha), "an outcome shown where the header has none"
    assert "  Title:    Spec — beta" in beta
    assert "  Anchor:   plans/changes/beta/spec.md" in beta
    assert "  Outcome:  Beta does a thing." in beta
    assert "  Proposal: yes — the proposal for beta" in beta


def test_only_y_or_n_is_taken_as_an_answer(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one")
    ask = Script("yes", "maybe", "Y", "", " y ", "It fixes a format.", "One.", "Two.", "Three.")
    code, out = _decide(repo, ask)
    assert code == 0, out
    yn = [p for p in ask.prompts if "[y/n]" in p]
    assert len(yn) == 5, "yes, maybe, Y and blank must each be asked again"
    assert out.count("Answer y or n.") == 4
    assert "answer: 'yes'" in _answer_path(repo, "one").read_text(encoding="utf-8")


def test_a_lower_case_or_blank_reason_is_refused(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one")
    ask = Script("n", "", "lower case.", "`one` changes nothing.", "fine.", "One.", "  ", "Two.", "Three.")
    code, out = _decide(repo, ask)
    assert code == 0, out
    assert len([p for p in ask.prompts if "reason" in p]) == 3
    assert len([p for p in ask.prompts if "Line" in p]) == 5
    assert "reason: '`one` changes nothing.'" in _answer_path(repo, "one").read_text(encoding="utf-8")
    message = _msg(repo).read_text(encoding="utf-8")
    assert "Explained back by the maintainer:\n- One.\n- Two.\n- Three.\n" in message
    assert "fine." not in message


@pytest.mark.parametrize("exc", [EOFError, KeyboardInterrupt])
@pytest.mark.parametrize("at", range(len(FULL)))
def test_an_interrupt_at_any_prompt_never_writes(tmp_path: Path, exc: type[BaseException], at: int) -> None:
    repo = _repo(tmp_path, "one")
    replies: list[str | type[BaseException]] = [*FULL[:at], exc]
    code, out = _decide(repo, Script(*replies))
    assert code == 1
    assert out[-1] == "Interrupted — nothing was written."
    assert _written(repo) == []


def test_a_broken_anchor_or_a_refused_answer_is_listed_before_any_question(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "open", "answered")
    _write(repo / "plans/changes/broken/spec.md", "---\nclass: Feature\n---\n")
    code, out = _decide(repo, _never)
    assert code == 2
    assert any("plans/changes/broken/spec.md" in line for line in out)
    assert _written(repo) == []

    (repo / "plans/changes/broken/spec.md").unlink()
    _write(_answer_path(repo, "answered"), "schema_version: true\n")
    code, out = _decide(repo, _never)
    assert code == 2
    assert any("decisions/answers/answered/adr.yaml is refused" in line for line in out)
    assert _written(repo) == ["decisions/answers/answered/adr.yaml"]


def test_nothing_open_says_so(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one")
    assert _main(repo, *_record())[0] == 0
    code, out = _decide(repo, _never)
    assert code == 0
    assert out == ["No open ADR question — each of the 1 features has its answer file."]


# ---------------------------------------------------------------------------
# criterion 8 — what the command writes, and what it leaves alone
# ---------------------------------------------------------------------------


def test_the_written_answer_is_what_the_gate_accepts(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one", "two")
    ask = Script("y", "It fixes a format.", "n", "Nothing: structural, 'quoted' or #hashed.", "One.", "Two.", "Three.")
    assert _decide(repo, ask)[0] == 0
    for change, answer, proposed in (("one", "yes", "no"), ("two", "no", "no")):
        data, problems = cag.load_answer(_answer_path(repo, change))
        assert problems == []
        assert data["change"] == change and data["answer"] == answer
        assert data["shown"] == {"proposed": proposed, "proposal_reason": f"the proposal for {change}"}
        assert data["answered_by"] == "decider"
        assert data["answered_at"] == TODAY
    erg = subprocess.run([sys.executable, str(GATE), "--root", str(repo)], capture_output=True, text=True, check=False)
    assert erg.returncode == 0, erg.stdout
    assert "held 2 features" in erg.stdout


def test_the_command_never_stages_or_commits(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one", "two")

    def state() -> tuple[str, str, str]:
        return (
            _git(repo, "rev-parse", "HEAD"),
            _git(repo, "diff", "--cached", "--name-only"),
            _git(repo, "ls-files", "--stage"),
        )

    before = state()
    assert _main(repo, *_record(change="two"))[0] == 0
    assert state() == before
    assert _decide(repo, Script("n", "No.", "One.", "Two.", "Three."))[0] == 0  # the one question left: one
    assert state() == before
    assert _git(repo, "status", "--porcelain", "--untracked-files=all").splitlines() == [
        "?? decisions/answers/one/adr.yaml",
        "?? decisions/answers/two/adr.yaml",
    ]


def test_the_message_lands_where_git_says(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one", "two")
    assert _main(repo, *_record(reason="`one` adds a check."))[0] == 0
    message = (repo / ".git" / "ADR_ANSWER_MSG").read_text(encoding="utf-8")
    assert message.startswith("docs(decisions): ADR answer for one\n\n- one: no ADR — `one` adds a check.\n")
    assert "D-" not in message

    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-q", str(linked))
    out: list[str] = []
    code = harness.main(
        ["decide", "adr", *_record(change="two", answer="yes"), "--root", str(linked)],
        ask=_never,
        out=out.append,
        today=TODAY,
    )
    assert code == 0, out
    where = Path(_git(linked, "rev-parse", "--git-path", "ADR_ANSWER_MSG"))
    assert where.is_absolute(), "a linked worktree's git path is absolute"
    assert where.read_text(encoding="utf-8").startswith("docs(decisions): ADR answer for two\n\n- two: an ADR — ")
    assert f"wrote the commit message to {where}" in out


def test_the_printed_steps_name_the_merge(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one")
    code, out = _main(repo, *_record())
    assert code == 0
    text = "\n".join(out)
    assert "wrote decisions/answers/one/adr.yaml" in text
    assert "git add decisions/answers" in text
    assert f"git commit -F {_msg(repo)}" in text
    assert "decision pull request" in text and "label decision" in text
    assert "maintainer merges that pull request, or asks for the merge" in text


@pytest.mark.parametrize(
    "argv", [["decide", "adrx"], ["decid", "adr"], ["decide", "adr", "--bogus"], ["decide", "adr", "--chang", "one"]]
)
def test_an_unknown_verb_or_option_is_exit_2_and_never_writes(tmp_path: Path, argv: list[str]) -> None:
    repo = _repo(tmp_path, "one")
    with pytest.raises(SystemExit) as stop:
        harness.main([*argv, "--root", str(repo)], ask=_never, out=[].append, today=TODAY)
    assert stop.value.code == 2
    erg = _cli(repo, *argv, "--root", str(repo))
    assert erg.returncode == 2 and ("invalid choice" in erg.stderr or "unrecognized arguments" in erg.stderr), (
        erg.stderr
    )
    assert _written(repo) == []


# ---------------------------------------------------------------------------
# criterion 9 — an answer stated in the conversation
# ---------------------------------------------------------------------------


def test_a_stated_answer_is_recorded_without_a_terminal(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one")
    erg = _cli(repo, "decide", "adr", *_record(answer="yes", reason="It decides a boundary."), "--root", str(repo))
    assert erg.returncode == 0, erg.stdout + erg.stderr
    data, problems = cag.load_answer(_answer_path(repo, "one"))
    assert problems == [] and data["answer"] == "yes" and data["reason"] == "It decides a boundary."
    message = _msg(repo).read_text(encoding="utf-8")
    assert "- one: an ADR — It decides a boundary." in message
    assert "Stated by the maintainer in: session s-1, 2026-09-30" in message
    assert "Explained back" not in message


def _stated_cases() -> dict[str, list[str]]:
    full = dict(
        zip(
            ["--change", "--answer", "--reason", "--stated-in"],
            ["one", "no", "It is small.", "session s-1"],
            strict=True,
        )
    )

    def argv(**changed: str | None) -> list[str]:
        merged = {**full, **{f"--{k.replace('_', '-')}": v for k, v in changed.items()}}
        return [x for k, v in merged.items() if v is not None for x in (k, v)]

    cases: dict[str, list[str]] = {}
    for option in ("change", "answer", "reason", "stated_in"):
        cases[f"{option} missing"] = argv(**{option: None})
        cases[f"{option} blank"] = argv(**{option: "  "})
    cases["answer maybe"] = argv(answer="maybe")
    cases["answer Yes"] = argv(answer="Yes")
    cases["reason lower case"] = argv(reason="it is small.")
    cases["a bounded change"] = argv(change="small")
    cases["an unknown change"] = argv(change="nowhere")
    cases["an answered change"] = argv(change="answered")
    return cases


@pytest.mark.parametrize("case", sorted(_stated_cases()))
def test_a_stated_answer_that_breaks_a_rule_is_refused_and_never_writes(tmp_path: Path, case: str) -> None:
    repo = _repo(tmp_path, "one", "answered")
    _write(repo / "plans/changes/small/spec.md", "---\nclass: bounded\n---\n")
    assert _main(repo, *_record(change="answered"))[0] == 0
    kept = _answer_path(repo, "answered").read_bytes()
    _msg(repo).unlink()

    code, out = _main(repo, *_stated_cases()[case])
    assert code == 2, (case, out)
    assert out[-1] == "Nothing was written."
    assert _written(repo) == ["decisions/answers/answered/adr.yaml"]
    assert _answer_path(repo, "answered").read_bytes() == kept


def test_a_refusal_names_why_the_change_owes_no_answer(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one")
    _write(repo / "plans/changes/small/spec.md", "---\nclass: bounded\n---\n")
    _write(repo / "plans/changes/broken/spec.md", "---\nclass: Feature\n---\n")
    assert "states `class: bounded`" in "\n".join(_main(repo, *_record(change="small"))[1])
    assert "no change anchor names `nowhere`" in "\n".join(_main(repo, *_record(change="nowhere"))[1])
    assert "plans/changes/broken/spec.md" in "\n".join(_main(repo, *_record(change="broken"))[1])
    # a finding of another anchor does not block a recording
    assert _main(repo, *_record(change="one"))[0] == 0


# ---------------------------------------------------------------------------
# criterion 10 — who answered is configuration
# ---------------------------------------------------------------------------


def test_answered_by_is_the_role_the_map_names(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "one", "two", map_text=MAP.replace("decider", "someone-else"))
    assert harness.answering_role(repo) == "someone-else"
    assert _main(repo, *_record())[0] == 0
    assert cag.load_answer(_answer_path(repo, "one"))[0]["answered_by"] == "someone-else"
    code, out = _decide(repo, Script("n", "No.", "One.", "Two.", "Three."), role=harness.answering_role(repo))
    assert code == 0, out
    assert cag.load_answer(_answer_path(repo, "two"))[0]["answered_by"] == "someone-else"


@pytest.mark.parametrize(
    ("case", "map_text", "named"),
    [
        ("no map", None, 'prefix: "decisions/answers/"'),
        ("no entry", MAP.split('  - prefix: "decisions/answers/"')[0], 'prefix: "decisions/answers/"'),
        ("no owner_role", MAP.replace("    owner_role: decider\n", ""), "owner_role"),
        ("role not declared", MAP.replace("  decider:\n", "  other:\n"), "`decider:` under `roles:`"),
    ],
)
def test_a_map_without_the_role_refuses_before_asking(
    tmp_path: Path, case: str, map_text: str | None, named: str
) -> None:
    repo = _repo(tmp_path, "one", map_text=map_text)
    for args in ((), tuple(_record())):
        code, out = _main(repo, *args, ask=_never)
        assert code == 2, (case, args, out)
        assert named in "\n".join(out), (case, out)
        assert _written(repo) == []


def test_this_repository_declares_the_answering_role() -> None:
    assert harness.answering_role(REPO_ROOT) == "framework-architect"
    doc = yaml.safe_load((REPO_ROOT / "provenance.yaml").read_text(encoding="utf-8"))
    [entry] = [e for e in doc["paths"] if e["prefix"] == "decisions/answers/"]
    assert entry["allowed"] == ["human-decided"] and entry["frontmatter"] == "none"
