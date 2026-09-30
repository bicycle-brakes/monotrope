"""The barrier before a foreign endpoint - and the cases in which it holds.

`model-endpoints.yaml` declares which endpoint may see which data class, and a
declaration stops nothing. `scripts/leakcheck.py` stands between the rule and
the data flowing out, and every case here builds its own repository and its own
denylist: nothing reads the maintainer's real denylist or this repository's
history.

The most important test is `test_the_report_never_carries_the_match`: a gate
whose output has to be handled like a secret is the second disclosure, so the
whole output is searched for the planted value, not the function's intent.
"""

from __future__ import annotations

import os
import random
import re
import string
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import leakcheck  # noqa: E402

RULE = "planted = [a-z]{32}"
OTHER_RULE = "second = never-present-in-the-fixture"
SECRET = "".join(random.Random(20260930).choices(string.ascii_lowercase, k=32))

# The exit codes of `_verdict.py`: clean, and a match or "cannot measure".
CLEAN = 0
BLOCKED = 2


@pytest.fixture(autouse=True)
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A home, a denylist path and a git configuration that belong to the test."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("LEAKCHECK_DENYLIST", str(tmp_path / "denylist.txt"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))


def git(cwd: Path, *args: str) -> str:
    run = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return run.stdout.strip()


def write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def denylist(tmp_path: Path) -> Path:
    path = tmp_path / "denylist.txt"
    path.write_text(f"# a comment\n\n{RULE}\n{OTHER_RULE}\n", encoding="utf-8")
    return path


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Two commits on `main`, one untracked file, one ignored file in the change folder."""
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "--quiet", "--initial-branch=main")
    write(root, ".gitignore", "*.log\n")
    write(root, "plans/changes/demo/spec.md", "# Spec\n\nHarmless text.\n")
    write(root, "src/code.txt", "harmless = 1\n")
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", "first")
    write(root, "README.md", "# Readme\n")
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", "second")
    write(root, "notes.txt", "harmless notes\n")
    write(root, "plans/changes/demo/run.log", "ignored by git, in the change folder\n")
    write(root, "build.log", "ignored by git, outside the change folder\n")
    return root


def run_check(
    root: Path, denylist: Path, name: str = "demo", prompts: tuple[tuple[str, str], ...] = ()
) -> leakcheck.Result:
    return leakcheck.check(name, denylist, root, prompts)


def rendered(result: leakcheck.Result) -> str:
    return result.verdict.render()


# ---------------------------------------------------------------------------
# The verdict on a clean tree
# ---------------------------------------------------------------------------


def test_a_clean_tree_passes_and_names_its_counts(repo: Path, denylist: Path) -> None:
    """Exact numbers: six files, two commits, two rules - and a prompt text when there is one."""
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == CLEAN
    assert "leak check clean: 6 files, 2 commits, 2 rules" in rendered(result)
    assert (result.files, result.commits, result.rules) == (6, 2, 2)

    with_prompt = run_check(repo, denylist, prompts=(("prompt", "nothing to see\n"),))
    assert with_prompt.verdict.exit_code() == CLEAN
    assert "leak check clean: 6 files, 2 commits, 2 rules, 1 prompt texts" in rendered(with_prompt)


# ---------------------------------------------------------------------------
# A match anywhere in the scanned set goes red
# ---------------------------------------------------------------------------


def _in_a_change_file(root: Path) -> str:
    write(root, "plans/changes/demo/plan.md", f"value: {SECRET}\n")
    return "plans/changes/demo/plan.md:1"


def _in_an_uncommitted_edit(root: Path) -> str:
    write(root, "src/code.txt", f"harmless = 1\nvalue = {SECRET}\n")
    return "src/code.txt:2"


def _in_an_untracked_file(root: Path) -> str:
    write(root, "src/new.txt", f"{SECRET}\n")
    return "src/new.txt:1"


def _in_a_commit_message(root: Path) -> str:
    git(root, "commit", "--quiet", "--allow-empty", "-m", f"subject\n\nbody {SECRET}")
    return f"commit {git(root, 'rev-parse', 'HEAD')[:12]}:"


def _in_an_earlier_commits_patch(root: Path) -> str:
    write(root, "src/old.txt", f"{SECRET}\n")
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", "adds a value")
    sha = git(root, "rev-parse", "HEAD")[:12]
    git(root, "rm", "--quiet", "src/old.txt")
    git(root, "commit", "--quiet", "-m", "removes it again")
    return f"commit {sha}:"


def _in_a_remote_only_commit(root: Path) -> str:
    """A commit that no local branch reaches, only `refs/remotes/origin/side`."""
    git(root, "checkout", "--quiet", "-b", "side")
    write(root, "src/side.txt", f"{SECRET}\n")
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", "on the side")
    sha = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "--quiet", "main")
    git(root, "update-ref", "refs/remotes/origin/side", sha)
    git(root, "branch", "--quiet", "-D", "side")
    return f"commit {sha[:12]}:"


PLANTS = {
    "change file": _in_a_change_file,
    "uncommitted edit": _in_an_uncommitted_edit,
    "untracked file": _in_an_untracked_file,
    "commit message": _in_a_commit_message,
    "earlier commit's patch": _in_an_earlier_commits_patch,
    "commit only on a remote-tracking branch": _in_a_remote_only_commit,
}


@pytest.mark.parametrize("where", sorted(PLANTS))
def test_a_match_anywhere_in_the_scanned_set_goes_red(where: str, repo: Path, denylist: Path) -> None:
    assert run_check(repo, denylist).verdict.exit_code() == CLEAN, "the fixture is clean before the plant"
    place = PLANTS[where](repo)
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == BLOCKED, f"a match in the {where} was not found"
    assert place in rendered(result)


def test_a_match_in_a_prompt_text_goes_red(repo: Path, denylist: Path) -> None:
    result = run_check(repo, denylist, prompts=(("prompt", f"first line\nsecond {SECRET}\n"),))
    assert result.verdict.exit_code() == BLOCKED
    assert "prompt text prompt:2" in rendered(result)


def test_a_symbolic_link_is_read_as_its_targets_text(repo: Path, denylist: Path, tmp_path: Path) -> None:
    """A link to a file outside the repository still hands that file's text to the reviewer."""
    outside = write(tmp_path, "outside.txt", f"{SECRET}\n")
    (repo / "link.txt").symlink_to(outside)
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == BLOCKED
    assert "link.txt:1" in rendered(result)


def test_a_link_to_a_directory_is_refused_not_skipped(repo: Path, denylist: Path, tmp_path: Path) -> None:
    """Repair round 1, F-5: a reviewer reads through the link; a check that skips it is green over unread content."""
    outside = tmp_path / "outside"
    write(outside, "note.txt", f"{SECRET}\n")
    (repo / "customer").symlink_to(outside, target_is_directory=True)
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == BLOCKED
    assert "customer" in rendered(result) and "not a regular file" in rendered(result)
    assert SECRET not in rendered(result)


@pytest.mark.parametrize("added", [True, False], ids=["submodule-entry", "nested-repository"])
def test_a_nested_repository_is_refused_not_skipped(repo: Path, denylist: Path, added: bool) -> None:
    """Repair round 1, F-5: a submodule's directory, or a repository nested in the tree, holds files the check did not read."""
    nested = repo / "vendor"
    nested.mkdir()
    git(nested, "init", "--quiet", "--initial-branch=main")
    write(nested, "inside.txt", f"{SECRET}\n")
    git(nested, "add", "-A")
    git(nested, "commit", "--quiet", "-m", "inside")
    if added:
        git(repo, "add", "vendor")
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == BLOCKED
    assert "vendor" in rendered(result) and "not a regular file" in rendered(result)


def test_a_dangling_link_is_read_as_its_own_text(repo: Path, denylist: Path) -> None:
    """Repair round 1, F-5: nothing stands behind the link, but its target text is what git shows of it."""
    (repo / "dangling").symlink_to(SECRET)
    assert run_check(repo, denylist).verdict.exit_code() == BLOCKED
    (repo / "dangling").unlink()
    (repo / "dangling").symlink_to("harmless-target")
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == CLEAN and (result.files, result.commits) == (7, 2)


def test_a_tracked_file_that_is_gone_from_the_disk_is_not_a_refusal(repo: Path, denylist: Path) -> None:
    """Nothing is on the disk to read; the staged deletion is what the index scan sees."""
    (repo / "src" / "code.txt").unlink()
    assert run_check(repo, denylist).verdict.exit_code() == CLEAN


def test_a_value_staged_and_then_taken_out_of_the_file_is_still_found(repo: Path, denylist: Path) -> None:
    """Repair round 1, F-6: `git show :<path>` reads the index, whatever the working file says now."""
    write(repo, "src/staged.txt", f"{SECRET}\n")
    git(repo, "add", "src/staged.txt")
    write(repo, "src/staged.txt", "clean again\n")
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == BLOCKED
    assert "staged changes" in rendered(result)
    git(repo, "rm", "--quiet", "--force", "src/staged.txt")
    assert run_check(repo, denylist).verdict.exit_code() == CLEAN, "the staged value left the index with the file"


def test_the_advice_does_not_claim_a_rewritten_commit_is_clean(repo: Path, denylist: Path) -> None:
    """Repair round 1, F-6: a match in a commit is not gone when the commit is rewritten; the reflog still holds it."""
    place = _in_an_earlier_commits_patch(repo)
    text = rendered(run_check(repo, denylist))
    assert place in text and "reflog" in text


def test_the_advice_for_a_file_does_not_talk_about_the_reflog(repo: Path, denylist: Path) -> None:
    """The limit is named where it applies: a file on the disk is cleaned by editing it."""
    _in_an_untracked_file(repo)
    text = rendered(run_check(repo, denylist))
    assert "src/new.txt:1" in text and "reflog" not in text


def test_the_limits_of_the_scanned_set_are_stated() -> None:
    """Repair round 1, F-6: what the check does not read stands in its own text and in the doctrine."""
    doc = " ".join((leakcheck.__doc__ or "").split())
    workflow = " ".join((REPO_ROOT / "docs" / "WORKFLOW.md").read_text(encoding="utf-8").split())
    for text in (doc, workflow):
        assert "reflog" in text and "stash" in text and "staged" in text


def test_a_file_is_read_whatever_its_suffix(repo: Path, denylist: Path) -> None:
    (repo / "picture.png").write_bytes(b"\x89PNG\r\n\x00\xff" + SECRET.encode() + b"\n")
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == BLOCKED
    assert "picture.png:" in rendered(result)


# ---------------------------------------------------------------------------
# A check that cannot measure refuses
# ---------------------------------------------------------------------------


def _skip_as_root() -> None:
    if os.geteuid() == 0:
        pytest.skip("mode 000 does not stop root")


def test_a_check_that_cannot_measure_refuses(repo: Path, denylist: Path, tmp_path: Path) -> None:
    """Each case: exit 2 and the reason. An unchecked tree is not a clean one."""
    cases: list[tuple[str, leakcheck.Result, str]] = []

    cases.append(("denylist missing", run_check(repo, tmp_path / "nowhere.txt"), "is missing"))

    empty = tmp_path / "empty.txt"
    empty.write_text("# only a comment\n\n", encoding="utf-8")
    cases.append(("denylist empty", run_check(repo, empty), "holds no rule"))

    invalid = tmp_path / "invalid.txt"
    invalid.write_text("first = fine\nbroken = [unfinished\n", encoding="utf-8")
    cases.append(("denylist invalid pattern", run_check(repo, invalid), "line 2"))

    cases.append(("no name", run_check(repo, denylist, name=""), "no valid change name"))
    cases.append(("a name with a slash", run_check(repo, denylist, name="a/b"), "no valid change name"))
    cases.append(("a name that is a dot", run_check(repo, denylist, name=".."), "no valid change name"))
    cases.append(("folder missing", run_check(repo, denylist, name="absent"), "does not exist"))

    (repo / "plans/changes/hollow").mkdir()
    cases.append(("folder empty", run_check(repo, denylist, name="hollow"), "holds no file"))

    plain = tmp_path / "plain"
    write(plain, "plans/changes/demo/spec.md", "# Spec\n")
    cases.append(("not a repository", run_check(plain, denylist), "the tree cannot be listed"))

    for label, result, reason in cases:
        assert result.verdict.exit_code() == BLOCKED, f"{label}: expected exit 2"
        assert reason in result.verdict.render(), f"{label}: the reason is missing"


def test_an_unreadable_denylist_or_file_refuses(repo: Path, denylist: Path) -> None:
    _skip_as_root()
    denylist.chmod(0)
    try:
        result = run_check(repo, denylist)
        assert result.verdict.exit_code() == BLOCKED
        assert "cannot be read" in rendered(result)
    finally:
        denylist.chmod(0o644)

    locked = write(repo, "plans/changes/demo/locked.md", "text\n")
    locked.chmod(0)
    try:
        result = run_check(repo, denylist)
        assert result.verdict.exit_code() == BLOCKED
        assert "plans/changes/demo/locked.md cannot be read" in rendered(result)
    finally:
        locked.chmod(0o644)


def test_a_history_that_cannot_be_read_refuses(repo: Path, denylist: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    real = leakcheck._git

    def refuses_the_log(root: Path, *args: str):
        if args and args[0] == "log":
            return None, "git exited 128"
        return real(root, *args)

    monkeypatch.setattr(leakcheck, "_git", refuses_the_log)
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == BLOCKED
    assert "the history cannot be read" in rendered(result)


# ---------------------------------------------------------------------------
# The report never carries the match
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("denylist")
def test_the_report_never_carries_the_match(repo: Path) -> None:
    """Thirty-two planted letters: no run of eight of them, and no pattern, in stdout or stderr."""
    write(repo, "src/leak.txt", f"value = {SECRET}\n")
    run = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "leakcheck.py"), "--name", "demo", "--root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
        env=os.environ.copy(),
    )
    output = run.stdout + run.stderr
    assert run.returncode == BLOCKED
    for start in range(len(SECRET) - 7):
        assert SECRET[start : start + 8] not in output, "a part of the match is in the report"
    assert "[a-z]{32}" not in output, "the rule's pattern is in the report"
    assert "src/leak.txt:1" in output, "without a place the finding cannot be fixed"
    assert "'planted'" in output, "the rule's name is missing"
    assert "length 32" in output, "the match's length is missing"


def test_an_invalid_pattern_is_named_by_line_and_never_by_text(repo: Path, tmp_path: Path) -> None:
    broken = tmp_path / "broken.txt"
    broken.write_text("fine = ok\nsecret-looking-text = ([unfinished\n", encoding="utf-8")
    text = rendered(run_check(repo, broken))
    assert "line 2" in text
    assert "unfinished" not in text


# ---------------------------------------------------------------------------
# The command line
# ---------------------------------------------------------------------------


def test_the_cli_returns_the_exit_code_and_reads_a_prompt_file(
    repo: Path, denylist: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    prompt = write(tmp_path, "prompt.md", f"asks about {SECRET}\n")
    args = ["--name", "demo", "--root", str(repo), "--denylist", str(denylist)]
    assert leakcheck.main(args) == CLEAN
    assert leakcheck.main([*args, "--prompt-file", str(prompt)]) == BLOCKED
    assert "prompt text prompt.md:1" in capsys.readouterr().out
    assert leakcheck.main([*args, "--prompt-file", str(tmp_path / "missing.md")]) == BLOCKED


# ---------------------------------------------------------------------------
# The suite never reaches the real denylist
# ---------------------------------------------------------------------------


def test_the_suite_never_reaches_the_real_denylist_or_secrets(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The default denylist is read at call time, so a test's HOME and variable hold."""
    assert leakcheck.default_denylist() == tmp_path / "denylist.txt"

    monkeypatch.delenv("LEAKCHECK_DENYLIST")
    default = leakcheck.default_denylist()
    assert default == tmp_path / "home" / ".config" / "cc-routing" / "denylist.txt"
    assert not default.exists()

    other = tmp_path / "other-home"
    monkeypatch.setenv("HOME", str(other))
    assert leakcheck.default_denylist() == other / ".config" / "cc-routing" / "denylist.txt"
    assert re.search(r"cc-routing", str(default)), "the documented default path changed"
