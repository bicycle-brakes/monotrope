#!/usr/bin/env python3
"""leakcheck.py - what goes to a foreign endpoint is looked at first.

**What this stands against.** `model-endpoints.yaml` declares which endpoint may
see which data class, and a declaration stops nothing. Between the rule and the
data flowing out stands this script, and the stage-2 runner
(`scripts/stage2.py`) calls it in the same invocation, immediately before every
foreign call.

**What is scanned** (the scanned set):

    a. every file under `plans/changes/<name>/`;
    b. every file of the worktree that git tracks or lists as untracked and not
       ignored, as it stands on disk, whatever its suffix - a symbolic link to a
       file as its target's text, a link with nothing behind it as its own text;
    c. the message and the patch of every commit reachable from a local or a
       remote-tracking branch (merges with `--cc`: what a merge adds beyond its
       parents);
    d. the staged changes (`git diff --cached`): a value staged and then taken
       out of the working file stays readable with `git show :<path>`;
    e. every text the caller says it puts into a prompt (`--prompt-file`).

A foreign reviewer's tools read the tree and the history, so the check looks at
the tree and the history, not only at the change.

**What is NOT scanned, stated so that a clean report is not read as more.** The
reflog: rewriting a commit that held a value (amend, rebase) makes the check
clean, and `git log -g -p` still shows the value until git expires the reflog.
The stash (`refs/stash`), refs outside `refs/heads` and `refs/remotes` (tags,
`refs/dolt/`) and objects no ref reaches. After a rewrite, `git reflog expire
--expire=now --all` and `git gc --prune=now` are what remove those copies; the
check cannot say that they were run (measured in a temporary repository,
2026-09-30).

**What is NOT printed: the match.** A gate whose output has to be handled like
a secret is the second disclosure. The report names the place (file and line,
or commit and line of its patch, or the prompt text and its line), the rule's
name and the length of the match. It never prints the matched text and never a
rule's pattern.

**If it cannot measure, it refuses.** A denylist that is missing, unreadable,
empty or invalid, no change name, a change folder that is missing or empty, a
tree that cannot be listed, a file that cannot be read, a listed path that is
not a regular file (a link to a directory, a submodule, a repository nested in
the tree, a special file: a reviewer reads through it and this check does not),
an index or a history that cannot be read: each one is a BLOCK that names why.
Unchecked is not clean.

The denylist lives **outside the repository**: it names what is searched for,
and that is itself a statement about the customer. Default:
`~/.config/cc-routing/denylist.txt`, overridden by `--denylist` or by the
variable `LEAKCHECK_DENYLIST`. Format: one rule per line, `name = regex`; a
line from `#` on is a comment; a line without `name =` is the whole pattern and
its name is `line-<n>`.

Call:
    python3 scripts/leakcheck.py --name <change> [--denylist PATH]
                                 [--prompt-file PATH ...]
Exit: 0 clean, 2 a match or cannot measure (the vocabulary of `_verdict.py`).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _verdict import Verdict  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

# The marker that opens each commit in the history text. A NUL cannot occur in
# a commit message, and a patch line starts with a space, a plus or a minus.
COMMIT_MARK = "commit\x00"


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]


@dataclass
class Result:
    """The verdict and the three numbers the report states."""

    verdict: Verdict
    files: int = 0
    commits: int = 0
    rules: int = 0


def default_denylist() -> Path:
    """The denylist when none is named. Read at call time, never at import."""
    named = os.environ.get("LEAKCHECK_DENYLIST")
    if named:
        return Path(named)
    return Path.home() / ".config" / "cc-routing" / "denylist.txt"


def read_denylist(path: Path) -> tuple[list[Rule], str | None]:
    """The rules, or the reason there are none.

    A missing denylist is not an empty result but an unknown one. An invalid
    pattern is named by its line number, never by its text.
    """
    if not path.is_file():
        return [], f"the denylist {path} is missing"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return [], f"the denylist {path} cannot be read"

    rules: list[Rule] = []
    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, _, rest = line.partition("=")
        if rest:
            name, pattern = name.strip(), rest.strip()
        else:
            name, pattern = f"line-{number}", line
        try:
            rules.append(Rule(name, re.compile(pattern)))
        except re.error:
            return [], f"the denylist {path}, line {number}, holds a pattern that is not valid"

    if not rules:
        return [], f"the denylist {path} holds no rule"
    return rules, None


ADVICE = {
    "file": "The matched text is not shown. Open the place, remove or replace the value, run the check again.",
    "staged": (
        "The matched text is not shown. The value is in the index: take it out of the file, stage the file "
        "again, run the check again."
    ),
    "commit": (
        "The matched text is not shown. Rewriting the commit does not make the value gone: the reflog and the "
        "stash still hold it until git expires them (`git reflog expire --expire=now --all`, then `git gc "
        "--prune=now`), and this check does not look there. Run the check again after."
    ),
}


def _scan(text: str, prefix: str, rules: list[Rule], verdict: Verdict, kind: str = "file") -> int:
    """Report each match as a place, a rule name and a length. Returns the count."""
    hits = 0
    for number, line in enumerate(text.split("\n"), 1):
        for rule in rules:
            found = rule.pattern.search(line)
            if found:
                hits += 1
                verdict.block(
                    f"{prefix}:{number} - rule '{rule.name}' matches (length {len(found.group(0))})",
                    ADVICE[kind],
                )
    return hits


def _git(root: Path, *args: str) -> tuple[bytes | None, str]:
    """Run git in `root`. Returns the output, or None and a short reason."""
    try:
        run = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            check=False,
        )
    except OSError:
        return None, "git cannot be started"
    if run.returncode != 0:
        return None, f"git exited {run.returncode}"
    return run.stdout, ""


def _refuse(reason: str, detail: str) -> Result:
    result = Result(Verdict())
    result.verdict.block(reason, detail)
    return result


def _history_units(text: str) -> Iterable[tuple[str, str]]:
    """Split the history text into (sha12, text) per commit."""
    sha = ""
    lines: list[str] = []
    started = False
    for line in text.split("\n"):
        if line.startswith(COMMIT_MARK):
            if started:
                yield sha, "\n".join(lines)
            started = True
            sha = line[len(COMMIT_MARK) :].strip()[:12]
            lines = []
        elif started:
            lines.append(line)
    if started:
        yield sha, "\n".join(lines)


def check(
    name: str,
    denylist: Path,
    root: Path = REPO_ROOT,
    prompt_texts: Iterable[tuple[str, str]] = (),
) -> Result:
    """Scan the scanned set under `root` against the denylist."""
    if not name or "/" in name or name in {".", ".."}:
        return _refuse(
            "no valid change name",
            "Name the change folder under plans/changes/ (a single folder name). Without it the check cannot say what goes out.",
        )

    rules, reason = read_denylist(denylist)
    if reason is not None:
        return _refuse(
            "no rule set to check against - the call does not start",
            f"{reason}. Unchecked is not clean: without rules this script would report success over an empty set.",
        )

    folder = root / "plans" / "changes" / name
    if not folder.is_dir():
        return _refuse(
            f"plans/changes/{name}/ does not exist",
            "Without the change's artifacts it cannot be checked what goes into the call.",
        )
    change_files = [p for p in sorted(folder.rglob("*")) if p.is_file()]
    if not change_files:
        return _refuse(
            f"plans/changes/{name}/ holds no file",
            "An empty folder is a finding, not a scan that passed.",
        )

    listed, why = _git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if listed is None:
        return _refuse(
            "the tree cannot be listed",
            f"{why}. What cannot be listed is not checked, and it would go into the call all the same.",
        )
    result = Result(Verdict(), rules=len(rules))
    tree_files: list[Path] = []
    link_texts: dict[str, str] = {}
    unreadable = False
    for part in listed.decode("utf-8", errors="replace").split("\0"):
        if not part:
            continue
        path, name = root / part, part.rstrip("/")
        if path.is_file():
            tree_files.append(path)
        elif path.is_symlink() and not path.exists():
            # Nothing stands behind the link, but the link's own text is what git shows of it.
            link_texts[name] = str(path.readlink())
        elif path.exists():
            unreadable = True
            result.verdict.block(
                f"{name} is listed by git but is not a regular file",
                "A link to a directory, a submodule, a repository nested in the tree or a special file: a "
                "reviewer reads through it and this check did not. What cannot be scanned is not checked.",
            )
        # else: listed and gone from the disk - nothing to read there; a staged deletion shows in the index scan.

    scanned: dict[str, Path] = {}
    for path in (*change_files, *tree_files):
        scanned.setdefault(path.relative_to(root).as_posix(), path)

    hits = 0
    for relative, path in scanned.items():
        try:
            text = path.read_bytes().decode("utf-8", errors="replace")
        except OSError:
            unreadable = True
            result.verdict.block(
                f"{relative} cannot be read",
                "What cannot be read is not checked, and it goes into the call all the same.",
            )
            continue
        hits += _scan(text, relative, rules, result.verdict)
    for relative, text in link_texts.items():
        hits += _scan(text, relative, rules, result.verdict)
    if unreadable:
        return result
    result.files = len(scanned) + len(link_texts)

    staged, why = _git(
        root, "diff", "--cached", "--text", "--no-color", "--no-ext-diff", "--no-textconv", "--no-renames"
    )
    if staged is None:
        return _refuse(
            "the index cannot be read",
            f"{why}. The index is what `git show :<path>` reads; skipping it would leave a staged value unchecked.",
        )
    hits += _scan(
        staged.decode("utf-8", errors="replace"), "staged changes (git diff --cached)", rules, result.verdict, "staged"
    )

    history, why = _git(
        root,
        "log",
        "--branches",
        "--remotes",
        "--cc",
        "-p",
        "--text",
        "--no-color",
        "--no-ext-diff",
        "--no-textconv",
        "--no-show-signature",
        "--format=commit%x00%H%n%B",
    )
    if history is None:
        return _refuse(
            "the history cannot be read",
            f"{why}. The history is what a reviewer's tools can read; skipping it would leave half of it unchecked.",
        )
    for sha, text in _history_units(history.decode("utf-8", errors="replace")):
        result.commits += 1
        hits += _scan(text, f"commit {sha}", rules, result.verdict, "commit")

    labelled = list(prompt_texts)
    for label, text in labelled:
        hits += _scan(text, f"prompt text {label}", rules, result.verdict)

    if hits == 0:
        report = f"leak check clean: {result.files} files, {result.commits} commits, {result.rules} rules"
        if labelled:
            report += f", {len(labelled)} prompt texts"
        result.verdict.info(report)
    return result


def _read_prompt_files(paths: list[str]) -> tuple[list[tuple[str, str]], str | None]:
    texts: list[tuple[str, str]] = []
    for raw in paths:
        path = Path(raw)
        try:
            texts.append((path.name, path.read_bytes().decode("utf-8", errors="replace")))
        except OSError:
            return [], f"the prompt file {path.name} cannot be read"
    return texts, None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument("--name", default="", help="folder name under plans/changes/")
    parser.add_argument("--denylist", default=None, help="the rule file (default: see above)")
    parser.add_argument(
        "--prompt-file",
        action="append",
        default=[],
        help="a text that goes into a prompt, scanned as well (repeatable)",
    )
    parser.add_argument("--root", default=str(REPO_ROOT), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    denylist = Path(args.denylist) if args.denylist else default_denylist()
    prompts, why = _read_prompt_files(args.prompt_file)
    if why is not None:
        result = _refuse(why, "A text that goes into a prompt and cannot be read is a text that is not checked.")
    else:
        result = check(args.name, denylist, Path(args.root), prompts)
    print(result.verdict.render())
    return result.verdict.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
