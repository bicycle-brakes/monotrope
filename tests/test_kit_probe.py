"""The kit probe's own pytest launch stays serial (bead coding-harness-bxxt.13).

The targeted check runs the kit probe outside the verify admission; its process count is bounded
only because the probe starts pytest without an xdist worker option. The probe's subprocess is
doubled here, so no second pytest session starts.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
KIT = REPO_ROOT / "scripts" / "kit"

sys.path.insert(0, str(KIT))
import probe  # noqa: E402


def test_probe_pytest_remains_serial(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Spec criterion 2. Planted fault: the probe command contains an xdist worker option."""
    launched: list[list[str]] = []

    def fake_run(command, *_args, **_kwargs):
        launched.append([str(part) for part in command])
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(probe.subprocess, "run", fake_run)
    assert probe._faelle(tmp_path) == {}, "no report was written, so no case is read"
    pytest_runs = [command for command in launched if command[1:3] == ["-m", "pytest"]]
    assert len(pytest_runs) == 1, launched
    (command,) = pytest_runs
    assert "-n" not in command, command
    assert not any(part.startswith("-n") and part != "-n" for part in command), command
    assert not any(part.startswith("--numprocesses") for part in command), command
