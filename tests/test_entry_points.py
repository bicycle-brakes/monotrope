"""Der Instruktions-Einstieg: eine Grenze, ein Import, ein README-Verbot (RB-S1).

Der Regelwerk-Text nennt diese drei Erzwinger beim Namen; sie pruefen hier
denselben Vertrag wie im Ursprungs-Repo, gegen den hiesigen Bestand: die
Instruktionsdatei dieses Repos ist CLAUDE.md, ihr Quelldokument AGENTS.md —
der Verweis steht als Markdown-Link, das ist hier die Importform.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLAUDE_MD = REPO / "CLAUDE.md"
AGENTS_MD = REPO / "AGENTS.md"
BUDGET = 200


def test_claude_md_imports_agents_md_and_stays_short() -> None:
    """Der Einstieg delegiert auf AGENTS.md und bleibt selbst unter dem Budget."""
    text = CLAUDE_MD.read_text(encoding="utf-8")
    zeilen = text.count("\n")
    assert zeilen <= BUDGET, f"CLAUDE.md hat {zeilen} Zeilen — das Budget liegt bei {BUDGET}"
    assert "AGENTS.md" in text, (
        "CLAUDE.md verweist nicht auf AGENTS.md — der Einstieg wuergt die Instruktion ab, statt sie zu importieren."
    )


def test_instruction_files_are_under_200_lines() -> None:
    """Das Budget gilt je Instruktionsdatei, nicht im Mittel."""
    for pfad in (CLAUDE_MD, AGENTS_MD):
        zeilen = pfad.read_text(encoding="utf-8").count("\n")
        assert zeilen <= BUDGET, f"{pfad.name} hat {zeilen} Zeilen — das Budget liegt bei {BUDGET}"


def test_readme_is_never_imported() -> None:
    """Das README ist Besuchertext, kein Instruktionsdokument — nie importieren."""
    for pfad in (CLAUDE_MD, AGENTS_MD):
        assert "README" not in pfad.read_text(encoding="utf-8"), (
            f"{pfad.name} zieht das README als Instruktion herein — das README ist fuer Besucher, nicht fuer Agents."
        )
