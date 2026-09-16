"""Der Gate-Record — ein Zustandsautomat, aus dem `accepted` ABGELEITET wird.

`docs/governance/quality-gates.md` §6 sagt es in einem Satz: *ein Gate-Record ist
eine Datei, kein Feld.* Diese Datei macht daraus Code.

**Warum das wichtig ist, in Zahlen.** Im Fehler-Katalog stehen drei Befunde, die
alle dieselbe Ursache haben — eine Abnahme, die als *Feld* gefuehrt wurde:

  F-A-52  Eine Signatur wurde zurueckgezogen, weil sich die Schlussfolgerung
          aenderte — der Name stand gegen Text, den die Person nie las.
  F-A-53  `accepted_unsigned` kollabiert zwei Zustaende; der Normalfall hat
          keinen Namen.
  F-A-58  Drei Contracts stehen auf `accepted` gegen eine zurueckgezogene
          Abnahme. Signifikanz: **critical (data)**.

Ein Feld kann man setzen. Ein abgeleiteter Zustand nicht — er ist wahr oder er
ist es nicht, und die Begruendung faellt beim Rechnen mit ab.

**Deshalb gibt es hier keinen Setter fuer `ACCEPTED`.** `ist_abgenommen()`
liefert ein Paar aus Urteil und Begruendungen; wer nur das Urteil nimmt,
verliert nichts als die Erklaerung.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

# Die vier Zustaende aus quality-gates.md §6.
ZUSTAENDE: tuple[str, ...] = ("DRAFT", "IN_REVIEW", "ACCEPTED", "WITHDRAWN")

# Erlaubte Kanten. Was hier fehlt, ist verboten — nicht "ungewoehnlich".
#
# `ACCEPTED -> ACCEPTED` fehlt mit Absicht: eine zweite Abnahme desselben
# Records ist keine Bestaetigung, sondern verdeckt, dass sich der Gegenstand
# geaendert hat. Wer erneut abnehmen will, geht ueber WITHDRAWN.
UEBERGAENGE: dict[str, tuple[str, ...]] = {
    "DRAFT": ("IN_REVIEW",),
    "IN_REVIEW": ("DRAFT", "ACCEPTED", "WITHDRAWN"),
    "ACCEPTED": ("WITHDRAWN",),
    "WITHDRAWN": ("DRAFT",),
}


# Welche Rollen ein Gate VERLANGT. Aus der Tabelle in `quality-gates.md` §4,
# Spalte "Wer unterschreibt" — dort normativ, hier maschinenlesbar. Der Prosa-Name
# steht mit dabei, damit `test_the_required_roles_match_the_governance_table` beide
# Seiten gegeneinander halten kann: eine Rolle, die nur an einer der beiden Stellen
# steht, ist ein Befund, keine Kleinigkeit.
#
# **Warum es diese Menge ueberhaupt gibt.** Bis zum 2026-09-08 prueft
# `ist_abgenommen()` nur, dass *vorhandene* Eintraege vollstaendig ausgefuellt
# sind — nicht, dass die verlangte Rollenmenge erreicht ist. Ein HG-1-Record mit
# einer einzigen Unterschrift kam damit als abgenommen durch, und zwei Eintraege
# unter frei erfundenen Rollen-Strings ebenso. Genau das ist der Fehler, den
# F-A-58 ("critical (data)") beschreibt: drei Contracts standen auf `accepted`
# gegen eine Abnahme, die keine war.
PFLICHT_ROLLEN: dict[str, dict[str, str]] = {
    "HG-1": {"data-architect": "Data Architect", "fachseite": "Fachseite"},
    "HG-2": {"data-product-owner": "Data Product Owner (Consumer)", "data-architect": "Data Architect"},
    "HG-3": {"produktverantwortlicher": "Produktverantwortlicher", "data-architect": "Data Architect"},
    "HG-4": {"operations-owner": "Operations Owner"},
}


class UngueltigerUebergang(ValueError):
    """Ein Uebergang, den der Automat nicht kennt."""


def pruefe_uebergang(von: str, nach: str) -> None:
    """Wirft, wenn die Kante nicht existiert. Kein stilles Durchlassen."""
    if von not in ZUSTAENDE:
        raise UngueltigerUebergang(f"unbekannter Ausgangszustand: {von!r}")
    if nach not in ZUSTAENDE:
        raise UngueltigerUebergang(f"unbekannter Zielzustand: {nach!r}")
    if nach not in UEBERGAENGE[von]:
        raise UngueltigerUebergang(
            f"{von} -> {nach} ist kein erlaubter Uebergang. Erlaubt ab {von}: {UEBERGAENGE[von]}"
        )


def _zeit(wert: Any) -> dt.datetime | None:
    if isinstance(wert, dt.datetime):
        return wert
    if isinstance(wert, str):
        try:
            return dt.datetime.fromisoformat(wert.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def _in_review_seit(record: dict) -> dt.datetime | None:
    """Wann ging der Record zuletzt nach IN_REVIEW?

    Der **letzte** Uebergang zaehlt, nicht der erste: nach einer Rueckgabe nach
    DRAFT und erneuter Vorlage darf eine alte Zustimmung nicht weitergelten.
    """
    zeiten = [
        _zeit(e.get("at")) for e in record.get("history", []) if isinstance(e, dict) and e.get("to") == "IN_REVIEW"
    ]
    vorhanden = [z for z in zeiten if z is not None]
    return max(vorhanden) if vorhanden else None


def ist_abgenommen(record: dict, heutiger_hash: str | None = None) -> tuple[bool, list[str]]:
    """Leitet ab, ob dieser Record abgenommen ist — mit Begruendung je Bedingung.

    Die vier Bedingungen stehen in `quality-gates.md` §6. Jede liefert bei
    Verletzung ihren eigenen Satz; eine Liste von Gruenden ist brauchbar, ein
    nacktes `False` nicht.

    `heutiger_hash` ist der Hash des Gegenstands **jetzt**. Fehlt er, wird die
    vierte Bedingung nicht geprueft und das ausdruecklich gemeldet — Schweigen
    waere hier die gefaehrlichste Antwort (RB-G7).
    """
    gruende: list[str] = []

    if record.get("state") != "ACCEPTED":
        gruende.append(f"state ist {record.get('state')!r}, nicht ACCEPTED")

    # 1 · alle Pflicht-Rollen liegen vor, jede mit Review-URL
    signers = record.get("signers") or []
    pflicht = [s for s in signers if isinstance(s, dict)]
    if not pflicht:
        gruende.append("kein Unterzeichner eingetragen")

    # Die Rollenmenge des Gates — nicht nur "irgendjemand hat unterschrieben".
    gate = record.get("gate")
    verlangt = PFLICHT_ROLLEN.get(gate)
    if verlangt is None:
        gruende.append(
            f"gate {gate!r} kennt PFLICHT_ROLLEN nicht — ohne Sollmenge ist jede Unterschrift genug, "
            f"und das ist keine Abnahme. Bekannt: {', '.join(sorted(PFLICHT_ROLLEN))}"
        )
    else:
        unterschrieben = {s.get("role") for s in pflicht if s.get("role")}
        fehlend = sorted(set(verlangt) - unterschrieben)
        if fehlend:
            gruende.append(f"{gate} verlangt {', '.join(sorted(verlangt))} — es fehlt: {', '.join(fehlend)}")
        fremd = sorted(unterschrieben - set(verlangt))
        if fremd:
            gruende.append(
                f"{gate} kennt die Rolle(n) {', '.join(fremd)} nicht — eine erfundene Rolle ersetzt keine verlangte"
            )
        # Zwei Rollen in einer Hand sind eine Unterschrift, nicht zwei.
        handles = [s.get("handle") for s in pflicht if s.get("handle")]
        doppelt = sorted({h for h in handles if handles.count(h) > 1})
        if doppelt:
            gruende.append(
                f"{', '.join(doppelt)} unterschreibt in mehreren Rollen — "
                "das 'und' in quality-gates.md meint zwei Menschen, nicht zwei Zeilen"
            )

    for s in pflicht:
        if not s.get("role"):
            gruende.append(f"Unterzeichner ohne Rolle: {s}")
        if not s.get("handle"):
            gruende.append(f"Rolle {s.get('role')!r} ohne Handle — eine Rolle unterschreibt nicht, ein Mensch tut es")
        if not s.get("review_url"):
            gruende.append(f"{s.get('handle')!r} ohne Review-URL — dann ist die Zustimmung nicht nachlesbar")

    # 2 · die Zustimmung ist NACH dem Uebergang nach IN_REVIEW datiert
    seit = _in_review_seit(record)
    if seit is None:
        gruende.append("kein Uebergang nach IN_REVIEW in der history — der Record wurde nie vorgelegt")
    else:
        for s in pflicht:
            wann = _zeit(s.get("at"))
            if wann is None:
                gruende.append(f"{s.get('handle')!r} ohne lesbaren Zeitpunkt")
            elif wann < seit:
                gruende.append(
                    f"{s.get('handle')!r} hat vor der Vorlage zugestimmt "
                    f"({wann.isoformat()} < {seit.isoformat()}) — das ist eine Zustimmung zu einem anderen Text"
                )

    # 3 · der Zustimmende ist weder Autor noch letzter Pusher
    autor = record.get("author")
    pusher = record.get("last_pusher")
    for s in pflicht:
        handle = s.get("handle")
        if handle and handle == autor:
            gruende.append(f"{handle!r} ist Autor und Unterzeichner — das ist keine Abnahme, das ist eine Schleife")
        if handle and handle == pusher:
            gruende.append(f"{handle!r} hat zuletzt gepusht und unterschreibt — dieselbe Schleife")

    # 4 · subject.sha256 entspricht dem heutigen Hash
    subject = record.get("subject") or {}
    signiert = subject.get("sha256")
    if not signiert:
        gruende.append("subject.sha256 fehlt — dann ist die Unterschrift an nichts gebunden")
    elif heutiger_hash is None:
        gruende.append("kein heutiger Hash uebergeben — die Bindung an den Gegenstand wurde NICHT geprueft")
    elif signiert != heutiger_hash:
        gruende.append(
            f"der Gegenstand hat sich geaendert: signiert {signiert}, heute {heutiger_hash}. "
            "Was nach der Signatur geaendert wird, ist wieder unsigniert (RB-M1)"
        )

    return (not gruende), gruende


def pflichtfelder() -> frozenset[str]:
    """Was ein Record traegt — die Liste, gegen die die Vorlage geprueft wird."""
    return frozenset({"gate", "subject", "state", "history", "signers"})
