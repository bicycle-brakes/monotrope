"""Shared preparation of the neutral-path extension for every Pi launch."""

from pathlib import Path

NEUTRAL_SOURCE = Path(__file__).resolve().parent / "stage2_pi_neutral_paths.mjs"


def install_neutral(directory: Path, runner, *, source: Path | None = None) -> Path:
    """Copy the same source, refusing by the invoking runner's type before dispatch."""
    source = NEUTRAL_SOURCE if source is None else source
    copy = directory / "neutral-paths.mjs"
    try:
        copy.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    except OSError as error:
        raise runner.Refused(f"the neutral-path extension {source.name} could not be copied: {error}") from error
    return copy
