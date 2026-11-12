"""The night profile: sourced asks become denies, and the launcher refuses to wait (plans/changes/night-stall-guard).

The subject is `tools/claude-code/night.py` with its `night-settings.json` fragment and the install
entries of `tools/claude-code/install.sh`. Every run works in a temporary home (`CLAUDE_CONFIG_DIR`
and `HOME`), a temporary project directory and a fake `claude` executable that records its arguments
and the overlay it was given; nothing here touches the maintainer's real `~/.claude` or real settings.
A fake child proves how the launcher constructs the call; actual Claude Code refusal behavior is the
isolated runtime probe the plan names separately, not a test.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO = Path(__file__).resolve().parent.parent
NIGHT_PY = REPO / "tools" / "claude-code" / "night.py"
NIGHT_FRAGMENT = REPO / "tools" / "claude-code" / "night-settings.json"
INSTALLER = REPO / "tools" / "claude-code" / "install.sh"

ASK_RULE = "Bash(gh pr merge *)"
DENY_RULE = "Bash(git push *main*)"

# A fake `claude`: it records its argv, copies the overlay it was handed, notes that the overlay still
# existed while it ran (and the permission mode of its directory), and exits with CLAUDE_FAKE_EXIT.
FAKE_CLAUDE = """\
#!/usr/bin/env python3
import os
import shutil
import sys

args = sys.argv[1:]
record = os.environ["CLAUDE_FAKE_RECORD"]
with open(record + ".argv", "w", encoding="utf-8") as handle:
    handle.write("\\n".join(args))
overlay = args[args.index("--settings") + 1] if "--settings" in args else None
if overlay is not None:
    shutil.copyfile(overlay, record + ".overlay.json")
    mode = oct(os.stat(os.path.dirname(overlay)).st_mode & 0o777)
    with open(record + ".lifetime", "w", encoding="utf-8") as handle:
        handle.write(f"{os.path.exists(overlay)} {mode}")
sys.exit(int(os.environ.get("CLAUDE_FAKE_EXIT", "0")))
"""

_spec = importlib.util.spec_from_file_location("night_profile_module", NIGHT_PY)
night = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(night)


@pytest.fixture
def workspace(tmp_path: Path) -> SimpleNamespace:
    """A temporary home, a plain (non-Git) project directory and the fake `claude` on the PATH."""
    home = tmp_path / "home"
    project = tmp_path / "project"
    bin_dir = tmp_path / "bin"
    for directory in (home, project, bin_dir):
        directory.mkdir()
    fake = bin_dir / "claude"
    fake.write_text(FAKE_CLAUDE, encoding="utf-8")
    fake.chmod(0o755)
    env = dict(os.environ)
    env["HOME"] = str(home)
    env["CLAUDE_CONFIG_DIR"] = str(home / ".claude")
    env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"
    env["CLAUDE_FAKE_RECORD"] = str(tmp_path / "record")
    return SimpleNamespace(
        home=home,
        project=project,
        bin_dir=bin_dir,
        env=env,
        record=tmp_path / "record",
    )


def user_settings(ws: SimpleNamespace) -> Path:
    return ws.home / ".claude" / "settings.json"


def project_settings(ws: SimpleNamespace) -> Path:
    return ws.project / ".claude" / "settings.json"


def local_settings(ws: SimpleNamespace) -> Path:
    return ws.project / ".claude" / "settings.local.json"


def write_settings(path: Path, data: dict) -> bytes:
    """Write a settings fixture and return its bytes, so a test can hold the file against rewrites."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path.read_bytes()


def run_night(ws: SimpleNamespace, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(NIGHT_PY), *args],
        capture_output=True,
        text=True,
        env=ws.env,
        cwd=str(cwd or ws.project),
        timeout=60,
        check=False,
    )


def recorded(ws: SimpleNamespace, suffix: str) -> Path:
    return ws.record.with_name(ws.record.name + suffix)


def launched_argv(ws: SimpleNamespace) -> list[str]:
    return recorded(ws, ".argv").read_text(encoding="utf-8").split("\n")


def recorded_overlay(ws: SimpleNamespace) -> dict:
    return json.loads(recorded(ws, ".overlay.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("scope", ["user", "project", "local", "all"])
def test_inherited_asks_become_denies(workspace: SimpleNamespace, scope: str) -> None:
    """Criterion 1: an explicit ask rule in any supported scope is a deny rule in the night settings, not an ask."""
    targets = {
        "user": [user_settings(workspace)],
        "project": [project_settings(workspace)],
        "local": [local_settings(workspace)],
        "all": [user_settings(workspace), project_settings(workspace), local_settings(workspace)],
    }[scope]
    for path in targets:
        write_settings(path, {"permissions": {"ask": [ASK_RULE]}})
    done = run_night(workspace, "-p", "night check")
    assert done.returncode == 0, done.stderr
    overlay = recorded_overlay(workspace)
    assert overlay["permissions"]["defaultMode"] == "dontAsk"
    assert "ask" not in overlay["permissions"], "an inherited ask survived as an ask in the night settings"
    assert overlay["permissions"]["deny"] == [ASK_RULE]


def test_launcher_forces_noninteractive_permissions(workspace: SimpleNamespace) -> None:
    """Criterion 2, test half: the launched call and the overlay leave no interactive permission wait."""
    write_settings(
        user_settings(workspace),
        {"statusLine": {"type": "command"}, "permissions": {"ask": [ASK_RULE], "deny": [DENY_RULE]}},
    )
    write_settings(local_settings(workspace), {"permissions": {"deny": ["Bash(rm -rf /)"]}})
    passthrough = ["-p", "night work", "--model", "sonnet"]
    done = run_night(workspace, *passthrough)
    assert done.returncode == 0, done.stderr
    argv = launched_argv(workspace)
    assert argv[0] == "--settings" and Path(argv[1]).name == "settings.json"
    assert argv[2:4] == ["--permission-mode", "dontAsk"]
    assert argv[4:] == passthrough
    overlay = recorded_overlay(workspace)
    assert overlay["permissions"]["defaultMode"] == "dontAsk"
    assert "ask" not in overlay["permissions"]
    assert "allow" not in overlay["permissions"], "the night profile must not add blanket allows"
    deny = overlay["permissions"]["deny"]
    assert len(deny) == len(set(deny)), "the overlay repeats a deny rule"
    assert set(deny) == {ASK_RULE, DENY_RULE, "Bash(rm -rf /)"}
    assert set(overlay) == {"permissions"}, "inherited non-permission settings must stay in their native layers"
    assert recorded(workspace, ".lifetime").read_text(encoding="utf-8") == "True 0o700"
    assert not Path(argv[1]).exists(), "the overlay outlived the child"
    assert not Path(argv[1]).parent.exists(), "the private overlay directory outlived the child"


def test_day_permissions_remain_intact(workspace: SimpleNamespace) -> None:
    """Criterion 5: the night run keeps every unrelated day brake and rewrites no source file.

    The day fixture carries the narrowed merge asks beside the unrelated brakes — the alias and
    main-push asks, the Codex ask, the Omnigent ask and denies. None of them may disappear, no
    existing denial may be relaxed, and the day files must survive byte for byte.
    """
    day_user = {
        "permissions": {
            "ask": [
                "Bash(gh pr merge *)",
                "Bash(gh alias set *)",
                "Bash(git push *main*)",
                "Bash(codex *)",
                "mcp__omnigent__sys_advise_models",
            ],
            "deny": ["mcp__omnigent__sys_os_shell", "Edit(//**/.omnigent/config.yaml)"],
        }
    }
    day_project = {"statusLine": {"type": "command"}, "permissions": {"ask": ["Bash(gh -* pr merge*)"]}}
    day_local = {"permissions": {"deny": ["mcp__omnigent__sys_os_edit"]}}
    sources = (
        (user_settings(workspace), day_user),
        (project_settings(workspace), day_project),
        (local_settings(workspace), day_local),
    )
    before = {path: write_settings(path, data) for path, data in sources}
    done = run_night(workspace, "-p", "night check")
    assert done.returncode == 0, done.stderr
    for path, content in before.items():
        assert path.read_bytes() == content, f"the night run rewrote the day settings at {path}"
    deny = recorded_overlay(workspace)["permissions"]["deny"]
    for rule in (
        "Bash(gh alias set *)",
        "Bash(git push *main*)",
        "Bash(codex *)",
        "mcp__omnigent__sys_advise_models",
        "mcp__omnigent__sys_os_shell",
        "mcp__omnigent__sys_os_edit",
        "Edit(//**/.omnigent/config.yaml)",
        "Bash(gh pr merge *)",
        "Bash(gh -* pr merge*)",
    ):
        assert rule in deny, f"the night settings lost the day brake {rule!r}"


CONFLICTING_ARGS = (
    "--settings other.json",
    "--settings=other.json",
    "--permission-mode default",
    "--permission-mode=bypassPermissions",
    "--dangerously-skip-permissions",
)
BROKEN_SETTINGS = ("not-json", "not-object", "ask-not-list", "unreadable")


@pytest.mark.parametrize("case", [*CONFLICTING_ARGS, *BROKEN_SETTINGS])
def test_activation_is_scoped_and_refuses_invalid_overrides(workspace: SimpleNamespace, case: str) -> None:
    """Criterion 6: the selection binds one invocation; a conflicting argument or a broken settings
    file never starts Claude Code."""
    before = write_settings(user_settings(workspace), {"permissions": {"ask": [ASK_RULE]}})
    good = run_night(workspace, "-p", "night check")
    assert good.returncode == 0, good.stderr
    for suffix in (".argv", ".overlay.json", ".lifetime"):
        recorded(workspace, suffix).unlink(missing_ok=True)

    refusal_args = ["-p", "night check"]
    path = user_settings(workspace)
    if case in BROKEN_SETTINGS:
        if case == "not-json":
            path.write_text("{not json", encoding="utf-8")
        elif case == "not-object":
            path.write_text("[]", encoding="utf-8")
        elif case == "ask-not-list":
            write_settings(path, {"permissions": {"ask": [ASK_RULE, 5]}})
        else:
            path.unlink()
            path.mkdir()  # a directory where a readable settings file must be
    else:
        refusal_args += case.split()
    done = run_night(workspace, *refusal_args)
    assert done.returncode != 0, f"{case!r} silently replaced or ignored the night profile"
    assert not recorded(workspace, ".argv").exists(), f"claude started despite {case!r}"
    if case in BROKEN_SETTINGS:
        assert str(path) in done.stderr, done.stderr
    else:
        assert case.split()[0].split("=")[0] in done.stderr
        assert path.read_bytes() == before, "the refusal run changed the day settings"


@pytest.mark.parametrize("absent", ["user", "project", "local", "none"])
def test_a_missing_optional_layer_is_read_as_absent(workspace: SimpleNamespace, absent: str) -> None:
    """Absent settings layers are read as absent, and the profile still starts (plan step 2)."""
    layers = {
        "user": (user_settings(workspace), {"permissions": {"ask": [ASK_RULE]}}),
        "project": (project_settings(workspace), {"permissions": {"deny": [DENY_RULE]}}),
        "local": (local_settings(workspace), {"permissions": {"deny": ["mcp__omnigent__sys_os_shell"]}}),
    }
    expected: set[str] = set()
    for scope, (path, data) in layers.items():
        if absent not in ("none", scope):
            write_settings(path, data)
            rules = data["permissions"]
            expected.update(rules.get("ask", []), rules.get("deny", []))
    done = run_night(workspace, "-p", "night check")
    assert done.returncode == 0, done.stderr
    overlay = recorded_overlay(workspace)
    deny = overlay["permissions"]["deny"]
    assert set(deny) == expected
    assert len(deny) == len(set(deny)), "the overlay repeats a deny rule"
    assert overlay["permissions"]["defaultMode"] == "dontAsk"


def test_a_failing_child_is_forwarded_and_the_overlay_is_cleaned(workspace: SimpleNamespace) -> None:
    """The launcher forwards the child's exit status and removes the overlay afterwards (plan step 2)."""
    write_settings(user_settings(workspace), {"permissions": {"ask": [ASK_RULE]}})
    workspace.env["CLAUDE_FAKE_EXIT"] = "7"
    done = run_night(workspace, "-p", "night check")
    assert done.returncode == 7, done.stderr
    overlay_path = launched_argv(workspace)[1]
    assert recorded(workspace, ".lifetime").read_text(encoding="utf-8").startswith("True")
    assert not Path(overlay_path).exists(), "the overlay outlived a failing child"
    assert not Path(overlay_path).parent.exists(), "the private overlay directory outlived a failing child"


def test_the_project_root_is_the_git_worktree_or_the_working_directory(
    workspace: SimpleNamespace, tmp_path: Path
) -> None:
    """Inside Git the launcher reads the worktree's `.claude/settings.json`; the plain-directory runs are the else-branch."""
    repo = tmp_path / "repo"
    (repo / "sub").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(repo)], capture_output=True, timeout=60, check=True)
    write_settings(repo / ".claude" / "settings.json", {"permissions": {"ask": [ASK_RULE]}})
    done = run_night(workspace, "-p", "night check", cwd=repo / "sub")
    assert done.returncode == 0, done.stderr
    assert recorded_overlay(workspace)["permissions"]["deny"] == [ASK_RULE]


def test_the_night_fragment_carries_the_mode_and_no_ask() -> None:
    """The fragment is the night contract: `dontAsk`, no asks; a hand-added ask rule is refused."""
    fragment = json.loads(NIGHT_FRAGMENT.read_text(encoding="utf-8"))
    permissions = fragment["permissions"]
    assert permissions["defaultMode"] == "dontAsk"
    assert "ask" not in permissions
    with pytest.raises(ValueError):
        night.build_overlay({**fragment, "permissions": {**permissions, "ask": [ASK_RULE]}}, [])


def test_install_backup_and_check_cover_night_assets(tmp_path: Path) -> None:
    """Criterion 7: install copies both night assets through the existing backup/check mechanism.

    A rerun changes nothing, --check reports drift and writes nothing, a replaced asset keeps its
    previous contents beside it, and a fresh home is reported missing without being created.
    """
    home = tmp_path / "home"
    home.mkdir()
    env = dict(os.environ)
    env["HOME"] = str(home)
    installed = home / ".claude"

    def installer(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["/bin/bash", str(INSTALLER), *args],
            capture_output=True,
            text=True,
            env=env,
            timeout=120,
            check=False,
        )

    def listing() -> list[str]:
        return sorted(path.name for path in installed.iterdir())

    assert installer().returncode == 0
    fragment_source = NIGHT_FRAGMENT.read_text(encoding="utf-8")
    installed_night_py = (installed / "night.py").read_text(encoding="utf-8")
    installed_fragment = (installed / "night-settings.json").read_text(encoding="utf-8")
    assert installed_night_py == NIGHT_PY.read_text(encoding="utf-8")
    assert installed_fragment == fragment_source
    assert (installed / "statusline.sh").exists(), "the night assets displaced the usual files"
    assert isinstance(json.loads((installed / "settings.json").read_text(encoding="utf-8")), dict)

    assert installer().returncode == 0, "a rerun failed"
    assert not list(installed.glob("night*.bak-*")), "a rerun that changed nothing made a backup"
    in_sync = listing()
    checked = installer("--check")
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert listing() == in_sync, "--check wrote files"

    drifted = '{\n  "permissions": {\n    "defaultMode": "default"\n  }\n}\n'
    (installed / "night-settings.json").write_text(drifted, encoding="utf-8")
    checked = installer("--check")
    assert checked.returncode == 1
    assert "differs" in checked.stdout and "night-settings.json" in checked.stdout
    assert listing() == in_sync, "--check wrote files"

    assert installer().returncode == 0
    backups = list(installed.glob("night-settings.json.bak-*"))
    assert len(backups) == 1 and backups[0].read_text(encoding="utf-8") == drifted, "the previous contents were lost"
    assert (installed / "night-settings.json").read_text(encoding="utf-8") == fragment_source

    fresh = tmp_path / "fresh-home"
    fresh.mkdir()
    env["HOME"] = str(fresh)
    checked = installer("--check")
    assert checked.returncode == 1
    assert "missing" in checked.stdout and "night.py" in checked.stdout and "night-settings.json" in checked.stdout
    assert not (fresh / ".claude").exists(), "the check created the target"


@pytest.mark.parametrize("permissions", [None, [], "dontAsk", 42])
def test_malformed_fragment_permissions_are_refused(workspace: SimpleNamespace, permissions: object) -> None:
    """An installed fragment with a malformed permissions value fails before launch."""
    launcher = workspace.home / "night.py"
    launcher.write_bytes(NIGHT_PY.read_bytes())
    write_settings(launcher.with_name("night-settings.json"), {"permissions": permissions})
    done = subprocess.run(
        [sys.executable, str(launcher)],
        cwd=workspace.project,
        env=workspace.env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert done.returncode == 3, done.stderr
    assert "permissions" in done.stderr and "not an object" in done.stderr
    assert "Traceback" not in done.stderr
    assert not recorded(workspace, ".argv").exists()


@pytest.mark.parametrize("failure", [PermissionError("not executable"), OSError("launch failed")])
def test_child_launch_errors_are_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], failure: OSError
) -> None:
    """OS launch errors use the launcher diagnostic and 127, and clean the overlay."""
    monkeypatch.setattr(night, "project_root", lambda _cwd: tmp_path)
    monkeypatch.setattr(night, "user_settings_path", lambda: tmp_path / "absent.json")
    overlays = []

    def fail_launch(argv: list[str]) -> None:
        overlays.append(Path(argv[2]))
        raise failure

    monkeypatch.setattr(night.subprocess, "run", fail_launch)
    try:
        result = night.main([])
    except OSError as exc:
        pytest.fail(f"launcher must report OS launch errors with exit 127, raised {exc!r}")
    assert result == 127
    assert "night.py:" in capsys.readouterr().err
    assert len(overlays) == 1
    assert not overlays[0].parent.exists()
