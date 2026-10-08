"""Die Ventil-Liste selbst behauptet, nicht leer zu sein (RB-G7).

Ein Gate ueber einer leeren Menge ist gruen, ohne etwas geprueft zu haben.
Diese Datei existiert seit dem 2026-09-19 (2ee-Triage, Welle 2) — im
Ursprungs-Repo war sie Teil des Bestands; hier ist sie der erste, kleine
Erzwinger, den RB-G7 nennen darf.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from ramp_valves import REGEL_VENTILE, valves  # noqa: E402


def test_the_valve_list_is_not_empty() -> None:
    """Eine leere Ventil-Liste waere ein stillschweigend aufgehobener Vorbehalt."""
    ventile = valves()
    namen = {v.name for v in ventile}
    missing = sorted(set(REGEL_VENTILE) - namen)
    assert not missing, f"rule valves missing from valves(): {missing} — was the list emptied?"
    assert len(namen) >= 10, f"nur {len(namen)} Ventile — die Regel-Ventile wurden entfernt?"
