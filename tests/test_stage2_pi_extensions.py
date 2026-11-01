"""Every Pi builder refuses a failed neutral-extension copy before dispatch."""

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import stage2  # noqa: E402
import stage2_availability  # noqa: E402
import stage2_session  # noqa: E402
from stage2_research_run import Run  # noqa: E402


def test_shared_neutral_copy_preserves_source(tmp_path):
    """Every launch receives the repository extension's complete source."""
    try:
        import stage2_pi_extensions
    except ImportError:
        pytest.fail("no shared neutral-path copy helper")

    copied = stage2_pi_extensions.install_neutral(tmp_path, stage2)
    assert copied == tmp_path / "neutral-paths.mjs"
    assert copied.read_bytes() == stage2_pi_extensions.NEUTRAL_SOURCE.read_bytes()


@pytest.mark.parametrize("builder", ["review", "probe", "research", "session"])
@pytest.mark.parametrize("failure", [FileNotFoundError("missing source"), PermissionError("unreadable source")])
def test_neutral_copy_failure_is_shared_named_refusal(tmp_path, monkeypatch, builder, failure):
    """Fault: a builder bypasses the shared source reader or leaks an OSError."""
    original = Path.read_text

    def read(path, *args, **kwargs):
        if path.name == "stage2_pi_neutral_paths.mjs":
            raise failure
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read)

    def no_dispatch(*_a, **_kw):
        pytest.fail("dispatch reached after copy failure")

    monkeypatch.setattr(stage2, "launch", no_dispatch)
    monkeypatch.setattr(stage2, "dispatch_go", no_dispatch)
    monkeypatch.setattr(stage2_availability, "_checked_probe", lambda *_a, **_kw: None)
    monkeypatch.setattr(stage2_availability, "install_measured_models", lambda *_a, **_kw: [])
    with pytest.raises(stage2.Refused, match="neutral-path extension stage2_pi_neutral_paths.mjs") as caught:
        if builder == "review":
            stage2.run_reviewer(SimpleNamespace(root=tmp_path), "model", "prompt", "key")
        elif builder == "probe":
            stage2_availability.probe_go(stage2, tmp_path, "demo", "model", "key", [])
        elif builder == "research":
            run = Run.__new__(Run)
            run.root, run.selection, run.runner, run.change, run.key = tmp_path, {}, stage2, "demo", None
            run.pi_command({"model": "model", "tools": "repository"}, "prompt", tmp_path)
        else:
            install = getattr(stage2_session, "install_neutral", None)
            if install is None:
                pytest.fail("the session builder has no neutral-path copy")
            install(tmp_path, stage2)
    assert caught.value.__cause__ is failure
