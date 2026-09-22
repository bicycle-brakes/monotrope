"""Der Instruktions-Einstieg: eine Datei, eine Grenze, ein README-Verbot (RB-S1).

Der Regelwerk-Text nennt diese Erzwinger beim Namen; sie pruefen hier
denselben Vertrag wie im Ursprungs-Repo, gegen den hiesigen Bestand: die eine
Instruktionsdatei dieses Repos ist AGENTS.md. Eine CLAUDE.md gibt es seit dem
2026-09-22 nicht mehr — Claude Code liest AGENTS.md seit 2.1.277 selbst, sobald
keine CLAUDE.md im Baum liegt. Kaeme eine zurueck, wuerde sie AGENTS.md
verdraengen (nur CLAUDE.md wird dann gelesen) und die zweite Quelle waere da.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLAUDE_MD = REPO / "CLAUDE.md"
AGENTS_MD = REPO / "AGENTS.md"
BUDGET = 200


def test_agents_md_is_the_only_instruction_file() -> None:
    """Keine CLAUDE.md neben AGENTS.md — sonst liest Claude Code nur die CLAUDE.md."""
    assert AGENTS_MD.is_file(), "AGENTS.md fehlt — der Einstieg fuer jeden Harness"
    assert not CLAUDE_MD.exists(), (
        "CLAUDE.md liegt wieder im Baum — sie verdraengt AGENTS.md fuer Claude Code und ist die zweite Quelle."
    )


def test_instruction_file_is_under_200_lines() -> None:
    """Das Budget gilt fuer die Instruktionsdatei, nicht fuer die Doku dahinter."""
    zeilen = AGENTS_MD.read_text(encoding="utf-8").count("\n")
    assert zeilen <= BUDGET, f"AGENTS.md hat {zeilen} Zeilen — das Budget liegt bei {BUDGET}"


def test_readme_is_never_imported() -> None:
    """Das README ist Besuchertext, kein Instruktionsdokument — nie importieren."""
    assert "README" not in AGENTS_MD.read_text(encoding="utf-8"), (
        "AGENTS.md zieht das README als Instruktion herein — das README ist fuer Besucher, nicht fuer Agents."
    )
