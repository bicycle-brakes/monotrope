"""Der Zustandsautomat des Gate-Records — und die Gegenprobe zu jeder Regel.

Drei Befunde aus `docs/governance/fehler-katalog.md` haben dieselbe Ursache:
eine Abnahme, die als *Feld* gefuehrt wurde. F-A-58 traegt Signifikanz
**critical (data)** — drei Contracts standen auf `accepted` gegen eine
zurueckgezogene Abnahme.

Diese Datei prueft die vier Bedingungen aus `quality-gates.md` §6 einzeln, und
zwar jede in ihrer verletzten Form. Ein Test, der nur den gruenen Fall kennt,
belegt nicht, dass die Ableitung ueberhaupt etwas ablehnt.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import gate_record as g  # noqa: E402

VORLAGE = REPO / "templates" / "gate-record.yaml"


def _gueltiger_record() -> dict:
    """Ein Record, der alle vier Bedingungen erfuellt — die Basis jeder Mutation."""
    return {
        "gate": "HG-1",
        "subject": {"kind": "entity-contract", "path": "contracts/x.yaml", "sha256": "abc123"},
        "state": "ACCEPTED",
        "author": "autorin",
        "last_pusher": "autorin",
        "history": [
            {"to": "DRAFT", "at": "2026-01-01T00:00:00Z", "by": "autorin"},
            {"to": "IN_REVIEW", "at": "2026-01-02T00:00:00Z", "by": "autorin"},
        ],
        "signers": [
            {
                "role": "data-architect",
                "handle": "architektin",
                "at": "2026-01-03T00:00:00Z",
                "review_url": "https://example.invalid/pr/1#review-1",
            },
            {
                # HG-1 verlangt Data Architect UND Fachseite. Bis zum 2026-09-08
                # stand hier `data-product-owner` — die Rolle des HG-2 —, und
                # nichts hat es gemerkt, weil die Rollenmenge nie geprueft wurde.
                "role": "fachseite",
                "handle": "eignerin",
                "at": "2026-01-03T12:00:00Z",
                "review_url": "https://example.invalid/pr/1#review-2",
            },
        ],
    }


def test_a_complete_record_is_accepted() -> None:
    """Die Vorbedingung: der gruene Fall ist wirklich gruen.

    Ohne ihn koennte jede Mutation unten aus einem beliebigen anderen Grund rot
    sein, und die Tests behaupteten etwas, das sie nicht messen.
    """
    ok, gruende = g.ist_abgenommen(_gueltiger_record(), "abc123")
    assert ok, f"der vollstaendige Record wird abgelehnt: {gruende}"


# --- Bedingung 1: Rollen, Handles, Review-URLs -----------------------------


def test_a_gate_with_a_missing_required_role_is_not_accepted() -> None:
    """Gesaete Gegenprobe zum Befund vom 2026-09-08 — der Kern von F-A-58.

    Der unabhaengige Review von PR #124 hat einen HG-1-Record mit **einer**
    Unterschrift auf `(True, [])` gebracht: `ist_abgenommen()` prueft, ob
    vorhandene Eintraege vollstaendig ausgefuellt sind, aber nicht, ob die vom
    Gate verlangte Rollenmenge erreicht ist. Ein Tor, das eine von zwei
    Unterschriften durchlaesst, ist kein Tor.
    """
    r = _gueltiger_record()
    r["signers"] = [r["signers"][0]]  # nur die Architektin, die Fachseite fehlt
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "ein HG-1-Record mit nur einer von zwei Pflicht-Rollen gilt als abgenommen"
    assert any("fachseite" in x for x in gruende), gruende


def test_an_invented_role_does_not_replace_a_required_one() -> None:
    """Zwei Eintraege sind nicht zwei Rollen.

    Der zweite Fall aus demselben Review: dieselbe Zahl Unterschriften, aber
    unter frei erfundenen Rollen-Strings. Zaehlt man nur Eintraege, ist das
    ununterscheidbar von einer echten Abnahme.
    """
    r = _gueltiger_record()
    for s_, rolle in zip(r["signers"], ("irgendwas", "irgendwas-anderes"), strict=True):
        s_["role"] = rolle
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "zwei erfundene Rollen gelten als die zwei Pflicht-Rollen des HG-1"
    assert any("kennt die Rolle" in x for x in gruende), gruende


def test_one_human_in_two_roles_is_one_signature() -> None:
    """Das `und` in quality-gates.md meint zwei Menschen, nicht zwei Zeilen."""
    r = _gueltiger_record()
    r["signers"][1]["handle"] = r["signers"][0]["handle"]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "dieselbe Person in beiden Pflicht-Rollen gilt als zwei Unterschriften"
    assert any("mehreren Rollen" in x for x in gruende), gruende


def test_an_unknown_gate_has_no_required_set_and_is_refused() -> None:
    """Ohne Sollmenge ist jede Unterschrift genug — das muss laut sein (RB-G7)."""
    r = _gueltiger_record()
    r["gate"] = "HG-9"
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "ein unbekanntes Gate laesst sich abnehmen"
    assert any("PFLICHT_ROLLEN" in x for x in gruende), gruende


def test_the_required_roles_match_the_governance_table() -> None:
    """`PFLICHT_ROLLEN` und quality-gates.md §4 sagen dasselbe — oder es faellt auf.

    Die Tabelle ist normativ, das Dict ist maschinenlesbar. Zwei Fassungen
    derselben Aussage laufen auseinander, sobald niemand sie gegeneinander
    haelt; dann steht die Regel an der einen Stelle und die Wirkung an der
    anderen.
    """
    tabelle = (REPO / "docs" / "governance" / "quality-gates.md").read_text(encoding="utf-8")
    zeilen = [z for z in tabelle.splitlines() if z.startswith("| **HG-")]
    assert len(zeilen) == len(g.PFLICHT_ROLLEN), (
        f"quality-gates.md nennt {len(zeilen)} Human Gates, PFLICHT_ROLLEN kennt "
        f"{len(g.PFLICHT_ROLLEN)} — eines von beiden ist nicht nachgezogen"
    )
    for zeile in zeilen:
        spalten = [s.strip() for s in zeile.strip("|").split("|")]
        gate = spalten[0].strip("* ")
        wer = spalten[3]
        assert gate in g.PFLICHT_ROLLEN, f"{gate} steht in der Tabelle, aber nicht in PFLICHT_ROLLEN"
        namen = [t.strip() for t in wer.split("**und**")]
        assert len(namen) == len(g.PFLICHT_ROLLEN[gate]), (
            f"{gate}: die Tabelle nennt {len(namen)} Rolle(n) ({wer}), PFLICHT_ROLLEN {len(g.PFLICHT_ROLLEN[gate])}"
        )
        for prosa in g.PFLICHT_ROLLEN[gate].values():
            assert prosa in wer, f"{gate}: PFLICHT_ROLLEN nennt {prosa!r}, die Tabelle nicht: {wer!r}"


def test_a_record_without_signers_is_not_accepted() -> None:
    r = _gueltiger_record()
    r["signers"] = []
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("kein Unterzeichner" in x for x in gruende)


def test_a_signer_without_a_review_url_is_not_accepted() -> None:
    """Eine Zustimmung ohne Fundstelle ist nicht nachlesbar."""
    r = _gueltiger_record()
    del r["signers"][0]["review_url"]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("Review-URL" in x for x in gruende)


def test_a_role_without_a_human_is_not_a_signature() -> None:
    r = _gueltiger_record()
    del r["signers"][1]["handle"]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("Handle" in x for x in gruende)


# --- Bedingung 2: Zustimmung nach der Vorlage ------------------------------


def test_a_signature_before_the_review_started_is_not_accepted() -> None:
    """Eine Zustimmung von vor der Vorlage gilt einem anderen Text — F-A-52."""
    r = _gueltiger_record()
    r["signers"][0]["at"] = "2026-01-01T06:00:00Z"
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("vor der Vorlage" in x for x in gruende)


def test_the_last_review_transition_counts_not_the_first() -> None:
    """Nach Rueckgabe und erneuter Vorlage gilt eine alte Zustimmung nicht mehr."""
    r = _gueltiger_record()
    r["history"] += [
        {"to": "DRAFT", "at": "2026-01-04T00:00:00Z", "by": "autorin"},
        {"to": "IN_REVIEW", "at": "2026-01-05T00:00:00Z", "by": "autorin"},
    ]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok, "beide Zustimmungen liegen vor der zweiten Vorlage und duerfen nicht weitergelten"
    assert any("vor der Vorlage" in x for x in gruende)


def test_a_record_never_submitted_is_not_accepted() -> None:
    r = _gueltiger_record()
    r["history"] = [{"to": "DRAFT", "at": "2026-01-01T00:00:00Z", "by": "autorin"}]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("nie vorgelegt" in x for x in gruende)


# --- Bedingung 3: nicht sich selbst -----------------------------------------


def test_an_author_cannot_sign_their_own_record() -> None:
    r = _gueltiger_record()
    r["signers"][0]["handle"] = "autorin"
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("Schleife" in x for x in gruende)


def test_the_last_pusher_cannot_sign_either() -> None:
    r = _gueltiger_record()
    r["last_pusher"] = "architektin"
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("gepusht" in x for x in gruende)


# --- Bedingung 4: Bindung an den Gegenstand --------------------------------


def test_a_changed_subject_invalidates_the_signature() -> None:
    """Der Kern von RB-M1: was nach der Signatur geaendert wird, ist unsigniert."""
    ok, gruende = g.ist_abgenommen(_gueltiger_record(), "ein-anderer-hash")
    assert not ok and any("geaendert" in x for x in gruende)


def test_a_missing_subject_hash_is_not_accepted() -> None:
    r = _gueltiger_record()
    del r["subject"]["sha256"]
    ok, gruende = g.ist_abgenommen(r, "abc123")
    assert not ok and any("an nichts gebunden" in x for x in gruende)


def test_an_unchecked_binding_is_named_not_silent() -> None:
    """Ohne heutigen Hash wird die vierte Bedingung NICHT geprueft — und das
    wird gesagt. Stillschweigend durchzuwinken waere hier der gefaehrlichste
    Ausgang (RB-G7)."""
    ok, gruende = g.ist_abgenommen(_gueltiger_record(), None)
    assert not ok and any("NICHT geprueft" in x for x in gruende)


# --- Der Zustand wird abgeleitet, nicht gesetzt ----------------------------


def test_accepted_is_derived_not_set() -> None:
    """`state: ACCEPTED` allein genuegt nicht — F-A-58.

    Der Record hier traegt den Zustand und verletzt trotzdem drei Bedingungen.
    Genau so standen drei Contracts der Instanz auf `accepted`.
    """
    nackt = {"gate": "HG-1", "state": "ACCEPTED", "subject": {}, "history": [], "signers": []}
    ok, gruende = g.ist_abgenommen(nackt, "abc123")
    assert not ok
    assert len(gruende) >= 3, f"nur {len(gruende)} Gruende — die Ableitung prueft zu wenig: {gruende}"


@pytest.mark.parametrize(
    "von,nach",
    [("DRAFT", "ACCEPTED"), ("ACCEPTED", "ACCEPTED"), ("WITHDRAWN", "ACCEPTED"), ("DRAFT", "WITHDRAWN")],
)
def test_an_unknown_transition_is_refused(von: str, nach: str) -> None:
    with pytest.raises(g.UngueltigerUebergang):
        g.pruefe_uebergang(von, nach)


@pytest.mark.parametrize(
    "von,nach",
    [("DRAFT", "IN_REVIEW"), ("IN_REVIEW", "ACCEPTED"), ("ACCEPTED", "WITHDRAWN"), ("WITHDRAWN", "DRAFT")],
)
def test_the_allowed_transitions_pass(von: str, nach: str) -> None:
    g.pruefe_uebergang(von, nach)


def test_every_state_can_be_left() -> None:
    """Eine Sackgasse im Automaten waere ein Zustand, aus dem niemand herauskommt."""
    for zustand in g.ZUSTAENDE:
        assert g.UEBERGAENGE.get(zustand), f"{zustand} hat keinen Ausgang"


# --- Die Vorlage -----------------------------------------------------------


def test_the_template_is_a_draft_not_an_example_of_acceptance() -> None:
    """Eine Vorlage, die ACCEPTED vormacht, lehrt den Fehler."""
    record = yaml.safe_load(VORLAGE.read_text(encoding="utf-8"))
    assert record["state"] == "DRAFT"
    ok, _ = g.ist_abgenommen(record, record["subject"]["sha256"])
    assert not ok, "die Vorlage gilt als abgenommen — dann ist sie ein Freifahrtschein"


def test_the_template_carries_every_required_field() -> None:
    record = yaml.safe_load(VORLAGE.read_text(encoding="utf-8"))
    fehlend = sorted(g.pflichtfelder() - set(record))
    assert not fehlend, f"die Vorlage laesst Pflichtfelder aus: {fehlend}"


def test_a_record_without_a_required_field_is_caught() -> None:
    """Gegenprobe zum Test darueber."""
    record = yaml.safe_load(VORLAGE.read_text(encoding="utf-8"))
    verstuemmelt = copy.deepcopy(record)
    del verstuemmelt["signers"]
    assert sorted(g.pflichtfelder() - set(verstuemmelt)) == ["signers"]
