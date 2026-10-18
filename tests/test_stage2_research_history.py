"""Local frozen-HEAD history contracts, using only disposable Git repositories."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


def module():
    import stage2_research_history

    return stage2_research_history


def git(root, *args, env=None):
    done = subprocess.run(
        [
            "git",
            "--literal-pathspecs",
            "-C",
            str(root),
            "-c",
            "core.hooksPath=" + os.devnull,
            "-c",
            "core.fsmonitor=false",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "user.name=History Contract",
            "-c",
            "user.email=history@example.invalid",
            *args,
        ],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout.strip()


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-q")
    return tmp_path


def commit(root, subject, body=None, paths=("a.py",), env=None):
    git(root, "add", "--", *paths)
    args = ["commit", "-q", "-m", subject]
    if body is not None:
        args.extend(["-m", body])
    git(root, *args, env=env)
    return git(root, "rev-parse", "HEAD")


def packet(root, head, paths):
    return module().build_research_history(root, head, paths, deadline=time.monotonic() + 30)


def test_history_uses_frozen_head_and_never_current_working_bytes(repo):
    (repo / "a.py").write_text("VALUE = 1\n")
    first = commit(repo, "first")
    (repo / "a.py").write_text("VALUE = 2\n")
    later = commit(repo, "later")
    (repo / "a.py").write_text("UNCOMMITTED = 3\n")
    result = packet(repo, first, ["a.py"])
    assert result["frozen_head"] == first
    assert result["paths"] == {"a.py": [first]}
    assert later not in result["commits"]
    assert result["commits"][first]["subject"] == "first"
    assert result["commits"][first]["touched_mapped_paths"] == ["a.py"]


def test_history_ten_per_path_and_shared_commits_preserve_all_mapped_touches(repo):
    hashes = []
    for index in range(12):
        (repo / "a.py").write_text(f"VALUE = {index}\n")
        touched = ["a.py"]
        if index in (0, 11):
            (repo / "b.py").write_text(f"PEER = {index}\n")
            touched.append("b.py")
        hashes.append(commit(repo, f"change {index}", paths=touched))
    result = packet(repo, hashes[-1], ["a.py", "b.py", "a.py"])
    assert result["paths"]["a.py"] == list(reversed(hashes[-10:]))
    assert result["paths"]["b.py"] == [hashes[-1], hashes[0]]
    assert len(result["commits"]) == 11
    assert result["commits"][hashes[-1]]["touched_mapped_paths"] == ["a.py", "b.py"]
    assert any(item["path"] == "a.py" for item in result["not_read"])
    assert not any(item["path"] == "b.py" for item in result["not_read"])


def test_history_author_date_is_utc_and_body_cap_counts_unicode(repo):
    (repo / "a.py").write_text("VALUE = 1\n")
    env = {
        **os.environ,
        "GIT_AUTHOR_DATE": "2000-01-01T08:00:00+08:00",
        "GIT_COMMITTER_DATE": "2000-01-01T08:00:00+08:00",
    }
    head = commit(repo, "Unicode body", "ü" * 4500, env=env)
    record = packet(repo, head, ["a.py"])["commits"][head]
    assert record["author_utc"] == "2000-01-01T00:00:00Z"
    assert record["subject"] == "Unicode body"
    assert record["body"] == "ü" * 4000 and record["body_truncated"]


def test_history_pathspec_magic_is_a_literal_filename(repo):
    literal = ":(glob)*.py"
    (repo / literal).write_text("literal\n")
    first = commit(repo, "literal", paths=[literal])
    (repo / "a.py").write_text("ordinary\n")
    head = commit(repo, "ordinary")
    result = packet(repo, head, [literal])
    assert result["paths"][literal] == [first]
    assert head not in result["commits"]


def test_history_untracked_mapped_file_has_measured_empty_history(repo):
    (repo / "a.py").write_text("committed\n")
    head = commit(repo, "baseline")
    (repo / "new.py").write_text("untracked\n")
    result = packet(repo, head, ["new.py"])
    assert result["paths"] == {"new.py": []}
    assert result["commits"] == {}
    assert result["not_read"][0]["outcome"] == "measured-empty"


@pytest.mark.parametrize("head", ["HEAD", "", "1234567", "--all", None])
def test_history_requires_a_full_frozen_hash_before_git(head, monkeypatch):
    history = module()
    monkeypatch.setattr(history, "_git", lambda *_args: pytest.fail("invalid identity started Git"))
    with pytest.raises(history.ResearchHistoryError):
        packet(Path(), head, [])


@pytest.mark.parametrize("path", ["../outside.py", "/absolute.py", "a//b.py", "a/../b.py", "a\0.py"])
def test_history_path_validation_precedes_git(path, monkeypatch):
    history = module()
    monkeypatch.setattr(history, "_git", lambda *_args: pytest.fail("invalid path started Git"))
    with pytest.raises(history.ResearchHistoryError):
        packet(Path(), "a" * 40, [path])


def test_history_all_commands_are_local_and_ignore_ambient_repository_overrides(repo, monkeypatch):
    (repo / "a.py").write_text("VALUE = 1\n")
    head = commit(repo, "local")
    history = module()
    original = history.subprocess.run
    calls = []
    monkeypatch.setenv("GIT_DIR", "/nonexistent-ambient-repo")
    monkeypatch.setenv("OPENCODE_API_KEY", "synthetic-never-pass-to-history")

    def checked(*args, **kwargs):
        env = kwargs["env"]
        assert env["GIT_NO_LAZY_FETCH"] == env["GIT_LITERAL_PATHSPECS"] == env["GIT_NO_REPLACE_OBJECTS"] == "1"
        assert env["GIT_ALLOW_PROTOCOL"] == "" and env["GIT_TERMINAL_PROMPT"] == "0"
        assert env["GIT_CONFIG_GLOBAL"] == env["GIT_CONFIG_SYSTEM"] == os.devnull
        assert "GIT_DIR" not in env and "OPENCODE_API_KEY" not in env
        calls.append(args[0])
        return original(*args, **kwargs)

    monkeypatch.setattr(history.subprocess, "run", checked)
    assert packet(repo, head, ["a.py"])["paths"]["a.py"] == [head]
    assert calls


def test_history_missing_local_object_is_a_failure_not_empty_evidence(repo):
    with pytest.raises(module().ResearchHistoryError) as failure:
        packet(repo, "a" * 40, ["a.py"])
    assert failure.value.exit_code == 1


def test_history_expired_shared_deadline_starts_no_child(repo, monkeypatch):
    history = module()
    monkeypatch.setattr(history.subprocess, "run", lambda *_args, **_kwargs: pytest.fail("deadline started a child"))
    with pytest.raises(history.ResearchHistoryError, match="deadline"):
        history.build_research_history(repo, "a" * 40, ["a.py"], deadline=time.monotonic() - 1)


@pytest.mark.parametrize("deadline", [float("nan"), float("inf"), "later", None, True])
def test_history_deadline_must_be_a_finite_number_before_git(deadline, monkeypatch):
    history = module()
    monkeypatch.setattr(history, "_git", lambda *_args: pytest.fail("invalid deadline started Git"))
    with pytest.raises(history.ResearchHistoryError, match="deadline"):
        history.build_research_history(Path(), "a" * 40, [], deadline=deadline)


def test_history_repository_wide_dot_is_not_a_mapped_file(monkeypatch):
    history = module()
    monkeypatch.setattr(history, "_git", lambda *_args: pytest.fail("dot path started Git"))
    with pytest.raises(history.ResearchHistoryError):
        packet(Path(), "a" * 40, ["."])


def test_history_shallow_boundary_is_not_complete_or_measured_empty(repo, tmp_path):
    (repo / "a.py").write_text("first\n")
    commit(repo, "first")
    (repo / "a.py").write_text("second\n")
    head = commit(repo, "second")
    shallow = tmp_path / "shallow"
    git(repo, "clone", "-q", "--depth=1", repo.as_uri(), str(shallow))
    result = packet(shallow, head, ["a.py", "unknown.py"])
    assert result["paths"] == {"a.py": [head], "unknown.py": []}
    assert {row["path"] for row in result["not_read"]} == {"a.py", "unknown.py"}
    assert all(row["shallow"] and "outcome" not in row for row in result["not_read"])


def test_history_replace_objects_cannot_change_frozen_commit_evidence(repo):
    (repo / "a.py").write_text("original\n")
    original = commit(repo, "original subject")
    (repo / "a.py").write_text("replacement\n")
    replacement = commit(repo, "replacement subject")
    git(repo, "replace", original, replacement)
    record = packet(repo, original, ["a.py"])["commits"][original]
    assert record["subject"] == "original subject"
    assert record["touched_mapped_paths"] == ["a.py"]


def test_history_timeout_is_one_failure_without_retry(repo, monkeypatch):
    history = module()
    calls = []

    def expired(*args, **kwargs):
        calls.append(args[0])
        raise subprocess.TimeoutExpired(args[0], kwargs["timeout"])

    monkeypatch.setattr(history.subprocess, "run", expired)
    with pytest.raises(history.ResearchHistoryError) as failure:
        packet(repo, "a" * 40, ["a.py"])
    assert failure.value.exit_code == 1 and len(calls) == 1


def test_history_rechecks_shared_deadline_before_every_command(repo, monkeypatch):
    history = module()
    calls = []
    monkeypatch.setattr(history.time, "monotonic", iter([1.0, 3.0]).__next__)

    def first(*args, **kwargs):
        calls.append(args[0])
        assert kwargs["timeout"] == 1.0
        return subprocess.CompletedProcess(args[0], 0, "commit\n", "")

    monkeypatch.setattr(history.subprocess, "run", first)
    with pytest.raises(history.ResearchHistoryError, match="deadline"):
        history.build_research_history(repo, "a" * 40, ["a.py"], deadline=2.0)
    assert len(calls) == 1


def test_history_missing_objects_cannot_invoke_a_promisor_remote(repo):
    history = module()
    (repo / "a.py").write_text("local\n")
    commit(repo, "baseline")
    marker = repo / "transport-was-run"
    transport = repo / "transport"
    transport.write_text('#!/bin/sh\n: > "' + str(marker) + '"\nexit 1\n')
    transport.chmod(0o755)
    git(repo, "config", "remote.origin.url", "ext::" + str(transport))
    git(repo, "config", "remote.origin.promisor", "true")
    git(repo, "config", "remote.origin.partialclonefilter", "blob:none")
    git(repo, "config", "protocol.ext.allow", "always")
    with pytest.raises(history.ResearchHistoryError):
        packet(repo, "a" * 40, ["a.py"])
    assert not marker.exists()


@pytest.mark.parametrize("encoding", ["UTF-8", "ISO-8859-1"])
def test_history_metadata_output_is_utf8_despite_local_display_encoding(repo, encoding):
    (repo / "a.py").write_text("VALUE = 1\n")
    head = commit(repo, "Unicode ü subject", "Unicode ü body")
    git(repo, "config", "i18n.logOutputEncoding", encoding)
    failure = None
    result = None
    try:
        result = packet(repo, head, ["a.py"])
    except module().ResearchHistoryError as error:
        failure = str(error)
    assert failure is None, "valid Unicode metadata must use deterministic UTF-8 output: " + str(failure)
    assert result["commits"][head]["subject"] == "Unicode ü subject"
    assert result["commits"][head]["body"].rstrip() == "Unicode ü body"
