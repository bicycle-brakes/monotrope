#!/usr/bin/env python3
"""Launch Claude Code in the night profile: sourced asks become denies, and nothing waits for a person.

An unattended session starts Claude Code through this launcher
(`python3 ~/.claude/night.py`, followed by the arguments a normal `claude` call
would take; plans/changes/night-stall-guard). It reads the explicit permission
rules of the supported settings scopes — the user settings under
`$CLAUDE_CONFIG_DIR` (else `~/.claude`), the current Git worktree's
`.claude/settings.json` and the optional `.claude/settings.local.json` beside
it; outside Git the working directory is the project root — and writes a
private overlay that repeats their denies and turns every sourced ask rule into
a deny. The overlay carries nothing else: inherited non-permission settings
stay in their native layers, and Claude Code still reads them there. It then
starts `claude --settings <overlay> --permission-mode dontAsk` with the
remaining arguments as an argv list, waits for the child, removes the overlay
and forwards the child's exit status.

An unattended session cannot answer a permission question, so the profile
refuses instead of waiting. The launch stops before `claude` runs when a
present settings file cannot be read or parsed — a half-read profile could
silently lose a brake — and arguments that would replace the profile
(`--settings`, `--permission-mode`, `--dangerously-skip-permissions`, in
`--flag value` and `--flag=value` form) are refused the same way. No source
setting is ever rewritten.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CLAUDE = "claude"
LOCAL_SETTINGS = ".claude/settings.local.json"
PROJECT_SETTINGS = ".claude/settings.json"
USER_SETTINGS = "settings.json"
FRAGMENT_NAME = "night-settings.json"

# Arguments that would silently replace or bypass the night profile.
PROFILE_FLAGS = ("--settings", "--permission-mode", "--dangerously-skip-permissions")


class SettingsError(Exception):
    """A present settings file cannot be read or parsed; the profile would be built on a guess."""


def user_settings_path() -> Path:
    """The user settings file: under `$CLAUDE_CONFIG_DIR` when set, else `~/.claude`."""
    configured = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(configured) / USER_SETTINGS if configured else Path.home() / ".claude" / USER_SETTINGS


def project_root(cwd: Path) -> Path:
    """The current Git worktree's root, else the working directory itself."""
    try:
        done = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return cwd
    top = done.stdout.strip() if done.returncode == 0 else ""
    return Path(top) if top else cwd


def load_settings(path: Path) -> dict | None:
    """A present settings file, parsed and shape-checked; None when absent; SettingsError on unreadable or malformed."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise SettingsError(f"cannot read {path}: {exc}") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SettingsError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SettingsError(f"{path} is not a JSON object")
    permissions = data.get("permissions")
    if permissions is not None and not isinstance(permissions, dict):
        raise SettingsError(f"{path}: 'permissions' is not an object")
    if isinstance(permissions, dict):
        for kind in ("ask", "deny"):
            rules = permissions.get(kind)
            if rules is not None and (not isinstance(rules, list) or not all(isinstance(r, str) for r in rules)):
                raise SettingsError(f"{path}: 'permissions.{kind}' is not a list of strings")
    return data


def build_overlay(fragment: dict, layers: list[dict]) -> dict:
    """The night overlay: the fragment, plus every existing deny and every sourced ask as a deny.

    Sourced asks are never carried as asks and no blanket allow is added; the deny order follows the
    layers, each layer's denies before its asks, duplicates taken once.
    """
    overlay = json.loads(json.dumps(fragment))
    permissions = overlay.setdefault("permissions", {})
    asks = permissions.get("ask")
    if asks:
        raise ValueError(f"the night settings fragment must not carry ask rules: {asks}")
    permissions.pop("ask", None)
    deny: list[str] = []
    for layer in layers:
        sourced = layer.get("permissions") or {}
        for kind in ("deny", "ask"):
            for rule in sourced.get(kind) or []:
                if rule not in deny:
                    deny.append(rule)
    permissions["deny"] = deny
    return overlay


def profile_conflict(argv: list[str]) -> str | None:
    """The first argument that would replace or bypass the profile, or None."""
    for arg in argv:
        for flag in PROFILE_FLAGS:
            if arg == flag or arg.startswith(flag + "="):
                return arg
    return None


def main(argv: list[str] | None = None) -> int:
    """Build the overlay and run Claude Code with it; the child's exit status, or the launcher's own refusal."""
    argv = list(sys.argv[1:] if argv is None else argv)
    conflict = profile_conflict(argv)
    if conflict is not None:
        print(
            f"night.py refuses {conflict}: the night profile fixes its own settings, mode and bypass flags",
            file=sys.stderr,
        )
        return 2

    root = project_root(Path.cwd())
    layer_paths = [user_settings_path(), root / PROJECT_SETTINGS, root / LOCAL_SETTINGS]
    try:
        layers = [data for path in layer_paths if (data := load_settings(path)) is not None]
    except SettingsError as exc:
        print(f"night.py: {exc}", file=sys.stderr)
        return 3

    fragment_path = Path(__file__).resolve().with_name(FRAGMENT_NAME)
    try:
        fragment = json.loads(fragment_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"night.py: cannot read the night settings fragment {fragment_path}: {exc}", file=sys.stderr)
        return 3
    except json.JSONDecodeError as exc:
        print(f"night.py: the night settings fragment {fragment_path} is not valid JSON: {exc}", file=sys.stderr)
        return 3
    if not isinstance(fragment, dict):
        print(f"night.py: the night settings fragment {fragment_path} is not a JSON object", file=sys.stderr)
        return 3
    try:
        overlay = build_overlay(fragment, layers)
    except ValueError as exc:
        print(f"night.py: {exc}", file=sys.stderr)
        return 3

    overlay_dir = Path(tempfile.mkdtemp(prefix="claude-night-"))
    try:
        overlay_path = overlay_dir / "settings.json"
        overlay_path.write_text(json.dumps(overlay, indent=2) + "\n", encoding="utf-8")
        try:
            done = subprocess.run([CLAUDE, "--settings", str(overlay_path), "--permission-mode", "dontAsk", *argv])
        except FileNotFoundError:
            print("night.py: 'claude' was not found on the PATH", file=sys.stderr)
            return 127
        return done.returncode if done.returncode >= 0 else 128 - done.returncode
    finally:
        shutil.rmtree(overlay_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
