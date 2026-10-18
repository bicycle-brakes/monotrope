"""Frozen research input contracts using disposable repositories and canaries."""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from test_stage2_research_history import commit, git

CHANGE = "plans/changes/example"
RESEARCH = CHANGE + "/research.md"


def module():
    import stage2_research_snapshot

    return stage2_research_snapshot


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / CHANGE).mkdir(parents=True)
    (root / RESEARCH).write_bytes(b"---\nupdated: 2000-01-01\n---\nOriginal research\n")
    (root / "a.py").write_bytes(b"VALUE = 1\n")
    (root / ".gitignore").write_bytes(b"ignored.txt\n")
    commit(root, "baseline", paths=["a.py", RESEARCH, ".gitignore"])
    return root


def freeze(repo, **kwargs):
    return module().freeze_research_state(repo, CHANGE, deadline=time.monotonic() + 30, **kwargs)


def test_snapshot_keeps_uncommitted_tracked_and_nonignored_change_bytes(repo):
    (repo / "a.py").write_bytes(b"UNCOMMITTED = 2\n")
    (repo / CHANGE / "new.md").write_bytes(b"new change input\n")
    (repo / CHANGE / "ignored.txt").write_bytes(b"ignored canary\n")
    (repo / "outside.md").write_bytes(b"unrelated untracked canary\n")
    with freeze(repo) as state:
        sources = state.sources()
        manifest = state.manifest()
        assert sources["a.py"] == b"UNCOMMITTED = 2\n"
        assert sources[CHANGE + "/new.md"] == b"new change input\n"
        assert CHANGE + "/ignored.txt" not in sources and "outside.md" not in sources
        assert manifest["untracked"] == {CHANGE + "/new.md": hashlib.sha256(b"new change input\n").hexdigest()}
        assert manifest["head"] == git(repo, "rev-parse", "HEAD")
        assert not state.directory.resolve().is_relative_to(repo.resolve())
        assert state.changed_paths() == []
        assert "Original research" not in str(manifest)


def test_snapshot_copies_stay_frozen_and_are_deleted_on_exit(repo):
    with freeze(repo) as state:
        directory = state.directory
        (repo / "a.py").write_bytes(b"later\n")
        assert state.sources()["a.py"] == b"VALUE = 1\n"
        assert state.changed_paths() == ["a.py"]
    assert not directory.exists()


def test_snapshot_copies_are_deleted_on_consumer_abort(repo):
    with pytest.raises(RuntimeError), freeze(repo) as state:
        directory = state.directory
        raise RuntimeError("consumer aborted")
    assert not directory.exists()


def test_snapshot_digest_binds_working_bytes_and_manifest_does_not_alias(repo):
    with freeze(repo) as first, freeze(repo) as same:
        original = first.manifest()
        assert original == same.manifest()
        original["paths"].clear()
        assert first.manifest()["paths"]
        (repo / "a.py").write_bytes(b"VALUE = 2\n")
        with freeze(repo) as changed:
            assert changed.manifest()["head"] == first.manifest()["head"]
            assert changed.manifest()["digest"] != first.manifest()["digest"]


@pytest.mark.parametrize("operation", ["add", "remove", "edit"])
def test_snapshot_detects_untracked_change_input_set_and_byte_drift(repo, operation):
    path = repo / CHANGE / "input.md"
    if operation != "add":
        path.write_bytes(b"first\n")
    with freeze(repo) as state:
        if operation == "remove":
            path.unlink()
        else:
            path.write_bytes(b"second\n")
        assert state.changed_paths() == [CHANGE + "/input.md"]


def test_snapshot_detects_new_tracked_paths_and_changed_head(repo):
    with freeze(repo) as state:
        (repo / "other.py").write_bytes(b"new\n")
        commit(repo, "later", paths=["other.py"])
        assert state.changed_paths() == ["HEAD", "other.py"]


def test_snapshot_does_not_treat_any_research_append_as_runner_owned(repo):
    original = (repo / RESEARCH).read_bytes()
    expected = original + b"\nRunner audit\n"
    with freeze(repo) as state:
        (repo / RESEARCH).write_bytes(expected)
        assert state.changed_paths() == [RESEARCH]
        assert state.changed_paths(owned_research_bytes=expected) == []
        (repo / RESEARCH).write_bytes(expected + b"Foreign appended bytes\n")
        assert state.changed_paths(owned_research_bytes=expected) == [RESEARCH]


def test_snapshot_runner_restamp_may_not_rewrite_frozen_research_body(repo):
    original = (repo / RESEARCH).read_bytes()
    with freeze(repo) as state:
        expected = original.replace(b"2000-01-01", b"2000-01-02") + b"\nAudit\n"
        (repo / RESEARCH).write_bytes(expected)
        assert state.changed_paths(owned_research_bytes=expected) == []
        rewritten = expected.replace(b"Original research", b"Rewritten research")
        (repo / RESEARCH).write_bytes(rewritten)
        with pytest.raises(module().ResearchSnapshotError, match="prefix"):
            state.changed_paths(owned_research_bytes=rewritten)


def test_snapshot_missing_tracked_file_refuses_and_cleans_preparation(repo, tmp_path):
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    (repo / "a.py").unlink()
    with pytest.raises(module().ResearchSnapshotError):
        freeze(repo, scratch_parent=scratch)
    assert list(scratch.iterdir()) == []


@pytest.mark.parametrize("directory", [False, True])
def test_snapshot_never_follows_file_or_parent_symlink(repo, tmp_path, directory):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "private.txt").write_bytes(b"synthetic ambient canary\n")
    if directory:
        parent = repo / "nested"
        parent.mkdir()
        (parent / "private.txt").write_bytes(b"tracked input\n")
        commit(repo, "nested input", paths=["nested/private.txt"])
        (parent / "private.txt").unlink()
        parent.rmdir()
        parent.symlink_to(outside, target_is_directory=True)
    else:
        (repo / "a.py").unlink()
        (repo / "a.py").symlink_to(outside / "private.txt")
    with pytest.raises(module().ResearchSnapshotError):
        freeze(repo)


def test_snapshot_refuses_copies_inside_repository(repo):
    with pytest.raises(module().ResearchSnapshotError, match="outside"):
        freeze(repo, scratch_parent=repo)
    assert not list(repo.glob("research-inputs-*"))


def test_snapshot_expired_deadline_reads_no_file(repo, monkeypatch):
    snapshot = module()
    monkeypatch.setattr(snapshot, "_read", lambda *_args: pytest.fail("expired snapshot read a file"))
    with pytest.raises(snapshot.ResearchSnapshotError):
        snapshot.freeze_research_state(repo, CHANGE, deadline=time.monotonic() - 1)


def test_snapshot_mid_freeze_change_refuses_and_cleans_copies(repo, tmp_path, monkeypatch):
    snapshot = module()
    original = snapshot._read
    changed = False
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    def changing(root, path, deadline):
        nonlocal changed
        result = original(root, path, deadline)
        if path == "a.py" and not changed:
            changed = True
            (root / path).write_bytes(b"changed during freeze\n")
        return result

    monkeypatch.setattr(snapshot, "_read", changing)
    with pytest.raises(snapshot.ResearchSnapshotError, match="changed"):
        freeze(repo, scratch_parent=scratch)
    assert list(scratch.iterdir()) == []


@pytest.mark.parametrize("deadline", [float("nan"), float("inf"), None, "later", True])
def test_snapshot_invalid_deadline_starts_no_git(repo, monkeypatch, deadline):
    snapshot = module()
    monkeypatch.setattr(snapshot, "_git", lambda *_args: pytest.fail("invalid deadline started Git"))
    with pytest.raises(snapshot.ResearchSnapshotError, match="deadline"):
        snapshot.freeze_research_state(repo, CHANGE, deadline=deadline)


def test_snapshot_interrupt_during_preparation_deletes_copies(repo, tmp_path, monkeypatch):
    snapshot = module()
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    def interrupt(*_args):
        raise KeyboardInterrupt

    monkeypatch.setattr(snapshot, "_read", interrupt)
    with pytest.raises(KeyboardInterrupt):
        freeze(repo, scratch_parent=scratch)
    assert list(scratch.iterdir()) == []


def test_snapshot_special_file_read_cannot_block_preparation(repo):
    import os

    os.mkfifo(repo / CHANGE / "pipe")
    with pytest.raises(module().ResearchSnapshotError, match="regular"):
        module()._read(repo, CHANGE + "/pipe", time.monotonic() + 30)
