#!/usr/bin/env python3
"""harness.py — the Coding Harness command. One verb today: `decide adr`.

`decide adr` puts the ADR question of every feature without an answer to the
maintainer and writes the answers in the format the gate `adr-answers` reads
(`scripts/check_adr_answers.py`, the one reader of that format). Two ways in:

  * in a terminal, typed by the maintainer: each open question with its
    context, `y` or `n`, a one-sentence reason, and three explain-back lines;
  * stated by the maintainer in a conversation and recorded by whoever holds
    it, without a terminal, one change per run:
    `--change <name> --answer yes|no --reason <text> --stated-in <where>`.

Either way it writes the answer files and a commit message, and prints what is
left: stage, commit, and carry the answers in a decision pull request, which
takes effect when the maintainer merges it or asks for the merge. It never
stages, commits, pushes, merges or signs anything itself.

Who answers is named by the provenance map, looked for at `provenance.yaml`
and then `decisions/provenance.yaml`; when both places hold one, it refuses.

Usage:
    python3 scripts/harness.py decide adr
    python3 scripts/harness.py decide adr --change <name> --answer yes|no \\
        --reason "<one sentence>" --stated-in "<where the maintainer said it>"
Exit: 0 = done (or nothing open), 1 = interrupted, nothing written,
      2 = refused, nothing written.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any

import check_adr_answers as gate
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

MESSAGE_FILE = "ADR_ANSWER_MSG"
PROVENANCE_PLACES = ("provenance.yaml", "decisions/provenance.yaml")
ANSWERS_PREFIX = f"{gate.ANSWERS_DIR}/"
OWNER_ENTRY = (
    f'  - prefix: "{ANSWERS_PREFIX}"\n    allowed: [human-decided]\n    frontmatter: none\n'
    "    owner_role: <a role declared under roles:>"
)
RECORDING = ("change", "answer", "reason", "stated_in")
TEMPLATE = ".github/PULL_REQUEST_TEMPLATE/decision.md"

Ask = Callable[[str], str]
Out = Callable[[str], None]


class Refused(Exception):  # noqa: N818 — a verdict, not an error class
    """The command refuses before it writes anything. Exit 2."""


# ---------------------------------------------------------------------------
# what the command needs before it asks or writes
# ---------------------------------------------------------------------------


def provenance_map(root: Path) -> tuple[Path, str]:
    """The one provenance map of the tree; `Refused` when neither place holds one and when both do."""
    present = [place for place in PROVENANCE_PLACES if os.path.lexists(root / place)]
    if not present:
        raise Refused(
            "no provenance map: looked for "
            f"{PROVENANCE_PLACES[0]} and {PROVENANCE_PLACES[1]}; one of them must name who "
            f"answers, under `paths:`:\n{OWNER_ENTRY}"
        )
    if len(present) == 2:
        raise Refused(f"two provenance maps, {PROVENANCE_PLACES[0]} and {PROVENANCE_PLACES[1]} — keep one of them")
    where = present[0]
    return root / where, where


def answering_role(root: Path) -> str:
    """Criterion 10: the `owner_role` of the map's entry for `decisions/answers/`, declared under `roles:`."""
    path, where = provenance_map(root)
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise Refused(f"cannot read {where} ({exc}); it must name who answers, under `paths:`:\n{OWNER_ENTRY}") from exc
    if not isinstance(doc, dict):
        raise Refused(f"{where} is not a mapping; add under `paths:`:\n{OWNER_ENTRY}")
    entries = [e for e in doc.get("paths") or [] if isinstance(e, dict) and e.get("prefix") == ANSWERS_PREFIX]
    if not entries:
        raise Refused(f'{where} has no `paths:` entry with prefix "{ANSWERS_PREFIX}"; add:\n{OWNER_ENTRY}')
    role = entries[0].get("owner_role")
    if not isinstance(role, str) or not role.strip():
        raise Refused(
            f'the `paths:` entry for "{ANSWERS_PREFIX}" in {where} has no `owner_role:`; '
            "add `owner_role: <a role declared under roles:>` to it"
        )
    roles = doc.get("roles")
    if not isinstance(roles, dict) or role not in roles:
        raise Refused(
            f"`owner_role: {role}` in {where} names no role under `roles:`; "
            f"add `{role}:` under `roles:`, or name a role that is there"
        )
    return role


def message_path(root: Path) -> Path:
    """Where the commit message goes: the file `git rev-parse --git-path ADR_ANSWER_MSG` names."""

    def git(*args: str) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)
        except FileNotFoundError as exc:
            raise Refused("git is not installed; the commit message has nowhere to go") from exc

    inside = git("rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        raise Refused(f"{root} is not a git work tree; the commit message has nowhere to go")
    where = git("rev-parse", "--git-path", MESSAGE_FILE)
    if where.returncode != 0 or not where.stdout.strip():
        raise Refused(f"git rev-parse --git-path {MESSAGE_FILE} failed: {where.stderr.strip() or where.returncode}")
    path = Path(where.stdout.strip())
    return path if path.is_absolute() else root / path


# ---------------------------------------------------------------------------
# writing — the same for both ways in
# ---------------------------------------------------------------------------


def render_answer(feature: gate.Feature, answer: str, reason: str, role: str, today: date) -> str:
    data = {
        "schema_version": 1,
        "change": feature.change,
        "question": "adr",
        "answer": answer,
        "reason": reason,
        "shown": {"proposed": feature.proposed, "proposal_reason": feature.proposal_reason},
        "answered_by": role,
        "answered_at": today,
    }
    # safe_dump quotes `'no'` and `'yes'`, which YAML 1.1 would read as booleans.
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def render_message(answers: list[tuple[gate.Feature, str, str]], tail: list[str]) -> str:
    if len(answers) == 1:
        subject = f"docs(decisions): ADR answer for {answers[0][0].change}"
    else:
        subject = f"docs(decisions): ADR answers for {len(answers)} changes"
    lines = [subject, ""]
    for feature, answer, reason in answers:
        lines.append(f"- {feature.change}: {'an ADR' if answer == 'yes' else 'no ADR'} — {reason}")
    return "\n".join([*lines, "", *tail]) + "\n"


def write(
    root: Path,
    answers: list[tuple[gate.Feature, str, str]],
    tail: list[str],
    *,
    out: Out,
    today: date,
    role: str,
    message: Path,
) -> int:
    """Render every answer, re-read each through the gate's reader, and only then write."""
    rendered: list[tuple[Path, str]] = []
    for feature, answer, reason in answers:
        text = render_answer(feature, answer, reason, role, today)
        data, problems = gate.parse_answer(text)
        if problems or data["change"] != feature.change:
            out(f"refused: the answer for {feature.change} would not pass the gate ({'; '.join(problems)})")
            out("Nothing was written.")
            return 2
        rendered.append((root / gate.answer_rel(feature.change), text))
    for path, text in rendered:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    message.write_text(render_message(answers, tail), encoding="utf-8")

    for path, _ in rendered:
        out(f"wrote {path.relative_to(root).as_posix()}")
    out(f"wrote the commit message to {message}")
    out("Left to do — this command stages, commits and merges nothing:")
    out(f"  1. git add {gate.ANSWERS_DIR}")
    out(f"  2. git commit -F {message}")
    out(
        f"  3. carry it in a decision pull request (label decision, body from {TEMPLATE}); "
        "it takes effect when the maintainer merges that pull request, or asks for the merge"
    )
    return 0


# ---------------------------------------------------------------------------
# the two ways in
# ---------------------------------------------------------------------------


def _ask_until(ask: Ask, out: Out, prompt: str, problem: Callable[[str], str | None]) -> str:
    while True:
        text = ask(prompt).strip()
        why = problem(text)
        if why is None:
            return text
        out(why)


def _yes_no(text: str) -> str | None:
    return None if text in ("y", "n") else "Answer y or n."


def _sentence(text: str) -> str | None:
    why = gate.reason_problem(text)
    return None if why is None else f"This line {why}; start it with a capital letter or a backtick."


def decide_adr(root: Path, *, ask: Ask, out: Out, today: date, role: str, message_path: Path) -> int:
    """Criterion 7: the maintainer answers each open question in a terminal."""
    ex = gate.examine(root)
    blocking = [line for _, line in ex.anchor_findings] + [line for _, line in ex.answer_findings]
    if blocking:
        for line in blocking:
            out(line)
        out("Stopped before asking: fix these first. Nothing was written.")
        return 2
    open_ = ex.missing
    if not open_:
        out(f"No open ADR question — each of the {len(ex.features)} features has its answer file.")
        return 0

    answers: list[tuple[gate.Feature, str, str]] = []
    explained: list[str] = []
    try:
        for i, feature in enumerate(open_, 1):
            out("")
            out(f"ADR question {i} of {len(open_)} — change {feature.change}")
            out(f"  Title:    {feature.title}")
            out(f"  Anchor:   {feature.anchor.rel}")
            if feature.outcome:
                out(f"  Outcome:  {feature.outcome}")
            out(f"  Proposal: {feature.proposed} — {feature.proposal_reason}")
            yn = _ask_until(ask, out, "Does this change need an architecture decision record (ADR)? [y/n] ", _yes_no)
            reason = _ask_until(ask, out, "Your reason, in one sentence: ", _sentence)
            answers.append((feature, "yes" if yn == "y" else "no", reason))
        out("")
        out("Explain back, in three lines, what you decided and what follows from it.")
        for k in (1, 2, 3):
            explained.append(_ask_until(ask, out, f"  Line {k}: ", _sentence))
    except (EOFError, KeyboardInterrupt):
        out("")
        out("Interrupted — nothing was written.")
        return 1

    tail = ["Explained back by the maintainer:", *(f"- {line}" for line in explained)]
    return write(root, answers, tail, out=out, today=today, role=role, message=message_path)


def _why_not_a_feature(ex: gate.Examination, change: str) -> str:
    named = [a for a in ex.anchors if a.name == change]
    if not named:
        return f"no change anchor names `{change}` (looked under {gate.CHANGES_DIR}/ and its archive)"
    for anchor in named:
        lines = [line for a, line in ex.anchor_findings if a == anchor]
        if lines:
            return "its anchor has findings:\n" + "\n".join(lines)
        cls = ex.classes.get(anchor.rel)
        if cls and cls != "feature":
            return f"{anchor.rel} states `class: {cls}`, and only a feature owes an answer"
    return f"no feature with a readable anchor names `{change}`"


def record_adr(
    root: Path,
    change: str,
    answer: str,
    reason: str,
    stated_in: str,
    *,
    out: Out,
    today: date,
    role: str,
    message_path: Path,
) -> int:
    """Criterion 9: record one answer the maintainer stated elsewhere, without a terminal."""
    if answer not in ("yes", "no"):
        raise Refused(f"--answer must be yes or no, is {answer!r}")
    reason = reason.strip()
    if why := gate.reason_problem(reason):
        raise Refused(f"--reason {why}")
    ex = gate.examine(root)
    feature = next((f for f in ex.features if f.change == change), None)
    if feature is None:
        raise Refused(f"`{change}` is not a feature with a readable anchor: {_why_not_a_feature(ex, change)}")
    if (root / gate.answer_rel(change)).exists():
        raise Refused(
            f"{gate.answer_rel(change)} exists already; an existing answer changes only by an edit in a decision pull request"
        )
    tail = [f"Stated by the maintainer in: {stated_in.strip()}"]
    return write(root, [(feature, answer, reason)], tail, out=out, today=today, role=role, message=message_path)


# ---------------------------------------------------------------------------
# the command line
# ---------------------------------------------------------------------------


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="harness.py", description=(__doc__ or "").split("\n")[0], allow_abbrev=False)
    verbs = ap.add_subparsers(dest="verb", required=True, metavar="verb")
    decide = verbs.add_parser(
        "decide", help="put a question to the maintainer and record the answer", allow_abbrev=False
    )
    questions = decide.add_subparsers(dest="question", required=True, metavar="question")
    adr = questions.add_parser("adr", help="the ADR question of every feature without an answer", allow_abbrev=False)
    adr.add_argument("--change", help="record: the change the maintainer answered for")
    adr.add_argument("--answer", help="record: yes or no, as the maintainer stated it")
    adr.add_argument("--reason", help="record: the maintainer's reason, one English sentence")
    adr.add_argument("--stated-in", help="record: where the maintainer stated it (a session, a comment)")
    adr.add_argument("--root", type=Path, default=REPO_ROOT, help="repository to work in (default: this one)")
    return ap


def main(argv: list[str] | None = None, *, ask: Ask = input, out: Out = print, today: date | None = None) -> int:
    args = parser().parse_args(argv)
    root: Path = args.root.resolve()
    given: dict[str, Any] = {name: getattr(args, name) for name in RECORDING}
    try:
        if any(v is not None for v in given.values()):
            flags = {name: "--" + name.replace("_", "-") for name in RECORDING}
            absent = [flags[n] for n, v in given.items() if v is None or not str(v).strip()]
            if absent:
                raise Refused(
                    f"recording an answer needs all four of {', '.join(flags.values())}; missing or blank: {', '.join(absent)}"
                )
        role = answering_role(root)
        message = message_path(root)
        day = today or date.today()
        if given["change"] is not None:
            return record_adr(
                root,
                given["change"],
                given["answer"],
                given["reason"],
                given["stated_in"],
                out=out,
                today=day,
                role=role,
                message_path=message,
            )
        if not sys.stdin.isatty():
            raise Refused(
                "run this yourself in a terminal — the questions are for the maintainer to answer; "
                "an answer stated elsewhere is recorded with --change, --answer, --reason and --stated-in"
            )
        return decide_adr(root, ask=ask, out=out, today=day, role=role, message_path=message)
    except Refused as exc:
        out(f"refused: {exc}")
        out("Nothing was written.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
