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
import shlex
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


def test_a_root_below_the_top_of_the_repository_sees_its_own_edits(tmp_path: Path) -> None:
    """Criterion 3: pointed at a subdirectory, the check still finds its uncommitted files (git diff --relative)."""
    repo = _repo(tmp_path)
    sub = repo / "sub"
    _write(repo, "sub/provenance.yaml", MAP)
    _write(repo, "sub/docs/edited.md", _doc("2026-09-10"))
    _write(repo, "sub/docs/clean.md", _doc("2026-09-10"))
    _commit(repo, "2026-09-10T12:00:00+00:00")
    assert _found(sub) == {}, "the subdirectory is measured as a repository of its own"

    # Without `--relative`, git diff names `sub/docs/edited.md`, which is not a path below the root:
    # the edit would be dated by its commit, and the stale stamp would pass.
    _write(repo, "sub/docs/edited.md", _doc("2026-09-10", body="edited, not committed"))
    found = _found(sub)
    assert sorted(found) == ["docs/edited.md"]
    assert found["docs/edited.md"][0] == cfc.STALE and "uncommitted" in found["docs/edited.md"][1]
    assert cfc.run(sub, False, TODAY, UTC_TODAY) == 1


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


def test_a_shallow_answer_that_fails_is_not_full_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 4: a git that cannot say whether the clone is shallow (before 2.15) is exit 3, not a pass."""
    repo = _repo(tmp_path)
    _write(repo, "docs/a.md", _doc("2026-09-10"))
    _commit(repo, "2026-09-10T12:00:00+00:00")
    assert cfc.run(repo, False, TODAY, UTC_TODAY) == 0
    capsys.readouterr()

    echt = cfc._git

    def ohne_flag(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        if "--is-shallow-repository" in args:
            return subprocess.CompletedProcess(list(args), 129, "--is-shallow-repository\n", "usage: git rev-parse")
        return echt(root, *args)

    monkeypatch.setattr(cfc, "_git", ohne_flag)
    assert cfc.run(repo, False, TODAY, UTC_TODAY) == 3
    err = capsys.readouterr().err
    assert "NOT MEASURED" in err and "shallow" in err


def test_a_map_that_holds_no_file_is_not_a_pass(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 4: a map whose `required` prefixes match no file measured nothing (exit 3), in both modes."""
    repo = _repo(tmp_path, 'schema_version: 1\npaths:\n  - prefix: "nothing/"\n    frontmatter: required\n')
    _write(repo, "docs/stale.md", _doc("2026-09-01"))
    _commit(repo, "2026-09-10T12:00:00+00:00")

    assert cfc.run(repo, False, TODAY, UTC_TODAY) == 3
    assert cfc.run(repo, True, TODAY, UTC_TODAY) == 3
    err = capsys.readouterr().err
    assert err.count("NOT MEASURED") == 2 and "measures nothing" in err
    assert b"updated: 2026-09-01" in (repo / "docs/stale.md").read_bytes(), "a run that measured nothing wrote"


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


def test_a_header_with_crlf_or_a_byte_order_mark_is_read_and_stamped_in_kind(tmp_path: Path) -> None:
    """Criteria 2 and 5: CRLF and a BOM do not make a header "no frontmatter"; the stamp keeps both."""
    repo = _repo(tmp_path)
    crlf = _doc("2026-09-10").replace("\n", "\r\n")
    bom = "﻿" + _doc("2026-09-10")
    beides_alt = "﻿" + _doc("2026-09-01").replace("\n", "\r\n")
    ohne_zeile = "﻿" + _doc(None).replace("\n", "\r\n")
    _write(repo, "docs/crlf.md", crlf)
    _write(repo, "docs/bom.md", bom)
    _write(repo, "docs/both-stale.md", beides_alt)
    _write(repo, "docs/both-missing.md", ohne_zeile)
    _commit(repo, "2026-09-10T12:00:00+00:00")

    assert {f: k for f, (k, _) in _found(repo).items()} == {
        "docs/both-stale.md": cfc.STALE,
        "docs/both-missing.md": cfc.MISSING,
    }, "a header that is there was called absent, or a current one reported"

    assert cfc.run(repo, True, TODAY, UTC_TODAY) == 0
    assert (repo / "docs/both-stale.md").read_bytes() == beides_alt.replace(
        "updated: 2026-09-01", "updated: 2026-09-20"
    ).encode()
    assert (repo / "docs/both-missing.md").read_bytes() == ohne_zeile.replace(
        "last_reviewed: 2026-09-01\r\n", "last_reviewed: 2026-09-01\r\nupdated: 2026-09-20\r\n"
    ).encode(), "the inserted line has the file's own line ending, and the BOM stays"
    assert (repo / "docs/crlf.md").read_bytes() == crlf.encode(), "a current file was rewritten"
    assert cfc.run(repo, False, TODAY, UTC_TODAY) == 0


def test_the_stamp_never_crashes_on_a_file_that_is_not_utf8(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 5: invalid UTF-8 is named and left unchanged, and the stamp exits 1; the check reports, it does not crash."""
    repo = _repo(tmp_path)
    kaputt = _doc("2026-09-01").encode() + b"caf\xe9 in latin-1\n"
    (repo / "docs").mkdir()
    (repo / "docs/latin1.md").write_bytes(kaputt)
    _write(repo, "docs/fine.md", _doc("2026-09-01"))
    _commit(repo, "2026-09-10T12:00:00+00:00")

    assert _found(repo)["docs/latin1.md"][0] == cfc.STALE
    assert cfc.run(repo, True, TODAY, UTC_TODAY) == 1
    out = capsys.readouterr().out
    assert "docs/latin1.md" in out and "not valid UTF-8" in out and "left unchanged" in out
    assert (repo / "docs/latin1.md").read_bytes() == kaputt, "the stamp changed a file it could not read"
    assert b"updated: 2026-09-20" in (repo / "docs/fine.md").read_bytes(), "one bad file stopped the others"
    with pytest.raises(cfc.CannotStamp):
        cfc.stamp(repo / "docs/latin1.md", TODAY)


def test_a_trailing_yaml_comment_after_the_date_is_still_the_date(tmp_path: Path) -> None:
    """Criterion 2: YAML reads `2026-09-10  # note` as the date, so it is read as one; `2026-09-10#x` is not."""
    repo = _repo(tmp_path)
    _write(repo, "docs/comment.md", _doc("2026-09-10  # stamped by hand"))
    _write(repo, "docs/quoted-comment.md", _doc('"2026-09-10" # note'))
    _write(repo, "docs/stale-comment.md", _doc("2026-09-01  # old"))
    _write(repo, "docs/no-space.md", _doc("2026-09-10# glued"))  # a string in YAML, not a date
    _commit(repo, "2026-09-10T12:00:00+00:00")

    assert {f: k for f, (k, _) in _found(repo).items()} == {
        "docs/stale-comment.md": cfc.STALE,
        "docs/no-space.md": cfc.UNREADABLE,
    }


def test_the_map_holds_documents_not_harness_configuration() -> None:
    """Criteria 1 and 7: the real map holds the documents a person reads, and no functional frontmatter."""
    paths, excluded = cfc.load_map(REPO_ROOT)

    def held(rel: str) -> bool:
        return cfc.is_held(rel, paths, excluded)

    for rel in (
        "docs/adr/0001-early-parallelism.md",
        "docs/architecture/x.md",
        "docs/research/x.md",
        "docs/how-to/x.md",
        "docs/governance/x.md",
        "docs/WORKFLOW.md",
        "plans/changes/x/plan.md",
        "docs/journal/handover/x.md",
    ):
        assert held(rel), f"{rel} is a document a person reads and must be held"
    for rel in (
        ".claude/agents/x.md",  # its frontmatter is configuration
        ".agents/skills/x/SKILL.md",
        "prompts/04-implement.md",
        "templates/handover.md",
        "plans/INDEX.md",
        "README.md",
        "AGENTS.md",
        "docs/archive/x.md",
    ):
        assert not held(rel), f"{rel} carries no document header and must not be held"


# ---------------------------------------------------------------------------
# the batched history (bead coding-harness-bxxt.21)
# ---------------------------------------------------------------------------

FLAT_MAP = 'schema_version: 1\npaths:\n  - prefix: ""\n    frontmatter: required\n'


def _oracle(root: Path, rel: str) -> tuple[date, str] | None:
    """What one literal `git log -1 --no-merges -- <file>` with `log.follow` off answers, in the check's own env."""
    erg = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "--literal-pathspecs",
            "-c",
            "log.follow=false",
            "log",
            "-1",
            "--no-merges",
            "--format=%cs %h",
            "--",
            rel,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    zeile = erg.stdout.strip()
    if not zeile:
        return None
    tag, kurz = zeile.split(" ", 1)
    return date.fromisoformat(tag), kurz


def _per_file_reference_dates(root: Path, files: list[str], today: date) -> dict[str, tuple[date, str]]:
    """The check's former per-file lookup, with the literal pathspec and `log.follow` off the spec asks for."""
    dirty = set(cfc._git_z(root, "diff", "--name-only", "--no-renames", "--relative", "-z", "HEAD"))
    dirty |= set(cfc._git_z(root, "ls-files", "-z", "--others", "--exclude-standard"))
    out: dict[str, tuple[date, str]] = {}
    for f in files:
        if f in dirty:
            out[f] = (today, "uncommitted")
            continue
        found = _oracle(root, f)
        if found is None:
            raise cfc.CannotMeasure(f"git log cannot date {f}: no commit changed it")
        out[f] = found
    return out


def _edit(repo: Path, *rels: str, tag: str) -> None:
    for rel in rels:
        _write(repo, rel, _doc("2026-09-01", body=f"{rel} {tag}"))


def _branchy_history(tmp_path: Path) -> Path:
    """Merges that keep one side, the other side or neither, a move, a subdirectory, and names git could misread."""
    repo = _repo(tmp_path, FLAT_MAP)
    _git(repo, "config", "log.follow", "true")
    _write(repo, "sub/provenance.yaml", FLAT_MAP)
    _edit(
        repo,
        "side.md",
        "ours.md",
        "evil.md",
        "trunk.md",
        "trunk2.md",
        "top2.md",
        "old.md",
        "a*b.md",
        "aXb.md",
        "q?.md",
        "qZ.md",
        "[x].md",
        "x.md",
        ":lead.md",
        "lead.md",
        "sub/s.md",
        "sub/t.md",
        "sub/u.md",
        tag="base",
    )
    _commit(repo, "2026-09-01T12:00:00+00:00")
    trunk = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")

    # The side branch touches nothing below sub/.
    _git(repo, "switch", "-q", "-c", "side")
    _edit(repo, "side.md", "ours.md", "evil.md", tag="side")
    _commit(repo, "2026-09-03T12:00:00+00:00")
    _git(repo, "switch", "-q", trunk)
    _edit(repo, "trunk.md", "evil.md", "sub/t.md", tag="trunk")
    _commit(repo, "2026-09-04T12:00:00+00:00")
    # side.md comes from the branch, ours.md stays as on trunk, evil.md differs from both sides.
    _git(repo, "merge", "-q", "--no-ff", "--no-commit", "-s", "ours", "side")
    _git(repo, "checkout", "side", "--", "side.md")
    _edit(repo, "evil.md", tag="resolved by hand")
    _commit(repo, "2026-09-10T12:00:00+00:00", "merge side")

    # A glob or pathspec magic in the names above would match these.
    _edit(repo, "aXb.md", "qZ.md", "x.md", "lead.md", tag="decoy")
    _commit(repo, "2026-09-11T12:00:00+00:00")
    _git(repo, "mv", "old.md", "new.md")
    _commit(repo, "2026-09-11T18:00:00+00:00")

    # The merge takes sub/ from the branch, while the trees differ outside it.
    _git(repo, "switch", "-q", "-c", "side2")
    _edit(repo, "sub/s.md", "top2.md", tag="side2")
    _commit(repo, "2026-09-12T12:00:00+00:00")
    _git(repo, "switch", "-q", trunk)
    _edit(repo, "trunk2.md", tag="trunk2")
    _commit(repo, "2026-09-13T12:00:00+00:00")
    _git(repo, "merge", "-q", "--no-ff", "--no-commit", "-s", "ours", "side2")
    _git(repo, "checkout", "side2", "--", "sub/s.md", "top2.md")
    _commit(repo, "2026-09-15T12:00:00+00:00", "merge side2")
    return repo


def test_batch_matches_literal_per_path_history(tmp_path: Path) -> None:
    """Spec criterion 2: every clean file gets the date and hash its own literal `git log -1 --no-merges` gives.

    The repository sets `log.follow=true`; the oracle and the batch force it off. Run at the top and at a
    subdirectory root, across merges that keep one side, the other or neither.
    """
    repo = _branchy_history(tmp_path)

    got: dict[Path, dict[str, tuple[date, str]]] = {}
    for root in (repo, repo / "sub"):
        files = cfc.held_files(root)
        want = {f: _oracle(root, f) for f in files}
        assert None not in want.values(), "every file in the fixture has history"
        got[root] = cfc.reference_dates(root, files, TODAY)
        assert got[root] == want, f"the batch differs from per-path git log at {root}"
    assert {"a*b.md", "q?.md", "[x].md", ":lead.md", "new.md", "sub/t.md"} <= set(got[repo])
    assert {"s.md", "t.md", "u.md"} <= set(got[repo / "sub"])

    # The fixture bites: a walk that follows both sides of a merge dates ours.md by the discarded branch edit,
    # and a glob pathspec dates a*b.md by the decoy.
    def date_of(*args: str) -> str:
        erg = subprocess.run(
            ["git", "-C", str(repo), "-c", "log.follow=false", "log", "-1", "--no-merges", "--format=%cs", *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return erg.stdout.strip()

    assert date_of("--full-history", "--", "ours.md") == "2026-09-03"
    assert got[repo]["ours.md"][0] == date(2026, 9, 1)
    assert date_of("--", "a*b.md") == "2026-09-11"
    assert got[repo]["a*b.md"][0] == date(2026, 9, 1)


def test_date_check_has_bounded_git_processes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Spec criterion 1: the date lookup starts at most three git processes, however many files it dates."""
    repo = _repo(tmp_path)
    for n in range(8):
        _write(repo, f"docs/d{n}.md", _doc("2026-09-10"))
    _commit(repo, "2026-09-10T12:00:00+00:00")
    _write(repo, "docs/d7.md", _doc("2026-09-10", body="edited"))
    files = cfc.held_files(repo)
    assert len(files) == 8

    started: list[object] = []
    echt = subprocess.Popen

    class Counting(echt):  # type: ignore[misc, valid-type]
        def __init__(self, args: object, *rest: object, **kw: object) -> None:
            started.append(args)
            super().__init__(args, *rest, **kw)  # type: ignore[arg-type]

    monkeypatch.setattr(subprocess, "Popen", Counting)
    counts = []
    for size in (1, 3, len(files)):
        started.clear()
        refs = cfc.reference_dates(repo, files[:size], TODAY)
        assert len(refs) == size
        counts.append(len(started))
    monkeypatch.undo()

    assert max(counts) <= 3, f"processes per lookup: {counts}"
    assert len(set(counts)) == 1, f"the process count grows with the held set: {counts}"


def test_staged_and_untracked_documents_use_today(tmp_path: Path) -> None:
    """Spec criterion 3: modified, staged, newly staged and untracked files are dated today as uncommitted."""
    repo = _repo(tmp_path)
    for rel in ("docs/clean.md", "docs/staged.md", "docs/edited.md"):
        _write(repo, rel, _doc("2026-09-10"))
    _commit(repo, "2026-09-10T12:00:00+00:00")
    _write(repo, "docs/staged.md", _doc("2026-09-10", body="staged"))
    _git(repo, "add", "docs/staged.md")
    _write(repo, "docs/edited.md", _doc("2026-09-10", body="edited"))
    _write(repo, "docs/new-staged.md", _doc("2026-09-10"))
    _git(repo, "add", "docs/new-staged.md")
    _write(repo, "docs/untracked.md", _doc("2026-09-10"))

    refs = cfc.reference_dates(repo, cfc.held_files(repo), TODAY)
    for rel in ("docs/staged.md", "docs/edited.md", "docs/new-staged.md", "docs/untracked.md"):
        assert refs[rel] == (TODAY, "uncommitted"), f"{rel} was dated by a commit"
    assert refs["docs/clean.md"] == _oracle(repo, "docs/clean.md")
    assert refs["docs/clean.md"][0] == date(2026, 9, 10)


def test_missing_history_keeps_per_file_diagnostic(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Spec criterion 4: a clean file the batch cannot date is exit 3 with the per-file diagnostic, as before."""
    repo = _repo(tmp_path)
    _write(repo, "docs/a.md", _doc("2026-09-10"))
    _commit(repo, "2026-09-10T12:00:00+00:00")
    for rel in ("docs/b-new.md", "docs/c-new.md"):
        _write(repo, rel, _doc("2026-09-10"))
        _git(repo, "add", rel)

    # Staged files are dirty; hiding the diff makes them clean files no commit ever changed.
    echt = cfc._git

    def blind(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        if args[:1] == ("diff",):
            return subprocess.CompletedProcess(["git", *args], 0, "", "")
        return echt(root, *args)

    monkeypatch.setattr(cfc, "_git", blind)
    for do_stamp in (False, True):
        assert cfc.run(repo, do_stamp, TODAY, UTC_TODAY) == 3
        err = capsys.readouterr().err
        assert err == "NOT MEASURED: git log cannot date docs/b-new.md: no commit changed it\n"


def test_failed_batch_names_command_without_blaming_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Spec criterion 5: a failed batch is exit 3, names its command and the end of its stderr, blames no file."""
    repo = _repo(tmp_path)
    _write(repo, "docs/a.md", _doc("2026-09-01"))
    _write(repo, "docs/b.md", _doc("2026-09-10"))
    _commit(repo, "2026-09-10T12:00:00+00:00")
    command = shlex.join(["git", "-C", str(repo), *cfc.HISTORY_ARGS])

    echt = cfc._git
    stderr = {"text": ""}

    def failing(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        if "log" in args:
            return subprocess.CompletedProcess(["git", *args], 128, "", stderr["text"])
        return echt(root, *args)

    monkeypatch.setattr(cfc, "_git", failing)

    def excerpt(text: str) -> str:
        stderr["text"] = text
        assert cfc.run(repo, False, TODAY, UTC_TODAY) == 3
        captured = capsys.readouterr()
        assert captured.out == ""
        err = captured.err
        assert err.count("NOT MEASURED") == 1
        assert command in err and "exit 128" in err
        assert "docs/a.md" not in err and "docs/b.md" not in err, "the failure was blamed on a file"
        return err.split("stderr:\n", 1)[1].removesuffix("\n")

    assert excerpt("fatal: bad object HEAD\n") == "fatal: bad object HEAD"

    lines = [f"stderr line {n:02d} token=sk-not-redacted" for n in range(30)]
    shown = excerpt("\n".join(lines) + "\n")
    assert shown == cfc.STDERR_CUT + "\n" + "\n".join(lines[-20:]), "not the last 20 lines, unredacted, marked"

    long_line = "0123456789" * 500 + "END"
    shown = excerpt(long_line)
    assert shown.startswith(cfc.STDERR_CUT + "\n")
    body = shown[len(cfc.STDERR_CUT) + 1 :]
    assert body == long_line[-2000:] and len(body) <= 2000


def _mixed_history(base: Path) -> Path:
    """Stale, current, missing, future, headless and branch-dated documents, one edited and one new."""
    base.mkdir()
    repo = _repo(base)
    _write(repo, "docs/current.md", _doc("2026-09-05"))
    _write(repo, "docs/stale.md", _doc("2026-09-01"))
    _write(repo, "docs/missing.md", _doc(None))
    _write(repo, "docs/future.md", _doc("2099-01-01"))
    _write(repo, "docs/headless.md", "# no header\n")
    _write(repo, "docs/branch.md", _doc("2026-09-05"))
    _write(repo, "docs/edited.md", _doc("2026-09-05"))
    _commit(repo, "2026-09-05T12:00:00+00:00")
    trunk = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    _git(repo, "switch", "-q", "-c", "side")
    _write(repo, "docs/branch.md", _doc("2026-09-05", body="edited on the branch"))
    _commit(repo, "2026-09-08T12:00:00+00:00")
    _git(repo, "switch", "-q", trunk)
    _write(repo, "docs/current.md", _doc("2026-09-10", body="edited on trunk"))
    _commit(repo, "2026-09-10T12:00:00+00:00")
    _git(repo, "merge", "-q", "--no-ff", "-m", "merge side", "side", when="2026-09-12T12:00:00+00:00")
    _write(repo, "docs/edited.md", _doc("2026-09-05", body="not committed"))
    _write(repo, "docs/new.md", _doc("2026-09-01"))
    return repo


def _tree_bytes(repo: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(repo)): p.read_bytes()
        for p in repo.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(repo).parts
    }


def test_batch_preserves_check_and_stamp_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Spec criterion 6: check and stamp print, exit and write as the per-file lookup does on a twin."""
    batch = _mixed_history(tmp_path / "batch")
    per_file = _mixed_history(tmp_path / "per-file")

    def both(do_stamp: bool) -> tuple[tuple[int, str, str], tuple[int, str, str]]:
        code = cfc.run(batch, do_stamp, TODAY, UTC_TODAY)
        mit = capsys.readouterr()
        with monkeypatch.context() as m:
            m.setattr(cfc, "reference_dates", _per_file_reference_dates)
            code_alt = cfc.run(per_file, do_stamp, TODAY, UTC_TODAY)
        ohne = capsys.readouterr()
        return (code, mit.out, mit.err), (code_alt, ohne.out, ohne.err)

    neu, alt = both(False)
    assert neu == alt
    assert neu[0] == 1 and "docs/branch.md: stale" in neu[1] and "docs/edited.md: stale" in neu[1]
    assert "docs/current.md" not in neu[1], "the merge commit dated a file"

    neu, alt = both(True)
    assert neu == alt
    assert _tree_bytes(batch) == _tree_bytes(per_file), "the stamp wrote different bytes"
    assert b"updated: 2026-09-20" in _tree_bytes(batch)["docs/stale.md"]
