"""The check behind the gate `frontmatter-current`, and its stamp.

Every test builds its own git repository in a temporary directory and never
reads this repository's files or dates. The one exception is the real
`provenance.yaml`, which travels with the kit. A test over this repository's
dates would be red on every day after its stamp, in the kit probe's fresh
one-commit copy above all.

Each rule stands next to the fault that turns it red (docs/WORKFLOW.md, phase
5: a gate that has never been red measures nothing).
"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_frontmatter_current.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import check_frontmatter_current as cfc  # noqa: E402

TODAY = date(2026, 9, 20)
UTC_TODAY = date(2026, 9, 20)

MAP = """\
schema_version: 1
paths:
  - prefix: "docs/"
    frontmatter: required
  - prefix: "docs/opt/"
    frontmatter: optional
  - prefix: "docs/opt/req/"
    frontmatter: required
  - prefix: "docs/none/"
    frontmatter: none
excluded:
  - "docs/archive/"
"""


def _env(when: str | None = None, author_when: str | None = None) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    if when:
        env["GIT_COMMITTER_DATE"] = when
        env["GIT_AUTHOR_DATE"] = author_when or when
    return env


def _git(repo: Path, *args: str, when: str | None = None, author_when: str | None = None) -> str:
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
        env=_env(when, author_when),
    )
    return erg.stdout.strip()


def _repo(tmp_path: Path, map_text: str = MAP) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "provenance.yaml").write_text(map_text, encoding="utf-8")
    return repo


def _commit(repo: Path, when: str, message: str = "c", author_when: str | None = None) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message, when=when, author_when=author_when)


def _doc(updated: str | None, body: str = "body") -> str:
    kopf = 'title: "t"\nlast_reviewed: 2026-09-01\n'
    if updated is not None:
        kopf += f"updated: {updated}\n"
    return f"---\n{kopf}---\n\n{body}\n"


def _write(repo: Path, rel: str, text: str) -> Path:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="")
    return p


def _found(repo: Path, today: date = TODAY, utc_today: date = UTC_TODAY) -> dict[str, tuple[str, str]]:
    return {f: (kind, detail) for f, kind, detail in cfc.findings(repo, today, utc_today)}


def test_only_required_prefixes_are_held(tmp_path: Path) -> None:
    """Criterion 1: the map decides, the longest prefix wins, nothing else is held.

    Every file is stale (stamp 2026-09-01, last change 2026-09-10). Only the
    two under a `required` prefix may be reported.
    """
    repo = _repo(tmp_path)
    stale = _doc("2026-09-01")
    for rel in (
        "docs/a.md",  # required
        "docs/opt/x.md",  # the longer optional prefix beats the shorter required one
        "docs/opt/req/y.md",  # the longest prefix is required again
        "docs/none/n.md",
        "docs/archive/q.md",  # under a required prefix, but excluded
        "notes/z.md",  # no entry at all
        "docs/ignored.md",  # untracked and ignored
        "docs/gone.md",  # tracked, deleted from the work tree
    ):
        _write(repo, rel, stale)
    _write(repo, "docs/a.txt", stale)  # not Markdown
    _write(repo, ".gitignore", "docs/ignored.md\n")
    _commit(repo, "2026-09-10T12:00:00+00:00")
    (repo / "docs/gone.md").unlink()

    assert cfc.held_files(repo) == ["docs/a.md", "docs/opt/req/y.md"]
    assert sorted(_found(repo)) == ["docs/a.md", "docs/opt/req/y.md"]


def test_a_header_without_a_readable_updated_goes_red(tmp_path: Path) -> None:
    """Criterion 2: no header, no line, two lines and a non-date are each reported."""
    repo = _repo(tmp_path)
    _write(repo, "docs/no-header.md", "# just a heading\n")
    _write(repo, "docs/no-line.md", _doc(None))
    _write(repo, "docs/two.md", _doc("2026-09-10").replace("updated:", "updated: 2026-09-09\nupdated:", 1))
    _write(repo, "docs/soon.md", _doc("soon"))
    _write(repo, "docs/impossible.md", _doc("2026-02-30"))
    _write(repo, "docs/indented.md", "---\ntitle: t\nproduced_by:\n  updated: 2026-09-10\n---\n\nx\n")
    # None of these may be reported: the date on the day of the change, quoted or not.
    _write(repo, "docs/plain.md", _doc("2026-09-10"))
    _write(repo, "docs/quoted.md", _doc('"2026-09-10"'))
    _write(repo, "docs/single.md", _doc("'2026-09-10'"))
    _commit(repo, "2026-09-10T12:00:00+00:00")

    assert {f: k for f, (k, _) in _found(repo).items()} == {
        "docs/no-header.md": cfc.NO_FRONTMATTER,
        "docs/no-line.md": cfc.MISSING,
        "docs/two.md": cfc.DUPLICATE,
        "docs/soon.md": cfc.UNREADABLE,
        "docs/impossible.md": cfc.UNREADABLE,
        "docs/indented.md": cfc.MISSING,
    }
    assert cfc.run(repo, False, TODAY, UTC_TODAY) == 1


def test_a_far_future_stamp_goes_red(tmp_path: Path) -> None:
    """Criterion 2: a date after tomorrow (UTC) is reported; tomorrow is not."""
    repo = _repo(tmp_path)
    _write(repo, "docs/far.md", _doc("2099-01-01"))
    _write(repo, "docs/day-after.md", _doc("2026-09-22"))
    _write(repo, "docs/tomorrow.md", _doc("2026-09-21"))
    _commit(repo, "2026-09-10T12:00:00+00:00")

    assert {f: k for f, (k, _) in _found(repo).items()} == {
        "docs/far.md": cfc.FUTURE,
        "docs/day-after.md": cfc.FUTURE,
    }


def test_the_check_goes_red_when_a_later_commit_outdates_the_stamp(tmp_path: Path) -> None:
    """Criterion 3: a body change and a move, each a day after the stamp; the author date is not asked."""
    repo = _repo(tmp_path)
    _write(repo, "docs/a.md", _doc("2026-09-10"))
    _commit(repo, "2026-09-10T12:00:00+00:00")
    assert _found(repo) == {}

    # Authored long ago (a cherry-pick, a rebase), committed a day after the stamp: the committer date decides.
    _write(repo, "docs/a.md", _doc("2026-09-10", body="changed"))
    _commit(repo, "2026-09-11T12:00:00+00:00", author_when="2026-09-01T12:00:00+00:00")
    kind, detail = _found(repo)["docs/a.md"]
    assert kind == cfc.STALE
    assert "2026-09-10" in detail and "2026-09-11" in detail, "the message names both dates"

    # A stamp in a new commit clears it.
    _write(repo, "docs/a.md", _doc("2026-09-11", body="changed"))
    _commit(repo, "2026-09-11T18:00:00+00:00")
    assert _found(repo) == {}

    # A move to a new path is a change at the new path, however similar the content.
    _git(repo, "mv", "docs/a.md", "docs/b.md")
    _commit(repo, "2026-09-12T12:00:00+00:00")
    assert _found(repo)["docs/b.md"][0] == cfc.STALE


def test_the_committers_own_offset_decides_the_day(tmp_path: Path) -> None:
    """Criterion 3: 23:30 at -05:00 is the 20th, though it is the 21st in UTC."""
    repo = _repo(tmp_path)
    _write(repo, "docs/a.md", _doc("2026-09-20"))
    _commit(repo, "2026-09-20T23:30:00-05:00")
    assert _found(repo, today=date(2026, 9, 25), utc_today=date(2026, 9, 25)) == {}

    _write(repo, "docs/b.md", _doc("2026-09-19"))
    _commit(repo, "2026-09-20T23:30:00-05:00")
    assert _found(repo, today=date(2026, 9, 25), utc_today=date(2026, 9, 25))["docs/b.md"][0] == cfc.STALE


def test_a_merge_commit_never_counts(tmp_path: Path) -> None:
    """Criterion 3: a --no-ff merge days later dates nothing; the side that changed the file does."""
    repo = _repo(tmp_path)
    _write(repo, "docs/side-only.md", _doc("2026-09-01"))
    _write(repo, "docs/both.md", _doc("2026-09-01", body="one\n\n\n\ntwo"))
    _commit(repo, "2026-09-01T12:00:00+00:00")
    trunk = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")

    _git(repo, "switch", "-q", "-c", "side")
    _write(repo, "docs/side-only.md", _doc("2026-09-05", body="edited on the branch"))
    _write(repo, "docs/both.md", _doc("2026-09-05", body="ONE\n\n\n\ntwo"))
    _commit(repo, "2026-09-05T12:00:00+00:00")

    _git(repo, "switch", "-q", trunk)
    _write(repo, "docs/both.md", _doc("2026-09-01", body="one\n\n\n\nTWO"))
    _commit(repo, "2026-09-06T12:00:00+00:00")
    _git(repo, "merge", "-q", "--no-ff", "-m", "merge side", "side", when="2026-09-10T12:00:00+00:00")

    assert _git(repo, "log", "-1", "--format=%cs").startswith("2026-09-10"), "the merge really is the newest commit"
    found = _found(repo)
    assert "docs/side-only.md" not in found, "the merge commit made the branch-only file stale"
    kind, detail = found["docs/both.md"]
    assert kind == cfc.STALE and "2026-09-06" in detail, "a file changed on both sides is dated by the newer side"


def test_an_uncommitted_edit_is_held_against_today(tmp_path: Path) -> None:
    """Criterion 3: a modified, a staged and an untracked file are each measured against today."""
    repo = _repo(tmp_path)
    for rel in ("docs/worktree.md", "docs/staged.md", "docs/clean.md"):
        _write(repo, rel, _doc("2026-09-10"))
    _commit(repo, "2026-09-10T12:00:00+00:00")

    _write(repo, "docs/worktree.md", _doc("2026-09-10", body="edited, not staged"))
    _write(repo, "docs/staged.md", _doc("2026-09-10", body="edited and staged"))
    _git(repo, "add", "docs/staged.md")
    _write(repo, "docs/new.md", _doc("2026-09-10"))

    found = _found(repo)
    assert sorted(found) == ["docs/new.md", "docs/staged.md", "docs/worktree.md"]
    assert all(kind == cfc.STALE and "uncommitted" in detail for kind, detail in found.values())

    for rel in found:
        (repo / rel).write_text(_doc("2026-09-20"), encoding="utf-8")
    assert _found(repo) == {}, "stamped today, they are current"


def test_a_shallow_clone_is_not_a_pass(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 4: a --depth 1 clone measures nothing (exit 3) and says how to get the history."""
    src = _repo(tmp_path)
    _write(src, "docs/a.md", _doc("2026-09-10"))
    _commit(src, "2026-09-10T12:00:00+00:00")
    _write(src, "docs/a.md", _doc("2026-09-10", body="two"))
    _commit(src, "2026-09-10T13:00:00+00:00")
    clone = tmp_path / "clone"
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", f"file://{src}", str(clone)], check=True, capture_output=True, env=_env()
    )

    assert cfc.run(clone, False, TODAY, UTC_TODAY) == 3
    err = capsys.readouterr().err
    assert "fetch-depth: 0" in err and "needs_history" in err


def test_nothing_is_measured_where_the_question_cannot_be_asked(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 4: not a work tree, no commit and no readable map are exit 3, not a pass."""
    plain = tmp_path / "plain"
    plain.mkdir()
    assert cfc.run(plain, False, TODAY, UTC_TODAY) == 3

    repo = _repo(tmp_path)
    assert cfc.run(repo, False, TODAY, UTC_TODAY) == 3, "no commit yet"

    _commit(repo, "2026-09-10T12:00:00+00:00")
    (repo / "provenance.yaml").write_text("paths: [", encoding="utf-8")
    assert cfc.run(repo, False, TODAY, UTC_TODAY) == 3, "the map does not parse"
    assert capsys.readouterr().err.count("NOT MEASURED") == 3


def test_the_failure_names_the_stamp_command(tmp_path: Path) -> None:
    """Criterion 4: exit 1 and the fix line, verbatim, when a header is stale (the real command line)."""
    repo = _repo(tmp_path)
    _write(repo, "docs/a.md", _doc("2026-09-01"))
    _commit(repo, "2026-09-10T12:00:00+00:00")

    erg = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(repo)], capture_output=True, text=True, check=False, env=_env()
    )
    assert erg.returncode == 1, erg.stdout + erg.stderr
    assert "docs/a.md: stale" in erg.stdout
    assert "fix: python3 scripts/check_frontmatter_current.py --stamp" in erg.stdout


def test_the_stamp_touches_only_the_updated_line(tmp_path: Path) -> None:
    """Criterion 5: flow mappings, comments, quotes, CRLF and non-ASCII bytes stay as they were."""
    repo = _repo(tmp_path)
    body = "\r\nText with Umlaute: äöü\r\nsecond line\r\n"
    vorher = (
        '---\ntitle: "x"   # keep this comment\nreview: {status: pending, approved_by: null}\n'
        'last_reviewed: 2026-09-01\nupdated: "2026-09-01"   \ntags: [a, b]\n---\n' + body
    )
    _write(repo, "docs/replace.md", vorher)
    _write(
        repo,
        "docs/after-review.md",
        "---\ntitle: t\nlast_reviewed: 2026-09-01\ntags: [a]\n---\n\nbody\ntail without newline",
    )
    _write(repo, "docs/no-review.md", "---\ntitle: t\n  updated: 1999-01-01\ntags: [a]\n---\n\nx\n")
    _commit(repo, "2026-09-10T12:00:00+00:00")

    for rel in ("docs/replace.md", "docs/after-review.md", "docs/no-review.md"):
        assert cfc.stamp(repo / rel, TODAY) is True

    nachher = (repo / "docs/replace.md").read_bytes().decode("utf-8")
    assert nachher == vorher.replace('updated: "2026-09-01"   \n', "updated: 2026-09-20\n")

    assert (repo / "docs/after-review.md").read_text(encoding="utf-8") == (
        "---\ntitle: t\nlast_reviewed: 2026-09-01\nupdated: 2026-09-20\ntags: [a]\n---\n\nbody\ntail without newline"
    ), "the line goes directly after last_reviewed"

    assert (repo / "docs/no-review.md").read_text(encoding="utf-8") == (
        "---\ntitle: t\n  updated: 1999-01-01\ntags: [a]\nupdated: 2026-09-20\n---\n\nx\n"
    ), "without last_reviewed the line closes the block; an indented updated is not the one"


def test_the_stamp_is_idempotent_and_never_writes_a_header(tmp_path: Path) -> None:
    """Criterion 5: a second run changes no byte, and a file without a header stays without."""
    repo = _repo(tmp_path)
    _write(repo, "docs/stale.md", _doc("2026-09-01"))
    _write(repo, "docs/missing.md", _doc(None))
    _write(repo, "docs/unreadable.md", _doc("soon"))
    _write(repo, "docs/future.md", _doc("2099-01-01"))
    _write(repo, "docs/current.md", _doc("2026-09-10"))
    _commit(repo, "2026-09-10T12:00:00+00:00")

    def alle() -> dict[str, bytes]:
        return {p.name: p.read_bytes() for p in (repo / "docs").glob("*.md")}

    assert cfc.run(repo, True, TODAY, UTC_TODAY) == 0
    nach_erstem = alle()
    assert nach_erstem["current.md"] == _doc("2026-09-10").encode(), "a current file is left alone"
    assert b"updated: 2026-09-20\n" in nach_erstem["stale.md"]
    assert cfc.run(repo, False, TODAY, UTC_TODAY) == 0, "a stamped file is still reported"
    assert cfc.run(repo, True, TODAY, UTC_TODAY) == 0
    assert alle() == nach_erstem, "the second run rewrote a file"

    # What a stamp cannot repair is named, left alone, and keeps the exit red.
    _write(repo, "docs/headless.md", "# no header at all\n")
    _write(repo, "docs/twice.md", _doc("2026-09-01").replace("updated:", "updated: 2026-09-02\nupdated:", 1))
    _commit(repo, "2026-09-20T12:00:00+00:00")
    davor = alle()
    assert cfc.run(repo, True, TODAY, UTC_TODAY) == 1
    assert alle()["headless.md"] == b"# no header at all\n", "a header was invented"
    assert alle()["twice.md"] == davor["twice.md"]

    # Called directly, the stamp still writes nothing it need not: no change, no write; no header, no invention.
    heute = repo / "docs/stale.md"
    assert cfc.stamp(heute, TODAY) is False
    assert cfc.stamp(repo / "docs/headless.md", TODAY) is False
    assert cfc.stamp(repo / "docs/twice.md", TODAY) is False
    assert alle()["headless.md"] == b"# no header at all\n"
