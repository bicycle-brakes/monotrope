"""Branch search of the registry's reverse coupling (bead coding-harness-l54q).

A running bead whose change folder lives only on a pushed branch is not drift;
a running bead with no folder anywhere still is. Every test builds a temporary
work repository whose origin remote-tracking refs come from a second repository,
so no network and no real branch is touched.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import plans_registry  # noqa: E402
from _verdict import Level  # noqa: E402

TODAY = dt.date.today().isoformat()


def artefact(bead: str, body: str = "# Body\n") -> str:
    return (
        f"---\nstatus: draft\nimplementation_status: none\ndate: {TODAY}\n"
        f"last_reviewed: {TODAY}\nbead: {bead}\n---\n\n{body}"
    )


def git(cwd: Path, *args: str) -> str:
    done = subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True)
    return done.stdout


class Lab:
    """A work repository (the checked tree) and a source repository standing in for origin."""

    def __init__(self, root: Path) -> None:
        self.work = root / "work"
        self.src = root / "src"
        for repo in (self.work, self.src):
            repo.mkdir()
            git(repo, "init", "-q", "-b", "main")
            (repo / ".gitkeep").write_text("", encoding="utf-8")
            git(repo, "add", ".gitkeep")
            git(repo, "commit", "-q", "-m", "root")
        self.root_commit = git(self.src, "rev-parse", "HEAD").strip()

    def branch(self, name: str, files: dict[str, str]) -> None:
        """A branch of the source repository holding exactly these files besides the root."""
        git(self.src, "checkout", "-q", "-B", name, self.root_commit)
        for rel, text in files.items():
            path = self.src / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        git(self.src, "add", "-A")
        git(self.src, "commit", "-q", "--allow-empty", "-m", f"branch {name}")

    def fetch(self) -> None:
        git(self.work, "fetch", "-q", str(self.src), "+refs/heads/*:refs/remotes/origin/*")

    def tree(self, files: dict[str, str]) -> None:
        for rel, text in files.items():
            path = self.work / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def tracker(self, running: list[str]) -> None:
        path = self.work / ".beads" / "issues.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = [{"id": bead, "status": "in_progress"} for bead in running]
        rows.append({"id": "demo-open", "status": "open"})
        path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


@pytest.fixture
def lab(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Lab:
    monkeypatch.setenv("GIT_AUTHOR_NAME", "t")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "t@example.invalid")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "t")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "t@example.invalid")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    fixture = Lab(tmp_path)
    monkeypatch.setattr(plans_registry, "REPO", fixture.work)
    monkeypatch.setattr(plans_registry, "PLANS", fixture.work / "plans")
    monkeypatch.setattr(plans_registry, "INDEX", fixture.work / "plans" / "INDEX.md")
    return fixture


def run(fixture: Lab, *, branches: bool = True):
    """The registry verdict, with a current index so that only the coupling is in question."""
    plans = fixture.work / "plans"
    plans.mkdir(parents=True, exist_ok=True)
    (plans / "INDEX.md").write_text(plans_registry.render_index(), encoding="utf-8")
    return plans_registry.check(branches=branches)


def messages(verdict, level: Level) -> list[str]:
    return [f.message for f in verdict.at(level)]


def missing(verdict) -> list[str]:
    return [m for m in messages(verdict, Level.DRIFT) if "has no artefact under plans/changes/" in m]


def summary(verdict) -> list:
    return [f for f in verdict.at(Level.INFO) if "found only on branches" in f.message]


def test_branch_only_artefact_satisfies_running_bead(lab: Lab) -> None:
    lab.branch("lane", {"plans/changes/lane/spec.md": artefact("demo-lane")})
    lab.fetch()
    lab.tracker(["demo-lane"])
    verdict = run(lab)
    assert missing(verdict) == []
    assert messages(verdict, Level.BLOCK) == []


def test_missing_artefact_remains_drift(lab: Lab) -> None:
    lab.branch("lane", {"plans/changes/lane/spec.md": artefact("demo-lane")})
    lab.fetch()
    lab.tracker(["demo-lane", "demo-nowhere"])
    verdict = run(lab)
    assert missing(verdict) == ["Bead 'demo-nowhere' is 'in_progress' but has no artefact under plans/changes/"]


def test_branch_summary_counts_distinct_branch_only_beads(lab: Lab) -> None:
    lab.tree({"plans/changes/tree/spec.md": artefact("demo-tree")})
    two = artefact("demo-two")
    lab.branch("a", {"plans/changes/x/spec.md": two, "plans/changes/t/spec.md": artefact("demo-tree")})
    lab.branch("b", {"plans/changes/x/spec.md": two, "plans/changes/y/spec.md": artefact("demo-one")})
    lab.fetch()
    lab.tracker(["demo-tree", "demo-two", "demo-one", "demo-nowhere"])
    verdict = run(lab)
    found = summary(verdict)
    assert len(found) == 1
    assert found[0].message == "4 running beads checked, 2 found only on branches, 1 without artefact anywhere"
    assert missing(verdict) == ["Bead 'demo-nowhere' is 'in_progress' but has no artefact under plans/changes/"]


def test_no_remote_refs_preserves_tree_only_check(lab: Lab) -> None:
    lab.tracker(["demo-nowhere"])
    verdict = run(lab)
    assert missing(verdict) == ["Bead 'demo-nowhere' is 'in_progress' but has no artefact under plans/changes/"]
    infos = messages(verdict, Level.INFO)
    assert "1 running beads checked, 1 without artefact" in infos
    assert any("no origin remote-tracking branches" in m for m in infos)
    assert summary(verdict) == []


def _failing_git(monkeypatch: pytest.MonkeyPatch, fail_on: str | None) -> None:
    """Make the registry's Git calls fail: all of them, or only one subcommand."""
    real = subprocess.run

    def fake(cmd, *args, **kwargs):
        if cmd[0] == "git" and (fail_on is None or fail_on in cmd):
            if fail_on is None:
                raise FileNotFoundError("git")
            raise subprocess.CalledProcessError(128, cmd)
        return real(cmd, *args, **kwargs)

    monkeypatch.setattr(plans_registry.subprocess, "run", fake)


@pytest.mark.parametrize("fail_on", [None, "for-each-ref", "ls-tree", "cat-file"])
def test_git_read_failure_blocks_incomplete_search(lab: Lab, monkeypatch: pytest.MonkeyPatch, fail_on) -> None:
    lab.branch("aaa", {"plans/changes/a/spec.md": artefact("demo-a")})
    lab.branch("zzz", {"plans/changes/z/spec.md": artefact("demo-z")})
    lab.fetch()
    lab.tracker(["demo-a", "demo-z", "demo-nowhere"])
    _failing_git(monkeypatch, fail_on)
    verdict = run(lab)
    blocks = [m for m in messages(verdict, Level.BLOCK) if "Branch search incomplete" in m]
    assert len(blocks) == 1
    assert "3 running beads still unresolved" in blocks[0]
    assert missing(verdict) == []
    assert summary(verdict) == []
    assert not any("running beads checked" in m for m in messages(verdict, Level.INFO))


def test_git_read_failure_credits_completed_reads(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> None:
    lab.branch("aaa", {"plans/changes/a/spec.md": artefact("demo-a")})
    lab.branch("zzz", {"plans/changes/z/spec.md": artefact("demo-z")})
    lab.fetch()
    lab.tracker(["demo-a", "demo-z", "demo-nowhere"])
    real = subprocess.run

    def fake(cmd, *args, **kwargs):
        if cmd[0] == "git" and "ls-tree" in cmd and "refs/remotes/origin/zzz" in cmd:
            raise subprocess.CalledProcessError(128, cmd)
        return real(cmd, *args, **kwargs)

    monkeypatch.setattr(plans_registry.subprocess, "run", fake)
    verdict = run(lab)
    blocks = [m for m in messages(verdict, Level.BLOCK) if "Branch search incomplete" in m]
    assert len(blocks) == 1
    assert "2 running beads still unresolved" in blocks[0]
    assert missing(verdict) == []


def test_incomplete_search_reports_malformed_files_already_read(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> None:
    lab.branch("aaa", {"plans/changes/a/spec.md": "# No frontmatter\n"})
    lab.branch("zzz", {"plans/changes/z/spec.md": artefact("demo-z")})
    lab.fetch()
    lab.tracker(["demo-z"])
    real = subprocess.run

    def fake(cmd, *args, **kwargs):
        if cmd[0] == "git" and "ls-tree" in cmd and "refs/remotes/origin/zzz" in cmd:
            raise subprocess.CalledProcessError(128, cmd)
        return real(cmd, *args, **kwargs)

    monkeypatch.setattr(plans_registry.subprocess, "run", fake)
    verdict = run(lab)
    assert any("Branch search incomplete" in m for m in messages(verdict, Level.BLOCK))
    assert "1 branch files with absent or unreadable frontmatter ignored" in messages(verdict, Level.INFO)
    assert missing(verdict) == []
    assert summary(verdict) == []


def test_git_read_failure_in_a_non_repository_blocks(tmp_path: Path, monkeypatch) -> None:
    plain = tmp_path / "plain"
    plain.mkdir()
    monkeypatch.setattr(plans_registry, "REPO", plain)
    monkeypatch.setattr(plans_registry, "PLANS", plain / "plans")
    monkeypatch.setattr(plans_registry, "INDEX", plain / "plans" / "INDEX.md")
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    plain_lab = Lab.__new__(Lab)
    plain_lab.work = plain
    plain_lab.tracker(["demo-nowhere"])
    verdict = run(plain_lab)
    assert any("Branch search incomplete" in m for m in messages(verdict, Level.BLOCK))
    assert missing(verdict) == []


def test_branch_scan_preserves_checkout_and_worktree(lab: Lab) -> None:
    lab.branch("lane", {"plans/changes/lane/spec.md": artefact("demo-lane")})
    lab.fetch()
    lab.tracker(["demo-lane"])
    run(lab)  # creates the generated index first, so that only the search itself can change the tree
    (lab.work / "scratch.txt").write_text("untracked\n", encoding="utf-8")
    (lab.work / ".gitkeep").write_text("modified\n", encoding="utf-8")
    before = (git(lab.work, "rev-parse", "--abbrev-ref", "HEAD"), git(lab.work, "status", "--porcelain"))
    run(lab)
    after = (git(lab.work, "rev-parse", "--abbrev-ref", "HEAD"), git(lab.work, "status", "--porcelain"))
    assert after == before
    assert (lab.work / "scratch.txt").read_text(encoding="utf-8") == "untracked\n"
    assert (lab.work / ".gitkeep").read_text(encoding="utf-8") == "modified\n"
    assert not (lab.work / "plans" / "changes" / "lane").exists()


def test_default_check_never_searches_branches(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> None:
    lab.branch("lane", {"plans/changes/lane/spec.md": artefact("demo-lane")})
    lab.fetch()
    lab.tracker(["demo-lane"])

    def refuse(*_args, **_kwargs):
        raise AssertionError("an ordinary check must not read branches")

    monkeypatch.setattr(plans_registry.subprocess, "run", refuse)
    verdict = run(lab, branches=False)
    assert missing(verdict) == ["Bead 'demo-lane' is 'in_progress' but has no artefact under plans/changes/"]
    assert not any("branch" in f.message for f in verdict.findings)


def test_malformed_branch_frontmatter_is_counted_as_info(lab: Lab) -> None:
    bare = "# No header\n\nbead: demo-body\n"
    broken = "---\nbead: [\n---\n\n# Broken\n"
    lab.branch("a", {"plans/changes/x/spec.md": bare, "plans/changes/y/plan.md": broken})
    lab.branch("b", {"plans/changes/x/spec.md": bare})
    lab.fetch()
    lab.tracker(["demo-body"])
    verdict = run(lab)
    assert missing(verdict) == ["Bead 'demo-body' is 'in_progress' but has no artefact under plans/changes/"]
    assert messages(verdict, Level.BLOCK) == []
    counted = [m for m in messages(verdict, Level.INFO) if "branch files with absent or unreadable" in m]
    assert len(counted) == 1
    assert counted[0].startswith("3 branch files")


def test_branch_sample_is_sorted_and_bounded(lab: Lab) -> None:
    lab.branch("d", {"plans/changes/b1/spec.md": artefact("demo-b1")})
    lab.branch("a", {"plans/changes/b1/spec.md": artefact("demo-b1")})
    lab.branch(
        "b",
        {"plans/changes/b2/spec.md": artefact("demo-b2"), "plans/changes/b3/spec.md": artefact("demo-b3")},
    )
    lab.branch("c", {"plans/changes/b4/spec.md": artefact("demo-b4")})
    lab.branch("z", {"plans/changes/b5/spec.md": artefact("demo-b5")})
    lab.fetch()
    lab.tracker(["demo-b1", "demo-b2", "demo-b3", "demo-b4", "demo-b5"])
    verdict = run(lab)
    (found,) = summary(verdict)
    assert found.message.startswith("5 running beads checked, 5 found only on branches")
    assert "branch-only on: origin/a, origin/b, origin/b" in found.detail
    assert "origin/c" not in found.detail
    assert "origin/d" not in found.detail


def test_branch_scan_excludes_head_and_includes_main(lab: Lab) -> None:
    lab.branch("feature", {"plans/changes/f/spec.md": artefact("demo-f")})
    lab.branch("main", {"plans/changes/m/spec.md": artefact("demo-m")})
    lab.fetch()
    git(lab.work, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/feature")
    lab.tracker(["demo-f", "demo-m"])
    verdict = run(lab)
    (found,) = summary(verdict)
    assert "2 found only on branches" in found.message
    assert "branch-only on: origin/feature, origin/main" in found.detail
    assert "origin/HEAD" not in found.detail


def test_branch_artefacts_use_tree_frontmatter_semantics(lab: Lab) -> None:
    def header(*lines: str) -> str:
        return "---\n" + "\n".join(lines) + "\n---\n\n# Body\n"

    lab.branch(
        "sem",
        {
            "plans/changes/q/spec.md": header('bead: "demo-quoted"'),
            "plans/changes/e/spec.md": header('bead: "demo-\\x65scaped"'),
            "plans/changes/al/spec.md": header("base: &b demo-aliased", "bead: *b"),
            "plans/changes/mk/spec.md": header("defaults: &d", "  bead: demo-merged", "<<: *d"),
            "plans/changes/archive/old/spec.md": header("bead: demo-archived"),
            "plans/changes/body/spec.md": "# Only body\n\nbead: demo-bodyonly\n",
            "plans/changes/x/_note.md": header("bead: demo-underscore"),
            "plans/changes/INDEX.md": header("bead: demo-index"),
        },
    )
    lab.fetch()
    wanted = [
        "demo-quoted",
        "demo-escaped",
        "demo-aliased",
        "demo-merged",
        "demo-archived",
        "demo-bodyonly",
        "demo-underscore",
        "demo-index",
    ]
    lab.tracker(wanted)
    verdict = run(lab)
    still_missing = sorted(m.split("'")[1] for m in missing(verdict))
    assert still_missing == ["demo-bodyonly", "demo-index", "demo-underscore"]


def test_search_skipped_when_nothing_unresolved(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> None:
    lab.branch("lane", {"plans/changes/lane/spec.md": artefact("demo-lane")})
    lab.fetch()

    def refuse(*_args, **_kwargs):
        raise AssertionError("no branch search was due")

    monkeypatch.setattr(plans_registry.subprocess, "run", refuse)

    # the tracker is unavailable
    verdict = run(lab)
    assert not any("branch" in f.message.lower() for f in verdict.findings)

    # no bead is running
    lab.tracker([])
    verdict = run(lab)
    assert not any("branch" in f.message.lower() for f in verdict.findings)

    # every running bead has an artefact in the checked tree
    lab.tree({"plans/changes/tree/spec.md": artefact("demo-tree")})
    lab.tracker(["demo-tree"])
    verdict = run(lab)
    assert not any("branch" in f.message.lower() for f in verdict.findings)
