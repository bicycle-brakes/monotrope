"""The central harness configuration holds (criteria 1-7 of central-config).

Every mutation case runs against files of its own — synthetic roots and the
real checker subprocess — so no test edits the real policy. The one live-tree
assertion is the owned value itself: `config/harness/` travels with the kit,
so this holds in the probe copy too.
"""

from __future__ import annotations

import dataclasses
import os
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKER = REPO_ROOT / "scripts" / "check_harness_config.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import harness_config  # noqa: E402

KEY = "lanes.writing_sessions_per_repository"
PLACEHOLDER = "{{ harness.lanes.writing_sessions_per_repository }}"


def marker(value: object) -> str:
    """The prose marker spelling for one value."""
    return f"<!-- harness-config: {KEY} -->{value}<!-- /harness-config -->"


def build_root(
    tmp_path: Path,
    count: int = 2,
    *,
    name: str = "repo",
    agents: str | None = None,
    implement: str | None = None,
    lanes: str | None = None,
    scripts: dict[str, str] | None = None,
) -> Path:
    """A synthetic repository whose central configuration and bindings agree by default."""
    root = tmp_path / name
    (root / "config" / "harness").mkdir(parents=True)
    (root / "config" / "harness" / "lanes.yaml").write_text(
        lanes if lanes is not None else f"writing_sessions_per_repository: {count}\n", encoding="utf-8"
    )
    (root / "prompts").mkdir()
    (root / "prompts" / "04-implement.md").write_text(
        implement if implement is not None else f"limit {PLACEHOLDER}\n", encoding="utf-8"
    )
    (root / "AGENTS.md").write_text(
        agents if agents is not None else f"at most {marker(count)} sessions\n", encoding="utf-8"
    )
    (root / "scripts").mkdir()
    for relative, source in (scripts or {}).items():
        module = root / "scripts" / relative
        module.parent.mkdir(parents=True, exist_ok=True)
        module.write_text(source, encoding="utf-8")
    return root


def run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    """The real checker subprocess against one root, in enforcement mode."""
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root), "--check"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def test_initial_session_limit_has_one_authority(tmp_path: Path) -> None:
    """Criterion 1. Planted fault: no owned setting, a changed initial count, or a live
    duplicate of the owned name is accepted."""
    snapshot = harness_config.load(REPO_ROOT)
    assert snapshot.config.lanes.writing_sessions_per_repository == 2, "the initial policy is not two"
    assert len(snapshot.sources) == 1, "the owned setting is declared more than once"

    changed = build_root(tmp_path, count=3, name="changed")
    assert run_checker(changed).returncode == 0, "one changed value with agreeing prose is one authority"

    duplicate = build_root(
        tmp_path,
        scripts={"lane_copy.py": "WRITING_SESSIONS_PER_REPOSITORY = 2\n"},
        name="duplicate",
    )
    done = run_checker(duplicate)
    assert done.returncode == 1, "a live numeric duplicate passed the checker"
    assert "lane_copy.py" in done.stdout + done.stderr

    missing = tmp_path / "no-configuration"
    missing.mkdir()
    assert run_checker(missing).returncode == 3, "a missing owned setting was not refused"


def test_one_schema_rejects_unknown_topics_keys_and_bad_counts(tmp_path: Path) -> None:
    """Criterion 2. Planted fault: an extra topic or key, a subdirectory entry, a renamed
    topic, an empty directory, or a Boolean, string or non-positive count is accepted."""
    cases: dict[str, dict[str, str]] = {
        "extra-topic": {"models.yaml": "temperature: 0.2\n"},
        "subdirectory": {},
        "extra-key": {"lanes.yaml": "writing_sessions_per_repository: 2\ndefault: 2\n"},
        "bool-count": {"lanes.yaml": "writing_sessions_per_repository: true\n"},
        "string-count": {"lanes.yaml": 'writing_sessions_per_repository: "2"\n'},
        "zero-count": {"lanes.yaml": "writing_sessions_per_repository: 0\n"},
        "negative-count": {"lanes.yaml": "writing_sessions_per_repository: -1\n"},
        "no-topic": {"renamed.yaml": "writing_sessions_per_repository: 2\n"},
        "empty-directory": {},
    }
    for name, files in cases.items():
        root = tmp_path / name
        directory = root / "config" / "harness"
        directory.mkdir(parents=True)
        if name == "subdirectory":
            (directory / "nested").mkdir()
        for filename, text in files.items():
            (directory / filename).write_text(text, encoding="utf-8")
        with pytest.raises(harness_config.HarnessConfigError) as raised:
            harness_config.load(root)
        message = str(raised.value)
        assert "config/harness" in message, (name, message)
        assert message.split(": ", 1)[-1].strip(), (name, "the refusal carries no reason")


def test_unusable_config_has_path_and_reason_without_defaults(tmp_path: Path) -> None:
    """Criterion 3. Planted fault: malformed, missing, unreadable, duplicate-key or
    merge-key input yields usable settings instead of the refusal."""
    cases: dict[str, bytes | None] = {
        "malformed": b"writing_sessions_per_repository: [unclosed\n",
        "duplicate-key": b"writing_sessions_per_repository: 2\nwriting_sessions_per_repository: 3\n",
        "merge-key": (b"defaults: &d\n  writing_sessions_per_repository: 2\nlanes:\n  <<: *d\n"),
        "invalid-utf8": b"writing_sessions_per_repository: \xff\xfe\n",
        "empty": b"",
        "missing-file": None,
    }
    for name, payload in cases.items():
        root = tmp_path / name
        directory = root / "config" / "harness"
        directory.mkdir(parents=True)
        if payload is not None:
            (directory / "lanes.yaml").write_bytes(payload)
        with pytest.raises(harness_config.HarnessConfigError) as raised:
            harness_config.load(root)
        message = str(raised.value)
        assert "config/harness" in message, (name, message)
        assert message.split(": ", 1)[-1].strip(), (name, "the refusal carries no reason")

    gone = tmp_path / "gone"
    with pytest.raises(harness_config.HarnessConfigError) as raised:
        harness_config.load(gone)
    assert str(gone) in str(raised.value), "the refusal does not name the missing directory"

    locked = tmp_path / "unreadable" / "config" / "harness" / "lanes.yaml"
    locked.parent.mkdir(parents=True)
    locked.write_text("writing_sessions_per_repository: 2\n", encoding="utf-8")
    locked.chmod(0o000)
    try:
        if os.geteuid() != 0:
            with pytest.raises(harness_config.HarnessConfigError) as raised:
                harness_config.load(locked.parent.parent.parent)
            assert "cannot be read" in str(raised.value), str(raised.value)
    finally:
        locked.chmod(0o644)


def test_prompt_render_uses_one_snapshot_and_refreshes_next_time(tmp_path: Path) -> None:
    """Criterion 4. Planted fault: an intervening edit changes the captured view, or the
    next render stays stale."""
    root = build_root(tmp_path, count=2)
    first = harness_config.load(root)
    template = f"limit {PLACEHOLDER}\n"
    assert harness_config.render(first, template, "prompts/04-implement.md") == "limit 2\n"

    (root / "config" / "harness" / "lanes.yaml").write_text("writing_sessions_per_repository: 4\n", encoding="utf-8")
    assert harness_config.render(first, template) == "limit 2\n", "the edit changed the captured composition"
    assert first.sources == ((root / "config" / "harness" / "lanes.yaml", b"writing_sessions_per_repository: 2\n"),)

    second = harness_config.load(root)
    assert harness_config.render(second, template) == "limit 4\n", "the next composition stayed stale"
    assert second.config.lanes.writing_sessions_per_repository == 4

    with pytest.raises(ValidationError):
        first.config.lanes.writing_sessions_per_repository = 5
    with pytest.raises(dataclasses.FrozenInstanceError):
        first.config = second.config


def test_unknown_or_malformed_reserved_placeholder_refuses(tmp_path: Path) -> None:
    """Criterion 4's placeholder half. Planted fault: an unresolved reserved token survives
    the render, or an expression inside one is evaluated."""
    snapshot = harness_config.load(build_root(tmp_path))
    malformed = [
        "{{ harness.lanes.not_a_setting }}",
        "{{ harness.lanes }}",
        "{{ harness }}",
        "{{ harness.lanes.writing_sessions_per_repository",
        "{{ harness.lanes.writing_sessions_per_repository | default(9) }}",
        "{{ harness.lanes.writing_sessions_per_repository.extra }}",
        "{{ harness.lanes.__class__ }}",
    ]
    for token in malformed:
        with pytest.raises(harness_config.HarnessConfigError) as raised:
            harness_config.render(snapshot, f"limit {token}\n", "prompts/04-implement.md")
        message = str(raised.value)
        assert "prompts/04-implement.md" in message, (token, message)
        assert any(
            word in message
            for word in (
                "unknown setting",
                "malformed reserved token",
                "not resolved",
                "below a scalar value",
                "only a scalar value renders",
            )
        ), (token, message)

    assert harness_config.render(snapshot, f"limit {PLACEHOLDER}\n") == "limit 2\n"
    spaced = "limit {{  harness.lanes.writing_sessions_per_repository  }}\n"
    assert harness_config.render(snapshot, spaced) == "limit 2\n"
    assert harness_config.render(snapshot, "no token here\n") == "no token here\n"


def test_checker_rejects_stale_missing_or_unknown_prose_bindings(tmp_path: Path) -> None:
    """Criterion 6. Planted fault: changed prose, a deleted required marker, a marker naming
    an unknown setting, or a malformed marker passes the real checker."""
    stale = build_root(tmp_path, count=2, agents=f"at most {marker(5)} sessions\n")
    done = run_checker(stale)
    assert done.returncode == 1, "changed prose passed the real checker"
    assert "AGENTS.md" in done.stdout + done.stderr
    assert "states '5'" in done.stdout + done.stderr, done.stdout + done.stderr

    missing = build_root(tmp_path, count=2, agents="at most 2 sessions\n", name="missing")
    done = run_checker(missing)
    assert done.returncode == 1, "a deleted required marker passed"
    assert "required marker" in done.stdout + done.stderr

    unknown = build_root(
        tmp_path,
        count=2,
        agents="x <!-- harness-config: lanes.other -->2<!-- /harness-config --> y\n",
        name="unknown",
    )
    done = run_checker(unknown)
    assert done.returncode == 1, "a marker naming an unknown setting passed"
    assert "unknown setting" in done.stdout + done.stderr

    malformed = build_root(tmp_path, count=2, agents=f"x <!-- harness-config: {KEY} -->2 sessions\n", name="malformed")
    done = run_checker(malformed)
    assert done.returncode == 1, "a malformed marker passed"
    assert "malformed" in done.stdout + done.stderr


def test_checker_rejects_named_duplicates_and_literalized_prompt(tmp_path: Path) -> None:
    """Criterion 7. Planted fault: a canonical, uppercase, annotated, attribute or dict-key
    numeric declaration of the owned name, or a literalized placeholder, passes the checker."""
    declarations = {
        "canonical": "writing_sessions_per_repository = 2\n",
        "uppercase": "WRITING_SESSIONS_PER_REPOSITORY = 2\n",
        "annotated": "writing_sessions_per_repository: int = 2\n",
        "attribute": "settings.writing_sessions_per_repository = 2\n",
        "dict-key": 'LIMITS = {"writing_sessions_per_repository": 2}\n',
    }
    for name, source in declarations.items():
        root = build_root(tmp_path, scripts={"drift_mod.py": source}, name=name)
        done = run_checker(root)
        assert done.returncode == 1, f"{name} passed the real checker"
        assert "drift_mod.py" in done.stdout + done.stderr, name
        assert str(REPO_ROOT / "config") not in done.stdout + done.stderr, "the synthetic root is not scanned"

    literal = build_root(tmp_path, implement="limit 2\n", name="literalized")
    done = run_checker(literal)
    assert done.returncode == 1, "a literalized placeholder passed"
    assert "04-implement.md" in done.stdout + done.stderr

    tests_only = build_root(
        tmp_path,
        scripts={"test_drift_mod.py": "writing_sessions_per_repository = 2\n"},
        name="tests",
    )
    assert run_checker(tests_only).returncode == 0, "test fixtures are not duplicate-authority inputs"


def test_checker_goes_red_on_drift_and_distinguishes_unreadable(tmp_path: Path) -> None:
    """Mutation evidence for the harness-config gate: the real checker subprocess notices
    tampering. Planted fault: drift or unreadable evidence exits 0."""
    green = run_checker(build_root(tmp_path))
    assert green.returncode == 0, f"measured agreement failed: {green.stdout + green.stderr}"

    stale = run_checker(build_root(tmp_path, count=2, agents=f"at most {marker(7)} sessions\n", name="stale"))
    assert stale.returncode == 1, "drift did not turn the check red"
    assert "states '7'" in stale.stdout + stale.stderr, "the drift does not name the marked value"

    unreadable = run_checker(build_root(tmp_path, lanes="writing_sessions_per_repository: [oops\n", name="unreadable"))
    assert unreadable.returncode == 3, "unreadable evidence did not get its own exit code"
    assert "lanes.yaml" in unreadable.stdout + unreadable.stderr
