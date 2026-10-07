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


@pytest.mark.parametrize("flag", ["skip-worktree", "assume-unchanged"])
def test_the_staged_changes_are_read_against_the_last_commit_not_the_working_file(
    repo: Path, denylist: Path, flag: str
) -> None:
    """Repair round 2 (F-6 note): plain `git diff` compares the index with the working file and is blind to an
    entry git was told to assume unchanged; `git diff --cached` compares it with `HEAD` and is not."""
    write(repo, "src/code.txt", f"{SECRET}\n")
    git(repo, "add", "src/code.txt")
    write(repo, "src/code.txt", "harmless = 1\n")
    git(repo, "update-index", f"--{flag}", "src/code.txt")
    assert git(repo, "diff", "--", "src/code.txt") == "", "the fixture no longer hides the entry from `git diff`"
    result = run_check(repo, denylist)
    assert result.verdict.exit_code() == BLOCKED and "staged changes" in rendered(result)
    git(repo, "update-index", f"--no-{flag}", "src/code.txt")
    git(repo, "reset", "--quiet", "--", "src/code.txt")
    assert run_check(repo, denylist).verdict.exit_code() == CLEAN


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
# The secret rules skip `tests/`; the others do not (maintainer, 2026-10-07, O-4)
# ---------------------------------------------------------------------------

CUSTOMER = "acme-" + SECRET[:8]
SECRET_RULE = "secret:planted = [a-z]{32}"
CUSTOMER_RULE = "customer = acme-[a-z]{8}"

# Folders whose files the secret rules skip, and folders that merely look like it.
EXEMPT_DIRS = ["tests", "tests/fixtures/deep"]
SCANNED_DIRS = ["src", "tests_extra", "docs/tests", "plans/changes/demo/tests", "mytests", "tests-old"]


@pytest.fixture
def split(tmp_path: Path) -> Path:
    """A denylist of one secret rule (marked) and one customer rule (unmarked)."""
    path = tmp_path / "split.txt"
    path.write_text(f"{SECRET_RULE}\n{CUSTOMER_RULE}\n", encoding="utf-8")
    return path


def commit_file(root: Path, relative: str, text: str) -> str:
    write(root, relative, text)
    git(root, "add", "--", relative)
    git(root, "commit", "--quiet", "-m", f"adds {relative}")
    return git(root, "rev-parse", "HEAD")[:12]


def commit_and_remove(root: Path, relative: str, text: str) -> str:
    """Only the patches of two commits hold the text afterwards: the tree and the index are clean again."""
    sha = commit_file(root, relative, text)
    git(root, "rm", "--quiet", "--", relative)
    git(root, "commit", "--quiet", "-m", f"removes {relative}")
    return sha


def test_a_rule_is_a_secret_rule_by_the_prefix_of_its_name(tmp_path: Path) -> None:
    path = tmp_path / "marked.txt"
    path.write_text(
        "secret:one = a\ntwo = b\nSecret:three = c\nsecret:four\n secret:five = e\nsecret: six = f\n",
        encoding="utf-8",
    )
    rules, why = leakcheck.read_denylist(path)
    assert why is None
    assert [(rule.name, rule.secret) for rule in rules] == [
        ("secret:one", True),  # the name is kept as written, prefix included
        ("two", False),
        ("Secret:three", False),  # exactly `secret:`, in lower case
        ("line-4", False),  # a line without `name =` is never marked
        ("secret:five", True),  # the line is stripped first
        ("secret: six", True),
    ]


@pytest.mark.parametrize("folder", EXEMPT_DIRS)
def test_a_secret_shaped_fixture_under_tests_passes(folder: str, repo: Path, split: Path) -> None:
    write(repo, f"{folder}/test_fixture.py", f'KEY = "{SECRET}"\n')
    result = run_check(repo, split)
    assert result.verdict.exit_code() == CLEAN, rendered(result)


@pytest.mark.parametrize("folder", SCANNED_DIRS)
def test_the_same_fixture_outside_tests_blocks(folder: str, repo: Path, split: Path) -> None:
    """`tests_extra/`, `docs/tests/`, a change's own `tests/` and a look-alike are not `tests/`."""
    write(repo, f"{folder}/test_fixture.py", f'KEY = "{SECRET}"\n')
    result = run_check(repo, split)
    assert result.verdict.exit_code() == BLOCKED
    assert f"{folder}/test_fixture.py:1 - rule 'secret:planted'" in rendered(result)


@pytest.mark.parametrize("folder", EXEMPT_DIRS)
def test_a_customer_rule_still_scans_tests(folder: str, repo: Path, split: Path) -> None:
    write(repo, f"{folder}/test_fixture.py", f'NAME = "{CUSTOMER}"\nKEY = "{SECRET}"\n')
    result = run_check(repo, split)
    assert result.verdict.exit_code() == BLOCKED
    text = rendered(result)
    assert f"{folder}/test_fixture.py:1 - rule 'customer'" in text
    assert "secret:planted" not in text, "the secret rule skipped the file, the customer rule did not"


def test_the_accepted_consequence_is_real_a_key_in_a_test_file_is_not_found(repo: Path, split: Path) -> None:
    """The maintainer's decision names it: under `tests/` the check cannot tell a real key from an invented one."""
    write(repo, "tests/test_real_looking.py", f'KEY = "{SECRET}"\n')
    assert run_check(repo, split).verdict.exit_code() == CLEAN


def test_the_report_of_a_clean_run_names_the_exemption(repo: Path, split: Path, denylist: Path) -> None:
    assert "2 rules (1 secret rule not applied under tests/)" in rendered(run_check(repo, split))
    assert "secret rule" not in rendered(run_check(repo, denylist)), "no marked rule, no remark"


def test_a_symbolic_link_under_tests_is_not_exempt(repo: Path, split: Path, tmp_path: Path) -> None:
    """A link can lead out of the folder, and a reviewer reads through it."""
    outside = write(tmp_path, "outside.txt", f"{SECRET}\n")
    (repo / "tests").mkdir()
    (repo / "tests" / "link.txt").symlink_to(outside)
    result = run_check(repo, split)
    assert result.verdict.exit_code() == BLOCKED
    assert "tests/link.txt:1 - rule 'secret:planted'" in rendered(result)


def test_a_dangling_link_under_tests_is_not_exempt(repo: Path, split: Path) -> None:
    (repo / "tests").mkdir()
    (repo / "tests" / "dangling").symlink_to(SECRET)
    result = run_check(repo, split)
    assert result.verdict.exit_code() == BLOCKED
    assert "tests/dangling:1" in rendered(result)


def test_a_prompt_text_is_never_exempt(repo: Path, split: Path) -> None:
    result = run_check(repo, split, prompts=(("tests/prompt.md", f"{SECRET}\n"),))
    assert result.verdict.exit_code() == BLOCKED
    assert "prompt text tests/prompt.md:1 - rule 'secret:planted'" in rendered(result)


@pytest.mark.parametrize("folder", EXEMPT_DIRS)
def test_a_commit_patch_that_touches_tests_follows_the_same_split(folder: str, repo: Path, split: Path) -> None:
    commit_and_remove(repo, f"{folder}/test_fixture.py", f'KEY = "{SECRET}"\n')
    result = run_check(repo, split)
    assert result.verdict.exit_code() == CLEAN, rendered(result)
    assert result.commits == 4

    sha = commit_and_remove(repo, f"{folder}/test_name.py", f'NAME = "{CUSTOMER}"\n')
    blocked = run_check(repo, split)
    assert blocked.verdict.exit_code() == BLOCKED
    assert f"commit {sha}:" in rendered(blocked) and "rule 'customer'" in rendered(blocked)
    assert "secret:planted" not in rendered(blocked)


@pytest.mark.parametrize("folder", SCANNED_DIRS)
def test_a_commit_patch_outside_tests_blocks_on_the_secret_rule(folder: str, repo: Path, split: Path) -> None:
    sha = commit_and_remove(repo, f"{folder}/test_fixture.py", f'KEY = "{SECRET}"\n')
    result = run_check(repo, split)
    assert result.verdict.exit_code() == BLOCKED
    assert f"commit {sha}:" in rendered(result) and "rule 'secret:planted'" in rendered(result)


def test_only_the_hunk_of_the_other_file_blocks_when_a_commit_touches_both(repo: Path, split: Path) -> None:
    """One commit, two files with the same text: the one under `tests/` is skipped, the other is found once."""
    write(repo, "tests/test_a.py", f'KEY = "{SECRET}"\n')
    write(repo, "src/b.py", f'KEY = "{SECRET}"\n')
    git(repo, "add", "tests/test_a.py", "src/b.py")
    git(repo, "commit", "--quiet", "-m", "both")
    sha = git(repo, "rev-parse", "HEAD")[:12]
    git(repo, "rm", "--quiet", "tests/test_a.py", "src/b.py")
    git(repo, "commit", "--quiet", "-m", "removes both")
    result = run_check(repo, split)
    text = rendered(result)
    assert result.verdict.exit_code() == BLOCKED
    assert text.count(f"commit {sha}:") == 1, "one hit for the hunk outside tests/"
    assert text.count("rule 'secret:planted'") == 2, "the same file's removal in the next commit is the second"


def test_the_exemption_follows_a_hunk_back_out_of_tests(repo: Path, split: Path) -> None:
    """The file order of a patch is alphabetical: `src/` comes before `tests/`, and the state must not leak."""
    write(repo, "src/early.py", "harmless\n")
    write(repo, "tests/test_late.py", f'KEY = "{SECRET}"\n')
    write(repo, "zzz/after.py", f'KEY = "{SECRET}"\n')
    git(repo, "add", "src/early.py", "tests/test_late.py", "zzz/after.py")
    git(repo, "commit", "--quiet", "-m", "three files")
    sha = git(repo, "rev-parse", "HEAD")[:12]
    result = run_check(repo, split)
    assert result.verdict.exit_code() == BLOCKED
    assert f"commit {sha}:" in rendered(result)
    assert "zzz/after.py:1 - rule 'secret:planted'" in rendered(result)
    assert "tests/test_late.py:1" not in rendered(result)


@pytest.mark.parametrize(
    "name",
    ["a b.py", "ä.py", 'q"uote.py'],
    ids=["a-space", "non-ascii", "a-quote"],
)
def test_a_name_that_is_hard_to_read_in_a_header_is_exempt_or_scanned_never_mixed_up(
    name: str, repo: Path, split: Path
) -> None:
    """A space and a non-ASCII letter are read with certainty; a quoted name is not, and then the check blocks."""
    commit_and_remove(repo, f"tests/{name}", f'KEY = "{SECRET}"\n')
    result = run_check(repo, split)
    if '"' in name:
        assert result.verdict.exit_code() == BLOCKED, "a header that cannot be read with certainty is scanned in full"
    else:
        assert result.verdict.exit_code() == CLEAN, rendered(result)


def _resolve_a_conflict(root: Path, folder: str, resolved: str) -> str:
    """A merge whose combined diff (`--cc`) shows the line the resolution adds beyond both parents."""
    relative = f"{folder}/shared.py"
    commit_file(root, relative, "VALUE = 0\n")
    git(root, "checkout", "--quiet", "-b", "side")
    commit_file(root, relative, "VALUE = 1\n")
    git(root, "checkout", "--quiet", "main")
    commit_file(root, relative, "VALUE = 2\n")
    run = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false",
         "merge", "--no-commit", "side"],
        cwd=root, capture_output=True, text=True, check=False,
    )  # fmt: skip
    assert run.returncode == 1, "the fixture must conflict"
    write(root, relative, resolved)
    git(root, "add", "--", relative)
    git(root, "commit", "--quiet", "-m", "merge side")
    sha = git(root, "rev-parse", "HEAD")[:12]
    git(root, "branch", "--quiet", "-D", "side")
    # The resolved value is taken out again in a commit of its own, so that only history holds it.
    git(root, "rm", "--quiet", "--", relative)
    git(root, "commit", "--quiet", "-m", "removes")
    return sha


def test_a_merge_resolution_under_tests_follows_the_same_split(repo: Path, split: Path) -> None:
    _resolve_a_conflict(repo, "tests", f'VALUE = "{SECRET}"\n')
    assert run_check(repo, split).verdict.exit_code() == CLEAN
    # The same resolution outside `tests/` is found, so the fixture really shows a combined diff.
    other = repo.parent / "second"
    other.mkdir()
    git(other, "init", "--quiet", "--initial-branch=main")
    write(other, "plans/changes/demo/spec.md", "# Spec\n")
    git(other, "add", "-A")
    git(other, "commit", "--quiet", "-m", "first")
    sha = _resolve_a_conflict(other, "src", f'VALUE = "{SECRET}"\n')
    result = run_check(other, split)
    assert result.verdict.exit_code() == BLOCKED
    assert f"commit {sha}:" in rendered(result)


@pytest.mark.parametrize("folder", EXEMPT_DIRS)
def test_the_staged_diff_follows_the_same_split(folder: str, repo: Path, split: Path) -> None:
    relative = f"{folder}/staged.py"
    write(repo, relative, f'KEY = "{SECRET}"\n')
    git(repo, "add", "--", relative)
    write(repo, relative, "clean again\n")
    result = run_check(repo, split)
    assert result.verdict.exit_code() == CLEAN, rendered(result)

    git(repo, "reset", "--quiet", "--", relative)
    write(repo, "src/staged.py", f'KEY = "{SECRET}"\n')
    git(repo, "add", "--", "src/staged.py")
    write(repo, "src/staged.py", "clean again\n")
    blocked = run_check(repo, split)
    assert blocked.verdict.exit_code() == BLOCKED
    assert "staged changes" in rendered(blocked)


def test_a_commit_message_is_never_exempt_not_even_one_that_forges_a_header(repo: Path, split: Path) -> None:
    """The message is not a file under `tests/`. A line in it that looks like a diff header changes nothing."""
    forged = f"subject\n\ndiff --git a/tests/x.py b/tests/x.py\nKEY = {SECRET}\n"
    git(repo, "commit", "--quiet", "--allow-empty", "-m", forged)
    sha = git(repo, "rev-parse", "HEAD")[:12]
    result = run_check(repo, split)
    assert result.verdict.exit_code() == BLOCKED
    assert f"commit {sha}:" in rendered(result) and "rule 'secret:planted'" in rendered(result)


def test_a_message_with_a_secret_blocks_though_the_patch_is_under_tests(repo: Path, split: Path) -> None:
    write(repo, "tests/test_a.py", f'KEY = "{SECRET}"\n')
    git(repo, "add", "tests/test_a.py")
    git(repo, "commit", "--quiet", "-m", f"subject\n\nthe key is {SECRET}")
    sha = git(repo, "rev-parse", "HEAD")[:12]
    result = run_check(repo, split)
    text = rendered(result)
    assert result.verdict.exit_code() == BLOCKED
    assert text.count(f"commit {sha}:") == 1, "the message, and not the hunk under tests/"


def test_the_report_of_an_exempt_run_still_never_carries_the_match(repo: Path, split: Path) -> None:
    write(repo, "src/leak.txt", f"value = {SECRET}\n")
    write(repo, "tests/fixture.txt", f"value = {SECRET}\nname = {CUSTOMER}\n")
    text = rendered(run_check(repo, split))
    assert "src/leak.txt:1" in text and "tests/fixture.txt:2 - rule 'customer'" in text
    for start in range(len(SECRET) - 7):
        assert SECRET[start : start + 8] not in text.replace(CUSTOMER, ""), "a part of the match is in the report"
    assert CUSTOMER not in text


def test_the_exemption_and_its_consequence_are_stated() -> None:
    """The docstring and the doctrine say what is skipped, by which marker, and what that costs."""
    doc = " ".join((leakcheck.__doc__ or "").split())
    workflow = " ".join((REPO_ROOT / "docs" / "WORKFLOW.md").read_text(encoding="utf-8").split())
    for text in (doc, workflow):
        assert "`secret:`" in text and "tests/" in text, "the marker and the folder"
        assert "real key" in text and "not found" in text, "the accepted consequence"
        assert "customer" in text, "the rules for a customer's names still apply"


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
